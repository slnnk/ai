---
system: nomad-test
status: verified
checked: 2026-11-10
tags: [nomad, configuration, gitlab]
---
# DevOps-916 CallMasking stand configuration

## Task

Implement and publish DevOps-916 CallMasking Endpoint and Secret settings for monolith test stands. Related application MR: https://gitlab.youdo.sg/youdo/youdo/-/merge_requests/10112 .

## Context and findings

Repository `/home/slnnk/git/automation-test-yandex`; Nomad overlays `nomad_environment.json.j2` after the common environment config in `prepare_configs.yml:101`. Initial advice to use only the common template was too categorical; the user corrected it, and history confirmed existing service additions in the Nomad overlay. For this task the Nomad overlay is the selected destination. The user explicitly supplied both setting templates. Secret values are omitted from this note; the repository is the source of the approved configuration.

## Approvals and actions

Initial branch/base proposal: `DevOps-916-call-masking-config` from `origin/master`, approved by the user. Switching failed because it would overwrite unrelated local MSSQL edits in `3-restore-from-backup.yml`; no stash/reset or worktree was used. The user then explicitly approved creating the same branch from current HEAD `d26e37e401763f7ae32bbfaaf4aa78286040b1e2` and requested an MR. After presentation of the actual four-line diff, checks, commit/title/body, source/target and CI effects, the user explicitly approved publication.

Snapshot guard matched before staging; the index was initially empty. Reviewed the full staged diff, committed only the single requested template, pushed and created ready MR130 assigned to a.solonenko, squash false, remove source on merge true. All 16 unrelated MSSQL modified/untracked paths were preserved.

## Validation and outcome

Jinja2 StrictUndefined render, JSON parsing and exact CallMasking value assertions passed for all22 stand files; git diff --check passed. No tracked .gitlab-ci.yml, remote ci_config_path empty, Auto DevOps false; no MR pipelines.

Commit `8e33aedfd10da49302a7d2feb7954da03cc0e6ea`, source `DevOps-916-call-masking-config`, target `master`, title `DevOps-916 add call masking settings for test stands`. MR https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/130 was created and verified. A later helper lookup found no open MR; direct GET by IID confirmed it had already been merged at18:19:15+03:00 into `f49c108cf642385b93e0c940d67c891f6fcc9b92`. The agent did not merge it. Head pipeline null.

## Status and risks

2026-11-10: User confirmed DevOps-916 closed. Closure is accepted on the user report; no tracker write or additional runtime verification performed.

Requested source edit and publication complete. No deployment or runtime validation requested or performed. Endpoint retained exactly as requested, without a URL scheme. Task-scoped TODO reconciliation found no existing DevOps-916 item; no new follow-up is required for the completed publication request. Background push and publication commands finished.

## Portable lesson

none

## InternalApi follow-up (2026-11-10)

User requested an additional `Services.InternalApi.Secret` stand template in the same Nomad overlay and confirmed placement inside `Services`. Proposed and explicitly approved branch `DevOps-916-internal-api-secret` from current HEAD `8e33aedfd10da49302a7d2feb7954da03cc0e6ea` (already merged into master). The user asked to prepare an MR immediately. Created the approved branch and added only the requested three-line object; all unrelated MSSQL paths remained intact, index empty.

Jinja2 StrictUndefined rendering and JSON parsing passed for all22 stand files, exact requested value verified, and comparison against the original render confirmed all previous settings unchanged. Initial validation selected only3files by explicit instance key; corrected the file selection to cover all22stand files with inventory-name fallback. `git diff --check` passed. Read-only project GET confirmed empty ci_config_path and Auto DevOps false; no tracked GitLab CI configuration, so no automatic pipeline or deployment expected.

Publication proposal and snapshot: `~/ai-data/gitlab-workflow/DevOps-916/internal-api-secret/`. Proposed commit `add internal api secret for test stands`, ready MR title `DevOps-916 add internal api secret for test stands`, source `DevOps-916-internal-api-secret`, target `master`. Publication awaits the second supervised approval; no stage, commit, push, MR creation or runtime deployment performed. The earlier user closure applies to the completed CallMasking work; this separately requested follow-up is tracked in the central TODO. No background operations remain.

### InternalApi publication completed

The user explicitly approved the complete second-stage proposal with `Да`. Snapshot check matched before staging. Reviewed the entire staged diff (one template, three added lines), committed `b0693d4b921d23f9284199562b09d452ea84615f` with message `add internal api secret for test stands`, verified the resulting commit, and pushed only `DevOps-916-internal-api-secret`. Initial sandbox network attempts failed before reaching GitLab; after escalated push, a read-only MR inspection found no existing MR, then authorized publication created ready [MR131](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/131), target `master`, assigned to a.solonenko, squash false, source deletion on merge true. Creation verification passed with the expected SHA/title/body/source/target; pipelines empty and pipeline verification available.

This supersedes the pending-publication status above. Publication request complete; central TODO publication item closed. All16unrelated MSSQL modified/untracked paths preserved and index empty. No merge, deployment or runtime validation performed. Task commands finished; no background operations remain.

### User-confirmed final closure

2026-11-10: User reports MR131 merged and DevOps-916 closed, including the InternalApi follow-up. Accepted on the user report; no additional remote verification, tracker write, deployment or runtime check performed. Central publication TODO already completed; no remaining task actions or background operations.
