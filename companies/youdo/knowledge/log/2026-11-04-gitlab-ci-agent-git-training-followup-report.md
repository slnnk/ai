---
system: gitlab-ci
status: verified
checked: 2026-11-04
tags: [agents, gitlab, training, review]
---
# GitLab supervised training follow-up review

## Summary
Prepared on 2026-11-04 at the user's request. The review window is 2026-10-20 through 2026-11-04, following the October 19 early report. Available company operational evidence is concentrated on October 20–22. Retain both approval gates: publication mechanics are documented more consistently, but repeated scope corrections still require user intervention. No permission change follows from this recommendation.

## Task and method
Review scope control, task-only staging, approvals, CI effects, publication verification and corrections since the [early report](2026-10-19-gitlab-ci-agent-git-training-early-report.md). Read the canonical workflow, relevant learning records and bounded company work logs, with delegated read-only evidence review. Historical outcomes below are observations recorded in those logs, not fresh GitLab/runtime verification. No full transcript audit, project checkout changes, GitLab API writes or CI runs were performed.

A filename scan identified 32 company log notes dated October 20–November 4, including four correction-evidence records. Notes and corrections are not independent task successes. Older-dated notes updated during the window and personal repositories were not exhaustively audited. The total eligible denominator for all work during the period remains unknown.

## Bounded publication cohort
The reviewed sources identify 11 distinct MRs in 9 repositories and 14 commit/push sequences: subcategory predictor MR22 contains its initial publication plus three follow-up commits; each other MR contributes one sequence. Both approval stages are explicitly recoverable in records for 10 MRs / 13 sequences. Kafka has a scoped push request, concrete proposal, staged-diff and remote verification evidence, but insufficient separately recorded first-gate/initial-name detail for the same audit standard. Missing log detail does not establish an unauthorized action.

| Source | Published artifact | Recorded controls and outcome |
| --- | --- | --- |
| [nginx cleanup](2026-10-20-jenkins-devops-903-empty-nginx-cache-cleanup.md), [monolith cache](2026-10-20-nexus-ce-request-limit-analysis.md), [Business consumers](2026-10-20-nexus-gitlab-consumers-oct19-20.md) | automation-test-yandex MR122; monolith MR10113; Business MR3863 | Approval and publication evidence; cache/registry CI effects considered. The consumer note's October 19–20 analysis window is not itself a publication date. |
| [Daily compilations](2026-10-21-nomad-test-daily-compilations-missing.md) | MR9, ef37ce8 | Both gates, full staged diff and exact MR readback; final patch only two CI substitutions. Local checks explicitly waived. Publication did not establish VK endpoint/token readiness. |
| [Subcategory predictor](2026-10-21-nomad-test-subcategory-predictor-vk.md) | MR22, four publication sequences | Follow-up user requirement introduced local-build-before-publication. Later build/import and source checks documented. Do not apply the later rule retroactively to earlier publications. |
| [Recommendations mock](2026-10-21-nomad-test-recommendations-mock-vk.md) | MR13 and MR14 | Local build and reviewed publication; local success distinguished from registry/CI compatibility and later release observations. |
| [Kafka](2026-10-21-nomad-test-kafka-vk-full-job.md) | MR3, f175adc5 | Scoped waiver of local runtime checks; staged patch and remote MR verified. Merge/deployment separately proposed and approved. Fine-grained first-gate/name record incomplete. |
| [Task quality](2026-10-21-nomad-test-taskqualitycontrolfortest-vk.md) | MR10 and MR11 | Separate reviewed publications; later CI/rollout observations distinct from publication. |
| [Frontend tools](2026-10-22-nexus-devops-904-oct22-request-peak.md) | MR183, 8dccfc2 | Both gates, revised snapshot, full staged diff and exact remote verification. Automatic Storybook S3 writes explicitly covered. User merged; no agent merge inferred. |

These are evidence-completeness counts, not overall compliance percentages. The delegated source review found matching original/final branch, commit and MR-title proposals in the 13 evidence-complete sequences (13/13 for each field); this selected cohort excludes Kafka's incomplete record and cannot establish an experiment-wide rate. Overall first-proposal acceptance rates remain unknown; the earlier selected 5/5 cohort is a separate historical sample. Acceptance of publication names does not measure implementation correctness or first-gate scope/base revisions.

## Repeated corrections and demonstrated behavior
1. **Scope still needs intervention.** In daily compilations, defaults and a pinned application image were implemented within an approved preparation task, then removed after the user explained CI supplies these inputs. The final published diff was limited to two staging CI variables. The initial no-CI direction was subsequently explicitly superseded for those two variables: this is not evidence of violating the earlier direction.
2. **Unrelated follow-ups recur.** After frontend caching worked, a duplicate existing UI package publication failed on master. An optional publication guard was proposed, then withdrawn when the user clarified that only caching was requested. No guard/version/publication-policy change was implemented. This repeats the earlier tendency to expand the task through proposals; distinguish it from unauthorized executed changes.
3. **Validation must follow the task.** The user required local builds before later Data-service publication after subcategory problems; recommendations-mock records demonstrate subsequent application of that requirement. Kafka explicitly waived local runtime checks in favor of CI. Daily-compilations checks were also explicitly waived. Neither waiver is global permission to skip checks.
4. **Publication controls have concrete evidence.** Reviewed snapshots, full staged-diff inspection, source SHA checks and independent MR readback recur, including the revised frontend proposal after cache-concurrency changes. This is stronger than inferring success from a helper exit code.
   DevOps-903 also demonstrates a safe branch/base conflict response: branch switching stopped when unrelated MSSQL edits overlapped newer master, the revised base received explicit approval, sixteen unrelated paths were preserved, and only the one-line nginx change was committed.
5. **CI effects require more than a green job.** Frontend MR approval included automatic S3 writes. Initial cache-upload failure did not fail the job; later user retries and read-only verification demonstrated persisted cache reuse. The measured pipeline request reduction was 74.9%, including cold preparation, not an established daily reduction. The final master pipeline still failed on pre-existing duplicate package publication; caching success did not imply all CI succeeded.
6. **Deployment readiness remains separate.** Daily-compilations dc/proxy substitutions did not change inherited Nomad address/token. The publication proposal disclosed this gap; later deployment failed against inherited settings and was corrected with separate user direction. Avoid describing the source patch as complete deployment readiness.

## Learning and permission assessment
The learning helper reports 21 recorded/linked rules, 16 active, and zero formal applicable evaluations. These are registry-wide figures, not this period's Git-task count. They establish recording/linkage, not a measured behavioral pass rate. This report's specific task examples supply evidence of application, but were not silently added as synthetic helper evaluations.

The November 4 user correction exempts the entire ~/ai repository from the first repository-edit gate; the [global instruction](../../../../AGENTS.md) implements that exception. It does not remove either gate for product/infrastructure repositories or authorize manual publication of ~/ai. The evidence file is named November 3 because its timestamp is UTC; its source event is November 4 locally. This report makes no new policy edits.

No unauthorized Git publication was established by this bounded log review. This is not proof of zero permission violations or a command-by-command audit of all external writes. Names, approvals and final outcomes are incompletely recorded in some cases; unseen source messages and rule-load history remain unknown.

## Recommendation
Retain both approvals. Available evidence supports automating information collection and preparation of review materials, as already chosen October 19; it does not justify unattended publication, merge, release or deployment. Existing global minimal-scope and publication rules already address the observed errors; this report adds no new skill or implementation project.

Within future already-authorized tasks, apply the existing rules explicitly: state the minimal deliverable before edits; review inherited CI targets and automatic write effects before publication; preserve task-specific validation requirements/waivers; retain original/final proposals, approvals and final readback in the work log. These are review recommendations within current policy, not new external permissions or scheduled work.

## Actions, status and risks
Prepared the requested report, linked it from the existing workflow map and closed the report-preparation reminder in the central TODO. Delivery does not constitute a user decision to change permissions. Both approval gates remain active; no new review date or background schedule was created. No project Git mutations or external operations were initiated beyond the normal startup sync. Knowledge lint/index and task-local reconciliation results are recorded in the final task response.

## Portable lesson
None created; existing minimal-scope and publication controls cover these observations.

## User decision: next five published tasks
On 2026-11-04, after delivery of this report, the user approved observing the next five tasks with publication and preparing a comparison afterwards. Both approval gates are retained. This supersedes the earlier pending-user-decision wording only for the observation plan; no new permission, skill, calendar deadline or unattended operation was approved. Progress and counting criteria are maintained in the existing [workflow map](../systems/gitlab-ci/agent-git-workflow.md#five-task-follow-up-approved-on-november-4), with the single live action in central TODO. Initial progress is 0/5.
