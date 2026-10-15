---
system: jenkins
status: verified
checked: 2026-10-15
tags: [help, nomad, gitlab, DevOps-899]
---
# Help parallel rollout to eight test stands

## Summary

Help1.0.14 deployed in parallel on test and test1-test7; all eight GitLab jobs succeeded (31-39s), all eight Nomad jobs running/healthy/zero restarts.

## Task and context

User explicitly authorized Help while asking about Socket failure. Project557 youdo/youdo.help, release1.0.14 pipeline140977. Seven manual deploy-yandex-test jobs played; successful test5 job3228412 retried as3229441. Existing image/pipeline reused. No repository edits.

## Actions and evidence

Local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-help-stands899.py launch|watch|status` uses eight concurrent launch workers. Receipts under `/home/slnnk/ai-data/jenkins-recovery/help-stands-20261015/`. Only GitLab and Nomad status checks requested/performed. Nomad job name `youdo-help-<stand>`, from CI PROJECT_NAME.

## Changed files and limits

Local rollout helper/receipts and KB bookkeeping. No additional application/data/BuildAPI validation; no configuration changes.

## Results

| Stand | Job | Status | Duration seconds |
|---|---|---|---|
| test | 3228407 | success | 35.38 |
| test1 | 3228408 | success | 36.28 |
| test2 | 3228409 | success | 38.90 |
| test3 | 3228410 | success | 34.95 |
| test4 | 3228411 | success | 36.61 |
| test5 | 3229441 | success | 33.93 |
| test6 | 3228413 | success | 38.32 |
| test7 | 3228414 | success | 30.84 |
