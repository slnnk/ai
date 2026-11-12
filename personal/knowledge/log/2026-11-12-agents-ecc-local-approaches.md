---
system: agents
status: verified
checked: 2026-11-12
tags: [agents, ecc, research, context, evaluation]
---
# ECC: selective local workflow review

## Task

Assess whether approaches from the public ECC repository could improve local agents.
Research and recommendations only; no installation or instruction changes requested.

## Context

Canonical policy: shared AGENTS.md, knowledge README and agent-learning skill.
Existing [merged experiments](2026-11-06-knowledge-base-merged-agent-experiments.md)
already cover behavioral evaluations, resumption and lifecycle hooks. ECC was one
source for the implemented [learning workflow](2026-10-19-agent-learning-shared-correction-workflow.md).

## Actions

Ran ai-sync.sh successfully with no output or reminders. Retrieved scoped learning
rules and read canonical targets. Read selected public ECC source files through web
tools, then compared their mechanisms with current policy and pending experiments.
No ECC code was executed and no helpers were spawned.

## Findings

Engineering recommendations, not measured gains:

1. Compact resumption state is the strongest initial candidate: goal, authorized
   scope, decisions/cancellations, completed checks, next permitted step and running
   operations in the existing task record. Compare interrupted fresh-session behavior
   against the current approach; this maps to E08, not a second backlog.
2. Behavioral regression cases complement static lint: distinguish discussion from
   implementation approval, missing data from empty results, and preserved unrelated
   edits from unsafe changes. Repeated fresh trials with fixed cases, outcomes, time
   and total cost map to E02/E03/E05. A green instruction lint is not behavior evidence.
3. One targeted lifecycle check could reduce missed checks. Start with a nonblocking,
   supported check and evaluate duplicate invocation, false positives, latency and
   nested tool coverage; map to E12. Supported runtime coverage must be checked in the
   selected client before proposing a concrete hook. Do not copy Claude hooks blindly.
4. Search-first is partly implemented locally (existing scripts, KB and available
   tools). Its useful refinement is checking existing repository utilities and a
   suitable maintained dependency before writing a new helper, proportionate to scope.

Do not adopt automatic parallel agents or background observers: these conflict with
the user-selected single-agent default and explicit helper authorization. Do not
automatically promote repeated observations to global rules: local learning requires
scope, provenance and confirmation of inferred generalizations. Fixed coverage targets,
universal test sequences and model capability claims are not local evidence.

Sources inspected:

- [Resumption and compaction](https://github.com/affaan-m/ecc/blob/main/skills/strategic-compact/SKILL.md).
- [Evaluation harness](https://github.com/affaan-m/ecc/blob/main/skills/eval-harness/SKILL.md).
- [Lifecycle hooks](https://github.com/affaan-m/ecc/blob/main/hooks/README.md).
- [Search first](https://github.com/affaan-m/ecc/blob/main/skills/search-first/SKILL.md).
- [Agent orchestration](https://github.com/affaan-m/ecc/blob/main/rules/common/agents.md).
- [Continuous learning](https://github.com/affaan-m/ecc/blob/main/skills/continuous-learning-v2/SKILL.md).
- [Verification loop](https://github.com/affaan-m/ecc/blob/main/skills/verification-loop/SKILL.md).

## Changes

This assessment and learning outcome evidence only. No agent rules, skills, hooks,
settings, packages, Git publication or external systems changed.

## Status and risks

Research complete on 2026-11-12. Benefits are unmeasured; public main-branch sources
are mutable. Existing [central backlog](../../../TODO.md#knowledge-base) retains the
E02-E14 selection and coordination proposals; no duplicate tasks added. E08 first,
then targeted behavioral cases and a single hook remain optional proposals requiring
a separate implementation decision. No background task operations remain.

## User follow-up November 12

The user asked to add these approaches to the pilot list for future evaluation. Updated the existing E02-E14 central backlog entry and merged design evidence with the E08, E02/E03/E05 and E12 mapping. Refreshed the affected Russian display title. Recording is complete; pilot execution remains deferred, with no installation, runtime settings change or background operations.

## Portable lesson

none
