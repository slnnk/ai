---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [landings, b2b, preflight, gitlab]
---
# DevOps-898 B2B Landings readiness

## Task

User approved checking next service youdo-business-landings under DevOps-898. Remaining order Landings→Billing→MobileID→TKB→Tochka→Business. No pipeline/deployment requested in this turn, no superpowers skills used.

## Context

Project532, existing checkout `/home/slnnk/git/youdo.business.landings`, clean prepare-dev branch preserved. Read-only origin fetch confirms live master2f6e82ec9b18b9d41eeb9a556d1c005f7a7281b1. Latest generated master-104/pipeline139691 SUCCESS, build-web3187744 and build-api3187745 success. No target VK Nomad jobs. Evidence `/home/slnnk/ai-data/DevOps-898/landings-preflight.json`, checked2026-10-15T19:56:22Z.

## Actions

KB lookup, delegated multi-file source/build/CI review, GitLab/Nomad GET audit. No HTTP/Consul/integration probes, source changes, branch switches or external writes.

## Findings

- No mandatory stand configuration changes found. Only web/API workloads, no DB/migrations/RabbitMQ/Redis. API .NET8 and web nginx8080. Frontend docs use same-origin /business/api; API retains existing test S3 documents bucket. No credentials copied.
- CI uses v3per-stand and DEPLOY_PROD_MODEauto. Old pipeline139691 predates VK template adaptation; fresh master pipeline recommended. Automatic production canary/update and release included by deploy-prod-only-web; disclose before creating pipeline.
- Static build review found CI Node16.20.2 versus newer engines in lockfile (Vite/ky>=18, env-cmd>=20.10), but engine-strict=false and last two-image build succeeded on current commit. No Node/source upgrade authorized or introduced solely from that mismatch; investigate actual failure only if a fresh build fails.
- Shared .nodejs-build.yml passes the Node image/tag build arguments and repository Dockerfile consumes them. Historical successful web-job trace did not provide readable version signatures; do not claim the exact runtime version was verified from that trace. Current successful build remains sufficient reason to attempt normal fresh build before proposing optional upgrades.

## Changes

Read-only refs/status artifact and KB records only. No repository edits, pipeline creation, tags or stand deployment. Ordinary historical test10–test15 jobs3187758–3187763 remain manual but do not assume they capture merged VK template fixes.

## Limits

Historical successful builds are not a guarantee for a fresh build; mandatory source changes not demonstrated. User action required to launch fresh pipeline with automatic production/release effects, then separate approval for ordinary parallel deployment. Open work tracked centrally in ~/ai/TODO.md.

## User-approved fresh master pipeline

After automatic production canary/update/release effects disclosed, user requested "Сделай". Created exactly one pipeline141007/IID105 at2026-10-15 19:58:41UTC on master2f6e82ec9b18b9d41eeb9a556d1c005f7a7281b1. [Pipeline](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/pipelines/141007). Helper `/home/slnnk/ai-data/DevOps-898/landings-pipeline.py create|status`, durable receipts in `landings-build/`.

Initial GET verified pipeline running,3preparation jobs running, build-web3229694/build-api3229695 created. Expected master-105 after builds. Production direct canary3229716/update3229717/release3229719 created; no child bridge. Ordinary test10–test15 jobs3229708–3229713 created/not played. No source edits or Node change. No claim builds/production/release completed.

## Portable lesson

none

## Subsequent build diagnosis and approved local fixes

Pipeline141007 web build3229694 failed with npm EINTEGRITY for @youdo/ui0.17.5; API3229695 succeeded, deployment/production skipped. User approved task branch and lock checksum repair, then explicitly requested the internal Node image. A second stale checksum for @youdo/eslint-config1.2.5 was verified during local validation. Both current Nexus metadata/artifact pairs agree. Local diff changes only four integrity fields and CI Node image/tag; versions unchanged. Existing internal Node24 recipe/image is already built; no base-images change required. See [build diagnosis and approval record](2026-10-15-nomad-test-devops-898-landings-build-integrity.md). User subsequently explicitly approved publication ("Подтверждаю публикацию"); reviewed two-file commit ee64ce015fce4b59a921e078019c30c596bbae85 was pushed successfully to the approved branch. [MR18](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/merge_requests/18) created; MR pipeline141016 created and checkout clean. Merge/deployment not performed. Full isolated Docker build with the actual internal Node24 base completed successfully (npm install and npm run build, exit0); CI Lint and independent four-field lockfile JSON diff also passed.
