---
system: nomad-test
status: verified
checked: 2026-10-22
tags: [csi, vk-cloud, jenkins, incident]
---
# Nomad test1 CSI detach blocked by cloud VM error

## Task
Investigate [dynamic_deploy5895](https://build.youdo.sg/job/dynamic_deploy/5895/) and repeated CSI errors in later jobs. Read-only investigation; no infrastructure or repository edits authorized/performed.

## Context
VK test Nomad; CSI plugin `vk-csi`; Elasticsearch volume `test1-vk-csi-es`. Existing checkout `~/git/automation-test-yandex`; related [system map](../systems/nomad-test.md).

## Actions
Read Jenkins5895–5899 logs and parameters, Nomad nodes/plugins/volume details, client journal and CSI container logs over SSH, and the exact cloud server via authenticated GET. Local evidence/helper files: `~/ai-data/nomad-csi-5895/`. Delegated read-only inspection of ES claim wait code under the KB economical-tool rule.

## Findings
-5895 and5897 failed on test1 after60claim-release polls (5s delay);5898 was running at the same wait during the snapshot.5896 on test5 succeeded;5899 on test5 passed claim release and created its new disk while still running.
- `es_vk_deploy.yml:17` purges the previous ES job; line27 waits for volume404 or empty `ReadAllocs` and `WriteAllocs`. Condition is valid. No tag selection in5895 skipped job stop. Failure is before disk deletion/recreation; `no_log` hides the underlying response.
- All8Nomad clients ready; CSI8/8nodes and8/8controllers healthy. Volume retains writer `ab5d2184-fb2c-c376-a8ca-0210390d4191`, despite allocation desiredstop/clientcomplete and both tasks dead since11:54UTC.
- CSI logs repeatedly show `ControllerUnpublishVolume` failure: cloud HTTP409, `Cannot 'detach_volume' instance 372e06a4-11f1-4bc1-a693-9a6864932829 while it is in vm_state error`.
- Cloud GET confirms VM `vk-ms1-nomad-agent-test-07` (`10.18.26.21`), UUID `372e06a4-11f1-4bc1-a693-9a6864932829`, status `ERROR`, vm_state `error`, power_state1, task_state null, fault `MessagingTimeout`/500 at2026-10-22T11:38:39Z. VM remains reachable and Nomadready; cloud control-plane state is inconsistent with guest availability.
- Attached disks include root `b20c7913-2b2a-459b-8842-4f35bfd89475`, ES test2 `406a8924-7a48-4607-875a-9a0a4b1cc501`, test13 `e2230399-d012-4add-88c6-7c9eb0c63960`, and blocked test1 `584dcc6f-609a-45e6-954e-5693cbe80128`. Future detach of test2/test13 may encounter the same rejection; not demonstrated.
- Immediate cause verified: Nova error state rejects CSI disk detach, preserving the writer claim and blocking stand rebuild. Provider-side origin of `MessagingTimeout` remains unknown.

## Changes
KB evidence/system map/backlog only. No restart, reset-state, force-detach, disk deletion, deployment or Jenkins retry.

## Status and risks
2026-10-22 diagnosis complete, recovery pending. Restore cloud VM control-plane state with provider assistance or a separately reviewed approved action; then observe automatic CSI detach and verify ordinary deployment. No destructive recovery proposed. Remaining action is tracked in [central TODO](../../../../TODO.md), section nomad-test / Consul.

## Portable lesson
none

## Project-wide cloud VM audit (2026-10-22)

User requested checking all VK Cloud machines. Paginated Compute servers/detail returned40VMs in the accessible project/RegionOne:36ACTIVE and4ERROR. All4have power_state1, task_state null and fault MessagingTimeout/500. Guest/application health was not checked in this wider audit.

| VM | UUID | Fault time UTC |
| --- | --- | --- |
| vk-ms1-nomad-agent-test-07 | 372e06a4-11f1-4bc1-a693-9a6864932829 | 2026-10-22T11:38:39Z |
| vk-ms1-elastic-b2b-test01 | 24c7267a-66cc-4d0b-a10d-6cd4db25156c | 2026-10-22T11:38:45Z |
| vk-ms1-nomad-agent-test-05 | 198e36be-c539-4375-b2ca-111fa383b620 | 2026-10-22T11:41:16Z |
| vk-ms1-pg-b2b-test | 7d38b527-d082-4dc7-8711-ce2dbf8a69a3 | 2026-10-22T11:41:57Z |

Correlated faults within3minutes18seconds suggest a shared cloud control-plane incident; this is an inference, not verified provider root cause. Existing Nomad snapshot showed both affected clients ready. Provider investigation/recovery should cover all4VMs; no reset/reboot or external support message performed. Sanitized snapshot: ~/ai-data/nomad-csi-5895/all-servers.json. Remaining recovery tracked in the existing central TODO entry.
