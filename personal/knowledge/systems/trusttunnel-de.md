---
system: trusttunnel-de
status: verified
checked: 2026-11-04
tags: [trusttunnel, vpn, ansible, nftables, crowdsec]
---
# TrustTunnel endpoint it-garage-de-01

## Staleness review (2026-11-04)

Reconciled with the current local Ansible defaults and VPN playbook and the [2026-11-04 server cleanup verification](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md). TrustTunnel remains the configured VPN; StrongSwan is absent from both active Ansible configuration and the recorded VPS state. The latest recorded service checks show TrustTunnel, nftables, nginx and the CrowdSec bouncer active, with the shared certificate and TrustTunnel renewal hook retained and HTTPS `/tt_ping` returning HTTP 200. The [user confirmed iPhone TrustTunnel on 2026-11-02](../log/2026-11-02-vpn-gateway-strongswan-ansible.md); no new iPhone session or server probe was performed during this review. Use `.ansible-venv/bin/ansible-playbook` from the repository root for the delivery commands below.

The original Ansible snapshot was recorded on 2026-09-26. Later dated sections
record deployment and service checks; the current documented state was reconciled
on 2026-11-04, with verification limits stated below.

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

`cd /home/slnnk/mygit/ansible && .ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/vpn.yml`
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

## Local PC client routing adjustment

On2026-10-11 the local PC client configuration received an explicitly authorized corporate OpenVPN endpoint exclusion; the TrustTunnel server itself was unchanged. Client exclusion activation verified after user restart; corporate VPN reconnected and controlled Nexus transport verification passed; browser symptom confirmation pending. See [client routing log](../log/2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md).

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.

## StrongSwan local preparation, 2026-11-02

The local Ansible checkout now also defines `roles/strongswan` and
`playbooks/strongswan.yml` for IKEv2/EAP-MSCHAPv2 on this host. It reuses the
TrustTunnel certificate; `vpn.yml` runs it after TrustTunnel. The nftables role
owns authenticated IPsec forwarding and IPv4 NAT, with UDP 500/4500 added in
VPN inventory. Client credentials are now encrypted as `vault_strongswan_clients` in
`inventory/group_vars/vpn-vault.yml`, passed explicitly with `-e @...`. The Vault
password is `ANSIBLE_VAULT_PASSWORD` in `~/ai/personal/.env`. Deployed on 2026-11-02 by explicit user request; StrongSwan and TrustTunnel
verified active together, IKEv2 connection loaded, UDP 500/4500 listening,
and IPv4 forwarding/NAT active. Live iPhone verification remains pending. See [preparation log](../log/2026-11-02-vpn-gateway-strongswan-ansible.md)
and the central TODO under Personal / StrongSwan endpoint.

## iPhone client authentication, 2026-11-02

TrustTunnel and StrongSwan have independent credential lists. The current
StrongSwan account shares a username with an existing TrustTunnel account but
uses a different password. The inventory `trusttunnel_clients` credential was
verified against the running server without exposing values. Recent iPhone
reconnection diagnostics found authentication failures; the user subsequently corrected the password and confirmed on 2026-11-02
that TrustTunnel works on iPhone. The corresponding central TODO is closed. See the
[diagnostic log](../log/2026-11-02-vpn-gateway-strongswan-ansible.md).

## StrongSwan Ansible removal, 2026-11-04

The user chose TrustTunnel on iPhone and retired StrongSwan from local Ansible. The role, playbook, dedicated Vault file, inventory settings and IPsec firewall/NAT additions are removed; previous StrongSwan preparation and deployment sections are historical. TrustTunnel settings remain unchanged. IKEv2 verification is cancelled in the central TODO. No VPS changes were made, so the deployed service and related server files may remain. See the [removal log](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md).

## StrongSwan server removal, 2026-11-04

After a separate user request and explicit approval of the cleanup command, StrongSwan was also removed from the VPS. Its service, eight packages, credentials, chain copies, renewal hook, persistent sysctl file and IPsec firewall/NAT rules are absent; IPv4 forwarding is disabled. This supersedes the local-only removal limitation above. TrustTunnel, nftables, nginx and CrowdSec bouncer are active; the TrustTunnel renewal hook and shared certificate are preserved. HTTPS `/tt_ping` returned HTTP200. No actual iPhone session tested in this cleanup. See the [removal log](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md).
