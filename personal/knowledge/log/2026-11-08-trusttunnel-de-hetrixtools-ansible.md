---
system: trusttunnel-de
status: verified
checked: 2026-11-08
tags: [ansible, monitoring, hetrixtools]
---
# Reusable HetrixTools Ansible agent role

## Task

The user requested installing the HetrixTools agent through Ansible, confirmed
reuse of `/home/slnnk/mygit/ansible`, branch `master`, base `b857c7e`, and required
the role to support other servers through parameters. Approval applies to local
implementation; no deployment or publication was approved.

## Context

The existing `vpn` uptime monitor checks `https://v.slnnk.com/tt_ping`.
The user confirmed Telegram notification delivery. An API read earlier in this
conversation verified certificate-expiry alerts enabled five days before expiry,
with certificate expiry `2027-02-05`; domain-expiry alerts are also enabled for
five days. These account settings were not changed.

## Actions

Inspected existing role conventions and official HetrixTools agent sources.
Chose direct versioned agent download and native systemd scheduling because the
upstream installer deletes the runtime directory and recreates the runtime user.
Implemented the role, inventory and playbooks locally. Encrypted the user-provided
SID with the existing `ANSIBLE_VAULT_PASSWORD` from `personal/.env`; no plaintext
SID or Vault password was stored in repository files or this log.

## Findings

Agent `2.4.2` supports service status checks with systemd and process fallbacks.
Each host needs a unique agent SID. Group settings define monitored services;
the role defaults contain no VPN-specific values. The role uses a systemd timer
and refuses legacy cron schedules or the official systemd launcher until explicit
migration, avoiding duplicate collection. Switching runtime user stops collection
before changing file ownership. Runtime config and files are private, and TLS
verification stays enabled. Optional RAID/drive monitoring requires root.

## Changes

- `roles/hetrixtools/`: defaults, tasks, handlers, config/systemd templates, README.
- `playbooks/hetrixtools.yml`: focused run for `vpn`.
- `playbooks/vpn.yml`: agent role after TrustTunnel.
- `inventory/group_vars/vpn.yml`: services `trusttunnel` and `nginx`.
- `inventory/host_vars/it-garage-de-01.yml`: Vault-encrypted unique agent SID.
- `AGENTS.md`: reusable monitoring role and scheduler conventions.

Existing unrelated and untracked files were preserved. No stage/commit/push/MR.

## Verification

Both focused and VPN playbook syntax checks passed, including with the existing
Vault password. A local Ansible harness decrypted the SID without displaying it,
rendered default/nonroot and custom/root configurations, and verified rejection
of invalid SID, invalid port and privileged drive monitoring without root.
The repeat harness run reported `changed=0`, `failed=0`, with three expected
validation failures caught by rescue blocks. This verifies template idempotency,
not a full live role run.

The official agent parser accepted both rendered configurations without sending
data. Shell syntax, managed headers and role task tags passed. Legacy scheduler
checks distinguish active/commented cron entries and detect the official launcher.
Runtime ownership changes are rejected for install-only execution or when config
tasks are skipped; local Ansible guard checks passed for both rejection paths and
normal full-role execution.
Systemd unit verification exited zero; local host netplan/Varlink/snap warnings
were unrelated to the rendered HetrixTools units.

Instruction lint: 10 files, zero errors, one `CDX-AG-005` warning in repository
`AGENTS.md`, line 41; report-only, no automatic fixes.

## Status and risks

At the initial local-implementation stage on 2026-11-08, deployment, live metric delivery and
whole-role runtime idempotency were unverified; dashboard warning thresholds
and service-down alerts are separate account settings. Deployment is a proposal
in the [central TODO](../../../TODO.md), requiring explicit approval. No remote
services, firewall rules or account settings changed at that stage. See the
subsequent authorized deployment below for the current status.

## Deployment authorized and verified, 2026-11-08

The user approved deployment with `Примени`. Applied only
`playbooks/hetrixtools.yml`, limited to `it-garage-de-01`, using the existing
Vault password helper. The play ended with `ok=17`, `changed=8`, `failed=0`,
`unreachable=0`. Apt updated `iproute2`, `procps` and its `libproc2-0` dependency.
Agent `2.4.2`, its private configuration and systemd timer were installed.

The local assistant server restarted after successful deployment. Deployment
was not repeated. Resumed read-only checks confirmed the timer enabled/active,
collector running as `hetrixtools`, and TrustTunnel/nginx active. A configuration
check with `--tags hetrixtools-config --check` ended with `ok=13`, `changed=0`,
`failed=0`, `unreachable=0`; a second mutating deployment was not run, so full-role
runtime idempotency is still not demonstrated.

Native HetrixTools MCP returned repeated metric snapshots, agent version `2.4.2`,
service statuses `trusttunnel=online`, `nginx=online`, RAM around 24.2 percent,
and root filesystem usage 27.25 percent. Resource and service warning policies
were read and are disabled. No account warning settings were changed.

Deployment and metric-delivery work is complete. At the deployment stage, the central TODO retained a proposal to configure
resource/service warnings. The subsequently approved configuration below supersedes
that pending status. No task background commands remain; the intended systemd timer keeps
collecting every minute. Inspect with `systemctl status hetrixtools_agent.timer`;
stopping it with `sudo systemctl stop hetrixtools_agent.timer` changes the server
and requires authorization. No Git publication was performed.

## Warning policies enabled and verified, 2026-11-08

The user requested warning configuration and approved the concrete proposed
thresholds with `Да`. One native HetrixTools MCP update enabled five policies for
the `vpn` monitor: CPU >=90 percent averaged over five minutes, RAM >=90 percent
averaged over five minutes, root filesystem >=85 percent averaged over five
minutes, no agent data for more than five minutes, and either `trusttunnel` or
`nginx` stopped. All policies repeat every 30 minutes while the issue persists.

Each policy explicitly targets the existing `Contacts` list, verified to contain
email and Telegram channels. The API returned success. A separate read-back
confirmed all five enabled policies, thresholds, averaging windows, repetition
frequency, contact list and selected disk/services. Other warning policies were
not changed. No VPS or Ansible configuration changes were needed.

Configuration is verified, but no failure was deliberately induced and no new
notification-delivery test was sent. Telegram delivery was user-confirmed earlier.
The corresponding central TODO proposal is closed. No task background work remains.

## Portable lesson

None; implementation guidance is in the repository role README.
