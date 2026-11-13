---
system: home-network
status: verified
checked: 2026-11-13
tags: [ansible, dns, adguard-home]
---
# Home network: VPS AdGuard Home DNS role

## Task

Prepare Ansible role dns for it-garage-de-02, already added by the user to group dns.
The final design is one VPS AdGuard Home, without Unbound or a home AdGuard instance,
serving home clients and phones on mobile networks.

## Context and approvals

Repository /home/slnnk/mygit/ansible, existing master from b857c7e. The proposal was
native systemd AdGuard Home and Unbound, base roles, shared nginx/Certbot and DoT.
User explicitly confirmed branch/base and selected d.slnnk.com. Work was paused for
discussion before repository edits. User then chose a single VPS AdGuard instance,
public DoT without client IP/ASN restrictions, and finally accepted the proposed
Cloudflare + AdGuard Unfiltered encrypted upstreams and requested continued role
preparation. This final scope drops Unbound. No publication or deployment approval
was requested or received. Existing unrelated untracked files were preserved;
inventory/hosts was not edited by the agent. No branch change, staging or commit.

## Actions

Prepared roles/dns defaults, validation/tasks, systemd and YAML templates, handler
and README; playbooks/dns.yml; group_vars/dns.yml; host_vars/it-garage-de-02.yml;
tests/test_dns_role.py; and matching architectural guidance in AGENTS.md.

AdGuard Home 0.107.80 uses its official versioned amd64 archive and upstream SHA-256
manifest. Downloaded validation artifacts are outside the repository in
/tmp/dns-role-validation. The archive hash was verified. No upstream installer ran.

Shared nginx serves only HTTP ACME, with 404 elsewhere. Shared Certbot provisions
the d.slnnk.com lineage before DNS configuration and restarts active adguardhome
only on renewal. Public DoT uses TCP853 with SNI checking. Plain DNS and other
encrypted server protocols are disabled. The admin listener is loopback3000;
access is via SSH forwarding. Firewall inventory exposes only HTTP80 and DoT853
in addition to the existing SSH policy. No Unbound, Docker or monitoring SID added.

Upstreams use Cloudflare and AdGuard Unfiltered DoH with load_balance. Ordinary
bootstrap DNS resolves upstream names; no plaintext query fallback is configured.
One local AdGuard DNS filter is enabled. A Vault-encrypted admin bcrypt hash is a
required deployment input, with validation before host mutations. No secret value
was generated for inventory or exposed in logs. Native config validation precedes
atomic replacement; service shutdown avoids runtime YAML overwrite races and
unmanaged settings are preserved. Native normalization required canonical1d/7d
retention strings to avoid repeated restarts.

## Verification

- DNS functional playbook syntax check passed; both plays target only it-garage-de-02.
- Three DNS integration tests passed using the actual0.107.80 binary: real local
  Ansible preflight/rendering and rejection of a missing secret, native config
  validation, DoT-to-DoH resolution with a loopback HTTPS fixture, local filtering,
  admin authentication, disabled plain DNS and stable runtime normalization.
- Three existing nginx rollback/idempotence tests passed.
- Agent instruction lint:0errors,1warning CDX-AG-005 at the pre-existing generic
  defaults/main.yml reference in AGENTS.md; report-only, no unrelated fix.
- No production DNS request, server connection, certificate issuance, client
  migration or systemd installation was performed. Listener checks in the role
  are not claims of end-to-end home/mobile success.

## Status and risks

Local preparation complete. Runtime deployment still requires explicit approval,
a Vault-encrypted admin hash and working public DNS/ACME reachability. Verify both
actual upstreams, public DoT and client setup during approved deployment. Public
DoT is intentionally available to third parties. Remaining work is tracked in
[central TODO](../../../TODO.md) under Home network. No background tests/services
remain after test cleanup. No publication, commit, push or infrastructure changes.

## Portable lesson

none

## Administrator credential provisioned (2026-11-13)

At the user explicit request, generated a cryptographically random 12-character
admin password and saved it only as ADGUARD_HOME_ADMIN_PASSWORD in personal/.env
(mode0600). Added its bcrypt hash as an inline Ansible Vault value in
inventory/group_vars/dns.yml, encrypted with the existing ANSIBLE_VAULT_PASSWORD
from the same private environment file. The password, hash and Vault key stayed
in memory during generation/encryption; no plaintext secret was printed or added
to repository files. Verified bcrypt matching, Vault round-trip, actual Ansible
inventory decryption for it-garage-de-02 and the private environment permissions.
README records the variable locations, never their values. The earlier missing
admin-hash prerequisite is now satisfied. No server configuration or deployment.

## Read-only deployment preflight (2026-11-13)

The user requested continuation after credential provisioning. Public A lookup for
d.slnnk.com returned31.77.132.212; AAAA lookup was empty. Strict-host-key SSH
inspection confirmed Ubuntu24.04.4 LTS x86_64,1vCPU,1967MiB RAM and16GiB free
root space. No ansible account was found. nginx, adguardhome, unbound, CrowdSec
and nftables were inactive; only SSH and loopback systemd-resolved listeners
were observed. Both chosen DoH upstreams returned HTTP200 to an example.com
DNS-message query from the VM; response payload semantics were not inspected.
No installation, restart, firewall write or certificate request was performed.
The next step is explicit approval of the functional dns.yml command, including
base packages/user/SSH/CrowdSec, nftables replacement, nginx80, Certbot issuance
and AdGuard Home853. No background probes remain.

## Deployment approved and verified (2026-11-13)

After the exact functional playbook command and its base/user/SSH/CrowdSec,
firewall replacement, HTTP ACME, certificate and DNS effects were presented, the
user explicitly approved deployment. Ran the approved command:

```sh
.ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/dns.yml --limit it-garage-de-02 --vault-password-file /tmp/dns-vault-password.py
```

The local Vault password helper contains no secret literals; it reads the existing
personal environment key and passes it to Ansible. Result:ok114 changed54
unreachable0 failed0 skipped17 rescued0 ignored0. The background execution ended.
Base roles, automation user, key-only SSH, CrowdSec/bouncer, nftables, nginx,
Certbot and AdGuard Home0.107.80 are installed. No reboot, client/router changes,
Git publication or certificate-renewal dry run was performed.

Read-only external checks confirmed trusted TLS1.3 for d.slnnk.com, certificate
expiry2027-02-11 19:36:06UTC, successful example.com A resolution over DoT and
ad.doubleclick.net blocked as0.0.0.0. Public TCP53/3000/443 were closed/filtered,
UDP53 returned no DNS response, and HTTP root returned404. Basic-auth read-only
API calls over SSH verified the generated admin credentials, protection enabled,
the two selected encrypted upstreams and an enabled local filter with191282 rules.
The runtime YAML explicitly has serve_plain_dns:false, upstream_mode:load_balance
and empty client allow/deny lists. API version output differs for those fields,
so runtime YAML/listeners were checked directly without printing credentials.
AdGuard, nginx, CrowdSec, bouncer, nftables and certbot.timer are active. Listener
inspection confirmed admin3000 is loopback-only; host systemd-resolved53 remains
loopback-only. All verification commands have exited.

### Private-panel SSH forwarding conflict

Deployment exposed an integration omission: the existing shared SSH role renders
AllowTcpForwarding no, contradicting the DNS role documented SSH-tunnel access.
The API/password works over SSH remote execution, but ordinary ssh -L is not yet
available. Current effective server config was read-only verified as forwarding no.

Prepared a local fix in the approved checkout: sshd_permit_open defaults to an
empty list; a nonempty loopback target list renders AllowTcpForwarding local plus
PermitOpen. DNS inventory supplies only127.0.0.1:3000. Default hosts remain
forwarding no/PermitOpen none; remote forwarding and other destinations remain
disabled. Added input validation, SSH/DNS README updates, AGENTS.md guidance and
tests/test_sshd_forwarding.py. Two native sshd -T tests passed with temporary test
host keys; DNS and focused SSH playbook syntax checks passed. Agent lint0errors,
one existing CDX-AG-005 warning at the generic defaults/main.yml reference.

The fix is prepared but NOT applied. The proposed separate command is:

```sh
.ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/sshd.yml --limit it-garage-de-02 --tags sshd-config --vault-password-file /tmp/dns-vault-password.py
```

This updates the SSH drop-in, validates it and reloads SSH only; it requires a new
explicit external-change approval. Follow with effective-settings and actual
tunnel checks. The current DNS service itself is live and externally verified.
Home/mobile DNS cutover remains in central TODO and is not claimed complete.
Earlier preparation-only statements in this log are historical and superseded
by this dated runtime result. No background operations remain.

## Restricted panel tunnel applied and verified (2026-11-13)

The user explicitly approved the separately proposed focused SSH-config command.
Ran playbooks/sshd.yml limited to it-garage-de-02 with tags sshd-config and the
existing private Vault password client. Result:ok8 changed2 unreachable0 failed0.
The only configuration diff replaced AllowTcpForwarding no with local and added
PermitOpen127.0.0.1:3000; native server validation passed and SSH was reloaded.

A real temporary local SSH tunnel as ansible successfully carried an authenticated
GET to the private AdGuard control/status API:HTTP200 and runningtrue. A separate
forward attempt to the already-listening loopback8081 service was rejected as
administratively prohibited, proving the destination restriction. Both temporary
SSH processes were terminated and waited for; verification and Ansible have exited.
This supersedes the earlier prepared-but-not-applied SSH-fix status. The private
panel is accessible with ssh -N -L3000:127.0.0.1:3000 ansible@31.77.132.212, then
http://127.0.0.1:3000, username admin; password stays only in personal/.env under
ADGUARD_HOME_ADMIN_PASSWORD. No password is reproduced in this note.

DNS deployment and panel tunnel are complete. Home/mobile client cutover remains
in central TODO; no router/phone configuration, Git publication or renewal dry run
was performed. No background task/tunnel remains.
