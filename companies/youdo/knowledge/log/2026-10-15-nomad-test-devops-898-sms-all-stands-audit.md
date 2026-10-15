---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [sms, release, audit]
---
# DevOps-898 SMS all-stand release audit

## Task

Verify SMS on all stands. User requires latest release versions only. No deployment requested or authorized by this verification task.

## Context

DevOps-898; active C2C test/test1–test7 and B2B test10–test15. test8/test9 remain excluded from rollout scope but were inspected too. SMS uses generated master-N release images; semantic1.0.0 is historical and was explicitly rejected by the user in the earlier SMS task.

## Actions

Read-only GitLab, Nomad and Consul GET requests through local helper `/home/slnnk/ai-data/jenkins-recovery/verify-sms-all-stands898.py`. Network sandbox required approved escalation. Sanitized results: `/home/slnnk/ai-data/jenkins-recovery/sms-all-stands898-status.json`. Last check2026-10-15T18:28:22Z.

## Findings

- Latest generated release tag master-191, commit21060f765af794bbe6bd1447237cf1dbea8f94f4, equals current master. Latest master pipeline140987/IID191. Build webapp/worker/migrations jobs3228605/6/7 all success.
- Pipeline aggregate failed because deploy-monitoring3228652 has runner_system_failure; this does not change observed runtime health. No claim pipeline is green.
- test/test1–test7: all8Nomad jobs running, enabled, IMAGE_TAG master-191; all8allocations healthy. All16webapp/worker Consul service checks passing, all task restarts0. Migration tasks dead/Failedfalse, expected completion.
- test10–test15: all6SMS Nomad jobs absent (HTTP404). test8/test9 also absent and outside current rollout scope.
- No SMS delivery test performed; observed infrastructure health only.

## Changes

Local read-only audit helper and KB records only. No runtime changes, repository changes, or external writes.

## Limits

Missing B2B deployments tracked in ~/ai/TODO.md. Deploying them requires explicit authorization for the deployment and its DB effects.

## Portable lesson

none
