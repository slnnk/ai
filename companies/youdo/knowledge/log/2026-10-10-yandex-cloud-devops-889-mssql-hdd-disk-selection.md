---
system: yandex-cloud
status: verified
checked: 2026-10-10
tags: [yandex-cloud, mssql, recovery, quota]
---
# DevOps-889: switch recovery MSSQL boot disks to HDD

## Summary
The user provided an explicit network-ssd quota failure from step_1 at 23:45:20 and requested trying MSSQL network-hdd boot disks. Four existing disk-type entries were changed locally on approved DevOps-889-recover-mssql-vms: temporary base and three final stands; all prior minimal destination edits were preserved. Syntax-check and diff --check pass. Fresh zone-a HDD headroom is 595 GiB, so the 400 GiB base fits but three final 400 GiB disks do not. Final minimum HDD limit is 1705 GiB at the current 505 GiB baseline; propose 2000 GiB for MSSQL, with ES budget separate. No runtime stage was executed by the agent.

## Task
Follow the user's explicit local disk-type change request for [DevOps-889](https://youtrack.youdo.com/youtrack/issue/DevOps-889/Recovery-Vosstanovit-VM-MSSQL-s-bolshoi-BD) after SSD quota failure.

## Context
Prior minimal folder/zone/inventory adaptation is in the [recovery plan](2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md). Earlier [zonal quota diagnosis](2026-10-10-yandex-cloud-devops-889-zonal-quota-blocker.md) remains historical; current selected disk type is HDD. Cloud b1g8s9lk6hktue4a48mg, target folder b1gra6b6tvv67paql8hs, zone ru-central1-a. The user explicitly requested HDD; runtime effects still require separate permission under global rules.

## Actions
- User supplied step_1 failure explicitly identifying SSD quota at 23:45:20 and requested trying HDD.
- Changed only four disk-type entries network-ssd to network-hdd: playbooks/roles/yandex-mssql-test/tasks/1-create-instance-for-update.yml and tasks/6-create-test-instances-from-base-image.yml.
- Preserved all prior minimal destination/inventory edits and unrelated repository state.
- Verified syntax-check and git diff --check; no git staging, commit, push or external infrastructure change.
- Read current zone-a quota usage and calculated HDD capacity for staged workflow.

## Findings
| Zone-a resource | Limit | Usage | Free |
|---|---:|---:|---:|
| network-hdd, GiB | 1100 | 505 | 595 |
| vCPU | 260 | 230 | 30 |
| RAM, GiB | 1400 | 970 | 430 |
| network-ssd, GiB | 2116 | 2095 | 21 |

Base demand is 4 vCPU, 8 GiB RAM and 400 GiB HDD: this fits current quotas. Three final stands demand 12 vCPU, 24 GiB RAM and 1200 GiB HDD after the base is deleted. CPU/RAM fit; HDD needs an absolute limit of at least 1705 GiB, 605 GiB above current 1100 GiB. Proposed 2000 GiB limit leaves 295 GiB after MSSQL allocation at this baseline; Elasticsearch disk size and budget remain unverified and must be added separately. Current headroom is shared, not reserved capacity.

## Changes
Only the authorized four repository disk-type substitutions were made by the parent implementer. Knowledge logs, existing system map and single TODO list reflect the HDD choice and final-stage blocker. Publication and runtime execution remain pending explicit approvals.

## Risks and limits
HDD performance for large SQL databases needs runtime assessment. Source image minimum disk remains 400 GiB; selecting HDD does not reduce allocated size. Recheck quotas/resource absence before step_1. Current quota fit does not establish instance creation, WinRM reachability, backup access or database integrity. Existing image replacement/deletion and final stand recreation retain their prior reviewed semantics.

## Portable lesson
none

## Conditional Elasticsearch capacity update (2026-10-10)

If Elasticsearch targets the same test/test1/test6 stands, the READY thick source image minimum is 40 GiB per disk, adding 120 GiB. Current 595 GiB HDD headroom fits base 400 GiB plus ES 120 GiB with 75 GiB left; final MSSQL 1200 GiB plus ES 120 GiB requires absolute limit 1825 GiB, so proposed 2000 GiB leaves 175 GiB at the baseline. ES stand scope is not explicitly selected. See the [ES capacity update](2026-10-10-nomad-test-elasticsearch-recovery-destination-review.md).
