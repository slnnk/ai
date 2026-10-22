---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [data, daily-compilations, test5]
---
# Daily compilations subscription errors on test5

## Summary

Initial test5 errors are one daily-compilations subscription API404 chain; the generator is not required for subscription updates. User-approved minimal repository change only sets staging CI NOMAD_VAR_dc/proxy to vk-test. MR9 was published and subsequently user-merged; tag0.5.15 pipeline141347 built/released successfully. Staging3241027 failed403 submitting to Nomad. At failure, inherited Data NOMAD_STAGE_ADDR pointed to yandex-test and stage token differed from reviewed VK token. User subsequently authorized correcting both values in Data group; exact values GET-verified and temporary project overrides removed. No project/pipeline overrides exist; protected0.5.15 tag can receive protected variables. Changing dc/proxy does not select the Nomad API server. VK daily-compilations job remains absent. User retried staging successfully as job3241056; fresh GET acceptance confirms API0.5.15/PostgreSQL running with0restarts, Consulpassing, /health and /users HTTP200. User promoted production deploymentedf404b3; job3241028 and pipeline141347 now SUCCESS, rollout2/2healthy with API0.5.15/0restarts, Consulpassing and sharedhealth200. No agent deployment or API write performed. Earlier direct deployment, image pin and Nomad defaults proposals below are superseded. Local tests/lint were skipped per user request. Generator assessment is in the final section.

## Task
Investigate two test5 LogReader exceptions and the suspected missing Data services, including the user-suggested daily-compilations-generator and recommended-tasks-generator.

## Context
Read-only investigation. Local daily-compilations HEAD 6e5c72a, monolith HEAD abc9c7ae1a5; no fetch, repository edits or external changes. Runtime inspected through current VK Nomad and Consul GET APIs. LogReader web URLs require login; exact exceptions read with SELECT from test5 YouDoLogsExceptions using Vault secret/resources/databases/mssql USER/PASSWORD in memory.

## Actions
Read exact exception GUIDs, traced DailyCompilationsService and IHttpDailyCompilationsClient, compared Data project README and deployment specification, read live Nomad job templates and enumerated jobs/catalog services. GET /health on the configured endpoint returned404. Diagnostic helpers are in /home/slnnk/ai-data/data-services-diagnosis/.

## Findings
- 92f770bb-aa4b-4118-99e9-57714e896048,2026-10-21 10:43:05.687: Refit.ApiException, HTTP404 in DailyCompilationsService.SetUserSubscriptionAsync line68.
- 0c48bad8-2ec5-4215-b308-c2962c77fd69,50ms later: wrapper exception `can't set subscribed setting for daily compilations`.
- Client GET/PUT /users/{user_id} uses DailyCompilationsEndpointUrl. Live test5 Nomad templates set http://v1.daily-compilations.vk-test.youdo.local; GET /health returns404.
- Current VK Nomad job list and Consul catalog have no names containing compilation or recommend. This establishes the expected daily-compilations service is absent from those inventories; no per-stand runtime audit was performed.
- Correct dependency is https://gitlab.youdo.sg/data/daily-compilations, the subscription API. Its README identifies daily-compilations-generator as the separate email selection producer. recommended-tasks-generator produces recommendations stored by recommended-tasks and is not implicated by these two stack traces.
- Cached local daily-compilations CI still declares yandex-test for staging dc/proxy; staging specification includes the API and PostgreSQL group. Remote current revision and full deployment prerequisites were not checked.
- During the local template read, an inline APNs private key field was exposed in output from automation-test-yandex/playbooks/deploy/app/roles/app_deploy/templates/environment.json.j2 (Push.Apns.PrivateKey). Value is not retained here; validity and consumer scope unverified.

## Changes
Knowledge-base bookkeeping only; no deployments, SQL writes, CI runs, source changes or Git mutations.

## Status and risks
Diagnosis complete. Restoring the shared API requires deployment preparation and explicit approval; follow-up proposal is tracked in ~/ai/TODO.md under nomad-test / Consul. Generator recovery alone does not supply the missing subscription API. Exposed inline key review is tracked under Security.

## Portable lesson
none

## Restoration preparation and user constraint (2026-10-21)

User requested preparation, then explicitly directed `ci менять не нужно`. This is task-scoped: no CI source changes for this restoration. The prior proposed CI edits are withdrawn. No repository edits, branch changes, publication or external mutations occurred. Existing service-deployment convention remains in force; direct deployment below is a proposed exception requiring explicit approval, not inferred authorization.

Fresh project204 GET and read-only fetch verify default master39b7fd86c433deeb70f442225d4d57278401867a, no openMRs, clean existing checkout on historical recovery branch. Only master/ latest/ historical branch images exist; tag0.5.14 image is absent. Master pipeline140799/build3223285 succeeded, digest sha256:0dd8eb937a52c68c053b0af4148340d5791a004fc67b3fc813d3741bdbde9b47. Current master CI automatically deploys staging and production on tags. Historical staging job2628835 and production2628836 in pipeline125685 both succeeded; retrying staging would require unavailable image0.5.14. Project CI variables are empty; inherited Data staging variables do not match reviewed VK address/token. No variables were changed.

Prepared proposal without CI changes: use existing staging.nomad and configs/staging.yaml byte-identical to reviewed master, render locally with version=master, dc=vk-test, proxy=vk-test, pin application image to reviewed digest, submit one new Nomad job daily-compilations to http://nomad.service.vk-test.consul:4646. Existing specification supplies one API group and one PostgreSQL group (default count1),100MiB/20CPU each, PostgreSQL10-alpine with sticky/migrating ephemeral allocation storage, app creates tables via db.create_all. This is a new empty subscription database; no historical subscriptions restored. Shared route v1.daily-compilations.vk-test.youdo.local serves consumers that use this address. Production is not a target of the proposed command.

Local validation passes with zero job warnings; driver validation skipped because the default local Nomad endpoint is unavailable. Local nomad job run -output successfully renders reviewed source. Fresh GET confirms job absent and8ready/eligible VK nodes; capacity reservation and runtime image pulling remain unverified. Docker Hub manifest postgres:10-alpine exists and includes linux/amd64. Registry metadata confirms application digest; no image rebuild/publication needed.

Prepared helper /home/slnnk/ai-data/data-services-diagnosis/prepare_no_ci.py defaults to local preparation only. Explicit --apply performs one POST /v1/jobs after checking source SHA/hashes, master image digest, job absence and absence of a previous receipt; EnforceIndex=true/JobModifyIndex=0 prevents overwriting a concurrently registered job. Nomad token is loaded from existing .env in memory. Request-pending receipt prevents automatic repeat after uncertain submission. No --apply executed.

Proposed command, pending explicit exception/deployment approval:

```bash
python3 /home/slnnk/ai-data/data-services-diagnosis/prepare_no_ci.py --apply
```

Acceptance after separately approved registration: both allocations running, Consul checks passing, GET /health200, read-only API response consistent with empty database; the reported subscription update needs an explicitly approved test write or user UI retry. Rollback would stop only this new job and requires separate approval; data should be preserved pending a decision. No persistent storage redesign or generator recovery is included. Central TODO now tracks approval/execution; preparation itself is complete.

## Approved repository preparation (2026-10-21)

User requested repository edits without checks, then explicitly approved branch DevOps-898-restore-daily-compilations-vk in data/daily-compilations from origin/master39b7fd86. Created the approved branch from that exact SHA in the existing clean checkout. Only deployments/staging.nomad changed: dc/proxy defaults vk-test, version default master, API image pinned directly to reviewed sha256:0dd8eb937a52c68c053b0af4148340d5791a004fc67b3fc813d3741bdbde9b47. The version variable now supplies task metadata; overriding it does not change the pinned API image. Database and resource specification unchanged. CI source unchanged; its explicit yandex-test variable overrides remain, so existing CI jobs are not retargeted by these defaults.

This supersedes the earlier proposal to deploy through the external preparation helper: repository change is now the requested deliverable. No checks, tests or lint were run after editing, as explicitly requested. Startup sync emitted no output. No commit, push, MR, tag, CI job, deployment or external variable update occurred. Publication/deployment still require separate approval. User-requested skip also covers final KB lint/index checks; index regeneration is bookkeeping only.

## Deployment-variable correction (2026-10-21)

User questioned repository dc/proxy defaults because deployment injects them. Existing .gitlab-ci.yml deploy:staging sets NOMAD_VAR_dc and NOMAD_VAR_proxy; those supply Nomad HCL variables at deployment. Reverted only the unnecessary hardcoded vk-test defaults to original empty strings in the approved task file/branch. This corrects the earlier direct-launch assumption while preserving CI source and external settings. Remaining local changes: version default master and pinned API image digest. No post-edit checks run per user request; no publication/deployment. This is a task-scoped correction, not a global rule to remove defaults from other services.

## Explicit CI-variable change requested (2026-10-21)

After confirming CI still supplied yandex-test, user explicitly requested changing those values. This supersedes the earlier no-CI-edits constraint only for the two staging YAML variables. In the already approved data/daily-compilations branch DevOps-898-restore-daily-compilations-vk, changed .gitlab-ci.yml deploy:staging NOMAD_VAR_dc and NOMAD_VAR_proxy from yandex-test to vk-test. No project/group CI variables, Nomad address/token, production job or other CI behavior changed. Existing staging.nomad default version/pinned image edits retained; dc/proxy defaults remain original empty values. No checks run per user request; no publication or deployment. Nomad address/token selection remains unchanged and is not verified to target VK, so changing these two values alone does not establish deploy readiness.

## CI-supplied image version restored (2026-10-21)

User explicitly requested removing Nomad image-tag changes because CI builds and deploys the new version. Removed the fixed API digest and default master version from deployments/staging.nomad, restoring the original required version variable and image registry.youdo.sg/data/daily-compilations:${var.version}. Together with the earlier dc/proxy-default correction, the Nomad file has been restored to its original content. The intended remaining repository change is only .gitlab-ci.yml staging NOMAD_VAR_dc/proxy from yandex-test to vk-test. No post-edit checks run per user request; no commit/publication/CI/deployment. Nomad address/token selection remains unchanged and requires consideration before deployment; the previous helper and pinned-image proposal are superseded and must not be used for the current deliverable.

## Publication proposal prepared (2026-10-21)

User requested publication and MR creation. Actual working diff contains only two .gitlab-ci.yml substitutions NOMAD_VAR_dc/proxy yandex-test -> vk-test; staged diff empty, Nomad file unchanged. Tests/lint intentionally skipped per user request. Proposed commit: use vk datacenter and proxy for staging. Proposed ready MR: DevOps-898 use vk datacenter and proxy for staging; source DevOps-898-restore-daily-compilations-vk -> master. Russian body: staging dc/proxy changed from yandex-test to vk-test, followed by DevOps-898 task link. Publication bundle and bound snapshot saved under /home/slnnk/ai-data/gitlab-workflow/daily-compilations-vk/daily-compilations/.

Inspected actual CI: branch push builds/publishes branch image and latest; release/staging/production jobs are tag-only. No deployment or tag proposed. NOMAD_STAGE_ADDR/TOKEN unchanged, so VK connection readiness is not established by these two edits. Concrete commit/MR names and image publication effects are presented for the second supervised approval; no stage/commit/push/MR performed yet.

## Publication completed (2026-10-21)

User replied `Да` to the concrete second-stage publication proposal, covering task-only stage/commit/source push/MR and stated branch/latest image publication. Pre-stage bound snapshot matched. Inspected complete staged diff: only two .gitlab-ci.yml staging substitutions, no unrelated staged content. Created commit ef37ce8927f80e25e6bda18a5434442812c1bfbc, subject use vk datacenter and proxy for staging; resulting patch matched approval and worktree clean. Pushed DevOps-898-restore-daily-compilations-vk to verified origin.

Created ready MR9 https://gitlab.youdo.sg/data/daily-compilations/-/merge_requests/9 targeting master, title DevOps-898 use vk datacenter and proxy for staging, exact approved Russian body, assignee a.solonenko, squashfalse, remove-source-on-mergetrue. Helper independently verified branch/MR SHA, source/target/title/body/settings. Pipeline141345 was RUNNING at publication verification: https://gitlab.youdo.sg/data/daily-compilations/-/pipelines/141345. No success claim; local tests/lint skipped per request. No merge/tag/deployment performed. Nomad address/token selection remains unchanged and VK readiness is unresolved beyond dc/proxy values. Central backlog now tracks MR decision and deployment separately from completed publication.

## Generator necessity assessment (2026-10-21)

User asked whether data/daily-compilations-generator is needed on test. Cloned missing project into /home/slnnk/git/daily-compilations-generator through the repository helper; inspected current master cc1014f6d4f220218f6e861f580c2f26f2cc9d2f without edits or execution. Generator reads eligible users/tasks from ClickHouse, filters unsubscribed users through daily-compilations API, obtains recommendations, and sends email events through RabbitMQ plus Kafka. Thus API subscription updates do not require the generator; generating/sending actual daily email selections requires it.

Current staging.nomad defines a one-shot batch job daily-compilations-generator-staging in dc data, manual staging CI job uses NOMAD_PROD_ADDR/TOKEN. This is a shared Data test run, not an existing per-stand VK generator. Staging caps email messages at5, rewrites recipient addresses and disables last-compilation timestamp updates. It still references common ClickHouse, daily-compilations dc selectel, RabbitMQ and Kafka; staging is not isolated to VK test5. README documents ClickHouse migrations/ETL freshness requirements for the current implementation. No runtime health audit, generator build, job launch, CI edits or deployment requested/performed. No generator restoration action added to backlog because the user asked for necessity assessment only.

## Staging job3241027 diagnosis (2026-10-21)

User supplied https://gitlab.youdo.sg/data/daily-compilations/-/jobs/3241027. Fresh GET: deploy:staging FAILED/script_failure, protected release0.5.15 at user-merged masterb1901e5da78526c2fc53941fa54cc239e6deaf7a, pipeline141347 FAILED. Exact trace: `nomad job run -var "version=${CI_COMMIT_TAG}" staging.nomad`, then `Error submitting job: Unexpected response code: 403 (Permission denied)`. Build3241024, Nomad lint3241025 and release3241026 SUCCESS; production3241028 SKIPPED. No allocation/application startup was reached by the failed submission.

Current project/pipeline Nomad variable overrides absent. Data group NOMAD_STAGE_ADDR is http://nomad.service.yandex-test.consul:4646; NOMAD_STAGE_TOKEN is protected and differs from reviewed VK token. Tag0.5.15 protectedtrue, so protected status does not explain missing variable availability. The committed staging YAML consumes those stage variables for NOMAD_ADDR/TOKEN. This verifies the deployment still targets the old Nomad endpoint despite dc/proxy=vk-test. Read-only token-self probe at old address returned404; this does not prove the exact token ACL failure independently of the job403. Known VK token GET /v1/job/daily-compilations returns404, confirming job absent there.

Required correction proposal: project-only NOMAD_STAGE_ADDR and NOMAD_STAGE_TOKEN overrides scoped to staging, supplying reviewed VK endpoint and existing .env VK_TEST_NOMAD_TOKEN without changing shared Data-group consumers. External variable creation/update needs explicit approval; subsequent existing-job retry needs separate approval. No source change, external CI variable update, retry or deployment performed. Diagnostic scripts in /home/slnnk/ai-data/data-services-diagnosis/ read metadata/trace/variables in memory and print only sanitized relevant evidence.

## Authorized staging credential correction, moved to Data group (2026-10-21)

User explicitly requested correcting the variables after the exact project-scoped correction proposal. Applied two project204 staging overrides NOMAD_STAGE_ADDR/TOKEN (protected, token masked), with independent GET verification. While that command was running, user clarified: if inherited from Data, change them in the group. The project mutation completed before the clarification could be acted on; reported this timing to the user before proceeding.

Per clarified instruction, updated only existing Data group wildcard-scope NOMAD_STAGE_ADDR and NOMAD_STAGE_TOKEN values to http://nomad.service.vk-test.consul:4646 and existing current/.env VK_TEST_NOMAD_TOKEN respectively. Preserved existing scope/protected/masked/raw/type metadata. This affects all projects inheriting these group keys; no global preference inferred. After independent group readback, removed only the two exact task-created project204 staging overrides and verified their absence, restoring group inheritance. No NOMAD_PROD_*, SPB2 or Yandex-specific variable keys changed. Secret stayed in memory/API only; receipts contain key/scope/action metadata, no secret values.

Executed local helper configure_group_staging_vars.py --apply; sanitized receipt group-staging-vars-receipt.json in /home/slnnk/ai-data/data-services-diagnosis/. All2group PUT and2project cleanup DELETE actions succeeded, group exact values and project override removal independently GET-verified. No CI job retry, new pipeline, release, deployment or source change. Failed job3241027 remains the last observed runtime attempt; a retry requires separate user instruction. Earlier statements that staging keys still target Yandex are historical and superseded by this verified group update. Live job environment after retry has not yet been observed.

## User retry succeeded and VK runtime accepted (2026-10-21)

User reported successful deployment using original job3241027 URL. Fresh pipeline141347 jobs GET identifies successful retry deploy:staging3241056 https://gitlab.youdo.sg/data/daily-compilations/-/jobs/3241056; old3241027 failure remains historical. Release/build/lint jobs successful. The existing automatic downstream deploy:production3241028 was RUNNING at observation, not manually played by the agent. Production effect/outcome not inspected beyond job status and not claimed successful.

Read-only acceptance: Nomad daily-compilations running in vk-test, API image0.5.15, PostgreSQL10-alpine. Desired-run allocations APIa2f4b911-167f-1ea2-ccda-e34f0bd91716 on agent06 and PG9ab4fb04-9a20-a8b7-b966-f183190fe611 on agent01 both running, taskrestarts0. Both Consul service/check sets passing. Configured endpoint http://v1.daily-compilations.vk-test.youdo.local/health and GET /users?max_results=1 each HTTP200. No user payloads read into output or retained. No subscription write performed; initial monolith UI subscription operation not independently retried. This confirms restored API availability and read path, not full email generation or long-term stability.

Evidence: /home/slnnk/ai-data/data-services-diagnosis/acceptance.json. No infrastructure changes, job retries, deployment requests or database mutations by agent during acceptance. Central test restoration TODO is completed; automatic production job result is a separate pending observation.

## Production monitoring: healthy canary requires promotion (2026-10-21)

User explicitly requested monitoring production job3241028 to a correct outcome. Read-only GET confirms job RUNNING and trace waiting for Nomad deployment edf404b3-9b2f-084a-73fb-829403c8a68e, version45. Actual production specification targets Selectel, count2, canary1, auto_reverttrue and no auto_promote. Trace and live deployment agree: manual promotion required, Promotedfalse, HealthyAllocs1/UnhealthyAllocs0. Canaryecb85fff-f9ba-9260-c915-d619a79f0b74 runs API0.5.15 with0restarts and Healthytrue. Two prior version44 allocations remain running, with14and11historical restarts; all three current Consul registrations/checks passing. Two old completed2019allocations also appear with DesiredStatusrun; excluded from current healthy-service count. Shared production endpoint http://v1.daily-compilations.proxy.youdo.local/health returns200. This request reaches the load-balanced endpoint; it does not isolate the canary, whose own Nomad/Consul health is passing.

Production uses its existing external database configuration, not the new VK test PostgreSQL group. No direct SQL write or production DB mutation attempted. Snapshot /home/slnnk/ai-data/data-services-diagnosis/production-acceptance.json contains sanitized runtime evidence.

Concrete next action proposed for explicit approval: promote only production deployment edf404b3-9b2f-084a-73fb-829403c8a68e for daily-compilations at http://nomad.service.selectel.consul:4646, using existing .env SELECTEL_PROD_NOMAD_TOKEN in memory. Nomad command is deployment promote for this exact ID. This continues the already-started production rollout from canary to desired2replicas. Monitoring permission is not promotion permission under the external-change rule. No promotion, retries, cancellation or infrastructure changes performed. After approval/revalidation, monitor terminal deployment/GitLab outcome and current allocations/checks.

## Production completed after user promotion (2026-10-21)

User reported executing promote. Fresh independent GET confirms production job3241028 SUCCESS and full pipeline141347 SUCCESS, completed14:33:09MSK. Trace records promotion11:32:42UTC and deployment successful11:33:08UTC. No agent promotion or other external mutation occurred.

Nomad deployment edf404b3-9b2f-084a-73fb-829403c8a68e successful, Promotedtrue, desired2/placed2/healthy2/unhealthy0. Two current running version45/API0.5.15 allocations ecb85fff-f9ba-9260-c915-d619a79f0b74 (msk3-nomad03) and cca0e0ce-8a67-4ea2-2e44-2527a15647d3 (msk3-nomad02) have0restarts and Healthytrue. Old version44 services removed from current Consul registrations. Both current Consul service/check sets passing; shared production /health HTTP200. Historical completed2019allocations remain in Nomad API history and are not current service instances. Evidence updated in production-acceptance.json; sanitized GitLab trace inspected in memory.

Production monitoring objective complete. Immediate rollout/process/service-health verification passed; no subscription business-operation write, independent SQL mutation/test or extended stability claim. Central production monitoring entry closed; unrelated APNs credential review remains open and is not part of the restored service rollout.
