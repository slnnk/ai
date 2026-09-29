---
system: gitlab-ci
status: verified
checked: 2026-09-28
tags: [resource-group, deploy-prod, youdo-business, replica]
---
# DevOps-846: prod-deploy lock rollout and youdo.business replica migrations

## Task

DevOps-846: serialize automatic production deploys (`resource_group` on a parent trigger job,
steps in a child pipeline) and fix the youdo.business replica migration jobs that caused the
2026-09-10 revert.

## Context

- Templates: `sysadmins/devops-tools/gitlab-ci-templates`, first merge 2026-09-09
  (`7b3cf57`), revert 2026-09-10 (`695775a`).
- youdo.business (`youdo/microservices/youdo.business`, project 423) has its own jobs that
  rerun migrations on the logical replica via PG proxy `172.24.0.230` (DevOps-826,
  `5ffd11ae4`). YouTrack comment 2026-09-21 by `a.kalmykov` pointed at them.
- System map: `~/ai/current/knowledge/systems/gitlab-ci/resource-groups.md`.

## Actions

- CI Lint of youdo.business with templates pinned to `7b3cf57` reproduced the break:
  `step 2.1 - pre migrations pg proxy job: undefined need: step 2 - pre migrations`.
- Per the user, replica migrations stay in youdo.business and may run any time after the
  deploy. Changed `.gitlab-ci.yml`: hidden `.deploy-prod-migrations-pg-proxy` got
  `stage: .post` and `resource_group: production-replica`; `step 2.1`/`step 5.1` became
  `step 8 - replica pre migrations` (`needs: [set-variables, deploy production]`) and
  `step 9 - replica post migrations` (`needs: step 8`).
- Listed all projects (449), fetched `.gitlab-ci.yml` of default branches, found 23
  consumers of the three auto templates, CI-linted each with the include ref pinned to
  `7b3cf57`. All valid except `a.solonenko/test_signals` (include ref to a deleted branch).
  Only youdo.business depended on moved steps.
- User pushed templates branch again, MR !82 (`c205041`) merged 2026-09-28 21:31 MSK as
  `029b0ba5c`; then merged the youdo.business change.

## Findings

- Pipeline 139705 (youdo.business `master`, `936cbe916`) succeeded: trigger
  `deploy production` 21:46:16-21:54:41, child 139706 ran `set-variables` → `step 1..6` in
  order; `release`/`notify` started 21:54:42 right after the trigger; `step 8` 21:54:43-58
  and `step 9` 21:54:59-21:55:13 ran after it in `.post`. Rollback stays manual in the parent.
- Resource groups `production` and `production-replica` exist in project 423, both
  `process_mode=unordered`.
- The concurrent case (two master pipelines at once) was verified in `test_signals`; the
  user accepts this as sufficient.
- YouTrack DevOps-846 moved to `Fixed` (MR description `Closes DevOps-846`).

## Changes

- gitlab-ci-templates: MR !82 (lock re-applied).
- youdo.business: `.gitlab-ci.yml` replica migration jobs as above.

## Open items

None. User decisions 2026-09-28: the concurrent case verified in `test_signals` is
accepted; `process_mode=oldest_first` not needed for now; manual prod templates do not need
the lock; the stale `test_signals` include ref does not matter (test repository).

## Portable lesson

`~/ai/general/knowledge/gitlab-ci/resource-group-serialize-production-deploy.md`, section
"Moving shared template jobs into a child pipeline breaks consumers".
