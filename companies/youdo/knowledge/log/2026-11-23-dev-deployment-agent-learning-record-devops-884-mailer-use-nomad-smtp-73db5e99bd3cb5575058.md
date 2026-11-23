---
system: dev-deployment
status: verified
checked: 2026-11-23
tags: [agents, learning]
---
# Agent learning: devops-884-mailer-use-nomad-smtp

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-23T19:05:22.197719+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-23T20:19:53.746631+00:00",
      "cause": "",
      "event_id": "devops-884-mailer-use-nomad-smtp-render-20261123",
      "expected": "Use the existing Nomad test scheduler SMTP endpoint and sender settings in the DevOps-884 mailer values. Do not replace them with a new relay.",
      "outcome": "pass",
      "revision": 2,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#mailer-dev-single-mr-publication-proposal-2026-11-23",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#mailer-reuse-nomad-test-smtp-2026-11-23"
    }
  ],
  "expected": "Use the existing Nomad test scheduler SMTP endpoint and sender settings in the DevOps-884 mailer values. Do not replace them with a new relay.",
  "key": "devops-884-mailer-use-nomad-smtp",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-23T19:05:22.197719+00:00",
      "cause": "",
      "event_id": "devops-884-mailer-use-nomad-smtp-20261123",
      "expected": "Use the existing Nomad test scheduler SMTP endpoint and sender settings in the DevOps-884 mailer values. Do not replace them with a new relay.",
      "source": "User decision in the DevOps-884 discussion on 2026-11-23",
      "summary": "User chose the existing Nomad test SMTP settings for mailer in dev-single."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "current",
  "summary": "User chose the existing Nomad test SMTP settings for mailer in dev-single.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#mailer-reuse-nomad-test-smtp-2026-11-23",
  "task_id": "DevOps-884",
  "updated": "2026-11-23T20:19:53.746631+00:00",
  "version": 1
}
```
