---
system: vk-cloud
status: verified
checked: 2026-10-21
tags: [network, incident, router, jenkins, nexus, nomad]
---
# VK inter-subnet connectivity incident affecting Jenkins Nomad and Nexus

## Task
Investigate user-reported access failures for build.youdo.sg, Nomad and Nexus. Diagnostics only; no infrastructure changes or support message authorized.

## Context
VK RegionOne, network 996906a7-99ca-42e7-a916-632cc7eb6a28, router shared-router (024c38ca-3d4d-4fc3-aad0-d8a3d1f47375). Existing maps: [Nomad](../systems/nomad-test.md), [Jenkins](../systems/jenkins.md), [Nexus](../systems/nexus.md). Address map: ../../service-addresses.env. Current incident is separate from the previously user-closed nested-VPN access diagnosis.

## Actions
Read-only checks at 08:26–08:30 UTC (11:26–11:30 Moscow). Checked workstation VPN/DNS/HTTP, SSH to gateway and balancer, gateway routes/firewall counters, targeted TCP packet headers, Neutron/Nova GET APIs using existing automation credentials. API authentication values remained in memory. Created local diagnostic helper /home/slnnk/ai-data/vk-access/cloud_read.py and support draft /home/slnnk/ai-data/vk-access/support-draft.txt.

## Findings
- Corporate tun0 and its gateway 172.30.63.1 respond; GitLab HTTPS returns 302. SSH reaches ipsec-vm (10.18.20.3) and balancer-test01 (10.18.20.97). Balancer-to-gateway ping succeeds and local nginx responds 301.
- build.youdo.sg resolves to 138.16.201.238 but HTTP response times out. Its balancer cannot connect to Jenkins 10.18.26.8:8080.
- Gateway cannot connect to Nomad 10.18.26.11:4646 or Nexus 10.18.24.233:80. Workstation direct connections also time out. Nomad discovery returns SERVFAIL/timeouts; gateway loopback DNS query also times out despite bind9 active. DNS upstream reachability is a hypothesis, not independently isolated.
- Routes from gateway and balancer to affected destinations use 10.18.20.254. Gateway has a reachable ARP entry for that address; ping receives no replies (alone not proof of router failure).
- Targeted packet capture on gateway ens3 sees repeated TCP SYN to Nomad with no response. This capture cannot distinguish router, target host, or return-path loss.
- Nginx errors also show connection timeouts to Nomad proxy 10.18.26.10:80 and Kubernetes ingress 10.18.26.60:80. Failure spans multiple backends and two destination subnets.
- Cloud API reports shared-router, all three router interfaces, selected VM ports, Jenkins/Nexus/gateway/balancer VMs ACTIVE. Relevant test/prod ingress groups allow any IPv4 protocol from 10.18.20.0/24. Router updated_at is October16; relevant group update timestamps predate this incident. Effective provider enforcement and target guest health remain unverified.
- Working hypothesis: inter-subnet virtual-network forwarding failure involving shared-router/dataplane. Exact fault location, onset and provider-wide scope remain unknown. No host restarts, firewall changes or router modifications performed.

## Changes
Local diagnostic helper, support draft, this note, linked map status and central backlog only. No external writes except the standing daily KB sync.

## Status and risks
Initial checkpoint: incident was unresolved and a support draft was prepared but not sent by the agent. Superseded by the dated recovery follow-up below; the user confirmed recovery and the central incident entry is closed. Exact root cause remains unknown.

## Portable lesson
none

## Recovery follow-up, 2026-10-21 09:04–09:10 UTC
The user reported nginx, Nexus and Nomad recovered, then initially reported Jenkins UI hanging. Public /login, balancer-to-controller /login and controller loopback returned HTTP200; three full public login GETs and four CSS/JS resource GETs succeeded. Controller container had been up four days, memory available about6GB, /data55%used. One later workstation-to-controller SSH attempt timed out; no stable-network claim follows from the HTTP checks.

Correction to initial evidence: controller publishes host TCP80 to container8080. The earlier balancer probe to host10.18.26.8:8080 used the wrong port and is not evidence of Jenkins network failure. Independent gateway-to-Nomad/Nexus failures and other nginx upstream timeouts remain valid. Final local support draft is archived as recovered; it was not sent by the agent. User submission/provider intervention are not independently verified.

The user next reported empty monolith/static versions in dynamic_deploy and missing branches in youdo_web_testing_one. Read-only job config inspection showed dynamic_deploy Active Choices calls http://lenochka.youdo.sg/api/versions/18 and /278, then GitLab pipeline API. Web job branch parameter is Git Parameter PT_BRANCH against https://gitlab.youdo.sg/youdo/youdo.static.git. At09:08UTC controller and container resolved both names; unauthenticated HTTP probes returned401 quickly, proving DNS/HTTP reachability only, not authenticated data retrieval. No authenticated parameter evaluation or build was triggered. Before further checks, the user confirmed that everything now works; diagnostics stopped. Exact cause of the transient parameter/branch failure remains unproven.

Final status: access and parameter/branch recovery accepted on user confirmation; no Jenkins/cloud configuration changes, restarts or builds by the agent. The central incident entry is closed without claiming provider root cause or long-term stability.
