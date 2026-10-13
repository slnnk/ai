---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, vkcloud, nginx, recovery]
---
# DevOps-892: replacement balancer nginx inspection

## Task

Inspect the replacement Jenkins balancer supplied by the user for [DevOps-892](https://youtrack.youdo.com/youtrack/issue/DevOps-892) and reconcile the recovery plan with read-only evidence.

## Context

Controller10.18.26.8 and AutoTest10.18.26.26 are restored; Jenkins remains in recovery quiet mode. Earlier records said no replacement balancer existed. User subsequently supplied10.18.20.97, superseding that dependency blocker.

## Actions

Read-only SSH inspection as youdo identified balancer-test01; root login was denied. Inspected Nginx service/version and existing Jenkins configuration. Nginx1.30.1 is active/enabled, with841 *.conf files under /etc/nginx/conf.d. Ran sudo -n nginx -t and checked upstream DNS. Queried /login with curl --resolve build.youdo.sg:443:10.18.20.97 https://build.youdo.sg/login using normal certificate validation. No remote files changed, reload, build or recovery restriction changes occurred. No private key contents were read.

## Findings

Existing /etc/nginx/conf.d/build.youdo.sg.conf redirects port80 to HTTPS301 and listens on443ssl. TLS material locations are /etc/nginx/ssl/wildcard.youdo.sg.crt and /etc/nginx/ssl/wildcard.youdo.sg.key. proxy_pass targets http://vk-ms1-jenkins-test.mcs.local/, resolving to10.18.26.8. The forced-address HTTPS request returned200 and X-Jenkins2.555.1; TLS validation passed. nginx -t passed with server_names_hash max_size1024/bucket64 warnings.

Proxy configuration uses proxy_http_version1.1 and Host/X-Real-IP/X-Forwarded-For/X-Forwarded-Proto headers. Connection is empty and no explicit Upgrade directive exists, so this check does not establish WebSocket forwarding. Balancer-local getent resolves build.youdo.sg to138.16.201.238; global DNS and public end-to-end routing were not verified. Earlier no-balancer and old-DNS observations are superseded by these scoped checks.

## Changes

Updated the existing Jenkins system map and Jenkins item in ~/ai/TODO.md. Added VK_TEST_PUBLIC_BALANCER_IP=10.18.20.97 and observation/verification comments in current/service-addresses.env. Added this log, rebuilt the knowledge index and recorded the change in ~/ai/.sync-notes. No repository task files or remote configuration were changed.

## Risks and limits

An HTTPS login response with a forced address proves the inspected balancer route and certificate, but does not verify public reachability, global DNS, WebSocket agent traffic or functional builds. Jenkins still has the recovery quiet hook. Backup migration, monitoring, image Git correction and Git publication retain their previously recorded status; open work is tracked only in ~/ai/TODO.md.

## Portable lesson

none
