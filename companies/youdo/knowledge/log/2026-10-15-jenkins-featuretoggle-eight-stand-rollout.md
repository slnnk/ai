---
system: jenkins
status: verified
checked: 2026-10-15
tags: [featuretoggle, nomad-test, DevOps-899]
---

## Summary

Completed FeatureToggle1.0.11 parallel deployment on all eight stands: test,test1-test7. User requested this deployment. User then explicitly narrowed validation: no additional checks, just launch deploy-yandex-test jobs and afterwards check GitLab and Nomad statuses. No DB fingerprints, data API calls, BuildAPI validation or additional tests performed.

## Source and launch

Existing FeatureToggle1.0.11 release and current master SHA2d8d1419be70266da8f2c64f2d659f99f0a7f1d2, project258, pipeline140973. Existing two image builds and unit tests successful; no new build/release/repository changes needed. Source devops/config.yml has recreate_db=false, preserving existing configured stand databases; no skip-tag override needed or passed. The earlier suggestion of before/after data checks was dropped after user correction.

Launched seven manual jobs and retried previous successful test5 job to deploy all eight targets. Jobs: test3228285,test1=3228286,test2=3228287,test3=3228288,test4=3228289,test5=3229418(retry of3228290),test6=3228291,test7=3228292. POST calls sequential, jobs execute concurrently. All eight observed running initially.

## Evidence and verification scope

~/ai-data/jenkins-recovery/deploy-featuretoggle-stands899.py launch|watch|status; durable per-stand intents/receipts and job-status.json/nomad-status.json in featuretoggle-stands-20261015/. Read-only watcher polls only GitLab job statuses and current Nomad job/allocation status. Nomad acceptance requires running job and healthy current allocation. No trace reads or migration-log audits requested.

## Risks and limits

Existing DB seed/auth setup retained; no PostgreSQL/PgBouncer changes. Preservation follows release configuration, not independent table-hash verification. Data API and BuildAPI correctness are outside this run's explicitly limited checks. No other service deploy started.

## Final GitLab/Nomad status acceptance

All eight jobs SUCCESS; all eight current Nomad jobs running/not stopped, allocations healthy with zero restarts. Watcher exited ALL_EIGHT_STANDS_ACCEPTED. Durations38.96–55.59seconds. No further service checks performed.

| Stand | Job | Duration |
| --- | --- | --- |
| test | 3228285 | 41.32s |
| test1 | 3228286 | 40.98s |
| test2 | 3228287 | 55.59s |
| test3 | 3228288 | 38.96s |
| test4 | 3228289 | 46.93s |
| test5 | 3229418 | 40.98s |
| test6 | 3228291 | 53.35s |
| test7 | 3228292 | 41.78s |

Final evidence featuretoggle-stands-20261015/job-status.json and nomad-status.json. Existing data was kept by release recreate_db=false; no before/after data fingerprint assertion is made. No BuildAPI reads, dataAPI calls, standalone DNS/HTTP checks or migration log scans after user narrowed scope.
