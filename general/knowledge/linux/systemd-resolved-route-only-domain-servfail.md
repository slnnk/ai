---
system: linux
status: verified
checked: 2026-08-20
tags: [linux, systemd-resolved, systemd-networkd, netplan, dns, servfail]
---
# systemd-resolved returns SERVFAIL for public names when the only link has a route-only domain

## Symptom

On an Ubuntu host using `systemd-resolved` (`/etc/resolv.conf` -> `127.0.0.53`), names in the local
zone resolve, but ordinary public names fail:

```
$ resolvectl query github.com
github.com: resolve call failed: Could not resolve 'github.com': SERVFAIL   # or "No appropriate name servers"
$ dig @192.168.1.1 github.com +short       # the upstream itself works
140.82.121.4
```

Applications report `Temporary failure in name resolution` / `EAI_AGAIN`; log shippers cannot reach
their endpoint by hostname.

## Cause

A `.network` drop-in (often generated for netplan, e.g.
`/etc/systemd/network/10-netplan-eno1.network.d/local-domain.conf`) sets only a route-only search
domain such as `Domains=~local`. That marks the link's DNS servers as suitable *only* for that domain,
and if no other link is a default DNS route, `resolvectl status` shows the interface with
`DefaultRoute: no` and there is no server left for everything else. The upstream resolver is fine;
the routing inside `systemd-resolved` is broken.

Diagnose:

```bash
resolvectl status            # look for "DNS Domain: ~local" and "Default Route: no" on the link
resolvectl query github.com  # fails
resolvectl query host.local  # works
```

## Fix

Add the catch-all route-only domain `~.` next to the specific one so the same link becomes the
default DNS route while keeping unicast resolution of `.local` (instead of mDNS):

```ini
# /etc/systemd/network/10-netplan-eno1.network.d/local-domain.conf
[Network]
Domains=~local ~.
```

```bash
systemctl restart systemd-networkd systemd-resolved
resolvectl status | grep -A3 'Link .*eno1'     # Default Route: yes
resolvectl query github.com
```

## Limits

- If several links carry DNS, choose deliberately which one gets `~.`; adding it to a VPN link, for
  example, sends all queries through the VPN.
- A hand-made drop-in is invisible to netplan and to configuration management; record it in the
  role/playbook that owns the host, otherwise the next provisioning run silently drops it.
- `~local` is used here to force unicast DNS for a corporate `.local` zone; on hosts that rely on
  mDNS for `.local` do not add it.
