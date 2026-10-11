---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, nginx, dns, balancer]
---
# DevOps-890: public Jenkins routing

## Task

User requested switching build.youdo.sg manually on the balancer first, then persisting matching changes in automation-services. No publication requested. Existing approved branch DevOps-890-update-jenkins-images is reused. Concrete remote mutation remains subject to global AGENTS.md explicit command approval.

## Context

Balancer root@10.16.20.35 identifies as balancer-test01. Active regular vhost /etc/nginx/conf.d/build.youdo.sg.conf isroot:root0644, SHA256da8153526579193eea8cba19c8c768ee7687a735be2e95d85392209e8ece654f. Single proxy_pass points to http://jenkins-test.ru-central1.internal/. No duplicate build vhosts found. Includes /etc/nginx/conf.d/*.conf and /etc/nginx/sites-enabled/*. Newcontroller http://10.16.28.8/login returns200 from balancer.

## Actions

Read-only baseline nginx -t failed: host not found in upstream proxy.service.yandex-test.consul in /etc/nginx/conf.d/accountant.autotest01.youdo.sg.conf:9. Balancer /etc/resolv.conf points to self10.16.20.35; active dnsmasq /etc/dnsmasq.d/common.conf forwards yandex-test.consul to old10.16.26.11/.12/.13. Other configured forwarders are10.16.20.3 and ru-central1.internal via10.16.20.2.

Subsequent direct SSH timed out; access via ProxyJump root@10.16.28.8 works without agent forwarding. Direct DNS queries from balancer to all newmasters10.16.28.11/.12/.13:53 returnNOERROR and proxy A records10.16.28.10/.35/.38. Controller/corporate DNS independently return same healthy service records. Repairing old balancer Consul forwarders is the necessary prerequisite to nginx reload; do not disable vhosts or insert placeholder service addresses.

## Findings

User explicitly approved the exact SSH helper action with "Выполни". Sandbox attempt failed before connection; identical outside-sandbox retry through controller ProxyJump completed exit0. DNS forwarders updated to10.16.28.11/.12/.13, Jenkins upstream changed tohttp://10.16.28.8/, nginx test/reload passed. Backups retained at `/root/devops-890-routing/20261010T222502Z` (UTC).

Independent runtime checks confirm new forwarder/upstream lines, nginx and dnsmasq active, nginx -t successful (existing unrelated deprecated http2/protocol/server_names_hash warnings remain). Publichttps://build.youdo.sg/login returned200 withTLSverify0 and publicremote178.154.207.53. Public authenticated API reports Jenkins2.555.1, all11 jobs,116 active plugins, empty queue and AutoTest online with5 executors. No jobs were triggered.

Only after successful manual cutover/public verification, matching local repository changes were made: roles/nginx/templates/vhost/build.youdo.sg.j2 upstream10.16.28.8; inventories/yandex/group_vars/balancers_test five-entry dnsmasq_dns_servers override preserving10.16.20.3 and ru-central1.internal→10.16.20.2, changing only Consul masters. Other hosts retain shared group settings. Scoped diff check, YAML load, Jenkins template render, balancers.yml syntax check and independent review passed. Syntax check used recovery inventory without balancer groups, producing expected unmatched-host warnings; direct YAML/render checks verified modified files separately. No Ansible reapply or Git stage/commit/push occurred; unrelated local changes preserved.

Independent review identified a rollback gap after a failed/timed-out nginx reload; corrected helper to restore/test/reload original vhost while repaired DNS remains available, then revert DNS. Rollback failures are explicit rather than claiming success. Local getent addresses must match verified direct-DNS service addresses. Final syntax and independent re-review passed; manual cutover remains unexecuted pending explicit approval.

Jenkins upstream can be replaced by10.16.28.8, but a plain nginx reload would fail before DNS repair. SSH jump route provides verified access. No remote changes/reload or repository route/DNS edits occurred in this preflight.

## Changes

Prepared local /home/slnnk/ai-data/jenkins-recovery/switch-jenkins-route.py, pending explicit approval. It guards hostname/root/regular files and vhost SHA, verifies new DNS/controller availability, backs up DNS/vhost under protected /root/devops-890-routing/<UTC>/, updates only three Consul forwarding lines, tests/restarts dnsmasq, verifies local resolution, changes only Jenkins proxy_pass, tests/reloads nginx. Failure restores changed configuration files and restarts original DNS configuration. Local Python syntax checked; independent review in progress.

Proposed concrete remote action:

```bash
ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=10 -J root@10.16.28.8 root@10.16.20.35 'python3 -' < /home/slnnk/ai-data/jenkins-recovery/switch-jenkins-route.py
```

After successful manual cutover and HTTP/API verification, update roles/nginx/templates/vhost/build.youdo.sg.j2 to the same upstream and persist new forwarders as a full five-entry dnsmasq_dns_servers override in inventories/yandex/group_vars/balancers_test (scoped to balancers, preserving two non-Consul forwarders). Group all currently carries legacy forwarders; do not broaden this recovery fix to every host.

## Risks

DNS correction affects Consul resolution on this balancer; nginx reload resolves all literal upstream names, including existing proxy vhosts, against healthy recovered service records. Backups retain prior configuration. Verify public TLS/HTTP/API/redirect and recovered agent status after cutover. Global remaining work stays in ~/ai/TODO.md.

## Portable lesson

none
