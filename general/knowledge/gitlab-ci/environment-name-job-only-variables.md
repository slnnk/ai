---
system: gitlab-ci
status: verified
checked: 2026-08-25
tags: [gitlab-ci, environment, CI_PIPELINE_ID, CI_PIPELINE_IID, CI_COMMIT_REF_SLUG, resource_group, dynamic-environments]
---
# `environment:name` with `$CI_PIPELINE_ID` expands to an empty suffix

## Symptom

A dynamic environment is declared as
`environment: { name: "dev/$CI_PROJECT_PATH_SLUG-$CI_PIPELINE_ID" }`. In the Environments
page the environment is actually named `dev/<project-slug>-` (trailing dash, no number).
Every pipeline of the project therefore reuses the same environment, `auto_stop_in`/`on_stop`
actions of one pipeline act on another pipeline's deployment, and `resource_group` built
from the same expression serializes everything into one queue.

## Cause

`environment:name` (like `resource_group`, `environment:url`, and a few other keywords) is
expanded by GitLab itself **before** the job runs, using only variables that exist at
pipeline-creation/"persisted" level. `CI_PIPELINE_ID` is a job-level persisted variable
that is not available for that expansion, so it evaluates to an empty string. The job script
still sees the correct `CI_PIPELINE_ID`, which hides the problem.

## Fix

Use variables that are available at pipeline creation:

```yaml
1 deploy dev:
  environment:
    name: dev/$CI_COMMIT_REF_SLUG          # stable per branch/MR; or $CI_PIPELINE_IID per pipeline
    on_stop: "3 delete dev"
    auto_stop_in: 7 days
  resource_group: dev/$CI_PROJECT_PATH_SLUG-$CI_COMMIT_REF_SLUG
```

Pick the identity deliberately:

- `$CI_COMMIT_REF_SLUG` when repeated pipelines of the same branch should update **one**
  environment (typical for review/dev stands with stable names);
- `$CI_PIPELINE_IID` when every pipeline must own its own environment.

Verify via the API after the first run:
`GET /projects/:id/environments?search=dev/` should show the fully expanded name and the
correct `auto_stop_at`. Stop and delete the malformed environment record once its resources
are cleaned up.

## Limits

- The list of variables usable in `environment:name` is documented under "Where variables
  can be used" in GitLab docs; check it whenever a keyword is expanded by GitLab rather than
  by the shell.
- Changing the name creates a new environment record; old ones remain until stopped/deleted.
- Observed on GitLab 17.x; behaviour is long-standing.
