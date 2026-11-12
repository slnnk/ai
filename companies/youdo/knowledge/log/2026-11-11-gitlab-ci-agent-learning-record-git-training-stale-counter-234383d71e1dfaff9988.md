---
system: gitlab-ci
status: verified
checked: 2026-11-11
tags: [agents, learning]
---
# Agent learning: git-training-stale-counter

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-11T17:32:43.323765+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Reconcile the training counter from linked publication records; keep the comparison pending and do not interpret an unchanged counter as absence of published tasks.",
  "key": "git-training-stale-counter",
  "kind": "fact",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-11T17:32:43.323765+00:00",
      "cause": "Publication evidence was recorded in task logs but not reconciled into the aggregate counter.",
      "event_id": "git-training-counter-20261111-user-correction",
      "expected": "Reconcile the training counter from linked publication records; keep the comparison pending and do not interpret an unchanged counter as absence of published tasks.",
      "source": "/home/slnnk/ai/current/knowledge/systems/gitlab-ci/agent-git-workflow.md#five-task-follow-up-approved-on-november-4",
      "summary": "User challenged stale 0/5 despite multiple published MRs; existing logs establish at least six distinct tasks after November 4."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User challenged stale 0/5 despite multiple published MRs; existing logs establish at least six distinct tasks after November 4.",
  "system": "gitlab-ci",
  "target": null,
  "task_id": "",
  "updated": "2026-11-11T17:32:43.323765+00:00",
  "version": 1
}
```
