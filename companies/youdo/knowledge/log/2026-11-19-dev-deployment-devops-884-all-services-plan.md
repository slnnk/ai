---
system: dev-deployment
status: verified
checked: 2026-11-19
tags: [kubernetes, helm, gitlab-ci, devops-884]
---
# DevOps-884 shared services rollout assessment

## Task

## Context

## Actions

## Findings

## Changes

## Open items

Independent source review checked Houston Host isolation, the router registration/callback pairing, ai-qa cutover, exact legacy image handoff and concurrent namespace bootstrap. Findings are incorporated above. Inventory and table comparison confirmed 19 unique matching services. The implementation proposal remains open in the central backlog. All commands and the reviewer finished.

## Portable lesson

none
## Summary

The original assessment covered 19 applications. The current rollout targets 18 in permanent namespace `dev-single`. User confirmed on 2026-11-19 that ai-qa stays in `dev-ai-qa`; moving its image publication to Nexus remains separate. Seven shared services have prepared MRs and verified dev deployments. The user waived the S3 upload/download acceptance test for chat-content.

## Resumption checkpoint

Verified on 2026-11-19 Moscow time. [DevOps-884](https://youtrack.youdo.com/youtrack/issue/DevOps-884) covers 18 shared services in the permanent `dev-single` namespace. The user intends to resume in the next session. Read this checkpoint and the existing central TODO entry first. Refresh mutable GitLab refs, deployed state and any current approval before acting.

### Completed and verified

Fresh Kubernetes read showed **7 of 18 releases Ready**. Count `chat-content` as one release with two components. RabbitMQ is common infrastructure. `ai-qa` stays in `dev-ai-qa`.

| Shared release | Merged MR | Verified dev result |
| --- | --- | --- |
| geocoder | [!57](https://gitlab.youdo.sg/youdo/microservices/geocoder/-/merge_requests/57) | Jobs 3310062 and 3310071 succeeded. Internal `geocoder.dev.youdo.corp`, port8080, `/hc` and test geocoding returned200. |
| BlackListedEmailChecker (blec) | [!6](https://gitlab.youdo.sg/youdo/BlackListedEmailChecker/-/merge_requests/6) | Job3310289 succeeded, internal fixture results correct. Uses internal .NET 2.1 SDK and runtime, cache under /tmp. |
| tinkoff-e2c-sign-service | [!13](https://gitlab.youdo.sg/youdo/microservices/tinkoff-e2c-sign-service/-/merge_requests/13) | Job3310441 succeeded, internal `/health`200, port8080. Signing operation remains untested. |
| pechkin | [!238](https://gitlab.youdo.sg/youdo/mail/pechkin/-/merge_requests/238) | Job3310886 succeeded, 3/3 Ready, internal root and example HTML200. `npm start` binds3005, so values use3005. Test mode `production=0` bypasses the production unsubscribe generator. |
| chat-content | [!14](https://gitlab.youdo.sg/youdo/chat-content/-/merge_requests/14) | Job3310972 succeeded, both components at1.1.17 and internal `/debug/vars`200. User waived the S3 upload/download check. |
| escrow-tinkoff-router | [!52](https://gitlab.youdo.sg/youdo/microservices/escrow.tinkoff/-/merge_requests/52) | Job3310988 succeeded, one Ready router, private `/hc`200. Both ingress hosts are in the release. Public edge and callback acceptance remain open. |
| userinsurance-gotenberg | [!77](https://gitlab.youdo.sg/youdo/vsk/youdo.userinsurance/-/merge_requests/77) | Job3311017 succeeded, Ready with internal `/health`200, image8.21.1. User waived PDF conversion verification. |

The shared namespace installation and repeat application upgrades were verified. Namespace Helm revision1 persisted across the recorded app redeploys. Shared CI master `c74bea9` has all four merged template changes: [!93](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/93) single bootstrap with common values, [!94](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/94) universal `APP_IMAGE_PUBLIC_NAME`, [!95](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/95) optional manual dev job, [!96](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/96) timeout7m. A fresh consumer MR verified `allow_failure: true` on the actual job. Scheduling of later stages during an already-running dev job was not independently exercised.

YouTrack readback confirms seven struck service names, 11 links in the dedicated **Merge Request** field, and eight approved comments present. For future updates use that field for MR links and keep deployment marks in the description. The template comment is 74-125683 and the seven service comment IDs are 74-125685 through 74-125691. The format is a repository heading followed by a linked MR number and short change description, separate comments by service.

### Pending decisions and resumption order

1. **Next service outside GitLab Data:** start with `youdo-business-doc-generator`, then `taskqualitycontrol` and `HoustonV2Mock` from the proposed next non-Data batch. First describe the scope, repo/branch/base and wait for the applicable edit approval. The Gotenberg and Escrow router entries of that batch are already deployed.
2. **Helm draft is local and available for review.** `~/git/helm-charts`, branch `DevOps-884-microservice-command-args` from `3254a7f`. Three modified/untracked files comprise two intended commits, optional component `command`/`args`, then ConfigMap/Secret file mounts. The bound combined snapshot matched at handoff, and remote master is still `3254a7f`. Exact diffs, body and checks are in `~/ai-data/gitlab-workflow/DevOps-884/helm-charts/`. One MR with separate commits was requested. Recheck compatibility for existing GitLab and Jenkins renders, then obtain explicit approval for the actual publication. Model init and PostgreSQL lifecycle work are still design only.
3. **Escrow public edge is a separate scoped change.** The router Helm values already declare `t-escrow-router.dev.youdo.corp` and `t-escrow-router.dev.youdo.sg`. The last public probe returned301 to youdo.sg. A future `automation-services` MR should use `inventories/yandex/group_vars/balancers_test` to forward the public host to Traefik with the original `Host`, allowing only the known callback and notification routes. Registration stays private because it lacks authentication. The router has one serving instance and process-local registrations; test a new registration and callback reaching the same instance. Do not move existing bank test traffic or change primary C2C values without an approved rollout. Recheck edge config, which was last inspected at `60fc7e85`.
4. **Keep the main `userinsurance` and `escrow.tinkoff` workloads per C2C stand.** Their shared Gotenberg and router jobs already work independently. Main values/catalog changes are deferred. On future C2C wiring check same-cluster reachability before using the stable Service DNS; configure `Policy__GotenbergServiceUrl` and `Router__Url` separately. The user waived the Gotenberg PDF test.
5. **ai-qa registry work is separate.** Keep `dev-ai-qa`. The proposed Nexus migration in `~/git/ai-qa` changes its image publication/login, preserves image digest and verifies controller/worker image selection. The proposed repo base was `d559872`; refresh before proposing edits. The migration was discussed, not implemented or approved for rollout.

### Remaining shared services

| Service | Main decision or work |
| --- | --- |
| youdo-business-doc-generator | Existing dev.yml, S3, HTTPS/health configuration. Keep its existing Jenkins deployment behavior when adding the shared Helm release. |
| taskqualitycontrol | Use the sysadmins test mock `taskqualitycontrolfortest`, scope MR image build while preserving staging-* release convention. |
| HoustonV2Mock | Legacy CI and Host-based per-stand fixture lookup. Validate two actual dev hostnames and cache keys together. |
| youdo_recommendations_mock | Existing fixture store and legacy CI. Preserve existing image/attestation settings and writable storage. |
| youdo-call-service | Web+worker, Postgres and migrations, shared RabbitMQ, mock provider/callback. |
| textvalidation | PostgreSQL, pre-migration and application connection options. |
| mailer | PostgreSQL, RabbitMQ, Pechkin and controlled test SMTP; three application components. |
| DebuggingEvents | Select isolated Elasticsearch7.17.14 placement and storage, with API in the shared chart. |
| daily-compilations | Data group. Gunicorn command, YAML and PostgreSQL; needs chart publication and data decision. |
| subcategory-predictor | Data group. Model/JamSpell initialization and Kafka REST. |
| moderation-bert | Data group. Confirm release source at tag0.1.6, model/S3/ClickHouse prerequisites and cold-start timing. |

### Conventions and permission checkpoint

- Use one application chart, `helm-charts/microservice`, for GitLab and Jenkins. Preserve mode-specific CI rules, standard upstream image build and optional manual `deploy dev`. Legacy repositories may need explicit same-pipeline image handoff.
- Internal dev ingresses use `.dev.youdo.corp`. Router has the explicit public test exception `t-escrow-router.dev.youdo.sg`. Use an actual listener/readiness port. For non-root ASP.NET Core set `ASPNETCORE_URLS` and container port8080; other apps may already listen on another suitable port.
- Leave CPU requests and limits at chart defaults; omit `cpu` and `cpuLimit` in new dev values. Keep app boot environment and tested resource sizing. Existing services remain outside incidental cleanup.
- Bootstrap uses shared CI overrides rather than a separate namespace values file. RabbitMQ is common, with `emptyDir`, and no management Ingress. Registry/Vault sync and RabbitMQ readiness gates were exercised. Namespace-specific application deploys reuse the release.
- Pending note from user: shared `dev/logreader/LogreaderConnectionString` was reported incorrect. Geocoder's bind failure was a separate port issue and current health/geocoding succeeded. Any Vault change needs an exact source/destination proposal and explicit approval. App credentials already provisioned for geocoder and chat-content.
- Keep previous approval evidence scoped to the action already taken. The user's additional explain-before-edit rule was session-only; resume with the current AGENTS.md repo edit, publication and external-write gates. No queued local commands, automation or deployment started by the agent remains active.

## Context and common changes

Sources: [accepted inventory](2026-11-17-nomad-test-devops-884-shared-service-inventory.md#target-dev-kubernetes-inventory-user-decision-november17), [first ten and CI decisions](2026-11-17-dev-deployment-devops-884-first-ten-assessment.md), [ai-qa rollout](2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md).

- In `gitlab-ci-templates` and `helm-charts`, make the first deploy install the namespace Helm release from common values, including registry and Vault integration. Remove TTL using existing ai-qa overrides. Serialize first installs across projects around the shared Helm release; project-local resource_group alone does not do this. Reuse the deployed namespace release on later jobs. Verify failed/pending install handling and gate app deployment on registry/Vault readiness, including image pulls and required secret paths for each service. Preserve existing template consumers and their namespace lifecycle outside dev-single.
- Add a stable per-service Helm release and a manual dev job. Preserve existing build, test, release, staging and production rules. For standard v3 projects use MR plus the existing release mode (semver tag for manual, master for auto). For legacy pipelines, publish a pipeline-specific MR tag or digest and hand the exact same-pipeline build/release image to the dev job using explicit job dependencies and metadata. Keep each service’s release tag convention, including staging-* for taskqualitycontrolfortest, and prove the effective jobs in MR/tag/master. Avoid updating shared latest tags from the MR-only path. Gotenberg is the pinned upstream image and needs no dedicated image build.
- Preserve service paths and per-stand behavior. Check routing from a representative ephemeral namespace before switching a group of consumers. Keep existing endpoints available while validating the new ones. Any consumer switch is a separate rollout step. Use test credentials and endpoints for payment, telephony and outbound mail checks.

## Proposed service plan

| Wave | Target | Change and dependencies | Acceptance check |
| --- | --- | --- | --- |
| 1 | geocoder | Pilot: standard v3, single API, Yandex/DaData and Exceptional logging settings. | First install and redeploy, /hc and one test address lookup. |
| 1 | youdo-business-doc-generator | Adapt existing values and route from old Jenkins dev flow for this service. Auto/master. S3 and Vault. | Generate a document and check its S3 object. |
| 1 | chat-content | Deploy uploader and downloader with their own images and S3 configuration. | Both components Ready and both /debug/vars endpoints respond through internal ingress. User waived S3 upload/download. |
| 1 | tinkoff-e2c-sign-service | Use existing web image and signing material access from the image; confirm configured path. | /health and a test signature verified by its consumer. |
| 1 | BlackListedEmailChecker | Supply domain-list network access and a writable cache. Select an actual readiness route or TCP as appropriate. | Refresh list and validate blocked and allowed fixture domains. |
| 1 | pechkin | Preserve templates; keep the reachable test unsubscribe endpoint or make it configurable if the URL changes. | Render a message and exercise unsubscribe link generation. |
| 2 | HoustonV2Mock | Add scoped MR build beside legacy master/tag builds. Preserve per-stand Host parsing. The current regex only matches test stand labels. Agree compatible dev hostnames or update the regex together with ingress and consumer URLs. | Seed the same fixture key with different values from two actual dev stand URLs, check both interfaces and re-seeding after restart. |
| 2 | youdo_recommendations_mock | Existing single image, legacy master/tag jobs. Preserve no-attestation and writable JSON fixtures, with one instance for fixture consistency. | Call task, contractor and similar-task fixture routes. |
| 2 | taskqualitycontrol | Source sysadmins/taskqualitycontrolfortest, confirmed by live image. Existing single image, legacy master/tag jobs and in-memory fixtures. | Seed via POST /evaluation/testdata and test POST /evaluation. |
| 2 | userinsurance-gotenberg | Deploy only Gotenberg 8.21.1 on port 3000 from youdo/vsk/youdo.userinsurance, keeping its existing app/Nomad jobs. | Deployment and internal /health verified. User waived PDF conversion acceptance. |
| 2 | escrow-tinkoff-router | Deploy only /router image from escrow.tinkoff, retain its staging settings and test callback routing. Pass the exact router subimage from build-router. Registrations live in one process for up to eight hours. Route both escrow registration and provider callbacks to the same instance, and retain the old route during outstanding test flows or drain them before switching. | Verify /hc and an app-originated registration followed by end-to-end test redirect/forwarding. |
| 3 | youdo-call-service | Web and worker, PostgreSQL/PVC, pre/post migrations, RabbitMQ, mock provider and callbacks. | Migrations finish, web/worker work together and a mock call completes. |
| 3 | textvalidation | API, PostgreSQL/PVC, pre-migration image, logging settings. | Run migration and representative validation request. |
| 3 | mailer | API, scheduler and dispatcher, PostgreSQL, migration, RabbitMQ, Pechkin and test SMTP. | Drain a test message end to end to a controlled recipient. |
| 3 | daily-compilations | API on port 5000 needs the Nomad gunicorn command or an equivalent image entrypoint. Provide YAML config and PostgreSQL/PVC. Source creates schema at startup. Decide whether subscriptions are seeded or transferred. Preserve tag release and adapt existing build. | /health and GET/PUT of an isolated test subscription; verify persistence across redeploy. |
| 4 | DebuggingEvents | API plus Elasticsearch 7.17.14. Select an existing or separate compatible ES endpoint and storage; test chart limits around mounts and kernel settings. | ES health and event write/read. |
| 4 | subcategory-predictor | Fetch versioned model archive and JamSpell artifact; mount app YAML and configure Kafka REST/Eventum. Observed VK app memory request 5000 MB. | /health, real prediction fixture, and event received by the test destination. |
| 4 | moderation-bert | Live image 0.1.6 corresponds to tag f628bd18; master 78a3bdfc contains planning files and does not contain the release tag in its ancestry. Establish the source base. Data CI template 3ff6ffb has separate build/release and tag deploy jobs. Verify effective image handoff to Helm and MR eligibility. Recreate S3 prestart fetch, shared model volume, YAML and ClickHouse BI access. Select active/shadow versions and measure startup before setting timeout. | /ready after model load, scoring fixture and any selected shadow behavior. |
| Separate | ai-qa | Keep the existing release in dev-ai-qa and move its image publication to Nexus. | Verify a build, controller rollout and worker image pull in dev-ai-qa. |

## Source evidence and limits

Refreshed first ten and ai-qa, plus common templates/chart. The first-ten source SHA list remains valid. Additional source refs: [Houston](https://gitlab.youdo.sg/youdo/mock/houstonv2mock/-/tree/e10c1e2), [daily](https://gitlab.youdo.sg/data/daily-compilations/-/tree/b1901e5), [subcategory](https://gitlab.youdo.sg/data/subcategory-predictor/-/tree/11909b4), [recommendations](https://gitlab.youdo.sg/sysadmins/youdo_recommendations_mock/-/tree/74f4115), [router](https://gitlab.youdo.sg/youdo/microservices/escrow.tinkoff/-/tree/3ceb86f), [quality mock](https://gitlab.youdo.sg/sysadmins/taskqualitycontrolfortest/-/tree/a81f45e), [Gotenberg job](https://gitlab.youdo.sg/youdo/vsk/youdo.userinsurance/-/tree/397ed0c), [BERT release](https://gitlab.youdo.sg/data/moderation-bert/-/tree/0.1.6), [ai-qa](https://gitlab.youdo.sg/youdo/ai/ai-qa/-/tree/d559872). Read Nomad job specs for six ambiguous or dependency-heavy targets, including current BERT image and resource settings. The chart has env/secret refs and built-in PG wait, but its Deployment template lacks generic config file mounts and arbitrary init containers. Plan a focused chart extension or service-owned manifests only for workloads that require them.

No builds, effective CI dry-run, live dev route or secret validation, state transfers, application changes or deployments in this assessment. No current readiness claim for dev-single. Wave assignment and checks are proposals. Use the central DevOps-884 entry for implementation status.

Independent source review checked Houston Host isolation, the router registration/callback pairing, ai-qa cutover, exact legacy image handoff and concurrent namespace bootstrap. Findings are incorporated above. Inventory and table comparison confirmed 19 unique matching services. The implementation proposal remains open in the central backlog. All commands and the reviewer finished.

## Portable lesson

None.

## Task metrics: DevOps-884-all-services-plan

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-884-all-services-plan",
  "created": "2026-11-19T13:17:00.678124+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "investigation",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Verified 19 unique inventory rows; refreshed repository refs and inspected six live job specs; independent source review findings included in final plan.",
  "updated": "2026-11-19T13:17:00.678170+03:00"
}
```

## Shared microservice chart requirement

The user explicitly requires one application chart for standalone services and Jenkins B2B deployments. Both entry points already use `helm-charts/microservice`. Jenkins supplies the deployment namespace, release name, build suffix, storage class and routing overlay. Direct GitLab Helm deploy uses a stable namespace/release from service values. Keep the same values contract, and make capabilities opt-in per service. The existing `ephemeral-namespace` chart keeps its separate infrastructure responsibility. CI owns namespace selection and bootstrap, image selection and deployment timeout.

## Chart blockers and proposed order

Refs `helm-charts/3254a7f`, `jenkins-pipelines/9e60d3e`, `gitlab-ci-templates/56ba8a1` freshly fetched. Baseline lint for both charts, migration Job names and PostgreSQL StorageClass render checks passed. Real values for ai-qa, B2B Billing and youdo.business also rendered against chart master with representative namespace, image and build overrides. This check did not reproduce the full Jenkins routing overlay.

1. Application startup and config files. The Deployment template has no per-component command, args or volume mounts. The current ConfigMap contains environment variables. Daily compilations needs the Gunicorn invocation and YAML config from its Nomad spec. Propose optional per-component command, args, volumes and volumeMounts. Define an ordinary release-scoped file ConfigMap for nonsecret content, with a separate conditional pod checksum if the chart owns the file content. Keep the existing env checksum unchanged for legacy values. Allow references to existing Secret objects for secret files and preserve the current environment ConfigMap contract. The live daily-compilations YAML contains DB configuration with secret material and uses Consul templating. Its Kubernetes rollout needs a reachable database and secret-backed configuration. The first MR fixture uses synthetic data only. Keep fields absent in rendered manifests for existing values.
2. Model startup. Subcategory predictor needs its models and JamSpell artifact before start. Moderation BERT uses a prestart fetch and mounts the shared files. Support per-component initContainers sharing a volume with the main process; render one list alongside the existing wait-for-postgres. Keep kube readiness and liveness separate. Add opt-in startupProbe if cold startup tests show it is necessary, including tests for fetch failures and delayed readiness. Model versions and credentials stay in service configuration. GitLab Helm timeout defaults to five minutes and is separately configurable. Jenkins currently uses ten minutes. The BERT rollout notes describe cold starts much longer than either timeout. Measure with a cold cache and leave readiness tied to model availability. Jenkins needs a service-specific timeout only if it deploys BERT.
3. Permanent database lifecycle. The chart renders PostgreSQL StatefulSet and Service as pre-install/pre-upgrade hooks with before-hook-creation. That recreates database resources on app upgrades even though the PVC survives ordinary upgrades. Existing pre-migration hooks depend on the database Service existing before they run. The StatefulSet accepts passwordSecretRef, but generated pgService rejects this mode, and migration CON_STR uses the default password without envValueFrom/envFrom support. The application VaultStaticSecret is an ordinary resource, so on first release it cannot create the password Secret in time for the pre-install PostgreSQL hook. Pre-provision the Secret or explicitly order its bootstrap and readiness. Treat permanent DB lifecycle and credentials as a separate design during database onboarding. For DB-backed services choose a persistent endpoint with an independently managed lifecycle or define a bootstrap/migration contract with compatible hook ordering, shared Secret references and install/upgrade/rollback tests. Preserve existing B2B defaults.
4. DebuggingEvents and other dependencies. Keep the API under microservice. Select the Elasticsearch runtime and storage separately; its Docker memory lock/ulimit semantics are not implemented by the chart. Configure existing RabbitMQ, Vault and registry once through the namespace path. The chart already supports multiple service components, exact image override, HTTP/TCP probes and ordinary ingress. Avoid a separate application chart or a deployment-mode flag.

First proposed repo edit gate: `sysadmins/helm-charts`, branch `DevOps-884-microservice-runtime-config` from `origin/master` at `3254a7f`. Scope only optional command/args, file configuration and mounts in microservice, documented values and targeted render fixtures. Implement after user approval. Compare baseline and changed manifests for representative real B2B values with Jenkins overrides and ai-qa values with GitLab overrides. Prove the new daily-compilations shape with synthetic secret-free values, then run Helm lint and both existing regressions. Chart master is consumed by both pipelines, so merge affects subsequent deploys and compatibility is required.

Independent source review confirmed the execution paths and the first-install Secret ordering concern. Its findings were incorporated above. Discussion only. No repository task edits, branch changes or deployments. The first edit gate is pending. The remaining rollout proposal stays under the same DevOps-884 backlog item.

## Proposed dev-single infrastructure details

- Namespace: store shared values in `helm-charts/ephemeral-namespace/dev-single.yml`. Set one namespace, both TTL keys to null, and use the existing developer RoleBinding and Vault/registry integration. In GitLab `v3/.deploy-helm.yml`, apply the install-once path only for dev-single. Any first service can install release dev-single in default. Reuse a deployed release, with bounded wait for a concurrent first install and an explicit failure for a failed or stuck release. Verify VSO readiness and the resulting registry Secret before deploying the application. Subsequent deploys upgrade only the application release. Maintain the infrastructure release separately when its settings change.
- RabbitMQ: enable the existing in-namespace broker as a ClusterIP on `rabbitmq:5672` for call-service and mailer, using a dev Vault-backed broker credential and the same configured vhost and topology on producers and consumers. Disable the management ingress and Redis at first. Use the existing emptyDir for disposable test messages as the initial proposal. If retaining queued messages after pod replacement is required, add opt-in stateful/PVC support or use an approved persistent test broker before onboarding the consumers. The existing persistence flag alone renders no PVC. Check broker readiness and test both messaging flows before switching consumers.
- Elasticsearch: propose a dedicated Elasticsearch 7.17.14 single node for DebuggingEvents with internal-only Service and its own persistent claim, managed separately from namespace bootstrap and from the API Helm release. The API stays on microservice and points `Elasticsearch__Host` at the internal Service, with a dev-specific index prefix. Dedicated isolation is appropriate because the API lists indices and independently deletes expired matching indices, and its current client only explicitly configures the endpoint. Confirm the dev cluster can run the existing ES version and its memory/kernel settings without blind reuse of Nomad Docker settings. Verify health, event write/read and preservation after ES pod replacement. Start with fresh dev indices as a proposal. No Elasticsearch dependency for the first chart MR.

A secret-free local render of chart master 3254a7f confirmed eight resources for these namespace settings, including RabbitMQ Service/Deployment and two VaultStaticSecrets, with no TTL, management Ingress, Redis or RabbitMQ PVC. No runtime, credential, endpoint or topology check ran. Discussion and proposed defaults only. No repository or cluster changes and no background operations.

### Simplified bootstrap values option

The user asked why dev-single needs a separate values file when ai-qa reuses its existing devops/dev.yml. Verified that the current GitLab template passes this one file to both charts. ai-qa sets both TTL keys to null and disables RabbitMQ and Redis in that file. Reusing any first service's namespace settings for dev-single would make the common setup depend on which service deploys first. The earlier separate dev-single values file was proposed to remove that dependency.

Revised proposal: keep the existing service dev.yml as the source of global.namespace, global.projectName and application values. For only the dev-single install-once path, set the small set of constant infrastructure overrides directly in the shared CI invocation using Helm --set, and inherit the namespace chart's existing Vault and registry defaults. Use the same TTL null overrides as ai-qa, and explicitly set RabbitMQ enabled, its management ingress disabled, and Redis disabled. This removes the proposed extra file while preserving the first-service bootstrap and identical settings for any installer. Keep the existing ai-qa path and Jenkins behavior. If these settings grow substantially, reconsider the values location. This is a revised proposal in response to the user's design question. No repository or infrastructure changes.

## Compatibility and review sequence

User requires preserving current deployments and splitting changes for review. This supersedes the proposed first MR that combined command/args, file configuration and mounts.

1. Chart MR: optional per-component command and args only. Proposed repo sysadmins/helm-charts, branch `DevOps-884-microservice-command-args`, based on `origin/master` at `3254a7f`. Render identical manifests with old values before and after, including actual ai-qa and representative B2B values with effective GitLab/Jenkins overrides and routing overlay. Compare resource names, labels/selectors, ingress, images, pod checksums, database and migrations. Run chart lint and existing regressions, plus a focused fixture to prove explicit command and args are rendered.
2. Chart MR: optional file configs and mounts. Validate nonsecret ConfigMap and existing Secret references, change-triggered rollout only for the participating release, and unchanged legacy manifests.
3. CI template MR: bootstrap dev-single once using the shared CI overrides. Compare existing ai-qa path and B2B flow, then verify first install, repeat deploy and parallel first jobs. Deploy and update a geocoder pilot only with separate rollout approval.
4. Follow with focused chart MRs for model init and DB lifecycle as their onboarding requires. Keep service values and rollout changes out of the shared chart MRs.

Each MR has its own bounded scope and evidence for user review. Show actual diff, checks and CI effects under the existing supervised publication gate. Current branches and deployments are untouched. First chart edit gate awaits user approval. No background operations.

### One chart MR with separate commits

The user selected one MR with separate commits for review, superseding the separate chart MRs above. Keep the chart changes in one helm-charts MR with small commits and compatibility evidence by commit. Changes to GitLab CI bootstrap live in gitlab-ci-templates and require their own repository MR. Existing deployment compatibility remains the acceptance criterion.

The proposed first commit exposes optional Kubernetes command and args on each microservice component. The daily-compilations image defaults to python -m daily_compilations, while current Nomad staging deliberately runs Gunicorn with port 5000 and four threads. This chart capability preserves the current runtime invocation using the existing image. Values without these fields retain the container image defaults. The commit demonstrates rendering only; daily-compilations still needs config delivery and database access for rollout. The user requested this explanation while reviewing scope. No repository task edits or background operations.

### Command and args change prepared locally

The user said `Подготовь изменения` immediately after the explanation of step 1. Applied the approved first scope in the existing sysadmins/helm-charts checkout, on new branch `DevOps-884-microservice-command-args` from `origin/master` at `3254a7f`. The original branch was clean and remains available. Only microservice/templates/deployment.yaml and microservice/README.md changed. Each component optionally renders Kubernetes command and args as YAML lists. Omitted and empty lists retain the previous manifest. Suggested commit subject: `support microservice container command and args`.

Helm 3.14.0 byte comparison showed identical before/after manifests for ai-qa with GitLab image values and for B2B Billing and youdo.business with Jenkins namespace, image, storage class, build suffix and routing overrides. Both present and absent dependency routing cases were exercised for each B2B service. A secret-free fixture confirmed exact Gunicorn argv, independent command-only and args-only settings, and omission for missing or empty lists. Both chart lints, existing migration-name and StorageClass tests, and git diff --check passed. This was local render validation, not a Kubernetes deployment. The actual diff was checked and the index is empty.

CI config was inspected. It permits MR and master validation pipelines; the job runs chart lint, regressions and renders. Neither publication nor deployment was requested in this stage. The first change is ready for review in the local branch. Later chart changes are separate commits in the same intended MR. No staging, commit, push, MR, pipeline creation or background operations.

### Config file mounts and combined MR preparation

The user asked to prepare the MR, explain the next change first, and advance to it. Explained how daily-compilations needs its Nomad-style YAML and how ConfigMap and Secret mounts deliver file-based settings. Continued the next agreed chart step on the same `DevOps-884-microservice-command-args` branch from `3254a7f` to retain one chart MR. Saved the first reviewed patch separately before extending the worktree.

The second change adds opt-in per-component `configFiles`, `volumes` and `volumeMounts`. Nonsecret files get an ordinary component ConfigMap and mounted-volume support. Existing Secret and ConfigMap references are supported through native volume specs. Only components using the chart-owned file ConfigMap get its checksum. The real daily-compilations database, secret provisioning and rollout are separate. Current worktree changes are limited to three paths: microservice/README.md, microservice/templates/deployment.yaml and microservice/templates/config-files.yaml.

Helm 3.14.0 compared chart master, first patch and combined state. All five current GitLab/Jenkins scenarios rendered byte-identically, including B2B present and absent dependency routing. Synthetic fixtures checked Gunicorn, managed ConfigMap and existing Secret/ConfigMap mounts, unchanged PostgreSQL wait, and omission for empty configuration. Changing file contents changed exactly the file ConfigMap and the corresponding API Deployment. Both chart lints, migration Job-name and PostgreSQL StorageClass checks, and tracked diff whitespace checks passed. No deployment test.

Combined local Ready MR proposal: `DevOps-884 extend microservice container configuration`, `DevOps-884-microservice-command-args -> master`, assignee a.solonenko, squash off and source removal after merge per project defaults. Commit subjects in order: `support microservice container command and args`, `support microservice config file mounts`. GitLab read-only inspect found no open MR for the source. MR workflow triggers validate:helm, with no deployment. Actual diffs, body, reproducible render check and bound snapshot are in `/home/slnnk/ai-data/gitlab-workflow/DevOps-884/helm-charts/` (about 16 KB retained for review and the supervised publication gate). Step-one snapshot is historical after the second diff. The final snapshot is authoritative for this two-commit proposal. No staging, commits, push, MR publication, pipeline creation or background operations.

### User correction on implementation approval

The user clarified that the agent must describe each change first and await approval before implementing it. The second-stage implementation started after the explanation without waiting for explicit approval of that stage. The combined proposal is pending review. Leave the current local diff available for review and wait for the user before any additional implementation or publication. The user clarified that this additional per-stage approval rule applies to the current conversation only.

### Stage 3 edit proposal

User requested moving to the next stage. Session-only agreement requires describing the implementation and awaiting explicit approval. First two Helm changes remain local for review. Stage 3 uses a separate gitlab-ci-templates MR, because the application chart is a separate GitLab project.

Proposed repository `sysadmins/devops-tools/gitlab-ci-templates`, branch `DevOps-884-dev-single-bootstrap` from `origin/master` at `56ba8a1`. Change only `v3/.deploy-helm.yml` and `v3/DEPLOY_HELM.md`. Leave the current namespace-upgrade flow for every namespace except dev-single. Jenkins does not use this job. Keep application deploy, image overrides, job rules and other deployment modes as before.

For dev-single, reuse the existing chart defaults for Vault and registry and pass consistent CLI overrides for one namespace, both TTL keys null, RabbitMQ on, management ingress off and Redis off. The existing dev.yml still provides global.namespace, global.projectName and application values. Inspect the Helm release dev-single in default. On absence attempt install, never upgrade in this branch. If another job installs concurrently, wait boundedly for the deployed release. Fail visibly on API errors, failed or stuck releases. Wait for registry Secret and broker readiness before the app. Existing Namespace alone is insufficient. Verify regular ai-qa command flow, first and repeat installs, parallel first jobs, error handling, and that one service cannot change shared values. Local checks first; shared cluster pilot requires separate authorization. No implementation begun.

### Stage 3 diff prepared locally

After explaining the purpose, the compatibility scope and the effect on ai-qa, user gave the first-stage approval for this repository with `Подготовь изменения и покажи diff этого этапа`. Created `DevOps-884-dev-single-bootstrap` from `origin/master` `56ba8a1` in the existing sysadmins/devops-tools/gitlab-ci-templates checkout. The previous branch was clean. Changed only v3/.deploy-helm.yml and v3/DEPLOY_HELM.md as proposed. The helm-charts worktree remains separately available for review.

The dev-single branch uses an exact Helm release lookup, installs once with shared CLI values, rechecks the release after an install conflict and polls pending-install at most 60 times with five-second intervals. Failed/stuck releases and lookup/readiness errors stop before application upgrade. The gate checks registry-auth SecretSynced, the registry Secret name, and RabbitMQ Deployment rollout. The existing per-service values and Helm upgrade path remain for other namespaces. Jenkins is outside this MR.

Local shell simulations passed 15 cases, including byte-identical command traces for dev-ai-qa and a second legacy namespace, first and repeat deploy, concurrent installation states and failure/timeout cases. YAML comparison confirmed unchanged job settings/rules and application shell block. Actual Helm template invocation with the proposed flags rendered eight resources, no TTL, Redis or management Ingress. No Kubernetes or GitLab runtime test executed. git diff --check passed and the index is empty. Saved exact diff and reproducible check under `/home/slnnk/ai-data/gitlab-workflow/DevOps-884/gitlab-ci-templates/` (about 11 KB retained for review and future verification). No commit, push, MR, deployment or background operation.

### Geocoder pilot prepared locally

Proposed the pilot purpose, repository, branch, base and acceptance criteria before touching the repository. User explicitly approved the pilot edit with `Подтверждаю`. Refreshed geocoder master and confirmed `328aef3`. Created `DevOps-884-geocoder-dev-single` in the existing clean checkout. Added one Helm template include to .gitlab-ci.yml, preserving CRLF and all other bytes. Added devops/dev.yml for stable release geocoder in dev-single: API port 80, /hc readiness, /metrics, proposed geocoder.dev.youdo.sg ingress, existing Nomad resource sizing and Vault references under dev/projects/geocoder. Disabled tracing for this pilot because the default app host points at a non-dev example domain and Nomad injects its own agent address. Existing deploy environments receive no configuration changes.

GitLab CI Lint validated the configuration. Simulations of existing semver tag 1.2.12 showed the same 13 original jobs plus manual deploy dev. Master was empty in both original and revised simulations. MR manual availability follows the unchanged MR rule; no real MR pipeline ran. Helm lint passed. Helm renders from master and the prepared chart were byte-identical, with five resources including API Deployment, Ingress, /hc and Vault mapping. The render initially found an empty metrics path when only enabled was set. The final render includes the explicit /metrics path. Whitespace check with CRLF handling passed, and the index is empty.

Vault path and key availability, ingress and dependency reachability and application rollout remain unverified. The CI bootstrap change needs to reach the shared template master before any pilot deploy. There are no Vault writes, stage, commit, push, MR, deploy or running tasks. The exact patch and local check are retained for review under `/home/slnnk/ai-data/gitlab-workflow/DevOps-884/geocoder/` (about 4.5 KB).

### Geocoder Vault source and destination preflight

User requested creating dev/projects/geocoder using the old configuration. No geocoder config.yml was found in the inspected checkout or local history. The active legacy Nomad mapping in geocoder devops/test.hcl reads YANDEX_API_KEY and DADATA_TOKEN from secret/dotnet/geocoder, and LOGREADER_CONN_STRING from secret/resources/databases/mssql. Authenticated read-only VK test Vault metadata checks confirmed all three fields are nonempty and the destination returns 404. Capabilities-self returned root for the destination. No secret values were printed or stored.

Proposed external write for approval: create only secret/dev/projects/geocoder in VK test Vault with the three same-named values from the legacy Nomad Vault sources listed above. Recheck absence immediately before writing and compare the three values in memory during readback. Existing source paths are not edited. No repository or deployment changes. Waiting for confirmation of the resolved source mapping and exact Vault write. No background operations.

### Shared dev Logreader for geocoder

The user pointed out the existing dev/logreader secret. Read-only VK test Vault check confirmed its nonempty `LogreaderConnectionString` field. This matches an existing dev chart mapping documented in the FNS deployment note. Revise the proposal to reference dev/logreader directly for `ConnectionStrings__Exceptional`, and to create dev/projects/geocoder with only YANDEX_API_KEY and DADATA_TOKEN from dotnet/geocoder. This supersedes the earlier proposed copy of LOGREADER_CONN_STRING. The worktree and Vault are untouched pending approval for the scoped config edit and external write. No values printed or persisted, no background work.

### Geocoder Vault provisioning verified

User confirmed both the scoped geocoder values edit and the exact VK test Vault write with `Подтверждаю`. Modified devops/dev.yml on the existing DevOps-884-geocoder-dev-single branch from 328aef3. The file now renders one VaultStaticSecret for both provider keys from dev/projects/geocoder and a second VaultStaticSecret for ConnectionStrings__Exceptional from dev/logreader/LogreaderConnectionString. Updated the local review diff and test. Helm lint passed, and all six pilot resources rendered identically on chart master and the prepared chart.

Rechecked both source credentials and shared Logreader in memory and confirmed dev/projects/geocoder was absent immediately before creation. One POST returned HTTP204. An independent readback matched the legacy provider values exactly and confirmed only the two approved keys. No credential values were printed or saved. Source credentials and shared Logreader were unchanged. Local changes await review. No stage, commit, push, MR or application deploy. CI bootstrap merge and separately approved pilot deploy remain pending. No background operations.

### Stage 3 publication proposal

User requested publishing the bootstrap MR. The already-reviewed actual two-file diff matches the current worktree exactly. Refreshed origin/master and HEAD are both 56ba8a1. Index is empty, no matching remote branch or open MR. Reran all 15 local shell cases, the actual namespace render and diff whitespace verification successfully. GitLab project428 metadata shows builds disabled, Auto DevOps off and no custom CI path. Root has no .gitlab-ci.yml. The project pipeline API returned HTTP403 with CI disabled. No deploy-on-publish effect. The consumer side changes after merge when a dev-single deploy job is manually run.

Prepared the Ready MR publication proposal for sysadmins/devops-tools/gitlab-ci-templates: source DevOps-884-dev-single-bootstrap, target master, commit `bootstrap dev-single once`, title `DevOps-884 bootstrap dev-single once`, assignee a.solonenko, squash enabled and source deletion on merge per project defaults. Exact body and bound repository snapshot are stored next to dev-single-bootstrap.diff under `/home/slnnk/ai-data/gitlab-workflow/DevOps-884/gitlab-ci-templates/`. Waiting for the second supervised approval of the concrete publication parameters. No staging, commit, push, MR, merge or deployment. No background operations.

### Stage 3 publication verified

User replied `Да` to the exact two-file publication proposal. Snapshot check matched. Staged and committed patches matched the reviewed diff byte-for-byte, staged whitespace check passed, and the commit was `78e1c820339690aeacb45c8c13d8fe4400cb599c` (`bootstrap dev-single once`). Pushed only DevOps-884-dev-single-bootstrap. The initial helper timed out on its GET /user preflight. Read-only reconciliation showed no MR and confirmed the remote branch SHA. The helper retry had the same preflight timeout. A username lookup confirmed a.solonenko, and one direct GitLab API create used the approved payload.

Independent GET confirmed Ready [MR93](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/93), exact title and body, source and target, commit SHA, assignee, squash and source deletion on merge. The MR head pipeline is null, consistent with CI being disabled. Checkout clean and tracks origin. Publication complete. No merge, deployment, or other repository publication. Pilot requires merge and separate deploy permission. No background operations.

### Bootstrap merged, pilot chart dependency checked

User reported merging template MR93. GitLab GET confirmed merged on 2026-11-19 at 14:20:22 Moscow, merge d462f56a3737e0f2b08032d3fce77a342d0befe7, squash 2ea7462ef1fd9ba1b7748ba880b05f627c9ba68e. Remote master and refreshed origin/master both match the merge SHA. Master now contains the dev-single bootstrap, registry and RabbitMQ checks. The geocoder checkout still has the prepared local CI and values changes.

The existing geocoder render comparison proved it uses the same six resources with chart master and the pending runtime configuration changes. The chart MR with command/args and file mounts is still needed for later services, including daily-compilations, and is independent of the geocoder pilot. No chart publication, pilot publication or deploy in this step. No background operations.

### Geocoder publication proposal

User requested preparation of the pilot MR after bootstrap merge. Refreshed geocoder master and confirmed it equals local branch base 328aef3. Index empty, no matching remote branch or open MR. The stored exact two-file patch still matches. Repeated Helm lint and six-resource comparison against chart master and pending chart changes. Read-only GitLab CI Lint with the merged bootstrap template confirms existing tag 1.2.12 exposes manual deploy dev. Shared MR rules retain API build/image publication and unit tests. Manual dev and existing test jobs require play. Production and monitoring release rules do not match MR pipelines.

Prepared Ready MR in youdo/microservices/geocoder: source DevOps-884-geocoder-dev-single, target master, commit `add geocoder dev-single deployment`, title `DevOps-884 add geocoder dev-single deployment`, assignee a.solonenko, squash off and source deletion after merge on. Exact body, diff and bound snapshot are under `/home/slnnk/ai-data/gitlab-workflow/DevOps-884/geocoder/`. Waiting for the second supervised approval. No stage, commit, push, MR, deploy or background operation.

### Geocoder MR published

User confirmed the publication proposal with `Да`. The snapshot matched and staged/committed content matched the approved patch byte-for-byte. CRLF-aware staged whitespace check passed. Created `167988a57af84c6950e1652e4aafcd3502afb40f` (`add geocoder dev-single deployment`) and pushed only DevOps-884-geocoder-dev-single. GitLab readback independently verified Ready [MR57](https://gitlab.youdo.sg/youdo/microservices/geocoder/-/merge_requests/57), exact source SHA, target, title and body, assignee a.solonenko, no squash and source deletion on merge.

GitLab then exposed MR pipeline 143636 for the exact SHA, pending at observation. Jobs build-api, dotnet-unit-tests and deploy dev were created. Dev job 3309644 had not started and is governed by the reviewed manual rule. No merge or deploy performed. The remote pipeline may continue independently and can be checked or cancelled on the GitLab pipeline page if authorized. No local background process remains.

### First geocoder deploy diagnosed

User manually started GitLab job3309644 and supplied its trace. Independent GitLab API read confirmed failed at 14:42:19 Moscow after starting at 14:36:26. Namespace release dev-single is Deployed revision1 in default. Registry VSO condition passed and RabbitMQ Deployment rolled out; read-only Kubernetes confirmed rabbitmq1/1 and geocoder-api0/1. Both application VaultStaticSecrets are Ready and SecretSynced.

The geocoder pod is Pending, container ImagePullBackOff with zero restarts. Warning event reports connection refused for the image pull from msk3-nexus.youdo.corp. The app lost the Helm wait deadline because its image never started. GitLab group variables confirm APP_IMAGE_NAME derives from NEXUS_HOST (msk3-nexus.youdo.corp), while APP_IMAGE_PUBLIC_NAME uses NEXUS_PUBLIC_HOST (nexus.youdo.com). Nomad deploy templates already use APP_IMAGE_PUBLIC_NAME. The generated registry Secret is configured for registry.youdo.sg and nexus.youdo.com. Authenticated HEAD to the exact public Nexus image tag returned HTTP200 and digest sha256:7db7a6c1aed9434103aea492afd01e4aec5d1a144e28d8101e3e8e28060eaec2, exactly the commit-specific manifest digest from build job3309642. No credentials printed or persisted. Public workstation /hc returned301 to youdo.sg; ingress status exists in the cluster, but application and external route acceptance are pending.

Proposed follow-up only: in sysadmins/devops-tools/gitlab-ci-templates on a new DevOps-884-dev-single-public-image branch from master d462f56, use APP_IMAGE_PUBLIC_NAME for dev-single application installs and keep APP_IMAGE_NAME for existing namespaces. Validate the internal/public image selection and reuse of the deployed namespace before a separately approved new pipeline deploy. The failed job consumed the previous template snapshot. No edits, deploy or retry authorized/performed. No background operations.

### Public image fix prepared

After the diagnosis and exact edit proposal, user authorized the change with `Исправь`. Refreshed template master d462f56 and created the agreed DevOps-884-dev-single-public-image branch in the clean existing checkout. In application Helm block only, use APP_IMAGE_PUBLIC_NAME when the namespace is dev-single, with a diagnostic for a missing or empty public image name. Other namespaces use APP_IMAGE_NAME. Bootstrap and CI rules are byte-identical, and image tag and optional digest are preserved. Documented the choice in v3/DEPLOY_HELM.md.

Shell checks verified exact Helm parameters for dev-ai-qa and dev-other, the registry-only delta for dev-single with or without digest, and the early app block failure for a missing public name. Stock chart renders the exact public pilot image. GitLab project CI remains disabled. Compared existing flows at user request: ai-qa defines both IMAGE and IMAGE_PUBLIC as CI_REGISTRY_IMAGE and publishes the digest. The B2B Jenkinsfile constructs nexus.youdo.com/project path directly and passes it as image.registry. geocoder uses the shared Nexus defaults, and existing Nomad jobs already use the public alias.

Exact current patch, proposal and bound snapshot stored under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/gitlab-ci-templates-public-image/. Ready MR proposed DevOps-884 use public image registry for dev-single; commit use public image registry for dev-single; same branch to master, a.solonenko, squash and source deletion on. No staging, commit, push, MR or retry. Waiting for publication approval, then a fresh pipeline deploy needs separate approval. No background operations.

### Uniform public image name direction

User selected migrating ai-qa builds to Nexus and using APP_IMAGE_PUBLIC_NAME for Helm application deployments in every namespace. This supersedes publication of the currently local dev-single-only image conditional. No new code changes authorized or applied in this discussion.

Technical split: first simplify the template on the existing DevOps-884-dev-single-public-image branch from d462f56 to pass APP_IMAGE_PUBLIC_NAME unconditionally, with no namespace-specific image branch. Both ai-qa variables currently equal CI_REGISTRY_IMAGE so this preserves the existing ai-qa image. B2B Jenkins already selects nexus.youdo.com and bypasses the changed CI job. Check all consumers and existing image/tag/digest contract before publication. Then move ai-qa build publication in a separate ai-qa MR, proposed DevOps-884-ai-qa-nexus from d559872: use standard IMAGE and IMAGE_PUBLIC values, reuse common Nexus login and retain build smoke, tag and dotenv digest. The controller and QA_AGENT_IMAGE already get the same image from Helm; the raw deploy utility takes an explicit --image. Verify a Nexus build manifest followed by a separately approved ai-qa rollout and worker image pull. The order can preserve geocoder progress while keeping changes reviewable. Waiting for specific stage approval. The previous local conditional proposal is superseded and remains uncommitted.

### Uniform image template prepared

User replied `делай` after the exact first-step proposal. Checked the previous conditional-stage snapshot and reused its unchanged branch DevOps-884-dev-single-public-image from master d462f56. Replaced the conditional draft with one universal APP_IMAGE_PUBLIC_NAME expansion and a clear error if it is absent. CI rules, bootstrap script, image tag and digest remain unchanged. Documented the shared image input. No changes in ai-qa or Jenkins repositories.

A local workspace search found ai-qa and geocoder as direct consumers. Shell tests confirmed that dev-ai-qa gets identical Helm arguments while dev-single and other namespaces select the public name. Actual Helm renders confirmed identical ai-qa objects including controller and QA_AGENT_IMAGE, plus the exact public Nexus image for geocoder. Diff whitespace and empty index checks passed. There is no cluster redeploy yet. New proposal and snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/gitlab-ci-templates-uniform-image/ about 9.6KB retained for review. Commit `use public images for helm deploys`, Ready MR `DevOps-884 use public images for Helm deploys`, same branch to master, assignee a.solonenko, squash and source deletion enabled. Template project CI disabled. Supersedes the conditional patch publication proposal. No staging, push, MR or deployment. Waiting for publication approval. No background operations.

### Uniform image MR published

User confirmed the exact commit, source/target, title, text and CI effects with `Подтверждаю`. Snapshot matched, staged whitespace passed, and both staged and committed diffs matched the prepared patch byte-for-byte. Pushed commit `e1a3d6ca4399cd0b38a250841809b78dd48408e3` (`use public images for helm deploys`) on DevOps-884-dev-single-public-image only. GitLab readback verified [MR94](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/94), exact title/body/source/target/SHA, Ready, a.solonenko, squash and deletion after merge. The list GET separately confirmed the MR and SHA. Project builds are disabled, and pipeline listing returned HTTP403. No merge or deploy. Geocoder needs a fresh pipeline after this merge. The separate ai-qa Nexus migration remains pending. No background operations.

### Second geocoder deploy observed

User linked GitLab job3309911. Refreshed gitlab-ci-templates master 293b171 contains uniform APP_IMAGE_PUBLIC_NAME. Job used the public Nexus image tag devops-884-geocoder-dev-single-143645, and the pod pulled and started it. Namespace dev-single remained Deployed revision1, RabbitMQ1/1, and both application VaultStaticSecrets were SecretSynced and Ready. This verifies the registry and namespace reuse changes in the live second attempt.

Job ended failed at 15:13:39 Moscow with Helm upgrade context deadline exceeded. Cluster readback showed geocoder revisions1 and2 failed, deployment0/1 and public-image container restarted five times. Previous container termination showed exit134. Kubernetes returned only a CRI-O unable-to-retrieve-container-logs message. The one Loki stream for geocoder in the time window is integrations/docker from the Nomad job, not evidence for the Kubernetes pod. Exact application abort cause remains unknown. Direct Traefik ingress /hc returned503 and public DNS endpoint redirected301 to youdo.sg. No geocoding check because the application was unready. No writes, deployment retry, rollback or background local operations. The Kubernetes controller can continue container restarts; next diagnostic needs runtime logs tied to the new pod and container.

### Geocoder exit 134 root cause verified

User asked for the exact cause and reported the shared Logreader value is incorrect. Read-only Kubernetes log recovery eventually produced the real 25-line startup exception from the public Nexus pod instead of the earlier CRI-O unavailable message. `System.Net.Sockets.SocketException (13): Permission denied` originates in Socket.DoBind, Kestrel CreateDefaultBoundListenSocket and WebHost.StartAsync in GeoCoder.Api.Program.Main. The pod declares port80 without extra capabilities. Authenticated read-only Registry config for the exact deployed tag declares user nonroot:nonroot and `ASPNETCORE_URLS=http://+:80`. Current blocker is Kestrel binding the privileged port, not an SQL exception. The incorrect shared dev/logreader value reported by the user remains a separate issue and was not edited or independently assessed.

Proposed first-gate change: in geocoder reuse DevOps-884-geocoder-dev-single at 167988a (MR57, master base 328aef3) and set `ASPNETCORE_URLS: http://+:8080` and the api component port8080 in devops/dev.yml. Temporary Helm render confirmed Deployment and readiness port8080, Service stays port80 with targetPort8080. No repository change, retry, or Vault mutation. The failed deployment continues to reconcile pods in the cluster. No local background operations.

### Geocoder listener and private ingress prepared

User approved the listener change and selected geocoder.dev.youdo.corp for the only ingress host. Applied on the existing DevOps-884-geocoder-dev-single branch at 167988a, targeting master 328aef3 in MR57. Changed only devops/dev.yml: ASPNETCORE_URLS=http://+:8080, api component port8080, and private host replacing the .sg name. DNS for the .corp hostname already points to private Traefik 10.18.26.60. Helm lint passed. Chart master and prepared chart rendered identically, with readiness8080, Service80 to8080 and only the internal hostname. Shared Logreader unchanged. Prior matching cases are youdo.business dev-107 and youdo.kitcut dev-86. Saved the developer's container-port convention in the dev-deployment map.

Separate approved-object publication proposal prepared, still awaiting confirmation: add commit `fix geocoder port and internal ingress` to existing Ready MR57, preserving title/body, assignee and settings. Patch and bound snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/geocoder-runtime/. Push will trigger the usual MR build and tests. Deploy remains manual and separately approved. Index empty; no commit, push, retry or cluster changes.

User also asked whether the RabbitMQ rollout wait in job3309911 means the broker was recreated. Read-only cluster check: namespace Helm revision1 and RabbitMQ Deployment generation1, revision1. Deployment and only ReplicaSet were created at 14:36:38 Moscow. Current pod rabbitmq-cbbd88fff-27smt was created at 15:06:52 Moscow by that same ReplicaSet. Container start was 15:06:55 and restartCount0. Job3309911 started at 15:07:55, after creation of the current pod. The log's rollout status command waits for availability and did not recreate the Deployment or issue a fresh rollout.

RabbitMQ event follow-up: original pod rabbitmq-cbbd88fff-jdxs5 received ScaleDown and Killing at 15:06:51 Moscow; the same ReplicaSet created the replacement at 15:06:52. The replacement's Ready transition was 15:08:34, after job3309911 had started. This explains the rollout status wait. No new RabbitMQ Helm release revision, Deployment, or ReplicaSet was created by the job. No local background operations.

### Geocoder listener and private ingress published

User explicitly approved publication of the prepared follow-up with `Опубликуй`. Bound snapshot matched. Index contained only devops/dev.yml; staged whitespace and staged and committed patch comparisons passed. Commit `626b264fc749d3f450c7573e675503d390a0d8ea` (`fix geocoder port and internal ingress`) was pushed to DevOps-884-geocoder-dev-single. GitLab verified existing MR57 source, target, exact new SHA, unchanged title/body and settings. The new MR pipeline143656 was running on readback. Job-details endpoint timed out on a separate optional query. No deploy job was played and no merge performed. The pipeline remains remote and can be viewed or cancelled in GitLab. Local checkout clean with no running command.

### Geocoder pilot passed on the third deploy

User linked job3310062. Independent GitLab status Success at 15:29:09 Moscow after 38 seconds. Helm reported geocoder revision3 Deployed in dev-single. Read-only cluster confirmed geocoder-api1/1 Ready, its public Nexus image from MR pipeline143656, zero restarts, and only the .corp ingress. Both geocoder VSO resources are SecretSynced and Ready. RabbitMQ1/1 and namespace release dev-single remained Deployed revision1. This is live evidence that the application redeploy reused the namespace release.

Internal http://geocoder.dev.youdo.corp/hc returned200. One search request for a public landmark via internal API returned HTTP200 and one result. The public .sg URL returned fallback301 to youdo.sg. This completes the pilot acceptance checks. Functional Logreader was not tested. No publication, merge, deployment initiation or other external changes by the agent. No background diagnostic operations remain. DevOps-884 overall and the ai-qa/Helm proposals remain open.

### Nonblocking manual dev deploy proposal

User reported deploy dev should not block other stages and explicitly selected allow_failure true so dev does not affect pipeline success. GitLab job3310071 (tag1.2.13, pipeline143657) succeeded but actual job metadata shows allow_failure false. The shared v3/.deploy-helm.yml sets manual via rule references and currently omits allow_failure. Existing test deploy jobs already set allow_failure true. GitLab documents that rule-defined manual jobs default to blocking and that an explicit true enables optional jobs.

Proposed first gate: sysadmins/devops-tools/gitlab-ci-templates, new DevOps-884-nonblocking-dev-deploy branch from master293b171. Add allow_failure true only to deploy dev in v3/.deploy-helm.yml. Retain MR/semver/master rules by service mode, artifact flow, namespace bootstrap, and all test/prod settings. Check CI lint for the manual job flag and equivalent rules and validate on a fresh pipeline that skipping or failing dev does not gate later stages. Job3310071 was success; a separate user-started deploy vk-test was running at the time of inspection. No edits, kicks or publication. Stage awaits explicit edit approval.

### Optional deploy dev prepared

User authorized the exact implementation stage with `Добавь, опубликуй мр`. Created DevOps-884-nonblocking-dev-deploy from refreshed master293b171 and added a single line allow_failure true only on deploy dev in v3/.deploy-helm.yml. Byte comparison confirmed all other template content is identical. Read-only GitLab CI lint simulated geocoder tag1.2.13 with the one-key job override and confirmed effective allow_failure true for the still manual deploy dev, with identical job names/stages/when. Real scheduling while dev runs remains untested. git diff --check passed and index is empty. GitLab project CI remains disabled, default squash and branch removal enabled, no matching open MR.

Publication proposal is Ready MR `DevOps-884 make dev deploy optional`, commit `make dev deploy optional`, source DevOps-884-nonblocking-dev-deploy and target master, assignee a.solonenko. Actual patch, body and bound snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/gitlab-ci-templates-nonblocking-dev/. Waiting for the required exact publication confirmation. No staging, push, MR or new deployment. No local background commands.

### Optional deploy dev MR published

User approved the exact publication proposal with `Да`. Bound snapshot matched, staged diff contained exactly one insertion, staged whitespace passed, and staged and committed patches matched the reviewed diff. Pushed `19c1424a5f48b12954bedb70a62717be8af296b6` (`make dev deploy optional`) to DevOps-884-nonblocking-dev-deploy. GitLab verified Ready [MR95](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/95), exact title/body/source/target/SHA, a.solonenko, squash and source deletion on merge. GitLab pipeline listing returned HTTP403 for the CI-disabled template project. No merge, fresh consumer pipeline, or deployment initiated. Actual scheduling acceptance remains after merge. Checkout clean; no local background work.

### Optional dev deploy and pilot merge verified

User reported merging the optional dev deployment change. GitLab GET confirmed MR95 merged at 15:42:05 Moscow and refreshed master equals 17d15809d9b109a1cf4e6726c3459a7be7938d79 with deploy dev allow_failure true. Geocoder MR57 is also merged at ad7aaa9e. Tag1.2.13 pipeline143657 is manual after the successful dev job and is older than the template fix. Verify the optional job on the next normal fresh consumer pipeline. No extra release, pipeline or deployment requested or triggered.

The next chart publication remains one helm-charts MR for the two prepared local diffs, subject to refreshing checks and second approval. The ai-qa Nexus migration and downstream service onboarding remain separate. No local background work.

### Candidates using chart master

After the geocoder pilot, user asked which other services can be onboarded using the current microservice chart. Rechecked local master sources for v3 CI/image layout and existing chart image override. Closest candidates: BlackListedEmailChecker (single ASP.NET component, use port8080 and valid readiness, outbound domain list and writable cache), tinkoff-e2c-sign-service (single Node component with configurable PORT and existing signing-file path), and pechkin (single Node component, existing unsubscribe link dependency). Additional chart-ready candidates: chat-content (two component images and S3), youdo-business-doc-generator (existing dev.yml and S3, retain/coordinate its existing Jenkins flow), and userinsurance-gotenberg (pinned upstream image via existing service.image, internal address and PDF smoke). The router and mocks can fit the chart but require callback ordering or legacy CI/Host work. No implementation, rollout or new scope selected. No background operations.

### BlackListedEmailChecker edit proposal

User requested publishing the next pilot MR. Local master is clean and refreshed at 3a23a85, correct project youdo/BlackListedEmailChecker. Proposed branch DevOps-884-blec-dev-single from origin/master, remote name available. Add only the existing manual Helm job include and devops/dev.yml for fixed release blec in dev-single, component web matching APP_SERVICE, explicit non-root ASP.NET 8080 listener and TCP readiness, internal blec.dev.youdo.corp ingress, and writable /tmp file settings for exact and suffix domain caches. The current private DNS resolves to the internal Traefik IP. Service refreshes raw.githubusercontent.com lists on startup in its current code. No application database or Vault secret is indicated. Preserve v3 manual release flow and existing test/prod jobs. Verify Helm, CI Lint and internal blocked/allowed fixtures after the first download. Existing chart master suffices. Waiting for first-stage approval of the exact code scope. No repository edits, publication, deploy or background operations.

### BlackListedEmailChecker MR prepared

After confirming that current source and both Nomad configs use no application secrets, the user authorized preparation with `Подготовь мр`. Created DevOps-884-blec-dev-single from refreshed master3a23a85. Only .gitlab-ci.yml and devops/dev.yml changed, preserving all existing CI bytes and line endings apart from one include. Added web component port8080, explicit ASPNETCORE_URLS, TCP readiness, /tmp cache paths and blec.dev.youdo.corp. Preserved CPU100m and memory512Mi from the Nomad spec. Current chart master and pending chart changes render byte-identical. Helm lint and diff whitespace passed.

Read-only GitLab CI Lint for tag1.0.2 showed 13 existing jobs unchanged and one new manual optional deploy dev. Comparison for master unchanged. Shared MR rules match existing build and .NET tests; dev/test jobs remain manual. No real build, upstream fetch or rollout check. GitLab project129 confirmed no matching MR, squash off and recent source removal on merge true. Prepared Ready publication proposal with commit `add blec dev-single deployment`, title `DevOps-884 add blec dev-single deployment`, source DevOps-884-blec-dev-single to master, assignee a.solonenko. Exact body, actual diff and bound snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/BlackListedEmailChecker/. Awaiting exact publication approval. No stage, commit, push, MR or deploy. No background operations.

### BlackListedEmailChecker MR published

User confirmed the exact publication proposal with `Да`. Snapshot matched. CRLF-aware staged whitespace check passed; staged and committed patches matched the reviewed actual diff byte-for-byte. Pushed commit `a4eac923f0da9b42ca0df4b797fed183a7105167` (`add blec dev-single deployment`) only to DevOps-884-blec-dev-single. GitLab independently verified Ready [MR6](https://gitlab.youdo.sg/youdo/BlackListedEmailChecker/-/merge_requests/6), exact source/target, SHA, title/body, assignee a.solonenko, squash off and branch removal on merge.

GitLab returned MR pipeline143664 running for the exact SHA. build-web, dotnet-unit-tests and deploy dev were created. Actual deploy dev job3310270 has allow_failure true, proving the merged template flag is effective in the new consumer MR pipeline. No deploy started or merge performed. Remote pipeline can be inspected/cancelled from GitLab; local checkout is clean and no local background operation remains.

### BlackListedEmailChecker .NET 2.1 base images

User asked whether internal equivalents exist for BLEC base images. Application CI still uses mcr.microsoft.com/dotnet/core/sdk:2.1 and mcr.microsoft.com/dotnet/core/aspnet:2.1. Refreshed base-images master f898137 contains microsoft/dotnet-sdk/2.1 and microsoft/dotnet-aspnet/2.1 Dockerfiles, pinned to Microsoft's corresponding .NET 2.1 upstream image digests. Both release tags are present, and docker manifest inspect succeeded for registry.youdo.sg/youdo/base-images/microsoft/dotnet-sdk:2.1 and microsoft/dotnet-aspnet:2.1. Manifest access only, no layer pulls, images or configuration changes. No switch requested, no background work.

### BLEC base images follow-up prepared

After reviewing the two exact internal image paths, user requested switching them in the same MR. Confirmed MR6 open at a4eac92, branch matches and master remains3a23a85. Reused DevOps-884-blec-dev-single and changed only DOTNET_BUILD_IMAGE and DOTNET_BASE_IMAGE in .gitlab-ci.yml, preserving CRLF. Both tags stay2.1. Verified both internal manifests without pulling layers. GitLab CI Lint for tag1.0.2 merged config differs only in the two names, jobs and master behavior unchanged. Whitespace check passed and index empty. No real build or deploy of this follow-up.

Prepared exact existing MR6 update proposal: commit `use internal dotnet base images`, same branch to master and same title/settings; append a sentence to the existing MR body documenting the source. The patch, proposed body and bound snapshot are in /home/slnnk/ai-data/gitlab-workflow/DevOps-884/BlackListedEmailChecker-base-images/. Push triggers usual MR build and tests, no auto deploy. No staging, commit, push or MR update yet. Waiting for exact publication approval. No local background operations.

### BLEC internal images published and deploy verified

User confirmed the base-image publication proposal with `Да`. Snapshot matched; staged and committed patches matched the reviewed CRLF-preserving two-variable diff. Pushed `cd6ddb2b278dc0f5a6de3b1626c6354b1e7af31a` (`use internal dotnet base images`) on the existing MR6 branch. The helper API preflight and first direct description update timed out. Readback confirmed the old body before the approved retry. The retry and independent GET confirmed the exact new approved description and SHA, with title and MR settings unchanged. Pipeline143671 was running when checked and deploy dev remained optional.

User then linked job3310289. GitLab confirmed Success at 16:10:16 Moscow, 45 seconds, blec namespace dev-single revision1 Deployed. Read-only cluster shows blec-web1/1 Ready with zero restarts and only blec.dev.youdo.corp ingress. The namespace Helm release dev-single stayed at revision1. Functional internal API returned HTTP200 and true for synthetic@mailinator.com and HTTP200 and false for synthetic@example.org, demonstrating populated effective domain lists. The agent made no deployment operation and no merge. No local background processes remain.

### Tinkoff signing service edit proposal

User asked to prepare the next pilot MR. Confirmed clean existing checkout, refreshed master5daa847, correct project youdo/microservices/tinkoff-e2c-sign-service and available branch name DevOps-884-tinkoff-sign-dev-single. Propose changing only .gitlab-ci.yml and a new devops/dev.yml. Add v3/.deploy-helm.yml, configure fixed release tinkoff-e2c-sign-service in dev-single, component web matching the current image path, env PORT=8080, HTTP /health readiness and one internal ingress tinkoff-e2c-sign-service.dev.youdo.corp. DNS already resolves to private ingress 10.18.26.60. Preserve Nomad resource sizing and inherited manual CI release rules. Image Dockerfile copies repository files to /app and the application defaults to the existing signing file path. Only file location was checked, never key contents; no key, Vault or Dockerfile change proposed. Verify Helm lint/render and CI Lint before publishing, and perform separately authorized rollout validation with test signing material. Waiting for exact branch/base/edit approval. No repository edits, publication, deploy or background operations.

### Tinkoff signing service MR prepared

User confirmed the proposed first edit stage with `Да, опубликуй мр потом`. Refreshed master5daa847; created DevOps-884-tinkoff-sign-dev-single from the agreed base. Changed only .gitlab-ci.yml (one shared Helm include with original line endings) and devops/dev.yml (fixed single web release, PORT8080, /health, 500m CPU and 256Mi memory, internal tinkoff-e2c-sign-service.dev.youdo.corp). Checked the existing signing file path without reading key contents. No key or image-source changes.

Helm lint and render comparison passed using both current chart master and pending chart changes. GitLab CI Lint on semver0.0.10 confirmed nine prior jobs identical plus optional manual deploy dev, and master simulation unchanged. CI build-web will publish an MR image; NODEJS_UNIT_TESTS remains false. No runtime or signing check, no stage or push. Prepared Ready MR `DevOps-884 add tinkoff signer dev-single deployment` with commit `add tinkoff signer dev-single deployment`, source DevOps-884-tinkoff-sign-dev-single to master, assignee a.solonenko, squash off and branch removal on merge. Exact diff/body and bound snapshot are under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/tinkoff-e2c-sign-service/. Waiting for exact publication confirmation. No background operations.

### Tinkoff signing service MR published

User approved the exact publication proposal with `Да`. Snapshot matched, staged whitespace and bytes verified, and committed patch was identical to the accepted review patch. Pushed commit `bc73e231798709ca3ecda5a1e21e7b2d48c2ef6e` (`add tinkoff signer dev-single deployment`) only on DevOps-884-tinkoff-sign-dev-single. GitLab confirmed Ready [MR13](https://gitlab.youdo.sg/youdo/microservices/tinkoff-e2c-sign-service/-/merge_requests/13), exact body/title/SHA and branches, a.solonenko, no squash and delete source on merge. MR pipeline143678 was running, with build-web3310440 and optional deploy dev3310441 created. No merge, deploy or signing request. Pipeline can be checked or cancelled in GitLab. No local background operations.

### Tinkoff signing service deploy verified

User linked job3310441. GitLab confirms Success at 16:57:34 Moscow after 89 seconds and tinkoff-e2c-sign-service Helm revision1 Deployed. Read-only Kubernetes showed 1/1 Ready, pod Running with zero restarts, only internal tinkoff-e2c-sign-service.dev.youdo.corp ingress, and shared dev-single release still revision1. Internal /health returned HTTP200. No signing request was sent, so functional signing and consumer verification are still untested. No external changes or local background operations by the agent.

### Pechkin edit proposal

User asked to prepare the next MR. Refreshed clean checkout base master78a4776, project youdo/mail/pechkin, proposed branch DevOps-884-pechkin-dev-single is available. Scope is .gitlab-ci.yml (existing v3 manual Helm job include) and devops/dev.yml (web component in dev-single, PORT8080, production=0, HTTP / readiness as in Nomad, three replicas and per-pod CPU/memory matching the current Nomad job, internal pechkin.dev.youdo.corp resolved to private Traefik). Existing templates and tag/build/test/production job eligibility are preserved. Current microservice chart supports this service.

The current stand unsubscribe generator URL is hardcoded and was unresolved from the workstation DNS during the planning check. Cluster reachability and unsubscribe rendering remain distinct acceptance checks. The initial proposal leaves the application endpoint contract unchanged. If runtime evidence confirms the need to replace it, scope an endpoint override separately. No repository work or deployment has started. Waiting for exact first-stage approval. No background operations.

### Pechkin MR prepared

User confirmed exact first-gate edits with `Да`. Created DevOps-884-pechkin-dev-single from refreshed master78a4776 in the existing clean checkout. Actual diff only adds the Helm include and devops/dev.yml. Values keep production=0, existing three replicas and resource sizing (1000m, 512Mi), PORT8080, / readiness and internal pechkin.dev.youdo.corp ingress. No application source change. Helm lint passed and chart master and pending chart output matched byte-for-byte. GitLab CI Lint on tag2.14.24 showed all 11 original jobs unchanged plus optional manual deploy dev; master unchanged. Diff whitespace passed, index empty. No runtime template or unsubscribe link check yet.

Prepared Ready MR `DevOps-884 add pechkin dev-single deployment`, commit `add pechkin dev-single deployment`, branch DevOps-884-pechkin-dev-single to master, assignee a.solonenko, squash off and source deletion on merge. Actual diff, approved candidate body and bound snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/pechkin/. Opening MR is expected to build and publish its image; existing NODEJS_UNIT_TESTS false, deploy manual. Waiting for publication confirmation. No staging, commit, push, deployment or background operations.

### Pechkin CPU resource correction

User specified leaving both CPU limits and CPU requests at the defaults for dev services. The original Pechkin draft copied the Nomad CPU amount as a request; it had no CPU limit. Removed the explicit request after clarification. Updated the canonical dev-deployment map and learning rule. Current Helm render has neither CPU request nor limit, with 512Mi memory request/limit, three replicas, port8080 and private ingress. Chart master and pending chart render identically. Helm lint and diff whitespace pass; CI file still exactly matches the previous already-linted one-line include. The updated actual diff and bound `proposal-no-cpu.json`/`snapshot-no-cpu.json` replace the earlier publication snapshot. Merge request title, body and source/target remain as proposed. No stage, commit, push, deploy or background operations. Awaiting publication approval.

### Pechkin MR published

User authorized publishing the no-CPU proposal with `Публикуй`. Latest snapshot matched. CRLF-aware staged whitespace passed, and staged/committed bytes matched the reviewed no-CPU diff. Pushed `7d1eaf253c2423fde8f4e2acfe6848feedd6ef1e` (`add pechkin dev-single deployment`) only to DevOps-884-pechkin-dev-single. GitLab verified Ready [MR238](https://gitlab.youdo.sg/youdo/mail/pechkin/-/merge_requests/238), exact source/target/SHA/title/body, assignee a.solonenko, squash off and deletion after merge on. The matching MR pipeline143692 was pending; build-web3310880 and deploy dev3310881 created, with allow_failure true for the deploy. No merge or deploy started. Remote pipeline can be viewed or cancelled in GitLab. No local background commands.

### Pechkin deploy port mismatch diagnosed

User linked job3310881. GitLab confirmed failed at 17:38:04 Moscow with context deadline exceeded. Kubernetes had all three web containers running with zero restarts but 0/3 Ready and connection refused on readiness. Live pechkin-env ConfigMap has PORT8080. Logs from two pods both reported listening on 3005. The local exact MR SHA uses npm start in the existing Dockerfile, and package.json start explicitly sets PORT=3005 via cross-env. This overrides the Helm-provided value. Application code falls back to 3005 naturally when PORT is unset. Shared namespace dev-single remains Deployed revision1 and RabbitMQ1/1; pechkin release revision1 is failed.

Proposed follow-up first gate: in youdo/mail/pechkin reuse DevOps-884-pechkin-dev-single at 7d1eaf2, existing open MR238 targeting master base78a4776. Remove only PORT=3005 from package.json scripts.start, keeping NODE_ENV and npm run server. This restores environment-based port selection while preserving the existing 3005 default. Require new build and separately approved deploy, then validate readiness and test template rendering. No source edit, MR change, deploy or retry performed. No local background operations.

### Pechkin values-only port follow-up prepared

User chose the values-only solution after the port mismatch diagnosis and authorized the exact edit with `Сделай и опубликуй`. Reused the existing branch DevOps-884-pechkin-dev-single at 7d1eaf2, target master78a4776. Changed only devops/dev.yml by removing PORT and setting component port3005 to match npm start. Helm lint and both chart renders passed. Service80 targets3005, readiness path / port3005, internal ingress and three replicas verified, CPU defaults and memory unchanged. GitLab GET confirmed MR238 still open at the baseline with original title and body. No app/CI modification or live retry.

Prepared exact update proposal with `match pechkin helm port to application` for existing Ready MR238, preserving its title and body. Actual diff, proposal and bound snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/pechkin-port/. Push triggers the existing MR build, optional manual deploy. Awaiting separate exact publication approval. No stage, commit, push, deploy or background operations.

### Pechkin port follow-up published

User confirmed the exact existing-MR update with `Да`. Snapshot matched, the staged/committed patch matched the reviewed diff byte-for-byte, and staged whitespace passed. Pushed commit `ee10032f9777130eb0aa9939a101f9a689c2814b` (`match pechkin helm port to application`) to DevOps-884-pechkin-dev-single. GitLab confirmed [MR238](https://gitlab.youdo.sg/youdo/mail/pechkin/-/merge_requests/238) exact SHA and unchanged metadata. Pipeline143693 running, build-web3310885 running, manual optional deploy dev3310886 created. No deployment or merge by the agent. GitLab pipeline is the only remote work in progress; local checkout clean with no active local commands.

### Pechkin dev deploy verified

User linked job3310886. GitLab confirms Success at 17:47:44 Moscow after 154 seconds. Helm release pechkin revision2 Deployed. Kubernetes showed all three web pods Ready, zero restarts, public Nexus image from pipeline143693 and only internal pechkin.dev.youdo.corp ingress. RabbitMQ1/1 and shared dev-single remained on Deployed revision1. Internal root returned HTTP200 and the GET sample BusinessEmailConfirmation v1 rendered valid HTML with HTTP200. No message was sent.

Source follow-up corrected the earlier dependency assumption: generatorRoutes._getTplParams calls UnsubscribeLink.getLink only when config.isProd and the default layout are selected. The deployed production=0 mode does not use that external generator for the tested preview. Its legacy DNS status is not an acceptance blocker for this preview. No agent-initiated deployment or other external change, no background operations.

### Chat-content edit proposal

User asked to prepare the next MR. Refreshed clean checkout at master f47a22b, project youdo/chat-content, branch DevOps-884-chat-content-dev-single is available. Proposed edits only .gitlab-ci.yml and devops/dev.yml: add shared manual Helm deploy, stable chat-content release in dev-single, uploader and downloader component names matching current build artifacts, existing listener18180 and /debug/vars readiness, 1Gi memory per component and CPU chart defaults. Internal chat-content-uploader.dev.youdo.corp and chat-content-downloader.dev.youdo.corp resolve to the private ingress. Preserve existing custom build and manual release rules. Chart master already supports both Deployments.

Read-only VK test Vault check found S3ACCESSKEYID, S3ACCESSKEY, S3ENDPOINT and S3BUCKET nonempty at the legacy Nomad source secret/dotnet/chat-content and 404 at secret/dev/projects/chat-content. Proposed dev.yml reference targets the dedicated dev path. Copying the four existing test fields into that path requires separate explicit external-write approval. No values printed, no provision, repo edit, publication or deployment. Exact first edit gate awaits approval. No background operations.

### Chat-content configuration prepared and Vault verified

User approved the scoped edits and exact dev Vault write with `Создай секреты в vault dev/projects/chat-content, и опубликуй мр`. Created DevOps-884-chat-content-dev-single from refreshed master f47a22b. Only .gitlab-ci.yml (one include, existing line endings) and devops/dev.yml changed. The values render the two existing images on18180 with /debug/vars, internal .corp hosts, 1Gi memory and CPU defaults. The shared app VaultStaticSecret maps the exact four keys. Helm lint, exact render comparison and whitespace check pass; index empty. CI Lint 1.1.16 preserves 11 previous jobs and adds one optional manual deploy dev; master simulation unchanged.

Verified all source fields nonempty in VK test secret/dotnet/chat-content and confirmed destination absent before the approved write. One POST to secret/dev/projects/chat-content returned HTTP204. Independent readback matched exactly the four authorized S3 fields. No secret values printed or stored in local artifacts. No app deployment or S3 object operations.

Prepared Ready MR publication proposal for youdo/chat-content: branch DevOps-884-chat-content-dev-single to master, commit `add chat-content dev-single deployment`, title `DevOps-884 add chat-content dev-single deployment`, a.solonenko, squash off and branch removal on merge. Opening MR builds and publishes both images; dev deployment stays manual. Exact diff/body and bound snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/chat-content/. Awaiting second-stage publication approval. No stage, commit, push or MR. No background operations.

### Chat-content MR published

User confirmed the exact publication proposal with `Да`. Snapshot matched, CRLF-aware staged whitespace passed, and the staged/committed diff matched the reviewed patch. Pushed `c02f1a5d8ac740909cd7441ed389515e0d501e56` (`add chat-content dev-single deployment`) only to DevOps-884-chat-content-dev-single. GitLab verified Ready [MR14](https://gitlab.youdo.sg/youdo/chat-content/-/merge_requests/14), exact title/body/source/target/SHA, a.solonenko, squash disabled and source deletion on merge. Matching MR pipeline143695 was running, build3310921 running and optional deploy dev3310922 created with allow_failure true. No merge, deployment or S3 test. Pipeline can be checked or cancelled in GitLab. Local checkout is clean and no local background operations remain.

### Chat-content first deployment checked

User linked job3310922. Job started 18:36:59 and failed at 18:42:15 Moscow, Helm context deadline exceeded. Uploader initially served internal /debug/vars HTTP200. Downloader required1Gi and scheduler reported insufficient memory on all three workers. Kubernetes requested autoscale3 to4; only three nodes were registered at 18:41:37 and downloader was still Pending. Namespace release dev-single was Deployed revision1 and RabbitMQ ready throughout; app VSO SecretSynced and Ready.

After failure, read-only checks observed four Ready nodes, both uploader/downloader Deployment1/1 and zero restarts. Each /debug/vars returned JSON through the Kubernetes Service proxy. App Helm release chat-content revision1 remains failed despite current pod readiness. Private ingress checks from the workstation timed out for both chat-content names and also for a geocoder control request, so ingress response was not verified in the final observation. No object uploaded or downloaded from S3; no retry/deploy initiated by the agent. No background job or local operation remains.

### Seven-minute Helm timeout edit proposal

User requested increasing dev deploy timeout from 5 to 7 minutes after chat-content readiness arrived after autoscaling. Refreshed shared template master17d1580 and confirmed DEV_HELM_TIMEOUT:5m. The existing variable is passed to Helm namespace/app waits and readiness waits for registry, RabbitMQ and PostgreSQL. Proposed first gate: sysadmins/devops-tools/gitlab-ci-templates, new DevOps-884-dev-helm-timeout from origin/master17d1580, change only the default DEV_HELM_TIMEOUT to 7m in v3/.deploy-helm.yml. Validate the one-line diff and effective CI value; no new cluster or deployment work. Awaiting edit approval. No repository edits or background operations.

### Seven-minute Helm timeout prepared

User approved the exact edit with `Сделай`. Created DevOps-884-dev-helm-timeout from refreshed master17d1580. Only v3/.deploy-helm.yml default DEV_HELM_TIMEOUT changed from5m to7m; byte comparison verified other content is identical. GitLab CI Lint simulated chat-content tag1.1.16 using the new effective default, all remaining merged YAML identical and manual optional deploy present. Whitespace check passed and index empty. No live deploy.

Prepared Ready MR proposal `DevOps-884 increase dev Helm timeout`, commit `increase dev helm timeout`, source DevOps-884-dev-helm-timeout to master, assignee a.solonenko, squash and source deletion on merge. CI-disabled project means no job or deploy on publication. Reviewed diff, body, proposal and bound snapshot retained under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/gitlab-ci-templates-dev-timeout/. Awaiting publication confirmation. No stage, commit, push or background operations.

### Seven-minute Helm timeout MR published

User approved the exact publication proposal with `Да`. Bound snapshot matched, and staged/committed diff and whitespace check passed. Pushed `c7677171f048f21febc379280b78839c119ad0db` (`increase dev helm timeout`) only on DevOps-884-dev-helm-timeout. GitLab confirmed Ready [MR96](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/96), exact title/body/source/target/SHA, a.solonenko, squash and removal after merge. Pipeline listing returned HTTP403 for the CI-disabled template project. No merge, new consumer pipeline or deploy started. Checkout clean; no local operations remain.

### ai-qa namespace scope

User clarified on 2026-11-19 that ai-qa is intended to remain in dev-ai-qa. This supersedes the earlier proposal to move its controller, state and routes into dev-single. The previous 19-item inventory comprised 18 shared rollout targets and ai-qa. Five of the 18 have prepared MRs, and four have successful dev-single deployments. Chat-content workloads became Ready after its Helm job timed out, so ingress and S3 acceptance remain open. The proposed separate Nexus image publication change for ai-qa still uses dev-ai-qa; this clarification grants no edit or rollout approval. Updated active plan, system summary and the central backlog. No runtime changes or background operations.

### Proposed next five outside GitLab Data

User prefers the next batch outside the GitLab data group. Proposed order: userinsurance-gotenberg (pinned converter only), youdo-business-doc-generator (reuse service values and preserve Jenkins compatibility), taskqualitycontrol (the sysadmins test mock and tagged/MR image handoff), HoustonV2Mock (mock ingress preserving per-stand Host fixture isolation), escrow-tinkoff-router (router subimage and test callback routing). All fit the stock microservice chart without app DB/migrations. This is batch selection for review, not an edit or rollout approval. No infrastructure or repository changes, no background operations.

### Gotenberg shared dependency and C2C userinsurance design

User specified that userinsurance itself will use a B2B-like ephemeral deployment in the C2C group. Keep the application's per-stand lifecycle and the shared converter's lifecycle independent.

Propose a Gotenberg-only values file devops/gotenberg-dev.yml and the existing manual Helm job in youdo/vsk/youdo.userinsurance with a job-scoped DEV_HELM_VALUES_FILE. Keep devops/dev.yml for the future C2C userinsurance deploy. The current Nomad Gotenberg image is gotenberg/gotenberg:8.21.1. A stock-chart render produced only Deployment and ClusterIP Service, fixed release userinsurance-gotenberg plus component api, /health on3000, and Service80 to3000. Same-cluster clients can use http://userinsurance-gotenberg-api.dev-single.svc.cluster.local. The full services[].image override preserves the explicit pinned image regardless of ordinary application image/tag arguments.

Wire Policy__GotenbergServiceUrl for the future C2C API/worker/scheduler via their dev values, reusing the existing configurable key. Confirm C2C uses the same dev cluster before selecting Service DNS. Existing Nomad stage/prod job definitions have their own Gotenberg release logic. Check conversion of a test policy from one C2C namespace and verify creation/destruction of a second C2C stand does not change the shared converter release revision. No current C2C-specific template entry was found in the two inspected CI repos. This is a design proposal and temporary render only. No repo or external changes; no background operations.

### Escrow router shared dependency and C2C escrow design

User extended the same placement decision to escrow.tinkoff and escrow-tinkoff-router. Keep escrow.tinkoff ephemeral in the C2C catalog, and deploy the router separately in dev-single, using an independent values file and optional manual Helm job in the same repository. The current build-router produces the /router image. A stock-chart temporary render using the explicit full component image, ASPNETCORE_URLS8080 and /hc yielded ConfigMap, Deployment and a ClusterIP Service http://escrow-tinkoff-router-api.dev-single.svc.cluster.local. A same-cluster C2C consumer sets Router__Url to that address.

Existing code caches route registrations by request key for eight hours in the process. Keep a single serving router instance for the test flow and verify that both registration and the Tinkoff test callback reach that same router and route to the intended stand. Determine the callback network route before switching test consumers; existing Nomad test and production routes are part of the current lifecycle. Include two C2C fixtures to check independent request keys and routing. No application, CI or infrastructure change; this is a design and temporary render only. No background operations.

### Custom shared dependency job names verified

User asked whether the shared jobs can be named deploy dev gotenberg and deploy dev router. Tested the repository-local GitLab CI composition without editing files: include the existing v3/.deploy-helm.yml, suppress its visible deploy dev alias in that project with rules when never, and create the named job extending the shared job with its own MR/manual release rule references and DEV_HELM_VALUES_FILE for the dependency. CI Lint simulations on userinsurance0.0.69 and escrow.tinkoff13.8.12 retained all39 and40 existing jobs respectively and added exactly one optional manual job with the proposed name. Shared template and chart require no changes for this design. The future C2C jobs can remain separate. No repository edits, pipeline trigger, deploy or background operations.

### Gotenberg and Escrow shared deployment edit proposals

User requested separate MRs for both shared dependencies, Ingress for both, and private plus public entrypoint t-escrow-router.dev.youdo.sg for Escrow. User explicitly excluded values for the main C2C applications. Refreshed repo bases: youdo/vsk/youdo.userinsurance master397ed0c, youdo/microservices/escrow.tinkoff master3ceb86f; existing checkouts clean and proposed branches available. Proposed first gates: DevOps-884-gotenberg-dev-single and DevOps-884-escrow-router-dev-single. In each application repo only add the named optional manual job and its dedicated devops/gotenberg-dev.yml or devops/router-dev.yml. Use existing microservice chart, private userinsurance-gotenberg.dev.youdo.corp and t-escrow-router.dev.youdo.corp, CPU defaults, existing component images/ports and readiness. Router uses the /router build, ASP.NET8080, one replica with Recreate appropriate to its process-local routes. Main devops/dev.yml and C2C catalog remain outside scope.

Independent read-only review confirmed the router registration controller has no local authentication attribute or configured auth middleware. Its public callback paths and private registration must be separated. The chart applies the same path to all hosts. Current public hostname resolves to the public edge and HTTPS returned301 to youdo.sg. Refreshed sysadmins/automation-services master60fc7e85 inventories/yandex/group_vars/balancers_test has explicit public dev vhosts routed to traefik.dev.youdo.corp but no t-escrow-router host. Recommended keep the Kubernetes router Ingress private and configure an explicit public nginx vhost in a separate edge MR. Allow only the four GET callback paths and two POST notification paths, with fixed private upstream Host and preserved path/query/body. Validate no public access to route registration, then prove a sandbox callback for a newly registered route reaches its intended C2C stand. Current Nomad routes and banking sandbox endpoint selection are separate rollout concerns. No confirmed public router flow existed at planning time.

Await explicit approval for the two application changes and, separately, the public edge scope. No code, pipeline, router or infrastructure edits performed, no deployments or active background reviewer.

### Gotenberg and Escrow router service MRs prepared

After the exact two service proposals and public edge separation, user requested preparation with `Подготовь МР`. Created agreed branches DevOps-884-gotenberg-dev-single from 397ed0c and DevOps-884-escrow-router-dev-single from 3ceb86f. In each repo changed only .gitlab-ci.yml and the dedicated dependency values file. Both named jobs inherit shared deploy dev, retain its optional/manual eligibility and select their dedicated DEV_HELM_VALUES_FILE. The generic job is suppressed locally. Main C2C values remain outside scope.

Gotenberg uses gotenberg/gotenberg:8.21.1 with port3000 and /health on userinsurance-gotenberg.dev.youdo.corp. Router uses the /router built component, ASP.NET8080, Staging env, one replica with Recreate and /hc on t-escrow-router.dev.youdo.corp. Both follow CPU defaults; memory follows the existing Nomad sizing. Helm lint and identical stock/pending chart render checks passed for both. GitLab CI Lint retained all39 job definitions on userinsurance tag0.0.69 and all40 on escrow tag13.8.12, adding only the respective named optional manual dev job. Master simulations unchanged. Whitespace passed and both indexes empty.

Prepared two Ready publication proposals with exact diffs, body and bound snapshots under /home/slnnk/ai-data/gitlab-workflow/DevOps-884/youdo.userinsurance/ and escrow.tinkoff/ (20KiB allocated each). Commits `add gotenberg dev-single deployment` and `add escrow router dev-single deployment`, each with DevOps-884 MR title prefix to master, a.solonenko, squash off and source deletion on merge. Publishing runs existing MR builds, no deployment. The public Escrow entrypoint needs the separately approved edge change; these two service diffs contain internal ingress only. No commits, publication, runtime changes or background operations. Awaiting both publication confirmations.

### Escrow public Host routing clarification

User explained the public proxy forwards the original Host to Traefik, which selects the Service by that host. Current router-dev.yml still has only the .corp ingress host, as prepared in the prior split. A temporary stock-chart render with the requested .sg host showed both names route / Prefix. For the clarified topology, propose adding t-escrow-router.dev.youdo.sg to the router MR values, and preserving that Host on the external Nginx callback-only vhost. Access to registration stays private. This supersedes rewriting the public request Host to .corp in the earlier edge proposal. No new chart changes needed if the edge allowlists callbacks and notifications. The new host is not yet in the checkout, and no Nginx or external change has been applied. Awaiting explicit approval on this material source tweak. No local background operations.

### Escrow router public Host added to local draft

User authorized adding the public host to the router values and requested publication with `Да и опубликуй МР`. Checked the earlier private-only bound snapshot, then added t-escrow-router.dev.youdo.sg as the second ingress host on the existing uncommitted DevOps-884-escrow-router-dev-single branch. Helm lint passed; stock/pending renders are identical. Both host rules route the same Service at80 to the same single Recreate router on8080. CI file matches the already-linted custom job draft exactly. Whitespace check passed; index empty. Main C2C values remain out of the patch.

Refreshed exact Ready MR proposal DevOps-884 add escrow router dev-single deployment, commit add escrow router dev-single deployment, same branch to master, a.solonenko, squash off and remove source on merge. Actual updated diff, MR text and bound snapshot are in /home/slnnk/ai-data/gitlab-workflow/DevOps-884/escrow.tinkoff-public-host/. The public Nginx rule is separately pending and must preserve the .sg Host and only forward callback/notification. No app deployment or edge edits. The earlier private-only snapshot is superseded. Gotenberg draft remains separate. Awaiting second-gate approval of this exact updated publication. No background operations.

### Escrow router MR published

User replied `Да` to the exact public-host publication proposal. Bound snapshot matched. Staged and committed diff matched the reviewed two-file patch byte-for-byte with CRLF-aware whitespace checks. Pushed `431e5349ee10477299a1447d70f30e12d61d30ef` (`add escrow router dev-single deployment`) only to DevOps-884-escrow-router-dev-single. GitLab verified Ready [MR52](https://gitlab.youdo.sg/youdo/microservices/escrow.tinkoff/-/merge_requests/52), exact body/title/SHA/source/target, a.solonenko, squash off and source deletion on merge. Pipeline143703 was running; build-router3310985 and optional manual deploy dev router3310988 were created. No deploy, merge, Nginx or Gotenberg change. Remote pipeline can be viewed or cancelled in GitLab; local checkout clean, no local operations remain.

### Gotenberg MR published

User confirmed the exact Gotenberg publication with `Да`. Snapshot matched, CRLF-aware whitespace passed and staged/committed diff matched approved bytes. Pushed `60f2a4f47625f42f7cbe74a8593f0d6c0b762204` (`add gotenberg dev-single deployment`) only on DevOps-884-gotenberg-dev-single. GitLab independently verified Ready [MR77](https://gitlab.youdo.sg/youdo/vsk/youdo.userinsurance/-/merge_requests/77), exact metadata and body, a.solonenko, no squash and source deletion on merge. Matching MR pipeline143704 was running and optional manual deploy dev gotenberg3311017 was created. No merge or deploy triggered. GitLab pipeline can be checked or cancelled in the UI; checkout clean and no local background operations.

### Chat-content tag deployment verified

User linked job3310972. GitLab confirmed success at 19:08:49 Moscow after 26.6 seconds, Helm chat-content revision3 Deployed. Both /debug/vars endpoints returned HTTP200 over their respective internal .corp ingresses. Read-only Kubernetes confirmed both tag1.1.17 images running with zero restarts, Deployments1/1 Ready, app VaultStaticSecret Ready and SecretSynced. RabbitMQ1/1 and dev-single remains Deployed revision1. Earlier revision1 and2 status is superseded. S3 upload/download remains untested. No deployment or S3 operation initiated by the agent, no background operations. Refreshed aggregate scope counts in the plan and system map.

### Escrow router deployed; chat-content S3 check waived

User linked job3310988 and explicitly waived chat-content upload/download verification. The functional S3 round trip is removed from chat-content's open acceptance, with no claim it ran. Health and ingress evidence for chat-content remains verified.

Read-only checks confirm Escrow job3310988 Success at 19:34:26 Moscow, about35 seconds, router Helm revision1 Deployed. Deployment1/1 Ready and zero pod restarts. Both requested .corp/.sg host rules exist in the Kubernetes Ingress and private /hc returned200. External .sg root still returned301 to youdo.sg; the public Nginx Host forwarding and path allowlist remain pending. Shared dev-single stayed revision1. No callback or S3 request was sent, no edits or deployments initiated, and no background operations.

### Shared Gotenberg deploy verified

User linked job3311017. GitLab confirmed Success at19:35:51 Moscow after approximately40 seconds. The userinsurance-gotenberg Helm release is revision1 Deployed. Kubernetes confirmed Deployment1/1 Ready, pod Running with zero restarts, and only internal userinsurance-gotenberg.dev.youdo.corp ingress. Its internal /health returned HTTP200. The shared dev-single release remains revision1 Deployed. Document conversion through C2C userinsurance remains to verify after it is wired to the converter. No deployment, conversion call or other external mutation initiated by the agent. No background operations.

### Gotenberg PDF conversion check waived

User explicitly waived the proposed PDF conversion verification after C2C userinsurance is connected. Removed that check from the active acceptance criteria and retained successful deploy, Ready pod and private /health HTTP200 evidence. This does not change the already agreed C2C dependency design. No PDF conversion performed or claimed. No deployment, configuration or external changes. No background operations.

### Live dev-single service count

A fresh Kubernetes Deployment read for dev-single confirmed seven application releases, all Ready: geocoder, blec, tinkoff-e2c-sign-service, pechkin, chat-content, escrow-tinkoff-router and userinsurance-gotenberg. Counting by release keeps both chat-content components under one service. Pechkin is 3/3; each other Deployment is 1/1. RabbitMQ is namespace infrastructure and ai-qa uses its own namespace. This is 7 of the 18 shared service targets. No changes or background operations.

### YouTrack deployment progress update proposed

User requested striking out the services already deployed and adding all related MRs in the issue. Fresh authenticated GET confirmed DevOps-884/id71-138332 and the original19-item list. Prepared a single description-only change: strike exactly the seven verified dev-single releases and append an MR section containing the seven service MRs and four template MRs. GitLab global title search found exactly those11 MRs, all merged. The helm-charts edits are still local. Other issue text, order, ai-qa and undeployed entries are preserved.

Exact current and proposed descriptions and actual diff are retained for review and guarded readback under /home/slnnk/ai-data/devops-884/description-rollout-proposal.json and description-rollout.diff. Waiting for explicit approval of this description edit. No YouTrack mutation, no comments, no background operations.

### YouTrack deployment progress updated

User confirmed the exact description-only change with `Да`. Fresh GET matched task DevOps-884/id71-138332 and the saved original description. One approved POST returned HTTP200. Independent GET confirmed byte-for-byte approved description, unchanged issue title, seven struck service names and eleven exact MR links (seven service and four shared CI). Sanitized receipt saved at /home/slnnk/ai-data/devops-884/description-rollout-receipt.json. No comment, status, repository or cluster mutation. No background operations.

### YouTrack dedicated Merge Request field proposal

User pointed out the issue's dedicated MR field after the description edit. Authenticated GET confirmed Merge Request id222-47, type TextIssueCustomField and empty value. Proposed one guarded issue update moving the 11 exact MR URLs into that field as a Markdown list and removing only the previously added duplicate section from description, preserving all seven strikethroughs and other text. Checked the official YouTrack TextFieldValue update schema. Exact two-field proposal and previews in /home/slnnk/ai-data/devops-884/move-mr-field-proposal.json, move-mr-field.diff and merge-request-field-preview.md. Waiting for confirmation. No YouTrack mutation or background operations.

### YouTrack MR links moved to the dedicated field

User confirmed the exact two-field update with `Да`. Fresh GET matched approved prior description and empty Merge Request field. One approved POST returned HTTP200. Independent GET confirmed exact updated description with seven struck service entries and the dedicated Merge Request field containing all11 URLs in the approved order. Also checked that the rendered text contains all11 clickable link targets. Removed the duplicate description section; issue title preserved. Receipt retained at /home/slnnk/ai-data/devops-884/move-mr-field-receipt.json. No comments, state or other changes, no background operations.

### Template-only YouTrack comment draft

User requested a draft with linked MR number and concise change per entry, only CI template MRs. Read-only GitLab GET verified !93–!96 merged, and issue inspection found zero existing comments. Exact four-entry Russian Markdown draft at /home/slnnk/ai-data/devops-884/template-mrs-comment.md. Draft only; no comment or issue update requested or performed, no background operations.

User requested the repository name at the start of the template-only draft. Updated the saved draft header to sysadmins/devops-tools/gitlab-ci-templates and retained the four entries. No comment posted.

### Template-only YouTrack comment published

User approved publishing the exact revised draft and directed adding a new comment without checking the existing comment list again. One POST to DevOps-884/id71-138332 returned HTTP200 and created comment74-125683. Direct GET of that comment matched the exact Russian draft: repository heading and four linked template MRs only. No existing comment list requested for publication. No other issue field changes. Receipt at /home/slnnk/ai-data/devops-884/template-mrs-comment-receipt.json. No background operations.

### Separate service YouTrack comment drafts

User requested one comment per deployed service, following the existing template-comment format. Verified the seven struck entries in the issue, the repository heading in comment74-125683 and the seven merged service MRs via GitLab. Prepared seven separate concise Russian drafts with repository heading, linked MR number and description of its actual diff. The Escrow description covers configured host rules and does not claim public Nginx availability. Exact drafts saved under /home/slnnk/ai-data/devops-884/service-mr-comments.json for review. No publication or other background operations.

### Separate service comments published

User approved the seven exact service drafts with `Опубликуй эти комментарии`. Confirmed issue DevOps-884/id71-138332 and no existing matching service drafts or MR references in comments. Created one comment per service, IDs74-125685 through74-125691. Independent direct GET of each verified its exact approved text and single MR link. All seven IDs are distinct. Receipt retained at /home/slnnk/ai-data/devops-884/service-mr-comments-receipt.json. No issue field, template comment or other change. No background operations.
