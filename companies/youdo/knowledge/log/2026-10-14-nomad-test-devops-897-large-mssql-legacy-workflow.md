---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [mssql, ansible, awx, vk-cloud]
---
# DevOps-897: legacy large MSSQL recreation workflow

## Task

Investigate the historical large MSSQL refresh/deployment flow for DevOps-897 before migration from Yandex Cloud to VK Cloud. User scope excludes small databases. No repository implementation or runtime action requested in this investigation.

## Context

Repository: /home/slnnk/git/automation-test-yandex, committed baseline a240575. Checkout is on DevOps-894-deploy-elasticsearch-on-vk with unrelated ES work and earlier DevOps-889 MSSQL edits. Historical names below come from committed HEAD, not those local edits. User recalls weekend AWX launches; exact AWX workflow, schedule and timezone were not independently retrieved.

## Actions

Ran ai-sync.sh (no output), consulted current context/TODO/repos and MSSQL notes, inspected git status and historical task files with git show HEAD:path. Delegated multi-file read-only investigation. Preserved all repository changes.

## Findings

playbooks/yandex-mssql-test.yml documents weekly/weekend refresh and contains seven tags:

1. step_1: create temporary VM/hostname sql-base from OS image yc-sql-service-os01, boot disk yc-sql-base.
2. step_2: install Windows updates and reboot.
3. step_3: install RecreateDBProcedures.sql, disable the YouDo login, restore YouDo only through sp_RestoreDB_FromBackup using the latest dated CleanYouDo.bak under the configured SMB share, re-enable login and shut Windows down.
4. step_4: delete old prepared image yc-sql-base, create replacement from disk yc-sql-base, then delete VM sql-base.
5. step_5: delete old sql-test, sql-test1, sql-test6 VMs.
6. step_6: create these VMs/hostnames again from image yc-sql-base; boot disks yc-sql-test, yc-sql-test1, yc-sql-test6.
7. step_7: run ChangeZabbixConfig.vbs, sp_CorrectServerName and reboot Windows on test VMs.

Original destination: ru-central1-b, folder b1gnfk02b6vos0csupua; VM sizing 4 vCPU/8GB, standard-v3, network-ssd. Historical live inspection on 2026-10-09 recorded 400GiB boot disks with auto_delete=true and no secondary disks; this is historical evidence, not a current VK sizing recommendation.

Large stands test/test1/test6 use instance_type=thick. playbooks/deploy/db/restartMSSQLSERVER.yml dispatches thick to restartMSSQLSERVER_on_VM.yml (Windows MSSQLSERVER restart and port1433 wait); thin to ../docker/deploy_mssql_nomad.yml. playbooks/deploy/db/restoreSnapshotMaster.yml uses SQL procedures sp_RestoreFromLastSnapshot and sp_RecreateSnapshot across application databases; that flow also includes public-test, which is absent from the three weekend VM clones. SQL database snapshot reset and cloud boot-image recreation are separate operations.

Prior DevOps-889 yc-a-sql-* naming and HDD local edits are a Yandex recovery adaptation, not the original naming or a completed VK migration. Earlier recovery evidence: [DevOps-889 plan](2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md).

## Historical inventory and deployment contract (2026-10-14)

Private IP persistence: committed step_1/step_6 cloud creation commands set VM name/hostname but do not supply a fixed private address. Stand group_vars use stable sql-test[1|6].ru-central1.internal DNS endpoints; dynamic inventory discovers the current NIC private IPv4. Therefore the historical automation did not guarantee the same IP across weekly delete/recreate cycles; no live historical IP allocation audit was performed.

User asked whether inventory is required. Historical root test_inventory.sh fetched JSON from dyninv.yandex-test.youdo.local; the client did not generate inventory locally. DevOps-896 now covers that consumer's VK migration and SQL host mapping vk-ms1-sql-{stand} to {stand}_sql0. [Inventory migration contract](2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md).

restartMSSQLSERVER.yml routes thick stands to restartMSSQLSERVER_on_VM.yml, whose play targets sql hosts and restarts MSSQLSERVER via win_service; it waits for port1433 on the sql endpoint variable. restoreSnapshotMaster.yml also targets sql and gates the reset block to test/test1/test6/public-test. Inventory identifies the SQL VM and stand membership; existing group_vars supply stand variables and Windows/SQL access configuration. Static inventories/public-test/hosts demonstrates sql under windows:children; stand group_vars/all.yml supplies instance, instance_type=thick and sql.

The weekly refresh targets local127.0.0.1 for cloud resource operations and sql for Windows steps2/3/7 in the committed original. Inventory is required for guest operations and ordinary deployment; a static inventory can provide that contract without waiting for the dynamic service. Existing mssql_inventory.ini is a DevOps-889 Yandex recovery artifact, not a ready VK inventory. Exact historical AWX invocation/order remains unverified. Source inspection also encountered embedded notification credentials in playbooks/deploy/app/newdeploy.yml; only this location is recorded, never the value.

## Changes

Only this knowledge note, the existing nomad-test system map and generated index/sync bookkeeping. No branch change, repository edits, staging, commit, push, MR or external changes.

## User destination naming decision (2026-10-14)

The user reports that image yc-sql-base already exists in VK Cloud. Availability, ID and readiness have not been independently checked. Preserve this exact name when referring to the existing source image; no rename or deletion is authorized by the naming decision.

User selected vk-ms1 instead of yc as the prefix for destination disks and images, and vk-ms1 as the VM prefix. Destination naming: temporary VM and boot disk vk-ms1-sql-base; newly prepared image vk-ms1-sql-base; stand VMs and boot disks vk-ms1-sql-test, vk-ms1-sql-test1, vk-ms1-sql-test6. This naming is scoped to DevOps-897; it does not rename historical assets or authorize repository edits, branch creation or infrastructure changes. Source OS-image choice for the seven-stage process remains to be established; the available prepared yc-sql-base image must not be silently equated to the historical seed yc-sql-service-os01.

## Risks and limits

Live follow-up now confirms mcs.local and resolver10.18.20.3 on running VK VMs; default Jenkins DNS works, while agent01 local dnsmasq times out for tested private names. This supersedes the earlier network-domain uncertainty below. [Live DNS check](2026-10-14-nomad-test-devops-897-vk-private-dns-check.md).

VK private DNS documentation checked2026-10-14: official vkcs provider documents network private_dns_domain, subnet enable_private_dns (enabled by default), and port dns_name. Custom subnet DNS servers replace built-in resolvers and the example explicitly warns that private resource DNS names then become unavailable. Sources: https://github.com/vk-cs/terraform-provider-vkcs/blob/master/docs/resources/networking_network.md, https://github.com/vk-cs/terraform-provider-vkcs/blob/master/docs/resources/networking_subnet.md, https://github.com/vk-cs/terraform-provider-vkcs/blob/master/docs/resources/networking_port.md. This supports evaluating a stable port DNS name for MSSQL recreation; actual project domain/resolver settings and deletion/recreation propagation were not checked. Do not assume that VM display-name prefixes alone establish DNS registration.

Actual AWX configuration is unavailable in collected evidence. Committed playbook comments confirm weekend use, but do not establish AWX job names or exact schedule. No resource recreation or Windows/SQL checks were run. VK migration design and branch approval remain outside this historical investigation.

## Portable lesson

none
