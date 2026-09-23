---
system: terraform
status: verified
checked: 2026-09-21
tags: [terraform, postgresql, provider, grants, parallelism, XX000, concurrency]
---
# Terraform PostgreSQL provider: `pq: tuple concurrently updated (XX000)` on parallel grants

## Symptom

An apply of a grants stack built on the `cyrilgdn/postgresql` provider (`postgresql_grant`,
`postgresql_default_privileges`) fails part-way with:

```text
could not execute revoke query: pq: tuple concurrently updated (XX000)
```

Only one or two resources fail; sibling resources for the same database and schema, but
other roles, succeed in the same run. The CI runner and the database are healthy and the
job runs for only a few tens of seconds. Retrying sometimes succeeds and sometimes fails
on a different resource.

## Cause

The provider implements every grant resource as a `REVOKE ... ; GRANT ...` reconciliation on
the target object's ACL. Terraform applies independent resources concurrently (default
`-parallelism=10`). When a module creates one `postgresql_grant` per role with `for_each`,
several resources update the ACL of the *same* catalog row at the same time (for schema
grants this is the `pg_namespace` tuple; for `object_type = "table"` or `"sequence"` it is
each relation's `pg_class` row). PostgreSQL does not serialise catalog ACL updates with
row locks; the second writer sees a tuple that changed under it and aborts with the
internal error class `XX000`. This is a race in the apply, not a data or permission
problem.

## Fix

Serialise the ACL mutations.

Operational retry after a partial apply (completed resources are already in state):

```bash
terraform apply -input=false -auto-approve -parallelism=1
terraform plan -input=false -detailed-exitcode   # expect exit 0: nothing left
```

Durable fix in CI: add `-parallelism=1` to the apply (and plan) command of the grants stack,
or set `TF_CLI_ARGS_apply="-parallelism=1"` for that job. Alternatively chain the per-role
resources with `depends_on` so grants on one object never run concurrently; this is harder
to express with a flat `for_each` map and usually not worth it for a small stack.

Treat a failed apply as partial: check state and the actual ACLs (`\dn+`, `\dp`) before
assuming nothing was changed.

## Limits

- `-parallelism=1` slows the whole stack; for large grant matrices consider splitting the
  stack per database instead.
- The race also exists between table-level and sequence-level grants in the same run, so a
  retry at default parallelism can fail again at a later layer even after schema grants
  are in state.
- Seen with the `cyrilgdn/postgresql` provider on a managed PostgreSQL service; the same
  mechanism applies to any tool that issues concurrent `GRANT`/`REVOKE` on one object.
