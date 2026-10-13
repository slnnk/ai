---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, alloy, vk-cloud, recovery]
---
# DevOps-893 VK Alloy traces deployment

## Task

User approved Alloy traces apply with `Да`. Deploy individually and maintain the service address map.

## Context

Approved DevOps-893 branch, vk-test root, Consul state terraform/vkcloud-terraform. Copied traces job has no Vault-secret-consuming template; unused Vault block removed before approved plan to avoid proven invalid-token dependency. Other config, image and resource behavior preserved apart from VK addresses.

## Actions

Executed terraform_stage.py apply --service alloy-traces with reviewed saved plan:1add/0change/0destroy. GET verification: allocation a3a0ac24-ae65-8cfb-2b13-d580d31b6cc4 running on vk-ms1-nomad-agent-test-03; Consul registrations alloy-traces10.18.26.37:28760 and alloy-otlp10.18.26.37:30254. Direct GET /-/ready and /metrics HTTP200. Recorded all observed endpoints and configured route names in service-addresses.env.

## Findings

Image grafana/alloy:v1.10.0,200CPU/512MiB, memory_max1024MiB, one allocation. Consul services registered; job defines no application health checks, so node check passing alone is not process-readiness evidence. Direct readiness/metrics succeeded. End-to-end trace/metrics delivery to configured backends not tested.

## Changes

Approved runtime creation only plus address-map/KB updates. No runtime fixes needed, no shared Vault edits, no Git publication. Trace job's removed unused Vault block already disclosed in approved preparation.

## Status

Alloy traces running/readiness verified. Remaining current Terraform scope: main Alloy module and Cinder CSI. Both need functioning Nomad→Vault integration under their current source configuration; CSI additionally needs VK Cloud credentials/secret/policy (user deferred cloud credentials). Track those prerequisites in ~/ai/TODO.md. No token creation, credential replacement or further apply authorized in this step.

## Portable lesson

none
