---
system: macos
status: verified
checked: 2026-07-21
tags: [macos, dns, networksetup, mdnsresponder, dscacheutil, ci-runner]
---
# macOS keeps stale DNS answers after changing resolvers

## Symptom

On a macOS build host you switch the DNS server of a network service (for example to an internal
resolver that overrides public hostnames to internal IPs), `dig` and `dig @<new-resolver>` already
return the new address, but `curl`, `git`, Ruby and `dscacheutil -q host -a name <host>` still connect
to the old public IP for minutes.

Also seen: a host silently "loses" its intended DNS server and falls back to the DHCP-advertised
gateway resolver, which may be unstable (`dig +tries=1 +time=1 @<gateway> <host>` failing 8-27 times
out of 30 while `@1.1.1.1` through the same gateway fails 0/30).

## Cause

`dig` talks to the resolver directly; everything else goes through the system resolver
(`mDNSResponder`), which caches records independently and does not drop its cache when the
resolver list changes. The DNS server list itself is per network service and can be overwritten by
DHCP, profiles or MDM scripts.

## Fix

Set the resolver persistently on the network service and flush the system cache:

```bash
sudo networksetup -setdnsservers Ethernet 10.0.0.53      # your resolver(s), space separated
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Verify with the system resolver, not only `dig`:

```bash
networksetup -getdnsservers Ethernet
scutil --dns | head -20                       # resolver #1 and the scoped en0 resolver
dscacheutil -q host -a name example.internal
curl -Iv --connect-timeout 8 https://example.internal/   # check the "Trying <ip>" line
```

To see what DHCP is pushing (and whether it explains an unexpected resolver):
`ipconfig getpacket en0`.

## Limits

- `networksetup -setdnsservers` survives reboots but not a profile/MDM/DHCP script that rewrites
  the service; if the value keeps reverting, look there.
- Use `ping`/`nc` on TCP/443 to separate DNS problems from connectivity problems: in the observed
  case TCP to external hosts was stable while UDP and TCP DNS to the gateway were failing.
- Test a suspect resolver with repeated `dig +tries=1 +time=1 @<ip> <name> A +short` loops; a single
  successful lookup proves nothing about an intermittent forwarder.
