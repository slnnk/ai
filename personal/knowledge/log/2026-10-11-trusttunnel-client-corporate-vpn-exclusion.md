---
system: trusttunnel-client
status: verified
checked: 2026-10-11
tags: [trusttunnel, openvpn, routing]
---
# Exclude corporate OpenVPN endpoint from TrustTunnel routing

## Task and context

User reported corporate Nexus UI works when the local TrustTunnel client is disabled and authorized editing its local configuration. Corporate OpenVPN profiles `~/openvpn/a.solonenko.ovpn` and `~/Downloads/a.solonenko.ovpn` specify UDP remote `msk-vpn.youdo.sg:1194`; DNS resolves `45.159.210.228`. Before the change, `ip route get 45.159.210.228` selected TrustTunnel tun1, table880, source172.16.219.2. Corporate VPN transport was therefore nested through TrustTunnel. Credentials and inline key/certificate material were not output.

## Changes and checks

Root agent added exactly `45.159.210.228/32` after existing `84.252.128.136/32` in `[listener.tun].excluded_routes` of `/home/slnnk/trusttunnel/trusttunnel_client.toml`. TOML parsing passed; deep before/after dictionary assertion confirms only that route changed. Config mode0600. Local backup `/home/slnnk/trusttunnel/trusttunnel_client.toml.before-corporate-vpn-20261011T172038Z`, mode0600, contains credentials and must remain private; no values were read into output or notes.

The user restarted TrustTunnel; live endpoint bypass is verified. No system firewall, remote VPN endpoint or routing configuration changed. Live route lookup for45.159.210.228 now uses192.168.192.1 viawlp0s20f3, source192.168.192.107, verifying the exclusion is active. Corporate VPN subsequently reconnected; controlled Nexus transport checks pass, browser symptom confirmation pending. Existing launcher `/home/slnnk/trusttunnel/run-trusttunnel.sh` changes to the client directory and executes sudo client with the exact configuration path. Restart requires stopping the existing foreground client then launching from `/home/slnnk/trusttunnel`; do not start a second concurrent instance.

## Findings and limits

Private networks, including10/8, were already excluded; missing exclusion concerned the public corporate VPN endpoint. Nested routing is directly verified, while packet-loss mechanism along the nested path remains only partly localized. User disabling TrustTunnel is supporting functional evidence; endpoint route is verified after restart, while Nexus checks require corporate VPN reconnection. Related company evidence: [Nexus recovery](../../../current/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md).

## Post-restart verification

User restarted the local client. `ip route get45.159.210.228` selects192.168.192.1 onwlp0s20f3, source192.168.192.107; public endpoint bypass is active. However10.18.24.233 also routes viaWiFi rather than corporate tun0, showing corporate VPN currently disconnected/missing private routes. Large-request probe timed out at connection after7.01s; this is not an MTU comparison. Reconnect corporate VPN before testing Nexus UI and large request again. No agent restart or additional network/configuration mutation occurred.

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.
