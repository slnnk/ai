---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, elasticsearch, vk-cloud, csi, ansible]
---
# DevOps-894 Elasticsearch deployment migration to VK Cloud: analysis and plan

## Summary

Read-only analysis for [DevOps-894](https://youtrack.youdo.com/issue/DevOps-894). The user explicitly selected preserving disk recreation from prepared Elasticsearch data. Current deployment purges the job, deletes the Yandex disk and clones a thin/thick Compute image. Recommend Cinder snapshots in VK with CSI-managed create/delete using plugin `vk-csi`; substituting a plugin ID alone loses the prepared data. Empty-volume lifecycle is verified by DevOps-893; snapshot cloning and Elasticsearch recovery remain unverified. No repository files, infrastructure or task state changed.

## Task

Analyze `~/git/automation-test-yandex` and prepare a scoped migration plan for Elasticsearch deployment from Yandex Cloud to VK Cloud with a different CSI driver.

## Context and approvals

- User approved analysis/planning only and chose “preserve recreation from prepared data”; task ID supplied as DevOps-894.
- Existing checkout: `DevOps-889-recover-mssql-vms`, tracking `origin/master`; unrelated MSSQL edits and untracked `mssql_inventory.ini` preserved.
- Proposed future branch: `DevOps-894-deploy-elasticsearch-on-vk`, repository `~/git/automation-test-yandex`, base `origin/master`. Initially unapproved at analysis time; user approved this exact branch/base and local playbook edits later on 2026-10-13. See [implementation approval and evidence](2026-10-13-nomad-test-devops-894-playbook-adaptation.md).
- Plan stored in the company work log rather than the repository to preserve the analysis-only scope. No approval for deployment, commits, push or MR publication was requested or obtained.
- References: [previous Yandex destination review](2026-10-10-nomad-test-elasticsearch-recovery-destination-review.md), [VK SSD lifecycle](2026-10-13-nomad-test-devops-893-vk-ssd-lifecycle.md), [platform map](../systems/nomad-test.md).

## Actions and key commands

Ran `~/ai/general/scripts/ai-sync.sh` (no output/reminders), KB keyword searches, read-only repository status and targeted line reads. Delegated multi-file repository and VK evidence inspection as required by user instructions. Checked official Nomad volume documentation and Cinder v1.34.1 controller source. Local `nomad version` is 1.3.5; `nomad volume create -help` and `nomad volume delete -help` confirm both commands exist and deletion requires a registered, unused volume. This does not verify snapshot parsing or the controller/server version. No live API calls or deployment checks performed for DevOps-894.

## Findings

| File / lines (relative to repository) | Current behavior | Required migration |
| --- | --- | --- |
| `playbooks/deploy/docker/deploy_es_nomad.yml:8-119` | Purge job, deregister volume, delete YC disk, recreate from base image | Replace cloud disk lifecycle with Cinder-aware CSI lifecycle |
| Same file `:70,91,101,110,119` | YC CLI lookup/delete/detach/create; zone `ru-central1-b`; source `yc-csi-es-base-{{ instance_type }}` | Remove YC calls from the VK path; use snapshots per instance type |
| `playbooks/deploy/docker/files/nomad_es/yc-csi-es-volume.hcl.j2:2-14` | Plugin `yc-csi`, `external_id=disk_id`, `typeID`, `FolderId` | Use plugin `vk-csi`; provision with Cinder parameters instead of registering a YC disk |
| `playbooks/deploy/docker/files/nomad_es/es_thin.j2:24-38`, `es_thick.j2:24-38` | Volume source/mount `{{ instance }}-yc-csi-es` | Keep registered ID, source and mount alias consistent |
| Same thin/thick templates `:92-94,131-132` | Service names use `yandex-test.youdo.local` | Target VK service domains from scoped variables |
| `playbooks/deploy/docker/recreate_es_base_image.yml:9-38` | Delete/recreate two YC Compute images from seed disks | Prepare versioned Cinder snapshots of VK seed volumes |
| `group_vars/all.yml:5`, `inventories/autotest/group_vars/all.yml:2`, `test_inventory.sh:2` | Yandex DC and inventory entrypoint | Provide explicit VK inventory/variables without changing unrelated global targets |
| `playbooks/deploy/docker/files/nomad_es/es_public-test.j2:40` | Host bind mount `/data/elastic/data` | Preserve separate non-CSI path |

Existing teardown defects in the touched playbook: line 79 has invalid Jinja; lines 77-84 retry `debug` with stale disk state; lines 88-110 do not retry deletion after detach. Several errors are ignored and force deregistration is automatic. `--tags run_es` needs `disk_result` populated by a skipped task. Fixed sleeps do not prove allocations/claims are released.

Verified target from local deployment evidence: DC `vk-test`, default namespace, Nomad `http://nomad.service.vk-test.consul:4646`; plugin `vk-csi`, provider `cinder.csi.openstack.org`, image v1.34.1. Dynamic provisioning passed for `type=ceph-ssd`, `availability=MS1`, `ext4`, `single-node-writer`, `file-system`. Other available disk types were listed but not lifecycle-tested. CSI owns its cloud authentication via Vault `secret/admin/vk-csi`; ES templates need no cloud password.

## Proposed implementation plan

**Goal:** Recreate each selected VK stand's Elasticsearch volume from prepared thin/thick data and run its existing Nomad container.

**Architecture:** Use a Cinder snapshot per data variant and let Nomad/Cinder CSI create, attach and delete stand volumes. Preserve existing Elasticsearch versions, resources, mount path and reset semantics. Ordinary `run_es` must discover/use the existing registered volume; it must not require the previous create task's output.

**Constraints:** Minimal changes to the ES deployment path and required inventory inputs only. Keep `public-test` outside CSI conversion. No general cloud abstraction or unrelated cleanup. No global default/DC switch for other services. All runtime mutations require explicit command approval; training publication approval is separate.

### 1. Establish the VK data source and runner prerequisites

Before implementation, identify the authoritative prepared thin/thick datasets and the source/destination access route. Existing Yandex source sizes were 5/40 GiB; verify real imported filesystem and snapshot sizes rather than hardcoding those historical values. Confirm the controller's actual Nomad CLI/server versions and snapshot/create/delete support. The successful earlier test used the HTTP API; do not assume every old CLI supports the same request fields.

The user later recalled a weekend DAG preparing the data, probably in `dags-admin`/`dags_adm`. First trace that producer, its dataset definition, latest successful run and output storage. Prefer regenerating the same datasets on VK seed volumes through the established producer, or restoring a supported Elasticsearch repository snapshot. A stopped-volume cold transfer is a conditional fallback requiring independent validation; it is not a supported Elasticsearch backup method. Never copy active Elasticsearch data directories. Preserve the source and verify target ES version, directory layout, ownership, indices and expected documents. Stop the seed writer and release the mount before taking a Cinder snapshot. A Yandex Compute image ID is neither a Cinder snapshot ID nor an Elasticsearch repository snapshot. [Elasticsearch 6.8 snapshot/restore](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/modules-snapshots.html) is the supported cluster backup/transfer route.

Acceptance: two available Cinder snapshots in the CSI service account's project; each can create a separate disposable volume, mount read/write and start the corresponding ES image with expected indices/documents. Creation, removal and seed import each need runtime authorization. Until this passes, snapshot-based migration is a proposal, not verified functionality.

### 2. Define scoped configuration and volume template

Files: `deploy_es_nomad.yml`, `files/nomad_es/yc-csi-es-volume.hcl.j2`, thin/thick templates; create `inventories/vk_es/hosts` and `inventories/vk_es/group_vars/all.yml` using `inventories/autotest/hosts` as the structural reference. Populate only user-selected stands with `instance`, `instance_type` and local connection. Rename the CSI template to `es-csi-volume.hcl.j2` and update its one caller; do not rename the repository.

Define `dc=vk-test`, `es_nomad_namespace=default`, `es_csi_plugin_id=vk-csi`, `es_volume_id={{ instance }}-vk-csi-es`, `es_disk_type=ceph-ssd`, `es_disk_availability=MS1`, and `es_base_snapshot_ids` / `es_volume_sizes_gib` maps keyed by `thin` and `thick`. Snapshot UUIDs and sizes come from step 1. Both capacity bounds must specify the same requested GiB size, at least the seed snapshot size. Keep `dc`/credentials compatible with existing inventory inputs. Do not place secret values in generated HCL or notes.

For creation, render `snapshot_id`, `capacity_min/max`, plugin ID, namespace, filesystem capability and `parameters { type=... availability=... }`; remove `external_id`, `typeID` and `FolderId`. Update thin/thick sources and mounts together; retain `/usr/share/elasticsearch/data` and `elasticsearch:6.8.23`. Define `es_service_domain=vk-test.youdo.local` in the VK inventory and replace the three hardcoded domain suffixes with this variable, preserving each existing hostname prefix. Keep the current domain as fallback for other inventories. `test_inventory.sh` calls `http://dyninv.yandex-test.youdo.local/`; its generator is absent here, so use the explicit local VK inventory instead of modifying that shared script. Obtain `nomad_token` through the approved VK secret route at execution, without storing the value in inventory.

Acceptance: render both variants with synthetic UUIDs and assert matching volume IDs, namespace/DC, Cinder parameters and snapshot selection; no YC parameters remain in the VK output. Render the public-test template unchanged. Compile all touched Jinja expressions; YAML syntax-check alone is insufficient.

### 3. Replace teardown/provision and repair independent tag execution

File: `deploy_es_nomad.yml`. Preflight selected stand/type, endpoint, ACL/namespace, healthy plugin, source snapshot, requested capacity and mount compatibility before stopping anything. Use one stable volume identity and explicit namespace in all volume commands. Confirm reset affects only the selected stand, never either seed volume/snapshot.

Sequence: stop/purge selected ES job; poll fresh allocation and CSI claim state until released; delete the registered backing volume through `nomad volume delete` while its registration is still available; confirm cloud deletion; deregister any remaining Nomad record if necessary for the deployed version; create the replacement from the selected snapshot; confirm usable registration; validate/plan the rendered job; run it and check ES readiness. Do not deregister first and lose the backing volume reference. No automatic force deregistration or manual Nova detach fallback; stop with diagnostics on unexpected claims/errors. Treat genuine absence idempotently, but do not swallow authentication/network errors.

Keep current full-run reset behavior and documented tags. `run_es` should load an existing Nomad volume directly and fail clearly if absent. `create_disk` must not silently delete an existing disk. `remove_disk` must verify claim release even when `stop_es` was skipped. Retries query fresh state, have bounded timeouts and do not repeat destructive calls after ambiguous responses without first reconciling IDs. Remove obsolete YC-only debug/detach tasks with the invalid Jinja expression.

Acceptance: isolated command/API fixtures cover first deployment (no old job/volume), reset, run_es-only, busy claims, unavailable snapshot, permission denial and interrupted create/delete. Busy/invalid-source cases must perform no subsequent create/run. A reset creates exactly one volume per stand; source snapshots remain intact. Keep fixture tests outside the repository unless the project has a suitable existing test convention; do not add general test tooling for this task.

### 4. Adapt base data refresh

File: `recreate_es_base_image.yml`; preserve entrypoint to avoid changing callers without evidence. User confirmed the playbook was executed through AWX in TWO stages (corrected initial recollection of three), and that this AWX instance was in Yandex and is currently unavailable. Code contains `delete_image` and `create_image`; exact historical AWX template names, settings and schedule are not retrieved. Treat base publication as an AWX/playbook responsibility following DAG data delivery, not as an established task inside `DBA_Clean`.

Replace YC image handling with a documented seed-volume-to-Cinder-snapshot workflow. Preserve the two functional stages: replacement snapshot publication and obsolete artifact cleanup. Create a versioned replacement snapshot from a quiesced seed and wait until available. Validate a disposable restored clone before switching the configured UUID; execute cleanup only after that succeeds. Do not delete the current source first; obsolete snapshots may be removed only when specifically approved and unused by configured deploys. Snapshot IDs and success state must persist across AWX jobs rather than relying on pod-local `/tmp` or Ansible facts from another job. Exact AWX restoration/migration is a dependency to review separately; no AWX infrastructure changes authorized by the analysis request.

Acceptance: refresh failure leaves the previous usable snapshot selected; thin/thick point to their corresponding dataset; a changed source passes the same ES data checks as step 1. Limit removal of obsolete code to the touched YC workflow.

### 5. Validate and publish/run only after review

Local checks: `ansible-playbook --syntax-check` and `--list-hosts` using the explicit VK inventory and one stand limit; offline Jinja render/parse of both variants and public-test; `nomad job validate` of rendered jobs with the intended CLI; fixture checks from steps 2-4. No production/remote `--check` claim: command tasks and inventory generation can behave differently, so inspect them before execution.

Read-only preflight: endpoint/DNS from the actual controller, plugin health, node capacity, namespace ACLs, Cinder quota/types/AZ and source access. `nomad job plan` verifies the rendered schedule but cannot prove attachment or data integrity.

After reviewed runtime approval, pilot one named stand: restore expected indices/documents, Consul check passing, retained data after container restart, full reset from the same source and no leftover disk/claims. Then review any broader rollout separately. A container rollback cannot recover a deleted stand disk; the immutable base snapshot is the reset recovery source.

Publication proposal for future review: commit `adapt elasticsearch deployment to vk cloud`; MR `DevOps-894 Deploy Elasticsearch on VK Cloud`; source `DevOps-894-deploy-elasticsearch-on-vk`, target `master` (confirm observed project settings at implementation). Describe the final implemented scope in one Russian paragraph plus the task link, following training rules. Actual diff, check outcomes and CI effects must be reviewed before publication; these names are proposed and unapproved.

## Prepared-data producer follow-up

User recalled a weekend DAG, probably in `dags-admin`. Read-only fetch updated `dags_adm` origin/master to `2344385` dated2026-10-13; it has no matching ES seed producer. Deployed Airflow inspection was not completed: sandbox SSH was denied and the escalated attempt's approval was aborted. This is an access limit, not evidence that the DAG is absent from Airflow.

A matching producer was found in `~/git/dba/airflow_dags/mssql_clean_jobs.py`: DAG `DBA_Clean`, cron `12 12 * * 6` (Saturday; wall-clock timezone must be checked in Airflow because the code uses naive datetimes). The user independently recalled the name as `DBA_CLEAN`. Read-only fetch established current origin/master `37d5330` dated2026-10-09; its destination is already `10.16.28.4`. The local task checkout remains unchanged; deployed Airflow freshness is unverified. It has `clean_elastic_reindex` and `preseed_elastic_reindex`, each followed by ES data copy. The producer selects `clean_run_environment`, default `test`, and resolves source hosts through `backup_server_<environment>` / `ssh_dba_svc_root_<environment>`. Copy tasks instead use the hardcoded `backup_server_prod` connection; resolve this discrepancy before changing destinations.

- Thick: SQL `CleanYouDo` → source Elasticsearch port9202 → `clean_elastic_copy_test`: stop `elasticsearch1`, copy `/backup/sql/elastic/data/` to `root@10.16.28.4:/data/elastic/thick/` with `rsync --delete`, restart source container.
- Thin: SQL `YouDo_preseed` → source Elasticsearch port9201 → `preseed_elastic_copy_test`: stop `elasticsearch_smalldb_1`, copy `/backup/sql/elastic_smalldb/data/` to `root@10.16.28.4:/data/elastic/thin/` with `rsync --delete`, restart source container.
- The reindexer image is `registry.youdo.sg/youdo/youdo/elastic_reindexer:latest`; it builds executors, landings, suggestions and tasks from prepared SQL data.
- Copy tasks stop and restart source ES containers around rsync. This is historical cold-directory preparation, not an Elasticsearch repository snapshot backup.
- The Ansible image playbook separately creates YC Compute images from `yc-csi-es-base-thick/thin` disks. Matching mount paths, actual disk UUIDs and the orchestrator connecting data copy to image creation have not been verified. Do not assume the Airflow DAG invokes that playbook.

User correction: `10.16.28.4` is the Yandex destination and is probably unavailable. Treat its unavailability as a planning assumption, not a measured outage. Access to that host, its disk mapping and old YC images is NOT a prerequisite for VK recovery.

Refinement of plan step1: start from the producer-side Airflow Connections and verify the source datasets in `/backup/sql/elastic/data/` and `/backup/sql/elastic_smalldb/data/` on the actual backup source. Check timestamps, latest successful reindex task results and matching SQL dataset versions; a failed Yandex copy does not by itself prove source preparation failed or succeeded. Confirm the source containers' current state before any approved stop/copy work. If usable prepared data remains, use it as the VK seed source. Otherwise verify SQL `CleanYouDo`/`YouDo_preseed`, reindexer image and source ES dependencies, then regenerate through the existing preparation chain under separate runtime authorization. Do not trigger the whole DAG with its old destination.

Choose a reachable VK staging host with two separate base volumes; verify the mount/device identities there before any copy with `--delete`. Update only the ES copy destination and the snapshot publication stage. After a successful copy or supported ES snapshot restore, verify each base dataset, release its writer/mount, create a versioned Cinder snapshot and test a disposable cloned stand. For subsequent refreshes keep the previous snapshot UUID selected if preparation or clone validation fails. Preserve SQL/ES dataset generation consistency, especially for matching thick/thin MSSQL test stands. Historical producer→YC image mapping can be investigated later if needed; it does not block this source→VK path.

This discovery adds a second repository to potential implementation scope (`dba`) and requires its own approved task branch before edits. It does not authorize modifications to the rest of `DBA_Clean`, Airflow connections or DAG triggering.

AWX clarification: the user recalled image refresh through the Yandex AWX instance, now unavailable, and finally confirmed two stages. This aligns with the playbook's `delete_image` / `create_image` tags but does not establish retrieved AWX job definitions. Full target delivery is DAG preparation → VK base disks → AWX/playbook snapshot refresh → Nomad stand recreation. Weekly refresh must be retained; regular refresh timing/dependencies need reconstruction from AWX export/backup or user settings. Fresh `dags_adm` backup code points to newer AWX databases; a historical checkout referenced old test backup `/data/backup/awx-test/` on the `msk3-backup02` connection with seven-day retention. Existence/content of historical backups is unverified and not a prerequisite for source-data recovery.

## Alternatives and limits

Source-presence prerequisite subsequently confirmed by read-only SSH to `backup_server_prod`172.24.0.19: both `nodes` directories exist and are mounted into running ES6.8.23 containers. User stated dates do not matter for this stage; do not block seed preparation on freshness. [Source check](2026-10-13-nomad-test-devops-894-es-source-check.md) records actual sizes and limits. Select VK seed destination next; do not copy active source files without the reviewed consistency procedure.

Subsequent user-selected destination:10.18.26.4 (`vk-ms1-share-test01.mcs.local`), SSHyoudo. User explicitly selected system-disk staging; `/data/elastic/thin` and `/data/elastic/thick` were created and verified on `/dev/vda1`,239.48GiBfree. This replaces separate-volume attachment as a prerequisite for initial staging, but not the need to produce standalone ES data disks for the proposed Cinder snapshot design. No data transfer or container/snapshot action authorized/performed.

Later user-approved transfers completed separately: [thin](2026-10-13-nomad-test-devops-894-thin-transfer.md)120572815bytes and [thick](2026-10-13-nomad-test-devops-894-thick-transfer.md)22667132593bytes. Bothcold copies checksum/metadata match sources; both source ES containers restarted/runningtrue; heapdump excluded. Prepared-data delivery toVK staging is complete. Separate Cinder seed disks, snapshot creation/clone testing, target ES validation and repository/DAG adaptation remain unperformed and require their applicable approvals.

Next-stage [preflight](2026-10-13-nomad-test-devops-894-seed-disk-preflight.md) confirms the two dedicated seed disks already exist onshare (5/40GiBceph-hdd/MS1, sameCSIproject); no new disk creation needed. Actual historical mount playbook maps those roles to `/data/elastic/thin` and `/data/elastic/thick`; preserve those paths rather than provisional/mnt or/public layout. Move/preserve system-disk staging before mounting. Thin needs reviewedext4format; thickexistingext4 can be reused/remounted withoutformat. Originalceph-ssd default is superseded for these existingceph-hdd seeds; clone volume type must be tested before final runtime parameter choice. No seed format/mount/fill performed yet.

Later approvals/execution: thin formatted separately, then allfourmount/fillpoints explicitly approved and [completed](2026-10-13-nomad-test-devops-894-seed-mount-fill.md). BothCinderseedfilesystems populated and checksum/metadata verified at historicalESpaths; rootstagingcopies retained;UUIDfstabrows persisted withbackup andotherrows preserved. This completes seed filesystem preparation only. Snapshotcreation/clonevalidation/ESboot andDAG/repositoryadaptation remain next separatelyauthorizedstages.

Recommended: native Cinder snapshot + CSI create/delete, which avoids cloud credentials on the Ansible controller and covers the tested CSI management path. Alternative: create a volume via OpenStack from a Glance image and register `external_id` with Nomad; useful if image import is mandatory, but requires separate controller credentials/tooling and dual lifecycle ownership. Empty disk with separate data load was not selected by the user. Snapshot consistency, source availability and data compatibility remain prerequisites, not assumptions.

Official references: [Nomad CSI specification](https://developer.hashicorp.com/nomad/docs/other-specifications/volume/csi), [volume delete](https://developer.hashicorp.com/nomad/commands/volume/delete), [volume deregister](https://developer.hashicorp.com/nomad/commands/volume/deregister), [Cinder v1.34.1 CreateVolume source](https://github.com/kubernetes/cloud-provider-openstack/blob/v1.34.1/pkg/csi/cinder/controllerserver.go). The driver accepts type/availability and snapshot/volume content sources; its CreateVolume path does not pass a Glance image source in the inspected version. Recheck CLI syntax/capabilities against the installed Nomad version before implementation.

## Changed files and risks

Only this log, the existing Nomad platform map, repo catalog, live TODO and generated KB indexes were updated. Repository status remained unchanged. No live DevOps-894 API reads, snapshot creation, Elasticsearch checks, syntax checks of future code or deployment were performed. Verified status applies to source analysis and prior evidence, not to the proposed migration.

## Portable lesson

none
