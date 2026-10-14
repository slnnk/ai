---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [ansible, elasticsearch, DevOps-894]
---
# DevOps-894 simultaneous deployment of all14ESstands with2m/3mdeadlines

## Summary
All14requested ESstands deployed successfully in one concurrent batch121.790seconds, without retry deployments. Updated healthy_deadline2m/progress_deadline3m and internal registry ES/head images applied through the actual Ansible playbook.

## Task
User explicitly requested another simultaneous deployment of all previous13stands plus test.

## Context
Approved local DevOps-894 automation branch, Nomad vk-test/default, vk-csi; previous13stand run required two retries with1mdeadline. User selected2mhealthy/3mprogress values in thin/thick templates. Current request authorized runtime rollout of those values. Base mirror images released via MR40 and tags.

## Actions
Extended local run_es_batch.py to accept stand test as well as test<number> and sort its result. Saved previous logs/results under ai-data/devops-894-playbooks/before-deadline-2m-3m-batch. Ran --instances test test1 test2 test3 test4 test5 test6 test7 test10 test11 test12 test13 test14 test15 --workers0. All14full Ansible lifecycle executions started together; each stopped its job, waited for claims, deleted/recreated its disk from the prepared snapshot, waited for Cinder available and completed blocking nomad job run successfully. No manual force, retry deployment, separate ES checks or Git publication.

## Findings
Exit0for all14, total121.790s. Thick40GiB: test92.039s, test1 121.786s, test6 104.936s. Thin5GiB: test2 81.100s, test3 75.479s, test4 71.229s, test5 87.916s, test7 93.579s, test10 70.474s, test11 86.592s, test12 81.680s, test13 82.521s, test14 77.519s, test15 65.143s. No healthy-deadline misses in this run; a single successful batch is not proof that all future runs fit these deadlines.

## Changes
All14stand jobs and data disks recreated under explicit authorization. Deadlines2m/3m and internal ES/head references now deployed through prepared templates. Service addresses unchanged. Batch results/logs remain in ai-data/devops-894-playbooks. Repository modifications remain unpublished on the approved DevOps-894 branch.

## Open items
Automation Git publication, DBA_Clean/AWX migration tracked in ~/ai/TODO.md. No pending execution for this request.

## Portable lesson
none
