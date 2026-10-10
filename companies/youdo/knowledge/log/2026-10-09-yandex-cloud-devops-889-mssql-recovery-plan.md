---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [mssql, recovery, ansible]
---
# DevOps-889: MSSQL VM recovery plan for zone a

## Summary
The user corrected scope to minimal Ansible edits for running the existing seven-stage workflow in the new folder. The expanded helper, tests, SQL changes, Windows changes, defaults and generation mechanism were removed. Current approved branch DevOps-889-recover-mssql-vms contains six modified existing files plus one small static inventory: target folder/zone/subnet/names, base-only and tests-only host groups, and target DNS lookup in the existing Zabbix script. Syntax, list-hosts, diff checks and independent review passed. No recovery stage, quota request or publication was executed. Optional improvements are recorded only in ~/ai/TODO.md. SSD headroom remains insufficient (959 GiB available, 1200 GiB needed); image quota is sufficient for the original replacement workflow because step_4 deletes the existing target image before rebuilding it. Earlier expanded implementation sections below are historical and superseded.

## Task
[DevOps-889](https://youtrack.youdo.com/youtrack/issue/DevOps-889/Recovery-Vosstanovit-VM-MSSQL-s-bolshoi-BD): restore MSSQL VMs for test, test1 and test6, using the destination of recovery Kubernetes cluster yc-a-k8s-dev. YouTrack description contains precisely these three stands; no comments or attachments were returned.

## Context and verified destination
- Repository: /home/slnnk/git/automation-test-yandex, origin git@gitlab.youdo.sg:sysadmins/automation-test-yandex.git. Legacy entry point playbooks/yandex-mssql-test.yml, role playbooks/roles/yandex-mssql-test.
- Reference cluster: catg1hn09gu2jslb8vgl, yc-a-k8s-dev, RUNNING, ru-central1-a.
- Folder: test-platform-folder, b1gra6b6tvv67paql8hs.
- Subnet: test-platform-subnet-a, e9b32eqch1la7rq0ed6e, 10.16.28.0/24, owned by the destination folder.
- VPC: shared_network, enpo166pnu2hbn1s7v5k. Same VPC as the old environment; the subnet, folder and zone change. VPC owner folder differs from destination folder.
- Route table: enp1rr12evj2uedu2p2h. DHCP DNS: 10.16.20.3. KB records default route via 10.16.20.3; actual end-to-end reachability requires verification.

## Source inventory
All three old instances are RUNNING according to the control plane, in folder b1gnfk02b6vos0csupua and zone ru-central1-b, with 4 vCPU/8 GiB, one boot disk, no secondary disks reported. Each boot disk is 400 GiB network-ssd and auto_delete=true. RUNNING/READY does not establish guest, SQL or data availability.

| Stand | Old instance ID | Boot disk ID | Proposed recovery name |
| --- | --- | --- | --- |
| test | epd1aeuebue3vm66q9m7 | epd4m2db3bfkj0pf5533 | yc-a-sql-test |
| test1 | epdpqulg28r74u5fk6ho | epd671ftpc4g3e76ur5t | yc-a-sql-test1 |
| test6 | epdkhv211fomrr18u53m | epd7vqcbchi29v1t5i30 | yc-a-sql-test6 |

All three disks identify source image fd8fig4dgkdkc1gnk1mm (yc-sql-base), READY, created 2026-10-04T10:09:22Z, minimum disk 400 GiB. Initial OS image yc-sql-service-os01 is fd85ba0q598o5i9bbo86, READY, created 2024-06-11T13:00:06Z, minimum disk 400 GiB. Both images have os.type=LINUX metadata, whereas the role uses Windows/WinRM modules: treat guest OS and SQL versions as unverified until inspected. Image creation date does not prove backup data date.

## Legacy workflow and hazards
The weekly refresh comment describes OS image -> temporary sql-base -> restore YouDo -> yc-sql-base -> three clones -> hostname/SQL server name/Zabbix correction. Scheduler was not found during repository investigation.

References in automation-test-yandex:
- playbooks/yandex-mssql-test.yml:2: workflow; step_1 through step_7.
- playbooks/roles/yandex-mssql-test/tasks/6-create-test-instances-from-base-image.yml:5: three instances, standard-v3, 4 CPU, 8 GB, network-ssd; old folder/zone, no explicit network-interface.
- playbooks/roles/yandex-mssql-test/tasks/3-restore-from-backup.yml:23: sqlcmd without -b and unreliable failed_when.
- playbooks/roles/yandex-mssql-test/files/RecreateDBProcedures.sql:92: hardcoded UNC, latest dated folder and CleanYouDo.bak; destructive ordering.
- playbooks/roles/yandex-mssql-test/tasks/7-update-services-for-test-env.yml:4: identity correction, sp_CorrectServerName and reboot; procedure depends on xp_cmdshell.
- group_vars/test.yml:3, test1.yml:3, test6.yml:3: applications use sql-test[1|6].ru-central1.internal.
- group_vars/sql.yml: mssql_user/mssql_password; group_vars/windows.yml: ansible_* access references. Secret values must never be copied to notes. test_inventory.sh obtains dynamic inventory; validate its folder filtering.

Do not run the complete legacy playbook: step 5 deletes old instances; step 4 deletes an existing base image; many resource operations depend on the active YC profile and omit folder. The boot image workflow only captures the boot disk. Verify actual SQL file paths and any external storage before relying on it.

## Earlier recovery proposal (superseded by the full seven-stage request)
1. Read-only preflight: data freshness was confirmed by the user; check actual guest/SQL versions, file layout, YouDo state and backup availability. Confirm YC image access from target-folder service account, available IPs, VM licensing requirements and quota headroom. Three baseline clones require 12 vCPU, 24 GiB RAM and 1200 GiB network-ssd; temporary base/pilot overlap increases headroom. Keep old instance/disk/image IDs recorded. Do not delete old instances with auto-delete boot disks.
2. Selected data source (user confirmation 2026-10-09): existing yc-sql-base by immutable ID fd8fig4dgkdkc1gnk1mm. Validate boot/database integrity on the pilot. No backup restore or new base image is needed for the selected route. The following alternatives are retained only as contingency context: This bypasses old base deletion, old VM deletion and backup restoration. For a newer clean baseline, build a uniquely named temporary base from yc-sql-service-os01 in the target subnet, restore an explicitly selected verified backup, stop cleanly and create a uniquely named/versioned image. If current per-stand changes must be retained and old guests are accessible, take application-consistent snapshots of each required disk and create target-zone disks from them. Snapshot creation/stopping writes requires separate approval. Source zone unavailability may prevent making new snapshots; existing READY images/backups remain candidates.
3. Prepare local Ansible changes after supervised branch approval. Proposed repository automation-test-yandex, branch DevOps-889-recover-mssql-vms, base origin/master (confirm fetched project baseline first). Parameterize source/target folder separately, ru-central1-a, subnet ID, security groups, source image ID, new VM names and inventory. Use explicit folder or immutable IDs in every lookup/mutation; do not change the global YC profile or overwrite/delete existing images. Add a recovery entry point with explicit safe stages and new-host-only limits. Keep runtime passwords in the established secret source. Run syntax/list checks and review the exact cloud command set; do not rely on --check to safely simulate arbitrary shell tasks.
4. Prepare networking: private addresses in 10.16.28.0/24, reviewed SG membership/rules and Windows firewall. Check application/Kubernetes effective source addresses -> TCP1433, Ansible controller -> TCP5986, SQL VM -> SMB TCP445 at the backup server, DNS to 10.16.20.3, update/time dependencies and return routes. Existing internal SG self-membership rules do not prove access. No public SQL endpoint is required. Verify the real UNC endpoint: script uses \\10.16.26.4\public\sql\, another script copy uses 172.26.0.115.
5. For fresh-backup route only, verify access as the SQL Server service identity, not the WinRM user. Check exact file/date/size, RESTORE HEADERONLY/FILELISTONLY/VERIFYONLY and capacity before destructive restore; use correct data/log MOVE paths. Fix missing-backup handling, validate before dropping any existing DB/snapshots, and make SQL errors fatal with sqlcmd -b plus SQL error handling. Test on the temporary base only. VERIFYONLY alone is insufficient: complete an actual restore and integrity/application checks before publishing the base image.
6. Create pilot yc-a-sql-test with baseline standard-v3, 4 vCPU, 8 GiB, 400 GiB network-ssd in the target folder/subnet. Prefer boot disk auto-delete disabled for recovery assets. Validate image actually boots as expected, WinRM, SQL service, hostname/@@SERVERNAME, unique monitoring identity, YouDo ONLINE, database data date and integrity, log/tempdb paths and free capacity. Validate sp_CorrectServerName results explicitly; do not blindly enable xp_cmdshell. Prevent cloned maintenance/refresh tasks from reaching original stands or production backups until reviewed.
7. Test connectivity and representative application operations from the intended client network and, when required, the recovered Kubernetes workloads. Create and validate yc-a-sql-test1 and yc-a-sql-test6 after pilot acceptance. New zone-a resource names follow current yc-a- convention; preserve logical stand mappings through explicit connection strings/managed aliases. Do not assume old *.ru-central1.internal resource records can simply be repointed. Find all runtime consumers, Vault-backed connection strings, inventory, DNS and monitoring before cutover. Switch one stand at a time after approval.
8. Accept when all three VMs/SQL services are healthy, YouDo is ONLINE with agreed data date, logins/application operations work, integrity checks pass and monitoring is correct. Keep source assets through an agreed rollback window; rollback restores previous connection settings/endpoints. Once applications write new data, reverting requires accounting for those writes. Separate approval is required for removal of old resources and re-enabling scheduled refresh. Adapt weekly refresh to the new source/target and explicit safe failure behavior before resuming it.

## Actions and key commands
Ran ai-sync.sh (no output), KB keyword searches and delegated repository review. Retrieved YouTrack issue via existing youtrack_sprint.py client using GET only. Used read-only yc managed-kubernetes cluster get, yc vpc subnet get, yc compute instance list, yc compute image list and yc compute disk list. Network reads required escalation after sandbox DNS failure/stall; no token values printed. Repository task files were not edited.

Yandex documents cross-zone disk recovery through snapshots: [moving a VM](https://yandex.cloud/en/docs/compute/operations/vm-control/vm-change-zone). Special relocate command currently targets zone d; do not use it as an assumed route to zone a. Cross-folder source-image/snapshot IAM must be checked with the actual executor.

## Changes and approvals
Only this KB log, the existing test-infra system map and the single backlog are updated. No branch creation, source edits, commit, push, MR, cloud mutation, deployment or tracker write. Recovery names and implementation branch above are proposals, not approved names. Repository edits need stage-one supervised approval; commit/push/MR need stage-two approval. External changes need explicit action approval, including creating VMs/images/snapshots, stopping guests, running configuring Ansible, switching runtime DNS/connection settings and deleting resources.

## Risks and limits
Image usability, actual guest OS, SQL/Windows versions, guest accessibility, exact SG rules, routes, licensing and quota headroom remain unverified. The old control-plane RUNNING status is not proof of availability in zone b. Three boot disks consume 1200 GiB baseline; restored SQL files may require additional capacity. The earlier destructive backup procedure defect is evidence from [the August restore investigation](2026-08-02-mssql-yandex-mssql-restore-youdo.md); it must be addressed if the fresh restore route is used.

## Portable lesson
Existing recipe: [restore procedure drops DB before verifying backup](../../../../general/knowledge/mssql/restore-procedure-drops-db-before-verifying-backup.md).

## User decision: existing image data is current (2026-10-09)

User confirmed item 1: data in the existing image is current. Use yc-sql-base fd8fig4dgkdkc1gnk1mm to create the three new zone-a VMs. Skip OS-base preparation, backup restore, replacement base-image creation and snapshots in the selected recovery route. Still validate image boot, actual OS/SQL versions, database integrity and application behavior. This confirmation selects the data source; it does not authorize repository branch creation/edits or external infrastructure changes.

## Approved image copy (2026-10-09)

User explicitly confirmed creating yc-a-sql-base in test-platform-folder from existing image fd8fig4dgkdkc1gnk1mm while preserving the original. Preflight source READY, destination image list empty. Executed only the approved cloud mutation:

```bash
yc compute image create yc-a-sql-base --source-image-id fd8fig4dgkdkc1gnk1mm --folder-id b1gra6b6tvv67paql8hs --format json
```

New image ID fd8rim6q4rkns8c35q3s appeared in destination folder with CREATING status. Creation completed successfully in 3m48s. Independent image GET verified fd8rim6q4rkns8c35q3s is READY in b1gra6b6tvv67paql8hs, minimum disk 400 GiB; source image GET also confirms original fd8fig4dgkdkc1gnk1mm remains READY in its original folder. The recovery VM creation step must now use the destination copy ID fd8rim6q4rkns8c35q3s. The copy inherits os.type=LINUX metadata; actual guest OS remains a pilot verification item. No VMs created, source image deleted, repository edits, Git operations or unrelated external changes performed.

## Scope correction: full seven-stage rebuild in target folder (2026-10-09)

User now requests adapting Ansible and executing all seven stages exclusively in the new folder. This supersedes the earlier execute-only-step_6/step_7 route: a temporary VM must be created, Windows updated, fresh backup restored, a new prepared image created, and target-folder stand VMs recreated/configured. The already copied READY yc-a-sql-base remains a fallback until replacement validation. Original folder assets must not be touched. Source OS image may be referenced by immutable ID in the old folder; any required copy into the target folder is a separate reviewed action.

Read-only fetch completed; clean automation-test-yandex checkout on master matches origin/master a240575. Proposed task branch remains DevOps-889-recover-mssql-vms, base origin/master. No task branch creation or repository edits are authorized yet; proposal will be presented to the user. External actions require specific confirmations under the user's global rules.

## Approved local implementation and checks (2026-10-09)

The user explicitly confirmed the proposed design and branch. Created the branch in the existing automation-test-yandex checkout; preserved clean starting baseline origin/master a240575. No worktree, staging, commit, push or MR was performed. Code uses the existing playbook/role and all step_1 through step_7 tags.

Changed repository paths:
- playbooks/yandex-mssql-test.yml and playbooks/roles/yandex-mssql-test/defaults/main.yml: target defaults and dedicated local/base/test plays; remote credentials reference existing root vars files.
- Role tasks/main.yml, all seven stage task files, and new tasks/discover.yml: folder-scoped discovery, explicit generation, targeted guest steps, all-three readiness and deterministic hostname/Zabbix correction.
- New files/yc_mssql_recovery.py: owned-resource validation, explicit folder on every YC command, exact approved folder/zone/subnet guard, private-address discovery, immutable generation image lifecycle, verified-restore marker, retained test boot disks, quota preflight and safe API failures.
- files/RecreateDBProcedures.sql: backup path and exact set/type/database/freshness checks, HEADERONLY/FILELISTONLY/VERIFYONLY with planned MOVE paths before destructive operations. Reject multiset files rather than checking a different set than FILE=1.
- New tests/test_mssql_recovery.py and tests/test_mssql_backup_quoting.py: guards, quota behavior, retry marker/image lifecycle and actual Ansible rendering of UNC paths with dollar signs/apostrophes.
- New docs/mssql-recovery.md: runtime commands, effects, permissions, dependencies and acceptance criteria.

The existing hardcoded tester credential was left in its original task; no new secret values were copied to notes or scripts, and that task is now no_log. SQL credentials use existing vars and a transient SQLCMDPASSWORD environment under no_log, never password command arguments.

Verification: sixteen tests passed (including relevant RED-to-GREEN cases), all modified role YAML parsed, Python helper compiled, git diff --check passed, Ansible syntax and list-tags passed. Read-only real-cloud discovery passed with changed=0. Wrong-folder Ansible execution failed at the initial assertion before any API call, changed=0. Static syntax checks warn that new inventory groups are absent before discovery, as expected. SQL stored procedures and Windows mutation tasks were not executed; static checks do not prove runtime SQL compatibility or network/guest availability.

Independent reviewer identified three important issues: PowerShell UNC quoting, stale same-generation images after a repeated restore, and backup freshness checking a different set than FILE=1. Quoting and lifecycle fixes were demonstrated by failing then passing tests. SQL exact-set validation was changed and reviewed locally, but actual SQL validation remains required on the temporary VM. No confirmed critical findings or deferred minor findings were returned. A possible disk-name collision was not confirmed and was not treated as a defect.

## Live network and quota preflight (2026-10-09)

GET network confirms default SG enphd14jsltn0jan0fmf; its ingress/egress allow ANY from/to 0.0.0.0/0. New VMs have private addresses only. SG therefore permits necessary traffic, but actual routes, Windows firewall, SMB service identity permissions and guest reachability remain runtime checks.

Cloud b1g8s9lk6hktue4a48mg, target folder test-platform-folder. Quota-manager read returns:
- SSD: limit 6000 GiB, usage 5041 GiB, free 959 GiB. Three new 400 GiB test disks need 1200 GiB; shortage 241 GiB. Temporary base alone fits; it is removed before the three test disks are created.
- Images: limit 1500 GiB, usage 1390.02 GiB, free 109.98 GiB. Reserve up to 400 GiB for the new full-disk generation image; quota is insufficient.
- RAM: 2048 GiB limit, 2014 GiB used, 34 GiB free. Baseline temporary 8 GiB / subsequent three tests 24 GiB fit current headroom.
- CPU: 500 limit, 474 used, 26 free. Baseline temporary 4 / subsequent three tests 12 fit current headroom.
- Disk/image/instance count limits have headroom for this cycle. Other work may change these values; helper rechecks before mutations.

Proposed external quota request (not yet authorized or executed):

```bash
yc quota-manager quota-request create \
  --resource-id b1g8s9lk6hktue4a48mg \
  --resource-type resource-manager.cloud \
  --desired-limit quota-id=compute.ssdDisks.size,value=7516192768000 \
  --desired-limit quota-id=compute.images.size,value=2147483648000
```

This requests SSD 7000 GiB and images 2000 GiB; actual approval by Yandex must be verified. Existing source/fallback assets are retained instead of being deleted to free quota.

## Publication proposal (not approved)

Commit: scope mssql refresh to platform folder. MR title: DevOps-889 recover mssql VMs in platform folder. Source DevOps-889-recover-mssql-vms, target master. CI config is unchanged; old weekend invocations must be adapted to the mandatory generation after acceptance. MR description, when publishing is approved, must follow training rules: one short Russian change paragraph then the task link only. No publication approval is inferred from the local-edit approval.

## User scope correction and minimal final diff (2026-10-09)

User rejected the expanded change set: only minimal edits necessary to run in the new folder should be made, with improvement proposals in TODO. Reverted only the agent's expanded local edits using read-only git show HEAD:path and local writes; removed only newly created helper/discovery/docs/tests files. No state-changing git command was used for this correction. Original SQL procedures, Windows update/restore/service tasks, role defaults/main and existing seven-stage semantics are byte-identical to HEAD.

Final repository changes:
- tasks/1-create-instance-for-update.yml: target base VM/disk/hostname yc-a-sql-base, explicit target folder for lookup/create, zone a and explicit target subnet. OS image yc-sql-service-os01 is read from its existing original folder; no OS image copy is required.
- tasks/4-delete-base-instance.yml: original image replacement and base deletion logic, using target names and explicit target folder on all three commands. This stage will delete the copied target image yc-a-sql-base before rebuilding it; the source-folder image remains outside these commands. Runtime approval must cover this original lifecycle.
- tasks/5-delete-old-instances.yml: original deletion semantics but only new target-folder yc-a-sql-test/test1/test6 names.
- tasks/6-create-test-instances-from-base-image.yml: target names/folder/zone/subnet/image folder, existing size/platform/wait semantics.
- playbooks/yandex-mssql-test.yml: only three host-group substitutions; step_2/step_3 target sql_base, step_7 targets sql_test.
- files/ChangeZabbixConfig.vbs: only two line changes: suffix array limited to test/test1/test6 and nested replacement of lookup DNS in the ping command. Logical monitoring names and caller SrvName remain unchanged; no ByRef parameter assignment is introduced.
- New root mssql_inventory.ini (18 lines): only new resource DNS names, sql_base/sql_test groups inheriting sql/windows credentials from existing group_vars, and local 127.0.0.1.

Tracked diff: six existing files, 38 insertions and 34 deletions, plus the new 18-line inventory. Existing SQL/WinRM credentials were not printed in the minimal diff or copied elsewhere. During earlier investigation a legacy inventory-script authentication line was inadvertently included in tool output; record only its location test_inventory.sh and external inventory access route, never its value. Optional secret migration is recorded in TODO.

Verified syntax-check, list-hosts (only new base for 2/3, exactly new three stands for 7), git diff --check and independent review. No critical/important findings in the final minimal review. Previous sixteen-test results apply only to the removed implementation, not this final version; no replacement tests were added for these configuration changes.

Run shape from the repository root (not executed):

```bash
ansible-playbook playbooks/yandex-mssql-test.yml -i mssql_inventory.ini --tags step_1
```

Use the same inventory for the remaining separately reviewed tags. The original weekend scheduler must adopt this inventory when publication/runtime changes are approved. No generation argument is required by the minimal version.

Quota correction: original step_4 removes the target copied image (about 400 GiB), freeing its image quota before creating the replacement. Therefore the earlier proposed image-quota increase is unnecessary for the selected minimal workflow. SSD quota still needs resolution before creating all three stand disks; current 959 GiB headroom is short by 241 GiB. No quota request was sent.

Optional safeguards, SQL restore failure handling, immutable images, readiness/retry improvements and secret migration are proposals in the single TODO list, not repository changes. Reusable user correction was applied to global AGENTS.md and the canonical supervised Git workflow map. Publication proposal is now commit update mssql recovery cloud settings, MR DevOps-889 update mssql recovery cloud settings; source/target remain approved branch -> master. No publication approval is inferred from this scope correction.
