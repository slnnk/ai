---
system: home-network
status: verified
checked: 2026-11-13
tags: [ansible, jackett, hetrixtools]
---
# Remote Jackett deployment on dline-de-01

## Task

Apply the existing full Jackett playbook to the VM added by the user to group `jackett`, including base services and Jackett.

## Context

Existing checkout `/home/slnnk/mygit/ansible`, branch/base `master`, HEAD `b857c7e`. Preserve pre-existing untracked files; no staging, commit, push or publication. Actual target is `dline-de-01`, `166.1.36.104`, Debian 13.4 x86_64; the former placeholder `dline-pl-01` is no longer in group `jackett`.

## Actions

The user selected `ext.slnnk.com`, superseding the earlier `tv.slnnk.com` proposal for this deployment, and supplied this monitor's installation command. Only the SID and service selection were extracted; no upstream installer was run. Group settings already monitor `docker` and `nginx`. The user explicitly approved creating host vars on existing `master` from `master`; created `inventory/host_vars/dline-de-01.yml` with the selected domain and Vault-encrypted SID. Vault password route: `ANSIBLE_VAULT_PASSWORD` in `personal/.env`; temporary helper `/tmp/jackett-vault-password` contains no credential value. SID decryption, format and uniqueness against existing hosts passed without displaying values. Playbook syntax passed.

Initial DNS returned no address locally and on the VM. The user subsequently supplied a DNS propagation screenshot; fresh VM resolution returned `166.1.36.104`. The user then explicitly answered yes to the full remote deployment proposal. Started `.ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/jackett.yml --limit dline-de-01 --vault-password-file /tmp/jackett-vault-password`. No other host is targeted. Bootstrap and base/SSH/firewall stages have completed; deployment is still running at this entry's initial creation.

## Findings

Expected result: successful playbook recap, automation SSH/sudo access, active security/runtime/web services, running loopback-only Jackett/FlareSolverr containers, valid public TLS and protected result/download routing, and active HetrixTools timer. Verification must use live service/container/HTTP checks; a successful syntax check does not establish runtime health. Tracker credentials, indexer migration and TV/Lampa cutover are outside this deployment request.

## Changes

Only `inventory/host_vars/dline-de-01.yml` was added to the Ansible checkout. The legacy placeholder host-vars file remains preserved. Remote changes are those made by the approved functional playbook. Current execution and verification status will be appended below; central backlog remains the only action list.

## Status and risks

At the initial entry deployment was still in progress. The final outcome below supersedes that interim status. Existing SSH hardening disables TCP forwarding; the README's suggested `ssh -L` administration route does not work with the deployed policy. No hardening exception was made. For the future home-server placement, keep administration private on the LAN; the exact access configuration remains part of the planned work in central TODO.

## Final outcome and home-server decision

Ansible exited2 with recap `ok=128 changed=56 unreachable=0 failed=1 skipped=13 rescued=0 ignored=0`. Bootstrap, common, nftables, sshd, CrowdSec, Docker, nginx and certificate issuance/renewal setup completed. The Compose reconciliation and Jackett restart handler reported changes. FlareSolverr readiness then failed after12attempts with `Connection refused` at `http://127.0.0.1:8191/`. The role's subsequent Jackett listener check and the monitoring role were not reached. The complete stack, live TLS/API health and metrics delivery were not verified; no successful final deployment is claimed.

The user's htop screenshot showed CPU100%, load average25.81,751/830MiB RAM used and no swap, with Chromium processes from FlareSolverr present. New SSH sessions timed out during banner exchange. HTTPS handshakes also timed out both locally and from the existing personal VPN host; that probe made no configuration changes on either server. Resource pressure is supported by the screenshot; the individual memory/CPU contribution and precise failure cause were not measured. No assertion of an OOM kill is made. A temporary1GiB swap file was proposed but not approved or created. The later2GiB sizing discussion was an estimate for low concurrency, not a successful load test or an instruction to resize.

The user decided to plan Jackett/FlareSolverr on the home server and said they will switch off the VM. This cancels the VM deployment/recovery branch, including the temporary-swap proposal; do not resume VM diagnostics or deployment automatically. No VM shutdown, service/container stop, DNS change, certificate revocation, monitoring-account change or repository cleanup was performed by the agent. Preserve the new Vault-protected host vars and the historical placeholder; removal was not requested. Do not reuse the VM's monitoring SID for a different host. The selected home host and its resources remain unspecified. Existing PC containers, indexers and TV settings were not changed.

The planned home-server placement reuses the prepared roles where appropriate and requires explicit implementation authorization, target identification, private administration, chosen indexer migration/Lampa cutover, and resource validation. A VPN client on the home server is not inherently required: the existing Cudy/podkop route can provide VPN access to blocked tracker destinations, while LAN clients access Jackett locally. Target-specific reachability remains unverified. The central TODO closes the cancelled VM proposal with this outcome and tracks the home-server plan separately.

Execution closeout: local Ansible session48715 returned its final failed recap and is closed; PID68726 had already exited, so there was nothing left to interrupt. All diagnostic exec sessions completed. The prepared verification and temporary-swap scripts were never run. No agent-started local background operation remains. Remote containers/services may remain active until the user powers down the VM; their final state and the shutdown itself are unverified, and the agent will perform no further remote checks after cancellation.

## Portable lesson

none
