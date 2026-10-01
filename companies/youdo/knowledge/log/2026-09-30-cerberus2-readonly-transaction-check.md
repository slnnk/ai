---
system: cerberus2
status: verified
checked: 2026-09-30
tags: [postgres, selectel, cerberus2, readonly]
---
# Cerberus2: 25006 read-only transaction on user ban insert


## Task

Explain `Npgsql.PostgresException 25006: cannot execute INSERT in a read-only transaction` in cerberus2 API (`UsersController.UnbanUser` -> `UserGrain.ChangeBanState` -> `UserRepository.SetUserBan`, `src/Cerberus.Data/UserRepository.cs:109`). Read-only DB check only.

## Context

- App uses one connection string `PostgreSql` from Vault `secret/dotnet/cerberus2` (`devops/production.hcl`), no read replica split in code.
- Prod DB: Selectel DBaaS, host `master.93570de9-4f4b-4932-9f57-b641e7ceb290.c.dbaas.selcloud.ru`, port `5433` (connection pooler, rejects startup `options`), database `cerberus`, user `youdo`, `SSL Mode=Disable`. Shared cluster with ~28 other service databases.
- User supplied the string in untracked `devops/.env` of the cerberus2 checkout (secret; must not be committed).

## Actions

- Queries run only inside `BEGIN TRANSACTION READ ONLY; ... ROLLBACK;` via psql, `PGSSLMODE=disable` (libpq default verify failed on cert).
- Checked `pg_is_in_recovery()`, `pg_settings`, `pg_roles.rolconfig`, `pg_db_role_setting`, `pg_postmaster_start_time()`, `pg_stat_replication`, `pg_stat_activity`, hourly counts in `user_bans_events`.

## Findings

- 2026-09-30 18:35: primary, `pg_is_in_recovery() = f`, PostgreSQL 16.15, one sync streaming replica.
- `default_transaction_read_only = off` (source `database`); every database, incl. `cerberus`, has explicit `default_transaction_read_only=FALSE` in `pg_db_role_setting` (hypothesis: left by a DBaaS/DBA read-only toggle, e.g. disk-full protection or maintenance). Role `youdo` has no rolconfig.
- Postmaster started 2026-09-29 21:07:54 +03; all 54 app pooler backends started from 21:17:17 -> restart/switchover yesterday evening.
- Inserts into `user_bans_events` succeed continuously (last 2026-09-30 18:32), no gap except sparse hours.
- Conclusion: DB is writable now; the 25006 errors are transient — most likely during the 2026-09-29 ~21:07-21:17 restart/switchover (pooler routed to a standby / old primary) or a temporary read-only toggle. Confirm by the error timestamps in Exceptional.

### Update 18:45 (errors continue, last at ~18:32)

- Errors are not limited to the restart window: `DELETE` in `UserRepository.ChangeBanStateExecuted` fails now. On the primary since restart: `user_bans_commands` 77 ins / 72 del; 5 commands stuck (sent 18:12-18:18, not deleted).
- All live Orleans silos (`orleansmembershiptable`, status 3: 172.24.0.11-13 = msk3-nomad01..03, started 2026-09-10, never restarted) use this cluster; Consul dc `selectel` services `cerberus2`, `cerberus2-api`.
- No `SET ... read_only` in `pg_stat_statements` (only DBaaS monitoring `SHOW default_transaction_read_only`). `master.` resolves to 172.28.0.51 only; replica pooler not reachable, so stale connections to old primary are unlikely.
- Server backends churn continuously, except those from right after promotion: cerberus pids 89656, 90343 (backend_start 2026-09-29 21:17), also antifraud2 24, textvalidation 4, daily_compilations 1.
- Hypothesis (unverified: other sessions' GUCs are not visible to a non-superuser): backends opened while DB-level `default_transaction_read_only` was still `true` during the switchover keep read-only for life (DB settings apply at backend start only); the pooler hands them to random clients -> intermittent 25006. Fix candidates (state-changing, need approval): `pg_terminate_backend` of the old backends, or pooler restart via Selectel support.

- 2026-09-30 ~18:50, with user approval: `pg_terminate_backend` of cerberus pids 89656, 90343 (idle, from 2026-09-29 21:17). Orleans reconnected; watch Exceptional for further 25006 to confirm the hypothesis.

- Retry logic: `BanExecutorGatewayGrain.Process` (timer 10 s) re-publishes the oldest pending `user_bans_commands` row per user when `date_sent` is older than 1 h; on failure `UserBanExecutedProcessor` does `Nack()` and logs, the completion message is not retried by itself. Stuck events 6007998, 6007999, 6008013, 6008014, 6008016 were resent hourly (log state 2), next retries ~19:12-19:18. Failed API `SetUserBan` (unban) rolls back and is not retried: callers must repeat.

- 18:50 `UpdateIAmAlive failed` 25006 on silo 6563baca46d5 (172.24.0.13, msk3-nomad03) AFTER the backend termination -> old-backend hypothesis refuted. IAmAlive (~5 min) fails mostly on .13 (15:35, 15:40, 15:50 UTC missed), .11/.12 fine. New hypothesis: silo .13 reaches a non-primary DB node (stale DNS/CNAME or different resolver/route). On msk3-nomad01 `master.` resolves to 172.28.0.51 (CNAME 8750c811-bd30-429c-a07c-bd921ab7c593.ru-2.c.dbaas.selcloud.ru), resolver 172.24.0.11. SSH to msk3-nomad03 by name failed with `Host key verification failed` only because `known_hosts` had no entry for the name (BatchMode cannot accept a new key); the IP entry exists and `ssh root@172.24.0.13` works — not a key change.

- ~18:53 user restarted worker on msk3-nomad03: new silo writes IAmAlive fine (no 25006) but stuck in Joining — Orleans join ping to silo on .12 timed out (".12 not answering"; `Remote socket closed while receiving connection preamble` every 10 s is the Consul TCP check, noise). ~18:59 user restarted worker on msk3-nomad02 -> by 19:00:49 all three silos Active (.11 1c9cec70ad60, .12 ec03aea28085, .13 f95cbaebb6aa). Silo .11 not restarted yet. Lesson: after a DB primary switchover restart all long-lived Orleans silos one by one.

- Verified 2026-10-01 00:02: all 5 stuck commands executed on the 19:12-19:18 resend (state 3), `user_bans_commands` empty; since 19:00 every created command is sent and executed within the hour; silos .11/.12/.13 Active. Not done (user decided 2026-10-01 to stop work on cerberus2): restart silo on .11, repeat failed API unbans.

## Changes

None on the server. Local helper script only in the session scratchpad.

## Open items

- Match Exceptional timestamps of 25006 errors with 2026-09-29 21:07-21:17; if errors continue after that, check the Vault connection string matches `devops/.env` and ask Selectel about read-only events.

## Portable lesson

Selectel DBaaS pooler port 5433 rejects `PGOPTIONS=-c ...`; enforce read-only with an explicit `BEGIN TRANSACTION READ ONLY`.
