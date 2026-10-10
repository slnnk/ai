---
system: yandex-cloud
status: verified
checked: 2026-10-10
tags: [yandex-cloud, mssql, recovery, quota]
---
# DevOps-889: zone-a Compute quotas block MSSQL recovery

## Summary
Historical early-day zonal diagnosis: CPU/SSD quota blocked the temporary base. The user later supplied explicit SSD failure at 23:45:20 and requested HDD; four local disk-type entries were switched. Latest free zone-a resources are 30 vCPU, 430 GiB RAM and 595 GiB HDD, sufficient for the base. Final three stands need HDD absolute limit at least 1705 GiB (current 1100 GiB); propose 2000 GiB for MSSQL with separate ES budget. See the [HDD selection update](2026-10-10-yandex-cloud-devops-889-mssql-hdd-disk-selection.md). Earlier limits and SSD inference below are historical; later user trace explicitly confirms SSD. No quota request was sent by the agent.

## Task
Resume [DevOps-889](https://youtrack.youdo.com/youtrack/issue/DevOps-889/Recovery-Vosstanovit-VM-MSSQL-s-bolshoi-BD), diagnose the reported step_1 quota failure and calculate quota requirements for the existing seven-stage workflow.

## Context
Local minimal Ansible adaptation and approvals are recorded in the [recovery plan](2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md). Cloud b1g8s9lk6hktue4a48mg; target folder test-platform-folder b1gra6b6tvv67paql8hs; target zone ru-central1-a. Yesterday's aggregate headroom calculation is superseded by the zonal limits below. The approved target image copy remains distinct from this runtime attempt.

## Actions
- User ran step_1 and reported a quota failure; this does not demonstrate successful VM creation.
- Read-only quota-manager query: `yc quota-manager quota-limit list --resource-id b1g8s9lk6hktue4a48mg --resource-type resource-manager.cloud --service compute`.
- Calculated current headroom and required absolute limits; no external mutation or repository change was performed by the agent.

## Findings
| ru-central1-a resource | Limit | Usage | Free | Base requires | Final three require | Minimum absolute limit | Proposed limit |
|---|---:|---:|---:|---:|---:|---:|---:|
| vCPU | 237 | 234 | 3 | 4 | 12 | 246 | 260 |
| RAM, GiB | 988 | 978 | 10 | 8 | 24 | 1002 | 1024 |
| network-ssd, GiB | 2116 | 2115 | 1 | 400 | 1200 | 3315 | 3500 |

Exact zonal quota IDs: `compute.instanceCores.count.ru-central1-a`, `compute.instanceMemory.size.ru-central1-a`, `compute.ssdDisks.size.ru-central1-a`.

The base is deleted before final VM creation, so capacity does not require adding both stages together. Proposed limits provide 26 vCPU, 46 GiB RAM and 1385 GiB SSD headroom at this baseline; quotas are shared and must be rechecked before retry.

Image quota `compute.images.size` is now 2147483648000 bytes limit / 1492526301184 bytes usage (2000 / 1390.0234375 GiB), sufficient for the existing replacement workflow. Counts have headroom: instances 72/100, disks 154/170, images 14/32. An image quota request is unnecessary for this selected route.

## Changes
Created this log and updated the prior recovery summary, existing Yandex test infrastructure map and single TODO list to reflect the zonal blocker. No repository files were changed; no quota request was submitted.

## Risks and limits
Quota headroom is a point-in-time cloud observation, not reserved capacity or proof of zone capacity. Other work can consume it. User approval is required before a quota request and before each subsequent reviewed runtime action. Recheck whether step_1 left any resource before retry; the quota error alone does not establish resource absence.

## Portable lesson
none

## User quota request verified (2026-10-10)

Read-only quota-request list confirms user request `atd5luhfrd8phca3a4qv`, created at 16:22:45 Europe/Moscow (13:22:45 UTC), status `PENDING`. Requested zone-a limits: 260 vCPU, 1024 GiB RAM, 3500 GiB SSD; all three entries `PROCESSING`. A fresh quota-limit list confirms effective limits remain 237 vCPU, 988 GiB RAM and 2116 GiB SSD, with usage 234, 978 GiB and 2115 GiB respectively. Recovery remains blocked pending approval/application. The agent made no external changes.
