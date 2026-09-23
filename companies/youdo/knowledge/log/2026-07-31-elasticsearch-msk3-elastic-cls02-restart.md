---
system: elasticsearch
status: verified
checked: 2026-07-31
tags: [incident, elasticsearch6, java-heap, oom, docker, heap-dump, gc]
---
# Elasticsearch 6 restart on msk3-elastic-cls02 (2026-07-31)

## Task

Explain the automatic restart of the Elasticsearch container on `msk3-elastic-cls02` on 2026-07-31.

## Context

- Date: 2026-07-31, Europe/Moscow.
- Host: `root@msk3-elastic-cls02.youdo.corp` (`172.24.0.32`).
- Service: Elasticsearch 6.8.23, Docker container `elasticsearch`.
- Compose project: `es6`.
- Compose file and working directory: `/opt/es6/docker-compose.yml`, `/opt/es6`.
- Persistent data: `/data/data-es6`.
- Logs and GC logs: `/data/logs-es6`.
- Cluster: `elastic-new-six`; discovery nodes `172.24.0.31`, `.32`, `.33`.
- HTTP/transport ports: `9201`/`9301`.

## Findings

### Incident summary

The container restarted automatically at `2026-07-31 11:05:24 MSK` because the
Elasticsearch JVM exhausted its configured 16 GiB Java heap. This was an
in-process Java heap OOM, not a Linux kernel/cgroup OOM, manual restart, Docker
daemon restart, or host reboot.

### Evidence

- Docker state after the incident:
  - container ID `89763433b9354168d9cba2a5641c93d8d24e3155b609761da71060aae86d95f2`;
  - `RestartCount=1`;
  - previous finish `2026-07-31T08:05:23.851623548Z`;
  - exit code `127`;
  - `OOMKilled=false`;
  - restart policy `always`;
  - Docker journal says `manualRestart=false`.
- Elasticsearch log:
  - first visible `java.lang.OutOfMemoryError: Java heap space` at
    `11:04:27.825 MSK`;
  - fatal OOMs in Netty request threads at `11:05:21 MSK`;
  - `ElasticsearchUncaughtExceptionHandler` exited the JVM.
- GC log `/data/logs-es6/gc.log.18`:
  - repeated Full GC and GC overhead immediately before exit;
  - heap stayed around `16225M` after Full GC with a `16384M` maximum;
  - final heap usage was `16666613K`;
  - around 910 G1 humongous regions were retained;
  - final Full GCs reclaimed almost nothing.
- A heap dump was generated at `/data/data-es6/java_pid1.hprof`:
  - timestamp `2026-07-31 11:05:16 MSK`;
  - size about 16.46 GB;
  - generation paused the JVM for about 48.3 seconds.
- No OOM killer / killed-process records were found in the kernel journal.
- The host had not rebooted (`uptime` about 50 days) and the Docker daemon stayed
  running.

### Current state after restart

At approximately `11:45 MSK`:

- cluster health was `green`;
- 3/3 data nodes were present;
- 966 active shards, none unassigned or initializing;
- no pending cluster tasks;
- local heap was about 4.8 GB / 16 GB (27%);
- breakers had not tripped and thread-pool rejection counters were zero.

### Conclusion

Immediate root cause: Java heap exhaustion in Elasticsearch 6.8.23 caused the
JVM to terminate with exit code 127. Docker then restarted the container because
`restart: always` is configured.

The exact retaining object / originating query or indexing request is not
provable from ordinary logs alone. The retained heap contained a large amount
of humongous allocation (roughly 7.1 GiB in 910 x 8-MiB regions), while total
live heap approached 16 GiB. The preserved heap dump is the artifact needed to
identify the dominant object graph and likely request/workload.

## Open items

- Analyze `/data/data-es6/java_pid1.hprof` with Eclipse MAT on a machine with
  enough disk and RAM; inspect Leak Suspects and dominator tree. Treat the dump
  as sensitive because heap dumps can contain request and document data.
- Do not remove the heap dump until analysis/retention is agreed. It currently
  consumes about 16.46 GB, while `/data` had about 705 GB available.
- Check monitoring/history for heap growth, request volume, expensive
  aggregations/searches and bulk indexing immediately before `11:04 MSK`.
- Add/verify alerts for sustained old-gen/heap pressure and GC overhead before
  the node reaches OOM.
- Elasticsearch 6.8.23 is legacy; plan an upgrade and review request circuit
  breaker behavior and workload limits.

## Actions

Diagnostic commands used:

```bash
docker inspect elasticsearch
docker events --filter container=elasticsearch
journalctl -u docker
journalctl -k
docker logs --timestamps elasticsearch
tail /data/logs-es6/gc.log.18
curl http://127.0.0.1:9201/_cluster/health
curl http://127.0.0.1:9201/_nodes/_local/stats/jvm,breaker,thread_pool
```

SSH note: the saved hostname key matched, but the saved key for IP
`172.24.0.32` differed. Diagnostics used `CheckHostIP=no` while retaining
hostname host-key verification; `known_hosts` was not changed.

## Portable lesson

`~/ai/general/knowledge/elasticsearch/java-heap-oom-vs-docker-oomkilled.md`
