---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [fns, preflight, gitlab]
---
# DevOps-898 Fns deployment readiness

## Task

Determine whether Fns needs changes for DevOps-898 stand deployment. User then explicitly requested deployment. Current acceptance is GitLab/Nomad job statuses only; ordinary jobs with DB recreation.

## Context

Project244, existing checkout `/home/slnnk/git/Fns`, master7e819e850f47289abd2a7eea66c46bab231d6f7f matches live master. Latest generated release master-598, pipeline140951/IID598.

## Actions

Read-only repository/CI/config/build review plus GitLab/Nomad GET preflight. Delegated multiple-file inspection per global instructions; no superpowers skills used. Evidence `/home/slnnk/ai-data/DevOps-898/fns-preflight.json`.

## Findings

- No required repository changes found. CI includes v3/.deploy-test.yml, per-stand deployment enabled, WITHOUT_DROP_DB=false. Normal VK path already proven on C2C.
- Pipeline140951 success; all4api/service/scheduler/migrations builds success. All8C2C jobs test/test1–test7 running/healthy/master-598/restarts0 at18:42UTC.
- PostgreSQL common pool is intentional for shared Fns, even on B2B stands; database fns-{{ instance }}, pre/post migrations. PostgreSQL/RabbitMQ/DocValidation addresses derive from the current datacenter/stand. Required dependencies include DocValidation, Monolith, PostgreSQL/RabbitMQ and CI OPEN_API_MASTER_TOKEN; only its location/name recorded.
- No hardcoded Yandex endpoints in stand deployment config. Legacy Consul fallback was not a demonstrated blocker and was left unchanged.
- test10–test15 Fns jobs absent; normal manual GitLab jobs3227508–3227513 available in existing pipeline140951.

## Changes

No repository changes, new branch, release or pipeline required. After explicit user deployment request, prepared receipt-backed helper `/home/slnnk/ai-data/DevOps-898/deploy-fns-stands.py launch|status` to play six normal jobs concurrently, with DB recreation and no keep-db overrides. Receipts under `fns-rollout/`.

## Limits

Final acceptance below covers GitLab/Nomad statuses only. No additional HTTP/Consul/business checks requested.

## Approved deployment result

User explicitly requested "Запусти деплой fns" after the preflight. Played six ordinary manual jobs3227508–3227513 concurrently2026-10-15 18:44:10UTC in existing pipeline140951, retaining normal DB recreation (no skip-tags override). All6jobs SUCCESS; durations88.23/69.47/80.59/79.40/80.55/81.57seconds for test10 through test15. Final status helper confirms all6Nomad jobs running/enabled, all allocations running/healthy, master-598, restarts0. Combined with C2C8status proof, all14target stands have current Fns release. No service repo edits, tags, new pipeline, branch or MR needed. Evidence `/home/slnnk/ai-data/DevOps-898/fns-rollout/status.json` and per-stand receipts.

## Portable lesson

none
