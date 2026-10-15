---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [cerberus, pgbouncer, orleans, DevOps-899]
---
# Cerberus test1 direct Nomad pilot through PgBouncer; Orleans startup pending

## Summary

User explicitly requested switching the consumer on test1. Applied a scoped direct Nomad job-spec pilot: three Cerberus workers and API now use PgBouncer port 5433 with No Reset On Close=true; migrations retain direct PostgreSQL 5432. No database recreation and no repository changes. PgBouncer transport works without observed queue, but all three workers restarted after the five-minute Orleans membership activation timeout. Consumer switch completed; sustained runtime startup failed.

## Authorization and context

After the [approved PgBouncer preparation](2026-10-15-postgresql-cerberus-test1-pgbouncer-pool.md), user explicitly said to do the switch on test1. This approved the scoped consumer pilot, not a global rollout or separate stale-membership modification. No repository branch/edit approval was requested or used for this direct runtime pilot. Existing [restart diagnosis](2026-10-15-nomad-test-cerberus-restart-loop-membership.md) remains relevant.

## Actions and changed scope

At 20:32:36 UTC, updated only Nomad job cerberus2-test1 using CAS against source ModifyIndex 16756/version 0. New index 19922/version 1, evaluation b4c62f00-8937-97ef-dd8f-2c7d0ba50693. Plan showed one destructive allocation update. New allocation 5adea323-d524-9790-1c08-b54a951ba605 on 10.18.26.21 started runtime tasks at 20:32:51 UTC.

Changed four runtime PostgreSql assignments inside environment templates, adding Port=5433 and No Reset On Close=true while preserving credentials, database, host and other job settings. Both migration CON_STR values remain direct port 5432. No Ansible deploy/recreate command, DB reset, source edit or other stand change was performed. Local transformation tests checked preservation of the input and migration settings.

Local helpers: `/home/slnnk/ai-data/jenkins-recovery/switch-cerberus-test1-pgbouncer.py` and `/home/slnnk/ai-data/jenkins-recovery/cerberus-pgbouncer-status.py`. Receipts under `/home/slnnk/ai-data/jenkins-recovery/cerberus-pgbouncer-test1/`: pilot-plan.json, pilot-applied.json, pilot-status.json. Raw job templates contain credentials; do not quote them in logs or summaries.

## Initial verification and limits

At 20:33:04 UTC, PgBouncer showed three client connections, one backend server, cl_waiting 0 and 31 queries. PostgreSQL had one local backend for test1 plus the diagnostic connection. Current membership had three Joining silos (status 2), generation 529792372.

Startup still encountered obsolete Active endpoint 10.18.26.38:15001, generation 529792219, last heartbeat 20:30:27 UTC, status 3, with ConnectionRefused. Thus working pooled SQL transport does not itself establish Orleans application readiness.

## Final pilot outcome

At 20:38:23 UTC, the same version-1 allocation 5adea323-d524-9790-1c08-b54a951ba605 still reported Nomad healthy=true, but all three workers had Restarts=1. Worker1 was pending and the other workers had restarted at 20:38:19/20 UTC; API Restarts=0. Worker1 stderr showed OrleansLifecycleCanceled at stage 19999, System.TimeoutException, MembershipOracle activating failed after 00:05:00, followed by abort/exit 134.

At 20:38:25 UTC, PgBouncer showed one backend server, cl_waiting 0, 123 queries and two clients during the restart. PostgreSQL total connections were 974. Membership totals were six Active, 18 Joining and 78 Dead; initial pilot generation 529792372 remained Joining. The observed timeout is not attributable to a PgBouncer waiting queue at these snapshots. Original stale-membership trigger and complete causal ordering remain unproven.

Membership row lifecycle and physical deletion must be distinguished: retained Dead history does not itself imply a running silo, whereas unreachable old Active endpoints are relevant to startup failure. Application Program.cs normally calls host.StopAsync only after host.StartAsync succeeds; a startup exception bypasses that explicit normal shutdown path. This is an evidenced cleanup risk, not proof that it originally caused the stale Active records. No membership cleanup was authorized or executed.

## Read-only deployed entrypoint verification

User asked whether the earlier signal-forwarding fix is active in Cerberus. Inspected the actual pilot allocation 3afa1815-44dd-3c4e-7e10-da3003c9de2b on 10.18.26.30, automatically rescheduled at job version 1 after the initial allocation startup failures. Local helper: `/home/slnnk/ai-data/jenkins-recovery/inspect-nomad-entrypoint.py --node --alloc`. Commands were read-only Docker inspect and container process/filesystem reads; no signal delivery, restart or shutdown test was performed.

Worker image 1.0.9 image ID: sha256:1b1d424e4d2aaf1214502a2b1816482b59e8f738756c64a746e7084c87c562d4. API image 1.0.9 image ID: sha256:69ea3dc0465eea6219ae0ac8e6a1ab634f54b42105697317d7a13ee8b0c37f66. Both actual `/app/entrypoint.sh` files have SHA256 b4c23d769c8c3faca12e0511bbf6fe38b6c2feda206cbf198438812a4afb5f90, matching cached templates origin/master and the signal-forwarding fix merged on 2026-10-01 as 7fabb47, [MR85](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/85). An initial attempt used the wrong root path; only the subsequently verified `/app` file/hash is evidence.

Actual PID 1 is `/bin/bash ./entrypoint.sh`, with child dotnet Cerberus.dll or dotnet Cerberus.API.dll. M_TAG is unset, so the fixed runtime branch is active: background dotnet, TERM/INT traps forwarding SIGTERM to the child, then a wait loop; stop skips the ordinary 10-second exit delay. This branch has no .NET version condition and applies to the deployed .NET 2.1 application. Migration Pre/Post branches have different behavior and were not the subject of this runtime verification.

Live Nomad KillTimeout is 5 seconds and KillSignal is empty. Correct forwarding is verified in the deployed scripts/process arrangement; graceful shutdown completion within that window was not tested. Application StartAsync/StopAsync behavior remains a separate risk described above, and no evidence here proves how the original stale Active membership records were created.

## Persistence and recovery follow-up

Direct Nomad job-spec change is not persisted in the repository. The next ordinary CI deployment can overwrite it with source defaults pointing at direct PostgreSQL; source persistence needs separate branch/edit approval. Any stale membership recovery remains a separate proposed action awaiting explicit user approval. No membership or database changes were performed in this pilot. Consumer port switch is complete, but healthy application acceptance must not be claimed.
