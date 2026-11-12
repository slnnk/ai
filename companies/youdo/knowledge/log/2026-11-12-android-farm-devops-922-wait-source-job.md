---
system: android-farm
status: verified
checked: 2026-11-12
tags: [gitlab-ci, artifacts, failed-suite, supervised-review]
---
# DevOps-922: wait for source job before retry-suite download

## Task and context

The user assigned the source-job completion check to DevOps-922and requested an MR. Read-only YouTrackGETconfirms Android autotest rerun fix task, no description. The related [job3293803diagnosis](2026-11-12-android-farm-job3293803-failed-suite-download.md) shows retry-suite download overlapping source artifact upload, invalid27byteinput, and TestNGparsefailure. Source job success/failure must not gate download; completion is the intended condition.

## Original first-stage proposal — pending

Existing clean checkout /home/slnnk/git/youdo-android-testing currently on DevOps-908-gradle-image-18; refreshed origin with no working-tree/index change. Base origin/masterf126825b2f64098a57e37e6f9ec201764523a55a, confirmed project defaultmaster. No matching DevOps-922branches or matching open MRfound. Proposed branch DevOps-922-wait-for-source-job from origin/master. User has requested task/MR but not yet confirmed this concrete branch/base proposal; no branch creation/switch or repository edit performed.

Proposed scope: .gitlab-ci.ymlfailed-suite block only. Move existing source-job metadata GET before XMLdownload; poll finished_at until nonnull, accept source success/failed equally. Proposed bounded wait5minutes with5secondpollinterval; timeout yields clear message before any device preparation. Reuse response pipeline.id. Fail HTTPrequests visibly rather than treating an error body as valid job metadata/XML. No XMLparser dependency, emulator/device changes or revival of cancelled preparation proposals.

Expected validation: mocked source initiallyrunning thenfinishedsuccess/failed yields download only after finish; alreadyfinishedsource proceeds immediately; neverfinishedsource times out without download/preparation; API/download HTTPfailure fails clearly. Check actual CI block with local mock HTTPresponses and simulated time, parse YAML, git diff --checkand GitLabCILint. Inspect actual publication CI rules before second approval. No real sourcejobwait, CIrerun or farm commands.

## Status

Await first approval. Second publication approval remains necessary after actual diff/checks/names/CIeffects are prepared. No background commands/agents remain.

## Portable lesson

None.

## First approval and actual implementation — 2026-11-12

User replied `Да` to the exact repository/branch/base/scope proposal, including5minute/5secondwait and explicit HTTP-error handling. Created approved DevOps-922-wait-for-source-job from origin/masterf126825b2f64098a57e37e6f9ec201764523a55a in existing clean checkout. Only .gitlab-ci.ymlfailed-suite before_script block changed:17insertions/2deletions. Existing source-job GET moved before download; use finished_at completion, reuse pipeline.id, curl--failon metadata/download. Deadline based on date+300, curlmax-timebounded by remaining deadline, sleep5between pending polls. No status-success requirement, XMLparserdependency, device/emulator/adb.shchange or actual CIrun. Existing non-retry/source0branches preserved.

## Verification

External local harness extracts and executes the actual YAMLblock with localhostHTTP/mockdate/sleep, synthetic token and no realGitLab/farmcalls.10cases passed: running→success, running→failed, alreadyfinishedsuccess, alreadyfinishedfailed,300secondtimeout/60polls/noartifactrequest, metadataHTTP500, malformedmetadata, artifactHTTP404, normalsuitebypass, source0bypass. Artifact download asserted never before completion; pipeline.id456reused. Fakeclock removes real5minwait. All HTTPservers/threads stopped.

PyYAMLparse, git diff --checkand semantic YAMLcomparison passed: after replacing the one intended block, entire YAMLmatches base. GitLabCILintvalid/noerrors/nowarnings. Index empty; only approved .gitlab-ci.ymlmodified. Generated harness/results, exact change.diff, CI-lint/body/proposal/snapshot stored under ~/ai-data/gitlab-workflow/DevOps-922/youdo-android-testing/.

## Second publication proposal — pending

Commit `wait for source job before retry suite download`; ReadyMRtitle `DevOps-922 wait for source job before retry suite download`; source approved branch, targetmaster, assigna.solonenko, squashfalse/remove-source-on-mergetrue based on read-only project preferences. No matching openMRexists. Body exactly:

```text
Перед скачиванием набора упавших тестов добавлено ожидание завершения исходной job независимо от её результата. Проверка выполняется каждые 5 секунд до 5 минут; ошибки HTTP завершают запуск с ошибкой.

https://youtrack.youdo.com/youtrack/issue/DevOps-922
```

Inspected complete CIworkflow: only CI_PIPELINE_SOURCEweb/api allowed, no includes. Push/MRcreationdo not match; no automatic farm job, preparation/retry/reportupload/notification triggered by publication. No pipeline/manualjobexecution or merge requested. Snapshot saved before publication request; stage/commit/push/MRnot yet performed. Applicable scope/naming outcomes pending actual final artifacts, no speculative pass recorded. No background operation remains.

## Second approval and verified publication — 2026-11-12

User replied `Да` to exact stage2commit/push/ReadyMRproposal. Snapshot check matched before staging. Staged only .gitlab-ci.yml; actual full index diff reviewed and whitespace checkpassed. Commit6c18e1ad19dd36f4cfeab5a44845cbdb906411fe has exact approved patch, byte-for-byte comparison with change.diffpassed; no extra files or unrelated edits. Working treeclean. Non-force push completed.

Created [MR1165](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/merge_requests/1165), Ready, sourceDevOps-922-wait-for-source-job,targetmaster, assigneda.solonenko,squashfalse/remove-source-on-mergetrue. Exact title/body/source/target/fullSHA verified in publish result and separate read-only verification. Both show pipelinesempty, consistent with web/apionlyworkflow. No real autotest, device preparation, notification, new retry pipeline or farm operation triggered by publication.

Requested MRpreparation/publication complete. Integration/review remains in central TODO. No merge, manual/web/APIpipelineexecution, YouTrackcomment/fieldwrite or runtimevalidation performed. Original XMLsyntax-validation suggestion was not implemented: approved task scope is completionwait plus HTTPfailurehandling, with no XMLparserdependency. Retain that distinction rather than claiming all possible invalid XMLinputs are rejected. Scope/naming first-attempt outcomes evaluated on actual artifacts. All commands finished; no background operations remain.

## User merge and requested comment draft — 2026-11-12

User reported merge and requested preparing a DevOps-922comment. GETconfirms MR1165merged into master20:10:46MSK, mergecommitd603c3e5e9f11ae4decda3716ec209dde00a8d17. Task remains In Progress/unresolved, comments empty, Merge Requestfield222-47empty. Do not claim task closure. Prepared behavior-only Russian draft without local-test details or an MR-integration sentence; exact text in external youtrack-comment.txt:

```text
Перед скачиванием `FailedTestSuite` добавлено ожидание завершения исходной job независимо от её результата: проверка каждые 5 секунд, максимум 5 минут. При превышении времени ожидания или HTTP-ошибке запуск завершается с ошибкой до подготовки устройств и старта тестов.
```

MR1165URLis prepared separately for the dedicated Merge Requestfield; no field/comment update requested or performed in this preparation turn. Original corrected DevOps-921format remains scoped evidence, not a new global instruction. Comment review first-attempt evaluation pending user feedback/publication. Central integration follow-up now records verified merge and pending proposed summary/field review. No new CI/farm/APIwrites, no background commands.

## Comment revision: problem description requested — 2026-11-12

The user requested adding the problem description to the prepared DevOps-922comment. Revised task-specific draft adds early source-artifact request risk and the verified job3293803TestNGprologfailure, preserving uncertainty of the exact27byteHTTPpayload. It keeps local-check details and MRintegration sentence out; MR1165remains a separately prepared dedicated field value. Updated exact draft:

```text
Повторный запуск мог запросить `FailedTestSuite` до окончания публикации артефактов исходной job. В [job3293803](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3293803) TestNG получил некорректный XML и завершился с `Content is not allowed in prolog` до запуска тестов.

Перед скачиванием `FailedTestSuite` добавлено ожидание завершения исходной job независимо от её результата: проверка каждые 5 секунд, максимум 5 минут. При превышении времени ожидания или HTTP-ошибке запуск завершается с ошибкой до подготовки устройств и старта тестов.
```

Await user review; no tracker write or task-state change.

## Approved comment publication — 2026-11-12

After reviewing the revised draft with problem description, the user explicitly requested adding the comment. Read-before-write confirmed DevOps-922identity and no matching summary. Created comment74-125545with exact body from external youtrack-comment.txt. Independent GET confirmed exact text equality; receipt youtrack-comment-receipt.json has verifiedtrue. No issue-state or custom-field write performed. Subsequent GET still shows StateInProgress and Merge Requestfield222-47null. The separately prepared MRfield update remains a proposal requiring authorization; do not claim task closure or field completion.

Original draft described the change only; user requested adding the problem. Revised approved/persisted text includes the early artifact-request risk and job3293803XMLparsefailure, then completionwait/timeout/HTTPbehavior. No local-check paragraph or MRintegration sentence in comment. Record first-attempt comment-review fail for the user-corrected draft; recovered final publication independently verified, not rescored as pass. Task-specific description preference recorded without making it global. All commands finished, no background operations.

## Omitted MR attachment corrected — 2026-11-12

The user corrected the omitted MRattachment after comment publication. The agent had incorrectly left the expected dedicated MRfield as a separate proposal despite the user already explaining this workflow in the same discussion. User correction authorizes attaching the known task MR. Read-before-write confirmed field222-47still empty; saved MR1165URLand independently verified exact value. Receipt mr-field-receipt.jsonverifiedtrue. Comment74-125545remains unchanged; no issue-state change. This supersedes the pending MRfield proposal above.

Final task-summary delivery complete: mergedcode, approved problem/fixcomment and dedicated MRfield verified. Closed agent follow-up only; YouTrackwas lastobservedInProgress, no issueclosure claimed. Original XMLsyntaxparser not implemented outside approved wait/HTTPscope. No background operations.
