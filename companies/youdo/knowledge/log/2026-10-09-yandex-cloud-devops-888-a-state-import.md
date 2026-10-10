---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, recovery]
---
# DevOps-888: import existing a node group and review remaining plan

## Summary
User authorized the recommended existing-nodegroup import and plan. Import succeeded into a backend: serial2->3, managed resources9->10, all previous resource IDs preserved. Saved post-import plan has only one create action for CoreDNS data; no cluster/nodegroup changes or deletions. Kubernetes nodeReady=True confirmed, versionv1.35.1 in ru-central1-a.

## Context
Existing group cat2jn302140sq4qlfkb had completed despite job3217265 RPCtimeout, but was absent from Consul terraform/yandex-dev-k8s-a. Cluster catg1hn09gu2jslb8vgl already managed. Repository remains clean on DevOps-888-recovery-k8s-a; root/CI matches current origin/master. No source changes needed.

## Actions and key commands
Used protected task helper ~/ai-data/terraform-recovery/DevOps-888/reconcile_a.py: verifies isolated backend type/path and existing cluster ID, saves restrictive raw state backup, imports exact group address with locking, asserts group ID and preservation of all previous IDs, then generates protected refresh-enabled plan and filtered summary. Existing TF_DATA_DIR a-plan-data, Terraform1.9.4 and cached providers used. User instruction “do what is necessary” followed the concrete import/plan recommendation and authorizes that import; no broader deployment authorization inferred.

Command: terraform import -input=false -no-color -lock-timeout=30s yandex_kubernetes_node_group.yc_a_k8s_dev_node_group cat2jn302140sq4qlfkb. Exit0. Backup a-pre-import-serial-2.tfstate protected0600. Postimport state serial3/10resources. Plan exit0; a-post-import.tfplan SHA256c5a5e5d16b63f0911c56e2fc33d3da7b6440a9b262374391c09d7b6ee33eda1d, filtered a-post-import-summary.json. All artifacts under ~/ai-data/terraform-recovery/DevOps-888, outside git; no secrets printed.

Generated separate local a-check.kubeconfig0600 with explicit context devops-888-a-check targeting newcluster10.16.28.49, existing YCprofileterraform-k8s-test. Default user kubeconfig/context untouched. TCP443reachable. GET nodes confirmed cl11b6jbeget0ffll0fk-abof ReadyTrue, zoneru-central1-a, kubeletv1.35.1.

## Remaining reviewed effect
Saved plan only creates Terraform management of data in existing ConfigMap kube-system/coredns-user, force=true, Corefile forwarding consul,youdo.corp,youdo.local to10.16.20.3. It does not create cloud infrastructure. This next apply modifies Kubernetes configuration and remote state and requires its own explicit approval under the user's per-command external-state rules. Native CoreDNS behavior, corporate DNS egress and workload recovery remain to be checked after apply. No apply, retry, merge or source edit performed.

## Changed files and risks
Protected helper/artifacts, separate local verification kubeconfig and KB notes only. No git changes. Local plan uses Terraform1.9.4; do not consume it in CI1.7.5. Saved plan must be rechecked against unchanged configuration/state before approved application. Workload/data migration is separate from cluster readiness. Live backlog in ~/ai/TODO.md.
