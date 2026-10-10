---
system: nomad-test
status: verified
checked: 2026-10-10
tags: [nomad, elasticsearch, recovery, yandex-cloud]
---
# Elasticsearch recovery: Ansible disk destination dependencies

## Summary
Read-only review of automation-test-yandex Elasticsearch Ansible finds hardcoded zone-b disk creation and the old folder in the CSI volume template. Recovery into ru-central1-a/test-platform-folder requires minimal destination changes and explicit source-image access. Nomad logical datacenter and endpoint remain yandex-test, conditional on unchanged runtime configuration. No code or infrastructure changes were made. Live read-only /v1/nodes and /v1/jobs with NOMAD_YANDEX_TEST_TOKEN returned HTTP 403, so current topology and jobs are unverified.

## Task
Assess whether existing Elasticsearch deployment automation needs recovery changes before use with recovered Yandex test Nomad infrastructure.

## Context
Repository /home/slnnk/git/automation-test-yandex. Existing entrypoint: `ansible-playbook -i test_inventory.sh playbooks/deploy/docker/deploy_es_nomad.yml -l test19`. Targets inventory group docker and requires per-stand instance/instance_type; mssql_inventory.ini is unsuitable. Existing unrelated MSSQL local changes were preserved.

## Actions
Read-only tracing of the playbook, four ES templates and selected variable keys; inspected repository status without mutations. Ran YAML syntax-check with dummy localhost inventory (docker unmatched warning) and isolated Jinja compilation of the existing detach-debug expression. Runtime API GET attempts returned HTTP 403; no topology/job conclusions are drawn from these responses.

## Findings
- playbooks/deploy/docker/deploy_es_nomad.yml:119 creates instance-yc-csi-es from yc-csi-es-base-instance_type in hardcoded ru-central1-b. Explicit target folder and source image folder/ID are absent. Existing thin/thick image availability and appropriate data are runtime dependencies.
- Folderless disk get/delete/get/detach commands occur at lines 70/91/101/110. They inherit the YC CLI profile destination; lookup/destructive commands must be reviewed for target-folder scope.
- playbooks/deploy/docker/files/nomad_es/yc-csi-es-volume.hcl.j2:14 hardcodes FolderId b1gnfk02b6vos0csupua. Plugin yc-csi and external_id=disk_id bind the generated volume to the created disk.
- CSI template line 13 declares typeID=network-hdd; disk-create command has no explicit --type, so actual disk type/default and source-image size must be verified. Latest zone-a HDD quota is 511 GiB limit / 505 GiB usage / 6 GiB free (548682072064 / 542239621120 bytes). The older 11:39 quota request includes desired HDD-a 1000 GiB and is processing; the latest 13:22 request covers CPU/RAM/SSD only. Do not assume the HDD request is approved.
- group_vars/all.yml:5 sets dc=yandex-test. Nomad commands address nomad.service.dc.consul:4646; templates use dc as datacenter. No explicit namespace or node/zone constraint is present. Do not replace the logical datacenter solely because master IPs changed.
- Full invocation stops/purges the stand ES job, deregisters CSI volume, deletes its old disk, clones a base image and registers/runs the replacement. It is not a read-only deployment check.
- --tags run_es alone depends on disk_result.stdout from create_disk (lines 128-132). Selected create_disk/run_es workflow needs shared results or a separately requested minimal existing-disk lookup.
- Existing debug template at line 79 has an extra closing parenthesis; isolated Jinja compilation reports unexpected ')'. YAML syntax-check passes but does not validate this runtime expression.

## Changes
Only knowledge-base log, existing infrastructure map and the single TODO list were updated. No repository adaptation, publication or runtime mutation was authorized or performed.

## Risks and limits
Validate zone-a Nomad clients, yc-csi controller/node readiness, image access, disk quota, ACL/namespace and intended data-source freshness before any reviewed runtime action. HTTP 403 on read endpoints is an authorization limitation, not proof of missing nodes or jobs. Runtime topology remains unknown.

## Portable lesson
none

## Runtime recheck after user token update (2026-10-10)

Direct loading of the refreshed `NOMAD_YANDEX_TEST_TOKEN` from `~/ai/current/.env` restores GET access. The existing dotenv helper uses `os.environ.setdefault`, so an inherited old token produced transient repeat 403s until the file value was used explicitly. No token value was printed or stored. Nomad reports eight `yc-a-nomad-agent-test-01` through `-08` clients, all `ready`, scheduling `eligible`, datacenter `yandex-test`. The `yc-csi` plugin has 8/8 healthy controllers and 8/8 healthy nodes. GET jobs across all namespaces returned no Elasticsearch jobs, and CSI volume listing across all namespaces returned no ES-named volumes. Node Attributes/Meta exposed no zone field in the filtered check; do not treat the hostname prefix alone as control-plane zone verification. The destination code changes identified above remain necessary. No runtime or repository changes were performed.

## DevOps-889 scope expanded by user (2026-10-10)

Read-only YouTrack GET confirms title `[Recovery] Восстановить ВМ MSSQL с большой БД и elasticsearch`, state `In Progress`. Description retains MSSQL stands `test`, `test1`, `test6` and adds Elasticsearch recovery in Nomad; Elasticsearch stand selection is not explicitly specified. Proposed local implementation: reuse repository `/home/slnnk/git/automation-test-yandex`, branch `DevOps-889-recover-mssql-vms` targeting `master`; extend minimal destination changes in existing `playbooks/deploy/docker/deploy_es_nomad.yml` and `playbooks/deploy/docker/files/nomad_es/yc-csi-es-volume.hcl.j2`. New-scope branch reuse/local edits need explicit supervised-stage confirmation before repository modifications. No publication or runtime authorization inferred from ticket edit.

## Verified capacity update (2026-10-10)
Source-folder image metadata: yc-csi-es-base-thick fd8gd3kceh80hfvdsick READY, minimum disk 42949672960 bytes (40 GiB); yc-csi-es-base-thin fd86u1lns6d3sujfjms0 READY, minimum 5368709120 bytes (5 GiB). Local group_vars/test.yml, test1.yml and test6.yml choose thick. If ES recovery targets the same three MSSQL stands, ES disks require 120 GiB; the user has not explicitly selected ES stands, so this scope is conditional.

Current zone-a HDD usage 505 GiB/limit 1100 GiB leaves 595 GiB. Conditional ES alone 120 GiB fits; MSSQL temporary base 400 GiB plus ES 120 GiB fits with 75 GiB remaining. After base deletion, final MSSQL 1200 GiB plus ES 120 GiB needs absolute HDD limit 1825 GiB. Proposed 2000 GiB leaves 175 GiB after these allocations at the current baseline.

Three thick ES jobs reserve 8064 MB (7.875 GiB), with combined memory maxima 15744 MB (15.375 GiB). Each count 1 job main task reserves 2560 MB/max 5120 MB and head reserves 128 MB/100 MHz CPU. Main CPU is unspecified; local no-submit job rendering preserves CPU:null, so total CPU default remains unverified. Live Nomad checks show eight ready clients; per-node free RAM 67.621-77.695 GiB and CPU 26264-31300 MHz using full allocations. These observations provide ample nominal memory/CPU headroom for the three jobs, but do not prove CSI disk topology placement, volume readiness or successful application startup.
