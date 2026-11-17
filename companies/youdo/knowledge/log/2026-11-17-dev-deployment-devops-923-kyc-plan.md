---
system: dev-deployment
status: verified
checked: 2026-11-17
tags: [kyc, jenkins, helm, DevOps-923]
decision_state: cancelled
decision_scope: DevOps-923 optional extend/delete lifecycle verification and old source Vault key cleanup
decision_summary: User cancelled optional lifecycle verification and old source secret cleanup; completed dev rollout evidence is retained and production HCL/routing remain deferred.
decision_date: 2026-11-17
decision_source: #session-closeout-decision-2026-11-17
---
# KYC dev Kubernetes onboarding plan

## Task
Prepare a plan for DevOps-923, adding KYC to the dev Kubernetes deployment catalog. Planning only; no repository edits, publication or deployment authorized.

## Context
Issue GET: summary `[B2B] Добавить сервис KYC в деплой на dev k8s`, description links to https://gitlab.youdo.sg/youdo/microservices/kyc; no comments. GitLab GET verified project630, path kyc, default master. Existing system map: [overview](../systems/dev-deployment/overview.md).

## Actions
Cloned the missing checkout into /home/slnnk/git/kyc via gitlab_repo.py; registered its repository mapping. Inspected KYC master893428b and refreshed origin refs for Jenkins, Helm and CI templates without changing branches or working trees. Inspected Jenkins master af3c6da, Helm master3254a7f, templates master56ba8a1. No external writes or deployment commands.

## Findings
KYC already includes v3/.deploy-dev.yml and devops/dev.yml in master. Four build jobs produce api, api-ext, worker and migrations images. Values configure PostgreSQL, pre migrations with ConnectionStrings__Kyc=pgService, namespace RabbitMQ credentials, Staging, tracing disabled, probes /health/live and /_/healthcheck. Internal API has no ingress; api-ext and worker have public/internal ingress respectively.

Jenkins config/deploy-dev-b2b.groovy has13services and no KYC. Proposed canonical name youdo-kyc matches PROJECT_NAME and ingress naming; project_id630 resolves the GitLab trigger name kyc by ID. Proposed dependencies=[] because KYC core is independent of legacy B2B/docvalidation. Runtime currently expands every primary to the full catalog; dependencies are not selective deployment controls. Adding KYC affects other B2B deployments too.

Secret references use mount secret/path dotnet/business and keys KycNeuroVisionApiToken, KycNeuroVisionScenarioId, KycNeuroVisionScenarioSecret, KycEncryptionKekV1. README claims the API token was saved by the user; no live secret availability or Vault policy validation performed. KEK must be Base64 encoding32bytes. Provider testing must use an approved test scenario and synthetic data.

Local Helm render against refreshed master passed:3Deployments,1PostgreSQL StatefulSet,1pre-migration Job,1VaultStaticSecret,2Ingresses. Example build923 generated youdo-kyc-api-ext-923.dev.youdo.sg and youdo-kyc-worker-923.dev.youdo.corp. No server validation, runtime check, image availability check or provider call performed.

## Plan rationale
Minimal expected repository change is one catalog entry in Jenkins, plus relevant catalog test/documentation updates. Reuse KYC values and shared templates unless validation demonstrates a concrete gap. Confirm current Jenkins kubeconfig-dev and GitLab KUBECONFIG_DEV target, storage, VSO path access and image availability first; old overview references to Yandex are historical and do not prove the current target. Publish/reload catalog only through the approved workflow. Exercise KYC-primary deploy, migration/probes/network boundaries, repeat deploy, another-primary catalog inclusion, TTL extension and cleanup. B2B/docvalidation routing and end-to-end provider integration are separate acceptance scope; do not equate healthy pods with full KYC workflow success.

## Changes
Only KB records/catalog bookkeeping changed. Repository task files remain untouched. Both repository approval gates remain pending; future runtime and secret changes require their own explicit approval.

## Status and risks
Planning complete. Implementation remains a proposal tracked in [central TODO](../../../../TODO.md). No background task operations remain. Main unverified prerequisites: live target/access, Vault values/policy, matching image tags, provider connectivity and runtime behavior.

## Portable lesson
None.

## Task metrics: DevOps-923-plan

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-923-plan",
  "created": "2026-11-17T15:39:36.928746+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "analysis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Issue/project GET, refreshed source inspection and successful local Helm render; requested plan prepared, runtime unverified",
  "updated": "2026-11-17T15:39:36.928792+03:00"
}
```

## User-selected Vault path (2026-11-17)
User requested moving KYC secrets to dev/projects/kyc. This supersedes the previous planned use of dotnet/business. Read-only VK test Vault check confirms KV v1 at mount secret: source secret/dotnet/business contains all4KYC keys, nonempty, plus21other fields; destination secret/dev/projects/kyc exists with1other field and none of the4KYC fields. Values were neither printed nor saved. First safe mutation is merging only the4KYC fields into the destination while preserving its existing field, with immediate equality readback. Source removal must follow consumer cutover: current KYC master dev.yml still references dotnet/business. Repository changes require branch/base approval. Per-command external-change confirmation remains pending before writing Vault. No background operations remain.

## Approved destination write (2026-11-17)
User explicitly confirmed the previously described single Vault destination write with `Да`. One POST to VK test Vault secret/dev/projects/kyc returned HTTP204. Readback confirmed all4KYC values exactly match source and all existing destination fields were preserved. No values printed or persisted outside Vault. Source secret/dotnet/business was not modified. No retry, repository task edit, consumer cutover, source deletion or deployment performed. Destination population is complete; full migration remains pending configuration cutover and separately approved source cleanup. No background operations remain.

## KYC MR first-gate proposal (2026-11-17)
User requested preparing an MR changing devops/dev.yml to dev/projects/kyc. Refreshed KYC origin/master remains893428b; checkout master is clean, identity configured, no matching local/remote DevOps-923 branch and no open project MRs. Proposed repository youdo/microservices/kyc, new branch DevOps-923-kyc-dev-vault-path from origin/master893428b targeting master. Scope: one Vault path substitution in devops/dev.yml and the matching outdated path paragraph in devops/README.md. First supervised approval pending; no repository edits or Git mutations performed. Expected verification: net diff/YAML and Helm render preserve secret mappings and use secret/dev/projects/kyc. Publication requires a later concrete diff/checks/CI proposal. All preflight commands finished; no background operations remain.

## KYC MR prepared after first approval (2026-11-17)
User confirmed the exact first-gate proposal with `Да`. Created DevOps-923-kyc-dev-vault-path from origin/master893428b in the existing clean checkout. Changed only devops/dev.yml Vault path and matching README paragraph. git diff --check passed. Parsed YAML comparison proves only secrets[0].path changed and all mappings preserved. Helm render against helm-charts origin/master3254a7f passed and asserts VaultStaticSecret mount secret/path dev/projects/kyc;3Deployments and1migration Job retained. No product tests required for this values/docs-only change.

Prepared commit `use dedicated vault path for kyc dev secrets`, ready MR title `DevOps-923 Use dedicated vault path for kyc dev secrets`, source task branch -> master, assign user184, squashfalse and remove-source-on-mergetrue consistent with project defaults. Exact short Russian body and patch/proposal saved under ai-data/gitlab-workflow/DevOps-923/kyc. CI inspection: MR rules build/push4tagged images and run dotnet tests; dev/test deploy manual, monitoring applies only production rules, no master/tag publication. Publication approval pending; nothing staged, committed, pushed or published. No background operations remain. Original source secrets remain untouched; Jenkins catalog addition and full dev verification remain outside this MR.

## Approved KYC MR publication (2026-11-17)
User explicitly confirmed the full second-stage proposal with `Да`, covering task-only staging/commit/push and ready MR creation with stated CI effects. Snapshot check matched. Entire staged diff and resulting commit patch exactly matched the approved review.patch. Commit86db5c8448c93ff0b654954331b775b293fdf0cf uses approved subject, branch and scope; push succeeded. Created [MR4](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/4); API readback verified exact SHA, title/body, source/target master, user assignee, ready state, squashfalse and remove-source-on-mergetrue. Initial pipeline list empty, not a successful CI result. Checkout clean. No merge, deployment or source-secret deletion authorized/performed.

Original and final proposed branch, scope, commit and MR wording matched; no user corrections to publication artifacts. Applicable outcomes: preserved clean unrelated state, honored both approvals, inspected exact staged/commit patch, published only reviewed source branch, verified metadata by readback. Dedicated Vault destination was populated earlier; master consumer path changes only after merge, which remains unperformed. Jenkins catalog onboarding and first runtime acceptance remain pending in central TODO. All local publication commands completed; CI status reported separately.

Final read-only verification: MR4 exact metadata/SHA still matches. Pipeline143316 RUNNING: https://gitlab.youdo.sg/youdo/microservices/kyc/-/pipelines/143316 . This is remaining remote CI work, not deployment; inspect or cancel through that pipeline page. No local background command remains.

## Task metrics: DevOps-923-kyc-vault-mr

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-923-kyc-vault-mr",
  "created": "2026-11-17T15:47:52.906811+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Approved additional ingress commit7a00265 exactly matches patch; MR4 updated and readback verified; Helm render and agent lint pass; CI143321 running, no runtime rollout",
  "updated": "2026-11-17T16:23:20.069337+03:00"
}
```

## Jenkins catalog MR first-gate proposal (2026-11-17)
User requested a separate Jenkins catalog MR. Existing checkout /home/slnnk/git/jenkins-pipelines is clean on prior task branch DevOps-886-dev-ttl-controller af3c6da. Read-only fetch confirms origin/masterf4705b0; no matching DevOps-923 branch or opened MR for proposed branch. No root AGENTS.md or CI file in tracked root. Active Groovy catalog lacks KYC; regression test asserts exact catalog membership/order and project resolution. Existing README explains full-catalog behavior. Proposed new branch DevOps-923-add-kyc-dev-deploy from origin/masterf4705b0, target master. Changes limited to config/deploy-dev-b2b.groovy entry youdo-kyc/project630/dependencies[] and tests/deploy_dev_b2b_test.groovy expected catalog plus project-ID/GitLab-name resolution checks. Existing full-catalog semantics remain, so KYC joins other-primary fresh deployments too. Local Groovy executable absent but cached Groovy4core/json jars found for offline Java runner. First approval pending; no task repository mutation performed. All preflight operations finished; no background work remains.

## Jenkins catalog MR prepared after first approval (2026-11-17)
User confirmed first-gate proposal with `Да`. Created DevOps-923-add-kyc-dev-deploy from origin/masterf4705b0. Added one youdo-kyc/project630/dependencies[] catalog entry and8test lines for expected membership, ID lookup and GitLab kyc name mapping. Total2files/13insertions. Updated existing test failed on missing catalog membership before implementation, then full existing deployment-set test passed after addition using installed Java/cached Groovy4.0.1core/json (no downloads). git diff --check passed. Existing parameterized deployment-order and repeat-deploy tests now cover expanded14service catalog. No pipeline logic changes.

Project590 GET confirms CI builds disabled, Auto DevOpsfalse and empty ci_config_path; no root GitLab CI file. Publication does not trigger deployment. After separate merge to master, next Jenkins full-catalog deploy will include KYC, including when another primary service is selected. No Jenkins build/reload performed. Ready MR proposal: commit `add kyc to dev deployment catalog`, title `DevOps-923 Add kyc to dev deployment catalog`, task branch -> master, assign user184, squashfalse, source-deletion-on-mergetrue. Exact Russian body, patch and proposal saved under ai-data/gitlab-workflow/DevOps-923/jenkins-pipelines. Second approval pending; no staging/commit/push/MR write. All test/background commands finished.

## Approved Jenkins catalog MR publication (2026-11-17)
User explicitly confirmed complete second-stage publication proposal with `Да`. Snapshot check matched. Entire staged diff and resulting commit patch exactly matched approved review.patch:2files/13insertions. Commit135e951da36cc22ee58b8fc3037258620271fda4 with approved subject `add kyc to dev deployment catalog` pushed successfully to DevOps-923-add-kyc-dev-deploy. Created [Jenkins MR3](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins-pipelines/-/merge_requests/3); immediate API readback verified exact SHA/title/body/source/target, assignee a.solonenko, ready state, squashfalse and remove-source-on-mergetrue. CI pipeline listing GET403; project previously verified builds disabled and Auto DevOpsfalse, so no CI success claimed. Local Groovy test and diff checks passed before publication. Checkout clean; all task commands finished, no background processes or agents remain. No merge, Jenkins trigger/reload, deployment or old secret removal performed.

Applicable first-attempt outcomes: first/second approvals respected, original/final names and scope unchanged, approved staged/commit bytes identical, only task branch published, MR metadata verified. Remaining work is review/merge of the two prepared MRs (latest KYC MR4 state not rechecked), runtime acceptance via ordinary Jenkins deployment, and separately approved source-key cleanup after confirmed consumer cutover. Central TODO reflects published catalog status rather than an unimplemented catalog edit.

## Task metrics: DevOps-923-jenkins-catalog-mr

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-923-jenkins-catalog-mr",
  "created": "2026-11-17T15:56:36.997221+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Both approvals; full existing Groovy test passed; exact staged/committed patch and MR3 metadata readback verified; pipeline list403, merge/runtime unverified",
  "updated": "2026-11-17T15:56:36.997269+03:00"
}
```

## First KYC dev rollout evidence (2026-11-17)
User supplied job3304994 for assessment. Read-only GitLab GET/trace confirms `1 deploy dev` SUCCESS, pipeline143316 SUCCESS at commit86db5c8, Jenkins test/208 SUCCESS (buildingfalse, duration567674ms). Jenkins log resolves project630 kyc -> youdo-kyc, selects KYC as primary and full14service catalog, deploys release youdo-kyc-devops-923 into dev-devops-923 with image tag devops-923-kyc-dev-vault-path-143316. Explicit rollout success for api/api-ext/worker; logged pods all1/1Running/restarts0, PostgreSQL1/1Running/restarts0 and pre-migration Job Completed. This is build-time runtime evidence, not a fresh kubectl pod audit. Artifacts/environment published. No HTTP business/provider test performed.

External api-ext URL https://youdo-kyc-api-ext-devops-923.dev.youdo.sg/health/live returns HTTP301 Location https://youdo.sg; plain HTTP gives the same redirect. NoRedirect probes confirm this is not a successful application health response. Routing root cause not diagnosed; no external routing changes made. Advertised worker URL http://youdo-kyc-worker-devops-923.dev.youdo.corp not independently checked. Internal API intentionally has no ingress.

MR readback: Jenkins MR3 merged2026-11-17 into9e60d3e398b980b3bb199011c0ddb64db0c58244. KYC MR4 still opened. No retries, builds, merges or runtime mutations performed by agent. All diagnostic commands finished, no agent background operations remain. Initial commentary presumed a failure before checking; actual job is successful and reported as such. Remaining central TODO updated: external routing diagnosis, KYC MR merge, lifecycle checks, source-secret cleanup after verified cutover; Jenkins catalog publication/merge and first rollout are no longer pending.

## Internal API ingress requirement (2026-11-17)
User explicitly requires the internal KYC API to be accessible through ingress. This supersedes earlier no-ingress statements as desired behavior; existing deployed values and repository docs still lack ingress. User request takes precedence over current repository AGENTS.md statement limiting dev API to Kubernetes Service. Proposed internal host youdo-kyc-api.dev.youdo.corp follows worker internal domain convention; chart injects deployment suffix, expected current stand URL http://youdo-kyc-api-devops-923.dev.youdo.corp. Host selection remains a proposal pending approval, not a verified access restriction or active route.

Read-only refresh confirms origin/master893428b, clean task branch86db5c8 and MR4stillopened. Proposed scope reuses DevOps-923-kyc-dev-vault-path/MR4 targeting master, adds api ingress block in devops/dev.yml and updates conflicting dev guidance in devops/README.md and AGENTS.md. First approval for expanded scope pending; no repo edits. Expected checks: Helm render api route points at api Service80 -> port8080, prior routes preserved; diff checks; mandatory report-only agent lint after AGENTS.md edit. Publication/title/body change requires later concrete approval. No runtime/DNS changes or deployment approved; all preflight commands finished.

## Approved internal host and original isolation rationale (2026-11-17)
User chose youdo-kyc-api-int.dev.youdo.corp and requested an additional commit in existing MR4; this authorizes the first-gate expanded implementation, with publication confirmation still pending. Current local changes add api ingress and align AGENTS.md/devops README; Helm render passed with youdo-kyc-api-int-devops-923.dev.youdo.corp -> api Service80 -> container8080, preserving other2routes. agent_lint --force including repo AGENTS passed0errors/0warnings/1info; git diff --check passed. Nothing staged/committed/pushed for ingress.

User asked why original no-ingress guidance existed. git blame identifies commit8400bf9 (2026-11-17, Site-26010), associated merged MR2 https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/2. Its description explicitly links removing internal API JWT/signing-key/DocumentAccessContext checks to trusting services in a closed network; caller owns end-user checks. Its risk section requires closed-network access and explicitly verifying absence of ingress. This is documented architecture/security intent, not incidental or stale wording. Root README lines46-48 also retains no-ingress guidance and needs alignment only once the new ingress retains trusted-network reachability. Corporate host naming by itself is not evidence of a network boundary. Live ingress controller exposure/access controls not verified in this turn. Local edits remain uncommitted, no background operations. User clarification is intermediate; parent ingress MR work remains active.

## Internal ingress publication proposal (2026-11-17)
User confirms *.dev.youdo.corp is the internal network and considers this ingress safe; accept this task/environment-scoped network context rather than adding unrequested access-control work. Supersedes previous uncertainty about intended trust boundary; no independent network audit claimed. Final host youdo-kyc-api-int.dev.youdo.corp. Local change set adds api ingress and updates3docs/instructions (AGENTS.md, README.md, devops/README.md). Helm render/YAML comparison passed: only api.ingress added, actual stand host youdo-kyc-api-int-devops-923.dev.youdo.corp -> api Service80 -> port8080, other2routes retained. Agent lint0errors/0warnings/1info, diff checkPASS. Prepared additional commit `add internal api ingress for kyc dev` on existing branch/MR4; no branch rename. Proposed final MR title `DevOps-923 Configure kyc dev secrets and internal api ingress`, concise Russian combined-scope body under ai-data/gitlab-workflow/DevOps-923/kyc/ingress. MR4remainsopened at86db5c8. Preserve ready/assignee/squash/source-delete settings. MR pipeline builds/pushes4images and tests; deployments manual. Second-gate approval pending before staging/commit/push and exact MR metadata update. No runtime changes or background work.

## Additional ingress commit published (2026-11-17)
User confirmed exact final publication proposal with `Подтверждая`. Snapshot matched; entire staged and resulting commit patch exactly matched approved ingress/review.patch. Additional commit7a002653bbd93cc5691a45d95a2a279cbc66ea85 `add internal api ingress for kyc dev` pushed to existing task branch/MR4. It adds3line api ingress block and aligns AGENTS.md/README.md/devops README:4files,11insertions/7deletions. Exact approved MR title/body updated by single PUT and read back; source/target, ready, assignee, squash and deletion settings preserved. Independent helper verify confirms remote branch/MR SHA, exact title/body and metadata. Pipeline143321 RUNNING https://gitlab.youdo.sg/youdo/microservices/kyc/-/pipelines/143321; inspect/cancel on that page. No local background processes remain; checkout clean. No deployment, merge, DNS or source-secret cleanup performed.

Expected deployed internal URL after separately started ordinary deployment: http://youdo-kyc-api-int-devops-923.dev.youdo.corp . Current earlier deployed revision does not acquire ingress merely from source publication. User-confirmed internal domain context retained; no separate network audit claimed. Helm render/YAML/diff and agent lint (0errors/0warnings/1info) passed. Task-scoped ingress learning outcome recorded pass from actual implemented/rendered behavior, not publication approval alone. Remaining acceptance in central TODO.

## Nginx Nomad/Kubernetes routing proposal (2026-11-17)
User requested nginx config in automation-services with existing B2B render flow; clarified nexus meant Kubernetes, Nexus only stores images. Existing clean checkout inspected, origin/master refreshed toa87ac230. No first-gate edit approval yet; no repo edits. Proposed branch DevOps-923-kyc-nginx-routing from origin/mastera87ac230 targetingmaster; no existing MR for that branch.

traefik.youdo.com.j2 preserves Host and proxies to variable $proxy_backend, supporting either orchestrator. Actual VK group defines global nginx_proxy_traefik=proxy.service.vk-test.consul and nginx_dev_traefik_addr=traefik.dev.youdo.corp. Shared template currently ignores item.nginx_proxy_traefik, so merely adding per-vhost dev override wrongly routes to Nomad. Minimal proposal gives item.nginx_proxy_traefik precedence, retaining existing global/default fallbacks. Existing normal Nomad render is equivalent apart from blank lines; strict Jinja preview selects Nomad backend for test7 and Kubernetes backend for dev task host while retaining Host. Initial preview assertion compared blank-line layout too strictly; corrected nonempty-line comparison passed, no source edit involved.

Proposed VK balancers_test nginx_vhost_str entries: one inside existing nginx_platforms loop for youdo-kyc-api-ext.{{ platform }}.youdo.sg -> Nomad global backend, plus dynamic dev entry exact youdo-kyc-api-ext.dev.youdo.sg and regex ^youdo-kyc-api-ext-.*\.dev\.youdo\.sg$ -> nginx_dev_traefik_addr, wildcard.youdo.sg certificate. Nomad web_ex.j2 matches public Host youdo-kyc-api-ext.<stand>.youdo.sg, and Kubernetes ingress matches task host; no Host rewriting required. Outer YAML, templated vhost string, from_yaml and vhost template must all render (existing role flow). Existing vhosts must retain their rendered behavior. Do not change obsolete parallel YAML service catalog, unrelated inventory or deploy runtime. Internal .corp API/worker route remains through internal Traefik and is outside this public nginx edge proposal. No prod scope.

Before final publication, perform full affected inventory render and regex checks, existing vhost regression, diff check and suitable local nginx syntax check if toolchain permits. Shared template reuse prevents an unnecessary KYC-specific template. Second-stage publication and separate rollout approvals remain required. All read-only probes complete; no background operations remain.

## Dedicated nginx vhost prepared (2026-11-17)
User revised previous proposal: leave traefik.youdo.com.j2 unchanged and implement a dedicated B2B-style vhost. Treat direct instruction to implement this alternative as first-stage approval of previously proposed automation-services branch/base with revised template scope. Created DevOps-923-kyc-nginx-routing from origin/mastera87ac230; clean existing checkout preserved. Added roles/nginx/templates/vhost/youdo-kyc-api-ext.youdo.com.j2 based on existing business-mock-api pattern, using dedicated nginx_kyc_api_ext_youdo_com_backend and optional nginx_preserve_host (true in both new inventory entries). Updated only VK balancers_test inventory: per-platform entry inside nginx_platforms loop and appended dynamic dev entry with base/task regex. Nomad backend is youdo-kyc-api-ext.<platform>.vk-test.youdo.local; dev backend traefik.dev.youdo.corp. TLS uses existing wildcard.youdo.sg. No shared template or Yandex/prod/internal corp routes changed.

Verified outer YAML and actual Ansible2.13Templar nginx_vhost_str/from_yaml:920existing ->942total vhosts; all920prior items identical/orderpreserved;21Nomad+1dev new templates rendered fully with no unresolved variables. Host and backend assertions passed, all5tested KYC base/task/numeric/feature/Nomad names select exactly1vhost; internal API/worker and unrelated B2B do not select KYC. Existing shared templates untouched. Initial host-match harness encountered an existing item without server_name; corrected harness skips absent server_name and full checks pass. No runtime actions. Target nginx syntax check remains pending: local1.18does not support existing http2 on directive. Do not claim target nginx -t passed.

Publication proposal saved ai-data/gitlab-workflow/DevOps-923/automation-services/nginx-routing: exact2file patch/body/proposal/checks and rendered KYC configs. Proposed commit `add kyc external api nginx routing`, ready title `DevOps-923 Add kyc external api nginx routing`, source task branch -> master, user assigned, squashfalse/source-delete-on-mergetrue. CI inspected: initial branch push suppresses automatic Molecule jobs via zero-before-SHA, MR source lacks CI_COMMIT_BRANCH; existing manual Nomad job may be exposed, will not run it. No automatic rollout/release; runtime apply/reload separately approved. Second-stage publication confirmation pending. Local render/tests finished; no background commands remain.

## Production inventory extension prepared (2026-11-17)
User explicitly requested adding prod_selectel to the pending nginx change. Added only one entry at the end of inventories/prod_selectel/group_vars/balancers nginx_vhost: public youdo-kyc-api-ext.youdo.com, dedicated KYC template, backend youdo-kyc-api-ext.proxy.youdo.local, wildcard.youdo.com. Like existing B2B prod entries, nginx_preserve_host is omitted: Nginx default Host is backend $proxy_host, matching expected internal Traefik route. Do not preserve public Host without a verified matching prod router. Backend naming follows existing production B2B convention; no live KYC production Nomad router/deployment independently verified and KYC repo currently has no production HCL, so this is a prepared edge route, not claimed production readiness.

Actual production outer YAML/Ansible template render passed;70existing vhost items unchanged and ordered; new certificate path/backend/Host assertions passed. New rendered production config/checks saved alongside22test/devrenders. git diff --checkPASS. Scope now3files: prod inventory, VK inventory, dedicated template; shared template unchanged. Expanded proposal/body/patch saved; prior2file publication snapshot superseded by publication-with-prod-snapshot.json. Commit/MR names unchanged. Publication confirmation remains pending for complete3file scope; no staged changes, commit, push, external apply/reload or background operations.

## Single test-balancer vhost application instructions (2026-11-17)
User asked how to apply only the new domain, not for agent runtime execution. Role inspection found nginx-vhost-only also selects default.conf, so a tag-only recommendation would change more than requested. Prepared local generated helper ai-data/gitlab-workflow/DevOps-923/automation-services/nginx-routing/apply-dev-vhost.yml (outside repo): hosts balancers_test, explicit --limit balancer_test01, filter rendered nginx_vhost_str/from_yaml to exactly youdo-kyc-api-ext.dev.youdo.sg, assert exactly1entry, import existing nginx role tasks_from vhost_configs only, then nginx -t before notified reload handler. Imports base-vars only for existing managed-file header; no Vault fetch required by these selected tasks. Requires existing cert/includes and source template already in local checkout. Does not install packages, certificates, default.conf, other vhosts or production files.

Local syntax-check passed; list-tasks confirms exactly assert, single role template loop and nginx -t. Existing inventory warnings for invalid group chars and group/host name collisions observed, not task findings. No remote connection/apply/reload executed. In check mode templating diff is previewed and command nginx -t is skipped; normal run executes validation before end-of-play reload. If validation fails, new config remains on disk but reload is not executed. Normal handler reloads nginx as a whole, while only one vhost file is changed. No background commands remain. Instructions are an intermediate operation guide; original MR publication still pending and no user runtime acceptance inferred.

## User-applied nginx and redeployment readiness (2026-11-17)
User reports applying the single-vhost playbook and asks whether to deploy the new version. Read-only GitLab confirms MR4head7a00265/pipeline143321SUCCESS, all4image builds3305091-3305094and unit tests3305095SUCCESS; latest `1 deploy dev` job3305096 remains manual. Independent public external API GET /health/live now HTTP200 with {"status":"ok"}, resolving previously observed301route symptom. No agent deployment/retry/apply. Advise user to start latest pipeline job3305096, not old pipeline143316: the latest commit carries internal ingress. Internal ingress URL after deployment expected http://youdo-kyc-api-int-devops-923.dev.youdo.corp. No data deletion or previous-source secret cleanup. This is intermediate rollout guidance; acceptance/lifecycle and MR publication/merge remain pending. All probes completed, no background commands remain.

## Internal ingress rollout verified (2026-11-17)
User reports deploy3305096SUCCESS and requests verification. Read-only GitLab confirms job/pipeline143321SUCCESS at7a002653bbd93cc5691a45d95a2a279cbc66ea85. Jenkins test/209 resultSUCCESS, buildingfalse, duration115860ms. Log confirms selected KYC tag devops-923-kyc-dev-vault-path-143321, api/api-ext/worker rollout success, all3application pods and PostgreSQL1/1Running/0restarts at build snapshot, pre-migration Job Completed. This is repeat deployment in same namespace dev-devops-923; independent database-row persistence audit not performed.

Independent current GETs allHTTP200: external API https://youdo-kyc-api-ext-devops-923.dev.youdo.sg and internal API http://youdo-kyc-api-int-devops-923.dev.youdo.corp and worker http://youdo-kyc-worker-devops-923.dev.youdo.corp, each /health/live returns {"status":"ok"} and /_/healthcheck returns Healthy. This directly confirms new internal ingress is reachable and application PG/Rabbit readiness checks pass. Business/provider workflow, extend/delete and old-source secret cleanup not performed. No runtime mutations or retries by agent; all diagnostic/background commands finished.

## Ansible nginx MR published (2026-11-17)
User explicitly requested publishing the prepared Ansible MR, authorizing the reviewed3file scope including prod_selectel. Snapshot-with-prod check matched. Entire staged and resulting commit patch byte-identical to review-with-prod.patch. Commit3f3c5912cae826f167154897fcabf46ac95d7397 `add kyc external api nginx routing`,3files/53insertions, on approved DevOps-923-kyc-nginx-routing. First sandbox push hung without output, interrupted with exit130; read-only API returned404for branch before retry. Elevated push succeeded without force; no duplicate write. Created [automation-services MR1399](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1399). Helper API readback verifies exact commit SHA/title/body/source/target master, ready, assignee a.solonenko, squashfalse and remove-source-on-mergetrue. Initial pipeline list empty, no CI success claimed. No Ansible apply/reload, merge or production rollout performed by agent. Clean checkout and publication process completion verified.

Original dedicated-vhost scope updated only by user additions (prod_selectel); shared traefik template unchanged. Source verification covered23new configs (21Nomad,1dev,1prod) and990unchanged prior inventory items, render/regex/diff checks passed. Target production nginx -t and backend router readiness remain pending. User previously applied test-only vhost and both external/internal KYC health verifiedHTTP200 after deploy3305096. All task operations completed, no agent background processes remain. Central TODO updated to publication complete with actual remaining review/rollout/lifecycle/source-key steps.

## Task metrics: DevOps-923-nginx-mr

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-923-nginx-mr",
  "created": "2026-11-17T17:18:03.270723+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Reviewed3file patch equals staged/commit;23new renders with990old items preserved; MR1399 exact metadata verified, no rollout; sandbox push recovered after404readback",
  "updated": "2026-11-17T17:18:03.270773+03:00"
}
```

Final independent publication verification: MR1399metadata/SHA matches; pipeline143333SKIPPED as expected from existing rules (https://gitlab.youdo.sg/sysadmins/automation-services/-/pipelines/143333). No local/background processes remain.

## Session closeout decision 2026-11-17
User states item1merged: KYC MR4and automation-services MR1399 accepted as merged based on user confirmation, without an additional API audit. Dev deployment and endpoint evidence remain accepted. Item2production route verification is explicitly deferred in central TODO, and production Nomad HCL must be prepared first. This message records future work, not authorization to implement/deploy production HCL now. Item3is cancelled: do not perform extend/delete lifecycle checks or delete original Vault keys under this task. Earlier pending references to these cancelled steps are historical and superseded by this decision; no such operations were performed or claimed successful.

Remaining task scope: prepare production KYC Nomad HCL as deferred work and, after separately authorized production rollout, verify the production nginx/Traefik route and run target nginx -t. Existing prepared nginx inventory alone is not production service readiness. No external state changes in this closeout. All prior task commands finished; no background operations remain.

## YouTrack performed-work comment draft 2026-11-17
User requested preparing a performed-work comment for DevOps-923. Fresh issue/comment GET confirmed the matching KYC dev Kubernetes issue and no existing comments. Draft checked against rollout, ingress, Vault and MR evidence above and the closeout decision; no fresh runtime claim or production readiness claim. Existing central TODO retains deferred production HCL/routing; cancelled lifecycle and source-key cleanup remain cancelled. No external write performed. Exact draft is saved locally at `/home/slnnk/ai-data/youtrack/DevOps-923-comment.md` and reproduced below. Posting requires explicit confirmation of this text per company CONTEXT; approval and readback remain pending. All task commands have finished; no background operations remain.

```markdown
KYC добавлен в деплой на dev Kubernetes.

- Добавлен в каталог Jenkins: `youdo-kyc`, включая сборку полного набора dev-сервисов — [MR !3](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins-pipelines/-/merge_requests/3).
- Dev-конфигурация переведена на отдельный путь Vault `secret/dev/projects/kyc`; необходимые секреты скопированы с сохранением существующих данных. Добавлен ingress для внутреннего API — [MR !4](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/4).
- Настроена маршрутизация внешнего API через nginx для dev и тестовых стендов; подготовлена конфигурация для production — [MR !1399](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1399).
- Проверены первичный и повторный dev-деплой: миграции завершились, API, внешний API и worker успешно запущены. После повторного [деплоя](https://gitlab.youdo.sg/youdo/microservices/kyc/-/jobs/3305096) у всех трёх компонентов `/health/live` и `/_/healthcheck` возвращали HTTP 200.

Dev-деплой проверен. Бизнес-сценарий с провайдером не проверялся. Production отложен: сначала требуется подготовить Nomad HCL, затем после согласованного развёртывания проверить маршрут nginx/Traefik и `nginx -t`.
```

## YouTrack comment user revision 2026-11-17
User removed the deployment/health verification bullet and the concluding paragraph about provider testing and deferred production from the proposed comment. This is a task-specific editorial direction; operational evidence and deferred production TODO remain unchanged. Updated exact draft below supersedes the prior comment draft. No posting authorized or performed; awaiting confirmation of revised text. Local draft updated; no background operations remain.

```markdown
KYC добавлен в деплой на dev Kubernetes.

- Добавлен в каталог Jenkins: `youdo-kyc`, включая сборку полного набора dev-сервисов — [MR !3](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins-pipelines/-/merge_requests/3).
- Dev-конфигурация переведена на отдельный путь Vault `secret/dev/projects/kyc`; необходимые секреты скопированы с сохранением существующих данных. Добавлен ingress для внутреннего API — [MR !4](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/4).
- Настроена маршрутизация внешнего API через nginx для dev и тестовых стендов; подготовлена конфигурация для production — [MR !1399](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1399).
```

## Approved YouTrack comment publication 2026-11-17
User explicitly approved the revised three-bullet text with `Да`. Fresh comment GET found no matching existing comment. One POST created comment `74-125619` in DevOps-923; individual GET verified exact approved text and MR URLs. Receipt: `/home/slnnk/ai-data/youtrack/DevOps-923-comment-receipt.json`. Original draft, requested omissions and final wording remain above. Requested comment work is complete; production follow-up remains deferred in central TODO and cancelled checks remain cancelled. No issue status change, deployment or other external mutation performed. Publication command exited0; no task background operations remain.
