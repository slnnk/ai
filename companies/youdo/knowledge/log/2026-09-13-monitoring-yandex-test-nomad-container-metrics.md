---
system: monitoring
status: verified
checked: 2026-09-13
tags: [victoriametrics, cadvisor, alloy, mimir, zabbix, nomad-test, retention, promql]
---
# Yandex-test Nomad: historical container metrics

## Task

Determine where historical CPU/RAM metrics for containers running on the `yandex-test` Nomad
clients are stored, which retention applies, and pull a verified seven-day usage slice for the
capacity analysis of that cluster.

## Context

- Check date: 2026-09-13, Europe/Moscow
- System: Nomad clients `nomad-agent-test-*`, datacenter `yandex-test`
- IaC: `/home/slnnk/git/infra-tf/dev/victoriametrics.tf`, scrape config `/home/slnnk/git/infra-tf/dev/config/vmagent.yml`

## Findings

### Verified metrics route

`Alloy/cAdvisor on the Nomad clients` → scrape job `alloy-cadvisor` in `vmagent.dev.youdo.corp` → remote write to VictoriaMetrics `vminsert` → queries through `http://vmselect.dev.youdo.corp/select/0/prometheus`.

- `vmagent` is a collector/forwarder and does not store history itself.
- Prometheus-compatible query API: `http://vmselect.dev.youdo.corp/select/0/prometheus/api/v1`.
- Grafana ingress: `http://grafana.dev.youdo.corp` (the datasource may be stored in the Grafana DB; no static datasource provisioning configuration was found in the repository).
- Primary remote write in IaC: internal `vmcluster-victoria-metrics-cluster-vminsert.victoriametrics.svc.cluster.local:8480/insert/0/prometheus`.
- In IaC, vmstorage is configured with `retention = "7d"`, PVC `10Gi`, a single vmstorage. At the time of the check the query API returned container data from at least `2026-09-04 08:00 UTC`, i.e. more than 9 days. Only the configured 7-day window should be treated as guaranteed: physical deletion of old storage parts may happen later.

### Available data and labels

Confirmed metrics:

- `container_cpu_usage_seconds_total`
- `container_memory_working_set_bytes`

For Nomad container series the available labels include:

- `job="alloy-cadvisor"`, `dc="yandex-test"`, `cluster="k8s-dev"`
- `node="nomad-agent-test-XX"`
- `container_label_com_hashicorp_nomad_alloc_id`
- `container_label_com_hashicorp_nomad_job_id`
- `container_label_com_hashicorp_nomad_namespace`
- `container_label_com_hashicorp_nomad_node_id`, `container_label_com_hashicorp_nomad_node_name`
- `container_label_com_hashicorp_nomad_task_group_name`, `container_label_com_hashicorp_nomad_task_name`
- `service_name`, `name`, `image`, `component`, `owner` (not present on every series)

Verified PromQL/MetricsQL:

```promql
sum(rate(container_cpu_usage_seconds_total{job="alloy-cadvisor",container_label_com_hashicorp_nomad_alloc_id!=""}[5m]))
```

```promql
sum(container_memory_working_set_bytes{job="alloy-cadvisor",container_label_com_hashicorp_nomad_alloc_id!=""})
```

For a per-node breakdown add `by (node)`, for a per-job breakdown add `by (container_label_com_hashicorp_nomad_job_id)`.

### Verified historical slice

Range query over the last 7 days, step 5 minutes, sum over containers with a Nomad alloc ID only:

| Metric | Average | P95 | Maximum | Latest in slice |
|---|---:|---:|---:|---:|
| Container CPU | 15.37 cores | 22.65 cores | 53.45 cores | 11.52 cores |
| Container working-set RAM | 156.6 GiB | 263.5 GiB | 272.0 GiB | 125.0 GiB |

The range contains gaps caused by stopped/unavailable clients and scrape targets, so the average must not be interpreted as a continuous seven-day average. Peaks and P95 refer only to the samples that were received.

### Scrape state on the check date

- `alloy-cadvisor` and `nomad_telemetry` discover Nomad endpoints through Consul SD.
- Several active client targets were `up`.
- There were also stale/down targets, including Nomad server cAdvisor endpoints (connection refused) and individual client endpoints. Before a capacity decision, check `http://vmagent.dev.youdo.corp/api/v1/targets` and account for the gaps.

### Zabbix

- API: `http://zabbix-test.youdo.corp/api_jsonrpc.php`, Zabbix `6.4.21`.
- The access token is stored only as `ZABBIZ_DEV_TOKEN` in `~/ai/current/.env` (the variable name contains `ZABBIZ`, not `ZABBIX`).
- Searching Zabbix host interfaces by the IPs of current/recently removed Nomad clients `10.16.26.7`, `.33`, `.44`, `.48`, `.54`, `.55`, `.59`, `.62`, `.64` returned nothing.
- Searching item names/keys for `container` returned nothing. On the check date Zabbix is not a source of historical container CPU/RAM for this Nomad group.

### Mimir long-term storage

- Mimir is available for PromQL at `http://mimir.dev.youdo.corp/prometheus/api/v1` and stores blocks in S3.
- `dev/config/mimir-values.yaml` does not set `limits.compactor_blocks_retention_period`; the Mimir default `0` means compactor retention is disabled and blocks are not automatically deleted from object storage.
- `blocks_storage.tsdb.retention_period: 2h` is the retention of the local copy of blocks/WAL in the ingester after shipping to S3, not the retention of long-term data.
- However, the additional remote write from vmagent to Mimir has a URL relabel rule `source_labels=["__name__"], regex="youdo.*", action="keep"`. Therefore Mimir receives only the application metrics `youdo_*`, and cAdvisor `container_*` is not sent there.
- Live Mimir query over a 365-day range: 20 metric names available, all starting with `youdo_`; the first non-empty results appear around 2026-09-05. Queries `count({__name__=~"container_.*"})` for the current instant and for the yearly range returned 0 series.
- Consequence: Mimir is indeed an indefinite long-term storage, but as of 2026-09-13 it holds no historical CPU/RAM metrics of Nomad containers. For those only VictoriaMetrics with the configured `7d` retention is available (physically the API may temporarily return older parts).

## Open items

- Related capacity analysis: see [`2026-09-13-nomad-test-agent-scale-down.md`](2026-09-13-nomad-test-agent-scale-down.md). The actual cAdvisor peaks are noticeably below the total physical capacity, but further scale-down is limited by Nomad scheduler reservations and placement constraints, not only by observed CPU/RAM.
- The per-job resource table built on these metrics is in `2026-09-13-nomad-test-resource-optimization.md`.

## Portable lesson

none
