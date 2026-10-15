---
system: jenkins
status: verified
checked: 2026-10-14
tags: [jenkins, deploy, vk-test, monolith]
---
# dynamic_deploy test5 with latest published release

## Task and authorization

User requested test5 deployment: all Restore options initially enabled, deploy monolith, other deployment options disabled. After reviewing proposed parameters, user explicitly authorized launching if latest-release monolith image was published, corrected RESTORE_B2B_ELASTIC=false and SUGGESTIONS_REINDEX=true. Large/thick DB stands excluded. This approval authorized one Jenkins build, not repository edits/publication, retries or job configuration changes.

## Preflight

Read-only GitLab API scan of newest pipelines found latest pipeline containing build_release:139914, MR10093/head, pipeline success. Successful build_release job3225571 has artifacts.zip1546296527bytes expiring2026-11-13; build_docker_release3226107 success. Registry tag API confirmed all20 required monolith repositories have numeric tag139914 and digests. Receipt ~/ai-data/jenkins-recovery/test5-preflight.json stores nonsecret metadata. No artifact/image downloaded or build re-triggered by preflight.

STATIC_PIPELINE_ID139593 retained from last successful dynamic_deploy5818; metadata contains successful build_ssr and is required even WEB_STATIC=false. Last successful deployment was test7, so this is a metadata-compatible static fallback, not independently verified current test5 static version. Static deployment disabled.

## Applied parameters

TEST_INSTANCE=test5; MONOLITH_PIPELINE_ID=139914; STATIC_PIPELINE_ID=139593; AUTOMATION_BRANCH=master; BRANCH=gitlab. RESTORE/REDIS/RABBIT/ELASTIC/S3/NGINX/SUGGESTIONS_REINDEX=true; RESTORE_B2B_ELASTIC/WEB_STATIC/MICROSERVICES=false. Deploy monolith, Stop service and Update buildsinfo are unconditional Pipeline stages.

## Actions and result

Existing job queue/running preflight clear. POST buildWithParameters returned201, queue19128; queued2026-10-14T20:56:51UTC. Jenkins [build5819](https://build.youdo.sg/job/dynamic_deploy/5819/) completed FAILURE in71719ms. Fresh API read verified every submitted parameter matches the build. Stage wfapi endpoint returned404. Console reviewed with secrets suppressed. Checkout was master9ad35fb8206427a5ebfbdd453f659c2e7d0aa254. No automatic retry or infrastructure correction performed.

## Changed files and validation

Local helper ~/ai-data/jenkins-recovery/deploy-test5.py supports discover/preflight/launch/status and refuses duplicate launch when receipt exists. Nonsecret launch/result receipt ~/ai-data/jenkins-recovery/test5-deploy-receipt.json. No repository files or Git state changed. Knowledge notes updated and lint/index checks run after diagnosis.

## Risks and limits

Full Restore/deployment acceptance not achieved. Exact failed step and effects of preceding stages must be determined from console. Existing recovery/hardening issues remain outside this minimal VK run.

## Root cause (diagnosed after midnight, 2026-10-15 MSK)

Restore PG DB failed on test5_postgres with Host key verification failed before database reset could run. Clear Nginx cache failed on test5_lb10.18.20.97: SSH root access denied (publickey,password). Rabbit API http://rabbitmq.service.vk-test.consul:15672/api/queues/test5 returned401/not_authorized/Login failed; ignore_errors masked this, followed by queues_name parsing/undefined errors. These are VK access/trust/credential problems, not stale yandex-test addresses in Restore. Precise credential correction and SSH trust enrollment are not authorized by the one-build approval.

Stop service found no youdo-test5 Nomad job; handled/ignored. Parallel Restore continued: thin MSSQL, ES CSI reset/deployment, Redis and S3 tasks executed; final recaps still require interpretation. Monolith and static deploy and Post update (including Suggestions reindex) were skipped because of earlier failure. User-requested monolith version139914 was not deployed by this failed build.

Next minimal work: approve/perform Jenkins PostgreSQL SSH host-key enrollment based on independently verified fingerprint, correct Jenkins/root SSH access to the VK balancer, and align Rabbit API credentials with current VK broker. Then separately authorize another deployment. Existing reset logic remains unchanged.
