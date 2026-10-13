---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, vkcloud, firewall, vpn]
---
# DevOps-892: approved Jenkins VPN firewall access

## Task

Allow the diagnosed VPN source to reach Jenkins through balancer10.18.20.97 for DevOps-892.

## Context

User explicitly answered «Разреши» to the proposed firewall change limited to source172.28.0.200/32, TCP80/443. This approves the runtime rule, not a separate remote persistence write.

## Actions

Used an idempotent sudo iptables -C INPUT -i ens3 -s172.28.0.200/32 -p tcp -m multiport --dports80,443 -j ACCEPT check, adding the identical rule with -A only if absent. Verified rule presence and counter1packet60bytes. Forced-address workstation HTTPS request with --resolve build.youdo.sg:443:10.18.20.97 to/login returned200 with normal TLS validation.

## Findings

The diagnosed VPN-path runtime firewall block is resolved. The ordinary DNS path still times out after5seconds; public-IP binding/path remain unverified. netfilter-persistent is absent. Enabled restore-iptables.service has ExecStart/ExecReload /usr/sbin/iptables-restore --wait=5 /etc/iptables-rules, so persistence requires a separately approved write to that file. No persistence change or service reload was made.

## Changes

Runtime INPUT accept rule changed on balancer-test01 under the explicit approval. Local KB changes: this log, existing Jenkins map, relevant ~/ai/TODO.md item, index and sync-note. No repository task files changed.

## Risks and limits

The rule is currently runtime-only and can be lost when existing restore automation runs or on reboot. Public DNS end-to-end access and WebSocket forwarding remain unverified; open work is tracked in ~/ai/TODO.md.

## Portable lesson

none

## User-approved removal

The user explicitly requested removal of this balancer change. Removed only the runtime rule with `sudo -n iptables -D INPUT -i ens3 -s 172.28.0.200/32 -p tcp -m multiport --dports 80,443 -j ACCEPT`. A matching `iptables -C` check confirmed absence. The existing allow rule for corporate OpenVPN source45.159.210.228 remains present. A normal DNS/TLS request using `curl --interface tun0 https://build.youdo.sg/login` returnedHTTP200 from138.16.201.238 after removal. No Nginx configuration, persistent firewall file or service reload was changed. The previous persistence proposal is superseded; the removed rule requires no persistence.
