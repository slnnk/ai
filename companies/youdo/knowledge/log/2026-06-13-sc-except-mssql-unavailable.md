---
system: sc-except
status: verified
checked: 2026-06-13
tags: [mssql, incident, sc-except01, vm.max_map_count, OutOfMemoryException, DBCC, zabbix]
---
# sc-except01 MSSQL unavailable investigation

## Task

Investigate the Zabbix alert `PROBLEM TRIGGER MSSQL: Service is unavailable, port 1433 down`, original problem ID 89429609, on `sc-except01.youdo.corp` (2026-06-13).

## Context

- Host: sc-except01.youdo.corp
- MSSQL runs as Docker Compose service `mssql` in `/data/docker-compose.yml`, container `data-mssql-1`, image `mcr.microsoft.com/mssql/server:2017-CU15-ubuntu`.

## Findings

Summary:
- At investigation time only `data-logreader-1` was running; `data-mssql-1` was stopped with `Exited (1)`.
- Docker event: `data-mssql-1` died at 2026-06-13 02:43:00 UTC (05:43:00 MSK) with exitCode=1. The alert around 05:35 MSK matches the MSSQL crash window.
- SQL Server crash time in dump: 2026-06-13 02:33:49 UTC. Crash id: 928dffdc-2d2c-47d3-9ae0-720c7a926dd2.

Evidence:
- `ss -ltnp`: port 1433 was not listening; port 9900/logreader and 10050/zabbix were listening.
- `docker ps -a`: `data-mssql-1` exited; `data-logreader-1` up.
- `docker inspect`: MSSQL container had no Docker memory limit, no restart policy, OOMKilled=false.
- SQL logs contained many `Not enough storage is available to process this command` read warnings for `/var/opt/mssql/data/YouDoLogsExceptions.mdf`, followed by fatal `Unhandled Exception: OutOfMemoryException`.
- SQL errorlog contained Error 701 `There is insufficient system memory in resource pool internal to run this query`.
- Crash info showed `VMA Count: 65532`, `VMA Limit: 65530`, `Percent VMA Used: 100`, with host/container `vm.max_map_count = 65530`.
- Current disk was not full: `/data` 49G total, 23G used, 25G available; root 15G total, 13G used, 1.9G available.
- Database files in `/data/data`: `YouDoLogsExceptions.mdf` about 22.4G, `YouDoLogsExceptions.ldf` about 679M.

Conclusion:
- Immediate cause of alerts: MSSQL TCP port 1433 is down because Docker container `data-mssql-1` crashed and was not restarted automatically.
- Root technical cause found in SQL crash metadata: SQL Server exhausted process VMA mappings at the default `vm.max_map_count=65530`, then hit internal memory errors and crashed with OutOfMemoryException. This is not a host disk-full condition and not a kernel OOM kill.
- There is possible data integrity risk because SQL logged repeated MDF read failures and explicitly recommended DBCC CHECKDB.

Recommended next steps (as written at investigation time):
- Restore service deliberately: start `data-mssql-1` only with owner approval, then verify 1433 and application behavior.
- Before or immediately after restart, raise `vm.max_map_count` persistently for this host (common mitigation for MSSQL on Linux/container workloads) and consider setting MSSQL max server memory / Docker memory policy.
- Run DBCC CHECKDB for `YouDoLogsExceptions` after MSSQL is online.
- Add restart policy for compose service or alert/runbook for stopped container state.
- Review Zabbix SQL stored procedures and LogReader workload, because errorlog had high spid numbers and internal memory pressure before the crash.
- Move secrets from `/data/docker-compose.yml` and Zabbix scripts to a secret store or environment file with restricted access; do not duplicate secret values in notes.

## Actions and changes

Update 2026-06-13:
- User raised `vm.max_map_count` to 262144 and restarted MSSQL container before DBCC.
- Verified `data-mssql-1` running and port 1433 listening.
- Ran read-only diagnostic check: `DBCC CHECKDB ([YouDoLogsExceptions]) WITH NO_INFOMSGS, ALL_ERRORMSGS;` via sqlcmd inside `data-mssql-1`.
- Result from MSSQL errorlog: `DBCC CHECKDB (YouDoLogsExceptions) WITH all_errormsgs, no_infomsgs executed by sa found 0 errors and repaired 0 errors. Elapsed time: 0 hours 15 minutes 35 seconds.`
- Container remained running after the check; port 1433 remained listening.

Update 2026-06-13 CPU load:
- After MSSQL restart and DBCC, CPU remained high because `sqlservr` was processing many concurrent client requests, not because of DBCC.
- Snapshot at about 08:03 UTC: top showed `sqlservr` up to ~180% CPU on 2 vCPU; docker stats showed MSSQL memory about 4.6GiB and LogReader container near idle.
- SQL DMV snapshot: about 523 active requests and 608 user sessions. Most active requests were `UPDATE`/`DELETE` in `YouDoLogsExceptions`, many suspended on lock waits (`LCK_M_S`, `LCK_M_IU`, `LCK_M_U`, `LCK_M_IX`) with blocking sessions changing quickly.
- Identified request text from `logreader` / `.NET SqlClient`: `Delete From Exceptions Where GUID = @guid And ApplicationName = @ApplicationName`.
- Interpretation: CPU/load alerts after recovery are caused by a thundering-herd/backlog of LogReader/application SQL writes/deletes and lock contention after MSSQL came back, plus SQL using both vCPUs to catch up. This is related to the outage but separate from the original VMA exhaustion crash.

## Access

Credentials note:
- MSSQL SA password for `sc-except01.youdo.corp` was found in `/data/docker-compose.yml` as `SA_PASSWORD`.
- Per explicit user request, the value was saved only in `~/ai/current/.env` as `SC_EXCEPT01_MSSQL_SA_PASSWORD`.
- Do not duplicate the secret value in Markdown notes, logs, scripts, or chat output.

## Open items

- Restart policy for the compose service or an alert/runbook for the stopped-container state.
- MSSQL max server memory / Docker memory policy.
- Review of Zabbix SQL stored procedures and LogReader workload.
- Move secrets out of `/data/docker-compose.yml` and Zabbix scripts.

## Portable lesson

`~/ai/general/knowledge/mssql/linux-crash-vma-exhaustion-vm-max-map-count.md`
