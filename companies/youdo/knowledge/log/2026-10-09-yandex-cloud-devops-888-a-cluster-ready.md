---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [kubernetes, terraform, recovery]
---
# DevOps-888: successful a apply and cluster readiness

## Summary
User-run job3217390 and pipeline140497 succeeded. CoreDNS corporate-zone forwarding applied; deployment1desired/1ready/1available, log confirms Reloading complete. NodeReadyTrue/v1.35.1. Independent refresh-enabled Terraform plan exits0 with no changes. Infrastructure recovery configuration is converged; workloads/data and end-to-end corporate DNS resolution remain separate verification/recovery work.

## Context
User said runnernetworkaccess was being added by colleagues, then supplied [successful job3217390](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/jobs/3217390). apply:test-k8s master SHAf0c6d181bdef427bec20b5e09bf964b6fa37c3e2, runner106/gitlab-runner-docker-2(172.28.0.172), pipeline140497. Previous retry3217387 had TCPtimeout to newprivateAPI. Agent did not change network, retry job or execute apply.

## Actions and findings
Delegated longtrace inspection confirms plan/apply1addition0changes0deletions, only management of kube-system/coredns-user data; no errors, other resources unchanged. Explicit-context Kubernetes GET confirms Corefile now forwards consul,youdo.corp,youdo.local to10.16.20.3. Node cl11b6jbeget0ffll0fk-abof ReadyTrue/v1.35.1. Deploymentcoredns1desired/1ready/1available. Last15minute logs show Reloading, newconfigurationSHA512 and Reloading complete, no error lines returned. Corporate DNS query from a workload was not executed; successfulreload is not an end-to-end DNS test.

Ran protected helper reconcile_a.py plan with Terraform1.9.4, isolated a-plan-data, verified Consul backendterraform/yandex-dev-k8s-a, original nodegroupID recorded. Refresh-enabledplan exit0, filtered changes[], no pending create/update/delete. a-post-import.tfplan/log/show/summary artifacts overwritten with current verificationplan; earlier savedCoreDNS-onlyplan/hash in importlog is historical and must not be reused. Repository clean on DevOps-888-recovery-k8s-a, no code changes in this stage.

## Result and limits
Newcluster yc-a-k8s-dev catg1hn09gu2jslb8vgl privateAPI10.16.28.49, nodegroupcat2jn302140sq4qlfkb in ru-central1-a/subnete9b32eqch1la7rq0ed6e. Kubernetes1.35, originalbcluster not deleted. Previousgroup import and existing resources retained. Terraform/CI infrastructure stage complete. Existing application manifests, credentials, storage/data, ingress/DNSrouting and infra-tf/dev integration have not been restored by this root. Quotaheadroom limitation for preservedmax10 remains. Follow-up actions stay in ~/ai/TODO.md.

## Changed files and approvals
KB bookkeeping and protected local verificationartifacts only. Agent used read-only cloud/Kubernetes/Terraformchecks. User/colleagues performed networkfix and jobretry; no agent externalmutation, sourceedit, commit/push/MR/merge or infrastructureapply in this turn.
