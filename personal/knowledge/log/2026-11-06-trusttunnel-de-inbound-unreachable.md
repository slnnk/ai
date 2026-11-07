---
system: trusttunnel-de
status: verified
checked: 2026-11-06
tags: [vpn, trusttunnel, network, access]
---
# TrustTunnel endpoint: inbound access times out

## Task

Investigate inability to connect to the personal VPN from both PC and phone.

## Context

TrustTunnel endpoint `it-garage-de-01`, `2.26.30.176`, domain
`2.26.30.176.nip.io`; see the [system map](../systems/trusttunnel-de.md).
The user supplied a provider VNC console screenshot during the investigation.

## Actions

- Read the existing endpoint record and local Ansible firewall template.
- Inspected the PC route to the endpoint, resolved its domain, and attempted
  HTTPS `/tt_ping`, SSH and direct TCP connections to ports 22, 80 and 443.
- Sent three ICMP echo requests to the endpoint from the PC.
- Requested read-only VNC output for service activity, listening sockets and
  `cscli decisions list`, because remote SSH was unavailable.
- After the user's explicit request, repeated diagnostics via the corporate
  gateway `root@sc-gateway2` (`172.28.0.200`). The existing known-host address
  allowed SSH to the gateway; the short alias did not have a verified host key.
- Attempted SSH to the VPS through that gateway, tested HTTPS and TCP 22 from
  the gateway, and requested a bounded VNC packet capture for both source IPs.
- Correlated gateway TCP probes and successful ICMP with a second VNC capture;
  then captured target-specific egress headers on the gateway and checked an
  unrelated public TCP/443 endpoint as a control. All captures were bounded.

## Findings

- The VNC screenshot shows `ens3` up with `2.26.30.176/32` and five successful
  pings from the VPS to `8.8.8.8` (0% loss). This verifies outbound ICMP at the
  screenshot time, not inbound reachability or VPN service health.
- The PC resolves `2.26.30.176.nip.io` to `2.26.30.176`. Its route to that IP is
  direct through the home Wi-Fi gateway, outside the active corporate tunnel.
- HTTPS timed out before TCP/TLS establishment; SSH port 22 also timed out.
  Independent direct-IP TCP probes to ports 22, 80 and 443 all timed out.
- ICMP from the PC received zero of three replies. The phone failure is
  user-reported; whether it used cellular data or the same Wi-Fi is unknown.
- The local Ansible template allows SSH and VPN ports and accepts ICMP, but
  places CrowdSec source blocking before the ordinary input rules. This is
  desired configuration, not evidence of the current runtime rules.
- Root cause remains unknown. Source blocking, host/provider filtering and
  a network-path problem remain hypotheses. The observed PC failure occurs
  before VPN authentication; no password or certificate failure was observed.
- Later VNC output confirms all five checked services active: TrustTunnel, SSH,
  nftables, CrowdSec and its firewall bouncer. TCP 22/80/443 and UDP 443 listen
  on the public IPv4 wildcard address.
- VNC `nft -t list ruleset` shows explicit accepts for TCP 22/80/443, UDP 443
  and ICMP, with established/related traffic and loopback accepted. Output is
  accepted; the only earlier input hook shown is CrowdSec source blocking.
  Terse output omits set contents, so it cannot establish source membership.
- The PC's current public source is `193.160.204.45`, absent from the seven
  decisions visible in the screenshot. Exact nftables set membership remains
  unverified. Gateway egress was independently checked as `45.159.210.228`.
- SSH to the corporate gateway succeeds. From there, three VPS pings succeed
  with 0% loss and approximately 40 ms RTT, while HTTPS times out before TCP
  connection and a bounded TCP 22 check times out. SSH through the gateway
  never established a VPS session. This is not a complete VPS network outage.
- Six repeated TCP probes to each of ports 22 and 443 from each source all
  timed out at 13:49:51–13:50:32 UTC. The first VNC capture showed zero packets,
  so a second capture included ICMP as a positive control.
- At 13:52:41, 13:52:47 and 13:52:53 UTC (16:52 MSK), gateway probes reported
  successful ICMP and TCP 22/443 timeouts. The matching VPS VNC capture shows
  echo requests from `45.159.210.228` and replies at those times, but no TCP
  packets from that source. The 45-second capture ended normally, with 16
  packets captured and no kernel drops. The last two gateway probe rounds
  occurred after the displayed capture window and are not paired evidence.
- A separate gateway egress capture at 13:54:41–13:54:45 UTC shows SYN packets
  and retransmissions for VPS TCP 22/443 without replies, plus a successful
  ICMP exchange. Concurrent TCP/443 to `1.1.1.1` succeeds. Gateway probes
  therefore generate outbound TCP and general outbound TCP/443 is functional.
- Conclusion: tested TCP traffic does not reach the VPS interface capture,
  while ICMP does. The failure occurs before the VPN application and ordinary
  guest input rules. The precise loss point between gateway egress and VPS
  ingress remains unknown; provider firewall/anti-DDoS/ACL or transit filtering
  are hypotheses, not verified root causes. Provider-side investigation is
  the proposed next step. UDP/QUIC had not yet been tested at this stage;
  the subsequent UDP checks are recorded below.

## Changes

Knowledge-base records only. No server, client configuration or Ansible
repository changes; no service restarts.

## IPv6 access check

The user subsequently supplied VNC `ip -6 a` output showing global address
`2a0d:d940:1a:9d0::2/64` on `ens3` and asked to try SSH over IPv6.
Both the PC and `sc-gateway2` return `Network is unreachable` for the IPv6
route lookup. Direct PC SSH and gateway IPv6 ping/TCP 22 checks fail with the
same local routing error, before reaching the VPS. This does not establish
whether the VPS is reachable over IPv6 from a connected IPv6 network. No
network configuration changes were made; all checks exited.

## UDP access check

At the user's request, tested UDP/443 from the PC and the explicitly authorized
gateway. Each test sends a 1200-byte QUIC long-header datagram with reserved
version `0x0a0a0a0a` and random connection IDs, up to three attempts with a
three-second timeout. A Version Negotiation response is checked for version
zero and reversed matching connection IDs. Method reference:
[RFC 9000, section 6](https://www.rfc-editor.org/rfc/rfc9000.html#section-6).

Both sources received no reply from `2.26.30.176:443` after three probes.
Both received valid matching Version Negotiation responses from the control
`1.1.1.1:443`, advertising QUIC v1 (27 bytes; approximately 20 ms from the PC
and 1.5 ms from the gateway). This confirms the probe and general UDP/443
connectivity work from both sources, but does not by itself locate the loss
or prove that the target implementation must answer this probe. A bounded VNC
UDP capture with ICMP control was requested to distinguish arrival from silence.
No VPN credentials, client routing changes or server changes were used.

## Status and risks

2026-11-06: access diagnostics completed, access not restored. The user provided
VNC evidence; no SSH session to the VPS succeeded. Upstream TCP-path/provider
investigation is proposed and tracked in
[central TODO](../../../TODO.md) under Personal / TrustTunnel endpoint.
All agent-started commands exited, including both repeated-probe processes and
the bounded gateway capture. Both user VNC capture screenshots show completion
and a returned shell prompt. No task background operation remains.

## Portable lesson

none
