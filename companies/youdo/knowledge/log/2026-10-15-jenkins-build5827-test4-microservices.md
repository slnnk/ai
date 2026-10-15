---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, microservices, ansible, gitlab-ci]
---
# Build5827 test4 deployment acceptance

## Summary

Jenkins dynamic_deploy5827 completed SUCCESS after54m48s for test4 (RESTORE/ELASTIC/WEB_STATIC/MICROSERVICES enabled). First microservices attempt failed, but configured retry(2) ran a second successful attempt. All eight current BuildAPI metadata/live Nomad services verified; monolith has two running allocations. Initial root interpretation that greenresult hid a finalmicroservicefailure was incorrect and corrected to the user.

## Findings

First attempt waited on the seven test4 jobs intentionally canceled with user approval during next-test5 rollout; original hang was PostgreSQL interactive pager, alreadyfixed in AnsibleMR112. Fallback attempted oldinsurance0.0.66 job2616524 (oldpipeline125382) and failed because historical image missing. This was superseded by retry(2), not a final blocker or reason to rebuild0.0.66. Second attempt launched jobs3228523-3228530; all8success, fallbackskipped, recapfailed0. Currentinsuranceversion0.0.68.

BuildAPI GET accepted all8currentmetadata/live exactjobs: docmaster757,Fns master598,insurance0.0.68,attribution1.0.22,brute1.13.20,badge21.13.5,antifraud23.8.7,escrow13.8.12. Allrunning/dependsMonolith. Receipt~/ai-data/jenkins-recovery/jenkins5827-test4-buildapi-safe.json. Monolithyoudo-test4Version0Stopfalse allocations3ce0a694/68fe92ba bothrunning (health not separately asserted).

Ignored cleanup errors remain: stopping previouslyabsentyoudo-test4 onfirstdeployment, RabbitMQqueues_nameundefined, emptynginxcachegrep→xargsrmrc123. No changes or rerun requested/performed as part of this read-only investigation.

## Evidence and limits

Authenticated Jenkins metadata/console read in-memory; no raw credential-bearing console saved. Source URL https://build.youdo.sg/job/dynamic_deploy/5827/. Current GET runtime and BuildAPI checks support finalmicroservicesacceptance. Unrelated Rabbitcleanup andnginx optionalfixes tracked centrally ifrequested.
