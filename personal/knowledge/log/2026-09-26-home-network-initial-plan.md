---
system: home-network
status: verified
checked: 2026-09-26
tags: [planning, openwrt, trusttunnel]
---
# Home network: questions and deployment plan

## Task

Prepare a question list and a deployment plan for the user's home infrastructure in the new
repository `/home/slnnk/mygit/home-infra`. Starting point: TP-Link Archer C64 with stock
firmware, TrustTunnel VPN in Germany, per-client split routing (`.ru`/`.su` direct).

## Context

- Repository `/home/slnnk/mygit/ansible`: inventory and roles for `it-garage-de-01`, see
  [trusttunnel-de](../systems/trusttunnel-de.md).
- PC client config `/home/slnnk/trusttunnel/trusttunnel_client.toml`.
- Older StrongSwan VPS: [vpn-gateway](../systems/vpn-gateway.md).

## Actions

- Read the Ansible repo (inventory, `trusttunnel` role defaults and README, `vpn.yml`).
- Read the PC client config (secrets masked).
- Checked OpenWrt support for Archer C64 and TrustTunnel clients for OpenWrt on the web.
- Wrote `README.md`, `QUESTIONS.md` (27 questions, prioritised A/B/C with default
  assumptions) and `PLAN.md` (7 phases, hardware options, risks) in `home-infra`.

## Findings

- Archer C64 is not supported by OpenWrt: MT7626 (TP1900BN) SoC, flash about 4 MB, no
  OpenWrt device on this SoC; ToH page absent. A separate gateway device is required.
- TrustTunnel on OpenWrt exists only as community packages: `iamvladdy/trusttunnel-openwrt`
  (OpenWrt 24.10/25.x, netifd proto, tested on aarch64 MT7986, split routing via podkop)
  and `NooBiToo/TrustTunnelOpenWrt` (OpenWrt 25.12+, dnsmasq-full nftsets, killswitch via
  blackhole route). Also `TrustTunnel/TrustTunnelClient` CLI (Linux, tun or SOCKS5) and
  `artemevsevev/TrustTunnel-Keenetic`. The client terminates TLS/QUIC in userspace, so a
  MIPS router will be slow; hypothesis: choose aarch64 or x86.
- The VPS inventory keeps client passwords in plaintext; Vault migration is a prerequisite
  before adding a router account.
- The VPN domain is `2.26.30.176.nip.io`; the role README mentions
  `video.slnnk.beget.tech` as an example, unclear whether the user owns a domain.

## Round 2, same day

The user answered all 27 questions. Decisions: VPN only for domain lists, everything else
direct; no per-device exceptions; clients stay on phone and PC; fail-open plus Telegram;
encrypted DNS with AdGuard Home; TorrServer + Lampa for the TV; new router, mini PC and
8-port switch; no guest network, no VLAN, no remote access, no domain; second VPS kept;
code in `~/mygit/ansible`; Vault, monitoring and repo hosting deferred.
Facts: ISP Elit-TV, Ethernet, DHCP, 1 Gbit/s, no IPv6, WAN `100.64.6.13` (CGNAT), blocks
by DNS, IP and DPI; Archer C64 v1.0 covers the flat.
`PLAN.md` rewritten as version 2 (6 phases, hardware table, DNS chain rationale), README
updated, round-2 questions R1-R3 appended (hardware confirmation, TV OS, first domain list).

## Round 3, same day

User picked the Cudy WR3000 line, TV is Hisense 55U7S PRO, Telegram and Discord added to the
VPN list. Checks: Cudy WR3000 v1 has 16 MB SPI NOR and no USB (too small for the TrustTunnel
client plus dnsmasq-full); WR3000 v2 uses a different SoC and is unsupported; Cudy WR3000S v1
(MT7981, 256 MB RAM, 128 MB NAND, OpenWrt 24.10.5+, two-step flash via Cudy-signed image)
chosen instead. Newer WR3000S units (date code 2543+) need the current Cudy transition image.
Hisense 55U7S PRO runs VIDAA; Lampa is installed from VidaaHub or via Media Station X with
start parameter `lampa.mx`. `PLAN.md` 2.1, questions R4-R6 appended.

## Round 4, same day

Answers: mini PC budget accepted, user creates the Telegram bot (token and chat id go to
`~/ai/personal/.env`), purchase order TV first, then router, switch, server. User asked
whether Lampa is guaranteed on the TV. Verified: Hisense 55U7S PRO sells in Russia with
VIDAA U9.5; Lampa docs list VIDAA U6+ as supported, install path is Media Station X from the
VIDAA store with start parameter `lampa.mx`; TorrServer cannot run on VIDAA and stays on
the home server. Native Lampa exists only for Android TV, webOS, Tizen; a Google TV set or
box is the alternative if the MSX wrapper feels slow. `PLAN.md` 2.2, no open questions.

## Round 5, same day: alternatives review

User asked to verify every proposed component against alternatives and whether Lampa
will lag on the TV. Four parallel web research agents (TV client, media server, DNS,
router routing). Written up in `docs/alternatives.md` of the repository; `PLAN.md` v3.
Key findings (web sources, not verified on hardware):
- Lampa on VIDAA is a browser app inside Media Station X; owners of VIDAA 7-9 sets report
  torrent speed collapse, freezes on seek, DTS/AC3 issues; no reports for U9.5. Plan: test
  first, budget a Homatics Box R 4K Plus (~10k RUB) as the likely fix.
- TorrServer MatriX is alive (145 on 2026-09-17), no real competitor; Lampac moved to
  `lampac-nextgen/lampac`, JacRed to `jacred-fdb/jacred`, public parser `jac.red`.
  TMDB domains and lampa.* must go through the VPN list; TMDB DNS intercepted since
  2026-08-26.
- Since mid-August 2026 Russian ISPs DNAT UDP/53 to 8.8.8.8/1.1.1.1 and cut DoH/DoT to
  Google, Cloudflare, partly Quad9 and AdGuard DNS by SNI. Decision: home AdGuard Home
  upstream = own AdGuard Home on the VPS (DoT 853 on the nip.io host) with Unbound
  recursion; phones use TrustTunnel `dns_upstreams` pointing there. AdGuard Home on the VPS
  moved from "later" to phase 3.
- Router routing: podkop (0.7.22, 2026-08-18) + TrustTunnel as netifd interface
  (iamvladdy) chosen; NooBiToo dropped (fail-closed only, 25.12 only); fallback
  i-zhirov/trusttunnel-openwrt (1.0.32, 2026-09-25, fail-open, no DNS changes).
- Protocols: TrustTunnel not reported signature-blocked as of 2026-09-26, but TSPU
  "freezes" connections by ASN/behaviour since June 2026 and TrustTunnel UDP over HTTP/2 is
  slow (3-12 Mbit/s, TrustTunnel issue #153). Decision: add AmneziaWG 3.x on UDP on the same
  VPS (Ansible role) as backup and for UDP-heavy lists; kernel module awg-openwrt.
- zapret/youtubeUnblock not used: YouTube/Instagram blocked by IP since April 2026,
  mass breakage 2026-09-23.
- Throughput on MT7981: WireGuard kernel 370-525 Mbit/s, sing-box ~250, TrustTunnel
  client ~100-200 TCP (hypothesis).

## Changes

- `/home/slnnk/mygit/home-infra/{README.md,QUESTIONS.md,PLAN.md}` created.
- `systems/home-network.md`, `systems/trusttunnel-de.md` created; `repos.md` extended.

## Open items

- Phase 1: buy TV, test Lampa via Media Station X; C64 backup, device list, tunnel speed
  test from the PC.
- Bench tests before family rollout: podkop fail-open on `ifdown tun0`; podkop FakeIP DNS
  with AdGuard Home DoT upstream; reachability of the VPS public IP from inside the tunnel.
- Router account password will land in the plaintext inventory until Vault is done.
- `home-infra` is not a git repository yet; the user decides where to host it.

## Portable lesson

none
