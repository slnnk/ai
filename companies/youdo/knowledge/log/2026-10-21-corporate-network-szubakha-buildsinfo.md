---
system: corporate-network
status: verified
checked: 2026-10-21
tags: [openvpn, dns, buildsinfo]
---
# OpenVPN s.zubakha buildsinfo access investigation

## Task

Investigate why buildsinfo is inaccessible over corporate VPN for s.zubakha. User identified the client OS as macOS; subsequent screenshots verified the resolver failure and successful local fix.

## Context

Current VPN gateway root@172.28.0.200, sc-gateway2.youdo.corp. Earlier route inspection: [gateway access](2026-10-13-corporate-network-openvpn-n-velikanets-routes.md).

## Actions

Read-only SSH inspection of server.conf, CCD s.zubakha, selected non-secret profile directives, matching status entries and recent PUSH_REPLY records. No remote changes.

## Findings

Server log at 2026-10-21 10:18:03 sends s.zubakha route 10.18.26.0/24, DNS 172.30.63.1 and DOMAIN youdo.local. CCD only adds routes; no push-reset. Stored profile uses msk-vpn.youdo.sg:1194/UDP and pull. Multiple same-CN sessions exist; their presence alone does not establish a fault. Gateway DNS resolves buildsinfo.vk-test.youdo.local via buildapi.dev.youdo.corp to 10.18.26.60 and HTTP returns401. The user's workstation also reached HTTP401 after starting OpenVPN.

Hypothesis: macOS resolver handling of .local or VPN DNS integration; not established without client output. Apple documents possible conflicts at https://support.apple.com/en-us/101903. Route installation on the affected Mac is also unverified. Server push proves transmission, not client application.

## Changes

Agent changed only local investigation records and central backlog. The user applied the macOS resolver configuration below; no agent remote changes.

## Status and risks

Resolved based on user-provided screenshots on 2026-10-21. Before the fix, nslookup used 172.30.63.1 and returned CNAME buildapi.dev.youdo.corp / A10.18.26.60, while dscacheutil returned no host result. Forced-IP curl with the original hostname returned HTTP401 and WWW-Authenticate Basic, proving HTTP reachability through VPN.

The user created /etc/resolver/youdo.local containing `nameserver 172.30.63.1`, flushed dscacheutil cache and sent HUP to mDNSResponder. The final screenshot shows ordinary curl without --resolve returning HTTP401 at 10:29:46GMT. System DNS resolution and HTTP connectivity are restored. Browser login was not independently verified. The static resolver requires corporate VPN reachability and must be updated if the VPN DNS address is reconfigured. Related diagnostic entry in [central TODO](../../../../TODO.md) is closed.

## Portable lesson

none
