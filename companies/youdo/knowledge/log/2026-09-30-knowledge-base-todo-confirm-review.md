---
system: knowledge-base
status: verified
checked: 2026-09-30
tags: [todo, review, helm, nomad, youtrack]
---
# TODO (confirm) items reviewed with read-only checks

## Task

Walk through the 22 `TODO.md` items marked `(confirm)` (collected from old notes on
2026-09-28) with the user: close, keep, or rewrite with current evidence.

## Context

A subagent checked 15 items read-only: `git fetch` + `origin/master` (YouDoApp:
`origin/develop`), GitLab and YouTrack GET, Nomad API GET. Nothing was changed in repos,
Vault, GitLab, YouTrack or Nomad. Host-only items were left to the user.

## Actions

- Closed as not relevant (user): Consul master CPU, Nexus pulls / PMTU, `idcn-10` disk
  cleanup, host `192.168.50.17` NVMe, MSSQL `RecreateDBProcedures`, sc-except restart
  policy, pg-b2b-test `test*` DBs, team-copilot `ANTHROPIC_BASE_URL`.
- Closed by the user: Jenkins Location URL (builds from 121 show the external URL).
- Closed with evidence: `RabbitMq__Url` global env, `youdo-business-worker` memory,
  DevOps-812/810.
- Kept and rewritten with evidence: GitLab environments cleanup, helm-charts Service bug,
  Helm `services[]` list merge, youdo-kitcut `SentryDsn`, Nomad 1.5.3, iOS `.ipa`, dotnet
  test concurrency, base images, prod_yandex runners, Selectel docker3 runner.

## Findings

- `gitlab-ci-templates` `76347cd` `v3/.deploy-dev.yml:77` hard-codes
  `JENKINS_URL=https://build.youdo.sg`; environment names are `dev/$CI_COMMIT_REF_SLUG`, no
  `CI_PIPELINE_ID`. Stale stopped environments in docvalidation: id 440
  `dev/youdo-microservices-docvalidation-`, 441 `...-devops-689-k8s`.
- No global `RabbitMq__Url` in any `devops/dev.yml`; docvalidation `044f867`, Fns `dd16902`,
  youdo-sms-service `d781952` keep it under `services[].env`.
- `helm-charts` `4ab8743` `microservice/templates/service.yaml:4`:
  `ne ($serviceConfig.enabled | default true) false` renders a Service for
  `enabled: false` (verified with `helm template`). Recipe:
  [default true overrides false](../../../../general/knowledge/helm/default-true-overrides-false.md).
- `microservice/values.yaml:197` is still `services: []` (list merge unchanged).
- youdo.business `3f8c5dab9` (2026-09-03): worker `memory`/`memoryLimit: 512Mi`.
- youdo.kitcut `b31af25` `devops/dev.yml:41-43`: `Sentry__Dsn: SentryDsn` from
  `dev/projects/youdo-kitcut`; Vault key not checked.
- Nomad Yandex test: all 7 clients `agent-test-01..07` and 3 servers `master-test-01..03`
  on `1.5.3`; `KillMode=process` still in `automation-test-yandex`
  `deprecated/roles/nomad-client/templates/nomad.systemd.j2:10`.
- `automation-services` `f37e59cd`: runner host_vars moved to `deprecated/` (`d3d6133c`,
  `d13d56fd`, AP-2228, 2026-09-15/16); Terraform-derived inventory has no gitlab-runner
  hosts. The local checkout has uncommitted edits in `roles/gitlab-runner/*` (left alone).
- YouDoApp `develop` `facff4aa81`: `Build development` keeps `build/YDMainApp.app.zip`,
  `fastlane/Fastfile:481-508` uploads `gitlab_youdo.zip`; `.ipa` change `5cf852ca96` only on
  `IOS-5008`.
- youdo.business `79254cc49` (2026-09-08): xUnit `maxParallelThreads: 4`, `conservative`;
  no runner/concurrency change for `dotnet-unit-tests`, no timing sections.
- `base-images` `a6d14d5`: LibreOffice PPA via plain `add-apt-repository` in 3 images; buster
  archive sed only in `dotnet-core-aspnet/3.1`; `3.1-gdilibs`/`3.1-libvips*` use `apt-key adv`.
- team-copilot `2084919`: `ANTHROPIC_BASE_URL` read in `src/agent/options.ts:115`; env from
  secret `team-copilot-env` via `envFrom`.
- YouTrack: DevOps-812 Fixed 2026-07-22, DevOps-810 Fixed 2026-07-21. API base is
  `https://youtrack.youdo.com/youtrack/api` (already in `systems/youtrack.md`).

## Changes

- `~/ai/TODO.md`: 13 items closed, 11 rewritten with evidence, no `(confirm)` left; rule
  about `(confirm)` removed.
- New recipe `general/knowledge/helm/default-true-overrides-false.md`.

## Open items

Tracked in `TODO.md`.

## Portable lesson

[Helm/Sprig: default true turns an explicit false into true](../../../../general/knowledge/helm/default-true-overrides-false.md)
