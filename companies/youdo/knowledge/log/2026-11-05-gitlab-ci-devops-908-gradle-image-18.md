---
system: gitlab-ci
status: verified
checked: 2026-11-05
tags: [android, gitlab-ci]
---
# DevOps-908: Android autotest Gradle image tag 18

## Task
Update the Android autotest CI image to tag `18` for DevOps-908 and prepare an MR.
Source job: https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3250511.

## Context
Existing clean checkout `/home/slnnk/git/youdo-android-testing`; project `youdo/Test/youdo-android-testing` (69).
Read-only GitLab inspection confirmed job `autotests`, failed pipeline `141642`, ref `master`, SHA `0777c8260bce68b867952417ff4731d2575d1b99`.
Fetched `origin/master`; it matches the job SHA. No existing DevOps-908 MR was found.

## Actions
Proposed and approved branch `DevOps-908-gradle-image-18` from `origin/master`.
User approval: `Да и подготовь МР` after the exact branch/base/tag proposal.
Created the branch in the existing checkout and changed `.gitlab-ci.yml` line 68 from `gradle:12` to `gradle:18`.
Names were accepted without correction.

## Checks and CI effects
`git diff --check` passed. PyYAML parsed the configuration; the exact image and workflow rules were verified.
The actual diff contains one replacement only. Index was initially empty; the staged diff was reviewed and contained only the approved one-line image change.
`workflow.rules` allows only `web` and `api`; push and MR creation do not create a pipeline.
No real autotest run or registry pull was performed. CI job retry and deployment are outside this proposal.

## Publication proposal
Source `DevOps-908-gradle-image-18`, target `master`, ready MR.
Commit: `update android autotest gradle image to 18`.
Title: `DevOps-908 Update android autotest gradle image to 18`.
Description and immutable-state snapshot are under `/home/slnnk/ai-data/gitlab-workflow/DevOps-908/youdo-android-testing/`.

## Status and risks
2026-11-05: second approval received as `Да` in direct response to the full commit/push/MR proposal. Snapshot comparison passed immediately before staging.
Committed `7ac4940501f03dcabeae0a35bad49a1733cc39dc`; reviewed the resulting commit and pushed the approved source branch successfully.
Created and verified ready [MR !1163](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/merge_requests/1163), source `DevOps-908-gradle-image-18`, target `master`.
The helper verified source/MR SHA, title and description; assignee `a.solonenko`, squash disabled, source deletion on merge enabled. Pipeline inspection was available and returned an empty list.
Sandbox DNS blocked the first push attempt before connecting; the escalated push succeeded. No merge, pipeline execution or tracker write performed.
Publication is complete and its entry in [central TODO](../../../../TODO.md) is closed. No background operations remain.

## Portable lesson
none

## Endpoint follow-up approved for local implementation (2026-11-05)
User requested replacing every `yandex-test` endpoint, then approved reuse of `DevOps-908-gradle-image-18` / target `master` and added the three large MSSQL servers for test/test1/test6.
Only `config/selenium.conf` changed:221 literal domain replacements and3 MSSQL hostname replacements from `sql-test*.ru-central1.internal` to `vk-ms1-sql-test*.mcs.local`; port1433 preserved.
The three destination names match `automation-test-yandex/group_vars/test.yml`, `test1.yml`, `test6.yml` and the prior recovery evidence. Logical database names remain as configured.
Exact transformation and file scope verified; `git diff --check` passed. Typesafe Config1.4.2 parsed and resolved the full file; the three exact MSSQL URLs were asserted successfully.
Proposed follow-up commit: `update autotest service and mssql endpoints for vk`.
Proposed expanded MR title: `DevOps-908 Update android autotest image and endpoints for vk`.
Updated Russian description includes image18, all VK endpoints and the three MSSQL servers, followed by the DevOps-908 link.
Proposal/body/snapshot stored under `/home/slnnk/ai-data/gitlab-workflow/DevOps-908/youdo-android-testing/endpoints/`.
The earlier image publication is complete; this expanded endpoint publication requires renewed second approval. No follow-up commit/push/MR update yet; no real run or service availability audit performed.
CI workflow is unchanged: push/MR update creates no pipeline; no deployment/retry authorized. Broader service readiness is unverified.

## Endpoint publication completed (2026-11-05)
Second approval received as `Да` in direct response to the exact follow-up diff, commit, expanded MR title/body and CI-effects proposal. Snapshot check matched before staging. The entire index and resulting commit were checked against the approved literal transformation.
Committed `cdea347741d72635371e4bdd80becd645a2efadf` and pushed the existing approved source branch successfully. The checkout is clean.
Updated MR1163 title and description through one targeted PUT because the standard publication helper rejects a changed existing title. GET verification before and after preserved readiness, assignee, source/target, squash and source-deletion settings.
The standard verify helper then confirmed exact remote source/MR SHA, title and body. Ready [MR1163](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/merge_requests/1163) remains assigned to `a.solonenko`, squash disabled, source deletion on merge enabled. Pipeline list is empty; no new run was launched.
This supersedes the pending endpoint publication status above; its central TODO entry is closed. Merge, deployment and runtime validation were not performed. No background operations remain. Endpoint readiness beyond the earlier Houston GETs remains unverified.

## Gradle dependency-cache follow-up locally prepared (2026-11-05)
After the read-only [637-request baseline](2026-11-05-nexus-android-autotest-job3278160-request-count.md), user requested implementation and explicitly approved reusing project69, branch DevOps-908-gradle-image-18 from master, existing MR1163. Original and final branch/base names are unchanged; initial `Сделай` was followed by `Да` to the explicit repository/branch/MR proposal.
Starting checkout was clean at cdea3477. Changed exactly two files: removed unconditional `--refresh-dependencies` from `.gitlab-ci.yml` and added `configurations.configureEach { resolutionStrategy.cacheChangingModulesFor 0, 'seconds' }` to build.gradle. Existing cache keys/paths and failed-suite behavior are unchanged; no cache-splitting change was included.
This preserves per-build checks for changing/SNAPSHOT modules while immutable dependencies retain default caching. It applies to all changing dependencies, including the two declared internal SNAPSHOTs.
Checks: diff whitespace passed, YAML parsed, whole CI structure compared with only refresh flag removal, exact build.gradle insertion verified, Groovy4.0.28 SourceUnit syntax parse passed without build execution. Gradle8.13 configuration/real tests and Nexus savings remain unverified; no build-tool downloads or CI runs performed.
Prepared commit `reuse gradle cache while refreshing snapshot dependencies`; expanded MR title `DevOps-908 Update android autotest image, endpoints and dependency caching`; Russian description preserves prior image/endpoints context and adds dependency-cache behavior, followed by the task link.
Publication proposal/body/snapshot stored in `/home/slnnk/ai-data/gitlab-workflow/DevOps-908/youdo-android-testing/gradle-cache/`. Second approval for this expanded publication is pending; no staging/commit/push/MR update for this follow-up yet.
CI workflow remains web/api only: push/MR update creates no pipeline. The proposed later job behavior changes dependency freshness, not deployment. No background operations remain.

## Publication status rechecked and device issue deferred (2026-11-05)
On user status request, local HEAD remains cdea3477; only .gitlab-ci.yml and build.gradle have unstaged cache-policy edits (4insertions/1deletion). Read-only GitLab inspection confirms MR1163 remains open with its published image/endpoints title. The cache follow-up has not been committed, pushed or included in the MR; publication approval has not been received.
User explicitly deferred the separate x4pf5l5haegykni7 device/IME issue to the central backlog. Do not treat it as authorization for repair or as unfinished DevOps-908 code scope. Cache publication and later authorized request-count validation remain the existing DevOps-908 follow-up; merge is unperformed and requires separate authorization if requested of the agent.

## Gradle-cache publication completed (2026-11-05)
User explicitly instructed `Опубликуй изменения по кэшу` after the exact prepared publication proposal and status review; this authorizes the previously described task-only commit/push/MR sequence.
Snapshot comparison passed before staging. Entire staged diff was verified against the expected two-file transformation. Created commit `91ce02f2e47e05f44d3fa8fea710dc57acc03e84`, message `reuse gradle cache while refreshing snapshot dependencies`; inspected resulting commit and pushed source branch successfully.
Updated MR1163 title to `DevOps-908 Update android autotest image, endpoints and dependency caching`, preserving previous image/endpoints context in its Russian description and adding new cache behavior. Existing helper refuses changed titles, so a narrow PUT updated only title/description after checking branch SHA and preserved metadata. GET read-back and standard verify helper confirmed expected source/MR SHA, title, body, source/target, readiness and assignee.
Ready MR remains assigned to a.solonenko, target master, squash false, source deletion on merge true. Pipeline list is empty; no new job/retry/merge/deployment occurred. Checkout is clean; no background operations remain.
This supersedes pending/unpublished cache statuses above. Publication is complete. Static checks passed as previously recorded, but no Gradle8.13 project execution or Nexus request-reduction measurement exists yet. Any later run/merge needs its own applicable authorization; device IME work remains separately deferred.

## Merge and measured cache validation complete (2026-11-05)
User reported merge and launched pipelines; read-only GitLab verification confirms MR1163 merged20:02:27 Moscow asf126825b. Both post-merge jobs3278752/3278763 succeeded on that SHA and restored/saved Gradle cache.
[Measured Nexus verification](2026-11-05-nexus-devops-908-autotest-cache-verified.md) exactly matches server/trace counts:316requests in successful pre-patch warm job3278749,8each in the two post-merge runs,97.47%reduction. The remaining8requests check metadata/POM/JAR for the two internal SNAPSHOTs. Fresh-library checking remains active; a newly republished SNAPSHOT artifact was not part of this sample.
This supersedes earlier unmerged/unmeasured statuses. Requested publication and warm-cache verification scope is complete; central TODO item is closed. Cross-runner/cold-cache verification and cache splitting were not requested or performed. Device IME issue remains separate and deferred. No background operations remain.

## Requested narrow YouTrack comment published (2026-11-05)
User explicitly requested adding only the supplied image18/VK-endpoints/three-MSSQL-hosts paragraph to DevOps-908, excluding cache and runtime-count information.
Read-only inspection confirmed issue71-139081 (`[Android] Не работают автотесты`) with zero comments. Created comment74-125201; GET read-back verified exact supplied text. No issue fields/state were changed. Local text/receipt under `/home/slnnk/ai-data/gitlab-workflow/DevOps-908/youtrack/`. No background operations remain.

## User task closure (2026-11-05)
User reports DevOps-908 closed after the requested comment publication. Accept the task as complete; no external tracker mutation or independent status GET was performed in this step.
Source changes, merge and warm-cache verification are already complete. No DevOps-908 follow-up remains pending. The separately deferred x4pf5l5haegykni7 UnicodeIME item remains open outside this task and is not reopened or executed by task closure. No background operations remain.
