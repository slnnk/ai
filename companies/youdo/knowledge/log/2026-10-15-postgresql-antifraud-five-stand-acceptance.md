---
system: postgresql
status: verified
checked: 2026-10-15
tags: [antifraud, pgbouncer, DevOps-899]
---

## Summary

User manually redeployed Antifraud23.8.8 on test2/test3/test4/test5/test7 from pipeline140992. Read-only acceptance verified all five jobs successful, all current allocations healthy, runtime5433/version23.8.8 and matching BuildAPI version/pipeline/source job. No state changes performed by the agent during acceptance.

## Results

- test2 job3229391 SUCCESS111.11s, allocation f7f691c9 healthy, zero restarts.
- test3 job3229392 SUCCESS100.53s, allocation be64f522 healthy, zero restarts.
- test4 job3229393 SUCCESS98.10s, allocation eaa09d9a healthy, zero restarts.
- test5 job3229394 SUCCESS82.10s, allocation6fdc23c7 healthy, zero restarts.
- test7 job3229395 SUCCESS204.00s, allocation54590dae healthy, one restart. Its earlier allocation was unhealthy; migration lifecycle tasks completed0.

BuildAPI/ms_builds for all five stands has project384/ref23.8.8/pipeline140992/SHA b02e317a752ede337a0d5bfadca475e1af31cc8f and the corresponding successful job above. No stale test5 metadata remains after these successful deployments; manual backfill was not needed.

## PgBouncer client limit incident

During test7 startup scheduler received Npgsql.PostgresException08P01: no more connections allowed (max_client_conn). Error confirmed in both initial and current allocations before recovery. PgBouncer max_client_conn remains implicit100; later live snapshot had85 connected clients, so saturation was transient rather than persistent at that observation. Backend cap remains youdo10/perDB2, verified PG snapshot exactly2 loopback backends per five Antifraud DBs,10 total. PostgreSQL total clients91 at snapshot, limit500, so PostgreSQL capacity was not the test7 failure cause.

Recommend increasing only PgBouncer max_client_conn100to500 in /etc/pgbouncer/pgbouncer.ini on10.18.26.39, checking process filedescriptor limit, keeping backend10/2 and transaction mappings intact. No configuration change/reload was made for this recommendation.

## Evidence

~/ai-data/jenkins-recovery/antifraud-pgbouncer899/rollout-status.json and rollout-verification.json contain final all-five acceptance. Sanitized runtime failure evidence monolith-services-audit/antifraud-test7-3229395-runtime-diagnosis.json. Current five-stand concurrency is now verified; prior pilot-only limitation superseded. Historical3229011 CLI cancellation remains separate from these successful runs.
