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

## Portable lesson

none
