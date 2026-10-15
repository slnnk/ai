---
system: postgresql
status: verified
checked: 2026-10-15
tags: [b2b, postgresql, pgbouncer, capacity]
---
# B2B PostgreSQL and PgBouncer connection limits1000

## Task

User explicitly requested B2B PostgreSQL and PgBouncer (if installed) limits analogous to C2C after auth deployment failed from exhausted connections. Authorized scope: PG max_connections1000/restart, PgBouncer max_client_conn1000/reload and required nofile2048. No job retry authorization inferred.

## Context

VK B2B PostgreSQL10.18.26.44, postgres-b2b.service.vk-test.consul:5432; PgBouncer1.22 on5433. SSH via existing workstation id_ed25519 as youdo, sudo-n; no credential values recorded. C2C reference max_connections1000/max_client_conn1000/softnofile2048/hard524288. [Failed auth deployment](2026-10-15-nomad-test-devops-898-auth-service-b2b-rollout.md).

## Actions

Read-only inspection showed PG16/main max100 and PgBouncer runtime max_client_conn100; softnofile1024/hard524288. B2B memory24GB/23GBavailable. At saturation even local postgres connections failed; process aggregate99idleSMSclients. Implemented receipt-backed local helper `/home/slnnk/ai-data/DevOps-898/b2b-connection-limits.py [--apply]`, plan before apply; evidence directory `b2b-connection-limits/`. Apply executed once under explicit user request.

Changed /etc/postgresql/16/main/postgresql.conf max_connections100->1000, validated effective config before restart; systemctl restart postgresql@16-main took2.405seconds. Data /data/postgresql/16/main. Changed /etc/pgbouncer/pgbouncer.ini max_client_conn100(default)->1000; daemon-reload/prlimit set softnofile2048, hard524288 retained, persistent drop-in /etc/systemd/system/pgbouncer.service.d/devops-898-client-limit1000.conf. PgBouncer reload only.

## Findings

Runtime SQL verifies max_connections1000/pending_restartfalse,89connections immediately after restart. PG shared_buffers128MB/work_mem4MB unchanged. PgBouncer SHOW CONFIG verifies max_client_conn1000; PID43719 unchanged. Runtime nofile2048/hard524288; other runtime settings/auth-file hash preserved. Both services active. No additional application/HTTP/Consul probes performed.

## Changes

Remote settings as above, backups /etc/postgresql/16/main/postgresql.conf.devops-898-before-max-connections1000 and /etc/pgbouncer/pgbouncer.ini.devops-898-before-client-limit1000. Local helper, sanitized plan/intent/applied receipts and KB/service-address map. No repository source edits, GitLab retries or unrelated remote changes.

## Limits

PostgreSQL restart interrupts active connections; application recovery is not claimed from SQL/config verification alone. Failed auth jobs remain failed until an explicitly approved retry. Capacity changes do not themselves deploy auth-service.

## Portable lesson

none
