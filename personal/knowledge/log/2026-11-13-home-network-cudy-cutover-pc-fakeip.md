---
system: home-network
status: verified
checked: 2026-11-13
tags: [router, podkop, trusttunnel, dns, cutover]
---
# Cudy cutover: local PC TrustTunnel captures router FakeIP addresses

## Task

Verify user-reported ISP cutover and investigate Firefox connection failures for
openai.com and help.openai.com. Duplicate cutover message treated as one event.

## Context

[Home network](../systems/home-network.md), Cudy192.168.168.1 with podkop FakeIP and
router TrustTunnel; PC retains its own TrustTunnel client as previously requested.

## Actions

Read-only WAN/DNS/service diagnostics, then compared ordinary PC curl with a request
bound to wlp0s20f3. Prepared the necessary local client route exclusion; no client
restart, router configuration change or container modification in this investigation.

## Findings

- Cudy now receives ISP DHCP100.64.6.13/16, gateway100.64.0.2, DNS185.154.74.2 and
  77.88.8.8. No Archer route remains. LAN192.168.168.1/24; PC Wi-Fi192.168.168.249,
  wired interface has no IPv4 address.
- Podkop was found using dns.adguard-dns.com via UDP and bootstrap8.8.8.8, rather
  than prior Archer DNS. Agent did not make or overwrite this intervening configuration.
  One ordinary router DNS query timed out; later resolver queries answered. This is not
  proof of a persistent resolver failure or provider DNS spoofing.
- Root router curl to openai.com/help.openai.com reached HTTPS403/TLS0. PC system
  DNS returned198.18.0.46 and198.18.0.44; route lookup selected PC tun0/table880.
  Ordinary PC curl failed with connection refused. Same requests bound to Wi-Fi Cudy
  reached403/TLS0. Thus PC TrustTunnel captures the router's synthetic addresses;
  HTTPS403 confirms transport reachability, not authenticated browser success.
- Sing-box also logged missing fakeip records after intervening reloads; cached client
  addresses are a separate potential follow-up if failures remain after route correction.
- Local TT process PID52525 observed from host namespace; launched by
  `/home/slnnk/trusttunnel/run-trusttunnel.sh` using sudo and the local TOML. No systemd
  ownership was established. Sandbox process enumeration was empty and not interpreted
  as no client; host read confirmed the process.
- Jackett/TorrServer still publish192.168.192.107:9117/8090 despite PC moving to
  192.168.168.249. These old bindings/TV endpoints need approved cutover work.

## Changes

Added198.18.0.0/15 to listener.tun.excluded_routes in
`/home/slnnk/trusttunnel/trusttunnel_client.toml`. Parsed TOML validation confirmed all
other values preserved. Existing plaintext credentials were not printed or duplicated.
Nonsecret prior route list: `/home/slnnk/ai-data/cudy/local-client-routes-before-fakeip.json`.
Client configuration directory is not a Git repo. Running VPN remains unchanged until restart.

## Codex403: stale system resolver cache

User restarted the local client and confirmed the initial sites work; current route
lookup for198.18.0.57 uses Wi-Fi/Cudy rather than PC tun0, confirming the exclusion
active. User then reported standalone Codex0.167.1 returns403 when local VPN is off.
Scoped Codex log inspection extracted only request hosts/paths/status markers, not
tokens or dialogue content. Failing endpoint is chatgpt.com/backend-api/codex/responses,
already covered by the existing chatgpt.com domain_suffix rule. Router fresh answers:
chatgpt.com198.18.0.57, ab.chatgpt.com198.18.0.58; suffix list is intact.

PC system resolver cache still returned real chatgpt.com addresses8.47.69.0/8.6.112.0
with remaining TTL approximately3000s, and real openai.com addresses with TTL1200s.
With PC VPN active these real addresses route into PC tun0; without it they bypass
the intended router FakeIP routing. User screenshot also shows stale real apex IPs
while auth.openai.com already gets FakeIP. A Wi-Fi-bound forced-FakeIP GET to the exact
Codex responses URL reached405/TLS0 without authentication (expected unsupported GET,
not an authenticated model test). Therefore missing wildcard coverage is not established;
stale cache is the concrete next issue to correct before retesting authenticated Codex.

Attempted `sudo -n resolvectl flush-caches` after describing the action; sudo requires
a password and the operation did not execute. Subsequent queries confirm cache unchanged.
Ask user to run `sudo resolvectl flush-caches` locally, then verify dig chatgpt.com returns
FakeIP and restart the affected standalone Codex window. Never request the password in chat.
No resolver/router/domain changes were made in this diagnostic stage. Browser/Codex success
without PC VPN remains pending user activation/retest; no background diagnostic jobs remain.

## Current follow-up

Telegram expansion completed after user supplied the v2fly telegram file and requested
addition: all21 literal domain suffixes added manually, no duplicates or previous
domain removals. Existing Telegram community/IP list retained; preflight also found
geoblock already enabled by intervening user changes, which was preserved. Source,
reviewed apply script and verification are in `/home/slnnk/ai-data/cudy/telegram-domains/`;
reusable direct-import helper `/home/slnnk/ai-data/cudy/add_domains.py`. Backup:
`/root/cudy-before-v2fly-telegram/podkop`. Generated JSON check passed; all21 domains
returned FakeIP; previous-domain preservation verified. Selector VPN/3successes and
egress152.234.226.70 confirmed. This verifies routing, not Telegram voice/message behavior.
Source: [v2fly telegram](https://github.com/v2fly/domain-list-community/blob/master/data/telegram).

Manual v2fly expansion completed after explicit instruction to add all domains directly.
User then explicitly chose suffix webpubsub.azure.com instead of the one regex entry.
Fetched the requested raw source, parsed24 literal domain entries (including full: hosts
and tagged telemetry), skipped the regex during literal import and then added the
user-selected replacement. Five literal suffixes already existed; added19 plus the
replacement suffix,20 new records total. All previously configured domains retained;
main user list now39 entries. Plain manual entries inherit podkop domain_suffix behavior.
No remote subscription, custom converter service or duplicate-removal operation applied.
This supersedes the earlier proposed MetaCubeX integration below, which was not selected.

Backup `/root/cudy-before-v2fly-openai/podkop`; source/manifest/reviewed script and
verification under `/home/slnnk/ai-data/cudy/openai-domains/`. Full list reload and
sing-box JSON validation passed. All25 domain records plus a generated dynamic Azure
host (26 probes) returned FakeIP; previous list preservation verified, selector VPN/3
successes, German egress152.234.226.70 and completed list update confirmed. No task jobs
remain. These probes verify routing, not authenticated Sora/voice/telemetry functionality.

Concrete proposal after inspecting installed podkop: connect the ready sing-box source
JSON at `https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/openai.json`
through main.remote_domain_lists. The current artifact matches the referenced v2fly
list's suffix/exact/regex coverage, including voice and telemetry. Native remote JSON
support preserves these semantics and uses the existing daily refresh/proxy detour;
no custom converter, local HTTP server or podkop patch is needed. Local domain lists
in this installed version import plain suffixes only, so local JSON there is unsuitable.
After verifying loaded rules/DNS/transport, propose removing only five duplicated manual
suffixes; retain openaimerge.com because it is absent in this artifact. Keep the main
selector so failover behavior is preserved. This is a proposal, not installation permission.

User referenced [v2fly OpenAI list](https://github.com/v2fly/domain-list-community/blob/master/data/openai)
for comparison. It is broader than the six manually added suffixes: additional branded
domains, exact CDN/Azure endpoints, a webpubsub regex, LiveKit voice endpoints and tagged
telemetry. Existing podkop plain-domain importer accepts validated domain suffixes,
not v2fly full:/regexp:/attribute syntax. A complete import needs conversion to sing-box
source/binary rules preserving suffix/exact/regex scope; do not broaden Azure/Cloudflare
parents. No adoption, telemetry policy or router change authorized by the comparison.
This broader reference does not alter the confirmed cache-related403 recovery above.

Resolved after user action: user ran `sudo resolvectl flush-caches`; dig chatgpt.com
returned198.18.0.57. After restarting the affected Codex CLI, user supplied a screenshot
of a successful model response. This confirms recovery for the reported no-local-VPN
scenario after the requested retry. No extra domain, wildcard, Codex update, account
change or router edit was needed. Earlier pending cache/Codex statements above retain
the diagnostic history and are superseded by this confirmed outcome.

Original FakeIP-capture issue is corrected and active after the user restart; separate
Codex403/cache correction is now user-verified by an authenticated CLI response.
Keep PC VPN available as desired; no additional domain/routing expansion is needed.
Cutover/media and own DNS follow-up remain in [central TODO](../../../TODO.md).
No diagnostic/background job remains; the original PC/router VPN processes continue running.

## Portable lesson

Clients with a separate full-tunnel VPN must route the router's FakeIP198.18.0.0/15
back to the home router. Compare source-bound and ordinary requests before attributing
an application failure to the router tunnel or DNS; HTTP reachability is not login success.
