---
system: selectel
status: verified
checked: 2026-06-04
tags: [mks-infra, kubeconfig, kubectl, managed-kubernetes, workstation]
---
# mks-infra kubeconfig

## Task

Update the local Kubernetes config for the Selectel Managed Kubernetes cluster `mks-infra`
(owned by `selectel-tf/prod-mks`) on the workstation, keeping the existing contexts.

## Actions (2026-06-04)

- Task: update local Kubernetes config for `mks-infra`.
- Local file: `/home/slnnk/.kube/config`.
- Backup before change: `/home/slnnk/.kube/config.backup-20260604-142753`.
- Cluster entry: `mks-infra`, API server `https://172.31.3.164:6443`.
- Context: `admin@mks-infra`.
- Authinfo used by context: `youdo-sa`.
- Existing `yc-kube-test-temp` context was preserved.

## Findings: validation

- `kubectl config get-contexts` shows `admin@mks-infra` as current and bound to `youdo-sa`.
- `kubectl config view --minify` shows `mks-infra` server `https://172.31.3.164:6443`.
- `kubectl --request-timeout=5s get namespace kube-system` succeeded outside the sandbox; `kube-system` status `Active`, age `198d`.

Secrets note: token, client certificate, and private key values are intentionally not stored here. They are embedded only in the local kubeconfig as requested.

## Portable lesson

none
