---
system: knowledge-base
status: verified
checked: 2026-11-18
tags: [graphyfi]
decision_state: cancelled
decision_scope: Graphify adoption in the knowledge base
decision_summary: The user declined adoption after the pilots. Existing retrieval remains in use.
decision_date: 2026-11-19
decision_source: #adoption-decision
---
# Graphyfi adoption request

## Task

The user requested a backlog entry for integrating graphyfi into the knowledge base.

## Context

The request concerns the shared knowledge base and names the tool as `graphyfi`.

## Actions

Checked the backlog and added an open entry under `Knowledge base`.

## Findings

The request specifies the intended integration. Its implementation details remain open.

## Pilot proposal, 2026-11-19

Assumed tool identity: [Graphify](https://github.com/Graphify-Labs/graphify),
distributed as `graphifyy`. The official CLI supports traversing a saved graph
with `query` and `path`. Rich Markdown extraction needs a semantic backend.
The offline `--code-only` mode skips documents. The documented Ollama backend
can run locally. See [supported inputs](https://docs.graphify.com/open-source/features/languages)
and [privacy](https://github.com/Graphify-Labs/graphify#privacy).

Proposed pilot: allowlist 20–30 related Markdown notes on knowledge-base
retrieval, learning, and setup from the personal and general layers, preserving
relative paths. Run the pinned CLI manually with a local Ollama endpoint and
keep scratch outputs outside the repository. Exclude company notes, environment
files, and generated indexes. Compare `kb_find.py` alone with `kb_find.py`
plus Graphify on the same 10 questions. Include ordinary lookups, multi-note
paths, and superseded decisions. Compare correct primary sources, number of
notes opened, and time including indexing separately. Adopt only if the graph
finds additional verified relations or consistently saves reads on multi-note
queries while preserving source accuracy. Verify every proposed relation against
Markdown. If adopted, document manual refresh and setup on another PC.

The user authorized the pilot, paused it during preparation, and resumed it
with the requirement to omit Ollama. See the executed comparison below.

### Proposed run protocol

1. Copy the selected Markdown files into a temporary tree with the original
   layer layout so both arms use the same snapshot. Point `kb_find.py` at
   that tree with its existing `AI_ROOT` override. Before the scored runs,
   record 10 questions and the expected source paths and sections: two
   direct lookups, six multi-note questions, and two superseded decisions.
2. Pin the CLI and model versions. Smoke-test three notes with a known
   connection against a local endpoint, with external model access disabled.
   Check source paths, elapsed time, and memory use. Stop before scaling
   up if the connection cannot be recovered or local resources are insufficient.
3. Run both arms from clean context with the same initial queries and budget.
   Give the second arm access to the saved graph. Record verified source
   coverage, wrong or outdated claims, notes opened, and elapsed time
   per question. Measure graph build time and disk usage separately.
4. Proposed adoption threshold: preserve source accuracy and current
   decisions, and get either an additional verified relevant link or fewer
   source reads on at least two of the six multi-note questions. Summarize
   results per question and keep the compact report in this note.

## Changes

Added one item to [the central backlog](../../../TODO.md#knowledge-base).

## Pilot results, 2026-11-19

Ran Graphify 0.9.112 in a temporary Python environment. The allowlist held
21 Markdown files from the general and personal layers. No Ollama runtime
or model was downloaded or started. Graphify's local structural parser
linked the E03 proposal to its published result in the three-file smoke
test. Codex added 44 section-backed concepts inline for the semantic arm.
Identical concept labels in distinct notes were linked as inferred edges.
No separate model or subagent process was used.

The two Graphify arms interleaved the first distinct source files from
Graphify's BFS and the literal search, starting with the literal result.
All arms had a five-file inspection budget and the same prepared terms.
Ten cases and their required source files were fixed before building the
full graphs. These are retrieval measurements. Rank of the last required
source is a proxy for reading effort. No separate answer-generation run
or blinded grader was used. The current Claude cancellation and E03
completion sources remained available in all arms.

| Arm | Cases with all required sources | Median CLI time |
| --- | ---: | ---: |
| `kb_find.py` | 5/10 | 65 ms |
| `kb_find.py` and explicit Markdown links | 8/10 | 337 ms |
| `kb_find.py` and the graph with Codex concepts | 7/10 | 342 ms |

Structural gains were frontmatter (D1), the setup guide and audit (M3),
and task resumption (M6). The semantic arm kept D1 and M3. For the
retrieval-regression question (M2), both graph arms moved the last required
source from rank two to rank three. Both saved graphs built in about 0.22 s
each and occupied 214–251 kB. This excludes Codex extraction and preparation.

`kb_find.py` intentionally skips `README.md`. In a follow-up sensitivity
check, placing the canonical README first when it matched all prepared
terms brought the normal workflow to 8/10. Rephrasing the setup query as
`another pc` recovered both sources at ranks one and two, bringing that
workflow to 9/10. The normal workflow also gives a direct README path in
the task-resumption implementation note. These follow-up checks are
exploratory. The gain against bare literal search does not establish a
benefit against the workflow that already loads canonical instructions.
The Codex semantic pass did not improve the structural result.

Recommendation: keep the current retrieval workflow for routine work.
Retain the structural option for a future bounded test on systems with
real cross-note navigation misses. No Graphify hook, MCP server, persistent
install or sync step was added.

The private replay archive is
`~/ai-data/graphify-pilot/2026-11-19-replay.tar.gz` (88 KiB allocated).
It contains the frozen corpus and queries, annotations, pinned Python
dependencies, runner and results. After extracting into a temporary
directory, install `requirements.txt` into a Python 3.12 venv at
`venv`, then run `venv/bin/python build.py` with `smoke`, `structural`
and `semantic`, followed by `compare.py`, `scope_check.py` and
`rephrase.py` with the same interpreter. The archive preserves the
initial pilot evidence.

### Larger-sample proposal

Keep the first 10 questions for a paired comparison on the original
21-note snapshot and the larger general and personal corpus. The two
layers currently contain 221 notes excluding README and generated
indexes. Include canonical README through the ordinary context workflow
in both arms. Add 20 new questions with preset source sections on the
larger corpus, emphasizing operational links among decisions, subsequent
verification and current guidance. Give both arms the same query reformulation
and five-source budget. Compare normal retrieval with normal retrieval plus
the explicit-link graph. Record full source coverage, candidate ranks,
latency, and losses on direct lookups and superseded decisions. This would
test scale separately from whether the original questions generalize.
The user authorized the expanded run with `Запускай`.

### Expanded results, 2026-11-19

Compared the archived 21-file snapshot with all 221 current general and
personal notes plus the canonical README (222 Markdown files). Excluded
generated indexes. Froze the original ten questions and 20 new questions
with two fixed query formulations each, source paths and, for the new
questions, section locations. The new cases were four direct lookups,
12 chains and four current-status lookups. Both arms included README
when relevant and shared the same five-source limit. The Graphify arm
kept the first two ordinary results and interleaved graph candidates
with the remaining ordinary candidates. Used Graphify 0.9.112 with its
local Markdown parser and no Ollama or semantic model.

| Questions and corpus | Ordinary search | Ordinary search plus graph |
| --- | ---: | ---: |
| Ten original, 21 files | 10/10 | 10/10 |
| Ten original, 222 files | 10/10 | 8/10 |
| Twenty new, 222 files | 19/20 | 19/20 |

The metric is all expected source files in the first five. It does not
measure answer generation. The new-case results break down as 4/4 direct,
11/12 chains, and 4/4 status for both arms. Graphify shortened no complete
source list on the new questions. At the larger scale it pushed daily
agnix update evidence and the retained retrieval-work evidence for the
Claude cancellation outside the first five on two original questions.

Both arms missed the original capability-inspection example on the new
M02 question. A post-run exact-endpoint path check confirmed a two-hop
connection. The graph contained a path, but the tested query did not put
the needed source in the inspection budget. This diagnostic did not
change the score.

The large graph had 192 cross-file reference edges, compared with 23 in
the small graph. Cold large-graph build was 1.45 s and the JSON was
1.55 MB. On new questions median CLI time rose from 187 ms to 652 ms,
including process startup. The replay reproduced all 40 source rankings
and graph sizes. This comparison supports leaving everyday retrieval as
it is. The results apply to this corpus, question set and ranking strategy.

The private expanded replay archive,
`~/ai-data/graphify-pilot/2026-11-19-expanded-replay.tar.gz` (604 KiB allocated),
preserves both frozen corpora, the source-section rubric, manifest, pinned
dependencies, runner and both results. Extract into a temporary directory,
install `requirements.txt` in a Python 3.12 venv and run `expanded.py`
with its interpreter. The archive is retained as reproducible evidence
for the adoption decision.

### Markdown linkage inspection

Inspected the three incomplete graph queries in the expanded replay.
In M02 the implementation note names P0.1 in prose and reaches the
original example through a learning record. A direct link to the C01
section would make that relationship available in one hop. In M5 the
lint-enforcement note points to its initial pilot. The daily-update note
links to accepted exceptions. Neither file directly links to the other.
In S1 the retrieval outcome already links to the Claude cancellation.
The existing link did not bring the outcome note into the graph
candidates. The three cases therefore include both indirect or absent
links and a selection miss despite a direct link.

A possible follow-up is a small change to a disposable copy: add direct
links on the first two cases, hold the query and ranking fixed, and keep
the third case as a control for ranking. The saved results are enough
to identify these hypotheses. The user authorized the edited-case comparison.

### Two-link trial, 2026-11-19

Rebuilt both 222-file graphs from the frozen corpus with Graphify
0.9.112. Reproduced the archived ranks for M5, M02 and S1 in the
unmodified arm. In the disposable copy, linked the decision-example
implementation directly to P0.1 C01 and the agnix enforcement note to
the daily update verification. Verified that exactly those two files
changed and Graphify extracted both edges. Cross-file reference edges
rose from 192 to 194. The P0.1 path shortened from two hops to one.

Reused the same queries, candidate interleaving and five-source budget.
The ordinary and graph candidate orders were identical before and after
for all three questions, including the unchanged S1 control. Neither
added link recovered the missing source through the tested query.
This checks two specific links and one query strategy. Both links are
available for direct navigation between known sources.

The private `~/ai-data/graphify-pilot/2026-11-19-links-trial.tar.gz`
(4 KiB allocated) contains the script and results. Extract it alongside
the expanded replay archive in a fresh temporary directory and use the
same venv to run `links_trial.py original` and `links_trial.py edited`.
Only this task note was changed in the live knowledge base.

## Status and risks

Both pilots and the two-link trial are complete. See the adoption decision
below for the closing status. No background operations remain.

## Adoption decision

On 2026-11-19 the user declined integrating Graphify into the knowledge
base after reviewing the expanded pilot and two-link trial. The existing
retrieval workflow stays in use. The [backlog item](../../../TODO.md#knowledge-base)
is closed with adoption declined. The pilot results and replay archives
remain as evidence. There is no outstanding implementation.

## Portable lesson

none

## Task metrics: knowledge-base-graphyfi

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "knowledge-base-graphyfi",
  "created": "2026-11-19T00:51:27.212677+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "experiment",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Expanded replay reproduced all 40 rankings. Two-link trial verified two added edges, shorter P0.1 path, and unchanged candidate orders.",
  "updated": "2026-11-19T01:01:48.800064+03:00"
}
```
