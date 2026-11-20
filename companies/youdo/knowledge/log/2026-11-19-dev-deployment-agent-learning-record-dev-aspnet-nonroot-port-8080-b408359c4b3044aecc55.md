---
system: dev-deployment
status: verified
checked: 2026-11-19
tags: [agents, learning]
---
# Agent learning: dev-aspnet-nonroot-port-8080

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-19T12:24:23.597129+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-19T12:51:50.585237+00:00",
      "cause": "",
      "event_id": "devops-884-blec-listener-20261119",
      "expected": "Use port 8080 for non-root ASP.NET Core workloads in dev Kubernetes. Set ASPNETCORE_URLS and align the chart component port and probes. The Kubernetes Service may expose port 80.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#blacklistedemailchecker-mr-prepared",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/dev-deployment/overview.md#aspnet-core-container-listener"
    }
  ],
  "expected": "Use port 8080 for non-root ASP.NET Core workloads in dev Kubernetes. Set ASPNETCORE_URLS and align the chart component port and probes. The Kubernetes Service may expose port 80.",
  "key": "dev-aspnet-nonroot-port-8080",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-19T12:24:23.597129+00:00",
      "cause": "",
      "event_id": "devops-884-port-8080-user-20261119",
      "expected": "Use port 8080 for non-root ASP.NET Core workloads in dev Kubernetes. Set ASPNETCORE_URLS and align the chart component port and probes. The Kubernetes Service may expose port 80.",
      "source": "DevOps-884 user confirmation on 2026-11-19; same failure previously observed in youdo.business dev-107",
      "summary": "User confirmed the dev Kubernetes HTTP listener convention after the geocoder bind failure."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User confirmed the dev Kubernetes HTTP listener convention after the geocoder bind failure.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/dev-deployment/overview.md#aspnet-core-container-listener",
  "task_id": "",
  "updated": "2026-11-19T12:51:50.585237+00:00",
  "version": 1
}
```
