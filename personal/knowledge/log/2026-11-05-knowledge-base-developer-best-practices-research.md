---
system: knowledge-base
status: verified
checked: 2026-11-05
tags: [agents, skills, research, evals, context]
decision_state: restricted
decision_scope: Standing proposal-recording rule inferred from this discussion only
decision_summary: The user limited proposal recording to this dialogue. The mistakenly added permanent rule was removed and its learning record rejected; research proposals remain recorded.
decision_date: 2026-11-05
decision_source: #scope-correction
---
# Agent methodology: primary-source developer practices

## Summary

Primary-source research requested by the user into practices for the existing local
agent methodology: rules, skills, scripts, retrieval and task coordination. Sources
were opened from OpenAI, Anthropic, Google and LangChain. This concerns how agents
work, not business knowledge freshness. The strongest next investments are observable
behavior evaluations, scoped skill activation, precise tool outcomes, canonical
instruction ownership and measured removal of unnecessary procedural overhead.
Existing four central proposals were enriched, not duplicated. F1 from the preceding
review is already fixed; other implementation remains unrequested. The user clarified
that proposal recording applies only to this dialogue. The mistakenly added standing
README rule was removed and its learning record rejected. No model-backed evaluations, installations or external
state changes were performed. Vendor experiments are not measurements of this setup.

## Task

Continue recording proposals within this dialogue and research
best practices, particularly from AI developers. Research and local bookkeeping are
authorized; the broader implementation proposals are not.

## Context

- [Methodology review and current proposal mapping](2026-11-05-knowledge-base-agent-methodology-review.md).
- [Prior source research](2026-10-19-knowledge-base-agent-capabilities-research.md):
  historical pilots remain subject to their scoped final decisions. The cancelled
  Claude evaluation is not reopened by reading Anthropic engineering guidance.
- [Existing retrieval outcome](2026-11-04-knowledge-base-retrieval-context-decisions.md)
  and [completed sync fix](2026-11-05-knowledge-base-sync-checker-failure-stop.md).
- [Canonical procedure](../../../general/knowledge/README.md), [central TODO](../../../TODO.md).
- Applied agent-learning and OpenAI Docs. Three delegated read-only research tasks
  covered OpenAI, Anthropic, and Google/LangChain; the parent owned synthesis and writes.

## Actions

1. Ran required sync and consulted applicable local rules and existing proposals.
2. Searched official domains and opened primary sources; checked publication dates
   and distinguished current documentation from version-specific experiments.
3. Compared findings with the already observed local failures and existing structure.
4. Initially overgeneralized the dialogue-scoped proposal-recording instruction into
   a standing rule. The original evidence event is retained in
   `~/ai-data/agent-research/2026-11-05-best-practices/preference-event.json`;
   the erroneous promotion was later reversed as recorded under Scope correction.
5. Linked research recommendations into the existing four TODO proposals; retained
   current implementation/approval status and preserved unrelated file changes.

## Sources

All checked on 2026-11-05. Publication dates below are the dates shown by the authors;
undated documentation is an observed current page, not a pinned immutable version.

| ID | Primary source | Published | Evidence type |
| --- | --- | --- | --- |
| S1 | [OpenAI: Customization](https://learn.chatgpt.com/docs/customization/overview) | Undated | Product guidance |
| S2 | [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills), Dominik Kundel and Gabriel Chua | 2026-01-22 | Practical evaluation method |
| S3 | [OpenAI: Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex), Tony Alaniz | 2026-08-03 | Adaptable workflow recipe |
| S4 | [Anthropic: Writing effective tools for agents](https://www.anthropic.com/research/writing-tools-for-agents) | 2025-09-11 | Engineering recommendations and examples |
| S5 | [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Undated | Skill-authoring guidance |
| S6 | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | 2026-01-09 | Evaluation design guidance |
| S7 | [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) | 2025-11-26 | Case-specific engineering experience |
| S8 | [Anthropic: Harness design for long-running application development](https://www.anthropic.com/research/harness-design-long-running-apps), Prithvi Rajasekaran | 2026-03-24 | Later model/task-specific experiments |
| S9 | [Google: The Anatomy of Harness Engineering](https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/), Taylor Mullen and Christian Gunderman | 2026-09-09 | Behavioral evaluation guidance |
| S10 | [Google: Architecting efficient context-aware multi-agent framework for production](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/), Hangfei Lin | 2025-12-04 | ADK architecture experience |
| S11 | [LangChain: Deep Agents v0.7](https://www.langchain.com/blog/deep-agents-v0-7), Sydney Runkle | 2026-07-29 | Developer-reported comparative experiment |
| S12 | [LangChain: Context Engineering: How Deep Agents Remember](https://www.langchain.com/blog/context-engineering-deep-agents-remember), Jess Weng | 2026-10-14 | Implemented context-management techniques |

## Findings and local adaptations

### R1 — Separate structural, script and behavioral checks

S2 evaluates skill selection, observable actions and artifacts, including explicit,
implicit and adjacent negative cases. S6 distinguishes a trace from the final state
and cautions against requiring one exact solution path. S9 recommends narrow
behavioral checks and repeated trials for stochastic behavior.

Local proposal: extend the existing bounded evaluation direction rather than build
a new service. Start with one skill and roughly 10–20 representative cases, then
repeat relevant cases to compare reliability. This initial size is a working proposal,
not a guaranteed coverage threshold. Cases should include read-only review, an
adjacent out-of-scope request, missing publication approval, existing approval,
preserved unrelated changes and a missing required source. Check actual artifacts
and observable permission events; do not demand arbitrary tool-call sequences.

Keep three reports distinct: instruction lint, deterministic helper tests, and fresh
agent-session behavior. Sanitized fixtures belong with tests; private traces belong
under `~/ai-data/`. No such model runs were started during this research.

### R2 — Give each rule or workflow one canonical owner

S1 separates durable project guidance from reusable skills. S3 assigns improvements
to the smallest appropriate owner instead of creating a new skill for every correction.
S5 describes metadata-driven discovery and loading detailed instructions only when useful.

Proposed local ownership:

| Artifact | Responsibility |
| --- | --- |
| AGENTS | Always-applicable boundaries and routing to scoped procedures |
| SKILL | One coherent recurring workflow and its invocation conditions |
| README/reference | Detailed procedure with direct, validated links |
| Existing script | Mechanical invariants and deterministic failure checks |
| Central TODO | Proposed, active and completed action status |
| Task/source record | Decisions, evidence, limits and resumption state |

Review the existing overlaps first. The proposal does not introduce a new plugin,
parallel backlog or compulsory collection of GOALS/PLANS files. Explicit durable user
instructions still take effect immediately within their authorized scope.

### R3 — Make tool completion, coverage and recovery explicit

S4 recommends meaningful, bounded responses and actionable errors. S12 retains large
results outside the active context and provides a route back to the source material.

Our proposed helper contract distinguishes successful results, a completed empty
search, completed findings and execution failure. Where relevant, include result
count, truncation/partial-coverage indicator, continuation cursor or line range,
source reference and the next permitted diagnostic action. Those fields are a local
design proposal, not a vendor-prescribed universal JSON schema.

Keep concise output as the normal path and make detailed evidence retrievable. Store
sanitized artifacts in `~/ai-data/`, respecting existing secret constraints. Failure
must remain visible even when output is abbreviated. F1 implements one narrow part;
the missing-root and secret-format coverage defects remain open separately.

### R4 — Preserve a compact, verifiable resumption state

S7 describes progress artifacts and environment checks for continuing long tasks.
S3 recommends preserving decisions, constraints and evidence provenance without
repeating full command histories.

Use the existing task record for the user goal, approved scope, decisions, performed
checks, unresolved uncertainty and next permitted step. Keep cancelled directions
explicit. At resumption, compare important recorded state with observable files or
the requested read-only source before acting. This is not a second live TODO list.
Vendor examples using automatic commits do not change our publication permissions.

### R5 — Delegate bounded work with explicit context and ownership

S10 separates durable state from per-invocation context and motivates focused context
for independent subagents. Applying it here, give a reviewer a concrete objective,
source paths, constraints, expected evidence format and an explicit read/write scope.

Evaluate independence, reading volume and coordination cost rather than the number
of files. A coordinator owns shared index/TODO/sync and deduplicates returned evidence.
Narrow context can omit relevant constraints, so important approvals and prohibitions
must be passed explicitly with a route to ask the coordinator for missing context.

### R6 — Revalidate procedural overhead as models and tasks change

S8 reports removing earlier context resets and later mandatory sprints as stronger
models made them unnecessary for the studied application tasks. S11 compares a leaner
harness across models and reports a 65% reduction in base input tokens; cost effects
were mixed, and its planning middleware became opt-in.

Local proposal: compare one procedural change at a time using a fixed baseline,
model/settings and case set. Candidates are duplicate reads, mandatory planning for
small tasks and file-count-based delegation. Measure correctness and constraint
violations first, then time, extra reads and token use. Do not transfer vendor savings
percentages to this setup or treat removal of their planning middleware as permission
to remove our central backlog. User-selected permissions are held fixed.

### R7 — Turn corrections into a small change plus evidence

S3's ownership approach fits the existing learning workflow. For a proposed technical
improvement, identify the affected owner, failure mechanism, smallest change and
verification scenario. Prefer an existing script check for a reproducible mechanical
failure over accumulating repeated prose. Preserve the distinction between an explicit
user instruction, a task-specific direction and an agent-inferred hypothesis.

No new learning database or mandatory approval stage is proposed. The current fix for
F1 is an example: the error was reproduced, the existing script changed narrowly and
the failure/allowed-result cases were tested.

## Decision and backlog mapping

The user's instruction to continue recording proposals applies only within this
dialogue. It establishes no new permanent rule. All R1–R7 technical adaptations
remain proposed; this research does not authorize model evaluations or implementation.

| Existing proposal | Research details |
| --- | --- |
| Automation checks, F2/F4 | R3: completion/failure semantics and coverage |
| Instruction/knowledge retrieval, F3/F6 | R1/R3: measure visibility, expose partial results and continuation |
| Skills/prompts/templates, F5/F7 | R2/R7: canonical ownership, scoped triggers and targeted enforcement |
| Applicability and coordination | R1/R4/R5/R6: behavior evaluation, state, delegation and controlled simplification |

Suggested sequence for a later decision: address known protective-check defects;
prepare a small behavioral baseline before changing skill activation or broad process
rules; then compare one scoped improvement at a time. Detailed source reading alone
does not establish a gain. The existing cancelled Claude pilot remains cancelled.

## Scope correction

On 2026-11-05 the user clarified: `Но ведь это было только в рамках текущего диалога`.
The agent had incorrectly classified a dialogue-specific request as a standing
instruction despite the already-loaded learning skill's task-scope rule.

Removed only the newly added proposal-recording paragraph from README. Marked
`persist-methodology-discussion-proposals` rejected through the learning helper,
preserving its history while excluding it from active instruction retrieval.
Corrected this note and the linked review so the rejected instruction cannot be
presented as current. Existing saved proposals, central TODO entries, older general
bookkeeping rules and the authorized F1 sync fix are retained. No replacement
standing rule was created; the direction remains within the current dialogue.

## Verification and limits

Sources were searched and opened, with dates and caveats recorded. The source review
combines vendor documentation, engineering advice and vendor-run experiments; it is
not an independent reproduction of their results. No local performance/cost improvement
has been measured here. No benchmark baseline was replaced. Local checks cover the
bookkeeping edits and the scope rollback; they do not validate R1–R7 behavior.

## Changes

The mistakenly added standing README rule has been removed and its learning entry
rejected. This research note, links from the existing review/TODO, affected title-cache
entries, indexes and sync history preserve the research and the scope correction. No implementation script,
skill workflow, runtime setting or external system was changed by the research.

## Status and risks

The later user-requested [prioritized skills and tooling research](2026-11-05-knowledge-base-prioritized-agent-tools.md)
combines these proposals and the earlier defects into a twenty-item dated ranking.
It adds concrete candidates without installing or activating them. Dialogue-only
scope remains unchanged; central TODO links both evidence records.

Research and proposal recording completed on 2026-11-05. Remaining actions live only
in [central TODO](../../../TODO.md), Knowledge base, through the four existing proposal
groups. No additional implementation is assumed. All delegated research finished;
no background work or model-backed evaluation remains running.

## Portable lesson

none
