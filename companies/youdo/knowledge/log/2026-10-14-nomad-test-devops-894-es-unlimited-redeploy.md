---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [ansible, elasticsearch, registry, DevOps-894]
---
# DevOps-894 simultaneous ES redeployment with internal registry images

## Summary
All13ESstands test1–test7/test10–test15 now use internal registry ES6.8.23/head images. User explicitly requested simultaneous full redeployment with no worker cap. Initial13concurrent full resets finished159.555s:11passed, test2/test4missed healthy_deadline. Simultaneous stop_es,run_es retries preserved their new disks and succeeded59.892/61.107s. Final13/13Nomad deployment successes, image references verified via GET job configs.

## Task
Redeploy all13previously selected stands at once with the new internal images. User subsequently asked if download latency caused the health deadline failures.

## Context
Existing approved DevOps-894 automation branch and local template changes. ES/head images published by merged base-images MR40 and successful tag builds140808/140809. test1/test6thick, other11thin. Cinder readiness polling and release/deletion synchronization remain enabled.

## Actions
Removed the local batch helper's1–4worker limit; --workers0 starts one worker per stand. Saved prior logs/results under ai-data/devops-894-playbooks/before-internal-images-batch. Executed the full actual Ansible entrypoint for all13stands concurrently. Read-only Nomad diagnostics for failed deadlines. Simultaneously retried test2/test4with stop_es,run_es; no manual force or disk recreation on retry. Saved initial failed logs and results. GET each of13job configs confirms elastic and elastic_head exactly match registry.youdo.sg/youdo/base-images/elasticsearch:6.8.23 and registry.youdo.sg/youdo/base-images/elasticsearch-head:sha-1a888b928135. No ES HTTP/index checks or Git publication.

## Findings
The failing allocations9c515c7f-5599-bd30-0e79-8825fa8b0bc9(test2) and3585321a-f9d7-94e0-dfe1-e5c8f369cc5e(test4) were running but marked unhealthy at60.02s. test2Received0.02s→TaskSetup35.51s→Started35.84/35.89s. test4Received0.02s→TaskSetup42.95s→Started43.25/43.30s. No Downloading image events were recorded; setup-to-container-start only0.3–0.4s. Main delay was before task setup, not image loading during Docker start. CSI/allocation pre-run is a possible contributor, but its exact attribution has not been established from node logs. TCP EScheck interval10s/timeout2s plus default min_healthy_time10s must fit healthy_deadline1m; available evidence proves deadline exhaustion but does not measure the first passing TCP check. Container running alone does not prove readiness. Repeated stop/run succeeded after the main batch.

Actual original seconds by stand:
- test1 thick: 91.7s, exit0
- test2 thin: 154.632s, exit2
- test3 thin: 74.377s, exit0
- test4 thin: 159.55s, exit2
- test5 thin: 74.373s, exit0
- test6 thick: 107.7s, exit0
- test7 thin: 69.35s, exit0
- test10 thin: 87.624s, exit0
- test11 thin: 77.438s, exit0
- test12 thin: 78.563s, exit0
- test13 thin: 85.173s, exit0
- test14 thin: 90.513s, exit0
- test15 thin: 75.281s, exit0

## Changes
Remote13stand jobs/disks were recreated under user authorization. Two failed-deadline jobs then restarted on retained disks. Local batch helper generalized for all-at-once mode; templates were already prepared. All configured service addresses unchanged. Original successful stand test was outside this13stand batch and not redeployed.

## Open items
Automation Git publication remains in ~/ai/TODO.md. Healthy deadline adjustment is a proposal requiring a separate user request, not implemented. No more deployment runs pending.

## Portable lesson
none

## Approved deadline adjustment
User explicitly selected healthy_deadline2m and progress_deadline3m (instead of the proposed3m/5m). Changed only these values in es_thin.j2 and es_thick.j2. Existing TCP checks and min_healthy_time retained. Nomad template parsing and git diff --check passed. Local changes only; no new redeployment or Git publication authorized/performed. Existing running jobs retain previous deadlines until their next deployment.
