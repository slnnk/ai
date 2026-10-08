---
system: dev-deployment
status: verified
checked: 2026-10-07
tags: [k8s, rbac, keycloak, oidc, pinniped, devops-883]
---
# DevOps-883: developer/QA kubectl access to dev-* namespaces (design)

## Task

DevOps-883: give developers and QA kubectl read/write access to `dev-*` namespaces of the Yandex dev cluster (debug, port-forward to DB). Consider SSO via LDAP/Keycloak. Design only, nothing applied.

## Context

- Dev cluster: Yandex MK8s, server `v1.34.1`, private API `https://10.16.26.3` (VPN/corp network only).
- Operator kubeconfig `~/.kube/config-yandex-dev` is a static token of SA `kube-system:admin-user` (cluster-admin); not suitable for distribution.
- Keycloak realm `https://auth-tech.youdo.com/realms/youdo` is already used by `headlamp-oauth2-proxy` (`--provider=keycloak-oidc`) for Headlamp `headlamp.dev.youdo.corp`; Headlamp itself runs with its SA token and ClusterRole `view` (`-unsafe-use-service-account-token`), so the user identity does not reach the API server.
- LDAP = FreeIPA (see `systems/automation-services/local-vault-ansible-access.md`).

## Actions

Read-only: `kubectl auth whoami`, `get ns`, `get clusterrolebindings`, `get validatingadmissionpolicies,validatingwebhookconfigurations`, ns `dev-devops-832` labels/rolebindings, Headlamp deployment args; read `helm-charts/ephemeral-namespace/templates/namespaces.yaml`; YouTrack GET DevOps-883; web search on Yandex MK8s OIDC.

## Findings

- `dev-*` namespaces have no RoleBindings and no Pod Security Admission labels; the cluster has no admission policies except `keda-admission`. Granting `edit` without PSA `enforce: baseline` lets a user run privileged/hostPath pods, i.e. node root.
- `ephemeral-namespace` chart owns the Namespace object, so a RoleBinding template there covers every new `dev-*` namespace automatically.
- Yandex MK8s offers no API-server OIDC flags; Yandex Marketplace provides "OIDC Authentication" (Pinniped Concierge + Supervisor) supporting OIDC/LDAP/AD (hypothesis: works with this cluster version; not tested). Alternative is Yandex Organization SAML federation from Keycloak plus RBAC by Yandex user id (per-user, `yc` CLI required).
- `edit` grants: secrets read (Vault-synced DB passwords, registry pull secret), `pods/exec`, `pods/portforward`, use of the namespace SA bound to Vault role `dev-ephemeral-deployer`, and changes to Helm release secrets that Jenkins manages.

## Chosen direction: shared kubeconfig without SSO (plan, not applied)

- User chose one shared ServiceAccount kubeconfig. Permissions: `edit` in `dev-*` via RoleBinding from the `ephemeral-namespace` chart, cluster-wide only `get/list/watch namespaces`; no namespace creation.
- (superseded 2026-10-07: user dropped the Vault/LDAP distribution; SA is `k8s-access/k8s-dev-developer`; kubeconfig is handed out by DevOps.)
- Repos: `infra-tf/dev` (new `k8s-access` namespace, SA `dev-developer`, token Secret, ClusterRole/Binding; Terraform `kubernetes` provider like `dev/namespaces.tf`), `helm-charts/ephemeral-namespace` (RoleBinding template, PSA label in `namespaceDefaults.labels`), `infra-tf/vault/test` (test Vault `vault.service.yandex-test.consul` serves dev: LDAP group -> read policy on `secret/dev/k8s/kubeconfig-developers`).
- Name `k8s-access` instead of `dev-access`: `gitlab-ci-templates/v3/.deploy-dev.yml:149` validates `^dev-...` and monitoring/cleanup of `dev-*` is planned.
- `kubectl label --dry-run=server ns dev-devops-832 pod-security.kubernetes.io/enforce=baseline` returned no warnings (2026-10-07): current workloads pass `baseline`.
- RoleBinding reaches existing namespaces only on their next Jenkins deploy.

## Changes

- `infra-tf` branch `DevOps-883-k8s-access` (user-created): new `dev/developer-access.tf` (namespace `k8s-access`, SA `k8s-dev-developer`, token Secret, ClusterRole `dev-namespace-lister` + binding), pattern copied from `dev/awx-backup.tf`. Not committed. Targeted `terraform plan` (backend needs `CONSUL_HTTP_TOKEN` from `.env`): 5 to add, 0 change, 0 destroy. Nothing applied.
- Token Secret in TF state: metadata changes update in place, the token survives; name/namespace/type change or SA recreation issues a new token. Rotation: `terraform apply -replace=kubernetes_secret_v1.k8s_dev_developer_token`.

## Open items

None for DevOps-883; optional SSO later.


## Portable lesson

none

## Applied by the user (2026-10-07)

- `infra-tf` merged and applied by the user. Verified: ns `k8s-access`, SA `k8s-dev-developer`, Secret `k8s-dev-developer-token`, ClusterRole `dev-namespace-lister`; `auth can-i --as=system:serviceaccount:k8s-access:k8s-dev-developer`: `list namespaces` yes, `get pods -n dev-devops-832` no (RoleBinding not yet in the chart).
- Jenkins `pipelines/deploy-dev-b2b.Jenkinsfile:782` uses `helm-charts` branch `master` and chart default `values.yaml` (only `--set namespaces[0].*`), so a chart merge takes effect on the next deploy without Jenkins changes.

## helm-charts change (branch `DevOps-883-dev-access`, not committed)

- New `ephemeral-namespace/templates/developer-access.yaml` (RoleBinding `developer-access` -> ClusterRole `edit`, toggle `developerAccess.enabled`), `values.yaml` block `developerAccess` and PSA `baseline` labels in `namespaceDefaults.labels`, `docs/ephemeral-namespace-role.md` updated.
- Checks: `helm lint` ok; `helm template` with Jenkins-style `--set namespaces[0].*` renders labels and RoleBinding; `developerAccess.enabled=false` renders none; `kubectl apply --dry-run=server` of Namespace + RoleBinding for `dev-devops-832` accepted without Pod Security warnings.
- Same branch: `docs/ephemeral-namespace-role.md` rewritten against `jenkins-pipelines` `ae1a125` (task-based `dev-{DEPLOY_ID}`, release name = namespace, annotations, Redis, PSA, developer RoleBinding, cleanup via GitLab `3 delete dev`, agent `AutoTest`); RoleBinding switched to the `ephemeral-namespace.labels` helper. Example `examples/jenkins/Jenkinsfile.ephemeral-namespace` still uses `dev-{BUILD_NUMBER}` (listed, not changed).

## After helm-charts merge (2026-10-07)

- `helm-charts` master `7b3b491` (merge of `e4710c9`). `dev-devops-832` still from Jenkins `170`: no PSA label, no `developer-access` RoleBinding until the next deploy.
- New script `current/scripts/k8s_dev_developer_kubeconfig.sh` (`build -o FILE` writes kubeconfig 0600 from Secret `k8s-access/k8s-dev-developer-token`, CA from the Secret; `check -f FILE [-n NS]` runs `auth can-i` and a server dry-run privileged pod). Pre-deploy check: token authenticates, cluster-level expectations pass, namespace permissions and PSA fail as expected.

## Verified after redeploy (2026-10-07)

- Jenkins `171` redeployed `dev-devops-832`: label `pod-security.kubernetes.io/enforce=baseline`, RoleBinding `developer-access` -> `ClusterRole/edit`; 45 Running, 24 Completed pods (no Pod Security rejections).
- `k8s_dev_developer_kubeconfig.sh check -n dev-devops-832`: all checks ok (rc 0), privileged pod rejected by Pod Security.
- Practical: `port-forward svc/docvalidation-devops-832-postgres 15432:5432` connects, `logs deploy/redis` and `exec deploy/redis -- redis-cli ping` (PONG) work with the shared kubeconfig.
- Remaining: hand out the file, developer instructions, rotation procedure.
- Distribution (by the user): Vaultwarden `https://vaultwarden.youdo.com`, collection `test_passwords/yandex-test`, item `k8s kubeconfig dev cluster`. Rotation must update this item.
- Developer instruction drafted (Russian) for a YouTrack child article of DevOps-A-50; commands checked against `dev-devops-832` with the shared kubeconfig. PostgreSQL credentials are chart constants in the StatefulSet env; the article points to the env instead of quoting them.
- Published (user approved) YouTrack article DevOps-A-51 "Dev deployment: доступ через kubectl", child of DevOps-A-50. System map `dev-deployment/overview.md` updated; TODO item closed.
