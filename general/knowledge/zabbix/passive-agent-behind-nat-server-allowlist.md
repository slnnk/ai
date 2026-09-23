---
system: zabbix
status: verified
checked: 2026-08-13
tags: [zabbix, zabbix-agent2, nat, passive-checks, connection-reset]
---
# Zabbix passive agent behind NAT: "Connection reset by peer", host unavailable

## Symptom

A new host in Zabbix stays red: interface `available=2`, error
`Get value from agent failed: ... Connection reset by peer` (or `connection refused`), no item
values. On the host `zabbix-agent2` is active and listens on TCP 10050, and `telnet <host> 10050`
from the server connects. The agent log shows:

```
failed to accept an incoming connection: connection from "10.20.0.1" rejected, allowed hosts: "198.51.100.10,198.51.100.11"
```

## Cause

Passive checks are validated against the `Server=` allowlist in the agent config. When the Zabbix
server reaches the site through NAT (site-to-site VPN, office gateway), the agent sees the gateway's
inside address as the peer, not the server's real IP, so the connection is dropped after accept.

## Fix

Add the address the agent actually sees to `Server=` (comma-separated), keep the real server IPs for
sites without NAT, and leave `ServerActive=` pointing at the real server (active checks are outbound
and unaffected by NAT):

```ini
Server=198.51.100.10,198.51.100.11,10.20.0.1
ServerActive=198.51.100.11
```

In Ansible put the extra address into the group_vars of the NAT-ed site group rather than into a
global default, then apply narrowly (`--limit <host> --tags zabbix-agent2`) and re-check the interface
in the frontend (`available=1`, error cleared, first OS values arriving).

## Limits

- `Server=` accepts a network in CIDR notation; allowlisting the NAT gateway trusts every host that
  can source traffic through it, so keep it scoped to the site group that needs it.
- If active checks also time out (`ServerActive` host unreachable on 10051) that is a separate
  routing problem; passive monitoring works without it.
- Agent-side templates for services on the host (e.g. a Selenium Grid on 4444) still need to be added
  separately; agent reachability alone monitors only the OS.
