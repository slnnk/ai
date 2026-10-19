---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [nomad, vk-cloud, classifier, gitlab-ci]
---
# DevOps-898 classifier VK deployment assessment

## Summary

Assessment only, requested as an additional shared single-instance service under DevOps-898. Actual master/tag2.6.9 is d864cf03d081d624a4f9a911cefb2dbd5cb0e669. Minimal repository change: staging Nomad datacenter and routing domain from yandex-test to vk-test. Application changes are not justified by static inspection. Live VK lacks houston-hub v2, a functional prerequisite.

## Context and actions

Read-only GitLab GET project164, master, latest pipelines and project/ancestor group variable metadata; GET current data/ci-templates Python UV service and base templates. Fetched classifier origin without switching/editing the checkout. Local master remains39096c7; its obsolete Python/staging/spb2 configuration must not be used for implementation. Inspected current files with git show origin/master:path. GET VK Nomad jobs and Consul catalog services.

## Findings

- deployments/staging.nomad lines13/18 hardcode yandex-test.youdo.local/yandex-test. Replace with vk-test.youdo.local/vk-test for existing internal staging migration. count1, instance=common, port8000 and /health already exist; Redis and exporter are included. No new replica configuration is needed.
- Current .gitlab-ci.yml includes data/ci-templates/templates/python-uv-service.gitlab-ci.yml, which includes .python-service-base.gitlab-ci.yml. Shared deploy:staging runs automatically for tags and uses NOMAD_STAGE_ADDR/TOKEN; deploy:production is manual. Avoid introducing a release tag merely to test deployment. Existing pipeline118059/tag2.6.9 is successful; actual registry manifest availability has not been checked.
- Project variables and data/houston variables are empty. Group data provides protected NOMAD_STAGE_ADDR/TOKEN and Yandex/production variables, with no VK token. Minimal project-scoped NOMAD_STAGE_ADDR/TOKEN overrides can route only classifier staging to VK without shared-template changes; must preserve effective protection/scope and production settings. Values were neither printed nor saved.
- configs/staging.yaml requires Consul houston-hub version v2 and houston-classifier-redis. VK GET found no classifier/houston jobs or catalog registrations; only Kafka and kafka-schema-registry were present among matching entries. Hub deployment/registration or a separately verified cross-DC route is prerequisite. Bundled Redis should register during classifier deployment.
- Current app sends houston_choices through basis_fastapi.EventsSender; previous explicit Kafka REST configuration was removed. Event delivery backend/defaults remain unverified; do not claim the old hardcoded Kafka REST dependency applies to current master.
- Current Python3.12/uv build uses private base images/packages. No Dockerfile/lock/application edits justified. Image existence/pull and runtime functional readiness remain unverified.

## Changed files and risks

Only KB bookkeeping and local sanitized template audit files under ~/ai-data/DevOps-898/classifier-audit were written. No task branch approval, repository edits, CI variable changes, builds, tag creation or deployment occurred. Superpowers was not used as explicitly requested. Implementation requires supervised branch approval; external writes/deployment need explicit approval. A successful health endpoint alone will not establish working Hub classification/event delivery.
