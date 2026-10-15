---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, gitlab-ci, ansible, inventory]
---
# Next test5 service deployment analysis after Monolith recovery

## Summary

Active scope is eight Nomad services: broadcast, cerberus2, featuretoggle, youdo.content, youdo.landings, youdo.trackingpixel, YouDo.Socket, youdo.help. User added Help and excluded WalletOne; MiniSape/Form/B2B remain excluded. Six services need rebuilds/new pipelines but no confirmed repository adaptations. Content requires its custom CI migration, while Cerberus requires Ansible PG compatibility and an explicit first-start database decision. No service repository edits, publication, build triggers or deployments were performed; git fetch updated remote refs only and preserved existing feature checkouts.

## Source selection

Fresh GitLab project/master/tag/pipeline GETs and read-only git fetch verified all local origin/master refs match live master. Seven current release tags equal master SHA; Socket current master and1.2.9 release have equivalent CI/config (full-tree equality was separately checked). Content malformed two-part2.471 tag is not a valid standard release source; correct latest stable three-part release is2.5.11. All selected projects have manual production mode. Proposed rebuilds use new pipelines at the listed release refs to resolve current shared templates; Content needs a new tag after its approved changes are merged.

| Service | Current release | Builds | Dependencies | Required preparation |
| --- | --- | --- | --- | --- |
| broadcast | 1.2.11 | 3 api, scheduler, migrations | PostgreSQL broadcast-test5; monolith API, RabbitMQ | No source changes found |
| cerberus2 | 1.0.9 | 3 api, worker, migrations | PostgreSQL Cerberus_test5; RabbitMQ | Custom Ansible PG raw/postgres identity correction; absent Cerberus template requires explicit first-deploy DB policy |
| featuretoggle | 1.0.11 | 2 api, migrations | PostgreSQL featuretoggle-test5 | No source changes found; recreate false means no template clone |
| youdo.content | 2.5.11 | 1 api | MSSQL YouDo/YouDoLogsExceptions; Vault storage keys; Consul SQL key | Migrate custom Levant/Nomad Yandex endpoints and BuildAPI registration to VK; keep libvips/Vault templates |
| youdo.landings | 1.3.35 | 1 webapp | Public test5 monolith/static endpoints; npm internal endpoint | No source changes justified; existing internal npm artifact HEAD200 |
| youdo.trackingpixel | 1.0.5 | 3 webapp, worker, migrations | PostgreSQL test5_youdo-trackingpixel | No source changes found |
| YouDo.Socket | 1.2.9 | 1 web | Custom socketchat.yml; per-stand runtime | No source changes found; existing1.2.9 CI/config matches current master |
| youdo.help | 1.0.14 | 1 web | No DB; npmjs build dependencies | No source changes found |


## Cerberus first-start blocker

Custom deploy script invokes playbooks/deploy/docker/cerberus2.yml instead of generic deploy_microservices.yml. Its remote PostgreSQL command tasks still need the old-Ansible/Python3.12 correction (raw plus become postgres). CI entrypoint already bootstraps SSH; no additional service SSH edits are justified.

Current database policy creates empty databases only for test/test1/test6/public-test. For test5 it necessarily clones Cerberus_test5 from Cerberus, independently of thin/thick instance type. Read-only SELECT on VK PG10.18.26.39 confirmed source database Cerberus is absent. Either restore the genuine template or introduce an explicit first-launch parameter allowing empty Cerberus_test5 with existing Pre migrations. Initial migration20180726175709 creates Orleans and service schema; empty service DB is technically supported but lacks template production data. Do not create an empty shared template as a substitute. Existing recreate_db_cerberus2 tags are separate from dropdb.

## Content custom delivery

Keep its custom Levant/Nomad/Vault flow; generic Ansible with its sparse config would discard storage configuration. Migrate Nomad/Consul/DC/domain and old BuildAPI in .gitlab-ci.yml40-80 to VK, and register /ms_builds metadata consistently with existing Nomad DEPENDS_ON=Monolith. Retain current3.1-libvips build/runtime, ProcessorType=vips and jemalloc. Current runtime uses MSSQL YouDo and YouDoLogsExceptions. Read-only checks confirmed Consul test_instances/test5/mssql_db exists and VK Vault secret/dotnet/youdo-content/test5 has all required nonempty storage/AWS keys; no secret values recorded or new credentials proposed.

## npm and shared templates

Old hostname alone is not a migration requirement. Landings current lock has431 internal Nexus URLs; HEAD of its exact Next tarball through msk3-nexus.youdo.corp returned200 (the corresponding public Nexus path404). Preserve .npmrc/lock versions and URLs; actual rebuild will establish full package availability. Metadata HEAD500 did not prove tarball failure. Help builds via Docker npm ci against npmjs, no .npmrc. Socket npm install occurs before its .npmrc COPY, so that old registry does not affect installation. Both use nodejs-build-docker and do not inherit nodejs-npm-restore. No additional shared gitlab-ci-templates changes are currently required.

Generic Ansible already includes VK endpoints, direct PostgreSQL handling/raw compatibility and corrected monolith Traefik domain. Cerberus alone bypasses the fixed PG tasks; Socket custom handler has no PG/SSH work. None of the three generic .NET services declares depends_on=Monolith; their BuildAPI acceptance must preserve actual metadata rather than blindly demand Monolith. Content's custom catalog registration must reflect its existing Monolith runtime meta.

## Proposed execution order

Review/approve the minimal Content and Ansible fixes, select Cerberus empty-service-DB versus real-template restoration, publish/merge under the existing supervised workflow, create a new Content release after merge, rebuild15components across8services, then deploy foundation services Cerberus/featuretoggle before consumers, Content before frontend consumers, and verify health/image versions and saved/live/rendered BuildAPI data. Other six ordinary rebuild paths can proceed independently once explicitly authorized. Production deployment stays manual. No implementation branch names or release/build/deploy approval was requested or obtained by this research turn.

## Separate moderation track

User's prior list also had youdo-moderation, delivered via its own CI/S3 rather than Nomad. Keep separate from eight-service Nomad scope. Existing source targets youdo-static-test/test5, recursively clears that asset prefix, uploads assets/manifest/shared fonts and writes Consul static/test5/manifest.json. Consul write currently omits ACL header, a possible VK permission issue requiring confirmation on actual rollout. .npmrc/lock old URLs alone do not justify changes after the supported internal endpoint check. This potentially changes existing static assets, so do not fold into a Nomad rollout implicitly.

## Evidence and limits

Local artifacts under /home/slnnk/ai-data/jenkins-recovery/monolith-services-audit/: next-iteration-live-sources.json, next-test5-analysis.json, next-test5-runtime-summary.json (no candidate jobs present). Analysis used current source, GitLab metadata, targeted read-only PG/Vault/Consul checks and exact npm artifact HEAD; it does not certify future NuGet/npm restore or full build success. Earlier provisional old-npm migration and stale gdilibs findings were corrected before this report. No private values retained.
