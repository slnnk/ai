---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, elasticsearch, vk-cloud, cinder, DevOps-894]
---
# DevOps-894 VK ES snapshot clone validation

## Summary

Both VK seed snapshots successfully restored through vk-csi into temporary 5/40 GiB ceph-hdd volumes. Elasticsearch 6.8.23 started on both clones. All source index names, UUIDs, Lucene document counts, primary/replica configuration, aliases and active primary shard counts matched. Both temporary jobs were stopped/purged and clone volumes deleted with cloud/Nomad 404 verification. Source seeds and snapshots are retained.

## Task

DevOps-894: validate prepared-data restoration before adapting the deployment playbook for VK Cloud.

## Context

User requested "Проверь" after the concrete next stage was described: temporary CSI clones, isolated ES 6.8.23 startup and index comparison. Scope and automatic deletion of test jobs/clones were stated before execution. No production jobs or producer containers were modified during this validation.

## Actions

Prepared minimal local helper and HCL outside repositories, then ran `python3 ~/ai-data/nomad-es-vk-transfer/validate_clones.py run --apply`, thin then thick. Command completed exit 0. Nomad API volume create used top-level SnapshotID, explicit 5/40 GiB capacity, plugin vk-csi, single-node-writer/file-system, ext4, ceph-hdd, MS1. Cinder clone snapshot_id/type/size checked before startup.

Jobs devops-894-es-check-thin and devops-894-es-check-thick used elasticsearch:6.8.23 with the existing deployment's configuration/memlock settings and variant heap sizes (512 MiB/2 GiB), writable clone mount at /usr/share/elasticsearch/data and unique single-node clusters. No Consul/Traefik services registered. Inherited Consul/Vault tokens cleared before submitting job JSON. Metadata-only source GET requests on 172.24.0.19:9201/9202; no documents collected.

Offline Python compilation and both HCL parse/validation commands passed, zero warnings; local validation could not validate the remote Docker driver. Actual successful startup subsequently verified the runtime path. Worker08 read-only readiness: vm.max_map_count=1048576, 59443 MiB available memory, Nomad ready/eligible and not draining.

## Findings

| Variant | Version | Indices / aliases | Primary shards | Lucene docs.count total | Health | Metadata match | Cleanup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| thin | 6.8.23 | 5 / 5 | 21 | 340668 | yellow | true | verified |
| thick | 6.8.23 | 5 / 5 | 21 | 74235448 | yellow | true | verified |

Both report 27 unassigned shards, matching the source single-node baseline; all 21 primary shards are active. The comparison uses _cat/indices docs.count, which includes nested Lucene documents and is not a business-level document count. Recovery/startup and metadata comparison passed; no exhaustive scan of every document was performed.

Thin clone Cinder UUID 745d09dc-d22e-42a6-8c02-dd1fe72b6308, allocation cef9e282-b10b-50b6-1c4c-8c94aa10a159 on node19c8032d-d68e-144d-d1f0-7e716e394870. Thick clone UUID e898eded-46f2-41a6-b3b5-7738aa0250a3, allocation 1cc83d68-5886-5e7a-be00-854e81f1654f. Both clones deleted. Snapshots c249047d-e6c3-4b9f-b78a-a1ceef11c206 and bb8ea2de-2484-4169-9438-df5352643bd4 remain retained.

## Changes

Created, ran and removed only two temporary test jobs and two cloned Cinder disks. No repository, DAG, AWX or stand deployment changes. Local helper, generated HCL and baseline/actual metadata evidence: ~/ai-data/nomad-es-vk-transfer/validate_clones.py, devops-894-es-check-{thin,thick}.hcl, clone-validation.json. No credentials stored in these artifacts.

## Limits

Successful snapshot restoration does not itself migrate the deployment/playbook, weekly DBA_Clean copy or AWX publication chain. Those changes remain separate work under supervised repository approval. Backlog is maintained in ~/ai/TODO.md.

## Portable lesson

none
