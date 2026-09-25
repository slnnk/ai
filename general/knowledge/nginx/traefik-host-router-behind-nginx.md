---
system: nginx
status: verified
checked: 2026-09-23
tags: [nginx, traefik, host-header, websocket]
---
# nginx in front of Traefik: Host header must match the router rule

## Symptom

A service behind an nginx edge and Traefik returns Traefik's `404 page not found` (or nginx's
error/maintenance page when `proxy_intercept_errors on`), although the backend is healthy and a
direct request to the allocation works. Or the reverse: a request by the internal name works, but
the public name gets 404.

## Cause

Traefik selects a router by the `Host` header of the incoming request. nginx either:
- overrides it (`proxy_set_header Host <internal-backend-name>`), while the router matches only the
  public name (`Host(\`app.example.com\`)`); or
- passes `Host $host` (the public name), while the router matches only the internal name
  (`Host(\`app.proxy.internal\`)`).

The name in `proxy_pass`/`upstream` only selects which Traefik instance to connect to; it does not
affect routing unless it is also sent as `Host`.

## Fix

1. Read the router rule in the service's orchestrator job (Nomad/Consul tags, k8s IngressRoute).
2. Router matches the public name: `proxy_pass` to Traefik and `proxy_set_header Host $host`.
3. Router matches only an internal name: set `Host` to that name and, if the app builds absolute
   URLs (OAuth issuer, redirects), add `X-Forwarded-Host $host` and `X-Forwarded-Proto https`,
   and make the app trust the edge network for forwarded headers.
4. For SignalR/Blazor Server or other WebSocket apps also pass
   `proxy_http_version 1.1`, `Upgrade $http_upgrade`, `Connection $connection_upgrade`, and use
   a long `proxy_read_timeout`.
5. Verify: `curl -H 'Host: <name nginx sends>' http://<traefik>/<health>` must return 200.

## Limits

- Traefik may have several routers for one service (e.g. `Host(public) || Host(internal)`);
  then either header works.
- Sticky sessions set by Traefik (cookie) pass through nginx unchanged; no nginx config needed.
