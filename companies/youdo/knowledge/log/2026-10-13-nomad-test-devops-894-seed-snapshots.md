---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, elasticsearch, vk-cloud, cinder, DevOps-894]
---
# DevOps-894 VK Elasticsearch seed snapshots

## Summary

User-approved snapshots of both prepared VK ES seed disks completed. Both snapshots are available (100%); original filesystems were cleanly unmounted during creation and remounted successfully. Clone/ES boot validation remains unperformed.

## Task

DevOps-894: preserve prepared-data recreation when migrating Nomad Elasticsearch from Yandex Cloud to VK Cloud.

## Context

Seed disks on share-test01 (10.18.26.4) contain checksum-verified cold copies of Elasticsearch 6.8.23 data. Root staging copies remain at /data/elastic-staging/{thin,thick}. User explicitly approved the concrete two-snapshot operation with "Да" after the named operation was presented.

## Actions

Executed `python3 ~/ai-data/nomad-es-vk-transfer/snapshot_seeds.py --apply`. Guarded cloud disk identity and attachment, filesystem UUID and absence of active filesystem users. For each disk: unmount, create Cinder snapshot with force=true (disk remains attached), wait for available, remount in finally. Exit 0. Separate subsequent GET requests and mount checks verified both results.

## Findings

| Variant | Snapshot name | Snapshot UUID | Size | Source Cinder volume |
| --- | --- | --- | --- | --- |
| thin | vk-ms1-share-base-thin-20261013 | c249047d-e6c3-4b9f-b78a-a1ceef11c206 | 5 GiB | ad66e572-b39a-4ed7-86a6-eb5a094763cb |
| thick | vk-ms1-share-base-thick-20261013 | bb8ea2de-2484-4169-9438-df5352643bd4 | 40 GiB | 6b8a8094-227f-4eb2-968c-5469e98fd92c |

Both snapshots status=available, progress=100%, project=6929552e493f46b899798519f279be0b. Thin and thick filesystem UUIDs match their original seed filesystems at /data/elastic/thin and /data/elastic/thick. No target Elasticsearch startup or CSI snapshot restoration was performed.

Read-only Nomad readiness: vk-csi controllers/nodes healthy 8/8; all controllers advertise snapshot creation/listing and clone support. Agents report Nomad 1.5.3; workstation CLI 1.3.5. Planned clone provisioning uses API SnapshotID rather than relying on the old CLI HCL parser. Source ES APIs at 172.24.0.19:9201 (thin) and :9202 (thick) report 6.8.23, yellow health, 21 active primary shards, five indices and five aliases each. Actual clone compatibility remains unverified.

## Changes

Two retained cloud snapshots created; temporary unmounts restored. Local helper and non-secret state are at ~/ai-data/nomad-es-vk-transfer/snapshot_seeds.py and snapshots.json. No repository, DAG, AWX or running Nomad application changes. No previous snapshots deleted. Credentials remain in their existing access locations and are not recorded here.

## Limits

Snapshot readiness confirms cloud artifact creation, not Elasticsearch index integrity. A separately approved temporary clone/boot/comparison/cleanup operation is needed. Weekly producer copy and publication automation still require repository/AWX changes under the supervised branch workflow. Backlog is maintained in ~/ai/TODO.md.

## Portable lesson

none
