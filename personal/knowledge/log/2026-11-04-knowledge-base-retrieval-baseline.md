---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [search, benchmark, retrieval]
decision_state: superseded
decision_scope: Implementation status after the frozen measurement
decision_summary: The original measurement is retained. Retrieval proposals 1-4 are now implemented; follow the linked current outcome.
decision_date: 2026-11-04
decision_source: 2026-11-04-knowledge-base-retrieval-context-decisions.md#current-outcome
---
# Knowledge retrieval: fixed-question baseline

## Summary

The user selected the retrieval experiment from the agent pilot proposals. On a
frozen corpus of 566 notes, 12 predefined questions and 36 query formulations were
tested in 84 conditions with three sequential repetitions (252 healthy CLI runs).
Exact and English technical queries retrieved the expected note in the top five
for all 12 questions. All 12 short Russian queries returned no matches. Technical
queries ranked the expected note first in 9/12 cases; layer scoping reduced noise
and typical latency but did not improve that count. Default snippets exposed a
preselected answer line for only 6/12 technical queries, a location proxy rather
than proof of a complete answer. Status is visible, but neither recency nor semantic
supersession affects ranking. No search implementation or agent rules were changed.
This is a small synthetic baseline, not a representative user-query evaluation.

## Task

Independently prepare real questions with expected source notes, measure top-five
retrieval, historical-note confusion, output size and latency, and report failure
causes. The user authorized running this local experiment, not implementing a
search engine, installing tools or running infrastructure diagnostics.

## Context and provenance

Original [pilot proposal](2026-10-19-knowledge-base-agent-capabilities-research.md),
step6. The corpus spans general, personal and current company knowledge. A separate
agent selected and read sources and fixed the dataset before any benchmark query
was executed. Questions were derived from known notes rather than real query logs;
this biases the test toward discoverable technical identifiers. Company systems
were not rechecked; this experiment evaluates retrieval of recorded evidence only.

Artifacts outside Git: `~/ai-data/kb-retrieval/2026-11-04/` contains `cases.json`,
`manifest.json`, `results.json`, `summary.json`, and the executed `run_benchmark.py`.
The manifest records every searched note's SHA-256, script and case hashes, Python
and platform versions. It includes 72 general, 46 personal and 448 company notes.
README and INDEX files are excluded by the search tool. Corpus hashes matched
before and after all 252 recorded runs. Raw source contents and raw search snippets
are not copied into artifacts; results retain note paths, status, checked dates,
snippet line numbers, output byte counts and timing. Expected-answer evidence in
the dataset is limited to short inspected nonsecret excerpts.

## Method

Each question has one expected note and three fixed query types: distinctive exact
terms, 2-4 Russian words in a short user-style formulation, and 2-3 English technical
terms. The Russian questions are constructed probes of the language mismatch, not
observed user search logs. Each variant runs with default AND search across all
layers and with `-l` for its known layer. Technical queries additionally run scoped
`--any` as a diagnostic. All calls use `-m 5` and the default `-n 3`; the query set is
never tuned after observing results. No translation or external model is invoked.

Top1/top5 refer to the preselected single target, not judged relevance of every
result. A lower-ranked alternate note can still be useful. MRR@5 is the mean
reciprocal target rank, with missing targets scored zero. Answer-line exposure means
that at least one predefined source line appears in the target's default snippets.
It does not prove completeness or even visibility of the decisive words because
lines are clipped to 160 characters around the first query pattern.

Latency includes Python startup, full file traversal and text processing on this
machine's warm local filesystem. Three repetitions check output determinism and
give a rough latency baseline; they are not independent relevance observations.
The initial harness attempt used a Python method unavailable on the local Python3.8;
it stopped before a complete run and is excluded. The corrected final harness and
all 252 successful runs are retained. No production script was modified.

## Results

| Search mode | Query type | Top1 | Top5 | Answer-line exposure | Median ms | P95 ms | Median output bytes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| default_and | exact | 11/12 | 12/12 | 9/12 | 115.35 | 144.92 | 835.5 |
| default_and | natural | 0/12 | 0/12 | 0/12 | 110.57 | 118.44 | 17.0 |
| default_and | operational | 9/12 | 12/12 | 6/12 | 123.6 | 141.94 | 3043.5 |
| scoped_and | exact | 12/12 | 12/12 | 9/12 | 63.1 | 134.02 | 513.0 |
| scoped_and | natural | 0/12 | 0/12 | 0/12 | 62.91 | 105.69 | 17.0 |
| scoped_and | operational | 9/12 | 12/12 | 6/12 | 62.57 | 126.53 | 835.0 |
| scoped_any | operational | 8/12 | 12/12 | 6/12 | 72.59 | 210.5 | 2448.0 |

The layer is known in advance in scoped conditions. These figures therefore do not
measure an agent's ability to choose the right layer. The median number of matching
notes for technical queries was 8 unscoped, 1.5 scoped AND, and 29.5 scoped ANY. Broader
matching did not improve top-five recall and reduced top-one hits from 9 to 8 while
increasing output volume. It is not an automatic replacement for AND search.

### Per-question technical-query results

All 12 exact and 12 technical queries found their target in the top five, while all
12 Russian formulations returned zero results in both default and scoped modes.
This table shows the default unscoped technical condition; complete formulations,
expected sections and line numbers are in the frozen case dataset.

| ID | Expected source | Technical query | Target rank | Answer line exposed |
| --- | --- | --- | ---: | --- |
| g01 | [java-heap-oom-vs-docker-oomkilled](../../../general/knowledge/elasticsearch/java-heap-oom-vs-docker-oomkilled.md) | `elasticsearch heap OOM` | 1 | yes |
| g02 | [systemd-resolved-route-only-domain-servfail](../../../general/knowledge/linux/systemd-resolved-route-only-domain-servfail.md) | `resolved SERVFAIL` | 1 | yes |
| g03 | [udp-sender-pointed-at-grpc-port-no-spans](../../../general/knowledge/jaeger/udp-sender-pointed-at-grpc-port-no-spans.md) | `jaeger spans port` | 1 | no |
| g04 | [add-apt-repository-gpg-key-timeout](../../../general/knowledge/docker/add-apt-repository-gpg-key-timeout.md) | `ppa key timeout` | 1 | yes |
| g05 | [environment-name-job-only-variables](../../../general/knowledge/gitlab-ci/environment-name-job-only-variables.md) | `environment pipeline suffix` | 1 | no |
| g06 | [default-true-overrides-false](../../../general/knowledge/helm/default-true-overrides-false.md) | `helm false default` | 1 | no |
| k01 | [setup-another-pc](../../../general/knowledge/knowledge-base/setup-another-pc.md) | `knowledge workstation setup` | 1 | no |
| k02 | [2026-09-30-knowledge-base-token-cost-kb-find-summaries](../../../personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md) | `kb_find token summaries` | 1 | yes |
| k03 | [2026-10-19-knowledge-base-skill-evaluation-pilot](../../../personal/knowledge/log/2026-10-19-knowledge-base-skill-evaluation-pilot.md) | `Claude skills access` | 3 | yes |
| c01 | [ci-cd](../../../current/knowledge/systems/android-farm/ci-cd.md) | `android APK Nexus` | 5 | no |
| c02 | [overview](../../../current/knowledge/systems/dev-deployment/overview.md) | `B2B deployment Jenkins` | 2 | yes |
| c03 | [agent-git-workflow](../../../current/knowledge/systems/gitlab-ci/agent-git-workflow.md) | `agent GitLab approvals` | 1 | no |

## Findings

- Literal English technical search is adequate on these selected known-answer cases;
  this experiment does not justify a new database or embedding service.
- The Russian formulations fail because matching is case-insensitive literal substring
  search with AND across patterns, while the target notes are written in English.
  There is no translation, stemming or semantic synonym expansion. A different
  ranking formula alone would not solve this language mismatch.
- Finding a document is easier than exposing its answer. Three snippets are chosen
  from the earliest lines matching any term, not from the most relevant section or
  the conjunction of terms. For Jaeger, GitLab environment variables, Helm false
  values, setup, Android APK flow and Git approvals, the selected answer anchor is
  absent from default technical snippets. Some titles or other lines can still help;
  this is a limited answer-location metric, not a score of response correctness.
- The Android APK delivery target is fifth for `android APK Nexus`; four other
  Android/Nexus notes precede it. Some are useful alternate context, so this does
  not demonstrate four irrelevant results. The target's delivery line is absent.
- The cancelled Claude evaluation target is third for `Claude skills access`.
  The older research note ranks first and still contains historical access-blocked
  statements. The target's cancellation line is among its snippets, but ranking
  does not understand that this later decision supersedes older statements.
- The PPA recipe is first but explicitly marked `outdated` in metadata. The exact
  query does not expose its warning line; the technical query exposes that line
  number, but clipping can omit the beginning containing the reuse warning. No
  safe interpretation by an answering agent was tested. `checked` and `status` are
  displayed but not used by the ranking function. Old dates alone do not prove a
  note is wrong, and an outdated note is the correct target for a reuse-risk question.
- Useful immediate practice is to search with technical identifiers, scope to the
  known layer and inspect the selected section before treating evidence as current.
  This finding is guidance for interpreting this baseline, not a new global rule.

## Changes and checks

Added this result note and preserved the frozen benchmark artifacts. Updated the
original proposal and central TODO to record selection/completion of the baseline;
search improvements remain proposals. An independent agent checked all 12 targets and
answer anchors against source content and reviewed the line-exposure, clipping,
single-target and historical-supersession limitations. All 252 final CLI calls exited
with the expected 0/1 codes, had no stderr and produced deterministic results per
condition. Corpus and search-script hashes were stable throughout execution.

To repeat against the same corpus before later documentation additions, retain
the manifest and use the saved harness. Running against a changed live corpus is a
new measurement, not an exact reproduction of this baseline. The harness refuses
to reuse output directories and detects corpus changes during a run:

```bash
python3 ~/ai-data/kb-retrieval/2026-11-04/run_benchmark.py \
  --cases ~/ai-data/kb-retrieval/2026-11-04/cases.json \
  --out /tmp/kb-retrieval-new-run --repeats 3
```

## Status and risks

Baseline complete on 2026-11-04. No installation, external access, model benchmark,
search modification or infrastructure operation was performed. The small manually
selected sample and constructed queries do not establish overall search quality.
The cancellation case is intentionally retained to check history interpretation; it
does not reopen the cancelled Claude evaluation. Potential snippet/language
improvements and further pilot selection are tracked only as proposals in the
[central TODO](../../../TODO.md); this experiment grants no implementation permission.

## Portable lesson

none

## Query preparation adopted (2026-11-04)

The user subsequently authorized only proposal1: agent-side preparation of
search terms, layer selection and bounded empty-query reformulation. The
[implementation record](2026-11-04-knowledge-base-query-preparation.md) links the
canonical AGENTS/README procedure. This supersedes the earlier statement that
no agent rules were changed only for this later action; the baseline measurement
and its frozen artifacts remain unchanged. No snippet, ranking, lifecycle-status
or search-engine changes were implemented. Remaining proposals are in central TODO.
