---
system: trusttunnel-de
status: verified
checked: 2026-11-13
tags: [vpn, relay, ansible, migration, monitoring]
---
# Russian relay migrated to SimpleCloud

## Task and authorization
User added `simplecloud-msk-01` and redirected DNS, explicitly requested applying vpn-proxy, then requested powering off `dline-spb-01` and using its HetrixTools SID. Prior instruction against SID reuse was superseded for this specific retired-to-new-host identity transfer; the old agent was stopped before new collection started. User separately approved adding `inventory/host_vars/simplecloud-msk-01.yml` in existing checkout `/home/slnnk/mygit/ansible`, reusing `master` with base `b857c7e`. No publication requested or performed.

## Preflight
User's inventory already had `simplecloud-msk-01` at85.143.174.240 as the sole vpn_proxy member; old host remained in all only. Debian13.5/x86_64, root SSH and Python available, roughly1GBRAM/20GBdisk, no pre-existing nginx/CrowdSec. German backend152.234.226.70 HTTPS returned200/TLS0 from the new relay. Syntax and limited-host list checks passed. Existing user/untracked files were preserved. No separate worktree.

## Changes and execution
Initially applied existing functional playbook with `--limit simplecloud-msk-01 --skip-tags hetrixtools -e trusttunnel_proxy_domain=v.slnnk.com`, because new host had no domain/SID vars yet. It created the automation user and configured common, nftables, sshd, CrowdSec and shared nginx TCP/UDP relay. Recap:77ok,38changed,0unreachable,0failed. No backend changes or Certbot invocation.

After repo gate approval, copied only the prior host's two host-var definitions into the new host_vars file: domain derived from the German inventory and the already Vault-encrypted SID. Ciphertext copied without exposing plaintext; decryption in memory confirmed equal32-character SIDs. Only agent-created repository file is `inventory/host_vars/simplecloud-msk-01.yml`. No stage/commit/push. Syntax check passed again using existing Vault-password helper backed by personal/.env.

After new relay HTTPS passed, SSH to48.103.180.18 confirmed hostname dline-spb-01 and at00:51:25MSK executed `systemctl stop hetrixtools_agent.timer hetrixtools_agent.service && systemctl poweroff`, exit0. Subsequent SSH timed out. This confirms accepted shutdown command and network unreachability; provider-panel physical power state was not observed. No force reset or deallocation performed.

Applied `--tags hetrixtools` with the Vault password helper to the new host. Recap19ok,7changed,0unreachable,0failed. Role installed the versioned agent/timer using the migrated SID. Old/new agents were not deliberately run concurrently. API subsequently returned hostname simplecloud-msk-01, Debian13, kernel6.12.86+deb13-amd64 and nginx online. Agent reports the new VM's IPv6 egress address; this is distinct from the public relay A record. Future power-on of the retired old VM must avoid reactivating its old SID collector; no extra disable/power-on operation was performed.

## Verification
- `nginx -t` passed; nginx/nftables/ssh/crowdsec/bouncer active and failed units0. TCP80/TCP443/UDP443 listeners present.
- Pinned new-IP HTTPS /tt_ping returned200/TLS0 in0.147seconds; plain HTTP redirected301.
- Temporary local SOCKS TrustTunnel clients authenticated viaHTTP2 andHTTP3, both returning German egress152.234.226.70. Existing encrypted inventory credentials were used only in memory, with non-secret client settings; no main client or system route modification. Both temporary clients stopped.
- Missing-token ACME probe returned404 and German access log confirmed receipt from85.143.174.240 with original path. No file created, no renewal test or certificate changes.
- New-VM kernel scan found0softlockup/RCU-stall signatures at verification; this is a short observation, not a guarantee of sustained reliability.

## DNS and monitoring limitation
Cloudflare DoH returned A85.143.174.240 and noAAAA; Google DoH still had old A48.103.180.18. Direct authoritative DNS over UDP/TCP from workstation timed out, so authority consistency was not independently established. All those diagnostic commands exited; no ongoing DNS probes.

Latest uptime monitor snapshot was DOWN and full details showed `resolve_address=48.103.180.18`, with10-second connection timeouts. The obsolete resolve address and stopped old relay support DNS caching as the cause; the new pinned address and authenticated transports passed. New agent identity/metrics are separately verified and do not establish uptime-location convergence. No monitor API settings were edited. This earlier pending status is superseded by the user-confirmed monitoring recovery below.

## Status and risks
Requested relay deployment and SID installation are complete. Old host shutdown command completed with exit0; panel power state remains unobserved. The user subsequently confirmed HetrixTools recovery, closing the operational migration follow-up. User selection of SimpleCloud supersedes the earlier unselected-provider search and budget question. All playbooks, SSH checks and temporary clients finished; no task background operations. Normal nginx and monitoring timer remain running.

## Portable lesson
None. Existing encrypted host-vars and functional-playbook patterns were reused. Scoped approval and verification outcomes are recorded here.

## Monitoring recovery confirmed by user

User reported receiving the successful HetrixTools server-UP notification after migration. This resolves the remaining monitoring-recovery follow-up; central TODO is closed on that evidence. No further infrastructure changes or network probes were requested or run. Recovery of every recursive DNS cache was not independently rechecked and is not claimed. Relay application, authenticated HTTP2/HTTP3 and new-agent identity were verified during deployment. Migration is complete, with no remaining session action or background task.

## Post-migration DOWN check at 01:26 Moscow

User requested investigating another HetrixTools DOWN alert. Outage39989144c159cce5a66eae31c5d7ccd7 lasted01:21:55–01:26:40MSK (285seconds); final API read showed UP in all four locations. German vpn monitor stayed UP. Failure log recorded connection timeouts after10seconds; monitor resolve_address still held old48.103.180.18. Network diagnostics mixed old-IP ping failures and successful new85.143.174.240 pings with0%loss, supporting residual DNS caching after migration as the leading explanation, not a proven cause of each location failure. No monitoring/DNS edits.

Direct SSH at01:26:47 confirmed new host uptime47minutes, nginx/nftables/crowdsec/agent timer active, no failed units, and no nginx or kernel warning entries in the previous30minutes. Pinned new-IP HTTPS returned200, TLS verification0, in3.23seconds. Agent metrics were fresh with low load; pre-migration historical samples belong to the reused SID and must not be attributed to the new VM. Requested diagnosis complete; no remediation required by the observed recovery, no follow-up execution proposed, all diagnostic commands finished and no background task remains.
