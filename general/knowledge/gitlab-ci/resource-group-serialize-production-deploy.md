---
system: gitlab-ci
status: verified
checked: 2026-09-09
tags: [resource_group, deploy, child-pipeline, trigger, strategy-depend, process_mode]
---
# Serialize production deploys across pipelines with `resource_group`

## Symptom

Several merges into the default branch in quick succession create several pipelines that
run their production deploy jobs concurrently, racing each other on the same environment.
Putting the same `resource_group` on each of several deploy steps (`migrations`, `deploy`,
`update`) does not help: a job from another pipeline slips in between the steps.

## Cause

A `resource_group` is a lock that is held for the duration of **one job** and released as
soon as that job finishes. Jobs of the same stage are independent and may claim the lock in
undefined order. So per-step locks serialize individual steps, not the whole deploy
sequence. The default `process_mode` is `unordered`, so waiting jobs are not started in
pipeline order either.

## Fix

Single-step deploy: one job, one lock.

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

Multi-step deploy that needs separate jobs, stages, logs and retries: put the steps into a
child pipeline and hold the lock on the parent trigger job. `strategy: depend` makes the
trigger job wait for the child, so the resource stays locked until every step is done.

```yaml
# parent .gitlab-ci.yml
deploy_prod:
  stage: deploy-prod
  resource_group: production
  trigger:
    include:
      - local: .gitlab/deploy-production.yml
    strategy: depend
```

```yaml
# .gitlab/deploy-production.yml
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

Rules that matter:

- Do **not** set the same `resource_group` inside the child pipeline: parent and child would
  wait for each other (deadlock).
- A manual rollback job in the parent may use the same `resource_group`; it then cannot run
  while an automatic deploy is in progress.
- For strict oldest-first ordering set the process mode per project through the API
  (`process_mode=oldest_first`); it cannot be set in YAML:

  ```bash
  curl --request PUT --header "PRIVATE-TOKEN: $TOKEN" \
    --data "process_mode=oldest_first" \
    "$CI_API_V4_URL/projects/<id>/resource_groups/production"
  ```
- Other pipelines are still created and their build/test jobs run in parallel; only the
  locked job waits, showing `Waiting for resource`.
- When the child config is loaded from a shared templates repository, make the ref a
  variable so a feature branch of the templates can be tested end to end.

Verify with a throwaway project where every step is `echo "$CI_JOB_NAME"; sleep 10`, push two
commits quickly and watch the second trigger job wait for the first child pipeline.

## Limits

- `trigger:strategy: depend` exists in GitLab 17.x; `strategy: mirror` needs GitLab 18.2+.
- The lock is per project. Deploys of the same environment from different projects need a
  different mechanism (for example an environment-level lock in the deploy tool).
- Checked on self-managed GitLab 17.9.8 with CI Lint and a live test pipeline.
