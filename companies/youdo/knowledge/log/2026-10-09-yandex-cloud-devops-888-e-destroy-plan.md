---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, recovery, destroy-plan]
---
# DevOps-888: reviewed destroy plan for e remnants

## Task
User authorized continuing after [live preflight](2026-10-09-yandex-cloud-devops-888-e-to-a-preflight.md). Prepared a destroy plan for the e recovery remnants; destructive execution is not yet authorized. Overall [e-to-a work plan](2026-10-09-yandex-cloud-devops-888-e-to-a-plan.md).

## Context
Repository `/home/slnnk/git/yandex-tf`, root test-k8s, branch DevOps-888-recovery-k8s-cidr remains clean. Backend Consul terraform/yandex-dev-k8s-e, datacenter selectel, remote serial 2. Cloud cluster catm6t35irdu867q0ab0 is absent, but its state entry is tainted. Actual remaining resources: recovery SA and seven IAM bindings.

## Actions
Created an isolated local e configuration snapshot at `/home/slnnk/ai-data/terraform-recovery/DevOps-888/e-destroy-config`, separate TF_DATA_DIR e-destroy-data, existing key.json accessed via symlink. Initialized Consul backend with init -reconfigure -input=false, cached Yandex0.169.0/Kubernetes2.38.0 providers; no state migration. Local Terraform1.9.4 generates/applies the saved plan; remote state source was Terraform1.7.5.

Saved the original serial2 state via authenticated GET into protected e-pre-destroy-serial-2.tfstate. Refresh-enabled, normally locked plan -destroy initially failed because original subnet datasource ajcbvev5ac7hjj691c5v had been deleted and network_id evaluated null. In the local cleanup snapshot only, pinned the verified old VPC enpo166pnu2hbn1s7v5k, subnet ID ajcbvev5ac7hjj691c5v and zone ru-central1-e as literals. This does not modify repository/cloud/network resources; it lets destroy-mode validation proceed without the absent datasource.

Re-ran plan -destroy -input=false -lock-timeout=30s -out=e-destroy.tfplan: success. Parsed plan JSON in memory and saved only a limited resource summary. Structural verification confirms exactly expected eight delete actions, no additions/updates, all IAM members scoped to recovery SA. Protected state/plan/summary permissions are0600 within0700 data directory. Remote state GET after planning still returns serial2, so planning has not persisted refresh changes. Repo status is clean.

## Findings and exact scope
Plan0 add/0 change/8 destroy:
- Delete yandex_iam_service_account.k8s_dev_e_sa, k8s-dev-e-main-sa, IDaje1hmeguu3shk97d7ih, old test folder b1gnfk02b6vos0csupua.
- Remove its five role bindings in b1gnfk02b6vos0csupua: k8s.clusters.agent, compute.admin, logging.writer, container-registry.images.puller, k8s.tunnelClusters.agent.
- Remove its two role bindings in network folder b1gmdluusovi2uqivdha: vpc.privateAdmin and vpc.user.

Absent cloud cluster is not an API-deletion target in the saved plan. No node group, CoreDNS, VPC, subnet, original kube-test or workload resources are targeted. Cleanup reconciles stale state naturally; no state rm/import/manual state mutation is proposed.

## Artifacts and execution boundary
Protected artifact directory: `/home/slnnk/ai-data/terraform-recovery/DevOps-888/`.
- e-pre-destroy-serial-2.tfstate: original backup; do not publish raw contents.
- e-destroy.tfplan: saved plan SHA25611911f792ffacf129479e9fe634cef6938ac6f73317452fcd4f1bfd843171fed.
- e-destroy-summary.json: limited readable deletion summary.

After explicit approval, verify saved plan hash and current remote serial, then use the same local Terraform1.9.4/config/data directory to apply the exact saved plan, not a fresh auto-approved destroy. Execution deletes SA plus seven bindings in the two stated folders and updates only the e recovery backend. Verify actual SA/bindings absence and no managed resources remaining in e state. Do not delete the state key or perform a deployment without separate scope/approval. If any relevant change occurs before execution, regenerate and re-review the plan.

## Changes
Generated local protected artifacts and KB bookkeeping only. No destroy/apply/remote resource change, repository edit, commit or publication. Current deletion approval is pending.

## Risks
Backups/plan may contain private infrastructure information; keep protected and outside git. Retain the original backup. Source kube-test/shared network/workload states are unrelated and excluded. New a configuration must not replace the old root until cleanup is verified. Offline provider lock has Linux-only locally calculated checksums; this saved plan is for the verified local toolchain, not CI1.7.5.

## Portable lesson
None.

## Approved execution and verification
User explicitly approved deletion of the reviewed eight resources on 2026-10-09. Verified saved plan SHA25611911f792ffacf129479e9fe634cef6938ac6f73317452fcd4f1bfd843171fed and unchanged remote serial2 before execution. Applied the exact saved plan using local Terraform1.9.4, isolated e cleanup config/data directory and normal locking. Exit0: 0 added,0 changed,8 destroyed. No fresh auto-approved destroy or additional cleanup actions.

Consul GET after apply: serial4, Terraform1.9.4, resources[] (no managed or data entries). State key and original protected backup are retained. Limited result artifact e-destroy-result.json has0600 permissions. Independent Yandex GET checks: recovery SAaje1hmeguu3shk97d7ih NotFound; zero bindings for that member in both old test and network folders. Original kube-testcatd03r096n9ih2qahac remains RUNNING/HEALTHY. Target a subnet remains unchanged. Entire sharedVPC inventory lists six ranges10.16.20/24,10.16.24/24,10.16.26/24,10.16.28/24,10.128/16,10.144/16; candidate10.129/16 and10.145/16 are free from subnet overlap across this VPC, failed e reservations absent. Connected-route overlap, quotas and zonal capacity remain unverified.

Next stage proposal: branch DevOps-888-recovery-k8s-a in existing checkout from origin/master95e4f60, same test-k8s root, new folder/subnet/names/zone/backend. Stage1 branch/local-change approval pending. Repo remains clean; no new branch or a deployment created. No state-key removal, network/subnet mutation, merge, commit or push in this execution stage.

## Target naming correction
User announced yc-a- prefix and requested cluster yc-a-k8s-dev. Proposed target SA/node-group names now follow that prefix; branch DevOps-888-recovery-k8s-a/local implementation approval is still pending. Canonical rules updated in company CONTEXT.md and terraform-test-k8s system map. Previous kube-dev-a naming proposal retained here as history, superseded for the target cluster.
