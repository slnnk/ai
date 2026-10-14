---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, elasticsearch, vk-cloud, ansible, csi, DevOps-894]
---
# DevOps-894 full Ansible reset cycle for test thick ES

## Summary
Full reset exposed asynchronous CSI disk deletion and creation races. The latest full run failed at deployment after 145.559 seconds; it must not be recorded as a successful full cycle. User requested manual cleanup before subsequent repeatability runs.

## Task
Run the complete deployment cycle for test/thick through the prepared Ansible playbook. User then requested waiting for volume claims after job deletion, followed by manual deletion of the test job/disk and explicit force permission for terminal claims.

## Context
Repository automation-test-yandex, approved local branch DevOps-894-deploy-elasticsearch-on-vk; Nomad 10.18.26.11:4646/default, plugin vk-csi. Deployment remains Nomad-only. Prepared seed disks and snapshots are retained.

## Actions
Ran the full Ansible lifecycle. First failure after 138.022 seconds reused the deleting disk because CSI create is idempotent by name. Added a Nomad external-volume absence wait before replacement creation and orphan-registration cleanup. Latest full run failed after 145.559 seconds because attachment was requested while disk e963460d-a6f2-42f2-8fc8-42f502b9e417 was still creating. A follow-up stop/run attempt was interrupted on user instruction before deployment. Manual cleanup helper purged elasticsearch-test. A failed allocation 90821988-d3c8-07c2-e7df-d43d90aba2d3 still held a write claim; user explicitly authorized force removal. Force deregistration dropped terminal claims; the same backing disk was registered without stale claims solely for CSI deletion.

## Findings
ReadAllocs and WriteAllocs are Nomad claims, which can remain after a failed allocation and job purge. Force deregistration drops terminal claims and does not itself delete the cloud disk. Disk creation readiness remains an unresolved full-cycle issue; the previously successful stop/run pilot does not demonstrate full reset repeatability.

## Changes
Added bounded ReadAllocs/WriteAllocs-empty wait after stop_es and before remove_disk, shared by those tags. Removed force from the deployment playbook; force is restricted to explicitly authorized manual cleanup. Updated inventories/vk_es/README.md. Syntax-check passed. Local helper: ai-data/devops-894-playbooks/cleanup_test_es.py --force. No Git publication.

## Open items
Repeatability runs and deployment readiness behavior remain tracked in ~/ai/TODO.md; Manual force cleanup completed: GET confirms job and Nomad volume absent, and CSI external-volume listing confirms backing disk e963460d-a6f2-42f2-8fc8-42f502b9e417 absent. No repeat deployments were started after the user requested cleanup.

## Portable lesson
none

## Repeat run after manual cleanup
User authorized another full playbook run. It failed with exit2/failed1 after125.805s. New40GiB disk942a91e9-d525-4df9-8297-2c16ee8b47e0 was created; job was submitted and remains present. Failed allocationbd7bd7e0-a817-a3b3-6e4a-2ca1716f2010 reports Cinder creating status at attach; replacementab7bdddf-f4a9-6835-24cf-5313f77e5d84 was pending when read. No automatic cleanup or further deployment was performed.

User asked whether CSI readiness can be polled before job submission. Actual Nomad data reports Schedulable=true, controllers/nodes healthy8/8, provider IsAbnormal=false and Status empty; these do not prove Cinder available. Verified v1.34.1 driver ListVolumes implementation returns ID/capacity/attachments without volume condition; CreateVolume returns without waiting for available. Plugin health is separate from individual disk readiness. Reliable readiness polling through the current Nomad/plugin API is unavailable. Alternatives are direct Cinder status polling (changes the Nomad-only requirement) or modifying the plugin to wait internally for available. Neither was implemented or authorized here.

Sources: https://github.com/kubernetes/cloud-provider-openstack/blob/v1.34.1/pkg/csi/cinder/controllerserver.go and https://developer.hashicorp.com/nomad/api-docs/volumes.
