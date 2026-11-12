---
system: trusttunnel-client
status: verified
checked: 2026-11-12
tags: [routing, bypass, diagnostics]
---
# PC Russian domain bypass verification

## Task

Check the user's suspicion that Russian domains bypass exclusions and travel through TrustTunnel. Read-only runtime diagnostics; no network settings changed.

## Context

PC client 1.0.49, PID 12583, started with `/home/slnnk/trusttunnel/trusttunnel_client.toml`. General mode, exclusions include `ru`, `*.ru`, `xn--p1ai` and `*.xn--p1ai`. `change_system_dns = false`; system resolver uses Wi-Fi router with the `~.` routing domain. Corporate VPN is also active. See [home network](../systems/home-network.md).

## Actions

Read selected nonsecret configuration, process command line, interface addresses, policy rules, resolver status and TCP sockets. Created bounded TLS connections with Python socket/ssl, bypassing application HTTP proxies. Compared site-specific TCP sockets with `ss -tn`. Read-only diagnostics required execution outside the sandbox because netlink and system bus access were blocked. Root socket process ownership was unavailable (`sudo -n` required a password); destination/source socket tuples remained visible.

## Findings

- `yandex.ru` (5.255.255.77), `mail.ru` (90.156.232.4), `ozon.ru` (185.73.193.68) and `vk.ru` (87.240.132.67) completed TLS. Each had both the original application-side socket with source 172.16.219.2 and a direct upstream socket bound to Wi-Fi 192.168.192.107. Bypass works for these tested domains.
- Control `example.com` had application-side sockets through the TUN and no matching direct Wi-Fi socket in the sample.
- `2ip.ru` (188.40.167.82) TLS/HTTPS timed out, but direct Wi-Fi sockets to its destination were observed. The timeout does not demonstrate tunnel use. Its external IP response was not obtained.
- `gosuslugi.ru` TCP connection timed out; its bypass result is inconclusive. `ipinfo.ru` did not resolve.
- Table 880 selects TrustTunnel tun0 for public destinations, including Russian site IPs. This alone cannot diagnose domain bypass: the client can accept the original flow and create a direct upstream connection.
- These tests do not prove every browser request or every Russian domain bypasses. Browser-specific behavior was not captured.
- Current upstream documentation describes `exclusions_tcp_early_ack_enabled` for wildcard/external-DNS handling; the installed old client was not changed and support was not established. No upgrade is needed to explain the four successful direct-flow observations.

Sources: [CLI configuration](https://github.com/TrustTunnel/TrustTunnelClient/blob/master/trusttunnel/README.md), [changelog](https://github.com/TrustTunnel/TrustTunnelClient/blob/master/CHANGELOG.md).

## Changes

Knowledge bookkeeping only. No client configuration, restart, installation, repository publication or remote change.

## Status and risks

Requested general check completed. A blanket Russian-domain bypass failure was not reproduced. Site-specific and browser-specific failures remain outside the verified sample; no repair was requested or proposed as necessary. Existing related TODO entries do not require changes. All diagnostic sessions completed.

## Portable lesson

none
