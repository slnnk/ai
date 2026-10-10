---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, recovery, gitlab]
---
# DevOps-888: prepare yc-a-k8s-dev in zone a

## Task
Prepare recovery cluster yc-a-k8s-dev in ru-central1-a for [DevOps-888](https://youtrack.youdo.com/youtrack/issue/DevOps-888/Recovery-Vosstanovit-klaster-k8s), using existing test-k8s root, test-platform-folder and a fresh Consul backend.

## Context
Approved e cleanup completed: eight resources deleted, e state serial4 with zero managed resources; legacy kube-test remains RUNNING/HEALTHY. User corrected naming to yc-a- and explicitly confirmed branch/local implementation after that correction. Repository /home/slnnk/git/yandex-tf; branch DevOps-888-recovery-k8s-a from origin/master 95e4f605c181747dae74f494fc745e9f30174efb. No unrelated local changes or staged changes.

## Actions
Updated eight Terraform files. Ran terraform fmt -check -diff, terraform validate -no-color, git diff --check and independent review: all passed, no blocking review findings. A refresh-enabled live plan against terraform/yandex-dev-k8s-a produced 11 additions, zero changes and zero deletions. Protected plan and filtered summary reside in ~/ai-data/terraform-recovery/DevOps-888/a-create.tfplan and a-create-summary.json. Isolated TF_DATA_DIR a-plan-data and local Terraform1.9.4 used existing Yandex0.169.0/Kubernetes2.38.0 providers. CI uses Terraform1.7.5 and must generate its own plan. No state migration or apply performed. After plan, Consul a key remained absent (HTTP404); e remained serial4/empty.

## Findings
Folder b1gra6b6tvv67paql8hs is ACTIVE. Subnet e9b32eqch1la7rq0ed6e is in ru-central1-a, CIDR10.16.28.0/24, shared_network enpo166pnu2hbn1s7v5k owned by network folder b1gmdluusovi2uqivdha. Default route uses 10.16.20.3. Complete shared-VPC subnet inventory confirms Pod10.129.0.0/16 and Service10.145.0.0/16 avoid all six existing ranges. Kubernetes1.35 is available in STABLE.

Live cloud-wide Compute quota headroom: 42 cores,96GiB RAM,1396GiB nonreplicated SSD,32 instances and24 disks. Initial worker8cores/48GiB/93GiB fits. Preserved max10 workers needs80cores/480GiB/930GiB, exceeding current free Compute CPU/RAM. Managed Kubernetes free node-group RAM is480GiB, leaving no extra worker RAM at maximum for expansion1 rollout. Quotas do not guarantee hardware availability in zone a. Private API connectivity from runner, connected-network range overlap and image-pull access to registries outside the new folder remain unverified until further checks/deployment.

## Changes
test-k8s/main.tf,data.tf,variables.tf,terraform.tfvars,k8s-cluster.tf,sa.tf,coredns-custom.tf,outputs.tf:49 additions/49 deletions. Cluster yc-a-k8s-dev; SA yc-a-k8s-dev-sa; node group yc-a-k8s-dev-node-group; folder test-platform-folder b1gra6b6tvv67paql8hs; subnet test-platform-subnet-a e9b32eqch1la7rq0ed6e; backend terraform/yandex-dev-k8s-a. Five IAM roles target the new cluster folder and two VPC roles target the existing network folder. Resource references updated consistently. Kubernetes1.35, private master, CALICO, worker sizing/autoscaling and CoreDNS forwarding preserved. .gitlab-ci.yml and .gitignore unchanged; existing validate/plan jobs run on publication, apply:test-k8s remains manual on master.

## Publication approval
Proposed commit: configure yc-a-k8s-dev recovery cluster. Proposed MR title: DevOps-888 configure yc-a-k8s-dev recovery cluster, without Draft. Source DevOps-888-recovery-k8s-a -> master. MR body is one short Russian change paragraph followed by the task link. Stage2 approval pending; no staging, commit, push, MR, merge or new deployment performed. The user's latest confirmation covered corrected branch/local implementation; no broader permission inferred. Live follow-up work remains in ~/ai/TODO.md.

## Portable lesson

none

## Stage2 approval and publication execution

User explicitly confirmed commit, push and MR creation after reviewing final diff/checks/names/CI effects. Staged exactly eight approved task paths and inspected the full staged diff; git diff --cached --check passed. Created commit dd272c70939f65606ed2af2880f7b9c2611f56cc (configure yc-a-k8s-dev recovery cluster) and pushed DevOps-888-recovery-k8s-a with upstream set. git show --numstat confirms49 additions/49 deletions; commit console used rewrite heuristics showing80/80. Initial sandbox push failed DNS; approved publication succeeded with network escalation. MR creation/verification is in progress. No merge or infrastructure apply authorized or performed.

## Publication result

MR [!235](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/merge_requests/235) created without Draft. Verification confirmed expected title/body/source/target and remote SHA dd272c70939f65606ed2af2880f7b9c2611f56cc. Assignee a.solonenko, squash false, removal after merge true. Checkout clean and tracks origin/DevOps-888-recovery-k8s-a. Last checked MR pipeline140496 running; branch pipeline140495 canceled. Local checks/live plan previously passed; CI final result still pending. Agent did not merge or apply.
