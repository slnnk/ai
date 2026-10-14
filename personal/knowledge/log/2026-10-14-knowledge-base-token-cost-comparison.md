---
system: knowledge-base
status: verified
checked: 2026-10-14
tags: [token-cost, kb-find, review]
---
# Knowledge base: October 14 token-cost comparison

## Task
Complete the October 14 reminder to compare knowledge-base access with the September 30 baseline.

## Context
Baseline: [September 30 measurement](2026-09-30-knowledge-base-token-cost-kb-find-summaries.md).
Saved snapshots: [October 1](../../usage/2026-10-01.txt), [October 8](../../usage/2026-10-08.txt), [October 14](../../usage/2026-10-14.txt).

## Actions
Read saved KB blocks and inspect the existing classifier. Generate a fresh snapshot with `python3 ~/ai/general/scripts/token_usage.py --days 7 --kb --top 0`.
Snapshot collected around 2026-10-13 22:10 UTC / October 14 01:10 Moscow. Its printed start date, October 6, is UTC; the rolling seven-day interval begins October 7 in Moscow.

## Findings
| Measurement | Agent | KB-active sessions | kb_find | Search | Index | Full reads | Partial reads | Full KiB |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| September 30 baseline | Claude | 10 | 8 | 142 | 7 | 47 | 79 | 1086 |
| October 1 | Claude | 11 | 21 | 152 | 2 | 31 | 96 | 764 |
| October 8 | Claude | 19 | 29 | 143 | 1 | 5 | 84 | 25 |
| October 14 | Claude | 5 | 6 | 47 | 0 | 1 | 20 | 10 |
| October 14 | Codex | 104 | 244 | 277 | 4 | 18 | 317 | 589 |

Claude full reads declined 47 -> 5 -> 1; October 8 was 89.4% below baseline, and October 14 was 97.9% below baseline. Estimated full-read volume declined 1086 -> 25 -> 10 KiB (97.7% and 99.1%). Full reads per KB-active Claude session declined 4.7 -> 0.263 -> 0.2, so the reduction is also visible after this simple workload adjustment.
Codex entries in the saved October 1/8 snapshots are all zero, leaving no usable Codex baseline. Current Codex counts are descriptive only. Across both current agents, 19 full reads / 599 KiB are below the old Claude-only totals, but this is not a like-for-like comparison.
User correction on October 14: Claude usage declined because the user switched to Codex. The Claude decrease does not establish effectiveness for the active agent; per-session normalization does not control for the change in task mix. The earlier conclusion that no tightening is needed is withdrawn. Current original Codex counters provide a descriptive snapshot, but cannot establish a trend or measured token savings. A retrospective audit was subsequently completed below; the earlier assumption that local transcripts could supply a previous-week baseline was not supported by the inventory.

## Limits
Counts are command-text heuristics, not measured token savings or causal proof. A Codex functions.exec wrapper with multiple nested calls receives one category; keyword priority can hide reads, and literal mentions can create false positives. Relative paths and some Python/resource reads are missed. Full KiB uses present file sizes, not historical returned bytes. Session counts include classified KB-active subagent sessions. Agent/workload changes and overlapping rolling windows limit comparison.

## Changes
Saved the fresh usage snapshot and this evidence note; closed the dated comparison reminder in the central TODO. No repositories, external services, or agent rules changed.

## Portable lesson
None; effectiveness for Codex remains unverified.

## Corrected Codex retrospective audit

Requested by the user after clarifying the switch to Codex. Static analysis covers local active and archived transcripts. Two complete Moscow calendar windows were selected: September 30–October 6 and October 7–13, with UTC boundaries September 29 21:00, October 6 21:00 and October 13 21:00. The ongoing October 14 session is excluded.
No transcript events are present in the earlier window. This means missing local comparison history, not proof of zero actual usage.

| October 7–13 metric | Count |
| --- | ---: |
| Tool-active sessions | 127 |
| Sessions with recognized KB access | 101 |
| Sessions with requested full reads | 14 |
| Requested full note reads / full shell calls | 17 / 17 |
| Unique full-read note paths | 14 |
| Partial note reads | 292 |
| Search commands over AI paths | 646 |
| Actual literal kb_find invocation sites | 242 |
| INDEX reads | 1 |
| Sum of current full-note file sizes | 256475 bytes / 250.46 KiB |

Per KB-active session: 0.1683 full reads, 2.8911 partial reads, 2.48 KiB full-size proxy. Per tool-active session: 0.1339 full reads, 2.2992 partial reads, 1.97 KiB proxy. Full reads include verification of just-written notes; these counts do not establish unnecessary reading.

The original classifier on identical bounds counted 18 wrappers as full reads and 27 note-path mentions, with a size proxy of 603676 bytes / 589.53 KiB. These are different counting units, not evidence of behavior changing. The corrected extractor parses JS syntax with Acorn without executing transcript code, extracts nested static shell calls, splits shell commands and handles cwd/cd, pipelines, comments and heredoc bodies.

Coverage: 5438 wrappers; 7567 syntactic exec_command sites; 7452 static invocations recovered; 115 dynamic sites unresolved; 3 wrapper parse failures. Of the exclusions, 26 unresolved sites and one parse failure occur in wrappers mentioning knowledge-base paths. Five regression fixtures passed, including a reproduced-and-fixed semicolon/newline boundary failure. The root agent independently reran the fixtures and cross-checked original-classifier counts.

Additional limits: counts represent static requested reads, without success/output matching. Function bodies/conditional branches can overcount and loops can undercount; custom Python readers and dynamic paths can be missed. Conservative exclusion of output redirection can omit legitimate file reads. Current file sizes are neither historical returned bytes nor token usage. Sessions include subagents. Exact totals and token savings are not established.

### Artifacts and next measurement

- Reusable audit: `/home/slnnk/ai-data/token-cost/audit.py`, `extract.js`, `test_audit.py`.
- Aggregates: `/home/slnnk/ai-data/token-cost/audit.json`, `daily/audit.json`, `report.txt` (no raw commands or transcript bodies saved).
- Canonical `general/scripts/token_usage.py` was not modified; its original wrapper-classification limitations remain. The independent audit is used for this comparison.
- Repeat on October 21: `python3 /home/slnnk/ai-data/token-cost/audit.py --end-date 2026-10-21 --output /home/slnnk/ai-data/token-cost/2026-10-21`, comparing October 7–13 with October 14–20.

Conclusion: this supplies a corrected current baseline for Codex. No previous-week trend or causal effectiveness claim is justified. Reading-rule changes are deferred pending comparable Codex evidence. Future actions are tracked only in the central TODO.
