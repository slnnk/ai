---
system: jenkins
status: verified
checked: 2026-10-15
tags: [broadcast, nomad-test, DevOps-899]
---

## Summary

Completed Broadcast1.2.11 deployment and live acceptance on all eight requested stands: test,test1-test7. User selected this base stand set and explicitly requested Broadcast deployment. Sequential rollout authorized; no other service deployment requested. Broadcast1.2.11 already healthy ontest5 and accepted read-only without recreating its existing database. Seven remaining manual deployment jobs are executed in order, with successful CI/Nomad/migration/BuildAPI verification before starting the next stand.

## Source and preflight

Broadcast project396, release1.2.11 and current master both SHA04291f24e8452c99ab7bedb15f346ea081e3fa36. Existing pipeline140972 has all three image builds successful, unit tests successful and integration retry3228590 successful. No rebuild, tag, branch or repository changes needed. Existing per-stand jobs use VK endpoints; no new pipeline or production deployment requested.

Job mapping: test3228251, test1=3228252, test2=3228253, test3=3228254, test4=3228255, test5=3228256(existing success), test6=3228257, test7=3228258.

## Database and runtime effects

Normal deploy jobs recreate broadcast-<stand> databases on C2C PostgreSQL5432, perform pre/post migrations and start API/scheduler. User informed of normal database recreation before launch. test5 accepted unchanged. Scheduler calls corresponding monolith API at youdo-api.<stand>.vk-test.youdo.local. Source contains no RabbitMQ runtime dependency. No PgBouncer changes or unrelated database cleanup.

## Execution and evidence

Helpers ~/ai-data/jenkins-recovery/deploy-broadcast-stands899.py inspect|step|verify and run-broadcast-stands899.py. Receipts/intent per stand and sanitized live verification in broadcast-stands-20261015/. Orchestrator starts at most one stand at a time; stops on failed CI or unsuccessful live acceptance. Initial test job3228251 launched and running. test5 already accepted.

## Validation criteria

Current Nomad job broadcast-<stand> running with expected image tag1.2.11 and CI source pipeline140972/SHA/job. Current allocation healthy, no failed tasks; both migration tasks terminated successfully with exit0. BuildAPI metadata project396 matches pipeline, tag, SHA and deploy job. Final rollout acceptance not yet established at this initial record.

## User-directed parallel continuation

First test job succeeded in84.17seconds, but postmigration was still running at initial CI-success observation; verifier correctly deferred acceptance until that task exited0. Both migrations, runtime health and BuildAPI then accepted. test1 job also succeeded.

User explicitly requested parallel deployment. Local sequential orchestrator and any remaining local step process stopped; GitLab jobs were not canceled. Current CI snapshot before batch: test/test1/test5 successful, remaining five manual. Launched only test2job3228253, test3job3228254, test4job3228255, test6job3228257, test7job3228258 with per-stand durable intent and receipt. Mutating POSTs issued sequentially, jobs execute concurrently. No duplicate plays.

Read-only watch-broadcast-parallel899.py observes all eight jobs and final live verification, with bounded waiting for lifecycle tasks that can finish after CI success. Additional helper launch-broadcast-parallel899.py records parallel-batch-launch.json. No scope expansion to other services.

## Final acceptance

All eight accepted: CI SUCCESS, version1.2.11, expected source SHA/pipeline140972/job, healthy current allocation with zero restarts and no failed tasks, all16pre/postmigration tasks exited0, BuildAPI project396 metadata matches for every stand. No manual BuildAPI writes needed. Seven new deploys performed; existing healthy test5 verified without redeploy/database recreation.

| Stand | Job | CI duration |
| --- | --- | --- |
| test |3228251|84.17s|
| test1|3228252|79.34s|
| test2|3228253|81.44s|
| test3|3228254|102.68s|
| test4|3228255|79.45s|
| test5|3228256(existing)|86.31s|
| test6|3228257|72.95s|
| test7|3228258|81.03s|

Some lifecycle postmigration tasks continued after CI success; acceptance waited for their actual termination. Final source evidence broadcast-stands-20261015/final-verification.json. Read-only watcher exited ALL_EIGHT_STANDS_ACCEPTED. No failed deployments or external retries required.

Nomad-declared route hosts observed for each stand: broadcast-api.<stand>.vk-test.youdo.local, broadcast-scheduler.<stand>.vk-test.youdo.local and alias broadcast.<stand>.vk-test.youdo.local. Added to current/service-addresses.env with observation date; runtime health verified, standalone DNS/HTTP route probing not performed. No other service deployment started.
