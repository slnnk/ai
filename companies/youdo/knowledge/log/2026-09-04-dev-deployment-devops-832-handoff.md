---
system: dev-deployment
status: verified
checked: 2026-09-04
tags: [devops-832, handoff, autotests, tochka, billing, tkb, jenkins, autotest-agent]
---
# DevOps-832 handoff — 2026-09-04

## Task

Scope and working policy: the active goal is to prepare post-deploy autotests for all current selected B2B services on feature branches, keep the coordinated application/test/template changes unmerged during preparation, then merge the complete set in dependency order and run final end-to-end verification. Active service scope: Tochka, Billing, TKB, and the main `youdo-business` suite. The operator explicitly removed Sber and Sber tests from scope on 2026-09-04 because the service is no longer current.

## Actions

### Jenkins deployment reliability

- `jenkins-pipelines/master` commit `20b9d78` fixes the post-rollout race by retrying the pod-phase check and excluding deletion-marked old ReplicaSet pods and Job pods while retaining failures for active unhealthy pods.
- `jenkins-pipelines/master` commit `ae1a125` pins the B2B dev deployment to Jenkins label `AutoTest`; README and Groovy contract coverage were updated.
- Billing Jenkins build `158` checked out `ae1a125`, ran on `AutoTest`, executed Python/PyYAML successfully, saw an old Billing pod in `Terminating`, ignored it correctly, and finished `SUCCESS`. This runtime-proves both the label pin and the race correction.

### AutoTest agent recovery

- Agent: Jenkins node `AutoTest`, inbound host `jenkins-agent-test-01`, address `10.16.26.23`.
- Jenkins had disabled it because the disk monitor reported 1022.34MiB free on `/tmp`, below the 1GiB threshold.
- Removed only the unused previous Jenkins inbound-agent Docker image; active image/container were untouched.
- Vacuumed systemd journal to 200MiB, freeing 488MiB.
- Root filesystem improved from 1.1GiB free / 89% used to 2.1GiB free / 78% used.
- Jenkins retained the stale monitor state, so its temporary offline flag was toggled once. Final API state: online, not temporarily offline, five executors.

### Tochka post-deploy autotests

- Service branch `DevOps-832-dev-autotests`, commit `8090532`: mock-worker exposure, dev-autotest opt-in, and four workload resource increases.
- Test branch `DevOps-832-dev-autotests`, commit `02dcaea`: Kubernetes `TARGET_ENV_SUFFIX` mode with legacy `TARGET_HOST` compatibility.
- Shared templates branch `DevOps-832-dev-autotests`, commit `34b63d6`: reusable dev-autotest jobs, automatic smoke after deploy, manual regression.
- Pipeline `137961`, successful deploy retry `3112466`, Jenkins build `153`, smoke `3112464`, and manual regression `3112465` prove the end-to-end chain. Smoke imported 603 cases: 587 passed, 16 skipped, no failures/errors.

### Billing post-deploy autotests and memory

- Service branch `DevOps-832-dev-autotests`, current commit `6804148`, raises Billing webapp to 512Mi request / 1Gi limit.
- Test branch `DevOps-832-dev-autotests`, commit `8e36a0f`, adds Kubernetes task-suffix addressing.
- Pipeline `137991` proved initial full-catalog deployment and automatic smoke. Manual regression `3114322` exposed the old 256Mi OOM: exit 137 followed by mass Traefik 502 responses.
- First repeat job `3114330` / Jenkins build `156` failed on the unlabelled generic Jenkins node because it lacked Python 3.
- Pipeline `137992` retry job `3114414` / Jenkins build `158` succeeded on `AutoTest`, upgraded only Billing to Helm revision 2, and preserved all dependencies.
- Live Billing webapp is Ready on image `devops-832-dev-autotests-137992`, uses 512Mi request / 1Gi limit, and has zero restarts or termination state. The previous OOM/502 failure pattern is gone.
- Smoke `3114412` and regression `3114413` each imported 545 cases: 543 passed and 2 failed. Both failures are parameterizations of `GetYouDoBalanceHistoryTest.getYouDoBalanceHistoryWithIncorrectPeriod` (`expected not 0.0, was 0.0`). Jobs are green because assertions are ignored and jobs are allowed to fail.

### Dependency memory changes

- `youdo-business-doc-generator` MR 34 merged through `bdee550d`, setting API to 512Mi request / 1Gi limit.
- `youdo.business` MR 3738 merged through `b7d1df43`, setting automation-web to the committed dev memory values recorded in the service map.
- Billing pipeline `137992` was a repeat deploy and deliberately preserved dependencies, so these two merged dependency changes still require verification in a fresh namespace during the next service onboarding.

## Findings

Repository state at handoff, checked on 2026-09-04: the local worktrees for Tochka service/tests, Billing service/tests, shared GitLab templates, Jenkins pipelines, `youdo.business`, TKB service, and TKB tests contain no uncommitted changes. Each is synchronized with its currently checked-out upstream branch. Jenkins pipelines are on clean `master` at `ae1a125`; feature repositories remain on their named DevOps-832 branches unless already merged separately by the operator.

## Open items

Next session:

1. Prepare TKB service and `youdo-business-tkb-tests` analogously to Tochka:
   - add Kubernetes `TARGET_ENV_SUFFIX` mode;
   - reconcile legacy test component names with Kubernetes names;
   - expose only the required mock-worker through an internal Service/Ingress;
   - enable automatic smoke and manual regression;
   - verify deploy, repeat deploy, reports, resources, and no public worker route.
2. Prepare `youdo.business` and `youdo-business-tests` after mapping every suite endpoint; one generic hostname is insufficient for this suite.
3. On the next fresh namespace, verify the merged doc-generator and automation-web resources, Ready state, restarts/OOM, and useful peak-memory evidence.
4. Keep all remaining preparation on feature branches. When TKB and `youdo-business` are ready, merge the shared template/test/service changes in coordinated dependency order, replace temporary template refs with `master`, and run final deploy → automatic smoke → manual regression verification for every active service.

Non-blocking QA debt:

- Test projects use `ignoreFailures=true`; GitLab job color is not a reliable test gate.
- Smoke/regression tag selection is not yet semantically separated in several suites.
- Billing has two repeatable balance-history assertions for QA follow-up.
- Tochka contains a hard-coded token fallback and an unrelated external retry probe; do not copy the secret value, and leave remediation to the recorded QA backlog unless scope changes.

Later platform hardening:

- Jenkins lock keyed by final namespace.
- Post-rollout HTTP health smoke.
- Helm schema/template regression coverage.
- Real `auto_stop_in` verification and TTL-controller ownership decision.
- Vault deployer ownership documentation and local kubeconfig permission review.
- Monitoring for stale namespaces, migrations, Vault failures, and expired environments with live resources.
- Rename Jenkins pilot job `test` and document routine cleanup/recovery commands.

Detailed evidence remains in `~/ai/current/knowledge/systems/dev-deployment/overview.md`, `~/ai/current/knowledge/systems/dev-deployment/post-deploy-autotests.md`, and `~/ai/current/knowledge/log/2026-09-04-dev-deployment-devops-832-billing-autotests-prepared.md`.

## Portable lesson

none
