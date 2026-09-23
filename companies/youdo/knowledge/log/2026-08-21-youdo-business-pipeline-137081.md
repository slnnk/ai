---
system: youdo-business
status: verified
checked: 2026-08-21
tags: [gitlab-ci, deploy-prod, manual-job, rollback, blocked-pipeline, gitlab-ci-templates]
---
# youdo.business pipeline 137081 blocked/manual

## Task

Explain why production pipeline `137081` of `youdo.business` shows as Blocked/manual after a successful deploy.

## Context

Date: 2026-08-21
Project: `youdo/microservices/youdo.business`
Pipeline: https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/pipelines/137081
Scope: read-only GitLab API and CI configuration review.

## Findings

### Verified facts

- Pipeline `137081` is still `manual` (GitLab UI may present this as Blocked), ref `master`, commit `9b67a7df1555460c2de4f9453dd2bcdb04185ed1`.
- The production sequence completed successfully: `step 1` through `step 6`, including both migration jobs, are `success`.
- The pipeline contains 89 manual jobs. The test and autotest manual jobs are `allow_failure: true`.
- The blocking job is `step 7 - rollback` (`job 3078629`): status `manual`, stage `deploy-prod`, `allow_failure: false`, no runner assigned and no execution timestamps.
- The release jobs `release`, `notify`, and `deploy-monitoring` remain `created`.

### Configuration chain

At the application commit, `.gitlab-ci.yml` includes `v3/.deploy-prod-full-auto.yml` from `sysadmins/devops-tools/gitlab-ci-templates` and sets `DEPLOY_PROD_MODE: auto`.

The shared template defines `step 7 - rollback` by extending `.deploy-prod-rollback`. That template uses `.rules-prod-manual`, whose matching rule for an automatic master deployment is `when: manual`. The rollback template also explicitly sets `allow_failure: false`.

### Conclusion

This is an intentional blocking rollback gate, not a runner, network, or failed deployment problem. The pipeline is waiting for an operator decision after the successful production deployment. Playing job `3078629` executes Nomad rollback and must not be done merely to clear the status.

## Open items

Safe follow-up:

- If rollback is not required, leave this job unplayed or cancel the obsolete pipeline according to the team's release procedure.
- If the pipeline must finish automatically in future, change the rollback job/template policy deliberately (for example, make the manual rollback non-blocking), review the safety impact, and run a new pipeline. Do not alter the current job by blindly pressing Play.

## Actions

Sources / checks:

- GitLab API: pipeline `137081`, pipeline jobs, job `3078629`, commit `9b67a7df1555460c2de4f9453dd2bcdb04185ed1`.
- Project `.gitlab-ci.yml` at the pipeline commit.
- Shared files `v3/.deploy-prod-full-auto.yml`, `v3/.deploy-prod.yml`, and `v3/.ci-rules.yml` in `sysadmins/devops-tools/gitlab-ci-templates`.

## Portable lesson

[`~/ai/general/knowledge/gitlab-ci/pipeline-blocked-by-manual-job-allow-failure-false.md`](../../../../general/knowledge/gitlab-ci/pipeline-blocked-by-manual-job-allow-failure-false.md)
