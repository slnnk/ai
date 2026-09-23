---
system: automation-services
status: verified
checked: 2026-09-18
tags: [vault, ansible, hashi_vault, ldap, oidc, acl, workstation]
---
# automation-services: local Ansible access to Vault

Last verified: 2026-09-18

## Context

- Repository: `/home/slnnk/git/automation-services` (`git@gitlab.youdo.sg:sysadmins/automation-services.git`), branch observed during setup: `master`.
- Workstation: Ubuntu 20.04 amd64.
- Purpose: local `ansible-playbook` runs that read inventory secrets from HashiCorp Vault KV v1.

## Verified local setup

- Ansible Core `2.15.13` runs under `/usr/bin/python3.9`; packages are installed under `~/.local/lib/python3.9/site-packages` rather than pipx.
- Python package `hvac 2.4.0` imports successfully in the same Python interpreter.
- `community.hashi_vault 6.2.1` is installed under `~/.ansible/collections`, satisfying repository constraint `>=6.0.0,<7.0.0` in `collections.yml`.
- Vault CLI `2.1.1` is installed as `~/.local/bin/vault`; the downloaded official archive was checked against HashiCorp's SHA256 list before installation.
- `ansible-doc -t module community.hashi_vault.vault_kv1_get` and syntax check of `playbooks/vault_check.yml` succeed.
- Production Vault endpoint is `http://vault.service.consul:8200`; it was reachable from this workstation on 2026-09-18.
- No `ansible.cfg` change is needed. The collection uses `VAULT_TOKEN` or `~/.vault-token`; inventory provides `vault_addr` to the secret-fetch task.

## Authentication state and operating procedure

- The pre-existing `~/.vault-token` had mode `0600` but dated from 2022 and was rejected with HTTP 403 `invalid token`. Its value was not read or recorded.
- Refresh monthly from an interactive user terminal:

```bash
export VAULT_ADDR=http://vault.service.consul:8200
vault login -method=ldap username=<FreeIPA UID>
vault token lookup
```

- LDAP login is intentionally interactive; never record the password or resulting token in notes.
- As documented by the team and last checked there on 2026-08-20, CLI OIDC is not usable until `http://localhost:8250/oidc/callback` is added to the `reader` role's `allowed_redirect_uris` on both Vault clusters. Browser OIDC must use the Vault DNS name, not an IP address.

## End-to-end check

After refreshing the token:

```bash
ansible-playbook -i inventories/prod_selectel/inventory.yml playbooks/vault_check.yml
```

The check is read-only. It reads `secret/ansible/{prod_selectel,prod_yandex,common}` through `playbooks/vault_fetch_tasks.yml`, suppresses secret values with `no_log: true`, and asserts each document is non-empty.

## Repository integration

- `playbooks/vault_fetch_tasks.yml` performs local delegated KV v1 reads and exposes the results as `vault_secrets`.
- Plays that consume Vault-backed variables must import that task file as an `always` pre-task.
- Inventory files define `vault_groups` and `vault_addr`; ordinary playbook invocation remains unchanged.
- AWX uses collections baked into its execution image and must be updated separately when collection versions change (see `awx-collection-dependencies.md`).

## Remaining action

- LDAP login was completed on 2026-09-18. The resulting token is valid through
  2026-10-20 and has Vault policies `default` and `ipausers`; no token value is
  recorded here.
- `vault token capabilities` returned `deny` for
  `secret/ansible/prod_selectel`, `secret/ansible/prod_yandex`, and
  `secret/ansible/common`. Direct read-only `vault kv get` checks failed with
  HTTP 403 before returning any secret data, and the Ansible check failed at the
  same read task. This proves the remaining failure is Vault ACL/policy mapping,
  not Ansible, `hvac`, DNS, transport, or token discovery.
- Vault administrators need to map the user's LDAP/FreeIPA group to an
  appropriate read policy, or update the existing mapped policy to grant the
  required KV v1 paths. Prefer the three exact paths (and any deliberately
  required list permission) rather than a broad `secret/*` grant. After the ACL
  change, repeat `vault token capabilities` and `playbooks/vault_check.yml`.

## ACL investigation update

- The `ipausers` policy visible in the production Vault UI contains only
  `path "kv/*"` with `read` and `list`; it does not cover the new Ansible secret
  paths under `secret/ansible/*`.
- `vault.service.consul:8200` and `vault.service.selectel.consul:8200` were
  checked on 2026-09-18 and reported the same cluster ID, so the hostname
  difference is only an alias and is not the cause.
- Mount metadata reports `kv/` as KV v2. Safe reads found no documents at
  `kv/ansible/prod_selectel`, `kv/ansible/prod_yandex`, or
  `kv/ansible/common`; the root contains only an unrelated legacy key name.
- Do not change `playbooks/vault_fetch_tasks.yml` from KV v1 `secret` to KV v2
  `kv`. Access must come from a policy covering `secret/ansible/*`; the later
  AP-2228 audit below establishes that the intended policy is the separate
  `ansible-infra` policy rather than an expansion of legacy `ipausers`.

## AP-2228 and LDAP root cause

- YouTrack issue `AP-2228` and article `AP-A-77008428` identify the intended
  human access policy as `ansible-infra`, not `ipausers`. The policy is managed
  in `/home/slnnk/git/infra-tf/vault/policies/ansible-infra.hcl` and grants
  `read,list` on `secret/ansible/*`.
- Terraform creates external identity group `vault-infra` with policy
  `ansible-infra`, but both `vault/prod/identity.tf` and
  `vault/test/identity.tf` create its only alias against the `oidc` auth mount.
- The documented terminal workaround logs users in through `auth/ldap` because
  CLI OIDC lacks the localhost callback. A fresh LDAP login after adding the
  user to FreeIPA group `vault-infra` still produced only `default,ipausers`
  and denied `secret/ansible/prod_selectel`. Thus the missing piece is an LDAP
  group-to-policy mapping (or an LDAP-specific identity group alias), not user
  membership or Ansible configuration.
- HashiCorp's direct LDAP mapping is
  `vault write auth/ldap/groups/vault-infra policies=ansible-infra`; it must be
  applied by an authorized Vault operator and represented in infrastructure as
  code. A fresh LDAP login is required afterward because LDAP policy mapping is
  evaluated when the token is created.
- During diagnosis a live token was pasted into chat output. Its value is not
  recorded here. It must be revoked immediately and replaced only after the
  mapping is fixed.

## Local token/password follow-up

- The user configured `~/.ansible.cfg` with
  `vault_password_file = ~/.ansible_pass`; the file exists with mode `0600`.
  This is the unrelated Ansible Vault decryption password and is used in the
  active tree only by `clickhouse.yml` for `vault_vars/clickhouse.yml`. It does
  not authenticate `community.hashi_vault` to HashiCorp Vault.
- A later `~/.vault-token` was valid but carried policy `root`. A read-only run
  of `playbooks/vault_check.yml` then succeeded end-to-end and reported document
  key counts 18 (`prod_selectel`), 5 (`prod_yandex`), and 1 (`common`). Thus
  HashiCorp Vault connectivity and Ansible integration are working with that
  token; any remaining playbook failure is a separate error.
- A `root`-policy token must not be used for routine Ansible execution. Replace
  it with an OIDC or otherwise issued token limited to `ansible-infra`. Do not
  revoke it blindly if it may be a shared emergency token; coordinate with its
  owner, then remove it from the workstation. No token values are recorded.

## Separate production and test tokens

- A concrete failing command used `inventories/yandex/inventory.yml` and host
  `balancer_test01`. That inventory declares
  `vault_addr: http://vault.service.yandex-test.consul:8200` and groups
  `yandex,common`.
- The token then cached in `~/.vault-token` was valid only on production
  `vault.service.consul:8200`; lookup against the test cluster returned HTTP 403
  `invalid token`. Production and test are separate Vault clusters and their
  tokens are not interchangeable.
- For a `yandex` run, obtain an OIDC token from the test Vault UI opened by its
  allowed DNS name and pass it in the current shell as `VAULT_TOKEN`. This
  overrides the single cached `~/.vault-token` without replacing it. Verify
  policy `ansible-infra` and capability on `secret/ansible/yandex` before the
  playbook run.
