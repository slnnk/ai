---
system: dev-deployment
status: verified
checked: 2026-08-30
tags: [jenkins, gitlab-ci, service-name, ci-project-name, gitlab-project-id, youdo-business, build-140]
---
# Dev deployment: GitLab job 3100457 / Jenkins build 140

Date: 2026-08-30 (Europe/Moscow)  
System: B2B ephemeral dev deployment  
GitLab project: `youdo/microservices/youdo.business` (project ID 423)  
GitLab job: `3100457`, `1 deploy dev`, pipeline `137651`  
Jenkins: job `test`, build `140`, queue item `18336`

## Findings

### Result

The GitLab runner and Jenkins bridge worked normally. GitLab created the Jenkins queue item and waited for build 140. Jenkins returned `FAILURE` during `Print selected services`, before namespace creation:

```text
ERROR: Unknown primary service 'youdo.business'.
```

The missing `deploy-dev.env` artifact in the GitLab trace is a downstream consequence of Jenkins failing before the namespace/artifact stage, not the root cause.

### Root cause

The shared GitLab template `gitlab-ci-templates/v3/.deploy-dev.yml` sends:

```text
SERVICE=$CI_PROJECT_NAME
VERSIONS=$CI_PROJECT_NAME|$CI_PROJECT_ID|...
```

For project 423, `CI_PROJECT_NAME` is the GitLab path `youdo.business`, while the canonical service name in `jenkins-pipelines/config/deploy-dev-b2b.groovy` is `youdo-business`. Jenkins build parameters confirmed the mismatched values:

```text
SERVICE=youdo.business
VERSIONS=youdo.business|423|mr|3567|
```

The newly published all-services Jenkins pipeline at commit `10ef2517` correctly rejected the unknown name before creating Kubernetes resources. The defect was dormant while only `docvalidation` and `fns`, whose GitLab paths match their Jenkins names, were used as primary services.

### Affected catalog entries

GitLab metadata for the 13 catalog projects was compared with Jenkins service names. Four paths require canonical mapping:

| GitLab `CI_PROJECT_NAME` | Jenkins service name |
| --- | --- |
| `youdo.business` | `youdo-business` |
| `youdo.business.landings` | `youdo-business-landings` |
| `youdo.kitcut` | `youdo-kitcut` |
| `youdo.notifications` | `youdo-notifications` |

The other catalog project paths match their Jenkins service names.

## Changes

Fix prepared locally. The selected fix uses GitLab project ID as the authoritative cross-system identity:

- `gitlab-ci-templates/v3/.deploy-dev.yml` passes hidden `GITLAB_PROJECT_ID=$CI_PROJECT_ID` in addition to the existing parameters;
- Jenkins resolves that ID through `config.services[].project_id` to the canonical service name and applies it to both primary selection and the matching `VERSIONS` record;
- manual Jenkins builds continue to use the human-readable `SERVICE` dropdown;
- old GitLab triggers without the new parameter remain supported for safe publication order;
- invalid/unknown IDs, IDs without complete GitLab audit context, and a missing matching `VERSIONS` record fail before namespace creation.

Local TDD checks cover the four dotted project mappings, unknown/malformed IDs, manual fallback, and the existing full-catalog fresh/repeat behavior. Groovy parsing/tests, YAML parsing, extracted shell syntax, and `git diff --check` pass. A read-only code review found no Critical or Important issues.

## Open items

The changes are not committed, pushed, or runtime-tested yet. Publish Jenkins first and run/reload the job once so `GITLAB_PROJECT_ID` is registered in job parameters; then publish the shared GitLab template and retry the failed deployment.

(Follow-up: runtime-proven in Jenkins build 142, see `2026-08-30-dev-deployment-jenkins-test-142-migration-job-name-length.md`.)

## Portable lesson

none
