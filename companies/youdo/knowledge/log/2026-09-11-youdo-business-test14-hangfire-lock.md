---
system: youdo-business
status: verified
checked: 2026-09-11
tags: [nomad, yandex-test, hangfire, postgresql, distributed-lock, rolling-update]
---
# 2026-09-11: youdo-business-test14 allocation failed on Hangfire lock

## Task

Explain why the Nomad allocation of `youdo-business-test14` failed after a rolling update.

## Context

- Environment: Nomad `yandex-test`.
- Job: `youdo-business-test14`, namespace `default`.
- Investigated allocation: `2bb43ed4-7619-eead-96d9-661a01430499`, job version 1.
- Allocation node: `nomad-agent-test-03` (`10.16.26.59`).
- Investigation date: 2026-09-11, MSK.
- Related source repository: `/home/slnnk/git/youdo.business`.
- Recurring-job registration: `YouDo.Business.Worker/StartupExtensions.cs`, method `UseRecurringJobs`.

## Findings

### Verified failure chain

1. The root failed task was `youdo-business-test14-worker`.
2. The worker exited repeatedly with code `134`; Nomad stopped retrying after exceeding the configured restart attempts.
3. Worker stderr contains an unhandled exception:

   ```text
   Hangfire.PostgreSql.PostgreSqlDistributedLockException: Timeout expired.
   The timeout elapsed prior to obtaining a distributed lock on the
   'hangfire:lock:recurring-job:company-subscriptions-commission-minimum-job' resource.
   ```

4. The exception is raised during application startup in:
   - `Hangfire.RecurringJobManager.AddOrUpdate`;
   - `YouDo.Business.Worker.StartupExtensions.UseRecurringJobs`, source line 556 in the deployed build;
   - `YouDo.Business.Worker.Startup.Configure`, source line 283.
5. All other long-running tasks in the allocation were healthy until Nomad reported `Sibling Task Failed` and stopped them. Their exit code `137` is a consequence of allocation teardown, not the primary fault.
6. Migration lifecycle tasks completed with exit code `0`.
7. The same worker failure repeated after rescheduling on allocation `e519014b-5e65-e8c4-6633-afa891228968`.

### Timeline and likely lock owner/lifetime

- Previous healthy version-0 allocation: `a95008f3-757d-88a3-5344-67e2ea20477b`.
- Rolling replacement began at `15:23:16 MSK`.
- The old worker was force-stopped and exited `137` at `15:24:02 MSK`.
- New version-1 workers repeatedly timed out acquiring the same recurring-job lock.
- Allocation `9efc7d5d-f43f-449f-975b-0c592e781496` failed its first worker start at `15:33:51`, then its retry started successfully at `15:34:02` and remained healthy.

Inference (hypothesis): the PostgreSQL-backed Hangfire lock/lease remained unavailable after the previous worker was force-killed during the rolling update. It became available about ten minutes after the old worker exited. The exact lock holder was not queried directly from PostgreSQL, so this is a strongly time-correlated explanation rather than a DB-level proof.

### Current state at investigation time

- A later job submission created version 2 at `15:40:09 MSK`.
- Current allocation: `2dd39d64-2256-709f-11bd-a600a56d7817` on `nomad-agent-test-05` (`10.16.26.7`).
- Job deployment `dbe8fa72` is successful and healthy.
- All service tasks, including `youdo-business-test14-worker`, are running with zero worker restarts.
- No remediation or mutation was performed during this investigation.

### Operational conclusion

Primary cause of allocation `2bb43ed4`: an unhandled Hangfire PostgreSQL distributed-lock timeout while registering `company-subscriptions-commission-minimum-job` during worker startup. This is application/Hangfire lock contention around rolling replacement, not CPU, memory, image-pull, migration, or Nomad-node failure.

## Open items

Recommended follow-up:

- avoid overlapping old/new worker startup registration where possible, or ensure graceful worker shutdown before replacement;
- make recurring-job registration tolerant of `PostgreSqlDistributedLockException` (retry/backoff or non-fatal startup handling);
- inspect Hangfire PostgreSQL distributed-lock settings and lock expiry in the deployed package/configuration;
- during recurrence, query PostgreSQL lock state and sessions before the lease expires to prove the holder;
- do not interpret sibling exit `137` as OOM without an OOM event: here Nomad explicitly killed siblings after worker failure.

## Actions

Read-only commands used:

```bash
nomad alloc status -verbose <alloc-id>
nomad alloc logs -stderr -tail -n 500 <alloc-id> youdo-business-test14-worker
nomad job status -all-allocs youdo-business-test14
```

## Portable lesson

[`~/ai/general/knowledge/dotnet/hangfire-postgresql-distributed-lock-timeout-on-restart.md`](../../../../general/knowledge/dotnet/hangfire-postgresql-distributed-lock-timeout-on-restart.md)
