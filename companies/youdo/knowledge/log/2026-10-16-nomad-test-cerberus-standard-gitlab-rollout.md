---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [cerberus, gitlab, DevOps-899]
---
# Cerberus standard GitLab redeploy with database recreation; workflow correction

## Summary

User corrected the deployment approach: use standard GitLab deployment with its normal database recreation rather than direct Nomad updates and separate membership repair. The agent acknowledged the avoidable workflow deviation. Standard deployment of Cerberus 1.0.9 succeeded on all 14 stands: GitLab SUCCESS, all current workers started and all 14 databases have exactly three matching current Active membership entries. No manual membership repair was executed.

## User correction and authorization

The active request remains deploying Cerberus on all stands. User explicitly directed rerunning normal GitLab deploy instead of inventing direct Nomad recovery. This steering covers the standard jobs and their established per-stand database recreation. It does not authorize arbitrary SQL metadata repair. The earlier prepared manual membership repair proposal is discarded; no membership repair SQL was executed.

Reusable convention recorded in current/CONTEXT.md: standard GitLab deploy is the default; do not substitute direct Nomad job-spec updates or change a service's established reset/preservation behavior unless requested. Cerberus standard deployment recreates its stand database on every run for all stands.

## Scope and actions

Use existing Cerberus project 153, pipeline 140997, deploy-yandex-test matrix indices 0–7 and 10–15, corresponding to test/test1–test7/test10–test15. Only play/retry existing deploy jobs; no new image build, CI source edit, Git mutation or unrelated infrastructure change. Existing merged MR117 template supplies PgBouncer runtime5433/No Reset On Close=true and shutdown timeout30s; normal migrations remain direct5432.

Standard Ansible path stops/purges the stand job, terminates DB sessions, drops/creates the empty stand database and grants database privileges to youdo, then registers Nomad jobs with migrations. This deliberately replaces the previous database-preserving directCAS rollout. No extra manual membership repair is needed as a separate proposal before this standard reset path.

## Final GitLab and Ansible verification

All 14 jobs succeeded: test 3230163; test1 3230164; test2 3230167; test3 3230162; test4 3230165; test5 3230170; test6 3230166; test7 3230168; test10 3230169; test11 3230171; test12 3230175; test13 3230174; test14 3230172; test15 3230173. Receipts: `/home/slnnk/ai-data/jenkins-recovery/cerberus-fourteen-stands-gitlab-20261016/`. Runner: deploy-cerberus-fourteen-stands899.py with --ordinary-rerun; only launch mutates, status/watch read state.

Read-only helper `/home/slnnk/ai-data/jenkins-recovery/inspect-cerberus-standard-deploy-traces.py` inspected all 14 terminal traces in memory without printing raw logs/credentials. Saved sanitized-trace-verification.json confirms every job executed and changed Stop nomad job, Recreating empty Cerberus db, Get nomad file and Run nomad task. Every recap was ok=5, changed=4, unreachable=0, failed=0. Successful DROP DATABASE/CREATE DATABASE outputs present, no DNS errors or zero-task no-ops. Every trace confirms a fresh automation repository clone and generated PgBouncer/No Reset/timeout settings. Exact checkout SHA was not printed in traces, so exact commit provenance is not claimed from those traces alone; merged source was verified separately.

## Final application and database verification

All 14 Nomad jobs are running/healthy, with all three workers running on each stand. There are 42/42 worker startup markers. Idempotent transformation check verifies all four runtime PostgreSql connections on 5433 with No Reset On Close=true and all four runtime shutdown timeouts 30s per stand.

Read-only cerberus-membership-status.py confirms every database now has exactly three current Active membership entries matching the current node/address, ports and start times, with no old Active orphans. Previously blocked test1/test2/test6/test7 now have startup markers and three current Active silos after standard database recreation, without manual membership repair.

test11 had one initial worker2 restart: stderr recorded stage8000 Npgsql stream EndOfStream. It recovered automatically and now has three Active silos and startup markers. Do not claim all stands had zero restarts. No additional restart/deployment was performed for this recovered startup event.

Last PostgreSQL snapshot at 21:29:53 UTC on October 15 (October 16 MSK): 280 total connections, 20 Cerberus backends, no waiting PgBouncer pools, compared with approximately 1000 total/777 Cerberus before pool migration. The deployment and current startup/membership checks passed; no application data/API business-operation verification is claimed.

Sanitized current application/alloc and membership receipts were copied from the earlier rollout tool directory to `cerberus-fourteen-stands-gitlab-20261016/final-runtime-verification/` to preserve this final evidence against future helper overwrites. The prior [direct rollout](2026-10-16-nomad-test-cerberus-pgbouncer-all-stand-rollout.md) remains historical evidence, superseded as the recovery workflow. Manual membership proposal discarded without SQL execution. Existing readiness/recovery TODO is closed; canonical deployment correction remains in CONTEXT.md.
