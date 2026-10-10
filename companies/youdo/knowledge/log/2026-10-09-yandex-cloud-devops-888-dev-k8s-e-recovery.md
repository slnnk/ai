---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, recovery, git-training]
---
# DevOps-888: prepare recovery cluster kube-dev-e

## Task
Prepare recovery cluster `kube-dev-e` in `ru-central1-e`, subnet `subnet-test-e` (`ajcbvev5ac7hjj691c5v`), Kubernetes 1.35/STABLE, separate clean state and GitLab CI support. Final user correction: reuse existing `test-k8s` directory instead of creating `dev-k8s-e`. Task: https://youtrack.youdo.com/youtrack/issue/DevOps-888/Recovery-Vosstanovit-klaster-k8s .

## Context
Repository `/home/slnnk/git/yandex-tf`, origin `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`. Supervised Git/MR workflow is active. YouTrack GET confirmed task title and empty description. Base `origin/master` is `33ca351`, which already defines `subnet-test-e` in the shared VPC (`10.16.28.0/24`).

## Actions
Ran `~/ai/general/scripts/ai-sync.sh` (no output/reminders). Read company context/backlog and delegated read-only multi-file inspection. Fetched origin. Created approved task branch. Initially prepared a separate `dev-k8s-e` root, matching the original user request; later moved the source changes into existing `test-k8s` and removed only the agent-created directory/additions after the user changed scope. No backend initialization, state migration, apply or deployment.

## Findings
Final backend path is `terraform/yandex-dev-k8s-e`, distinct from old `terraform/yandex-test-k8s`. New service account `k8s-dev-e-main-sa` avoids existing-name conflict. Master and nodes explicitly use target subnet; VPC and zone derive from that subnet, default provider zone is e. Cluster/node group use 1.35/STABLE; Yandex documentation lists 1.35/STABLE availability since 2026-08-19: https://yandex.cloud/ru/docs/managed-kubernetes/concepts/k8s-supported-versions . Sizing, private endpoint, CALICO and IAM roles are inherited. CoreDNS manages data of pre-created `kube-system/coredns-user` using `kubernetes_config_map_v1_data` with `force = true`.

## Changes
Final diff: nine existing files, 65 added and 72 removed lines. Eight tracked Terraform source files in `test-k8s` plus `.gitlab-ci.yml`. Existing CI jobs `validate:test-k8s`, `plan:test-k8s`, `apply:test-k8s` retain rules/cache/names; only plan/apply initialization gains `-reconfigure -upgrade`, preventing old cached backend state migration. `.gitignore` is unchanged from HEAD; no new directory remains. Existing local key/cache are preserved. Publication approved and completed; commit `3f8415a7464f95ab2357219123774b2788b80739`, MR !232.

## Verification
- `terraform fmt -check -diff`, `terraform validate -no-color`, `git diff --check`: passed for final test-k8s configuration.
- Terraform validation uses an isolated `TF_DATA_DIR` under `/tmp/devops-888-validation`, backend disabled during provider initialization, cached Yandex 0.169.0 and Kubernetes 2.38.0. Existing `test-k8s/key.json` is used without copying or exposing its contents. Sandbox blocks provider plugin startup, so validate was run outside sandbox.
- CI YAML parse/comparison passed: only the two expected init commands changed; all other CI content is equivalent to HEAD.
- Local tflint absent; actual tflint and cloud plan remain for CI. GitLab server lint was not run because POST requires separate external-action approval. Remote backend key existence, private API reachability and subnet egress remain unverified.
- Independent reviews of initial and final scopes found no blocking issues; final reviewer confirmed no leftover directory/CI additions and correct backend reconfiguration.

## Risks
The separate backend path is configured but not verified empty against Consul. New state creates a separate cluster/SA/node group; original state is not migrated or modified. Fresh cluster private API connectivity must be available to the runner for CoreDNS configuration. Existing workload recovery is a later stage.

## Training record
- Proposed branch `DevOps-888-recover-k8s`; final branch `DevOps-888-recovery-k8s`. User explicitly approved creating the corrected branch and local edits. Base `origin/master` `33ca351`, source/target `DevOps-888-recovery-k8s` -> `master`, project `sysadmins/yandex/yandex-tf`.
- Corrections: branch suffix `recovery-k8s`; Kubernetes 1.35; MR without Draft; reuse `test-k8s` instead of creating `dev-k8s-e`. These are task-specific; no broader permissions/preferences inferred.
- Proposed commit `add kube-dev-e recovery cluster`.
- Final proposed MR title `DevOps-888 add kube-dev-e recovery cluster`; initial Draft proposal was explicitly overridden by the user.
- Stage 2 publication explicitly approved by the user (“Confirm” follow-up on 2026-10-09) after the final reused-root summary. Staged exactly nine task files, checked the actual staged diff, committed and pushed. MR !232 created without Draft: https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/merge_requests/232 . SHA/source/target/description/draft=false verified by GET. Squash off, removal after merge on, assignee a.solonenko. Agent did not merge or deploy.
- Publication CI effect: existing validate/plan:test-k8s triggered by test-k8s file changes. Apply:test-k8s remains manual and master-only.

## Portable lesson
None.

## Publication and CI results
Published commit `3f8415a7464f95ab2357219123774b2788b80739` (`add kube-dev-e recovery cluster`) to `DevOps-888-recovery-k8s`; local checkout clean. MR !232 title/source/target/body match the approved proposal. MR pipeline 140484 succeeded: `validate:test-k8s` job 3217038 and `plan:test-k8s` job 3217039. Branch pipeline 140483 was canceled; existing rules selected multiple other-root jobs on new branch creation. No workflow-rule change was included (previously deferred by user). The user then supplied job 3217042; read-only diagnosis is ongoing. No job retry or apply triggered by the agent.

## Failed first apply: job 3217042
The user merged MR !232; fetched `origin/master` is `6358e067b037ce7e2a563bfa2893baa6a5a6400f`. User-supplied job https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/jobs/3217042 is failed `apply:test-k8s` in master pipeline 140485. Yandex rejected cluster creation because inherited pod CIDR `10.128.0.0/16` overlaps existing subnet `e9bfsliq0opqgpepndrt` with the same range. All seven IAM member resources and service account `k8s-dev-e-main-sa` (`aje1hmeguu3shk97d7ih`) completed; cluster/node group/CoreDNS did not. The new backend path and subnet lookup are correct. Successful plan 3217039 proposed 11 additions, 0 changes, 0 deletions; CIDR conflict surfaced only at creation. Pre-publication omission: copied pod/service CIDRs were not checked against live VPC reservations. Read-only live CIDR discovery is ongoing. Keep the partially populated new state so subsequent apply reuses SA and bindings; no remote changes or retries made by the agent.

## CIDR discovery and follow-up proposal
Read-only YC subnet inventory calls did not return data; investigation was stopped without any cloud/configuration changes. Candidate pod `10.129.0.0/16` and service `10.145.0.0/16` are unverified, not applied. Do not claim them free. Need live VPC/cluster/connected-network range verification before final selection. Proposed follow-up branch `DevOps-888-recovery-k8s-cidr` in the same checkout, base `origin/master` `6358e06`; branch/local-change approval pending under supervised training. No repository changes made after publication.

## User-provided VPC console evidence
The user supplied a screenshot of `shared_network` (`enpo166pnu2hbn1s7v5k`) showing six subnets: `subnet-test-e` 10.16.28.0/24, `subnet-test` 10.16.26.0/24, existing Kubernetes service reservation 10.144.0.0/16, existing Kubernetes pod reservation 10.128.0.0/16, `subnet-prod` 10.16.24.0/24, and `subnet-main` 10.16.20.0/24. This confirms both original cluster ranges remain reserved. Proposed replacement pod 10.129.0.0/16 and service 10.145.0.0/16 do not overlap the six visible subnet ranges; connected-network/route inventory is still unverified. The screenshot supplies evidence, not explicit follow-up branch approval. No repository edits or external changes performed.

## CIDR follow-up implementation
User explicitly approved `DevOps-888-recovery-k8s-cidr` creation/local changes and asked whether networks are created in zone e. Created branch from `origin/master` `6358e06`. Local diff only changes `test-k8s/k8s-cluster.tf`: Pod `10.128.0.0/16` -> `10.129.0.0/16`, Service `10.144.0.0/16` -> `10.145.0.0/16` (2 additions, 2 deletions). Master and nodes remain explicitly in the existing subnet-test-e/zone e. Pod/Service reserved subnet creation is managed by Yandex, with no separate zone argument in this Terraform configuration; actual reserved subnet zone must be observed after creation rather than assumed e.

Validation passed: terraform fmt, terraform validate (isolated TF_DATA_DIR, outside sandbox), git diff --check, Python ipaddress comparison against the six screenshot subnet ranges, independent read-only review. Source route-table search shows default routes and no more-specific destination overlapping the proposed ranges; live connected-network/routing inventory remains unverified. Backend/key/cache were not reinitialized or migrated. Keep the partially populated new remote state.

Follow-up proposed commit `set separate recovery cluster cidrs`; MR title `DevOps-888 set separate recovery cluster cidrs` without Draft; source `DevOps-888-recovery-k8s-cidr`, target `master`, project `sysadmins/yandex/yandex-tf`. Stage 2 approved explicitly by the user after the CIDR-only publication summary on 2026-10-09. Staged only test-k8s/k8s-cluster.tf, inspected full staged diff, committed and pushed. Follow-up MR !233 created without Draft. CI publication effect is existing validate/plan:test-k8s; apply remains manual master-only.

## CIDR follow-up publication
Published commit `c269e4ae3dad17a22a59c4acac28b0fbc42ea9e8` (`set separate recovery cluster cidrs`) on `DevOps-888-recovery-k8s-cidr`. MR https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/merge_requests/233 title `DevOps-888 set separate recovery cluster cidrs`, target master, assignee a.solonenko, squash false, source removal after merge true. Remote SHA/source/target/body/draft=false verified; checkout clean. MR pipeline 140489 running: validate:test-k8s 3217130 passed, plan:test-k8s 3217131 pending. Branch pipeline 140488 running: validate:test-k8s 3217117 passed, plan:test-k8s 3217123 running. These are the latest checked statuses, not final pipeline results. Agent did not merge, retry failed apply, or deploy; partial remote state stays intact.

## Second apply failure: managed master capacity
The user supplied https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/jobs/3217180 . Read-only trace diagnosis: failed apply:test-k8s, master pipeline 140491, SHA `95e4f605c181747dae74f494fc745e9f30174efb` (CIDR MR !233 merged by the user). Operation `catcuj6cadvq2usrdjl0` failed after about one minute with ResourceExhausted, `unable to create master instance`, `Not enough resources`. Exact master allocation failure; worker resources are not implicated. Official Yandex documentation associates this message with zonal hardware shortage: https://yandex.cloud/ru/docs/compute/qa/not-enough-resources . Live quota/capacity inventory was not checked; log provides no quota-limit detail.

Plan was 3 additions, 0 changes, 0 deletions; existing service account and all seven IAM bindings refreshed. Parameters confirmed: master 1.35, private endpoint, zone e, subnet ajcbvev5ac7hjj691c5v, VPC enpo166pnu2hbn1s7v5k, pod10.129/16/service10.145/16. Old CIDR rejection is resolved. Cluster creation did not complete; node group/CoreDNS did not start. No cloud cluster ID appears in trace; allocation/persistence of a failed cluster object and its state record cannot be determined from the log. Before retry, inspect cloud/state if accessible. Preserve terraform/yandex-dev-k8s-e. Next appropriate external action is a support request with operation ID/zone, or explicitly approved retry when capacity is available. No repository edits, retries, support ticket submission, merge or deployment performed by the agent during diagnosis.

## User changes recovery destination and requests plan first
User now targets folder test-platform-folder (`b1gra6b6tvv67paql8hs`), subnet test-platform-subnet-a (`e9b32eqch1la7rq0ed6e`) and an a-suffixed state. They suggested cleaning up e first and explicitly requested a work plan before execution. See [e-to-a plan](2026-10-09-yandex-cloud-devops-888-e-to-a-plan.md). No destroy, branch edits, backend initialization, plan-destroy or external changes made in this planning turn. Suggested kube-dev-a/SA/node-group/state names require review; actual e cleanup and a deployment need explicit approvals.

## Verified live preflight
User authorized work-plan step1. Consul e state serial2 holds SA+7bindings+tainted cluster catm6t35irdu867q0ab0; cloud GET of that cluster is NotFound. Actual remnants are SA and seven IAM bindings, all verified; legacy kube-test remains RUNNING. New test-platform folder/subnet metadata and read access verified, same shared VPC/network-owner folder. New Consul a key is absent. See [live preflight](2026-10-09-yandex-cloud-devops-888-e-to-a-preflight.md) for exact IDs, access scopes and limits. No destroy/plan/init/repository edit performed.
