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

Historical follow-ups were tracked in `~/ai/TODO.md`; DevOps-887 was closed by the user on 2026-10-09 (see closure below).

## Follow-up 2026-10-09

- Tracking issue: [DevOps-887](https://youtrack.youdo.com/youtrack/issue/DevOps-887), created by the user; description confirms parallel permission application failures.
- Local CI still runs `terraform apply -input=false -auto-approve` for `apply:prod-dbaas-grants` (`.gitlab-ci.yml:188`). Recommended scope: add `-parallelism=1` to this job only.
- Grants jobs currently watch only `prod-dbaas-grants/**/*` in `rules.changes`; a CI-only fix needs explicit inclusion of `.gitlab-ci.yml` or another reviewed mechanism to run the relevant jobs.
- Existing schema dependencies for table/sequence grants do not serialize role instances within `for_each`. A finer dependency solution requires module restructuring.
- Read-only investigation only: no repository edits, branch changes, Terraform plan/apply, CI triggers or external writes. Empty plan remains unverified. No implementation branch proposed or approved.
- Updated `~/ai/TODO.md` to link the existing item to DevOps-887.

## DevOps-887 local implementation 2026-10-09

- Repository: `/home/slnnk/git/selectel-tf`; base/target: `origin/master` / `master`. Proposed branch `DevOps-887-serialize-db-grants`; user corrected it to `DevOps-887-db-grants-parallelism` and explicitly authorized creating that branch.
- User scope correction: change only the CI apply command; do not add `.gitlab-ci.yml` to `rules.changes`. This correction is specific to DevOps-887.
- Fetched origin and created the approved local branch from `origin/master` at `adc2822` with no upstream tracking. Checkout was clean before the change.
- Changed only `.gitlab-ci.yml:188`: added `-parallelism=1` to `apply:prod-dbaas-grants`. No Terraform module changes.
- Checks: Python/PyYAML parsing succeeded; `git diff --check` succeeded; reviewed diff contains exactly one command-line change, one insertion and one deletion.
- Limit: existing changes rules still exclude a CI-only diff from grants jobs. No GitLab server lint, CI execution or Terraform apply/plan performed; empty plan remains unverified.
- No staging, commit, push or MR creation; publication approval not requested or received. MR link: none.

## DevOps-887 publication 2026-10-09

- User explicitly approved the proposed commit and MR text and requested publication.
- Commit: `bb9d6749f85746407beba85be9942874b9862433`, message `limit db grants apply parallelism`; exactly one insertion and one deletion in `.gitlab-ci.yml`.
- MR: [!93](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/merge_requests/93), title `DevOps-887 Limit db grants apply parallelism`; source `DevOps-887-db-grants-parallelism`, target `master`.
- Staged diff checked before commit; no pre-staged or unrelated changes included. Branch pushed with upstream tracking. Remote source SHA and MR source/target verified by the publication helper.
- Preserved project preferences: squash disabled, source branch removal enabled; assignee `a.solonenko`.
- No pipelines returned for this SHA immediately after MR creation. No CI job, Terraform apply, merge or deployment was manually triggered; empty plan remains unverified.
- Sandbox DNS prevented push and MR publication; retried with approved escalation. Publication succeeded without duplicate MR creation.

## DevOps-887 closure 2026-10-09

- User reported merging MR !93, posting the prepared task comment, and closing DevOps-887.
- Moved the existing backlog entry to Done in `~/ai/TODO.md` based on the user's explicit closure.
- Terraform apply and a subsequent empty plan were not independently verified by the agent; task closure does not constitute evidence of those runtime checks.

## Portable lesson reference

[Terraform PostgreSQL provider: `tuple concurrently updated (XX000)` on parallel grants](../../../../general/knowledge/terraform/postgresql-grant-tuple-concurrently-updated.md)
