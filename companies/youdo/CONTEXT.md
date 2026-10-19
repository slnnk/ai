# YouDo: working context

Read at the start of every task. Update when the stack or priorities change.

## Role and priorities

DevOps engineer. In system maps and long-lived notes prioritize infrastructure and CI/CD:
runners, build images, registries, artifacts, secret stores, pipelines and jobs, launch,
publish and deploy rules, environments, network dependencies, monitoring, logs, operations
and recovery. Describe product architecture only where it affects build, delivery, launch
and diagnostics.

## Stack (reviewed with the user 2026-09-30)

- Source and CI: GitLab (pipelines, dynamic Kubernetes runners, CI templates repo). Jenkins
  is active only for test and dev stands: deploys to Nomad test stands, web autotest runs,
  and the ephemeral dev deploy to Kubernetes (job `test`, DevOps-832).
- Runtime: Nomad + Consul for test stands and prod; Kubernetes (Yandex Managed K8s) for
  ephemeral dev environments, with the Helm charts repo. Direction: dev environments replace
  the Nomad test stands, then services migrate from Nomad to Kubernetes.
- Cloud and hosting: Yandex Cloud (Terraform), Selectel (Terraform, DBaaS), on-prem hosts
  in the corporate network.
- Config management: Ansible, AWX (`awx-ee` execution image), Vault for secrets.
- Registries and storage: Nexus (`msk3-nexus.youdo.corp`), container registry
  `registry.youdo.sg`, Yandex Object Storage for reports and artifacts.
- Observability: Zabbix; VictoriaMetrics with vmagent and Grafana; Loki with Alloy agents
  (Loki runs in the dev cluster, `loki.dev.youdo.corp`); Sentry; Jaeger tracing;
  Elasticsearch.
- Product: .NET services and base images; MSSQL and PostgreSQL; RabbitMQ, Redis, Hangfire
  (on PostgreSQL); Temporal (dev, in progress); iOS and Android apps.
- Test infrastructure: Android device farm (Selenium Grid, Appium, ADB, emulators and
  physical devices), iOS runners with fastlane, autotest repositories per product.
- Tracking and chat: YouTrack (DevOps tickets `DevOps-832`, product tickets like
  `Site-24856`, knowledge-base articles `DevOps-A-50`), Mattermost.

## Out of scope

- sorm (incl. its RabbitMQ) is handed over to another engineer (2026-09-30). Do not work on
  it without the user's explicit request.

## Conventions

- CI deployment target selection (verified 2026-10-16): inherited project/group `NOMAD_ADDR` and `NOMAD_TOKEN` override job YAML variables. Inspect effective inheritance and pass the reviewed target explicitly to Nomad CLI using the intended deploy-token variable; test with conflicting generic inherited placeholders before publication. [Incident](knowledge/log/2026-10-16-nomad-test-devops-898-houstonv2mock-vk-assessment.md).

- Recovery YouTrack work summaries (user correction, 2026-10-16): update the existing summary comment when present; do not add duplicate new comments. Preserve earlier performed-work evidence and replace superseded limitations.

- Service deployment workflow (user correction, 2026-10-16): default to the service's established GitLab deploy jobs. Do not substitute direct Nomad job-spec updates or change established database recreation/preservation behavior unless the user requests it. Cerberus ordinary GitLab deployment recreates the stand database on every run; retain that policy rather than inventing metadata repair to preserve it. [Correction and rollout](knowledge/log/2026-10-16-nomad-test-cerberus-standard-gitlab-rollout.md).

- Base-images release source (user correction, 2026-10-14): release tags in `youdo/base-images` must point to commits on `master`, after the reviewed MR is merged. Do not release from an unmerged feature branch. Tag creation/replacement and rebuild still require explicit user authorization; this rule does not grant standing permission for external writes.

- Jenkins shared credentials (user, 2026-10-14): use stable service/environment IDs without task prefixes. Created IDs: `vk-test-nomad`, `vk-test-consul`, `vk-test-cloud`; use these in the ES test Pipeline. This naming correction does not authorize renaming existing unrelated credentials.

- Nomad deployment credentials (user, 2026-10-14): use the common `nomad_token` variable for ES and other roles. Read it from externally injected `VK_TEST_NOMAD_TOKEN`; do not introduce an ES-only token alias or store a new token literal in the repository. Jenkins bindings must cover every role that consumes it.

- Recovery task ownership (user, 2026-10-14): Python libraries/PyPI → DevOps-890; Nomad periodic/cron workload images → DevOps-895; base images including data/dockers → DevOps-891. Historical approved Git branch/MR names are preserved; classification changes do not authorize renaming/history rewriting.
- DevOps-896 dynamic inventory recovery was closed by the user on2026-10-14. Treat the recovered VK service as accepted complete; retain SQL mapping, repeated-refresh and consumer-cutover verification limits without reopening the task or claiming those actions completed. Further work needs a separate user request.
- DevOps-895 cron image restoration was closed by the user on2026-10-14. Treat image availability recovery as accepted complete; retain runtime audit limitations without reopening the task or claiming all23jobs used new bytes. Further runtime investigation needs a separate user request.

- Nomad Docker auth (user, 2026-10-12): Nexus credentials belong in the common role configuration for all hosts whose Docker auth file is generated. Do not limit this setting to incident hosts through host_vars. Password must remain an external secret.

- Nexus Docker roles (user, 2026-10-12): reuse `nx-docker` for Docker service accounts; its content permissions include deletion. Do not introduce a separate full-access role without a specific need.

- Nexus library recovery (user, 2026-10-12): retry requested publish jobs first, investigate actual failures; verify published versions through Nexus metadata only, without downloading packages.

- Yandex Cloud naming: new resources in zone a use prefix `yc-a-` (user, 2026-10-09); recovery cluster `yc-a-k8s-dev`. Do not infer other-zone prefixes or rename unrelated existing resources.

- Environment names carry meaning: `prod`/`production` is sensitive, `test` and `dev`
  are shared stands. Treat anything named prod as change-controlled.
- Company skills live in `~/ai/current/skills/`: `rp` (daily and sprint reports from
  Mattermost and YouTrack), `android-dig` (Android CI infrastructure diagnosis).
- Secrets for tooling are in `~/ai/current/.env` (GitLab, YouTrack, Jenkins, Nomad,
  Consul, Zabbix tokens). Never copy values elsewhere.
- Android farm maps follow the extended template in `general/knowledge/README.md`.

## Where to look first

- `knowledge/INDEX.md`, then `knowledge/systems/<system>.md`.
- `knowledge/repos.md` for local clones under `~/git` and `~/mygit`.

## Operational scripts

- `scripts/gitlab_task_mr.py`: GitLab task publication helper (`inspect`, `publish`, `verify`; see `--help`). Uses the existing company GitLab token environment variable without printing its value. Publication requires the supervised workflow approval in `knowledge/systems/gitlab-ci/agent-git-workflow.md`.
- `scripts/gitlab_ci_lint.py`: read-only GitLab CI lint/dry-run helper; see `--help`. Validates parent/child configuration without creating a real pipeline.
