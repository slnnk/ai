---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [kubernetes, kubeconfig, recovery]
---
# DevOps-888: update local kubeconfigs to the recovery cluster

## Summary
User reports they added delivered kubeconfig to CI, then explicitly requests updating their previous local configuration. Updated ~/.kube/test-k8s-ci.kubeconfig and main ~/.kube/config to use yc-a-k8s-dev API10.16.28.49. Contextdefault is current; clusteraliaskube-test/useradmin-user retained. Existing unrelated main-config entries preserved. Both files mode0600; backups protected outside git. Authenticated defaultkubectl nodes GET succeeds, nodeReady/v1.35.1; dedicatedCIconfig readyz returnsok.

## Context and authorization
Previous dedicatedCIfile targeted10.16.26.3; mainconfig selected stale yc-kube-test-temp at10.16.26.68 and contained mks-infra access. KUBECONFIG environment unset. Both regularfiles, no symlinks. User request authorizes localfile/context updates. Source protectedcredentialfile ~/ai-data/terraform-recovery/DevOps-888/yc-a-k8s-dev-ci-140514.kubeconfig was previously tested afterCIapply.

## Actions and checks
Saved exact existingbytes to ~/ai-data/terraform-recovery/DevOps-888/local-kubeconfig-backups/test-k8s-ci.kubeconfig.20261009T135907Z.bak and config.20261009T135907Z.bak, mode0600/directory0700. Replaceddedicatedfile with currentstatickubeconfig. Merged namedclusters/contexts/users into mainfile; preserved allunrelated entries with assertions, setcurrent-contextdefault. Atomictempfilewrites/rename,0600. Tokens/privatekeys neverprinted or putinnotes/scripts/logs.

kubectl --request-timeout=15s get nodes throughdefaultconfig returned cl11b6jbeget0ffll0fk-abof ReadyTrue/v1.35.1. Explicit ~/.kube/test-k8s-ci.kubeconfig GET/readyz returnedok. Newdefault context maps clusterkube-test/useradmin-user tohttps://10.16.28.49. Old mks-infra and stale tempcontext entries remainavailable unchanged; no deletionorotherclusterupdate.

## Changes and limits
Localcredentialfiles andKB only; no cluster/GitLab/repo mutation. User-reported CIvariableupdate is not independently verified; agentdidnotwriteGitLabvariables. Traefik/application/data restoration remains separate.
