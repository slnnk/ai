---
system: home-network
status: verified
checked: 2026-11-14
tags: [ansible, docker, lampa, torrserver, jackett]
---
# Home media Docker roles and playbook

## Task

Prepare Docker roles for Lampa, TorrServer, Jackett and FlareSolverr and a home
playbook without nftables. This request authorizes local implementation only.

## Context and approval

Repository `/home/slnnk/mygit/ansible`, existing `master`, base `master` at
`b857c7e`. User explicitly approved this repository/branch/base proposal with
`Да`. Existing untracked inventory, playbooks, roles and docs were preserved;
no staging, commits, pushes or deployment were requested or performed.

The initial proposal reused the combined Jackett/FlareSolverr role. During work
the user specified `Не нужно host network` for the home stack and then requested
the standard automation-user, common and SSH roles. These are task-scoped
requirements, not changes to unrelated VPS workloads or global instructions.

## Changes

- New `lampa` role serves pinned yumata/lampa static files using httpd in Docker,
  checks the source archive SHA-256 and writes local Media Station X startup JSON.
- New `torrserver` role uses MatriX.150 with persistent `/opt/ts` data.
- Existing `jackett` role gains bridge mode; its default host mode remains for
  existing VPS consumers. Bridge mode publishes Jackett only on the selected LAN
  address, keeps FlareSolverr unpublished and uses Docker service DNS.
- `inventory/group_vars/home.yml` selects LAN addresses from `ansible_host`.
- `playbooks/home.yml` targets `home`/`home-01`, bootstraps `ansible-user` as root,
  then applies `common`, `sshd`, `docker`, `lampa`, `torrserver`, `jackett`.
  It does not include nftables. Application ports are8080,8090,9117.
- Role READMEs, Docker/Jackett docs, project AGENTS and four regression tests updated.

## Verification

Home syntax-check passed with the real inventory; both plays select only home-01.
Existing Jackett playbook syntax-check passed using a temporary local inventory
because the user's current inventory has no jackett group. Four tests passed:
native Docker Compose parsing and LAN-only publications, private solver,
unchanged default host networking, preserved API keys/passwords/proxy settings,
and local MSX startup URLs. GHCR manifest for MatriX.150 exists. Source archive
SHA-256 verified. No containers were started or images pulled for these checks.

Agent lint: zero errors, one existing CDX-AG-005 warning about the generic
`defaults/main.yml` reference in AGENTS; no automatic fixes. Direct agnix also
reports root-overview information, filtered by the established shared policy.

## Status and risks

Local preparation complete. Server deployment, runtime resource/peer checks,
indexer migration and TV cutover remain unperformed and require explicit approval.
No background task remains. Central TODO retains the deployment/migration action.
No host-network change was applied to existing VPS consumers. The local tests
do not prove TV playback or upstream tracker/Cloudflare behavior.


Deployment status updated2026-11-14: the user subsequently requested application; home-01 deployment and HTTP checks succeeded after a transient registry retry. See [deployment](2026-11-14-home-network-home-media-deployment.md). The preparation-only statements above describe the earlier stage; PC migration and TV cutover remain pending.

## Portable lesson

none

## Task metrics: home-media-roles-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "home-media-roles-20261114",
  "created": "2026-11-14T19:31:01.227905+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Local checks and task scope in this note; runtime not requested",
  "updated": "2026-11-14T19:31:01.227950+03:00"
}
```
