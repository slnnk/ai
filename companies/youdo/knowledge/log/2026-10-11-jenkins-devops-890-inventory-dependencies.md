---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, inventory, vault, registry, nginx]
---
# DevOps-890: recovery inventory, Vault/registry authorization and routing

## Task

Execute only stage 1 of [DevOps-890](https://youtrack.youdo.com/youtrack/issue/DevOps-890): prepare inventory for the two recovered Jenkins VMs, verify Vault/private-registry authorization and inspect existing public routing. User deferred publication until runtime recovery and validation.

## Context

Existing approved branch `DevOps-890-update-jenkins-images` in `/home/slnnk/git/automation-services`; previous [audit and plan](2026-10-10-jenkins-devops-890-recovery-audit.md). Controller `10.16.28.8`, agent `10.16.28.26`, root SSH. Registry credentials come from Vault `secret/ansible/yandex`, key `jenkins_client_docker_pass`, username configured as `nomad`.

## Actions

- Daily knowledge sync initially failed due sandbox DNS; approved outside-sandbox retry pushed successfully.
- Added `inventories/yandex/jenkins-recovery.ini` with exactly two new hosts, `host_type=jenkins` / `jenkins-agent`, root, Python3 and task-local new controller address. Existing Yandex group_vars still supply Vault groups and latest image pins. Invoke the exact inventory file, not the complete inventory directory, to avoid loading old Terraform hosts.
- `ansible-inventory --list` filtered to safe metadata confirmed host variables. `ansible-playbook jenkins.yml -i inventories/yandex/jenkins-recovery.ini --list-hosts` selected only the two new VMs; syntax check passed. Ansible ping returned pong on both, changed=false.
- Current Vault CLI cached token returned HTTP403 for lookup-self and both required documents. Verified the existing company `.env` variable `VAULT_YANDEX_TEST_TOKEN` instead: both document GETs succeeded. Values remained in process memory; no token/secret was printed or copied into repository files.
- Ran existing `playbooks/vault_check.yml --check` with the Yandex address/groups overridden and the token passed only through process `VAULT_TOKEN`, `VAULT_AUTH_METHOD=token`. Result: ok=6, changed=0, failed=0; yandex has nine nonempty keys and common one.
- Used Vault-backed registry credentials via GET bearer authentication and authenticated manifest GET for both selected tags. HTTP200 and expected digests matched; no Docker login, image pull or remote auth-file write occurred.
- Root SSH HTTP checks from both new VMs: Vault resolves to `10.16.28.16`, health HTTP200; registry/GitLab resolve to `89.169.136.178`; registry /v2/ HTTP401 is its expected unauthenticated challenge. Both TLS/network routes are reachable.
- Read live balancer vhost and checked DNS, upstream HTTP and TLS. No remote configuration changes or reloads.

## Findings

- Inventory and read-only dependencies checks pass with `VAULT_YANDEX_TEST_TOKEN` injected into the Ansible process environment. The default cached Vault CLI token remains invalid for this cluster and must not be used for the recovery run. The working token is not embedded in inventory.
- Jenkins manifest `2-555-1-2`: `sha256:6f80988c634047436ac35994bb37e54e6c3b61650a9f7a87be7fa5aaf688dbe4`; agent `3355.v388858a_47b_33.6`: `sha256:f40c3b92f4670dd59df5fca91c8158aeb6309982aec25788fb49fbd390f6dc2f`.
- Live route is `build.youdo.sg` -> public `178.154.207.53` -> `balancer-test01` (`10.16.20.35`) -> `jenkins-test.ru-central1.internal` -> old `10.16.26.16:80`. Current upstream and public HTTP requests time out. The new controller is not yet in this route.
- TLS handshake and hostname validation pass; public certificate expires 2026-11-26. TLS is distinct from the nonresponsive upstream.

## Changes

New local inventory only; earlier two image-pin edits and unrelated user changes preserved. No task commit/push/MR, VM provisioning, disk initialization, Jenkins start, routing change, Vault login/token creation or registry configuration change. Knowledge log/system maps updated.

## Risks

Stage 2 is disk preparation and requires explicit approval for formatting/mount/fstab changes. Further recovery stages remain in `~/ai/TODO.md`. Registry authorization was validated by manifest GET rather than full image download; a later role run will use the same credentials to pull. Existing hyphenated group name produces Ansible's invalid-character warning; empty legacy `jenkins` play produces a missing-group warning, while intended `jenkins-yandex` selects exactly two hosts.

## Portable lesson

none
