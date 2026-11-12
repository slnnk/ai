---
system: home-network
status: verified
checked: 2026-11-11
tags: [ansible, nginx, certbot, jackett]
---
# Home network: shared nginx and Certbot roles for VPN, relay and TV

## Task

Implement the inventory-driven shared nginx and separate Certbot design after the user explicitly said `Сделай` twice. Add HTTPS configuration for the selected media domain `tv.slnnk.com`, refactor existing VPN/relay consumers, and preserve their behavior. This task authorizes local code preparation, not remote deployment, DNS changes, certificate issuance or publication.

## Context

Existing checkout `/home/slnnk/mygit/ansible`, branch `master`, base `master` at `b857c7e`, already proposed in the same session and reused under the user's explicit implementation request. Most existing project files were untracked before work; no Git mutations or staging. Earlier [Docker/Jackett implementation and architecture discussion](2026-11-11-home-network-ansible-jackett-roles.md) provides the accepted design context.

VPN: nginx HTTP/80 for ACME and landing HTTP/8080, TrustTunnel TLS/443. Relay: nginx TCP/UDP 443 with HTTP ACME forwarding to the foreign endpoint, no local TLS certificate. Media host: nginx HTTPS/443 to loopback Jackett, FlareSolverr private. The inventory host entry is still being prepared by the user.

## Actions

Created a targeted snapshot of nonsecret role/playbook/instruction files in `/home/slnnk/ai-data/ansible-nginx/baseline/` and hashes of inventory before edits; existing inventory secrets were not copied into the snapshot or printed. Inspected current role templates, certificate paths and handler ordering.

Implemented shared nginx package/config/service ownership, typed arguments, named HTTP/stream dictionaries, explicit override/header merging, and a locked candidate-file transaction with complete syntax validation and restoration on failure. Retained includes for unrelated site files and limited legacy migration to explicit paths; the role owns its two dedicated config directories. Candidate nginx writes are atomic per file, with in-process multi-file rollback; no claim of power-failure atomicity.

Implemented Certbot webroot provisioning, missing-lineage-only issuance, separate per-lineage renewal hooks and renewal timer. Initial issuance uses `--no-directory-hooks`, confirmed in upstream documentation, so all certificates/configuration prerequisites can be satisfied before application restarts. No Certbot nginx plugin rewrites Ansible files. Explicit old hook paths are removed after replacements exist; no certificates/lineages or unrelated hooks are deleted.

Moved desired nginx/certificate state into group vars. New media host vars set `nginx_domain: tv.slnnk.com`. Renamed the VPN group Certbot email key without changing its value; preserved all other existing credentials/settings. `inventory/hosts`, `all.yml` and existing host-specific files were left unchanged. New media group/host vars add no real IP, SID or account credentials.

Updated functional playbooks and the focused VPN playbook to run HTTP bootstrap, Certbot where needed, final required-certificate nginx configuration, then the dependent app and monitoring. Kept previously disabled VPN base roles disabled. Relay validation runs before nginx, and no certificate role is imported on the relay. Removed the superseded application nginx templates/handlers and VPN certificate issuance/hook ownership; retained endpoint/landing/logrotate behavior and certificate prerequisite checks before replacing the live endpoint binary/configuration.

Prepared media HTTPS locations for indexer result APIs and `/dl/` downloads only; the public root/admin paths return 404. The admin UI remains available via SSH tunneling to loopback 9117. API keys remain enforced by Jackett. nginx access logs omit query arguments. Existing host-network Compose and private FlareSolverr are unchanged.

An agent daemon restart interrupted one local validation approval; inspected saved state before resuming. Local nginx checks first hit sandbox/socket and unprivileged-port restrictions. Retried through approved escalation with isolated test paths, high ports and generated test certificates; no nginx daemon was started and no system config was replaced.

## Findings

- Four Ansible syntax checks passed: `vpn.yml`, `vpn-proxy.yml`, `trusttunnel.yml`, `jackett.yml`.
- Controller-only rendering with actual inventory and role validators passed for VPN, relay and Jackett. Connections were explicitly local; no target facts or SSH calls were used. The final repeat reported zero changes on all three scenarios.
- Real local `nginx -t` passed all three rendered configurations after substituting isolated paths, synthetic TLS certificates and nonprivileged listener ports. These tests establish syntax, not public DNS/TLS or target connectivity.
- Synthetic certificate-state tests exercised the actual selection tasks: missing certificates defer HTTPS while retaining HTTP; available certificates enable the full configured site set.
- Certificate argument construction and hook `sh -n` checks passed for the current VPN lineages and TV domain. Mocked service-command tests verified lineage mismatch causes no action, VPN renewal targets TrustTunnel restart, and TV renewal targets nginx validation/reload. No actual renewal or service command was executed by those tests.
- Three durable unit tests passed for the real transaction helper: changed then no-op behavior/unmanaged preservation; rollback of contents, permissions, symlinks and stale files; validation even on a no-op.
- Deployment manifests parse and all referenced staged files exist; rendered Python helper compiles.
- Required agent instruction lint reports zero errors and one existing generic-path warning (`CDX-AG-005` for the `defaults/main.yml` example in repository AGENTS). This warning is unrelated to the new architecture and was not auto-fixed.

## Changes

- New `roles/nginx/`: defaults, argument specs, validation/configuration tasks, main/HTTP/stream templates, deployment manifest and transaction helper, shared reload handlers, README.
- New `roles/certbot/`: defaults, argument specs, validation/provisioning tasks, lineage hook template, README.
- Refactored `roles/trusttunnel` and `roles/trusttunnel-proxy` tasks/handlers/vars/docs; obsolete nginx and deploy-hook templates removed from their old owners.
- Updated `roles/jackett/README.md`, four playbooks and repository `AGENTS.md`.
- Group variables for VPN/relay now own site/proxy/certificate intent; new `inventory/group_vars/jackett.yml` and `inventory/host_vars/dline-pl-01.yml` describe TV HTTPS and the selected domain.
- New `tests/test_nginx_transaction.py`; generated fixtures, test keys/logs and controller-only verification scripts remain outside Git under `/home/slnnk/ai-data/ansible-nginx/`.

## Status and risks

Requested local refactor and verification are complete. No Git commit, push or publication, target deployment, DNS write, real certificate issue, application restart or nginx reload occurred. Local validation commands have finished; no task agent or background installer remains active. Existing local media containers were not touched.

The [central TODO](../../../TODO.md) tracks remote deployment as a separate proposed stage after the new host/IP, unique Vault monitoring SID, DNS/HTTP challenge reachability and explicit approval are ready. Live CA issuance/renewal, existing-host migration, protected TV API reachability, tracker setup and actual 1-GB browser memory behavior remain unverified. Local fixture syntax is not a substitute for an approved target check and runtime validation.

## Portable lesson

none
