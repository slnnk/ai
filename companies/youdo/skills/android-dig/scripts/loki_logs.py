#!/usr/bin/env python3
"""Collect sanitized infrastructure events and ingestion coverage from Loki."""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPHandler, HTTPRedirectHandler, HTTPSHandler, Request, build_opener


DEFAULT_ENDPOINT = "http://loki.dev.youdo.corp"
DEFAULT_HOST = "loki.dev.youdo.corp"
DEFAULT_GROUP = "Selenium"
DEFAULT_PATTERN = (
    r"(?i)(error|fail|timeout|timed out|offline|unauthorized|disconnect|reset|"
    r"out of memory|oom|killed process|no space|read-only file system|dns|resolve|"
    r"eai_again|connection refused|connection reset|502|503|504|adb|appium|"
    r"selenium|grid|uiautomator|instrumentation|systemport|emulator|qemu|usb)"
)
MAX_RESPONSE_BYTES = 20 * 1024 * 1024
SAFE_STREAM_LABELS = (
    "instance",
    "job",
    "job_name",
    "service_name",
    "unit",
    "systemd_unit",
    "source",
    "filename",
    "priority",
)


class ScriptError(RuntimeError):
    """Expected input, transport, or API failure."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


INFRA_CATEGORIES: Sequence[Tuple[str, re.Pattern[str]]] = (
    (
        "host_resource",
        re.compile(
            r"(?i)out of memory|oom(?:[-_ ]killer)?|killed process|no space left|"
            r"read-only file system|input/output error|disk quota"
        ),
    ),
    (
        "service_systemd",
        re.compile(
            r"(?i)failed to start|entered failed state|main process exited|start request repeated|"
            r"restart counter|unit .* failed|dependency failed"
        ),
    ),
    (
        "adb_device_usb",
        re.compile(
            r"(?i)(?:adb|device).*(?:offline|unauthorized|not found|no devices|disconnect|timeout)|"
            r"(?:offline|unauthorized).*(?:adb|device)|usb.*(?:disconnect|reset|error)|"
            r"device .* not found|no permissions.*usb"
        ),
    ),
    (
        "appium_uiautomator",
        re.compile(
            r"(?i)(?:appium|uiautomator|instrumentation|systemport).*(?:error|fail|timeout|"
            r"timed out|crash|exited|refused|reset|hang)|sessionnotcreated|could not proxy|"
            r"socket hang up|instrumentation.*(?:stopped|failed|crash)"
        ),
    ),
    (
        "selenium_grid",
        re.compile(
            r"(?i)(?:selenium|grid|webdriver).*(?:error|fail|timeout|timed out|unreachable|"
            r"refused|reset|no slot|queue)|session request.*(?:reject|timeout|fail)"
        ),
    ),
    (
        "emulator",
        re.compile(
            r"(?i)(?:emulator|qemu).*(?:error|fail|timeout|timed out|crash|killed|hang|"
            r"not responding|boot.*(?:fail|timeout))"
        ),
    ),
    (
        "network_dependency",
        re.compile(
            r"(?i)eai_again|nxdomain|temporary failure in name resolution|could not resolve|"
            r"name or service not known|connection refused|connection reset|network is unreachable|"
            r"no route to host|tls handshake timeout|i/o timeout|\b(?:502|503|504)\b"
        ),
    ),
)


SECRET_PATTERNS: Sequence[Tuple[re.Pattern[str], str]] = (
    (re.compile(r"(?i)\b(authorization\s*[:=]\s*)(?:bearer\s+)?\S+"), r"\1[REDACTED]"),
    (
        re.compile(
            r"(?i)\b(token|password|passwd|secret|private[_-]?token|access[_-]?token|"
            r"refresh[_-]?token|cookie)\s*[:=]\s*([^\s,;]+)"
        ),
        r"\1=[REDACTED]",
    ),
    (re.compile(r"(?i)(https?://)([^/@\s:]+):([^/@\s]+)@"), r"\1[REDACTED]@"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"), "[REDACTED_JWT]"),
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


def utc_iso_ns(raw_ns: int) -> str:
    seconds, remainder = divmod(raw_ns, 1_000_000_000)
    base = datetime.fromtimestamp(seconds, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    return f"{base}.{remainder:09d}Z"


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
) -> Tuple[List[str], str]:
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

    names: List[str] = []
    seen = set()
    for host in hosts:
        if not isinstance(host, dict) or host.get("enabled") is not True:
            raise ScriptError("inventory contains a host that is not Enabled")
        name = host.get("technical_name")
        if not isinstance(name, str) or not name or name in seen:
            raise ScriptError("inventory contains a missing or duplicate technical_name")
        if any(char in name for char in ('\n', '\r', '"', '\\')):
            raise ScriptError(f"inventory host name cannot be represented safely in LogQL: {name!r}")
        seen.add(name)
        names.append(name)
    if not names:
        raise ScriptError("inventory contains no Enabled hosts")
    return names, fetched_at.astimezone(timezone.utc).isoformat(timespec="seconds")


def validate_endpoint(endpoint: str, allowed_hosts: Iterable[str]) -> str:
    parsed = urlparse(endpoint)
    allowed = {host.lower() for host in allowed_hosts}
    if parsed.scheme not in {"http", "https"}:
        raise ScriptError("Loki endpoint must use http or https")
    if not parsed.hostname or parsed.hostname.lower() not in allowed:
        raise ScriptError(f"refusing Loki endpoint host {parsed.hostname!r}; use --allowed-host to permit it")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ScriptError("Loki endpoint must not contain credentials, query parameters, or a fragment")
    if parsed.path not in {"", "/"}:
        raise ScriptError("Loki endpoint must be an origin without an API path")
    return endpoint.rstrip("/")


def make_opener(ca_file: Optional[str]) -> Any:
    context = ssl.create_default_context(cafile=ca_file) if ca_file else ssl.create_default_context()
    return build_opener(NoRedirect(), HTTPHandler(), HTTPSHandler(context=context))


def api_get(opener: Any, endpoint: str, path: str, params: Sequence[Tuple[str, str]], timeout: float) -> Any:
    url = f"{endpoint}{path}?{urlencode(params)}"
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "android-dig-loki/1"})
    try:
        with opener.open(request, timeout=timeout) as response:
            if response.geturl() != url:
                raise ScriptError("Loki redirected the request; redirects are refused")
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as exc:
        detail = exc.read(1024).decode("utf-8", "replace")
        raise ScriptError(f"Loki HTTP {exc.code}: {sanitize(detail, 800)}") from exc
    except URLError as exc:
        raise ScriptError(f"cannot reach Loki: {exc.reason}") from exc
    if len(body) > MAX_RESPONSE_BYTES:
        raise ScriptError(f"Loki response exceeds {MAX_RESPONSE_BYTES} bytes")
    try:
        document = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ScriptError("Loki returned invalid JSON") from exc
    if not isinstance(document, dict) or document.get("status") != "success":
        raise ScriptError(f"Loki API failure: {sanitize(json.dumps(document), 800)}")
    return document.get("data")


def sanitize(value: Any, limit: int = 1500) -> str:
    text = str(value).replace("\x00", "")
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    text = "".join(char if char in "\n\t" or ord(char) >= 32 else " " for char in text)
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text[:limit] + ("…" if len(text) > limit else "")


def safe_labels(labels: Any) -> Dict[str, str]:
    if not isinstance(labels, dict):
        return {}
    return {key: sanitize(labels[key], 300) for key in SAFE_STREAM_LABELS if key in labels}


def is_security_stream(labels: Dict[str, Any]) -> bool:
    job = str(labels.get("job") or labels.get("service_name") or "").lower()
    filename = str(labels.get("filename") or "").lower()
    return "security" in job or "/falco/" in filename or filename.endswith("/falco/events.json")


def stream_selector(host: str, operational_only: bool = False) -> str:
    selector = f'{{instance="{host}"'
    if operational_only:
        selector += ',job!="integrations/security",filename!="/var/log/falco/events.json"'
    return selector + "}"


def logql_regex_value(values: Iterable[str]) -> str:
    """Escape RE2 alternatives and then escape backslashes for a LogQL string."""
    return "|".join(re.escape(value).replace("\\", "\\\\") for value in values)


def logql_string(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise ScriptError("LogQL pattern must not contain a newline")
    return value.replace("\\", "\\\\").replace('"', '\\"')


def parse_stream_results(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, dict) or data.get("resultType") != "streams" or not isinstance(data.get("result"), list):
        raise ScriptError("Loki query_range returned an unexpected result shape")
    entries: List[Dict[str, Any]] = []
    for result in data["result"]:
        if not isinstance(result, dict):
            continue
        labels = result.get("stream") if isinstance(result.get("stream"), dict) else {}
        values = result.get("values") if isinstance(result.get("values"), list) else []
        for value in values:
            if not isinstance(value, list) or len(value) != 2:
                continue
            try:
                timestamp_ns = int(value[0])
            except (TypeError, ValueError):
                continue
            entries.append({"timestamp_ns": timestamp_ns, "labels": labels, "line": str(value[1])})
    return entries


def query_range(
    opener: Any,
    endpoint: str,
    query: str,
    start_ns: int,
    end_ns: int,
    direction: str,
    limit: int,
    timeout: float,
) -> List[Dict[str, Any]]:
    data = api_get(
        opener,
        endpoint,
        "/loki/api/v1/query_range",
        (
            ("query", query),
            ("start", str(start_ns)),
            ("end", str(end_ns)),
            ("direction", direction),
            ("limit", str(limit)),
        ),
        timeout,
    )
    return parse_stream_results(data)


def collect_split(
    opener: Any,
    endpoint: str,
    query: str,
    start_ns: int,
    end_ns: int,
    limit: int,
    max_chunks: int,
    max_events: int,
    timeout: float,
) -> Tuple[List[Dict[str, Any]], bool, int]:
    pending = [(start_ns, end_ns)]
    collected: List[Dict[str, Any]] = []
    calls = 0
    truncated = False
    while pending:
        left, right = pending.pop(0)
        if calls >= max_chunks:
            truncated = True
            break
        batch = query_range(opener, endpoint, query, left, right, "forward", limit, timeout)
        calls += 1
        if len(batch) >= limit and right - left > 1:
            middle = left + (right - left) // 2
            pending[0:0] = [(left, middle), (middle + 1, right)]
            continue
        collected.extend(batch)
        if len(collected) >= max_events:
            collected = collected[:max_events]
            truncated = bool(pending) or len(batch) >= limit
            break
    deduplicated: Dict[Tuple[int, str, str], Dict[str, Any]] = {}
    for entry in collected:
        key = (entry["timestamp_ns"], json.dumps(entry["labels"], sort_keys=True), entry["line"])
        deduplicated[key] = entry
    ordered = sorted(deduplicated.values(), key=lambda item: item["timestamp_ns"])
    return ordered, truncated, calls


def extract_message(line: str) -> str:
    try:
        document = json.loads(line)
    except json.JSONDecodeError:
        return line
    if isinstance(document, dict):
        for key in ("MESSAGE", "message", "msg", "log", "output"):
            if document.get(key) is not None:
                return str(document[key])
    return line


def classify(line: str) -> List[str]:
    if re.search(r"(?i)\bfalco(?:ctl)?(?:[-_. ]|$)", line):
        return []
    return [name for name, pattern in INFRA_CATEGORIES if pattern.search(line)]


def sample_summary(entry: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if entry is None:
        return None
    return {
        "timestamp_ns": str(entry["timestamp_ns"]),
        "time_utc": utc_iso_ns(entry["timestamp_ns"]),
        "labels": safe_labels(entry["labels"]),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read Loki coverage and sanitized infrastructure errors for Enabled Selenium hosts "
            "from a fresh zabbix_hosts.py inventory."
        )
    )
    parser.add_argument("--inventory", required=True, help="zabbix_hosts.py JSON file, or - for stdin")
    parser.add_argument("--start", required=True, help="window start: epoch seconds or timezone-aware ISO-8601")
    parser.add_argument("--end", required=True, help="window end: epoch seconds or timezone-aware ISO-8601")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Loki origin")
    parser.add_argument("--allowed-host", action="append", default=[], help="additional permitted Loki hostname")
    parser.add_argument("--expected-group", default=DEFAULT_GROUP, help="required Zabbix group in inventory")
    parser.add_argument("--max-inventory-age", type=int, default=900, help="maximum inventory age in seconds; 0 disables")
    parser.add_argument("--max-window-hours", type=float, default=24.0, help="reject wider query windows")
    parser.add_argument("--pattern", default=DEFAULT_PATTERN, help="RE2-compatible LogQL candidate pattern")
    parser.add_argument("--limit", type=int, default=1000, help="Loki entries per request")
    parser.add_argument("--max-chunks", type=int, default=16, help="maximum split queries per host")
    parser.add_argument("--max-events", type=int, default=5000, help="maximum candidate entries per host")
    parser.add_argument(
        "--max-boundary-gap",
        type=int,
        default=300,
        help="maximum seconds from each window boundary to an operational sample",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout per request")
    parser.add_argument("--ca-file", help="custom CA bundle for HTTPS")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.limit < 1 or args.limit > 5000:
            raise ScriptError("--limit must be between 1 and 5000")
        if args.max_chunks < 1 or args.max_events < 1 or args.max_boundary_gap < 0 or args.timeout <= 0:
            raise ScriptError("chunk/event limits and timeout must be positive; boundary gap cannot be negative")
        start = parse_time(args.start, "start")
        end = parse_time(args.end, "end")
        if end < start:
            raise ScriptError("end must be greater than or equal to start")
        if args.max_window_hours > 0 and end - start > args.max_window_hours * 3600:
            raise ScriptError(f"query window exceeds --max-window-hours={args.max_window_hours:g}")
        inventory = load_inventory(args.inventory)
        hosts, inventory_fetched_at = validate_inventory(
            inventory, args.expected_group, args.max_inventory_age
        )
        endpoint = validate_endpoint(args.endpoint, [DEFAULT_HOST, *args.allowed_host])
        opener = make_opener(args.ca_file)
        start_ns = start * 1_000_000_000
        end_ns = (end + 1) * 1_000_000_000 - 1

        label_values = api_get(
            opener,
            endpoint,
            "/loki/api/v1/label/instance/values",
            (("start", str(start_ns)), ("end", str(end_ns))),
            args.timeout,
        )
        if not isinstance(label_values, list):
            raise ScriptError("Loki instance label endpoint returned an unexpected result")
        present = {str(value) for value in label_values}

        regex = logql_regex_value(hosts)
        series = api_get(
            opener,
            endpoint,
            "/loki/api/v1/series",
            (("match[]", f'{{instance=~"{regex}"}}'), ("start", str(start_ns)), ("end", str(end_ns))),
            args.timeout,
        )
        if not isinstance(series, list):
            raise ScriptError("Loki series endpoint returned an unexpected result")
        streams_by_host: Dict[str, List[Dict[str, Any]]] = {host: [] for host in hosts}
        for stream in series:
            if isinstance(stream, dict) and str(stream.get("instance")) in streams_by_host:
                streams_by_host[str(stream["instance"])].append(stream)

        coverage: Dict[str, Any] = {}
        events: List[Dict[str, Any]] = []
        category_counts: Counter[str] = Counter()
        total_query_calls = 2
        for host in hosts:
            host_streams = streams_by_host[host]
            operational_streams = [item for item in host_streams if not is_security_stream(item)]
            instance_present = host in present
            if not instance_present:
                status = "instance_absent"
            elif host_streams and not operational_streams:
                status = "security_only"
            elif operational_streams:
                status = "operational_streams_present"
            else:
                status = "instance_present_but_series_unknown"

            first_entry: Optional[Dict[str, Any]] = None
            last_entry: Optional[Dict[str, Any]] = None
            candidate_count = 0
            uncategorized_count = 0
            truncated = False
            host_query_calls = 0
            if operational_streams:
                selector = stream_selector(host, operational_only=True)
                first = query_range(opener, endpoint, selector, start_ns, end_ns, "forward", 1, args.timeout)
                last = query_range(opener, endpoint, selector, start_ns, end_ns, "backward", 1, args.timeout)
                host_query_calls += 2
                first_entry = min(first, key=lambda item: item["timestamp_ns"]) if first else None
                last_entry = max(last, key=lambda item: item["timestamp_ns"]) if last else None
                candidates, truncated, split_calls = collect_split(
                    opener,
                    endpoint,
                    f'{selector} |~ "{logql_string(args.pattern)}"',
                    start_ns,
                    end_ns,
                    args.limit,
                    args.max_chunks,
                    args.max_events,
                    args.timeout,
                )
                host_query_calls += split_calls
                candidate_count = len(candidates)
                for entry in candidates:
                    message = extract_message(entry["line"])
                    categories = classify(message)
                    if not categories:
                        uncategorized_count += 1
                        continue
                    category_counts.update(categories)
                    events.append(
                        {
                            "host": host,
                            "timestamp_ns": str(entry["timestamp_ns"]),
                            "time_utc": utc_iso_ns(entry["timestamp_ns"]),
                            "categories": categories,
                            "labels": safe_labels(entry["labels"]),
                            "message": sanitize(message),
                        }
                    )
            total_query_calls += host_query_calls
            first_gap = (
                max(0.0, (first_entry["timestamp_ns"] - start_ns) / 1_000_000_000)
                if first_entry is not None
                else None
            )
            last_gap = (
                max(0.0, (end_ns - last_entry["timestamp_ns"]) / 1_000_000_000)
                if last_entry is not None
                else None
            )
            boundary_coverage = (
                first_gap is not None
                and last_gap is not None
                and first_gap <= args.max_boundary_gap
                and last_gap <= args.max_boundary_gap
            )
            coverage[host] = {
                "status": status,
                "instance_value_present": instance_present,
                "stream_count": len(host_streams),
                "operational_stream_count": len(operational_streams),
                "security_stream_count": len(host_streams) - len(operational_streams),
                "streams": [safe_labels(item) for item in host_streams[:100]],
                "streams_truncated": len(host_streams) > 100,
                "first_operational_sample": sample_summary(first_entry),
                "last_operational_sample": sample_summary(last_entry),
                "first_sample_gap_seconds": round(first_gap, 3) if first_gap is not None else None,
                "last_sample_gap_seconds": round(last_gap, 3) if last_gap is not None else None,
                "boundary_coverage": boundary_coverage,
                "candidate_entries": candidate_count,
                "uncategorized_candidates_omitted": uncategorized_count,
                "event_query_truncated": truncated,
                "query_calls": host_query_calls,
            }

        events.sort(key=lambda item: (item["timestamp_ns"], item["host"]))
        result = {
            "schema_version": 1,
            "source": {
                "endpoint": endpoint,
                "api": "Loki HTTP API",
                "read_only": True,
                "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "inventory_fetched_at_utc": inventory_fetched_at,
                "inventory_group": args.expected_group,
                "instance_label": "instance",
            },
            "window": {
                "start_epoch": start,
                "end_epoch": end,
                "start_utc": datetime.fromtimestamp(start, tz=timezone.utc).isoformat(timespec="seconds"),
                "end_utc": datetime.fromtimestamp(end, tz=timezone.utc).isoformat(timespec="seconds"),
                "start_ns": str(start_ns),
                "end_ns": str(end_ns),
            },
            "query": {
                "hosts": hosts,
                "candidate_pattern": args.pattern,
                "per_request_limit": args.limit,
                "max_chunks_per_host": args.max_chunks,
                "max_events_per_host": args.max_events,
                "max_boundary_gap_seconds": args.max_boundary_gap,
                "total_api_calls": total_query_calls,
            },
            "summary": {
                "inventory_host_count": len(hosts),
                "instances_present": sum(1 for host in hosts if coverage[host]["instance_value_present"]),
                "hosts_with_operational_streams": sum(
                    1 for host in hosts if coverage[host]["operational_stream_count"] > 0
                ),
                "hosts_security_only": sum(1 for host in hosts if coverage[host]["status"] == "security_only"),
                "classified_event_count": len(events),
                "category_counts": dict(sorted(category_counts.items())),
                "coverage_complete": all(
                    coverage[host]["status"] == "operational_streams_present"
                    and coverage[host]["boundary_coverage"]
                    and not coverage[host]["event_query_truncated"]
                    for host in hosts
                ),
            },
            "coverage": coverage,
            "events": events,
        }
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
        sys.stdout.write("\n")
        return 0
    except ScriptError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
