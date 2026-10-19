---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: deterministic-todo-output

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T20:42:24.917802+00:00",
  "decisions": [
    {
      "at": "2026-10-19T20:49:05.122150+00:00",
      "decision": "adopted",
      "expected": "For todo or задачи, return all open tasks in source order as concise Russian descriptions in ordinary bullet lists with Russian headings; omit dates, source references and checkboxes. Use source-keyed cached descriptions; preserve pending actions, IDs, deferrals and permission limits.",
      "revision": 2,
      "source": "Current Codex user correction: Russian descriptions, no dates, src or checkboxes, ordinary bullet lists.",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-10-19T20:52:32.628298+00:00",
      "decision": "adopted",
      "expected": "For todo or задачи, return all open tasks in order as short Russian action titles, typically 6-12 words and no more than 120 characters, with no blank lines between items in a group. Omit dates, source links and checkboxes; preserve useful IDs and deferral/proposal labels. Use source-keyed cached titles; keep full details and permission conditions in source TODO.",
      "revision": 3,
      "source": "Current Codex correction with screenshot: descriptions still too long, output slow, large spaces between tasks.",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
  "evaluations": [],
  "expected": "For todo or задачи, return all open tasks in order as short Russian action titles, typically 6-12 words and no more than 120 characters, with no blank lines between items in a group. Omit dates, source links and checkboxes; preserve useful IDs and deferral/proposal labels. Use source-keyed cached titles; keep full details and permission conditions in source TODO.",
  "key": "deterministic-todo-output",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T20:42:24.917802+00:00",
      "cause": "",
      "event_id": "codex-20261019-todo-output-trigger-1",
      "expected": "For todo or задачи and backlog-list requests, run general/scripts/todo.py and return complete Markdown stdout without rewriting, translation, extra commentary or truncation. Default to all open tasks in file order; use filters only for an explicitly requested subset. Listing does not authorize task execution.",
      "source": "User request in current Codex session, 2026-10-19: Реализуй. Я хотел бы получать ответ по простому запросу todo или задачи.",
      "summary": "User requested standardized TODO output through the short requests todo or задачи."
    },
    {
      "agent": "codex",
      "at": "2026-10-19T20:49:05.286951+00:00",
      "cause": "",
      "event_id": "codex-20261019-todo-russian-bullets-1",
      "expected": "For todo or задачи, return all open tasks in source order as concise Russian descriptions in ordinary bullet lists with Russian headings; omit dates, source references and checkboxes. Use source-keyed cached descriptions; preserve pending actions, IDs, deferrals and permission limits.",
      "source": "Current Codex user correction: descriptions must be Russian; dates, src and checkboxes are unnecessary; use ordinary bullet lists.",
      "summary": "User requested standardized Russian TODO descriptions without dates, source references or checkboxes."
    },
    {
      "agent": "codex",
      "at": "2026-10-19T20:52:32.763088+00:00",
      "cause": "",
      "event_id": "codex-20261019-todo-compact-spacing-1",
      "expected": "For todo or задачи, return all open tasks in order as short Russian action titles, typically 6-12 words and no more than 120 characters, with no blank lines between items in a group. Omit dates, source links and checkboxes; preserve useful IDs and deferral/proposal labels. Use source-keyed cached titles; keep full details and permission conditions in source TODO.",
      "source": "Current Codex correction with screenshot: descriptions still too long, output slow, large spaces between tasks.",
      "summary": "User requested compact Russian TODO titles and tight bullet spacing."
    }
  ],
  "repo": "",
  "revision": 3,
  "scope": "global",
  "summary": "User requested compact Russian TODO titles and tight bullet spacing.",
  "system": "knowledge-base",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-10-19T20:52:32.763088+00:00",
  "version": 1
}
```
