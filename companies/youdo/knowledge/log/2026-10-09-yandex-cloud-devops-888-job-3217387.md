---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [kubernetes, terraform, gitlab, recovery]
---
# DevOps-888: inspect recovery job 3217387

## Summary
Retry apply:test-k8s job3217387 failed during the remaining CoreDNS operation because the runner could not establish TCP to private Kubernetes API10.16.28.49:443. Workstation Kubernetes reads succeed, nodeReadyTrue and systempodsready; coredns-user still contains the default commented example. No agent mutation performed.

## Context
User supplied [job3217387](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/jobs/3217387). Master SHAf0c6d181bdef427bec20b5e09bf964b6fa37c3e2, pipeline140497, statusfailed/script_failure. User ran retry after separately authorized nodegroup import; agent has not run CoreDNS apply. Plan1addition/0changes/0deletions, only kubernetes_config_map_v1_data.coredns_custom.

## Evidence and findings
Trace error checking existing ConfigMap kube-system/coredns-user at coredns-custom.tf:2: GET https://10.16.28.49/api/v1/namespaces/kube-system/configmaps/coredns-user failed dial tcp10.16.28.49:443:i/o timeout. No CoreDNS completion or apply success; no other modifications recorded. Error establishes runnerTCPconnection failure, not missing ConfigMap, badcredentials or resourcecreationtimeout.

Live GETs using separate a-check kubeconfig confirmed cl11b6jbeget0ffll0fk-abof ReadyTrue, zoneru-central1-a, kubeletv1.35.1. All12listed kube-systempods Running and allreportedcontainersReady; calico-typha-vertical-autoscaler has3restarts. coredns-user Corefile still standardcommentedexample (no corporateforwarding). KubernetesCoreDNS pod running does not prove corporatezones resolve. Normal local kubecontext untouched. Delegated runnermetadata/route inspection is ongoing.

## Actions and limits
Read-only job/trace and Kubernetes GETs, KB bookkeeping. No sourcechanges, SSHmutation, firewallroutechange, jobretry, Terraformapply or CoreDNSwrite. Need resolve runnernetworkpath to10.16.28.49 before expecting CIapply success; increasing Terraformcreationtimeout does not address this observed TCPfailure. Existing savedlocalCoreDNS-onlyplan requires revalidation before a separately approved apply.

## Confirmed runner and user follow-up

Actual runner106 gitlab-runner-docker-2 (172.28.0.172), manager47/systemIDr_qxLnmZnJ2LXE, GitLabRunner17.9.3/Linuxamd64, Dockerexecutor, image registry.youdo.sg/youdo/base-images/terraform:1.7.5. Timeout originates inside thisDockerjob. User says colleagues will add access from runnernetwork to the newnetwork; no completion claim yet. Further independentnetworkdiagnosis stopped to avoid duplicatework. Once access10.16.28.49:443 is confirmed, retryapply is expected to configure onlyCoreDNS, subject to its freshplan; no cluster/nodegroup recreation expected. No agentretry/applyauthorized/performed.

Bounded read-only SSH had already verified hostnamegitlab-runner-docker-2 at172.28.0.172: both API routes via172.28.0.1/deveth0/src172.28.0.172; newAPI443 TCP5stestfailed. OldAPItestresult notcollected before stopinstruction; no furtherdiagnosis or mutation.
