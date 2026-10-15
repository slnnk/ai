---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [kitcut, b2b, preflight, gitlab]
---
# DevOps-898 Kitcut readiness and requested rollout order

## Task

User selected remaining service order7,3,2,4,5,6,1: Kitcut,Landings,Billing,MobileID,TKB,Tochka,Business. Continue with Kitcut readiness under DevOps-898. Existing requirement: ordinary jobs and DB recreation for all stands, latest release versions, final GitLab/Nomad statuses only. No superpowers skills used.

## Context

Project513, existing checkout `/home/slnnk/git/youdo.kitcut`, clean DevOps-689-k8s preserved; read-only fetch, authoritative mastere3ac817c390f853639acfe0cd43e92415fe45a4f. Latest generated master-102/pipeline139611 successful,3api/web/migrations builds success. All target VK Nomad jobs absent. Evidence `/home/slnnk/ai-data/DevOps-898/kitcut-preflight.json`, checked2026-10-15T19:42:12Z.

## Actions

KB lookup, delegated multi-file config/build/CI review, GitLab/Nomad GET audit. No source edits, branch switches, pipeline creation, tag, deployment or external write yet.

## Findings

- CI uses .NET8/v3per-stand/DEPLOY_PROD_MODEauto, so generated master-N is the correct release convention, not manual semantic tags. New master pipeline includes automatic production child with web/migrations.
- No mandatory VK address adaptation found: B2B PostgreSQL/auto per-stand DB, PG5432, dynamic Redis stand address/port, pre/post migrations. External AppMetrica redirect is intentional, not old infrastructure routing.
- devops/config.yml:6 sets recreate_db="false". Initial agent proposal to change it to true was rejected by user; that proposal was unnecessary for first deployment. Ansible Create postgres db if not exist at deploy_microservices.yml155–161 has only db_type=pgsql condition, no recreate_db dependency: SELECT existence then CREATE DATABASE when absent. Drop/recreate and template-clone tasks require recreate_db==true. Pre/post migrations remain enabled independently in Nomad template; API/web use the same auto-named DB.
- No service repository changes needed. Old pipeline139611 predates VK template adaptation; new master pipeline recommended with automatic production effects disclosed before launch. No job plays authorized by order correction alone.

## Changes

KB readiness/order record only. Proposed branch DevOps-898-recreate-kitcut-test-db from origin/mastere3ac817c was explicitly rejected by user. No branch created and no files edited. User correction: absent DB should be created by Ansible; verified this behavior and withdrew the proposed recreate_db change. This is not approval for branch/edit/publication.

## Limits

Open work tracked centrally in ~/ai/TODO.md. Keep Kitcut recreate_db=false; ordinary job selection does not imply changing service-specific reset behavior. SQL/config inspection verifies the create-if-absent path, not actual remote DB creation or migration success. Historical successful builds do not prove a fresh build/runtime readiness.

## User-approved fresh master pipeline

After the unnecessary config change was withdrawn and fresh pipeline proposed, user requested "Делай". Created exactly one master pipeline141005/IID103 on e3ac817c390f853639acfe0cd43e92415fe45a4f at2026-10-15 19:47:24UTC, with disclosed automatic production deployment/migration effects. [Pipeline](https://gitlab.youdo.sg/youdo/microservices/youdo.kitcut/-/pipelines/141005). Helper `/home/slnnk/ai-data/DevOps-898/kitcut-pipeline.py create|status`, receipts in `kitcut-build/`.

GET verified pipeline running, set-variables/set-variables-nomad SUCCESS; prepare-nuget3229654/build-monitoring3229656 running. API3229657/web3229658/migrations3229659/tests3229660 created, production bridge created/no downstream yet. Expected master-103 after builds. Ordinary test10–test15 jobs3229673–3229678 created/not played. Config recreate_db=false preserved, no branch/source edits. No claim builds/tests/deployment/release completed.

User reported build completed; GET confirms API/web/migrations/monitoring builds and unit-tests all SUCCESS. Parent141005 running, auto-production downstream141006 running, release/monitoring deployment created. Ordinary test10–test15 jobs3229673–3229678 manual/ready. Prepared `/home/slnnk/ai-data/DevOps-898/deploy-kitcut-stands.py launch|status`, pinned pipeline141005/master-103/sourcee3ac817c; ordinary jobs retain recreate_db=false (create absent DB, preserve existing DB), not forced reset. No job plays executed. Await stand deployment approval.

Subsequent user-approved ordinary parallel deployment completed: jobs3229673–3229678 all SUCCESS/Nomad running/healthy/master-103/restarts0; recreate_db=false preserved. [Final acceptance](2026-10-15-nomad-test-devops-898-kitcut-b2b-rollout.md).

## Portable lesson

none
