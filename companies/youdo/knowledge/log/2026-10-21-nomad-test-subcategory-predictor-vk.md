---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [data, subcategory-predictor, vk, ci]
---
# Subcategory predictor minimal VK CI deployment preparation

## Summary
Release1.0.8 pipeline141391 and productionjob3242503 SUCCESS. User manually promoted production. Fresh GET confirms deployment0a973c76 successful/Promotedtrue/HealthyAllocs2of2/Unhealthy0: active allocations69ee0ee7 andee21104b both1.0.8/running/healthy/restart0. Both Consul registrations passing, shared /health200. VK also previously accepted healthy. No application/API/test sourcechanges from0.7.4; six build/CI/config/docs files differ, including jamspellpatch and artifactURL migration. Old internalS3 unregistered in queried production/VK Consul; current SelectelS3 artifacts successfully loaded. No agent production mutation. Remaining unrelated service restoration proposals are in centralTODO.

## Task
User requested minimal changes to launch data/subcategory-predictor in VK Cloud through CI. Subsequently requested parallel diagnosis of Jenkins youdo_web_testing_two2020; delegated that independent read-only log task explicitly, while retaining this objective.

## Context
Project179, existing /home/slnnk/git/subcategory-predictor checkout clean on historical nomad_tags/6491110. Read-only fetch obtained actual master62d5ded9ef7476c87608f7b1d885c5b075977201. Local historical source differed in Dockerfile, README and Nomad specs; proposed edits are based on fetched master, not old branch. No project AGENTS/CLAUDE files found.

## Actions
Fresh GitLab project/branches/tags/MR/pipelines/registry/CI-variable metadata and project runners inspected; no external writes. Compared current master CI/staging/source and artifact availability.

## Findings
- Current master62d5ded9: no openMRs. Registry repository46 currently has no image tags; a fresh build is required.
- Last master pipeline116820 failed build2257825; historical trace response is empty, so actual old failure cause is unknown and not used to justify speculative source rewrites.
- Project shared_runners_enabled=false and project runners GET returns emptylist. Enabling shared runners is a required external project-setting proposal before new CI can run, subject to explicit approval.
- No project Nomad variable overrides. Existing Data-group NOMAD_STAGE_ADDR and NOMAD_STAGE_TOKEN exactly match reviewed VK endpoint and .env VK_TEST_NOMAD_TOKEN. No need to add duplicate secrets or new aliases.
- Current master staging.nomad still targets yandex-test DC and v1.subcategory-predictor.yandex-test.youdo.local. CI contract/load tests target the older staging.subcategory-predictor.proxy-test.youdo.local route, which current HCL does not declare.
- Current master model sources already use Selectel S3; HEAD both200: models.tar.gz3280219475bytes and ru_small.bin81159179bytes. No download performed. URLs are in reviewed HCL; no artifact-source edit proposed.
- Existing staged deployment retains Levant, CI-supplied version, registry tag, model paths, resources5000MiB and4000MBephemeraldisk, update/canary settings. Runtime model extraction/capacity not verified before deployment. Eventum Kafka REST remains an existing dependency; do not infer prediction-event delivery from service startup.
- CI branch builds/pushes branch+latest images and runs tests/lints. Tag pipelines release, automatically stage, run contract/load tests and automatically production-deploy afterward. Publication/release effects must be explicitly presented before triggering writes; no production deployment requested for this task.

## Concrete repository proposal
Use existing checkout, create DevOps-898-restore-subcategory-predictor-vk from origin/master62d5ded9, pending first supervised approval. Exactly4line changes: staging.nomad datacenters yandex-test -> vk-test and matching Traefik route; .gitlab-ci.yml contract/load endpoint -> http://v1.subcategory-predictor.vk-test.youdo.local. No runtime pin/default image version, application code, model or dependency upgrade proposed. Further build corrections require observed failures and the smallest relevant fix.

Prepared patch outside repository: /home/slnnk/ai-data/data-services-diagnosis/subcategory-vk-proposal/proposal.patch. Proposed contents are preview artifacts, not edited checkout files. Preflight metadata: subcategory-preflight.json.

## Status and risks
Read-only preparation complete. Waiting for explicit branch/base approval before repository changes, and separate explicit approval to enable project shared runners. No branch mutation, repo edits, CI launch, commit/push/MR, project setting change or deployment performed. Parent five-service dependency-audit TODO tracks the overall restoration proposal; this task note records the scoped subcategory work without treating remaining targets as authorized. User previously requested no local checks in the daily-compilations task; any scope for this task remains subject to subsequent steering.

## Portable lesson
none

## User requested MR after diff review (2026-10-21)

After exact four-line diff and explicit branch/base proposal were shown, user requested `Сделай мр`. Applied this as confirmation of the displayed branch/scope: created DevOps-898-restore-subcategory-predictor-vk from exact62d5ded9 in existing clean checkout. Changed only staging.nomad DC/route and .gitlab-ci.yml contract/load URLs, exactly4insertions/4deletions. No image pin, version default, artifact/model/resource or production changes. git diff --check passed; CI YAML parsed and staging credential inheritance/tag triggers retained. No local image build or application test run; no newly written tests.

Publication bundle and bound snapshot saved under /home/slnnk/ai-data/gitlab-workflow/subcategory-predictor-vk/subcategory-predictor/. Proposed commit use vk target for subcategory predictor staging; proposed Draft MR title Draft: DevOps-898 use vk target for subcategory predictor staging, source approved branch -> master. Russian description states VK datacenter/route and contract/load target change followed by DevOps-898 link. Draft reflects unresolved runner prerequisite/pipeline verification. Actual CI source shows branch push builds/publishes branch+latest and tests/lints, no deployment; tag pipelines remain auto staging+contract/load+production. Publication proposal includes source image publication effect, no shared-runner setting update or release/deployment.

Second supervised approval still required for the concrete publication proposal and stated effects. Nothing staged/committed/pushed, no MR yet, no CI/settings/deployment actions. Earlier preparation-only status is superseded by these local task edits.

## Publication and shared runners completed (2026-10-21)

User replied `Да` to concrete second-stage proposal. Pre-stage bound snapshot matched. Staged exactly the approved2files, inspected complete staged diff, committed45556488c0cec9cb88ad12b052ebdd22ffbec2c0 with use vk target for subcategory predictor staging; post-commit patch matched4reviewedline changes and worktree clean.

While publication was active, user explicitly requested using shared runners. Enabled only project179 shared_runners_enabled=true with one project PUT; independent GET confirms true. No runner registration/tag/settings or other project fields changed. Sanitized receipt /home/slnnk/ai-data/data-services-diagnosis/subcategory-shared-runners-receipt.json; explicit request authorizes this setting change separately from publication.

Pushed approved source branch to verified origin and created Draft MR22 https://gitlab.youdo.sg/data/subcategory-predictor/-/merge_requests/22, exact approved title/body/source->master and SHA45556488, assignee a.solonenko, squashfalse, source-removal-on-mergetrue. Helper independent readback verifies branch/MR/settings and pipeline presence. Pipeline141366 https://gitlab.youdo.sg/data/subcategory-predictor/-/pipelines/141366 initially pending; subsequent jobs GET confirms build3242180 RUNNING on shared runner106 (instance_type), test3242181 and lint3242182/3242183 created. Pipeline list status stillpending at that snapshot; runner acquisition is demonstrated by running build rather than pipeline label alone.

No merge, new release tag, staging/production deployment or CI retry performed. Draft remains until observed CI outcome and user-approved readiness transition; full build/test success is not established. Local diff/YAML checks passed earlier; KB lint0errors/0warnings. Updated central dependency proposal now records MR22/build monitoring rather than waiting for publication/runners.

## Build3242180 failed: archived toolchain proposal (2026-10-21)

User supplied failed build URL. Independent GET: build3242180/pipeline141366 FAILED/script_failure on exact45556488. Trace reached Dockerfile2/9 after successfully pulling python:3.7; apt uses bookworm plus newly added Debianunstable. Actual failure: `Unable to locate package swig3.0` and `Unable to locate package gcc-8`, exit100. No Python dependency install or service build completed. Shared runner106 worked; this is a Dockerfile package-source failure, not VK Nomad connectivity. Initial absent latest cache was not the fatal error.

Prepared minimal Dockerfile proposal outside repo: FROMpython:3.7-buster, replace unstable source with archive.debian.org/debian buster main in /etc/apt/sources.list, and apt update option Acquire::Check-Valid-Until=false for archived metadata. Python major/minor and existing Python requirements/toolchain package names retained. Official Docker manifest GET verifies python3.7-buster exists/linuxamd64, digest2539f956bcccbac5e4a48ebdafbbbfbd26b4ab56e65b96076ae9cd1188b119b3. Debian archived Buster Release HEAD200 and actual amd64 Packages.gz contains gcc-8 version8.3.0-6 and swig3.0 version3.0.12-2. These read-only probes establish package/base availability, not full image build success.

Proposal files subcategory-vk-proposal/Dockerfile.proposed and Dockerfile.patch; probe evidence subcategory-base-probe.json under /home/slnnk/ai-data/data-services-diagnosis/. Repository remains unchanged/clean at45556488; no new commit, push, MR change or retry. Extending approved four-line scope to Dockerfile in existing branch DevOps-898-restore-subcategory-predictor-vk and MR22 requires renewed first-stage scope approval. Proposed base for continuation is current45556488, existing targetmaster retained. Actual builder correction/republication not authorized by a job-link-only diagnostic request.

## Reviewed Dockerfile correction added to MR22 (2026-10-21)

User replied `Сделай` to the exact three-line Dockerfile diff and the explicit question to add it to the existing branch/MR22. This confirms the scoped extension and requested MR update; existing publication source/target/title/draft and branch CI effects retained. Applied only those3lines in Dockerfile. git diff --check passed. Prepared separate buster-fix publication bundle/snapshot, verified unchanged snapshot immediately before staging, inspected complete staged diff and committed082451fb6583b044c65e5276f99e0deddd0bc4d5, subject use archived buster toolchain for image build. Resulting commit contains only Dockerfile3insertions/3deletions, worktree clean.

Pushed same approved branch, updated existing MR22 description with Buster/archive correction while preserving one-paragraph Russian format and task link. Helper independent readback verified exact082451fb, source/target/title/body, assignee and draft state. No new MR, title/readiness change, merge/tag/deploy or CI retry. New pipeline141370 https://gitlab.youdo.sg/data/subcategory-predictor/-/pipelines/141370 RUNNING at verification. Build success is not yet established; archived base/package availability and local diff check are the current validation evidence.

External operations performed under the user's specific existing-MR correction request and prior publication authorization: source push and MR description update only. The previous failed build3242180 remains historical. Further source changes require actual new failures; no speculative dependency upgrades included.

## Jamspell failure and required local-build-before-publication workflow (2026-10-21)

User supplied build3242362 and then explicitly directed `Прежде чем отправлять изменения проверь сборку локально`. Applied to this Data-service recovery, including parallel recommendations mock: image must build locally before further source publication; do not treat CI as the first feedback loop for these minimal fixes. This task-scoped direction does not create global permission or authorize infrastructure changes.

GET confirms build3242362/pipeline141370 FAILED at082451fb. Buster apt/toolchain installation passed. jamspell0.0.11 compiled but custom setup.py CustomInstall calls do_egg_install; wheel metadata generation fails and fallback installation reports missing .egg-info. Upstream PyPI source for0.0.12 changes that call to install.run(self), retaining SWIG3 requirement. Primary upstream issue https://github.com/bakwc/JamSpell/issues/103 independently shows the same0.0.11 metadata failure; blindly pinning pip was not used.

Local isolated context /home/slnnk/ai-data/data-services-diagnosis/subcategory-local-jamspell12/context changed only requirements.txt jamspell0.0.11->0.0.12. Full Docker build exit0, image local/subcategory-predictor:vk-jamspell-0.0.12; build.log/result.json retained. Offline docker run --network none imports jamspell,fastText,subcategory_predictor.app and constructs TSpellCorrector; exit0, distributionversion0.0.12 verified. This does not load full3GBmodels or prove prediction-event delivery. Applied the validated one-line requirements change in existing requested branch, and byte-for-byte comparison confirms every tracked file equals the locally built context (excluding .git metadata); diffcheckPASS. No repository tests added.

Prepared jamspell-fix proposal/snapshot under /home/slnnk/ai-data/gitlab-workflow/subcategory-predictor-vk/subcategory-predictor/. Proposed commit update jamspell to fix package installation, same DraftMR22 title/source/target retained; Russian body adds corrected package installer. Awaiting concrete second-stage publication approval. No new commit/push/retry/deploy after082451fb.

## Locally validated jamspell fix published (2026-10-21)

User confirmed the combined concrete publication proposal. Bound snapshot matched before task-only staging; complete staged diff only requirements.txt jamspell0.0.11->0.0.12. Created commit6e74f9e5e785650976dd42e7435c42b821149742, update jamspell to fix package installation; post-commit patch matched and worktreeclean. Pushed same branch and updated existing DraftMR22 Russiandescription, retaining approved title/source/target/draft/assignee/settings. Helper independent GET verifies exact6e74f9e5 and MR metadata.

New pipeline141377 https://gitlab.youdo.sg/data/subcategory-predictor/-/pipelines/141377 RUNNING at publication. Full local imagebuild/nativeimports passed before push; remote CI success not yet established. No merge/tag/deployment or manual retry. Earlier3242362 jamspell failure is historical. Concurrent recommendations mock published as readyMR13; its master/tag-only rules produce no branch pipeline.

## API Blueprint lint3242433: inaccessible Quay image (2026-10-21)

User supplied https://gitlab.youdo.sg/data/subcategory-predictor/-/jobs/3242433. FreshGET: lint:apibFAILED/exit125, pipeline141377FAILED at6e74f9e5. Build3242430SUCCESS, test3242431SUCCESS, lint:nomad3242432SUCCESS. Failed command docker run quay.io/bukalapak/snowboard lint API.apib never executes linter: pulling latest image returns unauthorized/access-not-authorized. This is tool-image delivery failure, not an API schema or application build error.

Official upstream https://github.com/bukalapak/snowboard is archived but offers release snowboard@4.1.19 with Linuxx64 archive. Downloaded exact official asset https://github.com/bukalapak/snowboard/releases/download/snowboard%404.1.19/snowboard-v4.1.19-linux-x64.tar.gz into /home/slnnk/ai-data/data-services-diagnosis/snowboard4.1.19/,39001059bytes. Archive includes its own Node12runtime and modules; no npm dependency resolution/upgrade needed. Prepared minimal lint job candidate: image=$IMAGE (alreadybuiltserviceimage), download/untar fixedrelease under /tmp, execute /tmp/snowboard/bin/snowboard lint API.apib. Existing PythonBuster image includes curl/bash/runtime libraries; actual local offline docker run mounted archive+currentAPI.apib read-only, extracted in temporary container filesystem, linter returned OK/exit0. Check is preserved, no skip or allow_failure added. No API.apib change.

Candidate CI/patch saved outside repo at /home/slnnk/ai-data/data-services-diagnosis/subcategory-snowboard-proposal/. Repository clean at6e74f9e5 and existingDraftMR22unchanged. Proposed reuse existing DevOps-898-restore-subcategory-predictor-vk from current6e74f9e5/targetmaster, subject to scope/reuse approval before editing lintjob. No push/retry/newpipeline/deploy. Localimagebuild/nativeimports evidence from earlier stage remains valid, since application source unchanged; new linter behavior was actually tested in that image.

## Approved Snowboard CI replacement applied and verified locally (2026-10-21)

User replied `Да` to reuse/scope proposal. In existing approved branch at6e74f9e5 changed only lint:apib: image$IMAGE, fixed official Snowboard4.1.19 archive download/extraction, run packaged binary lint. Actualdiff oneCIfile3insertions/1deletion, exact reviewedcandidate; YAMLparsed/gitdiffcheckPASS. No app/API.apib/Dockerfile/requirements or other job changes.

Full local build of copied exactcurrenttrackedsource after CI edit exit0, image local/subcategory-predictor:vk-snowboard-ci. Evidence /home/slnnk/ai-data/data-services-diagnosis/subcategory-current-snowboard-ci/result.json and build.log. Ran exact candidate curl/download/extract/Snowboardlint commands inside this image with API.apib read-only, exit0/stdoutOK/stderr empty; lint-result.json retained. No test bypass, schema rewrite or allow_failure. This exceeds earlier offline archive-only check by validating live container download and full command chain.

Publication proposal/body/snapshot /home/slnnk/ai-data/gitlab-workflow/subcategory-predictor-vk/subcategory-predictor/snowboard-fix/. Proposed commit restore api blueprint lint from official release; existing DraftMR22 title/source/target/draft preserved, Russianbody adds restored Blueprint lint. Sourcepush builds/publishes branch+latest and tests/lints; tag-only deploy triggers unchanged. Waiting for second concrete publication confirmation. No stage/commit/push/retry/deploy after6e74f9e5.

## Snowboard CI restoration published (2026-10-21)

User confirmed concrete combined second-stage proposal. Matched snapshot immediately before task-only staging; inspected complete stageddiff, only lint:apib CI3insertions/1deletion. Committed9166cb340c33cd457040fbb1038f63949ec69fdd, restore api blueprint lint from official release; actualcommitpatch matched/worktreeclean. Pushed existing approved sourcebranch and updated existingDraftMR22 description without changing title/source/target/readiness/settings. Helper independent readback verifies exact9166cb3 and MRmetadata.

New pipeline141383 https://gitlab.youdo.sg/data/subcategory-predictor/-/pipelines/141383 RUNNING at publication. Full current-source localimagebuild and exact Snowboard download/extract/lintchainPASS preceded sourcepush. RemoteCIoutcome not yet established. No merge/tag/deployment/jobretry. Concurrent recommendations mock permanentsetting published as readyMR14; featurebranchCI absent by existingrules.

## Green source CI, readiness and user-created release (2026-10-21)

User requested current pipeline checks: pipeline141383 at9166cb3 SUCCESS, build3242468/test3242469/lintnomad3242470/lintapib3242471 allSUCCESS. MR22 remainedDraft/open. User then directed proceeding after readiness/merge/release plan was explained; agent executed only guarded title PUT removing Draft, verifying exactsource9166cb3/headpipelineSUCCESS/draftfalse/mergeable/discussionsresolved. No agent merge/tag operation. Receipt subcategory-mr22-ready-receipt.json.

Before a further agent merge action, user reported having merged and tagged independently, linking141391. FreshGET confirms MR22merged11909b42271cf0e6f6724b5da1ad09d34e4d041c and release1.0.8 atthatSHA, pipeline141391RUNNING. First jobs snapshot: build3242495RUNNING, tests/lints/release/staging/postdeploytests/productioncreated. Current release monitoring is read-only; no automatic agent promotion/retry/deploy permission inferred. Existing tag rules automatically run staging, contract/load and production sequentially, as previously disclosed. Runtime/modeldownload/canary acceptance pending actual rollout.

## Release monitoring final observation (2026-10-21)

Pipeline141391 finishedFAILED on contract3242501, productionSKIPPED. VKNomad deployment5668cfca subsequentlysuccessful with1healthyinstance and0restarts; separate EventumKafkaREST DNS errors remain. Readiness race and existingbroker facts are canonical in [runtime diagnosis](2026-10-21-nomad-test-subcategory-readiness-kafka-rest.md). No contract retry or REST deployment performed; user deployment/tag creation is not standing permission for new mutations.

## Production read-only acceptance snapshot
User requested production deployment check. Pipeline141391 and deploy:service3242503SUCCESS. Fresh productionNomad/Consul/API GETs verify jobversion20/selectel/metaVERSION1.0.8 but rollout not complete: deployment0a973c76-56a1-48e2-dcf1-30a251666837 running, AutoPromotefalse, Promotedfalse, DesiredCanaries1, DesiredTotal2, PlacedAllocs1, HealthyAllocs0, UnhealthyAllocs0. Canary69ee0ee7-c945-19c6-b2fe-fe2b604a3286 running/restart0, healthnull during5minminhealthy; two activeprimaryreplicas09d8cf9f/b4620919 remain0.7.4/running/restart0. Ignore historicalcomplete2019allocations stilllistedDesiredStatusrun. All3Consulservicechecks passing and sharedGET/health200. Boundedstderr7117bytes has no classified DNS/connection/OOM/traceback/errorlevel failures; stdoutempty, no prediction/eventwrite performed. Deployment requires manualpromotion aftercanaryhealth; user has not authorized agentpromotion. Receipts subcategory-production-acceptance.json and subcategory-prod-log-summary.json under ai-data/data-services-diagnosis.

## Promote rejection and release scope comparison
User observed promote RPC rejection0/1healthy. Canary task started18:53:16MSK, running/restart0; at18:57:09 and18:58:11 Healthy null while Consulpassing. At18:59:31 fresh GET confirms Healthytrue with timestamp18:59:30MSK, so healthgate now satisfied; no agentpromotion. Rejection was during the configured5mincontinuoushealthwindow, not observed taskfailure.

User asked why oldproductionversion/howmuchservicechange. Local exactsourcecomparison tag0.7.4(1f9cbff,2021-06-13) to release-source9166cb3 shows9nonmergecommits/6changedfiles: Dockerfile, requirements.txt, .gitlab-ci.yml, staging.nomad, production.nomad, Readme.md. No applicationcode/API.apib/test changes. Dependencyjamspell0.0.11->0.0.12; imagebase/internalbasis1.1->Python3.7Buster with nativebuildtools; CI/lint/stagingrouting/documentation updates. ProductionHCL difference only2artifactURLs from internalS3 toSelectelS3, modeldirectory2018-12-28 unchanged; modelbytes not compared. Old activeallocations0.7.4started2026-09-10; tagcommitdate is not productionlastdeploydate. Git alone does not explain historicalnondeployment decisions.

## Legacy S3 endpoint availability
User asked whether http://s3.service.consul:7480 still works. Workstation DNS lookup failed Name or service not known; HEAD root and both legacy artifactURLs failed atDNS beforeHTTP. Independent authenticated productionSelectel and VKConsul health/service/s3 GETs both returned emptylists. Thus no registered legacy s3service in either queriedDC; no assertion about an unregistered historicalbackend or direct productionnodeDNS probe. Current release uses SelectelS3 and canary downloadedartifacts/started successfully.

## User promotion and final production acceptance
User reported manually promoting production. Independent authenticated GETs confirm deployment0a973c76-56a1-48e2-dcf1-30a251666837 successful, Promotedtrue, DesiredTotal2/PlacedAllocs2/HealthyAllocs2/UnhealthyAllocs0. Active69ee0ee7-c945-19c6-b2fe-fe2b604a3286 andee21104b-a9cf-9871-61c9-a3fae54c6540 are bothjobversion20/metaVERSION1.0.8/running/healthy/restart0; latesthealthtimestamp19:09:30MSK. Earlier0.7.4 activeallocations replaced; historicalcomplete2019allocations ignored. Both currentConsulservicechecks passing and sharedHTTP/health200. Finalreceipt subcategory-production-acceptance.json. No agentpromote/retry/deploy or prediction/eventwrites.
