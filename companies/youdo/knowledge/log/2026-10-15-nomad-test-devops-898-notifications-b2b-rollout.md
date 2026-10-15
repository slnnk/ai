---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [notifications, b2b, deployment, gitlab]
---
# DevOps-898 notifications test10-test15 rollout

## Task

User explicitly confirmed parallel ordinary notifications deployment to test10–test15 after build verification, with DB recreation. Acceptance is GitLab/Nomad job statuses only. No superpowers skills used.

## Context

DevOps-898, project505, pipeline141003/source80051dad9a5cc85db9ac9d36374725642d5d6a20, master-190;3image builds and unit-tests SUCCESS. [Preflight/build record](2026-10-15-nomad-test-devops-898-notifications-preflight.md).

## Actions

Validated pinned pipeline and all6manual ordinary jobs before mutation. Played jobs3229634–3229639 concurrently2026-10-15 19:38:09UTC, no skip-tags/keep-db overrides. Helper `/home/slnnk/ai-data/DevOps-898/deploy-notifications-stands.py launch|status`, receipts/status in `youdo-notifications-rollout/`.

## Findings

All6ordinary jobs3229634–3229639 SUCCESS. Durations84.22/85.90/82.79/88.52/88.44/84.91seconds for test10 through test15. Nomad all6jobs running/enabled/master-190, allocations running/healthy, task restarts0. No retries or source changes needed. Evidence `/home/slnnk/ai-data/DevOps-898/youdo-notifications-rollout/status.json`.

## Changes

Six approved GitLab job plays only. No source edits, branches/new releases/pipelines, HTTP/Consul/integration probes or unrelated runtime changes.

## Limits

Stand acceptance completed by GitLab/Nomad statuses only. Auto-production downstream141004 last running; its final outcome not claimed from stand acceptance. Other services tracked centrally in ~/ai/TODO.md. Next proposed service after this dependency is main youdo-business.

## Remaining catalog scope

After this rollout,5per-stand catalog services completed (SMS,Fns,DocValidation,auth,notifications); doc-generator shared instance accepted earlier under DevOps-898. Remaining7services: youdo-business,youdo-business-billing-service,youdo-business-landings,youdo-business-mobile-id,youdo-business-tkb-proxy,youdo-business-tochka-proxy,youdo-kitcut. No deploy authorization inferred for the next service from proposing it.

## Portable lesson

none
