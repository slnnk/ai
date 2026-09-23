---
system: dotnet
status: verified
checked: 2026-09-11
tags: [hangfire, postgresql, distributed-lock, recurring-job, rolling-update, nomad, kubernetes]
---
# Hangfire worker crashes on startup: `PostgreSqlDistributedLockException` on a recurring-job lock

## Symptom

After a rolling redeploy, the new worker instance exits repeatedly (exit code 134,
unhandled exception) with:

```text
Hangfire.PostgreSql.PostgreSqlDistributedLockException: Timeout expired.
The timeout elapsed prior to obtaining a distributed lock on the
'hangfire:lock:recurring-job:<job-id>' resource.
```

Stack: `RecurringJobManager.AddOrUpdate` called from application startup. Sibling containers
in the same allocation/pod die with 137 afterwards (orchestrator teardown), which looks like OOM
but is not. About ten minutes later a retry starts fine.

## Cause

`Hangfire.PostgreSql` implements distributed locks as rows in the `hangfire.lock` table. The
lock is released by the owner; if the previous worker is **force-killed** (SIGKILL after the
stop grace period) while holding the lock during `AddOrUpdate`, the row stays until the
storage's lock timeout/expiry cleanup removes it (default in the 10-minute range,
`DistributedLockTimeout`/`InvisibilityTimeout` depending on version). New instances registering
the same recurring job at startup wait `DistributedLockTimeout` (default 10 s) and throw. The
exception is not caught, so the whole worker process dies and the orchestrator restarts it into
the same wall.

## Fix

- Make registration tolerant: wrap `AddOrUpdate` calls in a retry with backoff, or run
  recurring-job registration in a hosted service after the app is up instead of in `Configure`,
  so a lock timeout does not kill the process.
- Give the old worker a graceful shutdown (`kill_timeout`/`terminationGracePeriodSeconds`
  longer than a registration cycle) and make the server stop before the new one starts
  (`max_parallel = 1` with health checks, or `Recreate` strategy).
- Tune `PostgreSqlStorageOptions.DistributedLockTimeout` upward for startup if registration is
  slow on the DB.
- During an incident, prove the holder instead of waiting: `SELECT * FROM hangfire.lock;`
  and `pg_stat_activity`; deleting the stale row is safe when the owner process is gone.

## Limits

- Exit 137 of sibling tasks is orchestrator teardown; check for an OOM event before treating it
  as memory pressure.
- The time-correlation (lock freed ~10 min after the old worker's SIGKILL) was consistent
  but the lock table was not inspected live; verify on your version.
