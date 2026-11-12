---
system: android-farm
status: verified
checked: 2026-11-12
tags: [gitlab-ci, apk, nexus, supervised-review]
---
# DevOps-921: fail Nexus APK publication on HTTP errors

## Task and evidence

User requested implementing the existing APK HTTP-error-handling task under DevOps-921. Read-only YouTrack GET confirms the issue concerns Android Nexus publication error handling, with no description. Existing incident job3273026returned two HTTP500responses but succeeded; Nexus storage was subsequently restored. Current fetched default develop3461102079still uses curl -v --upload-file without --fail for APK and version metadata in .publish_for_tests.

## First-stage proposal — pending

Repository /home/slnnk/git/android-youdo4, clean existing checkout currently on DevOps-904-cache-gradle-dependencies. Proposed new branch DevOps-921-fail-apk-upload-on-http-errors from origin/develop3461102079. Local/remote matching branches and matching open MR absent at November12read-only check. User has requested the task but has not yet approved this concrete branch/base proposal. No branch creation/switch or repository edits performed.

Proposed task-only scope: add --fail to the two curl uploads in .publish_for_tests. Preserve publication destinations, ordering, variables and allow_failure. Expected result: successful HTTP response retains exit0, HTTP500returns nonzero for either upload and stops the job script. Verify with local controlled HTTP responses using the same curl options and a small test payload; YAML parse and git diff --check. No Nexus upload, retry, pipeline or store publication requested. Second supervised publication gate remains separate.

## Status

Await first approval. Central TODO entry linked to this task. No background commands or agents remain. No external mutations, publication or repository changes.

## Portable lesson

None.

## First approval and implementation — 2026-11-12

User replied `Да` to the exact repo/branch/base/scope proposal. Created DevOps-921-fail-apk-upload-on-http-errors from approved origin/develop3461102079d0d36e9f683facfcd9be11e07f7da8 in the clean existing checkout. Actual change is exactly --fail added to the2curl uploads in .gitlab-ci.yml. Index remains empty; no unrelated changes. Did not change allow_failure, endpoints, variables or upload order.

## Verification

Local HTTP harness outside the repo extracts the3script commands from the actual YAML, substitutes only the localhost endpoint and supplies synthetic credentials/payload. Both201responses yield exit0; APK500yields exit22with1request/no metadata upload; version500yields exit22with2requests. Original commands without --fail reproduce exit0on500/500. All4cases passed with curl7.68.0; server/thread stopped. Sandbox initially denied local socket creation; approved execution outside sandbox completed. No Nexus requests or real credentials used. YAML parsed with !reference support; git diff --checkpassed. Read-only GitLab CI Lintvalid/noerrors/nowarnings, no pipeline created. Results, exact diff, body/proposal/snapshot under ~/ai-data/gitlab-workflow/DevOps-921/android-youdo4/.

## Second-stage publication proposal — pending

Commit: `fail apk uploads on http errors`. Ready MR title: `DevOps-921 fail apk uploads on http errors`. Source approved task branch; target develop. Body exactly:

```text
Добавлена проверка HTTP-ошибок при загрузке APK и файла версии в Nexus: при ответе 4xx/5xx публикация завершается с ошибкой вместо ложного успеха.

https://youtrack.youdo.com/youtrack/issue/DevOps-921
```

Assign a.solonenko, squashoff/source-deletion-on-merge based on project preferences; no merge authorized. Snapshot saved before asking for publication. No stage/commit/push/MR yet.

CI effects: source branch push matches neither staging/hot-fix nor MR-target rules. MRto develop enables feature build, feature_browserstack upload (allow_failuretrue), feature_notify calling YouTrack helpers for state/MR field and sending android-builds notification. ISSUE_NAME extraction accepts only AND-ids, so the DevOps branch maps to an invalid fallback issue string; these calls may fail or attempt updates against a nonexistent issue, not necessarily DevOps-921. This pre-existing behavior was not changed. Need explicit publication consent covering automatic BrowserStack/YouTrack/notification side effects. Nexus uploads remainmanual; store jobs do not match this branch. No real publication/release/deployment claimed or authorized.

Scope/naming outcomes remain pending task completion/publication; current diff/proposal matches canonical conventions and requested minimal scope. All task commands/HTTP server completed; no background work.

## Second approval and verified publication — 2026-11-12

User replied `Да` to the exact commit/push/Ready MR proposal, including disclosed automatic feature-pipeline BrowserStack/YouTrack/notification effects. Snapshot check passed unchanged before staging. Staged only .gitlab-ci.yml; reviewed entire staged diff/index (exact2--fail additions, no other files), git diff --cached --checkpassed. Committed `fail apk uploads on http errors` as536493b67c69a2c9cdb3f05307246db296ea1b85. Commit patch byte-for-byte matches prepared change.diff. Working tree clean.

Pushed approved source branch without force. Created [MR2926](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/merge_requests/2926), Ready, targetdevelop, assigneda.solonenko, squashfalse/remove-source-on-mergetrue. Full SHA, branch/source/target, title and exact approved body verified by publication helper and a separate read-only verify. Initial pipeline list empty; later verify reports [pipeline142947](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/pipelines/142947) running. No finished CI outcome or individual external side-effect success claimed. No merge, manual job, Nexus upload, release, deployment or YouTrack comment performed by the agent.

Publication stage complete; implementation has local HTTP/YAML/CI-lint verification. Integration and actual CI outcome remain pending in the central MR-review follow-up. Scope and naming first-attempt outcomes evaluated against actual commit/MR artifacts, not approval alone. No local background commands, server threads or agents remain; remote GitLab pipeline remains running, view/cancel controls on its linked page. No automatic watcher started.

## User merge/closure and comment preparation — 2026-11-12

User reported merging MR and closing the task, then requested a task comment. Read-only verification confirms MR2926merged into develop at19:34:09MSK, mergecommit8368aafe368c9b01e3cecf264d1515c82c9c7efa. YouTrack DevOps-921is Fixed/resolved, comments empty. Head pipeline142947is canceled, not successful; prior running state above is superseded, no watcher/background operation remains. User acceptance closes integration follow-up without claiming a real Nexus upload or successful full build.

Prepared concise Russian summary, exact draft under ~/ai-data/gitlab-workflow/DevOps-921/android-youdo4/youtrack-comment.txt. Draft includes2curl--fail changes, local201/500verification, successful CI Lint and clickable merged MR2926; no green pipeline/runtime claim. No matching summary exists, so propose creating one comment. Exact text:

```text
В `.publish_for_tests` добавлен `--fail` для загрузки APK и файла версии в Nexus. При HTTP 4xx/5xx job завершается с ошибкой; если не загрузился APK, загрузка версии не выполняется.

Проверено на локальных HTTP-ответах 201/500; GitLab CI Lint — без ошибок и предупреждений.

[MR2926](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/merge_requests/2926) влит в `develop`.
```

Await exact-comment confirmation required by current/CONTEXT.md. No YouTrack comment or issue-field mutation performed. Comment-review evaluation remains pending publication.

## Comment-format correction and MR field — 2026-11-12

The user removed the local-check paragraph from the proposed summary and requested placing MR2926in the issue dedicated MR field instead of a comment sentence. Keep this formatting direction scoped to DevOps-921. Original draft remains above as historical proposal; final proposed comment is:

```text
В `.publish_for_tests` добавлен `--fail` для загрузки APK и файла версии в Nexus. При HTTP 4xx/5xx job завершается с ошибкой; если не загрузился APK, загрузка версии не выполняется.
```

Read-only GET confirms Merge Request custom field222-47/typeTextIssueCustomFieldcurrentlynull. Proposed exact field value: https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/merge_requests/2926 . Await explicit confirmation of revised comment and concrete field update before external writes; no comment or field mutation performed. Existing helper defaults favor clickable MRlinks in comments, but this task-specific user direction supersedes that presentation for DevOps-921.

## Approved comment and MR-field publication — 2026-11-12

User replied `Да` to the revised exact comment and concrete MR-field update. Read-before-write confirmed field222-47still empty and no existing matching summary. Saved MR2926URL in Merge Request as TextIssueCustomField.value.text, verified GET. Created comment74-125544with the exact approved body from youtrack-comment.txt. Independent GET confirmed exact comment-text equality and reverified field URL. Receipt: ~/ai-data/gitlab-workflow/DevOps-921/android-youdo4/youtrack-publication-receipt.json, verifiedtrue. No issue state or other fields changed.

The original comment proposal included local-check details and a merged-MR sentence; user rejected those presentation choices. Corrected final text omits both, stores MR in the dedicated field and was explicitly approved before publication. First-attempt comment-review outcome is recorded as fail for this user-corrected proposal; recovered final publication is separately verified, not rescored as a pass. The task-specific formatting rule was introduced by this correction and is not evaluated against the mistake that created it.

DevOps-921accepted complete: user-merged/closed, code and final task summary delivered. Central follow-up closed; no additional runtime/Nexus run implied or requested. All commands finished, no local or remote task operation remains active (pipeline142947already canceled). Remaining unrelated Android items stay in central TODO.
