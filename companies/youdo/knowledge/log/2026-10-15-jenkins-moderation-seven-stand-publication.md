---
system: jenkins
status: verified
checked: 2026-10-15
tags: [moderation, static, gitlab, DevOps-899]
---
# Moderation static publication to seven additional test stands

## Summary

Moderation1.0.45 static publication accepted on test,test1-test4,test6,test7: all seven jobs SUCCESS150-173s. Existing successful test5 publication retained. The selected service/static rollout sequence is complete; TrackingPixel excluded and Cerberus2 postponed.

## Task and context

User approved the seven remaining stands after all selected runtime services were accepted. Project546 youdo/youdo.moderation, release1.0.45 pipeline140978. Jobs3228432-3228436/3228438/3228439 played concurrently; test5job3228437 not repeated. No new build/pipeline or repository changes. Original pipeline static publication behavior retained (stand-specific S3 prefix replacement/upload, common fonts and manifest registration).

## Actions and evidence

Local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-moderation-stands899.py launch|watch|status`; seven concurrent workers. Receipts `/home/slnnk/ai-data/jenkins-recovery/moderation-stands-20261015/`. Only GitLab job statuses checked; this is static publication, no Nomad job deployment.

## Changed files and limits

Local helper/receipts and KB bookkeeping. No additional HTTP/S3/content/Consul validation or configuration edits.

## Results

| Stand | Job | Status | Duration seconds |
|---|---|---|---|
| test | 3228432 | success | 171.41 |
| test1 | 3228433 | success | 153.71 |
| test2 | 3228434 | success | 171.83 |
| test3 | 3228435 | success | 171.56 |
| test4 | 3228436 | success | 150.02 |
| test6 | 3228438 | success | 171.63 |
| test7 | 3228439 | success | 172.60 |
