---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, recovery, plan]
---
# DevOps-888: recovery from zone e to zone a work plan

## Task and design brief
User requested moving recovery to `test-platform-folder` (`b1gra6b6tvv67paql8hs`), subnet `test-platform-subnet-a` (`e9b32eqch1la7rq0ed6e`) and state suffix a, and asked for a work plan first. Existing repository/root remain `/home/slnnk/git/yandex-tf/test-k8s`; Kubernetes 1.35/STABLE and private master are retained. Updated associated names under user naming correction: cluster `yc-a-k8s-dev`, proposed node group `yc-a-k8s-dev-node-group`, proposed SA `yc-a-k8s-dev-sa`, Consul path `terraform/yandex-dev-k8s-a`. These names and execution are proposals, not approved changes.

## Context
Implementation plan based on the user's latest requirements and [recovery work log](2026-10-09-yandex-cloud-devops-888-dev-k8s-e-recovery.md). Stack: Terraform/Yandex and Kubernetes providers, Consul backend, Yandex Managed Kubernetes, GitLab CI. Execution can be performed inline with read-only multi-file/log inspection delegated as required by the global agent rules; use executing-plans when execution is approved. This plan is stored in the KB because repository editing requires branch approval and the user keeps operational knowledge here. It introduces no note-local TODO list; the live action stays in ~/ai/TODO.md.

Current master `95e4f60` contains the e configuration. Last e apply failed at master VM allocation (operation `catcuj6cadvq2usrdjl0`, Not enough resources). SA `aje1hmeguu3shk97d7ih` and seven IAM bindings were created; failed cluster object/state presence remains unverified. New e state is `terraform/yandex-dev-k8s-e`, separate from original `terraform/yandex-test-k8s` and workload state `terraform/yandex-k8s-dev`.

## Constraints and review focus
Do not edit the e configuration/backend before its destruction is planned and completed. Destroy only verified resources owned by the e recovery state, never old cluster reservations/shared VPC/subnets/original state/workload state. Preserve restrictive backups of the current e state and saved destroy plan outside git; do not expose their raw contents. Preserve managed-cluster IAM bindings until cluster deletion completes. Inspect failed cloud objects absent from state; explicit approval is required for deletion/import/state mutation or any other external change. Do not migrate the e state into a. No automatic retry, merge, deployment, or tracker closure. New-folder/VPC IAM scopes and network connectivity must be checked, not copied blindly from e.

## Phase 1: read-only inventory and destruction preparation
1. Verify current master/clean checkout and keep an e-configured root. Inspect the e Consul key and cloud inventory for cluster, nodes, reserved subnets and IAM objects, including any failed object not recorded in state. Identify ownership before including anything for removal.
2. Load only required `CONSUL_HTTP_TOKEN` from `~/ai/current/.env` without printing it; use existing `test-k8s/key.json`. Use an isolated TF_DATA_DIR and restrictive generated-data directory under `~/ai-data/terraform-recovery/DevOps-888/`. Initialize the e backend with `terraform init -reconfigure -input=false`; no migrate-state or force-copy.
3. Pull a protected e-state backup and summarize `state list`/IDs. Generate `terraform plan -destroy -input=false -lock-timeout=30s -out=<protected saved plan>`, with refresh and normal locking. Summarize only resource addresses, IDs and change counts from plan JSON; no raw state/plan output.
4. Confirm plan affects only e-owned resources. Minimum expected inventory is SA plus seven IAM bindings; exact count depends on actual failed-cluster state. If cloud/Consul cannot be reached, stop the dependent action and obtain inventory through the console/known access route; do not infer an empty cloud from an absent log ID.

Deliverable: actual refresh-enabled destroy plan and explicit deletion list, with e backend identity and latest state serial verified. No destroy has been authorized yet.

## Phase 2: approved e cleanup
1. Present exact deletions and affected folder, including any failed-cluster/orphan handling, and ask explicit approval for applying the saved destroy plan.
2. Apply the reviewed saved plan only after approval. If separate orphan operations are required, each needs its own explicit approval; no hidden additional cleanup.
3. Verify e state is empty and e-owned cloud resources/reservations are absent, while shared/legacy resources remain. Preserve backups and the empty backend; state-key removal is not required for the move.
4. If destruction fails partially, retain state, investigate and regenerate the plan before further changes. Do not switch the root to a while e cleanup still requires it.

Deliverable: verified e cleanup. This is preferred before a creation to free any recovery CIDR reservations and avoid leaving unmanaged e resources.

## Phase 3: preflight and local a configuration
1. Read target folder/subnet metadata: subnet `e9b32eqch1la7rq0ed6e` must resolve to `ru-central1-a`; derive VPC network_id and verify the actual network-owning folder for `net_folder_id`/IAM. Confirm credentials can create resources in `b1gra6b6tvv67paql8hs` and access the subnet. Check required K8s 1.35/STABLE availability and folder quotas.
2. Inspect target VPC subnet/Pod/Service reservations and connected routes; choose nonoverlapping ranges. Keep current candidates Pod `10.129.0.0/16`, Service `10.145.0.0/16` only if free in the target network after e cleanup. Verify DNS `10.16.20.3`, private API runner reachability, node egress and default SG behavior for the new VPC.
3. Propose branch `DevOps-888-recovery-k8s-a` from current origin/master in the existing checkout and wait for supervised stage-1 approval before repository edits.
4. Update `test-k8s/terraform.tfvars` (target folder/subnet and verified network-owner folder); `variables.tf` (default zone a); `main.tf` (new backend and provider resource references); `k8s-cluster.tf` (cluster/node names and references, verified CIDRs if needed); `sa.tf` (new SA and correct IAM scopes/references); `data.tf`, `outputs.tf`, `coredns-custom.tf` (consistent a references). Keep master/node subnet explicit, CoreDNS adoption and cluster IAM dependencies.
5. Existing `.gitlab-ci.yml` jobs remain validate/plan/apply:test-k8s with init -reconfigure. Change CI only if required by discovered folder credentials/access; scope/effects must be reviewed explicitly.

Deliverable: consistent local a configuration and a distinct unused backend; e-state contents are not copied.

## Phase 4: verification and publication
1. Run terraform fmt -check, terraform validate with isolated data directory, diff --check, relevant TFLint/CI configuration verification and independent code review.
2. Inspect final task-only diff and present actual checks, commit message/MR title, source/target and CI effects. MR without Draft, one short Russian change paragraph plus task link. Wait for supervised stage-2 approval before staging/commit/push/MR publication.
3. Verify remote SHA/MR parameters and run/read the CI plan against the a backend. Initial a plan must contain only intended additions, no old-resource changes/deletions. Quota/capacity constraints may still surface at actual creation; a green plan alone is insufficient.

Deliverable: published reviewed MR with validated a plan; no merge/apply authorization implied.

## Phase 5: approved a deployment
1. User-approved merge to master and separate explicit approval for manual apply:test-k8s (or the user performs these actions). Inspect the exact master SHA/plan before apply.
2. Apply only the reviewed a configuration/state. On failure, retain partial state, inspect actual cloud objects and regenerate plan before retry.
3. Verify yc-a-k8s-dev master RUNNING in ru-central1-a, node group/nodes ready in target subnet, CoreDNS internal-zone forwarding and private API access from the runner. Observe auto-created Pod/Service reservation metadata; their zone is service-managed and not separately configured by Terraform.

Deliverable: operational infrastructure in a; e resources remain cleaned up. No workload restoration is implied by infrastructure success.

## Phase 6: workload recovery and closure
Prepare a separate reviewed workload-recovery scope for infra-tf/dev, kubeconfig/CI integration, storage/backups, DNS and services. Preserve existing workload state until its resource mapping/recovery strategy is reviewed. Confirm cluster health and useful service checks, update the existing system map/work log/repos record, then close completed actions in ~/ai/TODO.md. External writes retain their own approval boundaries.

## Approval record and self-review
This turn produces only a plan/KB bookkeeping. No Terraform backend initialization/pull/destroy plan, repository edits or external writes performed. Destruction, branch edits, publication, merge and new apply are separate checkpoints. Covered latest folder/subnet/state requirements; unknown network-owner folder, actual e remnants and target CIDR availability are explicit preflight decisions with a stop condition, not assumed values.

## Portable lesson
None.

## Progress: approved e cleanup complete
Phase1 inventory verified and Phase2 completed after explicit deletion approval. Saved plan removed exactly eight e resources; state serial4/resources[], SA and all bindings absent in cloud; legacy kube-test RUNNING/HEALTHY. Entire sharedVPC subnet inventory now verifies10.129/16 and10.145/16 avoid all six subnet ranges. Target a subnet unchanged. See [destroy execution](2026-10-09-yandex-cloud-devops-888-e-destroy-plan.md). Phase3 branch/local changes are not yet approved; quotas, connected-network overlap and target runner connectivity still need assessment before deployment.

## Naming correction
User announced prefix `yc-a-` and requested exact cluster `yc-a-k8s-dev`. Corresponding SA/node-group names are proposed above; Consul state proposal remains terraform/yandex-dev-k8s-a. Canonical resource naming recorded in CONTEXT.md and the existing terraform-test-k8s system map; no wider-zone policy inferred. The correction specifies the name but does not explicitly approve the proposed Git task branch; stage1 approval is still pending. No repo edits/cloud changes in this naming turn.

## Approved a implementation progress (2026-10-09)

User subsequently confirmed corrected yc-a- names and branch/local implementation. Phase3 completed on DevOps-888-recovery-k8s-a from origin/master95e4f60. Phase4 checks and independent review passed; live plan11create0change0destroy, a backend absent. Stage2 publication pending. Compute quotas fit initial1 worker but not preserved max10 CPU/RAM; quota follow-up recorded in the live backlog. No new deployment. See [implementation results](2026-10-09-yandex-cloud-devops-888-yc-a-k8s-dev.md). Earlier pending-stage entries above describe their original checkpoints.

## Phase4 publication completed

User approved publication; commit dd272c7 pushed on DevOps-888-recovery-k8s-a and MR !235 created/verified without Draft, targeting master. MR pipeline140496 running at last check. Phase5 merge/apply remains separately authorized work; no new deployment.
