---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [mssql, nomad, vk-cloud]
---
# DevOps-897 small MSSQL test5 deployment

## Summary

User paused large database recreation and authorized deletion of wrong-zone base disk, then selected and explicitly approved small MSSQL deployment on test5. Existing unmodified Ansible playbook successfully deployed mssql-test5 in vk-test using current test_inventory.sh. The subsequently requested one-line absent-job error fix was published and explicitly user-authorized for merge via MR106; master9ad35fb.

## Deployment

Existing playbooks/deploy/docker/deploy_mssql_nomad.yml uses image registry.youdo.sg/sysadmins/dba_projects/dba/mssql_preseed:latest with embedded prepared database files; no Cinder volume or Windows base image is required. The thin database producer is dba airflow_dags/mssql_clean_jobs.py preseed_copy_files/preseed_publish_image and preseed_scripts/docker/Dockerfile/init.sql. No producer rebuild was triggered.

The runtime command was ansible-playbook -i test_inventory.sh playbooks/deploy/docker/deploy_mssql_nomad.yml -l test5. Token was injected from current/.env VK_TEST_NOMAD_TOKEN, never saved to another file. Before deploy Nomad API returned404. First attempt failed because legacy failed_when matched uppercase ID while actual absent-job message used lowercase id. A retry with existing --tags run_es skipped the absent-job stop; recap ok2/changed2/failed0. No repository changes were needed for that successful run.

Read-only API confirmed job running/version0, allocation dfdb37e8-f2be-3e09-b723-c270c40c52bc and task mssql running. Consul sql-test5 is registered on vk-ms1-nomad-agent-test-08 at10.18.26.35:14305. Serf health passing is node health; SQL content/freshness and authenticated SQL query were not checked. No checksums or extra hardening were added.

## Requested error handling change

User then requested that absent MSSQL job not fail the playbook, and approved branch DevOps-897-handle-missing-mssql-job from origin/master0bfc65c in the existing checkout. All unrelated large MSSQL files were preserved unstaged. One line in playbooks/deploy/docker/deploy_mssql_nomad.yml now lowercases stderr before matching the absent-job string. Reproduced original failure; lowercase id and uppercase ID absence cases pass; successful stop passes; ACL denial and API connection failure still fail. Existing ambiguous-prefix handling was unchanged. Commit dad41d4833eb1b34d67cec4a604d5f02a1d4238f: handle absent mssql job during deployment. MR DevOps-897 Handle absent MSSQL job during deployment; target master. Published and merged after explicit user approval; publishing and merging this playbook file did not deploy or rebuild images.

## Wrong-zone disk deletion

User explicitly authorized deletion only, no replacement. Disk af3c6ccb-402e-4d2e-9b0b-d1a5fe075842 / vk-ms1-sql-base is PA2 (user initially saw PA1),400GiB ceph-ssd, unattached and creating. Ordinary DELETE returned400; os-force_delete returned403 because current role lacks volume_extension:volume_admin_actions:force_delete permission. A local waiting deletion helper is running (exec session58450), polling until creation completes and then deleting only this exact resource. No status reset or privilege changes. Deletion has not yet been confirmed. Large MSSQL controller was interrupted before any VM creation; local creation requests now explicitly select MS1 for both volume and VM.

## Training record and publication

2026-10-14, DevOps-897, automation-test-yandex. Branch proposal DevOps-897-handle-missing-mssql-job from origin/master0bfc65c accepted explicitly. Commit/MR proposal accepted with user instruction “Да и смержи”; that instruction additionally authorized this particular merge, without changing the general supervised policy. Fetch found unrelated master update d98f04c in group_vars/all.yml; no overlap with the one-line task file. Staged diff contained only that task file, one insertion/deletion; no other files committed. Syntax check and five error-expression cases passed; no repeat deployment.

Published commit dad41d4833eb1b34d67cec4a604d5f02a1d4238f. [MR106](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/106) assigned a.solonenko, squashfalse, existing remove-source-branch settingtrue. MR had no pipelines; head_pipeline null. Exact source SHA and one-file changeset checked before authorized merge. API confirms merged2026-10-14T17:23:08.886+03:00, merge commit and master SHA9ad35fb8206427a5ebfbdd453f659c2e7d0aa254. All unrelated large MSSQL edits remain unstaged in the existing checkout. No deployment or image build triggered by this action.

## Confirmed disk deletion

User requested a fresh disk check. New scoped API token found vk-ms1-sql-base / af3c6ccb-402e-4d2e-9b0b-d1a5fe075842 available,400GiB ceph-ssd,PA2; no matching VM. Previous waiting deletion process had stopped on401 after token expiration. Resumed the earlier explicitly approved deletion with fresh credentials: DELETE returned202, subsequent exact-volume GET returned404 and helper exited0 (session44923). Disk deletion is confirmed. No replacement disk or VM was created.

## All small MSSQL stands deployed

User interrupted the large DB image stage and requested small database Nomad jobs. Read-only list found only mssql-test5 running. Deployed missing10stands test2/test3/test4/test7/test10-test15 through existing deploy_mssql_nomad.yml using current test_inventory.sh and --tags run_es, so existingtest5 was not purged or restarted. Runtime helper run_small_db.py gained --stands outside the repository, with token passed in childenv and output redacted. No repository adaptation for this rollout. Ansible session53020 ended0: each10host ok2/changed2/failed0.

Read-only Nomad allocations and Consul services verified2026-10-14 20:04UTC:11/11 jobs and mssql tasks running, services registered, nodeSerfcheckpassing. This is not a SQL contents/freshness check. Existingtest5allocation dfdb37e8-f2be-3e09-b723-c270c40c52bc unchanged. Generated compact evidenceai-data/mssql-vk-dns/small-jobs-result.json. Service-addresses map updated for observed registrations.

Endpoints: sql-test2/3 at10.18.26.21 ports14302/14303; test4 at10.18.26.37:14304; test5 at10.18.26.35:14305; test7/test10 at10.18.26.38:14307/14310; test11 at10.18.26.10:14311; test12 at10.18.26.15:14312; test13 at10.18.26.35:14313; test14/test15 at10.18.26.34:14314/14315. Stable service names sql-<stand>.service.vk-test.consul; allocation IP may change on reschedule. Application deployment remains deferred by user.

LargeDBstatus at switch: freshcloudAPI base3cd129ea-9b4e-4b1e-84fb-2a575522f979 SHUTOFF, bootvolume b6553d1a-35f7-4bbd-88c0-0b699212f090 in-use/MS1, preparedimage vk-ms1-sql-base absent. Interrupted step4 command had not created thatimage; no running controller detected. No repeatstep4 or large cloud mutations in this small-DB rollout.
