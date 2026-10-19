---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [cerberus, pgbouncer, orleans, DevOps-899]
---
# Cerberus all-stand PgBouncer rollout preserving databases

## Summary

User explicitly authorized deploying Cerberus on all stands. All 14 live job specs now have the merged MR117 PgBouncer and 30-second timeout settings, preserving databases, images and migration settings. Ten stands passed application startup and current membership checks beyond five minutes; test1/test2/test6/test7 remain blocked by stale Active membership. PostgreSQL connections fell from approximately 1000 to 273, with Cerberus backends 777 to 22. Configuration rollout is done; full runtime readiness is not.

## Authorization and scope

The user explicitly requested Cerberus deployment on all stands after [MR117 source merge](2026-10-15-nomad-test-cerberus-pgbouncer-source-capacity20.md). Known target set is test, test1–test7 and test10–test15, 14 stands; live discovery and existing PgBouncer mappings must be checked before writes. test1 is already configured and should be skipped if its live spec matches.

Apply only four runtime PostgreSql settings Port=5433/No Reset On Close=true and four task kill_timeout values 30s, matching merged template commit 078c906b24fb5883395a2b76bd3964fbc4598d84 and reviewed source 461bb053. Preserve images, database identities, migration connections on direct5432 and other spec fields. No GitLab ordinary deploy retry is planned because that existing path recreates databases. Direct Nomad registration does not run the external Ansible DROP/CREATE task. No database cleanup, membership mutation or additional source edits are included.

## Context and acceptance limits

Prior pilot successfully routed SQL through PgBouncer without waiting, but failed Orleans membership activation after five minutes, while Nomad still reported healthy. Current restart counts alone hide replaced allocations. See [pilot evidence](2026-10-15-nomad-test-cerberus-test1-pgbouncer-pilot.md) and [initial diagnosis](2026-10-15-nomad-test-cerberus-restart-loop-membership.md).

Acceptance must include actual settings and pooled SQL traffic, allocation replacement/restart history, application startup completion or equivalent Orleans current membership readiness, and observation beyond the known five-minute failure window. Distinguish obsolete Active endpoints from retained Dead historical rows; do not infer authorization to delete either. PostgreSQL capacity relief requires observing old direct backends released; prepared pools alone do not demonstrate it.

## Actions and results

Local helper `/home/slnnk/ai-data/jenkins-recovery/rollout-cerberus-pgbouncer.py` supports plan/apply/status with --logs. Receipts under `/home/slnnk/ai-data/jenkins-recovery/cerberus-pgbouncer-rollout-20261016/` include per-stand plans, applied receipts and status evidence. At 21:12:11–13 UTC on October 15 (October 16 MSK), all 13 required CAS registrations were accepted, each changing four runtime connection strings and four timeouts. test1 already matched and was skipped. Guarded verification confirms desired PgBouncer5433/No Reset On Close=true/30s settings on all 14 specs. No CI jobs, database recreation, source changes or unrelated authentication/pool setting changes occurred in this rollout.

Final checks around 21:18 UTC, beyond the known five-minute failure window, verified the same allocation, three application startup markers, zero restarts and three current Active membership entries for each of these ten stands: test, test3, test4, test5, test10–test15. Membership matches were checked against current address, ports and start timestamps rather than counting historical Active records alone.

test1/test2/test6/test7 still had 8/6/5/9 orphan Active rows respectively and three current Joining silos each, with some current tasks pending/restarting. test2 had three restarts after five-minute activation timeouts; test6/test7 had already replaced allocations, and test1 retained the prior restart loop. test2 initially also logged transient DNS ResourceTemporarilyUnavailable at stage8000, then membership timeouts. The persistent common observation across the four stands is old membership, but the original reason those records became stale remains unproven.

Read-only helper `/home/slnnk/ai-data/jenkins-recovery/cerberus-membership-status.py` writes membership-status.json under the receipt directory. PostgreSQL audit at 21:18:16 UTC found 273 total connections versus approximately 1000 before rollout, and 22 Cerberus backend connections versus 777. All current Cerberus backends were from 127.0.0.1 and PgBouncer had no queue. This verifies substantial direct-connection relief, not readiness of the four failed stands.

## Prepared recovery proposal: not executed

Superseded by user correction: rerun [standard GitLab deployment with normal database recreation](2026-10-16-nomad-test-cerberus-standard-gitlab-rollout.md). The manual membership recovery proposal below is discarded; it was not executed. Do not treat it as the next action.

`membership-recovery-proposal.json` in the same receipt directory describes a scoped possible repair for only test1/test2/test6/test7: stop the four jobs and wait, back up the two Orleans membership tables per database, transactionally mark status<>6 rows as Dead (6) for DeploymentId Cerberus and increment membership version, then resume unchanged jobs and verify. Read-only preflight found one Cerberus deployment and one version row in each of the four databases. Application and reminder tables are outside the proposal.

Deployment approval does not authorize this database metadata repair. Explicit recovery approval is required. No stop action, membership SQL change or database repair has been executed; proposal preparation is not execution. Central TODO tracks readiness/recovery for these four stands, while the runtime configuration rollout is complete.
