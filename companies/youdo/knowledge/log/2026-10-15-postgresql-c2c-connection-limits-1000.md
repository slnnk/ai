---
system: postgresql
status: verified
checked: 2026-10-15
tags: [postgres, pgbouncer, capacity, DevOps-899]
---
# C2C PostgreSQL and PgBouncer connection limits increased to 1000

## Summary

User explicitly requested PostgreSQL and PgBouncer limits1000. Both effective values verified1000 on C2C10.18.26.39. PostgreSQL restarted4.362s; PgBouncer reload-only, PID114852 retained. FD soft limit2048 added to support1000clients; hard524288 unchanged.

## Context and authorization

Parallel Cerberus deployment saturated prior max_connections500. SQL snapshot initially failed even for local postgres; read-only backend-process count showed500idle connections. Largest consumers Cerberus_test10/13 each87, test11 65, test14 57, total296 across those4DBs. User explicitly instructed raising both PG and PgBouncer to1000. No unrequested pool-mode/backend-cap/auth changes.

## PostgreSQL change

Only `/etc/postgresql/16/main/postgresql.conf` max_connections500->1000, backup `.devops-899-before-max-connections-1000`. Offline configuration validation passed before restart of postgresql@16-main. RuntimeSQL confirmed1000/pending_restartfalse, version16.15, shared_buffers128MB/work_mem4MB retained. New postmaster start2026-10-15T18:00:12.528082UTC. PgBouncer files/auth hash unchanged by PG step.

Local helper `ai-data/jenkins-recovery/increase-c2c-pg-connections1000-899.py --apply` adapted existing500helper; supports offline preflight only if SQL fails with exact too-many-clients. Actual successful before probe recorded500. Receipt `antifraud-pgbouncer899/pg1000-applied.json`.

## PgBouncer change

Only `/etc/pgbouncer/pgbouncer.ini` max_client_conn500->1000, backup `.devops-899-before-client-limit-1000`. Reload applied without restart, SHOWCONFIG verified1000, PID unchanged. Auth hash and all other runtime settings verified unchanged; user youdo backend cap10 and Antifraud perDBcap2 retained.

For1000client sockets plus backend/service descriptors, prior softnofile1024 insufficient headroom. Added `/etc/systemd/system/pgbouncer.service.d/devops-899-client-limit1000.conf` with LimitNOFILE=2048:524288, systemctl daemon-reload, prlimit current PID soft2048/hard524288. No process restart. Helper increase-pgbouncer-clients1000-899.py --apply; receipt antifraud-pgbouncer899/client1000-applied.json.

## Deployment effects and limits

Cerberus test/test4 retries after capacity increase succeeded. test15 Orleans worker failed with Npgsql53300 before limit change, subsequent regular retry authorized within initial rollout. Five previously successful jobs had no surviving allocations after PG restart (test1/test2/test3/test5/test12); user explicitly chose regular GitLab deploy with DB recreation instead of proposed force-reschedule preservingDB. Recovery ongoing in rollout log. No further PostgreSQL/PgBouncer tuning applied.

Final recovery: all14Cerberus GitLab jobs SUCCESS and all14Nomad jobs running/healthy after user-authorized ordinary retries of five failed runtimes with DB recreation. [Rollout evidence](2026-10-15-jenkins-cerberus-eight-stand-rollout.md).
