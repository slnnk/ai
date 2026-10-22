---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [nomad, gitlab, vk-test]
---
# Task quality control mock VK deployment preparation

## Task
Deploy sysadmins/taskqualitycontrolfortest to vk-test with minimal repository changes.

## Context
Existing checkout /home/slnnk/git/taskqualitycontrolfortest is clean on master6f0aac71. Read-only fetch refreshed origin/master to9286ebee40e03c87c1a18f58d0f5e832bc7c7eda. Project233, default master, shared runners enabled, no open MRs. Registry repository74 exists; image availability has not been verified.

## Actions
Read shared instructions, scoped learning rules and GitLab workflow. Daily ai-sync returned success with no output or reminders. Inspected local source and refreshed remote refs. GitLab GET confirmed latest tag staging-0.0.6/pipeline110493 success and master pipeline110492 success; these historical results do not establish current build compatibility.

## Findings
Current master has parameterized staging.nomad: dc, proxy and version. Two manual tag-only deploy jobs target spb2 and yandex-test. Application uses ASP.NET Core2.1 and in-memory fixture settings, without an external database. Registered service taskqualitycontrol uses a TCP check. API POST/evaluation and POST/evaluation/testdata are documented. Dockerfile and source need no targeting changes.

Follow-up GitLab GET verified project has zero variables and inherits sysadmins group variables. NOMAD_TOKEN_VK_TEST exists, is unprotected with environment scope *, and equals the local VK credential (value not recorded). No VK test address variable exists. NOMAD_STAGE_ADDR and NOMAD_YANDEX_TEST_ADDR still point to Yandex; their tokens differ from VK. No variable writes performed.

## Changes
Proposed only .gitlab-ci.yml: rename deploy-yandex-test to deploy-vk-test; set NOMAD_VAR_dc/proxy to vk-test; change its Nomad command to explicit http://nomad.service.vk-test.consul:4646 and existing NOMAD_TOKEN_VK_TEST. Proposed branch DevOps-898-restore-taskqualitycontrolfortest-vk based on origin/master9286ebee. Initial proposal awaited approval; subsequently implemented as recorded below.

## Status and risks
2026-10-21: branch/base/edit approved by user response `Сделай`; local preparation complete; subsequent publication approved and completed as recorded below. Publication, release and actual deployment remain separately controlled. Current .NET2.1 build/registry availability and effective VK credential inheritance need verification during preparation. Existing central restoration item in [TODO](../../../../TODO.md), nomad-test / Consul, covers the remaining deployment. No external state changes.

## Portable lesson
none

## Approved implementation and publication proposal
User response `Сделай` approved the proposed branch/base and four-line CI edit. Created DevOps-898-restore-taskqualitycontrolfortest-vk from origin/master9286ebee and changed only .gitlab-ci.yml (4 insertions,4 deletions). YAML parse, exact VK parameters/token/address/manual-tag conditions and git diff --check pass. No application or Dockerfile changes, builds or runtime checks performed.

Prepared ready MR proposal: source DevOps-898-restore-taskqualitycontrolfortest-vk to master; commit `deploy task quality control mock to vk test`; title `DevOps-898 deploy task quality control mock to vk test`. Body is one Russian paragraph plus DevOps-898 link. Assign a.solonenko, squash off and source deletion on merge follow observed preferences. Proposal/body/snapshot stored under /home/slnnk/ai-data/gitlab-workflow/taskqualitycontrolfortest-vk/taskqualitycontrolfortest/. Snapshot matched.

CI effects: task branch/MR has no matching jobs; merging master builds/pushes master image; tags build/push tag image and expose manual spb2/VK deploys. Publication approval requested for task-only staging/commit/push/MR, excluding merge/tag/deployment. Existing central restoration TODO remains open and covers the pending rollout.

## Publication outcome
User response `Да` approved the displayed task-only commit/push/MR proposal. Snapshot check matched, complete staged diff contained only the reviewed four-line .gitlab-ci.yml patch, cached diff check passed. Committed2bfc03ac1de5ecd87717cc04c59a9c004e5aa62f with the approved message and pushed the approved source branch. Ready [MR10](https://gitlab.youdo.sg/sysadmins/taskqualitycontrolfortest/-/merge_requests/10) created against master, assigned a.solonenko, squash false/source deletion true. Independent verify GET confirmed exact branch/MR SHA, title/body/source/target and settings; pipelines empty as expected. Working tree clean.

Final2026-10-21: publication complete. No merge, tag, build or runtime deployment performed. Existing central restoration TODO remains open for the rollout; earlier approval-pending statements above are historical.

## Release build registry failure
User supplied job3242530. GET confirms build for tag staging-0.0.7/pipeline141397 at efbd84b4fb42c2f07cc93fa2d760c7479b84cf0d FAILED. Read-only fetch confirms origin/master and new release tag point to that merge commit. Restore and dotnet publish succeed; Docker image builds. Export includes child image manifest715dfac57fb2cb525c9776b9862c4d36319015c84eeecfbc4660ce4f40cb3d55, attestation manifest and index. All filesystem layers upload, then docker push fails with `blob unknown to registry` naming that exact child image-manifest digest.

Strong match to recommendations-mock attestation compatibility incident; its permanent BUILDX_NO_DEFAULT_ATTESTATIONS string1 correction subsequently passed master/tag push and deploy. Docker official variable reference confirms disabling default provenance: https://docs.docker.com/build/building/variables/#buildx_no_default_attestations . Registry internal defect remains inferred. Existing .NET build is proven compatible by this CI; no Dockerfile/application fix indicated.

Proposed minimal follow-up: add global variables/BUILDX_NO_DEFAULT_ATTESTATIONS string1 (three lines) to .gitlab-ci.yml on new branch DevOps-898-disable-taskqualitycontrol-attestations from origin/master efbd84b4. First branch/edit approval pending; no new repository edits, retry/pipeline/tag/deploy actions. Existing central restoration TODO remains open for this build blocker and deployment.

## No-attestation and legacy deployment cleanup prepared
User response `Сделай и убери старый spb2 деплой` approved the proposed branch/base/attestation edit and explicitly expanded scope to removal of deploy-spb2. Created DevOps-898-disable-taskqualitycontrol-attestations from origin/master efbd84b4fb42c2f07cc93fa2d760c7479b84cf0d in existing clean checkout. Changed only .gitlab-ci.yml:3added lines for global BUILDX_NO_DEFAULT_ATTESTATIONS string1,15deleted lines for deploy-spb2.

Checks PASS: YAML parse; semantic comparison confirms only those two requested changes; sole deploy-vk-test remains manual/tag-only; build jobs otherwise identical; git diff --check. No full rebuild performed: failed CI already proved .NET/image build passes; actual attestation/registry path requires subsequent CI.

Prepared ready publication: source DevOps-898-disable-taskqualitycontrol-attestations to master; commit `disable build attestations and remove spb2 deploy`; title `DevOps-898 disable build attestations and remove spb2 deploy`; one Russian paragraph explaining both changes plus DevOps-898 link. Proposal/body/bound snapshot in /home/slnnk/ai-data/gitlab-workflow/taskqualitycontrolfortest-attestations/taskqualitycontrolfortest/. Snapshot matched. Feature branch/MR has no matching jobs; master merge builds/pushes master image without default attestations, tags build/push tag image and expose sole manual VK deploy.

Publication approval pending. No staging/commit/push/MR/retry/tag/deploy performed for this follow-up. Existing central restoration TODO remains open and covers registry verification and actual deployment.

## No-attestation and spb2 cleanup publication complete
User response `Да` approved the exact prepared commit/push/ready MR proposal. Bound snapshot matched before staging; entire staged diff contained only3added global variable lines and15deleted deploy-spb2 lines. Cached diff check passed. Committed0794496921f1f51112773b2babf7298a9d7934de with approved message `disable build attestations and remove spb2 deploy`; actual commit scope matched, checkout clean. Pushed source DevOps-898-disable-taskqualitycontrol-attestations and created ready [MR11](https://gitlab.youdo.sg/sysadmins/taskqualitycontrolfortest/-/merge_requests/11) to master. Assigned a.solonenko, squash false, source removal true. Separate verify confirmed exact SHA/source/target/title/body/settings; no branch pipelines.

Final2026-10-21: publication complete; earlier publication-pending text is historical. No merge/tag/retry/pipeline creation/deployment performed. Registry push compatibility still awaits subsequent master/tag CI. Existing central restoration TODO remains open and covers MR merge/release and actual VK rollout.

## Endpoint GET404 follow-up
User reports deployed to VK and asks why /evaluation/testdata/ returns404. Read-only HTTP GET to /evaluation/testdata/, /evaluation/testdata, /evaluation and / all return404 with Server Kestrel and empty body. Traffic reaches an ASP.NET application rather than Traefik default404. Source controller exposes only HttpPost at /evaluation and /evaluation/testdata, no GET action; Startup uses ASP.NET Core2.1 MVC. Thus observed GET404 agrees with method mismatch, trailing slash is not the differentiator for these GET probes. No POST or fixture mutation performed; actual POST success and runtime rollout health not independently verified.
