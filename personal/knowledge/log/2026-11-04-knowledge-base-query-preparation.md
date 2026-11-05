---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [agents, search, retrieval]
decision_state: superseded
decision_scope: Earlier statement that only proposal1 is implemented
decision_summary: Query preparation remains in effect. Proposals 2-4 were subsequently implemented; follow the later current outcome.
decision_date: 2026-11-04
decision_source: 2026-11-04-knowledge-base-retrieval-context-decisions.md#current-outcome
---
# Agent query preparation for knowledge retrieval

## Task

The user requested implementing only proposal1 from the retrieval discussion:
teach agents to prepare search terms, choose layers and simplify empty queries.
No changes to snippet rendering, ranking, lifecycle status or benchmark expansion
were requested. [Baseline](2026-11-04-knowledge-base-retrieval-baseline.md).

## Context

The baseline retrieved all 12 known targets using technical terms, while all 12
constructed Russian keyword queries returned no matches. This motivates a small
agent-side procedure rather than changing literal matching in `kb_find.py`.

## Actions

Replaced the existing search entry in shared AGENTS with an explicit read trigger
for README Knowledge retrieval. Added the canonical preparation procedure there:
preserve identifiers and errors, translate concepts to English technical terms,
select the known layer(s), use AND first and limit empty-query reformulations to
two. Distinguish a real empty result from tool failures. Retain source-status and
selected-section inspection without claiming default snippets contain the answer.

## Findings

The same search script remains in place. Query translation is performed by the
agent; no translation API, dependency, runtime hook or extra service is introduced.
Scoped company queries may include the general layer for portable recipes. Unknown
scope is searched without an invented layer filter. Exact errors and identifiers
are not translated, and hypothetical causes must not become restrictive terms.

## Changes

Shared `~/ai/AGENTS.md` and `~/ai/general/knowledge/README.md`; this task record;
source baseline outcome and the affected central TODO proposal. The existing
agent entry-point links continue to reference the same canonical instructions.

## Status and risks

Only query preparation is implemented. Other proposals remain unimplemented in
the [central TODO](../../../TODO.md). Verification results are recorded below. No fresh-client behavioral evaluation is claimed by a static
instruction edit or by manually exercising prepared queries.

## Portable lesson

The canonical procedure is README Knowledge retrieval; no duplicate recipe.

## Verification (2026-11-04)

- Reused the baseline's prepared technical terms with their known layer: all 12
  targets appeared in the top five on the live corpus. This confirms that the
  examples work, not that an agent independently translated unseen questions.
- Exercised the bounded fallback on an isolated copy of the resolved/SERVFAIL
  recipe: an incorrect personal-layer filter gave two normal empty results;
  dropping the filter on the third call found the target. A first live probe
  encountered the baseline report itself, so isolation was necessary to test
  the empty-result branch rather than document self-contamination.
- The conservative README example `helm false` finds the expected recipe first.
  Review removed the guessed cause `default` from the initial example so the
  instructions do not contradict their own prohibition on invented causes.
- Search-script SHA-256 remained unchanged. No code, rendering or ranking changes.
- `kb_lint.py`: 0 errors and 0 warnings. `git diff --check`: passed.
- `agent_lint.py --force`: 9 files, 0 errors, 0 warnings and 2 informational
  findings; the helper rechecked one valid Codex configuration value against its
  version-compatibility rule. No automatic fixes were applied.
- Affected TODO title cache and source baseline reconciled. The new open proposal
  remains under Knowledge base and contains only unimplemented directions.

Artifacts: `~/ai-data/kb-query-preparation/2026-11-04/checks.json` and the saved
`check_prepared_queries.py`. The latter is the executed one-off verification
harness, not an installed search component. All task commands have finished;
the read-only reviewer is complete. No background operations remain.
