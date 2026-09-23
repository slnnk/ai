---
system: dev-deployment
status: verified
checked: 2026-09-07
tags: [devops-832, tkb, autotests, target-env-suffix, dev-yml, gitlab-ci-templates]
---
# Dev deployment: TKB post-deploy autotest preparation

Date: 2026-09-07  
System: B2B ephemeral dev deployment / DevOps-832  
Status: local preparation complete; push and runtime verification pending

## Context

The operator prepared clean `DevOps-832-dev-autotests` branches in:

- `/home/slnnk/git/youdo-business-tkb-proxy`
- `/home/slnnk/git/youdo-business-tkb-tests`

The implementation follows the runtime-proven Tochka/Billing `TARGET_ENV_SUFFIX` design while accounting for TKB's different Kubernetes component names.

## Changes

Service repository:

- `.gitlab-ci.yml` temporarily pins `sysadmins/devops-tools/gitlab-ci-templates` to `DevOps-832-dev-autotests`.
- Includes `v3/.autotests-dev.yml` and selects `AUTOTESTS_IMAGE_TAG=devops-832-dev-autotests`.
- `devops/dev.yml` enables a ClusterIP Service for `worker-mock`.
- Adds internal-only ingress base host `youdo-business-tkb-proxy-worker-mock.dev.youdo.corp` and TCP liveness/readiness probes.
- Existing 256Mi request/limit values remain unchanged because there is no TKB OOM evidence.

Test repository:

- `devops/entrypoint.sh` reports `TARGET_ENV_SUFFIX`.
- `BaseRequestSpecification` adds Kubernetes mode while retaining Nomad fallback.
- Kubernetes endpoint mappings are:
  - mock API test target -> `http://youdo-business-tkb-proxy-mock-webapp<suffix>.dev.youdo.corp`
  - mock worker test target -> `http://youdo-business-tkb-proxy-worker-mock<suffix>.dev.youdo.corp`
  - automation UI -> `https://b2bautomation<suffix>.dev.youdo.sg`

The existing test-selection, `ignoreFailures`, credential fallback, and retry behavior were intentionally not changed because those are QA-owned follow-up items outside DevOps-832.

## Actions

Verification:

- `git diff --check`: passed in both repositories.
- `bash -n devops/entrypoint.sh`: passed.
- YAML parsing for service `.gitlab-ci.yml` and `devops/dev.yml`: passed.
- `helm lint` against `/home/slnnk/git/helm-charts/microservice`: passed.
- `helm template` for `dev-devops-832`: rendered both internal ingress hosts, worker Service, and TCP probes correctly.
- `gradle compileJava` in local image `gradle:8.7.0-jdk17`: `BUILD SUCCESSFUL`.

## Open items

1. Review and commit both local diffs, then push both feature branches.
2. Wait for the TKB test image tagged `devops-832-dev-autotests`.
3. Start TKB `1 deploy dev`; confirm automatic smoke targets the generated namespace and Jenkins build.
4. Verify preflight/connectivity to mock webapp, mock worker, and automation-web; inspect reports, pod restarts/OOM, peak memory, and dependency resources.
5. Run manual regression and a repeat deployment, then verify cleanup/stale-pipeline protection.
6. Record GitLab pipeline/job and Jenkins build identifiers before marking TKB runtime-proven.

Do not store access tokens, kubeconfig contents, or test credentials in this note.

(Runtime result: `2026-09-07-dev-deployment-tkb-pipeline-138093.md`.)

## Portable lesson

none
