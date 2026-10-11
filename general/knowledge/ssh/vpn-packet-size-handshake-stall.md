---
system: ssh
status: hypothesis
checked: 2026-10-11
tags: [ssh, vpn, mtu]
---

# Diagnose SSH handshake stalls caused by packet size on a VPN path

## Summary

TCP connects and SSH banners exchange, but the client waits at expecting SSH2_MSG_KEX_ECDH_REPLY. A shorter host-key algorithm proposal completes the handshake, while larger ICMP packets fail and smaller ones succeed. This pattern strongly suggests a path MTU/MSS problem; it does not identify the dropping device.

## Symptom and cause

Hypothesis: the default algorithm proposal exceeds the effective VPN path packet limit; packets or fragments are dropped and PMTU recovery is ineffective. Tunnel interface MTU can exceed the usable end-to-end limit.

## Diagnosis and workaround

Use ssh -vv with a bounded timeout. Inspect the route and tunnel MTU. Compare ping -M do with different payload sizes (IPv4 total size is payload plus 28 bytes). Repeat SSH with -o HostKeyAlgorithms=ecdsa-sha2-nistp256 while retaining the host-key algorithm selected by the failing default attempt. If this succeeds, it isolates proposal size from the selected host-key algorithm. Keep normal host-key verification enabled.

The restricted algorithm list is a temporary workaround when the server supports that algorithm. Validate login separately: passing key exchange does not mean the user key is authorized. A permanent fix requires locating and correcting the tunnel MTU/MSS or PMTU signaling problem, with permission before infrastructure changes.

## Limits

Small ICMP samples do not prove exact TCP PMTU. Server health, filtering and transient loss remain alternatives. Packet capture or testing from another route is needed to identify where packets disappear. Do not infer that root login is disabled solely from public-key rejection.

## Interactive session validation

A short remote command can succeed while interactive setup still stalls after authentication. Test a real PTY, prompt and a command inside the shell. As a comparison, -F /dev/null bypasses user and system SSH configuration, removing environment and agent forwarding. If this succeeds, it establishes a usable temporary workaround but does not isolate the individual option responsible or correct the underlying packet-size problem.

## Isolate environment forwarding

Compare original configuration with -a against -F /dev/null -A: this separates agent forwarding from the remaining options. A further temporary config retaining original settings but ending with Host * / SendEnv -* can isolate environment forwarding. Check effective settings with ssh -G. A command-line SendEnv removal may precede system config additions and leave variables enabled, so do not assume it worked. In one diagnosis, removing only SendEnv restored the interactive shell; removing only agent forwarding did not. This proves an environment-forwarding trigger in that case, while the packet-size mechanism remains a hypothesis.
