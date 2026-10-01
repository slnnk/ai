---
system: knowledge-base
status: verified
checked: 2026-09-30
tags: [token-cost, test-k8s, android-farm, dev-deployment]
---
# Knowledge base: read-only checks that resolved stale questions in system maps

## Task

Answer the "Stale (unresolved)" questions left in system map Summaries after the
2026-09-30 reconciliation
([personal log](../../../../personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)).
Read-only commands only: `git fetch`/`log`/`grep`, `yc ... get/list`, `kubectl get`, HTTP GET,
reading files over SSH.

## Context

Workstation, company network without the Kazan office segment. yc profile `default`,
kubeconfig `/home/slnnk/.kube/config-yandex-dev`, YouTrack token from `current/.env`.

## Actions

- `git merge-base --is-ancestor 10ef2517 2eafc2ee` in `/home/slnnk/git/jenkins-pipelines`.
- `yc managed-kubernetes node-group get catd0sn7d33n3rrgivh6`; `cluster get` for
  `catd03r096n9ih2qahac` and `cate30plq4p8h3hkab00`; `node-group get catof0bd6l9rbnej3q9o`;
  `cluster list --folder-id <kube-test folder>`.
- `git grep` on `yandex-tf` `origin/master` for `platform_id`, `max_expansion`, `--profile`,
  `service-account-key`.
- `kubectl get namespace dev-119`, `kubectl get namespaces`.
- `curl -m 6` GET on Loki `/ready`, `/loki/api/v1/labels`, `/loki/api/v1/push` for
  `loki.dev.youdo.corp`, `loki.infra.youdo.corp`, `loki-read`/`loki-write.yandex-test.youdo.local`.
- `ssh -o BatchMode=yes root@172.28.0.175 'hostname; ip -4 -o addr; grep ... config.toml'`;
  same for `10.16.24.175` and farm hosts `192.168.30.147/.148`.
- `grep` in untracked `infra-tf/dev/GITLAB_RUNNER_ANDROID.md` for the runner tag.
- YouTrack `GET /api/articles/DevOps-A-50?fields=idReadable,summary,updated,updatedBy(login)`.

## Findings

- jenkins-pipelines: `2eafc2ee` ("fix for gitlab ci", adds Groovy tests) is the direct
  child of `10ef2517` on `master`; build `145` therefore included the full-catalog change.
- test-k8s: live node group `standard-v3`, 8 cores / 48 GB, autoscale 1-10,
  `max_expansion = 1`. `origin/master` has it (`e527c5c`, 2026-09-14) and no
  `--profile`; CI uses `yc config set service-account-key`; the local working tree is clean.
  So the `56` -> `48` change and the Ice Lake move are applied and committed.
- test-k8s-temp: cluster `cate30plq4p8h3hkab00` and node group `catof0bd6l9rbnej3q9o`
  return NotFound; the folder holds only `kube-test`. Deleted; who and when is unknown.
- dev cluster: `dev-119` NotFound; the only `dev-*` namespace is
  `dev-hide-employee-api-swagger` (14 days old).
- Loki: `loki.dev.youdo.corp` -> `10.16.26.101` (dev Traefik), `/loki/api/v1/labels` 200,
  `/ready` 404. `loki-read`/`loki-write.yandex-test.youdo.local` -> `10.16.26.33`, 404 on
  the API paths (the read route of the 2026-09-07 TODO item is still broken there).
  `loki.infra.youdo.corp` -> `172.31.2.5`, no response from the workstation.
- Farm hosts `192.168.30.147/.148`: `No route to host`; the Alloy push URL is unverified.
- Android runner VM: hostname `gitlab-runner-android`, only `172.28.0.175/24`, runner name
  `gitlab-runner-android (172.28.0.175)`, `concurrent = 6`. `10.16.24.175` times out on SSH;
  probably the NAT address seen by GitLab (hypothesis).
- Planned Kubernetes runner tag: `k8s-android-dynamic`, in untracked
  `infra-tf/dev/GITLAB_RUNNER_ANDROID.md`; nothing is committed or applied.
- Loki follow-up (user, same day): Loki moved to the dev cluster; `loki-read` and
  `loki-write.yandex-test.youdo.local` are retired. `android-dig` already uses
  `http://loki.dev.youdo.corp` (since 2026-09-08). `automation-services` `origin/master`
  sets `alloy_loki_address: "http://loki.dev.youdo.corp/loki/api/v1/push"` in
  `inventories/office/group_vars/all.yml` (commit `0929e6c1`, 2026-09-11); role default
  remains `loki.infra.youdo.corp`. `GET /loki/api/v1/push` on `loki.dev.youdo.corp` returns
  405 (route exists). Deployment to the farm hosts is unverified.
- Farm push check (same day; the map had wrong SSH addresses `.147/.148`, the inventory
  `automation-services/inventories/office/hosts` has `M-K0057` `192.168.30.31`, `M-K0058`
  `192.168.30.32`): Alloy `active` on both since 2026-08-27, `/etc/alloy/config.alloy`
  (mtime 2026-08-27) pushes to `http://loki.dev.youdo.corp/loki/api/v1/push`.
- Incident: pushes fail with `context deadline exceeded` (`status=-1`): 8 errors on
  2026-09-14, then ~1970 per day since 2026-09-16 on `M-K0057` (same on `M-K0058`); no
  `M-K0057`/`M-K0058` values in Loki label `instance`. Farm logs have not reached Loki for
  about two weeks; entries beyond Alloy's retry window are lost.
- Cause: on the hosts `loki.dev.youdo.corp` does not resolve. `systemd-resolved` on `eno1`
  has only `192.168.30.1` with `Domains=~local ~.` (drop-in
  `/etc/systemd/network/10-netplan-eno1.network.d/local-domain.conf`, AP-2268); `dig
  @192.168.30.1 loki.dev.youdo.corp` times out while `gitlab.youdo.sg` resolves. TCP to
  `10.16.26.101:80` works. The corporate DNS `172.30.62.1` (used by the workstation for
  `youdo.corp`) is reachable from the hosts on TCP 53 and answers `loki.dev.youdo.corp A
  10.16.26.101` (TTL 461). What changed around 2026-09-14 on the office resolver is unknown
  (hypothesis: `youdo.corp` forwarding stopped on `192.168.30.1`).
- YouTrack DevOps-A-50 "Dev deployment": last updated 2026-08-31 22:18 UTC by the user.

## Changes

Summaries of `yandex-cloud/terraform-test-k8s.md`, `dev-deployment/overview.md`,
`dev-deployment/jenkins-deploy-dev-b2b.md`, `dev-deployment/gitlab-ci-deploy-dev.md`,
`android-farm/system-map.md`, `gitlab-ci/android-youdo4-dynamic-runner.md`; `~/ai/TODO.md`.

## Open items

Tracked in `~/ai/TODO.md` (android-farm: DNS for `youdo.corp` on the farm hosts, Alloy
push failing since 2026-09-14).

## Portable lesson

none
