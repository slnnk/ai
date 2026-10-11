---
system: trusttunnel-client
status: verified
checked: 2026-10-11
tags: [trusttunnel, openvpn, routing, dns]
---
# Kickstarter routing with TrustTunnel and corporate OpenVPN

## Summary

User-provided simultaneous-VPN diagnostics verify public Kickstarter, ChatGPT and GitHub destinations route through TrustTunnel table 880. System resolution of api.openai.com returns private `10.255.0.31`, routed through corporate OpenVPN tun1; HTTPS root returns 403. This establishes DNS-directed corporate routing for that API hostname, but not the reason for the private mapping or the agent's exact failing API request. Kickstarter HTTPS completes and returns 403 through the TrustTunnel route; site-side reason is unconfirmed.

## Context

Client configuration: `/home/slnnk/trusttunnel/trusttunnel_client.toml`, `vpn_mode = "general"`, IPv4 default included, `change_system_dns = false`. No Kickstarter exclusion. Corporate endpoint exclusion from [earlier work](2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md) remains present.

## Actions and findings

Read-only commands: `ip -br addr`, `ip rule show`, `ip route show table all`, `getent ahostsv4 www.kickstarter.com`, `getent ahostsv6 www.kickstarter.com`, per-address `ip route get`, `resolvectl status`, `ss -tnp`. No VPN or DNS settings changed.

Verified with OpenVPN disconnected: rules priority 30801 look up table 880 before main at 32766; rules priority 30800 bypass table 880 for source ports 1-1024 and 5900-5920. Both `8.47.69.0` and `8.6.112.0` resolve for www.kickstarter.com and route via `tun0`, table 880, source `172.16.219.2`. Firefox established connections to both destinations have that local source address. IPv6 route to `2a06:98c1:3122:8000::` is unreachable; no working IPv6 bypass observed.

User-provided OpenVPN log: corporate tunnel `tun1`, server pushes broad public prefixes including `52.0.0.0/6`, `34.192.0.0/10`, `188.114.98.0/24` and `188.114.99.0/24`; DNS `172.30.63.1`. Local profile `/home/slnnk/openvpn/a.solonenko.ovpn` adds `dhcp-option DOMAIN-ROUTE .`, and up script installs routed DNS domain `.`. Hypothesis: DNS behavior changes during simultaneous VPN use; effect on site access needs live comparison, not established as a bypass cause.

Log additionally shows duplicate `10.16.26.0/24`, invalid `172.28.0.111/24`, and cleanup permission errors after dropping UID/GID to nobody/nogroup. These are separate observed errors and do not prove Kickstarter routing failure. Current routes show no remaining corporate tunnel after termination.

## Simultaneous VPN evidence from user

Both tun0 (`172.16.219.2`) and tun1 (`172.30.63.6`) are active. Table 220 does not exist; its lookup falls through. Policy priorities remain unchanged. DNS routing domains show `~.` on both Wi-Fi (`192.168.192.1`) and corporate OpenVPN (`172.30.63.1`); the earlier statement that only corporate DNS receives all public queries was too categorical. Equal best matching routing domains can use both resolvers.

- www.kickstarter.com: `8.47.69.0`, `8.6.112.0` via tun0/table880; curl to `8.6.112.0` completes TLS and gets 403 in 0.232 seconds.
- api.openai.com: `10.255.0.31` via `172.30.63.1 dev tun1`; curl completes TLS and gets 403 in 0.165 seconds.
- chatgpt.com: `8.47.69.0`, `8.6.112.0` via tun0/table880; curl completes TLS and gets 403 in 0.208 seconds.
- github.com: `140.82.121.3` via tun0/table880; curl gets 200 in 0.835 seconds.

Verified by user explicit DNS queries: `172.30.63.1` returns `api.openai.com A 10.255.0.31` (TTL5); home resolver `192.168.192.1` and public `1.1.1.1` return `162.159.140.245` and `172.66.0.243`. Thus corporate DNS is the confirmed source of the private answer. Private gateway intent, exact agent endpoint and rejection body are unknown. HTTP403 at API root alone does not establish an authenticated API failure. Suggested token-free comparison: curl `/v1/models` with `--resolve` to a public address versus normal resolution. `/etc/hosts` check not completed because user typed `/etc/host` and `rg` was unavailable; use `grep -nE` against `/etc/hosts`.

Candidate minimal local profile fix: remove/comment `dhcp-option DOMAIN-ROUTE .` while preserving corporate search/routing domains and pushed routes. With Wi-Fi `~.` remaining, public lookups should prefer Wi-Fi and more specific corporate domains still use OpenVPN. Requires profile reconnect and resolver/cache verification; not implemented or authorized as a runtime action.

## Changed files and risks

Only this diagnostic note and the existing home-network map were updated. No runtime changes. DNS split routing is a candidate fix after confirming the private mapping source and desired corporate API policy; no fix applied.
