---
system: corporate-network
status: verified
checked: 2026-10-13
tags: [openvpn, routing, read-only]
---
# Corporate OpenVPN: n.velikanets routes on current gateway

## Task

Check the corporate OpenVPN routes for `n.velikanets` on `172.28.0.200`, then add a per-user route for `192.168.30.0/24` as explicitly requested by the user. The user identified `10.16.20.3` as the old server and requested the current gateway explicitly.

## Context

Live SSH target `root@172.28.0.200`, hostname `sc-gateway2.youdo.corp`. The team topology document is indexed in [team-config-repo](../systems/team-config-repo.md). Historical `ipsec-vm` references are not the current endpoint identification.

## Actions

Read-only SSH inspection of the active OpenVPN process, server configuration, user profile directives/certificate identity, CCD directory, connection hook, status files and server push log. No profile private key, user public IP or other unnecessary personal data was retained.

After the user explicitly requested the route addition, one approved SSH mutation created `/etc/openvpn/ccd/n.velikanets` with the exact directive below, using an idempotent append that preserves any existing content. The file had been absent. The same command verified its content and ownership/mode: `root:root`, `0644`. OpenVPN was not restarted.

```text
push "route 192.168.30.0 255.255.255.0"
```

Key inspected paths and commands:

```text
ssh root@172.28.0.200
hostname
ps -eo args
/etc/openvpn/server.conf
/etc/openvpn/client-configs/files/n.velikanets.ovpn
/etc/openvpn/ccd
/var/log/openvpn/openvpn-server.log
```

## Findings

- The active process is `/usr/sbin/openvpn --config /etc/openvpn/server.conf`.
- The user profile exists at `/etc/openvpn/client-configs/files/n.velikanets.ovpn`; its certificate CN is `n.velikanets`, valid from 2023-10-18 through 2033-10-15. The profile enables `pull` and has no explicit `route`, `pull-filter` or `route-nopull` directive.
- Active `client-config-dir` is `/etc/openvpn/ccd`. Before the requested change, no per-user file for `n.velikanets`, matching `velikan` entry or `DEFAULT` CCD file existed. The `client-connect` hook appends the common name and IP to `connect.log`; it provides no route overrides. The created CCD file now pushes the additional `192.168.30.0/24` route for this CN.
- The server's last observed `SENT CONTROL [n.velikanets]` / `PUSH_REPLY` occurred at `2026-10-13 16:54:49` in server log time. Its 53 common route pushes span three continuation frames and match the current server configuration, whose mtime is `2026-10-13 13:59:13 UTC`. The server log timezone was not independently verified.
- The connection was assigned `172.30.63.4/24`, with gateway and DNS `172.30.63.1`, then disconnected at `16:55:06` in server log time. The user was absent from both status files when inspected.
- The pushes include corporate networks `10.18.20.0/24`, `10.18.24.0/24`, `10.18.26.0/24`, `10.16.26.0/24`, `10.16.28.0/24`, `10.255.0.0/24`, `172.26.0.0/24`; host routes include `138.16.201.238/32`, `172.31.2.5/32`, `172.28.0.150/32`. Broad public routes include `52.0.0.0/6` and `34.192.0.0/10`.

## Changes

Created `/etc/openvpn/ccd/n.velikanets` on `172.28.0.200` after the user's explicit authorization. Created this local work log, linked current verification from the existing team-network documentation index, and clarified the historical VPN-host reference in the Nexus system map. No repository task files, service restart or Git mutation occurred.

## Risks and limits

The prior server log proves which common routes were pushed to the user. The additional CCD route takes effect on the next client reconnect; its live push and the user's installed client routing table have not been verified. No service restart is needed for this CCD change.

## Portable lesson

none
