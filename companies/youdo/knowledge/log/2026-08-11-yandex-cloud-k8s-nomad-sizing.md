---
system: yandex-cloud
status: hypothesis
checked: 2026-08-11
tags: [managed-kubernetes, kube-test, sizing, nomad-test, capacity, victoriametrics, autoscaling]
---
# Sizing kube-test from the actual load of Nomad yandex-test

Date: 2026-08-11 (Europe/Moscow)

## Task

Select worker nodes for the new Yandex Managed Kubernetes cluster `kube-test`, to which as many
services as currently run in Nomad `yandex-test` are planned to be moved. The sizing is a
recommendation based on a partial (64.5-hour) metrics window; the measurements are verified, the
recommended shapes are a plan.

## Context and sources

- Goal: choose worker nodes of the new Yandex Managed Kubernetes `kube-test`, to which the same number of services as currently run in Nomad `yandex-test` is planned to be migrated.
- Nomad API access: variables `NOMAD_YANDEX_TEST_ADDR` and `NOMAD_YANDEX_TEST_TOKEN` in `~/ai/current/.env`; values are not recorded.
- Checks were performed read-only through the Nomad API, SSH as `root` to the client nodes, and PromQL against the internal VictoriaMetrics.
- A 10-day window was requested, but VictoriaMetrics is configured with `--retentionPeriod=2d`. In practice 741–742 points at a 5-minute step were available for 2026-08-08 22:10 UTC — 2026-08-11 14:40 UTC (about 64.5 hours).
- Mimir was found (`grafana/mimir:2.16.1`, multitenancy disabled), but the vmagent remote-write filter keeps only `youdo.*` there; `nomad_client_*` metrics do not reach it. There are no local sysstat archives on the inspected client node.
- At the user's request CSI volumes are excluded from the current sizing; persistent storage needs a separate migration plan.

## Findings

### Current Nomad

- 10 ready/eligible client nodes: `nomad-agent-test-01` ... `nomad-agent-test-010`.
- Each client node: 16 vCPU, about 78.5 GiB RAM, root disk about 91.4 GiB.
- Total physical capacity: 160 vCPU and 785.4 GiB RAM.
- Jobs: 408 running service, 3 running system, 1 running batch; there are also pending/dead jobs.
- Current API snapshot: 550 running allocations; SSH snapshot: about 1270 running Docker containers in total.
- Root disks of the current clients are about 32–80% full. `/var/lib/docker` takes about 13–55 GB/node, `/var/lib/nomad/alloc` about 1.9–8.9 GB/node. A large share of the disk is image/cache/churn, not application persistent data.

### Actual consumption over the available window

| Metric | Avg | P95 | P99 | Max |
|---|---:|---:|---:|---:|
| Host CPU, cores | 15.13 | 18.77 | 22.72 | 32.37 |
| Allocation CPU, cores | 17.98 | 22.06 | 23.74 | 33.75 |
| Host memory used, GiB | 313.39 | 335.22 | 335.65 | 336.14 |
| Allocation memory used, GiB | 281.77 | 305.15 | 308.90 | 310.03 |
| Allocation memory reserved, GiB | 561.96 | 598.21 | 598.70 | 603.41 |

- Actual allocation RAM at p95 is about 51% of reservations: 305 GiB versus 598 GiB.
- `nomad_client_allocs_cpu_allocated` is measured in MHz. At a frequency of about 1995 MHz/core the p95 reservation corresponds to roughly 139 cores; the actual p95 is about 22 cores, i.e. the reservation is overstated roughly 6.3 times.
- The load is memory-bound. CPU does not determine the number of workers; the constraints are RAM, pod density and N+1.
- Largest memory jobs by p95: `youdo-test12` 10.4 GiB; `youdo-autotest01` 8.8; `youdo-test16` 8.7; `youdo-test14` 8.6; `youdo-test9` 7.5; `alloy` 7.2; the remaining `youdo-test*` are usually 6–7 GiB. Elasticsearch instances are about 3.7–4.0 GiB p95.
- CPU leader is `alloy`: about 4.5 cores p95 and 5.3 max. The remaining jobs are considerably smaller; short peaks of individual services reach roughly 1–3 cores.

## Recommended kube-test configuration

### Control plane

- Zonal master, single instance (`etcd_cluster_size = 1`) — acceptable for test stands with an accepted downtime risk.
- Kubernetes `1.34`, release channel `STABLE`.
- For a large number of objects/pods the minimum master preset `s-c4-m16` (4 vCPU / 16 GiB) is recommended, even with a single master.

### Main worker node group

- Platform: `standard-v3`.
- One worker: 8 vCPU, 48 GiB RAM, core fraction 100%.
- Boot disk: at least 100 GB; 128 GB `network-ssd` recommended. The current 32 GB is insufficient for the image cache and churn of a large number of .NET/test containers.
- Autoscaling: min 10, initial 12, max 16 nodes.
- NAT/public IP: false; subnet `ru-central1-b` / `subnet-test`.
- Preemptible: false for the main group.

Raw capacity:

- min 10: 80 vCPU / 480 GiB;
- initial 12: 96 vCPU / 576 GiB;
- max 16: 128 vCPU / 768 GiB.

After system/kube reserved, the reference allocatable RAM for a 48 GiB node is about 44–45 GiB. With 10 nodes that is 440–450 GiB, which covers the allocation p95 of 305 GiB, Kubernetes/platform overhead and roughly 25–30% headroom. Losing one node leaves about 396–405 GiB allocatable. Initial 12 was chosen because of pod density: there are currently about 1270 running containers, and the actual number of Kubernetes pods depends on whether Nomad task groups are migrated as multi-container pods or as separate Deployments.

### Requests/limits

- Do not carry Nomad reservations over directly.
- Memory request: base it on the p95 of the specific task/service over a representative window plus 10–20%; memory limit — p99/max plus 20–30% and the minimum required by the runtime/GC.
- CPU request: base it on p95 plus a small margin; either do not set a CPU limit for test workloads, or set it considerably above the request so that short peaks are not throttled.
- Before the mass migration define namespace quotas/LimitRanges and introduce container metrics collection in the new Kubernetes.

## Alternatives

- Cheaper start: min 8 / initial 10 / max 16 with the same 8 vCPU / 48 GiB shape. It passes on RAM, but N+1 is worse and it may immediately hit pod capacity; not recommended as the main baseline.
- Larger nodes (for example 16 vCPU / 96 GiB) reduce the number of VMs but increase the blast radius and pod density; for test stands with many small services this is worse than 8/48.

## Open items

1. The result is based on roughly 64.5 hours, not the full 10 days. For final optimization, increase the retention of Nomad infrastructure metrics to at least 10–14 days and repeat the calculation.
2. Before apply, check the Yandex folder quotas for cores, RAM, instance groups and disks: the initial profile requires 96 vCPU and 12 workers simultaneously with the temporary cluster.
3. Check the expected number of Kubernetes pods and `maxPods`/pod CIDR. If ~1270 containers are migrated as separate pods, initial 12 may be the lower bound, and the autoscaler must be able to grow to 14–16 nodes.
4. Persistent CSI data, ingress/LB, Vault/monitoring and Helm workloads must be migrated and verified separately before deleting `test-k8s-temp`.
5. Terraform sizing has not been changed yet; plan/apply were not run at the user's request.

## Changes: configuration chosen by the user

After the analysis the user chose a more gradual service launch:

- worker: 8 vCPU / 50 GiB RAM, core fraction 100%;
- platform in the current Terraform: `standard-v2`;
- boot disk: 93 GB `network-ssd-nonreplicated`;
- node autoscale: min=1, initial=1, max=10;
- master remains zonal single-master;
- Kubernetes `1.34`, channel `STABLE`.

The change was made in `/home/slnnk/git/yandex-tf/test-k8s/k8s-cluster.tf`, `terraform validate` succeeded. Plan/apply were not run.

Important: the Yandex Managed Kubernetes Cluster Autoscaler grows the node group when there are pods that cannot be scheduled according to Kubernetes resource requests/constraints. `scale_policy.auto_scale` has no target utilization for CPU/RAM and does not support a setting such as "scale when 15% of resources are free". The required 15% headroom has to be provided by correct requests and, if necessary, Kubernetes overprovisioning/placeholder pods; this mechanism has not been added yet.

With max=10 the raw capacity is 80 vCPU / 500 GiB RAM. By measured RAM this is sufficient, however the approximately 1270 current Nomad containers may hit Kubernetes pod density/maxPods before RAM. Before migrating all stands, the actual number of pods after the move must be checked; if one Nomad task becomes a separate pod, max=10 may turn out to be insufficient.

## Portable lesson

none
