---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [lint, language, evidence]
---
# Knowledge base language warning audit

## Summary

All five current company-note language warnings are exact source evidence rather than Russian narrative. Preserve source strings. The linter excludes fenced code but counts inline code as prose. No source-note edits or linter changes were made; correction remains a proposal in the central TODO.

## Findings

| Note | Evidence lines | Classification |
| --- | --- | --- |
| [Appium investigation](2026-08-12-android-farm-appium-147-148.md) | 58, 128, 143, 155-157, 164 | Exact UI labels already in inline code. |
| [Autotest report](2026-08-12-android-farm-autotests-report-3063278.md) | 11, 23, 27, 29-31, 38 | Exact suite options, UI and locator strings, already marked as code. |
| [Vysor investigation](2026-08-12-android-farm-vysor-redmi-note-13-pro-input.md) | 24, 30 | Exact Android setting and navigation labels with English translations; line24 uses quotes rather than inline code. |
| [Suite map](../systems/android-farm/ci-suites.md) | 18-29, 37 | Exact GitLab selectable option values; first column needs consistent inline-code marking and a verbatim header. |
| [Post-deploy autotests](../systems/dev-deployment/post-deploy-autotests.md) | 166, 221 | Exact exception and SPA section labels already in inline code. |

## Cause and proposed correction

`general/scripts/kb_lint.py:64-72` strips fenced code only; the language check at190-193 counts Cyrillic in the remainder, including inline code. Proposed targeted change: exclude Markdown inline code from the language check while retaining checks on surrounding prose; consistently mark the unmarked source labels above. Do not translate evidence or suppress entire files. Meaningful verification should cover inline/fenced evidence and Russian prose that must still warn. No implementation authorized by this audit request.

## Actions, checks and limits

Read only warning excerpts/context and language-check implementation. Parent ran full KB and agent lint: KB0errors/6warnings; agnix9files/0errors/4warnings/2info. No infrastructure actions or repository changes. Source-note line numbers describe the audit snapshot. The central TODO is the only open-work list.

## Subsequent outcome: 2026-10-20

The user explicitly requested both proposed changes. Inline-code evidence is now
excluded from language counts, and the unmarked Vysor setting and suite-map option
values are consistently marked as code. All five audited warnings are resolved;
11 CLI regression tests pass and full KB lint reports 0 errors/0 warnings.
Original source strings and the surrounding-prose check are preserved.
[Implementation and limits](../../../../personal/knowledge/log/2026-10-20-knowledge-base-language-inline-code-fix.md).
The audit's no-implementation statements describe the earlier read-only stage.
