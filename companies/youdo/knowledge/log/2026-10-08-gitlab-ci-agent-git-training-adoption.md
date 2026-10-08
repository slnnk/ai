---
system: gitlab-ci
status: verified
checked: 2026-10-08
tags: [agents, gitlab, training]
---
# GitLab: adopted supervised agent training through October 30

## Task
Adopt naming/publication rules with user-supervised training until 2026-10-30. The user
requires branch approval before task-file edits, then commit-message and MR-title approval
before publication. Corrections must inform the main rules. Full automation is a later decision.

## Context
[Baseline review](2026-10-08-gitlab-ci-agent-git-workflow-review.md).
[Active canonical policy](../systems/gitlab-ci/agent-git-workflow.md).
Shared entry point `~/ai/AGENTS.md`; Claude and Gemini instructions link to it.

## Actions
Updated global Git and external-state sections with the two-stage training exception.
Created the canonical policy map, feedback-record requirements and October 30 review criteria.
Added a due reminder to `~/ai/TODO.md`. Marked the initial proposal superseded by adoption.
Ran daily ai-sync (no output), KB lint and index regeneration. No product repository or
external system was changed; no manual Git commit/push was performed.

## Findings and user correction
The user explained that `Closes <TASK-ID>` was inserted automatically during MR creation.
Removed the separate Closes rule from the adopted policy; preserve normal template behavior.
The previous proposed broad publication delegation is replaced by two explicit approvals.
A second-stage approval covers commit, approved-branch push and MR creation/update together.
Feedback must update canonical rules, with per-task evidence retaining initial/final proposals.

## Changes
`~/ai/AGENTS.md`, `~/ai/TODO.md`, canonical policy map, initial weekly review note, this log,
and generated KB index. Training deadline: 2026-10-30, Europe/Moscow; first active session
on/after the date prepares results. No unattended scheduling was configured.

## Risks
Date expiry does not grant automation. Continue the supervised workflow until the user
reviews the report and chooses automation or extended training. Incomplete records must
be exposed in the final report rather than treated as successful training examples.

## Portable lesson
None: this is adoption of the user's company workflow and approval preferences.
