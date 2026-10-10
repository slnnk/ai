---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, gitlab, recovery]
---
# DevOps-888: inspect recovery apply job 3217265

## Summary
Master apply:test-k8s job3217265 failed creating the a node group with gRPC DeadlineExceeded/stream timeout after about one minute. Cluster creation completed after8m26s. Live check confirms node group RUNNING but absent from state; import is needed before another apply. No retry performed.

## Context
User supplied [job3217265](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/jobs/3217265). Pipeline140497, master SHAf0c6d181bdef427bec20b5e09bf964b6fa37c3e2, script_failure. User merged MR !235; current fetched masterce0151f includes further AP2347 changes, but test-k8s and .gitlab-ci.yml match approved dd272c7 exactly. Local checkout clean on DevOps-888-recovery-k8s-a.

## Findings
Plan11add0change0destroy. Completed SAajebqdg33tfer4giq2i5, seven IAM bindings and new clustercatg1hn09gu2jslb8vgl. Error at yandex_kubernetes_node_group.yc_a_k8s_dev_node_group, test-k8s/k8s-cluster.tf:46: rpc error: code = DeadlineExceeded desc = stream timeout. RequestID0d369db7-451d-4347-8381-7232075e4022. No node-group completion or CoreDNS creation is recorded in trace. This is an RPC stream timeout, not proof of Compute quota exhaustion or insufficient zonal resources, and not proof that the backend did not accept the create request. Exact service/network root cause remains unknown.

## Actions and limits
Delegated long-trace inspection, fetched read-only refs, checked root/CI diff and native configuration. No repo edit, job retry, import/state mutation, cloud/Kubernetes write or deployment. Inspect actual nodegroups/operations and Consul a state before proposing another apply, preserving completed resources and avoiding duplicate creation.

## Live cloud and state verification
Newcluster catg1hn09gu2jslb8vgl yc-a-k8s-dev is RUNNING/HEALTHY, Kubernetes1.35, zonalru-central1-a, privateAPIhttps://10.16.28.49. Nodegroup cat2jn302140sq4qlfkb yc-a-k8s-dev-node-group exists and is RUNNING despite the CI timeout; instancegroupcl11b6jbeget0ffll0fk, allocation ru-central1-a, subnete9b32eqch1la7rq0ed6e. Consul terraform/yandex-dev-k8s-a state serial2 has exactly9managedresources:SA+cluster+7IAM, all normal; no nodegroup or CoreDNS entry. Therefore the API accepted/completed nodegroup creation, but the provider failed before recording its ID. CloudRUNNING does not prove Kubernetes nodeReady or workload health.

## Concrete next step
Prepare/review an import into the EXISTING a backend using exact address yandex_kubernetes_node_group.yc_a_k8s_dev_node_group and IDcat2jn302140sq4qlfkb, then refresh-enabled terraform plan to confirm convergence and remaining CoreDNS operation. Command: terraform import yandex_kubernetes_node_group.yc_a_k8s_dev_node_group cat2jn302140sq4qlfkb, with explicitly initialized a backend/credentials. Import changes remote Consul state and requires separate explicit approval; none requested/granted/executed in this read-only job inspection. Never blindly rerun apply while group is absent from state. No cloud object deletion or master recreation needed based on current evidence.

Final instance-group GET confirms one worker VM fhm1htctma7ltehtdmek, RUNNING_ACTUAL in ru-central1-a. Kubernetes nodeReady remains unverified.
