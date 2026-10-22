---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [recommendations, mock, vk, ci]
---
# Recommendations mock minimal VK CI preparation

## Summary

Recovery accepted2026-10-21: user merged MR14 as74f4115e and created/deployed release0.0.16. Master pipeline141384/build3242472 and release141385/build3242473/deploy3242474 allSUCCESS. Registry tag0.0.16 GET verified digest85d80ceabcdd234e56cbbda958a6d477048d3d5852be0b0af111e0d28dba820c. VK Nomad job running, task metadataVERSION0.0.16, one healthy allocation6265440f onagent01 with0restarts; Consulpassing, configuredrootHTTP200. No remote fixture writes or autotest rerun by agent. CI retains one manual tag-only VKdeploy and permanent no-attestation setting; missing unused Flask-Extension removed. Both MRs/source changes and localbuild/save-read smoke evidence are recorded below. Earlier emptyregistry/failure/pendingstatements are historical and superseded. User handled merge/tag/deploy; agent performed read-only acceptance.

## Task
User requested working on sysadmins/youdo_recommendations_mock while subcategory-predictor CI ran, then explicitly required only one VK deploy job. Existing Jenkins2020 failures identify6finaltests/12requests failing POST/save404 on recommendations-mock.vk-test.youdo.local.

## Context
Existing clean checkout /home/slnnk/git/youdo_recommendations_mock on oldmasterdec3f825; read-only fetch obtained current master018c304f696dd4e78bbb29be087bf50e9012d977. Current project205 has no openMRs; release0.0.14 points to currentmaster. Old release pipeline110488/tagbuild2030217 and deploy-yandex-test2030219 succeeded historically. Current registry repo53 has no tags, so an image rebuild is needed. Shared runners already enabled.

## Findings
Current master already parameterizes staging.nomad dc/proxy/version and removed legacy RexRay mount present in old localbranch. No Nomad/app/Dockerfile edit proposed based on obsolete source. App listens on80 matching Nomadportmap; Docker EXPOSE5000 is advisory. Flask app stores test fixtures in relative /app/json_files. Three fixture directories have tracked sample JSONs. Existing behavior is container-local test state; no persistent volume redesign proposed. Requirements currentmaster includes itsdangerous2.0.1 compatibility fix; do not overwrite it using oldcheckout.

Unlike Data projects, this project inherits sysadmins CI variables. NOMAD_TOKEN_VK_TEST already exists and exactly matches reviewed .env VK_TEST_NOMAD_TOKEN. Generic NOMAD_ADDR/TOKEN and old stage/Yandex keys also exist, so explicit CLI-address/token selection is required to avoid inherited target overrides. No group/project variable changes necessary.

User's scope refinement: replace two deployment jobs (deploy-spb2/deploy-yandex-test) with one manual tag-only deploy-vk-test. Keep build-for-master/build-for-tag jobs and CI-supplied version unchanged. New job supplies NOMAD_VAR_dc/proxy=vk-test and calls nomad job run with explicit http://nomad.service.vk-test.consul:4646 plus existing NOMAD_TOKEN_VK_TEST. HCL generates recommendations-mock.vk-test.youdo.local from suppliedproxy. No hardcoded image tag or repository dc/proxy defaults added.

## Proposal and status
Prepared full candidate CI and patch outside repo in /home/slnnk/ai-data/data-services-diagnosis/recommendations-mock-vk-proposal/. Source repo remains clean/unmodified. Proposed first approval: branch DevOps-898-restore-recommendations-mock-vk from origin/master018c304f. User has not yet been asked to confirm this concrete branch/base while parent handles new subcategory build failure. Source push on feature branches does not run current build jobs (master/tags only); mastermerge builds masterimage, release tag buildsversionimage and exposes manualVKdeploy. No production job exists in this project. Merge/tag/deploy remain separate approvals.

No source edits, branch mutations, commit/push/MR/settings changes, image build or deployment performed for this project. Central dependency proposal tracks this newly requested scope, other missing dependencies remain proposals only.

## Portable lesson
none

## User confirmed continuation; local build and API smoke passed (2026-10-21)

After concrete branch/base was stated, user directed `По youdo_recommendations_mock продолжай работу`. Created requested branch DevOps-898-restore-recommendations-mock-vk from018c304f in existing clean checkout. Applied candidate .gitlab-ci.yml, retaining exactly one manualtag-only deploy-vk-test and both original master/tag build jobs. No staging.nomad or app edit.

Following local-build-before-publication instruction, built isolated currentsource context. First build failed because Flask-Extension==1.0 is unavailable from PyPI. Source imports only Flask,re,os and never uses this package. Removed only that unavailable unused requirement in candidate context, retaining all other pins including itsdangerous2.0.1. Full second Docker build exit0, image local/youdo-recommendations-mock:vk. Offline container Flask test_client: GET/root200; POST/save302 followed by saved fixtureGET200 for each of similar_tasks,task_executors_2,user_recommendations_2. Synthetic fixture data existed only in discarded container, no external API writes. Evidence recommendations-mock-local/build-without-flask-extension.log, result-without-flask-extension.json and smoke-result.json.

Transferred only that validated requirements-line removal to existing branch, preserving original no-final-newline formatting. Exact tracked-file bytes match builtcontext; diffcheckPASS. CI YAML parse confirms exactly one manual tag-only deploy. Nomad local validate passed with existing deprecated task-network-resource warning; driver validation skipped because local Nomad endpoint unavailable. No unrelated warning fixes.

Prepared publication proposal/body/snapshot under /home/slnnk/ai-data/gitlab-workflow/recommendations-mock-vk/youdo_recommendations_mock/. Proposed commit deploy recommendations mock to vk; proposed ready MR DevOps-898 deploy recommendations mock to vk, source approvedbranch ->master, Russian one-paragraph body documents singleVKdeploy and unavailable unused dependency removal then DevOps-898link. Current actualdiff2files,4insertions/20deletions. Source push has no matching current jobs (onlymaster/tags); no new automatic build/deploy claim for featurebranch. No stage/commit/push/MR/merge/tag/deploy or settings updates yet. Awaiting second supervised publication confirmation; prior proposal-only status superseded by these local edits and verified build.

## Approved publication completed (2026-10-21)

User replied `Да` to concrete combined publication proposal for recommendations mock and subcategory. Both bound snapshots matched immediately before task-only staging. Mock complete staged diff inspected: .gitlab-ci.yml oneVKmanualjob and requirements.txt removal only,4insertions/20deletions. Created ca014d0975b121e7f390a99b78365fe7fdc7a41b, deploy recommendations mock to vk; inspected actual commit patch and worktreeclean, pushed approved source branch.

Created ready MR13 https://gitlab.youdo.sg/sysadmins/youdo_recommendations_mock/-/merge_requests/13, title DevOps-898 deploy recommendations mock to vk, targetmaster, exact approved Russianbody/DevOps898link, assigneea.solonenko, squashfalse, source-remove-on-mergetrue. Helper independently verified SHA/source/target/title/body/settings. Pipelines list empty, matching master/tag-only rules; do not claim branch CI passed. Local fullbuild and smoke evidence remains valid, with source file equality established before committing.

No merge, tag, masterbuild, remote image push or VK deployment executed. Need user review and separate merge/release/deploy authorization. Existing groupVKtoken and sharedrunners unchanged. Central dependency TODO updated to publishedMRstatus rather than waiting for publication.

## Latest two pipelines: successful build, failed manifest push (2026-10-21)

User requested inspecting the two latest pipelines. Fresh GET returns141379 ref0.0.15 and141378 refmaster, both at ec15cec0b5bb8093ee755c4a1dfe6445653015e6, bothFAILED. Independent MR13 GET confirms user merge at17:25:46MSK to thatSHA. No agent merge/tag creation.

Masterbuild3242434 and tagbuild3242435 both complete image build successfully, including all Python dependencies. Both fail only dockerpush with registry `blob unknown to registry`. Master missing digestdc0068f625f156731949a101827581b5a116ed8c2449bc4cba7ce0282b499d03; release07319993246a70abf59d1e7ee9a2941c34186ea391ecfa44337ddf4b2baf1e8e. These are the exported child image-manifest digests, not missing filesystem-layer digests. Both logs export an attestation manifest and enclosing manifestlist, then upload layers before registry rejection. deploy-vk-test3242436SKIPPED, no deployment attempted in that pipeline. Registry tags master and0.0.15 independently GET404 after failure.

Pattern strongly matches previously verified Buildx/registry attestation compatibility incidents: HoustonV2Mock141068->141070 and dynamic-inventory140829->140830 succeeded with pipeline-only BUILDX_NO_DEFAULT_ATTESTATIONS=1. Working explanation is registry handling of child manifests/indexes; exact registry internal defect not independently proven here. Official Docker documentation confirms this environment variable disables default provenance attestations: https://docs.docker.com/build/building/variables/#buildx_no_default_attestations .

Proposed bounded recovery: create a new pipeline for unchanged existing0.0.15/SHAec15cec0 with sole variable BUILDX_NO_DEFAULT_ATTESTATIONS=1. This rebuilds/pushes release image and exposes existing manual VK deploy; it does not create/change a tag or auto-deploy. Requires explicit external-action approval. Prepared payload /home/slnnk/ai-data/data-services-diagnosis/mock-no-attest-pipeline-proposal.json. A persistent CI setting is a separate optional decision, not applied. No local source edits, new pipelines, retries, registry writes or deployment performed during diagnosis.

Evidence /home/slnnk/ai-data/data-services-diagnosis/mock-latest-pipelines.json holds sanitized metadata/failed-trace tails. Earlier full local imagebuild/smokePASS remains valid for build/runtime package compatibility; local classic Docker27 image storage does not reproduce the CIcontainerd/default-attestation registry-push path. Actual compatibility recovery requires observed remote publication after separately approved pipeline creation.

## Persistent no-attestation CI correction requested (2026-10-21)

User explicitly requested adding the setting to the repository for future builds. Read-only fetch confirms origin/masterec15cec0b5bb8093ee755c4a1dfe6445653015e6 (MR13merge) and existing0.0.15tag. Current local oldsourcebranch remainscleanatca014d0; no repository task edits for this follow-up. Proposed new branch DevOps-898-disable-mock-attestations from origin/masterec15cec0, subject to first supervised approval; oldMR13ismerged, so do not silently update it or switch branches.

Prepared exact minimal change outside repo: global .gitlab-ci.yml variables entry BUILDX_NO_DEFAULT_ATTESTATIONS string1, inherited by both master/tag build jobs. Single manualVKdeploy unchanged; no image/runtime/source dependency changes. Proposal file/patch under /home/slnnk/ai-data/data-services-diagnosis/recommendations-mock-attestations/. Full local Docker build with this exact candidate CI and environmentvariable1 exit0, image local/youdo-recommendations-mock:vk-no-attest. No registrypush attempted: local Docker27/classicstore differs from CI modern containerd/attestation export, so actual registry compatibility must be verified by CI publication later. Prior app/save-read smoke remains applicable because app/requirements unchanged.

Candidate does not add pipeline-only overrides, edit CI settings, create pipelines, retry jobs or change tags. Source branch is not yet created; persistent fix not committed/pushed. This supersedes the earlier pipeline-only recommendation as the user's chosen scope; external pipeline-only recovery remains unexecuted.

## Persistent CI variable applied after branch approval (2026-10-21)

User replied `Да` to concrete two-repository branch/base/scope proposal. Created DevOps-898-disable-mock-attestations from exactec15cec0, leaving historical merged sourcebranch preserved. Applied exactly3line additions at .gitlab-ci.yml top: global variables/BUILDX_NO_DEFAULT_ATTESTATIONS string1. Matches candidate used in prior successful local imagebuild byte-for-byte. YAML parsed, gitdiffcheckPASS; deployment job and source remain unchanged. No registrypush tested locally.

Publication proposal/body/bound snapshot /home/slnnk/ai-data/gitlab-workflow/recommendations-mock-attestations/youdo_recommendations_mock/. Proposed commit disable default build attestations; ready MR DevOps-898 disable default build attestations, approvedsource->master. Russianbody explains master/tag build compatibility setting followed by DevOps898link. Featurebranch has no currentmatchingCIjobs; later mastermerge publishes masterimage, tags publish releaseimages, VKdeploymanual. No merge/tag/settings change included.

Waiting for second concrete publication approval. No staging/commit/push/MR for this follow-up; earlierMR13 remainsmerged. Exact registry compatibility remains for subsequent CI verification, not proven by localbuild alone.

## Persistent no-attestation setting published as MR14 (2026-10-21)

User replied `Да` to concrete combined publication proposal. Bound snapshot matched before staging. Complete staged diff only globalCIvar3line additions; committed6539c09efb93e310d882d4e09e1d02ac96d7031b, disable default build attestations, actualcommitpatch matched and worktreeclean. Pushed DevOps-898-disable-mock-attestations, created readyMR14 https://gitlab.youdo.sg/sysadmins/youdo_recommendations_mock/-/merge_requests/14 to master, exact agreedtitle/body/assignee/settings. Helper independently verifies branch/MR SHA/source/target/title/body, squashfalse/source-remove-on-mergetrue. No branchpipeline under currentmaster/tagonlyrules.

Global var inherits into both existingbuildjobs; manualVKdeploy unchanged. Full localcandidatebuildPASS remains current evidence, registry compatibility still requires actual post-merge CI publication. Existing0.0.15 tag/pipelines keep oldconfiguration; no tag rewrite, retry, newrelease or deployment performed. MR14merge requires separate approval. This replaces waiting-for-publication status; earlierMR13merged is historical precursor.

## User deployment0.0.16 accepted (2026-10-21)

User reported mock deployed and requested pipeline checks. FreshGET confirms MR14merged74f4115e6e8703775deac45b6f9111dcc417d3de. Master141384/build3242472 SUCCESS; tag0.0.16 pipeline141385 build3242473 and deploy-vk-test3242474 SUCCESS. Registry tag0.0.16 digestGET verified sha256:85d80ceabcdd234e56cbbda958a6d477048d3d5852be0b0af111e0d28dba820c. This establishes successful remote publication after permanent compatibility setting, resolving the previous blobunknown blocker.

Read-only runtime acceptance: recommendations-mock in vk-test RUNNING, taskMetaVERSION0.0.16 (image uses NOMAD_META_VERSION template), healthy runningallocation6265440f-c594-1663-920e-7c46f34ce4a8,0restarts, agent01. Consulchecks passing; http://recommendations-mock.vk-test.youdo.local/ returns200. No remote POST/save or fixture modification performed, so recovery acceptance covers deployment/service/root availability; local save/read smoke was previously verified. No claim all6Jenkinsfailures have been rerun/passed. Evidence current-data-pipelines.json/current-data-release-readback.json under ai-data. Central mock restoration item closed, other Data dependencies remain separate proposals/work.
