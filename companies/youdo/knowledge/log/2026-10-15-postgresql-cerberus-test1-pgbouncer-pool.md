---
system: postgresql
status: verified
checked: 2026-10-15
tags: [cerberus, pgbouncer, postgresql, DevOps-899]
---
# Cerberus test1 PgBouncer transaction pool prepared without consumer switch

## Summary

User reviewed the exact proposed configuration and explicitly said to apply it. Prepared one transaction pool for Cerberus_test1 on C2C PgBouncer at 10.18.26.39:5433 and increased the shared youdo backend cap from 10 to 20. Reload only; PID 114852 unchanged. No Cerberus repository change, client switch, rerun or deployment was authorized or performed.

## Context and approved scope

The [read-only Cerberus investigation](2026-10-15-nomad-test-cerberus-restart-loop-membership.md) found restart loops, stale Orleans membership and direct PostgreSQL connection pressure. Existing PgBouncer had no Cerberus mapping. User approval covers this configuration preparation only, not proof of Orleans 2/Npgsql 4 transaction-pooling compatibility.

## Actions and exact changes

On 10.18.26.39, changed `/etc/pgbouncer/pgbouncer.ini`: added database mapping `Cerberus_test1` with host 127.0.0.1, port 5432, dbname Cerberus_test1, pool_mode transaction, pool_size 10, min_pool_size 0, reserve_pool 0 and max_db_connections 10. In `[users]`, changed youdo max_user_connections from 10 to 20 to allow the scoped additional capacity. Global settings, authentication and all 16 existing database definitions were preserved.

Executed approved preparation with local helper `/home/slnnk/ai-data/jenkins-recovery/prepare-cerberus-pgbouncer.py`. Remote backup: `/etc/pgbouncer/pgbouncer.ini.before-cerberus-test1-transaction-20261015`. Evidence receipt: `/home/slnnk/ai-data/jenkins-recovery/cerberus-pgbouncer-test1/applied.json`.

The first attempt used per-database reserve_pool_size from newer documentation. PgBouncer 1.22 rejected it during reload; the script detected the missing runtime database mapping. Corrected the key to supported per-database reserve_pool, reloaded and verified runtime state. Do not treat a reload command exit alone as proof that the configuration was accepted.

## Verification and limits

Runtime SHOW DATABASES confirms Cerberus_test1 enabled with transaction mode, backend maximum 10 and current_connections 0. PgBouncer PID stayed 114852: no process restart. All global runtime settings, authentication and 16 existing definitions were verified unchanged. PgBouncer 1.22 SHOW USERS does not expose the user connection cap; cap 20 is verified in the configuration and successful reload, not claimed as a SHOW USERS field.

No Cerberus consumers were switched to port 5433 and no service was rerun. An idle prepared pool does not validate application compatibility or resolve existing Orleans membership failures. Any consumer pilot and deployment remain separate work requiring the applicable approvals. The single recovery follow-up remains in `~/ai/TODO.md`.

## Changed files and risks

Remote change was limited to the approved PgBouncer configuration plus backup. Locally, helper/receipt and KB log, existing nomad-test map, TODO and dated address-map comment record the result. No credentials are recorded here. Shared youdo cap now permits up to 20 PostgreSQL backends across its mappings; existing Antifraud per-database limits remain unchanged.
