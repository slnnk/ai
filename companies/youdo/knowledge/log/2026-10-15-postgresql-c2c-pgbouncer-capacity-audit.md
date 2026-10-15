---
system: postgresql
status: verified
checked: 2026-10-15
tags: [postgres, pgbouncer, DevOps-899]
---

## Summary

Read-only audit supports configuring the existing C2C PgBouncer before moving compatible application connections to5433. No configuration edits, reloads, service restarts, deployments or database session termination performed.

## Verified state

C2C PostgreSQL10.18.26.39: max_connections100, superuser_reserved_connections3, reserved_connections0. pg_stat_activity total105 includes background workers and must not be interpreted as105clientconnections. No idle-in-transaction sessions or activequeries older5minutes at observation. Largest idle groups: Antifraud test5/test4 each12, YouDoMailer11, BruteforcingDetector test5nine, Broadcast test5six.

PgBouncer1.22.0 active on5433, /etc/pgbouncer/pgbouncer.ini. Only grafana_test database maps to127.0.0.1:5432/grafana_test and only grafana_test auth entry exists (SCRAM). No youdo auth entry; pool limits/mode rely on defaults. No secrets printed. Earlier Antifraud bypass was due to missing mapping/auth, not demonstrated application incompatibility.

Antifraud references Hangfire.PostgreSql1.8.1 and Linq2Db2.9.7. Do not declare transaction pooling compatible without checking actual storage locking and client/session behavior. Ansible creates databases via local psql as postgres on PGhost; these administrative operations should remain direct. Existing applications must release/reconnect to reduce current saturation; adding PgBouncer alone will not release existing direct connections.

## Proposed direction (not applied)

Configure existing PgBouncer mappings/auth for actual per-stand DBs. Bound backend connections per database and globally per user, preserving capacity for direct migrations/admin and other users. Transaction pooling only for compatible runtime clients; session/direct for session-dependent clients until verified. Limit Npgsql client pool sizes where required. Start with one service/stand, verify auth, workload and background jobs, then roll out and retry failed deployments. Exact numeric budgets require accounting for retained direct clients and all database pools.

## Sources

Read-only SSH/SQL/config audit and local repository inspection. Official pooling compatibility: https://www.pgbouncer.org/features.html and limits: https://www.pgbouncer.org/config .

## Refined capacity and compatibility evidence

Later snapshot97clientbackends:95idle,1active,1startup, plus6backgroundworkers. Role youdo holds91connections across34databases and is SUPERUSER with no role limit; the configured3superuserreserved slots do not reserve capacity against this same superuser. Do not change role privileges without separate scope.

Exact Hangfire.PostgreSql1.8.1 upstream lock implementation uses transactional INSERT/UPDATE/DELETE in its lock table, not session pg_advisory_lock; Hangfire alone is not a demonstrated transaction-mode blocker here. Conversely Userinsurance DistributedLockRepository calls session pg_advisory_lock/unlock across nontransaction async work, so retain direct/session mode. Six initial candidates for transaction-mode validation: Fns, Attribution, Badgekeeper, Brute, Docvalidation, Antifraud. Badgekeeper migration includes session temporary-table use; keep migrations direct. Escrow uses MSSQL. Current implicit PgBouncer session mode will not multiplex persistent idle Npgsql connections.
