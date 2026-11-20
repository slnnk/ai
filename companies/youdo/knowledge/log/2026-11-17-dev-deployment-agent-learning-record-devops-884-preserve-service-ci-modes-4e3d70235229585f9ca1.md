---
system: dev-deployment
status: verified
checked: 2026-11-19
tags: [agents, learning]
---
# Agent learning: devops-884-preserve-service-ci-modes

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-17T19:16:08.805340+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-19T10:15:59.077534+00:00",
      "cause": "",
      "event_id": "devops-884-all-services-plan-20261119",
      "expected": "For DevOps-884 preserve DEPLOY_PROD_MODE and existing build/test rules. Use existing manual Helm deploy rules in MR and semver-tag pipelines for manual mode; auto-mode services retain master. Do not add independent all-services master activation.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#context-and-common-changes",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-17-dev-deployment-devops-884-first-ten-assessment.md#ci-mode-decision-user-correction-november17"
    },
    {
      "at": "2026-11-19T11:02:40.804799+00:00",
      "cause": "",
      "event_id": "devops-884-dev-single-bootstrap-prep-20261119",
      "expected": "For DevOps-884 preserve DEPLOY_PROD_MODE and existing build/test rules. Use existing manual Helm deploy rules in MR and semver-tag pipelines for manual mode; auto-mode services retain master. Do not add independent all-services master activation.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#stage-3-diff-prepared-locally",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-17-dev-deployment-devops-884-first-ten-assessment.md#ci-mode-decision-user-correction-november17"
    }
  ],
  "expected": "For DevOps-884 preserve DEPLOY_PROD_MODE and existing build/test rules. Use existing manual Helm deploy rules in MR and semver-tag pipelines for manual mode; auto-mode services retain master. Do not add independent all-services master activation.",
  "key": "devops-884-preserve-service-ci-modes",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-17T19:16:08.805340+00:00",
      "cause": "",
      "event_id": "devops884-20261117-ci-mode-correction",
      "expected": "For DevOps-884 preserve DEPLOY_PROD_MODE and existing build/test rules. Use existing manual Helm deploy rules in MR and semver-tag pipelines for manual mode; auto-mode services retain master. Do not add independent all-services master activation.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-17-dev-deployment-devops-884-first-ten-assessment.md#ci-mode-decision-user-correction-november17",
      "summary": "User selected existing service CI modes; dev deployment belongs in release-tag pipelines for manual mode."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User selected existing service CI modes; dev deployment belongs in release-tag pipelines for manual mode.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-17-dev-deployment-devops-884-first-ten-assessment.md#ci-mode-decision-user-correction-november17",
  "task_id": "DevOps-884",
  "updated": "2026-11-19T11:02:40.804799+00:00",
  "version": 1
}
```
