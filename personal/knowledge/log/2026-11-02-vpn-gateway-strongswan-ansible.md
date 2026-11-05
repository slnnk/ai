---
system: vpn-gateway
status: verified
checked: 2026-11-02
tags: [strongswan, ansible, iphone, ikev2, nftables]
---
# StrongSwan alongside TrustTunnel: local Ansible preparation

## Task

Prepare minimal local Ansible changes for StrongSwan beside TrustTunnel on the current inventory host. Deployment was not authorized by this request.

## Context and approval

Repository `/home/slnnk/mygit/ansible`, existing `master`, based on the current checkout at `b857c7e`. Proposed reusing this branch and preserving existing files. User explicitly confirmed and requested implementation. Most existing configuration is untracked; no staging, commits, push or branch mutations were performed. Publication approval has not been requested or granted.

## Actions and findings

- Inventory contains one unique host, `it-garage-de-01`, address `2.26.30.176`.
- No existing StrongSwan role. Old gateway `91.218.141.22` refused SSH on port 22; no configuration or credentials recovered. Historical notes describe IKEv2/EAP-MSCHAPv2 and L2TP, but do not establish which iPhone profile was used.
- Added `roles/strongswan` using `charon-systemd`/`swanctl`, IKEv2 EAP-MSCHAPv2, forced UDP encapsulation, IPv4 pool `10.250.0.0/24`, and the existing TrustTunnel certificate for `2.26.30.176.nip.io`.
- Added focused `playbooks/strongswan.yml`, included StrongSwan after TrustTunnel in `playbooks/vpn.yml`, and added nftables UDP 500/4500, authenticated IPsec forwarding and pool NAT.
- Credentials come from `vault_strongswan_clients` via an explicitly supplied encrypted vars file; no new passwords stored. Configuration is root-only and hidden from task logs/diffs.
- Added a Certbot hook loading each intermediate certificate separately and reloading StrongSwan; updated role documentation and repository `AGENTS.md` conventions.

## Validation

Both VPN playbooks passed syntax checks with the repo-local Ansible environment. Templates rendered locally using synthetic credentials. Checked secret escaping round-trip, certificate-chain splitting, renewal cleanup, idempotency, lineage filtering, inactive-service handling, and baseline firewall rendering without an IPsec pool. Native nftables/swanctl binaries are unavailable locally; runtime parsing and an actual iPhone connection remain unverified.

Agent lint: 0 errors, 1 warning (`CDX-AG-005` at an existing public-API instruction in repository `AGENTS.md`), 2 informational findings. Initial sandbox state access failure resolved by rerunning with escalation.

## Status and risks

Local preparation and the subsequently authorized deployment are complete, as recorded below. Vaulted credentials are configured. Live iPhone verification remains tracked in the central backlog under Personal / StrongSwan endpoint. This is IPv4-only; IPv6 leak prevention is not configured. Old L2TP profiles are not migrated automatically.

## Portable lesson

none

## Vault credentials added, 2026-11-02

User identified the personal `.env` values as VPN client credentials, supplied
`ANSIBLE_VAULT_PASSWORD`, and explicitly requested adding encrypted StrongSwan
secrets to the repository. Existing approval for the same checkout and `master`
remains applicable; no Git mutation or deployment was performed.

Created `inventory/group_vars/vpn-vault.yml` with `vault_strongswan_clients` from
`STRONGSWAN_USER` and `STRONGSWAN_PASSWORD` in `~/ai/personal/.env`, encrypted using
`ANSIBLE_VAULT_PASSWORD` from that file. Plaintext and the Vault password remained
in memory; no plaintext credential file was generated. The encrypted file is mode
`0600`, AES256 Ansible Vault format. Updated the StrongSwan role README with its
location, edit command and secret source variable names.

Verified encryption/decryption equality without printing values, both playbook
syntax checks using Vault, and a local no-log assertion that inventory resolves
`strongswan_clients` to the decrypted list. The encrypted vars file must be passed
explicitly with `-e @inventory/group_vars/vpn-vault.yml --ask-vault-pass`.
The separately approved deployment and live iPhone verification remain pending
in the central TODO; providing vaulted credentials is now complete.

## Deployment completed, 2026-11-02

User explicitly requested applying the StrongSwan role to the inventory server.
Ran `playbooks/strongswan.yml` limited to `it-garage-de-01`, with the encrypted
vars file and Vault password supplied in memory from the personal `.env`.
This authorized deployment included the focused playbook's required nftables
role and its CrowdSec bouncer restart handler. No Git publication performed.

Ansible recap: `ok=22 changed=11 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0`.
The nftables validation on the server passed before installing its ruleset.
Read-only SSH checks confirmed StrongSwan, TrustTunnel and nftables are active;
StrongSwan is enabled. The `iphone` IKEv2 connection is loaded with certificate
identity `2.26.30.176.nip.io` and EAP-MSCHAPv2 authentication. UDP 500/4500 are
bound by `charon-systemd`; TrustTunnel remains bound to UDP 443. IPv4 forwarding
is 1; input rules permit both IKE ports and the existing TrustTunnel ports;
IPsec forwarding and the `10.250.0.0/24` masquerade rules are loaded.

The server certificate SAN matches the domain, with validity from
`2026-11-02 03:13:59 UTC` through `2027-01-31 03:13:58 UTC`.
No active IKE SAs existed at the verification time; no real iPhone connection
or public client-to-server UDP reachability has yet been verified. The central
TODO now retains only the iPhone connection/Internet verification step.

## Initial iPhone connection diagnostics, 2026-11-02

User reported that the iPhone could not connect and asked whether nftables was
broken. Investigated read-only; no server configuration changes or restarts.
An initial SSH connection timed out, but subsequent TCP probes to 22/80/443 and
SSH succeeded. DNS resolves the VPN domain to the inventory IPv4 address.
Active nftables rules permit UDP 500/4500; StrongSwan and TrustTunnel are active.
The journal contained configuration load messages but no real client IKE exchange.

A synchronized tcpdump and single diagnostic IKE header probe from the local
Wi-Fi network captured an inbound UDP 500 datagram and the server's outbound
reply. This confirms UDP 500 reception and application response for that source;
it does not establish all client paths or UDP 4500 reachability. The capture
contained only these two diagnostic packets, with no identifiable phone attempt.
No established SAs were present.

The user confirmed the phone uses Wi-Fi. The supplied screenshot shows IKEv2,
correct server/remote ID, empty local ID, username authentication and proxy off.
The password field appears blank; this is an observation, not proof that no
password was saved. Asked the user to enter the VPN password, save the profile,
retry, and report the VPN switch behavior. Root cause remains unconfirmed;
waiting for an actual phone attempt. Existing central TODO for live iPhone
verification remains open; deployment is still complete.

## IKE path comparison and TrustTunnel iPhone diagnostics, 2026-11-02

Further IKE tests used a valid 376-byte IKE_SA_INIT. The server answered it
locally with a 457-byte SA/KE/nonce response. From the user's network, malformed
packets of the same length reached UDP 500 and received replies, while valid
IKE requests were absent from the server capture. Equivalent non-ESP-marker
probes on UDP 4500 also passed when malformed and disappeared when valid.
This is strong evidence of content-based filtering before the server; the
responsible provider/network is not established. iPhone and Android clients
both failed, including an iPhone retry over mobile data. Safari reached HTTPS.
No server changes were made during these diagnostics.

User then installed TrustTunnel on iPhone and reported loss of Internet while
the app repeatedly reconnects. Server TrustTunnel is active with no restarts
since 07:12:31 MSK; outgoing HTTPS returned 200 on both IPv4 and IPv6. Recent
logs contain repeated `Authentication error: Authentication failed`.
Verified without printing values that the StrongSwan username also exists in
TrustTunnel but its password differs. Also verified that the inventory
TrustTunnel password matches the deployed credential. Instructed the user to
use the existing `trusttunnel_clients` password, rather than
`STRONGSWAN_PASSWORD`. Client credential correction and actual iPhone Internet
access remain unverified, tracked under Personal / TrustTunnel endpoint.
No passwords or password hashes were retained in diagnostic output.

## iPhone TrustTunnel confirmed working, 2026-11-02

User confirmed the client credential mistake and reported TrustTunnel now
works on iPhone after using the correct password. This is user-reported
successful connectivity, not an independently observed client traffic test.
The TrustTunnel iPhone verification task is complete; no server configuration
change was needed. Historical failed-authentication diagnostics above remain
as evidence. The separate StrongSwan/IKE path-filtering issue remains unresolved.

## Superseded by local removal, 2026-11-04

The user chose working TrustTunnel on iPhone and requested removing StrongSwan from Ansible. Local removal is complete; IKEv2 client verification is cancelled. Earlier deployment and diagnostics remain historical evidence. No server cleanup was performed. See the [removal log](2026-11-04-vpn-gateway-strongswan-ansible-removal.md).
