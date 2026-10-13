---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, alloy, vault, vk-cloud, recovery]
---
# DevOps-893 main Alloy deployment verifies Nomad Vault integration

## Task

User explicitly approved main Alloy apply with `Запусти`, including verification of the restored Nomad→Vault integration via a real secret-consuming job.

## Context

Masters' existing Vault credential synchronized from secret/ansible/yandex and reloaded after prior approval. Current root vk-test/state terraform/vkcloud-terraform; main Alloy uses existing shared module unchanged, including monitoring Vault policy and mandatory secret/monitoring/alloy-cloudwatch env template. No credentials or template hardening requested.

## Actions

Executed terraform_stage.py apply --service alloy with reviewed saved module.alloy plan:1add/0change/0destroy. GET verification:8/8activeallocations/tasks running,8alloy Consul registrations; each direct /-/ready and /metrics returns200. Output filtered to statuses/events/addresses; no template/token content fetched or printed. Recorded8direct endpoints in service-addresses.env.

## Findings

Alloy jobs started with mandatory Vault token and template hooks, establishing real task token delivery and secret rendering after master-token replacement. Image grafana/alloy:v1.19.1,100CPU/512MiB perclient, memory_max1536MiB. All8ready/metrics200. AWS secret fields were incomplete in prior audit, but did not prevent current source-as-is job startup; no optional CloudWatch reconfiguration performed.

Placement endpoints: agent01 10.18.26.34:28274;02 .38:25905;03 .37:25361;04 .30:26824;05 .15:24412;06 .10:27240;07 .21:27942;08 .35:31098. Host ports dynamic; map records observation snapshot and Consul discovery hostname. Readiness does not prove end-to-end remote log/metric delivery.

## Changes

Only approved main Alloy runtime creation and map/KB records. Shared module/config unchanged. No Git publication, CSI creation, cloud credential changes or extra runtime changes.

## Status

Main Alloy healthy8/8; functional Nomad→Vault startup verified. CSI is the remaining configured undeployed job; requires deferred VK Cloud credentials, secret/vk/csi cloud_conf and vk-csi Vault policy before an individually approved apply. No claim of full Terraform convergence yet; no CSI disks created. Remaining work in ~/ai/TODO.md.

## Portable lesson

none
