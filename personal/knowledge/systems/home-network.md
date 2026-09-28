---
system: home-network
status: hypothesis
checked: 2026-09-26
tags: [home, router, openwrt, trusttunnel]
---
# Home network

Status `hypothesis`: the target design is planned, not deployed. Verified facts are marked.

## Purpose

Home LAN with router-level split routing by domain lists: everything direct, only listed
domains (YouTube, Instagram, torrent trackers, ...) through the user's TrustTunnel endpoint
(see [trusttunnel-de](trusttunnel-de.md)). Encrypted DNS with ad blocking (AdGuard Home),
TorrServer for the TV, basic monitoring. No remote access, no guest or IoT segments.

## Components

- ISP Elit-TV: Ethernet cable into the flat, WAN by DHCP, up to 1 Gbit/s, no IPv6.
  WAN address `100.64.6.13` is in `100.64.0.0/10`, so CGNAT. ISP blocks by DNS spoofing,
  by IP and by DPI. Verified 2026-09-26 from the user.
- Router TP-Link Archer C64 v1.0 (AC1200), stock firmware, basic internet setup, Wi-Fi
  covers the whole flat. Verified 2026-09-26 from the user. OpenWrt does not support it: SoC MediaTek MT7626 (TP1900BN),
  flash about 4 MB, no device on this SoC in OpenWrt (OpenWrt forum thread 104952, ToH page
  does not exist). Verified 2026-09-26.
- VPN clients: phone and PC. PC runs `trusttunnel_client` from `~/trusttunnel/` with
  `vpn_mode = "general"`, killswitch on, exclusions `ru`, `xn--p1ai`, `local`, `consul`,
  `corp`, work domains and a few CDN domains; `included_routes = ["0.0.0.0/0"]`, private
  ranges and three public IPs excluded, MTU 1280, `change_system_dns = false`.
- Family uses the network; one policy for all devices, no per-device exceptions; phone
  and PC keep their own TrustTunnel clients. Tunnel failure must be fail-open with a
  Telegram notification. Decided 2026-09-26.
- Planned (hypothesis): OpenWrt router Cudy WR3000S v1 (MT7981, 256 MB RAM, 128 MB NAND;
  not WR3000 v1 with 16 MB flash, not WR3000 v2 which is unsupported) with dnsmasq-full nftsets + policy routing into the
  TrustTunnel `tun0`; 8-port unmanaged switch; Debian mini PC (N100 class) with docker
  compose: AdGuard Home (DoH/DoT upstreams routed through the tunnel), TorrServer, Uptime
  Kuma. TV Hisense 55U7S PRO (VIDAA U9.5, not bought yet): Lampa via Media Station X with
  start parameter `lampa.mx`; TorrServer must run on the home server. Browser-based
  playback on VIDAA has known issues; Homatics Box R 4K Plus is the planned fallback. Purchase order: TV,
  then router, switch, server. Telegram bot credentials: `~/ai/personal/.env`. DNS chain: client -> dnsmasq on router (populates nftsets) -> AdGuard Home ->
  encrypted upstream. Archer C64 retired or kept as access point.
- Deferred: own domain, remote access, Ansible Vault, merging the StrongSwan VPS, data
  backups, AdGuard Home on the VPS with DoT 853 for phones outside home.
- Planning repository: `/home/slnnk/mygit/home-infra` (`AGENTS.md` with state and rules for
  agents, `README.md`, `QUESTIONS.md`, `PLAN.md`, `docs/alternatives.md`).

## Delivery path

Planned: router config via UCI driven by Ansible from `/home/slnnk/mygit/ansible`
(group `home-routers`), server via Ansible + docker compose (group `home-servers`).

## Control points

Not yet. Planned: OpenWrt `/etc/config/*`, procd service for the TrustTunnel client,
dnsmasq nftsets and policy routing table for VPN traffic.

## Operations

Not yet. Open questions and deployment plan live in the repository above.

## Boundaries

The German VPN endpoint belongs to [trusttunnel-de](trusttunnel-de.md). The StrongSwan
VPS belongs to [vpn-gateway](vpn-gateway.md); its role in the target design is undecided.

## Access

Router LAN only, from the user's PC. No remote access yet.

## Related log entries

- [2026-09-26 questions and deployment plan](../log/2026-09-26-home-network-initial-plan.md)
