---
system: trusttunnel-de
status: verified
checked: 2026-09-26
tags: [trusttunnel, vpn, ansible, nftables, crowdsec]
---
# TrustTunnel endpoint it-garage-de-01

Facts below come from the Ansible repository on 2026-09-26; the host itself was not
inspected in that session.

## Purpose

Self-hosted TrustTunnel VPN endpoint in Germany for the user's phone, PC and family.
Planned to also serve the home router (see [home-network](home-network.md)).

## Components

- Host `it-garage-de-01`, `ansible_host=2.26.30.176`, group `vpn`.
- Domain `2.26.30.176.nip.io` (`inventory/host_vars/it-garage-de-01.yml`,
  `trusttunnel_domain`). Certificate from Let's Encrypt via host `certbot`, webroot on
  nginx port 80. Hypothesis: a real domain is preferable; nip.io depends on a third party.
- TrustTunnel `1.0.33`, native binary under `/data`, systemd service, listens `0.0.0.0:443`
  TCP and UDP (QUIC on), forward mode `direct`, log `/var/log/trusttunnel.log` at level
  `debug`, metrics disabled.
- Three client accounts in `inventory/group_vars/vpn.yml` (`trusttunnel_clients`):
  `slnnk`, `aleshka`, `family`. Passwords are plaintext in the inventory; moving them to
  Ansible Vault is an open TODO of that repository.
- Firewall nftables: base rules from `group_vars/all.yml` plus 80/tcp, 443/tcp, 443/udp
  from `group_vars/vpn.yml`. CrowdSec installed.

## Delivery path

`cd /home/slnnk/mygit/ansible && ansible-playbook -i inventory/hosts playbooks/vpn.yml`
(roles `ansible-user`, `common`, `nftables`, `sshd`, `crowdsec`, `trusttunnel`).
Role docs: `roles/trusttunnel/README.md`. Syntax check with `--syntax-check` first.

## Control points

- `systemctl status trusttunnel`, `nginx`, `certbot.timer`; deploy hook restarts
  TrustTunnel on certificate renewal.
- Health paths: `/tt_ping`, `/tt_speed` on the domain.

## Operations

- Add a client: append to `trusttunnel_clients`, run the playbook (state change on the
  VPS, needs the user's confirmation).
- Client config on the PC: `/home/slnnk/trusttunnel/trusttunnel_client.toml`, run script
  `run-trusttunnel.sh` (sudo).

## Boundaries

Separate from the StrongSwan VPS `91.218.141.22` ([vpn-gateway](vpn-gateway.md)).

## Access

SSH as the ansible user created by role `ansible-user`; keys from
`inventory/group_vars/all.yml`. Client passwords: inventory file only, never in notes.

## Related log entries

- [2026-09-26 home network plan](../log/2026-09-26-home-network-initial-plan.md)
