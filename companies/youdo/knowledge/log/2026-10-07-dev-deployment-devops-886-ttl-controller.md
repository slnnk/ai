---
system: dev-deployment
status: verified
checked: 2026-10-07
tags: [k8s, ttl, terraform, helm]
---
# DevOps-886: k8s-ttl-controller as safety-net cleanup for dev namespaces

## Summary

YouTrack `DevOps-886` ("[Dynamic env] Запустить TTL operator", sprint 196). The user decided that the
controller is a **safety net**: GitLab `on_stop`/`auto_stop_in` stays the primary cleanup, and the
controller TTL is one day longer than GitLab's. Chart is installed from the external TwiN repo, styled
like the other `infra-tf` modules. infra-tf branch `DevOps-886-dev-ttl-controller` prepared by the user;
module merged to infra-tf `master` (`1f5f6c4`) and applied by the user 2026-10-07 14:25 UTC; runtime verified (see Verification).

## Task

Install a controller that deletes `dev-*` namespaces by the `k8s-ttl-controller.twin.sh/ttl` annotation.

## Context

- Before: no controller; annotations were metadata only (see [overview](../systems/dev-deployment/overview.md)).
- Annotations: Jenkins `deploy-dev-b2b.Jenkinsfile:786` `DEV_NAMESPACE_TTL = '7d'` + `refreshed-at`;
  `helm-charts/ephemeral-namespace/values.yaml:162,169` default `7d`;
  `gitlab-ci-templates/v3/.deploy-dev.yml:274` extend sets `5d`. GitLab `auto_stop_in: 7 days`.
- Live 2026-10-07: only `dev-devops-832` carries the TTL annotation (`7d`, refreshed `2026-10-07T12:04:33Z`).
- Helm release records (`sh.helm.release.v1.*` Secrets): namespace-chart release lives in `default`
  (`dev-devops-832`); service releases live inside the dev namespace. Orphan `ns-dev-119` already exists in
  `default` (old naming).

## Actions

- Chart `k8s-ttl-controller` 0.4.0 (image `ghcr.io/twin/k8s-ttl-controller:v1.4.0`, repo
  `https://twin.github.io/helm-charts`) reviewed: one Deployment, ClusterRole `*/*` get/list/delete.
- Controller source v1.4.0: `API_RESOURCES_TO_WATCH` limits listed resources; reconcile every 5 min;
  supports `d` units (str2duration) and `refreshed-at`. On a list error the inner pagination loop
  `continue`s with `list == nil` and spins without sleeping -> RBAC must cover every watched resource.
- infra-tf files: `modules/k8s-ttl-controller/{main,variables,outputs}.tf` (own ClusterRole: namespaces
  get/list/delete + events create; chart `clusterRole.create=false`, `clusterRoleBinding.create=false`,
  env `API_RESOURCES_TO_WATCH=namespaces`, requests 10m/64Mi, limit 128Mi),
  `dev/namespaces.tf` (+`kubernetes_namespace.k8s_ttl_controller`), `dev/k8s-ttl-controller.tf`.
- `terraform plan` needs `CONSUL_HTTP_TOKEN` (from `current/.env`) and
  `-var kubeconfig_path=$HOME/.kube/config-yandex-dev`.
  Targeted plan: `-target=module.k8s_ttl_controller -target=kubernetes_namespace.k8s_ttl_controller` -> 4 to add.

## Findings

- **Gotcha:** `infra-tf/dev` provider default `kubeconfig_path = ~/.kube/config`; on this workstation its
  current context is `yc-kube-test-temp` (`10.16.26.68`, unreachable), not the dev cluster (`10.16.26.3`).
  A targeted create-only plan "succeeds" against the wrong kubeconfig because it never calls the API; the
  full plan fails with i/o timeouts. Always pass the dev kubeconfig.
- Full plan with the right kubeconfig: +4 ours and 1 unrelated in-place update `module.victoriametrics.helm_release.vmalert`
  (master commit `e9d0455` AP-2346 not yet applied). Apply ours with `-target`.
- `dev/config/vmalertmanager.yml` and `prod/config/vmalertmanager.yml` hold a plaintext Rocket.Chat webhook URL
  with token (location only; value not recorded).
- Pulls from `ghcr.io` work in the cluster (44 running containers use it). CI runners previously timed out
  on GitHub Pages Helm indexes; other modules already use `*.github.io`, so this adds no new dependency class.
- Orphan analysis: when the controller deletes a namespace, the namespace-chart release record in `default`
  stays `deployed`. Next Jenkins `helm upgrade --install` probably recreates missing objects (hypothesis, to
  verify); `3 delete dev` was assumed to fail on a missing namespace — **wrong**: in `gitlab-ci-templates` `7fabb47` it runs `verify_dev_namespace` only if the namespace exists, uninstalls the `default` release if present and reports "already deleted" otherwise; no change needed.

## Verification (2026-10-07)

- Deployment `k8s-ttl-controller/k8s-ttl-controller` 1/1, 0 restarts, image `ghcr.io/twin/k8s-ttl-controller:v1.4.0`;
  Helm release `k8s-ttl-controller` rev 1 `deployed`, chart 0.4.0.
- Logs: `[namespaces/dev-devops-832] ... TTL of 7d ... expire in 165h39m25s`, run 124 ms, sleep 5m (no hot loop).
- `kubectl auth can-i --as=system:serviceaccount:k8s-ttl-controller:k8s-ttl-controller`: delete/list namespaces yes;
  delete pods/deployments (all ns) and secrets in `default` no.
- Expiry deletion verified (approved by the user): namespace `ttl-test-886` created 14:29:31Z with `ttl=5m`; run 14:30:08 "expire in 4m22s"; run 14:35:08 "expired 38s ago" -> `deleted`; namespace gone by 14:35:24. Deletion lag = up to one 5-minute interval after expiry.

## jenkins-pipelines (2026-10-07)

Branch `DevOps-886-dev-ttl-controller` (prepared by the user), uncommitted edit of `pipelines/deploy-dev-b2b.Jenkinsfile`:
`DEV_NAMESPACE_TTL` `7d` -> `8d`; new `sh` step before the namespace `helm upgrade --install`: if the namespace has
`deletionTimestamp`, `kubectl wait --for=delete` (5m); if the namespace is absent and `helm status "$NAMESPACE_RELEASE"`
succeeds, `helm uninstall --wait`. Read-only dry run of the condition against the live cluster: `dev-119`/`ns-dev-119`
-> would uninstall, `dev-devops-832` -> skip, nonexistent -> skip. No Groovy compiler locally; runtime check pending. Merged to `master` as `b919f21` (commit `af3c6da`).

## gitlab-ci-templates (2026-10-07)

Branch `DevOps-886-dev-ttl-controller` (prepared by the user), uncommitted: `v3/.deploy-dev.yml` job `2 update ttl dev`
(formerly "2 extend dev") annotation `ttl=5d` -> `6d` (GitLab `auto_stop_in: 5 days` + 1d). YAML parses. Merged to `master` as `6d9b695`.

## helm-charts (2026-10-07)

Branch `DevOps-886-dev-ttl-controller`, uncommitted: `ephemeral-namespace/values.yaml` label `ttl` and annotation
`k8s-ttl-controller.twin.sh/ttl` `7d` -> `8d`; `helm template` renders `8d` with and without Jenkins `--set-json` annotations; `helm lint` passes.
At the user's request the same branch also removes the unreferenced pre-Jenkins `feature-<branch>` tooling (`scripts/create-feature-namespace.sh`, `scripts/create-feature-namespace-simple.sh`, `scripts/cleanup-feature-namespaces.sh`, `examples/namespace-examples.yaml`; label `auto-cleanup`, no references in helm-charts/jenkins-pipelines/gitlab-ci-templates/infra-tf), drops the done "Terraform-managed stale namespace cleanup" section from repo `TODO.md`, and updates TTL/cleanup ownership in `docs/ephemeral-namespace-role.md` and `docs/agents-ephemeral-deploy-plan.md` (8d/6d, controller as safety net).

## End-to-end check (2026-10-07)

All four repos merged: infra-tf `1f5f6c4`, jenkins-pipelines `b919f21`, gitlab-ci-templates `6d9b695`, helm-charts `58ecd76`.
`youdo-business-tochka-proxy` MR 240: the user ran `3 delete dev` `3214186` in old pipeline `140209` (15:41Z), then new
pipeline `140403` (templates from `master`, include has no `ref`):
- `1 deploy dev` `3214195` -> Jenkins `test` build `172` SUCCESS, console `Namespace TTL refreshed: 8d from 2026-10-07T15:47:32Z`;
  namespace `dev-devops-832` recreated 15:47:34Z, `jenkinsJobId=172`, label `ttl=8d`; release record `dev-devops-832.v1` in `default`;
  45 pods Running, 24 Completed. Orphan step did not fire (record already removed by the delete job) — expected.
- `2 update ttl dev` `3214196` -> annotation `ttl=6d`, `refreshed-at=2026-10-07T15:55:16Z`; GitLab environment
  `dev/devops-832-example` (id 576) `auto_stop_at` 2026-10-12 15:55:16Z; controller: expires in 191h52m (~2026-10-13 15:55Z) = GitLab + 1 day.
- Gotcha: manual lifecycle jobs in an existing pipeline keep the template compiled at pipeline creation; a template change needs a new pipeline.
- Not exercised at runtime: Jenkins orphan-release cleanup and terminating-namespace wait (logic dry-run only).

- Orphan cleanup (approved by the user): namespace `dev-119` absent; `helm -n default uninstall ns-dev-119` -> `uninstalled` (manifest: Namespace `dev-119` + rabbitmq/redis Deployments/Services, Ingress, Vault CRs, all inside the gone namespace). `default` now holds only `dev-devops-832.v1`.

- MRs: infra-tf !198, jenkins-pipelines !1, gitlab-ci-templates !87, helm-charts !2 (all merged). YouTrack summary comment `74-124617` posted at the user's request; issue closed by the user afterwards.

## Changes

- infra-tf `master` `1f5f6c4` (merge of `DevOps-886-dev-ttl-controller`): files listed above; applied by the user.

## Open items

Tracked in `~/ai/TODO.md` (dev-deployment).

## Portable lesson

[k8s-ttl-controller with least-privilege RBAC](../../../../general/knowledge/kubernetes/k8s-ttl-controller-least-privilege.md)
