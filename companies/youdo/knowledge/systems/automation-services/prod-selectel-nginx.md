---
system: automation-services
status: verified
checked: 2026-09-23
tags: [nginx, traefik, prod-selectel, balancers, consul]
---
# prod_selectel nginx edge balancers

## Purpose

Public nginx edge for `*.youdo.com` and related domains in the Selectel prod environment,
configured by the `automation-services` Ansible repo (playbook `balancers.yml`, role `nginx`).

## Components

- Repository: `/home/slnnk/git/automation-services`.
- Inventory: `inventories/prod_selectel/group_vars/balancers`; vhosts are the list
  `nginx_vhost` (`name`, `template`, `server_name`, `ssl`, `state`, optional per-vhost vars).
- Templates: `roles/nginx/templates/vhost/<template>.j2`; proxy header lists in
  `roles/nginx/defaults/main.yml` (`nginx_proxy_conf*`, `nginx_vhost_https_*`).
- Certificates: `ssl: wildcard.youdo.com` for `*.youdo.com`.
- DNS: `*.youdo.com` is a wildcard, so a new subdomain needs only a vhost. Unknown names fall
  into the default server and get `301 -> https://youdo.com` with `x-source: nginx`.

## Delivery path

Client -> nginx edge (`server_name`) -> one of:
- `template: traefik.youdo.com` -> `nginx_traefik_addr` = `proxy.service.consul`
  (Consul-registered Traefik, 172.24.0.11-13 as of 2026-09-23) -> Nomad allocation chosen by the
  Traefik router rule, which matches the original `Host`. Used by `data-gateway`,
  `ugc-bot-admin`, `evaluation`, `giveaway-admin`.
- Per-service template with an `upstream` on `<service>.proxy.youdo.local` (also resolves to
  `proxy.service.consul`), e.g. `mcp.youdo.com` (overrides `Host` to the backend name and adds
  `X-Forwarded-Host`/`X-Forwarded-Proto` for the OAuth issuer).

## Control points

- Which Host the Traefik router of the Nomad job matches (public name vs `.proxy.youdo.local`)
  decides the template: see [nginx in front of Traefik](../../../../../general/knowledge/nginx/traefik-host-router-behind-nginx.md).
- `nginx_vhost` order: new items go to the end of the list (user convention).

## Operations

- Adding a Host-routed Nomad service: append an item with `template: traefik.youdo.com`, the
  public `server_name`, `ssl: wildcard.youdo.com`; roll out `balancers.yml` (tag `nginx`),
  check `nginx -t`, then `curl` the name: `301 -> youdo.com` means the vhost is not live.
- Removing an item from `nginx_vhost` does not delete the deployed conf; use `state: absent`.
- `403` "Доступ ограничен" from `giveaway-admin` (also seen on `ugc-bot-admin`, `evaluation`
  on 2026-09-23) is normal service behavior (confirmed by the user), not an nginx failure. Only
  `301 -> youdo.com` indicates a missing vhost.

## Boundaries

- Test environment edge is a separate map: [Yandex test nginx balancers](yandex-test-nginx.md).
- `business.youdo.com` routing details: [nginx business.youdo.com routing](nginx-business-youdo-routing.md).

## Access

Ansible from the `automation-services` repo with the prod_selectel inventory; Vault access for
inventory secrets: [local Ansible access to Vault](local-vault-ansible-access.md).

## History

- 2026-09-23: `giveaway-admin.youdo.com` added (DevOps-864),
  [log](../../log/2026-09-23-automation-services-prod-selectel-nginx-giveaway-admin.md).
- 2026-09: `mcp.youdo.com` added (DevOps-861).
