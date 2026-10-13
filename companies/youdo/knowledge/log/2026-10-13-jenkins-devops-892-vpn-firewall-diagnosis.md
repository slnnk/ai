---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, vkcloud, nginx, vpn, firewall]
---
# DevOps-892: replacement balancer VPN firewall diagnosis

## Task

Diagnose Jenkins access through replacement balancer10.18.20.97 for [DevOps-892](https://youtrack.youdo.com/youtrack/issue/DevOps-892), using read-only network and firewall checks.

## Context

The balancer's existing HTTPS route to controller10.18.26.8 responds locally, but requests from the workstation time out. Jenkins recovery quiet mode remains enabled.

## Actions

Checked workstation getent and dig using the default resolver and172.28.0.9; inspected route to10.18.20.97. HTTPS requests to the DNS address and to forced10.18.20.97 both timed out after5seconds. On balancer-test01 inspected Nginx listening sockets, local HTTPS response, iptables and nft rules. No remote configuration, firewall rules or services were changed.

## Findings

Workstation DNS queries return A138.16.201.238 and no AAAA. This differs from historical Yandex178.154.207.53; the current address is not established as belonging to the old service. Public-IP/floating-IP assignment to the replacement balancer has not been verified.

The workstation route to10.18.20.97 uses172.30.63.1 via tun0, source172.30.63.11. Nginx listens on0.0.0.0:80 and:443. Local curl with normal TLS validation and --resolve build.youdo.sg:443:127.0.0.1 returns/login HTTP200.

Confirmed firewall configuration: iptables INPUT policy is DROP. Its source allowlist includes172.30.62.0/24, historical10.16.{20,24,26,28}.0/24 networks and specific public addresses, but omits172.30.63.0/24 and has no universal80/443 acceptance. nft inet filter has an empty accept-policy chain; nft ip filter contains the iptables rules.

Packet capture on ens3 during the forced HTTPS request confirmed an arriving TCP SYN from172.28.0.200:37610 to10.18.20.97:443 while the request timed out. The VPN path translates workstation source172.30.63.11 to172.28.0.200. Neither172.28.0.200 nor its172.28.0.0 subnet is allowed by the inspected INPUT rules. This confirms the firewall block for the observed VPN request; adding only172.30.63.0/24 would not match the observed source. No firewall correction was authorized or applied. Public-IP binding and public-path reachability require separate evidence.

## Changes

Added this log; updated the existing Jenkins map, public-routing work item in ~/ai/TODO.md and observed DNS address in current/service-addresses.env. Rebuilt the knowledge index and recorded a sync-note. No repository task files or remote state changed.

## Risks and limits

The existing local HTTPS response establishes that Nginx and its Jenkins route work locally. It does not establish public reachability or WebSocket forwarding. Packet capture and firewall rules confirm the observed VPN request is blocked with translated source172.28.0.200. All open work remains in ~/ai/TODO.md.

## Portable lesson

none
