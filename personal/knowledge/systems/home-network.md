---
system: home-network
status: hypothesis
checked: 2026-10-13
tags: [home, router, openwrt, trusttunnel]
---
# Home network

## Summary

- The target router-level VPN and encrypted-DNS design remains a plan.
- The existing Archer C64 supplies the home LAN.
- Media Station X and Lampa startup on the TV are user-confirmed as of 2026-11-10.
- TorrServer MatriX.150 runs in Docker on the existing Linux PC.
- The current TV endpoint is `http://192.168.192.107:8090`.
- Host-side HTTP health passed; TV connectivity and playback remain pending.
- TorrServer data persists in `/home/slnnk/ai-data/torrserver`.
- Jackett runs on TCP 9117; working Lampa integration is user-confirmed after the CORS fix.
- Current Russian-language sources are RuTor, NNM-Club and RuTracker.org; the latter passed Test after FlareSolverr integration.
- FlareSolverr 3.5.2 runs privately on `home-media`; Jackett uses `http://flaresolverr:8191`.
- The PC must stay on for playback; its DHCP address can change.
- Components and Operations describe the current deployment and checks.
- Historical VPN diagnostics remain below; open work is tracked in central TODO.

## Staleness review (2026-11-04)

The home deployment remains a plan: local `home-infra/AGENTS.md` still records no deployment. Its version-3 `PLAN.md` and the explicit decisions in `AGENTS.md` specify podkop with TrustTunnel as a netifd interface, AmneziaWG UDP as backup, and encrypted DNS through the user's own VPS AdGuard Home with Unbound recursion; raw dnsmasq nftset routing is the fallback, not the selected primary design. Amend the planned-components paragraph accordingly and remove VPS AdGuard Home from the deferred list. Fail-open, FakeIP/upstream compatibility and actual tunnel egress still require the existing bench tests in the central backlog. No router, server, hardware purchase or client restart was checked during this review. StrongSwan's trial on the TrustTunnel host was removed on 2026-11-04, as recorded in the [removal log](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md); the separate old gateway's current state remains unconfirmed.

Status `hypothesis`: the target design is planned, not deployed. Verified facts are marked.

## Purpose

Home LAN with router-level split routing by domain lists: everything direct, only listed
domains (YouTube, Instagram, torrent trackers, ...) through the user's TrustTunnel endpoint
(see [trusttunnel-de](trusttunnel-de.md)). Encrypted DNS with ad blocking (AdGuard Home),
TorrServer for the TV, basic monitoring. No remote access, no guest or IoT segments.

## Components

- Shared nginx/Certbot local implementation (2026-11-11): the user approved the proposed refactor. Shared `nginx` owns main/HTTP/stream configuration with explicit inventory/header merges, validated reload and candidate rollback. Shared `certbot` owns webroot lineages and lineage-specific renewal actions. VPN and relay ownership was migrated locally while retaining TrustTunnel TLS, relay passthrough and issuance-before-service ordering. Media inventory now prepares HTTPS `tv.slnnk.com` for Jackett result/download APIs, with private admin/solver endpoints. Syntax, three isolated nginx configurations, bootstrap selection, hooks and rollback tests passed. No deployment, DNS or live certificate action; see [implementation](../log/2026-11-11-home-network-shared-nginx-certbot.md). This supersedes the earlier pending-refactor proposal below.

- Selected future remote media endpoint (2026-11-11): the user chose `tv.slnnk.com`. Proposed nginx TLS termination proxies to loopback Jackett 9117, with FlareSolverr still local-only. Shared nginx and separate Certbot roles are an architectural proposal after reviewing existing VPN/relay consumers; no refactor, DNS/certificate operation or public listener was implemented. Preserve relay TLS passthrough and VPN certificate ordering. See [proposal](../log/2026-11-11-home-network-ansible-jackett-roles.md#shared-nginx-architecture-proposal).

- Local Ansible preparation (2026-11-11): `/home/slnnk/mygit/ansible` now has roles `docker` and `jackett`, with the combined Jackett/FlareSolverr Compose project managed by `jackett`; `playbooks/jackett.yml` targets the user's existing `jackett` group and applies bootstrap/base/security/monitoring roles as well. Host networking accommodates the current nftables ruleset; both HTTP listeners default to loopback, CORS is on, and existing runtime secrets/indexers are preserved. Syntax, Compose validation and a synthetic settings-preservation test passed. The user's inventory files are unchanged; `dline-pl-01` still needs an address and unique monitoring SID. No remote deployment or Git publication. See [implementation and approval record](../log/2026-11-11-home-network-ansible-jackett-roles.md).

- Current verified media setup (2026-11-10): RuTor, NNM-Club and RuTracker.org are configured in Jackett. The user's RuTracker UI setup saved the account configuration; the agent did not read credentials. After explicit approval, deployed FlareSolverr 3.5.2 (`ghcr.io/flaresolverr/flaresolverr:latest`) on private Docker network `home-media`, connected Jackett to that network and set its solver URL to `http://flaresolverr:8191`; timeout remains 55000 ms and CORS true. FlareSolverr has restart `unless-stopped`, RAM-backed `/tmp` capped at 256 MB and no published host port. Solver health, the RuTracker login-page challenge (HTTP 200) and Jackett RuTracker Test (HTTP 204) passed. This supersedes the pending account/solver status below. See [installation and checks](../log/2026-11-10-home-network-pc-flaresolverr.md).

- Current media source choice (2026-11-10): user requested Russian-language releases after confirming the setup works. RuTor and NNM-Club (`noname-club`) are configured; NNM-Club save and Test returned HTTP 204. The previously configured English sources The Pirate Bay and YTS were removed for this request. The user has a RuTracker.org account and will add `RuTracker.org` through Jackett UI with personal credentials. No credential entry or RuTracker configuration by the agent. This supersedes the earlier source set below; see [source selection](../log/2026-11-10-home-network-jackett-indexers.md#russian-language-sources-selected).

- Verified 2026-11-10: user-approved Jackett container `jackett`, image `lscr.io/linuxserver/jackett:latest` (`v0.24.3042-ls32`), restart `unless-stopped`, configuration `/home/slnnk/ai-data/jackett` mounted at `/config`. TCP 9117 is published only on the PC LAN address: `http://192.168.192.107:9117`. Cookie-aware root/dashboard HTTP checks passed. RuTor, The Pirate Bay and YTS were subsequently configured at the user's request; all passed Jackett Test. The failed 1337x configuration was removed after it required FlareSolverr; no extra service was installed. TV-side parser integration and playback remain pending. See [deployment and approval](../log/2026-11-10-home-network-pc-jackett.md) and [indexer setup](../log/2026-11-10-home-network-jackett-indexers.md).

- Verified 2026-11-10: the user installed Media Station X on the TV and confirmed Lampa opens. TorrServer now runs on the existing Ubuntu Linux PC instead of waiting for the planned mini PC: Docker container `torrserver`, image `ghcr.io/yourok/torrserver:latest`, version `MatriX.150`, restart `unless-stopped`, data `/home/slnnk/ai-data/torrserver` mounted at `/opt/ts`. TCP 8090 is published on the PC's LAN IP only; `http://192.168.192.107:8090/echo` returned HTTP 200. TV access and playback are pending; the address may change with DHCP. See [deployment and approval](../log/2026-11-10-home-network-pc-torrserver.md).

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
  ranges and four public IPs excluded, MTU 1280, `change_system_dns = false`.
- Family uses the network; one policy for all devices, no per-device exceptions; phone
  and PC keep their own TrustTunnel clients. Tunnel failure must be fail-open with a
  Telegram notification. Decided 2026-09-26.
- Planned (hypothesis): OpenWrt router Cudy WR3000S v1 (MT7981, 256 MB RAM, 128 MB NAND;
  not WR3000 v1 with 16 MB flash, not WR3000 v2 which is unsupported) with podkop list-based routing, TrustTunnel as a netifd interface and
  AmneziaWG UDP as backup; raw dnsmasq nftsets and policy routing are the fallback; 8-port unmanaged switch; Debian mini PC (N100 class) with docker
  compose: AdGuard Home (encrypted upstream to the user's VPS AdGuard Home with Unbound
  recursion; no public resolver upstreams), TorrServer, Uptime Kuma. TV Hisense 55U7S PRO (VIDAA U9.5, not bought yet): Lampa via Media Station X with
  start parameter `lampa.mx`; TorrServer must run on the home server. Browser-based
  playback on VIDAA has known issues; Homatics Box R 4K Plus is the planned fallback. Purchase order: TV,
  then router, switch, server. Telegram bot credentials: `~/ai/personal/.env`. DNS plan: client -> router dnsmasq -> podkop resolver -> home AdGuard Home ->
  encrypted upstream at the user's VPS AdGuard Home / Unbound. FakeIP compatibility
  is a bench-test hypothesis. Archer C64 retired or kept as access point.
- Deferred: own domain, remote access, Ansible Vault, merging the StrongSwan VPS, data
  backups. VPS AdGuard Home with encrypted upstream access is part of the selected
  plan, not a deployed service.
- Planning repository: `/home/slnnk/mygit/home-infra` (`AGENTS.md` with state and rules for
  agents, `README.md`, `QUESTIONS.md`, `PLAN.md`, `docs/alternatives.md`).

## Delivery path

Planned: router config via UCI driven by Ansible from `/home/slnnk/mygit/ansible`
(group `home-routers`), server via Ansible + docker compose (group `home-servers`).

## Client routing observations

Verified 2026-10-11 with both VPNs: public Kickstarter, ChatGPT and GitHub destinations
route through TrustTunnel table `880`. System resolution of `api.openai.com` returns private
`10.255.0.31`, routed through corporate OpenVPN; its HTTPS root returns 403. Explicit DNS queries confirm corporate resolver `172.30.63.1` supplies that private
answer; Wi-Fi and `1.1.1.1` return public addresses. Intent of the mapping is unknown. Both Wi-Fi and OpenVPN advertise DNS
routing domain `~.`; TrustTunnel has `change_system_dns = false`.
See [diagnostic evidence](../log/2026-10-11-trusttunnel-client-kickstarter-routing.md).

## Control points

TorrServer on the PC: `http://192.168.192.107:8090`, Docker container `torrserver`.
Jackett on the PC: `http://192.168.192.107:9117`, Docker container `jackett`.
FlareSolverr: Docker container `flaresolverr`, reachable from Jackett at `http://flaresolverr:8191` on `home-media`, no host-published port.
Planned: OpenWrt `/etc/config/*`, procd service for the TrustTunnel client,
dnsmasq nftsets and policy routing table for VPN traffic.

## Operations

TorrServer cache inspection (2026-11-10): persisted `BitTorr` settings specify 64 MiB (`CacheSize: 67108864`) and RAM storage (`UseDisk: false`). Downloaded video pieces use a bounded cache rather than a permanent whole-film library. No cache tuning was applied; see [inspection](../log/2026-11-10-home-network-pc-torrserver.md#cache-configuration-inspected).

FlareSolverr: `docker ps --filter name=flaresolverr` checks its state; `docker exec jackett curl --max-time 15 http://flaresolverr:8191/` verifies readiness from Jackett. Stop only when requested with `docker stop flaresolverr`; Cloudflare-protected indexers depend on it. The user's RuTracker.org is now configured and its Test passed. Earlier download diagnostics showed DNS timeouts for NNM-Club; no DNS change was authorized or applied, and NNM-Club was not retested in the final solver-install turn.

Jackett: check with `docker ps --filter name=jackett`; open its root URL in a browser. Direct dashboard requests without cookies may return HTTP 400 (`Cookies required`); browser-style cookie support passed HTTP 200. Stop only when requested with `docker stop jackett`. Use the UI to transfer the generated API key into Lampa manually; do not copy it into notes. Scripted credential access belongs in the personal `.env`.

Lampa parser correction on 2026-11-10: the user confirmed the LAN URL, working Jackett UI in the TV browser and correct API key. After explicit approval, `AllowCORS` was changed from false to true through Jackett's settings API, which restarts its web host. Post-change settings and an authenticated API request with `Origin: http://lampa.mx` confirmed HTTP 200 and `Access-Control-Allow-Origin: *`. The three indexers remain configured and the container is running. TV-side retry after restarting Lampa and playback remain unverified; see [approved correction](../log/2026-11-10-home-network-pc-jackett.md#cors-correction-applied).

Subsequent user confirmation: Lampa now works. Current sources were then changed to Russian-language RuTor and NNM-Club; RuTracker.org awaits the user's manual credential entry. The earlier pending TV parser retry and three-source list are superseded. Specific movie audio/seek behavior has not been independently tested.

TorrServer: inspect with `docker ps --filter name=torrserver` and `docker logs --tail 30 torrserver`; host-side health check `curl --max-time 10 http://192.168.192.107:8090/echo`. Stop only when requested with `docker stop torrserver`. The PC must remain powered on during TV playback. Other open questions and the target deployment plan live in the repository above.

## Boundaries

The German VPN endpoint belongs to [trusttunnel-de](trusttunnel-de.md). The StrongSwan
VPS belongs to [vpn-gateway](vpn-gateway.md); its role in the target design is undecided.

## Access

Router LAN only, from the user's PC. No remote access yet.

## Related log entries

- [2026-11-11 shared nginx/Certbot refactor and local TV HTTPS configuration](../log/2026-11-11-home-network-shared-nginx-certbot.md)
- [2026-11-11 local Docker/Jackett Ansible roles prepared and checked](../log/2026-11-11-home-network-ansible-jackett-roles.md)
- [2026-11-10 FlareSolverr installed and RuTracker Test passed](../log/2026-11-10-home-network-pc-flaresolverr.md)
- [2026-11-10 three public Jackett indexers configured and tested](../log/2026-11-10-home-network-jackett-indexers.md)
- [2026-11-10 PC Jackett deployed for Lampa torrent discovery](../log/2026-11-10-home-network-pc-jackett.md)
- [2026-11-10 Lampa startup confirmed and PC TorrServer deployed](../log/2026-11-10-home-network-pc-torrserver.md)
- [2026-09-26 questions and deployment plan](../log/2026-09-26-home-network-initial-plan.md)

## PC TrustTunnel corporate VPN exclusion (2026-10-11)

Verified corporate OpenVPN endpoint `msk-vpn.youdo.sg:1194` UDP resolves45.159.210.228. Before change, it routed through TrustTunnel tun1/table880, nesting the corporate tunnel. User authorized one local route exclusion `45.159.210.228/32` in `[listener.tun].excluded_routes`; parse and exact-only diff assertions passed, mode0600 and private local backup retained. User restarted the client; public corporate VPN endpoint route bypasses TrustTunnel via WiFi as verified. Corporate VPN reconnection and controlled Nexus transport verification subsequently passed; no remote endpoint/firewall changes. See [client log](../log/2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md).

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.

## Jenkins public route exclusion prepared (October13)

Public Jenkins138.16.201.238 works via corporate OpenVPN, while ordinary requests route through TrustTunnel table880 and time out. Exactly138.16.201.238/32 was added to [listener.tun].excluded_routes in /home/slnnk/trusttunnel/trusttunnel_client.toml; Python3.12 tomllib and unique-route checks passed. Restart was not authorized or executed; the exclusion is inactive and ordinary requests still fail. See [local exclusion log](../log/2026-10-13-trusttunnel-client-jenkins-public-exclusion.md).
