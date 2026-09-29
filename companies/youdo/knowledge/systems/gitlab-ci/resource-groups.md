---
system: gitlab-ci
status: verified
checked: 2026-09-28
tags: [resource-group, deploy-prod, child-pipeline, gitlab-ci-templates, serialization]
---
# GitLab CI: serialized production deploy (resource groups)

Last checked: 2026-09-28. Translated from Russian.

## Current status (2026-09-28, DevOps-846, Fixed)

- Rolled out 2026-09-28: MR !82 merged (`029b0ba5c`), youdo.business replica jobs moved to
  `.post`; first prod pipeline 139705 succeeded end to end. Details:
  `~/ai/current/knowledge/log/2026-09-28-gitlab-ci-devops-846-prod-deploy-lock-rollout.md`.
- Scope decisions (user, 2026-09-28): only the three auto templates are locked; manual prod
  templates do not need it. `process_mode` stays `unordered` for now.

History:


- The branch was merged to `master` on 2026-09-09 (`68e31a0`, squash `7b3cf57`) and
  reverted on 2026-09-10 (`695775a`, merged as `0cb197f`). The reason for the revert is
  not recorded (ask the user). `master` currently has no prod-deploy lock.
- YouTrack comment of 2026-09-21 by `a.kalmykov`: problems with running migrations on the
  replica must be solved first.
- Blocker verified 2026-09-28: `youdo.business/.gitlab-ci.yml` (DevOps-826, `5ffd11ae4`,
  2026-08-19) adds parent jobs `step 2.1 - pre migrations pg proxy` and
  `step 5.1 - post migrations pg proxy` (logical replica via PG proxy `172.24.0.230`,
  `allow_failure: true`) with `needs` on `step 2 - pre migrations` / `step 5 - post migrations`.
  The lock moves those steps into the child pipeline, so the parent config is invalid.
  GitLab CI Lint of the youdo.business config with templates at `7b3cf57`:
  `step 2.1 - pre migrations pg proxy job: undefined need: step 2 - pre migrations`.
  Even with the needs removed, the replica jobs would run outside the lock. This is the
  likely reason for the 2026-09-10 revert (hypothesis: no failed youdo.business `master`
  pipeline exists between the merge at 18:48 and the revert at 00:13).
- Remote branch `DevOps-846-block-stage-prod` no longer exists (deleted on merge); only the
  local branch and the stale `origin/` ref remain.
- Chosen approach (user, 2026-09-28): keep the replica jobs in youdo.business only; they may
  run any time after the prod deploy (on failure the replica just queues changes).
  Implemented locally in youdo.business branch `DevOps-846-fix-replica-migrations`
  (uncommitted): hidden `.deploy-prod-migrations-pg-proxy` gets `stage: .post` and
  `resource_group: production-replica`; jobs `step 8 - replica pre migrations`
  (`needs: [set-variables, deploy production]`) and `step 9 - replica post migrations`
  (`needs: step 8`). Numeric prefix keeps alphabetical order in the stage view.
  CI Lint: valid with templates `7b3cf57`, invalid with current templates `master`
  (`undefined need: deploy production`), so the templates must be merged first.
- Consumer audit 2026-09-28: 23 projects include one of the three auto templates; all pass
  CI Lint against `7b3cf57` except `a.solonenko/test_signals` (its include ref points to the
  deleted branch). Only youdo.business had parent jobs depending on moved steps.
- Templates: local `c205041` equals current `master` plus the lock (lock files identical to
  `7b3cf57`); no code change is needed for the replica fix.
- 2026-09-28: branch pushed again, MR !82 (`c205041`, squash, delete source branch,
  mergeable, no conflicts). youdo.business config lints valid against the MR branch.
- 2026-09-22: `master` gained `v3/.deploy-prod-svc-migrations.yml` (`937d149`, manual
  semver-tag deploy: stop svc, pre-migrations, update, start svc, rollback). It is not
  covered by the lock branch.
- Local branch `DevOps-846-block-stage-prod` has an unpushed merge of `master`
  (`c205041`, 2026-09-23); it is 12 commits ahead of `origin/DevOps-846-block-stage-prod`
  (`185e3f8`). The sections below describe the implementation as of 2026-09-09.

## Task

When several merges into `master` happen in quick succession, GitLab creates several pipelines in parallel. Concurrent deploys into the same production environment must not be allowed.

## Verified mechanism

- Set the same `resource_group` on the production deploy job, for example `production`.
- The lock applies between jobs of different pipelines of the same GitLab project: only one job runs at a time; the others are in the state `Waiting for resource`.
- The pipeline itself is still created and its independent build/test jobs can run in parallel.
- The default order is `unordered`. For strict merge/pipeline order, set `process_mode=oldest_first` through the Resource Groups API.
- If the lock must cover several deploy jobs or the whole deploy pipeline, move them into a child pipeline. On the parent trigger job set `resource_group: production` and a strategy that waits for the child pipeline, so the resource is held until it finishes. In the corporate GitLab 17.9.8 this is `trigger:strategy: depend`; `strategy: mirror` is only available from GitLab 18.2.
- Do not assign the same resource group to jobs inside the child pipeline: this can lead to a mutual deadlock.
- The same `resource_group` on several separate jobs (`migrations`, `deploy`, `update`) of the parent pipeline is not an equivalent scheme. The resource is released after every job, so a job from another pipeline can slip in between them. In addition, jobs of one stage are independent by default and may claim the resource in an undefined order.
- If separate jobs are not needed, the simple safe option is one job that performs all three operations sequentially. If separate jobs, stages, logs and retry are required, use a child pipeline under one blocking trigger job.

## Minimal configuration

```yaml
deploy_prod:
  stage: deploy
  script: ./deploy.sh
  environment:
    name: production
  resource_group: production
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

## Several steps of one production deploy

Parent `.gitlab-ci.yml`:

```yaml
deploy_prod:
  stage: deploy-prod
  resource_group: production
  trigger:
    include:
      - local: .gitlab/deploy-production.yml
    strategy: depend
```

Child `.gitlab/deploy-production.yml`:

```yaml
stages: [migrations, deploy, update]

migrations:
  stage: migrations
  script: ./migrate.sh

deploy:
  stage: deploy
  script: ./deploy.sh

update:
  stage: update
  script: ./update.sh
```

Inside the child pipeline `resource_group: production` is not set again.

## Implementation for v3 auto deploy-prod

As of 2026-09-08, in `/home/slnnk/git/gitlab-ci-templates`, branch
`DevOps-846-block-stage-prod`, serialization of only the three auto entrypoints
was prepared locally:

- `v3/.deploy-prod-full-auto.yml`;
- `v3/.deploy-prod-only-web-auto.yml`;
- `v3/.deploy-prod-web-migrations-auto.yml`.

The external template paths are preserved. Every entrypoint creates a parent trigger job
`deploy production` with `resource_group: production` and
`strategy: depend`; the existing automatic steps were moved to
`v3/child/` and keep their sequence through `needs`. The dotenv variables
`APP_IMAGE_*` are loaded from the successful parent job `set-variables` through
`needs:pipeline:job`. `set-variables-nomad` runs inside the child, already under the
shared lock. Manual templates were not changed.

Manual rollback stays in the parent pipeline and uses the same resource group,
so it does not run concurrently with the auto deploy. For loading the child config
the variable `DEPLOY_PROD_TEMPLATES_REF` (default `master`) was added;
when testing a feature branch it must be overridden with the same ref.

Checks: all YAML files of the repository parse with Psych; the three assembled
child configs passed GitLab 17.9.8 CI Lint without errors or warnings.
The runtime check in the test repository was performed and accepted by the user.
The implementation is committed as `185e3f8` (`add prod-deploy block`), published to
`origin/DevOps-846-block-stage-prod` and as of 2026-09-09 sits directly
on top of the current `origin/master` (`7ddb881`), without conflicts and without
uncommitted changes. `git diff --check` and a repeated syntax check of
all YAML files passed; `git push --dry-run` returned `Everything up-to-date`.
The branch is ready to merge into `master`.

Operational next step after rollout: set
`process_mode=oldest_first` through the API in every consumer project where strict
production deploy pipeline order is needed.

For the runtime check, a full-auto test harness was prepared locally in `/home/slnnk/git/test_signals`.
The root `.gitlab-ci.yml` includes
`v3/.deploy-prod-full-auto.yml` with ref `DevOps-846-block-stage-prod`, and
`DEPLOY_PROD_CHILD_PROJECT=$CI_PROJECT_PATH` and
`DEPLOY_PROD_CHILD_REF=$CI_COMMIT_SHA` point the third child include at the
local `v3/child/.deploy-prod-full-auto.yml`. Six child jobs are linked by linear
`needs`; each runs only `echo "$CI_JOB_NAME"` and
`sleep 10`. The parent `set-variables`, `set-variables-nomad`, manual
rollback and release are also mocked with the same commands. For release,
`release: null` disables the creation of a real GitLab Release, but the job itself is
kept in stage `release` and runs after the deploy trigger completes.

For this substitution the shared templates gained
`DEPLOY_PROD_CHILD_PROJECT` and `DEPLOY_PROD_CHILD_REF`; production defaults
still point at the templates repository and
`DEPLOY_PROD_TEMPLATES_REF`. The mock child and the full merged config of
`test_signals` passed GitLab 17.9.8 CI Lint without errors or warnings.
Pipeline 138165 confirmed the creation of the parent trigger and the sequential start of the
child deploy steps; the absence of release in that run was caused by a temporary
`rules: when: never`. It was replaced with a safe mock release job. Per
the user's confirmation on 2026-09-09 the final version was verified in the test
repository and matches expectations.

## Source

- GitLab Docs: https://docs.gitlab.com/ci/resource_groups/

Main templates repository:
`/home/slnnk/git/gitlab-ci-templates`,
`git@gitlab.youdo.sg:sysadmins/devops-tools/gitlab-ci-templates.git`.
Test CI repository: `/home/slnnk/git/test_signals`,
`git@gitlab.youdo.sg:a.solonenko/test_signals.git`.

## Portable lesson

[`~/ai/general/knowledge/gitlab-ci/resource-group-serialize-production-deploy.md`](../../../../../general/knowledge/gitlab-ci/resource-group-serialize-production-deploy.md)
