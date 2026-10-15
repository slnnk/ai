---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [landings, b2b, nginx, deployment, gitlab]
---
# DevOps-898 Landings master-109 B2B rollout accepted

## Task

User explicitly approved ordinary parallel Landings deployment to test10–test15 after MR19 merge and master build. Verify using GitLab and Nomad statuses only.

## Context

Project532, master pipeline141019/IID109, source0d17499bbc2557e3c15aa5b3e4e5955d9f014fb6, image master-109. MR19 adds nginx listen80 while preserving8080 and was merged after separate user authorization. [Port repair and approvals](2026-10-15-nomad-test-devops-898-landings-stand-port-fix.md). Build-web3230136 and build-api3230137 SUCCESS.

## Actions

Parent played explicitly approved ordinary jobs3230150–3230155; receipts ~/ai-data/DevOps-898/landings-build/fixed-test10-deploy.json through fixed-test15-deploy.json. Delegated read-only monitor used service-preflight.py for project532/serviceyoudo-business-landings. No retries, new builds, deployment writes, HTTP or Consul probes by the monitor. Sanitized status artifact ~/ai-data/DevOps-898/landings-fixed-rollout-status.json, checked2026-10-15 21:08:46UTC /2026-10-16 00:08:46MSK.

## Findings

All six ordinary jobs SUCCESS: test10=3230150, test11=3230151, test12=3230152, test13=3230153, test14=3230154, test15=3230155. All six Nomad jobs running, not stopped, IMAGE_TAGmaster-109; desired allocations running, deployment healthytrue, task restarts0. Fixed port mapping therefore satisfies existing Nomad health conditions. No database configured for this service.

Master pipeline141019 still running due independent production/release stages; stand acceptance does not claim their completion. Other services' acceptance is recorded separately.

## Changes

KB log, existing nomad-test map, Landings repository row and central backlog updated. No repository changes during monitoring. Earlier source change and publication approvals recorded in the linked repair log.

## Limits

Acceptance strictly follows GitLab/Nomad status scope. No application integration, external site or production/release verification claimed. Future redeployment requires the user's applicable authorization.

## Portable lesson

none
