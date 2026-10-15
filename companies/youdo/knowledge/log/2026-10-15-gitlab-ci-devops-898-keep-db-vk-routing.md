---
system: gitlab-ci
status: verified
checked: 2026-10-15
tags: [gitlab, nomad, keep-db]
---
# DevOps-898 keep-db VK routing inheritance

## Task

Fix keep-db VK routing under DevOps-898 after SMS deployment failures. User also required normal jobs with DB recreation for this stand rollout; do not choose keep-db for these deployments.

## Context

Existing checkout `/home/slnnk/git/gitlab-ci-templates`; base origin/master7bd1578. Child keep-db jobs overwrote parent ANSIBLE_ARGUMENTS, losing VK address/token. No superpowers skills used per user instruction.

## Actions

Removed18child ANSIBLE_ARGUMENTS overrides in v3/.deploy-test-per-stands.yml. All test/test1–test17 keep-db jobs now inherit VK address/token and skip-tags dropdb from the existing shared parent. Public-test overrides and ordinary/all jobs unchanged. v2 review found a distinct old scheme without this VK inheritance; no v2 adaptation added.

## Findings

Effective inheritance verified for all18jobs;22ordinary/public/all job variable sets unchanged. GitLab CI Lint in pinned SMS21060f7 context valid/no errors/no warnings (60jobs); diff check and independent read-only review passed. Evidence in `/home/slnnk/ai-data/DevOps-898/keep-db-routing/`. Runtime keep-db was not executed after this fix. New configurations consume the change after merge; existing pipelines are immutable.

## Changes

Commit126620d7100e28b34d7dae406f0e25f2464590f9, one file/18deletions. [MR91](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/91) opened to master; source DevOps-898-fix-keep-db-vk-routing, assigned user, squash/source-deletion settings preserved. GET verified title/description/source/target/SHA. Head pipeline null; project pipeline-list GET returned403 after MR creation, so publication helper exited1 despite successful creation. No duplicate write/retry, merge or deployment performed by publication.

## Training record

2026-10-15, DevOps-898. Proposed/final branch DevOps-898-fix-keep-db-vk-routing, base origin/master7bd1578. User explicitly replied "Подтверждаю ветку" before branch creation or repository edits. Commit proposed/final `preserve vk routing in keep-db jobs`; MR proposed/final `DevOps-898 preserve vk routing in keep-db jobs`. User explicitly replied "Подтверждаю публикацию" before stage/commit/push/MR creation. Actual reviewed diff only removed18redundant overrides. MR body is one Russian paragraph plus task link. Publication approval covered that sequence; merge remains pending user action. User correction: for current stand recovery use ordinary jobs, recreate databases, and accept by GitLab/Nomad status only. Earlier agent choice of keep-db was not retained.

## Limits

User subsequently reported merging MR91. GET verified merged2026-10-15 21:41:20+03:00, mergeef12833655e94738c4f416591b2906bb5d7fa386/squash0cf1dde32f3e6d7c00279fbfce798a4b8ec2fe71. CI Lint is static validation, not runtime proof of corrected keep-db jobs.

## Portable lesson

none
