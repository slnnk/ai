---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [codex, tokens, parsing]
---
# Knowledge base: nested Codex shell accounting

## Task
Implement the requested improvement to regular `token_usage.py --kb` accounting: extract nested Codex shell calls rather than classify a whole JavaScript wrapper as one command.

## Context
The [October 14 audit](2026-10-14-knowledge-base-token-cost-comparison.md) established wrapper-level counting errors and supplied a separate static extractor in `~/ai-data/token-cost/`. The user explicitly requested implementation on October 19. This is local knowledge-base tooling; company Git/MR training gates are unchanged.

## Actions
Reused the audit approach in portable helpers under `general/scripts/`, without a runtime dependency on generated audit files. JavaScript is parsed using Node.js and Acorn; transcript code is never evaluated. Shell classification uses the Python standard library. Added integration and parser fixtures, and compared the original and updated `--brief` output on local transcripts.

Key verification commands:
```bash
python3 -m unittest discover -s ~/ai/general/scripts/tests -p 'test_token_usage*.py' -v
python3 ~/ai/general/scripts/token_usage.py --days 7 --kb --top 0
```

## Findings
- 17 regression tests passed on Python 3.8.10, Node 22.17.0 and Acorn 8.15.0.
- Original and updated token-total `--brief` output matched exactly on local transcripts.
- The live seven-day KB report completed successfully: 8682 wrappers, 11621 syntactic shell sites, 11531 extracted static calls, 90 unresolved dynamic sites and 11 JS parse failures. No dependency failures occurred. These counts describe the verification run, not a fixed weekly baseline.
- Missing Node/Acorn produces explicit unavailable/incomplete coverage while direct shell calls remain countable. Unsupported JavaScript is excluded rather than classified using source-string guesses.
- Commands are decoded separately, with cwd/turn context, ordinary cd, archived sessions, duplicate call identifiers, multi-file reads and partial-read pipelines handled. Patch bodies and literal path mentions are not treated as shell read calls.

## Changes
- `general/scripts/token_usage.py`: nested/direct Codex ingestion, per-command classification and parser coverage; token totals and Claude classification retained.
- `general/scripts/token_usage_kb.py`, `token_usage_extract.js`: portable static extraction and conservative shell classification.
- `general/scripts/tests/test_token_usage.py`, `test_token_usage_kb.py`: 17 focused regression tests.
- `general/knowledge/README.md`: dependencies and metric meaning documented.
- `~/ai/TODO.md`: implementation item completed; October 21 comparative audit remains open.

## Risks and limits
Counts are static requested reads, without matching successful tool output. Function bodies and branches can overcount; loops can undercount. Dynamic shell paths, custom readers, substitutions and complex shell control flow can be missed. Shell tokenization is not full shell validation. Output redirection is conservatively excluded. Current file sizes are not historical returned bytes or tokens. Missing parser dependencies are reported without installation or silent fallback. The existing historical audit is retained for the scheduled October 21 comparison; historical snapshots were not rewritten.

## Portable lesson
None; the portable implementation and its limitations are documented in script help.
