---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, csi, vk-cloud, recovery]
---
# DevOps-893 Cinder CSI deployment and startup diagnosis

## Task

User approved CSI apply with `Да`, then explicitly requested checking deployment. Diagnose actual runtime failures and prepare minimal local correction before requesting another runtime action.

## Context

vk-test root/state terraform/vkcloud-terraform; plugin uses existing admin Vault policy and user-requested secret/admin/vk-csi cloud_conf. All other7jobs deployed. No cloud disks or volume registrations authorized by this apply.

## Actions

Executed terraform_stage.py apply --service csi from reviewed saved plan:1add/0change/0destroy, registered plugin-vk-csi-monolith. GET verification:8activeallocationsfailedexit2, plugin vk-csi endpoint404. All7otherjobs activeallocationsrunning:mainAlloy8,traces1,exporter1,Jaeger8,SchemaRegistry1,Redis16,Traefik3.

Delegated bounded CSI stderr read. Exact failure: flag provided but not defined: -endpoint; Usage of /go-runner. Verified upstream v1.34.1 Dockerfile copies /bin/cinder-csi-plugin and sets CMD to it. Source: https://raw.githubusercontent.com/kubernetes/cloud-provider-openstack/v1.34.1/Dockerfile. Nomad args replaced CMD, so inherited wrapper received CSI flags without the binary command.

Prepared one-line local correction config.command=/bin/cinder-csi-plugin, preserving image/args/resources/Vault configuration. Nomad job validation passed; regenerated targeted update plan, not applied. No secret values or full logs printed/persisted.

## Findings

Initial failure is command dispatch, preceding CSI socket/API initialization. Missing socket is a consequence, not the root cause. Corrective deployment subsequently passed CSI startup and plugin health checks on all eight nodes. Disk operations remain untested. All other jobs remained running in the deployment check.

## Changes

User-approved runtime job creation plus necessary local command fix. No disks created, no Vault changes, no Git publication. Filtered diagnosis files under ai-data/nomad-vk-access; no network service address for CSI because it uses a local Unix socket. CSI uses local Unix socket only.

## Status

User approved corrective CSI apply with `Да`. Executed saved update:0add/1change/0destroy. Fresh GET verification after fingerprint propagation:8tasksrunning with Plugin became healthy events; vk-csi Provider=cinder.csi.openstack.org, NodesHealthy8/Expected8, ControllersHealthy8/Expected8, ControllerRequiredtrue. Prior8failedallocations remain historical; no manual cleanup required. Startup command correction resolved the actual failure. No cloud disks or test volumes created. CSI local-socket status recorded in service-addresses.env; there is no network endpoint to invent. Final full Terraform plan without resource targeting completed successfully: No changes. Infrastructure matches the configuration.

Initial failed allocations are historical. All eight configured jobs are deployed; the other seven jobs had 38 active running allocations in the deployment check. Disk lifecycle testing and Git publication remain outside the approved deployment action.

## Portable lesson

none
