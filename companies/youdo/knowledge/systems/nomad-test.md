---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, consul, terraform, vk-cloud, recovery]
---
# Nomad test platform and VK recovery

## Summary

- DevOps-893 restored the Terraform-managed test services in VK Cloud and was closed by the user on2026-10-13.
- Repository: ~/git/terraform, approved branch DevOps-893-recover-nomad-on-vk.
- Separate root vk-test; Consul state terraform/vkcloud-terraform.
- Eight ready clients; deployed Traefik3/3, Redis16/16 and Jaeger8/8.
- Consul exporter, Kafka Schema Registry and Alloy traces are deployed and checked.
- Current endpoints and observation evidence live in current/service-addresses.env.
- User excluded test16/test17, redis-autotest and unused local job files.
- All3master Vault tokens were synchronized from secret/ansible/yandex and reloaded.
- Fresh master-token checks200; main Alloy8/8running verifies task Vault startup/rendering.
- All8configuredjobs deployed; CSI8healthy nodes/controllers after command correction.
- SSD lifecycle verified: ceph-ssd 1 GiB, ext4, write/read SHA-256, detach and delete; no temporary resources remain.
- Older paragraphs below retain historical recovery findings; dated updates supersede them.
- Deployment evidence, approvals and limitations are in the linked work logs.

## BuildAPI Kubernetes recovery follow-up (2026-10-14)

User requested BuildAPI restoration in VK Kubernetes rather than the historical Nomad CSI job. Existing cluster access and private Terraform-identity CI kubeconfig are verified; no BuildAPI deployment has occurred at this checkpoint. See [BuildAPI access and CI image preparation](../log/2026-10-14-dev-deployment-devops-898-buildapi-vk-kubeconfig.md).

## DevOps-898 final approved launch completed (2026-10-14)

Ten single services and the explicitly limited LogReader test5 pilot are deployed through GitLab and runtime-verified: doc-generator master-137, DebuggingEvents 1.0.85, geocoder 1.2.12, call-service 0.0.9, chat-content 1.1.16, textvalidation 1.0.4, tinkoff 0.0.10, blec 1.0.2, pechkin 2.14.24, mailer 8.1.10 and LogReader 1.0.39. Service allocations run with expected versions; configured health checks pass where defined. Blec has no configured health check and its root route returns 404. LogReader has exactly one test5 group, HTTP 200, passing Consul and verified SQL SELECT 1 using its HCL Vault credentials. Test5 Consul SQL endpoint alone was updated by approved CAS. Other fifteen SQL stands remain a separate backlog dependency; full sixteen-stand acceptance is not claimed.

Socket is per stand and excluded from this rollout after the user's correction; reverse MR !82 merged into master 7f6d81b3 restores its original CI. User excluded unused vks-policy-generator and explicitly closed MR !18 without merge, new tag or deployment. Optional chat cache changes were not implemented; its new release build succeeded. Public-test remains unchanged. No YouTrack closure was performed. [Final launch versions, evidence and limits](../log/2026-10-14-nomad-test-devops-898-implementation.md#verified-final-launch-scope-2026-10-14). Historical progress sections below retain their dated observations.

## DevOps-898 GitLab rollout and Socket scope correction (2026-10-14)

Doc-generator is deployed through GitLab job 3226189 from pipeline 140895 with image `master-137`; Nomad job version 1, running allocation, Consul checks and configured HTTP health check pass. Its separately authorized production child pipeline 140898 succeeded. DebuggingEvents API and companion Elasticsearch are running from the initial approved direct deployment; TCP checks pass and Elasticsearch is green. GitLab deployment verification for DebuggingEvents remains pending.

Nine authorized release pipelines 140901–140909 cover geocoder, call-service, blec, mailer, LogReader, chat-content, tinkoff, vks-policy-generator and pechkin. Seven have ready manual VK jobs, no production jobs are active. Chat-content timeout and vks-policy-generator buster apt failures remain unresolved. Nexus nginx now whitelists VK gateway `10.18.20.3/32`; test/reload passed, observed HTTP 429 stopped and fresh NuGet restores pass.

The user requires Socket deployment per stand and cancelled its dynamic-mode change. Approved reverse branch `DevOps-898-restore-per-stand-socket-deploy` restores the original CI byte-for-byte; publication and merge remain pending. Remote Socket master still contains MR !81. The general manual-master shared-template proposal was rejected. Textvalidation local production-rule overrides were cancelled with no publication; explicitly requested new tag `1.0.4` was created at master `1fa42397` for standard manual release CI, with pipeline results pending. Public-test remains excluded. RabbitMQ retains old credentials on its new VM; other fifteen SQL stands still prevent full LogReader acceptance. [Current implementation and approvals](../log/2026-10-14-nomad-test-devops-898-implementation.md).

## Single and dynamic configuration merged; build preparation (2026-10-14)

DevOps-898: all four approved MRs merged (templates !88/master cda625bd, Socket !81/master 8b3912d8, DebuggingEvents !8/master 642d8dfa, textvalidation !37/master 1fa42397). Five CI lint checks passed, including preservation of Socket public-test behavior. RabbitMQ 3.8.34 runs with the old Vault login/password and 17 vhosts; Consul DNS and checks pass. Approved Vault endpoint changes preserve other fields. Test5 logging credentials passed SELECT 1. All 21 approved preparation retries are terminal: 13 set-variables and two prepare-nuget succeeded; six prepare-nuget failed with HTTP 429 under investigation. Seven separately approved release/master build jobs (3226175–3226181) are running. Application images and deployment are not yet verified. [Implementation](../log/2026-10-14-nomad-test-devops-898-implementation.md), [build evidence and approvals](../log/2026-10-14-nomad-test-devops-898-service-build-retries.md).

## Single and dynamic implementation start (2026-10-14)

DevOps-898 user-approved Docker auth applied to8VKNomadclients using the existing shared-role snapshot (MR1371source); no restarts. Authenticated NexusGET200verified8/8; registry auth retained. Rabbit10.18.26.7 is an empty VM; user clarified old login/password must be reused on new machine, no datastore migration inferred. Four task branch approvals pending, no app builds/deployments. test5YouDoLogsExceptions login/SELECT1verified with existing Vault credentials. [Implementation and approvals](../log/2026-10-14-nomad-test-devops-898-implementation.md).

## Single and dynamic service preflight (2026-10-14)

DevOps-898 live preflight verified8readyclients/24jobs/62runningallocs and ample scheduler headroom. User-approved NOMAD_TOKEN_VK_TEST/CONSUL_TOKEN_VK_TEST copied into GitLab youdo; both API200 and masked/unprotected/scope* verified. Docker runner105/106host connectivity passes; no fresh container-network test. All8clients lack Nexus auth;20expected app component manifest/tag checks show no ready images. Copied RabbitMQ address and shared logging SQL configuration remain Yandex; candidate VK RabbitMQ5672refuses. mssql-test5 accepted producer is running/passing at10.18.26.35:14305; LogReader consumes per-stand Consul server keys. DebuggingEvents has its own companion ES task, correcting the separate-backend hypothesis. No application rollout. [Preflight evidence](../log/2026-10-14-nomad-test-devops-898-preflight.md).

## Single and dynamic service recovery plan (2026-10-14)

Final plan updated after live preflight and13release-pipeline audits: repository configuration/source choices first, single rebuild afterward, then staged deployment with fixed verified tags. User explicitly returned to planning before build execution; no builds launched. Missing Nexus auth/tags and backend dependency blockers are prerequisites; test5SQLproducer accepted/reachable, other15LogReader targets fail. [Final plan](../log/2026-10-14-nomad-test-devops-898-single-dynamic-plan.md).

DevOps-898 scope is11single+2dynamic services from DevOps-A-33. Shared internal-test CI templates will switch to vk-test; public-test is explicitly excluded. Read-only audit found Socket CI mode true despite dynamic HCL and DebuggingEvents hardcoded Yandex Elasticsearch backend; effective app-group CI inheritance and dependency readiness remain execution preflight. Plan only; no repository or runtime changes. [Plan and evidence](../log/2026-10-14-nomad-test-devops-898-single-dynamic-plan.md).

## Large MSSQL refresh migration scope (2026-10-14)

DevOps-897 seven-stage VK adaptation2026-10-14: user requested start, selected ceph-ssd and rejected extra checks absent in legacy. Branch DevOps-897-recreate-large-mssql-on-vk from automation-test-yandex/origin/master0bfc65c; uri cloud tasks/defaults, independent-stage inventory discovery, VK backup UNC and three large stand endpoints locally adapted. Fixture5cases/syntax/diff passed; independent review proposals deferred at user direction. Live step1created base SSD400GiB af3c6ccb-402e-4d2e-9b0b-d1a5fe075842, currently creating; no guest/restore success yet. No Git publication. [Implementation and runtime state](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 manual SQL backup delivery complete2026-10-14: source backup172.24.0.19 /backup/sql/test/CleanYouDo.bak copied to VK share10.18.26.4 /public/sql/CleanYouDo.bak,96708001792bytes/90.1GiB, file date2026-10-11MSK, mode0644; source/destination size+mtime match, source unchanged, temporary file absent, Samba active,129GiB free. User explicitly skipped checksum; no hash verification. This supersedes in-progress statements below. Image active400GiB prerequisite confirmed; guest boot/restore and DBA_Clean/UNC migration remain separate. [Delivery result and user scope correction](../log/2026-10-14-nomad-test-devops-897-mssql-vk-preflight-and-backup.md).

DevOps-897 image preflight2026-10-14: VK yc-sql-base d840325b-16fd-4ff9-943d-9599b6bbf495 active/private, Windows metadata, virtio/BIOS, raw400GiB/min_disk400; no guest boot verified. STD3-4-8/STD2-4-8 flavors match historical4vCPU/8GiB, aggregate headroom sufficient for temporary+3stand400GiB disks. VK /public/sql backup path initially absent; source CleanYouDo.bak90.1GiB dated2026-10-11 verified on ES source backup172.24.0.19. User-authorized manual copy is running to share10.18.26.4 via temporary file and checksum-before-publish. DBA_Clean producer still targets Yandex10.16.28.4 in tracked code; restore procedure still old10.16.26.4. [Preflight and delivery evidence](../log/2026-10-14-nomad-test-devops-897-mssql-vk-preflight-and-backup.md).

DevOps-897 DNS publication complete2026-10-14: user-approved commit06d4821a pushed and [MR1374](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1374) created; user merged as master454ef804. Remote description/path/SHA and fetched master DNS rule verified. Pipeline140836 skipped, no agent merge/deployment. This supersedes DNS publication-pending statements below; the larger MSSQL migration remains separate. [Publication evidence](../log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md).

DevOps-897 persistence prepared2026-10-14: approved task branch DevOps-897-fix-nomad-private-dns from automation-services/origin/master71c37b2f, one-line client variable fix applied/checks/review passed, Git publication pending. All3Nomad masters already use working systemd-resolved10.18.20.3, no dnsmasq installed; DNS verified11/11across8repaired clients+3unchanged masters. Authorized branch-switch conflict in unrelated main.tf comment resolved preserving user's local version and excluding it from task staging. [Latest implementation/approval evidence](../log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md).

DevOps-897 Nomad DNS fixed manually2026-10-14: all8clients route mcs.local through IPsec/BIND10.18.20.3 instead of unreachable direct VK DNS10.18.20.65; dnsmasq active and local/private/Consul/system lookups verified8/8. Neutron identifies .65 as network:dns service port in shared_network, also IP10.18.26.252 (not queried). Master Ansible still has direct .65 rule; minimal one-line artifact prepared, task branch approval pending. Pilot backup-in-conf-dir mistake briefly stopped agent01 DNS, corrected before other clients. This supersedes earlier unresolved timeout and built-in-DNS characterization of .3. [Repair evidence and approval state](../log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md).

VK private DNS checked on running VMs2026-10-14: domain mcs.local; resolver10.18.20.3 returns Jenkins controller/agent A records10.18.26.8/.26. Default DNS on Jenkins controller works. Nomad agent01 can resolve through direct @10.18.20.3 queries, but its default local dnsmasq10.18.26.34 times out for these mcs.local names; no root cause/fix performed. SQL registration and recreation propagation remain unverified. [Live DNS evidence](../log/2026-10-14-nomad-test-devops-897-vk-private-dns-check.md).

DevOps-897 covers adapting automation-test-yandex large MSSQL refresh to VK Cloud. Historical committed seven-stage weekend workflow creates sql-base (disk yc-sql-base) from yc-sql-service-os01, restores backups, publishes image yc-sql-base, then replaces sql-test/sql-test1/sql-test6 with disks yc-sql-test/yc-sql-test1/yc-sql-test6. Large/thick deployment restarts Windows MSSQLSERVER and separately resets SQL database snapshots; small/thin Nomad deployment is excluded from this task. Exact AWX schedule/workflow settings remain unverified. Historical names are distinct from existing uncommitted DevOps-889 Yandex recovery edits; no DevOps-897 repository/runtime changes or branch approval yet. [Investigation evidence](../log/2026-10-14-nomad-test-devops-897-large-mssql-legacy-workflow.md).

DevOps-897 user naming decision2026-10-14: use vk-ms1 for VM/disk/image names: vk-ms1-sql-base and vk-ms1-sql-test/test1/test6; prepared output image vk-ms1-sql-base. User reports an existing VK image named yc-sql-base (not independently checked); its current name is distinct from the selected output name. No resource rename or implementation is implied. [Decision evidence](../log/2026-10-14-nomad-test-devops-897-large-mssql-legacy-workflow.md).

## Purpose

Nomad test platform services, Consul configuration and telemetry managed by `sysadmins/terraform`. VK recovery under DevOps-893 permits fresh empty data. This map records verified source behavior; proposed VK runtime details are explicitly unverified.

## Components

After user edits and explicit cleanup, vk-test/jobs contains only seven actively referenced files: Traefik, Redis, Jaeger agent, CSI, Alloy traces, Kafka schema registry, Consul exporter. Eleven inactive job files removed locally; user-edited nomad.tf preserved. Original Yandex root unaffected.

VK-specific user scope corrections: Redis only for test,test1–test15; omit test16/test17 and redis-autotest. Existing Yandex source retains its original configuration. Next saved Redis plan is16 groups/16GiB, not yet applied.

- `/home/slnnk/git/terraform`: test Nomad jobs, monitoring modules and Consul KV. No cloud VM provisioning or registered CSI volumes in inspected source.
- Traefik, OAuth proxy, Selenoid GGR/iOS, 18 stand Redis and three autotest Redis, Baget, Jaeger agent, Alloy, Mimir, VictoriaMetrics, Grafana, Tempo and Loki.
- External job repositories consume CSI volumes; BuildAPI MongoDB historically uses `yc-csi-buildsinfo`.

## Delivery path

October13 [local preparation](../log/2026-10-13-nomad-test-devops-893-vk-traefik-preparation.md): all28 tracked environment files copied as-is into vk-test with target substitutions and necessary Cinder conversion. Source active/commented state preserved from34b581b. Init and validate passed; saved targeted Traefik plan1add/0change/0destroy awaits apply approval. No CI or runtime changes.

DevOps-893 final user-approved target layout: separate `vk-test/` root, Consul backend path `terraform/vkcloud-terraform`. This supersedes the earlier proposed `terraform/vk-test`. Approved branch created from freshly fetched origin/master34b581b; Traefik is locally prepared first, not deployed.

GitLab CI validates/plans/applies environment roots. Existing `yandex-test` auto-applies on master and applies manually on other branches. Proposed recovery root `vk-test` must initially deploy through approved manual stages and separate Consul state `terraform/vk-test`, without migrating Yandex state.

## Control points

Existing CSI job `yandex-test/jobs/csi-plugin.hcl` deploys Yandex driver v0.10.0, privileged monolith plugin `yc-csi`. Proposed replacement is OpenStack Cinder with Nomad ID `vk-csi`; compatibility requires a disposable-disk mount/detach/reattach test on VK. At least three clients are needed for current Traefik static port placement; Redis alone reserves 21 GiB.

## Operations

Corrective CSI apply approved/completed:8tasksrunning, provider cinder.csi.openstack.org,8/8healthy nodes andcontrollers. All current jobs deployed. CSI disk create/attach/mount/detach operations have not been exercised; no disks/volumes created. Full Terraform convergence check pending final result. Map records local-socket-only plugin status.

CSI initial approved apply registered systemjob but8/8tasks failed. Stderr unknown-endpointflag in /go-runner; source image CMDbinary was displaced by Nomadargs. Verified binary/bin/cinder-csi-plugin, added config.command locally, updatedplanawaitsapproval. All7otherjobs running38activeallocations. [Diagnosis](../log/2026-10-13-nomad-test-devops-893-vk-csi-deployment.md).

Main Alloy approved/applied1add and healthy8/8; every direct readiness/metrics endpoint200. Job starts with monitoring Vault policy and mandatory secret template, verifying restored Nomad→Vault task integration. Shared module unchanged. Map updated with dynamic perclient ports. Only CSI remains undeployed pending cloud credentials/secret/policy and approval. [Evidence](../log/2026-10-13-nomad-test-devops-893-vk-alloy.md).

Alloy traces approved/applied and running on10.18.26.37:28760, OTLPregistration30254. Direct readiness/metrics200; end-to-end delivery untested. Map updated. Remaining active scope: main Alloy module and CSI, with shared Vault credential repair and CSI cloud credentials still required. [Deployment evidence](../log/2026-10-13-nomad-test-devops-893-vk-alloy-traces.md).

Kafka Schema Registry approved/applied and healthy: one allocation running on10.18.26.34:31264, Consul passing, /subjects200empty. Address map updated. Alloy traces is next; unused Vault declaration removed locally because no secrets are consumed. Shared Vault repair remains required for main Alloy module and CSI.

Consul exporter corrective apply completed after approval: one active allocation running, Consul HTTPcheck passing, /metrics200 and consul_up=1 at10.18.26.35:28270. Removed only unused Vault declaration; common Nomad→Vault token remains broken. Map updated. Next Kafka Schema Registry plan ready with VK Kafka DNS correction, not deployed.

Consul exporter initial approved apply registered job but allocation failed: Vault token derivation403invalid token, no service registration. Job has no secret dependencies; unused monitoring Vault block removed locally. Updated targeted plan1change awaits approval. Shared Nomad→Vault credential remains broken for jobs that need secrets. [Failure and fix proposal](../log/2026-10-13-nomad-test-devops-893-vk-consul-exporter.md).

Jaeger agent approved/applied1add0change0destroy;8/8allocations running and registrations present on8clients. Job has no application health checks; trace delivery not tested. Address map updated. [Deployment and cleanup evidence](../log/2026-10-13-nomad-test-devops-893-vk-jaeger-agent-deployment.md).

Redis deployed after explicit approval:16/16 allocations running and cache TCPhealth passing for test,test1–test15, ports1900–1915. Runtime endpoints recorded in service-addresses.env. [Deployment evidence](../log/2026-10-13-nomad-test-devops-893-vk-redis-deployment.md). Next Jaeger agent plan prepared, not applied.

First VK deployment completed after explicit user approval: traefik2-service3/3 allocations running; proxy and proxy-ui passing on10.18.26.30/.10/.21:80/8080. Addresses added to service-addresses.env. Redis test-stand plan is next; no other services deployed yet.

October13 [preflight](../log/2026-10-13-nomad-test-devops-893-vk-preflight.md): eight clients have ample free resources and ports; metadata UUID/AZMS1 available. Basic secret schemas exist, but configured Nomad server Vault tokens return403. CSI secret/policy absent; prom-ruller1.2.2 manifest unavailable; Grafana5433 must change to actual5432. Existing Yandex S3 buckets pass HEAD with target credentials. User stopped additional preflight and chose individual service rollout, starting Traefik then Redis. SSH route is `youdo` plus noninteractive sudo; root authentication fails.

Follow the [DevOps-893 deployment plan and secret matrix](../log/2026-10-13-nomad-test-devops-893-vk-deployment-plan.md). [Live access checks](../log/2026-10-13-nomad-test-devops-893-vk-access.md) verified Nomad/Consul/Vault endpoints, datacenter `vk-test`, management/root tokens and eight ready clients on1.5.3. Default namespace has no jobs/CSI volumes, CSI plugin list is empty, and target state keys do not exist. Full capacity and Nomad→Vault integration remain unverified. Job apply, secret updates, bucket creation, DNS/identity changes and external consumer deployment require reviewed explicit approvals.

Nonsecret address map grouped by datacenter: [service-addresses.env](../../service-addresses.env). API endpoints were contacted directly; other service IPs/ports and health are from Consul catalog.

## Boundaries

Keep production apply outside test recovery. Review the two production Alloy test-domain references separately. Empty bootstrap data does not authorize deletion of existing storage. Preserve disabled jobs and unrelated repositories. Loki/Tempo Yandex S3 dependencies and Mimir shared secret need explicit target configuration.

## Access

CSI final user choice: reuse existing admin Vault policy. Verified its secret/* read rights cover secret/admin/vk-csi; plugin uses policies=[admin]. No separate vk-csi policy publication needed. Targeted CSI plan awaits apply approval.

CSI credentials now stored at user-requested secret/admin/vk-csi, fieldcloud_conf; old secret/vk/csi proposal superseded. User-supplied login/password in current/.env VK_CSI_USER/VK_CSI_PASSWORD; VK_CSI_PROJECT_ID corrected to RCOpenStackUUID. RCsource ~/downloads/nomad-csi-openrc.sh. Plugin references new path; read-only vk-csi policy proposal awaits publication approval. Auth endpoint/region recorded in addressmap; cloud auth not yet tested.

Manual token replacement approved/completed October13: all three Nomad masters now use existing nomad_vault_token from secret/ansible/yandex, synchronized into server.hcl and reloaded bySIGHUP. Token validation and effective config/API200 on all3; Nomad services active. Prior invalid-token statements describe the historical state. Actual task-token derivation will be checked with next approved main Alloy deployment. [Replacement evidence](../log/2026-10-13-nomad-test-devops-893-vk-vault-token-replacement.md).

Fresh October13 master verification: all three /etc/nomad.d/server.hcl files AND effective Nomad configs enable Vault at the correct VK URL with a token configured. The server credentials each return403invalid token. Describe this as configured integration with broken authentication, not missing integration. Nomad API listens on actual10.18.26.11/.12/.13 addresses;127.0.0.1 API probe is not applicable.

VK Vault route: `http://vault.service.vk-test.consul:8200`. User-supplied verified operator variables in `~/ai/current/.env`: `VK_TEST_VAULT_TOKEN`, `VK_TEST_NOMAD_TOKEN`, `VK_TEST_CONSUL_TOKEN`. Earlier Jenkins recovery used `VK_VAULT_TOKEN`; do not confuse the names. Nomad server integration still needs verification. Required Vault schemas/policies and proposed GitLab CI variables are in the linked plan; no secret values are stored in notes.

## VK SSD lifecycle verified 2026-10-13

Cinder type=ceph-ssd and availability=MS1 passed dynamic provisioning through vk-csi, 1 GiB ext4 volume, single-node-writer/file-system, mounting at /data, 4 MiB write/read checksum verification, detach and deletion. API verified cloud/Nomad volume absence and completed/purged test job. No permanent resources or Terraform changes. Evidence: [SSD lifecycle log](../log/2026-10-13-nomad-test-devops-893-vk-ssd-lifecycle.md).

## VK CI publication preparation 2026-10-13

Local CI adds automatic plan:vk-test and master-only manual apply:vk-test, with existing inherited group VK Nomad/Consul tokens. CI lint and Terraform validation passed; full plan No changes. Exact publication scope is .gitlab-ci.yml plus17newvk-testfiles, preserving user edits. Commit/push/MR awaits supervised publication approval. External application migration is excluded from DevOps-893 by the user. [Publication preparation and approval record](../log/2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md).

## VK publication 2026-10-13

User approved final CI scope including disabling Yandex test/public-test jobs. Published commit22e451e and [MR440](https://gitlab.youdo.sg/sysadmins/terraform/-/merge_requests/440), targetmaster, no merge/apply. Pipeline140765 running at last observation; plan:vk-test running, existing unrestricted plan:production also included. Description readback exact match; checkout clean.

## VK CI apply verified 2026-10-13

User-run apply:vk-test [job3222681](https://gitlab.youdo.sg/sysadmins/terraform/-/jobs/3222681) succeeded with0add/8change/0destroy. Fresh direct-IP Nomad checks show all eight jobs working,46runningallocations, CSI8/8healthy nodes/controllers. Local Consul DNS currently fails, preventing a post-apply convergence plan; prior CI1.7.5 plan hidden eight updates differed from local1.9.4Nochanges, exact cause unproven. [Evidence and limitations](../log/2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md).

## DevOps-893 closed 2026-10-13

User reported task closure after successful deployment, SSD lifecycle verification, GitLab publication/CI and runtime checks. User waived additional plan convergence verification. The proposed cause of prior CI/local plan differences is differing Terraform versions1.7.5/1.9.4 (hypothesis, not proven). Existing YouTrack work comment74-124648 corrected and verified. No pending work for this task; older convergence caveats above are historical and do not represent required follow-up.

## DevOps-894 Elasticsearch migration plan 2026-10-13

Current working-job preflight2026-10-14: final `dynamic_deploy` Pipeline approved and GET-verified; Jenkins enabled/not quieting down. Minimal ES flags still execute unconditional app stop, monolith deploy and buildsinfo update. Valid `MONOLITH_PIPELINE_ID` and `STATIC_PIPELINE_ID` are required even when `WEB_STATIC=false`; role may rebuild missing artifacts/images. Use an available stand and compatible existing versions. `test5` is verified thin/5GiB; full reset uses `retry(2)`. Runtime acceptance of the working job remains pending. [Preset and limits](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md#working-job-minimal-run-preflight-2026-10-14).

User requested analysis/planning for `automation-test-yandex` and confirmed preserving recreation from prepared data. Current ES deployment clones Yandex thin/thick Compute images after deleting the stand disk. [Plan and source analysis](../log/2026-10-13-nomad-test-devops-894-elasticsearch-vk-plan.md) recommend Cinder snapshots and CSI-managed volume create/delete with `vk-csi`, plus a scoped VK inventory and service domain. Empty-volume lifecycle is already verified; seed import, snapshot restore and ES data validation remain unverified. No repository or runtime changes authorized or made. Proposed task branch is unapproved. This supersedes the October10 Yandex-only ES destination proposal for this VK task.

Producer follow-up: fresh `dba/origin/master` (`37d5330`,2026-10-09) `airflow_dags/mssql_clean_jobs.py` defines Saturday DAG `DBA_Clean`, independently recalled by the user. It reindexes prepared SQL `CleanYouDo`/`YouDo_preseed`, then cold-copies ES data to `10.16.28.4:/data/elastic/{thick,thin}`. Actual source Airflow Connections, destination disk mounts, deployed code and subsequent YC image publication linkage are unverified. Migration should restore this regular preparation chain and publish Cinder snapshots only after data validation; replacing Nomad volume settings alone does not restore the producer.

User identified `10.16.28.4` as Yandex and likely unavailable; outage not measured. Recovery must start from prepared data on the producer's backup source, or regeneration from the prepared SQL datasets, then deliver directly to VK seed volumes. Old destination access and YC disk/image mapping are not prerequisites. Check producer task success and source container state independently of failed copy tasks; no DAG trigger authorized.

User confirmed ES base image refresh ran through the now-unavailable Yandex AWX instance in two stages (corrected three). Repository tags are `delete_image` and `create_image`; historical AWX settings remain unretrieved. Preserve weekly preparation plus playbook/AWX publication when replacing images with Cinder snapshots; do not assume snapshot publication belongs inside `DBA_Clean`. Publish/validate new snapshots before obsolete-artifact cleanup; retain a usable previous version on failure. AWX recovery/configuration changes require separate scope and authorization.

Source check2026-10-13: user screenshot maps `backup_server_prod` to172.24.0.19; SSH confirms `msk3-backup.youdo.corp`. `/backup/sql/elastic/data/nodes` (~21.1GiB) and `/backup/sql/elastic_smalldb/data/nodes` (~130MiB) exist and are mounted by running ES6.8.23 containers `elasticsearch1`/`elasticsearch_smalldb_1`. User waived date relevance for this stage. Exclude the separate2.05GBheapdump from seed transfer, without deleting it. [Read-only source evidence and limits](../log/2026-10-13-nomad-test-devops-894-es-source-check.md); index integrity not checked, no runtime mutations.

VK seed destination2026-10-13: user supplied10.18.26.4, inventoryshare-test01; SSH asyoudo confirms `vk-ms1-share-test01.mcs.local`,~4GBRAM and NOPASSWD sudo. Root key login denied. Existing disks:250Groot,5Gno reported filesystem/mount,40Gext4mounted/public. ES target directories absent. Destination accessible; existing/public usage and cloud volume identity must be established before a reviewed mount/format/copy proposal. No remote changes made. Address map updated with verified host/IP/login and limits.

Later user approval2026-10-13: created `/data/elastic/thin` and `/data/elastic/thick` on root `/dev/vda1` with owner/groupyoudo(1001),0755 and verified writable;239.48GiBfree. These are system-disk staging paths, not standalone seed disks. No transfer/format/container/snapshot action performed. Existing5G/40Gdisks unchanged. Standalone Cinder snapshot publication still requires a reviewed data-volume preparation step.

Transfer-route check2026-10-13, root-only per user: root on172.24.0.19 can reach SSH10.18.26.4 but authentication asroot returns `Permission denied (publickey,password)`. No root credential installation or copying authorized/performed; remote known_hosts unchanged. Source→root transfer is blocked until approved access configuration is supplied or changed.

Later approved key installation2026-10-13: user requested adding backuproot public key toshare. RSA public key appended toshare `/root/.ssh/authorized_keys` without removing existing keys;0600root-owned, exactlyone match. Backup-local `/root/.ssh/id_rsa` with agent disabled successfully authenticates asroot to10.18.26.4 (`id -un`→root,rc0). [Evidence and limits](../log/2026-10-13-nomad-test-devops-894-backup-share-root-key.md). Source persistent known_hosts unchanged; test pinned host key transiently. Data transfer/DAG changes not authorized/performed.

Approved thin transfer2026-10-13 completed:120572815bytes copied to10.18.26.4 `/data/elastic/thin/` with sourcecontainerstopped; checksum/metadata verification no differences, source `elasticsearch_smalldb_1` restarted/runningtrue,rc0. Share has no Docker; target ES boot remains unverified. Thick preflight0deletions,22667132593bytes (~21.1GiB), excludesheapdump; actual thick transfer unapproved. [Transfer evidence](../log/2026-10-13-nomad-test-devops-894-thin-transfer.md).

Later approved thick transfer2026-10-13 completed:22667132593bytes to10.18.26.4 `/data/elastic/thick/`,5342regularfiles, heapdump excluded, checksum/metadata no differences, source `elasticsearch1` restarted/runningtrue,rc0. Bothdatasets now staged onshare rootdisk; no Docker/ES test, Cinder snapshot or DAG/repo change. Temporary size monitor stopped. [Thick evidence](../log/2026-10-13-nomad-test-devops-894-thick-transfer.md).

Seed preflight2026-10-13: existing Cinder `vk-ms1-share-base-thin`5GiBUUIDad66e572-b39a-4ed7-86a6-eb5a094763cb and `vk-ms1-share-base-thick`40GiBUUID6b8a8094-227f-4eb2-968c-5469e98fd92c areceph-hdd/MS1 onshare, sameCSIproject. Thin/dev/vdb has no signatures; thick/dev/vdc ext4mounted/public onlylost+found/noactiveusers. New disks unnecessary. Historical Ansible confirms actualintendedESmounts `/data/elastic/{thin,thick}`, so preserve paths and staging before mounting; current device order is reversed fromoldYandex. Formatting/mount/fstab/fill proposals still unapproved. [Identity/mount evidence](../log/2026-10-13-nomad-test-devops-894-seed-disk-preflight.md).

Later approvedthinformat2026-10-13: ext4,labeles-base-thin,filesystemUUID70806792-9f23-4776-8367-60b857a2c384 verified on5GiBdisk. Stillunmounted; existingthick/public androotstaging untouched. Preparedhelper read-onlypreflight0 for stage-preservingmount/fill andUUIDfstabentries; actualapplyawaitsapproval. [Format/operation review](../log/2026-10-13-nomad-test-devops-894-thin-format.md).

User-approvedfourstepseedpreparation2026-10-13 completed: rootcopies retained at `/data/elastic-staging/{thin,thick}`;5GiBthin/dev/vdb and40GiBthick/dev/vdc ext4 mounted at `/data/elastic/{thin,thick}`;UUIDfstabrows use defaults,nofail,backup `/etc/fstab.devops-894-before-es-seeds`,otherrows unchanged. Bothseedcontents checksum/metadata matchstaging;applyrc0. /publicno longerdedicatedmount. Snapshots/ESstartup unperformed;stagingretained. [Finalmount/fillevidence](../log/2026-10-13-nomad-test-devops-894-seed-mount-fill.md).


Approved seed snapshots 2026-10-13: thin `c249047d-e6c3-4b9f-b78a-a1ceef11c206` (5 GiB) and thick `bb8ea2de-2484-4169-9438-df5352643bd4` (40 GiB) are available/100%, from their verified Cinder seeds. Each filesystem was unmounted during snapshot creation and remounted, UUID checks passed; root staging retained. CSI clone/ES startup remains unverified. [Snapshot evidence](../log/2026-10-13-nomad-test-devops-894-seed-snapshots.md).


CSI ES restore verified 2026-10-13: both retained thin/thick snapshots restored into temporary ceph-hdd 5/40 GiB clones through vk-csi. ES6.8.23 booted with all five indices/five aliases and21activeprimaryshards; index names/UUIDs/docs.count/aliases matched source. Both single-node clusters yellow with27unassigned replicas, same as source. Temporary jobs stopped/purged and clones deleted/cloud+Nomad404; snapshots/seeds retained. This supersedes earlier unverified ES restore statements. Repository/DAG/AWX migration is still pending. [Validation evidence](../log/2026-10-13-nomad-test-devops-894-es-clone-validation.md).


DevOps-894 local playbook adaptation 2026-10-13: user approved branch `DevOps-894-deploy-elasticsearch-on-vk` from automation-test-yandex/origin/master. Scoped inventories/vk_es and ES task paths implement validated Cinder snapshot deployment/weekly publication, preserve Yandex/public-test and AWX tag names. Both entrypoints syntax-check, template parse and11local fixture scenarios passed; review findings corrected. No infrastructure apply or Git publication. DAG destination and unavailable AWX workflow still require separate work. [Implementation evidence and approvals](../log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md).


DevOps-894 explicit scope correction 2026-10-13: ES playbooks now VK-only. Removed legacy YC tasks/template, es_cloud branching and Yandex template fallbacks; public-test bind-mount template preserved with VK API entrypoint. This supersedes the earlier statement that these adapted ES entrypoints retain Yandex behavior. Unrelated MSSQL and other repository code remain outside scope. Syntax/templates and11fixture scenarios rechecked; no live apply or Git publication. [Correction evidence](../log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md).


DevOps-894 fast-deploy correction 2026-10-13: per explicit user instruction, ES deployment now waits only for blocking `nomad job run` success after CSI reset. Removed separate plugin, disk, claim/allocation and ES health checks from the deployment path; only operational CSI delete retry remains. run_es performs no Cinder authentication or snapshot lookup. Prepared snapshot validation remains in the separate publication workflow. Current syntax/template/focused success-failure fixtures pass; no live apply or Git publication. Earlier extensive-deploy-check descriptions are superseded. [Evidence](../log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md).


DevOps-894 actual create_image stage and fast-publication correction 2026-10-13: local AWX entrypoint run succeeded, failed0/exit0, publishing thin5GiB snapshot0d38e5f9-3c42-4923-9e29-4c50bb1de70c and thick40GiB snapshotef5fb5f1-c828-4605-9f1c-81022edd988b; mounts restored and temporary validation resources removed. User then explicitly removed clone/ES validation from future snapshot preparation. Publication now directly marks available snapshots es_published=true; no Nomad/ES checks. This supersedes all earlier claims that weekly publication must validate a disposable clone. Fallback inventory IDs updated to these prepared snapshots, previous artifacts retained, delete_image not run. No live rerun or Git publication. [Run evidence and steering](../log/2026-10-13-nomad-test-devops-894-awx-create-image-run.md).


DevOps-894 fixed-name correction 2026-10-14: per explicit user request, use original delete_image→create_image order and permanent snapshots vk-ms1-share-base-thin/thick. Removed version timestamps, retention, metadata publication and snapshot UUID fallback inventory. Deployment resolves the name to its CSI UUID automatically. This supersedes October13 versioned/publication-metadata design. Local create/delete/full-order fixtures and syntax pass. Existing prepared snapshots still have versioned cloud names; one-time rename helper prepared, awaiting specific approval, no cloud changes this turn. [Correction and pending rename](../log/2026-10-14-nomad-test-devops-894-fixed-snapshot-names.md).


DevOps-894 approved rename completed 2026-10-14: prepared snapshots now have permanent names vk-ms1-share-base-thin (0d38e5f9-3c42-4923-9e29-4c50bb1de70c) and vk-ms1-share-base-thick (ef5fb5f1-c828-4605-9f1c-81022edd988b). Helper exit0 and GET confirms both available. This clears the prior pending-rename condition; fixed-name lookup is usable without recreating data. [Approval/results](../log/2026-10-14-nomad-test-devops-894-fixed-snapshot-names.md).


DevOps-894 timed original-order refresh completed 2026-10-14: user-approved delete_image10.391s, create_image17.112s, total27.503s; both exit0/failed0. Exact permanent names vk-ms1-share-base-thin/thick deleted then recreated, snapshots ready and seed mounts restored. Prior snapshot IDs recorded in rename notes are now deleted/historical. Runtime selection remains by name, no new UUID inventory. No ES checks/clones, retention or metadata publication. Local timings exclude AWX queue/pod startup; no AWX configuration or Git publication. [Timing evidence](../log/2026-10-14-nomad-test-devops-894-refresh-timing.md).


DevOps-894 Nomad-only deployment and test pilot verified2026-10-14: explicit user instruction removed all direct cloud calls from deploy; Nomad/vk-csi create/delete/attach disks. Snapshot chosen via Nomad CSI list by ExternalSourceVolumeID (stable thin/thick seed) and latest ready CreateTime; provider names are empty, no snapshot UUID inventory. This supersedes fixed-name Cinder lookup/direct readiness polling described earlier. First pilot exposed absent-volume deletion handling and creating-disk attach race; fixed existence skip and Nomad reschedule5s with explicit attempts0/interval0. Final Ansible stop_es,run_es test/thick completed0/failed0 in60.037s, existing40GiB disk retained. Configured ES/head URLs recorded, HTTP/DNS not checked. Git publication and DBA_Clean/AWX migration still pending. [Pilot evidence](../log/2026-10-14-nomad-test-devops-894-test-thick-deploy.md), [Nomad-only implementation](../log/2026-10-14-nomad-test-devops-894-nomad-only-deploy.md).


DevOps-894 full reset/manual cleanup 2026-10-14: full run failed145.559s because CSI tried attaching a creating disk; earlier successful stop/run pilot remains distinct. Added Nomad claim-release wait after job purge and external-disk disappearance wait before replacement creation. User requested manual deletion, then explicitly authorized force dropping terminal claims. Cleanup completed: elasticsearch-test job absent, test-vk-csi-es registration absent, backing40GiB disk e963460d-a6f2-42f2-8fc8-42f502b9e417 absent from CSI provider list. Seeds/snapshots retained; no further deployment initiated. Full-cycle repeatability remains unresolved. [Evidence](../log/2026-10-14-nomad-test-devops-894-test-full-cycle.md).


DevOps-894 post-cleanup repeat failed2026-10-14 after125.805s: new disk942a91e9-d525-4df9-8297-2c16ee8b47e0 exists and elasticsearch-test was submitted; attach failed while Cinder creating. These resources have not been cleaned up. Current CSI returns no per-disk available condition (Status empty/IsAbnormal false); plugin healthy and Schedulable true do not prove disk readiness. No further changes applied. [Evidence](../log/2026-10-14-nomad-test-devops-894-test-full-cycle.md).


DevOps-894 readiness correction2026-10-14: user explicitly permitted direct VK Cloud polling. Deployment still creates/deletes through Nomad CSI, but reads ExternalID and polls Cinder until available before submitting job (create_disk/run_es). Existing scoped cloud auth reused; VK_CSI_* credentials required for deploy. Error statuses and retry exhaustion prevent job submission. Three actual Ansible fixtures and syntax-check pass; no live rerun or Git publication. This supersedes the earlier strictly Nomad-only deployment requirement. [Evidence](../log/2026-10-14-nomad-test-devops-894-cinder-readiness.md).


DevOps-894 readiness live verification2026-10-14: approved manual cleanup removed elasticsearch-test and backing disk942a91e9-d525-4df9-8297-2c16ee8b47e0, followed by full Ansible test/thick run with Cinder readiness polling. Three retries until available, then blocking Nomad deployment success; exit0/failed0 in89.680s. Stand is deployed again. This supersedes earlier failed-run/no-live-readiness statements; repeated reset of the now-successful allocation remains unverified. Seeds/snapshots retained. [Evidence](../log/2026-10-14-nomad-test-devops-894-cinder-readiness.md).


DevOps-894 repeat reset verified2026-10-14: user-authorized full test/thick Ansible reset succeeded102.438s, exit0/failed0, without manual force. Job stop→claim release(two retries)→CSI disk deletion→external disappearance(one retry)→snapshot clone→Cinder available(three retries)→Nomad deployment success. This clears the prior successful-allocation repeatability limitation. Two consecutive complete deployments passed89.680/102.438s. [Evidence](../log/2026-10-14-nomad-test-devops-894-cinder-readiness.md).


DevOps-894 requested ES stand batch verified2026-10-14: test1–test7 and test10–test15 all successfully deployed via Ansible. test1/test6 thick40GiB, other11thin5GiB. Initial batch315.412s succeeded12/13; test3healthy_deadline exceeded during task startup/image download, then stop_es,run_es retry succeeded62.088s on existing disk. Final13/13Nomad deployment success; no HTTP/index checks or Git publication. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-stands-batch.md).


ES internal image mirrors prepared2026-10-14: approved base-images branch DevOps-891-mirror-elasticsearch-images from origin/master8759867 contains two digest-pinned FROM Dockerfiles for Elasticsearch6.8.23 and elasticsearch-head/sha-1a888b928135. Existing DevOps-894 thin/thick/public-test Nomad templates now reference corresponding registry.youdo.sg/youdo/base-images targets locally. Template parsing, syntax and focused review pass. No image build/publication or redeployment; do not deploy these local references before release-tag builds. [Evidence/approvals](../log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md).


ES mirrors MR published2026-10-14 after explicit approval: base-images commit2e19eb0, [MR40](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/40), approved branch→master, only two Dockerfiles. No pipelines because builds are tag-driven; no merge/tags/images/deployments. Automation image references remain local pending availability and separate rollout authorization. [Evidence](../log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md).


ES mirror release verified2026-10-14: explicitly approved MR40mergec522f0f and release tags elasticsearch/6.8.23, elasticsearch-head/sha-1a888b928135. Both tag pipelines140808/140809 and jobs3223683/3223684 success. Authenticated manifest-only checks verify both internal images available for linux/amd64. This clears pending-image availability; stand image rollout remains separate, not performed. [Evidence/digests](../log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md).


DevOps-894 all-at-once internal-image rollout verified2026-10-14: authorized13concurrent full resets completed159.555s,11success. test2/test4hit1mhealthy_deadline; container start was35.84/43.30s after allocation, task setup→start0.3–0.4s with no image-download events. Exact pre-run delay origin not established; download is not supported as the primary bottleneck. Concurrent stop/run retries succeeded59.892/61.107s, final13/13Nomad deployment successes. GET all13job configs confirms both internal registry image refs. No Git publication/ESHTTPchecks. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-unlimited-redeploy.md).


DevOps-894 deadline adjustment2026-10-14: user chose healthy_deadline2m/progress_deadline3m; both thin/thick templates updated locally, TCP/min-healthy behavior retained. Nomad parse/diff checks pass. Running jobs not changed; next deployment applies these settings. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-unlimited-redeploy.md).


DevOps-894 all14deadline rollout verified2026-10-14: user-authorized simultaneous full deployment of test/test1–7/test10–15 completed121.790s,14/14exit0 with no retry deployments. test/test1/test6thick40GiB; other11thin5GiB. Templates with internal registry images and healthy2m/progress3m applied; no healthy-deadline misses. Prior pending-runtime-deadline statement superseded. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-all-stands-deadlines.md).

DevOps-894 Jenkins ES integration plan proposed2026-10-14: live dynamic_deploy is an inline Pipeline on linux, checking out automation-test-yandex at AUTOMATION_BRANCH. ES stage still uses legacy dynamic inventory and host limit; proposed scoped VK inventory, explicit instance/type and credentials bindings affect only the ES stage. No Jenkins configuration or repository changes applied. [Proposed plan](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md). User correction (2026-10-14): Jenkins must use test_inventory, currently being restored by the user; separate vk_es inventory is superseded for Jenkins. Verify the restored inventory contract before adapting the playbook/job.

DevOps-894 inventory endpoint correction (2026-10-14): user requested http://dyninv.vk-test.youdo.local; test_inventory.sh now targets it locally. Shell syntax verified; DNS/HTTP unprobed, no Git publication. [Jenkins plan and update](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

## VK dynamic inventory deployed (2026-10-14)

DevOps-896 release-0.56.4 runs API/updater job dynamic-inventory, default namespace, on vk-ms1-nomad-agent-test-06; routed dyninv.vk-test.youdo.local GET200,16stands/64Nomad aliases/0SQL. Clients01-04 represented;05-08 excluded per user. No SQL prerequisite for infrastructure groups. User closed DevOps-896 on2026-10-14 and accepted VK service recovery as complete. Consumer cutover/liveSQL mapping/repeated-refresh observation were not verified in this run; retain these as historical limits, not open requirements of the closed task. Further work requires a separate request. [Deployment evidence](../log/2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md).

DevOps-894 Jenkins preparation update (2026-10-14): user required global group_vars/all.yml and common nomad_token from injected VK_TEST_NOMAD_TOKEN; agent-created inventories/vk_es removed. ES-only Jenkinsfile/XML prepared locally, check mode default and test_inventory stand selection verified against recorded contract. No remote publication/build. Automation cloud credentials come from dynamic-inventory (Vault/Consul), with Cinder permissions still unverified. [Final preparation and checks](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins VK credentials created (2026-10-14, explicit user approval): vk-test-nomad and vk-test-consul are Secret text; vk-test-cloud is the dynamic-inventory automation Username/password. Types independently verified via credential config GET; no job/build yet. Common nomad_token reads externally bound VK_TEST_NOMAD_TOKEN. [Approval and creation evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES test job created (2026-10-14, explicit approval): https://build.youdo.sg/job/dynamic_deploy_es_vk_test/, exact Pipeline/parameters verified, manual-only, RECREATE_DATA=false, zero builds. Task branch publication remains pending before runtime validation; working dynamic_deploy unchanged. [Creation evidence and publication proposal](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

DevOps-894 automation published (2026-10-14, explicit approval): commitd66c21d, [Draft MR104](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/104), taskbranch→master verified, pipelines[]. Jenkins test job can now checkout the published branch; first check-only build approval pending. No merge or build. [Publication evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES test build1 (2026-10-14): user-approved check-only run initially queued due quietingDown=true; user-approved cancelQuietDown verifiedfalse. Build1 failed before Ansible: python3 absent on linux/controller. Local Pipeline fix selects python3 or image-provided python3.8; remote update/check-only retry approval pending. [Build diagnosis and approvals](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES build2/DNS root cause (2026-10-14): approved Python fix worked; build2 failed before Ansible on inventory. Controller ens3 DNS10.18.20.3 knows dyninv record, but resolved only has mcs.local and rejects .local lookup. Proposed runtime addition ~vk-test.youdo.local preserving current search/server awaits approval; no persistent DNS change or build retry. [Exact evidence and prepared helper](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins DNS role and checkbuild3 verified (2026-10-14): user-approved dnsmasq apply on controller10.18.26.8, persistent config/loopback compatibility checks passed. Existing Docker resolver127.0.0.53 now answers dyninv. Jenkins ES testbuild3 SUCCESS, one test5 target, checkchanged0/failed0, no reset. Full reset/Cinder-account validation approval pending; repository integration of controller overrides separate. [Apply/build evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

DevOps-894 fullbuild4 placement failure (2026-10-14): Nomad job Datacenters[yandex-test] vs8readyeligible vk-test nodes. Global all.yml dc overrode raw inventory dc; user-approved local common dc correction tovk-test resolves/renders correctly. Fix publication and build4 stop/full retry pending approval. [Root cause and checks](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES thin/thick verification complete (2026-10-14): build5/test5thin SUCCESS72.115s; build6/testthick SUCCESS100.608s. Thick CSI actual40GiB/source configuredthickseed, healthy Nomad/Consul, ES74,235,448primary docs/single-nodeyellow. No force/manual corrections. MR104 d95b385 remainsDraft/unmerged; working dynamic_deploy unchanged. [Final runtime evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

DevOps-894 master/working job update (2026-10-14): MR104 merged0bfc65c; dynamic_deploy ES uses VK bindings/test_inventory and retry2(first+one repeat), common Nomad binding covers all roles. UTF8 post encoding corrected and savedsourceverified. Existing unsandboxedscriptapproval remainspending, no build started. ProjectIDmove into global repo vars proposed as follow-up after userrequest. [Final changes/corrections](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).


DevOps-897 small MSSQL test5 deployed2026-10-14 using existing Ansible + test_inventory.sh and run_es tag after absent-job error. mssql-test5 task running; sql-test5 registered10.18.26.35:14305 on agent08. Subsequent requested case-insensitive absent-job handling published as dad41d4/MR106 and explicitly user-authorized merge completed to master9ad35fb; unrelated large DB edits preserved. Wrong-zone base disk deletion still pending creating; force-delete forbidden. [Evidence](../log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md).

DevOps-897 base PA2 disk deletion confirmed2026-10-14: after creating completed, fresh token found available; earlier waiting helper had stopped on expired-token401. Resumed previously authorized deletion, DELETE202 then exact GET404; no replacement or VM created. [Evidence](../log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md).

Large DB work resumed on user request2026-10-14 after deleting PA2 seed disk. Existing seven-stage edits run from current checkout without further changes. New MS1 ceph-ssd400GiB disk b6553d1a-35f7-4bbd-88c0-0b699212f090 creating; live step1 session94081 waits then creates VM/WinRM. [Live adaptation](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

Base guest network repaired via user-approvedDHCP command2026-10-14: stale172.26.0.103/24 replaced by10.18.26.9, WinRM/RDP/SQL reachable, authenticatedWinRM works. Step1green; stage2Windowsupdatesfailed0x80073712/noinstalls, legacyignore_errors preserved and reboot succeeded. Stage3restore started after usercontinue. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 small MSSQL fleet2026-10-14 20:04UTC: deployedmissing10test2-4/test7/test10-15 using existing Ansible+VKtest_inventory; preservedrunningtest5.11/11NomadSQLtasksrunning andConsulSQLservicesregistered, noSQLcontentsquery. LargeYouDo restore stage3completed/baseSHUTOFF; interruptedstep4notexecuted, preparedimageabsent. [Evidence](../log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md).

DevOps-897 user explicitly launched onlystage4today2026-10-14: Cinder uploadstoppedbase bootdisk accepted, preparedimagevk-ms1-sql-base pending; Ansible18374will clean temporarybase resources afteractiveimage. No stages5-7 launched and originalyc-sql-base retained. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 stage5 explicitly executed2026-10-14: all3exactmanagedstand names andnameddisks/ports absent, so no deletions; Ansiblefailed0. Stage6/7notlaunched. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).
