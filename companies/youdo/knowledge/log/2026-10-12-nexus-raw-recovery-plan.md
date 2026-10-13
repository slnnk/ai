---
system: nexus
status: verified
checked: 2026-10-12
tags: [recovery, raw, mobile, DevOps-890]
---
# Nexus raw repository recovery plan

## Task
Restore raw/raw-private Nexus configuration for DevOps-890, including Android/iOS publishers and Appium consumers.

## Context
Fresh Nexus on 10.18.24.233 has no raw repositories, raw-hosted blob, raw user or nx-raw role. Existing global anonymous access remains enabled by earlier user request. Public LB 172.28.0.141 already proxies both raw paths to msk3-nexus.youdo.corp.

## Actions
Read-only Nexus REST inventory, DevOps-890 GET, live GitLab default-ref source and variable GETs, public/internal HEADs, and SSH read of /etc/nginx/conf.d/nexus.youdo.com.conf. Prepared raw-plan.json and restore_raw.py under /home/slnnk/ai-data/nexus-recovery/. Schema validation against api-spec.json, py_compile and read-only restore_raw.py exited0. All five external creates were subsequently approved and completed; no repository edit.

## Findings
- Android project79/develop .gitlab-ci.yml uploads raw-private/android/gitlab_youdo_${TESTS_JOB_ID}.apk and corresponding version text.
- iOS project65/develop fastlane/Fastfile publishes raw-private/ios/gitlab_youdo.zip, gitlab_youdo_settings.zip and gitlab_youdo_version.txt.
- Android tests project69/master reads raw-private version text and sends Appium the raw/android APK URL. Therefore raw is a group with raw-private member.
- iOS tests project154/master (youdo/Test/youdo-ios-testing) reads version with auth, while Appium downloads http://nexus.youdo.corp/repository/raw-private/ios/gitlab_youdo.zip without auth. This internal hostname path was not independently network-tested.
- All four project-level NEXUS_CREDS values match, username raw. Secrets fetched at runtime only, never persisted or printed.
- Fixed iOS paths require hosted writePolicy ALLOW. No consumer DELETE requirement found.

## Changes
Prepared five creates in one explicitly reviewed apply command: File blob raw-hosted with relative path raw-hosted; hosted raw-private using it with strictContentTypeValidation=false and writePolicy=ALLOW; group raw using the same blob with member raw-private; role nx-raw with wildcard raw read/browse and raw-private add/edit; active raw user with existing credentials and sole nx-raw role. ATTACHMENT disposition. Required service email ci@youdo.com is an identifier only.

No branch or publication proposed: configuration is external API work, not a repository change. User explicitly approved all five changes with “Да”. Applied raw-hosted blob, raw-private hosted, raw group, nx-raw role and raw user. No branch/publication or CI run. First run stopped after repositories due to privilege name field mismatch (name vs id); corrected script and added guarded resume. A subsequent preflight assertion was corrected to accept Nexus relative blob path raw-hosted. Role/user were created; repository-root GET returned400 for raw group, so final verification uses asset REST and missing-object probes instead of expecting group directory listing200. No duplicate creates or changes outside approved scope.

## Risks
Recreated repositories are empty; historical APK/ZIP restoration or CI publication requires separate work and explicit external-write approval. Global anonymous read/browse includes raw-private and supports current iOS Appium URL. No change to anonymous policy proposed. No application artifact upload or pipeline run prepared. Local standard artifact directories have no ready mobile packages.

## Portable lesson
None.

## Applied verification
`python3 /home/slnnk/ai-data/nexus-recovery/verify_raw.py` exited0. Admin GET confirms raw-private online/ALLOW/raw-hosted/ATTACHMENT, raw group member raw-private, nx-raw exact read/browse/add/edit privileges and active raw user with sole nx-raw role. Authenticated raw asset listing HTTP200 and zero items; wrong password HTTP401. Missing-object probes return404 through internal msk3-nexus, public HTTPS nexus.youdo.com and iOS Appium HTTP nexus.youdo.corp for both repositories, authenticated and anonymous. This verifies missing-object routing, not successful real APK/ZIP downloading. No artifacts uploaded or pipelines run.
