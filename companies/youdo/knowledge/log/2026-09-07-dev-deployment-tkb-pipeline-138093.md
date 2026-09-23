---
system: dev-deployment
status: verified
checked: 2026-09-07
tags: [devops-832, tkb, autotests, pipeline-138093, build-159, memory, dev-devops-832]
---
# Dev deployment: TKB pipeline 138093 runtime check

Date: 2026-09-07  
System: B2B ephemeral dev deployment / DevOps-832  
Pipeline: https://gitlab.youdo.sg/youdo/microservices/youdo-business-tkb-proxy/-/pipelines/138093  
Status: infrastructure path proven; two masked functional failures and memory risk remain

## Context

Identifiers:

- Service branch/commit: `DevOps-832-dev-autotests`, `6b2428694c9044d78b47db839395ba220bcab8bd`
- Test branch/commit and source pipeline: `DevOps-832-dev-autotests`, `6615a9122437179c787294cdb7f98bc25cff9dbc`, pipeline `138092` (`success`)
- Deploy job: `3120707`
- Jenkins: `test/159`, result `SUCCESS`, `jenkins-pipelines` revision `ae1a125`
- Namespace: `dev-devops-832`, owner label `jenkinsJobId=159`
- Automatic smoke: `3120789`
- Manual regression: `3120790`

## Findings

### Deployment evidence

Jenkins ran on `AutoTest`, selected TKB as primary and all 12 other catalog services as dependencies, installed the fresh TKB release, completed migrations, and rolled out both `mock-api` and `worker-mock`. The generated ingress report contained:

- `http://youdo-business-tkb-proxy-mock-webapp-devops-832.dev.youdo.corp`
- `http://youdo-business-tkb-proxy-worker-mock-devops-832.dev.youdo.corp`

The deploy job automatically played exactly one smoke job. Namespace metadata points back to pipeline `138093`, job `3120707`, and Jenkins `159`.

At the read-only post-run check, every pod in the namespace was Ready with zero restarts and no retained last termination state. Kubernetes reported no Warning events. Both TKB Service/Ingress resources existed. HTTP health checks returned 200 for TKB mock-webapp, TKB worker-mock, and task-specific automation-web.

### Test evidence

Both jobs validated `DEV_NAMESPACE=dev-devops-832`, derived `TARGET_ENV_SUFFIX=-devops-832`, selected the feature test image, completed report upload, and remained green because the test build uses `ignoreFailures=true` and jobs are `allow_failure`.

Per job:

- Gradle: 183 tests, 2 failed.
- GitLab JUnit: 174 total, 172 passed, 2 failed.
- The 183-versus-174 reporting discrepancy remains part of the existing QA reporting debt.

The same tests failed in smoke and regression:

- incoming-payment identification to a beneficiary when the incoming payment is expected not to have failed;
- returned-payment identification when the incoming payment is expected not to have failed.

Both exhausted ten polling iterations in `CycleSpecification.cycleForIdentifyIncomingPayments` and threw `Входящий платеж не в статусе New`. All worker-trigger and incoming-payment-list Allure steps passed. TKB application logs show Billing rejecting balance refill for generated beneficiary accounts with `ACCOUNT_NOT_FOUND`. This is consistent with test-data/cross-service state mismatch; it is not a DNS, ingress, worker Service, Jenkins, or Kubernetes failure.

### Resource risk

The TKB pods remained Ready with zero restarts, but the metrics snapshot showed:

- `mock-api`: 256388Ki with a 256Mi request/limit, approximately 97.8% of the limit;
- `worker-mock`: 180880Ki with a 256Mi request/limit.

There is no OOM evidence yet, but mock-api has unsafe headroom and worker-mock would also benefit from headroom during parallel suites. Commit `aa4d083` on `DevOps-832-dev-autotests` sets 512Mi request / 1Gi limit for both components. YAML parsing, `git diff --check`, Helm lint, and rendered resource checks passed. MR pipeline `138096` built and unit-tested it successfully; manual deploy job `3120801` is waiting and the new limits are not yet runtime-proven.

## Open items

1. Commit/push the prepared memory correction and rerun both suites while collecting peak usage and restart/OOM evidence.
2. Decide with QA/application owners how ephemeral Billing accounts should be prepared for these two scenarios, or whether those expectations/data need adjustment.
3. Verify repeat-deploy isolation and old-ReplicaSet handling for TKB.
4. Verify delete/cleanup and stale-pipeline protection before marking the full TKB lifecycle complete.

No secrets, test payloads, kubeconfig contents, or generated beneficiary identifiers are stored here.

## Portable lesson

none
