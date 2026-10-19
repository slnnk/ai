---
system: gitlab-ci
status: verified
checked: 2026-10-16
tags: [devops-898, business, nomad, ansible, git-training]
---
# DevOps-898 Business Nomad job datacenter addresses

## Current approved behavior and publication

Latest user instruction supersedes the initial conditional design: Business Elasticsearch and FlashCall are shared VK dependencies for all stands, including public-test. Use literal `vk-test` in these six addresses; no `dc` interpolation or public-test special condition. This is task-specific configuration guidance, not a global rule for unrelated services.

Correction sequence: user explained public-test uses the same Elasticsearch and rejected conditions; requested `vk-test` through `dc`, then, after understanding inventory `dc: public-test`, explicitly chose `А понял тогда действительно хардкод vk-test`. Parent updated only the same template locally: all five Elasticsearch URLs now `http://elastic-b2b.service.vk-test.consul:9200`, FlashCall URL `http://youdo-call-service-web.vk-test.youdo.local`. Intermediate direct-`dc` revision was not committed/published. Earlier public-test-preserving claims below describe historical first revision only.

Independent review of latest local diff confirms exactly six ternary-to-literal replacements relative to published HEAD55745166, with no other file-content changes. `git diff --check` passed, index empty, sixteen unrelated MSSQL paths preserved. Existing branch remains `DevOps-898-use-datacenter-in-business-job` as history. Corrected publication proposal: commit `use shared vk addresses in business nomad job`, rename existing MR118 to `DevOps-898 use vk addresses in business nomad job`; source/target unchanged. User explicitly approved the corrected publication (`Подтверждаю обновление MR`). Parent reviewed the actual staged diff containing only this template/six replacements, committed `0cd8efb0fc1c0b74a7595c1c31227fc9389d2c64` (`use shared vk addresses in business nomad job`), pushed and updated MR118 title to `DevOps-898 use vk addresses in business nomad job`. Description is one Russian paragraph describing six fixed VK addresses for all stands including public-test, followed only by task link. GitLab API verified MR head0cd8efb, opened/source unchanged/target master/squash=false. Index empty; unrelated MSSQL files preserved. User subsequently merged MR118 as8179d6cf; deployment remains unauthorized.

## Task

User explicitly requested replacing legacy Yandex DC addresses in the Business Ansible Nomad job before deploying the last DevOps-898 service. This is an approved scope extension after readiness found the existing legacy addresses already resolve to VK compatibility aliases.

## Context

Repository `/home/slnnk/git/automation-test-yandex`. Proposed and user-approved branch `DevOps-898-use-datacenter-in-business-job` from fresh `origin/master 078c906b24fb5883395a2b76bd3964fbc4598d84`. Parent created/switched branch after explicit stage-one approval. Sixteen unrelated MSSQL paths were already modified and remain unchanged/unstaged. Target file had no prior local edits.

## Actions

Parent replaced exactly six literal `yandex-test` DC segments in `playbooks/deploy/docker/files/nomad_youdo-business/youdo-business.j2`: five `Elasticsearch__Host` values (lines260,401,542,797,1060) and `FlashCall__Url` (line685). Replacement expression: `{{ 'yandex-test' if dc == 'public-test' else dc }}`.

Independent read-only peer review confirmed the exact six-line scope and no other changes to this file. Full substitution reversal reproduces HEAD bytes. Jinja StrictUndefined renders of all six address lines passed for vk-test, yandex-test and public-test; yandex/public output exactly matches prior addresses, VK points to VK names. Parent also reported full-template render PASS for all three DCs. `git diff --check` passed. Staging index remains empty before publication approval.

## Findings

- No review issues. Components, images, DB behavior, ports, credentials and FlashCall disabled state unchanged.
- Public-test DC value is `public-test`, so the explicit compatibility branch preserves its previous Yandex dependency routes. Blind substitution with `dc` would have changed public-test behavior outside scope.
- Business master CI `.gitlab-ci.yml:383–385` clones `automation-test-yandex` during deployment. This repository has no `.gitlab-ci.yml` or image-build step. After merge, existing ordinary jobs3227749–3227754 will consume the updated default-branch template. No Business rebuild, new pipeline or Ansible image rebuild needed.
- Local source change does not alter any current Nomad runtime. Merge and deployment are separate actions requiring applicable approval.

## Changes

One repository task file, six changed lines. All unrelated MSSQL edits preserved, no staged files at review time. KB bookkeeping links the user-requested change to [initial readiness](2026-10-16-nomad-test-devops-898-business-preflight.md).

Publication proposal: commit `use datacenter addresses in business nomad job`; MR `DevOps-898 use datacenter addresses in business nomad job`; source `DevOps-898-use-datacenter-in-business-job` → target `master` in `automation-test-yandex`. Required one-paragraph Russian MR description with DevOps-898 link only; check results/CI effects belong in approval summary and this log. User explicitly approved stage-two publication. Parent reviewed the actual cached diff containing only the template path, committed `55745166fcd654f9d83ed6228cfdb4d4b6ffa3d2` with the proposed message, pushed the approved branch and created [MR118](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/118) with the approved title/source/target. Project530 preserves assignee a.solonenko, squash=false, remove_source_branch=true. GitLab CI is unconfigured and Auto DevOps=false; no pipeline created. Index is empty after publication; sixteen unrelated MSSQL paths remain local and preserved. Merge and deployment not authorized.

## Risks and limits

Publication approval covers only this explicit template path, commit, push and MR creation; no merge or service deployment implied. A later ordinary Business deployment recreates main and mock databases on target stands and still requires explicit permission. No runtime probes or functional tests performed for this source-only change.

## Portable lesson

none

## Publication result

MR118 is open and awaits user merge. No merge, runtime change or deployment performed. Existing Business release master-21509 and ordinary jobs3227749–3227754 remain the next rollout candidates after merge and explicit deployment approval.

## Corrected publication result

Final published MR118 head is0cd8efb; title and description reflect shared literal VK addresses, replacing the initial conditional design. User-approved commit/push/MR update completed. User subsequently merged MR118 as8179d6cf; no agent merge or deployment authorization inferred.

## User merge and existing pipeline compatibility

Parent live GitLab GET verified user merged MR118 at2026-10-16 00:26:44.329+03. Merge SHA8179d6cf0437cb64ee2b6006da5f5ba6ed5f6277, source0cd8efb0fc1c0b74a7595c1c31227fc9389d2c64. No agent merge performed. Existing ordinary Business jobs3227749–3227754 are ready to consume this default-branch template through runtime git clone; no fresh Business pipeline or image rebuild needed. Deployment is not authorized or started.

Pipeline140959 was created2026-10-15 13:55:07+03 after VK CI routing commit8cd278ba28640630e969602f7bcccbd5d11039a1 at13:41:41+03. Thus its compiled ordinary deployment jobs already route to VK. It predates later keep-db fix0cf1dde32f3e6d7c00279fbfce798a4b8ec2fe71 at21:41+03: do not use that historical pipeline keep-db jobs for this rollout. User chose ordinary jobs with DB recreation. GitLab CI includes are creation-time snapshots, while Ansible repository/template are cloned at job execution.

## Final related deployment

Subsequent user-approved Business deployment completed after separate DB compatibility/pager corrections MR119/MR120: jobs3230182–3230187 allSUCCESS, Nomad master-21509 healthy/restarts0, all66taskimage references verified. See [final rollout](2026-10-16-nomad-test-devops-898-business-rollout.md). No tracker state changes performed.
