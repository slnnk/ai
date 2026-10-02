---
system: android-farm
status: verified
checked: 2026-10-01
tags: [mikrotik, dns, loki, alloy, kazan]
---
# Kazan Gate_K forwards youdo.* DNS to decommissioned srv0

## Task

Find why farm hosts `M-K0057` (`192.168.30.31`) and `M-K0058` (`192.168.30.32`) cannot
resolve `loki.dev.youdo.corp` through the office resolver `192.168.30.1` (Alloy push to Loki
fails since 2026-09-14).

## Context

`192.168.30.1` is the Kazan office MikroTik `Gate_K` (CCR1009-7G-1C-1S+, RouterOS 6.49.20,
LAN `192.168.30.0/24`, interface `Razrab`). SSH access variables: `KAZAN_MIKROTIK_*` in
`~/ai/current/.env` (added 2026-10-01). Team docs: `claude-code-config-infra`
`docs/infra/office.md`, `docs/operations/mikrotik-tunnels.md`.

## Actions

Read-only only: `/ip dns print`, `/ip dns static print`, `/ip firewall filter|mangle|nat print`,
`/ip ipsec active-peers print`, `/log print where topics~"ipsec"`, `:resolve ... server=...`,
`/export terse hide-sensitive`; on farm hosts `dig @192.168.30.1`, `getent hosts`,
`journalctl -u alloy`.

## Findings

- The router itself resolves `loki.dev.youdo.corp` -> `10.16.26.101` via its upstream
  `/ip dns servers=10.16.20.3,91.225.76.3` (`10.16.20.3` works, `91.225.76.3` does not answer
  this name).
- LAN clients do not get an answer: `dig @192.168.30.1 loki.dev.youdo.corp` from both farm
  hosts times out, while `ya.ru` resolves. Alloy: 43 / 35 `context deadline exceeded` in 30 min.
- Cause: mangle `prerouting` rules mark DNS connections to `192.168.30.1:53` (udp/tcp) by
  layer7 regex (`youdo.corp`, `youdo.test`, `youdo.local`, `consul`), and `dstnat` rules
  "DNS Forwarding for ..." DNAT them to `192.168.60.10` (Moscow srv0). srv0 is decommissioned
  (user, 2026-10-01); `192.168.60.10` does not answer ping or DNS. The policy IPsec `peer1` to
  Moscow `Gate` `185.11.49.180` (`192.168.30.0/24 <-> 192.168.60.0/24`) is also down: phase 1
  `negotiation failed due to time up` every minute (log buffer starts 2026-09-30 20:52), no ping.
- Other srv0 leftovers on Gate_K: `/ip dns static` `youdo.corp` and `youdo.test` ->
  `192.168.60.10`; srcnat accept to `192.168.60.0/24`; `ip service ftp/ssh address` includes
  `192.168.60.0/27`.
- Via `10.16.20.3`: `consul.service.consul` -> `172.28.0.101`,
  `grafana.yandex-test.youdo.local` -> `10.16.26.101`; `gitlab.youdo.test` did not resolve
  (whether `youdo.test` is still used is not checked).

## Changes

Applied on `Gate_K` 2026-10-01 ~21:50 MSK with the user's approval:

    /ip firewall nat disable [find chain=dstnat comment~"DNS Forwarding for"]   # 4 rules
    /ip firewall mangle disable [find comment~"DNS Forwarding for" dst-address=192.168.30.1]  # matched 0, mangle left enabled (harmless without DNAT)
    /ip dns static disable [find address=192.168.60.10]   # youdo.test, youdo.corp
    /ip dns cache flush

Rollback: the same commands with `enable`. Local: `KAZAN_MIKROTIK_*` in `.env`.

Verified after the change: from `M-K0057`/`M-K0058` `dig @192.168.30.1` returns
`loki.dev.youdo.corp` -> `10.16.26.101`, `grafana.yandex-test.youdo.local` -> CNAME
`grafana.dev.youdo.corp` `10.16.26.101`, `consul.service.consul` -> `172.28.0.101-103`;
`getent` OK; push endpoint answers GET with 405. Last Alloy `context deadline exceeded`
21:49 / 21:49 on the two hosts, none after; Loki has fresh streams `instance=M-K0057` and
`M-K0058` (5-minute line counts 157 / 275). Logs from 2026-09-14 to 2026-10-01 were not
backfilled (not checked).

## Open items

- Clean srv0 leftovers on Gate_K: disabled dstnat/static entries, mangle layer7 marks and
  srcnat masquerade "DNS Forwarding for ...", policy IPsec `peer1` to `185.11.49.180`, srcnat
  accept to `192.168.60.0/24`, `192.168.60.0/27` in `ip service ssh/ftp address`.
- `youdo.test` does not resolve via `10.16.20.3`; check whether anyone in Kazan still uses it.
- Update team docs `docs/infra/office.md` (srv0 as internal DNS) when contributing there.

## Portable lesson

none
