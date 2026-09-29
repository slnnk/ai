---
system: dev-deployment
status: verified
checked: 2026-09-29
tags: [devops-832, autotests, smoke, regression, gitlab-ci, tochka, billing, tkb, target-env-suffix]
---
# B2B dev-deployment: post-deploy autotests

Last verified: 2026-09-07

Authoritative system map: `~/ai/current/knowledge/systems/dev-deployment/overview.md`.

## Merge readiness (checked in GitLab 2026-09-28, updated 2026-09-29)

2026-09-29: templates branch merged to `master` (`76347cd`, includes `.autotests-dev.yml`
with `TARGET_ENV_SUFFIX` without dash); the branch is kept. Master templates now emit the
no-dash value, so any service using `.autotests-dev.yml` must use a test image with
`DEV_HOST_SUFFIX` code; old `latest` images would build `...webappdevops-832...`.

2026-09-29 00:30-00:36: MR pipelines of Billing (139727, Jenkins 164), TKB (139728, Jenkins
165) and Tochka (139729, Jenkins 166) ran `1 deploy dev` at the same time. All three use task
id DevOps-832, so they target the same namespace `dev-devops-832`. Jenkins 166 failed with
Helm `UPGRADE FAILED: another operation (install/upgrade/rollback) is in progress`; the
namespace label `jenkinsJobId` ended at 166, and smoke jobs of 164/165 stopped at
`Namespace ownership mismatch` (the stale-pipeline protection worked as designed). Suffix and
images were correct (`Target environment suffix: devops-832`). Releases were left
`deployed` (none pending). Workaround: deploy services of one task one after another.

Sequential rerun 2026-09-29 00:43-01:06, all suffix-based URLs correct (no `...webappdevops...`):
- Tochka: deploy 3190033 (Jenkins 167), smoke 3189750 and regression 3189751: 514 cases,
  376 passed, 123 failed, 15 skipped. 121 failures are `404` on
  `POST /v1/beneficiaries/createPerson` (and the IE variant): the service `master` merged
  into the MR includes Site-24856 (`e4274f3`, 2026-09-22) which removed the v1 create
  methods; only `/v2/beneficiaries/createPerson` and `/v2/.../createIndividualEntrepreneur`
  remain. Tests (`CreatePersonStepImpl`, `CreateEntrepreneurStepImpl`, used by
  `PersonHelper`) still call v1. Application/QA drift, not infrastructure; legacy Nomad
  runs against the new service version will fail the same way.
- Billing: deploy 3190075 (Jenkins 168), smoke 3190117: 545 cases, 3 failed (two known
  `GetYouDoBalanceHistoryTest`, new `RefillYouDoBalanceTest [tkbBankDefault]` NPE on empty
  balance; data/QA).
- TKB: deploy 3190162 (Jenkins 169), smoke 3190163: 174 cases, same 2
  `IdentifyToBeneficiaryTest` failures. TKB repeat deploy recreated `postgres-0`
  (01:01) and `mock-api` restarted once with exit 137 `Error` (not OOMKilled) at 01:02
  (hypothesis: liveness failure while its DB pod restarted).
- On repeat deploy the primary's `postgres-0` pod is recreated (StatefulSet with PVC).

Merge 2026-09-29: test projects merged 01:11 (tochka-tests !85, tkb-tests !16,
billing-tests !64); Tochka service !237 merged 01:18:34 with `master` CI clean (no templates
`ref`, no `AUTOTESTS_IMAGE_TAG`). GitLab auto-started the environment `on_stop` job
`3 delete dev` 3189673 four seconds after the merge (confirms stop on MR merge, in addition
to `auto_stop_in: 7 days`). It failed by design: `Namespace dev-devops-832 belongs to Jenkins
build 169, but this job expects build 167` (the shared namespace was last deployed by TKB).
Tochka environment 457 stays `stopping` until the job succeeds; after the namespace is
gone, a retry of 3189673 finds no namespace and succeeds. Only the pipeline that owns the
namespace (TKB, 169) can delete it.

Final state 2026-09-29 01:40: TKB !63 merged 01:31, Billing !97 merged 01:38; all three
service `master` CI files include `v3/.autotests-dev.yml` without pins; master pipelines
139746/139748/139750 green; test-project master pipelines ran `build`, `publish-maven`,
`update latests`; namespace `dev-devops-832` is gone and environments 457/472/460 are
`stopped` (Tochka delete retried as 3190623). Tochka, TKB and Billing are rolled out.


Open MRs from `DevOps-832-dev-autotests`: `youdo-business-tochka-proxy` !237,
`youdo-business-tkb-proxy` !63, `youdo-business-billing-service` !97,
`youdo-business-billing-service-tests` !64 (last pipeline canceled). No MR yet for
`gitlab-ci-templates` (branch `DevOps-832-dev-autotests`, 3 commits: `b55929d`, `fd00a30`,
`34b63d6`; adds `v3/.autotests-dev.yml`, changes `v3/.deploy-dev.yml` and `v3/.main.yml`;
merges into current `master` without conflicts), `youdo-business-tochka-proxy-tests`
(`02dcaea`) and `youdo-business-tkb-tests` (`6615a91`). Main `youdo.business` and
`youdo-business-tests` have no branch.

Every service MR pins the templates include to `ref: DevOps-832-dev-autotests` and sets
`AUTOTESTS_IMAGE_TAG: devops-832-dev-autotests`; both must be removed once templates and
test projects are in `master`. Merge order: templates, test projects, service MRs.

TKB after the memory fix: pipeline 138096 (`aa4d083`), deploy 3120801 on 2026-09-07, smoke
3120883 and regression 3120884 both 172/174 with the same two `IdentifyToBeneficiaryTest`
failures; peak memory was not recorded. `3 delete dev` 3120803 ran 2026-09-14 23:24, seven
days after the deploy, which matches `auto_stop_in: 7 days`: the first observed real
auto-stop expiry. It uninstalled the release and deleted `dev-devops-832`.

## youdo.business suite: audit and plan (2026-09-28)

Branches `DevOps-832-dev-autotests` exist locally in `youdo.business`, `youdo-business-tests`,
`youdo-business-ui-tests` (equal to `master`, not pushed); local templates checkout is on
`DevOps-832-dev-autotests`.

Findings:
- `youdo-business-tests` builds all URLs in
  `src/main/java/api/steps/specifications/request/ApiEndpoints.java:13-24` from
  `TARGET_HOST` and `TARGET_PROXY=.yandex-test.youdo.local` (constant from Nexus artifact
  `b2b:youdo-business-test-lib`). Used:
  ADMIN `b2bautomation`, BUSINESS, BUSINESS_API, EMPLOYEE, MOCK
  (`youdo-business-mock-api`), BUSINESS_DOC (shared `doc-generator`, no stand label),
  DOC_VALIDATION (`doc-validation`, dev name is `docvalidation`), BUSINESS_WORKER
  (`https://b2bautomation.<H>.youdo.sg/hangfire/recurring/trigger`), TEST_CLIENT (shared
  `b2b-test-client`). C2C and MODERATION are defined but unused by tests.
- Tochka/TKB/Billing step classes come from their test projects as Maven
  `1.0.0-SNAPSHOT`; `publish-maven` runs only on `master`. The main suite therefore sees the
  `TARGET_ENV_SUFFIX` mode of those projects only after their MRs are merged.
- `b2b:youdo-business-test-lib` is module `lib` of `youdo/Test/youdo-business-tests-plugin`
  (project 537, `settings.gradle.kts`: `include("plugin", "lib")`); found by matching the
  Nexus upload time of `1.0-20260731.144748-8` with `publish-maven` job 3045413 of pipeline
  136105 (`e73e3bf`). `lib/.../BaseApiService.java:20-21` defines `TARGET_HOST` and
  `TARGET_PROXY`; `lib/.../specifications/ApiEndpoints.java:7-9` builds
  `B2B_AUTOMATION_URL`, `BUSINESS_MOCK_API_URL` (both need the suffix mode) and
  `METRICS_URL` (shared). Local checkout `~/git/youdo-business-tests-plugin` was 152 commits
  behind on 2026-09-29.
- Gradle plugin `b2b:youdo-business-test-plugin` (module `plugin` of the same repo) task `precondition` (dependency of `test`)
  hardcodes `http://b2bautomation.<TARGET_HOST>.yandex-test.youdo.local`.
- `b2b-test-client` (`youdo/Test/youdo-business-tests-client`) seeds data directly in
  `<targetHost>_youdo-business` on a shared PostgreSQL; the dev DB lives inside the namespace.
  Used by 5 test classes (company risks, repay, Tochka hold/documents, webhooks).
- UI suite: Kotlin + Playwright, local headless Chromium in the test image (no grid);
  `BaseTest.kt:254-255` `https://employee|business.<H>.youdo.sg`, auth cookie domain
  `.<H>.youdo.sg` (`:88-90`), header `X-Real-Ip` for AntiFraud; setup API calls through
  `youdo-business-tests` classes (SNAPSHOT). Template `v3/.autotests-ui.yml` has no dev
  variant; the deploy job autostarts only a job named `smoke tests`.
- Dev memory in `youdo.business/devops/dev.yml` is far below Nomad `memory_max`
  (business-web 256Mi vs 2048, worker 512Mi vs 2048, business-api/employee-web/mock-api/
  internal-api 256Mi vs 512).
- All suites: `ignoreFailures=true`; UI ~34 smoke / ~119 regress, API ~39 smoke / ~327
  regress; JUnit parallelism 15.

Dev hostnames (`<sfx>` = `-` + `TARGET_ENV_SUFFIX`, the dash is added in test code): `https://business<sfx>.dev.youdo.sg`,
`https://business-api<sfx>.dev.youdo.sg`, `https://employee<sfx>.dev.youdo.sg`,
`https://b2bautomation<sfx>.dev.youdo.sg`, `http://youdo-business-mock-api<sfx>.dev.youdo.corp`,
`http://doc-generator<sfx>.dev.youdo.corp`, `http://docvalidation<sfx>.dev.youdo.corp`.

Compatibility check of the prepared MRs (2026-09-29):
- Test projects (Tochka `02dcaea`, TKB `6615a91`, Billing `8e36a0f`): only the URL class and an
  entrypoint echo change; the Nomad fallback strings are byte-identical to `master`, so
  legacy jobs (no `TARGET_ENV_SUFFIX`) and SNAPSHOT consumers keep the old URLs.
- Templates branch `34b63d6`: 12 `deploy-dev` consumers lint valid. The new autostart in
  `1 deploy dev` runs only with `AUTOTESTS=true` and plays only a job named `smoke tests`;
  legacy `smoke-tests testN` jobs are not matched.
- Service MRs change only `.gitlab-ci.yml` and `devops/dev.yml` (dev-only memory, worker
  Service/ingress). `AUTOTESTS_IMAGE_TAG` is shared with the legacy `.autotests` jobs
  (`AUTOTESTS_IMAGE` in `v3/.main-vars.yml:30`, default `latest`), so the pin must be removed
  before merge together with the templates `ref`. Without both pins all three lint valid and
  expose `smoke tests` / `regression tests`. No conflicts with `master` (Tochka is 6 behind).
- Decisions 2026-09-29: UI suite is in DevOps-832 scope; tests depending on `b2b-test-client`
  are allowed to fail for now.

## Verified TKB integration status

On 2026-09-07 pipeline `138093` at service commit `6b24286` runtime-proved the initial deployment. Deploy job `3120707` triggered Jenkins build `159`, which loaded `jenkins-pipelines/master` commit `ae1a125`, ran on `AutoTest`, created `dev-devops-832`, and deployed TKB as primary plus all 12 catalog dependencies. The deploy job automatically started smoke `3120789`; regression `3120790` was started manually. Test-project pipeline `138092` successfully built branch commit `6615a91`; the service jobs selected its `devops-832-dev-autotests` image tag.

The service exposes component `worker-mock` through a ClusterIP Service plus internal host `youdo-business-tkb-proxy-worker-mock-devops-832.dev.youdo.corp`. No public worker route exists. HTTP checks returned 200 from TKB mock-webapp `/_/healthcheck`, worker-mock `/_/healthcheck`, and public automation-web `/health`. All namespace workloads are Ready with zero restarts and there are no Kubernetes Warning events.

The test branch now accepts `TARGET_ENV_SUFFIX` while preserving the existing Nomad `TARGET_HOST` fallback. Kubernetes mode maps the old logical test targets to `youdo-business-tkb-proxy-mock-webapp<suffix>.dev.youdo.corp`, `youdo-business-tkb-proxy-worker-mock<suffix>.dev.youdo.corp`, and `https://b2bautomation<suffix>.dev.youdo.sg`. The entrypoint reports the suffix without changing test selection, failure propagation, credential fallback, retries, or report behavior.

Both suites ran 183 Gradle tests and reported `BUILD SUCCESSFUL` only because `ignoreFailures=true`. Each had the same two failures: the two `IdentifyToBeneficiaryTest` cases expecting an incoming payment to remain `New` exhausted the ten polling iterations and threw `Входящий платеж не в статусе New`. GitLab imported 174 cases per job: 172 passed and 2 failed. All repeated worker-trigger and incoming-payment-list steps passed, so the endpoint mapping itself is proven. TKB logs during the tests contain Billing `ACCOUNT_NOT_FOUND` errors while refilling balances for generated beneficiaries; this supports a test-data/cross-service consistency issue, not an ingress or worker reachability failure. The exact application/QA correction remains pending.

TKB memory is not yet runtime-accepted for load stability. `mock-api` sampled at 256388Ki against its 256Mi limit (about 97.8%) after both suites; `worker-mock` sampled at 180880Ki (about 69%). Neither restarted or retained OOM state. Published service commit `aa4d083` raises both components to 512Mi request / 1Gi limit, matching the proven Tochka/Billing workload profile. MR pipeline `138096` built and unit-tested the commit successfully; manual deploy job `3120801` has not been started. Rerun deploy, automatic smoke, and manual regression while observing peak usage. Repeat-deploy isolation and cleanup/stale-pipeline verification are also pending.

## Verified Tochka pilot status

The Kubernetes post-deploy autotest path is operational on the three pushed `DevOps-832-dev-autotests` branches. Pipeline `137961` / successful deploy retry `3112466` used Jenkins build 153 and automatically started `smoke tests` job `3112464`. Namespace ownership and `TARGET_ENV_SUFFIX=-devops-832` were verified before the existing test image ran. GitLab received 603 JUnit cases: 587 passed, 16 skipped, no failed/error cases. `regression tests` job `3112465` exists as a manual job. Allure/JUnit publication succeeded.

Tochka's four workloads are now persisted and deployed with 512Mi memory requests and 1Gi limits; all remained Running with zero restarts through the successful smoke run.

## Verified Billing integration status

Billing pipeline `137991` at service commit `1b6ed25` succeeded on 2026-09-04. Deploy job `3114239` invoked Jenkins build `155`; the build loaded Jenkins revision `20b9d78`, created fresh namespace `dev-devops-832`, deployed the complete 13-service catalog with Billing primary, and published the expected Billing ingress. It automatically played `smoke tests` job `3114321`; `regression tests` job `3114322` remains manual.

The smoke job used billing-tests feature commit `8e36a0f` through image `registry.youdo.sg/youdo/test/youdo-business-billing-service-tests/autotests:devops-832-dev-autotests`, validated namespace ownership, derived `TARGET_ENV_SUFFIX=-devops-832`, retained `TARGET_HOST=none`, and reached `http://youdo-business-billing-service-webapp-devops-832.dev.youdo.corp`. Allure and JUnit artifacts were published successfully.

The green job is not a clean functional pass. Gradle logged 553 executed tests and 3 failures, while GitLab imported 545 cases: 542 passed and 3 failed. The three reported failures were one `RefillYouDoBalanceTest` parameterization returning a null item and two `GetYouDoBalanceHistoryTest` parameterizations returning zero where the test expected a non-zero value. Existing `ignoreFailures=true` converted the Gradle test task to `BUILD SUCCESSFUL`; the job is also `allow_failure: true`. This is the already documented QA-owned failure-propagation limitation, not a Kubernetes routing failure. The 553-versus-545 count discrepancy should be checked when QA/report semantics are addressed.

Runtime infrastructure after smoke:

- Billing webapp, doc-generator API, and automation-web were Ready with zero restarts and no retained termination reason.
- Merged master resources are active: doc-generator API and automation-web each use 512Mi request / 1Gi limit.
- Billing webapp still used 256Mi request/limit and sampled at approximately 248Mi after smoke. Manual regression job `3114322` then confirmed the risk: the container was `OOMKilled` at 19:29:14 MSK with exit 137 and restarted once. The restart caused 502 responses for the remainder of the suite.
- Two transient Warning events occurred during namespace bootstrap (`FailedMount` for RabbitMQ projected config and `FailedAttachVolume` while docvalidation PV provisioning converged); all PVCs are now Bound and affected pods are Running.
- Jenkins race-handling code executed and accepted all active workload pods, but this was a fresh namespace and did not recreate deletion of an old ReplicaSet pod. The original race scenario still needs a repeat deployment to be fully proven.

Manual Billing regression result:

- job `3114322`, runner `gitlab-runner-docker-3`, ran from 19:27:20 to 19:29:46 MSK and remained status `success` because failures are ignored;
- Gradle: 553 total, 540 failed; GitLab JUnit: 545 total, 13 passed, 532 failed;
- all 532 GitLab failures have the same infrastructure signature: expected HTTP 200 or 400, received 502;
- Billing webapp OOM/restart at 19:29:14 MSK is temporally aligned with the 502 cascade;
- the pod recovered and is Ready, using approximately 98Mi after restart, but the regression run is invalid;
- required correction: increase Billing webapp from 256Mi/256Mi, starting with 512Mi request / 1Gi limit, then redeploy and rerun regression while watching peak usage and restarts.

Repeat-deploy attempt after the memory correction:

- GitLab pipeline `137992`, deploy job `3114330`, Jenkins build `156`;
- Jenkins loaded the expected race-fix revision `20b9d78`, refreshed namespace TTL, upgraded the namespace chart to revision 2, and correctly selected only Billing for application upgrade;
- build 156 ran on Jenkins node `Jenkins`, unlike build 155 on `AutoTest`;
- the Billing branch failed before Helm rendering/upgrading because `writeServiceRoutingOverlay` invokes `python3`, which is absent on node `Jenkins`; shell exit code 127;
- Billing Helm release remains revision 1, image tag from pipeline `137991`, 256Mi request/limit, with the earlier single OOM restart;
- all existing namespace workloads remain available; no partial Billing release revision was created;
- correction options: preferably replace the node-local Python/PyYAML parsing with a portable mechanism already guaranteed by the pipeline, or explicitly standardize/install Python plus PyYAML and constrain eligible Jenkins agents. `Pipeline Utility Steps/readYaml` is not currently installed on this Jenkins instance.
- Operator-selected short-term correction: `jenkins-pipelines/master` commit `ae1a125` (`fix node`) pins the Jenkinsfile with `node('AutoTest')`, with README documentation and a passing Groovy assertion. On 2026-09-04 `AutoTest` host `jenkins-agent-test-01` was cleaned by removing only the unused prior agent Docker image and vacuuming the journal to 200MiB. Root free space rose from 1.1GiB to 2.1GiB; the active container/image remained running. Jenkins' stale temporary disk block was toggled off after cleanup, and API verification reported the node online with five executors.

Open infrastructure work:

- Resolved and runtime-proven: Jenkins build 152 / GitLab job `3112382` exposed a post-rollout race. `jenkins-pipelines/master` commit `20b9d78` retries the check, excludes deletion-marked and Job pods, and preserves failure for persistent non-Running active pods. Billing Jenkins build `158` observed the old ReplicaSet pod in `Terminating`, ignored it correctly, and completed successfully.
- `youdo-business-doc-generator/api` correction is merged to `master` through MR 34 / merge commit `bdee550d`: 512Mi request / 1Gi limit. `youdo.business/automation-web` correction is merged through MR 3738 / merge commit `b7d1df43`: 512Mi request / 1Gi limit. The existing `dev-devops-832` namespace predates both merges and therefore does not validate them.
- Manual `regression tests` job `3112465` succeeded in pipeline `137961` from 01:28:58 to 01:34:42 MSK (344 seconds), before both memory merges. Per operator decision, do not repeat Tochka solely for memory verification: the next service onboarded to post-deploy autotests will create/refresh the full dependency catalog from `master`, and that run must verify the new doc-generator and automation-web resources, restarts/OOM, peak memory, and Jenkins old-ReplicaSet handling.
- Rollout/merge policy: first configure post-deploy autotests for every selected service and test project on feature branches. Keep the coordinated application/test/template changes unmerged during preparation. After all projects are ready, merge the complete set in dependency order, switch temporary template refs to `master`, and run final end-to-end verification.

## Automation UI identification

The card-based admin landing page with sections such as `Пользователи б2б`, `Сообщения и рассылки`, and `Полезное` is the `YouDo.B2b.Automation.Web` SPA route `/automation`. Its source is `YouDo.B2b.Automation.Web/spa/src/components/automation/AutomationPage.tsx`; production is routed through `https://b2bautomation.youdo.com`, while task-specific Kubernetes environments use `https://b2bautomation-<buildId>.dev.youdo.sg`. A cropped screenshot without the browser address bar is insufficient to distinguish production from dev.

## Goal

Run a service's existing API autotests against the task-specific Kubernetes environment immediately after that service has been deployed as the main service by the Jenkins-backed `1 deploy dev` GitLab job. Tochka proxy is the pilot; the active rollout scope covers Billing, TKB, and the main `youdo-business` suite. By operator decision on 2026-09-04, Sber and its test project are excluded because the service is no longer current.

## Current delivery path

1. An opted-in service MR pipeline includes `v3/.deploy-dev.yml`, `v3/.autotests.yml`, and `v3/.autotests-dev.yml` from `gitlab-ci-templates`.
2. The manual `1 deploy dev` job invokes Jenkins and waits for a successful rollout.
3. Jenkins deploys the main service and catalog dependencies into `dev-<task-or-branch>` and archives `generated/deploy-dev.env` plus `generated/ingress-urls.txt`.
4. GitLab imports `DEV_NAMESPACE`, `JENKINS_BUILD_NUMBER`, and `JENKINS_BUILD_URL` into `deploy-dev.env`; it also retains the ingress report and publishes it in the GitLab Environment description.
5. The existing autotest template exposes 18 smoke and 18 regress jobs for static `TARGET_HOST=test..test17`. It launches the externally built test image with Docker-in-Docker and forwards `TARGET_*`, `TEST_*`, and `CI_*` variables.

The legacy static jobs remain uncoupled and use the Nomad `TARGET_HOST` contract. The new `smoke tests` and `regression tests` jobs consume deploy artifacts; successful deploy auto-plays smoke and leaves regression manual.

## Tochka endpoint audit

The current test code in `/home/slnnk/git/youdo-business-tochka-proxy-tests` constructs three targets from `TARGET_HOST` and the fixed `.yandex-test.youdo.local` suffix:

- mock webapp: used throughout the API steps;
- mock worker: used by job-trigger scenarios;
- `b2bautomation`: used by template-generation scenarios.

The Tochka feature branch now exposes the required `mock-worker` through a ClusterIP Service and internal `.dev.youdo.corp` ingress. The worker uses TCP liveness/readiness probes because it accepts connections on port 8080 but does not provide the web heartbeat route. `proxy-worker` remains internal with no Service because the test suite does not call it directly.

`youdo-business` provides `automation-web` and its task-specific `b2bautomation-<buildId>.dev.youdo.sg` ingress. MR 3567 was merged to `master` as `a4f80388` on 2026-09-03 after pipeline `137949` and Jenkins build `148` proved the corrected `Staging` configuration. A normal Tochka-main deployment can therefore use the default `youdo-business/master` dependency; no explicit feature version is required.

## Cross-service audit

Services currently enabling `v3/.autotests.yml` and `AUTOTESTS=true` on `origin/master`:

| Service | Test image repository | Endpoint shape | Kubernetes gap |
|---|---|---|---|
| `youdo-business-tochka-proxy` | `youdo-business-tochka-proxy-tests` | mock webapp + mock worker + automation-web | pilot gap resolved and runtime-proven on feature branches |
| `youdo-business-tkb-proxy` | `youdo-business-tkb-tests` | mock API + worker + automation-web | initial deploy and endpoint connectivity runtime-proven in pipeline `138093`; two masked functional failures and near-limit mock-api memory remain; repeat/cleanup pending |
| `youdo-business-billing-service` | `youdo-business-billing-service-tests` | webapp only | Completed for DevOps-832. Pipeline `137992`, deploy retry `3114414`, Jenkins `158` proved the `AutoTest` pin, repeat rollout, 512Mi/1Gi resources, zero restarts, smoke and regression connectivity. Each suite has 2 remaining functional assertions, masked by `ignoreFailures`. |
| `youdo.business` | `youdo-business-tests` | many product and dependency endpoints | requires a per-endpoint map, not one host suffix |

`youdo-business-sber-proxy` and `youdo-business-sber-proxy-tests` are explicitly outside the rollout scope because the service is no longer current; do not add Sber to the Jenkins dev catalog for DevOps-832.

This proves that `TARGET_HOST` cannot keep its old meaning of a stand name inserted as a separate DNS label. The reusable value must instead be the task suffix inserted into each component's known base hostname; schemes, zones, and the stable component base names remain owned by the individual test project.

## Additional correctness and security findings

Scope decision recorded 2026-09-03: these are QA-owned issues and are explicitly outside DevOps-832. The Tochka infrastructure pilot will run the existing suite as-is and change only endpoint selection through `TARGET_ENV_SUFFIX`. These findings do not block the pilot, but the resulting job must remain `allow_failure: true` and must not be presented as a trustworthy release gate until QA addresses them.

- Tochka, TKB, and Billing build scripts set `includeTags("regress")` unconditionally. `TEST_GROUP=smoke` currently changes report metadata but does not select smoke tests.
- Those projects set Gradle `ignoreFailures = true`; the entrypoint returns the Gradle exit code, so assertion failures may be reported as a successful container. QA must address this before the job can be treated as a gate; DevOps-832 leaves it unchanged.
- Tochka has a hard-coded fallback for `TEST_ACCESS_TOKEN` in `src/main/java/tochka/api/steps/specifications/BaseRequestSpecification.java`. Do not copy the value. Remove the fallback, obtain the credential from a masked/protected CI variable or secret store, and rotate it if it is still active.
- Tochka retry handling probes an unrelated external address before retrying the actual request. Replace this with retry handling around the target request or health preflight; otherwise failures can be misclassified.

## Recommended design

### Execution model

Keep the existing test image and Docker-in-Docker report/upload mechanism for the first rollout. Add dedicated `smoke tests` and `regression tests` jobs rather than duplicating the static `test..test17` matrix. Both jobs must:

- `need` artifacts from `1 deploy dev`;
- reuse the same `resource_group` as deploy/extend/delete so the namespace cannot be redeployed or deleted while tests run;
- run `verify_dev_namespace` against `DEV_NAMESPACE` and `JENKINS_BUILD_NUMBER` before testing;
- derive and pass the task-specific hostname suffix from `DEV_NAMESPACE`;
- record namespace, Jenkins build URL, exact endpoints, test image digest, and report URL;
- remain `allow_failure: true`; making it required is deferred until QA owns and corrects the existing test semantics.

Smoke should be started automatically only after a successful manually-started deploy. The existing same-pipeline GitLab API pattern from `.deploy-test-per-stands.yml` can play the dedicated manual job after Jenkins succeeds; the job's `needs` relation ensures artifacts are available before execution. Regression remains manual.

### Endpoint contract

Use one task-specific suffix instead of passing every endpoint or adding a machine-readable endpoint catalog. Hostnames generated by the current dev-deployment contract insert `-<deployId>` into the leftmost DNS label. The GitLab deploy job already receives `DEV_NAMESPACE=dev-<deployId>`, so the autotest job can derive:

```bash
TARGET_ENV_SUFFIX="${DEV_NAMESPACE#dev-}"
```

Changed 2026-09-29 (review comment on billing-tests !64): the value carries no leading dash;
the test code adds `-` itself (`DEV_HOST_SUFFIX`); no format validation in the tests (user
decision). Runs recorded
above before this date used the old form `-devops-832`.

For `DEV_NAMESPACE=dev-devops-689`, this produces `TARGET_ENV_SUFFIX=devops-689`. Tochka tests then construct their known component URLs:

```text
http://youdo-business-tochka-proxy-mock-webapp-${TARGET_ENV_SUFFIX}.dev.youdo.corp
http://youdo-business-tochka-proxy-mock-worker-${TARGET_ENV_SUFFIX}.dev.youdo.corp
https://b2bautomation-${TARGET_ENV_SUFFIX}.dev.youdo.sg
```

Keep two explicit compatibility modes during migration:

- `TARGET_HOST=test3`: existing Nomad URL construction;
- `TARGET_ENV_SUFFIX=devops-689`: Kubernetes dev-deployment URL construction.

When `TARGET_ENV_SUFFIX` is present, tests must use the Kubernetes form. When it is absent, they may fall back to the current Nomad form. If neither input is present, tests fail fast. Do not infer the mode from the content of a single overloaded variable.

The test project remains responsible for the stable base hostname, scheme, and zone of each component. This is simpler than a generic endpoint resolver and matches the existing ownership model. A JSON endpoint catalog should only be reconsidered if hostnames stop being deterministic or one component gains multiple candidate URLs that CI must choose between.

Known exceptions do not invalidate the suffix model but require one-time corrections in the affected test project: TKB old test names do not match the current Kubernetes component/host names, and worker endpoints still need a Service/Ingress before any suffix can make them reachable.

### Worker exposure

For the first Docker-runner pilot, enable a ClusterIP Service and an internal-only `.dev.youdo.corp` ingress for Tochka `mock-worker`. Do not publish worker trigger endpoints through public `.dev.youdo.sg`. Apply the same rule to TKB only when its suite is migrated.

If policy forbids even internal ingress for worker trigger endpoints, the alternative is to run the test image as a Kubernetes Job inside `DEV_NAMESPACE` and use ClusterIP DNS. That is safer but requires a new launcher, RBAC, transient secret handling, log streaming, artifact copying, and Job cleanup; it should be a separate second phase rather than a prerequisite for the Tochka pilot.

## Implementation sequence

1. **Prerequisites and contract tests**
   - Completed 2026-09-03: the approved `youdo.business` dev-deployment configuration was merged to `master` as `a4f80388`.
   - From the actual `docker` GitLab runner, verify DNS/TCP/HTTP access to task-specific `.dev.youdo.corp` and `.dev.youdo.sg` hosts.
   - Add tests for strict `DEV_NAMESPACE` validation and derivation of `TARGET_ENV_SUFFIX`, including empty, malformed, and maximum-length namespace values.

2. **Add the minimal Tochka Kubernetes target mode**
   - Add the `TARGET_ENV_SUFFIX` Kubernetes mode while retaining `TARGET_HOST` as the temporary Nomad fallback.
   - Construct the mock webapp, mock worker, and automation-web URLs from their stable base names plus the suffix while leaving all other test behaviour unchanged.
   - Leave tag selection, failure propagation, token handling, retry logic, and test content to the QA backlog; they do not block DevOps-832.
   - Publish the test feature branch as `devops-832-dev-autotests` and use that branch-specific image for the pilot; do not alter the legacy jobs' `latest` contract.

3. **Expose only required Kubernetes components**
   - Enable the Tochka `mock-worker` Service and add an internal task-specific ingress.
   - Verify webapp heartbeat, worker health/trigger endpoint, and automation-web health from the runner.
   - Confirm that no worker hostname is accepted by the public nginx route.

4. **Extend shared orchestration**
   - Derive `TARGET_ENV_SUFFIX` from the validated `DEV_NAMESPACE` in `v3/.deploy-dev.yml` or the reusable dev-autotest job; no Jenkins change or new endpoint artifact is required.
   - Add a reusable hidden dev-autotest job in `gitlab-ci-templates`; keep the static Nomad matrix separate during migration.
   - Add the dedicated smoke/regress jobs, namespace ownership verification, shared resource group, endpoint preflight, and automatic smoke play after successful deploy.

5. **Tochka pilot**
   - Deploy Tochka as main from an MR with a task ID.
   - Confirm the suffix is derived from the same namespace/build that produced the dotenv artifact and that all three constructed URLs resolve to that task environment.
   - Run smoke, inspect JUnit/Allure and application logs, then delete the namespace.
   - Repeat once with the same task namespace to verify upgrade isolation and stale-pipeline protection.
   - Keep `allow_failure: true`; deciding when the suite is trustworthy enough to become an MR gate is a separate QA-owned task.

6. **Rollout to other services**
   - Billing first (single existing webapp ingress): infrastructure rollout completed and runtime-proven in pipeline `137992`; 512Mi/1Gi eliminated the OOM/502 failure pattern. Two masked balance-history assertions remain for QA.
   - TKB second: initial deploy, automatic smoke, manual regression, worker exposure, and endpoint mapping are runtime-proven. The local branch now raises both mock-api and worker-mock memory; publish and runtime-check it, diagnose the two repeated incoming-payment failures, then verify repeat-deploy and cleanup.
   - Main `youdo-business` suite after decomposing its many explicit endpoints.

Sber is not a later rollout phase: the operator marked the service and its tests non-current on 2026-09-04.

## Acceptance criteria

- Starting `1 deploy dev` for a Tochka MR deploys the task-specific namespace and starts exactly one dev smoke job against that Jenkins build.
- The job does not contain or derive old Nomad domains.
- `TARGET_ENV_SUFFIX` is deterministically derived from the verified `DEV_NAMESPACE`; Tochka constructs the expected mock webapp, mock worker, and automation-web URLs and they pass preflight before tests.
- Existing Nomad jobs continue to work through `TARGET_HOST` until their explicit removal.
- The pilot preserves current QA-owned test-selection, exit-code, credential, retry, and reporting semantics and remains `allow_failure: true`.
- Deploy, repeat deploy, tests, and delete cannot race for the same namespace.
- A stale pipeline cannot test or delete a namespace owned by a newer Jenkins build.
- Worker trigger endpoints are not publicly routable.

## Related repositories

- `/home/slnnk/git/gitlab-ci-templates`
- `/home/slnnk/git/jenkins-pipelines`
- `/home/slnnk/git/helm-charts`
- `/home/slnnk/git/youdo-business-tochka-proxy`
- `/home/slnnk/git/youdo-business-tochka-proxy-tests`
- `/home/slnnk/git/youdo.business`
- `/home/slnnk/git/youdo-business-billing-service-tests`
- `/home/slnnk/git/youdo-business-tkb-tests`

## Related log entries

Newest first, all under `~/ai/current/knowledge/log/`:

- `2026-09-07-dev-deployment-tkb-pipeline-138093.md`
- `2026-09-07-dev-deployment-tkb-autotests-preparation.md`
- `2026-09-04-dev-deployment-devops-832-handoff.md`
- `2026-09-04-dev-deployment-devops-832-billing-autotests-prepared.md`
- `2026-09-04-dev-deployment-jenkins-pod-race.md`
- `2026-09-03-dev-deployment-devops-832-tochka-dev-autotests-prepared.md`
- `2026-09-03-dev-deployment-devops-832-tochka-dev-autotests.md` (plan)
- `2026-09-03-dev-deployment-devops-832-mock-worker-probe-failure.md`
