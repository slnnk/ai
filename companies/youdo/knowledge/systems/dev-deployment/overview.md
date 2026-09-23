---
system: dev-deployment
status: verified
checked: 2026-09-07
tags: [b2b, ephemeral-dev, jenkins, gitlab-ci, helm, kubernetes, yandex-dev, roadmap]
---
# B2B dev deployment: authoritative system map and roadmap

Last verified: 2026-09-07  
YouTrack: [DevOps-A-50](https://youtrack.youdo.com/youtrack/articles/DevOps-A-50/Dev-deployment)

Post-deploy autotest status and migration plan: `~/ai/current/knowledge/systems/dev-deployment/post-deploy-autotests.md`. The Tochka Kubernetes pilot is runtime-proven. Jenkins old-ReplicaSet handling and both dependency memory changes are merged to `master`; their runtime verification is intentionally deferred to the next service onboarded to post-deploy autotests. The rollout strategy is to prepare autotest support across all selected projects on feature branches first, then merge the coordinated set together. QA-owned tag selection, failure propagation, credential fallback, and retry behavior remain intentionally outside the pilot.

TKB post-deploy autotest support is runtime-proven for an initial deployment. Pipeline `138093` at service commit `6b24286` used Jenkins build `159`, created `dev-devops-832`, deployed TKB as primary with all catalog dependencies, and automatically started smoke job `3120789`; regression job `3120790` was also run manually. The new `mock-webapp`, `worker-mock`, and `b2bautomation` task endpoints all return HTTP 200, both TKB pods are Ready with zero restarts, and Kubernetes has no Warning events. Both suites executed 183 Gradle tests with the same two failures; GitLab imported 174 cases with 172 passed and 2 failed. Failures are masked by `ignoreFailures=true`/`allow_failure` and are tied to incoming-payment status/data behavior rather than endpoint connectivity. TKB `mock-api` sampled at 256388Ki and `worker-mock` at 180880Ki against 256Mi limits. Commit `aa4d083` raises both workloads to 512Mi request / 1Gi limit; MR pipeline `138096` built and tested it successfully and is waiting for manual deploy job `3120801`. Runtime resource verification, repeat-deploy, and cleanup evidence remain pending.

This is the authoritative local knowledge source for the B2B ephemeral development deployment system. Narrower notes (`gitlab-ci-deploy-dev.md`, `jenkins-deploy-dev-b2b.md`, and `helm-charts.md` in this directory, plus the helm-charts log entries under `~/ai/current/knowledge/log/`) are implementation history and should not be used to determine current rollout status without checking this file.

## Purpose

Deploy a B2B service under development, together with its catalog dependencies, into an ephemeral task-specific Kubernetes namespace in the Yandex dev cluster, driven from a GitLab merge-request pipeline through a Jenkins job and shared Helm charts, and run the service's existing autotests against that environment.

## Current status

- On 2026-09-07 TKB pipeline `138093` / deploy job `3120707` / Jenkins build `159` runtime-proved the initial TKB post-deploy path. Automatic smoke `3120789` and manual regression `3120790` reached all three task endpoints and published reports. Each ran 183 tests with two identical incoming-payment failures; GitLab imported 174 with 172 passed and 2 failed. Infrastructure is healthy, but `mock-api` reached roughly 97.8% and `worker-mock` roughly 69% of their 256Mi limits. Published commit `aa4d083` raises both to 512Mi request / 1Gi limit; pipeline `138096` is waiting for manual deploy `3120801`. See `~/ai/current/knowledge/log/2026-09-07-dev-deployment-tkb-pipeline-138093.md`.
- On 2026-09-04 Billing pipeline `137991` / service commit `1b6ed25` runtime-proved the second post-deploy autotest integration. Deploy job `3114239` triggered Jenkins build `155`, which loaded `jenkins-pipelines/master` commit `20b9d78`, created fresh namespace `dev-devops-832`, deployed Billing as primary plus the 12 catalog dependencies, and automatically started `smoke tests` job `3114321`. The job used test image `youdo-business-billing-service-tests:devops-832-dev-autotests`, derived `TARGET_ENV_SUFFIX=-devops-832`, reached the task-specific Billing ingress, and published Allure/JUnit. GitLab reports 545 cases: 542 passed and 3 failed; the job and pipeline are green only because the existing QA suite uses `ignoreFailures=true` and the CI job is allowed to fail. The failures are test/data/application-level, not deployment connectivity failures. `regression tests` job `3114322` remains manual.
- Billing regression job `3114322` was started manually and exposed a confirmed infrastructure resource failure. The Billing webapp hit its 256Mi limit and was `OOMKilled` at 19:29:14 MSK (exit 137, one restart); Traefik consequently returned 502 for the remaining test requests. Gradle recorded 553 tests with 540 failures; GitLab imported 545 with 532 failures and 13 passes. Every imported failure was an expected 200/400 versus actual 502 mismatch. The job remained green because of `ignoreFailures=true`. Raise Billing webapp memory, initially to 512Mi request / 1Gi limit, redeploy, and rerun regression before accepting Billing runtime stability.
- The attempted repeat deployment in pipeline `137992`, GitLab job `3114330`, failed in Jenkins build `156` before the Billing Helm upgrade. Build 156 was scheduled on Jenkins node `Jenkins` (`/data/jenkins/workspace/test`), while successful build 155 ran on `AutoTest`. The Jenkinsfile calls `python3` plus PyYAML in `writeServiceRoutingOverlay`; node `Jenkins` has no `python3`, so the main-service parallel branch exited 127 while reading `devops/dev.yml`. The namespace chart reached revision 2 and existing dependencies were preserved, but Billing application release remained revision 1 on pipeline-137991 image and 256Mi/256Mi. This is a Jenkins agent toolset/label portability defect, not the old-ReplicaSet race. Remove the undeclared Python dependency or make the eligible-node tool contract uniform before retrying.
- At operator request, `jenkins-pipelines/master` commit `ae1a125` (`fix node`) pins the pipeline to `node('AutoTest')`; README and the Groovy source-contract test were updated, and tests pass. On 2026-09-04 the agent host `jenkins-agent-test-01` (`10.16.26.23`) was cleaned safely: the unused previous Jenkins-agent Docker image was removed and systemd journal was vacuumed to 200MiB. Root free space increased from 1.1GiB (89% used) to 2.1GiB (78% used); the active agent image/container were not touched. Jenkins retained its stale disk-monitor block, so it was explicitly toggled online after cleanup. API verification then reported `offline=false`, `temporarilyOffline=false`, five executors.
- Pipeline `137992` was successfully recovered on 2026-09-04. Retried deploy job `3114414` triggered Jenkins build `158`, which checked out `jenkins-pipelines` commit `ae1a125`, ran on `AutoTest`, completed the Python/PyYAML routing step, and upgraded only Billing to Helm revision 2. The live Billing webapp is Ready on image `devops-832-dev-autotests-137992`, with 512Mi request / 1Gi limit and zero restarts. Smoke job `3114412` and regression job `3114413` each imported 545 cases: 543 passed and 2 failed. Both failures are the same `GetYouDoBalanceHistoryTest.getYouDoBalanceHistoryWithIncorrectPeriod` assertion (`expected not 0.0, was 0.0`); there are no mass 502 failures or new OOM evidence. The jobs remain green because test failures are ignored/allowed.
- Build 155 also proved that the merged dependency resource declarations are consumed: doc-generator API and automation-web both run at 512Mi request / 1Gi limit with zero restarts/OOM. This Billing suite does not load those endpoints, so it proves rollout/configuration but not their load sufficiency.
- On 2026-09-04 Tochka pipeline `137961` proved the post-deploy autotest chain end-to-end. Successful retry job `3112466` triggered Jenkins build 153, deployed the task environment, and automatically played `smoke tests` job `3112464`. The job validated namespace ownership, used `TARGET_ENV_SUFFIX=-devops-832`, published Allure/JUnit, and reported 603 cases: 587 passed, 16 skipped, no failures/errors. `regression tests` job `3112465` remains manual. Tochka's four workloads ran with 512Mi requests / 1Gi limits and zero restarts/OOM.
- The first attempt in the same pipeline, GitLab job `3112382` / Jenkins build 152, exposed a Jenkins readiness race: after current Deployments rolled out, the extra all-pod phase check failed on an old ReplicaSet pod briefly in `Error` while being deleted. `jenkins-pipelines/master` commit `20b9d78` retries the check six times at five-second intervals, ignores deletion-marked old pods and Job pods, and still fails for persistent non-Running active pods. Runtime verification completed in Billing Jenkins build `158`: an old ReplicaSet pod was `Terminating`, the check ignored it correctly, and the build succeeded.
- Memory changes were merged on 2026-09-04 after the first smoke/regression run. Doc-generator MR 34 merged commit `e9d86aa` through merge commit `bdee550d` and sets API to 512Mi request / 1Gi limit. `youdo.business` MR 3738 merged commit `a41e0a0` through merge commit `b7d1df43` and sets automation-web to 512Mi request / 1Gi limit. At the 18:36 MSK read-only check, the existing `dev-devops-832` namespace had not consumed either commit: doc-generator remained 256Mi/256Mi with three restarts and retained `OOMKilled`, while automation-web remained on the live patch 896Mi/1280Mi with zero restarts. By operator decision, the merged values and Jenkins race fix will be runtime-checked during the next service autotest onboarding rather than through another immediate Tochka run.
- A fresh full-catalog deployment is now runtime-proven. GitLab job `3100718` / pipeline `137654` triggered Jenkins build `145`; all 13 Helm releases deployed successfully in `dev-devops-689`, all migrations completed, every workload was Ready with zero restarts, and no Warning events existed at the post-build check.
- On 2026-08-31 the operator reported successful manual verification of full-catalog repeat isolation, extend/delete cleanup, `fns` as primary, rejection of primary `master`, and no-task-ID fallback naming/cleanup. No additional job/build identifiers were supplied, so these are recorded as operator-verified rather than independently trace-correlated evidence.
- Jenkins `master` commit `56691cc6` contains the two-service configuration:

  ```groovy
  deployment: [scope: 'all', allowed_services: ['docvalidation', 'fns']]
  ```

- The full `docvalidation`-primary lifecycle was verified with `fns` as the dependent service: initial deploy, repeat deploy, extend, and delete.
- On repeat deploy, `docvalidation` was upgraded while the existing `fns` Helm revision and pods remained unchanged.
- The namespace, application releases, PVC, and PV were removed by the delete job. There were no `dev-*` namespaces left after cleanup.
- Nine service repositories now have both `devops/dev.yml` and the shared `v3/.deploy-dev.yml` include in `master`: `docvalidation`, `fns`, `youdo-notifications`, `youdo-sms-service`, `youdo-business-landings`, `youdo-business-billing-service`, `youdo-business-mobile-id`, `youdo-business-tkb-proxy`, and `youdo-business-tochka-proxy`.
- All nine master values contain no stale `.dev.youdo.local` endpoints and pass fresh `helm lint` plus `helm template` against the current `helm-charts/master`.
- Jenkins `master` commit `10ef2517` removes the pilot `scope`/`allowed_services` model and activates all 13 catalog entries. Build `145` proves the initial full catalog; repeat and lifecycle semantics were subsequently confirmed manually by the operator.
- The first `youdo-business` trigger exposed a service-name boundary defect: GitLab job `3100457` passed `CI_PROJECT_NAME=youdo.business`, while Jenkins expects canonical name `youdo-business`. Jenkins build `140` rejected it before namespace creation. The same mismatch affects `youdo.business.landings`, `youdo.kitcut`, and `youdo.notifications`; see `~/ai/current/knowledge/log/2026-08-30-dev-deployment-deploy-job-3100457-service-name.md`.
- The GitLab bridge now sends `GITLAB_PROJECT_ID`, and Jenkins resolves it through the catalog to the canonical service name. Jenkins build `142` provided runtime proof with `423: youdo.business -> youdo-business`.
- Build `142` failed later because three migration Job names exceeded the Kubernetes 63-character label-value limit: billing service (66), Tochka proxy mock migration (68), and auth service post-migration (64). Ten other releases deployed. See `~/ai/current/knowledge/log/2026-08-30-dev-deployment-jenkins-test-142-migration-job-name-length.md`.
- The migration hook correction is published in `helm-charts/master` commit `4ab8743`; hooks render as `-mpre`, `-mpost`, `-mpre-mock`, and `-mpost-mock`. Jenkins build `145` proved the names at runtime for all catalog services, including the three releases blocked in build `142`.
- The partial build-142 namespace was cleaned and replaced by the successful build-145 environment. The earlier Hangfire distributed-lock error was transient; the repeatable worker failure was a `256Mi` OOM.
- `youdo.business` commit `83b2e24f` persists worker requests/limits at `512Mi`. Build `145` deployed that value; the worker was Ready with zero restarts at verification.
- Configured readiness endpoints on `.dev.youdo.corp` returned HTTP 200. Task-specific `.dev.youdo.sg` hosts continue to resolve to public `178.154.207.53`, but the public test nginx now routes the supported dynamic hostname patterns to dev Traefik `10.16.26.101:80`. The change is merged in `automation-services/master` as `ccd39521` (regexp commit `f18471ca`). On 2026-09-01 all seven generated hosts passed normal public HTTPS checks without forced DNS: TLS verification succeeded, no redirect occurred, and every public response matched direct Traefik. Readiness returned HTTP 200 on `/health` for the five general hosts and `/_/heartbeat` for both auth hosts.
- Ingress reporting is published and runtime-proven. `jenkins-pipelines/master` `8ae44be0` and `gitlab-ci-templates/master` `7ddb8813` were exercised by Jenkins build `147` / GitLab job `3103126`. Jenkins printed and archived all 26 RabbitMQ/service/component URLs and added 26 clickable build-description links; GitLab printed and retained the report and published all links in Environment `456` description via `CI_JOB_TOKEN`. All seven `*.dev.youdo.sg` URLs use HTTPS; the other 19 use HTTP.
- The YouTrack article was updated on 2026-08-28 with the same repository/runtime distinction and the paused-work continuation plan.
- `youdo-business-auth-service`, `youdo-business-doc-generator`, and `youdo-kitcut` are now present on `master` and were runtime-proven as dependencies in build `145`.
- `youdo.business` MR 3567 commit `83b2e24f` contains the current deployment configuration, including removal of stale `bot-web` configuration and the persisted `512Mi` worker limit; build `145` proved it as primary.
- On 2026-09-03 MR 3567 pipeline `137949` at commit `1d3ebc0c` completed successfully. Its `1 deploy dev` job `3111628` triggered Jenkins build `148`, which finished `SUCCESS` and refreshed environment `dev/devops-689-k8s`. The operator reported the fresh deployment as good; an independent public check immediately afterwards returned HTTP 200 from both `https://employee-devops-689.dev.youdo.sg/` and `/health`. This runtime-proves the `devops/dev.yml` environment correction introduced by commit `a067c985` (`Development` → `Staging`) and closes the employee-web HTTP 500 gap. MR 3567 was then merged to `master` as `a4f80388` at 2026-09-03 20:33 MSK. The pipeline's 117 deploy-test/autotest jobs remained manual and therefore do not constitute post-deploy autotest evidence.

## End-to-end delivery path

1. A service GitLab pipeline builds component images and publishes them to Nexus with a branch/pipeline-derived tag.
2. A user manually starts `1 deploy dev` in an MR pipeline.
3. The shared GitLab CI template calls the Jenkins deployment job and passes the service, MR/branch selector, project ID, pipeline/job URLs, and triggering-user audit fields.
4. Jenkins queries GitLab for the selected MR/branch and latest successful/relevant pipeline, derives the image tag, task-based namespace, stable Helm release names, and ordered deployment set.
5. Jenkins checks out `helm-charts/master` and the selected revisions of the service repositories.
6. The `ephemeral-namespace` chart creates the namespace and namespace-local infrastructure: Vault integration, registry secret synchronization, RabbitMQ, Redis, and RabbitMQ management ingress.
7. For every selected service, Jenkins loads `devops/dev.yml`, generates a routing overlay, and applies the `microservice` chart.
8. Jenkins waits for namespace infrastructure, Vault-backed secrets, migration hooks, deployments, and pods, then archives generated routing and `generated/deploy-dev.env`.
9. GitLab imports the Jenkins dotenv artifact and creates the GitLab Environment used by `2 extend dev` and `3 delete dev`.
10. Cleanup is performed by the GitLab environment `on_stop`/delete job. Kubernetes TTL annotations are currently metadata only because no TTL controller is installed.

## Naming and lifecycle contract

- Task IDs are extracted case-insensitively from the MR title or branch: `Site-123`, `DevOps-321`, or `AP-435`.
- A task such as `DevOps-689` maps to namespace `dev-devops-689`.
- If no task ID exists, a DNS-safe source-branch slug is used, limited to 63 characters.
- The namespace and release names stay stable across pipelines of the same task, enabling Helm upgrade and PVC reuse.
- `master` is forbidden for the primary service and allowed as the default version for dependencies.
- The primary service is always upgraded. An already installed non-primary application release is skipped; a missing one is installed to recover a partial first deployment.
- GitLab lifecycle jobs validate `createdBy`, environment, and the Jenkins build number before extending or deleting a namespace. A stale pipeline cannot manage an environment refreshed by a newer Jenkins build.
- GitLab `resource_group` serializes one project/ref. Different refs can still derive the same task namespace; Jenkins currently has no lock on the final namespace.

## Routing model

`devops/dev.yml` contains stable fallback addresses and a `routing.env` contract. Jenkins produces a generated values overlay:

- `type: self` points to the current task-specific hostname;
- `type: dependency` points to an ephemeral hostname only when that target service is in the effective deployment set;
- otherwise the stable `*.dev.youdo.corp` endpoint remains in use.

Current explicit routing targets in the two verified service files are:

| Source | Target | Behaviour |
|---|---|---|
| `fns` | `docvalidation` | Ephemeral when both are deployed; stable fallback otherwise. |
| `docvalidation` | `youdo-business` | Stable fallback until `youdo-business` is enabled in the set. |
| `docvalidation` | `cerberus2` | Stable fallback; `cerberus2` is intentionally outside the current Jenkins catalog. |

## Kubernetes and shared infrastructure

Last live check: 2026-08-27, kubeconfig `/home/slnnk/.kube/config-yandex-dev`.

- The Yandex dev cluster has two Ready worker nodes, each with 8 CPU and roughly 48 GiB memory.
- Kubernetes API server version was `1.34.1`.
- Traefik, Vault Agent Injector, Vault Secrets Operator, VictoriaMetrics, and Loki workloads were Ready.
- No ephemeral `dev-*` namespace remained after job `3095886`.
- No `k8s-ttl-controller` workload, resource, or API was found.
- Local kubeconfig permissions were observed as `0664`; reduce them to `0600` if this file remains a personal credential.
- Local kubectl was 1.29 while the server was 1.34. Lifecycle jobs use the controlled `kubectl:1.34.0` CI image.

The namespace chart creates RabbitMQ and Redis without persistence. The microservice chart can create PostgreSQL as a StatefulSet with a PVC. The PVC persists across Helm upgrades inside the namespace and is deleted with the namespace. `PGDATA` points to a subdirectory to avoid `lost+found` initialization failures.

Ephemeral service and PostgreSQL memory requests/limits should normally remain at or below `256Mi`. Current prepared service values do not exceed this cap.

## Repositories and ownership

| Component | Local repository | Current verified state | Responsibility |
|---|---|---|---|
| Jenkins orchestration | `/home/slnnk/git/jenkins-pipelines` | remote/Jenkins-loaded `master` at `10ef2517`; local checkout may require refresh | All 13 catalog services active; service selection, GitLab lookup, namespace/image resolution, Helm deployment, waits, artifacts. |
| GitLab CI bridge | `/home/slnnk/git/gitlab-ci-templates` | local feature refs stale; remote `master` includes MR 76 at `b8bff9a4` | Manual deploy/extend/delete jobs, Jenkins bridge, dotenv/environment lifecycle and stale-job guards. |
| Shared Helm charts | `/home/slnnk/git/helm-charts` | clean `master`, `4ab8743`; migration short-name fix runtime-proven | Namespace infrastructure and generic application/PostgreSQL deployment contract. |
| CI tool image | `/home/slnnk/git/base-images` | runtime image built from the `kubectl/1.34.0` definition; repo master has since advanced | Helm, kubectl, curl, and jq used by lifecycle jobs. |
| Cluster IaC | `/home/slnnk/git/yandex-tf` | dirty user worktree; do not overwrite | Yandex Kubernetes cluster and surrounding infrastructure. |
| Platform services | `/home/slnnk/git/infra-tf` | user branch with untracked `helm-charts/`; do not overwrite | Vault operator/injector and other cluster platform services. |

Jenkins job prerequisites:

- Pipeline from SCM with lightweight checkout disabled;
- GitLab API token in the configured Jenkins global environment;
- `kubeconfig-dev` Jenkins credential;
- SCM credential for `helm-charts` and service checkouts;
- Active Choices, Script Approval, Hidden Parameter, and Build User Vars support.

The current bridge endpoint is the pilot Jenkins job `https://build.youdo.sg/job/test`; `JENKINS_DEPLOY_DEV_JOB` can override it.

## Service catalog and rollout state

The catalog order is controlled by Jenkins. Dependencies below affect selection and routing, not arbitrary repository checkout order.

| Order | Jenkins service name | GitLab project | Jenkins catalog dependencies | Configuration state on 2026-08-28 |
|---:|---|---:|---|---|
| 1 | `youdo-business` | 423 | `youdo-notifications`, `docvalidation` | MR 3567 commit `1d3ebc0c` includes the persisted `512Mi` worker limit and `Staging` dev identity; build `145` proved the full initial deployment and build `148` proved the corrected employee-web root endpoint. |
| 2 | `youdo-business-auth-service` | 544 | — | `master` configuration, migrations, PostgreSQL, and both web workloads runtime-proven in build `145`. |
| 3 | `youdo-business-billing-service` | 491 | `youdo-business` | `master` configuration, migrations, PostgreSQL, and webapp runtime-proven in build `145`. |
| 4 | `youdo-business-doc-generator` | 527 | — | `master` configuration and API workload runtime-proven in build `145`. |
| 5 | `youdo-business-landings` | 532 | — | `master` configuration and API/web workloads runtime-proven in build `145`. |
| 6 | `youdo-business-mobile-id` | 551 | `youdo-business` | `master` configuration, external image, and mobileid/web workloads runtime-proven in build `145`. |
| 7 | `youdo-business-tkb-proxy` | 535 | `youdo-business` | `master` configuration, migrations, PostgreSQL, mock API, and worker runtime-proven in build `145`. |
| 8 | `youdo-business-tochka-proxy` | 492 | `youdo-business` | Both migration paths, PostgreSQL, and all four workloads runtime-proven from `master` in build `145`. |
| 9 | `youdo-kitcut` | 513 | — | `master` configuration with tracing disabled, migrations, PostgreSQL, API, and web runtime-proven in build `145`. |
| 10 | `youdo-notifications` | 505 | — | `master` migrations, PostgreSQL, webapp, and worker runtime-proven in build `145`. |
| 11 | `youdo-sms-service` | 498 | — | `master` migrations, PostgreSQL, webapp, and worker runtime-proven in build `145`. |
| 12 | `docvalidation` | 223 | `youdo-business` | Runtime-proven in the pilot, two-service lifecycle, and full build `145`; `dev.yml` and CI include are in master. |
| 13 | `fns` | 244 | — | Runtime-proven as non-primary in the two-service lifecycle and full build `145`; primary-service lifecycle remains pending. |

`youdo-business-tickets` has an untracked local `devops/dev.yml`, but it is not in the approved 13-service Jenkins catalog and is outside the current rollout. Jenkins build `145` provides initial runtime proof for every approved catalog entry; repeat/lifecycle evidence for the full catalog remains pending.

## `dev.yml` freshness audit

Audit updated: 2026-08-28. Remote refs were refreshed before comparison. The nine master-ready files pass `helm lint` and `helm template` against `helm-charts/master`, but that only proves chart compatibility. It does not prove that Vault paths and keys are valid, probes answer successfully, or the service starts with the selected application revision.

| Service | Assessment | Evidence / required action |
|---|---|---|
| `fns` | Master-ready and runtime-proven as non-primary | `dev.yml` and CI include are in master `7e819e8`; component set matches current CI (`api`, `service`, `scheduler`, `migrations`). Primary-service lifecycle remains pending. |
| `docvalidation` | Master-ready and runtime-proven | `dev.yml` and CI include are in master `a87c447`; component set matches current CI; full lifecycle proven. |
| `youdo-business-auth-service` | Initial runtime proven | Build `145` used `master`; migrations, PostgreSQL, Vault-backed startup, and both web workloads succeeded. |
| `youdo-business-billing-service` | Initial runtime proven | Build `145` used `master`; migrations, PostgreSQL, and webapp succeeded. |
| `youdo-business-doc-generator` | Initial runtime proven | Build `145` used `master`; the API and its image/Vault startup succeeded. |
| `youdo-business-landings` | Initial runtime proven | Build `145` used `master`; both Node.js web and API workloads succeeded. |
| `youdo-business-mobile-id` | Initial runtime proven | Build `145` used `master`; the external mobileid image and web workload started successfully. |
| `youdo-business-tkb-proxy` | Initial runtime proven | Build `145` used `master`; migrations, PostgreSQL, mock API, and worker succeeded. |
| `youdo-business-tochka-proxy` | Initial runtime proven | Build `145` used `master`; normal/mock migration paths, PostgreSQL, and all four workloads succeeded. |
| `youdo-kitcut` | Initial runtime proven | Build `145` used `master`; migrations, PostgreSQL, API, and web succeeded with Jaeger disabled. |
| `youdo-notifications` | Initial runtime proven | Build `145` used `master`; migrations, PostgreSQL, webapp, and worker succeeded. |
| `youdo-sms-service` | Initial runtime proven | Build `145` used `master`; migrations, PostgreSQL, webapp, and worker succeeded. |
| `youdo-business` | Master-ready and primary runtime proven | Build `145` used MR 3567 commit `83b2e24f`; migrations and all seven workloads succeeded, including the worker at `512Mi`. Pipeline `137949` / Jenkins build `148` used commit `1d3ebc0c` and proved the `Staging` correction with HTTP 200 on employee-web `/` and `/health`. MR 3567 was merged to `master` as `a4f80388` on 2026-09-03. |

Cross-service checks from this audit:

- The prepared service/migration component names match current master CI for every service except the stale `youdo-business` definition. `youdo-business-landings` is an intentional special case: its `web` image comes from `.nodejs-build-docker`.
- Every `routing.env.targetService` matches a Jenkins catalog name except `cerberus2`, which is an intentional stable-only fallback outside the catalog.
- The nine master-ready values contain no remaining `.dev.youdo.local` entries; the five previously local-only `.corp` correction sets are now merged.
- All prepared memory limits stay within the established ephemeral `256Mi` cap.
- Build `145` provides current-pipeline initial runtime evidence for all 13 services. Repeat-upgrade isolation and full-catalog lifecycle cleanup were subsequently confirmed manually by the operator. Public nginx routing and application readiness are runtime-proven for all seven generated `.dev.youdo.sg` ingress hosts.

## Verified runtime history

### Single-service pilot

The earlier `docvalidation` pilot verified creation and repeat upgrade in one stable namespace, preservation of the PostgreSQL PVC and an SQL marker, RabbitMQ/Redis reuse, extend, stale-job protection, complete delete, migrations, Ready workloads, no Warning events, and HTTP 200 from `/hc`.

Key historical identifiers: GitLab pipelines `137262` and `137264`, Jenkins builds `132` and `133`, stale extend job `3087694`, delete job `3087854`.

### Two-service deployment

| Operation | GitLab job | Jenkins / result | Evidence |
|---|---:|---|---|
| Initial deploy | `3095877` | Jenkins build `137` | `docvalidation` deployed from MR 133; dependent `fns` deployed from `master`, pipeline `137459`, tag `master-595`; both healthy and `fns` routed to ephemeral `docvalidation`. |
| Repeat deploy | `3095884` | Jenkins build `138` | `docvalidation` upgraded to the newer image from pipeline `137462`; `fns` Helm revision and pod UIDs remained unchanged. |
| Extend | `3095885` | success | Kubernetes TTL metadata refreshed to five days and GitLab environment auto-stop moved to 2026-09-01. |
| Delete | `3095886` | success | Namespace, application releases, PVC, and PV removed; GitLab environment stopped. |

This historical run proved dependency deployment and skip-existing-dependent behaviour for `docvalidation` as primary. It did not by itself prove `fns` as primary or three-or-more-service ordering; both were covered later by build `145` plus the operator-reported manual checks.

## Known gaps and risks

### Remaining baseline checks

- Attach job/build identifiers if durable trace-level evidence is later needed for the operator-verified repeat, lifecycle, `fns`-primary, and negative scenarios.

### Reliability and safety

- Add a Jenkins lock keyed by the final namespace. GitLab `resource_group` alone cannot serialize different refs that resolve to the same task ID.
- Add an HTTP health smoke stage after rollout; Jenkins currently validates Helm, migrations, rollout, and pod phase but does not perform the earlier pilot's `/hc` request automatically.
- Decide whether to install and own a TTL controller. Until then, document GitLab `on_stop` as the only enforced automatic cleanup path.
- Verify a real `auto_stop_in` expiry, not only manual `delete`.
- Restrict `/home/slnnk/.kube/config-yandex-dev` permissions if appropriate.

### Configuration quality

- Resolved and merged: `employee-devops-689.dev.youdo.sg/` had returned HTTP 500 while `/health` was 200 because `ASPNETCORE_ENVIRONMENT=Development` enabled `UseProxyToSpaDevelopmentServer` and attempted to execute `npm` in the runtime image. Commit `a067c985` changes the shared environment identity in `devops/dev.yml` to `Staging`. Pipeline `137949`, GitLab job `3111628`, and Jenkins build `148` runtime-proved the correction on 2026-09-03; both `/` and `/health` returned HTTP 200. MR 3567 was merged to `master` as `a4f80388`.
- Add `values.schema.json` or equivalent validation and chart template tests for `ephemeral-namespace` and `microservice`.
- Document the source of truth and owner for the external Vault role/policy `dev-ephemeral-deployer`; runtime proves it works, while repository agent notes still describe it as deferred.
- Reconcile or archive stale repo documentation, especially `helm-charts/docs/agents-ephemeral-deploy-plan.md`, `helm-charts/AGENTS.md`, and `helm-charts/docs/ephemeral-namespace-role.md`.
- Rename the Jenkins pilot job `test` after the interface stabilizes and update the CI variable/default endpoint.

### Deferred, non-MVP improvements

- Developer access to namespace-local Redis without distributing a cluster kubeconfig.
- Optional Adminer or a database catalog/autodiscovery mechanism.
- Removal of old stopped GitLab Environment records created under superseded naming schemes.
- `youdo-business-tickets` onboarding, which requires an explicit catalog decision.

## Rollout plan

### Phase 0 — Freeze the verified baseline

1. Completed by operator manual verification: `fns` as primary through deploy, repeat, extend, and delete.
2. Completed by operator manual verification: negative primary-`master` and no-task-ID branch scenarios, including cleanup.
3. Completed: YouTrack DevOps-A-50 was refreshed on 2026-09-01 with full-catalog, ingress-reporting, public-nginx, and seven-host smoke evidence plus the remaining hardening plan.

Exit criterion: both services can independently be primary, the shared CI include is on permanent refs, and the baseline documentation matches production configuration.

### Phase 1 — Harden the platform before broad rollout

1. Serialize builds by calculated namespace in Jenkins.
2. Add an HTTP smoke check driven by service health configuration.
3. Add chart schema/template regression tests.
4. Decide TTL-controller ownership or formally standardize GitLab-only cleanup; verify one actual auto-stop expiry.
5. Document the Vault deployer role and reduce local kubeconfig permissions.

Exit criterion: concurrent task deployments cannot collide silently, rollout includes application-level health evidence, and cleanup responsibility is explicit.

### Phase 2 — Validate the full active catalog

The staged `allowed_services` rollout was retired by operator decision on 2026-08-30. The prepared Jenkins change treats all 13 `services` entries as active: a fresh namespace installs the full catalog, while a repeat deploy upgrades only the selected primary and preserves existing non-primary releases.

1. Completed: the Jenkins all-services change is published and build `145` loaded `jenkins-pipelines` revision `2eafc2ee`.
2. Completed: build `145` selected the primary MR and `master` for all 12 dependencies, each with a successful image-producing pipeline.
3. Completed: fresh 13-service deployment, migrations, Ready workloads, ingress-level smoke checks, routing artifacts, and public HTTPS routing/readiness for all seven `.dev.youdo.sg` hosts were verified.
4. Completed by operator manual verification: repeat deploy advanced only the selected primary and preserved non-primary releases/pods.
5. Completed by operator manual verification: extend and delete cleanup semantics.
6. Initial-run evidence is in `~/ai/current/knowledge/log/2026-08-31-dev-deployment-deploy-job-3100718-full-catalog-success.md`; later checks have no supplied job/build identifiers.

### Phase 3 — Complete dependency and repeat-deploy proof

Build `145` completed the initial runtime onboarding of auth-service, doc-generator, kitcut, notifications, and `youdo-business` with its full selected catalog. The operator also manually confirmed repeat behavior and `fns` as primary. Remaining work:

1. Verify `youdo-notifications` and `docvalidation` fallback and ephemeral routing independently.
2. Run additional representative non-`youdo-business` primary services if broader per-primary upgrade evidence is desired beyond `fns`.
3. Completed on 2026-09-01: all seven generated `.dev.youdo.sg` hostnames were checked without forced address overrides; public results matched direct Traefik and every configured readiness endpoint returned HTTP 200.

### Phase 4 — Operationalize

1. Rename the Jenkins pilot job and update the shared CI default.
2. Add monitoring/alerting for stale `dev-*` namespaces, failed migrations, unavailable Vault secrets, and expired GitLab environments that still have Kubernetes resources.
3. Define routine cleanup and recovery commands in the operator documentation.
4. Decide separately whether to add `tickets`, Adminer, Redis developer access, and database discovery.

## Basic diagnostics

Use the dedicated kubeconfig; do not copy its contents into notes:

```bash
kubectl --kubeconfig /home/slnnk/.kube/config-yandex-dev get namespaces
kubectl --kubeconfig /home/slnnk/.kube/config-yandex-dev -n <namespace> get pods,deploy,sts,job,svc,ingress,pvc
kubectl --kubeconfig /home/slnnk/.kube/config-yandex-dev -n <namespace> get events --sort-by=.lastTimestamp
helm --kubeconfig /home/slnnk/.kube/config-yandex-dev list -A
```

Investigation order for a failed deployment:

1. GitLab `1 deploy dev` trace and linked Jenkins build.
2. Jenkins generated service routing and dotenv artifacts.
3. Helm release status/history and migration hook jobs.
4. Namespace events, Vault resources/secrets, pod descriptions, and logs.
5. Image existence/tag correctness in Nexus and corresponding GitLab service pipeline.

## Documentation maintenance rules

- Update this file after every newly enabled service or platform contract change.
- Separate verified facts from plans; include the verification date and job/build identifiers.
- Update YouTrack after a phase exit rather than after every exploratory edit.
- Preserve service worktrees and unrelated user changes. In particular, do not overwrite dirty `yandex-tf` or `infra-tf` worktrees.
- Never store tokens, kubeconfig contents, Vault values, or other secrets in this document.

## Related documents in this directory

- `post-deploy-autotests.md` — DevOps-832 post-deploy autotest status and design.
- `jenkins-deploy-dev-b2b.md` — Jenkins `deploy-dev-b2b.Jenkinsfile` component note and verified build history.
- `gitlab-ci-deploy-dev.md` — GitLab `v3/.deploy-dev.yml` bridge and lifecycle jobs.
- `helm-charts.md` — historical chart-specific observations (PostgreSQL persistence).

## Related log entries

Newest first, all under `~/ai/current/knowledge/log/`:

- `2026-09-07-dev-deployment-tkb-pipeline-138093.md`
- `2026-09-07-dev-deployment-tkb-autotests-preparation.md`
- `2026-09-04-dev-deployment-devops-832-handoff.md`
- `2026-09-04-dev-deployment-devops-832-billing-autotests-prepared.md`
- `2026-09-04-dev-deployment-jenkins-pod-race.md`
- `2026-09-03-dev-deployment-devops-832-tochka-dev-autotests-prepared.md`
- `2026-09-03-dev-deployment-devops-832-tochka-dev-autotests.md`
- `2026-09-03-dev-deployment-devops-832-mock-worker-probe-failure.md`
- `2026-09-03-dev-deployment-youdo-business-dev-deploy-pipeline-137949.md`
- `2026-09-01-dev-deployment-employee-web-root-500.md`
- `2026-09-01-dev-deployment-ingress-public-smoke.md`
- `2026-08-31-dev-deployment-deploy-job-3100718-full-catalog-success.md`
- `2026-08-30-dev-deployment-jenkins-test-142-migration-job-name-length.md`
- `2026-08-30-dev-deployment-deploy-job-3100457-service-name.md`
- `2026-07-30-dev-deployment-dev-master-node-replacement-db-recovery.md`
- `2026-06-26-dev-deployment-youdo-business-dev-yml.md` and the other `2026-06-*` dev.yml onboarding entries
- `2026-06-18-dev-deployment-service-url-routing.md`
