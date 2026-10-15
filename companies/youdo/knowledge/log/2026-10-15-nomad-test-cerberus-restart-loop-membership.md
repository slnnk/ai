---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [cerberus, orleans, postgresql, DevOps-899]
---
# Cerberus restart loops: stale Orleans membership and PostgreSQL connection pressure

## Summary

Read-only investigation on 2026-10-15 at 20:12–20:15 UTC found Cerberus restart/replacement loops despite earlier GitLab SUCCESS and Nomad healthy acceptance. Failed allocations and logs show Orleans membership activation timeouts, calls to stale silo endpoints and PostgreSQL 53300 errors. The immediate failure chain is evidenced; the original trigger of stale membership and the complete connection-budget cause remain unproven. No fixes, restarts, deployments or membership changes were authorized or performed during this investigation.

## Task and context

Investigate current Cerberus runtime restarts following the [fourteen-stand rollout](2026-10-15-jenkins-cerberus-eight-stand-rollout.md). Earlier status-only acceptance did not establish sustained application readiness. PostgreSQL and PgBouncer had already been [raised to 1000](2026-10-15-postgresql-c2c-connection-limits-1000.md).

## Actions and evidence

- Read-only Nomad allocation/event/log and PostgreSQL inspection, captured by `/home/slnnk/ai-data/jenkins-recovery/inspect-cerberus-restarts.py` and `/home/slnnk/ai-data/jenkins-recovery/cerberus-restarts-snapshot.json`.
- Inspected local Cerberus `src/Cerberus/Program.cs`, cluster constants/dependencies and `automation-test-yandex/playbooks/deploy/docker/files/nomad_cerberus/cerberus.j2`. No repository edits.
- Initial observed failed allocation counts for test1/test2/test6/test7 were 8/11/10/8. These are snapshot observations, not invariant counters: garbage collection subsequently reduced visible failed counts. Current task restart counts omit replacements and therefore understate historical failure volume.
- Failed workers logged stage 19999 MembershipOracle activation timeout after five minutes, followed by stage 20000 `OrleansMessageRejectionException` targeting dead silo endpoints. test2/test6 also logged PostgreSQL `53300`.
- At the snapshot, PostgreSQL had 963 connections against `max_connections=1000`; stable Cerberus databases each held approximately 60–85 idle connections. This is connection pressure, not proof that 963 itself exhausted the limit at that instant.
- Final snapshot at 20:15:50 UTC showed PostgreSQL 972/1000 connections, with 729 connections to Cerberus databases, all idle. On test1/test2/test6, all three current workers had Restarts=1, demonstrating further restarts during investigation; test7 retained the same current allocation with previous failure chains. Nomad healthy remained true during these restarts.
- `Cerberus_test1` membership had current host `10.18.26.34`, ports 15001/35001/50010, status 2 (Joining). Old `10.18.26.37` endpoints 15001/50010 still had status 3 (Active), last heartbeat 20:09:12 UTC at approximately 20:15 UTC inspection. Logs reported `ConnectionRefused` for obsolete endpoints. Current allocation ran on `vk-ms1-nomad-agent-test-01` (`10.18.26.34`); worker3 timed out at 23:14:53 MSK.

## Findings and limits

The confirmed current failure includes stale Active membership endpoints, failure to finish membership activation and rejected startup grain calls. PostgreSQL capacity failures coexist and can disrupt startup. It is not established whether connection pressure initially caused stale membership, whether an earlier shutdown failed to leave cleanly, or whether another failure started the loop. Do not present those causal hypotheses as verified root cause.

`Program.cs:103–133` uses the same per-stand PostgreSQL connection string for ADO.NET clustering and reminders; application data also uses it at line 149. ClusterId and ServiceId are both `Cerberus`; stands are isolated by their databases. The startup task at lines 172–190 awaits two real grain calls to register reminders, so stale routing can block application startup. The application does not explicitly configure membership timeouts; lifecycle stage-number attribution comes from logs rather than a constant in application code.

The test template launches three separate workers plus an API per stand. Runtime PostgreSQL connection strings have no explicit maximum/minimum pool size or idle lifetime, and target direct PostgreSQL rather than PgBouncer port 5433. Separate process pools can contribute to aggregate backend pressure; their exact effective pool defaults were not verified here. Changing PgBouncer limits alone does not bound these direct runtime connections.

Worker and API health checks are TCP only (10-second interval, 2-second timeout). A listening silo socket does not prove membership activation or startup grain calls have completed. Earlier GitLab SUCCESS/Nomad healthy results were a status snapshot and were insufficient evidence of sustained Cerberus readiness. Current restart totals alone are also insufficient without failed/replaced allocation history.

Advertised host IP, worker static ports, Docker port maps and listening ports are consistent in the inspected template/source. No port-mapping defect was found. `Program.cs:195–223` signals shutdown via CancelKeyPress/ProcessExit and calls StopAsync after successful StartAsync, with no surrounding try/finally. A startup exception bypasses that normal StopAsync path; this is a potential cleanup risk, not proof of the observed stale rows. The test template has no explicit kill timeout/signal/shutdown delay. Docker entrypoint signal forwarding was not established from this repository because build templates are external.

Restart policy is one attempt per one-minute interval, delay 10 seconds, mode fail; reschedule policy permits three attempts per five-minute interval. Replacement allocations can therefore reset the visible current restart counter.

## Changed local files and risks

Only knowledge-base bookkeeping and the local diagnostic artifacts were changed/created; service repositories and infrastructure were not modified. Existing `nomad-test.md` records the superseding runtime finding; the single follow-up is tracked in `~/ai/TODO.md`. No credentials or complete connection strings are recorded here. No service address change was discovered.

## PgBouncer option: read-only preflight around 20:18 UTC

User asked to consider PgBouncer; no switch or runtime changes were authorized. Effective inspected configuration: listen_port 5433, pool_mode session, max_client_conn 1000, default_pool_size 20, max_db_connections 0, max_user_connections 0, reserve_pool_size 0, max_prepared_statements 0. The `[users]` entry for youdo overrides the global user limit with `max_user_connections=10`.

The database list has 16 entries for Antifraud and grafana_test only: no Cerberus mappings and no wildcard. A connection-port switch alone would therefore fail to route Cerberus databases. With session pooling, long-lived Npgsql pool connections can pin PostgreSQL backends; the shared youdo cap of 10 can also cause queuing/starvation across mappings. These are configuration implications, not evidence of an attempted Cerberus connection through PgBouncer.

Any proposal needs explicit per-database mappings, pool mode and backend limits. Orleans 2/Npgsql 4 transaction-pooling compatibility requires a scoped test before rollout. Do not infer authorization to change global pool mode or the shared user cap from the question about PgBouncer. No switch, mapping, mode or limit change was performed.
