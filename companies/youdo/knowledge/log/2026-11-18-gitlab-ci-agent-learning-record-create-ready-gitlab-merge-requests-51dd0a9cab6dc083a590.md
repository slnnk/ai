---
system: gitlab-ci
status: verified
checked: 2026-11-18
tags: [agents, learning]
---
# Agent learning: create-ready-gitlab-merge-requests

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-18T15:05:40.405489+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-18T16:09:25.765961+00:00",
      "cause": "",
      "event_id": "devops-923-monitoring-ready-mr6-20261118",
      "expected": "Propose and create new MRs as Ready. State pending checks and dependencies separately. Existing MR readiness changes require explicit approval.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "current/knowledge/log/2026-11-17-dev-deployment-devops-923-kyc-plan.md#monitoring-template-removal-mr-published-2026-11-18",
      "target": "/home/slnnk/ai/companies/youdo/skills/gitlab-workflow/references/conventions.md"
    }
  ],
  "expected": "Propose and create new MRs as Ready. State pending checks and dependencies separately. Existing MR readiness changes require explicit approval.",
  "key": "create-ready-gitlab-merge-requests",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-18T15:05:40.405489+00:00",
      "cause": "",
      "event_id": "devops-923-no-draft-mrs-20261118",
      "expected": "Propose and create new MRs as Ready. State pending checks and dependencies separately. Existing MR readiness changes require explicit approval.",
      "source": "current/knowledge/log/2026-11-17-dev-deployment-devops-923-kyc-plan.md#user-correction-about-draft-mrs-2026-11-18",
      "summary": "User requires new GitLab MRs to be created without Draft"
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User requires new GitLab MRs to be created without Draft",
  "system": "gitlab-ci",
  "target": "/home/slnnk/ai/companies/youdo/skills/gitlab-workflow/references/conventions.md",
  "task_id": "",
  "updated": "2026-11-18T16:09:25.765961+00:00",
  "version": 1
}
```
