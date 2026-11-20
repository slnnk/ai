---
system: nomad-test
status: verified
checked: 2026-10-22
tags: [b2b, auth, pgbouncer, incident]
---
# B2B auth connection errors: missing PgBouncer database mappings

## Task

Investigate reported B2B test authorization database connection errors. User proposed MD5 as a possible cause. Read-only checks found missing database mappings instead. User explicitly approved adding six mappings and reload, then expanded the request to every test stand. Separately approved moving one rotated log archive to the data disk after a full root filesystem blocked the configuration backup.

## Context

B2B PostgreSQL and PgBouncer: `10.18.26.44`, `postgres-b2b.service.vk-test.consul`, ports `5432` and `5433`. Service `youdo-business-auth-service` runs on `test10` through `test15`. [Platform map](../systems/nomad-test.md). Access: workstation SSH as `youdo`, passwordless sudo; service credentials read into memory from Nomad using the existing token in `current/.env`.

## Actions

- Read Nomad job specifications and recent stdout/stderr for all six active stands.
- Used actual service credentials for twelve read-only `SELECT 1` checks, direct PostgreSQL and PgBouncer for each database.
- Inspected PgBouncer configuration, auth verifier type and disk usage without exposing credentials.
- First authorized configuration attempt failed creating its backup with `No space left on device`; configuration and service were not changed by that attempt.
- User-approved move: `/var/log/postgresql/pgbouncer.log.1` to `/data/pgbouncer.log.1.saved-20261022`; preserved 1451717537 bytes, root usage fell from 100% to 85%, leaving 1.4 GB free.
- User-approved addition of fourteen explicit database mappings followed by `systemctl reload pgbouncer` at `2026-10-22T08:15:37Z`. Backup `/etc/pgbouncer/pgbouncer.ini.before-auth-mappings-20261022T081537Z`. PID remained `240513`, service active.
- Repeated all twelve SQL probes and read fresh application log tails and task states.

## Findings

All six active stands logged `08P01: no such database: testNN_youdo-business-auth-service`. The databases existed and direct PostgreSQL probes passed; PgBouncer probes failed because its database list contained only TKB and Tochka entries, with no wildcard mapping.

`auth_type = md5` was already configured; the `youdo` auth-file verifier is SCRAM. No authentication setting, password or verifier needed changing. PostgreSQL had 434 connections with a limit of 1000 at initial inspection.

After reload, all six databases pass `SELECT 1` on both ports. Both web tasks on each stand remain running with zero restarts; recent fetched log fragments no longer contain the earlier connection errors. No end-to-end authorization transaction was performed.

## Changes

Added explicit same-name database mappings to `127.0.0.1:5432` for `test`, `test1` through `test7`, and `test10` through `test15` in `/etc/pgbouncer/pgbouncer.ini`. Existing mappings/settings preserved. The other eight stand databases do not currently exist; mappings prepare future ordinary deployments without creating databases or launching services. Moved only the approved rotated archive; active logs and database data preserved. No repository, CI, deployment or external tracker changes.

Local generated diagnostic helpers and sanitized evidence: `/home/slnnk/ai-data/b2b-auth-diagnosis/`. `runtime.json` and `database.json` reflect the latest verification rather than immutable before/after snapshots.

## Status and risks

Connection incident resolved on the six active stands; mappings prepared for all fourteen supported test stands. Remaining operational proposal (not implementation permission): review log retention and canonical configuration persistence, tracked in the central `~/ai/TODO.md` nomad-test section. Root logs were approximately 6.8 GB before archive relocation, including large current and rotated PgBouncer/syslog files; freeing space does not establish long-term disk stability. Authentication flow and future stand launches remain untested.


## Read-only follow-up (2026-11-19 MSK)

After the corporate VPN was connected, SSH to `vk-ms1-pg-b2b-test` succeeded. At 01:47 MSK, root was 39% used with 5.4 GiB free and `/data` was 40% used with 34 GiB free. `/var/log` occupied 1.6 GiB, including 915 MiB under journal and 293 MiB under postgresql. The saved 1.4 GiB archive remained on `/data`. PostgreSQL 16 and PgBouncer were active and accepted local connection probes on ports 5432 and 5433. The last 10,000 lines of the active PgBouncer log contained zero `no such database` entries, 5,370 connection-closing entries and 3,932 login-attempt entries. The PostgreSQL wildcard logrotate rule covers PgBouncer logs weekly, retaining ten rotations. Syslog rotates weekly and retains four. Both rules compress older files and specify no size cap. This snapshot verifies current headroom and listener state. Application authentication and long-term disk growth were outside this check. The existing TODO proposal remains open pending the user's decision.


## Provisioning provenance (2026-11-19)

The local automation-services checkout was inspected at cached origin/master `72002f69` and historical commit `db986d40`. The VK inventory lists this host in `pg_test`. Its `postgresql.yml` play manages base Linux, Zabbix, Consul and Alloy. It contains no PostgreSQL server installation. The host APT log records `apt-get install -y postgresql-16 postgresql-client-16` on 2026-10-12, consistent with an out-of-playbook installation. The initiating shell or script is unknown.

The PgBouncer APT command on 2026-10-13 matches Ansible's apt module invocation. The separately tracked `pgbouncer-vkcloud.yml` first appears on 2026-10-15 in `f7cc15dd`, so the exact source of the earlier run is unknown. The tracked playbook installs the package, sets the listen address and port, and manages the service. The database mappings applied in this incident are outside those tasks.


## Log rotation proposal (2026-11-19)

A read-only follow-up found 9,712 PgBouncer matches in the last 10,000 syslog lines. PgBouncer has an explicit logfile and systemd captures its output in the journal. The package rule rotates PostgreSQL and PgBouncer logs weekly with `copytruncate`. The rsyslog rule uses its packaged postrotate hook. The logrotate timer runs daily.

Proposed host-scoped policy: use hourly logrotate checks, `maxsize 100M` on the rules that cover PgBouncer and syslog, and keep weekly rotation with compression. Disable routine PgBouncer connection and disconnection logging while preserving pooler error logging. Validate the rendered rules and post-rotation writes. On 2026-11-19 the user deferred log rotation changes until the disk filling problem recurs. The existing TODO records the deferral. The separate configuration persistence proposal is updated by the fallback verification below.

## PgBouncer fallback verification (2026-11-19)

A read-only diff against the October 26 backup shows one addition to the active file under `[databases]`: `* = host=127.0.0.1 port=5432`. All fourteen explicit auth database mappings remain. The service started on November 13 with this path and port 5433 accepts connections. No test connection to a database relying on the fallback was performed.

GitLab GET confirmed [automation-services MR !1386](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1386) open against master. The source head `cbb0b8b3` has the fallback task and B2B host variable. The current master files have neither. The fallback supersedes the earlier proposal to code individual mappings for new B2B databases. The MR decision was pending at the time of verification. Later on 2026-11-19 the user identified this as another team member’s responsibility and requested closing the combined log rotation and PgBouncer item in the central TODO. This is a backlog closure. No log rotation change or MR merge was performed during closure.

## Portable lesson

none
