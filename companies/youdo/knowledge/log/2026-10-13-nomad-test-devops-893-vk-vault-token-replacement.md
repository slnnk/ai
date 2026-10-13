---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, vault, vk-cloud, recovery]
---
# DevOps-893 manual Nomad master Vault token replacement

## Task

User identified the existing nomad_vault_token field in Vault secret/ansible/yandex and explicitly requested manual replacement on every Nomad master and verification. This authorizes the three replacements/config reloads, not a further application deployment.

## Context

Masters10.18.26.11/.12/.13 have Vault integration enabled at the correct VK address. Old configured credentials consistently returned403invalid token. Ansible VK master inventory uses vault_secrets['yandex'].nomad_vault_token; the actual source is secret/ansible/yandex (KVv1). User suggested prior Ansible run lacked correct Vault integration; the precise historical cause was not established.

## Actions

Read existing source field through operator VK_TEST_VAULT_TOKEN; new token lookup-self200, policy root, TTL0. Value stayed in process memory and encrypted SSH stdin, never in command arguments, local files, logs or notes.

Ran replace_master_vault_token.py apply sequentially via youdo+sudo on all3masters. Changed only token string inside /etc/nomad.d/server.hcl Vault block. Atomic file replacement preserved owner/group/mode. Sent systemctl kill --kill-whom=main --signal=HUP nomad on each. Each change/reload succeeded; Nomad systemd service active and token lookup-self200 from every master.

Fresh masters_vault_probe.py confirmed on-disk tokens200 and effective Nomad VaultEnabledtrue/correctAddr/tokenconfigured on all3; effective API responses200. Source secret unchanged, no tokens created/revoked, no service restarts, no Ansible or Git changes.

## Findings

The existing Vault secret token is valid and differs from the invalid token previously configured on each master. Manual synchronization and config reload completed. Root-policy metadata records the user's existing secret choice; no secret value recorded. Real task-token derivation/secret rendering remains to verify with an actual secret-dependent job.

Prepared next main Alloy targeted plan from existing module:1add/0change/0destroy, system job alloy on8clients,100CPU/512MiB each, grafana/alloy:v1.19.1. It reads secret/monitoring/alloy-cloudwatch under monitoring policy and therefore provides functional verification of Nomad→Vault task token delivery. Earlier schema audit found missing AWS fields; source behavior preserved and any actual error will be diagnosed after approved apply.

## Changes

Runtime: only master server.hcl Vault token values and SIGHUP reloads, explicitly authorized by user. Local ai-data scripts/filtered verification artifacts plus KB bookkeeping. No new service addresses observed. No Terraform apply for main Alloy yet.

## Status

Three-master token replacement/config reload verified. Next main Alloy apply and task-token rendering check await explicit approval; remaining CSI cloud credential dependency remains deferred. Backlog tracked in ~/ai/TODO.md.

## Portable lesson

none
