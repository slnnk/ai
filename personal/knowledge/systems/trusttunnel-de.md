---
system: trusttunnel-de
status: verified
checked: 2026-11-13
tags: [trusttunnel, vpn, ansible, nftables, crowdsec]
---
# TrustTunnel endpoint it-garage-de-01

## Summary

- Personal TrustTunnel VPN on `it-garage-de-01`, `152.234.226.70`, in Germany.
- Active server endpoint: `v.slnnk.com`; TCP/UDP 443, nginx on TCP 80.
- Own domain deployed; external HTTPS `/tt_ping` returns 200 with valid TLS.
- The user confirmed clients work after migration to `v.slnnk.com` on 2026-11-08; migration complete.
- Managed by `/home/slnnk/mygit/ansible`, `playbooks/vpn.yml`.
- Host nftables permits SSH and VPN; CrowdSec filters blocked sources first.
- StrongSwan on this host was removed on 2026-11-04; dated sections retain history.
- PC client configuration lives under `/home/slnnk/trusttunnel/`.
- See Components, Delivery path and Access for configuration and access routes.
- See Local PC client routing adjustment for corporate-VPN coexistence history.
- On 2026-11-08, the user reported the previous IP was blocked, a replacement
  was issued, and they updated Ansible and applied the role.
- Local inventory confirms `152.234.226.70` and desired domain `v.slnnk.com`.
- The user confirmed VPN recovery before domain migration; new-domain HTTPS was subsequently verified by the agent.
- The old-address incident is closed; historical diagnostics remain below.
- Current Russian relay: `simplecloud-msk-01`, `85.143.174.240`; HTTP/2 and HTTP/3 authenticated checks passed on2026-11-13. Old relay poweroff accepted; user confirmed HetrixTools UP after migration.

## Current Russian relay: SimpleCloud, 2026-11-13

User-selected `simplecloud-msk-01` /85.143.174.240 is deployed with existing vpn-proxy
playbook:77ok/38changed/0failed; monitoring19ok/7changed/0failed. Domainv.slnnk.com
and old relay's Vault SID are stored in new host_vars after explicit repo gate approval.
Pinned HTTPS200/TLS0 and authenticatedHTTP2/HTTP3 both passed with German egress.
German access log confirms new-relay ACME forwarding. No certificate/backend changes.
At00:51:25MSK old dline-spb-01 agent was stopped and poweroff returned0; subsequentSSH
unreachable, provider-panel power state not observed. Do not run old SID collection if
the retired host is powered on again. HetrixTools already reports new hostname/metrics.
At deployment Cloudflare DNS saw new A/noAAAA while Google/monitor still cached old IP.
User subsequently confirmed HetrixTools UP; operational migration follow-up is closed.
Every recursive DNS cache was not rechecked; no extra changes requested.
Earlier old-relay/current-provider-selection sections are historical and superseded.
See [deployment and approval evidence](../log/2026-11-13-trusttunnel-de-simplecloud-relay-migration.md).

Post-migration DOWN recurred at01:21:55–01:26:40MSK (285seconds), then recovered UP in all four locations. New-relay pinned HTTPS200/TLS0 and SSH/service health passed; stale old resolve_address and mixed diagnostic IPs support residual DNS caching. No remote changes; see the migration log for evidence.

## Replacement hosting research, 2026-11-13

Historical comparison used budget200–400RUB/month. IHOR/AdminVPS/FirstByte proposals
were withdrawn after the user's order-flow availability corrections. User then selected
SimpleCloud and explicitly authorized the migration, old-relay shutdown and SID transfer;
those requested operations are now verified as described above. Search and destination
selection are resolved. See [research history](../log/2026-11-13-trusttunnel-de-hosting-shortlist.md)
and [migration outcome](../log/2026-11-13-trusttunnel-de-simplecloud-relay-migration.md).

## Current availability after authorized reboot, 2026-11-12

User reported a panel forced reboot; read-only verification at23:55:50 confirmed a new
bootID, `qxl.modeset=0`, no QXL driver bound, and persistent `sr0` polling0. SSH/nginx
active, failed units0, relay HTTPS200/TLS0. Earlier total-unreachable status below is
superseded by this recovery. HetrixTools recovered UP in all four locations at23:56:35.
New-boot journal has21sAHCI/SATA reset and87sUSB/runtime-PM lockups at23:54:14 despite
QXL disable; no later lockup through23:56. This does not prove identical causality to
prior runtime freezes. Host/QEMU versus guest-kernel cause unresolved; recurrence
assessment was subsequently stopped by user decision: user prefers changing provider rather than further diagnostics. Migration planning is a proposal in central TODO; no destination or deployment authorization. No further agent reset or remote changes.
See [verified outcome](../log/2026-11-12-trusttunnel-de-proxy-kernel-stall.md#access-recovered-and-boot-settings-verified).

## Relay kernel stalls, 2026-11-12

At 15:58 Moscow both hosts and HTTPS monitors were healthy. Neither VM rebooted today.
Relay monitor outages at 15:37–15:42 and 15:43–15:52 coincided with guest kernel
soft lockups, RCU starvation and systemd watchdog recovery. German VPN service
remained active with no recorded downtime today. Current load/resources and direct/relay
HTTPS checks were normal. Kernel versus provider/hypervisor cause is unresolved;
no remote changes were performed. See [diagnostic evidence](../log/2026-11-12-trusttunnel-de-proxy-kernel-stall.md).

Evening recurrence: relay outage 23:19:51–23:21:34 Moscow (103 seconds) coincided
with a 77-second CPU0 soft lockup in disk/CD-ROM polling and monitoring-agent timeout.
At 23:22 nginx had not restarted; relay/direct HTTPS returned200 with valid TLS.
Both monitors were UP, with New York still listed as failing for the relay in the
latest snapshot. Root cause remains unresolved; no remote changes or repair proposed.

Deep read-only follow-up found five lockups: four CD-ROM stacks and one QXL stack,
all at interrupt restoration. QEMU/KVM execution/emulation stalls are the leading
hypothesis; CD-ROM alone is not established as the cause. Low pre-outage guest load,
post-daytime steal14.17%, missing agent samples, and the482.838-second timer gap support
host investigation but do not prove a specific host defect. All four monitor locations
later recovered. Exact cause remains open in central TODO, pending host/provider data;
support-request draft exists locally, not sent. No remote changes.

At23:32:14 Moscow the user-approved temporary `/sys/block/sr0/events_poll_msecs=0`
was applied; independent readback at23:32:27 confirmed0. Nginx remained active without
restart; two relay HTTPS checks200/TLS0; monitor UP in all four locations. New outage
23:28:55–23:31:28 preceded the change and included both QXL and CD-ROM stacks.
Recurrence assessment remains pending; no persistent setting or reboot. QXL boot-time
disable is only a proposed next experiment, not authorized or performed.

Observation superseded by recurrence: at23:42:01 `sr0` polling still0, but QXL
lockups41/53seconds and anRCU stall occurred after the change. HetrixTools outage
23:40:48–23:41:35; relay HTTPS later200/TLS0 and nginx active/no restarts. CD-ROM
disable alone is insufficient. QXL boot-disable is the next proposed test, still
unapproved; exact QXL-versus-hypervisor cause remains unresolved. See diagnostic log.

## Russian nginx relay deployed, 2026-11-09

Latest outcome: separate tt.slnnk.com TLS support has been approved and deployed
on Germany (`ok18 changed5 failed0 unreachable0`). Both main_hosts and separate
certificate lineages are active; original v certificate is unchanged. tt's
certificate expires 2027-02-06 22:23:39 UTC and has webroot renewal configured.
Pinned HTTPS checks returned HTTP200/valid TLS for tt direct, v direct and v
through Russia. Both HetrixTools monitors are now UP. The failure and pending
preparation statuses below are historical and superseded by this outcome.
Subsequent home Wi-Fi reconnection and approved LE renewal checks passed, as
recorded below. On 2026-11-11, the user also confirmed the phone VPN works
through cellular data; the remaining client check is complete in central TODO.

Phone-path log check at02:29 Moscow found recent Android TrustTunnel sessions
direct to Germany (household public egress, not Russian relay IP), SNI v.slnnk.com.
No iOS-labelled sessions appeared in the inspected tail. This does not establish
phone relay cutover; DNS/client caching is only a hypothesis. See the relay log.

Latest HetrixTools check (02:11 Moscow): vpn-proxy UP with nginx online and fresh
Russian host metrics. German monitor vpn now targets tt.slnnk.com and is DOWN
in all four locations due to TLS handshake failures, while its agent reports
TrustTunnel/nginx online. Pinned checks on the same German IP confirm tt TLS
failure and v.slnnk.com HTTP200/valid TLS. Dedicated tt hostname/certificate
configuration is proposed, not applied; see central TODO and the relay log.

After user approval, local role preparation for tt is complete:
trusttunnel_additional_domains now supports independently named certificates,
and German host vars add tt.slnnk.com while retaining v.slnnk.com. Syntax,
offline certificate/template checks and remote check-mode passed (ok15,
changed4, failed0). Google/Cloudflare resolve tt to Germany with no AAAA.
Actual certificate issuance and config deployment await explicit approval;
the live TLS-host limitation and monitor DOWN remain unresolved at this stage.

After explicit approval, `playbooks/vpn-proxy.yml --limit dline-spb-01` completed
with `ok=80 changed=45 failed=0 unreachable=0`. Relay nginx, SSH, rsyslog,
nftables, CrowdSec/bouncer and monitoring timer are active. Both TCP/443 and
UDP/443 are forwarded to Germany, and HTTP ACME requests reach the German
nginx. TLS stays end to end; no certificate or Certbot was installed in Russia.

Pinned HTTPS `/tt_ping` returned 200 with verified TLS. Temporary authenticated
TrustTunnel HTTP/2 and HTTP/3 SOCKS probes returned German egress 152.234.226.70.
These local probes used the pre-existing VPN route to Russia; direct home/mobile
reachability is not established. HetrixTools `vpn-proxy` reports the Russian IP,
hostname, nginx online and repeated samples. At deployment time website probes
still checked Germany through unchanged DNS; subsequent user cutover is recorded
below. No monitoring-policy changes.

The nonfatal sudo hostname-resolution warning was subsequently fixed with the
user's hosts-only approval: added `127.0.1.1 dline-spb-01` to /etc/hosts using
the same parameters as the prepared common-role fix. getent and sudo checks
passed without the warning; nginx and the monitoring timer remain active.
Locale normalization was not applied. DNS propagation, client checks and actual
LE renewal validation remain pending in [central TODO](../../../TODO.md).
See [deployment evidence](../log/2026-11-09-trusttunnel-de-russian-nginx-relay-role.md#deployment-approved-and-verified-2026-11-09).
Historical preparation/preflight statuses below are superseded by this section.

User subsequently changed v.slnnk.com A to 48.103.180.18. Both REG.RU
authoritative servers confirmed the new A with TTL86400 and no AAAA. Google,
Cloudflare and ordinary local HTTPS still used the cached German IP during
verification; propagation is incomplete. The PC client already connects by
domain, so no fixed-IP edit is required. Home/mobile reconnection and an approved
Certbot renewal test remain pending. The agent did not change DNS.
After a user-requested local DNS cache flush, resolvectl on the PC returned
48.103.180.18 for v.slnnk.com. The VPN still needs reconnection and path
verification; no client configuration change was made by that cache operation.
Subsequent phone test at02:35 Moscow confirmed Android traffic arriving in
Germany from the Russian relay IP, with paired nginx TCP443 connections on the
relay. The phone path now works through Russia; Wi-Fi versus mobile data was
not specified by the user. Earlier direct-phone observations are historical.
At02:39 Moscow, fresh Linux sessions also reached Germany from48.103.180.18,
confirming PC relay use after reconnection. User clarified the phone test used
Wi-Fi. At02:44, the approved v.slnnk.com Certbot staging renewal succeeded;
seven matching HTTP200 challenge requests on Russia/Germany confirm the full
relay validation path. The production certificate fingerprint/validity and
TrustTunnel activation time were unchanged; both monitors stayed UP. Manual
dry runs should include --no-random-sleep-on-renew to avoid the observed
444-second Certbot delay. Cellular-data testing was pending at that time;
the user confirmed success on 2026-11-11. See the relay log's
[cellular test outcome](../log/2026-11-09-trusttunnel-de-russian-nginx-relay-role.md#phone-cellular-test-confirmed-2026-11-11).

## Russian nginx relay prepared locally, 2026-11-09

User selected client -> nginx in Russia -> public TrustTunnel IP in Germany, without IPsec. User created `playbooks/vpn-proxy.yml` and group `vpn_proxy`, then authorized local role preparation on existing `master`/`b857c7e`. Added `roles/trusttunnel-proxy`, relay group/host vars and repo architecture guidance. Local inventory target is `dline-spb-01` (`48.103.180.18`), backend derived from `it-garage-de-01` (`152.234.226.70`). TCP/UDP 443 are passed through; HTTP ACME requests go to Germany with the TLS hostname as Host. Certificate and renewal automation remain in Germany.

Both functional playbooks passed syntax checks. Isolated nginx tests passed TCP, UDP, ACME and redirects; no authenticated client or remote host test. Instruction lint has no errors and one existing missing-reference warning. The user subsequently supplied the relay SID and authorized encrypting it in `inventory/host_vars/dline-spb-01.yml` using the existing Vault password; persisted decryption and proxy playbook syntax passed. Agent deployment and monitor association/telemetry remain unverified. Deployment/DNS remain a separately approved proposal in [central TODO](../../../TODO.md). See [implementation and verification](../log/2026-11-09-trusttunnel-de-russian-nginx-relay-role.md).

Later deployment preflight confirmed `dline-spb-01` runs Debian 13.4 x86_64.
Backend TCP/80, TCP/443 and validated TLS `/tt_ping` succeeded from Russia;
UDP/QUIC is not yet verified. Ports 80/443 on the relay are free. Minimal-image
sudo and rsyslog prerequisites were added locally to bootstrap/CrowdSec roles;
both playbook syntax checks passed. No server changes or DNS switch; the full
relay playbook deployment remains pending explicit approval. See the relay log.

## Russian relay provider research, 2026-11-09

Discussion only: a Russian nginx stream relay could use cross-country private connectivity to a foreign endpoint. Timeweb documents custom routed networks across countries; its standard cloud VPC is within one location. Suitability and price for two small VMs remain unconfirmed. No purchase, outreach or deployment. See [provider research](../log/2026-11-09-trusttunnel-de-russian-relay-provider-research.md).

## TrustTunnel upgraded to 1.1.0, 2026-11-08

After separate approvals for local edits and deployment, updated the Ansible
version default and README from 1.0.33 to 1.1.0. Syntax validation passed.
The focused playbook targeted `it-garage-de-01` with `--skip-tags upgrade`,
skipping apt package changes: `ok=21 changed=7 unreachable=0 failed=0`.
The restart handler completed. Read-only checks confirmed binary version `1.1.0`,
systemd `active/running`, TCP/UDP 443 listening, and external HTTPS `/tt_ping`
HTTP 200 with successful TLS verification. No authenticated client session or
second mutating run was performed. No commit/push or task background operations.
See [upgrade and approval evidence](../log/2026-11-08-trusttunnel-de-upgrade-1-1-0.md).

## HetrixTools warning policies active, 2026-11-08

After approval of the concrete values, enabled CPU >=90 percent, RAM >=90 percent
and disk `/` >=85 percent (each averaged over five minutes), agent silence over
five minutes and service-down alerts for `trusttunnel`/`nginx`. Each repeats every
30 minutes and explicitly uses `Contacts` (email and Telegram). A separate API
read-back verified all saved values and targets. No deliberate failure test or
new test notification was sent; earlier Telegram delivery was user-confirmed.
See [approval and verification](../log/2026-11-08-trusttunnel-de-hetrixtools-ansible.md#warning-policies-enabled-and-verified-2026-11-08).

## HetrixTools agent deployed, 2026-11-08

After explicit user approval, the focused Ansible playbook installed agent
`2.4.2` on `it-garage-de-01` (`ok=17`, `changed=8`, `failed=0`). The enabled
`hetrixtools_agent.timer` collects every minute as user `hetrixtools`; both
TrustTunnel and nginx remain active. HetrixTools MCP confirmed repeated metric
snapshots and both monitored services `online`. Configuration-only check mode
reported `changed=0`, `failed=0`; a second full mutating run was not performed.

Resource and service-down warnings were disabled at deployment; the subsequent
approved policy configuration above supersedes that state. See [deployment evidence](../log/2026-11-08-trusttunnel-de-hetrixtools-ansible.md#deployment-authorized-and-verified-2026-11-08).
No task background commands remain; the timer is the intended recurring service.

## HetrixTools agent Ansible role prepared, 2026-11-08

Reusable local role `roles/hetrixtools` downloads agent `2.4.2` from the versioned
upstream URL, templates private configuration and schedules it every minute with
`hetrixtools_agent.timer`. It defaults to user `hetrixtools`; root, services,
interfaces, connection ports and optional collectors are configurable. Unique
SID is Vault-encrypted in host vars; `vpn` group selects `trusttunnel` and `nginx`.
Both `playbooks/vpn.yml` and focused `playbooks/hetrixtools.yml` include the role.
The existing Vault password is `ANSIBLE_VAULT_PASSWORD` in `personal/.env`.

Local syntax, Vault, template/parser and validation checks passed; repeated
template application reported no changes. Instruction lint had zero errors and
one `CDX-AG-005` warning in repo `AGENTS.md`. No server deployment or publication
was performed at this initial stage. The subsequent deployment above supersedes
this status; live metrics are verified, while full mutating rerun idempotency is not.
See [implementation and approval evidence](../log/2026-11-08-trusttunnel-de-hetrixtools-ansible.md).

## HetrixTools MCP configured in Codex, 2026-11-08

At the user's request, added local Codex server `hetrixtools` in
`~/.codex/config.toml`: Streamable HTTP URL `https://mcp.hetrixtools.net`,
header helper `python3 /home/slnnk/ai/personal/scripts/hetrixtools_mcp_headers.py`,
startup timeout 30 seconds and tool timeout 60 seconds. The helper reads only
`HETRIXTOOLS_API_KEY` from `personal/.env` and emits the `api-key` header to
Codex; never run it with stdout exposed in chat or logs. No secret is stored
in the config or helper. `default_tools_approval_mode = "writes"` preserves
confirmation for tools not annotated read-only. Existing per-command external
change approval rules still apply. A User-Agent header was configured after
an initial urllib MCP handshake without one returned HTTP 403.

Codex CLI 0.167.0 recognized the enabled configuration and its header helper.
A direct MCP protocol smoke check initialized server `hetrixtools` 0.6.0,
negotiated protocol `2025-03-26`, listed 48 tools, and called read-only
`list_uptime_monitors`: `vpn` was `up` and `active`, target
`https://v.slnnk.com/tt_ping`, SSL expiry `2027-02-05`.
No HetrixTools settings or monitors were modified during that initial check.
The initial conversation catalog had not reloaded; native adoption was pending.

Native adoption verified later on 2026-11-08 in a fresh conversation: all 48
`mcp__hetrixtools__*` tools are present. Native calls to `get_api_scope`,
`list_uptime_monitors`, `get_server_agent_metrics` and
`get_server_agent_warning_policies` all succeeded. Monitor `vpn` is `up` and
`active`, target `https://v.slnnk.com/tt_ping`; agent `2.4.2` reports
`trusttunnel` and `nginx` online. Warning read-back confirms the approved
CPU/RAM 90 percent, root disk 85 percent, five-minute windows and agent-silence
threshold, service alerts and 30-minute repeats. The adoption item in the
[central TODO](../../../TODO.md) is complete. Only read operations were tested;
mutating tools were not exercised. No task background process remains.
Report-only agent lint passed: 9 files, 0 errors, 0 warnings, 0 info.

Sources: [HetrixTools connection guide](https://docs.hetrixtools.com/hetrixtools-mcp-connection-guide/)
and [official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).

## HetrixTools monitoring and API access, 2026-11-08

The user created an external website monitor and added `HETRIXTOOLS_API_KEY`
to `personal/.env`. Read the key only from that file and pass it as the Bearer
token in the Authorization header to `https://api.hetrixtools.com/v3/`.
Never print the key or put it in command arguments, notes or request URLs.

A read-only `GET /uptime-monitors` returned HTTP 200 with one monitor:
`vpn`, target `https://v.slnnk.com/tt_ping`, type `website`, monitor status
`active`, accepted HTTP codes `[200]`, locations New York, Amsterdam,
Frankfurt and Warsaw. The API reports SSL expiration date `2027-02-05`.
This confirms authentication and monitor-list access, not write permissions,
notification delivery or configured certificate-expiration reminders. No
external settings were changed. The official API specification URL returned
HTTP 403 during discovery; the API request itself succeeded. All checks exited.

## Client migration confirmed, 2026-11-08

Following server deployment on `v.slnnk.com`, the user confirmed:
`Клиенты проверил - работает`. Client operation is user-confirmed; no additional
agent client edits, VPN sessions or remote checks were performed. The remaining
client migration task in the [central TODO](../../../TODO.md) is closed.
The own-domain migration is complete; no task background operations remain.

## Certificate ordering fixed locally, 2026-11-08

The user requested fixing the previously proposed certificate ordering issue.
Proposal: reuse `/home/slnnk/mygit/ansible`, branch `master`, base `b857c7e`,
change role task ordering and README, and syntax-check both VPN playbooks.
The user explicitly approved with `Да`. The implementation moves binary
installation and service configuration rendering after certificate issuance,
so neither can enqueue a TrustTunnel restart before the nginx handler flush.
Existing task bodies and tags are preserved. Updated the role README to explain
hostname migration, failure behavior and focused installation/configuration runs.

Both `playbooks/trusttunnel.yml` and `playbooks/vpn.yml` syntax checks passed.
A local YAML inspection verified ordering and absence of TrustTunnel restart
notifications before certificate issuance, plus role-wide tags on all tasks.
No new-domain runtime migration was performed for this code fix; the already
working server was left unchanged. No commit, push or publication was performed.
This completed the role ordering proposal. Client migration was subsequently
confirmed by the user above and is closed in the [central TODO](../../../TODO.md).

## Own domain deployed, 2026-11-08

After Google and Cloudflare DNS-over-HTTPS both returned `152.234.226.70`
for `v.slnnk.com`, the user authorized deployment with `Сделай` in response
to the proposed role application and certificate issuance.

Read-only preflight confirmed TrustTunnel and nginx active, nginx serving
the existing ACME webroot `/data/webroot`, and no new-domain certificate.
Role inspection found that `meta: flush_handlers` restarts TrustTunnel after
rendering the new TLS paths but before initial certificate issuance. To avoid
restarting with missing certificate files, one temporary playbook
`/tmp/trusttunnel-domain-migration.yml` first issued the certificate using
the existing nginx webroot (guarded by `creates`), then ran the existing
role with `--tags trusttunnel-config`. No role-code changes were made.
The temporary playbook syntax check passed. The authorized execution completed
with `ok=17 changed=5 unreachable=0 failed=0 skipped=2`.

Post-deployment verification: external HTTPS to `v.slnnk.com/tt_ping` pinned
to `152.234.226.70` returned HTTP 200 and certificate verification result 0.
TrustTunnel, nginx and `certbot.timer` are active. Certificate CN and SAN are
`v.slnnk.com`, expiry `2027-02-05 22:00:59 UTC`. This verifies server HTTPS,
not an authenticated client VPN session. PC and phone client configurations
were not modified by the agent. All agent commands exited. Client operation was
subsequently confirmed by the user above; both migration and the local role
ordering fix are closed in the [central TODO](../../../TODO.md).

## Own domain prepared locally, 2026-11-08

The user purchased `slnnk.com`, configured an A record for `v.slnnk.com`,
reported propagation still pending, and requested local Ansible preparation.
Proposal: reuse `/home/slnnk/mygit/ansible`, current branch `master`, base
`b857c7e`, and change only `inventory/host_vars/it-garage-de-01.yml` from
`152.234.226.70.nip.io` to `v.slnnk.com`. The user approved with `Да`.
The proposed one-line edit was applied; the server address remains
`152.234.226.70`. Full VPN playbook syntax check passed using the repository
venv. The initial sandbox run could not create `~/.ansible/tmp`; the same
syntax check passed with approved escalation.

At the preparation stage, no DNS propagation check, deployment, certificate issuance, client edit,
staging, commit, push or publication was performed. Last user-confirmed working
VPN configuration uses the nip.io name. After DNS propagation, deploying the
role for the new domain and updating clients were pending and required their
respective authorization; see Personal / TrustTunnel endpoint in the
[central TODO](../../../TODO.md). Existing untracked repository files were preserved.

## Address replacement and recovery, 2026-11-08

The user reported that the old address `2.26.30.176` was blocked and a new
address was issued. They updated Ansible and applied the role, then explicitly
confirmed VPN works. Local `inventory/hosts` now has
`ansible_host=152.234.226.70`; `inventory/host_vars/it-garage-de-01.yml` has
`trusttunnel_domain: 152.234.226.70.nip.io`. These files were read on 2026-11-08.
Recovery and blocking are user-reported; the agent did not independently verify
the new endpoint, the deployment, or the exact filtering mechanism. Further
old-address UDP capture and provider/path investigation are closed without
execution following recovery. No server or Ansible changes were made by the
agent in this update. See the [incident resolution](../log/2026-11-06-trusttunnel-de-inbound-unreachable.md#resolution-2026-11-08).

## Inbound access incident, 2026-11-06

Historical diagnostics for the old address; superseded by recovery above.

The user reports VPN failure on PC and phone. From the PC, DNS returns the
expected `2.26.30.176` and the endpoint route bypasses the corporate VPN, but
direct TCP 22/80/443 probes time out and ICMP receives no replies. A user-provided
VNC screenshot shows the VPS interface up and successful outbound pings to
`8.8.8.8`. Later VNC output confirms active TrustTunnel, SSH, nftables, CrowdSec
and bouncer services; TCP 22/80/443 and UDP 443 listeners; and runtime input rules
allowing those ports and ICMP. CrowdSec source blocking precedes these rules.
The user-authorized alternative gateway reaches the VPS by ping with 0% loss,
but TCP 22/443 still times out. Correlated VNC capture shows that gateway's ICMP
requests and replies, but no TCP; a later gateway capture confirms SYN egress
and retransmissions. Control TCP/443 to another public endpoint succeeds.
The tested TCP path fails before the VPS interface capture; the exact upstream
loss point and provider/transit filtering cause remain unconfirmed. Provider/path
investigation is proposed; SSH to the VPS has not succeeded. No remote
changes were made. These observations supersede the earlier access-health
snapshot, not the documented configuration. See the
[incident log](../log/2026-11-06-trusttunnel-de-inbound-unreachable.md) and
[central TODO](../../../TODO.md), Personal / TrustTunnel endpoint.

Subsequent UDP/443 QUIC Version Negotiation probes received no reply from the
VPS from either source (three attempts each), while the same probes to
`1.1.1.1:443` returned valid matching QUIC responses from both sources.
UDP service reachability is not confirmed; packet arrival at the VPS remains
unverified pending a user VNC capture with ICMP control. All agent probes exited.

## Staleness review (2026-11-04)

Reconciled with the current local Ansible defaults and VPN playbook and the [2026-11-04 server cleanup verification](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md). TrustTunnel remains the configured VPN; StrongSwan is absent from both active Ansible configuration and the recorded VPS state. The latest recorded service checks show TrustTunnel, nftables, nginx and the CrowdSec bouncer active, with the shared certificate and TrustTunnel renewal hook retained and HTTPS `/tt_ping` returning HTTP 200. The [user confirmed iPhone TrustTunnel on 2026-11-02](../log/2026-11-02-vpn-gateway-strongswan-ansible.md); no new iPhone session or server probe was performed during this review. Use `.ansible-venv/bin/ansible-playbook` from the repository root for the delivery commands below.

The original Ansible snapshot was recorded on 2026-09-26. Later dated sections
record deployment and service checks; the current documented state was reconciled
on 2026-11-04, with verification limits stated below.

## Purpose

Self-hosted TrustTunnel VPN endpoint in Germany for the user's phone, PC and family.
Planned to also serve the home router (see [home-network](home-network.md)).

## Components

- Host `it-garage-de-01`, `ansible_host=152.234.226.70`, group `vpn`.
- Global IPv6 `2a0d:d940:1a:9d0::2/64` on `ens3`, observed in user VNC output
  on 2026-11-06. IPv6 SSH could not be tested from the PC or the authorized
  alternative gateway because both lack an IPv6 route (`Network is unreachable`).
- Domain `v.slnnk.com` (deployed and HTTPS verified; `inventory/host_vars/it-garage-de-01.yml`,
  `trusttunnel_domain`). Certificate from Let's Encrypt via host `certbot`, webroot on
  nginx port 80. Hypothesis: a real domain is preferable; nip.io depends on a third party.
- TrustTunnel `1.1.0`, binary `/usr/local/bin/trusttunnel_endpoint`, configuration under `/data/trusttunnel`, systemd service, listens `0.0.0.0:443`
  TCP and UDP (QUIC on), forward mode `direct`, log `/var/log/trusttunnel.log` at level
  `debug`, metrics disabled.
- Three client accounts in `inventory/group_vars/vpn.yml` (`trusttunnel_clients`):
  `slnnk`, `aleshka`, `family`. Passwords are plaintext in the inventory; moving them to
  Ansible Vault is an open TODO of that repository.
- Firewall nftables: base rules from `group_vars/all.yml` plus 80/tcp, 443/tcp, 443/udp
  from `group_vars/vpn.yml`. CrowdSec installed.

## Delivery path

`cd /home/slnnk/mygit/ansible && .ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/vpn.yml`
(roles `ansible-user`, `common`, `nftables`, `sshd`, `crowdsec`, `trusttunnel`).
Role docs: `roles/trusttunnel/README.md`. Syntax check with `--syntax-check` first.

## Control points

- `systemctl status trusttunnel`, `nginx`, `certbot.timer`; deploy hook restarts
  TrustTunnel on certificate renewal.
- Health paths: `/tt_ping`, `/tt_speed` on the domain.

## Operations

- Add a client: append to `trusttunnel_clients`, run the playbook (state change on the
  VPS, needs the user's confirmation).
- Client config on the PC: `/home/slnnk/trusttunnel/trusttunnel_client.toml`, run script
  `run-trusttunnel.sh` (sudo).

## Boundaries

Separate from the StrongSwan VPS `91.218.141.22` ([vpn-gateway](vpn-gateway.md)).

## Access

SSH as the ansible user created by role `ansible-user`; keys from
`inventory/group_vars/all.yml`. Client passwords: inventory file only, never in notes.

## Related log entries

- [2026-09-26 home network plan](../log/2026-09-26-home-network-initial-plan.md)

## Local PC client routing adjustment

On2026-10-11 the local PC client configuration received an explicitly authorized corporate OpenVPN endpoint exclusion; the TrustTunnel server itself was unchanged. Client exclusion activation verified after user restart; corporate VPN reconnected and controlled Nexus transport verification passed; browser symptom confirmation pending. See [client routing log](../log/2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md).

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.

## StrongSwan local preparation, 2026-11-02

The local Ansible checkout now also defines `roles/strongswan` and
`playbooks/strongswan.yml` for IKEv2/EAP-MSCHAPv2 on this host. It reuses the
TrustTunnel certificate; `vpn.yml` runs it after TrustTunnel. The nftables role
owns authenticated IPsec forwarding and IPv4 NAT, with UDP 500/4500 added in
VPN inventory. Client credentials are now encrypted as `vault_strongswan_clients` in
`inventory/group_vars/vpn-vault.yml`, passed explicitly with `-e @...`. The Vault
password is `ANSIBLE_VAULT_PASSWORD` in `~/ai/personal/.env`. Deployed on 2026-11-02 by explicit user request; StrongSwan and TrustTunnel
verified active together, IKEv2 connection loaded, UDP 500/4500 listening,
and IPv4 forwarding/NAT active. Live iPhone verification remains pending. See [preparation log](../log/2026-11-02-vpn-gateway-strongswan-ansible.md)
and the central TODO under Personal / StrongSwan endpoint.

## iPhone client authentication, 2026-11-02

TrustTunnel and StrongSwan have independent credential lists. The current
StrongSwan account shares a username with an existing TrustTunnel account but
uses a different password. The inventory `trusttunnel_clients` credential was
verified against the running server without exposing values. Recent iPhone
reconnection diagnostics found authentication failures; the user subsequently corrected the password and confirmed on 2026-11-02
that TrustTunnel works on iPhone. The corresponding central TODO is closed. See the
[diagnostic log](../log/2026-11-02-vpn-gateway-strongswan-ansible.md).

## StrongSwan Ansible removal, 2026-11-04

The user chose TrustTunnel on iPhone and retired StrongSwan from local Ansible. The role, playbook, dedicated Vault file, inventory settings and IPsec firewall/NAT additions are removed; previous StrongSwan preparation and deployment sections are historical. TrustTunnel settings remain unchanged. IKEv2 verification is cancelled in the central TODO. No VPS changes were made, so the deployed service and related server files may remain. See the [removal log](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md).

## StrongSwan server removal, 2026-11-04

After a separate user request and explicit approval of the cleanup command, StrongSwan was also removed from the VPS. Its service, eight packages, credentials, chain copies, renewal hook, persistent sysctl file and IPsec firewall/NAT rules are absent; IPv4 forwarding is disabled. This supersedes the local-only removal limitation above. TrustTunnel, nftables, nginx and CrowdSec bouncer are active; the TrustTunnel renewal hook and shared certificate are preserved. HTTPS `/tt_ping` returned HTTP200. No actual iPhone session tested in this cleanup. See the [removal log](../log/2026-11-04-vpn-gateway-strongswan-ansible-removal.md).
