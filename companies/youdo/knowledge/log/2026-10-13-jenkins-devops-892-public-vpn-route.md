---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, vkcloud, vpn, routing]
---
# DevOps-892: public Jenkins route and local TrustTunnel exclusion

## Task

Determine why the browser cannot reach public Jenkins after the VPN private-route firewall correction.

## Context

Public build.youdo.sg resolves138.16.201.238. The workstation has corporate OpenVPN tun0 and personal TrustTunnel tun1. Runtime firewall persistence remains unapproved.

## Actions

Read-only curl --interface tun0 https://build.youdo.sg/login used normal DNS/TLS and returnedHTTP200 from138.16.201.238. Simultaneous balancer ens3 capture confirmed SYN source45.159.210.228 to10.18.20.97:443. Ordinary curl timed out after5seconds through TrustTunnel. Exactly138.16.201.238/32 was added to local TrustTunnel excluded_routes, after92.53.80.150/32; Python3.12 tomllib parsing and unique-route assertion passed without printing credentials. No client restart or remote mutation occurred.

## Findings

The public IP routes to the correct balancer and Jenkins HTTPS works through corporate OpenVPN. Its external source45.159.210.228 is already allowlisted, so no additional firewall rule is needed for that path. Workstation main-table route to138.16.201.238 uses172.30.63.1/tun0, but priority30801 lookup880 precedes main and ordinary requests use TrustTunnel tun1/source172.16.219.2. The local exclusion is pending client restart and has not changed active routing; browser access remains blocked.

## Changes

Local TrustTunnel route exclusion only; its configuration contains credentials and was not printed. Updated company and personal KB logs/maps, Jenkins TODO, service-addresses verification comments, indexes and sync-notes. No remote firewall persistence or client restart was authorized or executed.

## Risks and limits

The new exclusion requires client restart and route/browser verification. Do not start a second concurrent client. Runtime firewall persistence and WebSocket verification retain separate pending status; open work is in ~/ai/TODO.md.

## Portable lesson

none

## User browser verification

The user subsequently supplied a screenshot showing the authenticated Jenkins UI at https://build.youdo.sg, confirming browser access and superseding the earlier browser-blocked observation. The recovery quiet-mode banner remains visible. The screenshot does not prove the active TrustTunnel route or restart status; no runtime changes or builds were authorized by it.
