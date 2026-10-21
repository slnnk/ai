---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, nomad-test, DevOps-899]
---

## Summary

User explicitly requested full Jenkins deployments for test2, test3, test7 and test8, analogous to test4/test5. All four builds were launched and observed running; completion has not been verified.

## Actions and evidence

Reference dynamic_deploy 5827 was SUCCESS. Its complete parameters were copied, changing only TEST_INSTANCE. Monolith pipeline 139914, static pipeline 139593, automation master, BRANCH gitlab; RESTORE/REDIS/RABBIT/ELASTIC/S3/NGINX/WEB_STATIC/MICROSERVICES/SUGGESTIONS_REINDEX true, RESTORE_B2B_ELASTIC false. Release issues Release-2.1003 and Release-2.917 preserved. No active builds or queue entries existed before launch.

- test2: https://build.youdo.sg/job/dynamic_deploy/5828/
- test3: https://build.youdo.sg/job/dynamic_deploy/5829/
- test7: https://build.youdo.sg/job/dynamic_deploy/5830/
- test8: https://build.youdo.sg/job/dynamic_deploy/5831/

Every build's actual parameters matched its expected payload. All were running at the last observation. Launches were sequential POST requests with a durable intent and receipt per stand.

## Files and commands

Local helper: ~/ai-data/jenkins-recovery/deploy-four-stands899.py launch|status. Receipts: ~/ai-data/jenkins-recovery/four-stands-20261015/test{2,3,7,8}.json. No repository changes.

## Risks and limits

Full restore was explicitly requested and uses the reference build's effects. A running build does not establish successful deployment or BuildAPI registration. test8 was outside the earlier explicitly seeded catalog scope; its microservice catalog and final stage outcome remain unverified.

## Runtime diagnosis after launch

User questioned long duration and possible stale Antifraud BuildAPI version. Read-only evidence: BuildAPI test2/test3/test7 references Antifraud23.8.7, pipeline140965, SHAfb11521; latest release tag also23.8.7. Therefore a stale release version was not established. test3 original deploy3228066 failed at PostgreSQL DB creation against10.18.26.39:5432 with FATAL: sorry, too many clients already (9.29s execution,186.7s queue). Jenkins started retries3228678(test3) and3228686(test7); final results not yet verified at this observation.

Jenkins test2 #5828 has not reached microservices: Nomad youdo-test2 deployment357009c7 failed due to progress deadline. Initial run14:45:08UTC waited for deadline; retry14:57:39UTC saw the same failed deployment and returnedrc1. test3/#5829 andtest7/#5830 reached Deploymicroservices/Checkjobs waiting. This is separate from Antifraud metadata freshness. No remediation was applied as part of this diagnosis.


## Jenkins deployment follow-up closed by user — 2026-10-20

The user confirmed that deployment now works correctly and BuildAPI updates. Closed the test2/test3/test7 deployment and metadata-consistency follow-up in the [central backlog](../../../../TODO.md), moving its closed record from the unrelated FeatureToggle section to Jenkins recovery. Earlier build failures and diagnostic limits remain historical evidence, not a current open investigation. No new fixes, Jenkins reruns or independent runtime checks were performed in this closure. This acceptance does not close unrelated Jenkins backup, monitoring or recovery proposals.
