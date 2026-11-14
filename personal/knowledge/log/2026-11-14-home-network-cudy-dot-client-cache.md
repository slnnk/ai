---
system: home-network
status: verified
checked: 2026-11-14
tags: [dns, podkop, fakeip, codex]
---
# Cudy DoT cutover: stale PC DNS and Codex 403

## Task

User switched podkop DNS to the new VPS and reported Codex403 unless the separate
PC VPN client is enabled. Screenshots show a blocked HTML response from the
Codex responses URL, including a browser denial page. Do not infer that the
AdGuard upstream DNS provider itself returned the HTTP403.

## Context

[Home network](../systems/home-network.md), Cudy192.168.168.1, PC Wi-Fi and an active
standalone TrustTunnel client. The earlier same-host cache incident is recorded in
[prior investigation](2026-11-13-home-network-cudy-cutover-pc-fakeip.md#codex403-stale-system-resolver-cache).

## Actions and verified findings

Read-only router UCI/runtime inspection confirmed dns_type dot, dns_server
d.slnnk.com, bootstrap77.88.8.8; generated sing-box DNS has TLS/UDP/FakeIP servers.
Both dnsmasq and sing-box returned chatgpt.com198.18.0.57. Failover status selected
trusttunnel-out with3successes and0failures. The loopback Clash API probe on9090
failed to connect; this is not proof that routing is down. No router settings,
service restart or VPN toggle was performed by the agent.

PC Wi-Fi192.168.168.249 uses router192.168.168.1 for DNS. Its system resolver still
returned real A8.47.69.0/8.6.112.0 and two real AAAA addresses, while direct DNS
query to the router returned the FakeIP. Observed remaining TTLs were98s for A
and192s for AAAA. Route198.18.0.57 uses Wi-Fi/Cudy, so the previous FakeIP exclusion
from the PC tunnel remains effective.

A Wi-Fi-bound curl request forced to198.18.0.57 for
chatgpt.com/backend-api/codex/responses returned HTTP405 and successful TLS
verification. This is the expected unsupported-GET outcome and demonstrates
reachability through the intended router path, not authenticated model success.
The observed stale client DNS is the next concrete issue to correct; no new
missing domain rule or VPS DNS fault was established.

## Status and risks

Router own-DoT configuration is applied by the user and observed active. Final
household/Codex acceptance is pending: user should run sudo resolvectl flush-caches,
restart the affected Codex/browser process and retest without the separate PC VPN.
Do not automatically disable that VPN, clear caches or change external state.
Phone/mobile configuration remains pending. Open actions are in
[central TODO](../../../TODO.md). All diagnostic commands exited; no background
operation remains. No secret/token/dialogue log was collected.

## Portable lesson

none

## User recovery confirmed (2026-11-14)

The user performed the advised cache flush/application restart. Subsequent
read-only PC checks showed system resolution chatgpt.com198.18.0.57, identical
to the router answer, with routing via192.168.168.1 on Wi-Fi. PC tun0 no longer
existed. The user then explicitly confirmed Codex and ChatGPT work without the
separate PC VPN client. This closes the stale-cache incident and validates the
home DoT/FakeIP path for the reported use case. The earlier pending authenticated
Codex verification is superseded by this user confirmation, not by the prior
unsupported-GET405 test. The agent made no runtime/cache/VPN changes.

The home DNS cutover and AdGuard-DoT/FakeIP compatibility check are accepted
complete. Mobile-phone DNS setup and the separate VPS-public-IP-inside-tunnel
bench check remain in central TODO. No background operation remains.

## Android permanent Private DNS declined (2026-11-14)

The user asked about using VPS DNS on Android across all networks. Explained the
system Private DNS hostname setting and the concrete home-network conflict:
direct encrypted DNS to the VPS bypasses podkop DNS/FakeIP. Official references:
https://developers.google.com/speed/public-dns/docs/using/#android and
https://podkop.net/docs/client-dns/ . After this explanation the user declined
that setup. Do not enable permanent Android Private DNS or introduce automation
as a substitute without a new request. Home clients continue using the router
DNS/AdGuard path; no phone setting was inspected or changed by the agent.
The broader mobile-DNS follow-up is deferred, not implemented or silently
cancelled for every phone. No alternative was selected or authorized. This
supersedes the earlier active request to connect Android using a permanent
hostname setting. Central TODO retains the deferred mobile scope explicitly.

## Mobile DNS cancelled, not deferred (2026-11-14)

After the earlier refusal of permanent Android Private DNS, the user explicitly
asked to remove the broader deferred phone-DNS task because they will not do it.
The phone-DNS task is now cancelled without implementation, not merely deferred.
No alternate mobile configuration or automation is an active follow-up. Existing
phone settings were not inspected or changed. Home DNS via Cudy remains accepted.
This supersedes the earlier pending/deferred mobile scope in this note and map.
