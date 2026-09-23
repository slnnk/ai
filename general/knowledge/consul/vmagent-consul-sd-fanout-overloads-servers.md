---
system: consul
status: verified
checked: 2026-06-05
tags: [consul, vmagent, prometheus, service-discovery, blocking-query, 429, rpc_max_conns_per_client, cpu]
---
# Consul servers overloaded by Prometheus/vmagent Consul service discovery fan-out

## Symptom

Consul/Nomad server nodes run at high CPU; one becomes unresponsive and needs a reboot,
which helps only briefly. Server logs show, thousands of times, from a peer's address:

```text
agent.server.rpc: rejecting RPC conn from <peer>: rpc_max_conns_per_client exceeded
```

plus gRPC reconnect/cancel warnings on the RPC port `8300`. On the busiest server:

- `consul` holds well over a thousand file descriptors and hundreds of TCP connections on
  `8300`;
- the HTTP API port `8500` has ~1000 connections from one client (the metrics agent
  container);
- vmagent (or Prometheus) logs `cannot obtain Consul serviceNodes` for
  `/v1/health/service/<svc>?wait=300s` and Consul answers HTTP `429 too many concurrent
  connections`;
- Consul telemetry: `consul_api_http_count{path="v1_health_service_"}` in the millions,
  `consul_client_rpc` similar, catalog service count in the thousands.

## Cause

`consul_sd_configs` in vmagent/Prometheus opens one long blocking query
(`/v1/health/service/<name>?wait=...`) per discovered service. With a catalog of several
thousand service names (typical for a test cluster where every environment registers its
own copies), one scraper keeps thousands of concurrent watches open against a single
Consul agent. Each watch costs an HTTP connection, an internal RPC to the servers and a
re-fire on every catalog change. The agent hits `http_max_conns_per_client` (429 to the
scraper), the servers hit `rpc_max_conns_per_client` between themselves, and CPU is spent
serving blocking queries instead of Raft and health checks. Nomad job churn on the same
nodes amplifies the catalog change rate.

## Fix

Reduce the fan-out at the source; raising limits only moves the bottleneck.

1. Narrow discovery so watches are opened only for the services you scrape:

   ```yaml
   consul_sd_configs:
     - server: 127.0.0.1:8500
       services: [nomad, nomad-client, node-exporter]   # explicit list
       # or: tags: [metrics]  /  filter: 'ServiceMeta.metrics == "true"'
   ```

   Relabeling happens *after* the watch is opened, so `relabel_configs` alone does not
   reduce the load.
2. Shorten the blocking query and spread scrapers:
   `-promscrape.consul.waitTime=30s` (vmagent) instead of `300s`; point each scraper at
   its local Consul client agent rather than a server; shard by service list across agents.
3. Avoid duplicate targets (for example scraping both `nomad` and `nomad-client` when they
   expose the same nodes).
4. Consider `limits { http_max_conns_per_client = ... }` and `rpc_max_conns_per_client`
   only as a temporary relief after the fan-out is reduced.
5. Keep per-process CPU history (`sysstat`/`sar` with retention, or a node exporter) so the
   next incident can be attributed without guessing; a host without archives cannot show
   what was hot before a reboot.
6. Ask why the catalog is so large: thousands of service names usually mean environments
   or jobs are not being cleaned up.

## Limits

- Diagnosis relied on `ss -tnp` on ports `8300`/`8500`, Consul `/v1/agent/metrics`, the
  scraper's logs and `docker inspect` to map container IPs; all are read-only.
- Verified with vmagent 1.126 and Consul with `http_max_conns_per_client = 1000`. Prometheus
  behaves the same with `consul_sd_configs`; the flag names differ.
- A cluster with a small catalog (tens of services) does not need these restrictions.
