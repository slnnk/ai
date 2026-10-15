---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [sms, deployment, gitlab]
---
# DevOps-898 SMS deployment to test10-test15

## Task

User explicitly requested starting GitLab deployment of latest SMS release to test10–test15 under DevOps-898. Later user clarified acceptance uses GitLab and Nomad job statuses only; no additional Consul/HTTP checks required.

## Context

Project498, existing master pipeline140987, master-191/image source21060f765af794bbe6bd1447237cf1dbea8f94f4. All six target SMS Nomad jobs were absent before launch.

## Actions

Validated all six manual keep-db jobs and source SHA before mutation. User deployment request authorized six job plays. Launched GitLab jobs3228641–3228646 at18:29:49–18:29:50UTC. Kept existing DBs using keep-db jobs; migrations still part of deployment. Local helper `/home/slnnk/ai-data/jenkins-recovery/deploy-sms-b2b898.py inspect|launch|status`; receipts in sibling directory `sms-b2b898/`.

## Findings

All six jobs failed with script_failure after9–35seconds. Subsequent Nomad inspection still found all six target jobs absent. All traces identify `Run nomad task` submission HTTP403 Permission denied; earlier job query HTTP403 was ignored. Every recap ok15/changed4/failed1/ignored1. The create-DB-if-absent and Nomad rendering tasks were reached before failure; no DB deletion was requested. Read-only token-source diagnosis in progress; no automatic retry executed.

Read-only trace diagnosis found actual commands in keep-db job3228641 target old `http://nomad.service.yandex-test.consul:4646`, not VK. Token was present/nonempty; its value was not printed or stored. Thus VK ACL failure is not established. Hypothesis: compiled keep-db configuration in pipeline140987 predates the VK route adaptation. Do not retry these jobs unchanged. Ordinary per-stand deploy jobs3228623–3228628 remain available; their actual route must be confirmed before selecting them, and their DB recreation effects must be explicit.

Final cause supersedes the earlier compiled-config hypothesis: child keep-db jobs explicitly override ANSIBLE_ARGUMENTS with only `-D -vvv --skip-tags dropdb`, losing parent VK address/token overrides. Successful normal job3228662 trace uses VK but performs DROP DATABASE. Prepared correction: play existing normal manual jobs3228623–3228628 with job variable `ANSIBLE_SKIP_TAGS=dropdb`; normal VK overrides are retained, database drop tasks skipped, migrations still run. Local helper phase `launch-vk-keep-db` is prepared but not executed; next external action requires user approval under global AGENTS.md.

## Changes

Six approved GitLab jobs played. No repository edits or git mutations. Local helper and KB records created.

## Limits

The initial keep-db attempt failed; final ordinary deployment below succeeded. Acceptance scope per user is only GitLab and Nomad job statuses. Further external changes require explicit authorization.

## Final approved ordinary deployment

Supersedes failed keep-db outcome above. User explicitly required ordinary jobs with DB recreation and parallel execution; no ANSIBLE_SKIP_TAGS override used. Six normal jobs3228623–3228628 played concurrently2026-10-15 18:35:52UTC. All six SUCCESS, durations86.37/79.61/91.64/170.41/77.14/77.95seconds for test10 through test15. Last Nomad-only runtime verification18:39:27UTC: all6jobs running/enabled, allocations healthy, IMAGE_TAGmaster-191, all task restarts0. Existing C2C test/test1–test7 also running/healthy on same latest release. test8/test9 remain excluded. No Consul or HTTP probes used for final acceptance. Pipeline aggregate remains failed because earlier keep-db and monitoring attempts failed; final six ordinary jobs are success.

Keep-db template independently fixed/published in [MR91](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/91), pending merge; see [training record](2026-10-15-gitlab-ci-devops-898-keep-db-vk-routing.md). User's normal-job/DB recreation preference recorded for remaining DevOps-898 stand rollout.

## Portable lesson

none
