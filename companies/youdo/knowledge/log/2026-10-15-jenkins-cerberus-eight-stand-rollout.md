---
system: jenkins
status: verified
checked: 2026-10-15
tags: [cerberus, nomad, gitlab, DevOps-899]
---
# Cerberus parallel rollout to fourteen test stands

## Summary

Cerberus2 1.0.9 release rebuild pipeline140997 completed all image builds. Initial eight deployments failed due to YAML raw folding bug before DB creation. User-approved Ansible fix merged and rollout retried, expanded to test10-test15. Final outcome: all14jobs SUCCESS and all14Nomad jobs running/healthy.

## Task and authorization

User explicitly requested deploy after rebuild and then added test10-test15. Current scope test,test1-test7,test10-test15; excludes test8/test9. Parallel launch, only GitLab/Nomad status acceptance. No Cerberus CI source edits authorized in this step; user explicitly deferred switching base image refs.

## Failed initial attempt and fix

Initial deploy jobs3229493-3229500 all failed6-12s: raw YAML scalar had different indentation before psql vs following -c lines, preserving newline and executing -c as shell commands. First terminate-backend query ran; DROP/CREATE/GRANT did not run. Root acknowledged avoidable indentation mistake. User approved branch reuse, then reviewed +1/-1 publication/merge. `ae68c6230b1270f98e7567f2868087b1cf3c83a8`, [MR115](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/115), merged masterd2c5b9b603d3862a955f37c6c30fdf4e7f540609. Parsed YAML raw verified one shell command with4SQL arguments, sh-n/syntax/diff checks passed. All16unrelated MSSQL paths preserved.

## Relaunch and evidence

User-authorized repeat of eight jobs plus six new jobs. Local `/home/slnnk/ai-data/jenkins-recovery/deploy-cerberus-fourteen-stands899.py launch|watch|status` launches14concurrently. Receipts `/home/slnnk/ai-data/jenkins-recovery/cerberus-fourteen-stands-20261015/`. Earlier failed receipts retained under cerberus-stands-20261015. Watch only GitLab/Nomad statuses; no data/HTTP/BuildAPI checks. Existing recreation policy retained: create empty Cerberus_<stand>, migrations then runtime.

## Additional observation

DNS Windows172.28.0.9 returned NXDOMAIN for nomad.service.vk-test.consul while .8 returned10.18.26.11/.12/.13, including after Ansible fix. Initial ignored StopNomad error included this DNS failure; no DNS/runner settings changed. Current deployment successes show some jobs can resolve/reach Nomad, but do not certify both DNS paths.

## Final recovery and acceptance

User increased PostgreSQL and PgBouncer limits to1000 after test/test4 DB connection failures and test15 Orleans startup53300. PG restart caused five earlier successful runtimes to become dead: test1/test2/test3/test5/test12. Proposed force-reschedule withoutDB recreation was NOT executed; user explicitly requested ordinary GitLab retries with DB recreation instead. Retried as3229545-3229549. test/test4 retries3229541/3229542 and test15retry3229543 succeeded. All14current GitLab jobs now SUCCESS and Nomad jobs running/healthy. Existing allocations test6/test7 show3restarts, test11 2; current healthy, no zero-restart claim. Verification only GitLab/Nomad statuses; no HTTP/data/BuildAPI checks.

| Stand | Final job | Duration seconds | Nomad |
|---|---|---|---|
| test | 3229541 | 54.05 | running/healthy |
| test1 | 3229545 | 164.18 | running/healthy |
| test2 | 3229546 | 51.46 | running/healthy |
| test3 | 3229547 | 52.94 | running/healthy |
| test4 | 3229542 | 52.16 | running/healthy |
| test5 | 3229548 | 54.28 | running/healthy |
| test6 | 3229534 | 163.77 | running/healthy |
| test7 | 3229537 | 43.32 | running/healthy |
| test10 | 3229503 | 53.11 | running/healthy |
| test11 | 3229504 | 59.92 | running/healthy |
| test12 | 3229549 | 52.04 | running/healthy |
| test13 | 3229506 | 50.21 | running/healthy |
| test14 | 3229507 | 60.65 | running/healthy |
| test15 | 3229543 | 55.48 | running/healthy |
