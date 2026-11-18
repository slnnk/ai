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

## Production deployment preparation plan 2026-11-18

The user requested the plan for the deferred production follow-up. YouTrack DevOps-923 still describes dev Kubernetes onboarding. GitLab GET verified KYC MR !4 merged and remote master at 454d393b, automation-services MR !1399 merged at 32fb12c7, no KYC release tags, and no production HCL in the remote master devops tree. The checkout remains clean on the previous dev branch.

Proposed KYC branch DevOps-923-kyc-production-deploy from current origin/master after approval. Reuse the Nomad Selectel and v3 production CI patterns with an explicitly reviewed manual first rollout, one version for all four images, and blocking Pre EF migrations. The migrations helper exports CON_STR and invokes /app/entrypoint.sh. Image entrypoint and Pre-only behavior require verification. Validate effective production variables, DB and RabbitMQ access, Vault policy and per-process NeuroVision/KEK configuration, HCL and CI rules. Route the public nginx name to Traefik Host youdo-kyc-api-ext.proxy.youdo.local. Keep internal API and Worker private, validate nginx syntax on the target and smoke test health and the webhook route after approved rollout. Start with the B2B flag disabled. A first Nomad deployment has no previous job version to revert to.

Live production dependencies, rollout and routing remain pending. The existing DevOps-923 TODO entry retains these actions. Cancelled dev lifecycle and source-key cleanup remain closed. No repository edits or external writes.

## Production AUTO configuration prepared 2026-11-18

The user directed implementation of production HCL and the existing B2B AUTO CI flow, correcting the manual-mode proposal, and asked to follow nearby service HCL. Created the previously proposed DevOps-923-kyc-production-deploy branch from refreshed origin/master 454d393b. Added devops/production.hcl based on DocValidation web/svc layout and B2B PostgreSQL settings, and connected v3/.deploy-prod-full-auto.yml with auto, PostgreSQL youdo_kyc, and worker count one. The selected production secret path is the existing secret/dotnet/business, fields KycNeuroVisionApiToken, KycNeuroVisionScenarioId, KycNeuroVisionScenarioSecret, and KycEncryptionKekV1. Nomad also uses secret/resources/databases/postgres managed_host and youdo_password, and secret/resources/rabbitmq youdo_conn_string. Values and policy access were not verified in production.

GitLab CI Lint simulation on master passed with automatic deploy production and release jobs. The existing child runs blocking EF Pre and invokes the same idempotent EF runner at Post. Offline Nomad validation passed with the svc count zero warning common to the template's stop/start layout. Local JSON checks verified the task, image, Vault key, health check, database name and nginx/Traefik host wiring. Production DB_ADDR and the HCL host must resolve to the same database. Prod driver, Vault access, DB presence/permissions, and actual rollout/routing remain unverified. No staging, commit, push, MR or production change. Existing TODO remains open for publication, readiness checks and rollout.

## Production Vault path selected 2026-11-18

The user reported creating the production secrets at dotnet/kyc. Updated all three Nomad task templates to secret/dotnet/kyc, superseding secret/dotnet/business in the preceding local configuration. Offline Nomad validation passed with the same svc count warning. The rendered job confirms the new path for api, api-ext and worker. The production Nomad token policy and secret values remain unverified. No Vault or GitLab writes.

## Production HCL conventions and internal API name 2026-11-18

The user pointed out that B2B HCL does not use toJSON and requested naming the internal API api-int. Replaced toJSON in all Vault env templates with the quoted interpolation used in the neighboring DocValidation and Business Tickets jobs. Renamed the internal task, service, port label and generated Traefik route to youdo-kyc-api-int and api_int_port. Retained the api image expected by existing CI and dev/test deploys. Offline Nomad validation passed with the existing svc count warning. Rendered job checks verified both API names, routes and health checks, the internal image, and the Vault interpolation. No publication or runtime changes. Existing DevOps-923 TODO remains open for the production rollout.

## Production MR proposal 2026-11-18

Prepared Draft: DevOps-923 Add KYC production deployment, commit add kyc production deployment, branch DevOps-923-kyc-production-deploy to master, base 454d393b, assignee a.solonenko, squash off and source removal on merge. GitLab GET found no existing MR and ls-remote confirmed current master and no source branch. Current task patch has only .gitlab-ci.yml and devops/production.hcl. Exact body, patch, proposal and snapshot saved under ai-data/gitlab-workflow/DevOps-923/kyc/production. Offline Nomad validation passed with the svc count warning, rendered configuration checks passed, GitLab CI Lint master dry run passed with automatic prod and release. MR builds and pushes four MR images and runs dotnet tests. Merge triggers production and release. Draft status proposed while production Vault policy, database alignment and routing remain unverified. Second approval pending. No stage, commit, push, MR or deployment.

## Approved production Draft MR publication 2026-11-18

The user confirmed the reviewed publication proposal with `Да`. The snapshot matched and the entire staged and committed diffs matched review.patch byte for byte. Commit 67d4fc45bdc0a13189e19c1f86b29ba885b5c538 `add kyc production deployment` contains two files and 339 insertions. Pushed the source branch and created [KYC Draft MR !5](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/5). GitLab readback verified SHA, exact title and body, source to master, Draft, assignee a.solonenko, squash off, and source deletion on merge. MR pipeline 143534 initially created. No merge or production deployment. The central DevOps-923 item remains open for checking production Vault and DB alignment, rollout, and verifying nginx/Traefik.

## User correction about Draft MRs 2026-11-18

The user rejected the use of Draft for MR !5 and set a durable preference to create MRs without Draft. The previous proposal chose Draft because production prerequisites remained unverified. The company gitlab-workflow conventions now require new MRs to be Ready and pending checks to be reported separately. Existing MR !5 readiness remains pending explicit approval to update it. This does not authorize merge or deployment.

## Approved production MR Ready status 2026-11-18

The user confirmed removing Draft with `Да`. GitLab GET verified MR !5 was open at 67d4fc4 and auto-merge was disabled. One PUT changed the title to DevOps-923 Add KYC production deployment. GET readback verified Ready, the same SHA, description, branches, assignee and settings. MR pipeline 143534 was running. No merge or production deployment. Production prerequisites remain tracked in the existing TODO.

## Production prerequisites accepted 2026-11-18

The user confirmed that Nomad can read the KYC Vault path under the established production policy and that the CI/runtime PostgreSQL target was checked, citing the existing shared deployment pattern. Accept both prerequisites for this task on user confirmation. The agent did not perform an independent production read or connection test. GitLab readback confirmed Ready MR !5 at 67d4fc4 and running pipeline 143534. Separate merge approval and post-rollout migration, health and routing checks remain.

## Production PostgreSQL Terraform proposal 2026-11-18

The user requested recent activity and a description of the Terraform changes needed for the KYC production database. GitLab showed KYC MR !5 Ready and open at 67d4fc4 with pipeline 143534 running. Selectel Terraform master 680d69d includes DevOps-925 MR !96. Its MR grants apply succeeded, its DBaaS apply remained manual, and both master applies in pipeline 143530 remained manual. Live state was not inspected.

Proposed selectel-tf branch DevOps-923-kyc-prod-db from origin/master 680d69d. Append youdo_kyc to the B2B database list in prod-dbaas/terraform.tfvars and the B2B baseline grants list in prod-dbaas-grants/terraform.tfvars. Appending preserves existing count indexes. The service and Pre EF migrations use youdo. Review a plan with no unrelated changes. Apply DBaaS before grants and verify that CI DB_ADDR and Nomad managed_host point to the same cluster before merging the automatic KYC rollout. First-stage approval remains pending. No code or production changes. No background task commands remain.

## Production hardware balancer single-vhost procedure 2026-11-18

The user asked how to apply the new KYC vhost only. Prepared a local standalone playbook selecting a single present youdo-kyc-api-ext.youdo.com entry from production nginx_vhost, including the existing nginx vhost_configs tasks, then running nginx -t before the notified reload. Inventory and list-hosts confirmed balancers_hardware selects only msk3-balancer02 and msk3-balancer03. Serial one and fatal errors stop the rollout on a failing host. Syntax check and offline check-mode render passed using the inventory and role template with a substituted local test handler. No connection to production hosts or deployment. The existing DevOps-923 item retains the rollout verification.

## Production PostgreSQL Terraform MR prepared 2026-11-18

The user followed the first-gate branch proposal with `Подготовь МР`. Created DevOps-923-kyc-prod-db from origin/master 680d69d in the clean selectel-tf checkout. Added youdo_kyc at the end of the B2B lists in both Terraform stacks. Git diff check, Terraform console comparisons, and offline Terraform validate for both stacks passed. Existing prod-dbaas tfvars formatting was preserved. No live plans or apply.

Prepared Ready MR DevOps-923 Add KYC production database, commit add kyc production database, source DevOps-923-kyc-prod-db to master, assignee a.solonenko, squash off, remove source on merge. Exact body, patch and snapshot saved under ai-data/gitlab-workflow/DevOps-923/selectel-tf. CI runs validation and plan for both stacks on MR. Apply jobs are manual and DB creation precedes grants. Publication approval remains pending. No stage, commit, push or MR creation. No background operations remain.

## Production hardware vhost applied 2026-11-18

The user reported applying the production hardware vhost. Agent HTTPS requests with verified TLS to both hardware balancers and the public DNS name returned identical HTTP 404 bodies. The direct HTTP Traefik backend returned the same body. This supports edge forwarding with the upstream KYC route still absent. MR !5 pipeline 143534 succeeded and remote master remains 454d393b, before the KYC production commit. No agent remote apply or nginx -t. Merge and post-rollout health and route confirmation remain pending.

## Production PostgreSQL Terraform MR published 2026-11-18

The user approved the exact second-stage proposal with `Да`. Snapshot comparison passed. The full staged and commit diffs matched the approved patch. Pushed d01f0adeefd342f82890a5306e3f622a7f471ef3 to DevOps-923-kyc-prod-db and opened [Ready MR !97](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/merge_requests/97). Readback verified source and target branches, title, body, commit, assignee a.solonenko, squash off and source removal on merge. [Pipeline 143539](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/pipelines/143539) started. Publication is complete. No merge, manual apply or KYC prod rollout was performed. The existing TODO tracks DB plans, creation and grants, then the KYC production rollout and routing checks.

## Production DBaaS plan includes earlier cluster changes 2026-11-18

The user flagged extra changes in [DBaaS plan 3308206](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/jobs/3308206). This plan on d01f0ad creates only youdo_kyc and its CONNECT grant and also adds log_min_duration_statement=30000 to the config maps of both prod PostgreSQL clusters in place. [Earlier DevOps-925 plan 3307743](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/jobs/3307743) shows the identical two cluster updates and zero resource adds. The setting entered master through 88dc8ea before KYC. The MR !97 diff only adds the KYC database to the two lists. [Grants plan 3308207](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/jobs/3308207) adds 21 KYC grants and changes or destroys zero resources. Apply jobs in both pipelines are still manual.

Separate the existing cluster configuration difference from the KYC change. Check the actual threshold and agree on the cluster configuration before any apply. A KYC-only plan must show two resource additions, zero changes and zero deletions. The current TODO already tracks plan review before production apply. No changes to GitLab or production were made. No background operations remain.

## Selectel PostgreSQL primary and logging threshold check 2026-11-18

The user reported a possible PostgreSQL primary switch when reapplying log_min_duration_statement. Job 3308206 installed Selectel provider v6.8.0. The provider source sends config updates through the configuration path and resizes only for node_count, flavor or flavor_id changes. PostgreSQL 16 declares the parameter PGC_SUSET and supports applying it without a restart. Selectel documents a per-parameter is_restart_required field and documents primary switches during cluster scaling or loss of the primary. Public references do not provide the live flag for this parameter on the project.

The regional API returned HTTP 401 without the required project-scoped IAM token. The C2C primary name did not resolve for the read-only PostgreSQL check even outside the sandbox. GitLab jobs 3308121, 3308208 and 3307745 remained manual with no start timestamp. No observed application or primary switch can be attributed to these jobs. The existing plan-review TODO remains open. Read-only closure requires the Selectel parameter metadata for the actual cluster type or the corresponding restart marker in the control panel. No production changes or background operations.

## PostgreSQL restart observed during Terraform apply 2026-11-18

User asked whether [apply job 3308208](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/jobs/3308208) was restarting PostgreSQL. Job started 18:27:41 MSK and planned KYC database and CONNECT plus log_min_duration_statement=30000 on both clusters. Authenticated read-only TLS SQL on both C2C nodes returned pg_postmaster_start_time on the current primary at 18:30:54 and on the current replica at 18:31:10 MSK. Both returned 30s and pending_restart=false. The restart during apply is confirmed for both C2C nodes. This supersedes the earlier inference from the supplied control panel screenshot. A primary switch and outage duration are unverified. The B2B endpoints answered TCP 5432. No read-only B2B SQL credential was available for postmaster timing.

Terraform reported B2B modification complete in 2m19s, C2C in 3m21s, and KYC database creation complete in 1m09s. The run was still creating the CONNECT grant at the last recorded check. No agent-triggered apply, retry, or cancellation.

## Selectel restart support question 2026-11-18

GitLab job 3308208 finished successfully at 18:34:04 MSK. KYC grants job 3308209 was still manual when checked. Source review of [Selectel provider v6.8.0](https://github.com/selectel/terraform-provider-selectel/blob/v6.8.0/selectel/dbaas.go#L275-L306) found that a config change submits the full desired config map. Keys present remotely but absent from the desired map are sent as null. The provider waits for ACTIVE. Selectel API documents null as reset to default and exposes is_restart_required on parameter metadata. Public docs found no statement that this parameter requires restart. The provider has no explicit restart in this path. Prepared support question asking which operation or parameter caused the observed C2C restarts, whether unchanged restart-sensitive fields in the full configuration can cause them, whether B2B restarted or either primary changed, and which method can apply only the logging threshold. No support ticket was submitted.

## Production Pre migrations target diagnosis 2026-11-18

KYC MR !5 merged at 97a84a1c. Child job 3308276 failed in NpgsqlDatabaseCreator.CreateAsync with PostgreSQL 42501 on the administrative postgres connection. Selectel job 3308208 succeeded before this failure and created the B2B youdo_kyc database and CONNECT. Job 3308209 also succeeded. The Terraform MR !97 was still open. GitLab GET showed no KYC project or subgroup DB_ADDR. Inherited DB_ADDR expands to POSTGRES_ADDR_C2C, which matches the Terraform C2C primary. Business Tickets and Business Auth each have project DB_ADDR=$POSTGRES_ADDR_B2B, scope wildcard, env_var, raw false, unprotected and unmasked. The source B2B variable matches the B2B Terraform primary. User requested the same project-level mapping. Awaiting the explicit approval for the GitLab create operation. No GitLab updates or deploy retry performed.

## KYC B2B CI database override applied 2026-11-18

The user explicitly approved the KYC project variable creation. GET confirmed no prior project DB_ADDR. One GitLab POST created DB_ADDR=$POSTGRES_ADDR_B2B, wildcard scope, env_var, raw false, unprotected, unmasked. A fresh GET verified every setting including hidden false, matching Business Tickets and Business Auth. Parent pipeline 143542 on master 97a84a1c and its prod bridge 3308269 had failed. Child 143543 failed Pre migrations and release job 3308271 was skipped. No retry or new pipeline requested or performed. Restart requires separate approval.

## Production rollout verified and monitoring failure isolated 2026-11-18

Pipeline 143542 failed solely in deploy-monitoring job 3308272. The deployment bridge and child 143543 succeeded after the external retry of Pre job 3308285, which applied InitialKyc and OutboxRetrySchedule. Post migrations, Nomad API rollout, svc start and release job succeeded. The svc trace records one healthy Worker. Release master-46 points at 97a84a1c. Internal and external readiness returned 200. Public DNS and both hardware IPs with the production SNI returned HTTP 200 and the expected live body. Selectel TF MR !97 was verified merged at 737cb10f.

Monitoring deploy runs after release and failed with cat unable to open *.yml. KYC includes the shared monitoring template without a Pyrra SLO rules file, so there was no generated YAML to apply. No retry, monitoring changes, independent nginx -t, or business canary.

## Monitoring template removal proposed 2026-11-18

The user requested removal of the shared monitoring include after the monitoring job failed without KYC Pyrra rules. Proposed KYC branch DevOps-923-remove-kyc-monitoring-template from current origin/master 97a84a1c. Scope is one .gitlab-ci.yml include line. Merge would trigger the existing automatic production deployment again. First approval pending. No branch or repo edits.

## Monitoring template removal prepared 2026-11-18

The user approved the proposed branch and requested an MR. Fetched origin/master 97a84a1c, created DevOps-923-remove-kyc-monitoring-template, and removed exactly v3/.monitoring.yml from .gitlab-ci.yml. Diff checks and CI Lint master dry run passed. Both monitoring jobs are absent, build/test and auto prod deploy/release remain. Proposed Ready MR DevOps-923 Remove KYC monitoring template, commit remove kyc monitoring template, source to master, assignee a.solonenko, squash off, source delete on merge. Exact patch, body and proposal saved under ai-data/gitlab-workflow/DevOps-923/kyc/remove-monitoring. Second approval pending. No stage, commit, push or deployment.

## Monitoring template removal MR published 2026-11-18

The user explicitly approved the reviewed Ready MR. Snapshot matched and the entire staged and committed diffs matched the saved one-line removal. Pushed d4908d29d09884965ca4f2cf2c0371c9f5d6447d and opened [Ready MR !6](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/6). GitLab verified draft false, exact title/body, source to master, SHA, assignee a.solonenko, squash false, and source deletion on merge. Pipeline 143551 created. No merge or production deploy. Merge into master will trigger the existing automatic deployment and release.

## Final production rollout and YouTrack addendum draft 2026-11-18

The user reported closing DevOps-923. GET confirmed YouTrack Fixed. GitLab verified KYC MR !6 merged at 44cd55cc, successful master pipeline 143552 and child 143553 with both migration jobs and service start successful, the release master-49 pointing to the same commit, and no monitoring jobs. Public liveness returned status ok and internal readiness 200. Terraform MR !97 also merged.

Prepared the following exact Markdown addendum to existing YouTrack comment 74-125619, whose dev text is preserved in the full local draft. No YouTrack update made.

```markdown
### Продакшен

- Настроен автоматический деплой KYC в Nomad Selectel для внутреннего API, внешнего API и Worker. EF-миграции запускаются перед выкатыванием сервиса. [KYC MR !5](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/5)
- В B2B-кластере PostgreSQL создана база `youdo_kyc` и выданы права. В GitLab CI проекта задано `DB_ADDR=$POSTGRES_ADDR_B2B`. [Terraform MR !97](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/merge_requests/97)
- На hardware balancers применён nginx-vhost для `youdo-kyc-api-ext.youdo.com`. Публичный `/health/live` возвращает HTTP 200. [nginx MR !1399](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1399)
- Из GitLab CI убран шаблон мониторинга Pyrra, для которого в KYC нет SLO-правил. [KYC MR !6](https://gitlab.youdo.sg/youdo/microservices/kyc/-/merge_requests/6)

Прод-деплой завершился успешно, опубликован релиз `master-49`. [Пайплайн #143552](https://gitlab.youdo.sg/youdo/microservices/kyc/-/pipelines/143552)
```
