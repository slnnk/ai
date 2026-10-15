---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [auth, b2b, deployment, gitlab]
---
# DevOps-898 auth service test10-test15 rollout

## Task

User explicitly confirmed six ordinary parallel auth-service deployments to test10–test15, with DB recreation, after build verification and a deployment-specific approval question. Acceptance is GitLab/Nomad job statuses only.

## Context

DevOps-898, project544, new approved master pipeline141000, sourcef0d4a2fb971b4b2a8e4aafe7e2990ef3221f61f3, master-168. Images3of3/build-libs/unit-tests already successful. [Preflight/build record](2026-10-15-nomad-test-devops-898-auth-service-preflight.md).

## Actions

Validated pinned pipeline and all6manual ordinary jobs before plays. Launched jobs3229573–3229578 concurrently2026-10-15 19:18:07UTC, no keep-db overrides. Helper `/home/slnnk/ai-data/DevOps-898/deploy-auth-service-stands.py launch|status`, receipts/status in `youdo-business-auth-service-rollout/`. No superpowers skills used.

## Findings

All6ordinary jobs failed with script_failure after8.28/8.00/8.33/7.94/8.40/7.92seconds for test10 through test15. Nomad job GETs return HTTPError; no successful deployment acceptance. Read-only GitLab trace diagnosis delegated; no retry or other external write performed. Parent pipeline141000 remains running due approved auto-production bridge; downstream141002 scheduled at last GET, not claimed successful.

Trace diagnosis: all6fail at Create postgres db if not exist on postgres-b2b.service.vk-test.consul, local socket5432: FATAL sorry, too many clients already, rc2. Both existence SELECT and fallback CREATE could not acquire connection. No successful SQL changes, DB reset/migrations/Nomad run not reached. Prior stop returned No jobs found and was ignored. Recap ok12/changed1/failed1/ignored1; changed1 is not evidence SQL succeeded. Cause is B2B PostgreSQL connection exhaustion, no auth-service source bug established. Read-only capacity diagnosis requested before proposing a runtime change.

User then explicitly requested B2B PG/PgBouncer limits analogous to C2C. Applied and verified PG1000/PgBouncer1000/nofile2048; PG restart2.405seconds, PgBouncer reload/PIDunchanged. [Capacity result](2026-10-15-postgresql-b2b-connection-limits-1000.md). No retry yet; six failed jobs remain pending separate retry approval.

## User-approved retry

After capacity fix and an explicit six-job retry/DB-recreation question, user replied "Да". Retried original ordinary jobs concurrently2026-10-15 19:25:30UTC. New job IDs by stand: test10=3229609,test11=3229612,test12=3229610,test13=3229614,test14=3229613,test15=3229611. Same pipeline141000/master-168/sourcef0d4a2f, normal DB recreation retained. Receipts under `youdo-business-auth-service-rollout/retry/`. No other job plays or remote changes performed; final status follows.

## Changes

Six explicitly approved ordinary GitLab job plays. No repository edits, new tags/pipelines, unrelated runtime changes or HTTP/Consul probes.

## Limits

Stand acceptance uses GitLab/Nomad statuses only. Production downstream141002 was last scheduled; its success is not claimed from this stand rollout. Other services tracked centrally in ~/ai/TODO.md; next proposed service is youdo-notifications, a dependency of main youdo-business.

## Final acceptance

All6retry jobs succeeded: test10=3229609(100.41s),test11=3229612(111.58s),test12=3229610(113.79s),test13=3229614(104.38s),test14=3229613(107.73s),test15=3229611(105.50s). Nomad all6jobs running/enabled on master-168, allocations running/healthy, task restarts0. No further intervention/retry required. DB recreation and migrations were part of the approved normal deployment; no service repository changes. Evidence `/home/slnnk/ai-data/DevOps-898/youdo-business-auth-service-rollout/status.json`. PG/PgBouncer capacity correction resolved the initial blocker for this deployment. No HTTP/Consul/business probes performed.

## Portable lesson

none
