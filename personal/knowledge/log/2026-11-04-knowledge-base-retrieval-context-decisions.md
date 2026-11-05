---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [retrieval, search, benchmark, decisions]
---
# Knowledge retrieval: section context, scoped decisions and regression checks

## Summary

The user authorized proposals 2-4: section-context search excerpts, explicit scoped
decisions with source references, and reusable retrieval regression checks. Search
matching and document ranking are preserved. Verification passed: 23 tests and 72-condition comparison with no lost targets,
answers or required decisions at the new default context budget. Historical benchmark artifacts
are retained; existing unrelated KB changes are preserved.

## Task and authorization

The user requested implementing the remaining retrieval proposals. Before editing
repository code the user explicitly approved reusing `~/ai` main with origin/main
as base and no publication. The user subsequently exempted `~/ai` itself from the
first repository-edit gate. Neither approval authorizes manual KB commits or pushes;
ordinary sync remains the publication mechanism. No external operations requested.

## Context

[Frozen baseline](2026-11-04-knowledge-base-retrieval-baseline.md) and
[query preparation](2026-11-04-knowledge-base-query-preparation.md). The old baseline
counted answer-line exposure, which can overstate actual answer visibility after
clipping. This implementation uses stable text anchors selected independently
before new snippet trials. It does not claim that fixed prepared queries test an
agent's spontaneous translation or rule activation.

## Changes

- `general/scripts/kb_find.py`: fenced-heading-aware section context, coherent
  bounded excerpts, full explicit scoped decisions and `--json`; preserve flags,
  document ranking and path-only output.
- `general/scripts/kb_lint.py`: validate the optional five-field decision block,
  including source heading references and confinement to the KB.
- `general/scripts/kb_benchmark.py`: fixed-query suite runner with stable visible
  anchors, decision checks, baseline comparison and input fingerprints.
- Synthetic regression checks in `general/scripts/tests/`.
- README Knowledge retrieval documents the behavior, decision schema and repeat
  commands. Only known affected sources are annotated: cancelled Claude extension,
  its research summary, restricted PPA recipe and superseded implementation status
  of the frozen baseline. This does not relabel their unrelated recorded evidence.
- Real cases/results remain under `~/ai-data/kb-retrieval/`; no company-specific
  fixture data is added to the portable general layer.

## Decisions

Scoped scalar fields separate human decisions from verified/hypothesis/outdated
evidence status. A mixed report can retain Codex results while its Claude extension
is cancelled. Decisions are explicit and always displayed in full with a source,
not inferred from time or prose. Existing unannotated notes require ordinary reading.
The old English/Russian language mismatch remains handled by agent query preparation.

## Verification

The final live checks passed. Initial trial failures and refinements are
preserved in generated artifacts, not adopted as a passing baseline. Independent
review identified benchmark false-pass risks from missing variants/cases, empty
anchors and mutable suites; these are addressed before adopting the new checker.

## Current outcome

Proposals 1-4 are implemented. All four requested retrieval improvements are
complete. The separate Claude-specific evaluation remains cancelled by the user;
its [source decision](2026-10-19-knowledge-base-skill-evaluation-pilot.md#claude-extension-cancelled-2026-11-04)
is preserved. Other unselected agent pilots remain optional proposals. No deployment, external API writes or publication are part of this
task. Live remaining actions are recorded only in [central TODO](../../../TODO.md).

## Portable lesson

Canonical operation and decision schema are in README Knowledge retrieval.

## Final measurements and review

Same corpus and same fixed queries/anchors were used in both final control and
treatment: 72 conditions each, one execution per condition. The old renderer was
preserved in a one-off JSON adapter; the new renderer ran from its installed path.
The old default is 3 lines/160 characters, the new default is 5 lines/240 characters.
The observed gain includes section/window selection and the larger output budget;
it is not an isolated causal estimate of any single heuristic. Legacy adapter
startup adds overhead, so latency values do not establish a speedup.

| Default technical queries | Legacy default | New default |
| --- | ---: | ---: |
| Expected note in top5 | 12/12 | 12/12 |
| Target ranked first | 9/12 | 9/12 |
| Exact visible answer anchor | 2/12 | 8/12 |
| Required scoped decision with source | 0/2 | 2/2 |

The same counts hold with layer scoping for technical queries. Exact queries
improved from 7/12 to 8/12 visible anchors; Russian literal probes still return 0/12,
as expected without agent-side term preparation. Four technical answer anchors
remain outside the default excerpt; this is a documented retrieval limitation,
not a claim that all questions can be answered from search output alone. The new
numbers cannot be equated with the old baseline's weaker answer-line metric.

The equal-three-line diagnostic found 7/12 technical anchors but lost some earlier
anchors and failed enforcement; it is retained as a failed diagnostic, not adopted
as baseline. The chosen five-line default passes comparison with the legacy control.
This demonstrates why the checker records per-condition regressions rather than
relying only on aggregate gains.

The checker now freezes query, target and answer/decision definitions. It rejects
removed conditions, empty/scalar anchors or query lists, absent enforced variants,
changed inputs during a run and overwritten output directories. Tests include a
visible alternate anchor that must not replace an existing expected answer, plus
line insertions that must not break the stable anchor. Independent review findings
were verified and addressed. Twelve focused new tests plus eleven existing lint
tests pass. No optional model-backed benchmark was run.

Artifacts: `~/ai-data/kb-retrieval/2026-11-04-context-decisions/`. The original
`~/ai-data/kb-retrieval/2026-11-04/` is unchanged. Suite 2 retains legacy line/hash
fields solely as original selection provenance; current matching uses stable
anchors and the executed corpus hashes. The adopted `after-5/results.json` pins
the definitions for future comparisons, and the reusable command is in README.

## Limits and completion

Small known-answer sample, constructed query variants and a heuristic excerpt
selector limit generalization. There is one scoped decision group per note; several
independent decisions must be summarized with an honest scope or linked to separate
decision records. Only known affected sources were annotated; unannotated history
does not acquire an inferred lifecycle status. No architecture change to embeddings,
external search services, model execution, deployment or publication was performed.

Final KB lint: 0 errors/0 warnings. Indexes rebuilt. Agent lint: 0 errors,
1 warning and 2 informational findings with agnix 0.60.3. The warning is
`CDX-CFG-025` at `~/.codex/config.toml:5`, outside task-modified files; no
configuration change was performed. The linter version was updated independently
during this task, so the earlier 0.59.0 compatibility result is not its final report.
The ordinary documented benchmark command also passed after note/TODO bookkeeping:
72 conditions, no regression against the adopted baseline; its results are retained
in `post-bookkeeping/`. All 23 tests and `git diff --check` passed.
No task commands or delegated agents remain running.
No unfinished item from the four retrieval proposals remains; unrelated optional
agent-pilot selection is preserved in the central TODO.
