---
system: jenkins
status: verified
checked: 2026-10-15
tags: [content, nomad, gitlab, DevOps-899]
---
# Content parallel rollout to eight test stands

## Summary

Content2.5.13 parallel rollout accepted on all eight test/test1-test7 stands: GitLab all success35-78s; Nomad all running/healthy/zero restarts.

## Task and context

User explicitly approved Content as next service after accepted Help and Socket. Project334 youdo/microservices/youdo.content, release2.5.13 pipeline140983. Seven manual deploy-yandex-test jobs played; successful test5 job3228570 retried as3229459. Existing images/pipeline reused; no repository changes or new release.

## Actions and evidence

Local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-content-stands899.py launch|watch|status` uses eight concurrent launch workers. Receipts under `/home/slnnk/ai-data/jenkins-recovery/content-stands-20261015/`. Verification limited to GitLab/Nomad status, as requested. Custom Levant/Vault deploy behavior retained.

## Changed files and limits

Local rollout helper/receipts and KB bookkeeping only. No application, data, HTTP, logs or BuildAPI validation added. No configuration edits.

## Results

| Stand | Job | Status | Duration seconds |
|---|---|---|---|
| test | 3228565 | success | 78.09 |
| test1 | 3228566 | success | 73.14 |
| test2 | 3228567 | success | 64.11 |
| test3 | 3228568 | success | 35.02 |
| test4 | 3228569 | success | 72.46 |
| test5 | 3229459 | success | 47.12 |
| test6 | 3228571 | success | 38.85 |
| test7 | 3228572 | success | 48.37 |
