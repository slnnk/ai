---
system: postgresql
status: verified
checked: 2026-06-25
tags: [postgresql, npgsql, scram-sha-256, md5, password_encryption, pg_hba, docker, kubernetes]
---
# Old Npgsql client: `Authentication method not supported (Received: 10)` against PostgreSQL 14+

## Symptom

A .NET service using an old Npgsql version fails to connect to a freshly created PostgreSQL
(14, 15, 16 official image) with:

```text
Npgsql.NpgsqlException: Authentication method not supported (Received: 10)
```

Newer clients connect fine to the same server. The problem appears with disposable databases
created by a container/Helm chart, where you cannot upgrade the client quickly.

## Cause

Auth message type 10 is `AuthenticationSASL`. PostgreSQL 14+ defaults to
`password_encryption = scram-sha-256`, so the bootstrap role's password is stored as a
SCRAM hash and `pg_hba.conf` requests SCRAM. Old Npgsql (and other old drivers) only speak
`md5`.

Setting only `POSTGRES_HOST_AUTH_METHOD=md5` (official image) or `password_encryption=md5`
is **not enough**: `pg_hba.conf` will say `md5`, but the role created by `initdb` still has a
`SCRAM-SHA-256$...` hash in `pg_authid`, and the server cannot do md5 auth with a SCRAM hash.
The client keeps receiving the SASL request.

## Fix

Store the role password as an md5 hash. In the running instance:

```sql
SET password_encryption = 'md5';
ALTER ROLE CURRENT_USER WITH PASSWORD '<same password>';
SELECT rolname, left(rolpassword, 3) FROM pg_authid WHERE rolname = CURRENT_USER;  -- expect md5
```

For a container/chart, make it automatic and idempotent (official image, `postStart` hook or
init script). The hook must **retry** until the server and `POSTGRES_DB` exist, otherwise it
races `initdb` and the container restarts once with `FailedPostStartHook`:

```yaml
env:
  - name: POSTGRES_HOST_AUTH_METHOD
    value: md5
  - name: POSTGRES_INITDB_ARGS
    value: "--auth-host=md5 --auth-local=md5"
lifecycle:
  postStart:
    exec:
      command:
        - sh
        - -c
        - |
          until psql -U "$POSTGRES_USER" -d postgres -v ON_ERROR_STOP=1 \
              -c "SET password_encryption='md5'; ALTER ROLE CURRENT_USER WITH PASSWORD '$POSTGRES_PASSWORD';" \
              >/dev/null 2>&1; do sleep 2; done
```

Also add `password_encryption=md5` to the server config (`-c password_encryption=md5`) so
later `ALTER ROLE`/`CREATE ROLE` keep producing md5 hashes.

## Limits

- md5 is deprecated and weaker than SCRAM; use this only for throwaway dev/test databases or
  as a bridge until the client library is upgraded (Npgsql >= 4.0 supports SCRAM).
- Check both sides: `pg_hba.conf` method **and** the stored hash prefix in `pg_authid`.
- Existing volumes keep old hashes; the `ALTER ROLE` must run against them too.
