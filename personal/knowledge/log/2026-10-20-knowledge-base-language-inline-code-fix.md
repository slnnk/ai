---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [lint, language, markdown]
---
# Knowledge base language check: inline-code evidence

## Task

The user explicitly requested both parts of the existing language-warning proposal: exclude Markdown inline-code evidence from language counts and consistently mark exact source labels. This authorizes local KB changes; no Git publication or external changes were requested.

## Context

[Original warning review](2026-10-20-knowledge-base-lint-warning-review.md) and [company evidence audit](../../../current/knowledge/log/2026-10-20-knowledge-base-language-warning-audit.md). Five language warnings counted source evidence as prose.

## Changes

- `general/scripts/kb_lint.py`: language-only filtering now removes inline code with matching backtick-run lengths, including multiline spans. Unmatched or escaped opening delimiters remain prose. The existing fenced-code handling and greater-than-60 Cyrillic threshold are preserved. Secret, identifier and link checks continue to inspect original Markdown.
- `general/scripts/tests/test_kb_lint.py`: CLI regressions for inline/fenced evidence, Russian surrounding prose, multiple backticks, multiline spans, unmatched/escaped delimiters, threshold boundaries and secret/identifier checks inside inline code.
- [Vysor note](../../../current/knowledge/log/2026-08-12-android-farm-vysor-redmi-note-13-pro-input.md): mark the quoted Android setting as inline code.
- [Suite map](../../../current/knowledge/systems/android-farm/ci-suites.md): mark all selectable option values as inline code and identify the column as verbatim. Exact strings and historical infrastructure findings are preserved; no infrastructure revalidation was performed.
- Close only the affected central TODO proposal; preserve unrelated local edits.

## Checks and outcome

`python3 -m unittest discover -s ~/ai/general/scripts/tests -p test_kb_lint.py -v`: 11 tests passed. Full `kb_lint.py`: 0 errors, 0 warnings, including removal of all five audited language warnings. Forced `agent_lint.py --force`: 9 files, 0 errors, 1 existing CDX-CFG-025 warning and 2 informational findings. The warning concerns the unchanged Codex service-tier setting, as classified in the original warning review. Knowledge indexes refreshed after bookkeeping.

## Status and limits

Both requested parts implemented locally on 2026-10-20. No per-file suppression, evidence translation, threshold relaxation, external operation or manual Git mutation. The language check remains a Cyrillic-count heuristic, not a language detector or full Markdown parser. Existing fenced-code parsing is unchanged.

## Portable lesson

None; bounded implementation and regression evidence are in the script and tests.
