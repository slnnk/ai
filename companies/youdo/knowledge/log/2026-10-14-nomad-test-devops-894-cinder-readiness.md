---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [ansible, cinder, elasticsearch, DevOps-894]
---
# DevOps-894 Cinder readiness before Elasticsearch deployment

## Summary
User explicitly authorized direct VK Cloud readiness polling after observing creating-disk attach failures. The deployment now waits for Cinder available before submitting the Elasticsearch job; lifecycle operations remain in Nomad/CSI.

## Task
Add a disk readiness check through VK Cloud before job submission in automation-test-yandex, DevOps-894.

## Context
Approved local branch DevOps-894-deploy-elasticsearch-on-vk. Existing test/thick full cycle failed125.805s at attach while Cinder status was creating. CSI v1.34.1 does not expose per-disk readiness through Nomad. User changed the earlier Nomad-only constraint to permit the Cinder check.

## Actions
Added es_vk_wait_disk.yml: GET the registered volume from Nomad to obtain ExternalID, reuse es_vk_auth.yml for scoped Keystone authentication and regional Cinder endpoint, poll GET /volumes/<ExternalID>. Only available permits continuation. Error-prefixed statuses fail immediately; other states retry with existing60retries/5s delay and fail on exhaustion. Included this before rendering/submitting the job with create_disk and run_es tags. No cloud lifecycle changes were added.

## Findings
Actual Ansible local HTTP fixtures pass for creating→available (two reads before job submission), error (one read, no job submission), and perpetual creating (retry exhaustion, no job submission). Regression exposed that failed_when=false can suppress retry-exhaustion failure in installed Ansible; corrected to fail whenever final status is not available. Final syntax-check passes. Live execution was not performed under this change request.

## Changes
playbooks/deploy/docker/tasks/es_vk_deploy.yml, new tasks/es_vk_wait_disk.yml, inventories/vk_es/README.md. Local fixture ai-data/devops-894-playbooks/test_disk_ready.py. Deployment now requires VK_CSI_USER, VK_CSI_PASSWORD, VK_CSI_PROJECT_ID in AWX or process environment alongside Nomad credentials; credential values remain external. No staging, commit, push or MR.

## Open items
Repeat full-cycle validation and Git publication remain in ~/ai/TODO.md. Existing test job/disk from failed run remain; preparation seeds and snapshots unchanged.

## Portable lesson
none

## Approved live cleanup and deployment
User explicitly requested deleting the test job/disk first and then executing the playbook. Manual cleanup with authorized force terminal-claim removal completed: job elasticsearch-test and volume test-vk-csi-es absent; backing disk942a91e9-d525-4df9-8297-2c16ee8b47e0 absent from CSI external listing. Preparation seeds and snapshots retained.

Updated the local run_test_es.py helper to pass existing VK_CSI_USER, VK_CSI_PASSWORD, VK_CSI_PROJECT_ID environment credentials alongside Nomad/Consul credentials; no secret values persisted. Executed full Ansible deployment for instance=test, instance_type=thick. Cinder available check retried three times, then succeeded before job submission. Blocking Nomad job run completed successfully: exit0, ok20/changed1/failed0, elapsed89.680seconds. This is the first successful full create/deploy run with the readiness fix; it supersedes the earlier statement that no live run was performed. Repeated reset of an existing successful allocation is not yet validated. No ES HTTP/index checks, Git publication or second deployment were performed.

## Approved repeat reset from successful deployment
User explicitly requested another full playbook invocation for test/thick. It completed successfully in102.438seconds: exit0, ok23/changed1/failed0. The claim-release check retried twice after job purge; CSI deletion succeeded and the external-disk disappearance wait retried once. New disk creation succeeded; Cinder available polling retried three times before submitting the job. Blocking Nomad job run returned success. No manual force removal or cleanup was used in this repeat. This verifies one complete reset from the successful deployment and supersedes the earlier unverified-repeatability limitation. Two consecutive full deployments now passed:89.680s after manual cleanup and102.438s for playbook-only reset. No ES HTTP/index checks or Git publication.
