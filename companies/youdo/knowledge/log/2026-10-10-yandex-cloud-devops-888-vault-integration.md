---
system: yandex-cloud
status: verified
checked: 2026-10-10
tags: [vault, kubernetes, recovery, DevOps-888]
---
# DevOps-888 restored Vault integration verification

## Summary

Restored Vault Kubernetes integration already works for Sentry in the new cluster. The ephemeral deployment role still needs an end-to-end check.

## Task

Resume DevOps-888 and determine remaining Vault integration work after backup restoration. User provided VAULT_YANDEX_TEST_TOKEN in current/.env; only the variable name and access route are recorded.

## Context

Cluster yc-a-k8s-dev API is https://10.16.28.49. Vault endpoint is http://vault.service.yandex-test.consul:8200. Repository infra-tf remains on DevOps-886-dev-ttl-controller; no task files were changed and no publication or external mutation was performed.

## Actions

Read-only Vault GET sys/health, sys/auth, auth/kubernetes-dev/config and six role definitions. Read Kubernetes Pod, VaultAuth, VaultConnection, VaultStaticSecret, ServiceAccount and ClusterRoleBinding status; inspect VSO startup logs. Compare Vault CA with kubeconfig CA in memory without printing values. Inspect only Secret metadata/count, never secret payloads.

## Findings

- Vault 1.21.4 initialized, unsealed and active.
- kubernetes-dev already uses https://10.16.28.49; CA matches the new cluster, token_reviewer_jwt_set=true, disable_local_ca_jwt=true, disable_iss_validation=true.
- vault/vault-kubernetes-reviewer exists with vault-kubernetes-reviewer ClusterRoleBinding to system:auth-delegator; vault-kubernetes-reviewer-token is a service-account-token Secret bound to this SA. The exact token stored in Vault was not available through the read API, so identity equality was not independently proven.
- VSO 1.5.1 Pod is ready. vault/default VaultConnection healthy and ready; sentry/sentry VaultAuth uses role resources, SA default, mount kubernetes-dev and is healthy/ready.
- sentry/sentry-external VaultStaticSecret uses KV v1 secret/resources/sentry-dev and reports SecretSynced=True, Healthy=True, Ready=True. Destination Kubernetes Secret exists with eight keys. Last ready transition observed at 2026-10-10T12:50:39Z.
- dev-ephemeral-deployer requires audience vault, SA default and namespaces dev-*. helm-charts/ephemeral-namespace/templates/vault-auth.yaml explicitly requests audience vault. No dev namespace consumer currently exists in the cluster; this path remains unverified.
- Restored roles buildapi, headlamp, janitor, monitoring and resources exist. Only resources has live consumer evidence in this session.
- infra-tf module owns Helm releases but not reviewer resources or kubernetes-dev backend config/roles. Default VSO auth values include Vault namespace vault, whereas the live OSS connection works through explicit workload VaultAuth; inspect before relying on default auth.

## Changes

Knowledge log, existing yandex-cloud system map and central TODO only. Repository and external state unchanged.

## Risks and limits

Successful Sentry sync proves one consumer path, not every policy or secret payload correctness. Backup age and application secret freshness were not assessed. Further live login tests or deployments create external state and require explicit permission under global instructions.

## User correction: infra-tf before application deployment

User explicitly deferred dev deployment until infra-tf is reconciled. Read-only terraform state pull from existing dev backend returned serial 129, Terraform 1.9.4 and 21 Helm release entries. Live Helm metadata in yc-a-k8s-dev showed only traefik, awx-operator (revision 2) and vault-secrets-operator. Existing state therefore does not describe the currently installed platform completely; a refresh plan must establish per-resource recovery/import requirements. Do not infer that all resources recorded as deployed still exist.

Fetched infra-tf origin/master f57349d. Clean current checkout remains DevOps-886-dev-ttl-controller at 47d89cf. For dev/modules/vault/CI scope, difference to master is one gitlab-runner values change. No branch switch or repository edits performed. Latest root pipelines use dynamic child pipelines; root pipeline job listing alone is insufficient to establish dev apply history.

Recovery order: compare current master configuration and Consul state against the new cluster, produce a reviewed refresh plan with explicit kubeconfig and protected outputs, identify existing resources requiring import, then approve required state/config changes and platform recovery before application deployment. No refresh plan, import or apply ran in this session. Vault module supplies in-cluster Helm integration with the external Vault; its presence alone does not imply a second Vault server must be deployed.

## Correction: active recovery state terraform/yandex-dev-k8s-a

User identified the recovery state key terraform/yandex-dev-k8s-a. Read-only Consul GET verified serial16, Terraform1.14.3, 30 resources/instances. This state contains yc-a-k8s-dev (catg1hn09gu2jslb8vgl, API https://10.16.28.49), subnet, node group, cloud SA/IAM, CI identity, CoreDNS, four namespaces, Vault reviewer SA/Secret/auth-delegator binding, VSO Helm release, Sentry auth/static secret and ClickHouse, plus AWX and Traefik Helm releases. Its three deployed Helm entries match live Helm metadata.

The earlier comparison of live releases against terraform/yandex-k8s-dev used the legacy infra-tf backend and does not demonstrate drift in the active recovery state. Import/recreation requirements must not be inferred from that comparison. Before using infra-tf/dev, establish resource ownership and intended backend: its local configuration still names the legacy state, whereas new recovery state already owns some corresponding objects under different Terraform addresses. No state move/import/configuration changes performed; remaining-resource readiness and refresh-plan convergence not established by state inventory alone.

## Approved infra-tf backend change

User requested switching infra-tf key and checking plan, then explicitly answered Yes to stage1 proposal: repository /home/slnnk/git/infra-tf, branch DevOps-888-infra-state-a from origin/master f57349d. Created branch in existing clean checkout; changed only dev/main.tf backend path from terraform/yandex-k8s-dev to terraform/yandex-dev-k8s-a. No commit/push/MR approval requested or granted.

terraform init -reconfigure -input=false -lock=false succeeded without state migration. Cached backend confirms requested key. Local Terraform1.9.4; existing Helm/Kubernetes/local/null provider versions reused; Yandex provider0.238.0 resolved from resources in state. Refresh-enabled plan started with -lock=false, -parallelism=5, -detailed-exitcode and explicit kubeconfig_path=/home/slnnk/.kube/test-k8s-ci.kubeconfig. Protected outputs under ~/ai-data/terraform-recovery/DevOps-888/infra-state-a; do not print raw logs/state/plan because they may contain secrets.

Read-only review found ownership mismatch: cloud resources and reviewer identity in state have no declarations in infra-tf/dev; VSO state address helm_release.vault_secrets_operator differs from module.vault.helm_release.vault_secrets_operator and no moved rule connects them. Deletion/recreation is a prediction until a successful plan is available. No additional code changes made.

First full plan exited1: Yandex provider missing credentials/explicit configuration. Partial summary77add/3change/7remove. Seven removal candidates: CI admin SA/token/binding, Vault reviewer SA/token/binding, and root VSO release. Updates: Sentry ClickHouse StatefulSet, AWX operator release, Traefik release. A retry uses existing test-k8s/key.json through YC_SERVICE_ACCOUNT_KEY_FILE (no code provider change); only key path is recorded.

## Completed refresh plan for switched infra-tf backend

Authenticated retry exited2 (successful plan with changes):77add/3change/17destroy. Saved plan dev.tfplan and sanitized actions.txt under protected artifact directory. Yandex provider emitted a nonfatal tool initialization service connectivity warning.

Confirmed deletion addresses: yandex_kubernetes_cluster.yc_a_k8s_dev, yandex_kubernetes_node_group.yc_a_k8s_dev_node_group, yandex_iam_service_account.yc_a_k8s_dev_sa, seven yandex_resourcemanager_folder_iam_member bindings, three ci_admin identity resources, three vault_reviewer identity resources, helm_release.vault_secrets_operator. Those objects have no matching declarations in infra-tf/dev. New VSO release is declared at a module address without a moved rule.

Updates are kubernetes_stateful_set_v1.sentry_clickhouse_25 (wait_for_rollout only), module.awx.helm_release.awx_operator and module.traefik.helm_release.traefik (values/metadata). No replacement actions were present. Provider refresh performed no state write because plan used -lock=false and no apply.

Final tracked diff is only dev/main.tf backend key, diff --check passed. No apply/import/state move/commit/push/MR performed. User's requested key change and plan check are complete; destructive plan requires ownership/configuration reconciliation before any apply.
