---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, vk-cloud, gitlab-ci, recovery]
---
# DevOps-898 single and dynamic VK recovery plan

## Summary

The initial plan covered thirteen services from DevOps-A-33. The final user-approved target of ten single services and LogReader test5 is now deployed through GitLab and runtime-verified. Socket was corrected to per-stand delivery and its CI restored; unused vks-policy-generator was excluded. Public-test remains unchanged. The other fifteen SQL stands are a separate LogReader dependency. Historical planning findings below are superseded by [final launch evidence](2026-10-14-nomad-test-devops-898-implementation.md#verified-final-launch-scope-2026-10-14).

## Task

Sources: [DevOps-898](https://youtrack.youdo.com/youtrack/issue/DevOps-898), [service list](https://youtrack.youdo.com/youtrack/articles/DevOps-A-33/Shablony-GitLab-CI#Spisok-servisov). Issue has no description; scope comes from user and article.

## Context

Single: geocoder, youdo-call-service, youdo-business-doc-generator, chat-content, textvalidation, tinkoff-e2c-sign-service, vks-policy-generator, DebuggingEvents, blec (BlackListedEmailChecker), pechkin, mailer.
Dynamic: logreader (YouDo.Web.LogReader), socketChat (YouDo.Socket).

Last platform evidence is DevOps-893 acceptance on October13: eight ready clients, Traefik, Redis, Jaeger and Vault integration restored. This is historical evidence, not a fresh runtime health check. Target address is http://nomad.service.vk-test.consul:4646; Consul DC vk-test; routing suffix vk-test.youdo.local. Addresses already exist in current/service-addresses.env.

## Actions and verified findings

Read issue/article through YouTrack GET using existing youtrack_sprint.py client. Read all13 GitLab project CI/HCL files and project variable metadata using GET; no secret values were printed or persisted. Sanitized audit: /home/slnnk/ai-data/DevOps-898/services-audit.json.

All13 projects have master default branch, are not archived, and include v3/.deploy-test.yml without ref. All11 singles use DEPLOY_TEST_PER_STANDS=false; LogReader uses dynamic; Socket uses true despite dynamic HCL groups. All13 HCL use var.dc for datacenters and var.proxy for routing.

Shared v3/.deploy-test-single.yml and v3/.deploy-test-dynamic.yml hardcode yandex-test and bind NOMAD_YANDEX_TEST_ADDR/TOKEN. Hidden single template runs devops/test.hcl directly with nomad run, using NOMAD_VAR_image/version/DC/proxy and dynamic NOMAD_VAR_stands. ENV_NAME only names GitLab environment; routing comes from HCL var.proxy. Deploy allow_failure=true means green pipeline is insufficient acceptance evidence. Defaults in v3/.deploy-test-dynamic.yml include test16/test17; recovered VK platform excludes them.

Inherited group NOMAD_TOKEN_VK_TEST and CONSUL_TOKEN_VK_TEST were verified October13 (masked, unprotected, scope *); application-group inheritance and current effective values remain to verify. Local VK_TEST_NOMAD_TOKEN is an operator secret, not the GitLab variable name. Address-variable presence is not established.

Project NOMAD_IP_ADDR overrides exist in call-service, textvalidation, mailer (scope *, unprotected, unmasked); trace actual consumers before changes. DebuggingEvents devops/test.hcl:62 hardcodes http://debuggingevents-elastic-master.yandex-test.youdo.local. Call-service also has call-service.youdo.sg alias; retain until its role is understood.

## Step1 preflight result (2026-10-14)

[Fresh preflight and user-authorized CI variable copy](2026-10-14-nomad-test-devops-898-preflight.md) supersedes group-inheritance assumptions above. Both tokens are now in youdo. Runner host connectivity passes; app image manifests/auth and stale RabbitMQ/MSSQL consumer configuration remain blockers. mssql-test5 producer is accepted and LogReader uses per-stand generated Consul addresses, not the shared logging connection string.

## Final implementation plan (revised after preflight)

Goal: deploy11single+2dynamic services in VK Nomad, replacing internal yandex-test routes and CI access while preserving public-test.
Architecture: existing v3CI and per-service HCL; perform minimal configuration changes first, rebuild once afterward, and deploy reviewed HCL with explicit verified image tags. Legacy pipeline retries retain old CI YAML and must never be mistaken for deployment of the new configuration.

1. Preflight evidence retained. Nomad8ready/eligible clients; resources sufficient (about53GiB steady requested versus about460GiB scheduler headroom). Runner105/106 host DNS/Nomad HTTP pass; job-container path remains untested. User-approved VK tokens are now present in youdo and API200-verified. Required Vault paths and dotnet/resources policies exist. mssql-test5 generated SQL endpoint is accepted and reachable; other15LogReader SQLtargets remain unavailable. All20Nexus app component paths have no listed image tags; all8clients lack Nexus auth. No builds/deployments have been started.
2. Establish approved branches and exact source versions. Refresh gitlab-ci-templates local clean69cec4d against remote master6d9b695; inspect working trees without discarding changes. Proposed template branch DevOps-898-deploy-single-dynamic-on-vk from origin/master. Service branches only where CI/HCL needs correction: DevOps-898-restore-test-service-on-vk from each origin/master. Before repository edits, obtain branch/repository/base approval under supervised rules. Record each service application source tag/commit and resulting image tag before builds; listed historical releases are candidates, not an instruction to retry now. If configuration changes create a new source commit, reselect its source/ref before the single rebuild.
3. Apply minimal internal-test configuration changes. Modify v3/.deploy-test-single.yml and v3/.deploy-test-dynamic.yml: job names/ENV_NAME/NOMAD_VAR_dc/NOMAD_VAR_proxy=vk-test; DEPLOY_NOMAD_ADDRESS=http://nomad.service.vk-test.consul:4646; DEPLOY_NOMAD_TOKEN=$NOMAD_TOKEN_VK_TEST. Update DEPLOY_TEST_DYNAMIC_STANDS in v3/.deploy-test-dynamic.yml to test,test1..test15, checking overrides and independent public-test list. Preserve all public-test variables/rules/effective jobs and production behavior. Socket .gitlab-ci.yml must select dynamic. DebuggingEvents HCL must point to its own companion Elasticsearch using VK routing. Migrate active hardcoded logging SQLhost in textvalidation/DebuggingEvents; review all13routes and backend references. Do not delete unused NOMAD_IP_ADDR variables or alter call-service external alias automatically.
4. Prepare runtime dependencies before dependent rollout. Add Nexus auth through the existing common Nomad-client Docker-auth configuration (credentials external, no literals; local source changes need approved task branch, remote apply needs separate approval). Resolve VK RabbitMQ: old Vault address fails DNS, candidate10.18.26.7:5672refuses; restore/verify broker and then update the target VK Vault ADDR only under explicit authorization. Update shared logging SQL connection string for geocoder/mailer only after selecting a working YouDoLogsExceptions database/endpoint; avoid confusing it with LogReader per-stand Consul server keys. Change old PostgreSQL DC alias to verified VK hostname with preserved credentials. mssql-test5 recovery is complete; use it for initial LogReader pilot. Remaining15SQLstands need their existing recovery workflow before full16stand acceptance. External S3/SMTP/iDigital/API migrations are not automatically added to scope.
5. Validate and review configuration before rebuilding. Local YAML/HCL checks; Nomad job validate/run-output with exact image/version/DC/proxy/stands variables; inspect only nonsecret rendered fields. GitLab lint/dry-run must resolve reviewed candidate template refs; its POST operation requires approval under user rules. Check renamed-job consumers/needs and consumers outside13; code search API currently unavailable400, so do focused repository inventory before shared publication. Check unchanged public-test/prod jobs, dynamic group count and no old active internal-test backend references. Present actual diff/checks, source/target, commit/MR names and CI effects for publication approval; no merge or deployment implied. Merge/release order must account for unpinned includes in all13apps.
6. Build once after configuration/source choices are settled. Use the selected release tag or current master commit. For .NET, start at prepare-nuget (independent dependencies:[]); regenerate set-variables if dotenv is missing/expired before component build. For other languages no prepare-nuget exists in selected pipelines; regenerate set-variables as needed and run their actual component builds. Do not rerun set-variables-nomad or build-monitoring as build prerequisites. Historical retry preserves historical compiled YAML but .NET builds clone current shared Dockerfile: only use retry when the chosen source/configuration and effects are still correct. If new commit/pipeline is needed, first verify it starts build jobs without automatic test/prod deployment; do not create an unsafe normal master auto-release pipeline. Build authorization covers images only; changed source/ref/effects must be reviewed before execution. CI builds push selected tag and overwrite latest; deployments must use the recorded explicit tag rather than latest. Verify every required component manifest/digest in Nexus after builds and retain job URLs/failure reasons. Library/build failures are investigated from actual job results; no speculative refactors.
7. Deploy reviewed configuration in stages, under separate runtime approval. Select dependency-ready single pilot with verified images, then LogReader test5 or Socket test5 only when their specific dependencies pass. Use updated HCL/CI, never the old pipeline deploy-job snapshot. Bind the exact built image tag to NOMAD_VAR_version and image repository to NOMAD_VAR_image; this must match manifest verification, not an automatically derived unrelated branch tag. Nomad job plan against VK first (exit0nochanges/1expectedchanges/255error), then approved deployment. Expand singles by dependency order; expand dynamic to all16stands once SQL/broker/API readiness permits. Do not execute migrations/DB-drop or production jobs as image-build steps.
8. Accept and record results. Require successful deploy-job despite allow_failure, healthy allocations/Consul checks, Vault rendering, vk-test DNS/Traefik routes, service smoke tests and no failed old backend connections. Dynamic final acceptance covers all16stands; test5pilot alone is partial. No previous13targetjobs exist in VK; record any intervening job baseline. On failure stop expansion; restore previous VK spec/image if one exists, otherwise stop only the newly created job with explicit approval. Never revert to Yandex automatically. Record per-service version/image/domain/dependency/result; update KB and task under the required external permissions.

## Release/build candidates (read-only baseline)

| Service | Candidate source/ref | Existing pipeline |
| --- | --- | --- |
| geocoder | 1.2.12 | 119382 |
| youdo-call-service | 0.0.9 | 133637 |
| youdo-business-doc-generator | latest master, same commit as master-136 | 137986 |
| chat-content | 1.1.16 | 118609 |
| textvalidation | 1.0.3 | 125804 |
| tinkoff-e2c-sign-service | 0.0.10 | 115512 |
| vks-policy-generator | 0.0.26 | 115516 |
| DebuggingEvents | 1.0.84 | 115519 |
| blec | 1.0.2 | 115718 |
| pechkin | 2.14.24 | 136281 |
| mailer | 8.1.10 | 131625 |
| LogReader | 1.0.39 | 122131 |
| Socket | 1.2.9 | 133044 |

These sources were identified before pending repository changes. Existing master is newer than selected release in some projects; release preference is allowed by user, not permission to ignore a later approved source decision. Exact SHA/job IDs/downstream statuses are in /home/slnnk/ai-data/DevOps-898/build-candidates-dotnet.json and build-candidates-other.json. All5non-.NET set-variables build.env GET404; four.NET dotenv expirations are already past. Regenerate as needed after choosing final pipeline/source. No retry or pipeline creation was performed.

## Risks and review focus

Fresh preflight identified image/tag/auth and RabbitMQ/logging-SQL blockers. Partial SQL readiness supports test5pilot, not all16stands. Historical CI snapshot versus live cloned Dockerfile and latest overwrite must be reviewed when choosing build execution.

Unpinned shared includes affect consumers outside the article; audit before publication. Socket mode mismatch must be corrected. DebuggingEvents owns its companion ES; verify both tasks and the new route. Wrong variable scope/override can retain old Nomad access. Dynamic defaults and service overrides can deploy excluded stands. Green pipelines can conceal failed deploy jobs. SQL recovery is not yet accepted everywhere. Public-test must retain its original behavior throughout.

## Changes and approvals

KB log/map/backlog and sanitized local audit were created/updated; user-approved VK CI variables were also added to youdo. User corrections: shared internal-test templates may replace Yandex rather than add coexistence; public-test excluded. No branch name/base approval, Git publication approval or application runtime approval has been given. User requested build retries, then agreed to finish the plan before execution; no build was started. No secrets recorded.

## Portable lesson

none
