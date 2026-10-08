---
system: gitlab-ci
status: verified
checked: 2026-10-08
tags: [gitlab, agents, workflow]
---
# GitLab: weekly naming review and proposed agent publication rules

## Summary
- Scope: user-authored GitLab work, October 5–8, 2026 (Moscow time).
- Ten new MRs across eight projects: nine merged, one demonstration open.
- Branches normally use task ID plus English kebab-case; iOS uses task ID alone.
- Commit subjects are short lowercase English phrases without task prefixes.
- MR titles normally prepend the task ID to the commit subject.
- Bodies contain only Closes references; all MRs are assigned to the user.
- Source branch removal is enabled; squash off except the iOS MR.
- Findings and source links are in Findings; approval boundaries in Proposed instructions.
- Proposal permits a delegated publication chain while retaining manual merge.
- Active instructions and external systems were not changed.

## Task
Review the user's work during 2026-10-05 through the collection time on 2026-10-08 (Europe/Moscow), infer branch/commit/MR conventions, and propose agent automation rules. This is a proposal, not authorization to publish or a change to active AGENTS.md.

## Context
GitLab account `a.solonenko` (184). Credentials were read from `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env`; no credential values were recorded. Relevant existing knowledge: [team configuration map](../systems/team-config-repo.md), [DevOps-879](2026-10-06-web-autotests-devops-879-webdriver-read-timeout.md), [DevOps-883](2026-10-07-dev-deployment-devops-883-developer-kubeconfig-sso.md), [DevOps-886](2026-10-07-dev-deployment-devops-886-ttl-controller.md).

## Actions
Ran daily ai-sync (no output/reminders), read company context and backlog, consulted repo catalog and kb_find. Delegated multi-file weekly note and local git history review. Queried GitLab through GET only: authenticated user, paginated authored MRs updated since 2026-10-04T21:00:00Z, user events, associated project metadata and all-ref commits. Matched authored commits separately from generated merge/squash history. Network sandbox initially blocked DNS; a read-only collector was then approved outside the sandbox.
Temporary collector and raw response: `~/ai-data/gitlab-review/collect.py`, `~/ai-data/gitlab-review/week.json` (outside git). Coverage is the authenticated account and accessible projects; does not establish completeness for inaccessible work or non-Git operations.

## Findings
10 authored MRs created this week across 8 projects: 9 merged, 1 open demonstration. An older MR !237 (created September 3) was updated October 5 and is excluded from the new-MR count; its merge date is outside this week. Ten branch creation push events each contained one original feature commit. Main-branch push events with generated merge commits reflect MR integration, not evidence of manual direct pushes.

| Task / repository | Branch | Original commit subject | MR |
| --- | --- | --- | --- |
| DevOps-879 / autotest-core | DevOps-879-http-timeout | set selenium http timeout | [!20](https://gitlab.youdo.sg/team-youdo-testers/autotest-core/-/merge_requests/20) |
| DevOps-881 / automation-services | DevOps-881-zabbix-macos | zabbix macos; clean macos gitlab runner | [!1363](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1363) |
| IOS-5054 / YouDoApp | IOS-5054 | fastlane apple api key | [!3273](https://gitlab.youdo.sg/team-youdo-ios/YouDoApp/-/merge_requests/3273) |
| DevOps-883 / infra-tf | DevOps-883-k8s-access | add k8s developer user | [!194](https://gitlab.youdo.sg/sysadmins/infra-tf/-/merge_requests/194) |
| DevOps-883 / helm-charts | DevOps-883-dev-access | add developer access | [!1](https://gitlab.youdo.sg/sysadmins/helm-charts/-/merge_requests/1) |
| DevOps-886 / infra-tf | DevOps-886-dev-ttl-controller | add dev ttl controller | [!198](https://gitlab.youdo.sg/sysadmins/infra-tf/-/merge_requests/198) |
| DevOps-886 / jenkins-pipelines | DevOps-886-dev-ttl-controller | check expired helm release | [!1](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins-pipelines/-/merge_requests/1) |
| DevOps-886 / gitlab-ci-templates | DevOps-886-dev-ttl-controller | increase ttl time | [!87](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/87) |
| DevOps-886 / helm-charts | DevOps-886-dev-ttl-controller | increase ttl, delete old files | [!2](https://gitlab.youdo.sg/sysadmins/helm-charts/-/merge_requests/2) |
| DevOps-832 demonstration / tochka-proxy | DevOps-832-example | bump | [!240, open](https://gitlab.youdo.sg/youdo/microservices/youdo-business-tochka-proxy/-/merge_requests/240) |

All ten new MR titles are task ID + original commit subject, except demonstration `DevOps-832 demonstration`. All descriptions contain only `Closes <TASK-ID>`. All are assigned to `a.solonenko`, reviewers empty, source-branch deletion enabled. Nine have squash disabled; iOS has squash enabled and targets develop, the others target master. These are observed MR choices, not verified project-wide mandatory settings. Actual ticket closure by Closes was not checked.

Short English lowercase subjects and ticket-prefixed branch/MR names are consistent. Some subjects (`bump`, `increase ttl time`) omit the object or behavior; agents should be slightly more descriptive without introducing Conventional Commits. The same task can span repositories with shared branch names and different MR summaries. A merge is delivery of code, not proof of successful infrastructure rollout. Non-Git operational work is outside naming examples.

## Proposal status
Superseded on 2026-10-08 by the user-approved [supervised training policy](../systems/gitlab-ci/agent-git-workflow.md).
The original proposal below is retained as history; it is not active authority. The separate
Closes recommendation was removed from the adopted rules at the user's request.

## Original proposed instructions (historical, inactive)
The following is a candidate exception to the global Git and external-state rules. It must explicitly override both; otherwise the existing per-command approval requirements remain in force.

1. Publication authority: only when the user explicitly delegates publication for a task (for example, "implement DevOps-900 and publish an MR"), the agent may create a task branch, stage the task's paths, commit, push that branch and create/update its own MR without further approval for each command. This exception covers only the named task and repositories; "investigate", "prepare a diff" and "propose rules" do not authorize publication. A user may grant this authority for all implementation tasks separately; do not infer it from this review.
2. Preflight: inspect repository instructions, origin, base/target branch, git identity, working tree and existing MRs. Preserve unrelated staged/unstaged changes. Stage explicit paths; inspect the final staged diff for scope and secrets. Do not invent a ticket, rewrite git identity, or assume master; use project conventions (YouDoApp currently develop).
3. Branch: `<TASK-ID>-<short-english-kebab-case>`, e.g. `DevOps-879-http-timeout`. Use the exact tracker ID and observed project exception where applicable (iOS can use `IOS-5054`). One task branch and one MR per repository; reuse the task's existing branch/MR. Related repositories may use the same branch name. Do not overwrite a colliding branch belonging to someone else.
4. Commit: concise English lowercase action and object, no mandatory task prefix and no added fix:/feat: convention. Prefer one coherent commit for a small finished change; split independent changes when useful. Examples: `set selenium http read timeout`, `add developer access to dev namespaces`, `increase dev environment ttl to 6 days`. Never use uninformative `bump`, `fix`, `changes`. GitLab generates merge commits; agents do not synthesize them.
5. MR title: `<TASK-ID> <short English change summary>`, usually matching the coherent commit subject. Do not force a misleading single-commit title on a multi-commit MR.
6. MR body: identify the issue/change, checks actually performed and their results, material limits, and dependencies/links to other task MRs. Use a normal ticket reference for partial or cross-repository work. Preserve `Closes <TASK-ID>` only when task closure is intended and the integration behavior is understood; do not add it automatically to every partial MR or demonstration. Do not claim deployment or runtime success from a merge or static validation.
7. MR metadata: assign the user; do not invent reviewers or labels. Respect mandatory project settings. Observed defaults for these infra MRs: squash off, source-branch deletion on merge on; iOS exception: squash on. Draft when work/checks/dependencies remain incomplete; ready when the agreed checks pass. Missing checks must be stated. Never enable auto-merge.
8. CI side effects: inspect push/MR pipeline rules before publishing. The publication exception includes ordinary build/test/validation pipelines. Any automatic deployment, Terraform apply, destructive action, package/image release or other runtime mutation needs separate authorization covering that effect before push/MR creation. Do not bypass CI or protected-branch controls to avoid permission requirements. Manual deploy/retry buttons are not covered by publication authority.
9. Boundaries: no direct push to the target/protected branch, force push, remote branch deletion, tags, merge, automatic merge, deployment, task closure API call or history rewriting under this exception. Do not stash/reset/discard user changes. The source-branch deletion option authorizes deletion by GitLab upon a later user-approved merge, not an immediate agent delete. Local history rewrites and other nonessential Git mutations require explicit authorization.
10. Verification and completion: run appropriate checks; after push/MR creation verify the remote SHA, MR source/target and latest pipeline state for that SHA. Search for an existing MR and check remote state before retrying a timed-out mutation. Report branch, commit SHA, MR URL, checks and unresolved dependencies; leave merge to the user.

Example MR:

```text
DevOps-879 set selenium http read timeout

Set a bounded HTTP read timeout for RemoteWebDriver requests.
Checks: <actual command and result>.
Runtime validation: <actual result, or pending>.
Related: DevOps-879.
```

## Changes
Only this local review note and generated KB index were added/updated. Active AGENTS.md, repository files and external state were not changed. The daily ai-sync exception remains separate from the proposed publication authority. No new repository was discovered; repo catalog changes were unnecessary. The task concerns proposed agent behavior, so no infrastructure system map was changed.

## Risks
A one-week sample supports conventions but not a mandatory organization-wide standard. MR descriptions are too short to transfer validation evidence; slightly richer bodies are proposed. Project merge settings, CI behavior and ticket integration must be checked per future task. Rules above remain a proposal; adoption and the desired scope of standing publication authority are user decisions.

## Portable lesson
None created: this review documents company-specific observations and an unadopted policy proposal.
