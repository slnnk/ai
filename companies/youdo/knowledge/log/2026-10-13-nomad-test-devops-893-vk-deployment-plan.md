---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, vk-cloud, csi, recovery]
---
# DevOps-893 Nomad repository recovery deployment plan for VK Cloud

## Task

October13 user steering: stop additional prerequisite checks and deploy one service at a time, diagnosing concrete failures. Start Traefik, then Redis; do not make exhaustive preflight a gate. See [recorded preflight findings](2026-10-13-nomad-test-devops-893-vk-preflight.md). Branch and individual external-change approval rules remain applicable.

[DevOps-893](https://youtrack.youdo.com/youtrack/issue/DevOps-893), `[Recovery] Развернуть terraform репо в Nomad`. Prepare a deployment plan for `/home/slnnk/git/terraform`, replace Yandex CSI with a VK-compatible driver and change test environment URLs from `yandex-test` to `vk-test`. User explicitly permits empty data (October 13). No implementation or runtime deployment requested yet.

## Summary

Historical proposal below is superseded by the approved state terraform/vkcloud-terraform and the narrowed eight-job rollout. On 2026-10-13 the user explicitly excluded external application migration from DevOps-893. CI preparation is complete locally; publication awaits reviewed approval. See [current publication record](2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md).

- Repository provisions Nomad jobs and Consul KV, not cloud VMs.
- Proposed target: `vk-test/`, separate Consul state `terraform/vk-test`.
- Recommended CSI candidate: OpenStack Cinder; VK compatibility requires a disposable-volume smoke test.
- Fresh disks and buckets are allowed; no cross-cloud data migration is required.
- Audit found external CSI consumers, including BuildAPI MongoDB, outside this repository.
- Rename environment URLs, datacenters, KV placement, CI environment and provider/backend endpoints together.
- Loki/Tempo also depend on Yandex S3; Mimir takes S3 settings from a shared Vault secret.
- Existing CI auto-applies on master; bootstrap VK through explicitly approved stages.
- Nomad/Consul VK readiness and actual client capacity still require live read-only verification.
- Secret requirements and deployment stages below are a proposal, not applied configuration.

## Context

Implementation approval October13: user explicitly approved branch `DevOps-893-recover-nomad-on-vk` in `/home/slnnk/git/terraform` from `origin/master`; created from freshly fetched master34b581b. User requires a separate `vk-test/` root and corrected the backend path to **`terraform/vkcloud-terraform`**. Earlier `terraform/vk-test` proposals below are superseded. Initial local root contains only Traefik, with Nomad provider2.3.1 and3 allocations matching existing source. No deployment/publication approval given. Two init escalation prompts were interrupted before execution; successful initialization is not claimed.

Follow-up verification: [VK access check](2026-10-13-nomad-test-devops-893-vk-access.md) confirms the proposed Nomad/Consul/Vault service endpoints, DC `vk-test`, eight ready/eligible clients and an empty default namespace. User supplied local variables `VK_TEST_VAULT_TOKEN`, `VK_TEST_NOMAD_TOKEN`, `VK_TEST_CONSUL_TOKEN`; these supersede earlier operator-variable assumptions for this task. Proposed GitLab variable names below are not yet created or finalized. Separate nonsecret address map: [service-addresses.env](../../service-addresses.env). Remaining preflight includes capacity, registry, Nomad→Vault integration and application secrets.

YouTrack GET returned the task above, In Progress, no description, sprint 197. Repository is clean on `DevOps-696-test-metrics`; default remote branch is `origin/master`, origin `git@gitlab.youdo.sg:sysadmins/terraform.git`. No project AGENTS. Proposed implementation branch: `DevOps-893-recover-nomad-on-vk` from freshly checked `origin/master`, in the existing checkout. Branch proposal has NOT been approved; no repository edits or git mutations performed.

Known VK Vault address from Jenkins recovery notes: `http://vault.service.vk-test.consul:8200`; local access variable `VK_VAULT_TOKEN` in `current/.env`. Proposed Nomad/Consul endpoints `http://nomad.service.vk-test.consul:4646` and `http://consul.service.vk-test.consul:8500` and datacenter `vk-test` are hypotheses until live verification. Local Vault access does not establish Nomad server integration or job policy readiness.

## Actions

Ran daily `ai-sync.sh` (no reminders). Read task through the existing YouTrack helper's GET client, inspected repository and relevant KB notes read-only through a delegated audit, and checked primary upstream documentation. No external writes.

Useful inspection commands: `git status --short`, `git branch --show-current`, `git symbolic-ref refs/remotes/origin/HEAD`, `git grep -n yandex-test`, `rg 'secret |policies|storage.yandexcloud.net' yandex-test templates`.

## Proposed architecture

Adapt the existing test root to `vk-test/`; keep production resources outside the recovery apply. Preserve existing job behavior except required provider, address, secret and CSI changes. Register Cinder as proposed Nomad plugin ID `vk-csi`; upstream driver identity is `cinder.csi.openstack.org`. Start with the existing monolith/system pattern on eligible VK clients, using `csi_plugin.type = "monolith"` and a matching socket/mount path. Controller/node separation is an alternative if runtime tests reveal an operational need; it is not a prerequisite refactor.

Use a pinned released `registry.k8s.io/provider-os/cinder-csi-plugin:<verified-release>` image and record its digest after checking pull access and Nomad compatibility. Do not use `latest` or copy an old pack's version blindly. Pass `--endpoint=unix://<matching-mount-dir>/csi.sock`, `--cloud-config=<rendered-secret-path>`; configure metadata lookup from the actual VK VM identity, never Nomad node UUID. Match Cinder/Nova availability zones and permitted volume types from the actual project.

Primary sources: [HashiCorp Nomad Cinder integration](https://developer.hashicorp.com/nomad/integrations/hashicorp/csi-openstack-cinder), [upstream Cinder configuration](https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/cinder-csi-plugin/using-cinder-csi-plugin.md), [VK blockstorage volume resource](https://github.com/vk-cs/terraform-provider-vkcs/blob/master/docs/resources/blockstorage_volume.md). HashiCorp documents OpenStack VM requirements and privileged node containers. Upstream documents Keystone/Nova/Cinder and metadata configuration. These establish the driver candidate; they do not prove this VK deployment works.

## Deployment plan

1. **Read-only preflight.** Verify VK Consul DNS/quorum/datacenter, Nomad leader/versions/client readiness, Vault integration/policies and registry access. Inventory jobs and volumes, including external job sources such as BuildAPI. Confirm no already running job would be overwritten by a fresh Terraform state; reconcile existing ownership before any apply. Record project/region, VM UUIDs, Nova/Cinder AZs, disk types/quota, attach limits and metadata accessibility from plugin containers. Check at least three eligible clients for Traefik ports 80/8080, total reservations and allocation storage.
2. **Approve implementation branch; adapt local files.** Proposed branch `DevOps-893-recover-nomad-on-vk`, repository above, base `origin/master`. Move the test root to `vk-test/`, update `.gitlab-ci.yml`, all active test URLs/datacenters/Consul KV and relevant shared template inputs. Replace CSI image/auth/template/plugin ID. Use separate state path `terraform/vk-test`; initialize without migrating Yandex state. Configure VK CI ACL variables and initially manual VK apply. Preserve existing unrelated roots. Review the two production Alloy references as a separately disclosed change; no production apply in this task's VK rollout.
3. **Prepare prerequisites and secrets.** Verify/copy required secret schemas into target Vault, authorize job policies, verify Docker pull credentials on clients. Select reachable S3 endpoints and fresh buckets/prefixes for Loki/Tempo/Mimir; avoid modifying shared source secrets or reusing production bucket prefixes. Verify OAuth callback registration, VK DNS and ingress routing. External secret, bucket, identity, DNS and server changes require explicit approval per action.
4. **Static checks and review.** Run `terraform fmt -check`, initialization for the approved target backend and `terraform validate`; render and validate the changed Nomad jobs without logging rendered credentials. Run `terraform plan` against VK and inspect every create/update/destroy and CI effect. Check active test source has no `yandex-test` URLs/DCs and all endpoints resolve from their actual callers. Repository publication uses the supervised second-stage approval; it does not authorize deployment.
5. **Deploy CSI first after approval.** Apply only the reviewed CSI bootstrap resource, or use an explicitly reviewed equivalent job submission, with a reviewed isolated plan. Verify `nomad plugin status vk-csi`, healthy nodes/controllers and driver identity. Create a disposable fresh Cinder volume after approval; register/create it with `plugin_id = "vk-csi"`, `external_id` equal to the Cinder volume UUID when registering an existing disk, file-system attachment and `single-node-writer`. Write a marker, stop/unmount, reschedule to another eligible client, read marker and verify clean detach/reattach. Never test using existing application disks. Each runtime mutation needs the applicable explicit approval. Smoke-volume cleanup is a separately reviewed action.
6. **Deploy routing and basic jobs after approval.** Apply reviewed Traefik, OAuth, Selenoid GGR/iOS, stand/autotest Redis and Baget resources in dependency order. Verify images, service registrations, health checks, DNS, OAuth login and registry/NuGet access. Selenoid routers require healthy external browser/iOS backends; empty Redis is expected under the user's instruction.
7. **Deploy telemetry after approval.** Bring up reviewed VictoriaMetrics and exporters, Mimir, Loki, Tempo, Grafana and Alloy only after their secrets/S3 destinations exist. Verify an actual metric, log and trace reaches the VK target, Grafana datasources/auth work and no VK pipeline sends data to Yandex test inadvertently. Leave currently commented Jaeger, index-cleaner and Filebeat jobs disabled; do not activate unrelated functionality. Check Mimir and Victoria persistence semantics explicitly; empty-data permission is for bootstrap and does not silently approve data loss on every restart.
8. **External CSI users and acceptance.** Inventory and adapt external job sources under their own scope/branch approvals; create new VK volumes and update plugin IDs and disk UUIDs. Acceptance: reviewed desired jobs healthy, no blocked evals from capacity/volumes, no obsolete test URLs in active sources, fresh-volume detach/reattach passed, UI/OAuth/telemetry paths work, final full Terraform plan converges. Manual ingress/runtime release still requires approval. Record final endpoints, job list and any deferred consumers.

At each deployment stage use a freshly reviewed saved plan where practical. If bootstrap requires selective resources, explicitly disclose target addresses and follow with a complete plan; do not treat a partial plan as full convergence.

## URL and environment change inventory

| Location | Required treatment |
| --- | --- |
| `yandex-test/main.tf` | Consul backend address/DC/path and Nomad/Consul provider endpoints; new VK state |
| `yandex-test/{nomad,monitoring,consul}.tf` | Job/module DCs, Consul KV target, environment root references |
| Test jobs/configs, 26 of 28 files | `*.service.yandex-test.consul` to verified VK services; `*.yandex-test.youdo.local` to VK DNS/routes; Grafana root/domain/email, Selenoid status, Alloy forwarding, monitoring targets |
| `.gitlab-ci.yml` | root paths, environment name, provider tokens, plan/apply dependency names, apply rules |
| `production/jobs/alloy-traces.hcl:197,205` | Review the two cross-environment test-domain routes; explicitly disclose production behavior effects and keep production deployment separate |
| `yandex-test/configs/loki.yml:91`, `jobs/tempo.hcl:130` | `storage.yandexcloud.net` is a distinct storage endpoint, not a test-suffix replacement; configure verified destination/buckets |
| Shared Mimir template + target Vault | Inspect S3 endpoint/buckets schema at `secret/resources/mimir` without printing values; isolate target storage |
| External integrations | VK DNS/ingress, OAuth redirect URLs, dashboards/datasources, deploy tooling and CSI consumers |

Preserve shared identity/public URLs such as `auth-tech.youdo.com`, `.youdo.sg`, `.youdo.corp`, `.youdo.com` unless they specifically point to the test environment. Changing all test URLs does not mean inventing new shared identity services. Inspect full matching lines before bulk substitution; disabled config also needs corrected test addresses if retained.

## Secrets required and change locations

| Requirement | Location and proposed change |
| --- | --- |
| Terraform Nomad ACL token | GitLab project Settings → CI/CD → Variables: add `NOMAD_TOKEN_VK_TEST`; change `.gitlab-ci.yml` mappings from `NOMAD_TOKEN_YANDEX_TEST`. Scope to target namespace/jobs |
| Terraform Consul ACL token, including state access | Same location: `CONSUL_TOKEN_VK_TEST`; change CI mapping. Grant target state path and required KV/service read/write rights only |
| VK OpenStack CSI authentication | Proposed target Vault `secret/vk/csi`, replacing CSI's `secret/yandex/csi`; auth URL/region/project/domain identifiers plus password or supported application credentials. Render `cloud.conf` into allocation secrets, not GitLab artifacts or Terraform state |
| CSI Vault policy | Current CSI requests `yandex`. Proposed target policy `vk-csi` permits reading the exact CSI secret path. Match Vault KV version and Nomad integration; policy creation and server configuration are external changes |
| Existing application secrets | Populate target Vault paths/fields requested by active jobs; exact schema inventory below. Reuse secret values only where their backend/service still matches VK, otherwise provision target credentials |
| Loki/Tempo S3 | Existing reference `secret/resources/s3infra-test`; replace target access keys, bucket/endpoint configuration; do not overwrite source shared credentials |
| Mimir S3 | Existing `secret/resources/mimir`; target bucket/prefix and credentials must be checked separately from Loki/Tempo |
| Nomad → Vault integration | Verify on VK Nomad servers; local `VK_VAULT_TOKEN` is operator access only, not proof of server integration. Current job policies must exist in target Vault |
| Docker registry authentication | Verify the existing client Docker/Nomad auth route for `registry.youdo.sg`, Nexus and public CSI image; CSI job changes do not install client registry credentials |

Never print or store secret values in this plan. Record paths, field names and access routes only. Protected/environment-scoped GitLab variables must be available to the approved pipeline/branch. Do not assume a protected variable is usable from an unprotected task branch.

### Exact source-derived Vault schema

These paths are requested by source templates. Target Vault contents were not queried.

| Vault path | Required fields | Policy and source |
| --- | --- | --- |
| `secret/monitoring/grafana/postgres` | `user`, `password`, `database` | `monitoring`; `yandex-test/jobs/grafana.nomad:37` |
| `secret/monitoring/grafana/oauth` | `client_id`, `client_secret` | `monitoring`; same file:47 |
| `secret/monitoring/grafana/ldapreader` | `ldap_user`, `ldap_password` | `monitoring`; same file:66 |
| `secret/oauth2-proxy` | `COOKIE_SECRET`, `CLIENT_ID`, `CLIENT_SECRET`, `REDIS_PASSWORD` | `oauth2-proxy`; `yandex-test/jobs/oauth2-proxy.nomad:31,92` |
| `secret/resources/s3infra-test` | `access_key`, `secret_key` | `resources`; `yandex-test/configs/loki.yml:90`, `jobs/tempo.hcl:131` |
| `secret/resources/mimir` | `endpoint`, `bucket_name`, `bucket_name_ruler`, `access_key_id`, `secret_access_key` | `resources`, `monitoring`; `modules/mimir/templates/mimir.yaml.tpl:62,83` |
| `consul/creds/monitoring` | dynamically issued `token` | `monitoring`; Mimir template:12,31,42,79; `modules/victoriametrics/templates/vmalert.nomad.tpl:142` |
| `secret/monitoring/alloy-cloudwatch` | `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_REGION`, `AWS_ENDPOINT_URL` | `monitoring`; `modules/alloy/alloy.nomad.tpl:61` |
| Current `secret/yandex/csi` | obsolete `YANDEX_AUTH_KEYS`, `YANDEX_FOLDER_ID` | `yandex`; replace in `yandex-test/jobs/csi-plugin.hcl:30` with proposed `secret/vk/csi` and OpenStack schema |

For proposed `secret/vk/csi`, define `auth_url`, `region`, `project_id`, `username`, `password`, `user_domain_name` and applicable project-domain field for the selected authentication method; render them as the pinned driver's `[Global]` configuration keys (`auth-url`, `region`, `tenant-id`, `username`, `password`, `domain-name` and applicable project-domain key). Prefer verified project UUID over project-name ambiguity. If using application credentials, first verify VK support and replace username/password keys with the exact pinned driver's application credential keys; do not assume support. Nonsecret identifiers still belong beside secret auth configuration for consistency.

Configure the Vault Consul secrets engine/role behind `consul/creds/monitoring` for VK Consul; copying a previously issued token is insufficient. Verify policies `monitoring`, `resources`, `oauth2-proxy` and proposed `vk-csi` in target Vault. Grafana also needs a reachable Consul-registered PostgreSQL service/database, and OAuth/LDAP need reachable identity backends.

CI must export `NOMAD_TOKEN` from `NOMAD_TOKEN_VK_TEST` and **`CONSUL_HTTP_TOKEN` from `CONSUL_TOKEN_VK_TEST`**, while supplying the latter to backend `access_token`. Existing YC CI supplies Consul credentials only to the backend, whereas the Consul provider has no explicit token. No Vault provider is declared; Terraform does not require an administrative Vault token just to submit these jobs. Existing static monitoring basic-auth source values need backend consistency review without printing/copying them; unrelated secret cleanup remains separately scoped.

## Findings

`nomad.tf` enables Traefik, GGR/iOS, CSI, 18 stand Redis instances and 3 autotest Redis, Jaeger agent, OAuth, Baget and Alloy traces. `monitoring.tf` enables Alloy, Mimir, VictoriaMetrics, Grafana, Tempo, Consul exporter and Loki; Loki rules are Consul KV. Jaeger/index cleaner and Filebeat declarations are commented out.

Reservations include Redis 21 GiB, Tempo 4 GiB, Loki 2.5 GiB, Traefik roughly 3 GiB on three clients, Victoria storage 4 GiB and agent 3048 MiB, Mimir 2 GiB, plus other jobs and CSI per-client 500 CPU units/256 MiB. These are configuration reservations, not measured utilization. Aggregate eligible capacity remains unknown. Victoria storage uses `/data` and ephemeral disk settings without a persistent mount in the inspected source.

No `nomad_volume` or CSI consumer definitions were found in this repository. The [BuildAPI attachment incident](2026-09-13-nomad-test-buildsinfo-csi-stale-attachment.md) demonstrates external consumers. Fresh VK volumes must not reuse Yandex disk IDs or import Yandex state.

## Changes

Only KB records changed: this plan, a new nonduplicate Nomad test map, repository registry, live backlog and sync summary. No source edits, Terraform initialization/plan/apply, Nomad submissions, secret updates, branch changes or publication.

## Risks and rollback

Stop a stage on unhealthy CSI, wrong state ownership, missing secrets, insufficient capacity, mismatched AZs, unreachable S3 or wrong routing. Roll back only reviewed VK jobs/config versions and routes after approval. Keep newly created disks/buckets until their disposal is separately approved. Yandex availability is not assumed, so reverting DNS to Yandex is not a guaranteed recovery route. Do not destroy/reset state or delete shared storage as rollback.

## Status

Plan prepared; live validation, secret provisioning, branch approval, implementation, publication and deployment remain unperformed. Track remaining work in `~/ai/TODO.md`.

## Portable lesson

none
