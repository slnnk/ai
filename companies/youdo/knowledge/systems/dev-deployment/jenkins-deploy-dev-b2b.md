---
system: dev-deployment
status: verified
checked: 2026-08-31
tags: [jenkins, jenkins-pipelines, deploy-dev-b2b, active-choices, helm, ephemeral-namespace]
---
# B2B ephemeral development deploy pipeline (Jenkins)

> Historical/component note. The authoritative cross-system status and rollout plan is `~/ai/current/knowledge/systems/dev-deployment/overview.md`. Where this file conflicts with it, use the central document.

Last verified: 2026-08-31.

## Purpose and location

- Repository: `/home/slnnk/git/jenkins-pipelines`.
- Safe origin: `git@gitlab.youdo.sg:sysadmins/devops-tools/jenkins-pipelines.git`.
- Pipeline: `pipelines/deploy-dev-b2b.Jenkinsfile`.
- Service catalog and GitLab project IDs: `config/deploy-dev-b2b.groovy`.
- GitLab CI entry point: `/home/slnnk/git/gitlab-ci-templates/v3/.deploy-dev.yml`; the manual `deploy dev` job submits `SERVICE` and `VERSIONS` to Jenkins `buildWithParameters`.
- Jenkins job setup is documented in the repository `README.md`; lightweight checkout must be disabled because the pipeline loads the Groovy config during initialization.

## Execution path

Jenkins job -> Active Choices parameters -> GitLab API -> ephemeral Kubernetes namespace `dev-<BUILD_NUMBER>` -> Helm chart checkout -> service deployment.

- GitLab API base URL is stored in the Groovy config.
- `GITLAB_ACTIVE_CHOICES_TOKEN` comes from Jenkins global environment; the secret value is not stored here.
- Helm charts: `git@gitlab.youdo.sg:sysadmins/helm-charts.git`, branch `master`.
- Kubernetes credential ID: `kubeconfig-dev`.
- Namespace Helm chart: `helm-charts/ephemeral-namespace`.
- Service chart: `helm-charts/microservice`.
- Service images: `nexus.youdo.com/<gitlab-project-path>:<derived-pipeline-tag>`.
- Generated routing overlays are archived from `generated/<service>-routing.yml`.

## Ingress URL report published and runtime-proven on 2026-08-31

- Published `jenkins-pipelines/master` commit `8ae44be0` collects live Ingress objects after all parallel service rollouts complete.
- Mapping uses the chart labels `app.kubernetes.io/instance` and `app.kubernetes.io/component`, not name parsing. It includes RabbitMQ plus every catalog service component that owns an ingress and supports multiple hosts per component.
- URL scheme follows the operator-facing DNS contract: every `*.dev.youdo.sg` host is rendered with `https://`; every other ingress host is rendered with `http://`, independent of the Kubernetes `spec.tls` section.
- The deterministic `service / component / URL` report is printed to the Jenkins console, archived as `generated/ingress-urls.txt`, and rendered as clickable links in the Jenkins build description. The former standalone RabbitMQ description link is replaced by this complete table; the early RabbitMQ console line remains.
- A unit test covers RabbitMQ, multiple services, multiple hosts, hostname-based scheme selection, ordering, unrelated-ingress filtering, text output, and HTML links. Groovy 3 test and `git diff --check` pass. Jenkins build `147` completed with `SUCCESS`, archived `generated/ingress-urls.txt`, printed the report, and exposed 26 clickable links in its build description. The artifact contains 26 URLs: all seven `*.dev.youdo.sg` entries use HTTPS and the other 19 use HTTP.

## Full-catalog activation prepared on 2026-08-30

- Published `jenkins-pipelines/master` commit `10ef2517` removes `deployment.scope` and `deployment.allowed_services` from both the config and Jenkinsfile; Jenkins build 140 loaded this revision.
- The ordered `services` catalog is now the only source of active services. All 13 entries can be primary; the effective set is always the selected primary followed by the other 12 catalog entries.
- A fresh namespace installs all missing releases. A repeat deploy keeps the established invariant: the primary is upgraded, while existing non-primary releases are preserved.
- Active Choices shows version selectors for the full catalog; non-primary services default to `master`, so an open MR must be selected explicitly for any branch-only `dev.yml`.
- TDD evidence: the revised test first failed because the old three-argument `getOrderedDeploymentServices(scope, allowed, primary)` API remained. A review then identified missing fresh/repeat path coverage; the next RED failed on absent production helpers. Final tests use the same helpers as Jenkins for all 13 `SERVICE` choices, every primary-first order, fresh deploy of all 13, repeat primary-only selection, and recovery of a missing non-primary release. The suite passes against the real Jenkinsfile and config using the local Groovy runtime.
- Repository README documents full-catalog fresh/repeat behavior. The first runtime trigger reached Jenkins build 140 but failed before namespace creation because GitLab sent dotted project name `youdo.business` instead of canonical Jenkins service name `youdo-business`; details are in `~/ai/current/knowledge/log/2026-08-30-dev-deployment-deploy-job-3100457-service-name.md`.
- The optional hidden `GITLAB_PROJECT_ID` contract is published and runtime-proven by Jenkins build 142: project `423` resolved `youdo.business` to canonical catalog service `youdo-business`, and all 13 services were selected.
- Build 142 then exposed a chart-level blocker: migration Job names for billing, Tochka proxy, and auth service were 66, 68, and 64 characters. Kubernetes rejected the corresponding pod-template Job labels, whose value limit is 63. Ten releases deployed, while those three atomic installs failed. Details and partial namespace state are recorded in `~/ai/current/knowledge/log/2026-08-30-dev-deployment-jenkins-test-142-migration-job-name-length.md`.

## Parameter behavior changed on 2026-08-18

Task: simplify service/version selection in the B2B deployment form.

- Removed the `INCLUDE_DEPENDENCIES` checkbox and its expansion logic.
- `SERVICE` is now an Active Choices `PT_SINGLE_SELECT` dropdown with an empty default value. It identifies one main service.
- `VERSIONS` remains hidden/empty until a main service is selected, then renders a version selector for every service currently enabled in `deployment.allowed_services`.
- The selected main service is rendered first and marked `main`; all enabled services are deployed in that same ordering, while non-main services default to `master`.
- A build without a main service fails before namespace creation.
- The Jenkins runner skill examples were updated to stop passing `INCLUDE_DEPENDENCIES` and use the singular `SERVICE` parameter.
- Active Choices scripts must be approved in Jenkins In-process Script Approval after registration or modification. Without approval, the service list may be empty and `VERSIONS` renders its fallback error.

## Verification

- `git diff --check` passed.
- Static checks confirmed one `PT_SINGLE_SELECT` parameter and no remaining `INCLUDE_DEPENDENCIES` or `PT_CHECKBOX` references in the pipeline/runner documentation.
- No local Groovy executable or Jenkins test harness was available, so the form still needs a Jenkins-side smoke test after deployment.

## Operational checks and next steps

1. Update/reload the Jenkins job from SCM and open **Build with Parameters**.
2. Confirm `SERVICE` starts blank and permits only one selection.
3. Confirm no service version selectors are present before selection.
4. Select a service and confirm selectors appear for all enabled entries, with the selected service first.
5. Run a smoke deployment and inspect the console log, build description, archived routing overlays, namespace resources, Helm releases, and pod rollout status.

Risk: the form queries open merge requests for every enabled GitLab project after selection, so parameter rendering scales with `deployment.allowed_services`.

## Two-service rollout prepared on 2026-08-27

- User confirmed that `docvalidation` and `fns` must form the complete current deployment set: either can be main, and the other is a dependent service on `master` by default.
- `fns` was already present in the full Jenkins catalog with GitLab project ID `244`; its `devops/dev.yml` was reported merged before this change.
- Local uncommitted changes on `/home/slnnk/git/jenkins-pipelines` `master` set `deployment.scope=all` and `deployment.allowed_services=[docvalidation, fns]`.
- Multi-service ordering in both Active Choices and runtime is now constrained to `allowed_services`, not all 13 catalog entries. Main is first, so the expected sets are `[docvalidation, fns]` or `[fns, docvalidation]`.
- Added `tests/deploy_dev_b2b_test.groovy`. TDD RED failed on the missing deployment-set function; GREEN passed after the implementation. The test parses the real Jenkinsfile with the local Groovy 3 runtime and checks both main-service orders plus the real config.
- Updated repository `README.md` to document that `allowed_services` controls both the main-service choices and the enabled multi-service set.
- No commit, push, Jenkins job reload, or runtime deployment has been performed. After publication, reload the Jenkins job, approve modified Active Choices scripts if requested, verify exactly two `SERVICE` choices and two `VERSIONS` selectors, then run fresh/repeat/lifecycle smoke tests with each service as main. Update the YouTrack article after the runtime result; its current text still describes `scope=single` and the docvalidation-only pilot.

### First two-service runtime smoke: GitLab job 3095877 / Jenkins build 137

- The Jenkins changes were subsequently published as `jenkins-pipelines` master commit `56691cc6f811abac6abb063eb16d97531bd85e0a` (`add fns`). GitLab job `3095877` (`1 deploy dev`) in docvalidation pipeline `137264` ran on 2026-08-27 and succeeded in 169.8 seconds; it queued Jenkins item `18288`, monitored `test/137`, received `SUCCESS`, and uploaded the dotenv artifact.
- Input was `SERVICE=docvalidation`, `VERSIONS=docvalidation|223|mr|133|`. Jenkins reported `scope=all`, allowed services `docvalidation, fns`, and effective set `docvalidation, fns`.
- Docvalidation used MR 133/ref `DevOps-689-k8s`, image tag `devops-689-k8s-137264`. Fns defaulted to `master`, GitLab pipeline `137459`/IID `595`, commit `3d5fd9774fc04d94902780346952436dbe133b2a`, image tag `master-595`; the source pipeline was successful.
- Fresh namespace `dev-devops-689` was created for Jenkins build 137 with GitLab job/pipeline annotations, TTL `7d`, and refreshed timestamp `2026-08-27T18:31:04Z`. Helm releases `dev-devops-689` in `default`, `docvalidation-devops-689`, and `fns-devops-689` were all revision 1 and `deployed`.
- Both services installed their PostgreSQL StatefulSets and completed pre/post migration Jobs. Docvalidation API/service/scheduler and fns API/service/scheduler were Ready with zero restarts; RabbitMQ and Redis were Ready; the namespace had no Warning events. Both `http://docvalidation-devops-689.dev.youdo.corp/hc` and `http://fns-devops-689.dev.youdo.corp/hc` returned HTTP 200 `Healthy`.
- Jenkins archived both routing overlays. Fns live ConfigMap `fns-devops-689-env` set `DocValidationClient__BaseAddress=http://docvalidation-devops-689.dev.youdo.corp/api/v1`, confirming ephemeral dependency routing rather than the stable fallback. Docvalidation retained its stable Cerberus and YouDo API endpoints.
- Read-only cluster checks used `/home/slnnk/.kube/config-yandex-dev`. The file is mode `664`, so Helm warns that it is group/world readable; reduce access to `600`. Local kubectl is `1.29.3` against server `1.34.1`, outside the supported +/-1 minor-version skew; Jenkins itself used the matching `kubectl:1.34.0` lifecycle image, so these warnings did not affect job 3095877.
- GitLab environment `dev/devops-689-k8s` is currently `available`. Next multi-service checks: repeat deploy and confirm the main docvalidation release advances while existing fns Helm revision/pod UIDs remain unchanged; then extend/delete lifecycle verification. A separate run with `fns` as main is still pending.

### Two-service repeat deploy: GitLab job 3095884 / Jenkins build 138

- A new docvalidation MR pipeline `137462` at commit `53688d98166e1ac825ea0a65d3ee2b68aaa76fba` (`change templates branch`) ran `1 deploy dev` as job `3095884` on 2026-08-27. The GitLab job succeeded in 94.6 seconds and Jenkins `test/138` succeeded in 76.2 seconds.
- The stable namespace remained `dev-devops-689`; its creation timestamp stayed `2026-08-27T18:31:06Z`. Ownership/audit metadata moved from build 137/job 3095877/pipeline 137264 to build 138/job 3095884/pipeline 137462, and TTL refreshed to `7d` at `2026-08-27T18:45:20Z`.
- Jenkins detected the existing dependent release and logged `Keep existing dependent service fns: release fns-devops-689 will not be upgraded`; `Services selected for this deploy` contained only `docvalidation`.
- Namespace release and main docvalidation release advanced from revision 1 to revision 2. Docvalidation moved to image tag `devops-689-k8s-137462`, reran both migration hooks successfully, and received new application/PostgreSQL pod identities.
- Fns remained revision 1 with its original deploy timestamp `2026-08-27 21:31:42 +03:00`, image tag `master-595`, and unchanged pod identities from the first deploy: API `fns-devops-689-api-6c5c86fccb-f5h9s`, scheduler `fns-devops-689-scheduler-5c4d4b5b54-69g4d`, service `fns-devops-689-service-6856ccc468-2lcfh`, and PostgreSQL `fns-devops-689-postgres-0`; all retained their original creation timestamps and had zero restarts.
- RabbitMQ and Redis identities also remained unchanged. Both PostgreSQL PVCs stayed Bound with their original `2026-08-27T18:31:43Z` creation timestamps; docvalidation reused PVC UID `d816c332-df8c-4140-a258-7408d178f342`, and fns retained PVC UID `2af02c6d-9e41-4966-80f7-0548442795ea`.
- All deployments/StatefulSets were Ready, no Warning events existed, and both service `/hc` endpoints returned HTTP 200 `Healthy`. Fns live routing still pointed to `http://docvalidation-devops-689.dev.youdo.corp/api/v1`.
- The main multi-service repeat-deploy invariant is verified. Remaining runtime checks are extend/delete lifecycle on the current build 138 metadata and a separate deployment with `fns` as main.

### Two-service lifecycle extend: GitLab job 3095885

- GitLab job `3095885` (`2 extend dev`) from pipeline `137462` ran on 2026-08-27 and succeeded in 3.1 seconds using the unified `kubectl:1.34.0` image. Its dotenv metadata referred to namespace `dev-devops-689` and Jenkins build 138, so the ownership/stale-build verification passed.
- The job annotated the existing namespace without recreating workloads. Namespace label `jenkinsJobId=138` and Jenkins/GitLab deployment audit URLs remained tied to deploy job `3095884`/build 138.
- Kubernetes lifecycle metadata changed from TTL `7d` to `5d`; `k8s-ttl-controller.twin.sh/refreshed-at` became `2026-08-27T18:50:05Z`.
- GitLab Environment `442` (`dev/devops-689-k8s`) remained `available` and its `auto_stop_at` moved to `2026-09-01T21:50:06.050+03:00`, exactly five days after the extend job.
- All docvalidation/fns deployments and PostgreSQL StatefulSets remained Ready, no Warning events existed, and both service `/hc` endpoints returned HTTP 200 `Healthy` after extension.
- Extend behavior for the two-service build is verified. Remaining lifecycle check is `3 delete dev` from the same pipeline/build metadata, followed by confirmation that namespace, all three Helm releases/secrets, PVC/PV, and GitLab environment state are cleaned up. A separate deployment with `fns` as main is still pending.

### Two-service lifecycle delete: GitLab job 3095886

- GitLab job `3095886` (`3 delete dev`) from pipeline `137462` ran on 2026-08-27 and succeeded in 76.5 seconds using the unified `kubectl:1.34.0` image. Its ownership check accepted namespace `dev-devops-689` for Jenkins build 138.
- The trace showed namespace-chart release `dev-devops-689` uninstalled, namespace deletion requested, Kubernetes delete condition met, and the explicit terminal message `Namespace dev-devops-689 is fully deleted`.
- Post-checks confirmed namespace `dev-devops-689` is NotFound; Helm releases `dev-devops-689`, `docvalidation-devops-689`, and `fns-devops-689` are absent; no matching Helm release secrets remain in any namespace.
- Both previously Bound volumes (`pvc-d816c332-df8c-4140-a258-7408d178f342` for docvalidation and `pvc-2af02c6d-9e41-4966-80f7-0548442795ea` for fns) are absent, and no PV retains a claimRef to `dev-devops-689`.
- GitLab Environment `442` (`dev/devops-689-k8s`) moved to `stopped` at `2026-08-27T21:53:25.382+03:00` with `auto_stop_at=null`.
- The complete docvalidation-main two-service lifecycle is verified: fresh deploy, repeat deploy preserving fns, extend, and delete. The remaining rollout check is a separate deployment with `fns` as main, followed by its lifecycle cleanup. The YouTrack Dev deployment article should be updated after that final direction check or now with the verified docvalidation-main results plus an explicit pending fns-main item.

## Docvalidation single-service pilot and kubeconfig update (2026-08-25)

- Jenkins `master` commit `936de243594ce28b93cb14835897b903805f4b89` restricts the pilot to `docvalidation` with deployment scope `single`.
- Build 117 confirmed the guards: `SERVICE=docvalidation`, `VERSIONS=docvalidation|223|mr|133|`, and `services to deploy: docvalidation`. It selected GitLab pipeline 134202.
- Build 117 failed before namespace creation because the then-current `kubeconfig-dev` targeted unreachable Kubernetes API `https://10.16.26.68` and Helm received an I/O timeout.
- Jenkins system/global secret-file credential `kubeconfig-dev` was updated through the credentials `config.xml` API from the user-provided `/tmp/k8sdev`. The credential value is not stored in notes.
- The new credential targets `https://10.16.26.3`. Direct validation showed Kubernetes server 1.34.1 and permission to create/delete namespaces. A Jenkins-side size and SHA-256 comparison confirmed that the stored credential exactly matches the provided file.
- Next check: rerun the same Jenkins selection and verify the ephemeral namespace stage reaches the new API endpoint, then continue with Helm/Vault/RabbitMQ and docvalidation rollout diagnostics.

### Jenkins build 118 result

- Build 118 reached the new Kubernetes API successfully and again deployed only `docvalidation`. Namespace `dev-118` was created with the expected Jenkins/dev/TTL metadata; registry and RabbitMQ Vault secrets synchronized; RabbitMQ and Redis became Ready.
- Jenkins selected docvalidation MR 133 / GitLab pipeline 134202, repository commit `044f867d8813d6ed7e5e310e481e48d311d7d59f`, and image tag `devops-689-k8s-134202`. The archived routing overlay correctly kept Cerberus and youdo-business on their stable dev endpoints.
- The docvalidation Helm install failed after its ten-minute timeout. PostgreSQL 16 could not initialize because the dynamically provisioned filesystem contains `lost+found` at the PVC mount root `/var/lib/postgresql/data`.
- Root cause is in `/home/slnnk/git/helm-charts/microservice/templates/postgres-deployment.yaml`, introduced by Helm `master` commit `84288a7`: the StatefulSet mounts the PVC directly at PostgreSQL's default `PGDATA`. On 2026-08-25 the local clean `master` worktree was updated to set `PGDATA=/var/lib/postgresql/data/pgdata`; this change is not yet committed or pushed. Default and docvalidation-specific `helm lint`, `helm template`, rendered YAML parsing, and `git diff --check` passed.
- `helm upgrade --atomic` removed the `docvalidation-118` release but pre-install hook resources survived: the PostgreSQL StatefulSet/pod/service, pre-migration Job/pod, and bound 5 Gi PVC remained. The separate namespace release `ns-dev-118` also remained with running RabbitMQ and Redis. After verifying `createdBy=jenkins`, `environment=dev`, and `jenkinsJobId=118`, Helm release `ns-dev-118` was uninstalled; namespace `dev-118` and its resources/PVC were confirmed absent.

### Jenkins build 119 result

- Build 119 completed successfully in 6m15s and deployed only `docvalidation` into `dev-119` from the same MR/pipeline and image tag `devops-689-k8s-134202`.
- Helm releases `ns-dev-119` and `docvalidation-119` are deployed. PostgreSQL StatefulSet is Ready with `PGDATA=/var/lib/postgresql/data/pgdata` and a bound 5 Gi `yc-network-hdd` PVC; pre- and post-migration Jobs completed with exit code 0.
- API, scheduler, service, PostgreSQL, RabbitMQ, and Redis are Ready with zero restarts at verification time. `http://docvalidation-119.dev.youdo.corp/hc` returned HTTP 200 `Healthy` through Traefik at `10.16.26.101`.
- The routing artifact uses stable dev endpoints for Cerberus and youdo-business, as expected for single-service deployment.
- Observed transient warning: the pre-migration pod initially received Nexus `NotFound`/`ImagePullBackOff` for the migrations image, then successfully pulled the exact same tag about 90 seconds later and completed. RabbitMQ/Redis also had one initial service-account ConfigMap cache mount timeout and recovered. These did not affect the final result but should be watched in later runs.
- Namespace `dev-119` remains active for lifecycle testing (`extend dev` and `delete dev`).

## Portable lessons

- `~/ai/general/knowledge/k8s/postgres-pvc-lost-and-found-pgdata.md` (build 118 PostgreSQL init failure).
- `~/ai/general/knowledge/helm/atomic-install-failure-leaves-hook-resources.md` (build 118 leftover hook resources).
