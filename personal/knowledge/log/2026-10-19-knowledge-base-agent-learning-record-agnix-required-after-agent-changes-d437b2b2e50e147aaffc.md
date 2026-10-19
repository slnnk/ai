---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: agnix-required-after-agent-changes

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T20:29:20.567953+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Before final response after changing agent instructions, skills including references/scripts, or settings, run agent_lint.py --force with additional repository-local paths as needed, review findings and report results or pending failure. Normal ai-sync runs a change-aware fallback before daily Git skip; no auto-fix or new external permissions.",
  "key": "agnix-required-after-agent-changes",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T20:29:20.567953+00:00",
      "cause": "",
      "event_id": "0bfabf80-f159-4d1b-8c24-44132a5423be",
      "expected": "Before final response after changing agent instructions, skills including references/scripts, or settings, run agent_lint.py --force with additional repository-local paths as needed, review findings and report results or pending failure. Normal ai-sync runs a change-aware fallback before daily Git skip; no auto-fix or new external permissions.",
      "source": "User request 2026-10-19: Сделай сразу и обязательную и через синхронизацию.",
      "summary": "User chose mandatory report-only agnix after instruction/skill/settings edits plus change-aware ai-sync fallback; supersedes personal optional pilot mode."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "global",
  "summary": "User chose mandatory report-only agnix after instruction/skill/settings edits plus change-aware ai-sync fallback; supersedes personal optional pilot mode.",
  "system": "knowledge-base",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-10-19T20:29:20.567953+00:00",
  "version": 1
}
```
