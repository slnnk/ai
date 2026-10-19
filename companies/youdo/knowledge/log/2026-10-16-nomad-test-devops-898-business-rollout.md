---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [devops-898, business, nomad, ansible, postgresql]
---
# DevOps-898 Business test10-15 deployment

## Summary

Deployment COMPLETE on test10–test15: Business master-21509, ordinary third-attempt jobs3230182–3230187 all SUCCESS, exact Nomad jobs running/healthy with restarts0 at2026-10-15 21:45:17UTC (2026-10-16 Moscow). All66 task image references independently verified master-21509. User merged final pager fix MR120/585b5992 and explicitly authorized the retries. Main and mock databases recreated. Business completes the agreed13-service B2B catalog; shared doc-generator reused. Verification uses GitLab/Nomad statuses only. Earlier failures and approvals below are retained as history.

## Task

User explicitly requested starting ordinary Business deployments on test10–test15 after MR118 was merged. Parent launched all six ordinary jobs; scope includes main/mock DB recreation. This authorization covers the initial six jobs only, not subsequent retries or infrastructure changes.

## Context

Business project423, pipeline140959, release master-21509/current source523609a16. All nine builds succeeded. Ansible MR118 user-merged8179d6cf provides six shared literal VK Elasticsearch/FlashCall addresses through runtime repository clone. Existing jobs3227749–3227754 map sequentially to test10–test15. Receipts `/home/slnnk/ai-data/DevOps-898/business-test10-deploy.json` through test15. Parent launch helper `business-deploy.py` checked release/builds/template/ordinary-job scope before playing jobs.

## Actions

Read-only monitoring via `business-preflight.py --project 423 --service youdo-business --output /home/slnnk/ai-data/DevOps-898/business-rollout-status.json --brief`. Exact Nomad job IDs were matched to avoid accidentally including other B2B services. Read bounded error lines from all six GitLab traces; no raw logs or credentials saved. Checked OS-role identity using read-only SELECT1 on B2B PostgreSQL10.18.26.44.

## Findings

At2026-10-15 21:32:03UTC/2026-10-16 Moscow all six jobs3227749–3227754 FAILED, exact Business Nomad jobs absent on all six target stands. The stop-missing-job failure is ignored as expected. Blocking failure occurs at `Recreating main db`, before SQL execution:

`ModuleNotFoundError: No module named 'ansible.module_utils.six.moves'`

Delegated Ansible command-module bootstrap fails on `postgres-b2b.service.vk-test.consul`. This matches the previously diagnosed Ansible2.9.7/Python3.12 incompatibility from DevOps-899, addressed for generic PostgreSQL tasks using `raw` (MR110). Business uses a separate playbook and still has two legacy `command` tasks.

Additional necessary compatibility correction: these two tasks lack `become_user: postgres`. Actual read-only root `psql -U postgres -d postgres -c SELECT1` fails peer authentication; the same read as OS user postgres succeeds. Minimal source fix must use `raw` and `become: true`/`become_user: postgres` on both main/mock DB tasks, preserving SQL and `dropdb` tags. No DB modifications occurred before the module bootstrap error. No retries or source changes performed by this monitor.

## Changes

Only local monitoring/KB artifacts. No new Business runtime addresses discovered because jobs were never created; address map does not gain invented hostnames. Initial readiness is superseded by this observed special-playbook failure.

## Risks and limits

This section records the initial failure; final deployment acceptance is documented in Summary and final section. Source fix branch/local edits require first training approval, publication requires reviewed stage-two approval, merge and retry deployment require applicable separate approval. No HTTP/Consul/functional acceptance checks performed. Preserve sixteen unrelated local MSSQL changes in automation-test-yandex checkout.

## Portable lesson

none

## Proposed recovery branch

Parent proposed stage-one branch `DevOps-898-fix-business-db-recreation` from origin/master8179d6cf0437cb64ee2b6006da5f5ba6ed5f6277, limited to the two DB tasks in `playbooks/deploy/docker/youdo_business.yml`: command→raw plus become postgres, preserving SQL/dropdb tags. User explicitly approved branch/local changes; parent created the approved branch from8179d6cf, preserving sixteen unrelated MSSQL paths. Existing generic reference `deploy_microservices.yml:175–186` already uses raw+become true/become_user postgres for PG recreation.

Planned verification: exact two-task semantic diff preserves all SQL/delegation/dropdb tags; YAML/Ansible syntax checks; raw action accepts _raw_params and executes without remote Python; read-only SELECT1 through approved SSH route as postgres OS user already passed. No DROP/CREATE smoke test without explicit deployment permission. After implementation, review actual diff/checks before publication approval.

## Recovery implementation and publication proposal

Parent implemented only two DB tasks in `playbooks/deploy/docker/youdo_business.yml`: `command` → `raw`, with `become: true` and `become_user: postgres`. Existing `_raw_params` SQL dictionary retained. Independent YAML semantic review verified the exact two-task change, identical SQL/delegation/dropdb tags and all other playbook structures unchanged. Local `ansible-playbook --syntax-check` passed (parent evidence), `git diff --check` passed and index remains empty. Raw action accepts `_raw_params` and executes directly without remote Python; previous read-only SQL identity check passed as postgres. No destructive test/deployment performed.

Publication proposal: commit `run business database recreation without remote python`; MR `DevOps-898 fix business database recreation`; source `DevOps-898-fix-business-db-recreation` → target `master` in automation-test-yandex/project530. MR description: one short Russian paragraph plus DevOps-898 link only. User explicitly approved stage-two publication. Parent reviewed the actual cached diff containing only `youdo_business.yml`, committed `911f276b467b17e22bc8d8832a209604cb571008` (`run business database recreation without remote python`), pushed the approved branch and created [MR119](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/119) with proposed title/source→master. Preserved project settings: assignee a.solonenko, squash=false, remove_source_branch=true; no pipelines configured. Index empty; sixteen unrelated MSSQL paths preserved. MR119 awaits user merge; no merge or deployment retry authorized. Scope one explicit playbook path; sixteen unrelated MSSQL files excluded. This repository has no CI pipeline; after eventual merge, existing ordinary Business retry jobs clone the current default branch at runtime. Publication does not authorize merge or deployment retries.

## Recovery publication result

MR119 published at head911f276b after explicit user approval. Deployment remains all six initial jobs FAILED before SQL, exact Nomad jobs absent. Publication has no runtime effect until user merges and separately authorizes retries.

## User merge and authorized retry

User explicitly reported merge and requested restarting deployment. Parent verified MR119 merged at6b465a947c8ffd7b67f5c94e096aefa924f2736f, with both raw+postgres DB tasks in master. Parent retried six ordinary jobs only: test10/job3230176, test11/3230177, test12/3230178, test13/3230179, test14/3230180, test15/3230181; receipts `business-test10-db-fix-retry.json` through test15. Version remains master-21509; ordinary DB recreation retained. At21:38:17UTC all six jobs running, exact Nomad jobs not yet created. No additional retry or infrastructure action authorized.

## Retry blocked by interactive psql pager

The six approved retry jobs3230176–3230181 progressed beyond the original Python bootstrap/become problem but remained at `Recreating main db`; no exact Business Nomad jobs created. Job3230176 trace confirms SSH/become escalation succeeded and SQL command execution started. Read-only PostgreSQL-host inspection found six postgres-owned psql processes each with sh→pager descendants on allocated TTYs pts/2,3,5,7,9,11. PostgreSQL shows all six psql sessions idle/ClientRead after the first SELECT, ages173–181seconds at observation. This establishes an interactive output pager wait, not a database lock or Python failure.

Minimal additional fix: add `-P pager=off` to the psql command in each of the same two DB tasks. Existing generic reference `deploy_microservices.yml:177` already uses `psql -P pager=off -U postgres` with the same raw/become-postgres pattern. SQL/delegation/identity/dropdb tags need no further changes. First termination SELECT completed, but DROP/CREATE had not executed because psql was waiting on pager output. No pager/process termination, cancellation, further retry or source change performed by this monitor; all require applicable user authorization.

## Approved cancellation and pager correction

User explicitly approved canceling all six stuck jobs and the new recovery branch/local fix. Parent canceled jobs3230176–3230181; independent live GET verified all six terminal CANCELED. Read-only host process inspection verified all twelve previously recorded psql/pager PIDs disappeared; no process kill or SQL cleanup action performed by monitor.

Approved branch `DevOps-898-disable-business-db-pager` from master6b465a947c8ffd7b67f5c94e096aefa924f2736f. Parent changed only two commands in `playbooks/deploy/docker/youdo_business.yml`, adding `-P pager=off` and removing trailing whitespace on those two touched lines. Independent token/semantic review confirms identical remaining SQL, raw/postgres identity, delegation/dropdb tags and other task fields. Syntax-check and diff-check PASS; index empty, sixteen unrelated MSSQL paths preserved.

Parent performed a real read-only TTY reproduction check: SSH `-tt`, OS user postgres, `psql -P pager=off` with `SELECT generate_series(1,100)` returned all100rows and exit0 without hanging. No database mutation or service deployment included.

Publication proposal: commit `disable pager for business database recreation`; MR `DevOps-898 disable pager for business database recreation`; source approved branch → master. User explicitly approved stage-two publication. Parent reviewed actual cached diff containing only the two pager flags in this playbook, committed `bf91d5b9ec91cacf2bb48335b153390ba92ab858` (`disable pager for business database recreation`), pushed approved branch and created [MR120](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/120) with approved source→master and preserved project settings. No pipelines configured. Index empty; sixteen unrelated MSSQL paths preserved. MR120 awaits user merge and separate retry authorization; no merge/deployment performed.

## Final user merge, retry and acceptance

User explicitly reported MR120 merged and requested restart. Parent verified merge585b599273d20b810a78f019583d3ab8b39f554b, current master containing raw+postgres identity and both pager-off flags. Parent retried six ordinary jobs: test10/3230182, test11/3230183, test12/3230184, test13/3230185, test14/3230186, test15/3230187; receipts `business-test10-pager-fix-retry.json` through test15.

At2026-10-15 21:45:17UTC/2026-10-16 Moscow all six GitLab jobs SUCCESS and all six exact Nomad jobs running with current allocation healthy=true/restarts0. Bounded trace3230182 confirms main and mock DB recreation steps completed, followed by Nomad run and BuildInfo step. The ignored initial stop-missing-job message is expected, not a deployment failure.

The special job stores version in Meta.VERSION rather than Meta.IMAGE_TAG. Independent live Nomad image verification resolved all11 task image references per stand (seven runtime components and four pre/post migration tasks): all66 use master-21509, matching current release/source523609a16. Sanitized evidence `/home/slnnk/ai-data/DevOps-898/business-final-image-routes.json`, final status `business-rollout-status.json`. No extra retry, infrastructure change, HTTP or Consul acceptance checks performed.

Business is the final catalog service: all13 B2B dev-catalog services are now available on test10–test15, with existing shared doc-generator reused. SMS/Fns/DocValidation had also been accepted on C2C targets earlier. Status-based delivery is complete; no business-functional or external-provider claims. Observed runtime Nomad routes were added to current/service-addresses.env with date and status-only verification limits.
