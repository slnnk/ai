---
system: home-network
status: hypothesis
checked: 2026-10-13
tags: [home, router, openwrt, trusttunnel]
---
# Home network

## Summary

- MediaManager compatibility2026-11-15 applied via approved Ansible: structured qBittorrent add responses, S2E1-9 season parser and title-only Jackett season search.16tests passed; app apply failed0. Separate approved transaction recovered the already-downloading MobLand S02 without a new add: API linked seasons[2]. Basic search now32season1 results across all3indexers and10season2 results from NoNaMe/RuTracker. User acceptance2026-11-16: one MobLand episode watched2026-11-15 with normal playback; basic MiniDLNA workflow accepted and TODO closed. Hardlink details not independently verified in this follow-up. [Recovery](../log/2026-11-15-home-network-mediamanager.md#qbittorrent-response-and-season-parser-recovery).

- MediaManager metadata routing2026-11-15: approved user-selected dorninger.co suffix now in Cudy Podkop; complete MobLand season responses222587/49076bytes in0.49/0.29s replace prior direct-path18KiB stalls. Helper reload exit9 independently reconciled to preserved list, valid sing-box/FakeIP and healthy VPN. Direct Jackett search finds season2 on all3indexers; MediaManager Basic defaults to season1, select2 or use Advanced MobLand query. No torrents started. [Evidence](../log/2026-11-15-home-network-mediamanager.md#mobland-metadata-route-and-season-search).

- MediaManager replacement2026-11-15 deployed through approved Ansible on existing master: stable1.12.3 UI8000, private PostgreSQL17, shared movies/tv directories and read-only native MiniDLNA. Radarr stopped with /opt/radarr retained; qBittorrent/Jackett unchanged. Login and MobLand/movie search verified, all3indexer caps200. Admin email admin@example.com; initial password in target /opt/mediamanager/.env0600, field MEDIAMANAGER_BOOTSTRAP_PASSWORD. No downloads/requests started during deployment; subsequent one-episode MiniDLNA playback accepted by user2026-11-16. See [acceptance](../log/2026-11-15-home-network-mediamanager.md#mobland-playback-accepted-2026-11-16). [Result](../log/2026-11-15-home-network-mediamanager.md#deployment-and-independent-verification).

- Radarr transition2026-11-15 deployed: qBittorrent8081 and Radarr7878 Docker plus native MiniDLNA/Home Movies active, /data/minidlna contains separate downloads and movies. Authenticated links to qBittorrent and three existing Jackett indexers all passed Test; manual search only, RuTor needs Other8000. Admin passwords in target /opt/radarr/.env root0600; no secrets in Git. Independent auth/API/catalog/service checks passed; no downloads started. Cleanup39.04GB and Lampa restoration remain complete. Real1.55GB film download/import/hardlink accepted: two paths share device/inode and nlink2, Radarr hasFiletrue, MiniDLNA catalogs1video; user confirms TV playback. Duplicate-add409 caused the misleading connection error; no repair needed.4K/HDR/seeking not newly verified. [Result](../log/2026-11-15-home-network-radarr-roles.md#deployment-and-authenticated-linkage-completed).

- Current playback diagnosis2026-11-15: user confirms extended smooth playback including seeking through native TV DLNA player, same saved full MKV. MSX/HTML5 static HTTP and TorrServer controls both stalled near matching media positions. This strongly implicates the browser playback path, not a proven exact decoder/firmware bug; native selected track/exact positions not instrumented. Accepted current workaround is saved file ->MiniDLNA ->native TV player; no live-torrent/Lampa integration implemented. See [native result](../log/2026-11-14-home-network-4k-playback.md#native-dlna-playback-accepted-smooth-including-seeking).
- External corroboration2026-11-15: Stremio issue2055/linked Reddit describe browser/app buffering with same-source DLNA success. Posted VIDAA support letter promises MKV web-path improvement inU9.6.1; later firmware reports mixed, including U7 regression2026-11-09. Same failure class likely, exact identity unproven. User screenshot shows V01.09.50W.Q0312; another55U7S PRO review sample reports V01.09.60W.Q0611, exact-unit OTA/fix unverified. User ran built-in update check: reports latest/no newer OTA offered on V01.09.50W.Q0312. Exact official downloads card ID9243 has only PDF, no firmware binary. USB update route documented generically for VIDAA U9; exact-unit USB package/fix needs Hisense confirmation. Vendor inquiry proposed, no contact/update authorized.16MB/overlay theory not established. See [sources and limits](../log/2026-11-14-home-network-4k-playback.md#stremio-vidaa-issue-and-linked-reddit-discussion-match-the-failure-class).
- Distinct captured events: long66.655s plain-page wait had urgent piece3603 incomplete by32KiB; earlier short waits had ready source data and TV receiver backpressure. Do not collapse all events into one proven fault or blame audio/Docker. Keep4GiB RAM; SSD trial explicitly rejected. Source scheduler/peer cause and separate DV7 startup error remain open.
- Current temporary MSX action2026-11-15 /playback-http-control/?v=d8c3d949bd47 runs the same1min watch ->back30s ->3min watch ->forward30min ->5min watch using a complete unchanged37390284387byte MKV through Apache, bypassing live TorrServer. Approved resume completed and byte/Range/CORS/MIME/page/observer checks passed; actual TV sequence completed with four non-seek waits, no errors. Local read-only TCP/event collector52696 finished (TCP0,bounded logs124), browser expired; no task background operation. Approved single-file tv-dlna-test/Home TV Test container running; native TV smooth including seeking confirmed by user. Host TCP sampler95644 finished0; container intentionally remains active for viewing; USB unavailable. Startup backup /opt/lampa/diag-backups/full-http-20261115T105604Z, original Lampa startup backup /opt/lampa/diag-backups/plain-test-20261114T195322Z/start.json. Temporary source/pages/redirects need approved cleanup. See [current setup](../log/2026-11-14-home-network-4k-playback.md#full-unchanged-mkv-http-control-installed-and-verified).

- New74.5GB MKV/DolbyVision7 torrent reproduced NETWORK error2026-11-14: 100-164Mb/s preload completed with392MiB ready before TV closed stream. HTTP206/Range/CORS valid; exact cause unproven, MP4/H264/AAC control pending.
- Home4K buffering persists2026-11-14 despite4GiB cache; during stall3890MiB complete data was ahead, TV stopped consuming TCP. VIDAA MQTT connection/state read succeeded on192.168.168.160:36669, no PIN or keys sent; no screen access. AAC2.0/no-subtitle test pending.
- Home-01 runtime tuning2026-11-14: user-approved TorrServer4GiB RAM cache /10 percent preload persisted; swap disabled now and in fstab, swap file retained. Gigabit link verified; same4K film retest pending.
- User confirmed local MSX/Lampa works2026-11-14;40GB4K playback buffered. Home server negotiated100Mb/s; user replaced patch cord and1000Mb/s full duplex is now verified. User confirms buffering remains after gigabit repair; no cache/router changes.
- Lampa CORS repaired and automatic TV media settings deployed2026-11-14: MSX now receives allow-origin *, bootstrap supplies TorrServer/Jackett/key before app startup; live script/API checks passed, TV retry pending.
- Home Jackett indexers migrated2026-11-14 from PC: RuTor, NNM-Club and RuTracker.org all passed Test on home-01. Target API key retained; TV instructions supplied, playback not yet confirmed.
- Home media deployed2026-11-14 on home-01 /192.168.168.2: Lampa8080, TorrServer8090, Jackett9117 and unpublished FlareSolverr on Docker bridges. LAN HTTP checks passed; PC-data/indexer migration and TV cutover remain separate.
- Home media roles prepared2026-11-14 for inventory home-01 /192.168.168.2: Lampa, TorrServer, Jackett/FlareSolverr use Docker bridges; home.yml includes ansible-user/common/sshd and excludes nftables. Local checks passed; no deployment.
- Home server `home` uses persistent static `192.168.168.2/24` on `enp1s0` as of 2026-11-14; gateway/DNS `192.168.168.1`, SSH, routing and DNS verified. Netplan backup retained; reboot not tested.

- TrustTunnel1.1.12 and podkop0.7.24/sing-box1.13.21 run on Cudy with verified selective LAN routing and temporary user-approved Archer DNS.
- Automatic direct fallback and managed TrustTunnel recovery are verified for interface down, client exit, transport loss and network restart; household cutover remains pending.
- Archer C64 supplies the existing home LAN; Cudy WR3000S v1 now runs OpenWrt 25.12.5 behind it on a test LAN.
- User ISP cutover verified2026-11-13: Cudy WAN100.64.6.13/16, gateway100.64.0.2; prior Archer-upstream description above is historical. PC VPN/FakeIP recovery subsequently confirmed; old PC media bindings retired2026-11-15 after home-server migration.
- Cudy LAN192.168.168.1/24 and DHCP192.168.168.100-.249 verified2026-11-13; wired client192.168.168.165. SSH recovered by user; podkop API refreshed to192.168.168.1:9090 and LAN DNS/direct/VPN probes passed. WAN/DNS still through Archer192.168.192.1.
- Media Station X and Lampa startup on the TV are user-confirmed as of 2026-11-10.
- Current media host is home-01 /192.168.168.2: Lampa8080, TorrServer8090, Jackett9117 and internal FlareSolverr; user reconfirmed2026-11-15.
- PC Jackett/TorrServer/FlareSolverr containers, images, anonymous solver volume and empty home-media network removed2026-11-15. Jackett data deleted; user subsequently deleted root-owned PC TorrServer data, locally verified absent2026-11-15.
- Old PC endpoints192.168.192.107:8090/9117 are retired; no PC binding/TV URL update is needed. See [cleanup](../log/2026-11-15-home-network-pc-media-cleanup.md).
- Components and Operations describe the current deployment and checks.
- Historical VPN diagnostics remain below; open work is tracked in central TODO.
- Decision2026-11-13: plan Jackett/FlareSolverr on the home server; the VPS attempt failed readiness under observed resource pressure and was cancelled. The user will switch off the VM; home-server media deployment and indexer migration subsequently completed2026-11-14.
## Staleness review (2026-11-04)

Historical review: its AmneziaWG backup direction was cancelled by the user on 2026-11-13.

The home deployment remains a plan: local `home-infra/AGENTS.md` still records no deployment. Its version-3 `PLAN.md` and the explicit decisions in `AGENTS.md` specify podkop with TrustTunnel as a netifd interface, AmneziaWG UDP as backup, and encrypted DNS through the user's own VPS AdGuard Home with Unbound recursion; raw dnsmasq nftset routing is the fallback, not the selected primary design. Amend the planned-components paragraph accordingly and remove VPS AdGuard Home from the deferred list. Fail-open, FakeIP/upstream compatibility and actual tunnel egress still require the existing bench tests in the central backlog. No router, server, hardware purchase or client restart was checked during this review. StrongSwan's trial on the TrustTunnel host was removed on 2026-11-04, as recorded in the [removal log](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md); the separate old gateway's current state remains unconfirmed.

Status `hypothesis`: the target design is planned, not deployed. Verified facts are marked.

## Purpose

Home LAN with router-level split routing by domain lists: everything direct, only listed
domains (YouTube, Instagram, torrent trackers, ...) through the user's TrustTunnel endpoint
(see [trusttunnel-de](trusttunnel-de.md)). Encrypted DNS with ad blocking (AdGuard Home),
TorrServer for the TV, basic monitoring. No remote access, no guest or IoT segments.

- Radarr website VPN routing2026-11-15: approved radarr.video suffix added to Cudy podkop.main.user_domains, subdomains covered. Backup /root/cudy-before-v2fly-radarr/podkop; old list/other UCI preserved, sing-box/FakeIP and home-01 HTTPS200 verified. Browser refresh pending user. See [result](../log/2026-11-14-home-network-4k-playback.md#radarr-website-vpn-routing-applied-and-independently-verified).

## Proposed selection and predownload workflow

Latest comparison scope2026-11-15: compare home-01, NAS and Android HDMI box for4K torrent viewing; exclude Uptime Kuma and both photo applications from this analysis. Earlier full-home-server evaluation below is historical broader context, not the active comparison workload. Existing server +completed-only DLNA is the lowest equipment-cost proposal; HDMI Android player +existing server backend is the on-demand proposal; NAS does not improve native TV decoding. No option chosen or deployment authorized. See [comparison](../log/2026-11-15-home-network-media-station-comparison.md).


Planning update2026-11-15: user considers Synology as a full home-01 replacement,
budget not allocated, compare options before deciding. Revised photo workload uses
Synology Photos; Immich excluded from this comparison. Other services remain
Radarr/Jackett/qBittorrent/DLNA/Uptime Kuma. Earlier16GB target driven by Immich is
superseded;8GB is an initial recommendation,4GB may suit light use, exact model/
recognition/library load and expansion need checking. HEIC/HEVC preview support
may involve client-side Image Assistant. DS725+/DS925+ remain reference classes,
not selected purchases; consider lower configurations as well. No purchase,
migration or shutdown authorized; existing home-01/DLNA stay active. See
[revised scope](../log/2026-11-14-home-network-4k-playback.md#synology-evaluation-replaces-immich-with-synology-photos).


2026-11-15 discussion only: user accepts phone/PC control; TV remote UI optional.
Initial proposal is qBittorrent +VueTorrent, reuse existing Jackett search and
publish only completed downloads to native TV through MiniDLNA. Incomplete files
stay outside DLNA; no transcoding or duplicate media copy needed by design.
Radarr +qBittorrent is an alternative for poster/catalog-oriented film selection.
No choice/deployment approved yet; current one-file DLNA stays active. Storage,
retention/seeding policy and end-to-end publication checks need definition before
implementation. See [requirements and sources](../log/2026-11-14-home-network-4k-playback.md#proposed-convenient-torrent-predownload-and-native-dlna-workflow).

## Components

- TV firmware observed from user screenshot2026-11-15: V01.09.50W.Q0312, extended W.Q0312.X0001.W01.Y01.J01.9.05.00; no device/serial identifiers retained. Exact newer OTA/version and MKV fix for this unit unverified. See [firmware evidence](../log/2026-11-14-home-network-4k-playback.md#exact-tv-firmware-provided-by-screenshot).
- Temporary native DLNA control2026-11-15: tv-dlna-test, vladgh/minidlna digest sha256:cdfa0ed2bc9482b350c387d793ec6e2d41749cdafd9b69a4fe3579c0995469ef, host networking/enp1s0,1900UDP/8200TCP, Home TV Test. Bind only existing playback-http-control/source.mkv ->/media/test.mkv read-only, --rm/restartno. One film plus artwork, catalog/Range checks passed; user reports extended smooth playback including seeking. No automatic torrent publishing/Lampa integration. Container intentionally active; check sudo docker ps --filter name=tv-dlna-test; stop sudo docker stop tv-dlna-test requires approval. See [launch and result](../log/2026-11-14-home-network-4k-playback.md#native-dlna-playback-accepted-smooth-including-seeking).

- Home-media constraint (user2026-11-14): do not add external player portals/services or switch MSX startup to msxplayer.ru. Keep additional playback components local to home-01/TV. Existing external services were not cancelled. Local MSX video-menu trial remains a proposal requiring implementation authorization. See [decision](../log/2026-11-14-home-network-4k-playback.md#additional-external-player-portals-rejected).

- Home media RAM/swap changes (2026-11-14): user requested4GiB TorrServer RAM cache, superseding the1GiB proposal, and separately disabled swap. Official settings API preserved all other fields; CacheSize4294967296/PreloadCache10/UseDiskfalse verified in API and persistent JSON. /swap.img swapoff and fstab autostart disable applied with backups; final swap0, no active swap units, about10GiB RAM available. Swap file retained; no reboot/test of same movie yet confirmed. See [runtime result](../log/2026-11-14-home-network-4k-playback.md#user-approved-ram-cache-and-swap-changes).

- Home4K playback (2026-11-14): local Lampa startup/automatic settings accepted working by user. Ethernet TV buffers on a40GB4K file. Server CPU/RAM had headroom; enp1s0 negotiated100Mb/s despite gigabit-capable ends. User replaced patch cord;1000Mb/s full duplex verified with zero short-sample errors. Default64MiB TorrServer RAM cache unchanged. Retest result pending; no complete buffering cause proven. See [passive diagnostics](../log/2026-11-14-home-network-4k-playback.md).

- Lampa MSX startup and bootstrap (2026-11-14): user status0 report revealed missing CORS despite HTTP200 in TV access logs. Applied Apache headers and header-aware readiness, then user-requested automatic TorrServer/Jackett/key browser bootstrap. Home playbook starts backends before Lampa; source key comes from target ServerConfig with suppressed logs/diffs, stays out of Git, and is served to trusted LAN clients. Browser defaults apply once per settings fingerprint; subsequent manual choices/favorites remain. Server/script/key checks passed, actual TV retry still pending. This supersedes earlier manual API-key entry instructions. See [fix and verification](../log/2026-11-14-home-network-lampa-cors-bootstrap.md).

- Home indexer migration (2026-11-14): user-requested transfer copied only rutor/noname-club/rutracker configs and the source DataProtection key over SSH, preserving target ServerConfig/API key and existing key. Private target backup /opt/jackett/migration-backup-20261114T164258Z retained. All three final Test requests returned204; RuTor transient TLS reset cleared on retry without config changes. Old PC stack remained running at that time; user authorized its removal2026-11-15, completed including user-deleted root-owned TorrServer data (absence verified). TV cutover and broader media data were not changed during the migration itself. See [migration and TV instructions](../log/2026-11-14-home-network-home-indexer-migration.md).

- Home media deployment (2026-11-14): explicitly requested home.yml applied ansible-user/common/sshd/Docker and media without nftables on home-01. Initial lscr.io image timeout resolved by approved Jackett-only retry (failed0/unreachable0). All four containers run on bridges with unless-stopped and zero initial restarts; LAN HTTP8080/8090/9117 and internal solver checks passed. No PC-data/indexer migration or TV cutover. See [deployment](../log/2026-11-14-home-network-home-media-deployment.md).

- Home media local preparation (2026-11-14): user approved existing ansible master from b857c7e; home-01 is192.168.168.2. New Lampa/TorrServer roles and bridge-capable combined Jackett/FlareSolverr role are configured through group_vars/home.yml. home.yml bootstraps ansible-user, then common, sshd, Docker and media, with no nftables. FlareSolverr is unpublished; HTTP8080/8090/9117 bind only the LAN address. Syntax/native Compose/preservation/MSX checks passed; no deployment, migration, TV cutover or Git publication. See [preparation](../log/2026-11-14-home-network-ansible-home-media.md).

- Google Play downloads (2026-11-14): user enabled Google Play in podkop and confirmed downloading works. Keep this user-applied routing as the known working configuration. DNS log inspection found no blocking rule on the observed Play API and gvt1 download queries; exact direct-path failure remains unverified. No further diagnostics requested. See [result](../log/2026-11-14-home-network-google-play-podkop.md).

- User decision (2026-11-14): planned direct Internet, VPN and Wi-Fi speed measurements are cancelled without testing. Device inventory and separate reachability/media follow-ups were not cancelled by this decision. See [decision](../log/2026-09-26-home-network-initial-plan.md#speed-measurements-cancelled-by-user-2026-11-14).

- User cancellations (2026-11-14): the Archer C64 is powered off and retains its settings; its backup task is cancelled without creating a backup. The user also explicitly cancelled the mobile-phone DNS setup, superseding the previous deferred status. Do not resume phone Private DNS, propose automatic switching as ongoing work, or revive either task without a new request. Home DNS through Cudy and VPS AdGuard remains in use.

- Android DNS decision (2026-11-14): user declined permanent Private DNS to d.slnnk.com after the podkop/FakeIP bypass consequence was explained. Do not enable it or substitute automation without a new request. Home DNS via Cudy remains accepted; mobile DNS setup was initially deferred and subsequently cancelled explicitly by the user on 2026-11-14. See [decision](../log/2026-11-14-home-network-cudy-dot-client-cache.md#android-permanent-private-dns-declined-2026-11-14).

- User applied Cudy own-DoT cutover (2026-11-14): podkop uses d.slnnk.com over TLS with bootstrap77.88.8.8; router FakeIP and VPN selector are healthy. A stale PC DNS cache was corrected by the user; subsequent PC resolution matches router FakeIP198.18.0.57 and routes via Cudy, with no PC tun0. The user confirmed Codex and ChatGPT work without the separate PC VPN. Home cutover and DoT/FakeIP compatibility are accepted complete; mobile-phone DNS setup remains pending. See [cutover diagnosis](../log/2026-11-14-home-network-cudy-dot-client-cache.md).

- DNS deployed and externally verified (2026-11-13): AdGuard Home 0.107.80 is live on it-garage-de-02 / d.slnnk.com with public DoT, private admin, selected DoH upstreams and local ad filtering. Initial playbook failed0/unreachable0; trusted certificate expires 2027-02-11. Port53/3000 are not public. The separately approved narrow SSH forwarding exception is applied: a real authenticated panel tunnel returned HTTP200 and forwarding to loopback8081 was administratively prohibited. Home/mobile cutover is pending. See [runtime result](../log/2026-11-13-home-network-ansible-dns-role.md#deployment-approved-and-verified-2026-11-13).

- Earlier local DNS role preparation (2026-11-13, runtime status superseded by the deployment result above): roles/dns and playbooks/dns.yml target it-garage-de-02 / d.slnnk.com with AdGuard Home 0.107.80, public DoT, private admin, Cloudflare and AdGuard Unfiltered DoH, without Unbound. Native local DNS and Ansible checks passed; no runtime deployment/client cutover. The admin bcrypt hash is now Vault-encrypted in DNS group vars; its generated password is stored as ADGUARD_HOME_ADMIN_PASSWORD in personal/.env. See [preparation and approvals](../log/2026-11-13-home-network-ansible-dns-role.md).

- User decision (2026-11-13): deploy only one AdGuard Home, with external encrypted upstreams (superseding the earlier recursive Unbound proposal), on VPS it-garage-de-02 (inventory group dns), using d.slnnk.com. Home clients and phones on mobile networks will use this encrypted DNS endpoint. Cancel the home-server AdGuard Home instance; the earlier two-AdGuard DNS chain below is superseded. Subsequent user decision (2026-11-13): encrypted DNS-over-TLS on TCP 853 is public, without client IP/CIDR/ASN restrictions, for dynamic home and mobile clients. Any Internet client knowing the endpoint can use it. Do not expose plain DNS on port 53 or the loopback-only admin panel. This replaces the earlier unresolved allowlist proposal; deployment requires separate approval. Local dns-role preparation in /home/slnnk/mygit/ansible on existing master from b857c7e was approved, paused for discussion before edits, then explicitly resumed by the user with the final upstream-only design. The VPS was subsequently deployed with explicit approval; client/router DNS changes remain pending.

- User decision (2026-11-13): AmneziaWG backup tunnel is cancelled on both Cudy and the VPS. Keep TrustTunnel with the existing verified direct fail-open behavior. Earlier AmneziaWG mentions in dated planning records are historical and superseded; no deployment, removal or other runtime changes are authorized by this planning decision.

- User clarification (2026-11-13): the target home server must also host the Lampa web frontend; Media Station X on the TV opens that locally hosted frontend. The planned home-server services are Lampa, TorrServer, Jackett, FlareSolverr and Uptime Kuma. AdGuard Home placement was subsequently consolidated on the VPS by the user. This clarifies placement only; deployment is not authorized or completed. The older external lampa.mx startup description below records historical setup.

- Current remote-media decision (2026-11-13): the actual VPS target was `dline-de-01` (`166.1.36.104`) and the selected domain was `ext.slnnk.com`, superseding the historical `dline-pl-01`/`tv.slnnk.com` proposal below. Approved Ansible applied base/security/Docker/nginx and issued TLS, but failed FlareSolverr readiness; HetrixTools was not reached. User chose future home-server placement and will shut down the VM. No remote shutdown, swap, DNS cleanup, PC migration or TV cutover was performed. The final failed Ansible command has exited. Home host/resources and implementation remain to be agreed in central TODO; existing Cudy/podkop can route blocked tracker destinations. See [attempt, cancellation and plan](../log/2026-11-13-home-network-dline-de-jackett-deployment.md#final-outcome-and-home-server-decision).

- Router verified 2026-11-13: Cudy WR3000S v1 runs standard-layout OpenWrt 25.12.5, kernel `6.12.94`, `apk 3.0.5`, with SSH key access and separate WAN/LAN subnets. TrustTunnel client1.1.12 and iamvladdy netifd/LuCI integration are installed; `tun0` up and authenticated curl egress152.234.226.70 verified. Ordinary default route still uses Archer; podkop0.7.24 and sing-box1.13.21 now provide verified selective routing with user-approved temporary Archer DNS. Overlay13.5MiB free. See [bring-up](../log/2026-11-13-home-network-cudy-openwrt-bringup.md#trusttunnel-installed-and-verified).

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
  not WR3000 v1 with 16 MB flash, not WR3000 v2 which is unsupported) with podkop list-based routing, TrustTunnel as a netifd interface; raw dnsmasq nftsets and policy routing are the fallback; 8-port unmanaged switch; Debian mini PC (N100 class) with docker
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

## Home-01 hardware

Verified over read-only SSH on 2026-11-16 with `lscpu` and `dmidecode`:

- CPU: Intel Core i3-10105, 4 cores / 8 threads, 3.70 GHz base, 4.40 GHz maximum, 6 MiB L3 cache.
- Motherboard: Micro-Star International (MSI) PRO H410M-B (MS-7D82), revision 1.0.
- RAM: 16 GiB total, two A-DATA Technology 8 GiB DDR4 DIMMs, one in each channel A/B; single rank, 1.2 V. SMBIOS part number is the generic `DDR4 3200`; configured speed is 2667 MT/s. Exact retail module model was not exposed.
- SMBIOS reports 64 GB maximum and four logical device entries, including two empty entries; physical slot count and upgrade limits were not independently verified.

## Control points

Cudy management/SSH: `192.168.168.1`; DHCP pool `.100-.249`,12h leases. LAN change
via user UI and post-change podkop reload verified. Monitor reads its current controller
from generated JSON; current selector API is192.168.168.1:9090. ISP cutover subsequently verified2026-11-13; media now runs on home-01 and old PC endpoints are retired2026-11-15. See [LAN completion evidence](../log/2026-11-13-home-network-cudy-failover.md#current-completion-boundary).

TorrServer on home-01: `http://192.168.168.2:8090`.
Jackett on home-01: `http://192.168.168.2:9117`.
Lampa on home-01: `http://192.168.168.2:8080`.
FlareSolverr is internal to the home-server Docker stack; the old PC stack was removed2026-11-15.
Cudy: TrustTunnel is managed by netifd interface `tun0`; runtime TOML under
`/opt/trusttunnel_client/`, LuCI Status > TrustTunnel. Selective routing is active through podkop.

## Operations

For new reviewed Podkop domain lists, use [cudy_add_domains.py](../../scripts/cudy_add_domains.py) with the source file and `--label`. The default validates the local file. `--apply` changes the router and requires separate approval for the reviewed domain list. Keep source lists and run receipts under `~/ai-data/cudy/`.

LinkedIn routing added2026-11-15: all12 literal names from the user-specified v2fly
list appended to main manual suffix rules, including the three full-prefixed names
as suffixes with explicit user approval. All12 FakeIP checks, preserved prior domains,
unchanged remaining UCI settings, generated config and active VPN egress verified.
Backup `/root/cudy-before-v2fly-linkedin/podkop`; reload exit9 was followed by successful
independent state checks. See [result](../log/2026-11-15-home-network-cudy-linkedin-podkop.md).

Telegram domains expanded2026-11-13: all21 literal domains from the user-specified
v2fly telegram list added to manual main list, retaining existing Telegram community/IP
coverage and all other domains. All21 FakeIP probes, generated JSON and German VPN
egress passed. Backup `/root/cudy-before-v2fly-telegram/podkop`; local source/helper
and verification `/home/slnnk/ai-data/cudy/telegram-domains/`.

OpenAI domain expansion2026-11-13: user chose manual addition of all24 literal v2fly
openai entries, including CDN/voice/telemetry, plus explicitly authorized replacement
webpubsub.azure.com for the regex. Added20 new suffix records after deduplication;
existing main domains retained (39 total). No external JSON subscription installed.
Verified26 FakeIP names including dynamic Azure host, valid generated config and VPN
egress152.234.226.70. Backup `/root/cudy-before-v2fly-openai/podkop`; local artifacts
`/home/slnnk/ai-data/cudy/openai-domains/`.

Post-cutover diagnosis2026-11-13: PC own TrustTunnel routes router FakeIP198.18/15
into PC tun0/table880, causing Firefox/OpenAI connection refusal. Wi-Fi-bound requests
through Cudy reach HTTPS403/TLS0. Added the FakeIP range to PC client exclusions;
user restart/working-site confirmation and route lookup verify activation. Subsequent
standalone Codex403 targets already-covered chatgpt.com but PC cache retains real apex
IPs for up to50min; fresh Cudy answers are FakeIP. User cleared the system cache,
verified198.18.0.57 and supplied a successful restarted Codex CLI response screenshot;
the403 incident is resolved without additional domains or application changes. Router now
uses observed public AdGuard UDP/bootstrapGoogle DNS, not Archer; agent did not change it.
Historical PC media bindings192.168.192.107 were superseded by home-01 deployment; old local containers removed2026-11-15.
See [cutover diagnostics](../log/2026-11-13-home-network-cudy-cutover-pc-fakeip.md).

OpenAI routing added2026-11-13 at user's request: domain suffixes openai.com,
chatgpt.com, oaistatic.com, oaiusercontent.com, oaistatsig.com, openaimerge.com in
podkop main user list, including their subdomains. Router DNS probes return FakeIP;
selector uses TrustTunnel. API HTTPS401/TLS0 without key verifies transport.
Backup `/root/cudy-before-openai-domains/podkop`; existing lists preserved.

Wi-Fi on-air confirmation2026-11-13: user supplied an ARIIA associated-station screenshot
with client192.168.168.234, received signal approximately-51dBm, HE80/two spatial streams
and PHY rates1080.6/960.7Mbit/s. This supersedes the earlier AP-disabled observation below.
Screenshot does not show the channel number; do not infer149 was verified from it.
Actual payload/internet throughput, coverage at distance and radio0 activation remain
unverified. No additional router changes were requested or performed in this discussion.

Wi-Fi status2026-11-13: user-configured radio1 ARIIA/RU/channel100/HE80/sae-mixed
failed AP startup;5500MHz disabled in actual regulatory profile. Runtime channel list
allows149-161 for an80MHz block; proposed149 pending UI application/verification.
radio0 is still disabled and retains an unencrypted OpenWrt template. No station
connected at inspection; do not describe Wi-Fi as working until on-air/client checks.

Cudy approved repair verified2026-11-13: netifd owns a foreground TrustTunnel supervisor,
with WAN DNS bootstrap and authenticated readiness. Procd service cudy-vpn-failover
checks actual tun0 egress every10s;2 failures select direct-out,3 successes restore
trusttunnel-out via the main-out selector. FakeIP/DNS remain active. Native podkop WAN
monitoring restores policy routing after network restart. Four end-to-end scenarios passed:
manual ifdown/direct fallback13.1s, client exit/reconnect9.2s, transport loss/fallback19.6s,
and network restart. Selected/direct LAN HTTP(S) egress was verified after each recovery.
Test rules removed; monitor/client/selector healthy. Status:
`cat /var/run/cudy-vpn/status.json`, `ifstatus tun0`; monitor stop command:
`/etc/init.d/cudy-vpn-failover stop` (leaves current path, stops automatic switching).
Backup `/root/cudy-before-failover/`; local artifacts `/home/slnnk/ai-data/cudy/failover/`.
Full cold boot and individual UDP voice tests remain unverified. Cutover must adapt
temporary Archer DNS before disconnecting it. See [repair](../log/2026-11-13-home-network-cudy-failover.md).

Historical pre-repair test2026-11-13 (superseded by repair above): with `ifdown tun0`, unlisted openwrt.org stayed200 but
listed VPN service/TMDB connections reset while DNS retained FakeIP. Automatic direct
fallback is not implemented. `ifup tun0` alone initially reported up, then the client
exited after connection attempts and the TUN vanished. Cause unresolved. Restored by
stopping podkop, reconnecting TrustTunnel until its process/log/device were ready, then
starting podkop. LAN ordinary200/VPN200 German egress/TMDB301 and both services verified
again. No permanent repair applied; household cutover should wait for approved fail-open
and reconnect corrections. See [failure evidence](../log/2026-11-13-home-network-cudy-openwrt-bringup.md#tunnel-failure-test).

User confirmed2026-11-13 that own DNS/server is not ready and then explicitly chose
temporary DNS through Archer192.168.192.1. Podkop is now configured/enabled with VPN
section tun0, youtube/meta/telegram/discord lists and custom Lampa/TMDB/tracker domains.
dnsmasq forwards to sing-box127.0.0.42, upstream/bootstrap Archer over UDP; updates go
through TrustTunnel daily. Wired LAN tests verified German VPN egress and different
direct egress, YouTube200/TLS0, TMDB301/TLS0, Lampa HTTP200, ordinary HTTPS200/TLS0.
The fail-open/reconnect failures have been repaired as recorded above. Own encrypted DNS and household cutover remain pending. Backup:
`/root/cudy-before-podkop-config/`. Check `podkop get_status` and
`podkop get_sing_box_status`; `/etc/init.d/podkop stop` stops routing/sing-box and
restores the previous DNS path. See [configuration evidence](../log/2026-11-13-home-network-cudy-openwrt-bringup.md#podkop-configured-with-temporary-archer-dns).

Historical installation stages (superseded by the running configuration above):
Cudy dependency installation verified 2026-11-13 after explicit user approval:
`kmod-tun 6.12.94-r1`, `ip-full 6.18.0-r2`, `curl 8.23.0-r1` installed through APK
with four library dependencies. `/dev/net/tun` exists, tool version checks pass,
default route remains through Archer. At the dependency stage overlay had40.8MiB free;
subsequent client installation left approximately33.3MiB. TrustTunnel is now running,
podkop0.7.24 and sing-box1.13.21 were subsequently installed but remain disabled pending
configuration. Final overlay free13.7MiB. Installation auto-started unconfigured podkop;
it was stopped, boot disabled and exact DHCP backup restored. DNS queries through loopback
and LAN and direct HTTPS passed; network/firewall unchanged, tun0 up. Backups for this
stage: `/root/cudy-before-podkop/`. LuCI: Services > Podkop.
Check `ifstatus tun0`; stop with `ifdown tun0` only when authorized.
Network/firewall backups: `/root/cudy-before-trusttunnel/`; no LAN-wide VPN routes or
DNS changes applied. Full reboot recovery and selective fail-open tests remain unverified.
See [bring-up log](../log/2026-11-13-home-network-cudy-openwrt-bringup.md).

TorrServer cache inspection (2026-11-10): persisted `BitTorr` settings specify 64 MiB (`CacheSize: 67108864`) and RAM storage (`UseDisk: false`). Downloaded video pieces use a bounded cache rather than a permanent whole-film library. No cache tuning was applied; see [inspection](../log/2026-11-10-home-network-pc-torrserver.md#cache-configuration-inspected).

FlareSolverr: `docker ps --filter name=flaresolverr` checks its state; `docker exec jackett curl --max-time 15 http://flaresolverr:8191/` verifies readiness from Jackett. Stop only when requested with `docker stop flaresolverr`; Cloudflare-protected indexers depend on it. The user's RuTracker.org is now configured and its Test passed. Earlier download diagnostics showed DNS timeouts for NNM-Club; no DNS change was authorized or applied, and NNM-Club was not retested in the final solver-install turn.

Jackett: check with `docker ps --filter name=jackett`; open its root URL in a browser. Direct dashboard requests without cookies may return HTTP 400 (`Cookies required`); browser-style cookie support passed HTTP 200. Stop only when requested with `docker stop jackett`. Use the UI to transfer the generated API key into Lampa manually; do not copy it into notes. Scripted credential access belongs in the personal `.env`.

Lampa parser correction on 2026-11-10: the user confirmed the LAN URL, working Jackett UI in the TV browser and correct API key. After explicit approval, `AllowCORS` was changed from false to true through Jackett's settings API, which restarts its web host. Post-change settings and an authenticated API request with `Origin: http://lampa.mx` confirmed HTTP 200 and `Access-Control-Allow-Origin: *`. The three indexers remain configured and the container is running. TV-side retry after restarting Lampa and playback remain unverified; see [approved correction](../log/2026-11-10-home-network-pc-jackett.md#cors-correction-applied).

Subsequent user confirmation: Lampa now works. Current sources were then changed to Russian-language RuTor and NNM-Club; RuTracker.org awaits the user's manual credential entry. The earlier pending TV parser retry and three-source list are superseded. Specific movie audio/seek behavior has not been independently tested.

TorrServer now runs on home-01; LAN health endpoint `http://192.168.168.2:8090/echo`. Old PC containers and their automatic restart policies were removed2026-11-15; the PC is no longer required for playback. Other open questions and the target deployment plan live in the repository above.

## Boundaries

The German VPN endpoint belongs to [trusttunnel-de](trusttunnel-de.md). The StrongSwan
VPS belongs to [vpn-gateway](vpn-gateway.md); its role in the target design is undecided.

## Access

Router LAN only, from the user's PC. No remote access yet.

## Related log entries

- [Home server static LAN address](../log/2026-11-14-home-network-server-static-ip.md)

- [2026-11-14 Cudy own-DoT and stale PC DNS diagnosis](../log/2026-11-14-home-network-cudy-dot-client-cache.md)
- [2026-11-13 local VPS AdGuard Home role prepared](../log/2026-11-13-home-network-ansible-dns-role.md)
- [2026-11-13 VPS Jackett attempt cancelled; future home-server placement planned](../log/2026-11-13-home-network-dline-de-jackett-deployment.md)
- [2026-11-11 shared nginx/Certbot refactor and local TV HTTPS configuration](../log/2026-11-11-home-network-shared-nginx-certbot.md)
- [2026-11-11 local Docker/Jackett Ansible roles prepared and checked](../log/2026-11-11-home-network-ansible-jackett-roles.md)
- [2026-11-10 FlareSolverr installed and RuTracker Test passed](../log/2026-11-10-home-network-pc-flaresolverr.md)
- [2026-11-10 three public Jackett indexers configured and tested](../log/2026-11-10-home-network-jackett-indexers.md)
- [2026-11-10 PC Jackett deployed for Lampa torrent discovery](../log/2026-11-10-home-network-pc-jackett.md)
- [2026-11-10 Lampa startup confirmed and PC TorrServer deployed](../log/2026-11-10-home-network-pc-torrserver.md)
- [2026-09-26 questions and deployment plan](../log/2026-09-26-home-network-initial-plan.md)

## PC Russian domain bypass check (2026-11-12)

Read-only tests of client 1.0.49 confirmed direct Wi-Fi upstream TCP/TLS connections for `yandex.ru`, `mail.ru`, `ozon.ru` and `vk.ru`, despite application-side flows entering TrustTunnel tun0/table 880. Control `example.com` stayed in the tunnel. `2ip.ru` timed out but also showed direct Wi-Fi sockets; `gosuslugi.ru` was inconclusive. General bypass failure was not reproduced; browser-specific traffic was not captured. Configuration and services unchanged. See [diagnostic evidence](../log/2026-11-12-trusttunnel-client-ru-bypass-check.md).

## PC TrustTunnel corporate VPN exclusion (2026-10-11)

Verified corporate OpenVPN endpoint `msk-vpn.youdo.sg:1194` UDP resolves45.159.210.228. Before change, it routed through TrustTunnel tun1/table880, nesting the corporate tunnel. User authorized one local route exclusion `45.159.210.228/32` in `[listener.tun].excluded_routes`; parse and exact-only diff assertions passed, mode0600 and private local backup retained. User restarted the client; public corporate VPN endpoint route bypasses TrustTunnel via WiFi as verified. Corporate VPN reconnection and controlled Nexus transport verification subsequently passed; no remote endpoint/firewall changes. See [client log](../log/2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md).

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.

## Jenkins public route exclusion prepared (October13)

Public Jenkins138.16.201.238 works via corporate OpenVPN, while ordinary requests route through TrustTunnel table880 and time out. Exactly138.16.201.238/32 was added to [listener.tun].excluded_routes in /home/slnnk/trusttunnel/trusttunnel_client.toml; Python3.12 tomllib and unique-route checks passed. Restart was not authorized or executed; the exclusion is inactive and ordinary requests still fail. See [local exclusion log](../log/2026-10-13-trusttunnel-client-jenkins-public-exclusion.md).
