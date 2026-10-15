---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, acceptance]
---
# Jenkins build5826 recovery plan reconciliation

## Summary

Read-only Jenkins API and console inspection confirms dynamic_deploy5826 SUCCESS in331603ms on test5. Restore, monolith/static deployment, buildsinfo and Suggestions reindex completed. Four ignored Ansible failures and HTTP401 remain; green status does not establish successful Rabbit cleanup. AutoTest workflow, persistent quiet hook, fresh external backups and canonical configuration remain separate recovery follow-ups.

## Task and context

User asked what remains from Jenkins recovery after https://build.youdo.sg/job/dynamic_deploy/5826/ and explicitly prohibited superpowers skills. Reconciled the original DevOps-892 plan, Jenkins map, TODO and DevOps-894 acceptance record.

## Actions and findings

Used existing deploy-test5.py Jenkins authentication helper for GET build API and consoleText. wfapi/describe returns404; console stage markers supplied stage evidence. No remote mutations, retries or builds were requested or performed.

- Build5826: building=false, result=SUCCESS, duration331603ms.
- Monolith139914, static139593, test5, automation master, BRANCH gitlab.
- RESTORE, REDIS, RABBIT, ELASTIC, S3, NGINX, WEB_STATIC and SUGGESTIONS_REINDEX true.
- RESTORE_B2B_ELASTIC and MICROSERVICES false; only their stages skipped by condition.
- Restore Elastic Indexes, Deploy monolith, Deploy static, Update buildsinfo and Suggestions reindex executed; Finished: SUCCESS.
- ANSI-stripped console has four fatal markers, four ignoring markers, HTTP401 occurrences, no nonzero failed/unreachable recap counters. Interleaved parallel task output prevents reliable attribution from nearest TASK heading; no raw responses were copied. Rabbit cleanup remains unaccepted pending targeted review.
- Build5824 Suggestions authentication timeout is superseded as a deployment blocker by this successful run; no claim about the intervening fix or root cause.
- DevOps-894 working dynamic_deploy ES runtime acceptance is satisfied for test5 by this run, in addition to previous standalone thin/thick checks.

## Changes and limits

Updated Jenkins system map and TODO with build5826 evidence. No repository, runtime or tracker changes. AutoTest checkout, quiet-hook removal, external backup recovery, canonical image/DNS configuration and deferred monitoring/publication were not executed. No fresh Nomad health, hook-presence or quiet-mode inspection was performed during this reconciliation. See [Jenkins map](../systems/jenkins.md) and [original plan](2026-10-13-jenkins-devops-892-vk-recovery-plan.md).

## Portable lesson

None.
