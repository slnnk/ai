---
system: automation-services
status: verified
checked: 2026-09-23
tags: [nginx, traefik, prod-selectel, balancers, giveaway-bot, DevOps-864]
---
# prod_selectel nginx: giveaway-admin.youdo.com vhost (DevOps-864)

## Task

YouTrack DevOps-864, item 2: publish `server_name giveaway-admin.youdo.com` on the prod
nginx edge for the new .NET service `youdo-giveaway-bot` (repo
`youdo/marketing/youdo-giveaway-bot`, Nomad job `youdo-giveaway-bot`). The ticket asked for
"the same as DevOps-861 (mcp.youdo.com) but without the extra header requirements".
Items 1 (PostgreSQL `giveaway_bot` on the C2C cluster) and 3 (Vault `secret/dotnet/giveaway-bot`
under policy `dotnet`) were done by the user outside this session.

## Context

- Repository `/home/slnnk/git/automation-services`, inventory
  `inventories/prod_selectel/group_vars/balancers`, list `nginx_vhost`.
- System map: [prod_selectel nginx edge](../systems/automation-services/prod-selectel-nginx.md).
- DNS: `*.youdo.com` wildcard, no record needed. TLS: `wildcard.youdo.com`.
- Nomad job `devops/production.hcl`: group `web`, task `youdo-giveaway-bot-admin` (Blazor
  Server admin, `count = 1`), Traefik tags
  `traefik.http.routers.${NOMAD_TASK_NAME}.rule=Host(\`giveaway-admin.youdo.com\`)` and a
  sticky cookie `giveawayadmin_affinity`. The bot task `youdo-giveaway-bot-bot` only has the
  internal `.proxy.youdo.local` router for `/_/heartbeat`.

## Actions

1. Read both tickets through the YouTrack API (`YOUTRACK_TOKEN` in `current/.env`) and the Nomad
   job through the GitLab API (`GITLAB_YOUDO_TOKEN`).
2. First draft: dedicated template `giveaway-admin.youdo.com.j2` modeled on `mcp.youdo.com.j2`.
   It differed from mcp by keeping `Host $host` (the admin router matches only the public name)
   and using `nginx_proxy_conf_without_buff` for WebSocket/SignalR.
3. On the user's request switched to the shared template `traefik.youdo.com`, as used by
   `evaluation.youdo.com`, `data-gateway.youdo.com`, `ugc-bot-admin.youdo.com`. The custom template
   and its defaults variable were removed. Final entry, appended last in `nginx_vhost`:

   ```yaml
    - name: giveaway-admin.youdo.com
      template: traefik.youdo.com
      server_name: 'giveaway-admin.youdo.com'
      ssl: wildcard.youdo.com
      state: present
   ```
4. The user applied nginx on the balancers.

## Findings

- `traefik.youdo.com` fits Host-routed Nomad services: it proxies to `nginx_traefik_addr`
  (`proxy.service.consul`, 172.24.0.11-13), passes `Host $host`, `Upgrade`/`Connection`
  (WebSocket), `X-Forwarded-*`, `proxy_read_timeout 600s`. No maintenance/error page of its own.
- The mcp template overrides `Host` with the backend name (`youdo-mcp-web.proxy.youdo.local`);
  that only works for jobs that have a `.proxy.youdo.local` Host router on the public task.
  Portable rule: [nginx in front of Traefik](../../../../general/knowledge/nginx/traefik-host-router-behind-nginx.md).
- Before rollout the name answered `301 -> https://youdo.com` (default server). After rollout
  (2026-09-23, from the workstation) `https://giveaway-admin.youdo.com/` returns nginx `403`
  "Доступ ограничен", exactly like `ugc-bot-admin.youdo.com` and `evaluation.youdo.com`. The user
  confirmed this `403` is the normal behavior of the service for such a request, not an edge
  problem; the service works.

## Changes

- `inventories/prod_selectel/group_vars/balancers`: new `nginx_vhost` item
  `giveaway-admin.youdo.com` (template `traefik.youdo.com`).
- Same session, user's own work: `mcp.youdo.com` vhost kept as the last item before it
  (earlier accidental removal of the other vhosts in this file and in
  `inventories/yandex/group_vars/balancers_test` was reverted from `HEAD`).

## Open items

- None for DevOps-864. Note for future checks: a `403` "Доступ ограничен" from this host is
  expected; a `301 -> https://youdo.com` would mean the vhost is missing.

## Portable lesson

[nginx in front of Traefik: Host header must match the router rule](../../../../general/knowledge/nginx/traefik-host-router-behind-nginx.md)
