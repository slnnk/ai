---
system: sc-except
status: verified
checked: 2026-06-15
tags: [mssql, sc-except01, YouDoLogsExceptions, load, sqlcmd]
---
# sc-except DB state

## Task

Check the state of SQL Server on `sc-except01.youdo.corp` (2026-06-15 08:57 UTC).

## Context

- Context: checked SQL Server on `sc-except01.youdo.corp`
- Access path: `root@sc-except01.youdo.corp` -> `docker exec data-mssql-1` -> `sqlcmd`
- Secret source: `~/ai/current/.env` (`SC_EXCEPT01_MSSQL_SA_PASSWORD`)
- Related: `2026-06-13-sc-except-mssql-unavailable.md`

## Actions

### What was checked

- SQL Server version and liveness.
- Current user session count.
- Active request count and top long-running requests.
- Database states from `sys.databases`.

### Commands used

- `bash ~/ai/current/scripts/mssql_queue_snapshot.sh`
- Direct `sqlcmd` queries against the containerized SQL Server.

## Findings

- SQL Server is up and responding.
- Version reported: Microsoft SQL Server 2017 (RTM-CU15) 14.0.3162.1 on Linux.
- User sessions: 1070.
- Active requests: 908.
- Top requests are `UPDATE` statements in `runnable` state with no blocking session shown.
- Databases are `ONLINE`.
- Target database `YouDoLogsExceptions` is `ONLINE`, `MULTI_USER`, `SIMPLE`, read/write.

### Interpretation

- No sign of database outage, suspect state, or read-only mode.
- Current symptom is load/queue pressure rather than availability failure.
- The initial lightweight snapshot script needs a syntax cleanup if reused, but the underlying instance is healthy.

### Follow-up: latest exception rows

- The `YouDoLogsExceptions.dbo.Exceptions` table contains recent rows that match the UI screenshot.
- Latest visible rows are `Test Exception` events from multiple apps, including:
  - `Escrow.Tinkoff.Worker`
  - `YouDo.Web.MvcApplication`
  - `YouDo.Finance.Service`
  - `YouDo.Content`
  - `Youdo.Seo.Service`
  - `YouDo.Mailer.Scheduler`
  - `YouDo.Web.Api`
  - `YouDo.API`
- This looks like deliberate test traffic rather than a database storage fault.

## Open items

- If the goal is to diagnose the queue, inspect the source workload generating the `UPDATE` requests.
- If needed, sample `sys.dm_exec_requests` joined to SQL text and host/session metadata for the long-running updates.

## Portable lesson

none
