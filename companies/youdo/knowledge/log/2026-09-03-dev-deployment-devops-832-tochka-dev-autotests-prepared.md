---
system: dev-deployment
status: verified
checked: 2026-09-03
tags: [devops-832, tochka, autotests, gitlab-ci-templates, autotests-dev, oom, cookies, nomad-comparison, dev-devops-832]
---
# DevOps-832 Tochka dev autotests: prepared changes

Date: 2026-09-03  
State: local changes prepared, not committed or pushed; runtime GitLab/Jenkins validation pending (later sections record the runtime results through 2026-09-04).

## Context

Repositories and branches:

- `/home/slnnk/git/youdo-business-tochka-proxy-tests`, branch `DevOps-832-dev-autotests`;
- `/home/slnnk/git/gitlab-ci-templates`, branch `DevOps-832-dev-autotests`;
- `/home/slnnk/git/youdo-business-tochka-proxy`, branch `DevOps-832-dev-autotests`.

All three worktrees were clean before the task. Only the files listed below were changed.

## Changes

### Tochka autotests

- `BaseRequestSpecification.java` now reads optional `TARGET_ENV_SUFFIX`.
- When the suffix is present it constructs task-specific Kubernetes URLs for mock webapp, mock worker, and B2B automation; otherwise the original `TARGET_HOST` Nomad construction is preserved.
- `entrypoint.sh` logs the selected suffix without changing test selection, failure handling, token handling, retry logic, or report behaviour.

The existing Dockerfile image was built locally as `codex/tochka-dev-autotests:verify`; its Gradle `clean build compileTestJava -x test` and `downloadAllure` steps completed successfully on JDK 17. A host Gradle attempt failed before project configuration because the host has Java 11; this was an environment mismatch, not a source failure.

### Shared GitLab templates

- Added `autotests-dev` after the existing `autotest` stage.
- Reused the existing `AUTOTESTS` rules and image variables; explicit inclusion of `v3/.autotests-dev.yml` is the opt-in, so no duplicate dev variable family is required.
- Added `v3/.autotests-dev.yml` with one `dev smoke tests` job. It consumes the `1 deploy dev` dotenv artifact, validates namespace/build ownership through the pinned kubectl image, derives `TARGET_ENV_SUFFIX`, reuses the existing Docker test/report flow, shares the dev resource group, and remains `allow_failure: true`.
- `1 deploy dev` now finds the exact manual dev-smoke job across all GitLab API pages and auto-plays it after a successful Jenkins deployment when the opt-in variables are enabled.

Ruby/Psych parsed all modified/new YAML files successfully and `git diff --check` passed. Full GitLab CI merged-config lint remains pending until the feature branch exists remotely, because the service include intentionally references that branch.

### Tochka service

- The service CI temporarily references the template feature branch, includes `v3/.autotests-dev.yml`, and selects the existing `AUTOTESTS_IMAGE_TAG=devops-832-dev-autotests` for the backward-compatible pilot image.
- `mock-worker` now has a ClusterIP Service, internal task-specific `.dev.youdo.corp` ingress, and `/_/heartbeat` probes. No public `.dev.youdo.sg` worker ingress was added.

`helm lint` passed against `helm-charts/master`. Rendering for namespace `dev-devops-832` produced Service/Deployment/Ingress `youdo-business-tochka-proxy-mock-worker` and host `youdo-business-tochka-proxy-mock-worker-devops-832.dev.youdo.corp` with the expected probes.

Runtime correction prepared: the first live deployment showed that the added HTTP `/_/heartbeat` probes return 404 on mock-worker, leaving it `0/1 Ready` and causing kubelet restarts. Direct pod access confirmed `/_/hangfire` is available, but it must not be used as a health probe. The local service values now use TCP liveness/readiness probes on port 8080; Helm lint/render passed. Push the correction and redeploy. See `~/ai/current/knowledge/log/2026-09-03-dev-deployment-devops-832-mock-worker-probe-failure.md`.

## Actions

### Publication and runtime order

1. Autotest branch was pushed as commit `02dcaea` (`prepare tests for dev env`). Pipeline `137951` created manual build job `3111886`. Do not merge yet: run this job and verify that it publishes image tag `devops-832-dev-autotests`.
2. Commit/push the template branch.
3. Run GitLab CI Lint for the composed Tochka configuration.
4. Commit/push the service branch and run its MR pipeline.
5. Start `1 deploy dev`; correlate GitLab job, Jenkins build, derived namespace, auto-started dev test, endpoint access, reports, and cleanup.

No secret values were added to notes or new code.

## Findings

### Pipeline 137953 auto-start finding

Pipeline `137953` deployed successfully through GitLab job `3111987` and Jenkins build `150`, but `dev smoke tests` job `3112069` remained manual. The deploy trace printed `No dev smoke tests job is included; nothing to start` even though the job existed.

Cause: `dev smoke tests` used `needs` on the still-running `1 deploy dev`. While deploy queried only `scope=manual`, GitLab kept the dependent job in `created` state; it became `manual` only after deploy completed, too late for the caller to play it.

Local template correction: replace `needs` with `dependencies: ["1 deploy dev"]`. The dev job is then manual and discoverable while deploy is running, while stage ordering still delays execution until deploy completes and makes its dotenv artifact available. YAML parsing and `git diff --check` passed. The already completed pipeline requires manual start of job `3112069`; the automatic path must be retested in a new pipeline after the template correction is pushed.

### Job 3112069 execution finding

The manually started `dev smoke tests` job did launch the autotest image and Gradle `:test`, with `TARGET_ENV_SUFFIX=-devops-832`. No actual test case ran: the generated Allure report has `total=0`, and GitLab recorded one synthetic failed case, `Gradle Test Executor 1 / failed to execute tests`.

The first failure occurred in `ProjectTemplateSessionListener` before test discovery. Its eager `ProjectTemplateProvider.warmup()` attempted `POST https://b2bautomation-devops-832.dev.youdo.sg/api/Template` and received HTTP 502 instead of 200. The following Gradle `executor is null` exceptions are secondary fallout.

The initial inference that the whole `youdo.business` deployment was absent was disproved. Jenkins build `150` found and retained the existing `youdo-business-devops-832` Helm release, and the user confirmed the environment is deployed. Pipeline `137949` was also for `devops-689`, not the current `devops-832` environment, so its cleanup job is unrelated.

Two independent runtime faults were verified:

1. Browser mock login is broken by a cross-domain cookie configuration. B2B redirects to `http://youdo-business-mock-api-devops-832.dev.youdo.corp/youdo?...`; `/auth/login` responds with a secure cookie scoped to `domain=.dev.youdo.sg`. A response from `.dev.youdo.corp` cannot set a `.dev.youdo.sg` cookie, and a controlled curl cookie-jar check accepted zero cookies. The configuration-level fix is to expose the mock login on an HTTPS `*.dev.youdo.sg` hostname and point `AuthRedirectUrl` there; internal mock API dependency URLs can remain `.dev.youdo.corp`.
2. The autotest failure is not caused by the browser flow: the tests send a Bearer token directly. A read-only request with the exact token used by the autotest image reached the authenticated path but returned nginx `502 Bad Gateway`; `/health` and Swagger also returned 502. Thus the current test blocker is an unavailable/misrouted `automation-web` upstream behind the ingress. Direct pod/service/endpoints inspection is still required.

Kubernetes inspection could not be repeated because the local Yandex Cloud OAuth token is currently rejected for IAM token exchange; refresh access before the direct cluster check. Jenkins build `150` only validated the newly deployed Tochka release and explicitly kept the existing `youdo-business` release without upgrading or checking its rollouts.

The CI job nevertheless ended green because the QA Gradle configuration has `ignoreFailures = true`; report publication also posted a success marker despite the zero-test run. Per agreed scope, this QA-owned behavior is not changed in DevOps-832.

Before retrying the job, inspect `deployment/service/endpoints` and logs for `youdo-business-devops-832-automation-web`, restore its healthy upstream, and verify an authenticated request no longer returns 502. Browser login additionally needs the mock-auth hostname/domain correction described above.

### Nomad test14 comparison

Compared the live Nomad job `youdo-business-test14` with the source template `automation-test-yandex/playbooks/deploy/docker/files/nomad_youdo-business/youdo-business.j2` and Kubernetes `youdo.business/devops/dev.yml`.

- Nomad browser auth uses `AuthRedirectUrl=https://business-mock-api.test14.youdo.sg/youdo`, `Authentication__CookiesDomain=.test14.youdo.sg`, `Auth__CookiesDomain=.test14.youdo.sg`, `Auth__IsSecure=true`, and `B2BAutomationUrl=https://b2bautomation.test14.youdo.sg`. A controlled login stores the cookie successfully.
- Kubernetes correctly uses `.dev.youdo.sg` for both cookie settings and HTTPS for B2B, but its `AuthRedirectUrl` points to `http://youdo-business-mock-api-{buildId}.dev.youdo.corp/youdo`; mock-api has only that internal ingress. This is the confirmed browser-auth defect. Match the Nomad pattern by adding `business-mock-api.dev.youdo.sg` to the mock-api ingress (rendered as `business-mock-api-{buildId}.dev.youdo.sg`) and changing both the default and routing-template `AuthRedirectUrl` to its HTTPS URL.
- The effective Nomad `automation-web` task has 896 MB reserved and 1280 MB maximum; Kubernetes requests and limits only 256 MiB. The running Nomad test14 allocation was using about 436 MB when checked, already far above the Kubernetes 256 MiB limit. Other web/API components are also lower in Kubernetes, but `automation-web` is the current blocker. OOM/restart is therefore the leading explanation for the missing Kubernetes upstream, pending direct pod `lastState`/events confirmation.
- The compared variable-name set has no Nomad-only omissions after accounting for Vault-injected Kubernetes secrets. Kubernetes contains additional newer variables, so a missing environment key is not apparent.
- Runtime reference: Nomad `b2bautomation.test14.youdo.sg` returns `/health=200` and returns 200 with the exact Bearer token used by the Tochka test image. Kubernetes returns 502 for `/health` and for the same authenticated request.

Recommended `dev.yml` corrections: fix the public mock-login ingress/AuthRedirectUrl unconditionally; raise `automation-web` to `memory: 896Mi`, `memoryLimit: 1280Mi` if pod status/logs confirm OOM or memory pressure. Inspect pod last state, restart count, events, Service selectors, and Endpoints before making the resource change solely on inference.

### Manual Kubernetes correction

At the user's request, applied a live correction to namespace `dev-devops-832` using `/home/slnnk/.kube/config-yandex-dev` (the default kubeconfig used a different, broken Yandex IAM exec flow). Before the patch, pod `youdo-business-devops-832-automation-web-7769854684-d9b8t` had restarted six times; its last termination was confirmed `OOMKilled`, exit code 137. The deployment had a 256 MiB request and limit.

Live changes:

- ConfigMap `youdo-business-devops-832-env`: set `AuthRedirectUrl=https://business-mock-api-devops-832.dev.youdo.sg/youdo`.
- Ingress `youdo-business-devops-832-mock-api`: retained the internal `youdo-business-mock-api-devops-832.dev.youdo.corp` rule and added `business-mock-api-devops-832.dev.youdo.sg`, routed to Service `youdo-business-devops-832-mock-api:80`.
- Deployment `youdo-business-devops-832-automation-web`: set request `memory=896Mi` and limit `memory=1280Mi`, which triggered and successfully completed a rollout.

Post-change verification:

- new automation pod `youdo-business-devops-832-automation-web-5747d9d768-cs55z` became Ready with restart count 0;
- `https://b2bautomation-devops-832.dev.youdo.sg/health` returned 200;
- the same Bearer token used by the Tochka test image returned 200 instead of 502;
- `https://business-mock-api-devops-832.dev.youdo.sg/youdo` returned 200;
- browser-style B2B redirect targets the new HTTPS mock-login host;
- controlled user-8 login returned 302 to B2B and the client successfully stored the secure `youdoBusinessJwtAccessToken` cookie for `.dev.youdo.sg` (value not recorded).

These are live Kubernetes mutations and will be overwritten by the next Helm deployment. Persist the same AuthRedirectUrl, mock-api ingress host, and automation-web memory values in `youdo.business/devops/dev.yml` after runtime validation.

### Job 3112230 and Tochka OOM

The rerun job `3112230` executed the suite instead of failing at initialization. GitLab JUnit recorded 514 cases: 137 passed, 365 failed, and 12 skipped. Allure reported 584 results: 137 passed, 435 failed, and 12 skipped. The job still ended green because of the known QA-owned `ignoreFailures=true` behavior.

All 365 JUnit failures had exactly the same infrastructure symptom: HTTP 502. Of these, 180 expected HTTP 200 and 185 negative cases expected HTTP 400. No other JUnit failure category was present. Despite the CI name and `TEST_GROUP=smoke`, the test project still ran the hard-coded `regress` tag, which explains the large case count and remains outside the agreed DevOps-832 test-code scope.

Kubernetes proved the source of the 502 burst: pod `youdo-business-tochka-proxy-devops-832-mock-webapp-59fc8cbvx22l` was OOM-killed with exit code 137 and restarted once. Its previous process logged normal 200/400 responses through 23:40:52 MSK and was killed at 23:40:52.899. Allure then recorded 109 failures at 23:40:53, 171 at 23:40:54, and 146 at 23:40:55 (426 failures immediately after the kill). The pod recovered and the mock-webapp endpoint again returned HTTP 200.

No other current pod or init container in namespace `dev-devops-832` had a nonzero restart count or retained OOMKilled state after the earlier automation-web pod was replaced by its corrected rollout. Current Tochka Kubernetes resources are only 256 MiB request/limit for all four runtime components. At inspection time: mock-webapp 143 MiB after restart, mock-worker 244 MiB, proxy-webapp 138 MiB, proxy-worker 177 MiB. Mock-worker is therefore especially close to another OOM.

The live Nomad reference `youdo-business-tochka-proxy-test14` assigns 512 MB reserved and 1024 MB maximum to each of mock-webapp, mock-worker, proxy-webapp, and proxy-worker. Current Nomad usage was approximately 384, 416, 210, and 370 MB respectively. Before another load run, align the four Kubernetes deployments to `memory: 512Mi` and `memoryLimit: 1024Mi`, first as a live patch and then persistently in the Tochka `devops/dev.yml`.

### 2026-09-04 manual no-limit Tochka patch

Per user decision for test environments, manually updated all four Tochka Deployments in `dev-devops-832` to request 512 MiB and have no memory limit:

- `youdo-business-tochka-proxy-devops-832-mock-webapp`;
- `youdo-business-tochka-proxy-devops-832-mock-worker`;
- `youdo-business-tochka-proxy-devops-832-proxy-webapp`;
- `youdo-business-tochka-proxy-devops-832-proxy-worker`.

All four rollouts completed successfully. New pods were Ready with zero restarts, and mock/proxy webapp heartbeat endpoints returned HTTP 200. The scheduler placed mock-webapp, mock-worker, and proxy-worker on node `cl1e8jt27j03mj4g8q0g-ovir`; proxy-webapp also moved there during this rollout. The old mock-worker showed one restart roughly eight minutes before replacement, with readiness/liveness connection-refused events; its pod disappeared before `lastState` could be read, so OOM for that particular restart is likely from the previous 244/256 MiB pressure but not proven.

This is a live patch and will be overwritten by Helm. Persist the policy in Tochka `devops/dev.yml` as `memory: 512Mi` for all four services and omit `memoryLimit`.

### 2026-09-04 post-rerun OOM audit

After the user ran dev smoke job `3112281` (00:08:56-00:14:02 MSK), all four newly rolled out Tochka pods remained Ready with zero restarts and no retained OOM state. They kept `requests.memory=512Mi` with no memory limit. During the post-run sample, mock-webapp used about 756 MiB and mock-worker about 671 MiB, proving that the old 256 MiB limits would have killed both again; proxy-webapp used about 98 MiB and proxy-worker about 149 MiB.

One dependency did OOM during the same test job: `youdo-business-doc-generator-devops-832-api-6c99bcf55b-qljnm`, at 00:10:55 MSK, exit code 137, `OOMKilled`, restart count 1. Its request and limit are both 256 MiB. It recovered immediately and was Ready, using about 82 MiB after restart. No other current pod or init container in the namespace showed a nonzero restart count or retained OOMKilled state, and no eviction/MemoryPressure event was found.

If the no-memory-limits policy is extended from Tochka itself to its test dependencies, doc-generator is the next confirmed candidate: set a realistic request and remove its memory limit, then persist the change in the doc-generator `devops/dev.yml` rather than relying only on a live patch.

### 2026-09-04 dev smoke/regression jobs and persistent Tochka resources

The user superseded the earlier no-limit persistence decision for Tochka: the four runtime components should use `requests.memory=512Mi` and `limits.memory=1024Mi`.

Prepared, not committed or pushed:

- `/home/slnnk/git/gitlab-ci-templates/v3/.autotests-dev.yml`: preserved the user's existing local `needs` to `dependencies` change; made `.autotests-dev` extend the common `.autotests` template; renamed `dev smoke tests` to `smoke tests`; added `regression tests`; jobs set `TEST_GROUP` to `smoke` and `regress` respectively.
- `/home/slnnk/git/youdo-business-tochka-proxy/devops/dev.yml`: set `memory: 512Mi` and `memoryLimit: 1024Mi` for `proxy-webapp`, `mock-webapp`, `proxy-worker`, and `mock-worker`. PostgreSQL remains at 256Mi request/limit.

Validation:

- `git diff --check` passed in both repositories.
- Ruby/Psych parsed `v3/.autotests-dev.yml` successfully, including GitLab's custom `!reference` tag syntax.
- `helm lint ./microservice` passed.
- Rendering Tochka values with the shared `microservice` chart produced each of the four Deployments with memory request `512Mi` and limit `1024Mi`.
- Full GitLab merged-CI validation remains for after the template branch is pushed, because the service include references the remote `DevOps-832-dev-autotests` branch.

### Pipeline 137960 / deploy job 3112290

- Tochka commit `8090532` (`increase memory limits`) was deployed successfully through Jenkins build 151.
- Runtime verification in `dev-devops-832` confirmed all four Tochka Deployments now have `requests.memory=512Mi` and `limits.memory=1Gi`.
- The pipeline contains the renamed manual jobs `smoke tests` (`3112372`) and `regression tests` (`3112373`).
- Automatic smoke launch did not occur because `v3/.deploy-dev.yml` still queried the GitLab pipeline for the old job name `dev smoke tests`. The deploy trace printed `No dev smoke tests job is included; nothing to start`.
- Prepared locally in `/home/slnnk/git/gitlab-ci-templates/v3/.deploy-dev.yml`: changed the lookup and operator messages from `dev smoke tests` to `smoke tests`. Regression remains intentionally manual; only smoke is auto-played after a successful deploy.
- YAML parsing and `git diff --check` passed. The fix is not committed or pushed. Existing pipeline 137960 retains its compiled configuration; after publishing the template fix, a new service pipeline is required to verify automatic smoke launch. The current pipeline's smoke job can be started manually if only test execution is needed.

### Pipeline 137961 / deploy job 3112382

- The template fix was published as `gitlab-ci-templates` commit `34b63d6` (`fix smoke autostart`). Pipeline 137961 contains `smoke tests` job `3112464` and `regression tests` job `3112465`, both initially manual as designed.
- Deploy job `3112382` failed before reaching the smoke auto-play block because Jenkins build 152 returned `FAILURE`.
- The Helm upgrade itself succeeded, all four current Tochka Deployments rolled out, and their new pods were Ready. Jenkins then ran a strict post-rollout query for every non-Job pod with the release label and counted one old `proxy-webapp` pod from the previous ReplicaSet in phase `Failed`/displayed as `Error` while it was being removed.
- The stale pod was `youdo-business-tochka-proxy-devops-832-proxy-webapp-9cfd6dp5bp7`, owned by old ReplicaSet `...-9cfd6d8f9` with desired/current replicas 0. It was deleted normally moments later. Current Tochka pods are healthy; this was a rollout cleanup race, not an application deployment failure.
- The overly strict check is in `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile` around lines 980-990: immediately after successful `kubectl rollout status`, it counts all labeled non-Job pods with `status.phase!=Running`, including terminating pods from old ReplicaSets.
- Recommended minimal hardening: retry the non-running-pod check for a short bounded period after rollout (or filter pods with `metadata.deletionTimestamp != null`) so transient old ReplicaSet pods do not fail Jenkins, while persistent Pending/Unknown/Failed current pods still fail the deploy.
- Because Jenkins failed, GitLab never reached the now-correct smoke auto-start code. For pipeline 137961, smoke can be launched manually against the healthy deployed namespace; a subsequent clean pipeline is required to verify automatic launch end-to-end.

### Pipeline 137961 successful retry and automatic smoke verification

- The original deploy job `3112382` failed on the transient old-ReplicaSet pod race described above, but its retry `3112466` completed successfully through Jenkins build 153.
- The corrected GitLab template automatically played `smoke tests` job `3112464`; deploy trace explicitly reported `Started smoke tests job 3112464`. This proves the rename/autostart flow end-to-end.
- `smoke tests` received the deploy dotenv/artifacts, validated namespace ownership, and passed `TARGET_ENV_SUFFIX=-devops-832`, `TARGET_HOST=none`, and `TEST_GROUP=smoke` to the existing test image.
- GitLab JUnit summary for `smoke tests`: 603 total, 587 passed, 16 skipped, 0 failed, 0 errors. Allure/report artifacts were uploaded under job id `3112464`. `regression tests` job `3112465` remained manual as intended.
- All current Tochka workload pods remained Running with zero restarts after the smoke run. Sample memory: mock-webapp 437Mi, mock-worker 367Mi, proxy-webapp 122Mi, proxy-worker 172Mi; their 512Mi requests / 1Gi limits held.
- Dependency `youdo-business-doc-generator-devops-832-api-6c99bcf55b-qljnm` was OOMKilled again at 2026-09-04 01:22:02 MSK during smoke (exit 137), increasing restart count to 2. It recovered immediately and the test run still completed without failures. Its current 256Mi limit remains a confirmed separate reliability risk.

### 2026-09-04 dependency memory commits and regression timing

- Manual `regression tests` job `3112465` in pipeline `137961` completed successfully at 01:34:42 MSK after 344 seconds.
- Doc-generator branch `DevOps-832-increase-mem` was pushed later as commit `e9d86aa` at 18:21:02 MSK. It changes API memory from 256Mi/256Mi to 512Mi request / 1Gi limit.
- `youdo.business` branch `DevOps-832-b2bautomation-mem` was pushed later as commit `a41e0a0` at 18:24:58 MSK. It changes automation-web from 256Mi/256Mi to 512Mi request / 1Gi limit, not the earlier proposed/live-patched 896Mi/1280Mi.
- A read-only cluster check at 18:36 MSK proved that the namespace had not consumed the commits: automation-web was Running with zero restarts at the live-patched 896Mi/1280Mi; doc-generator was Running on the old 256Mi/256Mi pod with three restarts and retained `OOMKilled` state.
- Conclusion: source changes are pushed and the earlier regression job succeeded, but that regression cannot validate commits created roughly 17 hours later. Redeploy both feature revisions and rerun the load/regression check before declaring the memory work runtime-complete.

Follow-up operator decision and GitLab verification:

- Doc-generator MR 34 merged to `master` at 18:22:05 MSK with merge commit `bdee550d`.
- `youdo.business` MR 3738 merged to `master` at 18:29:40 MSK with merge commit `b7d1df43`.
- Do not run another Tochka deployment solely for these values. Verify them when onboarding the next service to post-deploy autotests; its fresh/full-catalog deployment will consume dependency `master` revisions.
- Prepare autotest changes across all selected projects first and keep them on feature branches. Merge the coordinated test projects, shared template, and service changes together only after the complete set is ready.
- Pipeline `137961` final status is success. The earlier failed deploy retry is retained in history, while the successful retry and smoke job determine the completed result.

## Open items

- Persist the `AuthRedirectUrl` / `business-mock-api-{buildId}.dev.youdo.sg` ingress correction in `youdo.business/devops/dev.yml` (live-patched only).
- Jenkins post-rollout pod check hardening (done as `20b9d78`, see `2026-09-04-dev-deployment-jenkins-pod-race.md`).
- Verify merged doc-generator/automation-web memory values in the next fresh namespace.

## Portable lesson

- `~/ai/general/knowledge/gitlab-ci/manual-job-with-needs-stays-created.md`
- `~/ai/general/knowledge/k8s/post-rollout-pod-phase-check-false-failures.md`
