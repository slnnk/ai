---
system: gitlab-ci
status: verified
checked: 2026-10-19
tags: [agents, gitlab, training, review]
---
# GitLab supervised agent training early review

## Summary
The user requested the training review on October 19 instead of waiting until October 30.
Review period: October 8–19, 2026, through the records available at preparation time.
The workflow has produced reviewed publications and reusable naming rules, but scope expansion and a release-source error still required user intervention.
Recommendation: automate deterministic inspection and proposal preparation; retain both supervised approvals for now. This recommendation is not a permission change.
Five publication sequences with complete original-name, approval and outcome records show unchanged branch, commit and MR-title proposals. This selected sample does not establish an experiment-wide acceptance rate.
The report is complete. On October 19 the user chose to retain both approvals while automating information gathering and review-material preparation. A follow-up review was proposed for October 30 or the first active session after it; no background job was scheduled.

## Task and context
Prepare the scheduled Git/MR training report early at the user's explicit request.
The [canonical workflow](../systems/gitlab-ci/agent-git-workflow.md) requires branch approval before repository edits and a second approval covering reviewed staging, commit, push and MR publication.
The [baseline review](2026-10-08-gitlab-ci-agent-git-workflow-review.md) predates this experiment's outcomes and is not counted as a training success.
No project repository, release, remote service or GitLab object was changed for this review.

## Evidence and counting method
Sources are dated work logs and the canonical workflow, reviewed with a delegated read-only evidence check. GitLab outcomes below are historical observations from those logs, not fresh remote verification.
A scan found 19 notes dated October 8–19 with an explicit training heading. This is a note count: notes may cover multiple repositories or duplicate a continuing branch; other publications have no dedicated training heading.
The total number of eligible task/repository/publication sequences is therefore not established. Missing approval text in a note is not proof that approval was absent.

The bounded metric cohort comprises five publication sequences with recorded original proposals, explicit approvals and final outcomes: ASP.NET archive MR36, Nomad HashiCorp MR6, base-images HashiCorp MR39, keep-db routing MR91 and SMTP MR1379.

| Measure | Recorded result in the selected cohort |
| --- | --- |
| Original branch proposal accepted unchanged | 5 of 5 |
| Original commit subject accepted unchanged | 5 of 5 |
| Original MR title accepted unchanged | 5 of 5 |
| Published with recorded remote SHA and MR verification | 5 of 5 |

The cohort is selected for evidence completeness, not randomly sampled. These figures cannot be extrapolated to all training work. Description changes, implementation corrections, release outcomes and later deployments are separate measures. Overall first-proposal acceptance rates remain unknown.

## Representative cases
| Case | Approval and correction evidence | Recorded outcome |
| --- | --- | --- |
| [DevOps-882 infrastructure](2026-10-08-gitlab-ci-devops-882-chat-agent-infrastructure.md), automation-services and selectel-tf | Both gates approved. Corrections covered separate worktrees, task-only commits, obsolete Molecule checks and Russian MR descriptions. | Commits a87b482 / MR1364 and 34061c2 / MR92; unrelated changes preserved. |
| [DevOps-882 service](2026-10-09-youdo-chat-agent-prod-deploy.md) | Branch proposal DevOps-882-chat-agent rejected; after further correction final branch DevOps-882-prod-deploy approved. Both gates approved; inclusion of two user edits explicitly authorized. | Commit 13fd1ff / MR9. Publication did not itself perform merge or deployment. |
| [DevOps-888 Kubernetes recovery](2026-10-09-yandex-cloud-devops-888-dev-k8s-e-recovery.md) | Branch wording recover-k8s corrected to recovery-k8s; Draft proposal overridden. User required reusing test-k8s and Kubernetes 1.35. | Commit 3f8415a / MR232; recorded MR pipeline 140484 succeeded. |
| [DevOps-889 MSSQL recovery](2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md) | Branch approved; expanded implementation rejected and reduced to minimal adaptation of the existing workflow. Revised publication proposal remained unapproved in the reviewed record. | Local changes only; no publication inferred. |
| [DevOps-891 Molecule build](2026-10-12-gitlab-ansible-molecule-toolset-recovery.md) | Both gates approved. User required retaining master packages and fixing the build instead of changing packages. | Commit 81f3a8e / MR1; local build passed. No SHA pipeline expected under the recorded filters. |
| [DevOps-891 ASP.NET archive](2026-10-12-gitlab-devops-891-aspnet-archive.md) | Original names accepted; both approvals recorded. Metric cohort member. | Commit 62226b8 / MR36; tag-only CI meant branch publication did not release images. |
| [DevOps-891 official HashiCorp releases](2026-10-12-gitlab-devops-891-official-hashicorp-releases.md), two repositories | Original names accepted in both repositories; branch approval and conditional publication approval recorded, checks satisfied. Two metric cohort members. | Nomad 1067d30 / MR6; base-images d90806f / MR39. Later merges/releases separately documented. |
| [DevOps-898 keep-db routing](2026-10-15-gitlab-ci-devops-898-keep-db-vk-routing.md) | Both approvals and unchanged names recorded. Rollout-job selection corrected separately. Metric cohort member. | Commit 126620d / MR91. MR creation succeeded, then optional pipeline GET returned 403; recovered without duplicate creation. |
| [DevOps-897 endpoint correction](2026-10-15-jenkins-build5832-mssql-old-endpoint.md) | Both gates explicit. Only three endpoint changes published; unrelated seven-stage changes preserved. Merge separately requested. | Commit cdb11b5 / MR113; guarded merge verified. Later runtime acceptance was user-reported. |
| [DevOps-898 SMTP](2026-10-16-nomad-test-mailer-smtp-diagnosis.md) | Both approvals recorded; original names accepted. Metric cohort member. | Commit ff104e3 / MR1379; one-line change, pipeline 141074 skipped; no Ansible apply or merge from publication. |
| [DevOps-900 nodes API](2026-10-16-youdo-business-devops-900-nodes-api-host.md) | Branch approved. Later explicit publication and immediate-merge request covered the established automatic production release effect. | Commit 4eb0605 / MR112; squash setting preserved. Merge 422/checking handled through GET before retry. Runtime completion not claimed. |

## Errors and correction patterns
1. **Release-source error.** [Base-images kubectl release](2026-10-14-dev-deployment-devops-898-buildapi-vk-kubeconfig.md), sections CI image preparation and Release-source correction: kubectl/1.35.6 initially targeted unmerged feature SHA 18c0ed83. The original release had separate user approval, so this establishes a source-selection error, not an unapproved-write finding. The user then explicitly requested merging MR41 and recreating the tag on master. Corrected pipeline 140923 and image verification succeeded. Canonical rules now require master-based release tags after merge.
2. **Repeated scope expansion.** DevOps-889 expanded the MSSQL adaptation; Molecule work proposed package changes instead of a build fix; DevOps-898 manual-release work proposed unnecessary CI overrides. These distinct cases support retaining a scope checkpoint and reusing established mechanisms. They do not establish that the same loaded rule was repeatedly ignored: rule-read evidence for every event is unavailable.
3. **Naming and description corrections.** Branch suffix must describe the change, not merely the repository. MR description must be one short Russian paragraph followed by the task link. Readiness/Draft choice must follow the agreed task state. The DevOps-888 branch wording correction is task-specific; it does not create a global vocabulary rule.
4. **Repeated partial-success handling defect.** [Internal kubectl MR90](2026-10-15-gitlab-ci-monitoring-internal-kubectl.md) and keep-db MR91 were created successfully before an optional pipeline-list GET403 caused a nonzero helper exit. Read-only recovery avoided duplicate writes. A command exit code alone did not describe the publication outcome.
5. **CI and deployment policy.** Ordinary jobs versus keep-db, Kitcut recreate_db and Cerberus DB recreation required separate corrections. These affect change scope and CI consequences; they are not branch-name rejection counts or evidence of unauthorized publication.
6. **Record quality.** Earlier pending paragraphs sometimes remain above later completion sections. Final state must use the superseding section. Exact initial proposals, approval evidence and final outcomes are not consistently available for all cases.

## Permission and validation assessment
The selected publication cases document both approvals, task-scoped staging and subsequent verification. The broader reviewed records do not establish an unauthorized-publication incident. This is not a complete command-by-command permission audit or proof of zero violations.
Successful MR creation does not prove successful CI, release or runtime deployment. Skipped or absent pipelines can be expected under project rules; the report preserves those distinctions. Separate user instructions authorized the merges/releases described above; training approvals alone do not authorize them.

## Recommendation and proposed workflow changes
Retain the two approval gates until the user explicitly changes them. Full unattended publication and release are not supported by the available evidence.
A unified Git/GitLab skill can centralize local-first inspection, revision selection, naming, minimal change scope, approval preparation and publication verification. Existing gitlab_task_mr.py already guards expected remote SHA and MR source/target; build on that helper rather than starting a duplicate publication tool.
Proposed improvements, not implemented by this report:
- Automate compact local repository inspection and generation of the reviewable proposal.
- Capture original and final branch, commit and MR names plus approval evidence and CI effects for every publication sequence, including uncorrected proposals.
- Separate successful commit/push/MR writes from optional verification failures; inspect remote state before retrying any uncertain write.
- Before a base-images release, verify that the exact reviewed tag target belongs to master after the MR merge; retain separate release authorization.
- Keep publication approval separate from merge, tags, deployment and destructive operations.

The local-first clone policy and unified skill discussed in this conversation remain proposals. This report creates neither the skill nor new clone/publication permissions.

## Actions and changes
Ran the daily ai-sync.sh; it completed without output or reminders. Queried scoped agent-learning rules, read the canonical workflow and selectively reviewed dated evidence through a delegated agent. No full transcript mining or GitLab writes were performed.
Created this report with new_note.py. Updated the existing workflow review status and the single backlog to record early delivery and retain the user decision as pending. No state-changing Git commands were run for this review apart from the required daily sync.
Verification: kb_lint.py reported zero errors and six existing warnings in other files; build_index.py rebuilt the company index. Scoped git diff --check passed. The repository-wide diff check found an existing extra blank line in systems/tracing.md, which this review did not change.

## Risks and limits
The full eligible denominator and experiment-wide acceptance rates remain unknown. Historical pipeline states are not current runtime assertions. The user subsequently chose to retain the supervised mode on October 19; any future permission change still requires an explicit decision. Evidence supports deterministic preparation, but release-source and scope mistakes still warrant explicit review.

## Portable lesson
None created; reusable changes remain proposals for the unified workflow.

## User decision after review (2026-10-19)
The user accepted retaining both approvals while automating information gathering and preparation of review materials. This supersedes the pending-decision statements in the original report. No unattended publication, merge, release or deployment was authorized. The assistant proposed the next review for October 30 or the first active session after it; the open action is maintained in the central TODO.
