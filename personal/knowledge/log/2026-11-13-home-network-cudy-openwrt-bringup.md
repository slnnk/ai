---
system: home-network
status: verified
checked: 2026-11-13
tags: [router, openwrt, ssh]
---
# Home network: Cudy OpenWrt installation and SSH baseline

## Task

Guide the user through Cudy installation and verify SSH access before router VPN work.

## Context

Existing Archer C64 remains upstream. Target design is recorded in
[home-network](../systems/home-network.md) and `/home/slnnk/mygit/home-infra/PLAN.md`.

## Actions

Downloaded the Cudy transition archive from the manufacturer's linked Google Drive;
ZIP CRC validation passed. Extracted `cudy_wr3000s-v1-sysupgrade_20251119.bin`.
Downloaded the official OpenWrt 25.12.5 standard-layout sysupgrade image; SHA256
matched the official release manifest:
`b0a26c80fa458b4b743508a6a6de8aa9d19867fa3deb1c3c49e40194d61aa8b2`.
The user flashed both images and supplied LuCI screenshots. The user confirmed
internet and DNS diagnostics work, then added their SSH key.
Agent SSH read-only checks succeeded with strict host-key checking and key authentication.

## Findings

- User-reported original hardware/firmware: `WR3000S V1.0`, `2.4.6-20250527-170229`.
- Verified board: `cudy,wr3000s-v1`, OpenWrt `25.12.5`, kernel `6.12.94`, `apk 3.0.5`.
- Hostname `cudy`; LAN `192.168.1.1/24`; WAN DHCP `192.168.192.146/24`,
  default gateway `192.168.192.1` (Archer). No LAN/WAN subnet overlap.
- Overlay available approximately 41.9 MiB; available RAM approximately 127 MiB.
- Clock was correct (`2026-11-13`, MSK) during SSH verification.
- Source review: iamvladdy installer detects apk and first installs `kmod-tun ip-full curl`.
  Podkop documentation describes 25.12 APK installation. Integration and combined storage
  requirements remain untested on this router.

## Changes

Firmware changes were performed by the user. Agent downloads are under
`/home/slnnk/ai-data/cudy/`. Baseline checks made no router writes.
After explicit user approval (`Сделай`), executed
`apk update && apk add kmod-tun ip-full curl`. All three were initially absent.
Installed `kmod-tun 6.12.94-r1`, `ip-full 6.18.0-r2`, `curl 8.23.0-r1` and four
dependency libraries. Installation completed successfully. Read-only checks confirmed
all three installed, working tool versions, `/dev/net/tun` as a character device,
the original default route through Archer and 40.8 MiB overlay free.
No network restart, VPN configuration or VPS changes were performed at the dependency stage.

## TrustTunnel installed and verified

User approved item 1 (`1 - сделай`): install and configure TrustTunnel. Installed
official ARM64 client `1.1.12`, archive SHA256
`10402be7e715f35380e8bcf67e2d8f2ceb9fad81eef8274a472e3a085a0d5cc1`,
matching the official GitHub release asset digest. Installed reviewed iamvladdy
netifd/LuCI integration at commit `469570cd3918a98878691d58f9429ceb77d65783`.
Local preparation/deployment helper: `/home/slnnk/ai-data/cudy/trusttunnel_setup.py`.
No Ansible repository edits or publication.

Existing authentication was decrypted from the inventory using the Vault password
route in `personal/.env`, kept in process memory and transferred over SSH; no credentials
were printed or written to local artifacts. Router runtime TOML is mode0600 in
mode0700 `/opt/trusttunnel_client`. Endpoint `v.slnnk.com:443`, HTTP/2, TLS verification
enabled. Config has empty included/excluded routes, killswitch disabled, MTU1280 and
`change_system_dns=false`. Created netifd `tun0` and a masquerading firewall zone with
reject input/forward and accept output; no LAN forwarding or podkop rules added.
Original network/firewall files were copied to `/root/cudy-before-trusttunnel/`.

Network reload did not discover the newly installed protocol (`proto:none`, NO_DEVICE).
A network service restart loaded it; the original SSH session later exited with
Broken pipe, while fresh SSH checks succeeded. LuCI exposes `luci.trusttunnel`.
`tun0` reports up with IPv4 `172.16.219.2/32`. A temporary host route to the IP-check
service permitted a curl request bound to tun0; authenticated VPN egress was
`152.234.226.70` (German backend). The temporary route was removed by cleanup.
The ordinary route to `1.1.1.1` still uses Archer on wan and direct HTTPS returned200
with verified TLS. No table880 routes or policy rules were left behind. After installation,
overlay had approximately33.3MiB free; combined podkop/client capacity is not yet proven.
No VPS changes or router reboot were performed.

Sources: [official client release](https://github.com/TrustTunnel/TrustTunnelClient/releases/tag/v1.1.12),
[integration](https://github.com/iamvladdy/trusttunnel-openwrt/tree/469570cd3918a98878691d58f9429ceb77d65783).

## Podkop installed, routing not configured

User approved installation (`Хорошо, установи podkop`). Downloaded official release0.7.24
APKs for podkop, luci-app-podkop and Russian translation; each matched its GitHub asset
SHA256 digest. Installed these with sing-box1.13.21-r1, jq, bind-dig, coreutils-base64,
nft-tproxy modules and libraries. Existing basic dnsmasq retained. Overlay free fell
from36.7MiB to13.7MiB; compressed recursive download used19.3MiB RAM and was cleaned up.
Backups: `/root/cudy-before-podkop/` (network, firewall, DHCP). Local artifacts/helper:
`/home/slnnk/ai-data/cudy/podkop/`.

Attempted `IPKG_NO_SCRIPT=1 apk add` did not prevent the podkop post-install hook from
starting it. Startup aborted on missing outbound configuration. Wrapper then exited
because sourcing `/lib/functions.sh` under nounset referenced unset `IPKG_INSTROOT`.
Packages themselves installed successfully. Explicitly stopped and disabled podkop and
sing-box; no running procd instances or boot links remain. Podkop stop changed dnsmasq
settings despite aborted startup. Restored the exact pre-install DHCP file and restarted
dnsmasq. An immediate query raced startup; subsequent independent queries through
127.0.0.1 and192.168.1.1 both resolved openwrt.org. Direct HTTPS200/TLS0, ordinary route
through Archer and tun0 up verified; network/firewall match backups and only base policy
rules remain. Temporary APK files in RAM were removed.

Verified installed APK names, sing-box version and LuCI menu at `admin/services/podkop`
(Services > Podkop). No domain lists or target tunnel/DNS config applied. Defaults use a
public DNS resolver and empty proxy endpoint; leave disabled pending selected home setup.
Local helper corrected to use APK no-scripts option and tolerate unset variables while
sourcing OpenWrt helpers; corrected install path was not rerun against installed router.
Sources: [release](https://github.com/itdoginfo/podkop/releases/tag/0.7.24),
[documentation](https://podkop.net/docs/install/).

## Podkop configured with temporary Archer DNS

User selected the second proposed option (`Второй вариант`): temporarily use Archer
DNS while own DNS/server is unavailable. This is a task-scoped exception to the target
own encrypted DNS design, not authorization for a VPS deployment or permanent public DNS.
Backup before configuration: `/root/cudy-before-podkop-config/` (podkop, DHCP, sing-box
UCI and JSON). Helper: `/home/slnnk/ai-data/cudy/podkop/configure-archer-dns.sh`.

Configured UDP DNS and bootstrap192.168.192.1, source br-lan, VPN section main bound
to tun0, community lists youtube/meta/telegram/discord, daily updates through the local
service proxy and TrustTunnel. User domain list: themoviedb.org, tmdb.org, jac.red,
lampa.mx, lampa.app, bylampa.online, rutor.info, rutor.is, nnmclub.to, nnm-club.me,
rutracker.org, rutracker.net, rutracker.nl. Exclusion section retains v.slnnk.com direct.
dnsmasq forwards to127.0.0.42; sing-box forwards actual DNS to Archer. Podkop boot enabled;
standalone sing-box boot disabled as intended because podkop owns its startup.

Preflight manually invoked the installed generator and validated JSON. Startup invoked it
again, skipping attachment of existing local user rulesets: community lists worked but
custom domains received real addresses. Diagnosed generated rule_set references and
resolved with the package reload, which clears and rebuilds temporary rulesets. Custom
domains then returned FakeIP. Local helper now relies on the package's own pre-start
JSON validation and avoids double generation; that corrected fresh-install path was not rerun.

Verification used the PC's wired enp0s31f6/source192.168.1.165, explicit Cudy DNS queries
and curl device binding/resolve, avoiding the PC TrustTunnel route. All four community
samples received FakeIP; rutracker.org/tmdb.org/lampa.mx also received FakeIP after reload.
Steam/openwrt.org/api.ipify.org and v.slnnk.com received real IPs. ip.podkop.fyi/check
through Cudy returned German backend152.234.226.70; unlisted api.ipify.org returned
a different valid public IP. LAN HTTPS: YouTube200/TLS0, TMDB301/TLS0,
openwrt.org200/TLS0. Lampa HTTP200; lampa.mx HTTPS had a TLS handshake failure and is
not verified. One initial YouTube request timed out; subsequent LAN and direct-tun0
requests both returned200/TLS0. Generated JSON check passed; daily list update completed.
Default route remained through Archer, with only podkop's mark-specific policy rule added.
Overlay free13.5MiB. Runtime APIs report podkop enabled and sing-box running/DNS configured;
the one-shot podkop init script itself does not remain a long-running process.

At the configuration stage no tunnel-down/reboot/household cutover test had been performed. No VPS changes. Initial
configuration/reload/list-update commands completed. Podkop/sing-box and TrustTunnel
remain active; check `podkop get_status`, `podkop get_sing_box_status` and `ifstatus tun0`.
Authorized stop: `/etc/init.d/podkop stop` restores its DNS path and stops sing-box;
TrustTunnel remains separate (`ifdown tun0`).

## Tunnel failure test

User approved item3 (`3 - сделай`): test access while TrustTunnel is down and restore
it afterwards. Helper `/home/slnnk/ai-data/cudy/podkop/test_tunnel_failure.py` and
results `tunnel-failure-result.json` bind all probes to PC wired LAN and Cudy DNS.
Before: openwrt.org200, VPN service200/German egress, TMDB301.
After `ifdown tun0`: openwrt.org still200, DNS still responds, but VPN service and
TMDB retain FakeIP and return TLS connection resets. Automatic fail-open FAILED:
unlisted direct traffic survives; listed traffic does not fall back to direct.

The finally handler issued `ifup tun0`. netifd reported up before authentication
completed. Client then exited with `Number of connection attempts exceeded`;
the tun device disappeared while netifd still reported up and its pidfile was stale.
Endpoint HTTPS remained200/TLS0. Exact cause of this failed reconnect is not proven.
This is not evidence of only a sing-box stale-interface issue or a diagnosed DNS loop.

Restored original runtime without persistent rule edits: stop podkop, ifdown tun0,
wait2s, ifup tun0, wait for actual client connected log, then start podkop. Independent
LAN probes then passed again: openwrt.org200, VPN service200/German backend152.234.226.70,
TMDB301. Process existence, kernel tun0 device, netifd up, podkop enabled and sing-box
running/DNS configured were verified. List update finished. The initial test helper
exit1 preserves the failed automated recovery; later manual recovery evidence is appended
to the same JSON rather than overwriting the failure. No test commands remain running.

No fail-open hook, watchdog or persistent reconnect repair was implemented. These
are proposals requiring explicit authorization before household cutover. Other bench
tests involving the future own DNS and reaching the VPS public IP remain pending centrally.

## Current status and risks

Superseded after explicit repair approval: automatic direct fallback, supervised client
recovery and WAN-triggered routing restoration are now deployed and verified in four
failure/restart scenarios. See [repair outcome](2026-11-13-home-network-cudy-failover.md).
Earlier proposal and failed-test details below retain their historical context.

Repair proposal, not implemented: keep sing-box/FakeIP active and introduce a selector
for selected traffic with TrustTunnel as preferred and direct as fallback, switched
through the local Clash API by a small health monitor. Probe actual egress bound to
tun0 rather than only ifstatus; proposed10s interval, two failures to fallback and
three successes to restore VPN. Keep normal unlisted routing and temporary Archer DNS.
Separately investigate the failed client reconnect and correct process supervision:
the installed netifd handler backgrounds the client with no_proto_task1 and reports
up on TUN creation, without verifying authentication or tracking subsequent exit.
These are confirmed design observations, not proof of the reconnect's root cause.
Validate interface-down, process-exit and silent transport loss scenarios before cutover.
No permission to implement is inferred from the user's request for a proposal.

Own DNS service is not deployed and its server is not ready. The user-approved temporary
Archer DNS configuration is now active. Its later replacement is tracked centrally.

SSH access, the router baseline, TrustTunnel egress and selective LAN routing are verified;
existing bench tests remain open in [central TODO](../../../TODO.md).
TrustTunnel runs under netifd; podkop is configured/enabled and selective routing verified.
The original failure was repaired in the linked follow-up; target DNS integration and
household cutover remain pending in central TODO; further
router changes require explicit approval per action. No deployment commands remain.
Check with `ifstatus tun0`; stop only when authorized with `ifdown tun0`.

## Portable lesson

On this router, `IPKG_NO_SCRIPT=1` did not prevent APK service startup. Verify actual
service and DNS state rather than inferring hook suppression. OpenWrt shell helpers also
assume unset variables are permitted. Preserve configuration before invoking cleanup hooks.

## Internet LED inspection

Read-only SSH inspection on2026-11-13 at the current LAN address192.168.168.1
confirmed `white:wan-online` brightness `0`, trigger `[none]`, and no UCI LED
sections. The Internet LED has no configured automatic trigger; its dark state
does not establish a WAN or Internet failure. The separate WAN port indicator
reports Ethernet link/activity. OpenWrt identifies the Internet GPIO as
`LED_FUNCTION_WAN_ONLINE` in the [board source](https://github.com/openwrt/openwrt/blob/main/target/linux/mediatek/dts/mt7981b-cudy-wr3000s-v1.dtsi).
No router configuration was changed and no background operations remain.
