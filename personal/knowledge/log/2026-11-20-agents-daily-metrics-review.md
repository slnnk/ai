---
system: agents
status: verified
checked: 2026-11-20
tags: [metrics, review]
---
# Daily agent metrics review for November 20

## Findings

The snapshot for November 19 has SHA-256 `450c2d2e356044551f917cd47b41557cfe7a45992e8af000a13fb3a502b603a4`. It contains 10 changed and closed task records out of 41 recorded. Three of 10 first results were pass and seven were unknown. All 10 final results were recorded as pass. All 12 rule events were recorded as pass with the rule loaded. Several events came from one work log.

[E03](2026-11-19-agents-e03-partial-tool-failures.md#findings) scored three of three in each arm on synthetic transcripts, so it provided no measured advantage for the tested guidance. The [staged secret and directory checks](2026-11-19-knowledge-base-staged-secrets-and-directory-errors.md#findings) reproduced fixture behavior in isolation. The [review tools discussion](2026-11-19-agents-memory-and-design-review-tools.md#changes-and-status) recorded the boundary between discussion and adoption and later documented the approved standing review trigger.

## Actions

Keep the existing permission and verification rules. The broader learning comparison remains under its existing November 20 backlog item. This slice supplies no basis for a new rule or trend claim.

## Limits

Corrections, unnecessary actions, critical events, attributable tokens and active time each had zero assessments out of 10 eligible tasks. Company examples were counted from snapshot metadata. Repeated events and changed records cannot be counted as independent trials. Usage was 86 Codex sessions, 930.4M input tokens including 920.4M cache reads, and 2.2M output tokens across a separate rolling seven-day cohort. Coverage outside recorded tasks is unknown.
