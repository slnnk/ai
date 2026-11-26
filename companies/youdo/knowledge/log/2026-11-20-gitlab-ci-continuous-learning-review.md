---
system: gitlab-ci
status: verified
checked: 2026-11-20
tags: [agents, learning, gitlab, youtrack]
---
# Continuous agent learning review, November 11–20

## Task

Review the [November 11 learning decision](2026-11-11-gitlab-ci-continuous-learning-supervised.md) through November 20 against the [previous correction audit](2026-11-11-gitlab-ci-correction-application-audit.md). Compare first approaches and delivered artifacts, substantive user interventions, evidence of rule use, and Git and YouTrack approvals. The user authorized the review and its bookkeeping on November 20. The review criterion is traceability from counts and conclusions to receipts, task logs, and locally available commit diffs.

## Findings

### Daily evidence

All seven snapshot SHA-256 values matched their saved review receipts. Calendar intervals use Moscow time and stop before November 20. The first slice spans November 7–13 and contains no registered tasks. Its recorded rule events fall within the November 11–19 date window. Task coverage begins November 14.

| Calendar interval | Changed records | First pass / fail / unknown | Final pass / partial / unknown | Rule pass / fail |
| --- | ---: | --- | --- | --- |
| Nov 7–13 | 0 | 0 / 0 / 0 | 0 / 0 / 0 | 30 / 9 |
| Nov 14 | 13 | 4 / 0 / 9 | 11 / 1 / 1 | 18 / 1 |
| Nov 15 | 4 | 2 / 1 / 1 | 4 / 0 / 0 | 4 / 0 |
| Nov 16 | 1 | 1 / 0 / 0 | 1 / 0 / 0 | 0 / 0 |
| Nov 17 | 6 | 3 / 0 / 3 | 6 / 0 / 0 | 3 / 0 |
| Nov 18 | 8 | 2 / 3 / 3 | 7 / 1 / 0 | 10 / 0 |
| Nov 19 | 10 | 3 / 0 / 7 | 10 / 0 / 0 | 12 / 0 |

Sources: [Nov 14](2026-11-14-agents-daily-metrics-review.md), [Nov 15](../../../../personal/knowledge/log/2026-11-15-agents-daily-metrics-review.md), [Nov 16](../../../../personal/knowledge/log/2026-11-16-agents-daily-metrics-20261116.md), [Nov 17](2026-11-17-agents-daily-metrics-review.md), [Nov 18](2026-11-18-agents-daily-metrics-review.md), [Nov 19](2026-11-19-agents-daily-metrics-review.md), [Nov 20](../../../../personal/knowledge/log/2026-11-20-agents-daily-metrics-review.md).

Deduplicate by task ID, keeping the latest snapshot version. The 42 changed rows represent 41 IDs, including 16 company records. One KYC issue alone contributes separate planning and MR records. The recorded first results are 15 pass, 4 fail and 22 unknown. Final results are 39 pass, 1 partial and 1 unknown, with 40 closed and 1 open. In the company subset all 16 closed, with 8 pass, 2 fail and 6 unknown at first delivery and 15 pass plus 1 partial at final delivery. The KYC child records and other related deliverables limit comparisons across independent tasks.

The [November 19 source recheck](2026-11-19-agents-daily-metrics-review.md#findings) found that the P2.2 retention failure was supported only by an internal Python retry. Treat it as unknown for first delivery in this analysis, yielding 15 pass, 3 fail and 23 unknown overall and 8 pass, 1 fail and 7 unknown in company records. Preserve recorded snapshot labels. Correction counts exist for 6/41 IDs and critical-event counts for 3/41. Unnecessary-action counts, attributable tokens and active time are unassessed for all 41. Rolling seven-day session usage cannot establish per-task cost or a time trend.

The daily snapshots contain 87 rule events, 77 pass and 10 fail. Count 3 failures in historical rule revisions and 84 current-revision events (77 pass, 7 fail). All 10 recorded failures say the rule was loaded, while one pass has unknown read status. The best available evidence on retrieval is the logged read indicator or documented read, with unreported stages left unknown. Several rules or lifecycle steps can produce events on one issue. The live learning report also applies its own historical-event exclusions, so its denominator differs. These counts cannot establish a learning rate, fresh-session transfer or causal benefit from daily review.

### Repository scope, naming and approvals

| Issue | Original proposal, actual diff and naming | Approval and verification evidence |
| --- | --- | --- |
| DevOps-921 | From develop, branch `DevOps-921-fail-apk-upload-on-http-errors`, commit `fail apk uploads on http errors`, Ready title `DevOps-921 fail apk uploads on http errors`. Commit `536493b` changes only the two curl uploads, as proposed. | Both approvals. Exact staged patch and MR !2926 text/refs verified. BrowserStack, YouTrack and notification effects were disclosed. Head pipeline later canceled. [Work log](2026-11-12-android-farm-devops-921-apk-http-errors.md) |
| DevOps-922 | From master, branch `DevOps-922-wait-for-source-job`, commit `wait for source job before retry suite download`, Ready title `DevOps-922 wait for source job before retry suite download`. Commit `6c18e1ad` limits the change to the retry block, including bounded wait and HTTP failure handling. | Both approvals. Exact staged patch and MR !1165 metadata verified. No XML parser introduced. The scope and names of DevOps-921 and 922 have existing first-attempt pass events. [Work log](2026-11-12-android-farm-devops-922-wait-source-job.md) |
| DevOps-923 | Dev Vault MR !4 retained the proposed source `DevOps-923-kyc-dev-vault-path` and master target, the approved commit/title and the matching two-file Vault path/README patch. Production was a separate decision: the user corrected the proposed manual mode to existing B2B AUTO and asked to follow nearby HCL. A later monitoring-only commit `d4908d2` removed one include after the new failure. | Both approvals and approved patch/metadata readback documented for dev Vault and monitoring changes. The monitoring MR disclosed the automatic deployment effect of merging. Distinguish changed requirements and separate approved scopes from matching the first production proposal. [Work log](2026-11-17-dev-deployment-devops-923-kyc-plan.md) |
| DevOps-926 | From master, branch `DevOps-926-update-aasa`, commit `update AASA paths`, Ready title `DevOps-926 update AASA paths`. Commit `3ffdc358` adds one final AASA entry and its delimiter. | Both approvals. Exact staged diff, branch/SHA and MR !1400 metadata verified. Empty pipeline list matched expected rules. [Work log](2026-11-18-automation-services-devops-926-nginx-aasa.md) |
| DevOps-927 | From master, branch `DevOps-927-build-libheif-1-19-8`, commit `build libheif 1.19.8 from source`, Ready title `DevOps-927 Build libheif 1.19.8 from source`. Commit `298e97b` touches only the libvips Dockerfile. Build inputs and runtime HEIF checks are tied to the version upgrade. | Both approvals, local image and conversion checks, staged diff and exact MR !44 metadata. Tag-driven CI effect assessed separately from MR publication and later production acceptance. [Work log](2026-11-19-base-images-devops-927-libheif-1-19-8.md) |

Local commit objects corroborate the indicated scopes and commit subjects, including the DevOps-918 recovery below. MR text, source/target, effects and approval chronology are supported by saved proposals and previous readbacks in the work logs. The reviewed later narrow patches transfer the earlier scope/naming workflow to distinct issues. This demonstrates concrete application in those cases. It leaves the full publication population, fresh-session instruction loading in every case and comparative improvement unmeasured.

### DevOps-918 and repeated mistakes

- **Tool availability.** The first Helm deployment template inspected custom Dockerfile additions but missed the parent image's installed tools. It introduced an API archive downloader, URL encoding and an external yq download/checksum/PATH setup. The user requested a direct clone. The actual kubectl image already supplied git and yq. Commit `723ea3b` replaced the acquisition logic with a shallow clone using the existing image and retained deployment behavior. Consumer CI Lint passed. The [existing simplicity failure](../../../../personal/knowledge/log/2026-11-12-agents-agent-learning-record-simplest-sufficient-solution-4cedeecedfca84d648d0.md) remains fail with loaded=yes. This was a known rule misapplied at approach selection, with observable missed base-image inspection. [Initial and corrected diff](2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md#before_script-simplified-to-git-clone-script-simplification-discussed)
- **Deployment assumptions.** User steering removed the custom Keystone helper and redundant CI inputs by reusing the group kubeconfig and chart defaults. PostgreSQL pre-install genuinely depended on an early Vault-sourced Secret under the original credential design. After the user chose standard dev PostgreSQL credentials, that dependency disappeared and the template dropped VSO precreation and waits. The later dev job and basic readiness passed, while full OIDC and worker acceptance were separate. These are same-task recoveries. DevOps-927 is a distinct example of justified build complexity, with a specific dependency version and measured runtime checks. Independent transfer of the exact parent-image/tool-inventory lesson remains unverified. [Decision evidence](2026-11-14-agents-p01-company-decision-evidence.md) · [Deployment outcome](2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md#november13-first-deployment-succeeded-and-basic-live-readiness-verified)
- **Scope and completeness.** The previous audit documented scope expansion. In this period the [Codex config review](../../../../personal/knowledge/log/2026-11-18-codex-config-performance-review.md) initially covered performance but omitted instruction loading, and the [helper audit](2026-11-18-agents-p16-helper-reuse.md#full-directory-audit-after-user-correction) initially sampled groups instead of completing the recursive audit. Both recovered after intervention. These are omissions of requested coverage, with a different direction of error from expansion. They support verifying the requested coverage explicitly. Available evidence does not establish identical causes or rule-read status across cases.
- **Remaining session items.** Five recorded failures span old and current revisions, including premature lists after intermediate checks, and omitted lists after actual completion. The later examples report the rule loaded. Rechecking the agreed parent outcome is the applicable existing rule. Reading the rule, or repairing the list in the same session, gives no independent transfer evidence. [Rule history](../../../../personal/knowledge/log/2026-10-19-agents-agent-learning-record-show-remaining-proposed-tasks-034300735f905cd3c220.md)

### YouTrack comment labels

| Issue | Draft, intervention and final outcome | Evidence-based classification |
| --- | --- | --- |
| DevOps-921 | User removed local checks and moved the MR URL from prose into the issue field. Exact revised comment and field both approved and read back. | New task-specific presentation requirement. Retain historical first-draft fail as evidence of steering. No prior identical format violation established. [Work log](2026-11-12-android-farm-devops-921-apk-http-errors.md#comment-format-correction-and-mr-field--2026-11-12) |
| DevOps-922 | Draft omitted the problem statement, which the user then requested. Approved revised comment was read back. The user had to correct omission of the already discussed dedicated MR attachment; the field was then separately written and verified. | Newly specified content in the first revision and a separate demonstrated miss of known same-discussion scope on delivery. Preserve the latter without turning the DevOps-921 format into a company default or adding a second first-draft failure. [Work log](2026-11-12-android-farm-devops-922-wait-source-job.md#comment-revision-problem-description-requested--2026-11-12) |
| DevOps-923 | User removed the deployment checks and closing caveat from the first draft. Exact three-bullet revision and MR URLs were read back after explicit approval. | One issue workflow. Two recorded passes cover drafting and publication stages. The first draft still received task-specific editing. Publication process verified, zero steering unsupported. [Work log](2026-11-17-dev-deployment-devops-923-kyc-plan.md#youtrack-comment-user-revision-2026-11-17) |
| DevOps-927 | User replaced a longer first draft with shorter first-person wording and explicitly requested posting it. Exact text and linked MR verified by GET. | Later-task evidence of approved publication and readback, with a new editorial preference. The pass event supports the publication procedure. It does not establish unassisted first-draft acceptance. [Work log](2026-11-19-base-images-devops-927-libheif-1-19-8.md#youtrack-comment-draft) |

## Actions

Keep the two repository approvals and exact-comment confirmation active. The observed results under supervision do not support reducing supervision. Use the existing scoped learning and metrics workflow. For future scoring, retain first delivered result and final outcome, count one applicable evaluation per rule and parent task, and distinguish new presentation choices, repeated known-rule misses and pre-delivery retries. Use actual inherited tooling and comparable in-project patterns before proposing acquisition or new deployment mechanisms. Existing P0.1/P1 evidence and the scoped decision examples cover these practices. The [P1.5 experiment decision](../../../../personal/knowledge/log/2026-11-18-agents-p15-adoption-decision.md) remains in effect. No new rule, duplicate evaluation, experiment or backlog item was needed.

## Changes and status

Saved this report, linked it from the November 11 decision and existing Git workflow map, and closed the dated item in central TODO. Completed the bounded review using existing local evidence. No live GitLab/YouTrack audit, project publication or deployment was performed. No task commands or agents remain in the background.

## Five-task follow-up November 25

The user approved collecting evidence from the next five distinct qualifying tasks
in normal work. The [company context](../../CONTEXT.md#five-task-first-delivery-check)
defines eligibility and capture. For each case, add the task ID and a link to its
first-delivery evidence. After five cases, report evidence coverage, first-delivery
outcomes and substantive corrections, and identify any repeated issue supported by
the artifacts. This small sample tests whether the evidence can be collected in
ordinary work. After the fifth case, close the corresponding TODO item and mark
the temporary collection instruction in company context complete.

Cases collected at setup: 0 of 5. Existing approval rules apply.

- `nexus-cleaner-20261125-shared-digest-diff` — [first diff and checks](2026-11-25-nexus-data-disk-capacity.md#first-delivery-of-the-cleaner-diff).

## Portable lesson

[Correction learning](../../../../general/knowledge/agents/correction-learning.md).

## Task metrics: continuous-learning-review-2026-11-20

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "continuous-learning-review-2026-11-20",
  "created": "2026-11-20T16:47:59.426558+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "analysis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Reconciled seven snapshot receipts and 41 unique IDs, compared project diffs and approval/comment sources, preserved first-attempt failures and closed the dated TODO.",
  "updated": "2026-11-20T16:47:59.426605+03:00"
}
```
