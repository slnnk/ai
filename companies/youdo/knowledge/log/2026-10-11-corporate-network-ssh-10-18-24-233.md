---
system: corporate-network
status: verified
checked: 2026-10-11
tags: [ssh, vpn, mtu]
---

# SSH handshake stall and rejected root keys on 10.18.24.233

## Summary

Default SSH stalls before authentication. Restricting HostKeyAlgorithms to ecdsa-sha2-nistp256 permits the handshake. Login as youdo succeeds with the workstation id_ed25519 key; root rejects all three available user keys. Packet-size-dependent loss strongly suggests a VPN path MTU/MSS problem; the exact dropping component is unverified.

## Task and context

Diagnose ssh root@10.18.24.233; user then requested a login test as youdo. Read-only network probes and remote id only. No infrastructure changes.

## Actions and key commands

- ip route get 10.18.24.233: via 172.30.63.1 dev tun1 src 172.30.63.8.
- ip -d link show tun1: MTU 1500.
- ssh -vvv -o BatchMode=yes -o ConnectTimeout=10 root@10.18.24.233 true: waits at expecting SSH2_MSG_KEX_ECDH_REPLY, then times out.
- ssh -o HostKeyAlgorithms=ecdsa-sha2-nistp256: handshake completes with unchanged ECDSA host-key algorithm. ED25519 host-key restriction also completed handshake.
- ping -n -c 2 -W 2 -M do -s 1200 10.18.24.233: total IP size 1228, 2/2 responses, about 120 ms.
- Payloads 1252, 1272 and 1372 (IP sizes 1280, 1300 and 1400): 0/2 responses each.
- Root login with restricted host-key list: ED25519, ECDSA and RSA user keys rejected; publickey,password advertised. Password not tested.
- youdo login with restricted host-key list: id_ed25519 accepted, remote id returned uid=1001(youdo) gid=1001(youdo) groups=1001(youdo), exit 0.

## Findings

Server advertises OpenSSH_8.9p1 Ubuntu-3ubuntu0.15. TCP/22 is reachable. Hypothesis: shrinking the client algorithm proposal avoids packets exceeding the effective VPN path limit. Successful handshake with the same ECDSA algorithm argues against an ECDSA-specific signing issue. ICMP evidence supports size-dependent packet loss but does not establish exact TCP PMTU or responsible gateway. Root key rejection does not establish whether root login is globally disabled.

Verified interactive workaround: ssh -F /dev/null -o HostKeyAlgorithms=ecdsa-sha2-nistp256 youdo@10.18.24.233. Normal first-connection host-key verification remains required. The earlier command without -F was validated only with a short remote command and does not reliably open an interactive shell.

Reusable recipe: [VPN packet-size handshake stalls](../../../../general/knowledge/ssh/vpn-packet-size-handshake-stall.md).

## Changed files and risks

Company diagnostic log, general recipe, TODO and generated KB indexes only. Temporary host-key file: /tmp/ssh-diag-10.18.24.233-known-hosts, populated during an explicitly approved diagnostic test. Main ~/.ssh/known_hosts unchanged. No password or private key recorded. No permanent VPN/SSH configuration changes. Follow-up tracked in ~/ai/TODO.md.

## Follow-up: interactive session failure

User reported the original workaround still hung. Reproduced with a PTY: authentication succeeds, then no PTY/shell acknowledgement after forwarding the agent and sending LANG plus many LC_* variables. The provided user trace matches this. With -F /dev/null, PTY and shell acknowledgements arrive and an interactive prompt opens on nexus-prod-01. Final interactive test executed id and exit and returned exit 0. This bypasses both ~/.ssh/config and /etc/ssh/ssh_config, including environment forwarding and agent forwarding. These settings were changed together, so their individual contributions remain unverified. Hypothesis: the larger combined session setup traffic hits the same packet-size problem. Removing configs is a temporary workaround, not a permanent MTU correction. No configs edited.

## Follow-up: isolate the SSH configuration trigger

User asked whether workstation SSH config explains why colleagues connect normally. ~/.ssh/config sets User root, ForwardAgent yes, AddKeysToAgent yes and ServerAliveInterval 60 globally. /etc/ssh/ssh_config line 50 sets SendEnv LANG LC_*. Effective IPQoS, ciphers and other transport options match the -F /dev/null baseline. Explicit youdo@ overrides User root.

Controlled PTY tests retaining HostKeyAlgorithms=ecdsa-sha2-nistp256:

- Original configuration with -a (agent forwarding disabled), SendEnv retained: authentication succeeds, interactive setup hangs; bounded diagnostic exits 124.
- -F /dev/null -A (agent forwarding enabled, environment not forwarded): shell, id and exit succeed, exit 0.
- Temporary /tmp/ssh-diag-no-sendenv.conf reproduces user and system options then removes SendEnv with Host * / SendEnv -* at the end: effective ForwardAgent yes and ServerAliveInterval 60 retained, SendEnv absent; shell, id and exit succeed, exit 0. Original files unchanged.

Therefore SendEnv is the isolated trigger for the post-authentication stall on this path, not ForwardAgent. The default host-key algorithm-list stall remains a separate setup-stage symptom, so the tested temporary config command still requires HostKeyAlgorithms=ecdsa-sha2-nistp256. Packet-size/PMTU mechanism remains a hypothesis; colleague configurations and network routes were not inspected. A command-line -o SendEnv=-* is insufficient here: later system configuration adds LANG LC_* again (verified by ssh -G). Including /etc/ssh/ssh_config in a custom config failed its stricter ownership check, so the diagnostic config copied the original settings into a local mode-0600 file.

## Requested permanent client configuration

User requested plain ssh youdo@10.18.24.233 to work. Added a host-specific block at the top of ~/.ssh/config with HostKeyAlgorithms ecdsa-sha2-nistp256; preserved existing Host * settings. Backup: ~/.ssh/config.before-10.18.24.233-20261011. ssh -G confirms the user and host-key algorithm are correct.

Prepared /tmp/ssh-diag-apply-system.py to wrap only the existing SendEnv directive in Host * !10.18.24.233 and restore Host * immediately afterward, preserving subsequent global options. Intended backup: /etc/ssh/ssh_config.before-10.18.24.233-20261011. Execution with sudo -n failed because a password is required; /etc/ssh/ssh_config is unchanged and effective SendEnv still includes LANG LC_*. Requested user to run the prepared sudo command locally. Plain interactive login has not yet been verified after the permanent change.

## Permanent configuration verification

User confirmed the sudo script completed. Fresh ssh -G youdo@10.18.24.233 shows HostKeyAlgorithms ecdsa-sha2-nistp256, no SendEnv, ForwardAgent yes and ServerAliveInterval 60. A comparison for 10.18.24.234 retains the default algorithm list and SendEnv LANG LC_*, confirming the exception is host-specific. Plain ssh youdo@10.18.24.233 opened the interactive shell, ran id and exit, and returned exit 0. A local timeout was used only to bound the diagnostic, not configured for normal sessions. The SSH client configuration task is complete; VPN path MTU investigation remains open separately.

## Nexus deployment transport verification

During the separately approved Nexus deployment, short SSH raw commands worked but larger Ansible setup traffic stalled. A local user-space TCP relay `/home/slnnk/ai-data/nexus-recovery/ssh_mss_proxy.py` sets TCP_MAXSEG1100 before connect and is used as ProxyCommand. SSH authentication and normal host-key validation remain intact; VPN routing, server networking and SSH security settings were not changed. Read-only transfer returned exactly65536 bytes and Ansible Gathering Facts completed through the relay. This verifies the connection workaround; VPN MTU/MSS or packet-drop mechanism remains a hypothesis and the dropping component is still unidentified.

## HTTP browser request-size reproduction

Nexus browser polling POST5310 bytes aborts without HTTP status. A controlled read-only HTTP request with6000-byte diagnostic header timed out after7.11s/default MSS, while identical request using MSS1100 returned HTTP200 in0.23s. Small requests with45KiB response succeed using either MSS. Request-size-dependent path failure is verified; precise VPN/gateway dropping mechanism remains unlocated. A temporary HTTP80 MSS1100 host rule is only prepared and awaits explicit approval; no network rule was applied by this diagnosis.

## Diagnostic direction: VPN capture first

The user preferred inspecting traffic on the VPN server before applying the proposed HTTP MSS rule. No MSS firewall rule was applied; its permission request is deferred. Read-only topology research finds an August3 corporate OpenVPN record for `ipsec-vm`10.16.20.3, tunnel172.30.62.1, config `/etc/openvpn/server.conf`; this is not proof of the recovered current endpoint. Current local route uses tun1 MTU1500, source172.30.63.8 and gateway172.30.63.1; Nexus sees browser source10.18.20.3. Current VPN host/interface identification and header-only traffic inspection are the next diagnostic steps. No packet capture or VPN configuration change was performed by delegated KB research.

## Recovered VPN access and paired header capture

User confirmed VPN/gateway recovery at `10.18.20.3`. Root SSH rejected authentication; `youdo` login and `sudo -n` work, hostname `ipsec-vm`, StrongSwan running with GRE interfaces. First connection accepted the new host key via TOFU into local known_hosts; no remote SSH/root configuration changed. Prior10.16.20.3 map is historical.

Root ran simultaneous35-second text captures, header-focused `tcpdump -s96 -v -S` without ASCII/hex output or pcap file: `/home/slnnk/ai-data/nexus-recovery/vpn-tcp-headers.txt` (any) and `nexus-tcp-headers.txt` (ens3). VPN148 packets, Nexus72 packets, both report0 kernel drops. Delegated analysis read only those local text artifacts. No firewall MSS rule applied.

Failed controlled flow50428: client172.28.0.200 SYN MSS1358 enters gre_selectel, gateway NAT source10.18.20.3 forwards SYN with MSS1310; server1460 SYNACK is clamped to1310 on GRE egress. Request starts at expected seq4267804146, but capture first receives only final911 bytes seq4267809338:4267810249. Missing first5192 bytes are already absent at GRE ingress and also absent at Nexus; Nexus repeatedly ACKs4267804146 until client FIN about7 seconds later. Gateway forwards the observed tail correctly. Thus loss occurs before the captured gateway GRE ingress, not between its ens3 and Nexus.

Successful comparison flow49224 advertises MSS1100, unchanged through gateway. Complete6103 request bytes seq4265393284:4265399387 arrive and are acknowledged; Nexus sends591 response bytes. SYNACK on return GRE still advertises1310, consistent with client-side outgoing segmentation making this comparison work. Capture packet lengths2176/1751 may reflect GRO/GSO coalescing and must not be treated as wire segment sizes. No IP fragment records observed. Exact upstream dropping device remains unidentified; additional upstream/GRE-path evidence is needed. Browser traffic from172.24.0.12 also traverses gre_selectel and receives MSS clamp1310.

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.
