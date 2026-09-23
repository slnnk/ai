---
system: nginx
status: verified
checked: 2026-09-11
tags: [nginx, proxy_pass, dns, resolver, consul, stale-upstream, 499]
---
# nginx: a literal `proxy_pass` hostname is resolved once, so a removed backend stays in the pool

## Symptom

A vhost proxies to a DNS name that returns several A records (Consul DNS, service
discovery, round-robin DNS). One backend is powered off or removed from DNS. Afterwards:

- requests through nginx alternate between fast (HTTP 200 in milliseconds) and hanging for
  tens of seconds until the client gives up; the access log shows status `499`,
  `upstream_connect_time` (`uct`) `-` and the dead backend's address in `$upstream_addr`;
- `dig` against the same name no longer returns the dead address, and the TTL is short
  (even 1 s);
- every backend that DNS *does* return answers immediately when queried directly;
- a global `resolver <ip> valid=30s;` is configured and looks like it should refresh.

Because the same upstream name is usually shared by many vhosts, the "one slow site"
report is actually a fleet-wide problem; grep all access logs for the dead address.

## Cause

`proxy_pass http://some.hostname;` with a *literal* hostname is resolved by nginx once, at
configuration load (start or reload), and the resulting address list is baked into the
worker processes. The `resolver ... valid=` directive only applies to names nginx resolves
at request time (variables in `proxy_pass`, `server ... resolve` in an upstream). A worker
therefore keeps round-robining over the address set it saw at its last reload, including
members that have since disappeared from DNS, and each request landing on the dead member
waits through the full TCP connect timeout (default `proxy_connect_timeout 60s`).

Confirm with `journalctl -u nginx` (time of the last reload) versus the time the backend
was removed, and `nginx -T` for the literal `proxy_pass`.

## Fix

Immediate recovery (safe, no config change):

```bash
nginx -t && systemctl reload nginx        # new workers resolve the current members
# verify: only live addresses in $upstream_addr, no new entries for the dead one
tail -f /var/log/nginx/*access.log | grep -F '<dead-ip>:'
```

Permanent options, in order of preference:

1. Make nginx re-resolve. On open-source nginx >= 1.27.3 use a shared-memory upstream with
   a resolving server:

   ```nginx
   resolver 127.0.0.1:8600 valid=10s ipv6=off;
   upstream backend_pool {
       zone backend_pool 64k;
       server some.hostname:80 resolve;
   }
   server { location / { proxy_pass http://backend_pool; } }
   ```

   On older versions use a variable so resolution happens per request
   (`set $backend "some.hostname"; proxy_pass http://$backend;`). Note that a variable in
   `proxy_pass` changes URI handling (no automatic URI rewriting) and disables keepalive
   pooling to the upstream; test paths and `Host` handling before rollout.
2. Let the discovery system drive reloads: consul-template (or equivalent) watches the
   service and runs `nginx -t && nginx -s reload` on membership change.
3. Add a bounded `proxy_connect_timeout 3s;` plus `proxy_next_upstream error timeout;` as a
   guardrail so a stale member costs seconds, not a minute. This masks the symptom; it is
   not the fix.

Operationally: before powering off a backend, drain it from service discovery, wait for the
DNS change, and reload edge proxies that use literal `proxy_pass` names.

## Limits

- Checked with nginx 1.30.x. The `resolve` parameter on `server` in open-source nginx
  requires 1.27.3 or later (earlier it was nginx Plus only).
- The per-request variable form re-resolves on every request; with a very short TTL and
  high traffic this puts load on the resolver and loses upstream keepalive.
- A graceful reload leaves old workers in `shutting down` state while long-lived
  connections finish; they accept no new connections, so this is harmless.
