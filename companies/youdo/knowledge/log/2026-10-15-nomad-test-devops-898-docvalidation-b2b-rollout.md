---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [docvalidation, deployment, gitlab]
---
# DevOps-898 DocValidation test10-test15 rollout

## Task

User explicitly approved deployment ("Запускай") after DocValidation readiness review. Deploy latest master-757 to test10–test15 through ordinary GitLab jobs, in parallel, with DB recreation. Acceptance is GitLab and Nomad job statuses only.

## Context

Project223, existing pipeline140949, sourceb5e247c7b52c6f4b711d875ef01d2c05bc6890c6. [Preflight](2026-10-15-nomad-test-devops-898-docvalidation-preflight.md) confirmed latest build, C2C8runtime and working normal template-DB cloning. No repository changes needed.

## Actions

Validated all6manual ordinary jobs and pinned source before starting. Played jobs3227436–3227441 concurrently2026-10-15 19:04:19UTC with no keep-db/skip-tags override. Local helper `/home/slnnk/ai-data/DevOps-898/deploy-docvalidation-stands.py launch|status`; per-stand receipts/status in `docvalidation-rollout/`.

## Findings

All6ordinary jobs3227436–3227441 SUCCESS. Durations86.18/91.18/93.91/81.78/97.98/86.43seconds for test10 through test15. Final Nomad statuses all running/enabled, master-757, all allocations running/healthy. Restart counts test12=1,test14=1, other4=0; no claim of zero restarts across all6. No automatic retry or intervention. Evidence `/home/slnnk/ai-data/DevOps-898/docvalidation-rollout/status.json`. Earlier C2C8verification plus current B2B6acceptance establishes latest release on all14target stands. No HTTP/Consul or integration probes performed.

## Changes

Six explicitly approved GitLab job plays. No source edits, branch changes, new pipeline/tag, extra HTTP/Consul probes or other external actions.

## Limits

Acceptance completed by requested GitLab/Nomad statuses. Startup restart causes not investigated because final state healthy and no additional checks requested. Remaining stand service work tracked in ~/ai/TODO.md. Next proposed service: youdo-business-auth-service; no deployment authorization inferred for it.

## Portable lesson

none
