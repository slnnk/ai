---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [mssql, ansible, vk-cloud, recovery]
---
# DevOps-897: adapt the seven-stage large MSSQL refresh to VK

## Task

Adapt automation-test-yandex's existing seven-stage large MSSQL weekly refresh to VK Cloud and begin testing it. Scope test/test1/test6, excluding thin databases and public-test. User requested fetching master with updated test_inventory, selected SSD after confirming historic YC network-ssd, then requested continuing runtime work without extra checks absent from the legacy flow.

## Context

Existing [preflight/backup delivery](2026-10-14-nomad-test-devops-897-mssql-vk-preflight-and-backup.md) establishes source yc-sql-base400GiB and copied CleanYouDo.bak90.1GiB; checksum explicitly skipped. [DNS repair](2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md) verified normal DNS across11Nomad nodes. Secrets remain in current/.env / established legacy group_vars; only variable names recorded.

## Actions

ai-sync emitted nothing. Read context/TODO/repos; delegated multi-file design audit. Fetch confirmed origin/master0bfc65c with dyninv.vk-test.youdo.local endpoint. Dirty paths did not overlap master changes. User's combined branch/design question concluded with SSD selection after Yandex type clarification; created DevOps-897-recreate-large-mssql-on-vk from origin/master in existing checkout, preserving inherited MSSQL recovery edits/untracked mssql_inventory.ini. No staging/commit/push/MR performed.

Kept entrypoint/role and step_1..step_7 tags. Added uri-based VK auth/inventory/create/delete tasks following repository API style. Cloud operations use scoped automation credentials from VK_AUTOMATION_USER/VK_AUTOMATION_PASSWORD and common vk_project_id or VK_PROJECT_ID. Parameters STD3-4-8,4vCPU/8GiB,400GiB ceph-ssd,test subnet10.18.26.0/24,test-internal security group.

Creation uses named Cinder boot disk, named Neutron DNS port and Nova volume-backed VM; default names vk-ms1-sql-base/test/test1/test6. Disk waits before VM creation; WinRM waits afterward. Prepared image vk-ms1-sql-base is uploaded from stopped Windows boot disk via Cinder force=true, original yc-sql-base retained, Windows BIOS/VirtIO metadata preserved, temporary base resources removed after image active. Stand deletion/creation remains three-target scope.

Dynamic inventory excludes base. Always-run discovery adds existing exact VK names to sql_base/sql_test/windows, using current private addresses, so separate AWX tag invocations can find hosts. Installed Ansible ignored tasks_from in a roles entry; switched discovery to include_role tasks_from and rechecked. Original source playbook guest logic and tags preserved except short guest names and explicit Zabbix FQDN argument. test1/test6 cloud names16characters exceed Windows15-character limit; guest names sql-test1/sql-test6 are distinct/valid.

Restore task passes explicit new UNC to existing sp_RestoreDB_FromBackup rather than changing SQL procedure. Added sqlcmd-b/return-code handling and no_log to credential-bearing SQL tasks. Three large stand sql variables now point at vk-ms1-sql-test*.mcs.local. Legacy Windows update task remains unchanged. Source audit encountered legacy tester-account credentials in tasks/2-install-windows-updates.yml; only that location is recorded.

## Findings

Local guard first failed because all four cloud stages still used YC CLI. Actual Ansible HTTP/TCP fixture then exercised creation/repeat, stopped-base image upload, clone creation, deletion, wrong project/API503 and disk-error paths. Initial fixtures found numericJSONsize/min_disk strings under installed Ansible; fixed using to_json on request bodies. All5fixture tests passed65.606s; separate creation/repeat test passed15.398s after discovery correction. Syntax and git diff --check passed. Windows guest operations have not yet run; no checksum/clone validation added.

Independent review recommended two additional checks (disk image provenance on reuse and exact attachment ownership on deletion). User explicitly rejected extra checks absent from legacy workflow. Neither recommendation was implemented; proposals deferred to central backlog, not runtime gates. Old untracked mssql_inventory.ini still has YC recovery names; excluded from task delivery/runtime commands. Actual launch uses test_inventory.sh plus localhost only.

User requested immediate execution/continuation; launched step_1 through local generated run_workflow.py with environment-only credentials. Authentication and disk create succeeded; volume af3c6ccb-402e-4d2e-9b0b-d1a5fe075842 named vk-ms1-sql-base400GiB ceph-ssd observed creating. Live Ansible exec session58794 waits for volume available; no VM observed yet. Do not claim step1 complete or boot/WinRM verified. Generated runtime/status/fixtures are under /home/slnnk/ai-data/mssql-vk-dns/; nothing optional added to repository test/tooling paths.

## Changes

Tracked: group_vars/test.yml,test1.yml,test6.yml; playbooks/yandex-mssql-test.yml; role defaults/main.yml, files/ChangeZabbixConfig.vbs, tasks/main.yml and stages1/3/4/5/6/7. New role tasks vk-auth.yml,vk-inventory.yml,vk-create-instance.yml,vk-delete-instance.yml. Existing SQL procedure and Windows update task unchanged. User/inherited unrelated changes preserved; old local inventory excluded. Local publication still requires supervised stage2approval.

## Risks and limits

Current live creation is in progress. Actual Windows boot/access, backup readability under SQL service identity, restore, prepared image export and stand deployment remain unverified. No original image deletion, DB restore, old stand deletion, image replacement or Git publication has yet occurred. User-directed deferred checks remain proposals; do not silently add them in subsequent iterations.

## Portable lesson

none

## Availability zone correction

User questioned PA1 rather than MS1. The create requests omitted availability_zone for both Cinder and Nova; naming does not select the zone. Read-only API observation reports the current boot volume af3c6ccb-402e-4d2e-9b0b-d1a5fe075842 in PA2, status creating, with no matching VM. Interrupted local step_1 controller (exit130) before VM creation. Local role now explicitly sets MS1 for both disk and VM; diff --check passed. Replacement of the existing wrong-zone disk awaits explicit user approval.

## Large database recreation resumed

User resumed large DB work after small test5 deployment/MR106 merge. Fetched origin/master9ad35fb; only group_vars/all.yml differs from current dad41d4, with no overlap in the large MSSQL tasks. Existing local seven-stage edits preserved, no branch switch or further repository edits. Syntax check and diff --check passed. Restarted authorized step_1 via run_workflow.py using fresh scoped credentials and test_inventory.sh. API confirms new boot volume b6553d1a-35f7-4bbd-88c0-0b699212f090 / vk-ms1-sql-base / ceph-ssd400GiB / availability_zone MS1 / creating, no matching VM yet. Live Ansible session94081 waiting for boot volume.

Live waiting continuation: compact API status checks still report the same MS1 boot volume creating and no VM. Ansible until/retry output is expected while status is creating, not evidence of Cinder error. Confirmed runtime gap retained from review: long cloud waits do not refresh expired tokens, and a rerun requires the existing disk available before reuse. New authentication occurs per separately invoked stage. No additional repository hardening or optional checks added.

## Waiting recovery and base VM

First MS1 run stopped in hidden wait result with36retries left, consistent with approximately1-hour token lifetime and earlier observed401; the exact hidden failure status was not retained. Fresh-token API still reportedcreating. Returned to previously approved DevOps-897-recreate-large-mssql-on-vk branch, then fast-forwarded origin/master9ad35fb under existing user pull-master instruction; all local edits preserved. Added shared vk-wait-resource.yml for existing long boot-volume and prepared-image waits: accept401, reauthenticate through existing vk-auth, continue same resource with bounded token renewals; real URI errors remain failures. Existing creating/downloading disk can resume waiting without creating another disk. No optional image provenance or attachment checks added.

Local fixture tests: expired-volume token requires additional authentication and exactly1disk/VM creation; expired-image token reauthenticates without duplicate upload; creating-disk resume reusesexistingID; all3passed32.452s. Normal image publication +3clones/deletion and error-disk no-VM cases bothpassed47.606s. These fixtures do not verify guest boot/SQL content. Diff --check passed.

Resumed step1 on existing disk (session13546). Disk available thenin-use/MS1. Nova VM3cd129ea-9b4e-4b1e-84fb-2a575522f979 / vk-ms1-sql-base ACTIVE, fixed IPv410.18.26.9. Live Ansible waiting for WinRM5986; not yet a completed stage. Old stage1 session94081 exited2.

## Guest DHCP root cause and repair

Step1 session13546 ended with600s WinRM5986 timeout while Nova stayedACTIVE. TCP probes from local VPN(source172.30.63.11) and same-subnet Nomad client01(10.18.26.34) returnederrno113/No route to host on5986/3389/1433. User console screenshots provedWindows booted and baseEthernet2 configuration:MACFA-16-3E-67-AD-9B, DHCPNo, stale172.26.0.103/24, gateway/DNS172.26.0.1. This is the confirmed guest root cause.

User handed over shared console and explicitly approved enablingDHCP forIPv4/DNS onEthernet2. Used read_vm_console.py --enable-dhcp: one elevatedPowerShell command with netsh interface ipv4 set address name='Ethernet 2' source=dhcp, set dnsservers source=dhcp and ipconfig /renew/ipconfig. No firewall/profile changes. Guest received10.18.26.9 andmcs.local. Explicitrenew reportedtimeout, but assignment completed and TCP5986/3389/1433opened. Step1rerun(session66110) passedfailed0 on sameVM. Stage2session48630 authenticatedWinRM/win_user passed, WindowsUpdatefailed(2download failuresHRESULT0x80073712,0installed of5found). Legacyignore_errors preserved, reboot succeeded,60s pause completed; overallrecapfailed0/ignored1. Do not claimWindowsupdates installed. User requestedcontinue; stage3restoration started with freshauth and deliveredUNCbackup.

Console API redirected officialmsk.cloud.vk.com tomsk.cloud.vk.ru, matching user browser screenshot. Console access parameters remained only in memory, never printed/saved. Screenshots and localhelpers underai-data/mssql-vk-dns. No changes to user's separate manualtest1.

Follow-up source contract: importedyc-sql-base retains stale static config. After successfulstep4, change onlystage1 to boot mssql_vk_boot_image|default(mssql_vk_prepared_image), documenting initialbootstrap overrideyc-sql-base. Keepmssql_vk_source_image unchanged asoriginalprotectedimage; stage4 asserts itdiffers fromoutput. No automaticfallback probes or optionalvalidation.

## Restore completed; image stage not executed at focus switch

Stage3session58581 restore command completedok, YouDo login enabled and Windows shutdownok; recapfailed0. Before completion SQLDMV query showedRESTOREDATABASE87.229927%, elapsed573s, estimatedremaining83s. Local sqlcmd18 used existing group_vars/sql.yml credentials via SQLCMDPASSWORD childenv, never printedpasswords/argv. No backup checksum or schema checks added.

User intentionally interrupted pendingstep4 tool call and requested smallNomadjobs instead. Read-only API later found baseSHUTOFF, bootvolumein-use, preparedimagevk-ms1-sql-base absent; no livecontroller detected. Therefore image capture/deletion stage is still pending, not claimed completed. All11thinSQLjobs nowrunning via existingplaybook, unchangedtest5; see [small rollout](2026-10-14-nomad-test-devops-897-small-mssql-test5.md). Originallarge seven-stage work and eventual publication remain unfinished. Futurestep1 prepared-image default switch is planned, not yet applied.

## Explicit one-stage launch

User first deferred further large DB work until tomorrow, then explicitly requested one next stage today and instructed to launch directly without extra preliminary checks. Started only run_workflow.py --stage step_4 (execsession18374), no steps5-7. Existing workflow foundbaseSHUTOFF and bootdisk; Cinder upload-to-image action returnedsuccess. Ansible now waits for preparedimagevk-ms1-sql-base. On activeimage it will preserveWindowsmetadata and delete temporarybaseVM/port/disk as part of this single authorizedstage. Originalyc-sql-base preserved. Stagecompletion not yet confirmed; no standaloneCloudchecks added after user instruction.

## Explicit stage5 execution

User explicitly asked to launchstage5 now. Executed onlyrun_workflow.py --stage step_5 (session87250),exit0,recapok39/changed1/failed0/skipped24. Exactmanagednames vk-ms1-sql-test/test1/test6 and associatednameddisks/ports were absent; all actualdelete tasks skipped. Changed1 was localinventoryadd_host forbase, not a resource deletion. No stage6/7 invoked. Backgroundstage4 image preparation remains separately running; no extra provider checks were performed for this request.

Stage4status on explicit userrequest: liveAnsible18374 stillwaiting. FreshAPI preparedimageb204affb-cf20-473c-816e-09cb03d76421 / vk-ms1-sql-base saving,sizeunset; sourcediskb6553d1a-35f7-4bbd-88c0-0b699212f090 uploading/MS1/400GiB, baseVM3cd129ea-9b4e-4b1e-84fb-2a575522f979 SHUTOFF. No cleanup begun, no completion claimed.

## Stage4 completion verified2026-10-15

On explicit status request, live session18374 returnedexit0 and recapok61/failed0. Preparedimage becameactive; Windowsmetadata preserved; temporarybase VM, Neutronport andbootdisk deletion waits completed. FreshAPI confirms imageb204affb-cf20-473c-816e-09cb03d76421 / vk-ms1-sql-base active,size429496729600bytes(400GiB), no matchingbaseVM orvolume. Temporary10.18.26.9 service address is retired; originalyc-sql-base was excluded fromstage4deletion. Stage5previously passed with no oldmanagedtargets; stages6/7 not launched. Next authorized decision is creation ofthree largeVMs frompreparedimage. Futureweeklystep1 prepared-image boot selection is still a local implementation item, not yet applied.


## Stage6 high-IOPS launch (2026-10-15)

User requested resuming stage6 for only the three large stands test/test1/test6, changing their disks to Network High-IOPS SSD (`high-iops`) and keeping placement in MS1. Applied one scoped variable override, `mssql_vk_volume_type: high-iops`, in `playbooks/roles/yandex-mssql-test/tasks/6-create-test-instances-from-base-image.yml`; base-stage default remains ceph-ssd. Existing checkout is `DevOps-899-fix-microservice-postgres-auth`; no branch switch, staging, commit, push or MR operation occurred, and all prior edits were preserved.

Read-only live API preflight found no matching target VMs/disks and confirmed prepared image `b204affb-cf20-473c-816e-09cb03d76421` active, 400GiB. The `high-iops` volume type extra_specs advertises GZ1, MS1, ME1 and PA2; volume and compute MS1 availability was confirmed. Existing Cinder volume and Nova server requests both explicitly set `availability_zone: MS1`; Keystone API endpoint region remains RegionOne, distinct from the MS1 availability zone.

`python3 /home/slnnk/ai-data/mssql-vk-dns/run_workflow.py --stage step_6 --syntax-check` exited0 (legacy inventory progress stderr/group warning), and `git diff --check` exited0. Started the user-requested `python3 /home/slnnk/ai-data/mssql-vk-dns/run_workflow.py --stage step_6`, live session96718; execution is progressing, completion not yet verified. Stage7 was not launched. Local generated `cloud_status.py` now reports Nova availability zone and accepts `--placement`; credentials remain outside outputs/notes. Post-run resource state, guest access and final recap remain unverified at this observation.

Fresh API after launch confirms first disk `vk-ms1-sql-test`, ID `599ef47e-db00-4d17-ad10-7a54c4a0c480`, downloading, 400GiB, type `high-iops`, availability zone `MS1`. No target VM yet; test1/test6 remain absent while sequential stage6 waits for the first disk.


## Parallel stage6 continuation (2026-10-15)

The initial sequential stage6 API observation found boot disk `vk-ms1-sql-test`, ID `599ef47e-db00-4d17-ad10-7a54c4a0c480`, downloading, 400GiB, volume_type high-iops, availability_zone MS1, no matching VM; test1/test6 had not yet been created because the loop waited for the first disk.

User then requested parallel creation. Stopped only the local sequential controller session96718 with SIGINT, exit99; existing cloud disk was preserved. Modified only generated `/home/slnnk/ai-data/mssql-vk-dns/run_workflow.py`: `--stand` accepts test/test1/test6 exclusively with step6 and passes an extra-vars singleton `mssql_vk_stands` list. Syntax check exited0. No further repository change or Git action.

Started three independent `run_workflow.py --stage step_6 --stand <stand>` controllers: test/session43477, test1/session51636, test6/session43232. Each inherits the existing high-iops disk type and explicit MS1 Cinder/Nova placement. All controllers launched; final cloud creation, guest availability and completion remain pending. Stage7 not launched. This supersedes the sequential-session96718 in-progress status above.

Parallel-run API verification: all three disks are downloading concurrently, each 400GiB/high-iops/MS1. IDs: test `599ef47e-db00-4d17-ad10-7a54c4a0c480`; test1 `e465ddf6-5472-4f34-b50e-e083cc4cc71b`; test6 `902c74bb-8081-4d38-abf7-a3d0b4f010b7`. No matching VMs yet.


## Stage6 completion verified (2026-10-15)

All three independent stage6 controllers completed with exit0 and WinRM wait successful: test/session43477 recap ok58/changed1/failed0/unreachable0/ignored0; test1/session51636 and test6/session43232 each ok59/changed1/failed0/unreachable0/ignored0. Fresh API verification found all three Nova VMs ACTIVE with `OS-EXT-AZ:availability_zone: MS1` and all boot disks in-use, 400GiB, volume_type high-iops, availability_zone MS1.

| Stand | VM ID | Private IPv4 | Boot disk ID |
| --- | --- | --- | --- |
| test | 2471779c-5f34-49b4-a462-0ea7051c7591 | 10.18.26.17 | 599ef47e-db00-4d17-ad10-7a54c4a0c480 |
| test1 | 5056803d-cc7d-47b1-b81c-1a5577779fb5 | 10.18.26.121 | e465ddf6-5472-4f34-b50e-e083cc4cc71b |
| test6 | 24ab1d9d-6d7f-4326-96d1-21ef65dd1108 | 10.18.26.9 | 902c74bb-8081-4d38-abf7-a3d0b4f010b7 |

Updated `current/service-addresses.env` with these three large-stand addresses and observation date, explicitly distinguishing cloud/WinRM verification from SQL verification. The former temporary base address10.18.26.9 is now assigned to test6. No SQL content verification performed; stage7 has not run, and reviewed Git publication remains pending. This supersedes all stage6-pending observations above.


## Stage7 completion verified (2026-10-15)

User explicitly requested starting stage7. `ai-sync.sh` emitted nothing. Ran `python3 /home/slnnk/ai-data/mssql-vk-dns/run_workflow.py --stage step_7`, session12238, exit0. Recap: localhost ok11/changed1/failed0; each of test/test1/test6 ok7/changed6/unreachable0/failed0/ignored0.

Windows renames to sql-test/sql-test1/sql-test6 and their rename reboots passed; VBS copy and Zabbix FQDN configuration change passed; credential-hidden `sqlcmd -b` execution of `sp_CorrectServerName` passed; final `win_reboot` passed for all three. The seven-stage runtime run is complete. No repository edits, staging, commits, pushes or publication occurred in this stage.

This verifies the executed guest configuration tasks, not application behavior, SQL schema/data contents or monitoring ingestion. Git publication/review and the previously recorded future stage1 prepared-image default change remain pending; no extra checks were added. This supersedes stage7-pending observations above.

## YouTrack comment refreshed (2026-10-15)

User explicitly requested updating the MSSQL task comment. Updated existing DevOps-897 comment `74-124677` through the YouTrack API; no duplicate comment created. Replaced obsolete stages6/7-not-started status with completed seven-stage runtime, three ACTIVE400GiB high-iops/MS1 VMs, successful stage7, merged endpoint MR113/cf88e422 and user-reported successful playbook acceptance. Preserved thin-job results, WindowsUpdate limitation, unpublished complete workflow/prepared-image first-stage follow-up and regular DBA_Clean delivery scope. Exact saved text verified by a fresh GET; SHA256 `df94c61f97dbe3ecf5039af969e6e47707e2690e330a954e7485e363089d941d`. Local text/helper/receipt are under `/home/slnnk/ai-data/mssql-vk-dns/devops-897-comment-*` and `update-devops-897-comment.py`.
