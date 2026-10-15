---
system: postgresql
status: verified
checked: 2026-10-15
tags: [pgbouncer, capacity, DevOps-899]
---

## Summary

User explicitly authorized increasing PgBouncer's client connection limit to500 after transient Antifraud test7 startup saturation at100. Applied on10.18.26.39 using reload only. Live SHOW CONFIG confirms max_client_conn500; process PID114852 unchanged, every other runtime setting unchanged.

## Exact change and verification

File /etc/pgbouncer/pgbouncer.ini, section[pgbouncer], max_client_conn100(default) to explicit500. Backup /etc/pgbouncer/pgbouncer.ini.devops-899-before-client-limit-500. Fileowner/mode preserved, existing unrelated entries and database mappings preserved by semantic assertions, authfile unchanged by SHA256 comparison. Only one new/changed setting.

Preflight process Max open files soft1024/hard524288,94 open descriptors. Soft1024 is sufficient for500clients plus bounded existing backend pools; no systemd limit or service restart was required. Admin console accessed read-only via local Unixsocket as the process UID using special user pgbouncer; no admin_users/auth changes needed.

After systemctl reload pgbouncer, SHOW CONFIG returned500 and all other settings matched preflight. Backend cap remains10 for user youdo across allDBs, Antifraud perDB2/transaction mode. PostgreSQL max_connections remains500 from previous task. No application deployments/restarts, database changes or new GitLabjobs.

## Evidence and limits

Helper ~/ai-data/jenkins-recovery/increase-pgbouncer-clients899.py [--apply], receipts antifraud-pgbouncer899/client500-plan.json and client500-applied.json. Configuration-file edit persists across process restarts; active Ansible source for this PgBouncer config is still absent. Runtime500 verification is not a500-client load test.

## Application health after reload

Read-only Consul verification: all20 Antifraud service checks passing across test2/test3/test4/test5/test7 (API, scheduler, service and Selenium on each). No runtime restarts or corrective actions performed.
