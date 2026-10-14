---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [dns, vk-cloud, mssql, nomad]
---
# DevOps-897: VK private DNS checked on running VMs

## Task

User asked to verify VK private DNS on already running VMs for the DevOps-897 large MSSQL migration.

## Context

Read-only SSH to Jenkins controller10.18.26.8 as root and Nomad agent01 10.18.26.34 as youdo. Existing SSH identities and known_hosts reused. No API/resource/remote configuration mutations.

## Actions

Checked hostname, hostname -f, resolv.conf, resolvectl status, getent ahostsv4 and dig. On Nomad inspected sudo -n ss -luntp for port53. DNS queries used time2seconds/tries1 where available. First sandbox SSH was denied; approved escalated read-only commands succeeded.

Key verification: dig @10.18.20.3 +time=2 +tries=1 vk-ms1-jenkins-test.mcs.local A; repeated for vk-ms1-jenkins-agent-test-01.mcs.local from Nomad agent01.

## Findings

- Controller hostname -f is vk-ms1-jenkins-test.mcs.local. systemd-resolved uses upstream10.18.20.3 and search domain mcs.local.
- Controller default resolver returns NOERROR: vk-ms1-jenkins-test.mcs.local ->10.18.26.8 and vk-ms1-jenkins-agent-test-01.mcs.local ->10.18.26.26. getent also returns the agent address.
- Nomad agent01 direct queries to10.18.20.3 return both same A records with NOERROR. VK private DNS and network reachability work from this client.
- Nomad agent01 /etc/resolv.conf is Ansible-managed, nameserver10.18.26.34, search youdo.local. dnsmasq listens on UDP/TCP53. Default dig and explicit @10.18.26.34 queries for the tested mcs.local names time out; getent returned no addresses. Root cause not investigated. This evidence does not establish failures for all DNS domains or all Nomad clients.
- MSSQL VM DNS records and deletion/recreation registration were not tested. New SQL names are expected candidates vk-ms1-sql-test/test1/test6.mcs.local, not confirmed existing records.

## Changes

This note, existing nomad-test map and DevOps-897 investigation link, service-addresses.env, central backlog and index/sync bookkeeping only. No remote files/services/network/resources changed.

## Risks and limits

Private names must resolve through the configured resolvers of deployment/application consumers. Working direct queries do not prove their default DNS path or container DNS behavior. Only controller and agent01 were sampled.

## Portable lesson

none
