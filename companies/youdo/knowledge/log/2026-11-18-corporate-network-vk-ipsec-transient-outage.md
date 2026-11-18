---
system: corporate-network
status: verified
checked: 2026-11-18
tags: [ipsec, incident, read-only]
---
# VK connectivity recovered during IPsec diagnostics

## Task
Check IPsec on 172.28.0.200 after reported loss of VK Cloud access. Investigation only; no external changes authorized or performed.

## Context
Employee OpenVPN gateway sc-gateway2.youdo.corp (172.28.0.200). VK traffic routes through Selectel FortiGate 172.24.0.1 / 5.188.184.67 to ipsec-vm (10.18.20.3, IKE identity 138.16.203.183), using gre_selectel on the VK side. See [previous topology evidence](2026-11-12-corporate-network-job3296907-vpn-nexus-diagnostics.md).

## Actions
Read-only SSH, ipsec statusall, routes/rules, bounded service journal inspection, short ICMP and HTTP probes, traceroute. No secrets read or retained. Daily sync exited0 without output.

## Findings
- At09:12UTC, 172.28.0.200 strongSwan had131days uptime; configured connections only to KZ and GCP, no direct VK tunnel. VK routes use172.28.0.1. Local gateway ping3/3, VK gateway and Nexus ping0/3; TCP attempts from gateway returned No route to host. Workstation SSH to10.18.20.3 timed out.
- Subsequent traceroute reached172.28.0.4 ->172.24.0.203 ->172.24.0.1 ->10.18.20.3. SSH then succeeded without agent intervention.
- VK journal shows charon SIGINT at09:12:34UTC and fresh start at09:12:36UTC. The to_fortigate_selectel IKE and CHILD SA established at09:12:36UTC;09:12:52snapshot shows bidirectional traffic (705377bytes inbound,4087337outbound). Host uptime38days, so this was a daemon restart, not a host reboot. systemctl metadata remained October11/NRestarts0; journal/process uptime provides direct restart evidence. The user subsequently confirmed a colleague initiated the restart; original failure cause was investigated below.
- At09:12:51–09:12:55UTC (12:12Moscow), gateway->VK ping5/5, average4.20ms; Nexus http://10.18.24.233/ HTTP200/0.035s; Jenkins http://10.18.26.8/login HTTP200/0.059s. Historical Jenkins host8080probe is not used as recovery evidence; host port80is correct.

## Changes
Local KB log, dated link in Nexus map, address-map observation only. No service restart, remote config change, cloud API call, deployment or repository task edit.

## Status and risks
Requested check complete; access recovered during observation. No background processes remain. Exact outage cause, restart initiator and sustained stability are unverified. Task-affected TODO reviewed: historical network incidents remain closed; no new implementation action inferred from this diagnostic request.

## Learning outcome evidence
Scoped learning rules and canonical instructions read before work. One agent performed read-only diagnosis, reported recovery without claiming remediation, and checked every diagnostic session exit. No new user correction or durable preference arose.

## Portable lesson
none

## Task metrics: 2026-11-18-vk-ipsec-check

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "2026-11-18-vk-ipsec-check",
  "created": "2026-11-18T12:13:39.677936+03:00",
  "first_result": "pass",
  "final_result": "partial",
  "state": "closed",
  "kind": "investigation",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Peer INVALID_SPI onset matches user outage timing and Zabbix GRE ingress loss; colleague restart recovered access; initiating event needs unavailable FortiGate logs.",
  "updated": "2026-11-18T12:18:43.580178+03:00"
}
```

## Follow-up: failure mechanism investigation
User requested cause analysis and confirmed a colleague restarted IPsec. User also confirmed the reported outage began approximately12:04Moscow. Read-only investigation continued; no external changes authorized or performed.

Collected charon/ipsec/ipsec_starter/kernel journal08:00–09:13UTC to `/home/slnnk/ai-data/vk-ipsec-20261118/ipsec-journal.txt` (81235lines, includes duplicated charon/ipsec messages). No authentication material retained. Scoped learning query and daily sync completed; no sync output.

### Evidence timeline
-08:06:30 and08:40:02UTC: local IKE reauthentication to FortiGate succeeded; new CHILD SAs installed. No new FortiGate CHILD SA is logged between08:40:02 and the colleague restart.
-09:02:25 and09:02:45UTC: received FortiGate INFORMATIONAL liveness requests0and1, generated replies. At09:03:30 repeated request1was handled as a retransmit.
-09:04:18UTC (12:04:18Moscow): received FortiGate INFORMATIONAL request1with DELETE payload; strongSwan logged `received retransmit of request with ID 1, retransmitting response`. Next received `N(INVAL_SPI)` from5.188.184.67. The log lacks the IKE SPI tuple for these individual exchanges; do not infer that separate requests with equal message IDs necessarily belong to the same IKE SA.
-09:04:18–09:12:32UTC:242charon INVALID_SPI notifications, request IDs0through241, approximately every2seconds. strongSwan generated INFORMATIONAL replies but did not establish a replacement CHILD SA. Two FortiGate IKE SAs remained in daemon state and were deleted on09:12:34shutdown.
-09:12:36UTC: restart established a fresh IKE/CHILD SA; previous HTTP/ping verification confirms restored connectivity.

### Interpretation and limits
Confirmed remote symptom: FortiGate reported unrecognized IPsec packet SPI while strongSwan retained local tunnel state. This supports mismatched/lost CHILD SA state on the FortiGate/strongSwan link as the immediate failure mechanism. [RFC7296section1.5](https://www.rfc-editor.org/rfc/rfc7296.html#section-1.5) defines INVALID_SPI for an unrecognized ESP/AH SPI. It does not establish why the receiver lost or rejected state. Rekey/expiry, FortiGate IKE-process reset or another peer-side event remain hypotheses; no automatic configuration fix is justified from current evidence. Successful IKE liveness traffic is consistent with failed data traffic; shortening DPD alone is not a demonstrated fix.

Zabbix FortiGate10445history corroborates failure: vkcloud-gre inbound item4055369has0through09:05:14–09:12:14UTC (also a short earlier zero interval09:02:44–09:03:14), then370424at09:12:44and7375376at09:13:14. Outbound item4055365remained nonzero. Values are stored monitoring samples, not cumulative wire counters. FortiGate uptime item103310grew continuously08:55–09:15; sampled master serial2572612/2572599and HA configuration checksum2572597were identical at09:02:31and09:12:14. This provides no evidence of a box reboot or persistent HA-master change, but sampling cannot exclude a short transition. CPU17samples08:45–09:15range0–36.9515percent; saturation unproven.

VK host root filesystem77percent used/2.2Gavailable; memory about1510MiBavailable after recovery. Kernel journal07:00–09:13has no entries. Config file mtimes remain October11. These are observations, not proof of historical resource stability. Global XfrmInStateSeqError5977053then5977066is cumulative across all peers since boot; it cannot attribute incident loss or trigger. Post-restart GCP churn and FortiGate unsupported-IKE-version messages were observed but are not established causes of this earlier outage.

FortiGate SSH attempt as admin failed host-key verification (no pinned entry found); verification was not bypassed. Available production Loki label inventory08:55–09:15has no FortiGate/ne1260/IPsec instance and no syslog job/source; no direct peer event log was obtained. Exact trigger requires FortiGate VPN/IKE events for12:02–12:05Moscow, connection `to_vkcloud`, remote138.16.203.183. The follow-up was recorded in the central TODO under YouDo / Corporate network access.

On 2026-11-18 the user cancelled the FortiGate log review and closed the follow-up in TODO. The initiating event remains unverified.

Final status: immediate failure mechanism identified, exact initiating event unresolved. All diagnostic commands finished; no background operations or remote changes.
