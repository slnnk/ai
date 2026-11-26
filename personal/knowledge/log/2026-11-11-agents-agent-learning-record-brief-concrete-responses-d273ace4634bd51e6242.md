---
system: agents
status: verified
checked: 2026-11-25
tags: [agents, learning]
---
# Agent learning: brief-concrete-responses

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-11T17:55:29.677180+00:00",
  "decisions": [
    {
      "at": "2026-11-24T22:57:34.303574+00:00",
      "decision": "adopted",
      "expected": "Keep user-facing replies brief and concrete. For each reported remaining action name the owner and concrete next step. State exactly what the user must do or decide when needed; when the agent owns the step, say when it will act and explicitly state when no user action is needed.",
      "revision": 2,
      "source": "November 25 conversation on the two pending learning checks: user explicitly requested concrete next actions in every handoff.",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
  "evaluations": [],
  "expected": "Keep user-facing replies brief and concrete. For each reported remaining action name the owner and concrete next step. State exactly what the user must do or decide when needed; when the agent owns the step, say when it will act and explicitly state when no user action is needed.",
  "key": "brief-concrete-responses",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-11T17:55:29.677180+00:00",
      "cause": "",
      "event_id": "discussion-learning-20261111-brief-concrete-responses",
      "expected": "Keep user-facing replies brief and concrete; state the result and only material limitations or required next actions.",
      "source": "User decision 2026-11-11 in current discussion: continuous learning, repository artifacts, YouTrack comments, confirmations retained; review November 20.",
      "summary": "User rejected excessive unnecessary information and requested concrete answers."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "global",
  "summary": "User rejected excessive unnecessary information and requested concrete answers.",
  "system": "agents",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-11-24T22:57:34.303574+00:00",
  "version": 1
}
```
