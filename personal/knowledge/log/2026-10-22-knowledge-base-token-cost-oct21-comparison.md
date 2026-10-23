---
system: knowledge-base
status: verified
checked: 2026-10-22
tags: [token-cost, codex, review]
---
# Knowledge base: October 21 scheduled Codex cost comparison

## Task
Execute the October 21 reminder: compare Codex October 7–13 with October 14–20, normalize KB reads and file-size proxies, report parser coverage, and decide whether reading rules need adjustment. Requested on October 22; measurement windows remain unchanged.

## Context
[Original baseline and methodology](2026-10-14-knowledge-base-token-cost-comparison.md).
[Regular accounting update](2026-10-19-knowledge-base-codex-nested-shell-accounting.md).
[Central backlog](../../../TODO.md), Knowledge base / Token cost optimization.
The audit uses active and archived local Codex transcripts, including subagents. Both periods were recomputed in one run against the same current filesystem.

## Actions
Ran the existing fixed-window audit, without changing scripts or agent rules:

```bash
PYTHONPATH=/home/slnnk/ai/general/scripts python3 /home/slnnk/ai-data/token-cost/audit.py --end-date 2026-10-21 --output /home/slnnk/ai-data/token-cost/2026-10-21
python3 -m unittest discover -s /home/slnnk/ai-data/token-cost -p test_audit.py -v
```
The initial invocation lacked PYTHONPATH and failed importing token_usage_kb after the October 19 module split. Supplying the existing script directory resolved the import; no script patch was needed. Five audit regression tests passed.
Artifacts: `/home/slnnk/ai-data/token-cost/2026-10-21/audit.json` from the audit, plus a concise `report.txt` written from its aggregates. These contain aggregates and note paths, not raw transcript bodies.
UTC boundaries: October 6 21:00, October 13 21:00, October 20 21:00; exclusive Moscow midnights define the two complete calendar weeks. Scanned 518 transcript files.

## Findings

| Metric | October 7–13 | October 14–20 |
| --- | ---: | ---: |
| Tool-active sessions | 127 | 178 |
| KB-active sessions | 101 | 152 |
| Sessions with full reads | 14 | 30 |
| Full file reads | 17 | 49 |
| Partial file reads | 292 | 439 |
| Full shell calls | 17 | 48 |
| Unique full-read note paths | 14 | 22 |
| kb_find invocation sites | 242 | 327 |
| Search commands | 646 | 1098 |
| INDEX reads | 1 | 0 |
| Current full-file size proxy, bytes | 480679 | 1212737 |
| Current full-file size proxy, KiB | 469.41 | 1184.31 |

| Normalized metric | October 7–13 | October 14–20 | Change |
| --- | ---: | ---: | ---: |
| Full reads / KB-active session | 0.1683 | 0.3224 | +91.52% |
| Partial reads / KB-active session | 2.8911 | 2.8882 | -0.10% |
| Full-size KiB / KB-active session | 4.6477 | 7.7915 | +67.64% |
| Full reads / tool-active session | 0.1339 | 0.2753 | +105.65% |
| Partial reads / tool-active session | 2.2992 | 2.4663 | +7.27% |
| Full-size KiB / tool-active session | 3.6962 | 6.6534 | +80.01% |

Tool-active workload grew 40.16%, and KB-active sessions grew 50.50%. Partial reads grew almost exactly in proportion to KB-active sessions. Full reads grew faster; a simple session-count adjustment does not remove that increase.

### Concentration and interpretation
README full reads increased 2 to 20; company repos.md increased 3 to 8. Together these two existing reference files account for 28/49 second-week full reads and 1085520/1212737 bytes (89.51%) of its current-size proxy. Their first-week totals were 5/17 reads and 249528/480679 bytes (51.91%). They account for 23 of the 32 additional full reads; all other notes total 12 then 21 full reads. Requested whole-file reads alone do not prove unnecessary reading: verification of edits and reference maintenance also occur in these windows.

The earlier saved baseline reported 250.46 KiB for the same 17 first-week reads. Recomputed current-size baseline is 469.41 KiB because referenced files have changed. Comparing the old saved byte total directly with the new second-week proxy would be invalid. Both columns above use the same present file sizes, which still do not reconstruct historical outputs. In particular, README and repos.md are living reference files.

### Parser coverage

| Metric | October 7–13 | October 14–20 |
| --- | ---: | ---: |
| JS wrappers | 5438 | 7924 |
| Wrapper parse failures | 3 | 9 |
| Syntactic exec_command sites | 7567 | 10806 |
| Recovered static shell invocations | 7452 | 10745 |
| Recovery / syntactic sites | 98.480% | 99.435% |
| Unresolved dynamic sites | 115 | 61 |
| Unresolved sites in KB-mention wrappers | 26 | 11 |
| Parse failures in KB-mention wrappers | 1 | 4 |
| Empty or failed shell parsing | 5 | 0 |

Recovery percentage is conditional on syntactic sites in successfully parsed JS; it is not overall recall. Failed wrappers and unsupported readers remain outside that percentage. No second-week INDEX read was recognized, rather than proven absent.

## Decision and limits
Measured KB access does not show reduced full reading for Codex across these weeks. Actual token savings, monetary expense and causal effects of rules remain unestablished. Counters represent statically requested accesses, without success/output matching; current bytes are not historical returned bytes or tokens. Dynamic paths/custom readers can be missed; branches can overcount and loops undercount. Session counts include subagents, and task mix and conversation length differ. Native token_usage.py CLI provides rolling session-based totals, not fixed-calendar event totals, so those totals were not substituted for the scheduled comparison.

Do not add or tighten reading rules from this result: existing instructions already require scoped search and selected sections. Apply those existing requirements to README and select only needed repository-registry rows. The concentration identifies the first place to check in later measurements, but does not establish a new rule or authorize implementation. No additional scheduled comparison is created. The original reminder is completed with these results, rather than left open awaiting causal proof.

## Changes and status
Saved this report and generated audit artifacts, linked the follow-up from the original baseline, and closed the October 21 reminder on October 22. No script, agent instruction, service or repository task changes. Five audit regression tests passed; KB lint: 0 errors, 0 warnings. Closed-reminder query returns no open matches. Knowledge indexes rebuilt after the report update.

## Portable lesson
None; this is local usage evidence with workload-dependent limits.
