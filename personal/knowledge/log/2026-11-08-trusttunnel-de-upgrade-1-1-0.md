---
system: trusttunnel-de
status: verified
checked: 2026-11-08
tags: [trusttunnel, ansible, upgrade]
---
# TrustTunnel upgraded to 1.1.0

## Task
Upgrade the personal VPN endpoint from 1.0.33 to stable 1.1.0 through Ansible.

## Context
Repository `/home/slnnk/mygit/ansible`, existing `master`, base `origin/master`.
The repository role and inventory files were already untracked; no staging,
commit, push or branch changes were performed.
See the [system map](../systems/trusttunnel-de.md).

## Approvals
The user requested preparation and deployment. The agent proposed the existing
checkout and branch/base, changing the version default and README examples, and
syntax validation. The user explicitly approved with `Да`.
After showing the actual changes and successful syntax check, the agent proposed
the focused playbook limited to this host with apt upgrades skipped and explained
the service restart. The user separately approved execution with `Да`.

## Changes
- `roles/trusttunnel/defaults/main.yml`: version 1.0.33 to 1.1.0.
- `roles/trusttunnel/README.md`: matching version and release archive URL.
- No new role settings or client configuration changes.

## Actions and verification
Syntax validation passed:

```bash
.ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/trusttunnel.yml --syntax-check
```

The initial sandboxed syntax check could not create its local temporary directory;
the same command passed outside the sandbox. Authorized deployment:

```bash
.ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/trusttunnel.yml --limit it-garage-de-01 --skip-tags upgrade
```

Recap: `ok=21 changed=7 unreachable=0 failed=0 skipped=2 rescued=0 ignored=0`.
The restart handler completed. Post-deployment read-only checks confirmed:
- `/usr/local/bin/trusttunnel_endpoint --version` reports `1.1.0`.
- `trusttunnel.service` is `active/running`, `ExecMainStatus=0`.
- The endpoint process listens on TCP and UDP `0.0.0.0:443`.
- External `https://v.slnnk.com/tt_ping` returned HTTP 200, TLS verify result 0.
The Ansible shell module labels read-only commands as changed by default; the
verification command did not modify remote configuration.

## Status and risks
Upgrade complete. No background commands remain. No second mutating run or
end-to-end authenticated client session was performed. No publication requested.
Reviewed the central TODO TrustTunnel endpoint section: no open upgrade item
requires reconciliation; unrelated monitoring and home-network entries remain unchanged.

## Portable lesson
none
