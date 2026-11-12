---
system: knowledge-base
status: verified
checked: 2026-11-12
tags: [agents, simplicity, review]
---
# Ponytail: assessment for local agent rules

## Task
Assess the public Ponytail repository for useful additions to existing local rules.
Research and proposals only; adoption was not requested.

## Context
Inspected main tree revision `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` through GitHub GET.
Sources: [AGENTS](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/AGENTS.md),
[review skill](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-review/SKILL.md),
[debt skill](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-debt/SKILL.md),
[copy checker](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/scripts/check-rule-copies.js),
[activation hook](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-activate.js),
[benchmark](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/results/2026-06-18-agentic.md).
Local comparison: shared AGENTS, README Simplicity and Verifiable results, agent-learning,
and [prior simplicity review](2026-11-12-knowledge-base-karpathy-guidelines-review.md).
Some web reads used main and may be cached; the tree revision is a reference snapshot,
not a claim that every fetched source was independently hash-verified.

## Actions
Read core instructions, review/debt skills, lifecycle activation and instruction builder,
copy-consistency checker, behavioral checker tests and agentic benchmark methodology.
Daily ai-sync exited 0 without output or reminders. No checkout, install or benchmark run.

## Findings
Existing Simplicity already covers YAGNI, unnecessary options and safeguards.
Proposed additions, inactive until user approval:
1. Prefer established project solutions, then stdlib/platform or installed dependencies,
   then minimal new code. Respect existing architecture; do not replace a project component
   merely because a native alternative is shorter. Dependency choice must fit requirements.
2. Determine the full affected flow before editing: callers, consumers, tests, fixtures,
   configuration and exports. Fix a shared cause when appropriate, within approved scope.
3. Require a concrete reachable failure scenario and source location for review findings;
   separate confirmed defects from hypotheses and style preferences. This is the highest-value addition.
4. For deliberate shortcuts, document the real limit and trigger for revisiting it.
   Keep actionable follow-ups in central TODO, without a separate debt backlog.
5. Copy-consistency checks can complement agnix where independent adapters really exist;
   existing symlinks are already better than copies for identical instruction bodies.

Do not adopt line-count targets, mandatory one-line formatting, ultra pushback mode,
a blanket deletion preference, automatic hooks or a separate debt ledger.
The activation hook injects instructions and writes mode/statusline state; adoption would
be a separate settings/runtime change. Current local activation and permission policy wins.
Author benchmark reports 54 percent fewer added lines on twelve FastAPI/React features,
Haiku 4.5, four runs per condition. Feature functionality was not validated in a server/browser.
The 100 percent safety result is twenty deterministic checks, not a security guarantee.
Older single-shot reductions were acknowledged as inflated by the conversational baseline.
Behavior checker unit tests validate grading heuristics, not actual fresh-agent compliance.
These results do not establish savings for our Codex DevOps tasks. No benchmark reproduced.

## Changes
Research note and central proposal only. Active rules, skills, settings and external state unchanged.

## Status and risks
Research complete. Adoption remains a proposal in [central TODO](../../../TODO.md).
No background task remains. Implementation behavior and local savings are unmeasured.

## Portable lesson
Reuse and concrete review evidence make simplicity operational; smaller diffs are only
useful when the required behavior and safeguards remain complete.

Checks: kb-lint reported zero errors and warnings; the proposal rendered under Knowledge base.
Discussion-before-implementation outcome recorded as pass from actual research-only behavior.
