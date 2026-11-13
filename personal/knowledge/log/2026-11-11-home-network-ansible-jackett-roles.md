---
system: home-network
status: verified
checked: 2026-11-11
tags: [ansible, jackett, flaresolverr, docker]
---
# Home network: Docker and Jackett Compose Ansible roles

## Task

Prepare local Ansible roles for the remote Jackett/FlareSolverr search service. The user specified exactly two roles, `docker` and `jackett`; the latter renders `docker-compose.yml` for both containers. Functional playbook must be named `jackett` and apply the default/base roles plus Docker and Jackett. The user is still filling inventory and the new machine has not started.

## Context

Repository `/home/slnnk/mygit/ansible`, existing checkout `master`, base `master` at `b857c7e`. Existing project instructions, inventory, playbooks and roles were mostly untracked before this task; preserve them and do not stage unrelated material. `inventory/hosts` already contains group `jackett` and host `dline-pl-01` with empty `ansible_host`. No target address or remote deployment was inferred.

Native installation is possible upstream, but Chromium dominates FlareSolverr memory regardless of Docker. A dedicated 1-vCPU/1-GB server was accepted as a trial for rare personal searches, with real browser memory measurements needed; no automatic swap or resizing was authorized.

## Actions

Initial proposal specified the local repository, reusing current `master` from `master` (`b857c7e`), and container-based deployment. The user then explicitly instructed `docker` + `jackett` roles and `jackett` playbook, reported the partially entered host, and said `Продолжи`. Continued in that previously proposed checkout/branch with the user-specified scope. No Git mutations, staging, commit or publication.

Inspected existing functional playbooks and base roles. Found nftables flushes the ruleset and drops new forwarding, so selected Linux host networking rather than changing firewall policy or relying on broken Docker bridge NAT. Announced this architecture before implementation. FlareSolverr binds loopback; Jackett defaults to loopback and external access is opt-in. Added that convention to repository `AGENTS.md` as required locally.

Implemented the two roles and Compose template, base-role functional playbook, role READMEs, and `community.docker` dependency. Installed community.docker 5.4.0 locally for validation; the sandbox DNS failure was retried with approved network escalation. No target service, firewall, inventory or container was changed. Compared inventory hashes before and after: all six files unchanged.

## Findings

- `docker`: official stable apt repository, Docker CE/containerd/Buildx/Compose plugin, service enabled; rejects conflicting distro runtimes rather than removing their workloads. Debian/Ubuntu x86_64 only, no architecture maps or daemon/firewall overrides.
- `jackett`: `/opt/jackett/docker-compose.yml`, pinned Jackett `v0.24.3042-ls32` and FlareSolverr `v3.5.2`, persistent private config, dedicated runtime account, log rotation, restart `unless-stopped`, solver scratch tmpfs cap 256 MiB (not reserved RAM).
- Managed JSON settings preserve API key, admin password hash, proxy and unknown options. Read/write tasks suppress secret output and diffs. Compare decoded objects to avoid whitespace-induced restarts. Jackett generates its first API key upstream; no plaintext credential introduced.
- FlareSolverr is `127.0.0.1:8191`; Jackett is `127.0.0.1:9117` by default, CORS true. No public listener, HTTPS proxy, certificates, port exceptions, tracker account migration or swap setup is implied.
- Functional playbook: `ansible-user` bootstrap, then `common`, `nftables`, `sshd`, `crowdsec`, `docker`, `jackett`, `hetrixtools`. Monitoring needs the new host's unique Vault-encrypted SID before deployment.

Validation: playbook syntax passed; list-hosts resolves only `dline-pl-01` in both plays. Real Compose rendering and `docker compose config --quiet` passed without daemon changes. A localhost Ansible smoke test (nine tasks, zero changes/failures) exercised the actual merge expression with synthetic credentials, unknown fields, a fresh config and a second semantic no-op. No live service deployment or target check-mode run occurred.

Required agent instruction lint: 10 files, zero errors, one CDX-AG-005 warning at repository `AGENTS.md:45`. Direct diagnostic identifies the pre-existing generic `defaults/main.yml` example as a missing relative file; the unchanged sentence is present in the pre-task snapshot. An earlier progress update incorrectly called this a size warning; the direct diagnostic corrects that interpretation. No unrelated instruction fix was applied.

## Changes

- New `roles/docker/tasks/main.yml`, `roles/docker/README.md`.
- New `roles/jackett/defaults/main.yml`, `tasks/main.yml`, `handlers/main.yml`, `templates/docker-compose.yml.j2`, `README.md`.
- New `playbooks/jackett.yml`.
- Updated `requirements.yml` and repository `AGENTS.md` only in the task scope.
- Generated baseline hashes, Compose rendering and synthetic validation under `/home/slnnk/ai-data/ansible-jackett/` outside Git.

## Status and risks

Subsequent outcome2026-11-13: the actual approved remote attempt used `dline-de-01` and `ext.slnnk.com`, then failed FlareSolverr readiness. The user cancelled VM placement and chose to plan deployment on the home server instead. Historical pending-VPS directions below are superseded; implementation and TV cutover have not run. See [final attempt and decision](2026-11-13-home-network-dline-de-jackett-deployment.md#final-outcome-and-home-server-decision) and central TODO.

Requested local implementation and checks are complete. All task commands finished; no background installer/agent or target deployment remains running. Existing local media containers from the prior TV setup were not changed. Publication and remote application remain unapproved.

The [central TODO](../../../TODO.md) tracks proposed deployment after the machine starts, `ansible_host` and the unique monitoring SID are supplied, TV/API access is chosen, and explicit runtime approval is obtained. Protect API access through an approved HTTPS proxy or explicit listener/firewall configuration before direct TV use. A 1-GB machine's actual browser memory peaks and challenge handling are not validated by syntax/rendering tests.

## Portable lesson

none

## Shared nginx architecture proposal

The user selected `tv.slnnk.com` for the future Jackett endpoint, then asked whether nginx should be extracted into a shared role, since two current service roles already manage it and Jackett would be the third consumer. This request authorizes investigation and a proposal, not the refactor, DNS changes, certificate issuance or deployment.

Read the existing nginx tasks/templates/handlers in `trusttunnel` and `trusttunnel-proxy`. The VPN endpoint uses nginx HTTP/ACME on 80 and a small page on 8080, while TrustTunnel itself owns TLS on 443. The relay uses nginx stream TCP/UDP 443 and forwards only HTTP ACME to the foreign endpoint; it must keep no local TLS certificate or Certbot. Jackett needs TLS termination at nginx with HTTP proxying to loopback 9117.

Recommended boundaries: shared `nginx` owns package/service/base includes, optional stream module, managed directory layout and the common `nginx -t` plus graceful reload handlers. Application roles retain their HTTP/stream site templates and notify the shared handler. Keep one owner of the outer stream context; the current relay file includes its own `stream` block and must be adapted deliberately if the shared role wraps the include. Manage named application configs and only known legacy/default files; do not wipe unrelated enabled sites.

Propose a separate `certbot` role for certificates, webroot issuance, renewal timer and per-certificate deploy actions. VPN renewal restarts TrustTunnel; Jackett renewal validates/reloads nginx. No certificate role on the relay. Preserve the existing certificate-before-VPN-config ordering and bootstrap HTTP/ACME before enabling any HTTPS site that references missing certificate files. Keep nginx configuration rendered by Ansible rather than asking Certbot's nginx plugin to rewrite it.

For the selected endpoint, proposed host-specific input is `jackett_domain: tv.slnnk.com`; shared group settings describe the proxy behavior and firewall ports. Planned TV path is HTTPS 443 -> nginx -> `127.0.0.1:9117`; FlareSolverr remains loopback-only. Domain selection is confirmed; DNS resolution, TLS and public access were not checked or changed. Refactor recommendation is recorded as a proposal in [central TODO](../../../TODO.md), separate from eventual remote deployment. All inspection commands finished, no repository or service changes were made for this proposal.

## Inventory-driven nginx design discussion

The user questioned application-owned nginx settings and suggested `nginx_domain`/`nginx_headers` in functional group vars. Revised the recommendation: one nginx role owns service and site configuration; inventory supplies differences, while application roles own their services. This supersedes the earlier recommendation to keep all site templates in application roles as the default design; custom site templates remain an escape hatch for unusual configurations. No implementation was requested or made in this discussion.

Reviewed official Ansible variable precedence, role argument validation, hash behaviour, nginx reload semantics, and NGINX's maintained installation/configuration role examples. Recommended small typed role inputs with `nginx_` prefixes, defaults in role defaults, group/host-specific values in inventory, separate HTTP sites and stream proxies, a few supported template types plus custom templates. Named site mappings are convenient for this repository but are an engineering choice, not an official requirement; lists also work. Mapping defaults and overrides must still be combined explicitly. Do not change global `hash_behaviour=merge`, and do not assume definitions in two peer inventory groups are automatically accumulated.

Recommended implementation checks: validate public arguments and duplicate listener/site identities, validate the complete candidate nginx configuration rather than treating a server fragment as a main config, apply a graceful reload only on changes, preserve/restore files on failed validation, and test all three consumers plus a second-run no-op. Keep Certbot webroot issuance and per-service renewal actions separate; render HTTP challenge endpoints before certificate issuance and enable HTTPS only after certificates exist. These are design proposals only; the existing central proposal/deployment entries remain the only follow-up records.

Primary references: https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_variables.html ; https://docs.ansible.com/projects/ansible/latest/reference_appendices/config.html#default-hash-behaviour ; https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation ; https://github.com/nginx/ansible-role-nginx-config ; https://nginx.org/en/docs/control.html .

## Shared roles implemented after approval

The user explicitly requested implementation. Shared inventory-driven nginx and separate Certbot roles, existing VPN/relay refactoring, and local TV HTTPS configuration are now prepared and checked. This supersedes only the earlier pending local-refactor proposal and missing HTTPS-role status; DNS, certificate issuance and remote application remain unapproved/unexecuted. See [implementation and validation](2026-11-11-home-network-shared-nginx-certbot.md). Docker/Jackett backend behavior and credential preservation remain as recorded above.
