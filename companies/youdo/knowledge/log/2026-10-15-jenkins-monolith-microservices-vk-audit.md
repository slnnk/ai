---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, microservices, gitlab-ci, ansible]
---
# Monolith-dependent microservices VK rebuild and deployment audit

## Summary

Read-only inventory of37local devops/config.yml files found9Monolith-dependent services: Fns, antifraud2, attribution, badgekeeper, bruteforcingdetector, docvalidation, escrow.tinkoff, youdo.form, youdo.userinsurance. Live GitLab master GET confirms all9still declare Monolith. User subsequently excluded unused youdo.form: active scope is8services. Required work: two service DNS fixes, shared v3 per-stand CI credentials/address mapping and peer-compatible delegated PG tasks. Legacy Form CI and selector changes are excluded. Rebuild all selected app/migration images, then bootstrap each service to test5 via fresh GitLab deploy jobs before using Jenkins recreate. No repository changes, builds or deployments performed.

## Task and scope

User requested the list from local ~/git repositories and analysis of service, gitlab-ci-templates and Ansible changes needed to rebuild/deploy to VK. Continuing test5 is the planning assumption; no wider stand rollout authorized. User's no-superpowers instruction retained. Local branch changes and Git publication remain subject to supervised approvals.

## Evidence and inventory

Sanitized inventory and current-master summaries: /home/slnnk/ai-data/jenkins-recovery/monolith-services-audit/. inventory.json includes local and independently queried live-master data. inventory.tsv is a local-state snapshot, not proof origin/master is fresh.

| Repository | Project | Application workloads |
| --- | --- | --- |
| Fns | fns | api, service, scheduler |
| antifraud2 | antifraud2 | api, service, scheduler, external selenium |
| attribution | attribution | api, service |
| badgekeeper | badgekeeper | api |
| bruteforcingdetector | bruteforcingdetector | api, service, scheduler |
| docvalidation | docvalidation | api, service, scheduler |
| escrow.tinkoff | escrow-tinkoff | api, web, worker |
| youdo.form (excluded by user: unused) | youdo-form | api |
| youdo.userinsurance | userinsurance | api, scheduler, workerservice |

All have migrations; postgres except escrow.tinkoff MSSQL. Local origin/master was stale for attribution and bruteforcingdetector: current remote master already has attribution Monolith and brute .NET8. Local badgekeeper branch pins an old template ref but current remote master has no pin. Do not introduce unnecessary master edits based on those local branches. youdo.form has unrelated dirty configuration/Dockerfile work; preserve it and choose clean source.

## Service configuration changes

- docvalidation/devops/config.yml38/47/57: YouDoApi URL has .yodo.local typo; use .youdo.local with existing dc interpolation.
- escrow.tinkoff/devops/config.yml37/63/93: Router__Url hardcodes router.yandex-test.youdo.local; use {{ dc }} and verify actual VK router availability before deployment.
- Other internal endpoints already use dc; depends_on is a classification, not a DNS resolver or startup orchestrator.
- Runtime config YAML is loaded by deploy_microservices.yml40; changing it alone does not technically require recompiling binaries. User explicitly requires rebuild to restore image availability; include all owned workloads plus migration images and verify companion external images.
- Dependency preflight: antifraud2 textvalidation/cerberus2/Selenium; docvalidation cerberus2; userinsurance vks-policy-generator/userinsurance-gotenberg; escrow router. Current DNS/service availability was not established for every dependency.

## Shared GitLab CI changes

Live templates mastercda625bdfea11b0fde3953ba783b771a8d38666f verified by GET. Existing single/dynamic VK migration does not cover per-stand jobs. v3/.deploy-test-per-stands.yml77/84 still passes NOMAD_YANDEX_TEST_ADDR/TOKEN. Both ordinary and keep-db variants need VK endpoint http://nomad.service.vk-test.consul:4646 and existing NOMAD_TOKEN_VK_TEST mapping into nomad_stage_addr/token. No new token required. Confirm inherited token availability/protection for chosen pipeline source.

Historical finding only, excluded from implementation: legacy Form uses .deploy_test.yml and a different job prefix. User excluded the unused service, so no legacy CI mapping or Jenkins selector compatibility is needed. Preserve public-test and existing v3 job names.

CI clones default automation-test-yandex branch; local fixes must be reviewed/published/merged before new deployment pipelines. Existing historical pipeline retries retain previously compiled YAML and old service commits, so do not count as applying new shared templates.

Current remote CI: Fns/docvalidation DEPLOY_PROD_MODE=auto, remaining v3manual. Master pipelines for those two can trigger production child deployment. Choose reviewed build-only/MR or targeted existing build jobs where suitable; do not alter production rules just for recovery. Legacy Form tag pipeline also publishes NuGets. No pipeline creation/retry/tag is authorized by this research.

## Ansible and Jenkins changes

Already VK: global dc, buildsinfo_addr, test_inventory.sh source, test SQL defaults and microservice Nomad templates/routes. No blanket DNS rewrite needed. Current Jenkins global VK_TEST_NOMAD_TOKEN credentials('vk-test-nomad') exists; do not add duplicate bindings. GitLab per-stand jobs still need their own correct mapping.

Required PG identity correction: deploy_microservices.yml155/173/184/194 executes delegated psql -U postgres without become_user. Same-day test5 PG16 peer behavior is verified in2026-10-15-jenkins-test5-deploy-retry.md; monolith-only become fix does not propagate here. Add become:true/become_user:postgres to four PG tasks/block only, preserving local Nomad/API tasks and pg_hba. Installed Ansible2.13.13 delegation resolves nonlocal delegates to SSH automatically, so no separate connection:ssh change required. Current test5_postgres inventory address10.18.26.39 verified; runner SSH/sudo must be checked. Fresh local root-key SSH probe failed authentication, so no new direct PG query result is claimed.

Fresh BuildAPI /ms_builds/test5 has only key278(static), no selected microservices. recreate_microservices.yml17-51 selects only saved rows with DEPENDS_ON==Monolith; enabling Jenkins MICROSERVICES now cannot bootstrap the8selected services. First GitLab deploys write metadata via deploy_microservices.yml253-273. Subsequent Jenkins recreate uses those records and replays jobs; it does not build images or discover repository configs.

## Proposed execution and material effects

1. Review minimal changes:2service configs, shared v3 per-stand CI mapping and delegated PG identity; do not change legacy Form CI or Jenkins job selectors.
2. Select clean current master commits and proper CI source; validate merged YAML/rules before build to exclude implicit production deployment. Publish reviewed changes under supervised workflow.
3. Rebuild app+migration images, verify exact tags and dependencies; new configuration uses new pipelines. Rebuild itself has no database-reset authority.
4. Preflight rendered config, registry, service DNS, PG delegate/SSH/sudo and required template DB DocValidation. Verify placement/resources and actual migrations before deployment approval.
5. Deploy one pilot then remaining selected services to test5 via GitLab; verify allocation/Consul/HTTP, migration result and BuildAPI records. Use exact tested immutable tags.
6. Confirm all8selected Monolith records before accepting Jenkins recreation.

All9local configs declare recreate_db:true. Normal playbook stops/purges the job and may reset databases; keep-db skips dropdb-tag tasks but create-if-absent still needs PG identity and migrations still run. Choose reset versus keep-db explicitly per service; do not infer reset approval from rebuild/research request. No unrelated hardening/refactors or production changes proposed.

## Changes and limits

Only sanitized audit artifacts, this work log, existing Jenkins map and TODO changed. No code changes, branch switches, git publication, builds, database writes or deployments. Build availability and all service DNS are preflight items, not claimed complete. No secret values copied into artifacts.

## Portable lesson

None.

## User scope correction

User: youdo.form is unused and must not be deployed. Active set: Fns, antifraud2, attribution, badgekeeper, bruteforcingdetector, docvalidation, escrow.tinkoff, youdo.userinsurance. Exclude Form rebuild, migrations, database work and deployment; remove legacy .deploy_test.yml and Form-specific Jenkins-selector changes from the proposed implementation. Historical inventory still records its config match, explicitly marked excluded.
