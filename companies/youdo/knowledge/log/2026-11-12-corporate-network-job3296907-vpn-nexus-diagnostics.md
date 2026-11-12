---
system: corporate-network
status: verified
checked: 2026-11-12
tags: [incident, openvpn, gitlab-ci, nexus]
---
# VPN disconnects and chat-agent Docker transfer delay

## Task
Diagnose reported employee VPN disconnects and slow [build-bot job3296907](https://gitlab.youdo.sg/youdo/ai/youdo-chat-agent/-/jobs/3296907). Investigation only; no external mutations authorized or performed.

## Context
Runner `gitlab-runner-docker-2`, `172.28.0.172`; Nexus `10.18.24.233`; current employee OpenVPN `sc-gateway2.youdo.corp`, `172.28.0.200`; VK IPsec gateway `10.18.20.3`. Existing chat-agent checkout inspected without edits; CI commit is `553a606529d4b1d736b2e68a4aa83fc8e94a4e29`, local checkout freshness was not assumed. [Nexus map](../systems/nexus.md), [current VPN identification](2026-10-13-corporate-network-openvpn-n-velikanets-routes.md).

## Actions
Read-only GitLab job/trace/pipeline queries, Zabbix history, SSH service/interface/log inspection on VPN, runner, Nexus and VK gateway; short ping/MTR probes. Initial sandbox network failures were retried through approved escalation. Generated sanitized trace and read-only diagnostic helpers are under `/home/slnnk/ai-data/gitlab-diagnostics/`, including `job3296907.trace`, `incident3296907.py`, and `incident3296907-gateways.py`. No credentials or full VPN client inventory retained.

## Findings
All times below are Moscow unless explicitly UTC.

- Job succeeded at19:25:03, started19:08:37, duration985.96s; queue2.55s. Previous bot builds lasted302.41s,135.58s and222.63s. Parallel build-web lasted782.55s on runner172.28.0.171; migrations131.56s on the same runner as bot. Therefore queue starvation and one hung runner do not explain the delay.
- Initial Docker cache-image pull began around19:09:13. Runner trace byte offsets were5752at19:09:40,5957at19:14:41,33200at19:21:41. Docker restore timestamp16:21:20UTC and BuildKit durations place the end of pull around19:21:00: approximately12minutes in pull, then restore3.5s and publish17.8s. Push started around19:21:48 and finished19:24:53: approximately3minutes. Timing is reconstructed, since individual Docker output lines lack wall-clock timestamps.
- Nexus backend request.log records all20bot manifest/blob GETs HTTP200 between19:09:13 and19:09:35; largest182,748,238-byte layer took261ms between backend and its local proxy. This is not end-to-end delivery timing. The165,630,839-byte upload PATCH completed19:24:50/backend1181ms, final PUT1761ms. Backend is responsive; frontend/network/client transfer is the delayed portion. nginx access logging is disabled and error logging goes to `/dev/null`, so historical frontend durations cannot be reconstructed. No `limit_rate` found in inspected nginx main/default configuration.
- Nexus data disk71%used,56GiBfree; Zabbix15:58–16:28UTC CPU idle minimum93.94%, aggregate iowait maximum0.511%. VPN CPU idle minimum87.00%; load0.18at16:27UTC, memory available1377MiB. FortiGate monitored CPU16samples maximum29.9697%; saturation is not established. Disabled/stale Zabbix items were not treated as healthy evidence. A reserve Kazan monitor has100%loss throughout the sampled window; no causal relationship established.
- Runner MTR at19:30:50: `172.28.0.4 -> 172.24.0.203 -> 172.24.0.1 -> 10.18.20.3 -> 10.18.20.254 -> 10.18.24.233`; first three hops0/10lost, final destination2/10lost with155.5–209.3ms replies. Repeat at19:31:30: destination0/25lost,13.0–39.3ms; intermediate60%ICMPnonresponses did not persist to destination and cannot establish transit loss there. Earlier direct runner ping0/10lost,5–17ms. This supports intermittent path degradation, not a persistent outage or an exact faulty hop.
- Control runner->VPN ping0/15lost,0.227msaverage; VKgateway->Nexus0/15lost,1.712msaverage. Runner->Nexus routes through FortiGate and VK `gre_selectel`; it does not traverse employee OpenVPN `tun0`. VK tunnel has installed SAs, no matching retransmit/dead-peer errors in the inspected window. SA lifecycle events at19:06:45 and19:25:02 are not proof of failure.
- Employee OpenVPN active continuously since October16, no current unit restarts. Physical NIC errors/drops0; accumulated tun0drops682414and KZGREerrors4502/drops2013 did not grow between snapshots and are not incident loss rates. At19:16:51 two distinct clients timed out simultaneously; another at19:19:37 and another timeout at19:25:49. `keepalive 20 60` means a timeout reflects preceding missing keepalives, not necessarily an outage beginning at that timestamp. UDP EHOSTUNREACH messages also occurred.25clients active at19:29. These are actual session liveness failures, but their upstream/client/server-network cause is unproven.

Working hypothesis: intermittent degradation on the Selectel/perimeter/VK path caused slow Docker transfer. The exact device/provider and any common cause with employee VPN disconnects remain unverified. Small ping recovery does not prove bulk TCP throughput recovered. No throughput load test, packet capture, FortiGate configuration change or service restart was performed.

## Requested repeat at19:36 Moscow

User requested an immediate repeat of runner-to-Nexus checks. Read-only SSH on the same runner172.28.0.172 ran19:36:10–19:36:33: MTR50probes showed destination0/50lost, RTT4.9/16.7/53.8ms min/avg/max; first three hops0%loss. VKgateway/intermediate router each omitted70%ofTTL-expired responses, while destination loss stayed0%; this does not establish transit loss on those routers. The subsequent direct Nexus ping lost1/25packets(4%), RTT4.326/8.841/24.680ms. Control VPNgateway ping0/15lost, RTT0.214msaverage. Occasional destination nonresponse remains observable; a persistent20%loss rate is not reproduced, and ICMP alone does not establish TCP impact or exact cause. All commands finished; no external changes or background operations.

## Requested repeat at19:41 Moscow

Same read-only probe sequence from runner172.28.0.172 ran19:41:12–19:41:35. Nexus MTR0/50lost, RTT5.3/37.7/76.8ms min/avg/max; direct Nexus ping0/25lost, RTT7.156/36.668/101.319ms. VPNgateway control0/15lost, RTT0.232msaverage. First three MTRhops0%loss; intermediate70%nonresponses again did not propagate to destination. Packet loss was not reproduced in this sample, but Nexus latency remained variable and higher than the19:36sample. No proof of bulk TCP recovery or exact fault location. Command exit0; no background operations.

## Changes recorded
Local diagnostic artifacts and this KB log; dated evidence linked in existing Nexus and chat-agent maps. No repository edits, Git mutation, external comments, retry, configuration change or deployment.

## Status and risks
Read-only diagnosis finished. No background operations remain. Exact transport cause and common VPN/build causality remain unknown; any remediation requires a separately reviewed action. Reconciled affected TODO sections: historical accepted closures retained, no new implementation task inferred from this diagnostic request.

## Learning outcome evidence
Loaded scoped learning rules and canonical global instructions before diagnostics. Used one agent, maintained progress updates, escalated sandbox network failures, completed all diagnostic child processes and reported causal limits. No new user correction or durable preference arose in this task.

## Portable lesson

none
