---
system: youdo-business
status: verified
checked: 2026-10-01
tags: [nomad, hangfire, graceful-shutdown, DevOps-872]
---
# youdo-business worker: hard kill on stop and Hangfire lock timeout on start

## Summary
The worker (Nomad group `svc`, task `youdo-business-worker`) is never stopped gracefully: the
image entrypoint `gitlab-ci-templates/v3/files/dotnet.entrypoint.sh` runs `dotnet $APP_ENTRYPOINT`
as a bash child without `exec`/trap, so SIGTERM is dropped and Nomad SIGKILLs after `kill_timeout`.
MR !3818 (DevOps-872, `kill_timeout` 30s -> 60s) alone only lengthened the stop; fixed in the template on 2026-10-01 (master `7fabb47`), verified on a test stand by the user (2026-10-01). The startup
crash `PostgreSqlDistributedLockException ... hangfire:lock:recurring-job:contract-payments-process-waiting-contract-accept`
is consistent with locks left by a hard kill (hypothesis, not proven: lock table not inspected).

## Task
Assess Greptile review on MR 3818 and the user's hypothesis that bad shutdown causes worker start failures.

## Context
- Pipeline 139823 (master, 2f55a9ac): `step 1 - stop services` 3194282 at 17:56:00-17:56:22 MSK,
  `step 6 - start services` 3194287 at 18:03:40, failed by progress deadline at 18:13:47
  (`svc` 2/2 unhealthy since 18:08:48). Retried: step 1 3194338 at 18:16, step 6 3194472 at 18:20 success.
- `devops/production.hcl` group `svc`: `count = 0`, `shutdown_delay = "30s"`, healthy_deadline 5m, restart delay 25s.
- Images built from `devops/Dockerfile` / `devops/Dockerfile.backend`, `ENTRYPOINT ["./entrypoint.sh"]`
  (copied from the templates repo at build time). `YouDo.Business.Worker/Dockerfile` with direct
  `dotnet` entrypoint is not the one used in CI.
- Hangfire.Core 1.8.23, Hangfire.PostgreSql 1.21.1; storage options only `InvisibilityTimeout = 90 min`
  (`YouDo.Business.Jobs/JobsExtensionMethods.cs`), so `DistributedLockTimeout` = 10 min default.
- Recurring jobs registered via `RecurringJob.AddOrUpdate` in `StartupExtensions.UseRecurringJobs`
  called from `Startup.Configure`; an exception there kills the process.

## Actions
- Read MR discussions and job trace via GitLab API (`GITLAB_YOUDO_TOKEN`).
- Read `v3/files/dotnet.entrypoint.sh` in `sysadmins/devops-tools/gitlab-ci-templates`.
- Reproduced locally: bash PID 1 + child with TERM trap, `docker stop -t 5` -> 5 s, exit 137, trap not run.
- Read Hangfire.PostgreSql 1.21.1 `PostgreSqlDistributedLock.cs`: lock = row in `hangfire.lock`
  (`resource`, `acquired` = client `DateTime.UtcNow`); released only on Dispose; stale rows deleted
  only when `acquired < now - DistributedLockTimeout`; acquire loop polls every 1 s until timeout.

## Findings
- Confirmed: SIGTERM never reaches dotnet (trace shows dotnet as PID 7 under entrypoint.sh).
  Consequences of each stop: in-flight Hangfire jobs killed, their fetched rows invisible for
  90 min (`InvisibilityTimeout`), held lock rows left for up to 10 min, MassTransit consumers cut.
- Greptile point (host ShutdownTimeout 30s default vs kill_timeout 60s) is valid but moot until signals are delivered.
- Hypothesis: stale `recurring-job:*` lock from the hard kill at ~17:56 blocked `AddOrUpdate` at start.
  Does not fully fit: lock should expire ~18:06, yet deployment was unhealthy at 18:08:48. Other
  candidates: lock held by a live process, or `acquired` timestamp offset (Npgsql legacy timestamp
  switch is set in worker Startup). Needs `select * from hangfire.lock` during an incident and Nomad
  events of old allocations (exit 137 / "Sent SIGKILL").

## Changes
- `~/git/gitlab-ci-templates`, branch `DevOps-872-dotnet-signals`, merged to master as `7fabb47` (commit `91e0d91`) on 2026-10-01; DevOps-872 closed: `v3/files/dotnet.entrypoint.sh`
  app branch runs `dotnet $APP_ENTRYPOINT &`, traps TERM and INT and forwards both as SIGTERM, loops
  `wait` until the pid is gone, skips `sleep 10` when stopped by a signal. Migration branch unchanged.
  Tested locally (bash:5, fake dotnet): docker stop -> child gets TERM, graceful, exit 0 in 2 s;
  SIGINT -> same; child exit 143 passed through; crash exit 3 -> exit 3 after `sleep 10`.
- `v2/files/entrypoint.sh` not changed: v2 is unused.

## Open items
- Done: signal forwarding in `v3/files/dotnet.entrypoint.sh` (master `7fabb47`); applies to images built after the merge.
- `v2/files/entrypoint.sh` has the same pattern but v2 is not used (per user, 2026-10-01); no fix needed.
- Shutdown timeouts left at defaults (.NET host 30 s): user decided on 2026-10-01 that 30 s is enough once SIGTERM is delivered.
- Make recurring-job registration at startup tolerant to lock timeouts.

## Portable lesson
[Bash entrypoint as PID 1 does not forward SIGTERM](~/ai/general/knowledge/docker/bash-pid1-no-sigterm-forward.md)
