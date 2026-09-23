---
system: dev-deployment
status: verified
checked: 2026-09-04
tags: [devops-832, billing, autotests, target-env-suffix, oom, jenkins-agent, autotest, pipeline-137991, pipeline-137992]
---
# DevOps-832: Billing post-deploy autotests prepared

Date: 2026-09-04  
Status: pushed and runtime-proven; functional/report and memory follow-ups remain

## Context

Repositories and branches:

- `/home/slnnk/git/youdo-business-billing-service`, branch `DevOps-832-dev-autotests`
- `/home/slnnk/git/youdo-business-billing-service-tests`, branch `DevOps-832-dev-autotests`

Both worktrees were clean before the changes. The service change was pushed as `1b6ed25`; the test-project change was pushed as `8e36a0f`.

## Changes

### Service changes

Changed `.gitlab-ci.yml` to:

- use shared template ref `DevOps-832-dev-autotests` during coordinated development;
- include `v3/.autotests-dev.yml` alongside the existing deploy/autotest templates;
- select test image tag `devops-832-dev-autotests` from `youdo/test/youdo-business-billing-service-tests`.

No `devops/dev.yml` resource or exposure change is needed for Billing. Its existing `webapp` ingress is sufficient. With deployment ID `devops-832`, the shared Helm chart renders `youdo-business-billing-service-webapp-devops-832.dev.youdo.corp`.

### Test-project changes

- `devops/entrypoint.sh` now reports `TARGET_ENV_SUFFIX` in the job log.
- `ApiEndpoints.BASE_URL` uses the Kubernetes form `http://youdo-business-billing-service-webapp<TARGET_ENV_SUFFIX>.dev.youdo.corp` when the suffix exists.
- Without `TARGET_ENV_SUFFIX`, the previous Nomad `TARGET_HOST` plus `.yandex-test.youdo.local` form remains unchanged.
- Existing QA semantics remain untouched: `TEST_GROUP`, hard-coded Gradle tag selection, `ignoreFailures`, reports, and test content.

## Actions

Verification:

- Both repository diffs pass `git diff --check`.
- Service `.gitlab-ci.yml` parses as YAML.
- `helm lint` passes with Billing `devops/dev.yml` and the current shared `microservice` chart.
- `helm template` confirms the exact task-specific webapp hostname expected by the test code.
- `gradle compileJava` in the repository Dockerfile base image `gradle:8.7.0-jdk17` completed with exit code 0 and `BUILD SUCCESSFUL`.

Next steps (planned before the runtime run):

1. Review, commit, and push both feature branches.
2. Let the billing-tests pipeline publish `autotests:devops-832-dev-autotests`.
3. Run the Billing service MR pipeline and manually start `1 deploy dev`.
4. Confirm Jenkins selects Billing as primary, consumes dependency `master` revisions, and deploys the expected task ingress.
5. Confirm automatic `smoke tests`, manual `regression tests`, namespace ownership validation, JUnit/Allure publication, and no relevant OOM/restarts.
6. Use this run to validate merged doc-generator/automation-web memory values and the Jenkins old-ReplicaSet race fix.

## Findings

### Runtime result: pipeline 137991

- GitLab pipeline: `137991`, status `success`, MR 97, service commit `1b6ed25`.
- Deploy job: `3114239`, status `success`, duration 237 seconds.
- Jenkins build: `test/155`, status `SUCCESS`, loaded `jenkins-pipelines/master` revision `20b9d78`.
- Namespace: `dev-devops-832`, created fresh with Billing primary and all 12 dependencies.
- Smoke job: `3114321`, automatically started, status `success`, duration 155 seconds.
- Regression job: `3114322`, manual and not started.
- Test image: Billing tests feature tag `devops-832-dev-autotests`, source feature commit `8e36a0f`.
- Target contract: `TARGET_ENV_SUFFIX=-devops-832`, `TARGET_HOST=none`, exact webapp ingress matched the implemented Kubernetes URL.
- Reports: Allure and JUnit uploads succeeded; report URL is recorded in the GitLab job/MR.

#### Test result caveat

GitLab imported 545 Billing smoke cases: 542 passed and 3 failed. Gradle itself logged 553 tests and 3 failures, then `BUILD SUCCESSFUL` because the project sets `ignoreFailures=true`. The failures are:

- `RefillYouDoBalanceTest`: parameter `tkbBankDefault`, null item caused a test-side NPE;
- `GetYouDoBalanceHistoryTest`: two parameterizations expected a non-zero value but received zero.

No DNS, ingress, connection, image, Kubernetes, or report-upload failure was observed. Treat the three failures as QA/test-data/application follow-up and retain the existing non-gating classification. Also investigate why Gradle reports 553 tests while GitLab JUnit imports 545.

#### Runtime resources

- Billing webapp: 256Mi request/limit, approximately 248Mi sampled after smoke, Ready, zero restarts. This is close enough to the limit to warrant a memory adjustment or measured regression run.
- Doc-generator API: 512Mi request / 1Gi limit, Ready, zero restarts.
- Automation-web: 512Mi request / 1Gi limit, Ready, zero restarts.
- No current pod in the namespace had a nonzero restart count or retained termination reason.
- All PVCs were Bound after startup. Transient bootstrap events included RabbitMQ `FailedMount` and docvalidation `FailedAttachVolume`; both recovered without operator action.

Jenkins `20b9d78` is now runtime-executed successfully, but build 155 created a fresh namespace. It does not yet reproduce the old-ReplicaSet deletion race; use a repeat deploy for that acceptance case.

### Manual regression job 3114322

The manual `regression tests` job ran from 19:27:20 to 19:29:46 MSK on `gitlab-runner-docker-3` and published reports successfully. Its green status is misleading:

- Gradle logged 553 tests completed and 540 failed, then `BUILD SUCCESSFUL` because `ignoreFailures=true`.
- GitLab JUnit imported 545 tests: 13 passed and 532 failed.
- All 532 imported failures expected HTTP 200 or 400 but received 502.
- Billing webapp container reached the 256Mi limit and was `OOMKilled` at 19:29:14 MSK, exit code 137. Kubernetes restarted it once.
- The OOM is temporally aligned with the mass 502 failures and is the infrastructure cause of the invalid regression run.
- After restart the pod recovered to Ready and sampled around 98Mi. No other namespace pod had a restart or retained termination reason.

Required follow-up: change Billing webapp resources from 256Mi/256Mi to an initial 512Mi request / 1Gi limit, redeploy, rerun regression, and verify peak usage plus zero restarts/OOM. The three earlier smoke functional failures remain a separate QA/application-data issue.

### Failed repeat deploy: pipeline 137992 / job 3114330

The repeat `1 deploy dev` job started Jenkins build 156 and failed after 34 seconds. This is unrelated to the Billing application and unrelated to the old-ReplicaSet race:

- Jenkins build 156 loaded `jenkins-pipelines/master` commit `20b9d78`.
- It was scheduled on node `Jenkins` with workspace under `/data/jenkins/workspace/test`; successful build 155 had run on node `AutoTest` under `/home/jenkins/work/workspace/test`.
- Namespace infrastructure checks passed, TTL was refreshed, and namespace Helm release was upgraded to revision 2.
- Repeat selection correctly preserved all 12 existing dependencies and selected only Billing as primary.
- Billing service commit `6804148` (`increase memory limit`) was checked out.
- Before the Billing Helm command, `writeServiceRoutingOverlay` executed `python3 -c ... yaml.safe_load(...)` against `devops/dev.yml`.
- Node `Jenkins` returned `python3: not found`; the service branch exited 127 and Jenkins finished `FAILURE`.

Live-state verification after failure:

- Billing Deployment generation remains 1 and Ready 1/1.
- Image remains the earlier `devops-832-dev-autotests-137991` image.
- Resources remain 256Mi request / 256Mi limit.
- Billing Helm history contains only revision 1; no partial application upgrade occurred.
- The pod remains Running with the one prior OOM restart from regression.

Root cause: the unlabelled Jenkins pipeline can execute on agents with different toolsets, while Python 3 plus PyYAML is an undocumented runtime dependency. Fix by removing that dependency in favor of a guaranteed portable parser/tool, or standardize the agent image/toolset and restrict the job to compatible nodes. A read-only plugin audit found that `pipeline-utility-steps`/`readYaml` is not installed, so switching to `readYaml` requires an explicit plugin installation first.

#### Local agent-pinning correction

At the operator's request, `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile` was changed from an unlabelled `node {}` block to `node('AutoTest') {}`. The README documents the label/toolchain prerequisite, and `tests/deploy_dev_b2b_test.groovy` asserts the label contract. The Groovy test suite and `git diff --check` pass. The change is present in `jenkins-pipelines/master` commit `ae1a125` (`fix node`) and the local worktree matches `origin/master`.

Jenkins API initially found the selected agent temporarily offline. Cause: `/tmp` free space was 1022.34MiB, below the configured 1GiB disk threshold.

#### AutoTest agent cleanup and recovery

On 2026-09-04 the agent was identified as inbound node `AutoTest`, host `jenkins-agent-test-01` (`10.16.26.23`). The root filesystem was 89% used: 8.3GiB of 9.8GiB, with 1.1GiB available. `/tmp` itself held only about 80MiB; the pressure came mainly from Docker data and the systemd journal.

Safe cleanup performed:

- removed only the unused previous Jenkins inbound-agent image tag ending in `.5` (about 1.04GiB reclaimable); active tag ending in `.6` and container `jenkins-agent-jenkins_agent-1` were left untouched;
- ran `journalctl --vacuum-size=200M`, which freed 488MiB and left the journal at about 192MiB.

After cleanup the root filesystem was 78% used: 7.3GiB used and 2.1GiB available. Docker reported one active image/container and zero reclaimable image space. Jenkins still held the old disk-monitor result, so the node's temporary offline flag was toggled once after the disk check. Final Jenkins API state: `offline=false`, `temporarilyOffline=false`, five executors. The deleted Docker image can be pulled again if needed; vacuumed journal history is not recoverable.

#### Successful recovery in pipeline 137992

Retried GitLab deploy job `3114414` triggered Jenkins build `158`. Jenkins checked out pipeline revision `ae1a125`, ran in `/home/jenkins/work/workspace/test` on node `AutoTest`, successfully executed the Python/PyYAML routing parser, preserved all 12 dependencies, and upgraded only `youdo-business-billing-service` to Helm revision 2. The namespace chart reached revision 3.

Post-deploy runtime state:

- Billing image: `webapp:devops-832-dev-autotests-137992`;
- resources: 512Mi request / 1Gi limit;
- deployment: one desired/updated/ready/available replica;
- current pod: Ready, zero restarts, no last termination state;
- rollout events are Normal only; the prior 256Mi ReplicaSet was scaled down.

Autotest results:

- smoke job `3114412`: 545 total, 543 passed, 2 failed;
- regression job `3114413`: 545 total, 543 passed, 2 failed;
- both failures in both suites are parameterizations of `GetYouDoBalanceHistoryTest.getYouDoBalanceHistoryWithIncorrectPeriod`, asserting that `0.0` should be non-zero;
- no repeated HTTP 502 pattern and no new OOM evidence were observed.

Pipeline `137992` finished `success`. The two autotest jobs also display `success` despite their two assertions because the suite ignores test failures and the GitLab jobs are allowed to fail; inspect JUnit/Allure counts rather than relying only on job color.

## Open items

- Two remaining `GetYouDoBalanceHistoryTest` assertions and the Gradle/GitLab count discrepancy are QA-owned.
- Merged doc-generator/automation-web memory values still need verification in a fresh namespace (build 155 consumed them; load sufficiency unproven).

## Portable lesson

none
