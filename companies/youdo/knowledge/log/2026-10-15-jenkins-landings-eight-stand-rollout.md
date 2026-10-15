---
system: jenkins
status: verified
checked: 2026-10-15
tags: [landings, nomad, gitlab, DevOps-899]
---
# Landings parallel rollout to eight test stands

## Summary

Landings1.3.35 deployed in parallel to test and test1-test7. All8GitLab jobs succeeded (22-41seconds); all8Nomad jobs running with healthy allocations and zero restarts. Verification limited to GitLab/Nomad status as explicitly requested.

## Task

User requested the next per-stand service rollout in parallel, authorizing all eight Landings deploy-yandex-test jobs.

## Context

Project485 youdo/youdo.landings, existing release1.3.35 pipeline140974, source85cf14d1ff958e18ae3aa6927c9773c410b587de. Existing test5 deployment repeated. No repository changes or new build required; release configuration recreate_db=false.

## Actions and evidence

Used local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-landings-stands899.py launch` with eight concurrent workers; seven manual jobs played and successful test5 job retried. Followed with `watch` for GitLab statuses and Nomad jobs `youdo-front-landings-<stand>`. Receipts/status files stored under `/home/slnnk/ai-data/jenkins-recovery/landings-stands-20261015/`.

| Stand | GitLab job | Status | Duration seconds |
|---|---|---|---|
| test | 3228315 | success | 21.72 |
| test1 | 3228316 | success | 40.74 |
| test2 | 3228317 | success | 40.25 |
| test3 | 3228318 | success | 39.68 |
| test4 | 3228319 | success | 22.18 |
| test5 | 3229437 | success | 37.73 |
| test6 | 3228321 | success | 38.69 |
| test7 | 3228322 | success | 38.73 |

## Findings and limits

All eight accepted from GitLab/Nomad statuses. No logs, HTTP/DNS, application behavior or BuildAPI checks added. Existing webEx_check=false means healthy Nomad deployment status does not constitute an application HTTP test.

## Changed files

Only local operational helper/receipts and KB bookkeeping; no repository or infrastructure configuration edits.
