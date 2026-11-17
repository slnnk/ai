---
system: dev-deployment
status: verified
checked: 2026-11-17
tags: [kubernetes, helm, gitlab-ci, devops-884]
---
# DevOps-884 first ten shared services: dev Kubernetes repository assessment

## Summary

- Current target: first ten shared services from the accepted19service inventory use permanent namespace `dev-single` (latest user decision). Existing CI modes remain unchanged: MR and semver release tag for manual mode, master for auto mode.
- Assessment only: no repository task edits, branch switch, pipeline creation, publication, Vault write or deployment authorized or performed.
- Six services are relatively simple to onboard; call-service, textvalidation and mailer need PostgreSQL/migration integration; DebuggingEvents also needs an Elasticsearch deployment decision.
- Baseline estimate: about20service configuration files (ten CI files, nine new dev values and one existing dev values update), plus shared CI/namespace work. This is an estimate, not a prepared diff or fixed delivery quote.
- Current user decision: preserve each service deployment mode and existing build rules. Helm deploy is manual in MR and, for manual mode, semver release-tag pipelines; auto mode retains master pipelines. Existing .rules-prod-manual already implements this; the earlier proposal to enable master independently for all ten is superseded.
- Existing chart supports multiple components, existing component image naming, per-component env, PostgreSQL PVCs and pre/post migration Jobs. Synthetic render probes for all ten shapes passed in literal namespace `dev`.
- Latest user selected namespace `dev-single`, matching the existing Vault role namespace pattern `dev-*`. The previously confirmed literal `dev` mismatch is resolved by target selection; no namespace-binding expansion is required. Secret-path/policy readiness is separate.
- User clarified desired bootstrap semantics: any service may create the shared namespace initially; later service deployments must reuse it without updating namespace infrastructure. Current deploy-helm unconditionally runs namespace helm upgrade --install, so a shared template adjustment is needed. A separate infrastructure repository/owner was not selected.
- No forced application rewrite or runtime upgrade established. Pechkin needs a small configurable unsubscribe endpoint if the old endpoint will not be retained. Node8/11, .NET2.1/3.1 and Go1.10 build success was not exercised.
- Current ai-qa source still targets dev-ai-qa. The latest all-services namespace dev-single requirement is the DevOps-884 target; this analysis does not claim that ai-qa/state was moved.

## Task and authorization

Sources: [DevOps-884](https://youtrack.youdo.com/youtrack/issue/DevOps-884) and [accepted inventory](2026-11-17-nomad-test-devops-884-shared-service-inventory.md#target-dev-kubernetes-inventory-user-decision-november17). User specified MR and master deployment and namespace `dev` for all services. Interpreted like current ai-qa: a manual deploy job, fixed service release name in a permanent shared namespace. Each MR deploy updates that service's shared instance; per-MR isolation was not requested. Automatic deployment is not inferred from pipeline availability.

No implementation approval requested during this assessment. Repositories stayed on their original branches and all13inspected worktrees remained clean. Read-only fetch refreshed master for the ten services, ai-qa, gitlab-ci-templates and helm-charts. FluentMigratorCore tag1.8.1 was inspected for the migration CLI contract without changing its checkout.

## Per-service assessment

| Service | Scope | Evidence / required configuration |
| --- | --- | --- |
| geocoder | Small | One api component, port80, /hc; env-based Yandex/DaData settings and Exceptional MSSQL logging connection. Add dev.yml and dev CI; no business database or migrations in test.hcl. |
| youdo-call-service | Medium | Web+worker, PostgreSQL, pre/post migrations, RabbitMQ and provider callback/settings. Chart supports components and migration hooks; configure per-component env and retain UseMockProvider for test behavior. |
| youdo-business-doc-generator | Smallest | Existing devops/dev.yml, api8080, /_/healthcheck, S3 and Vault mappings. Adapt existing values to fixed global.projectName/namespace dev and permanent namespace settings. Existing Jenkins .deploy-dev.yml needs deliberate replacement/isolation for this flow. |
| chat-content | Small | Uploader+downloader, two existing images, port18180, /debug/vars; S3 config is environment-driven. Chart already handles both images/components and ingress routes. |
| textvalidation | Medium | API plus PostgreSQL and pre-migration Job; app uses ConnectionStrings__Pg. Migrations use GlobalSettings/env and standard entrypoint CON_STR CLI override. Replace fixed database address via values, retain Exceptional logging config. |
| tinkoff-e2c-sign-service | Small | One web component, port32000, /health. Current image already contains the configured signing key file; only file paths were inspected, no key contents. Existing deployment can be represented in values; a separately chosen move to mounted signing material would add work. |
| DebuggingEvents | Largest | API plus Elasticsearch7.17.14, current2GiBheap/3GiBmemory; ES config file mount and Docker ulimits/memory-lock settings in Nomad. Decide a cluster-side ES deployment/config/storage approach or an explicitly selected external endpoint. microservice chart can use an explicit ES image, but does not reproduce arbitrary Docker ulimits or config mounts. Render alone does not establish ES readiness. |
| BlackListedEmailChecker | Small | One web component, port80; periodically downloads domain lists from GitHub and writes a local cache. Environment config supported. No DB/migrations; select a valid readiness check (Nomad has none, root404 from previous evidence). |
| pechkin | Small with conditional source change | One web component, port3005, /; preserve production=0 and source template assets. Current server/config.js hardcodes unsubscribe-link-generator test URL; UnsubscribeLink.getLink actually calls it. An env override is a small source change if moving that dependency URL; no change needed solely to keep using the existing reachable endpoint. Current3replicas are a sizing choice, not an obligation to use count1. |
| mailer | Medium / most integration work | API+scheduler+dispatcher, PostgreSQL, migration image, RabbitMQ, SMTP, Exceptional MSSQL logging and Pechkin. Use component-specific env. Current21allocations(1+10+10) are a sizing baseline, not an implicit request to reduce workers. App config loads env. Migrator's literal fallback can be overridden using standard CON_STR -> entrypoint -c; no mandatory migrator source rewrite established. |

## Common changes required

### Historical CI master expansion proposal (superseded by the decision below)

Current ai-qa source uses .main.yml + .deploy-helm.yml, DEPLOY_PROD_MODE=auto and manual deploy rules. Among the ten, only doc-generator already uses auto. Nine manual-mode projects currently build for MR and semver tag; .rules-prod and .rules-prod-manual do not include their master branch. Simply adding .deploy-helm.yml is therefore incomplete.

Keep dev build/test/deploy eligibility independent from production release/deploy mode. An opt-in shared dev-master rule can be connected to set-variables, .NET NuGet restore/build/unit tests, Node build and Helm deploy; chat-content build and DebuggingEvents integration-test rules are project-local consumers. Preserve tag releases and production controls. This requires a coordinated shared CI change beyond the ten service includes; exact file count depends on whether rules are factored centrally or overridden per project. Current .rules-prod-by-mode explicitly sets automatic execution for auto+master, so setting auto globally is a real production effect.

All existing builds already produce component images compatible with the chart's <repository>/<component>:<tag> convention; ai-qa's custom single-image builder is unnecessary here. Group KUBECONFIG_DEV metadata is env_var, unprotected, scope*; no variable value was printed or saved. Project chart-repository CI_JOB_TOKEN access and end-to-end MR availability remain to verify before rollout. Existing latest master pipeline metadata is often historical because manual-mode projects release via tags; old pipeline status is not a current build result.

### Permanent shared namespace

Use namespace dev with distinct stable release/global.projectName per service and no buildNumber suffix. Remove namespace TTL metadata; no auto-stop/namespace delete lifecycle. App Helm names are release/project-prefixed, so ten releases can coexist.

Current .deploy-helm.yml runs helm upgrade --install $namespace ephemeral-namespace -f <service-values> before every app deployment. All ten would operate on the same dev release in default. GitLab resource_group dev serializes only within a project. One service can also disable/delete RabbitMQ/Redis objects installed by another if their values differ. Establish a single canonical namespace/dependency bootstrap and allow app jobs to reuse it; do not duplicate namespace ownership in ten independent releases. This connects to the existing namespace-lock/owner topics already tracked under dev-deployment in central TODO.

Live GET /v1/auth/kubernetes-dev/role/dev-ephemeral-deployer returned default ServiceAccount and bound_service_account_namespaces=[dev-*], no namespace selector, policy dev-ephemeral-deployer. Literal dev needs an explicitly approved role-scope update. Helm probes render literal dev successfully; no chart naming change is intrinsically required. Policy access to selected service paths and existing registry/Vault resources must also be checked when preparing rollout.

### Dependencies and consumers

Define dev Vault mappings and service addresses rather than copying Nomad template expressions. Keep application DB connections and migration connections aligned. The three PostgreSQL workloads can use existing chart PostgreSQL+PVC and standard dev credential conventions; whether to create fresh dev databases or connect to current test data is not decided by this analysis. External PostgreSQL with VSO credentials would require checking pre-hook secret consumption/readiness separately.

RabbitMQ topology/queues must match dev consumers; SMTP and Pechkin must target the intended test routes. S3 access, Yandex/DaData APIs and logging MSSQL remain integration prerequisites. Repoint consumers in ephemeral dev environments to the shared services as a separately traced consumer change; deploying new ingress alone does not change existing URLs. No runtime data migration, secret provisioning, DNS cutover or application calls were executed.

## CI mode decision (user correction, November17)

User explicitly directed keeping the current service deployment modes and making the dev job available in the release-tag pipeline. This supersedes the earlier all-services-master interpretation and the proposed separate master build/test rule. Scope is DevOps-884; no global deployment policy change.

Verified shared .deploy-helm.yml uses .rules-mr-manual and .rules-prod-manual. The latter already selects auto+master or manual+semver tag, always with when:manual. .rules-prod-by-mode is a different helper and is not the rule used by this Helm job. Thus all ten get a manual MR dev job; nine manual-mode services get manual dev jobs on semver release tags (e.g.1.2.3), and doc-generator retains the auto-mode master path with a manual dev job. No DEPLOY_PROD_MODE, build/test mode or common rule changes are needed for this requirement. Include .deploy-helm.yml and service values; shared namespace ownership and Vault dev binding findings remain applicable.

No source or external changes. Exact user direction and verification are recorded here; the earlier CI proposal remains historical evidence only. User clarification does not authorize implementation.

## Verification and limits

- Fresh source refs for13repositories saved in /home/slnnk/ai-data/devops-884/repo-audit/revisions.json; actual project/default-branch/latest-master-pipeline metadata in project-ci-metadata.json.
- Read current service CI and Nomad configuration, relevant app configuration loading and dependency call sites. Library tag1.8.1 MigrateCommandExtension.cs accepts -c/--conn and chooses it over the source fallback; shared dotnet.entrypoint.sh passes CON_STR there.
- Synthetic, secret-free Helm interface probes use exact chart master3254a7f. All ten render Deployment/Service shapes, with PG/migration hooks in three; image paths and resource identities checked. Artifacts: render_probe.py, *-synthetic-values.yml and render-summary.json under the audit directory. These are probes, not deployable service values.
- Namespace probes with rabbitmq false/true render5/8resources and no TTL, showing both literal dev acceptance and differing shared release resource sets. Vault role check independently establishes dev auth mismatch.
- No application builds, CI lint POST, pipeline/job trigger, Kubernetes server dry-run, HTTP functional test, database initialization or deployment. Synthetic rendering does not validate app config, dependency reachability, ES kernel/bootstrap compatibility, persistent data or package availability.
- All13worktrees clean at final check; fetch only updated remote refs. All task commands finished; no agents or background operations remain.

## Status and bookkeeping

Repository assessment complete. Target namespace and pipeline requirements are recorded here and linked from the existing task record/system map. Existing dev-deployment backlog already tracks namespace lock/owner and Vault role ownership; this assessment does not close those items or authorize implementation. No new executable task or unrelated improvement was introduced. Repository catalog refreshed for the inspected ten service mappings; incorrect unrelated historical copied descriptions were replaced with observed service purposes and source references.

## Inspected revisions and source links

- `geocoder` master `328aef3a`: [CI](https://gitlab.youdo.sg/youdo/microservices/geocoder/-/blob/328aef3aa2dcd460ae5a4d0a2fb2a45ea7ae22a5/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/microservices/geocoder/-/blob/328aef3aa2dcd460ae5a4d0a2fb2a45ea7ae22a5/devops/test.hcl).
- `youdo-call-service` master `040cf5b1`: [CI](https://gitlab.youdo.sg/youdo/microservices/youdo-call-service/-/blob/040cf5b1ef2e416f8fc91c84b0af3298d6a181f0/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/microservices/youdo-call-service/-/blob/040cf5b1ef2e416f8fc91c84b0af3298d6a181f0/devops/test.hcl).
- `youdo-business-doc-generator` master `bdee550d`: [CI](https://gitlab.youdo.sg/youdo/microservices/youdo-business-doc-generator/-/blob/bdee550d87fc677d852e0b0d488d04094ef18d44/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/microservices/youdo-business-doc-generator/-/blob/bdee550d87fc677d852e0b0d488d04094ef18d44/devops/test.hcl).
- `chat-content` master `f47a22b9`: [CI](https://gitlab.youdo.sg/youdo/chat-content/-/blob/f47a22b96c1f932790277c7d239251e3b907289f/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/chat-content/-/blob/f47a22b96c1f932790277c7d239251e3b907289f/devops/test.hcl).
- `textvalidation` master `1fa42397`: [CI](https://gitlab.youdo.sg/youdo/microservices/textvalidation/-/blob/1fa4239704ff4d99e1b5e58a2dbccb3261375036/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/microservices/textvalidation/-/blob/1fa4239704ff4d99e1b5e58a2dbccb3261375036/devops/test.hcl).
- `tinkoff-e2c-sign-service` master `5daa847e`: [CI](https://gitlab.youdo.sg/youdo/microservices/tinkoff-e2c-sign-service/-/blob/5daa847e4dd7238425d6a2ab2f26dfe07b71da12/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/microservices/tinkoff-e2c-sign-service/-/blob/5daa847e4dd7238425d6a2ab2f26dfe07b71da12/devops/test.hcl).
- `DebuggingEvents` master `642d8dfa`: [CI](https://gitlab.youdo.sg/youdo/microservices/DebuggingEvents/-/blob/642d8dfa6acb1d80e75aae5a96c48b41b15abe7d/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/microservices/DebuggingEvents/-/blob/642d8dfa6acb1d80e75aae5a96c48b41b15abe7d/devops/test.hcl).
- `BlackListedEmailChecker` master `3a23a85f`: [CI](https://gitlab.youdo.sg/youdo/BlackListedEmailChecker/-/blob/3a23a85f54e5f506b9e3dc3d3f14005eadcb67f9/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/BlackListedEmailChecker/-/blob/3a23a85f54e5f506b9e3dc3d3f14005eadcb67f9/devops/test.hcl).
- `pechkin` master `78a4776e`: [CI](https://gitlab.youdo.sg/youdo/mail/pechkin/-/blob/78a4776e825ccbe198cbe881a02b1c3808aff2cd/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/mail/pechkin/-/blob/78a4776e825ccbe198cbe881a02b1c3808aff2cd/devops/test.hcl).
- `mailer` master `e1062c22`: [CI](https://gitlab.youdo.sg/youdo/mail/mailer/-/blob/e1062c2212bda8c0d5e3f08cbe58c40e0c1b76fd/.gitlab-ci.yml), [Nomad configuration](https://gitlab.youdo.sg/youdo/mail/mailer/-/blob/e1062c2212bda8c0d5e3f08cbe58c40e0c1b76fd/devops/test.hcl).
- ai-qa master `d5598727`; gitlab-ci-templates master `56ba8a1a`; helm-charts master `3254a7fa`.

## Portable lesson
none

## Task metrics: DevOps-884-first-ten-repo-analysis

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-884-first-ten-repo-analysis",
  "created": "2026-11-17T22:13:10.783210+03:00",
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
  "evidence": "Fresh refs13repos;10service CI/runtime/dependency source reviews,10synthetic Helm interface renders, live Vault role mismatch; repository worktrees unchanged.",
  "updated": "2026-11-17T22:13:10.783254+03:00"
}
```

## Namespace decision dev-single (user correction, November17)

User selected `dev-single` instead of `dev` in response to the Vault namespace-binding finding. This is the current DevOps-884 target namespace for the common service inventory, including the first ten under analysis. It supersedes prior desired namespace dev, not historical evidence about existing deployments. `dev-single` matches the verified existing role binding `dev-*`; no role-scope expansion is needed on this account. Shared namespace bootstrap ownership/concurrency and consistent RabbitMQ/Redis settings remain separate applicable findings. Existing service CI modes stay unchanged per the previous decision.

Bookkeeping only: no namespace created, service values edited, ai-qa state moved or infrastructure changed. No background operations remain.

## Namespace bootstrap intent (user clarification, November17)

User expected any first service deployment to create dev-single and later service deployments to leave the existing namespace unchanged. This is the task-specific desired lifecycle, not a claim about current Helm behavior or approval to implement. Current .deploy-helm.yml lines28–31unconditionally invoke helm upgrade --install for ephemeral-namespace, then separately upgrade the application release. Helm does not recreate an existing Namespace simply because of upgrade; however, existing namespace metadata and other resources in the namespace chart remain subject to reconciliation, including additions/updates/removals when values change. Namespace existence alone does not make that command a no-op.

Proposed adjustment matching user intent: bootstrap namespace/common infrastructure once from consistent shared settings, then skip namespace-chart upgrades for ordinary service deploys; continue upgrading only each application's Helm release. No separate infrastructure repository is intrinsically required. Initial concurrent deploys and partially completed bootstrap must be handled so another service does not race namespace installation or mistake an existing Namespace object for ready registry/Vault/dependency resources. These are bounded implementation concerns, not authority to create new services, locks or infrastructure.

Discussion remains in progress; no repository edits or namespace changes. Existing namespace lock/owner backlog is not closed or duplicated; it is historical context for the proposed bootstrap behavior. No background operations remain.

## Proposed bootstrap-once changes (November17)

User asked what is needed and what would change; design discussion only. Concrete minimal proposal for namespace bootstrap, separate from per-service onboarding:

- gitlab-ci-templates/v3/.deploy-helm.yml: replace unconditional namespace upgrade with ensure-once behavior. Inspect namespace Helm release dev-single in default, not just Namespace existence. On successful existing installation reuse without upgrading the namespace chart; install a missing release from canonical shared values, then continue to the ordinary per-service application upgrade. Concurrent first installers must converge on one release: on a confirmed concurrent installation, wait for that installation to finish instead of upgrading it. Authentication/API errors and failed/stuck initial installs must fail visibly rather than count as absence/success. A completed bootstrap includes required registry/Vault plumbing; namespace presence alone is insufficient.
- helm-charts/ephemeral-namespace/dev-single.yml (proposed new file, not created in repository): single shared bootstrap configuration for namespace dev-single, no TTL, existing registry/Vault integration and explicit common dependency settings. Do not pass an arbitrary service dev.yml to namespace installation; it must not be whichever service's flags happen to run first. RabbitMQ choice must cover current call-service/mailer consumers; redis is not a demonstrated dependency of these ten. Final dependency settings and endpoints are part of the reviewable implementation proposal, not selected by this discussion alone.
- gitlab-ci-templates/v3/DEPLOY_HELM.md: document creation-once, shared values, ordinary app-only upgrades and separate deliberate maintenance/recovery for namespace infrastructure.

Scope estimate for the bootstrap mechanism is three common files across two existing repositories, before per-service CI/dev.yml onboarding. No separate namespace repository, bespoke lock service or per-service copy of bootstrap logic proposed. An install-race waiting design requires focused verification during implementation; no claim that this behavior is already implemented/tested. Existing consumers of .deploy-helm.yml must be considered when binding the common values path so ai-qa/dev-ai-qa is not silently retargeted or given unrelated dependencies. All application DB/migration workloads remain in their own Helm releases; they are not skipped by namespace reuse.

Proposed validation: first install in absent namespace, later service with no namespace-release revision/resource changes, simultaneous first installs, failed/pending bootstrap, and unchanged MR/tag rules. No repository changes, local implementation, pipeline triggers or external mutations; no new execution approval requested. Discussion remains open; existing backlog is unchanged. All task commands finished, no background operations remain.

## Current namespace chart contents (November17)

User requested the actual contents of ephemeral-namespace. Fresh read-only master fetch confirms3254a7funchanged. Templates create, for each explicit namespaces[] entry: Namespace; VaultConnection+VaultAuth; registry VaultStaticSecret that asks existing VSO to generate youdo-registry-secret from dev/registries; developer-access RoleBinding; optional ServiceAccount; optional RabbitMQ Deployment/Service/Ingress/auth VaultStaticSecret; optional Redis Deployment/Service. Existing central Vault and VSO operator are prerequisites, not installed by this chart. Application Deployments, PostgreSQL and migrations belong to microservice releases.

Defaults: RabbitMQ3.8.34-management-alpine and Redis7.2-alpine enabled; RabbitMQ ingress enabled. Both workload templates use emptyDir, not PVC. Changing the declared persistence.enabled value alone does not introduce a PVC in these templates. Developer binding enabled, ClusterRole edit for k8s-access/k8s-dev-developer; ServiceAccount creation disabled, default used. Namespace defaults environment=dev, createdBy=jenkins, baseline Pod Security labels and TTL8d in both label and TTL-controller annotation. The external TTL controller handles expiration; the chart does not run a cleanup job. Namespace names must be supplied. RabbitMQ ingress needs explicit host or buildNumber for automatic hostname construction.

For desired permanent dev-single, explicitly remove TTL metadata and use shared dependency choices. This inspection introduces no new proposal or decision and changes no repositories/infrastructure. Fetch/checks complete; no background operations remain.
