---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, csi, vault, vk-cloud, recovery]
---
# DevOps-893 VK CSI credentials prepared in requested Vault path

## Task

User added VK_CSI_USER/PASSWORD/PROJECT_ID in current/.env and placed nomad-csi-openrc.sh in ~/downloads. User explicitly requested populating Vault at admin/vk-csi and using it for the plugin. Interpreted as secret/admin/vk-csi in the established secret KVv1 mount; announced that full path before execution.

## Context

CSI is the remaining undeployed Terraform job; root vk-test/state terraform/vkcloud-terraform. Nomad→Vault functional task startup already verified by main Alloy. Existing new-policy proposal vk-csi initially pointed to secret/vk/csi; user's destination correction supersedes that path.

## Actions

Parsed static OpenStack RC exports without executing the shell file. .env project identifier had13characters versus RC32hexUUID; corrected only VK_CSI_PROJECT_ID in local .env to RCprojectUUID needed for OpenStack scope. Service username matches RC. Credentials remain in .env; no values printed or persisted elsewhere locally.

Prepared cloud_conf in memory with [Global] auth-url/region/tenant-id/username/password/domain-name. AuthURL https://infra.mail.ru:35357/v3/, regionRegionOne, userdomainservice-users. Project/user identifiers and password omitted from notes. Updated plugin template to secret/admin/vk-csi and local proposed vk-csi policy to read that exact path.

Executed user-requested PUT secret/admin/vk-csi with singlefield cloud_conf:HTTP204. GET readback compared in memory and matched; secret content never printed/saved locally. Existing source secrets and unrelated Vault policies untouched. Prepared updated targeted CSI plan; no CSI apply.

## Findings

Requested Vault secret exists and plugin references it. Proposed policy file ~/ai-data/nomad-vk-access/vk-csi-policy.hcl grants only read at secret/admin/vk-csi. Policy publication is a separate external action awaiting approval; no policy created yet. Cloud API authentication/disk operations not tested and no disk created.

CSI candidate image registry.k8s.io/provider-os/cinder-csi-plugin:v1.34.1, monolith pluginIDvk-csi,500CPU/256MiB perclient, host network, unixsocket/csi/csi.sock. Source job reads cloud_conf into allocation secrets/cloud.conf mode0600. Cloud config fields follow upstream Cinder/OpenStack global config. Remaining execution needs policy publication then individually approved CSI apply/test.

## Changes

Local .env projectUUID correction, plugin Vault path update, local policy/helper preparation; user-authorized Vault secret creation. AuthURL/region recorded in nonsecret service-addresses.env as configured/unverified API access. No Git publication or Terraform apply.

## Status

User correction: existing admin Vault policy should be used. GET sys/policies/acl/admin200; its secret/* rule grants read among other rights, covering secret/admin/vk-csi. Changed plugin vault policies to [admin]. Separate vk-csi policy proposal withdrawn; no policy created/changed. Regenerated targeted CSI plan for this final configuration; user-approved secret unchanged, apply pending.

Vault credentials prepared/readbackverified. Separate vk-csi policy write and CSI deployment remain pending approval. Remaining work tracked in ~/ai/TODO.md.

## Portable lesson

none
