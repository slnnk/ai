---
system: jenkins
status: verified
checked: 2026-10-15
tags: [socket, nomad, gitlab, DevOps-899]
---
# Socket parallel rollout to eight test stands

## Summary

Socket1.2.9 parallel rollout: seven new-stand deploy jobs succeeded; repeated test5 job3229440 failed after7.07s. All eight Nomad jobs remain running, with two healthy allocations each and zero restarts. Failure reason not investigated because user limited checks to GitLab/Nomad statuses. Existing successful test5 deployment remains healthy.

## Task

User approved Socket as the next service after Landings, excluding TrackingPixel from this rollout sequence. Only GitLab and Nomad status checks requested.

## Context and actions

Project122 youdo/YouDo.Socket, existing release pipeline140976. Seven manual deploy-yandex-test jobs played; test5 previously successful job3228384 retried as3229440. Custom Ansible playbook deploy/docker/socketchat.yml manages per-stand Nomad jobs socketChat-<stand>. No repository edits or new pipeline/build.

Local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-socket-stands899.py launch|watch|status`; receipts in `/home/slnnk/ai-data/jenkins-recovery/socket-stands-20261015/`. Launch uses eight concurrent workers. Watch reads GitLab jobs and Nomad status/allocations only. No HTTP, data, logs or BuildAPI checks.

## Changed files and limits

Local operational helper/receipts and KB bookkeeping only. Existing custom deployment behavior retained; no database commands added.

## Results

| Stand | GitLab job | Status | Duration seconds | Nomad |
|---|---|---|---|---|
| test | 3228379 | success | 37.64 | running, 2healthy, 0restarts |
| test1 | 3228380 | success | 35.84 | running, 2healthy, 0restarts |
| test2 | 3228381 | success | 39.22 | running, 2healthy, 0restarts |
| test3 | 3228382 | success | 36.99 | running, 2healthy, 0restarts |
| test4 | 3228383 | success | 35.58 | running, 2healthy, 0restarts |
| test5 | 3229440 | failed | 7.07 | running, 2healthy, 0restarts |
| test6 | 3228385 | success | 36.78 | running, 2healthy, 0restarts |
| test7 | 3228386 | success | 33.79 | running, 2healthy, 0restarts |

No automatic retry performed. New pipeline or repository changes were not needed.

## User-requested failure diagnosis and retry

User explicitly requested failure cause after the initial status-only check. Job3229440 failed in `Run nomad task` because Nomad CLI returned `Error fetching deployment`, rc1, after successful evaluation930d3cfc and deployment2a203ce0 created allocations5b8c15fb/aa39b5df. Both were subsequently running/healthy0restarts. Earlier description of an unchanged previous test5 runtime was inaccurate: the deployment submitted and created these new allocations, but CLI monitoring failed. Full trace processed in memory; no credentials copied.

User explicitly requested restarting Socket test5; retried failed job as3229442. Existing receipt updated preserving prior job ID. No repository changes.

## Retry accepted

User-requested test5 retry3229442 succeeded in32.88s; both new allocationsdc5c1f50/fa65fc07 running/healthy0restarts. All eight GitLab jobs now successful and all16current allocations healthy/zero restarts. Final receipts supersede initial failed test5 attempt; no code/config edits.
