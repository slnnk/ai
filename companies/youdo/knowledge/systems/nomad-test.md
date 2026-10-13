---
system: nomad-test
status: verified
checked: 2026-10-13
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
