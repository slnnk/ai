---
system: knowledge-base
status: verified
checked: 2026-11-14
tags: [retrieval, agent-learning, regression]
---
# Rule and knowledge retrieval: relevance, coverage and continuation

## Task

Implement the existing F3/F6 proposal after the user explicitly requested
`Реализуй` following its three-part explanation: relevant rules survive result limits,
knowledge retrieval remains useful as logs grow, and incomplete output has observable
coverage and continuation. Implementation is local to `~/ai`; no external changes,
new agent/model runs or permission changes were authorized or performed.

## Context

- [Original findings F3/F6](2026-11-05-knowledge-base-agent-methodology-review.md).
- [Central backlog](../../../TODO.md), Knowledge base F3/F6 entry.
- Existing unrelated working-tree changes were present and preserved; no manual Git
  mutations were performed. The ai repository is exempt from the first edit gate.
- Expected result: exact-key and matching task rules survive a full global quota;
  repository/task isolation remains intact; saved retrieval conditions lose no target,
  visible answer or decision against the accepted November 4 baseline; pagination and
  excerpt limits are explicit and usable.

## Actions and findings

The before run reproduced five regression findings across 72 fixed conditions:
company case c01 operational queries lost the target and answer from top five in
both layer modes, plus the required scoped target failed. The old baseline and suite
were retained unchanged. Reports retained in `~/ai-data/kb-retrieval/2026-11-14-rules-stability/before/`.

`agent_learning.py query` now ranks exact keys, then topical matches and applicable
task/repository/layer specificity before active state and recency. All existing exclusion
filters remain, including task identity and rejected/superseded history handling.
Active global obligations remain in the result set; coverage distinguishes background
rules. `--offset` and a shell-quoted next command allow bounded continuation.

`kb_find.py` gives system maps and portable recipes a one-term tie preference and
uses matching-line density rather than raw frequency to limit long-log dominance.
More specific title identifiers retain priority. JSON and text report pagination;
JSON adds excerpt coverage, omitted matches and clipped-line indicators. Files-only
stdout remains path-only, with continuation on stderr. Source references support
reading full sections/lines. Pagination requires stable input between calls.

## Changes

- `general/scripts/agent_learning.py`, `general/scripts/kb_find.py`.
- Behavioral regressions in `general/scripts/tests/test_agent_learning.py` and
  `general/scripts/tests/test_kb_find.py`.
- Search contract in `general/knowledge/README.md` and agent-learning retrieval
  documentation in `general/skills/agent-learning/references/operations.md`.
- Existing F3/F6 TODO entry reconciled with this result; no new backlog copy.

## Verification and status

The first after run completed all 72 saved conditions with no regressions against
`~/ai-data/kb-retrieval/2026-11-04-context-decisions/after-5/results.json`.
Operational top5 improved from 11/12 to 12/12 in each layer mode; visible answers
from 7/12 to 8/12. Exact unscoped top1 improved from 11/12 to 12/12. Natural Russian
literal variants still return no matches, as before; query preparation remains required.
The suite, anchors and accepted baseline were not revised.

Behavioral suites passed: 17 agent-learning tests and 26 KB tests, including real
execution of both generated continuation commands, scope isolation, long-line clipping,
omitted sections, zero note budget and growth distractors. Agent lint reported zero
errors/warnings/info; KB lint reported zero errors/warnings. Task-scoped expected-result
and discussion-before-implementation outcomes were linked to this evidence.

Final reproducible run location:
`~/ai-data/kb-retrieval/2026-11-14-rules-stability/final/`.
Use `kb_benchmark.py --cases ~/ai-data/kb-retrieval/suite-v2.json --output-dir <fresh-dir>
--baseline ~/ai-data/kb-retrieval/2026-11-04-context-decisions/after-5/results.json --enforce`
to repeat the unchanged checks. The before and initial-after reports are retained in
sibling directories. The original baseline remains immutable.

Checkpoint: implementation and documentation are complete; the F3/F6 central TODO
entry is closed. The final saved suite run exited 0 with 72 conditions and no regressions;
agent-learning check validated 68 records and local diff whitespace validation passed.
No task processes or agents remain. No fresh-agent adoption experiment was launched. Ranking and
synthetic checks demonstrate retrieval mechanics, not fresh-agent adoption or universal
ranking guarantees. No new external search service or background evaluator is installed.

## Portable lesson

Use explicit coverage and continuation; relevance within existing scope filters is
separate from proving that a consumer loaded and applied the returned canonical rules.

Measured JSON output grew from 2136 to 2621 mean bytes per condition because coverage and continuation are now explicit. Corpus hashes and latency per condition are retained in the reports.
