---
system: jenkins
status: verified
checked: 2026-10-20
tags: [nginx, gitlab]
---
# DevOps-903: nginx cache cleanup empty-input fix

## Task and context

User requested the fix after creating DevOps-903. Existing checkout: `/home/slnnk/git/automation-test-yandex`, project `sysadmins/automation-test-yandex`. Historical symptom: ignored rc123 in dynamic_deploy5826 because empty grep output still launched rm.

## Actions and approval evidence

First proposal: branch `DevOps-903-fix-empty-nginx-cache-cleanup`, base `origin/master` ed63e3d. User approved. Switch was aborted by Git because local MSSQL restore changes overlap the newer master; no files were discarded. Revised proposal: same branch from existing HEAD bf91d5b9, which is already an ancestor of origin/master; nginx task identical to master. User explicitly approved the revised base. Created the agreed branch, preserving all 16 unrelated MSSQL modified/untracked paths and the empty index.

Added only `-r` to xargs in `playbooks/deploy/nginx/clear-cache.yml`. No other behavior changed.

## Validation and publication preparation

YAML parse PASS. Executed the command extracted from the playbook against a temporary cache: empty search rc0/no stderr; matching file removed; unrelated file retained; repeat rc0. `git diff --check` PASS. No live cache purge or Jenkins deployment performed.

GitLab GET confirmed master default, empty ci_config_path and auto_devops_enabled=false. No `.gitlab-ci.yml` in origin/master; no configured pipeline/deploy expected from publication. No open MR on the task branch; assign a.solonenko, squash off, source deletion on merge per inspected defaults.

Prepared commit: `fix nginx cache cleanup with empty search results`. MR title: `DevOps-903 fix nginx cache cleanup with empty search results`. Ready MR from `DevOps-903-fix-empty-nginx-cache-cleanup` to `master`. Russian body and proposal stored in `~/ai-data/gitlab-workflow/DevOps-903/automation-test-yandex/`.

## Status and risks

User approved the exact publication proposal. Snapshot check matched; staged diff and resulting commit contained only the one-line task change. Commit `d26e37e401763f7ae32bbfaaf4aa78286040b1e2` pushed, ready [MR122](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/122) created with exact SHA/title/body/source/target verified, assigned a.solonenko, squash off, source deletion on merge on, pipelines empty. Sandbox DNS failures required escalated network access; read-only inspection confirmed no MR before the create retry. Later verify found no open MR because the user had merged it. Direct GET confirmed state merged, merge commit `d9ee37aaa97bdfe036eb425b47b6bad8976cb7d1`; fetched origin/master contains xargs -r. No agent merge, tracker write or deployment. All16unrelatedMSSQL paths preserved. Task closed in [central TODO](../../../../TODO.md); live cleanup/runtime acceptance not exercised.

## Portable lesson

None.

## YouTrack comment (2026-10-20)

User requested a task comment and explicitly removed deployment and local-test paragraphs from the proposed text. User approved the final concise fix/MR text. Initial GET found no comments; published comment `74-124712` to DevOps-903 and independently GET-verified exact text. Issue state unchanged. Payload and result retained under the task artifact directory. These text corrections apply to this comment.
