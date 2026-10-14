---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, elasticsearch, vk-cloud, ansible, awx, DevOps-894]
---
# DevOps-894 two-stage snapshot refresh timing

## Summary

User-requested delete_image then create_image completed successfully with permanent snapshot names. Full Ansible stage durations: delete10.391s, create17.112s, total27.503s. Both named snapshots are ready and both seed filesystems remounted. No ES validation jobs or publication metadata used.

## Task

DevOps-894: execute both AWX preparation stages in the original order and measure execution time.

## Context

User explicitly instructed both steps and timing. This approved the existing named thin/thick snapshot deletion followed by replacement creation. Execution used the local checkout and the same inventory/entrypoint/tags intended for AWX; no AWX workflow was triggered or configured. Credentials stay in process environment. Existing unrelated MSSQL edits and Git state preserved.

## Actions

Executed `python3 ~/ai-data/devops-894-playbooks/run_refresh_timed.py --apply`. The helper runs two separate ansible-playbook commands against inventories/vk_es/hosts and playbooks/deploy/docker/recreate_es_base_image.yml, first --tags delete_image, then --tags create_image, with -l vk_es. Each stage uses monotonic timing from process start through completion, including cloud authentication, SSH and API readiness waits. Stage2 would not run on stage1 failure.

UTC interval2026-10-13T21:10:09.658084Z to21:10:37.161633Z (Moscow2026-10-14 00:10:09–00:10:37). Timings measure local execution, not AWX pod startup or queue delays.

## Findings

| Stage | Tag | Seconds | Exit code | Recap |
| --- | --- | --- | --- | --- |
| 1 | delete_image | 10.391 | 0 | ok15, failed0, unreachable0 |
| 2 | create_image | 17.112 | 0 | ok19, changed4, failed0, unreachable0 |
| Total | sequential | 27.503 | 0 | both completed |

Stage1 deleted the exact vk-ms1-share-base-thin/thick snapshots and observed404. Their previously recorded IDs0d38e5f9-3c42-4923-9e29-4c50bb1de70c andef5fb5f1-c828-4605-9f1c-81022edd988b are now historical/deleted. Stage2 recreated the same permanent names from their seed disks, waited available and remounted both filesystems through fstab. Future deployments resolve the names automatically; new snapshot IDs need not be stored. No temporary ES jobs, restored clone disks, index checks, metadata publishing or snapshot retention in this run.

## Changes

Only the approved cloud snapshot deletion/recreation and temporary seed unmount/remount. No repository task edits, commit, push, stand deployment or AWX configuration. Local timing helper and nonsecret result ~/ai-data/devops-894-playbooks/run_refresh_timed.py and refresh-timing.json. Censored stage logs timed-delete_image.log and timed-create_image.log,0600.

## Limits

Prepared seed data reused; no DBA_Clean trigger or fresh transfer. AWX workflow/schedule and DAG VK destination remain separate work. Backlog is maintained in ~/ai/TODO.md.

## Portable lesson

none
