---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, elasticsearch, vk-cloud, ansible, csi, DevOps-894]
---
# DevOps-894 Nomad-only ES deployment

## Summary

Deployment now communicates only with Nomad, with no Keystone/Cinder calls or cloud credentials. Nomad provisions/deletes/mounts stand disks through vk-csi. Snapshot UUID comes from Nomad CSI listing, selecting the latest ready snapshot for the exact thin/thick seed. Actual test/thick Ansible deployment succeeded after correcting reschedule defaults.

## Task

DevOps-894: satisfy user requirement that ES deployment depends only on Nomad, while retaining prepared-data recreation without manually maintained snapshot UUIDs.

## Context

User explicitly required the deployment playbook not use VK API and asked for Nomad to create the disk through the plugin. Base snapshot preparation remains cloud-aware. Prior fixed snapshot names still govern preparation/delete stages; the deployment lookup strategy changed because CSI snapshot listing does not expose provider names. This limitation and latest-ready-by-source strategy were stated to the user before implementing.

## Actions

Actual read-only Nomad GET /v1/volumes/snapshot?plugin_id=vk-csi&per_page=200 returned four snapshots, NextToken empty, with ID, ExternalSourceVolumeID, SizeBytes, CreateTime and IsReady. Name and SourceVolumeID were empty. The initially supplied source_volume_id query did not filter results; implementation explicitly filters ExternalSourceVolumeID client-side using stable seed IDs and chooses the maximum CreateTime among IsReady=true records.

Removed es_vk_auth include and every es_cinder reference from deployment tasks. Nomad URI create payload still uses SnapshotID, requested5/40GiB capacity and plugin parameters. Cloud access belongs to the existing plugin. Added existence handling for previous stand volume before deletion, because the first deployment has no volume to delete. No extra cloud/data/readiness preflight added.

Provider v1.34.1 returns from CreateVolume without waiting available; Nomad external-volume API cannot expose that state. Instead, attach failures use Nomad rescheduling delay5s/constant within the existing job deployment deadline. Explicit attempts0/interval0/unlimitedtrue avoid CLI1.3.5 default attempts3 conflicting with server1.5.3 validation. Removed the short-lived direct Cinder availability poll implementation before final deployment.

## Findings

Primary references: [Nomad CSI volumes API](https://developer.hashicorp.com/nomad/api-docs/volumes), [Cinder CSI CreateVolume/ListVolumes implementation](https://github.com/kubernetes/cloud-provider-openstack/blob/v1.34.1/pkg/csi/cinder/openstack/openstack_volumes.go#L55), [external volume fields](https://github.com/kubernetes/cloud-provider-openstack/blob/v1.34.1/pkg/csi/cinder/controllerserver.go#L381). Provider returns ID/capacity/attachments, without Cinder state or VolumeCondition; listing a volume cannot prove it is available. No async-disable setting exists in the inspected BlockStorageOpts.

Local syntax and both rendered job JSON parses pass. Three focused fixtures cover Nomad-only disk creation from the latest ready base snapshot, run_es-only success and propagated command failure; only /v1/Nomad endpoints are called. Real test/thick deployment through the Ansible entrypoint returned0, failed0 in60.037s. No standalone ES health/index checks.

## Changes

Changed tasks/es_vk_select_snapshot.yml, tasks/es_vk_deploy.yml, es_thin.j2/es_thick.j2 reschedule blocks and scoped README. Deployment requires only Nomad and optional Consul tokens. Cloud credentials remain necessary only in the separate preparation playbook. No cloud/provider/plugin configuration changes, Git commits, push or MR.

## Limits

Snapshot selection through CSI is by stable base-volume identity and latest ready creation time, not the unavailable provider Name field. Operator does not remember snapshot UUIDs. Prepared fixed names remain unchanged. Current snapshot list fits one page (four results, quota200); no migration to another storage backend implied. Backlog is in ~/ai/TODO.md.

## Portable lesson

none
