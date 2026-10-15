---
system: postgresql
status: verified
checked: 2026-10-15
tags: [pgbouncer, antifraud, DevOps-899]
---

## Summary

User approved applying plan step2 with mappings for all other active stands, stopping the five Antifraud Nomad jobs (step3), and pilot test5 deploy with database recreation (step4). No other service migration to PgBouncer was requested. Changes applied; pilot job3229011 started from existing23.8.8 pipeline140992.

## Configuration applied

Host10.18.26.39, /etc/pgbouncer/pgbouncer.ini:14 exact mappings for antifraud2-test, test1-test7 and test10-test15. test8/test9 excluded. Each mapping uses local PostgreSQL5432 with transaction mode, pool_size2, min_pool_size0, max_db_connections2 and reserve_pool0 (installed1.22 syntax). [users] youdo max_user_connections10; [pgbouncer] min_pool_size0 and server_idle_timeout30. Existing Grafana mapping and all other settings preserved; auth file unchanged by SHA256 comparison. Owner/mode preserved. Backup /etc/pgbouncer/pgbouncer.ini.devops-899-before-transaction-pools. Reload completed, service active and journal had no new configuration errors.

Installed1.22 configuration options verified against upstream tagged documentation. Initial helper execution failed with missing shlex import before any remote write; corrected and dry-run validated before successful apply. No repositories edited.

## Stop and pilot deployment

Stopped exact jobs antifraud2-test2/test3/test4/test5/test7 without purge. Parent verified Stop flags before retry. Other service jobs, PostgreSQL service and Grafana not stopped. Existing GitLab test2/test4 successes remain historical while their Nomad jobs are now stopped.

Normal canceled test5 job3228858 retried once with no skip/drop overrides after durable intent. New job3229011: https://gitlab.youdo.sg/youdo/microservices/antifraud2/-/jobs/3229011 . Source pipeline140992, version23.8.8, database recreation explicitly authorized. Other four stand jobs are not restarted by this pilot.

## Capacity snapshot

Immediately after stopping, clients fell from100 to71, including three remaining Antifraud loopback backends. Later snapshot68, all idle, zero Antifraud clients; diagnostic session excluded. Per-database details in ~/ai-data/jenkins-recovery/antifraud-pgbouncer899/pg-connections-by-db.json. Largest groups: YouDoMailer10, BruteforcingDetector16 across four stands, Fns8, Docvalidation7, Broadcast5. User was given full database breakdown.

## Evidence and limits

Helpers: tune-antifraud-pgbouncer899.py, stop-antifraud-nomad899.py, retry-antifraud-test5-tuned899.py, monitor-antifraud2388.py, c2c-pg-connection-snapshot899.py. Redacted receipts in antifraud-pgbouncer899/. No passwords/hashes copied locally. PgBouncer user cap applies only to connections through it; other direct clients remain outside its budget.

## Pilot runtime and actual migration logs

Allocation6fe5597f-dc76-908b-aac2-48cb4ba70174 observed healthy with no restarts; pre/postmigrations both exited0. Nomad ci_job_id3229011 and pipeline140992 confirmed, not inferred from version. Application runtime ports5433 and IMAGE_TAG23.8.8 match intended release. LaterPGsnapshot77clients, including exactly2 loopbackbackends for antifraud2-test5; otherdirectclients fluctuated.

User asked specifically about migration log errors. Full available premigrations stdout82661bytes/1232lines and postmigrations stdout8286bytes/149lines checked in memory. No SQL/Npgsql/Exception/Error/Fatal/timeout/auth/capacity errors detected. Final migration markers20210802102626_Add_AdditionalIndexes and20210126131837_Delete_Table_ImportTaskOfferData marked migrated. Eachstderr172bytes has only .NETCoreSDK-not-installed notice; no migrationfailure. User told actual logs were checked, not just exitcodes.

GitLab3229011 still running at this observation; trace1869bytes only initialstage, even nocacheGET; BuildAPI stillprevious23.8.7. HealthyNomad does not establish finalCIpublication. No corrective action yet.

## Remaining CI wait

Read-only runner106(172.28.0.172) process inspection identified Ansible waiting on its nomad run child, TCP connected to10.18.26.11:4646. Safe flags: nomad run -address=http://nomad.service.vk-test.consul:4646 -token=<redacted> /tmp/test5_antifraud2.nomad. Deployment0aa75c37 successful, healthy1/unhealthy0; evaluations f8a7e9de and6a541d3c complete. CIjob3229011 still running at426seconds; BuildAPI not updated yet because following Ansible publication tasks have not run. No process signals, cancellation or manual metadata backfill performed. Actual cause of CLI monitor not exiting remains unverified; do not attribute to migrations.

## Pilot CI cancellation requested by user

User requested canceling hung job3229011. Cancel request accepted, status canceling at first read-back. No Nomad mutation: allocation6fe5597f remains running/healthy. BuildAPI publication was still pending at cancellation request; no manual metadata update performed.

## Cancellation execution verified

After user cancel request, GitLab remained canceling. A force=true API request was attempted but did not change status; subsequent GET/version showed17.9.8, which predates supported force cancellation. Do not claim force-cancel success.

Read-only runner106172.28.0.172 inspection confirmed exact job main container cc1527b1f58a was already removed (docker inspect No such object) and no project384 containers remained. No docker stop/kill, runner restart or unrelated-container action was performed. Thus CI execution has ended on runner, while GitLab status reconciliation remains canceling at final GET. Nomad allocation6fe5597f verified running and healthy after cancel request. User informed of distinction. Cancel receipt antifraud-pgbouncer899/cancel-pilot.json.

## Outcome read-back at15:56UTC

User asked whether changes helped. Fresh verification: test5 allocation6fe5597f remains healthy, zero restarts, runtime23.8.8/5433; PostgreSQL82clientconnections total, exactly2loopbackbackendconnections for antifraud2-test5. Other four Antifraud Nomad jobs remain stopped. BuildAPItest5 still23.8.7, GitLabjob3229011stillcanceling despite removedrunnercontainer. Positive pilot outcome covers combined pooling/recreation and reduced concurrent stand count; all-five concurrency has not been validated.

## PostgreSQL capacity recommendation after user feedback

User noted max_connections100 will be insufficient for all services. Read-only resource check: PostgreSQL16.15 on Ubuntu24.04,12vCPU, MemTotal36943288KiB (~35.2GiB), MemAvailable35724816KiB (~34.1GiB), no swap. shared_buffers16384 blocks*8192=128MiB, work_mem4096KiB=4MiB, maintenance_work_mem64MiB. max_connections100 and superuser_reserved_connections3 remain defaults. Exact active source /etc/postgresql/16/main/postgresql.conf on10.18.26.39.

Propose raising max_connections to500 as an initial capacity step, retaining bounded Antifraud PgBouncer settings and monitoring memory/active-query concurrency/connection peaks during full rollout.500 is an initial operational recommendation based on available resources, not a guarantee for arbitrary query workloads or all future services. Increasing max_connections requires PostgreSQL restart and briefly interrupts all C2C DB connections; no permission to perform restart or edit inferred from user observation. No PostgreSQL settings changed.
