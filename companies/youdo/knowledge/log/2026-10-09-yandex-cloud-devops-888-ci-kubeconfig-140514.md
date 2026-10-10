---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [kubernetes, ci, recovery]
---
# DevOps-888: refresh CI kubeconfig after pipeline 140514

## Summary
CI pipeline 140514 succeeded after user apply; MR !236 is merged. Subsequent CI plan reports no changes. A fresh static CI kubeconfig was built from the current Kubernetes token Secret and tested: node Ready/v1.35.1. Token matches the earlier protected file; no rotation observed.

## Context and evidence
Pipeline140514 master SHA5958abfadb5a813373e20e1d7d1872abd227c5f6, MR !236 merged into this SHA. Initial plan3217715:0add1change0destroy. Apply3217716 succeeded:0added1changed0destroyed. Subsequent plan3217717 succeeded:No changes. The earlier empty Secret diff converged after the user-run CI apply; its precise root cause remains unproven. No agent CI retry/apply/merge or credential mutation.

## Actions
Read current kube-system/admin-user-token via existing explicit-context kubeconfig, in memory only. build_ci_kubeconfig.py wrote new protected file ~/ai-data/terraform-recovery/DevOps-888/yc-a-k8s-dev-ci-140514.kubeconfig with mode0600. Existing original files preserved. Verified context/current-contextdefault, clusteralias kube-test, useralias admin-user, endpointhttps://10.16.28.49, embedded CA and static token without exec dependency. In-memory constant-time comparison confirms token matches prior yc-a-k8s-dev-ci.kubeconfig; values/hashes not printed. Authenticated GET nodes returns cl11b6jbeget0ffll0fk-abof ReadyTrue/v1.35.1.

## Delivery and limits
File path provided to user; contents are for TEXT CI variable KUBECONFIG_YANDEX_DEV used by infra-tf/dev. Agent did not update GitLab variables. Credential Secret/state, local kubeconfig and access routes are recorded by location only, never secret values. Credentials grant cluster-admin as the original CI pattern. Default user kubeconfig and kubecontext unchanged. Traefik/application/data recovery remains separate.

## User delivery confirmation

UserreportsaddedCIvariable; agentdidnotmodifyGitLab. Subsequentlyupdatedpreviouslocaldedicatedanddefaultkubeconfigs afterexplicitrequest, withprotectedbackups andsuccessfulauthenticatedchecks. See [localupdate](2026-10-09-yandex-cloud-devops-888-local-kubeconfig.md).
