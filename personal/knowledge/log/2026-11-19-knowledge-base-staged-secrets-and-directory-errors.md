---
system: knowledge-base
status: verified
checked: 2026-11-19
tags: [sync, lint, regression]
---
# Staged secret scanning and knowledge directory failures

## Task

The user authorized implementing F2 and F4 from the
[methodology review](2026-11-05-knowledge-base-agent-methodology-review.md).

## Context

Sync previously limited staged secret checks to Markdown and read the working
copy. Search, lint and index generation could silently skip unavailable inputs.

## Actions

Use NUL-delimited Git paths and read whole changed blobs by object ID from the
index. Check with the existing credential patterns and block exact `.env` paths.
Report only the affected path. A missing object exits 2 before the completion
summary, which stops sync before publication. Read UTF-8 and BOM-marked UTF-16
or UTF-32. Gitlinks carry no file content, and archives are not unpacked.

Search, local lint, index generation and sync preview now expose errors from
directory traversal. A missing explicitly requested layer or an unavailable
configured layer fails. Absent optional default layers can be skipped when
other layers are configured. Index generation reads every selected layer before
writing any index.

## Findings

In an isolated fixture, Gitleaks v8.30.1 found a synthetic token in the full
staged Python blob (configured findings exit 10). It returned 0 for the staged
diff and working copy and 1 for an invalid directory target. The release archive
was verified by SHA-256 and used only for the fixture. Its existing published
[scan modes](https://github.com/gitleaks/gitleaks#commands) support full input via
stdin. Reusing the built-in rules meets the format-coverage requirement without
adding a runtime dependency. This comparison did not assess rule quality.

The 72-condition retrieval suite reported the same failure against the saved
baseline for both the pre-change and changed scripts. Case
`k03/operational/default_and` lost target, answer visibility and decision
visibility in both runs. The baseline was retained.

## Changes

Updated `kb_lint.py`, `kb_find.py`, `build_index.py`, sync and sync preview.
Added CLI regressions for partial staging, non-Markdown formats, failed Git
reads, unavailable paths and valid empty directories.

## Status and risks

F2 and F4 are complete locally and closed in the [central TODO](../../../TODO.md).
All 144 script tests passed, including a nested directory permission failure.
An isolated Git index with 14 task files had zero credential findings. KB and
agent instruction lint reported no findings, and generated indexes are current.
The scanner covers known patterns in changed blobs. It does not audit unchanged
files or Git history. The existing retrieval baseline discrepancy is outside the
directory-error change.

## Portable lesson

none

## Task metrics: kb-f2-f4-20261119

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "kb-f2-f4-20261119",
  "created": "2026-11-19T01:10:21.493431+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Task log records authorized F2/F4, isolated staged and directory checks, and baseline comparison.",
  "updated": "2026-11-19T01:10:21.493481+03:00"
}
```
