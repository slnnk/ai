---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [logreader, nomad, gitlab, consul]
---

# LogReader all active VK stands recovery

## Summary

LogReader1.0.39 is restored and accepted on all14active VK stands (`test`, `test1`–`test7`, `test10`–`test15`). The user approved the13Consul endpoint changes, explicitly requested the persistent project stand variable and new release pipeline, then approved manual VK deployment. Pipeline141021 preparation/build/tests and deploy3230221 all succeeded. Fresh read-only acceptance confirms14healthy Nomad groups/allocations, all Consul checks passing, HTTP200 for all14 URLs, zero task restarts, and no matched failure classes in28inspected stdout/stderr log streams. SQLSELECT1 passed on all14existing YouDoLogsExceptions databases before rollout. test8/test9 remain excluded. YouTrack comments have not been updated; the prepared comment plan now includes this completed rollout. Earlier pending statements below are historical stages and are superseded by final acceptance.

## Context and scope

Active scope: `test`, `test1`–`test7`, `test10`–`test15`. Exclude test8 (removed by user) and test9 (previously excluded). The historical dynamic template defaults to 16 groups, so pass an explicit active stand list. Do not change public-test or production. No source changes are needed to remove the pilot restriction: the pilot used the GitLab manual job variable NOMAD_VAR_stands=["test5"].

## Actions and findings

- Ran ai-sync.sh successfully with no output/reminders; consulted CONTEXT.md, TODO.md, repos.md and existing rollout evidence.
- Used systematic-debugging to trace HCL -> Consul stand SQL key -> Vault USER/PASSWORD -> YouDoLogsExceptions.
- GET Nomad confirms job `logreader`, dc vk-test, version 1.0.39, job version0, one running healthy allocation/group test5.
- GitLab project99 pipeline140905/ref1.0.39/SHA642c1c70c65b89aa8a6bdbd88557bde4d8811a08 contains successful build/test and latest deploy dynamic vk-test job3230188, which ran 2026-10-16 00:52 Moscow. Runtime remains one group. The job-variable GET endpoint was unavailable, so the exact latest retry variables were not inspected.
- DNS and TCP succeeded from Nomad client01 (10.18.26.34) to all14 canonical VK SQL endpoints.
- Eleven thin SQL endpoints passed SELECT1 directly from the workstation. Direct thick SQL checks timed out from the workstation; the same checks through temporary local SSH forwards on Nomad client01 passed on test/test1/test6. This establishes SQL login/database access via the runtime network route; no SQL data was modified.
- Credential source: Vault secret/resources/databases/mssql fields USER/PASSWORD, matching HCL. Database YouDoLogsExceptions. Credentials remained in memory and SQLCMDPASSWORD; no values saved or printed.

## Concrete endpoint update prepared

Command: `python3 /home/slnnk/ai-data/DevOps-898/logreader_consul_endpoints.py --apply`.

It will CAS-update exactly13 keys `test_instances/<stand>/mssql_db`, verifying the reviewed baseline value and ModifyIndex before writing. Targets: test/test1/test6 -> vk-ms1-sql-<stand>.mcs.local,1433; thin stands test2/test3/test4/test7/test10–test15 -> sql-<stand>.service.vk-test.consul,14300+stand-number. test5 remains sql-test5.service.vk-test.consul,14305. The script updates only endpoint keys, reads each back, and records sanitized receipts incrementally. It stops on a concurrent edit; multi-key application is not atomic, so the receipt identifies partial progress if any failure occurs. It does not deploy services or change Vault, SQL databases, repository files or Git state.

## Subsequent deployment approach

Use the established GitLab `deploy dynamic vk-test` path, release1.0.39 and an explicit14stand NOMAD_VAR_stands. Existing deployment job is already successful. The documented jobs retry API does not expose custom variable overrides (manual play does), so do not assume retrying the existing pilot changes its stand list. Prepare the next concrete GitLab action after the endpoint update, including any new pipeline build/test/image publication effects, and request separate approval. Prefer a valid existing manual VK job if one is available at that time; never use the old Yandex deployment job as a substitute. Official API reference: https://docs.gitlab.com/api/jobs/.

## Evidence and changed files

Local helpers and sanitized evidence under /home/slnnk/ai-data/DevOps-898:

- logreader_rollout_preflight.py and logreader-rollout-preflight.json: GET runtime/CI/Consul metadata, no secret contents saved.
- logreader_sql_all_stands.py and logreader-sql-all-stands.json: fourteen SQLSELECT1 results and Nomad DNS/TCP checks; --via-nomad checks thick SQL through temporary local forwards.
- logreader_consul_endpoints.py and logreader-consul-endpoints-plan.json: reviewed13key before/after values and CAS indexes; --apply has not run.

Updated existing system map, central backlog and sync/index bookkeeping. Repository checkout remains master with no local modifications. No YouTrack comments or external configuration changed during this preflight.

## Risks and acceptance limits

Service rollout is pending. SQLSELECT1 establishes login/database access, not full exception-log functionality. No task state is reopened. No infrastructure changes, database recreation, tag creation, release publication or CI launch is authorized by the preflight. Stand coverage must remain14active rather than16historical. Endpoint keys may also be read by other stand consumers; the proposed change points them to restored VK SQL. Full runtime acceptance requires GitLab deploy success, all14 desired Nomad groups/allocations, Consul passing and per-stand HTTP checks, with SQL error classes inspected without printing secret-bearing logs.

## Approved endpoint correction and next pipeline proposal

The user explicitly approved only the13Consul endpoint changes (reply “Да”). Executed `python3 /home/slnnk/ai-data/DevOps-898/logreader_consul_endpoints.py --apply`; exit0, verified_updates13, deployedfalse. Receipt: `/home/slnnk/ai-data/DevOps-898/logreader-consul-endpoints-receipt.json`; partial_application_possible=false. No Vault or SQL data changes.

Next reviewed command: `python3 /home/slnnk/ai-data/DevOps-898/logreader_new_pipeline.py --create`. This creates a new LogReader project99 pipeline on existing release tag1.0.39/SHA642c1c70c65b89aa8a6bdbd88557bde4d8811a08, setting both DEPLOY_TEST_DYNAMIC_STANDS and NOMAD_VAR_stands to the14active stands. It automatically performs preparation, unit tests, build-web and publishes/overwrites both web:1.0.39 and web:latest. VK/public-test/production deploy jobs remain manual. No Git tag, source modification or production deployment is proposed. The subsequent manual VK deployment requires its own approval. The older pipeline122131 has only Yandex jobs and cannot substitute for a fresh VK manual job. Pipeline creation has not been authorized or executed; no new-pipeline receipt exists.

The turn was interrupted by a server restart after preparation; local receipt inspection confirmed completed13key writes and absent pipeline creation receipt. No remote mutations were repeated.

## Persistent stand-list clarification

Fresh GET confirms shared gitlab-ci-templates master v3/.deploy-test-dynamic.yml still defines DEPLOY_TEST_DYNAMIC_STANDS as test/test1-test15 (16 entries), including removed/excluded test8/test9. Complete paginated project99, microservices group158 and parent youdo group variable reads found no DEPLOY_TEST_DYNAMIC_STANDS or NOMAD_VAR_stands overrides. Creating a pipeline alone does not deploy; playing its default VK dynamic job requests16groups of count1 in the existing logreader Nomad job, not18additional instances. The proposed14stand pipeline variables are persistent only for that pipeline and do not fix future pipeline defaults. The user asked where the list is stored; no pipeline creation approval was given. A persistent source/default correction should be considered before rollout; repository branch approval is required before any such source edit under supervised training.

## Persistent project variable and pipeline141021

The user explicitly requested adding the stand variable in project CI/CD Variables and starting a new pipeline. This authorized those two actions; no manual deploy was included.

Created project99 CI/CD variable DEPLOY_TEST_DYNAMIC_STANDS with the14active stands, variable_type=env_var, environment_scope=*, protected=false, masked=false, raw=true. GET readback matched every field. Receipt: `/home/slnnk/ai-data/DevOps-898/logreader-project-stand-variable-receipt.json`. No group/global CI template changes.

Created [pipeline141021](https://gitlab.youdo.sg/youdo/microservices/YouDo.Web.LogReader/-/pipelines/141021), ref1.0.39, SHA642c1c70c65b89aa8a6bdbd88557bde4d8811a08. Request included only ref, without pipeline-level stand variables; the persistent project variable is the source. Receipt: `/home/slnnk/ai-data/DevOps-898/logreader-all-stands-new-pipeline.json`.

Fresh GET verification: all5 preparation/build/test jobs SUCCESS: set-variables3230216, prepare-nuget3230217, set-variables-nomad3230218, build-web3230219, dotnet-unit-tests3230220. Pipeline status manual. Deployment [job3230221](https://gitlab.youdo.sg/youdo/microservices/YouDo.Web.LogReader/-/jobs/3230221) deploy dynamic vk-test is manual and ready. The build's normal publication includes web:1.0.39 and web:latest. Public-test and production jobs were not played.

The next concrete action is `python3 /home/slnnk/ai-data/DevOps-898/logreader_deploy.py --play`: one POST to jobs3230221/play, deploying LogReader1.0.39 via the standard GitLab path to all14active stands. It checks release SHA/ref, all preparatory job results, the persistent project variable and absence of pipeline stand overrides before play. It does not create/recreate SQL databases; the HCL only declares LogReader groups and consumes existing SQL endpoints. This manual deployment requires the next explicit approval.

The local read-only default of logreader_deploy.py saved fresh evidence at `/home/slnnk/ai-data/DevOps-898/logreader-all-stands-pipeline-status.json`, ready_for_deploy=true. No deployment play receipt exists.

## Final approved deployment and acceptance

The user replied “Да” to the concrete manual VK job3230221 deployment proposal. Ran `python3 /home/slnnk/ai-data/DevOps-898/logreader_deploy.py --play`; the script rechecked the release SHA, persistent project variable, no pipeline stand overrides and all5successful prerequisites, then played exactly that job. No other GitLab job was played. Receipt: `/home/slnnk/ai-data/DevOps-898/logreader-all-stands-play-receipt.json`.

Fresh command `python3 /home/slnnk/ai-data/DevOps-898/logreader_runtime.py` produced all_accepted=true at2026-10-15T22:10:35UTC (2026-10-16 01:10:35Moscow). [GitLab job3230221](https://gitlab.youdo.sg/youdo/microservices/YouDo.Web.LogReader/-/jobs/3230221) SUCCESS. Nomad job logreader has version1.0.39, dc vk-test, jobversion1, exactly14expected groups, one running healthy allocation each. All tasks running with0restarts. All14service registrations match their active allocation IDs; every returned Consul check is passing. All14 `http://logreader.<stand>.vk-test.youdo.local/` URLs return200. The28stdout/stderr tail reads all succeeded and yielded no matched SQL/unhandled/image/Vault/OOM failure classes. Saved only sanitized classes/statuses, no raw logs or credential-bearing templates.

Exact result artifact: `/home/slnnk/ai-data/DevOps-898/logreader-all-stands-runtime.json`. Acceptance is service availability and existing database access, not a synthetic exception-write/read functional test. SQL databases were not recreated by the LogReader job. Earlier test5-only acceptance remains historical; all14active stand availability is now verified. The comment plan for DevOps-898 must replace its old pilot-only limitation with this final scope and link the successful deployment.

Updated the current system map, LogReader repository entry, VK address-map verification status, central backlog, comment plan, index/sync bookkeeping. No repository source files or Git state changed; no YouTrack writes, production/public-test/autotest deployment, or test8/test9 recreation performed.
