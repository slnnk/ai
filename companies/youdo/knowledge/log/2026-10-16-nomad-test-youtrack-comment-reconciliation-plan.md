---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [youtrack, recovery, scope]
---

# Recovery task comment reconciliation plan

## Summary

Planning only: no YouTrack comments or issue states changed. Live GET inspection of the 50 most recently updated resolved DevOps issues confirmed the task boundaries: DevOps-899 owns per-stand microservices; DevOps-898 owns shared single/dynamic services. Later B2B delivery was recorded locally under DevOps-898, but belongs in the DevOps-899 delivery summary. Historical branch, MR, pipeline and artifact names remain valid evidence and must not be renamed.

## Task and context

The user requested a plan to reconcile closed task comments with completed local agent work, with a brief plan shown in chat. The user identified confusion between microservice deployment to stands and dynamic service deployment. This authorizes investigation and local planning, not external changes.

## Evidence and actions

- Ran ai-sync.sh; it exited successfully without output or reminders.
- Reused the GET client and environment loader in current/skills/rp/scripts/youtrack_sprint.py. No secrets were copied.
- Retrieved resolved DevOps issues with query `project: DevOps #Resolved sort by: updated desc`, top 50. Saved the read-only baseline at `/home/slnnk/ai-data/youtrack-comment-reconciliation/closed-issues-before.json`.
- Compared live comment text with the existing system map and dated rollout logs. These are historical delivery records, not fresh infrastructure checks.
- DevOps-899 comment `74-124678` describes initial test5 work and Jenkins test4 acceptance, and still excludes B2B/Cerberus. This is stale relative to completed October 15–16 rollouts.
- The original DevOps-898 comment `74-124675` described the earlier test5-only LogReader pilot. The subsequent user-approved rollout now establishes all14active stands and supersedes that limitation; ten single services, BuildAPI recovery and the Socket per-stand distinction remain valid. The B2B misclassification is in local records rather than the current published comment.
- DevOps-897 comment `74-124677` already includes MR113 and user-reported successful playbook execution; do not duplicate that update.

## Proposed comment changes (complete recheck)

The authoritative detailed inventory is the [closed recovery completeness audit](2026-10-16-nomad-test-recovery-comment-completeness-recheck.md). Fresh comparison covered all11closed recovery comments; update7rather than only the4initial headlines.

| Task | Proposed replacement scope |
| --- | --- |
| DevOps-899 | C2C/B2B per-stand service coverage and final Cerberus; FeatureToggle seed/49keys/13DBclones/template refresh; scoped authentication compatibility; C2C/B2B PostgreSQL/PgBouncer capacity/pools, TKBauth and Tochkaroutes; merged shared CI89/keep-db91; Landings/Business build/runtime/DBtask repairs. Preserve per-service stand limits. |
| DevOps-898 | Keep10single services and BuildAPI; replace test5-only LogReader text with verified14active rollout141021/3230221,13Consul endpoints and persistent project14stand variable. Reused shared doc-generator remains here; B2B per-stand work is899. |
| DevOps-894 | Add successful full parallel ES lifecycle on14stands,14of14exit0/no retry, deadlines2m/3m,3thick40GiB+11thin5GiB. No implied all-fleetHTTP/index check. |
| DevOps-892 | Add JenkinsSSH/plugin/static rebuild prerequisites and refine existing BuildAPIfailure-handling details. Record5828/5829/5830failures,5831success followed by test8retirement. Link5832/MSSQLfix to897; no false full-stand successes. |
| DevOps-891 | Add omitted .NET2.1SDK/ASP.NET mirrorsMR42and verified publication; SDKpipeline canceled/runtime successful. Update devdocker140984to failed, preserving already-described successful standalone PostgreSQL10publication and Broadcast tests. |
| DevOps-896 | Replace stale test_inventory.sh pending cutover with evidenced actual JenkinsVKconsumer; retain unrelated limits and closed acceptance. |
| DevOps-889 | Brief dated history of READYimagecopy, checked local minimal adaptation and HDD/quota analysis before Yandex route cancellation; link VKrecovery897. No claim of completed Yandex deployment. |

DevOps-890/893/895/897 already contain their material completed recovery work; retain without duplicate additions. JenkinsBuildAPIpublication details belong primarily892, linked from899rather than counted twice. Historical names remain unchanged.

Prepare exact existing-comment replacements and evidence links for review; no external update is authorized by this plan. Re-read each comment before its approved write and stop if the baseline changed. Keep all issue states closed.

## Devdocker base-image correction (user follow-up)

Devdocker image recovery belongs in **DevOps-891**, even though the historical implementation branch and MR refer to DevOps-899. Explicitly include this task in the comment-update plan. DevOps-899 retains the dependent Broadcast rollout and links to the image recovery, without counting the base-image work twice.

- Confirmed completed: devdocker [MR55](https://gitlab.youdo.sg/youdo/devdocker/-/merge_requests/55) merged, replacing external CI Docker client/DinD with internal base-images and an explicit docker alias. Runtime Dockerfiles unchanged.
- Confirmed completed separately: local build and publication of `registry.youdo.sg/youdo/devdocker/postgres:latest`, PostgreSQL 10.21 with `ru_RU.utf8`, digest `sha256:8b9bcb6701e75ce1b0d8d9b935d7c90e0d44df59b3abf7cdddd74c9cd5dc90f1`; Broadcast integration tests passed 8/8 and its dependent deployment succeeded.
- Fresh read-only GitLab GET on 2026-10-16: [pipeline140984](https://gitlab.youdo.sg/youdo/devdocker/-/pipelines/140984), merge SHA `1f0c0d5eda479a0e05d9d3fc9653d81dff252c33`, is **failed**. Job `test`3228588 succeeded, `master_build`3228589 failed. Do not claim successful full six-image recovery from this pipeline. The existing DevOps-891 comment says completion was not yet confirmed; replace that uncertainty with the observed failed result, retaining the independent PostgreSQL publication success.
- No retries, releases or infrastructure changes are included in this comment-only plan. The failed build cause and availability of the other five images were not investigated in this follow-up.

## Exact recorded delivery coverage for the DevOps-899 draft

| Group | Recorded completed scope |
| --- | --- |
| C2C eight stands: test, test1–test7 | Broadcast 1.2.11; FeatureToggle 1.0.11; Landings 1.3.35; Socket 1.2.9; Help 1.0.14; Content 2.5.13; SMS master-191; Moderation 1.0.45 S3 assets |
| Antifraud | 23.8.8 on test2/test3/test4/test5/test7 only |
| TrackingPixel | 1.0.5 on test5 only |
| Cerberus | 1.0.9 on all 14 active C2C/B2B stands |
| B2B six stands: test10–test15 | business master-21509; auth master-168; billing master-707; landings master-109; mobile-id master-58; TKB master-267; Tochka master-1767; Kitcut master-103; notifications master-190; SMS master-191; docvalidation master-757; Fns master-598 |
| Shared B2B dependency, retained under DevOps-898 | Existing doc-generator master-137 reused |

The C2C/B2B common SMS/Fns/DocValidation recorded rollout coverage is all 14 active stands; cite the relevant service rollout records in the eventual replacement. Initial eight-service pilot acceptance remains history rather than evidence of universal final coverage.

## Acceptance limits

- Distinguish completed deployments, prepared BuildAPI catalogs/manual-job links, and supporting image/package recovery. The 104 prepared links are not evidence of 104 completed deployments.
- Stand coverage is service-specific; never turn an eight-stand C2C result into a fourteen-stand result without evidence.
- B2B delivery was accepted through GitLab/Nomad status checks per user instructions; this does not establish full business-functional acceptance.
- LogReader is now accepted on all14active stands after the approved October16rollout. test8/test9 are excluded. The original test5pilot evidence alone remains insufficient for this final claim; cite pipeline141021/deploy3230221 and the final runtime artifact. Availability/SQLSELECT1 acceptance does not claim a synthetic exception-write/read test.
- Cerberus uses the established GitLab deploy path with ordinary database recreation. Do not describe the earlier database-preservation experiment as the final delivery. Final workers were 42; test11 had one recovered restart, so do not claim zero restarts everywhere.
- Fresh GET now confirms Jenkins5828–5830FAILURE,5831SUCCESSfollowed by test8retirement,5832FAILURE. Do not promote the failed runs to completed full-stand acceptance. Backup restoration/AutoTest acceptance remain unverified.
- Preserve the known Socket version-cell mapping and Landings UI/health-check limitations unless later evidence explicitly resolves them.

## Sources

- [Nomad test system map](../systems/nomad-test.md).
- [B2B plan and final delivery](2026-10-15-nomad-test-b2b-test10-15-deployment-plan.md), section `Final delivery 2026-10-16`.
- [Business rollout](2026-10-16-nomad-test-devops-898-business-rollout.md).
- [Cerberus standard GitLab rollout](2026-10-16-nomad-test-cerberus-standard-gitlab-rollout.md).
- [Previous published comment updates](2026-10-15-recovery-task-comment-updates.md).

## Changed files and risks

Created this local plan, a read-only issue snapshot, a plan reference in the existing nomad-test map, central backlog tracking and standard index/sync bookkeeping. No repository task files or external state changed. The snapshot may become stale before publication; concurrent-edit verification is required. Exact comment replacement text remains a later review artifact; the user requested a plan at this stage.

## LogReader prerequisite completed (2026-10-16)

The user requested completing LogReader before comment changes. This is now verified on all14active stands via standard GitLab deploy3230221. Updated the DevOps-898 proposed replacement scope accordingly. No YouTrack comment has been changed. [Approval history and final evidence](2026-10-16-nomad-test-logreader-all-active-stands.md).

## Completeness recheck2026-10-16

Expanded after the user identified missing work. Seven comments now have explicit correction scopes; four more already contain their completed results. Supporting database/data/CI/image work is included, not only rollout headlines. [Full evidence inventory](2026-10-16-nomad-test-recovery-comment-completeness-recheck.md). No YouTrack writes.

## Publication completed (2026-10-16)

After the explicit user correction to update existing comments rather than create new ones, all7existing target comments were updated and readback-verified, with original IDs and closed states preserved. No new comments. Earlier planning-only/pending statements in this note describe the prior stage. [Final publication record](2026-10-16-nomad-test-recovery-existing-comments-updated.md).
