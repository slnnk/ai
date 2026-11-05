---
system: vpn-gateway
status: verified
checked: 2026-11-04
tags: [strongswan, ansible, trusttunnel]
---
# Remove StrongSwan from personal Ansible

## Task

The user no longer needs StrongSwan because TrustTunnel works on iPhone, and requested removing its Ansible changes. Scope is local repository configuration only.

## Context and approval

Proposed repository `/home/slnnk/mygit/ansible`, reuse of existing `master`, base `b857c7e`, preserving unrelated local files and excluding Git publication or server changes. User explicitly confirmed with `Да`. Most configuration remains untracked; no Git mutations performed.

## Actions and changes

Removed `roles/strongswan`, `playbooks/strongswan.yml`, its invocation from `playbooks/vpn.yml`, dedicated encrypted `inventory/group_vars/vpn-vault.yml`, inventory variables, UDP 500/4500, and nftables IPsec forwarding/NAT support. Updated nftables documentation and removed obsolete repository AGENTS instructions. TrustTunnel settings and credentials remain unchanged. Personal `.env` was not changed.

## Validation

Repository-local Ansible syntax checks passed for `vpn.yml`, `nftables.yml`, and `trusttunnel.yml`. Compared inventory with a local before-change snapshot: TrustTunnel settings preserved and only the two IKE ports removed. Rendered firewall equals the former template with IPsec disabled, ignoring blank lines. No StrongSwan/IPsec references remain in active repository configuration. Agent lint: 0 errors, 1 pre-existing `CDX-AG-005` warning, 2 informational findings.

## Status and risks

Local and subsequently authorized server removal are complete. The iPhone IKEv2 verification task is cancelled by the user's decision, not completed testing. The server cleanup is recorded below; it supersedes the earlier local-only scope. Historical deployment evidence remains in the [original log](2026-11-02-vpn-gateway-strongswan-ansible.md).

## Portable lesson

none

## Server removal completed, 2026-11-04

The user explicitly requested server removal. Read-only inspection found the StrongSwan service active and eight related packages installed. An apt purge simulation confirmed only those eight packages would be removed. Presented the exact SSH cleanup action, including service stop/disable, package purge, credential and hook removal, sysctl cleanup, firewall changes and CrowdSec bouncer restart. The user explicitly confirmed with `Да` before execution.

Executed the prepared cleanup against `it-garage-de-01` (`2.26.30.176`). Validated the candidate firewall with `nft -c` before changes. Stopped and disabled StrongSwan; purged `charon-systemd`, `strongswan-swanctl`, `libcharon-extra-plugins`, `libstrongswan-extra-plugins`, `libstrongswan`, `libstrongswan-standard-plugins`, `strongswan-libcharon`, and `libcharon-extauth-plugins`. Removed `/etc/swanctl/swanctl.conf`, generated `ansible-strongswan-chain-*.pem` copies, the `strongswan-reload` Certbot hook and `/etc/sysctl.d/90-strongswan.conf`. Disabled IPv4 forwarding, removed IKE port rules and IPsec/NAT from `/etc/nftables.conf`, loaded the validated rules and restarted the CrowdSec firewall bouncer. No shared TrustTunnel certificates, TrustTunnel configuration or unrelated packages were removed.

Post-removal read-only verification passed: no StrongSwan unit or package records, no managed StrongSwan files, no UDP 500/4500 listeners, and no IPsec/pool/NAT firewall rules. SSH/HTTP/TrustTunnel allow rules remain. TrustTunnel, nftables, nginx and CrowdSec bouncer are active. Shared certificate/key and TrustTunnel renewal hook remain present. `net.ipv4.ip_forward = 0`. HTTPS `https://2.26.30.176.nip.io/tt_ping` returned HTTP200 with certificate validation. No actual iPhone session was tested in this cleanup. No Git mutations performed.
