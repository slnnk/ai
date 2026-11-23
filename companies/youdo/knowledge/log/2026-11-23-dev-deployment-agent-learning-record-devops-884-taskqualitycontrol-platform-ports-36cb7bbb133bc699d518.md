---
system: dev-deployment
status: verified
checked: 2026-11-23
tags: [agents, learning]
---
# Agent learning: devops-884-taskqualitycontrol-platform-ports

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-23T16:46:44.753901+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Use a Nomad task ports list with a group-level network port mapping to 80 and keep the Kubernetes application listener and probes on 8080 for TaskQualityControl.",
  "key": "devops-884-taskqualitycontrol-platform-ports",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-23T16:46:44.753901+00:00",
      "cause": "",
      "event_id": "devops-884-taskqualitycontrol-platform-ports-20261123",
      "expected": "Use a Nomad task ports list with a group-level network port mapping to 80 and keep the Kubernetes application listener and probes on 8080 for TaskQualityControl.",
      "source": "User direction in the DevOps-884 discussion on 2026-11-23",
      "summary": "User directed the TaskQualityControl Nomad port layout to match the document generator, using port 80 in Nomad and 8080 in Kubernetes."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "current",
  "summary": "User directed the TaskQualityControl Nomad port layout to match the document generator, using port 80 in Nomad and 8080 in Kubernetes.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#taskqualitycontrol-nomad-group-port-prepared-2026-11-23",
  "task_id": "DevOps-884",
  "updated": "2026-11-23T16:46:44.849603+00:00",
  "version": 1
}
```
