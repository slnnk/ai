---
system: nomad-test
status: verified
checked: 2026-06-05
tags: [incident, consul, nomad, vmagent, service-discovery, rpc_max_conns_per_client, cpu]
---
# 2026-06-05: nomad-consul-master-test-03 CPU/unavailable incident

## Task

Investigate why Consul/Nomad master `nomad-consul-master-test-03` (`10.16.26.13`) became
unavailable with high CPU and had to be rebooted manually, and find the source of the
ongoing control-plane pressure.

## Context

- Environment: test Consul/Nomad cluster, datacenter `yandex-test`.
- Investigated host: `root@10.16.26.13` (`nomad-consul-master-test-03`), Consul/Nomad master.
- Related peers:
  - `10.16.26.11` - `nomad-consul-master-test-01`
  - `10.16.26.12` - `nomad-consul-master-test-02`
  - `10.16.26.13` - `nomad-consul-master-test-03`
- Incident: host `10.16.26.13` was unavailable and was rebooted manually; provider console showed high CPU.
- Reboot observed: `2026-06-05 11:24 MSK`. Previous boot started `2026-06-02 14:55 MSK`.

## Findings

- On `10.16.26.13`, previous boot Consul logs repeatedly showed:
  - `agent.server.rpc: rejecting RPC conn from because rpc_max_conns_per_client exceeded`
  - all counted instances came from `10.16.26.12`.
- First observed `rpc_max_conns_per_client exceeded` on `10.16.26.13`: `2026-06-02 23:29:34 MSK`.
- Last observed before reboot: `2026-06-05 10:23:39 MSK`.
- Total counted on `10.16.26.13` for previous boot: `2101`, source `10.16.26.12`.
- `10.16.26.13` also had many Consul gRPC reconnect/cancel warnings on port `8300`.
- `10.16.26.13` Nomad logs showed sustained raft snapshots/compactions every few minutes and task churn, including `youdo-business-test12` around `2026-06-05 10:18-10:19`.
- Local sysstat archives were absent under `/var/log/sysstat`, so historical CPU samples could not be recovered from the host.

### Source of current cluster pressure

- `10.16.26.12` is still overloaded after the reboot of `10.16.26.13`.
- On `10.16.26.12`:
  - Consul uptime: since `2026-05-19 19:29 MSK`.
  - Nomad uptime: since `2026-05-19 19:29 MSK`.
  - Current top CPU at investigation time:
    - `nomad` about 33% of one CPU.
    - `vmagent-prod` about 32%.
    - `consul` about 16%.
  - Consul had about `1367` file descriptors.
  - TCP connections involving Consul RPC port `8300`: about `333`, with about `200` against `10.16.26.12` itself and about `103` against `10.16.26.11`.
  - Current Consul logs on `10.16.26.12` also show `rpc_max_conns_per_client exceeded` from `10.16.26.12` itself.
- Docker IP mapping on `10.16.26.12`:
  - `172.17.0.5` = `vmagent` container, image `victoriametrics/vmagent:v1.126.0`.
  - `172.17.0.6` = `consul-exporter`, image `prom/consul-exporter:v0.13.0`.
- HTTP connections to Consul `:8500` on `10.16.26.12` were dominated by `vmagent`:
  - about `1004` from `172.17.0.5`.
  - about `121` from `172.17.0.6`.
- `vmagent` is configured with Consul service discovery and long blocking queries:
  - `--promscrape.consulSDCheckInterval=60s`
  - `--promscrape.discovery.concurrency=1`
  - `--promscrape.consul.waitTime=300s`
- Consul metrics on `10.16.26.12`:
  - catalog service count was about `8930`.
  - `consul_api_http_count{method="GET",path="v1_health_service_"}` was about `12.7M`.
  - `consul_client_rpc` was about `11.7M`.
  - `v1_catalog_services` count was about `46k`.
- `vmagent` logs directly confirmed Consul throttling:
  - many `cannot obtain Consul serviceNodes` errors for `/v1/health/service/<service>?wait=300s`.
  - Consul returned HTTP `429` with "too many concurrent connections".
  - counted `5469` such `429` log entries since `2026-06-05 08:30 MSK`.

### Conclusion

Primary likely cause: Consul/Nomad control-plane overload from very large Consul service discovery fan-out, currently driven mainly by `vmagent` on `10.16.26.12`.

The `vmagent` workload opens long-lived Consul blocking queries per service. With about `8930` Consul service names and `wait=300s`, this creates roughly a thousand concurrent HTTP connections from one container and millions of `health/service` requests over time. This pressure causes Consul HTTP throttling, high Consul CPU/FD usage, high internal Consul RPC volume, and `rpc_max_conns_per_client exceeded` on Consul server RPC port `8300`. `10.16.26.13` was hit by this as a Consul peer and also processed ongoing Nomad raft/task churn.

The reboot of `10.16.26.13` reduced local symptoms but did not remove the underlying source, because `10.16.26.12` continues generating load.

## Open items (recommended next steps)

1. Reduce `vmagent` Consul SD scope:
   - restrict discovered services by tags, names, namespaces, or relabeling before service-level watches are opened if supported by the config;
   - avoid watching all ~8930 services from a single `vmagent`.
2. Lower concurrent pressure:
   - reduce `--promscrape.consul.waitTime` from `300s`;
   - shard Consul SD across agents or point agents to local Consul clients with safe limits;
   - avoid scraping both `nomad` and `nomad-client` when they produce duplicate targets.
3. Consider increasing Consul HTTP limit only as a temporary mitigation:
   - current Consul config has `limits { http_max_conns_per_client = 1000 }`;
   - raising it may hide 429s but increases FD/CPU pressure and does not fix fan-out.
4. Investigate and tune Consul RPC pressure:
   - current RPC limit is hit between Consul servers, especially from `10.16.26.12`;
   - do not only raise `rpc_max_conns_per_client` without reducing the Consul SD load.
5. Add persistent CPU/process telemetry:
   - sysstat exists but no archives were present;
   - enable retention for `sar`/process metrics or use existing monitoring to retain per-process CPU around incidents.
6. Review why Consul catalog contains about `8930` service names in test:
   - high environment/job churn appears to inflate watch cardinality and Nomad raft write rate.

## Portable lesson

[Consul: server overload from Prometheus/vmagent Consul SD fan-out (429, rpc_max_conns_per_client)](../../../../general/knowledge/consul/vmagent-consul-sd-fanout-overloads-servers.md)
