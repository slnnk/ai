---
system: jenkins
status: verified
checked: 2026-10-16
tags: [jenkins, dns, systemd-resolved]
---

# Jenkins AutoTest buildsinfo .local DNS routing failure

## Summary

Live SSH checks reproduced failure on AutoTest, while controller host/container resolved the name successfully. Applied the existing dnsmasq role to AutoTest after explicit user approval; post-change host and container lookups pass.

## Context and actions

User asked which DNS Jenkins uses because buildsinfo.vk-test.youdo.local fails. Checked resolv.conf, nsswitch, Docker network/DNS, dnsmasq forwarding, resolvectl status/query, getent and dig over SSH as root on controller10.18.26.8 and agent10.18.26.26. No secrets read or recorded.

## Findings

- Controller: /etc/resolv.conf nameserver10.18.26.8; dnsmasq default upstream10.18.20.3, Consul forwarding10.18.26.11/.12/.13:8600 and public-test.consul10.18.26.63. Container jenkins uses127.0.0.11 with cached external resolver127.0.0.53. Both host/container getent return10.18.26.60.
- Agent: systemd-resolved stub127.0.0.53 forwards ordinary DNS to10.18.20.3 on ens3, domainmcs.local. Container jenkins-agent-jenkins_agent-1 uses host networking and the same stub. Both host/container getent fail for buildsinfo.vk-test.youdo.local. resolvectl query reports No appropriate name servers or networks for name found; dig@127.0.0.53 returnsSERVFAIL.
- Direct dig@10.18.20.3 succeeds: buildsinfo.vk-test.youdo.local CNAME buildapi.dev.youdo.corp A10.18.26.60. This supersedes earlier wildcard-alias observations; no alias mutation performed by this investigation.
- Agent getent buildapi.dev.youdo.corp succeeds. Failure is systemd-resolved routing for the private .local name, not an absent upstream record. Only mcs.local is configured as a DNS domain.

## Applied fix and verification

User explicitly instructed applying the existing dnsmasq role to the agent. Ran a temporary playbook targeting only vk-ms1-jenkins-agent-test-01 (10.18.26.26), using the existing repository role and the same forwarding rules as the controller. Result ok10 changed8 failed0 unreachable0. dnsmasq installed/enabled/active; systemd-resolved disabled/inactive; /etc/resolv.conf points to10.18.26.26 and search youdo.local. dnsmasq --test passed. Host getent, dig@127.0.0.53 and the existing host-networked Jenkins agent container all resolve buildsinfo.vk-test.youdo.local via CNAME buildapi.dev.youdo.corp to10.18.26.60. No repository source files or Jenkins job configuration changed. HTTP endpoint behavior was not tested.
