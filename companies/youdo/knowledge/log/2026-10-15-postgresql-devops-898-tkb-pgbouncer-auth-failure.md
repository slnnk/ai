---
system: postgresql
status: verified
checked: 2026-10-16
tags: [devops-898, tkb, pgbouncer, nomad]
---
# DevOps-898 TKB rollout blocked by empty B2B PgBouncer authentication

## Task

Diagnose user-started TKB `master-267` deployments on test10–test15 in DevOps-898, using GitLab and Nomad evidence only.

## Context

Pipeline 141009/project 535/master d9b750543c1b4f2ab35a3891805ab6eb1f23656c. Ordinary jobs recreate target databases. Previous repository audit found no mandatory source changes.

## Actions

Read six GitLab job traces, Nomad task events and bounded stdout/stderr, and B2B PostgreSQL/PgBouncer configuration via read-only SSH to `youdo@10.18.26.44` with `~/.ssh/id_ed25519` and `sudo -n`.

Prepared `/home/slnnk/ai-data/DevOps-898/tkb-pgbouncer-auth.py`; `python3 -m py_compile` and its default read-only inspection passed. Parent subsequently applied the prepared fix after explicit user approval (`Да, исправить PgBouncer`); no deployment retries performed by this investigation.

## Findings

- GitLab jobs 3229807/test10, 3229815/test11, 3229820/test12 failed at `Run nomad task`, with deployment progress deadline reached. Jobs 3229825/test13, 3229829/test14, 3229833/test15 were canceled while awaiting deployment.
- All six Nomad jobs are dead at master-267. Test10 allocation `188dce37-e1d7-f09a-36a8-f04dfefac0fd` worker stdout reports `Npgsql.PostgresException: 08P01: password authentication failed` during Hangfire PostgreSQL initialization (`Worker.General/SetupExtensions.cs:49`). `Worker.Mock/Program.cs:21` catches the exception without setting failure exit code, explaining exit 0/restart followed by failed allocation. Mock API is stopped downstream.
- All task `ConnectionStrings__default` values target `postgres-b2b.service.vk-test.consul:5433`, role `youdo`, per-stand database, and use identical credential values. Values were compared in memory and never saved.
- PostgreSQL on 5432 has all six target databases; `youdo` has a SCRAM verifier. PgBouncer 1.22.0 PID 43719 listens on 5433, but `/etc/pgbouncer/pgbouncer.ini` has an empty `[databases]`, `auth_type=md5`, no auth_query/auth_user, and `/etc/pgbouncer/userlist.txt` is empty. `/var/log/postgresql/pgbouncer.log` confirms `no such user: youdo` followed by password authentication failures from Nomad clients.
- Pre/post migration logs show `Beginning Transaction` and `Committing Transaction`; legacy migration `CON_STR` uses direct port 5432, explaining different behavior from runtime connection on 5433.
- Required fix is infrastructure configuration; no TKB repository changes identified. Proposed minimal scope: six explicit TKB database mappings to local PostgreSQL 5432, existing PostgreSQL role verifier copied entirely on the server into PgBouncer authfile, reload only; preserve limits and other settings. User approved and parent executed `--apply` successfully: six routes added, existing PostgreSQL verifier copied on-server, reload only, PID 43719 unchanged.

## Changes

Remote changes approved and applied by parent: `/etc/pgbouncer/pgbouncer.ini` six explicit TKB routes, `/etc/pgbouncer/userlist.txt` existing `youdo` SCRAM verifier; root-only backups suffixed `.devops-898-before-tkb-auth`. No PostgreSQL role changes. Source repositories untouched.

Post-apply `/home/slnnk/ai-data/DevOps-898/tkb-pgbouncer-readcheck.py` read current credentials from all six Nomad worker tasks in memory and ran only `SELECT 1` against each target database on both direct 5432 and PgBouncer 5433: all 12 checks passed. Credentials passed via SSH stdin and subprocess environment only; none persisted or printed.

## Risks and limits

Prepared helper is single-use and refuses existing backups or an existing `youdo` auth entry. Configuration/reload was approved and completed; User subsequently explicitly approved both service retries; parent started TKB ordinary jobs 3230094–3230099 for test10–test15, retaining DB recreation. Authentication read-only SQL verification passed; GitLab/Nomad rollout verification remains after authorized retries. PgBouncer `auth_type=md5` supports automatic SCRAM negotiation when the authfile contains a SCRAM verifier in version 1.22.0; app credential compatibility passed live SELECT 1 checks for all six databases. No secrets copied to notes or local helper.

## Portable lesson

none

## Authorized rollout continuation

At 2026-10-15 21:03:56 UTC, TKB retry jobs3230094–3230097/test10–test13 SUCCESS with Nomad running/healthy, restarts0. test14/job3230098 running with new Nomad allocation running/restarts0/health pending; test15/job3230099 pending. Read-only monitor `/home/slnnk/ai-data/DevOps-898/bank-rollout-status.py` saves sanitized current statuses to `tkb-pgbouncer-retry-status.json`. No additional retries or source changes authorized/executed by monitoring agent.

## Final TKB acceptance

2026-10-15 21:06:19 UTC (2026-10-16 Moscow): all six user-approved ordinary retry jobs3230094–3230099/test10–test15 SUCCESS. All six Nomad jobs running, current master-267 allocations healthy=true, restarts0. Verification used GitLab job statuses and Nomad statuses only. Initial failed allocations are historical; current rollout accepted. No repository changes required.
