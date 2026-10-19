---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [devops-898, b2b, business, gitlab, nomad]
---
# DevOps-898 Business stand deployment readiness

## Task

Check the last DevOps-898 B2B service, `youdo-business`, for deployment readiness on test10–test15. User requested investigation only; no new pipeline, repository branch/edits or deployment authorized.

## Context

Repository `/home/slnnk/git/youdo.business`, GitLab project423. Read-only fetch updated origin/master to `523609a16f5b72aae98d876a6a166c99859c27c2`; clean existing checkout preserved. Latest release `master-21509` matches this SHA and successful pipeline140959. Parent artifact `/home/slnnk/ai-data/DevOps-898/business-preflight.json` confirms all nine image builds SUCCESS, target ordinary jobs3227749–3227754/test10–test15 manual, exact Nomad jobs `youdo-business-test10` through `youdo-business-test15` absent. Broad service-prefix matches would incorrectly include other B2B services.

## Actions

Audited current-master CI, custom Dockerfiles, dev deployment configuration, application hosting/configuration, shared GitLab inheritance and the special Ansible playbook/Nomad template. Compared nine required images against builds. DNS lookup only for old/new Elasticsearch service names; no HTTP or Consul acceptance probes.

## Findings

- No mandatory source or infrastructure changes identified. Existing release and six ordinary manual deploy jobs are ready; no new build/pipeline needed for this task.
- `.gitlab-ci.yml:364–385` overrides `.deploy-test-per-stand` to use `playbooks/deploy/docker/youdo_business.yml`. Current child template `v3/.deploy-test-per-stands.yml:76` supplies VK Nomad address/token and is inherited. The special playbook still has Yandex defaults, correctly overridden by child job extra-vars.
- Seven runtime components match dev deployment: worker, automation-web, business-api, employee-web, business-web, mock-api and business-internal-api. Two further images provide main and mock pre/post migrations. Source build definitions `.gitlab-ci.yml:138–227`; dev component declarations `devops/dev.yml:299–391`; special Nomad tasks in `automation-test-yandex/playbooks/deploy/docker/files/nomad_youdo-business/youdo-business.j2`.
- All runtime container port mappings use80. Internal `base-images/microsoft/aspnet/8.0/Dockerfile` explicitly sets both `ASPNETCORE_HTTP_PORTS=80` and `ASPNETCORE_URLS=http://*:80`; Business Dockerfiles preserve those defaults. No port correction required.
- Ordinary special playbook recreates two PostgreSQL databases per stand: `testN_youdo-business` and `testN_youdo-business_mock_db` (`youdo_business.yml:9–10,31–57`). Four migration tasks run against direct5432. Runtime `ConnectionStrings__Pg` omits port and therefore also uses5432; mock additionally connects to main DB via `ConnectionStrings__YouDoBusinessPg`. No Business PgBouncer5433 routes needed.
- Dependency URLs use stand/DC variables, including shared doc-generator and per-stand Billing, Kitcut, TKB/Tochka mocks, DocValidation, RabbitMQ and Auth/MobileID endpoints. Existing dependencies were accepted earlier; this check did not redo functional probes.
- Five Elasticsearch values retain `http://elastic-b2b.service.yandex-test.consul:9200` in the special Nomad template (lines260,401,542,797,1060). On2026-10-16 Moscow, read-only DNS lookup resolved BOTH legacy Yandex and canonical VK service names to10.18.26.32. This is an active compatibility alias, not a required migration fix. Canonical map `current/service-addresses.env` records the observation. A blanket DC substitution could change public-test behavior and is outside this deployment scope.
- Existing master pipeline enables automatic production/release and post-production replica migrations, but creating a fresh pipeline is unnecessary. Playing existing ordinary stand jobs limits action to the requested stands and database recreation; requires explicit deployment permission.

## Changes

KB bookkeeping only: this log, existing system map, repository index, backlog and address-map observation. No repository task file edits, branches, infrastructure changes, pipeline creation or deployment launches.

## Risks and limits

This is readiness evidence, not deployment acceptance. Ordinary jobs destroy/recreate the two stand databases. Acceptance after any separately authorized launch uses GitLab job status and Nomad job/allocation status. No functional or external integration claims.

## Portable lesson

none
