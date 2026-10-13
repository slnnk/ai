---
system: gitlab
status: verified
checked: 2026-10-13
tags: [gitlab, registry, runner, incident]
---
# Extraform missing Python UV images and disabled project runners

## Task

Diagnose [extraform pipeline 136592](https://gitlab.youdo.sg/data/extraform/-/pipelines/136592) and the screenshot of pending `data/dockers` job 3222108. Initial read-only diagnosis; subsequent user request authorized updating the existing recovery task comment. No agent infrastructure changes were authorized. The user explicitly excluded superpowers skills.

## Context

- GitLab projects: `data/extraform` ID291 and `data/dockers` ID215.
- Registry recovery excludes historical payloads; see [GitLab system map](../systems/gitlab.md).
- Existing API access: `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env`; token values were not logged.

## Actions

Inspected authenticated GET API responses and the failing job trace. Key API routes, relative to `/api/v4`:

```text
GET /projects/291/pipelines/136592
GET /projects/291/pipelines/136592/jobs
GET /projects/291/jobs/3222107/trace
GET /projects/215
GET /projects/215/jobs/3222108
GET /projects/215/runners
GET /projects/215/registry/repositories/425/tags
GET /runners/105
GET /runners/106
```

## Findings

- Extraform pipeline136592, ref `0.31.17`, SHA `3c04a38b`, originally succeeded on August11, including production deploy job3059803. Retried build3222107 on October13 fails at Dockerfile line22: `FROM registry.youdo.sg/data/dockers/python-uv:3.12-base` reports not found. Missing latest cache is an additional nonfatal message.
- `data/dockers` registry repository425 (`python-uv`) has no tags (`[]`). The required base image has not been recovered.
- `build-python-uv` job3222108 is pending, runner null, tags `[dind]`, ref `master`, pipeline119327. Its SHA `db897a772474e00993843e7d33b8b8ab9aac1875` belongs to the historic pipeline created2025-04-22.
- Project215 has `shared_runners_enabled=false` and `group_runners_enabled=true`; its eligible runners endpoint returns `[]`.
- Instance runners105/106 are online, unpaused, `access_level=not_protected`; tags include `docker`, `dind`, and respectively `gitlab-runner-docker-1`/`gitlab-runner-docker-2`. They satisfy the job tag but are excluded by the project's disabled instance/shared runners setting. Extraform has shared runners enabled.

## Changes

Initial diagnosis changed only local knowledge bookkeeping. In the follow-up, the user reported enabling instance runners in `data/dockers` and that the build was running; build completion and tag publication were not independently verified.

The user explicitly requested adding `data/dockers` to the existing base-image task comment and separately recording extraform as a periodic/cron Nomad workload, plus a plan to inventory all Nomad periodic jobs and rebuild their images. After approval, the existing DevOps-891 comment `74-124638` was updated by POST and independently GET-verified against the exact prepared text. Added the Python base-image repository bullet and recovery-plan point8: inventory periodic jobs/repositories/images, rebuild all used images in dependency order, verify tags; extraform depends on `python-uv:3.12-base`/`3.12-builder`. This plan authorizes neither deployment nor running Nomad jobs.

Local script: `/home/slnnk/ai-data/gitlab-recovery/update_extraform_comment.py`; snapshots/payloads: `devops-891-before-extraform-comment.json` and `devops-891-extraform-comment.json` in the same directory. No repository changes, agent runner-settings changes, CI retries, deployment, or Nomad launches were performed. Local bookkeeping updated this log, the existing GitLab system map, `~/ai/TODO.md`, generated indexes and `.sync-notes`.

## Risks and resolution

Instance/shared runners enabled by the user (user-reported). Verify the running job publishes `python-uv:3.12-base` and `python-uv:3.12-builder` before retrying extraform build. Job success and image publication remain unverified; registry recovery is incomplete for this previously uninspected project. Retrying the entire historic extraform pipeline may execute deployment jobs, so scope any retry approval to the required build job.

## Portable lesson

none
