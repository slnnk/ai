---
system: zabbix
status: verified
checked: 2026-11-05
tags: [zabbix, postgresql, docker, incident]
---
# DevOps-909: Zabbix outage after Docker started before data disk mount

## Task
User supplied a Zabbix frontend database-error screenshot and explicitly requested SSH inspection. Read-only diagnosis; no remediation authorized or performed.

## Context
`zabbix-selectel.youdo.local` resolves to172.28.0.120, host `sc-zabbix-01`; SSH root access worked.
Docker Compose definition `/data/docker-compose.yml`. Frontend `data-zabbix-web-nginx-pgsql-1` image `zabbix/zabbix-web-nginx-pgsql:ubuntu-6.4-latest`; server `data-zabbix-server-1` image `data-zabbix-server`; PostgreSQL `data-postgres-1` image `timescale/timescaledb:2.7.2-pg14`.
Root disk20G,77%used/4.5Gfree; separate250G `/dev/sdb` ext4 mounted at `/data` with fstab `defaults,nofail`.

## Confirmed timeline and causal evidence
2026-11-04 14:25:41 UTC /17:25:41 Moscow: Docker attempted automatic container startup after host reboot. PostgreSQL and frontend started.
Server startup failed at OCI mount of `/data/zabbix-server/odbcinst.ini` to `/etc/odbcinst.ini`, reporting directory/file mismatch. Container remains stopped (exit127); no10051 listener.
At14:25:42 UTC new running-cluster `PG_VERSION` was created on root filesystem. PostgreSQL reports postmaster start17:25:46 Moscow.
At14:26:00 UTC /17:26:00 Moscow systemd logged `Mounted /data`, after Docker container startup. Current host ODBC files on `/data` are regular files dated2022, consistent with the earlier missing-volume view.

## PostgreSQL verification
Read-only SQL in the running container reports database/user/schema `zabbix|zabbix|public`, zero public tables and database size9865kB. `public.dbversion` does not exist; neither `hosts` nor `users` appears in pg_tables.
Frontend config targets `postgres`, database/user `zabbix`; Docker DNS resolves it to172.18.0.3. This connects to the wrong newly initialized cluster.
Host `/data/postgresql/data`: device2064, inode9306114; PG_VERSION mtime2025-07-08, pg_control mtime2026-11-04 14:15:50 UTC.
Running PostgreSQL view `/proc/1607/root/var/lib/postgresql/data`: device2049, inode524815; PG_VERSION mtime2026-11-04 14:25:42 UTC.
These are different clusters on separate filesystems: actual mounted data disk versus the root-directory view bound before mount. The old data directory is present; its integrity, table contents and newest metric timestamps have not been verified. Do not claim data recovery or loss.

## Impact and status
Frontend UI and API return missing-dbversion error; API failure was reproduced even without a token. Docker marks frontend healthy despite unusable application DB.
Zabbix server is stopped, so server polling/processing through this instance is unavailable since reboot. Agent/proxy buffering and eventual history recovery remain unknown.
No service/container restarted or recreated; no mount, schema, permissions or data modified. All SSH commands finished; no background operations remain.
[Android diagnosis](2026-11-05-android-farm-dig-job-3278160.md) was blocked by this outage.

## Recovery proposal and authorization boundary
After explicit approval, preserve both clusters, verify the mounted original data directory, and recreate the affected containers so bind mounts point to the mounted disk; do not initialize/import a Zabbix schema into the empty active cluster. Review the exact compose configuration, service names and image behavior before proposing the external mutation command.
A persistent mount dependency for Docker or this stack is a separate proposed change; confirm the chosen scope before implementation. Remaining work is recorded in [central TODO](../../../../TODO.md), not authorized by this note.

## Portable lesson
none

## Stage1 read-only preflight completed (2026-11-05)
User explicitly requested execution of the previously described read-only checks. No recovery mutation was authorized.
`/data` is `/dev/sdb`, ext4/rw,246G total/114G used/119G available,1%inode usage. Current-boot kernel log shows ext4 recovery completed and no matching block I/O errors; this is not an offline filesystem integrity test.
Original PG_VERSION is14; pg_controldata from the existing PostgreSQL image was executed read-only using that image's musl loader via `/proc/1607/root`, without starting another container or copying tools to the host. It returned exit0 and readable control metadata; a loader current-directory warning preceded the normal output.
Original system identifier7524782209084661789; control version1300/catalog202107181. State `in production`, control updated Nov4 17:15:50 Moscow, latest checkpoint17:11:20. Crash recovery will be required at first start; successful recovery or complete WAL continuity has not been established.
Checkpoint REDO WAL `0000000100000A6900000040` exists and is16MiB. Page checksums are disabled; no full data-page or SQL integrity check was possible offline.
Original postmaster.pid remains from the prior instance; it was not removed. Every inspected postgres process has cwd device2049 (root filesystem), not2064 (original /data filesystem).
ODBC bind sources are regular readable root-owned0644 files. Driver section `mssql` points to `/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.1.1`; library existence within the stopped server filesystem was not checked.
The available Compose executable is `/usr/local/bin/docker-compose`, version2.27.1; `docker compose` is unavailable. Required `--no-deps`, `--force-recreate`, `--no-build` and `--pull` flags are supported.
Compose service names are `postgres`, `zabbix-server`, `zabbix-web-nginx-pgsql`, `zabbix-java-gateway`, project `data`. Server uses host networking and local build image; frontend resolves postgres through Compose networking. All services use restart always; dependencies only require service_started and do not wait for database readiness.
Current local image tags match actual container image IDs. PostgreSQL image is14.4/Timescale2.7.2; both server and frontend report Zabbix6.4.21. No image upgrade/build is needed.
Prepared exact per-service stop/recreate commands and intervening read-only verification gates in `/home/slnnk/ai-data/zabbix-recovery/recovery-proposal.json`. They are proposals only, require preservation/backup before recovery, and must receive per-command external-change approval. No command in that proposal was executed.
Preflight is complete; remaining recovery/backup and persistent mount ordering remain the existing central TODO proposal. All task SSH commands have finished; no background operations remain.

## Approved recovery stage: stop wrong-cluster containers (2026-11-05)
The user explicitly skipped the proposed backup/snapshot step (`Пропустим этот шаг`). No backup was created; this supersedes the proposal's backup prerequisite for this recovery only.
User then approved the exact stop command with `Да`: `/usr/local/bin/docker-compose -p data -f /data/docker-compose.yml stop zabbix-web-nginx-pgsql postgres` on172.28.0.120.
Executed at18:31:28 Moscow; SSH/Compose completed exit0. Both frontend and PostgreSQL report `Exited (0)`. Server remains stopped exit127; Java gateway remains running. Ports80/5432/10051 are no longer listening.
Read-only verification confirms `/data` remains mounted from `/dev/sdb`, original cluster device2064/inode9306114 unchanged.
No containers or data removed. No PostgreSQL recovery start yet. Next proposed command recreates only PostgreSQL on original mounted data with existing image, no build/pull; separate approval pending. No background commands remain.

## DevOps-909: original PostgreSQL recovery completed (2026-11-05)
User approved the exact PostgreSQL recreate/start command with `Да` and assigned all Zabbix recovery work to DevOps-909. This is separate from the Android image/endpoints task DevOps-908.
At18:35:21 Moscow executed `/usr/local/bin/docker-compose -p data -f /data/docker-compose.yml up -d --no-deps --force-recreate --no-build --pull never postgres`, exit0. Existing image retained; PostgreSQL skipped initialization and opened the original disk cluster.
Host and container data paths now match device2064/inode9306114. System identifier7524782209084661789 matches the preflight original cluster.
Logs: automatic recovery started18:35:22, REDO completed atA69/4527D888, ready to accept connections18:35:23. pg_isready passed; pg_is_in_recovery=false.
Read-only SQL: dbversion6040000/6040036,355 hosts-table rows,69135 item rows, database70GB. These row counts include Zabbix templates/discovery records; do not present them as355 active monitored machines.
Sample Enabled-host agent.ping histories are present up to Nov4 17:16:06–17:16:38 Moscow for five inspected hosts, value1. This is a sample, not a global latest timestamp or full history integrity check. Initial parent history table statistics were zero due to partitioning and were not interpreted as missing history.
PostgreSQL restoration is verified. Frontend and Zabbix server remain stopped; no fresh monitoring collection or UI/API recovery yet. User skipped backup; no snapshot made. No background task commands remain; the PostgreSQL service is intentionally running.
Next proposed approved-scope action is server recreation/start with existing image; a separate per-command confirmation remains required. Full recovery and persistent mount ordering remain in the central TODO.

## DevOps-909: Zabbix server restarted and collecting (2026-11-05)
User approved the exact zabbix-server recreate command with `Да`. Executed at18:37:24 Moscow: `/usr/local/bin/docker-compose -p data -f /data/docker-compose.yml up -d --no-deps --force-recreate --no-build --pull never zabbix-server`, exit0.
Container started18:37:25 using the same image8d9633c62ca2808163bb82664d7c27333f68341d2bc3f295d49ceea9ca0f6a57. Zabbix6.4.21 logs confirm schema06040000/06040036 and required mandatory06040000; main process started18:37:26. TCP10051 listens on IPv4/IPv6.
Read-only SQL confirms a new `msk3-sql01` agent.ping value1 at18:37:38 Moscow, proving collection/history writes resumed after recovery. Other four sampled hosts had not yet refreshed at that observation; do not claim global host recovery.
Initial logs contain missing SNMP MIB definitions and unsupported item warnings including obsolete veth interfaces, plus unknown-host active-check requests. These were observed but not remediated or classified as newly introduced; full item/host health remains unverified.
PostgreSQL and server are running, frontend remains stopped, Java gateway remains running. UI/API recovery and Enabled Selenium inventory check await the separately approved frontend start. No background commands remain.

## DevOps-909: frontend and authenticated API restored (2026-11-05)
User approved the exact frontend recreate command with `Да`. Executed18:41:14 Moscow, exit0: `/usr/local/bin/docker-compose -p data -f /data/docker-compose.yml up -d --no-deps --force-recreate --no-build --pull never zabbix-web-nginx-pgsql`.
Page HTTP200 with login form and title `Zabbix Selectel: Zabbix`, no missing-dbversion error. Token-free apiinfo.version returns6.4.21.
Authenticated Enabled-only Selenium inventory fetched15:41:31 UTC: group61, hosts M-K0056 (visible M-K0056-selenium-hub), M-K0057 and M-K0058. API access is restored; farm historical correlation was not resumed as part of recovery.
All three recreated containers are running with restart count0; frontend health is healthy. Five sampled real monitored hosts now have agent.ping=1 at18:41:06–18:41:38 Moscow.
Runtime recovery is complete. This supersedes earlier server/frontend/API-unavailable statuses. Full host/item health, MIB cleanup and outage-period proxy backfill were not established.
Docker has no RequiresMountsFor or drop-ins and its After set lacks data.mount. Thus boot ordering remains uncorrected. Propose `/etc/systemd/system/docker.service.d/10-data-mount.conf` with `[Unit]` / `RequiresMountsFor=/data`, followed by daemon-reload and read-only dependency verification. This affects Docker startup ordering on the whole host; no daemon restart or reboot is needed just to load the dependency. File write, daemon-reload and any reboot each need applicable external-change approval.
Remaining prevention proposal is in central TODO under Zabbix. No recovery commands are still running; PostgreSQL/server/frontend services are intentionally running. No backup was made, as explicitly directed.

## DevOps-909: persistent mount dependency applied (2026-11-05)
User explicitly declined adding this to the automation-services role and requested a host-local systemd change. After the exact file/content/daemon-reload/no-restart proposal, user instructed `Сделай изменения`, authorizing that concrete change.
Preflight confirmed no existing drop-in at the proposed path, no Docker drop-ins, and `/data` mounted from `/dev/sdb`.
Created root-owned0644 `/etc/systemd/system/docker.service.d/10-data-mount.conf` with exactly:

```ini
[Unit]
RequiresMountsFor=/data
```

Executed `systemctl daemon-reload` successfully, without restarting Docker or rebooting. Loaded unit properties now include RequiresMountsFor=/data, Requires=data.mount, After=data.mount and the exact drop-in path. Docker remains active.
All four container IDs, StartedAt timestamps and RestartCount values matched before/after the change. PostgreSQL/server/frontend remained running; frontend was healthy at preflight.
The runtime recovery and agreed persistent dependency work are complete; central DevOps-909 backlog entry is closed. Earlier pending prevention statuses in this log are historical and superseded.
Actual reboot/mount-failure behavior was not tested; this is a verification limitation, not an authorized pending reboot. No role/repository/Compose/fstab modifications were made. Residual MIB/item issues remain outside this recovery scope.
No background task commands remain; production service containers are intentionally running. Backup was skipped by explicit user decision.

## Final acceptance: no reboot test (2026-11-05)
User explicitly decided `Проверку перезагрузкой делать не будем.` Reboot validation is declined, not pending or deferred. DevOps-909 remains complete based on runtime recovery, UI/API/inventory/fresh-metric verification and loaded systemd dependency checks. Do not propose or execute a reboot for this task without a new user request. No external changes or background commands were performed in this acceptance step.

## DevOps-909 recovery comment published (2026-11-05)
User explicitly requested posting the prepared recovery summary with incident/recovery times and excluding the reboot-test sentence. Read-only inspection confirmed issue `71-139085` / DevOps-909, summary `[Zabbix] Не работает в Selectel`, with zero comments.
Created one comment `74-125195` using POST; read-back verified exact text. It records Nov4 ~17:25 Moscow outage, Nov5 18:37 collection recovery and18:41 UI/API recovery, mount-order cause, original DB/WAL restoration and RequiresMountsFor=/data mitigation. The requested reboot sentence is absent.
Only a comment was added; issue state and other fields were not changed. Local text and publication receipt are in `/home/slnnk/ai-data/zabbix-recovery/youtrack/`. No background operations remain.
