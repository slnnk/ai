#!/usr/bin/env python3
"""Build a Nomad job/task resource optimization CSV from Nomad and VictoriaMetrics.

Memory columns are MiB. CPU columns are MHz. The script reads credentials only
from environment variables and never writes them to the output.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


COLUMNS = [
    "Nomad job",
    "Nomad task",
    "Nomad mem limit",
    "Nomad max mem limit",
    "Nomad cpu limit",
    "Peak mem usage",
    "Peak cpu usage",
    "AVG mem usage",
    "AVG cpu usage",
    "Recommended mem limit",
    "Recommended max mem limit",
    "Recommended cpu limit",
]

JOB_LABEL = "container_label_com_hashicorp_nomad_job_id"
TASK_LABEL = "container_label_com_hashicorp_nomad_task_name"
ALLOC_LABEL = "container_label_com_hashicorp_nomad_alloc_id"
TEST_STAND_SUFFIX_RE = re.compile(r"-test\d*$")
TASK_TEST_TOKEN_RE = re.compile(r"-test\d*(?=-|$)")


def request_json(url: str, headers: dict[str, str] | None = None, timeout: int = 90) -> Any:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def nomad_get(base_url: str, token: str, path: str, params: dict[str, str] | None = None) -> Any:
    query = urllib.parse.urlencode(params or {})
    url = f"{base_url.rstrip('/')}{path}"
    if query:
        url = f"{url}?{query}"
    return request_json(url, {"X-Nomad-Token": token})


def vm_query(base_url: str, expression: str) -> list[dict[str, Any]]:
    url = f"{base_url.rstrip('/')}/query?{urllib.parse.urlencode({'query': expression})}"
    payload = request_json(url, timeout=180)
    if payload.get("status") != "success":
        raise RuntimeError(f"VictoriaMetrics query failed: {payload.get('error', payload)}")
    return payload["data"]["result"]


def vector_map(result: list[dict[str, Any]]) -> dict[tuple[str, str], float]:
    output: dict[tuple[str, str], float] = {}
    for entry in result:
        metric = entry.get("metric", {})
        job = metric.get(JOB_LABEL)
        task = metric.get(TASK_LABEL)
        if not job or not task:
            continue
        output[(job, task)] = float(entry["value"][1])
    return output


def normalized_key(key: tuple[str, str], merge_test_stands: bool) -> tuple[str, str]:
    if not merge_test_stands:
        return key
    job, task = key
    normalized_job = TEST_STAND_SUFFIX_RE.sub("", job)
    if normalized_job == job:
        return key
    return normalized_job, TASK_TEST_TOKEN_RE.sub("", task)


def aggregate_limits(
    values: dict[tuple[str, str], dict[str, int]], merge_test_stands: bool
) -> dict[tuple[str, str], dict[str, int]]:
    output: dict[tuple[str, str], dict[str, int]] = {}
    for raw_key, limits in values.items():
        key = normalized_key(raw_key, merge_test_stands)
        if key in output:
            output[key] = {name: max(output[key][name], limits[name]) for name in limits}
        else:
            output[key] = limits.copy()
    return output


def aggregate_metric(
    values: dict[tuple[str, str], float], merge_test_stands: bool, mode: str
) -> dict[tuple[str, str], float]:
    grouped: dict[tuple[str, str], list[float]] = {}
    for raw_key, value in values.items():
        grouped.setdefault(normalized_key(raw_key, merge_test_stands), []).append(value)
    if mode == "max":
        return {key: max(samples) for key, samples in grouped.items()}
    if mode == "mean":
        return {key: sum(samples) / len(samples) for key, samples in grouped.items()}
    raise ValueError(mode)


def aggregate_weighted_metric(
    values: dict[tuple[str, str], float],
    weights: dict[tuple[str, str], float],
    merge_test_stands: bool,
) -> dict[tuple[str, str], float]:
    totals: dict[tuple[str, str], float] = {}
    total_weights: dict[tuple[str, str], float] = {}
    for raw_key, value in values.items():
        weight = weights.get(raw_key, 0.0)
        if weight <= 0:
            continue
        key = normalized_key(raw_key, merge_test_stands)
        totals[key] = totals.get(key, 0.0) + value * weight
        total_weights[key] = total_weights.get(key, 0.0) + weight
    return {key: totals[key] / total_weights[key] for key in totals}


def grouped_expression(metric_expression: str, function: str, days: int, step: str) -> str:
    grouped = f"max by ({JOB_LABEL},{TASK_LABEL}) ({metric_expression})"
    if function == "peak":
        return f"max_over_time(({grouped})[{days}d:{step}])"
    if function == "p95":
        return f"quantile_over_time(0.95,({grouped})[{days}d:{step}])"
    if function == "avg":
        averaged = f"avg by ({JOB_LABEL},{TASK_LABEL}) ({metric_expression})"
        return f"avg_over_time(({averaged})[{days}d:{step}])"
    raise ValueError(function)


def round_up(value: float, quantum: int) -> int:
    return int(math.ceil(value / quantum) * quantum)


def fmt(value: float | int | None, digits: int = 1) -> str | int:
    if value is None:
        return ""
    if isinstance(value, int):
        return value
    return round(value, digits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--nomad-addr",
        default=os.getenv("NOMAD_ADDR") or os.getenv("NOMAD_YANDEX_TEST_ADDR"),
        help="Nomad HTTP address (default: NOMAD_ADDR or NOMAD_YANDEX_TEST_ADDR)",
    )
    parser.add_argument(
        "--nomad-token-env",
        default="NOMAD_YANDEX_TEST_TOKEN",
        help="Environment variable containing the Nomad ACL token",
    )
    parser.add_argument(
        "--vmselect-url",
        default="http://vmselect.dev.youdo.corp/select/0/prometheus/api/v1",
        help="Prometheus-compatible VictoriaMetrics API base URL",
    )
    parser.add_argument("--days", type=int, default=7, help="History window in days")
    parser.add_argument("--step", default="5m", help="Subquery sampling step")
    parser.add_argument(
        "--min-samples",
        type=int,
        default=24,
        help="Minimum historical samples required to emit a recommendation",
    )
    parser.add_argument(
        "--mhz-per-core",
        type=float,
        default=1999.0,
        help="Convert cAdvisor CPU cores to Nomad MHz",
    )
    parser.add_argument("--workers", type=int, default=16, help="Concurrent Nomad job reads")
    parser.add_argument(
        "--keep-test-stands",
        action="store_true",
        help="Keep -test/-testN jobs separate instead of merging them by service",
    )
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    if not args.nomad_addr:
        parser.error("Nomad address is required")
    token = os.getenv(args.nomad_token_env) or os.getenv("NOMAD_TOKEN")
    if not token:
        parser.error(f"Nomad token is missing in {args.nomad_token_env} or NOMAD_TOKEN")

    jobs = nomad_get(args.nomad_addr, token, "/v1/jobs")
    active_jobs = [job for job in jobs if job.get("Status") in {"running", "pending"}]

    def fetch_job(stub: dict[str, Any]) -> dict[str, Any]:
        encoded_id = urllib.parse.quote(stub["ID"], safe="")
        return nomad_get(
            args.nomad_addr,
            token,
            f"/v1/job/{encoded_id}",
            {"namespace": stub.get("Namespace", "default")},
        )

    current: dict[tuple[str, str], dict[str, int]] = {}
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch_job, stub): stub for stub in active_jobs}
        for future in as_completed(futures):
            stub = futures[future]
            try:
                job = future.result()
            except Exception as error:  # keep the report useful if one job disappears mid-run
                failures.append(f"{stub['ID']}: {error}")
                continue
            for group in job.get("TaskGroups") or []:
                for task in group.get("Tasks") or []:
                    resources = task.get("Resources") or {}
                    cpu = int(resources.get("CPU") or 0)
                    cores = int(resources.get("Cores") or 0)
                    if cpu == 0 and cores > 0:
                        cpu = round(cores * args.mhz_per_core)
                    key = (job["ID"], task["Name"])
                    values = {
                        "mem": int(resources.get("MemoryMB") or 0),
                        "mem_max": int(resources.get("MemoryMaxMB") or 0),
                        "cpu": cpu,
                        "lifecycle": 1 if task.get("Lifecycle") else 0,
                    }
                    if key in current:
                        current[key] = {name: max(current[key][name], values[name]) for name in values}
                    else:
                        current[key] = values

    selector = (
        f'job="alloy-cadvisor",{ALLOC_LABEL}!="",'
        f'{JOB_LABEL}!="",{TASK_LABEL}!=""'
    )
    mem_metric = f"container_memory_working_set_bytes{{{selector}}}"
    cpu_metric = f"rate(container_cpu_usage_seconds_total{{{selector}}}[5m])"

    expressions = {
        "mem_peak": grouped_expression(mem_metric, "peak", args.days, args.step),
        "mem_p95": grouped_expression(mem_metric, "p95", args.days, args.step),
        "mem_avg": grouped_expression(mem_metric, "avg", args.days, args.step),
        "mem_samples": f"count_over_time((max by ({JOB_LABEL},{TASK_LABEL}) ({mem_metric}))[{args.days}d:{args.step}])",
        "cpu_peak": grouped_expression(cpu_metric, "peak", args.days, args.step),
        "cpu_p95": grouped_expression(cpu_metric, "p95", args.days, args.step),
        "cpu_avg": grouped_expression(cpu_metric, "avg", args.days, args.step),
        "cpu_samples": f"count_over_time((max by ({JOB_LABEL},{TASK_LABEL}) ({cpu_metric}))[{args.days}d:{args.step}])",
    }
    raw_metrics = {name: vector_map(vm_query(args.vmselect_url, query)) for name, query in expressions.items()}
    merge_test_stands = not args.keep_test_stands
    current = aggregate_limits(current, merge_test_stands)
    metrics = {
        "mem_peak": aggregate_metric(raw_metrics["mem_peak"], merge_test_stands, "max"),
        "mem_p95": aggregate_metric(raw_metrics["mem_p95"], merge_test_stands, "max"),
        "mem_samples": aggregate_metric(raw_metrics["mem_samples"], merge_test_stands, "mean"),
        "cpu_peak": aggregate_metric(raw_metrics["cpu_peak"], merge_test_stands, "max"),
        "cpu_p95": aggregate_metric(raw_metrics["cpu_p95"], merge_test_stands, "max"),
        "cpu_samples": aggregate_metric(raw_metrics["cpu_samples"], merge_test_stands, "mean"),
    }
    metrics["mem_avg"] = aggregate_weighted_metric(
        raw_metrics["mem_avg"], raw_metrics["mem_samples"], merge_test_stands
    )
    metrics["cpu_avg"] = aggregate_weighted_metric(
        raw_metrics["cpu_avg"], raw_metrics["cpu_samples"], merge_test_stands
    )

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for key in sorted(current, key=lambda item: (item[0].lower(), item[1].lower())):
            limits = current[key]
            mem_peak_b = metrics["mem_peak"].get(key)
            mem_p95_b = metrics["mem_p95"].get(key)
            mem_avg_b = metrics["mem_avg"].get(key)
            cpu_peak_cores = metrics["cpu_peak"].get(key)
            cpu_p95_cores = metrics["cpu_p95"].get(key)
            cpu_avg_cores = metrics["cpu_avg"].get(key)
            mem_samples = metrics["mem_samples"].get(key, 0.0)
            cpu_samples = metrics["cpu_samples"].get(key, 0.0)

            mem_peak = mem_peak_b / 1048576 if mem_peak_b is not None else None
            mem_p95 = mem_p95_b / 1048576 if mem_p95_b is not None else None
            mem_avg = mem_avg_b / 1048576 if mem_avg_b is not None else None
            cpu_peak = cpu_peak_cores * args.mhz_per_core if cpu_peak_cores is not None else None
            cpu_p95 = cpu_p95_cores * args.mhz_per_core if cpu_p95_cores is not None else None
            cpu_avg = cpu_avg_cores * args.mhz_per_core if cpu_avg_cores is not None else None

            rec_mem = None
            rec_mem_max = None
            rec_cpu = None
            if (
                not limits["lifecycle"]
                and mem_samples >= args.min_samples
                and mem_peak is not None
                and mem_p95 is not None
                and mem_avg is not None
            ):
                rec_mem = round_up(max(64.0, mem_p95 * 1.20, mem_avg * 1.50), 16)
                # The reservation already includes its own safety margin. Applying
                # another 1.5x multiplier here double-counts that headroom and can
                # produce a hard limit far above the observed peak.
                rec_mem_max = round_up(max(128.0, mem_peak * 1.20, rec_mem), 64)
            if (
                not limits["lifecycle"]
                and cpu_samples >= args.min_samples
                and cpu_peak is not None
                and cpu_p95 is not None
                and cpu_avg is not None
            ):
                rec_cpu = round_up(max(50.0, cpu_p95 * 1.25, cpu_avg * 1.50), 50)

            writer.writerow(
                {
                    "Nomad job": key[0],
                    "Nomad task": key[1],
                    "Nomad mem limit": limits["mem"],
                    "Nomad max mem limit": limits["mem_max"] or "",
                    "Nomad cpu limit": limits["cpu"],
                    "Peak mem usage": fmt(mem_peak),
                    "Peak cpu usage": fmt(cpu_peak),
                    "AVG mem usage": fmt(mem_avg),
                    "AVG cpu usage": fmt(cpu_avg),
                    "Recommended mem limit": fmt(rec_mem),
                    "Recommended max mem limit": fmt(rec_mem_max),
                    "Recommended cpu limit": fmt(rec_cpu),
                }
            )

    print(
        json.dumps(
            {
                "output": str(output_path),
                "active_jobs": len(active_jobs),
                "rows": len(current),
                "jobs_fetch_failed": failures,
                "history_days": args.days,
                "merged_test_stands": merge_test_stands,
                "min_samples": args.min_samples,
            },
            ensure_ascii=False,
        )
    )
    return 0 if not failures else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as error:
        print(f"HTTP error {error.code} for {error.url}", file=sys.stderr)
        raise
