---
system: agents
status: verified
checked: 2026-11-18
tags: [agents, learning]
---
# Agent learning: progress-30s-and-background-status

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-03T22:47:24.189335+00:00",
  "decisions": [
    {
      "at": "2026-11-18T19:29:01.931600+00:00",
      "decision": "adopted",
      "expected": "During long work update progress every 30 seconds. Before finalizing verify and report completion and background status, disclose unknowns, and give check or stop instructions for remaining operations. When blocked on the user, say explicitly that the task is waiting for them, what input, decision or action is needed, and what resumes afterwards.",
      "revision": 2,
      "source": "2026-11-18 user explicitly made the P1.4 handoff correction global after having to ask what to do next. Evidence: personal/knowledge/log/2026-11-14-agents-p14-transfer-protocol.md#approved-scope-and-preflight-on-november-18",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    }
  ],
  "evaluations": [
    {
      "at": "2026-11-12T16:33:39.491500+00:00",
      "cause": "",
      "event_id": "incident3296907-progress-status",
      "expected": "During long work update progress at least every 30 seconds; before final response verify task background commands and agents, state completion and remaining operations, and give check or stop instructions when needed. Disclose unverifiable status.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "current/knowledge/log/2026-11-12-corporate-network-job3296907-vpn-nexus-diagnostics.md",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
  "expected": "During long work update progress every 30 seconds. Before finalizing verify and report completion and background status, disclose unknowns, and give check or stop instructions for remaining operations. When blocked on the user, say explicitly that the task is waiting for them, what input, decision or action is needed, and what resumes afterwards.",
  "key": "progress-30s-and-background-status",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-03T22:47:24.189335+00:00",
      "cause": "",
      "event_id": "01a1a394-d2ec-71b3-b042-951780436e35-progress-30s-20261104",
      "expected": "During long work update progress at least every 30 seconds; before final response verify task background commands and agents, state completion and remaining operations, and give check or stop instructions when needed. Disclose unverifiable status.",
      "source": "Codex session 01a1a394-d2ec-71b3-b042-951780436e35, user request on 2026-11-04 to implement proposal 2 with a 30-second interval.",
      "summary": "User requested implementing explicit progress and completion status, with updates every 30 seconds."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "global",
  "summary": "User requires explicit progress, execution status and handoffs that depend on the user.",
  "system": "agents",
  "target": "/home/slnnk/ai/general/knowledge/README.md",
  "task_id": "",
  "updated": "2026-11-18T19:29:01.931600+00:00",
  "version": 1
}
```
