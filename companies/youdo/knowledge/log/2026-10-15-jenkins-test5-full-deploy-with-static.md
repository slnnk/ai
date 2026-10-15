---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, nomad, static, monolith, vk-test]
---
# Jenkins test5 deployment with rebuilt monolith and static enabled

## Summary

User explicitly requested launching Jenkins deployment including static after the successful direct Nomad restart. Started [dynamic_deploy5824](https://build.youdo.sg/job/dynamic_deploy/5824/), queue19138, requested2026-10-14T23:07:07UTC. API confirmsbuildingtrue and exactparametersmatch. Subsequent status check confirmed finalFAILURE458192ms onPostupdateauthorizationtimeout after successful monolith/static deployment.

## Parameters

TEST_INSTANCE=test5, MONOLITH_PIPELINE_ID=139914, STATIC_PIPELINE_ID=139593, AUTOMATION_BRANCH=master, BRANCH=gitlab. RESTORE/REDIS/RABBIT/ELASTIC/S3/NGINX/SUGGESTIONS_REINDEX=true; WEB_STATIC=true; RESTORE_B2B_ELASTIC/MICROSERVICES=false. Previous Restore selections retained; no new large database restore option enabled.

## Preparation and cache check

- Rebuilt monolith artifact3226699 andDocker3226700 success; staticbuild_ssr3226692/builddocker3226693 success, checked by live GET. Refreshed localpreflight with20verifiedrebuiltmonolithdigests andnewartifactjob, enabledWEB_STATIC only.
- Jenkins automation uses mutable139914 tags withoutforce_pull. Direct successful Nomadjobversion3 usesdigestrefs, which does not imply numeric cached tags were refreshed. Read-only rootDockerinspect via existingyoudoSSH/sudo route on8eligible readyVKclients found all20numeric tags absent on eachnode. Dockerdaemonavailability andNotFounderrors distinguished; staleimagecount0, so no dockerpull/retag/cachedelete performed. Currentdigest-pinned job left untouched.
- Helper test5-image-cache.py and metadata receipts in ~/ai-data/jenkins-recovery; inspection executed only. SSHknownhosts localaccept-new uses workstationkey; no remote key or authfile change.
- deploy-test5.py launch guarded no existingreceipt/no concurrentdynamic_deployjob, wrote pendingreceipt beforePOST. Confirmedbuild5824parameters by GET; wfapi unavailable404, not treated asdeploymentfailure.

## Files and limits

Only localmetadata/helpers/KB changed, no repository checkout/branch/commit/CI source changes. Launchreceipt ~/ai-data/jenkins-recovery/test5-full-deploy-static-20261015.json. Jenkins performs selectedRestore/Post/Suggestions andGitLabstaticjob as normal; previousignoredRabbit401 is not assumed resolved. Final resultFAILURE; deployment succeeded butPostupdatefailed. [Prior image/runtime success](2026-10-15-jenkins-monolith-rebuild-nomad-restart.md).

## Final status check

User requested status. Jenkins5824 finishedFAILURE458192ms (7m38s); parametersmatchtrue. Monolith Nomadyoudo-test5 version6 running, deployment18c7f346-0c50-8fdb-4114-20c8939f9a60 successful; both groups HealthyAllocs1/UnhealthyAllocs0,19service tasksrunning andzero failed/restarts. Static GitLab [job3226701](https://gitlab.youdo.sg/youdo/youdo.static/-/jobs/3226701) SUCCESS149.517278s; Nomadyoudo-static-test5 running, deploymente03c9269-1142-ab6a-2af2-c51035441ea3 successful, taskrunning/failedfalse/restarts0. PostupdateTASKAuthandgetcookies encountered HTTP-1 requesttimeout against test5.youdo.sg/api/users/signin/. This is a postdeploy stand authorization request failure, not oldBuildAPI404 or MessageBusstartup failure. Detailed cause of endpoint timeout remains unverified. No fixes/retries made during read-only status check.

Exactfailedplaybook identified as playbooks/deploy/venus/reindex.yml (Suggestions reindex); Authandgetcookies timedout twice, initial attemptandretry. No separate Updatebuildsinfo failure observed; earlier genericPostupdatelabel describes Jenkinsstage, not thatbranch.
