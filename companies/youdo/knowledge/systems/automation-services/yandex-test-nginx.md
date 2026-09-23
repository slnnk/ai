---
system: automation-services
status: verified
checked: 2026-09-18
tags: [nginx, balancer-test, yandex-test, dev-routing, consul-dns, nomad-test, mcp]
---
# Yandex test nginx balancers

Living map of the public nginx balancers of the Yandex test environment
(`balancer-test01` / `balancer_test02`), configured from the `automation-services`
Ansible repository. Last checked: 2026-09-18.

## Components

- Repository: `/home/slnnk/git/automation-services` (`git@gitlab.youdo.sg:sysadmins/automation-services.git`).
- Inventory variables: `inventories/yandex/group_vars/balancers_test`.
- Public balancer `10.16.20.35` identifies as `balancer-test01` (`balancer-test01.ru-central1.internal`), nginx `1.30.1`; a second node is `balancer_test02`.
- Consul-backed upstreams: vhosts proxy to `<service>.<platform>.yandex-test.youdo.local`, a CNAME to `proxy.service.yandex-test.consul` (the Nomad proxy clients / Traefik).

## Dynamic `*.dev.youdo.sg` routing

- Dynamic B2B task/branch vhosts route to `traefik.dev.youdo.corp`.
- The eight dynamic regex vhosts are: `b2bautomation`, `business-auth-int`, `business`, `employee`, `smzbot`, `s`, `business-auth-ext`, and `business-mock-api`.
- Branch `DevOps-828-nginx`, commit `f18471ca` (`fix b2b dev regexp`), replaces the former numeric-only expression with a deliberately permissive and readable pair: an exact base hostname plus `~^<service>-.*\.dev\.youdo\.sg$`. It accepts numeric branch slugs, task IDs, and arbitrary branch-derived suffixes; Traefik is responsible for returning 404 when no matching ingress exists. Nginx wildcard syntax such as `s-*.dev.youdo.sg` cannot be used because `*` is only valid as a complete leading/trailing DNS-name part, not in the middle of a label.
- The general business regex also handles `business-api-*`, but uses a negative lookahead to exclude `business-auth-int`, `business-auth-ext`, and `business-mock-api` plus their suffixed variants. These hosts therefore match only their specific vhost and no longer rely on nginx include/regex evaluation order.
- The current worktree already contains extensive user changes removing the legacy `nginx_platforms` vhost loop and unrelated static vhosts. The regex edit was limited to the eight dynamic entries and their comment; do not restore or rewrite the surrounding user changes.
- `roles/nginx/files/ssl/wildcard.youdo.sg.crt` was checked on 2026-08-20 and its SAN includes `*.dev.youdo.sg` (certificate validity observed: 2026-07-10 through 2026-10-08).

## Operations: verification after inventory changes

After changing inventory, render/apply only through the normal test-balancer Ansible workflow, then run `nginx -t` and verify both the base host and a suffixed host for every required service. Note that removing an item from `nginx_vhost` does not delete an already deployed `/etc/nginx/conf.d/<name>.conf`; the role's delete task only acts on entries explicitly declared with `state: absent`. Check/remove stale legacy `*.dev.youdo.sg` config files during rollout.

Local verification on 2026-09-01:

- outer YAML and `nginx_vhost_str | from_yaml` rendered successfully through Ansible;
- `balancers.yml --syntax-check` passed (with expected warnings for inventory groups absent from the selected test inventory);
- general routing examples cover current task hosts, numeric branch slugs, arbitrary suffixes, and `business-api`; a dedicated seven-case business test confirmed that base/main/API hosts and all excluded auth/mock forms each match exactly one intended vhost;
- `git diff --check` passed for the inventory file.

Runtime verification on 2026-09-01:

- public balancer `10.16.20.35` identifies as `balancer-test01`, nginx `1.30.1`;
- nginx was reloaded at `2026-09-01 00:50:56 MSK` and its live `nginx -T` contains the new business regexp with the auth/mock exclusions;
- `GET https://business-devops-689.dev.youdo.sg/` at `00:56:39` returned `200` and was logged in `business.dev.youdo.sg-access.log` with upstream `10.16.26.101:80`;
- a correlated `GET /health` at `01:01:23` also returned `200` from upstream `10.16.26.101:80`;
- no `301` for this hostname was found in the current or rotated `access.log`, `youdo.sg-access.log`, or `business.dev.youdo.sg-access.log` files. If a browser still redirects after this reload, the likely source is its cached permanent redirect; verify in a private window or with `curl` before changing nginx again.
- `automation-services/master` merge commit `ccd39521` contains regexp commit `f18471ca`.
- A public smoke check on 2026-09-01 covered all seven generated hosts without DNS overrides. TLS verification passed and public root responses exactly matched direct Traefik: auth ext/int `404`, automation `401`, business API `404`, business web `200`, employee web `500`, and kitcut `s` `404`. These non-200 root codes are application behavior, not nginx fallback. Readiness returned `200` on `/health` for automation/business-api/business/employee/kitcut and on `/_/heartbeat` for auth ext/int.

## Known failure mode: stale Nomad proxy address (2026-09-11 incident)

Detailed log entry: [2026-09-11 stale powered-off Nomad proxy](../../log/2026-09-11-automation-services-yandex-test-nginx-stale-nomad-proxy.md).

- Symptom: `https://business-mock-api.test14.youdo.sg/sms` loaded intermittently for tens of seconds, while the allocation endpoint `http://10.16.26.7:24219/sms` was consistently fast.
- Confirmed path: public HTTPS -> nginx on `balancer-test01` (`10.16.20.35`) -> `youdo-business-mock-api.test14.yandex-test.youdo.local` -> CNAME `proxy.service.yandex-test.consul` -> Nomad proxy clients -> allocation `10.16.26.7:24219`.
- Direct allocation checks from the balancer took about 7-8 ms. Current Consul/DNS proxy clients `10.16.26.33`, `.44`, and `.55` each returned HTTP 200 in about 9-10 ms.
- Nginx had last reloaded on 2026-09-09 at 19:13 MSK and had cached two addresses for the statically named `proxy_pass`: `10.16.26.50` and `.55`. The operator confirmed that `.50` was a recently powered-off Nomad client. Current DNS has a 1-second A-record TTL and no longer contains `.50`, but the global nginx `resolver ... valid=30s` does not make a literal `proxy_pass http://hostname` re-resolve during worker lifetime.
- Controlled requests through local nginx alternated exactly: `.55:80` returned HTTP 200 immediately, while `.50:80` remained in TCP connect until the client timeout and was logged as 499 with `uct="-"`. A direct request to `.50:80` timed out at connect; direct requests to `.33/.44/.55` succeeded.
- Real browser requests on 2026-09-11 show the same failure, including 499 request times of 11.8, 38.5, and 54.1 seconds with upstream `.50:80`. Stale `.50` also occurs in access logs for many other test/autotest `youdo.sg` vhosts, explaining the reported wider impact.
- Source configuration: `/home/slnnk/git/automation-services/inventories/yandex/group_vars/balancers_test` and `roles/nginx/templates/vhost/business-mock-api.youdo.com.j2`. The template renders a literal `proxy_pass http://youdo-business-mock-api.<platform>.yandex-test.youdo.local`.
- Immediate recovery (not performed during diagnosis): validate with `nginx -t`, then reload nginx so the new workers resolve only the current Consul proxy members. Verify logs contain `.33/.44/.55` and no new `.50` entries.
- Permanent prevention: make the shared Consul-backed upstream dynamically re-resolvable by nginx (for nginx 1.30, use a shared-memory upstream zone plus a resolving server, or an equivalent carefully tested variable-based proxy pattern), or have Consul-template trigger a validated nginx reload whenever the proxy service membership changes. Apply this centrally to all vhosts routed through `proxy.service.yandex-test.consul`, not only mock-api. Add a short `proxy_connect_timeout` as a guardrail, not as the root fix.
- No service/config changes or nginx reload were made during this investigation.
- Operator recovery and verification at 2026-09-11 17:25-17:27 MSK: nginx was gracefully reloaded and new workers started at `17:25:15`. Consul DNS advertised only `.33/.44/.55`. A controlled 30-request HTTP/2 series through local HTTPS returned 30/30 HTTP 200 in 13-33 ms and used `.33` 11 times, `.44` 9 times, and `.55` 10 times; `.50` was used zero times. A scan of all active per-vhost access logs after the reload found zero new upstream `.50:80` records. The old workers were still in `shutting down` state because of existing long-lived connections, but accepted no new connections and had no active socket to `.50`. Current service is recovered; the static-DNS recurrence risk remains until the permanent prevention above is implemented.

## MCP test vhost HTTP 404 diagnosis (2026-09-18)

- Public `GET https://mcp.test1.youdo.sg/_/healthcheck` completed DNS, TCP, and
  TLS successfully but returned nginx's 712-byte maintenance page with HTTP
  404.
- `balancer_test01` had a loaded
  `/etc/nginx/conf.d/mcp.test1.youdo.sg.conf`. Its upstream resolved through
  `proxy.service.yandex-test.consul`; a direct backend health request returned
  HTTP 200.
- The same backend request with `Host: mcp.test1.youdo.sg` returned HTTP 404.
  The live MCP vhost inherited `proxy_set_header Host $host` from
  `nginx_proxy_conf`, and `proxy_intercept_errors` converted that upstream 404
  to the maintenance page. Access logs correlated the public request with
  upstream proxy members, proving the request reached this vhost rather than a
  default server.
- The `youdo-mcp` Nomad Traefik rule accepts its internal service host
  `youdo-mcp-web.<platform>.yandex-test.youdo.local` (and `mcp.youdo.com` for
  production), not public test host `mcp.<platform>.youdo.sg`. The nginx vhost
  therefore needs to send the internal backend hostname in `Host` while keeping
  the original public hostname in `X-Forwarded-Host`.
- Safe source direction: build the MCP proxy options from
  `nginx_proxy_conf_without_host`, then explicitly set `Host` to
  `nginx_mcp_youdo_com_backend` and `X-Forwarded-Host` to `$host` in the MCP
  template. Validate the rendered config and backend/public health response.
- The worktree at diagnosis contained an unsafe inventory diff: adding MCP had
  also removed roughly 361 lines of existing `nginx_vhost_str` entries. Do not
  deploy that diff. Restore the existing list and make the MCP addition
  additive before a normal (non-`-C`) rollout.
- Source correction completed locally on 2026-09-18: the full existing vhost
  list was restored, the MCP entry is now a six-line additive block inside the
  platform loop, the MCP proxy options use `nginx_proxy_conf_without_host`, and
  the template explicitly sends the internal backend `Host` while preserving
  `$host` as `X-Forwarded-Host` and `$scheme` as `X-Forwarded-Proto`.
- Verification: targeted `git diff --check` and playbook syntax-check passed;
  inventory evaluation produced 21 MCP hosts (`test`, `test1`-`test17`, and
  `autotest01`-`autotest03`). A focused two-host Ansible check/diff rendered the
  expected Host-header replacement on `balancer_test01` and a new MCP config on
  `balancer_test02`.
- Rollout was not performed. The focused check exposed unrelated live drift in
  `balancer_test02` default.conf: applying tag `nginx-vhost-only` would change
  its redirect from `public-test.youdo.sg` to `youdo.sg`. Resolve/approve that
  default-vhost delta or narrow the rollout mechanism before applying to both
  nodes.

## Boundaries

- Belongs here: the nginx role, `balancers_test` inventory, vhost templates and the two test balancer nodes.
- Nearby but separate: the Nomad proxy clients / Traefik behind `proxy.service.yandex-test.consul` (system `nomad-test`), `traefik.dev.youdo.corp` for the dev Kubernetes stand (system `dev-deployment`).

## Related log entries

- [2026-09-11 stale powered-off Nomad proxy address](../../log/2026-09-11-automation-services-yandex-test-nginx-stale-nomad-proxy.md)
- [2026-09-11 Nomad client group stop pilot (nginx upstream re-check requirement)](../../log/2026-09-11-nomad-test-agent-group-stop-pilot.md)
