---
system: jenkins
status: verified
checked: 2026-10-15
tags: [cerberus, ansible, postgresql, DevOps-899]
---
# Cerberus first-start empty database policy and VK PostgreSQL compatibility

## Summary

Local approved Cerberus2 Ansible adaptation prepared: all stands recreate an empty service database, without cloning absent shared Cerberus template. PostgreSQL command uses raw/become postgres/pager off. Publication, merge, build and deployment not yet authorized by branch approval.

## Task and approvals

User reopened postponed Cerberus2 and chose empty databases for all stands. Proposed automation-test-yandex branch DevOps-899-create-empty-cerberus-databases from current origin/master, only cerberus2.yml change plus necessary VK PG compatibility. User explicitly answered Yes. Fetched origin/master381391d ->cf88e422; created approved branch from cf88e422 while retaining16unrelated dirty/untracked MSSQL paths. No worktree or stash.

## Actions and changes

Only `playbooks/deploy/docker/cerberus2.yml` changed, +5/-19: replaced command with raw, added become true/become_user postgres and -P pager=off, retained terminate/drop/create/grant SQL and recreate_db_cerberus2 tag. Removed stand condition and duplicate template-cloning task, one unconditional empty-DB task remains. Existing database recreation behavior retained; migrations must populate schema/data. No empty shared template introduced.

## Checks

`ansible-playbook --syntax-check -i localhost, playbooks/deploy/docker/cerberus2.yml -e test_instance=test5` passed. Targeted git diff --check passed. YAML/task assertions confirmed one unconditional empty-DB task, raw/become/pager settings, no template clause, original recreate tag/drop/grant retained. Index empty; no staging/commit/push/MR or remote database changes.

## Proposed publication

Commit: create empty cerberus databases for all stands
MR title: DevOps-899 create empty cerberus databases for all stands
Source: DevOps-899-create-empty-cerberus-databases -> master
MR description (exact proposed text):

```text
Переводим Cerberus2 на создание пустой базы для всех стендов без клонирования шаблона Cerberus и адаптируем PostgreSQL-команду к VK: raw, выполнение от postgres и отключённый pager.

https://youtrack.youdo.com/issue/DevOps-899
```

Ansible publication changes future Cerberus deployments; no deployment is executed by local checks. Publication approval pending; merge/release/build/deploy require their own explicit scope.

## Risks and limits

No live playbook execution. Future regular Cerberus deployment retains its existing drop/recreate behavior. Empty database has no template data. All unrelated MSSQL paths preserved.

## Publication and merge accepted

User explicitly confirmed publication and merge of reviewed scope/names. Staged only cerberus2.yml, inspected actual staged diff+5/-19 and empty prior index, committed `13a23b1548a6fb9620463e076ee57c60bdc7e53e` with approved message, pushed approved branch. Created [MR114](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/114), exact approved title/description, assignee184, squashfalse/remove-source true preserved from project. Verified remote diff contains only task file, mergeable/no conflicts, no head pipeline. Merged using exact expected SHA into master `248bf03edc7b146e42e213182daf33fbe23b7067` at2026-10-15T20:34:21.790+03:00. Read-only GitLab master file bytes match reviewed local file exactly. All16unrelated MSSQL paths remain dirty/untracked, index empty. No service build or deployment requested/performed in this approval.

## Release rebuild authorized and launched

User explicitly answered Yes to rebuilding Cerberus2 1.0.9. Verified project153/tagSHA9f1c54fa6e37f4a8c51a95849bf9405e90895498; CI DEPLOY_PROD_MODE manual. Created [pipeline140997](https://gitlab.youdo.sg/youdo/cerberus2/-/pipelines/140997), IID135, ref1.0.9. Build-only approval; no deploy jobs played. Receipt `ai-data/jenkins-recovery/cerberus-build899.json`; local read-only watcher `watch-cerberus-build899.py [--once]`, status receipt cerberus-build899-status.json. Build outcome pending.

## Internal SDK image proposal

prepare-nuget3229485 succeeded after358.29s. Read-only trace/runner inspection confirmed initial delay pulling mcr.microsoft.com/dotnet/sdk:2.1 before restore (no build container yet), not a NuGet-feed failure. Builds3229488/89/90 then started. User requested moving SDK2.1 into base-images.

Read-only source manifest confirms Linux/amd64 digest sha256:ae4daaaab45c6c6b0d2e36d93d8eed8ab255bdab9df02f08f3c39ba90ceb22a9. No SDK2.1 recipe exists in base-images; existing SDK3.1 recipe is a plain FROM. Proposed internal target registry.youdo.sg/youdo/base-images/microsoft/dotnet-sdk:2.1. No repo changes yet. Proposed branches from fresh origin/master: base-images DevOps-899-mirror-dotnet-sdk-2-1 (one digest-pinned Dockerfile), cerberus2 DevOps-899-use-internal-dotnet-sdk (DOTNET_BUILD_IMAGE only; retain2.1). Branch approval requested. No image publication/tag/pipeline authorization requested yet at this stage.

User answered branch proposal with Add to TODO, deferring SDK mirror/consumer changes. Added canonical TODO item with target image/digest; no SDK branch created, no source edits or publication. Existing authorized Cerberus release build remains separate.

## Mirror scope resumed and expanded

User explicitly requested implementing now and moving all images used by Cerberus, superseding deferral. Read-only fetched base-images masterdfb2909 and Cerberus master9f1c54f; both checkouts clean. Consumer variables additionally require ASP.NET runtime2.1: MCR manifest Linux/amd64 digest sha256:80ddf066edeeb7e489b23c3c90d8e5dd741037d4a4875150c1dec777fd24cc76. Inventory of inherited job images delegated; branch approval must cover expanded final scope before edits. No new image repo edits yet.

## Folding fix and rollout resumed

User approved one-space correction then publication/merge: ae68c6230b1270f98e7567f2868087b1cf3c83a8, MR115 merged masterd2c5b9b603d3862a955f37c6c30fdf4e7f540609. Exact SQL retained, YAML folding now verified. User explicitly stopped all work temporarily, then resumed base-images and Ansible while deferring Cerberus image-ref updates. User authorized deployment on test/test1-test7 and extended test10-test15; see [rollout log](2026-10-15-jenkins-cerberus-eight-stand-rollout.md).
