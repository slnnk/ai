---
system: dotnet
status: verified
checked: 2026-09-22
tags: [hangfire, postgresql, 42501, permission-denied, schema, provisioning]
---
# Hangfire worker dies at startup: `permission denied for database` on `CREATE SCHEMA "hangfire"`

## Symptom

On a freshly created (or recreated) database the API and web containers start, but the
background worker crashes in a loop with SQLSTATE `42501`:

```text
Npgsql.PostgresException: 42501: permission denied for database <dbname>
   at Hangfire.PostgreSql.PostgreSqlObjectsInstaller.Install(...)
```

The failing statement is `CREATE SCHEMA "hangfire"`. Migrations ran fine before it; the
container exits 134 and the orchestrator reports no OOM.

## Cause

`Hangfire.PostgreSql` installs its own objects on first use (`PrepareSchemaIfNecessary`,
default `true`). Creating a schema requires the `CREATE` privilege **on the database**, which an
application role with only table-level grants does not have. Your migration tool runs with the
same role and never touched the `hangfire` schema, so nothing created it in advance.

## Fix

Least privilege (preferred), run once as the provisioning/admin role:

```sql
CREATE SCHEMA IF NOT EXISTS hangfire AUTHORIZATION <app_role>;
```

Then restart the worker; Hangfire logs `Hangfire SQL objects installed.`

Alternatives:

- `GRANT CREATE ON DATABASE <dbname> TO <app_role>;`, let Hangfire install, then `REVOKE` if
  policy requires.
- Make environment provisioning/migrations create and own the `hangfire` schema explicitly
  (add it to the "create database" step for ephemeral stands) so application startup never
  needs DDL privileges. Optionally set `PrepareSchemaIfNecessary = false` in production and
  apply Hangfire's scripts through the migration pipeline.

## Limits

- If the database owner is the application role itself (common when the DB is created by the
  same provisioning step), the error does not appear; it shows up only when the DB is created
  by an admin and the app role gets object grants afterwards.
- Do not read the sibling containers' exit 137 or the deployment progress deadline as the
  cause; they are consequences of the worker failure.
