---
system: knowledge-base
status: verified
checked: 2026-11-05
tags: [agents, learning]
---
# Agent learning: agnix-scoped-accepted-findings

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-03T23:38:00.509487+00:00",
  "decisions": [
    {
      "at": "2026-11-05T14:22:35.288191+00:00",
      "decision": "adopted",
      "expected": "Omit accepted AGM-004/CDX-AG-008 info findings only for the shared root policy, and CDX-CFG-025 warnings for validated default/priority values in scanned Codex config files regardless of agnix version; preserve other values, rules and severities.",
      "revision": 2,
      "source": "User instruction 2026-11-05: make the CDX-CFG-025 exception universal without an agnix version dependency.",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    }
  ],
  "evaluations": [],
  "expected": "Omit accepted AGM-004/CDX-AG-008 info findings only for the shared root policy, and CDX-CFG-025 warnings for validated default/priority values in scanned Codex config files regardless of agnix version; preserve other values, rules and severities.",
  "key": "agnix-scoped-accepted-findings",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-03T23:38:00.509487+00:00",
      "cause": "",
      "event_id": "codex-20261104-agnix-exclusions-request",
      "expected": "Omit accepted AGM-004/CDX-AG-008 info findings only for the shared root policy, and known-version CDX-CFG-025 false positives only for validated default/priority values; retain unrelated files, invalid values and warning/error severities.",
      "source": "User request on 2026-11-04 after the three diagnostics were explained: add lint exceptions so these events do not appear.",
      "summary": "User requested suppressing the three explained agnix findings."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "global",
  "summary": "User requested suppressing the three explained agnix findings.",
  "system": "knowledge-base",
  "target": "/home/slnnk/ai/general/knowledge/README.md",
  "task_id": "",
  "updated": "2026-11-05T14:22:35.288191+00:00",
  "version": 1
}
```
