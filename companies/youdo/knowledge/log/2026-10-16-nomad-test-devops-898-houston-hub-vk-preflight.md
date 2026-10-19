---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [nomad, vk-cloud, houston, gitlab-ci]
---
# DevOps-898 Houston Hub and classifier VK preflight

## Summary

User added Hub to classifier VK launch, initially requested an existing experiment source, then explicitly chose an empty database for the initial launch. No migration is now requested. Read-only investigation is complete; repository branch approval is pending under supervised Git rules. No deployment/build/external write executed.

## Context, actions and findings

- Hub repository /home/slnnk/git/hub is clean on existing nomad_tags branch. Read-only git fetch updated origin/master to b55f844caaf760e96b7280f5cd3cb2b60f9e4b9f. Latest tag2.7.5=13c69c6 has identical runtime/deployment files; master differs only in README. Classifier actual master/tag2.6.9 remains d864cf0.
- Both require only deployments/staging.nomad domain yandex-test.youdo.local to vk-test.youdo.local and datacenter yandex-test to vk-test for the minimal repository adaptation. count1 and instance=common already exist.
- Hub registers houston-hub with v2 tag and embeds MongoDB bitnami/mongodb:4.0.1 using200MB sticky/migrating ephemeral disk, not a durable volume. Verify image availability before rollout. No classifier/model/object-store/upstream dependency or circular dependency.
- Empty Mongo supports startup; no seed/migration code exists. Classifier choices return no experiment assignments without data. User explicitly accepts an empty initial database (latest instruction supersedes initial request for existing records).
- Existing test source absent: Yandex Nomad job GET404 and old test Hub /experiments GET404. Production Hub /experiments?max_results=1 returned200 with total291; record values were not printed or saved. Production access was GET-only; no import/export performed.
- GitLab project163 Hub and164 classifier have no project variables. GitLab registry repositories exist but tags GET returns empty for both; build/recovery required, historical successful pipelines do not establish present image availability.
- Both include data/ci-templates Python UV service template. Branch pipelines build/push branch image and latest without deployment. Tag pipelines release and automatically deploy staging unless STAGING_DISABLED is set; production manual. Do not create a release tag without review of these effects. Existing .deploy staging uses NOMAD_STAGE_ADDR/TOKEN. Project-scoped overrides to VK can preserve the existing deployment flow without shared-template changes; credentials remain external.

## Proposed changes and approval status

Propose branch DevOps-898-deploy-houston-hub-on-vk in hub and DevOps-898-deploy-classifier-on-vk in classifier, both from origin/master, changing only each deployments/staging.nomad. Await explicit branch/local-edit approval. Publication/build and external variable/deployment actions still require their respective reviewed approvals. No branch creation, switching, source edits, builds, publication or runtime actions yet. User request to launch with empty DB defines desired behavior; no individual external command has yet been presented for approval.

## Changed files and risks

KB log/system/repository index/backlog only, plus previously sanitized local template copies. Mongo ephemeral storage limits durability and must be reported without unsolicited storage redesign. Registry image recovery and startup health/functionality remain unverified. Superpowers was not used as requested.

## Proposed shared DC/domain variables (user steering)

User proposed centralizing DC and domain in GitLab group data for both services. Recommended concrete design: group variables NOMAD_VAR_staging_dc=vk-test and NOMAD_VAR_staging_domain=vk-test.youdo.local (scope *, nonsecret/unprotected so branch lint can read them). Declare required string staging_dc/staging_domain inputs in both deployments/staging.nomad and consume them in datacenters and routing domain. Nomad CLI reads NOMAD_VAR_* automatically, so shared CI template changes are unnecessary. Stage-specific input names avoid supplying generic dc/domain values to production job variables. Existing data services only change behavior if their job specs consume these same new names; no broad migration is implied. Address/token routing remains separate through NOMAD_STAGE_ADDR/TOKEN; do not repoint group-wide existing credentials without auditing other consumers. This replaces the earlier proposed hardcoded VK DC/domain edits; same proposed branches, still awaiting approval. No group variables or repository files changed.

## Approved local implementation and verification

User explicitly confirmed both proposed branches and local parameterization. Created DevOps-898-deploy-houston-hub-on-vk from hub origin/master b55f844 and DevOps-898-deploy-classifier-on-vk from classifier origin/master d864cf0 in existing checkouts. Both initial worktrees were clean; previous hub nomad_tags branch was preserved. Only deployments/staging.nomad in each repository changed: two required string inputs staging_dc/staging_domain, used in datacenters and local.traefik_domain (10 insertions/2 deletions each). No defaults silently route to the old cloud.

Verification: git diff --check PASS both. Nomad1.3.5 job run -output with NOMAD_VAR_staging_dc/domain PASS; structured comparison against original jobs confirms only expected DC/domain changes. Alternate test values propagate correctly. Missing required inputs rejected. Production render is identical with and without new group environment variables, including strict parsing. Local nomad job validate PASS both with zero job warnings; server driver validation skipped because deliberately no Nomad server connection. Sanitized report: ~/ai-data/DevOps-898/classifier-audit/nomad-parameter-verification.json. No cluster API validation, build or deploy occurred.

Next external action pending approval: create group data variables NOMAD_VAR_staging_dc=vk-test and NOMAD_VAR_staging_domain=vk-test.youdo.local, scope *, protected=false, masked=false, variable_type=env_var. They are nonsecret and must be available in branch lint jobs without an environment. No existing address/token variables are modified. Publication of the two task paths, commits, branch pushes and MRs still requires separate reviewed approval. Suggested commit for both: parameterize staging nomad datacenter and domain; suggested MR titles DevOps-898 parameterize hub staging datacenter and domain and DevOps-898 parameterize classifier staging datacenter and domain, targets master. Branch pipelines build/push branch image and latest; no tag, release, merge or deploy authorized.

## Group variables created and publication proposal

User explicitly approved creation of the two group variables (reply “Да” to the exact variable-creation proposal). POST created both in data; GET readback verified exact values vk-test / vk-test.youdo.local, scope *, protected=false, masked=false, variable_type=env_var, raw=true. Sanitized evidence: ~/ai-data/DevOps-898/classifier-audit/group-staging-variables.json. No existing address/token variables changed.

Read-only publication inspection: projects163/164 default master, no open MRs, squash default_off, recent preference squash=false/remove_source_branch=true, assignee a.solonenko. Current worktrees contain only the approved staging.nomad edit each. Ready MR description files prepared locally: hub-mr-description.md and classifier-mr-description.md in the audit directory, each one Russian paragraph plus task link only. No publication approval yet.

Publication proposal: commit in both repos parameterize staging nomad datacenter and domain. Hub MR DevOps-898 parameterize hub staging datacenter and domain from DevOps-898-deploy-houston-hub-on-vk to master; classifier MR DevOps-898 parameterize classifier staging datacenter and domain from DevOps-898-deploy-classifier-on-vk to master. Explicit paths deployments/staging.nomad only. Actual diff10insertions/2deletions each; local validation/render/production isolation checks passed as above. Branch push starts normal CI build/test/validation and pushes branch image plus overwrites latest. No tag-based release/staging deployment, manual production job, merge or runtime deployment included. NOMAD_STAGE_ADDR/TOKEN still require separate routing/access setup before actual deployment.

## Publication completed

Stage2 user approval: explicit “Да” to the reviewed commit/push/two-MR proposal including branch image/latest CI effects. Staged only deployments/staging.nomad in each repository; actual full staged path list and diff reviewed, diff --check passed. Commit message in both: parameterize staging nomad datacenter and domain.

- Hub f35af34763671084345e6062b1464d8661a5d26e pushed on DevOps-898-deploy-houston-hub-on-vk; MR24 https://gitlab.youdo.sg/data/houston/hub/-/merge_requests/24 to master. Pipeline141049 running, build3231728 running; three quality/Nomad test jobs created.
- Classifier0abc892ef2b9c9b80c670c962ade4cac87122c90 pushed on DevOps-898-deploy-classifier-on-vk; MR20 https://gitlab.youdo.sg/data/houston/classifier/-/merge_requests/20 to master. Pipeline141050 pending, build3231732 pending; four tests/quality/Nomad jobs created.

Readback verified exact branch SHA, MR title/source/target, a.solonenko assignment, squash=false and remove_source_branch=true for both. Both local working trees clean. No tag/release/deploy jobs exist in these branch pipelines. Pipeline success not yet established. No merge, tag, deploy or runtime write performed. Next separate external action proposal: project-specific NOMAD_STAGE_ADDR/TOKEN for both services, preserving protected staging credential policy and sourcing the intended shared VK deploy token from the existing GitLab variable rather than exposing any secret. Group-wide stage access variables remain unchanged.

## Project staging access configured; Mongo image blocker

User approved project staging credential creation (explicit “Да” to prior proposal). Created NOMAD_STAGE_ADDR=http://nomad.service.vk-test.consul:4646 and NOMAD_STAGE_TOKEN in projects163/164, scope*, protected=true matching inherited credential policy, token masked=true/address masked=false, raw=true. Token copied in memory from existing group youdo NOMAD_TOKEN_VK_TEST, never printed/saved; GET readback equality verified for all4project variables. No inherited group address/token changed. Sanitized evidence project-staging-access.json in audit directory.

Fresh initial CI snapshot: Hub build3231728 and lint3231731SUCCESS, ruff3231729SUCCESS, mypy3231730RUNNING; classifier build3231732PENDING, later jobs CREATED. Success not yet established for both complete pipelines.

Read-only image manifest HEAD checks: bitnami/mongodb:4.0.1 DockerHub404 and Nexus matching path404. Redis5-alpine and exporter v0.26.0-alpine DockerHub200. Exact archived bitnamilegacy/mongodb:4.0.1 is available200, digest sha256:8620699e9c7e9368330a7f36d6b18d375fdd9fff3c8cb9fb4fa77316c242099e. Official mongo4.0.28 also200 but unnecessary version/layout change avoided. Evidence sidecar-image-manifests.json and mongo-image-candidates.json. No image layers downloaded.

Prepared local1line Hub follow-up in deployments/staging.nomad image bitnami/mongodb:4.0.1 to bitnamilegacy/mongodb:4.0.1. Same branch; no commit/push yet. diff --check PASS; local job validate PASS (server driver validation skipped); structured rendered-job comparison confirms only image repository changed relative to current HEAD. Same Mongo version, /bitnami volume, TCP27017 and100MB unchanged. Runtime pull/start not established.

Publication approval needed for follow-up: commit use archived mongodb image for staging; push approved Hub branch and update existing MR24, target master. Revised MR title DevOps-898 configure hub staging deployment on vk; revised Russian description covers both parameters and image namespace replacement plus task link only. Normal CI rebuilds branch image/latest; no tags/deploy. Classifier MR20 unchanged. Request does not authorize merge/release/runtime actions.

Latest Hub CI result: mypy3231730FAILED runner_system_failure. Sanitized trace confirms failure before checks: runner could not pull python:3.12-slim-bookworm due to upstream TCP443 i/o timeout. Build, Ruff and Nomad lint remainSUCCESS. No retry performed; classifier build stillPENDING. This failure is not an HCL/type-check result.

## Mongo follow-up published; classifier runner blocker

User explicitly approved follow-up publication with “Сделай” to the reviewed1line diff/commit/push/MR-title update. Actual full staged diff contained only the Mongo namespace replacement; diff --check passed. Committed b933279af04ffc7d7a68434187a3f0060846e11e with use archived mongodb image for staging, pushed same Hub branch, updated existing MR24 title to DevOps-898 configure hub staging deployment on vk and Russian paragraph/task-link description. GET readback verified exact title/body/source/target/SHA and preserved assignee/squash settings. Local Hub worktree clean. Pipeline141051SUCCESS: build3231737,ruff3231738,mypy3231739,Nomad lint3231740 allSUCCESS. The earlier runner pull timeout did not recur. No merge/tag/release/deploy.

Classifier pipeline141050 remainsPENDING/build3231732tag dind with no runner. Fresh project GET identifies concrete cause: classifier shared_runners_enabled=false, group_runners_enabled=true, project runners list empty. Hub shared_runners_enabled=true, build ran successfully on instance runner105. Instance runner105/106 currently online and unpaused. Next separately approved external action: PUT projects/164 shared_runners_enabled=true only, so the existing pending dind build can be scheduled; no pipeline retry/recreation or YAML change required. No runner setting changed yet.

## Classifier shared runners enabled

User explicitly instructed “Включи shared runners”. PUT projects/164 shared_runners_enabled=true succeeded; fresh GET verified true, group_runners_enabled unchanged. Project now lists online/unpaused instance runners including105/106. Immediate build3231732 readback remainedPENDING with runner null; scheduler pickup/final pipeline result not yet established. No retry/recreated pipeline, merge, tag or deploy. Evidence shared-runners-enabled.json in audit directory.

## Hub merge/deploy readiness assessment

User asked whether Hub can be merged and deployed. Fresh GET: MR24opened/non-draft, mergeable/can_be_merged, no conflicts, discussions resolved, head b933279 and pipeline141051SUCCESS. Master stillb55f844. Project stage address VK and protected token present; group staging DC/domain correct; no STAGING_DISABLED at project/data/houston/data levels. All tags protected by *; protected staging credentials available to tag pipelines. Latest release2.7.5, next proposed2.7.6 (not created). Fresh GET /v1/jobs using the actual project staging token PASS, no houston-hub job exists in VK. Registry now contains branch image devops-898-deploy-houston-hub-on-vk and latest. Standard deployment path is merge MR, then separately approved new tag2.7.6 at resulting master; tag CI builds/releases and automatically deploys staging, production stays manual. User-approved initial empty Mongo applies. No merge/tag/deploy performed during assessment.

## Hub merge/tag authorized and executed

User explicitly instructed “Смержи и добавь тег” after the concrete Hub MR24 merge + protected tag2.7.6 on resulting master proposal, including automatic staging deployment effect. Rechecked source b933279/green CI/no conflicts and absence of2.7.6, merged MR24 with SHA guard, squash=false and agreed source deletion. Result master/merge commit b28b07ac3f91909c88442473e23139a65184e106. Separately created protected tag2.7.6 at that exact SHA and verified readback. Evidence hub-merge.json and hub-release.json. Release pipeline141056 running; build3231950 running, staging3231955 created, production3231956 created/manual policy. No manual production trigger. Read-only runtime monitoring script monitor-hub-release.py prepared in audit directory; first check no Hub job yet (404), matching pre-deploy state.

User asked classifier status during Hub execution. Fresh GET: classifier MR20opened/can_be_merged/no conflicts; pipeline141050SUCCESS with build3231732,test3231736,mypy3231734,ruff3231733,Nomad lint3231735 allSUCCESS. Latest tag2.6.9, next proposed2.6.10. No classifier merge/tag authorized or executed yet. Continue authorized Hub rollout monitoring; classifier merge/release awaits explicit instruction.

## Hub runtime accepted

Release141056SUCCESS; staging3231955SUCCESS, production3231956MANUAL/untriggered. Nomad job houston-hub version0 in vk-test uses registry.youdo.sg/data/houston/hub:2.7.6 plus bitnamilegacy/mongodb:4.0.1, exactly1app/1Mongo allocation. Both running and deployment healthy=true. Consul registration v2/instance=common, all checks passing. Routed /health200 and /experiments?max_results=1 HTTP200 with total0/returned0, matching user-approved empty database. Verified route added to current/service-addresses.env. Sanitized acceptance snapshot hub-release-status.json.

Initial startup: Mongo100MB allocation once OOM137, app twice exited while worker booting; recovered automatically without additional writes/retries/redeploy. Historical restart counts app2/Mongo1 retained, not reported as zero. Ephemeral persistence200MB/sticky+migrate and memory settings unchanged; no hardening added. Long-term memory stability not established by initial health.
