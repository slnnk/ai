---
system: knowledge-base
status: verified
checked: 2026-11-12
tags: [agents, instructions, review]
---
# Karpathy-inspired guidelines: local adaptation review

## Task

Review https://github.com/multica-ai/andrej-karpathy-skills for local instructions
and knowledge-base applicability. Initially research only; simplicity adoption was
subsequently approved and resumed after an interrupted session.

## Context

Read shared AGENTS, triggered KB README sections, current CONTEXT, the knowledge-base
backlog and agent-learning rules. Prior related proposal:
[one canonical owner per rule](2026-11-05-knowledge-base-developer-best-practices-research.md#r2--give-each-rule-or-workflow-one-canonical-owner).

## Actions

Read upstream README, CLAUDE.md, skills/karpathy-guidelines/SKILL.md and EXAMPLES.md
through web retrieval on 2026-11-12. No upstream commands executed. Daily sync exited
zero without output or reminders. Scoped search found no existing Karpathy note.

## Findings

Upstream offers four instruction principles: explicit assumptions, simplicity,
task-only changes and verifiable outcomes. It is guidance inspired by Karpathy's
observations, not evidence of measured behavioral improvement in this environment.

Task scope, preserving unrelated edits, approval boundaries and progress reporting
already have local owners. The useful proposed delta is a short requirement to
choose the simplest sufficient solution and establish an observable success check
before nontrivial changes. Existing rules should own the adaptation, without a new
plugin, duplicated instruction file or separate skill.

Proposed wording, not active policy: Prefer the simplest solution satisfying the
request and established operational requirements. Add abstraction/configurability
only for a demonstrated need. Before nontrivial changes, state the expected result
and proportionate verification; before completion, compare actual evidence with it.
For KB work, update the existing canonical note and preserve dated uncertainty.

Adaptation limits: clarify uncertainty that materially affects scope, correctness or
permissions, without stopping for routine reversible choices. Keep defensive handling
for realistic network and infrastructure failures. Line count alone is no reason to
rewrite working code. Test-first examples do not require new tests for trivial edits;
DevOps verification may use a plan, artifact inspection or read-only status check.
Verification loops never grant deployment, retry or external-write permission.

EXAMPLES.md's sorting example claims to verify equal-score ordering but asserts only
scores, leaving tie order unchecked. Treat examples as illustrations, not validated
test patterns. Benefit of the proposed local wording remains unmeasured.

## Changes

### Discussion correction: material assumptions

The initial recommendation foregrounded simplicity and success checks and omitted
assumption clarification as a proposed addition. In follow-up, the agent acknowledged
that existing scope/approval safeguards only partially cover interpreting the task.
The user challenged why a useful missing rule had not been proposed. The omission
was a recommendation error, not evidence that the user adopted a new standing rule.

Corrected proposal, pending adoption: First check material assumptions against
available context. If remaining uncertainty affects the result, scope or permissions,
clarify before acting; resolve routine reversible implementation choices independently.
Include this alongside simplicity and observable success in the same central proposal.
The initial omission remains a failed application of proactive gap detection; this
recovery does not replace that outcome with a pass. No operational policy changed.

Research note and central proposal bookkeeping only; operating instructions,
skills, settings and repositories were not changed or installed.

## Status and risks

Assessment complete. Simplicity adoption was approved and implemented locally on
2026-11-12; the remaining proposals are tracked under Knowledge base in
[central TODO](../../../TODO.md). Material-assumption clarification was subsequently
approved and implemented on the same date. Observable-success guidance was then
approved and implemented as well; all three adaptation items are complete in
[central TODO](../../../TODO.md). No plugin installed and no background operations
started. Behavioral effectiveness remains unmeasured in subsequent tasks.

## Portable lesson

### Simplicity wording review

The user selected simplicity as the first rule to discuss and supplied a same-day
company configuration example; evidence remains in the company task record, without
copying infrastructure identifiers into portable guidance. The rejected proposal
added an inventory-based condition, whereas the accepted result needed a single
unconditional directive. This supports focusing the proposed rule on unnecessary
conditions, not only abstractions or optional features.

Approved wording, now owned by README "Simplicity" with a short mandatory read trigger
in the shared AGENTS Local code and Git section:

> Prefer the simplest solution that meets the request and verified system constraints.
> Add conditions, exceptions, configuration options or abstractions only for a concrete
> requirement or demonstrated need, not hypothetical scenarios or future flexibility.
> Before presenting a change, check whether each added complication is necessary;
> omit it if removing it preserves the required behavior and existing safeguards.

The previous session ended after the user said `Хорошо, добавь правило про простоту`
and the agent announced the edit; no instruction write had occurred. Source:
Codex session `01a1ced4-16da-7e60-9d0b-b58427e7f6e6`, 2026-11-12.
The user requested resumption in the recovery session; the agreed rule was then added.
The detailed wording lives in README to retain the compact shared entry point.
Earlier research-only and pending-adoption statements above describe historical stages
and are superseded for simplicity by this implementation. Its behavioral effect has
not yet been measured on a subsequent implementation task.

Assumption clarification and observable-success proposals remain pending.
Verification after adoption: agent-lint checked 9 files with zero errors, warnings or
info; kb-lint reported zero errors and warnings; the remaining central TODO entry
rendered under Knowledge base with its refreshed Russian title. No background work.

### Material-assumption clarification adopted

After the user requested more detail about the first remaining proposal, the agent
explained checking existing context before asking, identifying interpretations that
change behavior, scope or permissions, and deciding routine reversible details
independently. The user approved the presented wording with `Сделай` in the recovery
conversation on 2026-11-12.

Implemented in README "Material assumptions", with a mandatory read trigger in
AGENTS.md "Before a task". The policy requires checking material assumptions against
available context, explicitly surfacing consequential alternative interpretations,
and clarifying before acting on that choice. Earlier pending-adoption statements
are historical and superseded for this rule. Observable success remains a proposal
in central TODO; no adoption of it or plugin installation was authorized.
Behavioral effectiveness of the new rule remains unmeasured in a subsequent task.
Post-edit verification: agent-lint checked 9 files with zero findings; kb-lint
reported zero errors and warnings after shortening the new read trigger to keep
AGENTS within its size limit.
The remaining central TODO entry renders under Knowledge base with an updated title.

### Verifiable results adopted

The user requested an explanation of the final proposal. The agent described
defining expected behavior and proportionate checks before nontrivial changes,
verifying that behavior before completion, and reporting evidence limits without
expanding permissions. The user approved the presented wording with `Сделай` in
the recovery conversation on 2026-11-12.

Implemented the approved wording in README "Verifiable results". Its mandatory
read trigger is in "Material assumptions", which the shared AGENTS requires agents
to read first; this keeps the shared entry point within its size limit. Earlier
pending-adoption statements are historical and superseded by this implementation.
All three approved proposals are implemented locally; no plugin installation was
requested. The completion check is to inspect the exact rule, its mandatory read
path and the closed TODO entry, then run agent-lint and kb-lint. Behavioral
effectiveness requires evidence from a subsequent applicable task.
Post-edit verification: exact rule and mandatory read path inspected; all three
central TODO entries are closed and the scoped listing contains no open items.
Agent-lint checked 9 files with zero findings; kb-lint reported zero errors and
warnings. No background operations remain.

None; local evaluation is retained here, upstream remains the primary source.
