---
system: nomad-test
status: verified
checked: 2026-09-13
tags: [nomad, capacity, cadvisor, victoriametrics, resource-limits, yandex-test]
---
# Yandex-test Nomad resource optimization table

## Task

Build a per-job/per-task table of configured Nomad resources versus observed cAdvisor usage for the
`yandex-test` Nomad cluster and derive recommended memory/CPU limits, then check whether the
recommendations allow shutting down another Nomad client.

## Context

- Generated: 2026-09-13, Europe/Moscow
- Merged CSV: [`../files/yandex-test-nomad-resource-optimization.csv`](../files/yandex-test-nomad-resource-optimization.csv)
- Interactive HTML: [`../files/yandex-test-nomad-resource-optimization.html`](../files/yandex-test-nomad-resource-optimization.html)
- Per-stand CSV: [`../files/yandex-test-nomad-resource-optimization-by-stand.csv`](../files/yandex-test-nomad-resource-optimization-by-stand.csv)
- Generator: `~/ai/current/scripts/nomad_resource_optimization.py`
- HTML renderer: `~/ai/current/scripts/render_nomad_resource_table.py`
- Sources: live Nomad API (`yandex-test`) and VictoriaMetrics `alloy-cadvisor` history.
- History window: 7 days, MetricsQL subquery step 5 minutes.
- Related: metrics route and retention for these containers are documented in
  `2026-09-13-monitoring-yandex-test-nomad-container-metrics.md`.

## Findings

### CSV contract

The CSV columns are exactly:

1. `Nomad job`
2. `Nomad task`
3. `Nomad mem limit`
4. `Nomad max mem limit`
5. `Nomad cpu limit`
6. `Peak mem usage`
7. `Peak cpu usage`
8. `AVG mem usage`
9. `AVG cpu usage`
10. `Recommended mem limit`
11. `Recommended max mem limit`
12. `Recommended cpu limit`

Memory values are numeric MiB. CPU values are numeric MHz. Empty usage and recommendation cells mean there was insufficient matching cAdvisor history; they must not be interpreted as zero.

The primary snapshot contains 213 merged service/task rows built from 1,343 unique current per-stand job/task pairs in 329 active Nomad jobs. All job specs were fetched successfully. Fifty `dead` jobs were excluded. In the merged CSV, memory history exists for 185 rows and CPU history for 198; recommendations pass the evidence/lifecycle gates for 156 memory rows and 155 CPU rows.

Test stands are normalized only when the Nomad job ends with `-test` or `-testN`: `antifraud2-test`, `antifraud2-test1`, ..., `antifraud2-test15` become job `antifraud2`. The corresponding token is removed from task names, so `antifraud2-api-test14` becomes `antifraud2-api`. Names such as `testlink` or `contest-service` are unchanged.

For a merged row:

- current Nomad memory/CPU values are the maximum configured value across current stands;
- peak and hidden P95 usage are the maximum across stands;
- AVG usage is weighted by the number of historical samples per stand;
- short lifecycle hooks such as pre/post migrations retain usage columns but receive no automatic recommendation.

If the same task name is present in multiple task groups of one job, the table intentionally merges it into one job/task row and uses the largest current resource values. Historical cAdvisor labels identify job and task but the requested CSV schema has no task-group column.

### Usage calculations

- Peak memory: temporal maximum of the maximum per-container `container_memory_working_set_bytes` for the job/task.
- Average memory: temporal average of the per-container average working set for the job/task; merged service averages are weighted by sample count.
- Peak CPU: temporal maximum of the maximum per-container five-minute rate of `container_cpu_usage_seconds_total`.
- Average CPU: temporal average of the per-container average five-minute CPU rate; merged service averages are weighted by sample count.
- cAdvisor CPU cores are converted to Nomad MHz with 1 core = 1,999 MHz, matching the current Nomad clients (`31,984 MHz / 16 cores`).
- Internally the generator also calculates P95 of the maximum observed instance for each job/task; P95 is used for recommendations but is omitted from the CSV because it was not part of the requested column contract.

### Recommendation formulas

- Recommended memory reservation: round up to 16 MiB from `max(64 MiB, P95 × 1.20, average × 1.50)`.
- Recommended maximum memory: round up to 64 MiB from `max(128 MiB, peak × 1.20, recommended reservation)`. The reservation already has its own safety margin, so it is not multiplied again.
- Recommended CPU reservation: round up to 50 MHz from `max(50 MHz, P95 × 1.25, average × 1.50)`.

### Capacity check (2026-09-13)

The cluster had 7 ready/eligible clients, each exposing 31,984 MHz CPU and
80,425 MiB memory. Applying the merged table as one common set of limits to all
test stands would produce approximately 175,440 MHz CPU and 551,468 MiB memory
reservations for the running allocations. CPU fits on 6 clients, but memory
requires all 7: six clients provide only 482,550 MiB, a deficit of 68,918 MiB.

The merged recommendations are deliberately based on the maximum P95 among
stands. Reusing that maximum for every stand multiplies the reservation of the
heaviest stand across all instances and is unsuitable as-is for node-count
reduction. The per-stand recommendations total about 142,140 MHz and 460,700
MiB; this is a theoretical six-node fit by totals with only about 4.5% memory
headroom, while the allocation-level packing heuristic did not find a six-node
placement. Therefore neither variant currently justifies shutting down another
node safely. A next iteration should derive a soft reservation from the pooled
cross-stand distribution while retaining a hard maximum based on the global
peak.

These are review candidates, not changes approved for automatic rollout. A seven-day window can miss monthly jobs, exceptional traffic and failure modes. Before changing a job, inspect restarts/OOM events, longer application-level history where available, concurrency, startup spikes, GC behavior and downstream latency. Roll changes out in batches and validate through Nomad deployment health and cAdvisor metrics.

Recommendations require at least 24 five-minute historical samples per representative stand (two hours of observations) and are suppressed for Nomad lifecycle tasks. Usage may still be shown when this gate is not satisfied.

Memory oversubscription is enabled in the current Nomad scheduler, so `memory` is treated as the normal reservation when `memory_max` is set and `memory_max` is the burst ceiling. Nomad `CPU` is primarily a scheduler reservation/share; workloads may burst when the host has idle CPU.

## Actions

### Rebuild command

```bash
set -a
. ~/ai/current/.env
set +a
python3 ~/ai/current/scripts/nomad_resource_optimization.py \
  --output ~/ai/current/knowledge/files/yandex-test-nomad-resource-optimization.csv
```

Add `--keep-test-stands` and write to `yandex-test-nomad-resource-optimization-by-stand.csv` to rebuild the detailed source table.

Use `--days`, `--step`, and `--mhz-per-core` to change the observation window or calculation assumptions. VictoriaMetrics is currently configured for a seven-day retention window for `container_*`; Mimir does not receive these metrics.

## Open items

- Recommendations are review candidates only; no Nomad job was changed.
- Neither the merged nor the per-stand variant justifies shutting down another client; a next iteration should use a pooled cross-stand distribution for the soft reservation and the global peak for the hard maximum.

## Portable lesson

none
