---
system: automation-services
status: verified
checked: 2026-09-11
tags: [incident, nginx, balancer-test01, proxy_pass, consul-dns, stale-upstream, nomad-test]
---
# Yandex test nginx: stale powered-off Nomad proxy

Date: 2026-09-11 (MSK)

## Task

Diagnose why `business-mock-api.test14.youdo.sg/sms` loaded intermittently for tens of
seconds while the application allocation itself answered quickly.

## Context

- Reported host: `business-mock-api.test14.youdo.sg`, path `/sms`.
- Load balancer: `balancer-test01.ru-central1.internal`, `10.16.20.35`, nginx 1.30.1.
- Allocation endpoint supplied by the operator: `10.16.26.7:24219`.
- Related source repository: `/home/slnnk/git/automation-services`, safe origin `git@gitlab.youdo.sg:sysadmins/automation-services.git`.
- System map: [Yandex test nginx balancers](../systems/automation-services/yandex-test-nginx.md).

## Findings (conclusion)

The application container is healthy. Nginx retained `10.16.26.50:80` in the address set resolved for the Consul-backed Nomad proxy service at its 2026-09-09 reload. The operator later powered off Nomad client `.50`. Consul DNS removed it and now advertises `.33`, `.44`, and `.55`, but the literal hostname in `proxy_pass` is not periodically re-resolved. Requests assigned to the stale address wait in TCP connect, producing the long page loads and client-aborted 499 records. The same stale proxy member affects many other test/autotest vhosts.

## Actions: evidence and commands

- `curl http://10.16.26.7:24219/sms`: HTTP 200, about 7-8 ms.
- `dig +noall +answer youdo-business-mock-api.test14.yandex-test.youdo.local`: CNAME to `proxy.service.yandex-test.consul`; current 1-second A records are `.33`, `.44`, and `.55`.
- Direct proxy checks with the correct Host header: `.33/.44/.55` return HTTP 200 in about 9-10 ms; `.50` reaches the 3-second TCP connect timeout.
- Controlled local HTTPS requests used `curl --resolve business-mock-api.test14.youdo.sg:443:127.0.0.1`. Fast requests logged upstream `.55:80`; every alternate request sent to `.50:80` timed out and logged status 499, `uct="-"`, and no response headers.
- Browser access-log evidence for `.50` included 499 durations 11.8, 38.5, and 54.1 seconds.
- `journalctl -u nginx`: latest reloads were 2026-09-09 19:10-19:13 MSK. Worker processes started at 19:13:54.
- Relevant files: `inventories/yandex/group_vars/balancers_test`, `roles/nginx/templates/vhost/business-mock-api.youdo.com.j2`, and live `/etc/nginx/conf.d/business-mock-api.test14.youdo.sg.conf`.

## Recovery and follow-up

1. Immediate, safe recovery: run `nginx -t`, reload nginx, then verify new requests use current Consul members and no new `.50` records appear.
2. Implement dynamic upstream membership handling centrally for `proxy.service.yandex-test.consul`; test URI/Host semantics before rollout.
3. Alternatively connect Consul-template service membership changes to a validated nginx config regeneration/reload.
4. Add a bounded `proxy_connect_timeout` only as a secondary guardrail.
5. Before shutting down another Nomad proxy client, drain it from Consul/Nomad, wait for DNS removal, and ensure edge proxies have refreshed membership.

## Changes

No runtime changes were made during the initial diagnosis. The operator subsequently performed a graceful nginx reload.

## Post-reload verification

- Reload completed at 2026-09-11 17:25:15 MSK; new worker PIDs were `1409209` and `1409210`.
- Current DNS and the new nginx pool contain only `10.16.26.33`, `.44`, and `.55`.
- Thirty controlled requests through nginx all returned HTTP 200 in 13-33 ms. Access logs recorded `.33` 11 times, `.44` 9 times, `.55` 10 times, and `.50` zero times.
- All active per-vhost access logs contained zero new `.50:80` upstream entries after the reload; the mock-api log contained no new 499/502/504 response.
- The old workers remained temporarily in graceful `shutting down` state due to existing connections, but did not accept new connections and had no active socket to `.50` at verification time.

## Open items

- The immediate incident is recovered. A future proxy-client removal can reproduce the issue until dynamic service-membership refresh is implemented (items 2-5 above).

## Portable lesson

[nginx: literal `proxy_pass` hostname is resolved once, stale upstream after DNS change](../../../../general/knowledge/nginx/proxy-pass-hostname-not-re-resolved-stale-upstream.md)
