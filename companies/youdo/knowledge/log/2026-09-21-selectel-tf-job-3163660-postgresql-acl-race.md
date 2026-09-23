---
system: selectel
status: verified
checked: 2026-09-21
tags: [terraform, postgresql, grants, gitlab-ci, job-3163660, prod-dbaas-grants, incident]
---
# selectel-tf job 3163660: PostgreSQL ACL concurrency race

## Task

Explain why `apply:prod-dbaas-grants` (job 3163660) failed while adding two databases to
the baseline grants matrix, and how to retry safely.

## Context

- Date checked: 2026-09-21 (Europe/Moscow).
- Repository: `/home/slnnk/git/selectel-tf`.
- GitLab project: `sysadmins/selectel/selectel-tf` (project ID 552).
- Merge request ref: `refs/merge-requests/87/head`, commit `4d59b9e389b9ade5e00632d9c534cac2346f2025`.
- Pipeline/job: pipeline 139112, `apply:prod-dbaas-grants`, job 3163660.
- Terraform stack: `prod-dbaas-grants`; Consul state path `terraform/selectel-prod-dbaas-grants`.
- Runner: `gitlab-runner-docker-1 (172.28.0.171)`, runner ID 105; it remained online.

## Change being applied

MR !87 adds two databases to the baseline grants matrix:

- B2B: `youdo_mcp`.
- C2C: `giveaway_bot`.

The final commit only fixed a missing trailing comma. The plan contained 42 additions and no changes or destroys.

## Findings

### Failure

Terraform successfully created many grants/default privileges, then PostgreSQL returned:

```text
could not execute revoke query: pq: tuple concurrently updated (XX000)
```

Failed addresses:

- `module.b2b_grants.postgresql_grant.schema["youdo_mcp/readonly"]`.
- `module.c2c_grants.postgresql_grant.schema["giveaway_bot/migration_runer"]`.

Both point to `prod-dbaas-grants/modules/db_grants/main.tf`, resource
`postgresql_grant.schema` (line 39 in the CI checkout).

### Root cause

This is an ACL update race in PostgreSQL, not a runner/network outage and not an
invalid database name. The module creates one `postgresql_grant.schema` resource per
role. Terraform runs these resources concurrently. For each new database, several
resources therefore execute the provider's `REVOKE`/`GRANT` reconciliation against
the same `pg_namespace` ACL tuple at once. PostgreSQL rejects one of the concurrent
tuple updates with SQLSTATE `XX000`.

The same concurrency risk exists at the next layer for table/sequence grants: several
role-specific resources can update ACLs of the same objects concurrently.

### State and recovery implications

- The apply was partial. Successful resources were created before Terraform exited;
  do not assume nothing changed.
- There were four successful schema grants in each newly added database; only one
  schema grant per database shown above failed in this run. Several default privilege
  resources also completed.
- A normal retry may progress because completed resources are now in state, but it can
  race again when table/sequence grant resources start.
- Safest operational retry: serialize the apply, for example
  `terraform apply -input=false -auto-approve -parallelism=1` in
  `prod-dbaas-grants`, then run a plan and confirm it is empty.
- Durable CI fix: serialize this stack (at minimum its PostgreSQL ACL mutations), for
  example by adding `-parallelism=1` to the apply command. A more granular dependency
  chain is possible but harder with the current `for_each` resource layout.

## Actions: evidence and checks

- Read job metadata and trace through GitLab API using the existing
  `GITLAB_YOUDO_TOKEN`; no token value was recorded.
- Job duration was about 33 seconds and `failure_reason=script_failure`.
- Runner and runner manager both reported online after the failure.
- No retry of `apply:prod-dbaas-grants` existed in pipeline 139112 at check time.

## Open items

- Retry the apply serialized (`-parallelism=1`) and confirm an empty plan afterwards.
- Add `-parallelism=1` (or a dependency chain) to the CI apply of `prod-dbaas-grants`.

## Portable lesson

[Terraform PostgreSQL provider: `tuple concurrently updated (XX000)` on parallel grants](../../../../general/knowledge/terraform/postgresql-grant-tuple-concurrently-updated.md)
