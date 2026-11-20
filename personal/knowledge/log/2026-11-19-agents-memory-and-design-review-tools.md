---
system: agents
status: verified
checked: 2026-11-19
tags: [agents, review, learning]
---
# Claude-Mem, Elephant–Goldfish, grill-me, and Karpathy guidelines

## Summary

Retain the existing Codex and Markdown workflow. Claude-Mem was already covered by
P0.2, with progressive retrieval selected as a pattern. The Karpathy guidelines
already have a local adaptation. EGM offers one additional
review technique for consequential designs. Give a fresh reviewer a self-contained
draft and source references, then ask for consequential gaps supported by evidence.
The useful grill-me addition is dependency order when clarification is necessary.
There is no evidence in this assessment to justify global installation or another
mandatory workflow.

## Task and context

The user requested a prior-art check and adoption assessment for four public
repositories. In the initial message two links pointed to EGM. The user supplied
the intended fourth link, multica-ai/andrej-karpathy-skills, in a follow-up. Scope is the shared local agent workflow.
Checked exact and alternate names with scoped knowledge retrieval, and checked the
relevant TODO entries and Markdown. P0.2 is a direct Claude-Mem match. No earlier
EGM or grill-me assessment surfaced in the searched KB. The existing
[bounded review guidance](2026-11-05-knowledge-base-developer-best-practices-research.md#r5--delegate-bounded-work-with-explicit-context-and-ownership)
covers related principles.

## Findings

### Claude-Mem

The [project](https://github.com/thedotmack/claude-mem#how-it-works) uses hooks, a worker,
an observer model, SQLite, and Chroma to capture and retrieve observations.
The [Codex adapter](https://github.com/thedotmack/claude-mem/blob/main/src/cli/adapters/codex.ts)
provides Codex-specific handling. Cloud sync is opt-in and the README says usage
analytics are enabled by default. A local database does not determine what the
observer provider receives. A second persistent stream of observations would add
retention, cost, and precedence questions alongside curated Markdown.

[P0.2](2026-11-14-agents-p02-learning-search-comparison.md#recommended-bounded-design)
already selected staged expansion. Current [retrieval rules](../../../general/knowledge/README.md#knowledge-retrieval)
use a bounded excerpt followed by the relevant source section and broader history
when needed. Improve or revisit capture only against an observed failure, such as
important decisions consistently missing from the KB or known records repeatedly
failing to surface. P2.1 was closed without a hook trial and the later
[adoption decision](2026-11-18-agents-p15-adoption-decision.md#p21-closure) found no
demonstrated reason to add lifecycle automation. No new adoption proposal.

### Elephant–Goldfish Model

[EGM](https://github.com/google/elephant-goldfish-model#how-it-works) separates
context-rich design from review with a fresh model context. The reviewer reads the
draft and its references without the parent discussion. The full process includes
five review stages. The [upstream test record](https://github.com/google/elephant-goldfish-model/blob/main/TESTING.md#harness-test-record)
reports 15 native reviewers in a complete Codex fixture, including brainstorm and
review. That measures workflow operation on that fixture. Its effect on our
designs and workflow cost is unmeasured. The [Codex integration guide](https://github.com/google/elephant-goldfish-model/blob/main/docs/codex.md#fresh-context-reviewers)
distinguishes parent-turn isolation from exclusion of host instruction files.
Fresh context does not enforce filesystem permissions.

The local candidate technique is one separately authorized, read-only review of a
consequential draft. Supply the document, goal, source links, scope and material
constraints. Leave out the author's narrative and prior verdicts. Ask what a reader
cannot reconstruct, what behavior is unspecified, and what the sources contradict.
Report location, scenario, impact and uncertainty. This extends
[Review evidence](../../../general/knowledge/README.md#review-evidence) to the
self-containedness of a design. Example: a deploy plan refers to rollback but leaves
the triggering metric and recovery owner only in the author conversation.
If used on a real task, evaluate findings by confirmed consequential omissions
beyond the ordinary review and the added review cost. A mandatory five-stage
workflow, permanent agent configuration or standalone trial has no demonstrated
local need.

### grill-me

The [skill text](https://github.com/RobMitt/grill-me-skill/blob/main/SKILL.md)
orders questions by decision dependencies, asks one at a time with concrete
options, looks in files first and summarizes the decisions. It requires Claude's
question tool and asks to complete every branch. The local
[Material assumptions](../../../general/knowledge/README.md#material-assumptions)
rule already handles file-first clarification of consequential requirements and
autonomous decisions for routine reversible details.

When a user explicitly asks to stress-test a design or a consequential ambiguity
blocks dependent decisions, ask the highest-leverage unresolved question first.
Offer concrete options and their trade-offs when useful, then revisit dependent
questions after the answer. Stop once the remaining choices fit within known
requirements or can be made reversibly. Example: settle downtime tolerance before
asking about cutover sequencing or rollback timing. A session-wide interview rule
and a separate skill are unnecessary for that technique.

### Karpathy guidelines

The exact [repository](https://github.com/multica-ai/andrej-karpathy-skills) was
[reviewed on November 12](2026-11-12-knowledge-base-karpathy-guidelines-review.md).
Its [skill](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md)
contains four coding principles. The user approved three local adaptations and
they are implemented in the shared README: clarify consequential assumptions,
choose the simplest sufficient solution, and define verifiable results before
nontrivial changes. The fourth principle, surgical changes, is already covered by
task-scoped edits in AGENTS.md and affected-flow checks in the README. The upstream
review diagnostic about tracing each changed line to the request is compatible
with those rules.

The local versions permit independent reversible decisions, retain handling of
realistic failures, and choose verification that matches the task. The current
skill and manifest describe the same guidance and show no additional mechanism
requiring adoption. Installing it would duplicate rules that already have
canonical owners. All three adoption entries remain closed in central TODO.

## Changes and status

The research phase was a documentary comparison. Recorded the assessment and task metrics. No
installation, pilot, delegated review, instruction change or prior backlog change.
The candidate practices are conditional on a real task and agreement to use them.
The experiment criteria require a concrete local problem with source evidence.
Reviewed the current P0.2, P1.5, P2.1 and P3.1 dispositions. No remaining
implementation or trial was committed to the backlog. The fourth-link follow-up
updated this assessment and confirmed the existing Karpathy decisions.

Applicable learning outcomes: this task exercised discussion-before-implementation,
because only investigation and bookkeeping were requested and performed.
There was no material ambiguity requiring a user question or recurring loaded-rule
failure requiring a new decision example.

## Local adoption

On November 19, the user approved implementing the selected EGM and grill-me
practices from this assessment. Both went into existing sections of the shared
README. [Material assumptions](../../../general/knowledge/README.md#material-assumptions)
now orders consequential questions by dependency, with options and consequences
when useful and a stopping condition. [Review evidence](../../../general/knowledge/README.md#review-evidence)
now specifies one read-only reviewer for an explicitly requested independent review
of a consequential draft, with a fresh context and clear source and scope boundaries.
The shared AGENTS.md already triggers both sections. Local adoption was limited to
documentation and learning evidence. No separate backlog action remains.

Verified both canonical texts, their existing read triggers and the explicit
review boundary. Instruction lint checked nine files without findings. Behavioral
benefit requires a future applicable task.

### Standing review trigger

The user said they would forget to request independent review. After confirming
that the proposed automatic trigger applies to plan and design drafts, the user
approved the three cases in the proposal. Before presenting a draft for approval,
one fresh-context, read-only reviewer checks risky production migrations or
cutovers, access changes with overgrant or lockout risk, and cross-system contract
changes with compatibility or rollout-order risks affecting multiple services or
teams. Other consequential drafts retain the explicit-request route. Code and
configuration can serve as evidence for plan review. The economical tool use rule
links this narrow exception, and implementation and external-change approvals
still apply. This supersedes the explicit-request-only activation recorded above.

## Task metrics: agents-memory-design-review-tools-20261119

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "agents-memory-design-review-tools-20261119",
  "created": "2026-11-19T00:34:17.673592+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "research",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Compared four primary repositories with canonical rules and checked existing analyses and adoption decisions",
  "updated": "2026-11-19T00:36:12.827064+03:00"
}
```

## Task metrics: agents-design-review-practices-20261119

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "agents-design-review-practices-20261119",
  "created": "2026-11-19T00:37:54.586111+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "instructions",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "User-approved changes in Material assumptions and Review evidence; both AGENTS triggers verified, instruction lint clean",
  "updated": "2026-11-19T00:37:54.586163+03:00"
}
```

## Task metrics: agents-standing-design-review-20261119

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "agents-standing-design-review-20261119",
  "created": "2026-11-19T00:41:16.659584+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "instructions",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Verified three automatic plan-review cases, narrow delegation exception and existing approval boundary; instruction lint clean",
  "updated": "2026-11-19T00:41:16.659630+03:00"
}
```
