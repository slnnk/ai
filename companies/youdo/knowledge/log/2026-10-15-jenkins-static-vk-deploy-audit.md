---
system: jenkins
status: verified
checked: 2026-10-15
tags: [static, jenkins, gitlab, vk-test]
---
# youdo.static deployment VK address audit

## Task

User asked whether youdo.static deployment needs changes during test5 monolith recovery. Read-only audit; WEB_STATIC remains false in current build5822. No source, variables, job settings or static deployment changed.

## Execution path

Live dynamic_deploy Deploy static calls playbooks/deploy/app/deploy_static_to_s3.yml. Despite its name this is a GitLab job launcher: selected project278 STATIC_PIPELINE_ID is searched for deploy_yandex_test 5/... then play/retry is posted during actual deployment. That GitLab job in youdo.static invokes deploy_static_nomad.yml for SSR and uploads assets to S3. Job names containing yandex are names, not endpoint addresses, and need no rename for minimal migration.

## Confirmed address changes needed

- automation-test-yandex/group_vars/all.yml:20 ssr_api_internal_url contains yandex-test, passed as SSR INTERNAL_URL by playbooks/deploy/docker/nomad_static/youdo-static.j2:68. Use the VK datacenter address.
- all.yml:16 buildsinfo_addr contains old buildapi.yandex-test; consumed by static result publication including required PUTs in downstream gitlab deploy_static_to_s3. Current canonical BuildAPI endpoint http://buildapi.dev.youdo.corp is recorded in service-addresses.env and DevOps898 recovery notes.
- playbooks/deploy/docker/deploy_static_nomad.yml:6-7 reads NOMAD_YANDEX_TEST_ADDR/TOKEN. Read-only project278 and ancestor CI-variable inspection confirmed group8 wildcard/unprotected endpoint is still http://nomad.service.yandex-test.consul:4646, so this is an actual stale endpoint, not merely an old variable name. Token is configured; its value was not printed/saved/tested. Access material location only: GitLab group8 CI variable NOMAD_YANDEX_TEST_TOKEN, read through current user's GitLab API role. Bind deployment to verified VK endpoint/token without unnecessary renaming of unrelated variables.

dc already vk-test; Nomad datacenter and Traefik route generation use it. External assets/S3 endpoints intentionally remain unchanged. Static image tag uses CI_COMMIT_REF_SLUG-MAJOR_VERSION.CI_PIPELINE_ID, distinct from monolith numeric pipeline tag.

## Current monolith deployment

Build5822 still running at audit completion, last observed task app_deploy Unpack artifacts. All five PostgreSQL reset tasks succeeded. Static switch remains false; its old endpoint variables are not activated by this static stage in the current run.

## Changes and limits

Only KB audit files updated. No static source edits, CI variable changes, play/retry call or artifact/image build. Read-only variable audit establishes the endpoint, not Nomad token validity or full static acceptance. Additional implementation requires requested scope/branch approval per supervised workflow.

## Related evidence

[Current deployment attempts](2026-10-15-jenkins-test5-deploy-retry.md), [Jenkins map](../systems/jenkins.md).

## Static change preparation and branch proposal

User requested preparing static changes. No standing publication/merge/deployment permission inferred from the previous PostgreSQL task. Proposed repository automation-test-yandex, baseorigin/master18c8d0e7, branch DevOps-892-adapt-static-deploy-to-vk; branch approval pending before repository edits.

Prepared ~/ai-data/jenkins-recovery/static-vk-proposed.patch outside checkout: group_vars/all.yml changes BuildAPI URL and SSR INTERNAL_URL uses dc; deploy_static_nomad.yml uses dc-driven default Nomad URL, removes legacy Yandex token lookup, and selects explicit existing nomad_stage_token override or common nomad_token. This preserves public-test token/address overrides without a new token alias. Common nomad_token already reads external VK_TEST_NOMAD_TOKEN.

Inherited GitLab group8 also has NOMAD_TOKEN_VK_TEST (wildcard/unprotected); canonical VK_TEST_NOMAD_TOKEN absent in project278/direct ancestor group8 at inspection. Known accepted canonical token source is current/.env key VK_TEST_NOMAD_TOKEN; no value exported or copied. Prepared metadata-only CI variable plan ~/ai-data/jenkins-recovery/static-vk-ci-variable-plan.json for project278 keyVK_TEST_NOMAD_TOKEN, maskedtrue/protectedfalse/scope*. Creating it requires later explicit permission; no API write performed.

youdo.static CI normal test jobs already clone automation master and invoke static play, so no youdo.static repo file edit proposed. Existing job names and external S3 untouched. Global BuildAPI/SSR settings are shared defaults and affect other consumers too, as intended address synchronization. Existing large MSSQL local modifications excluded from proposed scope.

Meanwhile build5822 reached terminalFAILURE370631ms after successful PG reset; failure diagnosis pending separately from static preparation.

## Approved local implementation

User explicitly approved branch DevOps-892-adapt-static-deploy-to-vk. Created it from origin/master18c8d0e7 in existing automation-test-yandex checkout; no worktree. Applied prepared two-file diff, +5/-6. Shared BuildAPI/SSR defaults changed; Nomad default address dc-driven, token selection retains explicit public-test override with fallback to common nomad_token. No new token literal/alias.

Offline ansible-playbook -i localhost, playbooks/deploy/docker/deploy_static_nomad.yml --syntax-check -e test_instance=test5 passed; scoped git diff --check passed. Independent read-only review found no blockers and confirmed override precedence. End-to-end deployment and endpoint connectivity were not tested; CI variable remains required and uncreated.

Actual diff hunk function context inadvertently exposed the existing buildsinfo_pass value in tool output. Value is not repeated/stored in notes or new scripts. Secret location only: automation-test-yandex/group_vars/all.yml buildsinfo_pass, repository access through current user. Separate rotation item recorded; no credential change in this task.

Publication proposal: commit adapt static deployment to vk cloud; MR DevOps-892 Adapt static deployment to VK Cloud; source approved branch, targetmaster. MR body prepared in ~/ai-data/jenkins-recovery/static-vk-mr-body.txt, one Russian paragraph plus DevOps-892 link. No CI configuration edit or automatic deployment in this diff; shared default address changes affect all consumers after merge. Commit/push/MR creation not yet authorized or executed. Project278 masked canonical variable creation is a separate external change, plan only.

## Confirmed publication

User explicitly confirmed reviewed diff and commit/push/MR proposal with Подтверждаю (after an equivalent keyboard-layout typo). Checked real index empty, staged exactly group_vars/all.yml and playbooks/deploy/docker/deploy_static_nomad.yml, reviewed sanitized staged diff without YAML hunk function context. Commitf42412797e09ee1ea96d1e5ed680fca1d6fcc8dc, adapt static deployment to vk cloud, +5/-6; pushed approved branch and set upstream.

Created [MR108](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/108), DevOps-892 Adapt static deployment to VK Cloud, source DevOps-892-adapt-static-deploy-to-vk, targetmaster, assignee a.solonenko, squashfalse/remove-source-branchtrue. Exact source SHA and MR metadata verified by publication helper. Pipeline list empty at publication. MR not merged; no CI variable creation or static deployment authorized/performed.

During publication user additionally requested checking Jenkins job logs. Build5822 failure is the old shared BuildAPI /upload URL; this MR already contains that address correction. See linked deployment evidence.

## Authorized integration follow-up

User authorized merge108/test5 deployment, CI canonical variable update and latest-release static build. MR108 mergedf916ad19; project278 VK_TEST_NOMAD_TOKEN created masked/scope*. No youdo.static source change needed. See [integration and rebuild](2026-10-15-jenkins-static-release-rebuild.md).
