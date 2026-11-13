---
system: home-network
status: verified
checked: 2026-11-13
tags: [router, openwrt, trusttunnel, podkop, failover]
---
# Cudy: automatic direct fallback and managed TrustTunnel recovery

## Task

User approved the proposed automatic direct fallback and reliable TrustTunnel process
recovery (`Сделай`). Apply only to Cudy192.168.1.1; keep selected domain policy,
temporary Archer DNS and existing upstream topology. No VPS or repository changes.

## Context

The [initial failure test](2026-11-13-home-network-cudy-openwrt-bringup.md#tunnel-failure-test)
found that listed FakeIP destinations failed on ifdown and the unmanaged client could
exit while netifd still reported up. Main system: [home-network](../systems/home-network.md).

## Actions

- Backed up podkop/sing-box/DHCP/network configuration, generated JSON and original
  protocol script under `/root/cudy-before-failover/` before remote edits.
- Replaced `/lib/netifd/proto/trusttunnel.sh` with a small handler using
  `proto_run_command`; installed `/usr/libexec/trusttunnel-supervisor`. The supervised
  foreground worker starts the client, waits for authenticated connection before up,
  reports down and retries5s after client exit. ifdown terminates worker and child.
- Worker resolves the endpoint hostname explicitly through WAN DHCP DNS and places
  only the numeric address in a mode0600 runtime TOML in tmpfs. Original credentials,
  configured TLS hostname and certificate verification are preserved. This removes
  startup dependence on podkop DNS; the exact cause of the historical failure remains
  unproven rather than retroactively diagnosed as a DNS loop.
- Converted podkop main-out to a selector, preferred trusttunnel-out, direct-out as
  initial/fallback choice. A separate list-free VPN section defines trusttunnel-out.
  All existing lists remain on main; no DNS/FakeIP change on path switching.
- Installed `/usr/libexec/cudy-vpn-failover` and procd init service
  `/etc/init.d/cudy-vpn-failover`, enabled at boot. Actual curl egress bound to tun0
  is checked every10s. Two failed probes choose direct, three successes choose VPN
  through the existing local Clash API. Selector interrupts affected connections
  on switching; existing applications may need to reconnect. Ordinary traffic stays direct.
- Initial network restart removed podkop's policy rule105 despite its nft table
  surviving. Enabled podkop's native WAN monitoring, registered via podkop restart;
  WAN-up now reloads/rebuilds podkop routing. Immediate JSON checking raced that async
  restart; later independent readiness/LAN checks passed. A second network restart
  verified automatic rule and VPN recovery. Both restart SSH sessions exited255 on
  lost connection; fresh SSH and runtime checks confirmed completed recovery.

Local code, installer and test artifacts: `/home/slnnk/ai-data/cudy/failover/`.
No extra packages installed. Deployed four-file SHA256 values match reviewed local files.

## Findings

All live probes use the PC's wired LAN/source192.168.1.165 and explicit Cudy DNS,
avoiding the PC VPN. Results retained as test-interface.json, test-client.json,
test-transport.json and test-network-restart.json in the local artifact directory.

1. Manual ifdown: selector switched directly in approximately13.1s; openwrt.org200,
   VPN-check domain200 with non-German egress and TMDB301, using the same FakeIP cache.
   Explicitly down interface stayed down until test cleanup called ifup. VPN returned
   automatically after3 healthy probes, with German egress152.234.226.70.
2. Client SIGTERM: supervisor replaced the PID and authenticated in approximately9.2s;
   subsequent LAN ordinary/VPN/TMDB probes passed without podkop restart.
3. Silent transport loss: temporary nft output rule blocked only Cudy TCP443 to the
   current relay while client was alive at injection. Selector fell back in19.6s,
   ordinary and listed probes passed directly. Deleting the test table automatically
   restored VPN and subsequent LAN probes passed. Final check confirms the table absent.
4. Network restart: WAN monitoring restored policy rule105/table105, supervisor/client
   and VPN selection. LAN ordinary200/VPN200 with German egress/TMDB301 passed. The1.1s
   value in the result is post-restart polling time, not total restart downtime.

Final state: tun0 up, client alive, monitor running under procd, selector on VPN after3
successes, sing-box JSON valid, ordinary default route through Archer, daily list update
finished, overlay13.5MiB free. All test/install commands finished; no failure injection remains.

## Changes

Router runtime files and UCI podkop only, as described above. No Git mutation, instruction
edits, publication, VPS configuration, household cutover or full router reboot.

## Status and risks

## Household cutover proposal (not authorized)

User requested a plan only. Read-only Cudy check confirms LAN192.168.1.1/24, WAN DHCP
and current upstream/DNS192.168.192.1. Default wireless entries still have OpenWrt SSID
and encryption none; activation state was not established by this query. Configure
protected Wi-Fi before use. Do not infer permission to move cables or change settings.

Propose preserving household192.168.192.0/24, gateway192.168.192.1 and media PC
192.168.192.107 via DHCP reservation so TV URLs and Docker bindings remain valid. Copy
existing SSIDs/security settings; password supplied privately through LuCI or personal.env,
not chat. Back up Archer and record WAN DHCP/MAC before work. During the approved window,
move ISP cable from Archer WAN to Cudy WAN while Cudy still uses test LAN1.0/24, check
actual ISP DHCP/DNS, replace the temporary Archer DNS with WAN-provided resolvers,
then power off Archer and apply the household LAN/Wi-Fi/reservation settings. Never
apply the old household LAN while Cudy WAN is still on the same Archer subnet.
Renew client leases and verify internet, VPN/direct fallback, Wi-Fi and media endpoints.
Rollback keeps Archer unchanged: restore ISP cable/power to Archer and disconnect Cudy.

## Current completion boundary

User-approved OpenAI routing addition: appended six deduplicated domain suffixes to
podkop.main.user_domains: openai.com, chatgpt.com, oaistatic.com, oaiusercontent.com,
oaistatsig.com and openaimerge.com. Existing lists retained. Backup:
`/root/cudy-before-openai-domains/podkop`. Reloaded podkop and validated sing-box JSON.
Explicit router DNS probes for base/API/WebSocket/static/file/CDN names all returned
FakeIP; selector trusttunnel-out/3successes and tun0 up verified. HTTPS API /v1/models
returned401/TLS0 without an API key, confirming transport/TLS only, not authenticated
ChatGPT or API functionality. List update completed; no task command remains running.
Source for domain selection: [OpenAI network recommendations](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps).
Third-party support/analytics/payment domains were not added by this request.

Wi-Fi diagnostics after user enable: radio1 configured SSID ARIIA, RU, channel100,
HE80, sae-mixed. hostapd rejected5500MHz with `Primary frequency not allowed` and
`AP-DISABLED`; no channel/SSID active and no stations. The earlier conditional channel100
recommendation did not fit the router's actual regulatory profile. `iw phy phy1 channels`
confirmed100-128 disabled while149/153/157/161 and36-64 are available. Proposed channel149
with80MHz instead, pending user UI application and on-air verification; no agent wireless
edits. radio0 remains disabled with default unencrypted OpenWrt entry; configure its
SSID/security before enabling. Passwords were not read. Future channel advice should
use the device's current channel list, not only generic DFS availability assumptions.

LAN change completed and verified after the user fixed SSH: current management
192.168.168.1/24, DHCP start100/limit150 (.100-.249), lease12h; wired PC received
192.168.168.165. User UI changes were preserved, including additional IPv6/LAN fields.
SSH authenticates using the previously verified host key and existing user key.
Post-change inspection found sing-box controller still bound to192.168.1.1:9090;
monitor selection was empty despite successful tunnel probes. Agent ran the authorized
podkop reload, regenerating controller192.168.168.1:9090. Policy rule105 survived and
selector/monitor returned to trusttunnel-out with3 successes. LAN probes through Cudy
DNS and wired binding passed: ordinary openwrt.org200, VPN-check200/German egress,
TMDB301. JSON valid and list update finished. Evidence:
`/home/slnnk/ai-data/cudy/lan-168-verification.json`. No background task remains.

This supersedes the SSH-refused/pending-verification observations below and the earlier
proposal to preserve household192.168.192.0/24. Archer WAN/DNS remains upstream;
household cutover has not happened. Because target LAN differs, media PC bindings and
TV endpoint addresses will need review during cutover; no media changes or reservations
were applied in this LAN task. The current probe helper now uses the new LAN address.

User confirmed UI change complete. Independent checks verify wired client
192.168.168.165/24, gateway192.168.168.1 and expected Cudy LAN MACd4:0d:ab:81:90:ae.
LuCI responds at192.168.168.1 (anonymous overviewHTTP403); TCP22 explicitly refuses
connections on repeated attempts. Thus actual LAN change is verified but exact DHCP
pool and post-change podkop/controller/VPN state cannot yet be inspected over SSH.
Request the user restart dropbear in LuCI System > Startup, then resume verification.
PC DNS output also includes the existing corporate resolver; do not infer Cudy's DNS
configuration from that client-wide setting. No additional router edits or jobs started.

Subsequent LAN decision: user chose192.168.168.0/24 with DHCP starting at .100;
proposed gateway192.168.168.1 and retained150-address pool (.100-.249). Read-only
preflight confirmed current LAN1.1/24 and no overlap with WAN192.168.192.0/24.
Prepared `/home/slnnk/ai-data/cudy/change-lan-168.sh` and added a local known_hosts
alias for192.168.168.1 using already verified Cudy public keys. Remote detached launch
failed because nohup is absent; log `/tmp/change-lan-168.log` reports command not found.
The script did not execute or alter router configuration; old-address SSH confirmed
LAN192.168.1.1/24. Local wired connection was reactivated and retained its old lease.
No background LAN job remains. User then took over (`Я сам поменяю через ui`): stop
agent router edits and wait for UI change confirmation. New subnet and updated podkop
controller address still need verification after the user applies them.

Approved failover/reconnect repair is complete and tested. Full router cold boot,
individual UDP/Discord voice behavior and future encrypted-DNS integration were not
tested. Direct fallback cannot bypass provider blocks; it preserves direct connectivity.
Own DNS readiness and household cutover remain in [central TODO](../../../TODO.md).
Before removing Archer, replace/adapt its temporary192.168.192.1 DNS path.

Check `cat /var/run/cudy-vpn/status.json`, `ifstatus tun0` and
`/etc/init.d/cudy-vpn-failover status`. Stop only when requested with
`/etc/init.d/cudy-vpn-failover stop`; stopping the monitor leaves the current selected
path and disables future automatic switching. `ifdown tun0` stops the managed tunnel;
monitor continues providing direct fallback. No unattended deployment/test job remains.

## Portable lesson

Readiness must reflect the actual connected process, not merely interface creation.
Preserve FakeIP handling while changing outbound so cached client addresses keep working.
Network-daemon restarts can remove independent policy rules even if nft tables survive;
use existing WAN triggers and verify actual client traffic after restart.
