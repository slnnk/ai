---
system: postgresql
status: verified
checked: 2026-10-15
tags: [antifraud, pgbouncer, DevOps-899]
---

## Summary

User manually started Antifraud23.8.8 deploy jobs frompipeline140992 and requested monitoring. Parent performed read-only observation only; no jobs were played/retried/cancelled and no infrastructure configuration was changed during monitoring.

## User-started jobs and database effects

Jobs: test2=3228855, test3=3228856, test4=3228857, test5=3228858, test7=3228860. All normal deploy jobs executed Recreating db, changed=true, with DROP DATABASE and CREATE DATABASE in sanitized trace evidence; ANSIBLE_SKIP_TAGS=dropdb was not applied by these manual launches. User informed that all five databases were recreated.

## Runtime evidence

Nomad Meta IMAGE_TAG23.8.8 and all three runtime connection ports5433 verified for all five stands. No healthy deployments at the initial observation; scheduler restarts and failed postmigrations observed. test2/test4 scheduler: NpgsqlException/stream-read timeout. test5 scheduler: PgBouncer08P01 server_login_retry. test7 direct postmigrations: PostgreSQL53300 too many clients already. BuildAPI retained23.8.7 while deploy jobs had not succeeded.

PG39 exhausted all100backend slots; even local postgres socket login rejected. PgBouncer recent sanitized logs repeatedly contained too many clients already and backend server_login_retry, no password/no-such-database errors. Auth/mappings valid; unchanged session pooling/default20 per DB can hold up to100backend connections across five DBs. No long-query or idle-transaction evidence established as cause; prior snapshots mostly idle pooled clients.

Nomad update HealthyDeadline300s, ProgressDeadline600s, AutoRevertfalse. Read-only helper ~/ai-data/jenkins-recovery/monitor-antifraud2388.py [--verify] persists compact status and verification in antifraud-pgbouncer899/. No credentials written.

## Proposed follow-up, not applied

User asked for recommendations during monitoring. Suggested initial per-Antifraud-DB transaction mode, pool_size2/max_db_connections2/reserve0; PgBouncer user youdo cap10. This is a trial budget pending application validation and capacity accounting, not a throughput guarantee. Addressed reconnection is needed to release retained old session backends. Leave migrations direct5432 and defer increasing PostgreSQL max_connections until memory/load reviewed. No approval for these changes inferred from asking for suggestions.

## Growth clarification

User noted future database count will increase. Clarified that cap10 was only an initial five-Antifraud-DB budget. Sustainable aggregate backend limit must remain bounded independently of mapping count, budgeted as PostgreSQL max_connections minus peak direct clients and operational reserve. Keep per-DB pools small, min_pool_size0, and evaluate server_idle_timeout to release idle backends across many pools. Requests queue at capacity; this is not unlimited throughput and waiting-time validation remains necessary. Further direct app cutover and PostgreSQL capacity review may be required. No settings changed.

## User-requested cancellation and final observed state

User requested stopping GitLab jobs. At cancellation time test2job3228855 and test4job3228857 had already succeeded (397.08/397.997seconds). Both runtime deployments subsequently verified healthy with23.8.8/5433 and BuildAPI matching pipeline140992/jobIDs. Remaining test3job3228856, test5job3228858, test7job3228860 received cancel requests and reached CANCELEDterminal at485seconds. No forcecancel or newdeploys executed.

Nomad allocations were not stopped by GitLab cancellation; test3/5/7 still had active unhealthy/unconfirmed deployments and restarted tasks at finalruntimeobservation. BuildAPI for those three retained23.8.7. Finalstatus receipts in antifraud-pgbouncer899/rollout-status.json, user-cancel-deploys.json; runtimeevidence rollout-verification.json.

User next requested a plan with exact locations for PostgreSQL/PgBouncer follow-up. This authorizes planning only, not applying pool changes, terminating DB sessions, stopping Nomad jobs or newdeploys.

## Concrete follow-up plan requested by user (not executed)

1. Read-only capacity snapshot onPG39, backups of its existing PgBouncer files, and check current allocations/DBmigration state. Budget B<=100-D_peak-R, where D_peak includes every direct app/migration/admin client and R is an operational margin. Initial Antifraud trial cap10 only if that budget is available; adding databases must not automatically raise it. User role remains SUPERUSER, so direct youdo clients can still consume PostgreSQL reserved slots; PgBouncer cap does not govern direct traffic.
2. Only runtime configuration file changed:10.18.26.39:/etc/pgbouncer/pgbouncer.ini. In five existing Antifraud database mappings set pool_mode=transaction, pool_size2,max_db_connections2,reserve_pool_size0. Keep min_pool_size0. In [users] add/adjust youdo max_user_connections10. In [pgbouncer] propose server_idle_timeout30 seconds to release unused backends between pools. This timeout is global and also affects unused Grafana backend reuse; Grafana mapping/mode/limits/auth unchanged. Verify every option against installed1.22.0 before applying. No wildcard mapping. Auth file /etc/pgbouncer/userlist.txt stays unchanged.
3. Controlled connection turnover for only Antifraud test2/3/4/5/7. Stop its workloads to release linked old session connections, reload PgBouncer, wait for unused backend cleanup and verify free PGslots. This briefly interrupts healthy Antifraud ontest2/test4; PostgreSQL is not restarted and unrelated DB sessions are not killed. Abort rollout if capacity remains insufficient.
4. Reuse existing23.8.8images/pipeline140992; no rebuild/tag/repositorychanges. Pilot test5 via manual deploy with modified variables ANSIBLE_SKIP_TAGS=dropdb, preserving DB. StandardRESTretry cannot be assumed to change variables; use supported manual-job retry-with-modified-values flow and verify skip in trace. Avoid existing keep-db variants because of knownVKargs override. Validate lifecycle migrations/application and PgBouncer transaction compatibility.
5. Sequential rollout remainingtest3/test7/test2/test4 with same preservation and checks. Confirm Nomadhealthy/no restartloop, currentversion/5433, successful GitLabjob and BuildAPIpipeline140992/tag23.8.8/sourcejob. Database DROP must be skipped. Rollback poolsettings from reviewed backup if client incompatibility appears, with reconnection; do not recreateDB or revert password.
6. FutureDB mappings retain same globalbudget, perDBsmall/on-demand pools and idlecleanup. Trial throughput/queue measurements decide budgetgrowth withinPGcapacity. PostgreSQLmax_connections/roles/pg_hba.conf remain unchanged in this iteration; expand capacity only after memory/load review. ActiveAnsiblePgBouncer source is absent; codifying runtimeconfig in automation-services is a separate scoped task requiring exactrolepath/branchapproval, not silently added to minimal change.

Planned repository changes thisiteration: none in antifraud2 (devops/config.yml already5433), gitlab-ci-templates, automation-test-yandex. Runtimehostconfigchange and controlledrestarts/deploys needexplicitapproval afterplanreview.
