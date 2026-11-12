---
system: youtrack
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: youtrack-comment-review

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-11T17:55:29.957350+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-12T16:41:14.803521+00:00",
      "cause": "User rejected local-check details and MR sentence in the first draft, introducing task-specific formatting preferences. Corrected draft was approved and exact posted comment plus dedicated MR field independently verified; original corrected first attempt remains fail, recovered final not rescored.",
      "event_id": "DevOps-921-comment-first-attempt",
      "expected": "Read issue context and applicable preferences, prepare the exact concise Markdown draft, check facts and relevant MR URLs, obtain explicit posting/update confirmation, verify readback and record original/final wording plus applicable outcomes.",
      "outcome": "fail",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-android-farm-devops-921-apk-http-errors.md",
      "target": "/home/slnnk/ai/companies/youdo/CONTEXT.md"
    },
    {
      "at": "2026-11-12T17:17:20.906238+00:00",
      "cause": "Initial draft omitted problem description; user requested its addition. Revised exact text was approved and posted/readback verified. Keep original corrected attempt fail; recovered final not rescored.",
      "event_id": "DevOps-922-comment-first-attempt",
      "expected": "Read issue context and applicable preferences, prepare the exact concise Markdown draft, check facts and relevant MR URLs, obtain explicit posting/update confirmation, verify readback and record original/final wording plus applicable outcomes.",
      "outcome": "fail",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-android-farm-devops-922-wait-source-job.md",
      "target": "/home/slnnk/ai/companies/youdo/CONTEXT.md"
    }
  ],
  "expected": "Read issue context and applicable preferences, prepare the exact concise Markdown draft, check facts and relevant MR URLs, obtain explicit posting/update confirmation, verify readback and record original/final wording plus applicable outcomes.",
  "key": "youtrack-comment-review",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-11T17:55:29.957350+00:00",
      "cause": "",
      "event_id": "discussion-learning-20261111-youtrack-comment-review",
      "expected": "Read issue context and applicable preferences, prepare the exact concise Markdown draft, check facts and relevant MR URLs, obtain explicit posting/update confirmation, verify readback and record original/final wording plus applicable outcomes.",
      "source": "User decision 2026-11-11 in current discussion: continuous learning, repository artifacts, YouTrack comments, confirmations retained; review November 20.",
      "summary": "User prioritized learning YouTrack task-comment content and formatting while retaining confirmation."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User prioritized learning YouTrack task-comment content and formatting while retaining confirmation.",
  "system": "youtrack",
  "target": "/home/slnnk/ai/companies/youdo/CONTEXT.md",
  "task_id": "",
  "updated": "2026-11-12T17:17:20.906238+00:00",
  "version": 1
}
```
