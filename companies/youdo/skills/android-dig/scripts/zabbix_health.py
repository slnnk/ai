#!/usr/bin/env python3
"""Collect Zabbix errors, trigger events, and metric summaries for an inventory snapshot."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Pattern, Sequence, Tuple

from zabbix_hosts import (
    DEFAULT_ENDPOINT,
    DEFAULT_ENV_FILE,
    DEFAULT_GROUP,
    DEFAULT_HOST,
    DEFAULT_TOKEN_ENV,
    ScriptError,
    get_token,
    make_opener,
    rpc_call,
    validate_endpoint,
)


SEVERITIES = {
    "0": "not_classified",
    "1": "information",
    "2": "warning",
    "3": "average",
    "4": "high",
    "5": "disaster",
}

CORE_EXACT_KEYS = {
    "agent.ping",
    "system.cpu.load[percpu,avg1]",
    "system.cpu.util[,idle]",
    "system.cpu.util[,iowait]",
    "vm.memory.size[pused]",
    "vfs.fs.size[/,free]",
    "system.uptime",
}

CORE_KEY_PATTERNS: Sequence[Pattern[str]] = (
    re.compile(r"^adb_dev\.status\[[^]]+\]$"),
    re.compile(r"^net\.if\.(?:in|out)\[[^,]+,(?:errors|dropped)\]$"),
)


def parse_time(raw: str, label: str) -> int:
    value = raw.strip()
    if value.isdigit():
        epoch = int(value)
        if epoch <= 0:
            raise ScriptError(f"{label} epoch must be positive")
        return epoch
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ScriptError(f"{label} must be epoch seconds or ISO-8601 with timezone") from exc
    if parsed.tzinfo is None:
        raise ScriptError(f"{label} ISO-8601 value must include a timezone")
    return int(parsed.timestamp())


def utc_iso(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat(timespec="seconds")


def load_inventory(path: str) -> Dict[str, Any]:
    try:
        if path == "-":
            document = json.load(sys.stdin)
        else:
            document = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScriptError(f"cannot read inventory JSON from {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise ScriptError("inventory must be a JSON object from zabbix_hosts.py")
    return document


def validate_inventory(
    inventory: Dict[str, Any], expected_group: str, max_age_seconds: int
) -> Tuple[List[Dict[str, Any]], str, datetime]:
    source = inventory.get("source")
    hosts = inventory.get("hosts")
    if inventory.get("schema_version") != 1 or not isinstance(source, dict) or not isinstance(hosts, list):
        raise ScriptError("inventory schema is not a supported zabbix_hosts.py document")
    group = source.get("group")
    if not isinstance(group, dict) or group.get("name") != expected_group:
        actual = group.get("name") if isinstance(group, dict) else None
        raise ScriptError(f"inventory group mismatch: expected {expected_group}, got {actual}")
    if source.get("host_status_filter") != "Enabled":
        raise ScriptError("inventory is not restricted to Enabled hosts")
    fetched_raw = source.get("fetched_at_utc")
    if not isinstance(fetched_raw, str):
        raise ScriptError("inventory has no fetched_at_utc timestamp")
    try:
        fetched_at = datetime.fromisoformat(fetched_raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ScriptError("inventory fetched_at_utc is invalid") from exc
    if fetched_at.tzinfo is None:
        raise ScriptError("inventory fetched_at_utc must include a timezone")
    age = (datetime.now(timezone.utc) - fetched_at.astimezone(timezone.utc)).total_seconds()
    if age < -300:
        raise ScriptError("inventory timestamp is more than five minutes in the future")
    if max_age_seconds and age > max_age_seconds:
        raise ScriptError(
            f"inventory is stale ({int(age)} seconds old; maximum {max_age_seconds}); refresh zabbix_hosts.py"
        )
    endpoint = source.get("endpoint")
    if not isinstance(endpoint, str):
        raise ScriptError("inventory has no Zabbix endpoint")

    normalized = []
    seen_ids = set()
    for host in hosts:
        if not isinstance(host, dict) or host.get("enabled") is not True:
            raise ScriptError("inventory contains a host that is not Enabled")
        hostid = str(host.get("hostid") or "")
        technical_name = host.get("technical_name")
        if not hostid.isdigit() or not isinstance(technical_name, str) or not technical_name:
            raise ScriptError("inventory host is missing a numeric hostid or technical_name")
        if hostid in seen_ids:
            raise ScriptError(f"inventory contains duplicate hostid {hostid}")
        seen_ids.add(hostid)
        normalized.append(host)
    if not normalized:
        raise ScriptError("inventory contains no Enabled hosts")
    return normalized, endpoint, fetched_at


def bool_string(value: Any) -> bool:
    return str(value or "0") == "1"


def zero_is_none(value: Any) -> Optional[str]:
    normalized = str(value or "0")
    return None if normalized == "0" else normalized


def normalize_hosts(raw_hosts: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_hosts, list):
        return []
    return [
        {
            "hostid": host.get("hostid"),
            "technical_name": host.get("host"),
            "visible_name": host.get("name"),
        }
        for host in raw_hosts
        if isinstance(host, dict)
    ]


def normalize_event(event: Dict[str, Any], problem_severity: Dict[str, str]) -> Dict[str, Any]:
    value = str(event.get("value", ""))
    severity = str(event.get("severity", "0"))
    objectid = str(event.get("objectid", ""))
    effective_severity = severity if value == "1" else problem_severity.get(objectid, severity)
    clock = int(event.get("clock") or 0)
    return {
        "eventid": event.get("eventid"),
        "objectid": event.get("objectid"),
        "state": "problem" if value == "1" else "recovery",
        "clock": clock,
        "time_utc": utc_iso(clock),
        "name": event.get("name"),
        "severity": int(effective_severity or 0),
        "severity_name": SEVERITIES.get(effective_severity, effective_severity),
        "acknowledged": bool_string(event.get("acknowledged")),
        "related_recovery_eventid": zero_is_none(event.get("r_eventid")),
        "hosts": normalize_hosts(event.get("hosts")),
    }


def normalize_problem(problem: Dict[str, Any]) -> Dict[str, Any]:
    clock = int(problem.get("clock") or 0)
    recovery_clock = int(problem.get("r_clock") or 0)
    severity = str(problem.get("severity", "0"))
    return {
        "eventid": problem.get("eventid"),
        "objectid": problem.get("objectid"),
        "clock": clock,
        "time_utc": utc_iso(clock),
        "recovery_eventid": zero_is_none(problem.get("r_eventid")),
        "recovery_clock": recovery_clock or None,
        "recovery_time_utc": utc_iso(recovery_clock) if recovery_clock else None,
        "name": problem.get("name"),
        "severity": int(severity or 0),
        "severity_name": SEVERITIES.get(severity, severity),
        "acknowledged": bool_string(problem.get("acknowledged")),
        "suppressed": bool_string(problem.get("suppressed")),
        "operational_data": problem.get("opdata") or None,
        "hosts": normalize_hosts(problem.get("hosts")),
    }


def compile_extra_patterns(raw_patterns: Iterable[str]) -> List[Pattern[str]]:
    compiled = []
    for raw in raw_patterns:
        try:
            compiled.append(re.compile(raw))
        except re.error as exc:
            raise ScriptError(f"invalid --include-key-regex {raw!r}: {exc}") from exc
    return compiled


def is_metric_item(item: Dict[str, Any], extra_patterns: Sequence[Pattern[str]], include_loopback: bool) -> bool:
    key = str(item.get("key_") or "")
    if key in CORE_EXACT_KEYS:
        return True
    if not include_loopback and re.match(r"^net\.if\.(?:in|out)\[lo,", key):
        return False
    return any(pattern.search(key) for pattern in (*CORE_KEY_PATTERNS, *extra_patterns))


def normalize_item(item: Dict[str, Any], host_names: Dict[str, str]) -> Dict[str, Any]:
    lastclock = int(item.get("lastclock") or 0)
    return {
        "itemid": item.get("itemid"),
        "hostid": item.get("hostid"),
        "host": host_names.get(str(item.get("hostid"))),
        "name": item.get("name"),
        "key": item.get("key_"),
        "value_type": int(item.get("value_type") or 0),
        "units": item.get("units") or None,
        "state": "not_supported" if str(item.get("state", "0")) == "1" else "supported",
        "error": item.get("error") or None,
        "lastclock": lastclock or None,
        "last_time_utc": utc_iso(lastclock) if lastclock else None,
        "lastvalue": item.get("lastvalue"),
        "history_retention": item.get("history"),
        "trend_retention": item.get("trends"),
    }


def sample_clock(sample: Dict[str, Any]) -> int:
    return int(sample.get("clock") or 0)


def summarize_numeric(samples: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    ordered = sorted(samples, key=lambda sample: (sample_clock(sample), int(sample.get("ns") or 0)))
    numeric = []
    valid_samples = []
    for sample in ordered:
        try:
            value = float(sample.get("value"))
        except (TypeError, ValueError):
            continue
        if math.isfinite(value):
            numeric.append(value)
            valid_samples.append(sample)
    if not numeric:
        return {"source": "history", "sample_count": 0}
    clocks = [sample_clock(sample) for sample in valid_samples]
    result: Dict[str, Any] = {
        "source": "history",
        "sample_count": len(numeric),
        "first": {"clock": clocks[0], "time_utc": utc_iso(clocks[0]), "value": numeric[0]},
        "last": {"clock": clocks[-1], "time_utc": utc_iso(clocks[-1]), "value": numeric[-1]},
        "min": min(numeric),
        "max": max(numeric),
        "avg": sum(numeric) / len(numeric),
        "max_gap_seconds": max((right - left for left, right in zip(clocks, clocks[1:])), default=0),
    }
    if key == "system.uptime":
        result["resets"] = [
            {"clock": clocks[index], "time_utc": utc_iso(clocks[index]), "from": numeric[index - 1], "to": numeric[index]}
            for index in range(1, len(numeric))
            if numeric[index] < numeric[index - 1]
        ]
    return result


def summarize_text(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(samples, key=lambda sample: (sample_clock(sample), int(sample.get("ns") or 0)))
    if not ordered:
        return {"source": "history", "sample_count": 0}
    transitions = []
    previous = object()
    for sample in ordered:
        value = str(sample.get("value", ""))
        if value != previous:
            clock = sample_clock(sample)
            transitions.append({"clock": clock, "time_utc": utc_iso(clock), "value": value})
            previous = value
    first_clock = sample_clock(ordered[0])
    last_clock = sample_clock(ordered[-1])
    return {
        "source": "history",
        "sample_count": len(ordered),
        "first": {"clock": first_clock, "time_utc": utc_iso(first_clock), "value": str(ordered[0].get("value", ""))},
        "last": {"clock": last_clock, "time_utc": utc_iso(last_clock), "value": str(ordered[-1].get("value", ""))},
        "value_counts": dict(Counter(str(sample.get("value", "")) for sample in ordered)),
        "transitions": transitions,
        "max_gap_seconds": max(
            (sample_clock(right) - sample_clock(left) for left, right in zip(ordered, ordered[1:])),
            default=0,
        ),
    }


def summarize_trends(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not samples:
        return {"source": "none", "sample_count": 0}
    ordered = sorted(samples, key=sample_clock)
    total_num = sum(int(sample.get("num") or 0) for sample in ordered)
    weighted = sum(float(sample.get("value_avg") or 0) * int(sample.get("num") or 0) for sample in ordered)
    return {
        "source": "trends",
        "sample_count": total_num,
        "trend_buckets": len(ordered),
        "first_bucket_utc": utc_iso(sample_clock(ordered[0])),
        "last_bucket_utc": utc_iso(sample_clock(ordered[-1])),
        "min": min(float(sample.get("value_min") or 0) for sample in ordered),
        "max": max(float(sample.get("value_max") or 0) for sample in ordered),
        "avg": weighted / total_num if total_num else None,
    }


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect Zabbix problems, trigger transitions, item errors, and metric summaries."
    )
    parser.add_argument("--inventory", required=True, help="zabbix_hosts.py JSON file, or - for stdin")
    parser.add_argument("--start", required=True, help="query start: epoch seconds or timezone-aware ISO-8601")
    parser.add_argument("--end", required=True, help="query end: epoch seconds or timezone-aware ISO-8601")
    parser.add_argument("--expected-group", default=DEFAULT_GROUP, help=f"required inventory group (default: {DEFAULT_GROUP})")
    parser.add_argument("--endpoint", help="override inventory Zabbix JSON-RPC endpoint")
    parser.add_argument("--token-env", default=DEFAULT_TOKEN_ENV, help=f"token variable (default: {DEFAULT_TOKEN_ENV})")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help=f"fallback token file (default: {DEFAULT_ENV_FILE})")
    parser.add_argument("--allowed-host", action="append", dest="allowed_hosts", help=f"approved Zabbix host; repeatable (default: {DEFAULT_HOST})")
    parser.add_argument("--ca-file", help="custom CA bundle when the endpoint uses HTTPS")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    parser.add_argument("--max-inventory-age", type=int, default=900, help="maximum inventory age in seconds; 0 disables check")
    parser.add_argument("--max-window-hours", type=float, default=24.0, help="maximum metric window (default: 24)")
    parser.add_argument("--problem-lookback", type=int, default=7 * 86400, help="seconds before start for recently resolved problem lookup")
    parser.add_argument("--max-history-points", type=int, default=100000, help="maximum history rows per value type")
    parser.add_argument("--include-loopback", action="store_true", help="include lo network error/drop metrics")
    parser.add_argument("--include-key-regex", action="append", default=[], help="additional monitored item key regex; repeatable")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.max_window_hours <= 0 or args.max_history_points <= 0:
        parser.error("timeout, max-window-hours, and max-history-points must be positive")
    if args.max_inventory_age < 0 or args.problem_lookback < 0:
        parser.error("max-inventory-age and problem-lookback must be non-negative")
    return args


def run(args: argparse.Namespace) -> Dict[str, Any]:
    start = parse_time(args.start, "start")
    end = parse_time(args.end, "end")
    if end <= start:
        raise ScriptError("end must be later than start")
    if end - start > int(args.max_window_hours * 3600):
        raise ScriptError(f"query window exceeds {args.max_window_hours:g} hours")

    inventory = load_inventory(args.inventory)
    hosts, inventory_endpoint, inventory_fetched_at = validate_inventory(
        inventory, args.expected_group, args.max_inventory_age
    )
    endpoint = validate_endpoint(args.endpoint or inventory_endpoint, args.allowed_hosts or [DEFAULT_HOST])
    token = get_token(args.token_env, Path(args.env_file).expanduser())
    opener = make_opener(args.ca_file)
    hostids = [str(host["hostid"]) for host in hosts]
    host_names = {str(host["hostid"]): str(host["technical_name"]) for host in hosts}
    request_id = 1

    event_rows = rpc_call(
        opener,
        endpoint,
        token,
        "event.get",
        {
            "output": ["eventid", "source", "object", "objectid", "clock", "ns", "value", "name", "acknowledged", "severity", "r_eventid"],
            "hostids": hostids,
            "source": 0,
            "object": 0,
            "time_from": start,
            "time_till": end,
            "value": [0, 1],
            "selectHosts": ["hostid", "host", "name"],
            "sortfield": ["clock", "eventid"],
            "sortorder": "ASC",
        },
        request_id,
        args.timeout,
    )
    request_id += 1
    if not isinstance(event_rows, list):
        raise ScriptError("event.get returned an unexpected result")
    problem_severity = {
        str(event.get("objectid")): str(event.get("severity", "0"))
        for event in event_rows
        if isinstance(event, dict) and str(event.get("value")) == "1"
    }
    events = [normalize_event(event, problem_severity) for event in event_rows if isinstance(event, dict)]

    current_rows = rpc_call(
        opener,
        endpoint,
        token,
        "problem.get",
        {
            "output": ["eventid", "objectid", "clock", "ns", "r_eventid", "r_clock", "name", "acknowledged", "severity", "suppressed", "opdata"],
            "hostids": hostids,
            "recent": False,
            "selectHosts": ["hostid", "host", "name"],
            "sortfield": ["eventid"],
            "sortorder": "ASC",
        },
        request_id,
        args.timeout,
    )
    request_id += 1
    if not isinstance(current_rows, list):
        raise ScriptError("current problem.get returned an unexpected result")

    recent_rows = rpc_call(
        opener,
        endpoint,
        token,
        "problem.get",
        {
            "output": ["eventid", "objectid", "clock", "ns", "r_eventid", "r_clock", "name", "acknowledged", "severity", "suppressed", "opdata"],
            "hostids": hostids,
            "recent": True,
            "time_from": max(1, start - args.problem_lookback),
            "time_till": end,
            "selectHosts": ["hostid", "host", "name"],
            "sortfield": ["eventid"],
            "sortorder": "ASC",
        },
        request_id,
        args.timeout,
    )
    request_id += 1
    if not isinstance(recent_rows, list):
        raise ScriptError("recent problem.get returned an unexpected result")
    overlap_rows = [
        problem
        for problem in recent_rows
        if isinstance(problem, dict)
        and int(problem.get("clock") or 0) <= end
        and (int(problem.get("r_clock") or 0) == 0 or int(problem.get("r_clock") or 0) >= start)
    ]

    item_rows = rpc_call(
        opener,
        endpoint,
        token,
        "item.get",
        {
            "output": ["itemid", "hostid", "name", "key_", "value_type", "status", "state", "lastclock", "lastvalue", "error", "units", "history", "trends"],
            "hostids": hostids,
            "filter": {"status": "0"},
            "sortfield": "name",
        },
        request_id,
        args.timeout,
    )
    request_id += 1
    if not isinstance(item_rows, list):
        raise ScriptError("item.get returned an unexpected result")
    extra_patterns = compile_extra_patterns(args.include_key_regex)
    selected_rows = [
        item for item in item_rows if isinstance(item, dict) and is_metric_item(item, extra_patterns, args.include_loopback)
    ]
    unsupported = [
        normalize_item(item, host_names)
        for item in item_rows
        if isinstance(item, dict) and (str(item.get("state", "0")) == "1" or bool(item.get("error")))
    ]

    samples_by_item: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    history_truncated: Dict[str, bool] = {}
    items_by_type: Dict[int, List[str]] = defaultdict(list)
    for item in selected_rows:
        items_by_type[int(item.get("value_type") or 0)].append(str(item.get("itemid")))
    for value_type, itemids in sorted(items_by_type.items()):
        history_rows = rpc_call(
            opener,
            endpoint,
            token,
            "history.get",
            {
                "output": ["itemid", "clock", "ns", "value"],
                "history": value_type,
                "itemids": itemids,
                "time_from": start,
                "time_till": end,
                "sortfield": "clock",
                "sortorder": "ASC",
                "limit": args.max_history_points + 1,
            },
            request_id,
            args.timeout,
        )
        request_id += 1
        if not isinstance(history_rows, list):
            raise ScriptError(f"history.get returned an unexpected result for value_type {value_type}")
        history_truncated[str(value_type)] = len(history_rows) > args.max_history_points
        for sample in history_rows[: args.max_history_points]:
            if isinstance(sample, dict):
                samples_by_item[str(sample.get("itemid"))].append(sample)

    numeric_missing = [
        str(item.get("itemid"))
        for item in selected_rows
        if int(item.get("value_type") or 0) in {0, 3} and not samples_by_item.get(str(item.get("itemid")))
    ]
    trends_by_item: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    if numeric_missing:
        trend_rows = rpc_call(
            opener,
            endpoint,
            token,
            "trend.get",
            {
                "output": ["itemid", "clock", "num", "value_min", "value_avg", "value_max"],
                "itemids": numeric_missing,
                "time_from": start,
                "time_till": end,
                "sortfield": "clock",
                "sortorder": "ASC",
            },
            request_id,
            args.timeout,
        )
        if not isinstance(trend_rows, list):
            raise ScriptError("trend.get returned an unexpected result")
        for sample in trend_rows:
            if isinstance(sample, dict):
                trends_by_item[str(sample.get("itemid"))].append(sample)

    metrics = []
    for item in selected_rows:
        itemid = str(item.get("itemid"))
        normalized = normalize_item(item, host_names)
        value_type = int(item.get("value_type") or 0)
        samples = samples_by_item.get(itemid, [])
        if samples:
            summary = summarize_numeric(samples, str(item.get("key_"))) if value_type in {0, 3} else summarize_text(samples)
        else:
            summary = summarize_trends(trends_by_item.get(itemid, [])) if value_type in {0, 3} else {"source": "none", "sample_count": 0}
        normalized["window_summary"] = summary
        metrics.append(normalized)
    metrics.sort(key=lambda item: ((item.get("host") or "").casefold(), (item.get("key") or "").casefold()))

    interface_errors = []
    for host in hosts:
        for interface in host.get("interfaces") or []:
            if not isinstance(interface, dict):
                continue
            if interface.get("availability") == "unavailable" or interface.get("error"):
                interface_errors.append(
                    {
                        "hostid": host.get("hostid"),
                        "host": host.get("technical_name"),
                        "type": interface.get("type"),
                        "availability": interface.get("availability"),
                        "error": interface.get("error"),
                        "errors_from_epoch": interface.get("errors_from_epoch"),
                    }
                )

    return {
        "schema_version": 1,
        "source": {
            "endpoint": endpoint,
            "inventory_group": args.expected_group,
            "inventory_fetched_at_utc": inventory_fetched_at.astimezone(timezone.utc).isoformat(timespec="seconds"),
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "window": {
            "start_epoch": start,
            "end_epoch": end,
            "start_utc": utc_iso(start),
            "end_utc": utc_iso(end),
            "problem_lookback_start_utc": utc_iso(max(1, start - args.problem_lookback)),
        },
        "hosts": [
            {"hostid": host.get("hostid"), "technical_name": host.get("technical_name"), "visible_name": host.get("visible_name")}
            for host in hosts
        ],
        "counts": {
            "hosts": len(hosts),
            "trigger_transitions": len(events),
            "current_problems": len(current_rows),
            "overlapping_recent_problems": len(overlap_rows),
            "interface_errors": len(interface_errors),
            "unsupported_items": len(unsupported),
            "selected_metrics": len(metrics),
            "metrics_without_window_data": sum(1 for item in metrics if item["window_summary"]["source"] == "none"),
        },
        "coverage": {
            "history_rows_truncated_by_value_type": history_truncated,
            "problem_lookback_seconds": args.problem_lookback,
            "problem_overlap_limit": "problems that started before the lookback and recovered after the window may be absent",
        },
        "errors": {
            "interface": interface_errors,
            "unsupported_items": unsupported,
            "current_problems": [normalize_problem(item) for item in current_rows if isinstance(item, dict)],
            "overlapping_recent_problems": [normalize_problem(item) for item in overlap_rows],
            "trigger_transitions": events,
        },
        "metrics": metrics,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = parse_args(argv)
        result = run(args)
        json.dump(
            result,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=args.pretty,
        )
        sys.stdout.write("\n")
        return 0
    except ScriptError as exc:
        print(f"zabbix_health.py: error: {exc}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
