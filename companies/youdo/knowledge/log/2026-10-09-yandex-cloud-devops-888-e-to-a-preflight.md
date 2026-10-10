---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, recovery, preflight]
---
# DevOps-888: verified e cleanup inventory and a destination

## Task
User authorized step 1 of the [e-to-a recovery work plan](2026-10-09-yandex-cloud-devops-888-e-to-a-plan.md): read-only state/cloud inventory and target access checks. No destruction or repository changes authorized in this step.

## Context
Repository `/home/slnnk/git/yandex-tf`, root `test-k8s`, clean branch `DevOps-888-recovery-k8s-cidr`. Existing provider key location `test-k8s/key.json`; operator SA `ajegfhq6i2abngq74fcc`. Consul token variable `CONSUL_HTTP_TOKEN` in `~/ai/current/.env`. No secret values copied or exposed.

## Actions
Ran ai-sync.sh (no output), checked repo status, and delegated bounded Yandex CLI GET inventory. Sandbox DNS failed; escalated read-only requests succeeded. Consul state GET returned a filtered resource summary, not raw state. New a state key GET returned 404. YC existing profiles match Terraform key; no profile mutation required. No terraform init/refresh/plan/state mutation, backup pull, destroy, apply, API write or repository edit performed.

## Findings: e state and actual cloud resources
Consul key `terraform/yandex-dev-k8s-e`, datacenter selectel, state serial 2, Terraform 1.7.5. State contains one subnet datasource and nine managed resources:
- SA `k8s-dev-e-main-sa`, ID `aje1hmeguu3shk97d7ih`.
- Seven folder IAM members: k8s.clusters.agent, compute.admin, logging.writer, container-registry.images.puller, k8s.tunnelClusters.agent in `b1gnfk02b6vos0csupua`; vpc.privateAdmin and vpc.user in `b1gmdluusovi2uqivdha`.
- Tainted cluster `kube-dev-e`, ID `catm6t35irdu867q0ab0`.

Actual cloud GET for `catm6t35irdu867q0ab0` returns NotFound, while old folder list contains only the existing RUNNING kube-test (`catd03r096n9ih2qahac`). Recovery SA and all seven bindings exist and were independently verified. No node group/CoreDNS exists in the recovery state; cluster did not progress to their creation. Old e subnet `ajcbvev5ac7hjj691c5v` and failed-cluster CIDR reservations 10.129.0.0/16 and 10.145.0.0/16 are absent from old-folder inventory. Old folder still contains subnet-test 10.16.26.0/24 and legacy kube-test reservations 10.128.0.0/16 and 10.144.0.0/16.

Conclusion: eight recovery resources actually remain (SA plus seven IAM member bindings); cloud cluster entry in state is stale. A refresh-enabled destroy plan must reconcile this naturally, rather than deleting state entries manually. The old e subnet datasource is also stale and must be accounted for if Terraform destroy planning reads it. Exact Terraform delete count is not yet established by a destroy plan.

## Findings: a target and access
- Folder test-platform-folder, ID b1gra6b6tvv67paql8hs, ACTIVE; cloud b1g8s9lk6hktue4a48mg.
- Subnet test-platform-subnet-a, ID e9b32eqch1la7rq0ed6e, folder b1gra6b6tvv67paql8hs, zone ru-central1-a, CIDR10.16.28.0/24.
- Same VPC shared_network, ID enpo166pnu2hbn1s7v5k, owner folder b1gmdluusovi2uqivdha. Existing net_folder_id remains appropriate for VPC IAM.
- Route selectel-test, ID enp1rr12evj2uedu2p2h, default 0.0.0.0/0 via10.16.20.3.
- New folder has one subnet, no clusters and no security groups. Network folder has subnet-main10.16.20.0/24.
- Operator cloud-level roles: editor, k8s.editor, iam.serviceAccounts.admin, organization-manager.organizations.owner; no direct operator binding in new/network folders. Read access verified and inherited roles inspected; this is not a write/capacity test.
- Proposed a backend terraform/yandex-dev-k8s-a does not exist (Consul HTTP404); it can be initialized as a distinct new backend later.

Candidate pod/service10.129.0.0/16 and10.145.0.0/16 are absent from the three inspected folders (old test, new target, network owner). Other VPC folders and connected networks were not inventoried. Folder quotas/capacity and runner/DNS/egress reachability were not tested. Do not claim complete network conflict or deployment-capacity verification.

## Changes
Knowledge-base bookkeeping only. Updated existing system map and recovery work log. No repository or infrastructure changes. The next deliverable is the actual destroy plan for verified e-owned resources; deletion still requires explicit user approval.

## Risks
Keep old legacy cluster/subnets and original/workload state out of cleanup. Do not switch the root to a before e cleanup is planned/completed. Preserve e IAM until any cluster deletion step has been reconciled; here the cloud cluster is already absent. If state changes before planning/execution, regenerate the plan. Confirm inherited access/quotas/network availability before a apply.

## Portable lesson
None.

## Next stage prepared
User authorized continuing. A refresh-enabled saved destroy plan now confirms0 add/0 change/8 delete, only SA+seven IAM bindings; isolated snapshot pins old network parameters to bypass deleted subnet datasource. Original serial2 backup protected, remote serial remains2. See [destroy plan](2026-10-09-yandex-cloud-devops-888-e-destroy-plan.md). Destruction is pending explicit approval.
