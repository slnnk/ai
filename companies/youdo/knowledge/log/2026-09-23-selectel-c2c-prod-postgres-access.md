---
system: selectel
status: verified
checked: 2026-09-23
tags: [postgres, selectel, dbaas, c2c, prod]
---
# Access to prod Selectel DBaaS PostgreSQL cluster C2C

## Task

Prepare access variables for the prod PostgreSQL cluster C2C in Selectel DBaaS, check the
connection and list the databases.

## Context

- Cluster: C2C, Selectel DBaaS PostgreSQL, **prod**.
- Endpoint: `master.93570de9-4f4b-4932-9f57-b641e7ceb290.c.dbaas.selcloud.ru:5433`
  (port 5433 is the connection pooler, not the backend directly).
- Server: PostgreSQL 16.14, the `master.` endpoint is the primary (`pg_is_in_recovery() = f`).
- Related: Terraform grants for C2C in [[2026-09-21-selectel-tf-job-3163660-postgresql-acl-race]].

## Actions

- Variables in `~/ai/current/.env` (values filled by the user):
  `SELECTEL_C2C_PROD_PG_HOST`, `SELECTEL_C2C_PROD_PG_PORT`, `SELECTEL_C2C_PROD_PG_USER`,
  `SELECTEL_C2C_PROD_PG_PASSWORD`, `SELECTEL_C2C_PROD_PG_DB`.
- The password contains shell metacharacters, so its value is wrapped in single quotes;
  otherwise `. .env` fails with a syntax error.
- Connection, read-only:

      set -a; . ~/ai/current/.env; set +a
      PGHOST=$SELECTEL_C2C_PROD_PG_HOST PGPORT=$SELECTEL_C2C_PROD_PG_PORT \
      PGUSER=$SELECTEL_C2C_PROD_PG_USER PGPASSWORD=$SELECTEL_C2C_PROD_PG_PASSWORD \
      PGDATABASE=$SELECTEL_C2C_PROD_PG_DB PGSSLMODE=disable \
      psql -X -c 'begin transaction read only' -c '\l'

## Findings

- The user asked for `sslmode=disable`; it works. Traffic, including credentials, is then
  unencrypted.
- With `sslmode=require` psql 12 fails with `certificate verify failed` because
  `~/.postgresql/root.crt` holds a Yandex internal CA (it is picked up automatically).
  TLS works with the Selectel CA from `https://storage.dbaas.selcloud.ru/CA.pem`
  (`CN = SelectelCloudDBaaS-RootCA`, valid to 2035-06-28) and `sslrootcert=<file>`,
  `sslmode=verify-full`.
- The pooler rejects startup `options` (`FATAL: unsupported startup parameter in options:
  default_transaction_read_only`), so `PGOPTIONS` cannot be used; start a read-only
  transaction instead.
- The access user is the owner of most databases, so it has write rights on prod.
- 33 non-template databases (2026-09-23). Largest: `antifraud2` 167 GB, `youdo_mindbox`
  74 GB, `youdo_mailer` 41 GB, `mindbox_analytics` 19 GB, `bruteforcingdetector` 16 GB.
  Others: `attribution`, `badgekeeper`, `broadcast`, `cerberus`, `daily_compilations`,
  `dba_local`, `dev_metrics`, `doc_validation`, `eventum`, `featuretoggle`, `fns`,
  `giveaway_bot`, `intercom_logs`, `postgres` (no CONNECT), `premoderation_machine`, `seo`,
  `smm_reach`, `sorm`, `textvalidation`, `ugc_bot`, `user_insurance`, `youdo_call_service`,
  `youdo_dengage`, `youdo_jivo_bot`, `youdo_search`, `youdo_sms_service`,
  `youdo_sms_service_2025_05_30`, `youdo_trackingpixel`.
- `sorm` (2026-09-23): `datacl = {youdo=CTc/youdo}`, PUBLIC has no CONNECT. Role `readonly`
  (also `backup`, `replication`) has `USAGE` on `public` and `SELECT` on all 17 tables, plus
  default privileges from `youdo`, but no `CONNECT` on the database, so it cannot log in to
  `sorm`. `readonly` also lacks CONNECT on `antifraud2`, `dba_local`, `giveaway_bot`,
  `postgres`; it has CONNECT on all other databases. The fix would be
  `GRANT CONNECT ON DATABASE sorm TO readonly` (not applied; may be a deliberate restriction).
- Re-checked 2026-09-23 13:51 MSK: someone else granted access, `datacl` is now
  `{youdo=CTc/youdo,readonly=CTc/youdo}`. `readonly` has CONNECT and SELECT on 17/17 tables,
  but the grant also includes `CREATE` (C) and `TEMPORARY` (T) on the database, i.e.
  `GRANT ALL ON DATABASE`, not just CONNECT.
- 13:56 MSK: login role `kmikhaylov` exists (not present in the earlier role list, created
  today), no role memberships. It has `CTc` on database `sorm` and `USAGE` on `public` (via
  PUBLIC), but SELECT on 0/17 tables and no default privileges, so it can connect but cannot
  read data. Options: `GRANT readonly TO kmikhaylov` or
  `GRANT SELECT ON ALL TABLES IN SCHEMA public TO kmikhaylov` (not applied).
- 14:01 MSK, after the user granted manually: `kmikhaylov` has all table privileges
  (SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER) on 17/17 tables and
  USAGE, SELECT, UPDATE on 8/8 sequences in `sorm.public`. No schema CREATE, no default
  privileges (new tables created by `youdo` will not be accessible), no role memberships.
- `youdo` has no `CREATEROLE` and no `ADMIN OPTION` on any role, so it cannot grant role
  membership (e.g. `GRANT readonly TO ...`); only object-level GRANTs.

## Changes

- `~/ai/current/.env`: added the `SELECTEL_C2C_PROD_PG_*` variables.

## Open items

- The password value was printed once in the agent session through a shell syntax error;
  rotation was recommended to the user.
- Consider a separate read-only role for agent access.

## Portable lesson

none
