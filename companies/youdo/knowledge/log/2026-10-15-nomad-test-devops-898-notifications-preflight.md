---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [notifications, b2b, preflight, gitlab]
---
# DevOps-898 notifications deployment readiness

## Task

Check youdo-notifications as the next B2B service under DevOps-898. User agreed to readiness checking only; no pipeline/deployment requested. No superpowers skills used.

## Context

Project505, repository `/home/slnnk/git/youdo.notifications`, clean DevOps-689-k8s checkout preserved; read-only fetch confirmed current master80051dad9a5cc85db9ac9d36374725642d5d6a20. Latest generated release master-189/pipeline137494 successful, builds webapp/worker/migrations all success.

## Actions

KB lookup, delegated multi-file repository review and GitLab/Nomad GET audit. Evidence `/home/slnnk/ai-data/DevOps-898/notifications-preflight.json`, checked2026-10-15T19:29:45Z. No HTTP/Consul/business probes or mutations.

## Findings

- No mandatory service repository changes identified. CI uses v3per-stand/.NET6, ordinary DB recreation, B2B PostgreSQL/auto per-stand DB, pre/post migrations using standard image entrypoint. PostgreSQL and RabbitMQ/vhost derive from datacenter/stand; no hardcoded Yandex deploy addresses found.
- All target Nomad jobs absent. Old pipeline137494 has ordinary manual test10–test15 jobs3097557–3097562, but predates VK template adaptation. Recommend a fresh master pipeline to capture merged VK templates; do not assume old compiled jobs include current overrides.
- DEPLOY_PROD_MODE=auto and .deploy-prod-full-auto.yml enable automatic production child/release. Fresh pipeline launch needs user authorization covering these effects. No new pipeline created here.
- Worker registers existing Bitrix24/Loop/email integrations; stand config does not replace these with mocks. No calls made or credentials copied; integration credential locations remain in existing source/settings, values not recorded.

## Changes

Read-only refs, sanitized audit artifact, KB bookkeeping only. No source edits, branch changes, releases/builds/deployments or external writes.

## Limits

Historical successful builds do not prove a fresh build or runtime readiness. Next proposed action is a fresh master pipeline with disclosed auto-production/release effects, then separately approved ordinary parallel test10–test15 deployment. Open work tracked in ~/ai/TODO.md.

## User-approved master pipeline

After automatic production/release effects were disclosed, user explicitly requested "Запусти пайплайн". Created exactly one pipeline141003/IID190 at2026-10-15 19:31:13UTC, refmaster, sourceSHA80051dad9a5cc85db9ac9d36374725642d5d6a20 verified unchanged. [Pipeline](https://gitlab.youdo.sg/youdo/microservices/youdo.notifications/-/pipelines/141003). Receipt-backed helper `/home/slnnk/ai-data/DevOps-898/notifications-pipeline.py create|status`; evidence `notifications-build/`.

Initial GET: pipeline running; set-variables/prepare-nuget/set-variables-nomad SUCCESS. build-webapp3229618/build-worker3229619/build-migrations3229620/dotnet-unit-tests3229621 running; expected generated image tag master-190. Production bridge created/no downstream yet; release3229644 created. Ordinary test10–test15 jobs3229634–3229639 created and not played. No claim images/tests/production/release completed. Stand deployment still requires separate explicit approval.

User reported build completed. GET confirms all3image builds and unit-tests SUCCESS, ordinary jobs3229634–3229639 manual/ready. Parent141003 still running; auto-production downstream141004 running, release3229644 created. Prepared local receipt-backed helper `/home/slnnk/ai-data/DevOps-898/deploy-notifications-stands.py launch|status`, pinned project505/pipeline141003/master-190/source80051dad. No job plays performed. Await explicit approval for parallel ordinary deployment to test10–test15 with DB recreation.

Subsequent user-approved ordinary deployment completed all6GitLab SUCCESS/Nomad healthy/master-190/restarts0. [Final rollout](2026-10-15-nomad-test-devops-898-notifications-b2b-rollout.md).

## Portable lesson

none
