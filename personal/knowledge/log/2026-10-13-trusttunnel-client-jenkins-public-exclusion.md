---
system: trusttunnel-client
status: verified
checked: 2026-10-13
tags: [trusttunnel, openvpn, routing]
---
# Jenkins public address excluded from TrustTunnel, restart pending

## Task

Prepare a local routing correction for Jenkins public access with personal TrustTunnel and corporate OpenVPN both active.

## Context

Public Jenkins138.16.201.238 works through corporate OpenVPN, but ordinary requests use TrustTunnel table880 and time out. Main-table route already points to corporate172.30.63.1/tun0.

## Actions

Added exactly138.16.201.238/32 after92.53.80.150/32 in [listener.tun].excluded_routes of /home/slnnk/trusttunnel/trusttunnel_client.toml. Python3.12 tomllib parsing and unique-route assertion passed. Credentials were not printed. No client restart occurred.

## Findings

Policy30801 lookup880 precedes main, sending ordinary requests through TrustTunnel tun1/source172.16.219.2. curl --interface tun0 to public Jenkins with normal DNS/TLS returnedHTTP200; company capture confirms corporate public source45.159.210.228 is already allowlisted. Config exclusion is prepared but inactive pending restart, so ordinary curl still times out.

## Changes

Local TrustTunnel configuration and personal/company KB bookkeeping. No server changes.

## Risks and limits

Client restart was not authorized or executed. Restart then route and browser verification are still needed. Do not launch a second concurrent client. The config contains credentials and must not be printed or copied into notes. Open work is tracked in ~/ai/TODO.md.

## Portable lesson

none
