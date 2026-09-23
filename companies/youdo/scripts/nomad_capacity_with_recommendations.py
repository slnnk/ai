#!/usr/bin/env python3
"""Estimate Nomad node capacity after applying a recommendation CSV.

The script is read-only. It reads NOMAD_YANDEX_TEST_ADDR and
NOMAD_YANDEX_TEST_TOKEN (or NOMAD_ADDR/NOMAD_TOKEN), fetches allocations from
ready/eligible clients, substitutes recommended CPU and memory reservations,
and runs a two-dimensional first-fit-decreasing packing estimate.

Example:
  python3 nomad_capacity_with_recommendations.py --recommendations table.csv
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import re
import urllib.parse
import urllib.request


TEST_STAND_SUFFIX_RE = re.compile(r"-test\d*$")
TASK_TEST_TOKEN_RE = re.compile(r"-test\d*(?=-|$)")


def get_json(base: str, token: str, path: str):
    request = urllib.request.Request(
        f"{base.rstrip('/')}{path}", headers={"X-Nomad-Token": token}
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


def normalized_key(job: str, task: str) -> tuple[str, str]:
    normalized_job = TEST_STAND_SUFFIX_RE.sub("", job)
    if normalized_job == job:
        return job, task
    return normalized_job, TASK_TEST_TOKEN_RE.sub("", task)


def number(value: str) -> int | None:
    if not value:
        return None
    return int(round(float(value)))


def pack(items: list[dict], bins_count: int, cpu_cap: int, mem_cap: int):
    """Best-fit-decreasing heuristic for CPU and memory reservations."""
    bins = [{"cpu": 0, "mem": 0, "items": 0} for _ in range(bins_count)]
    ordered = sorted(
        items,
        key=lambda item: max(item["cpu"] / cpu_cap, item["mem"] / mem_cap),
        reverse=True,
    )
    for item in ordered:
        candidates = []
        for index, target in enumerate(bins):
            new_cpu = target["cpu"] + item["cpu"]
            new_mem = target["mem"] + item["mem"]
            if new_cpu <= cpu_cap and new_mem <= mem_cap:
                slack = (cpu_cap - new_cpu) / cpu_cap + (mem_cap - new_mem) / mem_cap
                candidates.append((slack, index))
        if not candidates:
            return None
        _, index = min(candidates)
        bins[index]["cpu"] += item["cpu"]
        bins[index]["mem"] += item["mem"]
        bins[index]["items"] += 1
    return bins


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recommendations", required=True)
    args = parser.parse_args()

    base = os.getenv("NOMAD_ADDR") or os.getenv("NOMAD_YANDEX_TEST_ADDR")
    token = os.getenv("NOMAD_TOKEN") or os.getenv("NOMAD_YANDEX_TEST_TOKEN")
    if not base or not token:
        parser.error("Nomad address/token environment variables are required")

    recommendations = {}
    with open(args.recommendations, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            recommendations[(row["Nomad job"], row["Nomad task"])] = {
                "cpu": number(row["Recommended cpu limit"]),
                "mem": number(row["Recommended mem limit"]),
            }

    nodes = [
        node
        for node in get_json(base, token, "/v1/nodes?resources=true")
        if node.get("Status") == "ready"
        and node.get("SchedulingEligibility") == "eligible"
    ]
    items = []
    task_instances = changed_cpu = changed_mem = missing = 0
    per_node = {node["ID"]: {"current_cpu": 0, "current_mem": 0,
                             "recommended_cpu": 0, "recommended_mem": 0,
                             "allocations": 0} for node in nodes}
    for node in nodes:
        encoded_id = urllib.parse.quote(node["ID"], safe="")
        allocations = get_json(base, token, f"/v1/node/{encoded_id}/allocations")
        for allocation in allocations:
            if allocation.get("ClientStatus") != "running":
                continue
            current_cpu = current_mem = recommended_cpu = recommended_mem = 0
            tasks = (allocation.get("AllocatedResources") or {}).get("Tasks") or {}
            for task_name, resources in tasks.items():
                task_instances += 1
                cpu = int(((resources.get("Cpu") or {}).get("CpuShares")) or 0)
                mem = int(((resources.get("Memory") or {}).get("MemoryMB")) or 0)
                # Prefer an exact job/task row (the per-stand report), then fall
                # back to the normalized service row (the merged report).
                recommendation = recommendations.get((allocation["JobID"], task_name))
                if recommendation is None:
                    recommendation = recommendations.get(
                        normalized_key(allocation["JobID"], task_name)
                    )
                if recommendation is None:
                    missing += 1
                    rec_cpu, rec_mem = cpu, mem
                else:
                    rec_cpu = recommendation["cpu"] if recommendation["cpu"] is not None else cpu
                    rec_mem = recommendation["mem"] if recommendation["mem"] is not None else mem
                changed_cpu += rec_cpu != cpu
                changed_mem += rec_mem != mem
                current_cpu += cpu
                current_mem += mem
                recommended_cpu += rec_cpu
                recommended_mem += rec_mem
            item = {
                "id": allocation["ID"],
                "job": allocation["JobID"],
                "group": allocation["TaskGroup"],
                "cpu": recommended_cpu,
                "mem": recommended_mem,
            }
            items.append(item)
            placed = per_node[node["ID"]]
            placed["current_cpu"] += current_cpu
            placed["current_mem"] += current_mem
            placed["recommended_cpu"] += recommended_cpu
            placed["recommended_mem"] += recommended_mem
            placed["allocations"] += 1

    cpu_cap = min(node["NodeResources"]["Cpu"]["CpuShares"] for node in nodes)
    mem_cap = min(node["NodeResources"]["Memory"]["MemoryMB"] for node in nodes)
    total_cpu = sum(item["cpu"] for item in items)
    total_mem = sum(item["mem"] for item in items)
    lower_bound = max(math.ceil(total_cpu / cpu_cap), math.ceil(total_mem / mem_cap))
    feasible = None
    packed = None
    for count in range(lower_bound, len(nodes) + 1):
        result = pack(items, count, cpu_cap, mem_cap)
        if result is not None:
            feasible, packed = count, result
            break

    names = {node["ID"]: node["Name"] for node in nodes}
    current_cpu = sum(value["current_cpu"] for value in per_node.values())
    current_mem = sum(value["current_mem"] for value in per_node.values())
    output = {
        "eligible_ready_nodes": len(nodes),
        "node_capacity": {"cpu_mhz": cpu_cap, "memory_mib": mem_cap},
        "running_allocations": len(items),
        "task_instances": task_instances,
        "recommendation_coverage": {
            "missing_task_instances": missing,
            "changed_cpu_instances": changed_cpu,
            "changed_memory_instances": changed_mem,
        },
        "current_reservations": {"cpu_mhz": current_cpu, "memory_mib": current_mem},
        "recommended_reservations": {"cpu_mhz": total_cpu, "memory_mib": total_mem},
        "capacity_lower_bound_nodes": lower_bound,
        "packing_estimate_nodes": feasible,
        "theoretical_removable_nodes": len(nodes) - feasible if feasible else None,
        "per_node_at_current_placement": {
            names[node_id]: values for node_id, values in per_node.items()
        },
        "packed_nodes": packed,
        "limitations": [
            "CPU/memory reservations only",
            "does not model constraints, affinities, CSI/host volumes, ports, or disk",
            "first-fit-decreasing is a heuristic, not a Nomad scheduler plan",
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
