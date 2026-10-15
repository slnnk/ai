---
system: postgresql
status: verified
checked: 2026-10-15
tags: [postgres, capacity, DevOps-899]
---

## Summary

User authorized increasing C2C PostgreSQL max_connections from100 to500 after reviewing capacity and restart effects. Change applied on10.18.26.39; PostgreSQL restarted successfully in2.831seconds, runtime setting500/pending_restart=false verified. PgBouncer settings and auth files unchanged.

## Context and exact change

PostgreSQL16.15 Ubuntu24.04 cluster16/main,12vCPU,~35.2GiB RAM with~34.1GiB available at preflight. Data directory /data/postgresql/16/main. Exact source /etc/postgresql/16/main/postgresql.conf; one active max_connections line changed100to500, all other bytes preserved. Backup /etc/postgresql/16/main/postgresql.conf.devops-899-before-max-connections-500. Owner/mode preserved via atomic replace. No repository changes.

Before restart, postgres -D <data_directory> -c config_file=<file> -C max_connections validated500. Target service systemctl restart postgresql@16-main. Postmaster start changed from2026-10-15T06:49:06.501256+00:00 to2026-10-15T16:02:56.756750+00:00. After restart max_connections500 and pending_restart=false; shared_buffers128MB/work_mem4MB unchanged.

## Verification

PgBouncer config and auth file hashes compared before/after and unchanged; service active. Existing Antifraud app credentials successfully executed SELECT through5433 on antifraud2-test4 and antifraud2-test5. Diagnostic SELECT created a temporary test4 backend; test4 application remains stopped.

Client backends66 at immediate read-back (excluding diagnostic session); applications reconnecting. Current Consul checks for antifraud2-api-test5 and antifraud2-scheduler-test5 passing. This verifies targeted service recovery, not every application endpoint. No database recreation, service redeploy, client-pool edits or PgBouncer max_client_conn change in this task.

## Evidence and limits

Helper ~/ai-data/jenkins-recovery/increase-c2c-pg-connections899.py [--apply], durable plan/intent/applied receipts in antifraud-pgbouncer899/pg500-*.json. No secrets logged.500 is a capacity limit, not a proven safe simultaneous-active-query count; observe resource usage during further rollout. Earlier PgBouncer transaction per-DB2/aggregateyoudo10 limits remain.
