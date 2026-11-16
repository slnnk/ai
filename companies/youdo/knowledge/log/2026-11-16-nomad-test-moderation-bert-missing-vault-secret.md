---
system: nomad-test
status: verified
checked: 2026-11-16
tags: [moderation-bert, vault, deployment]
---
# Moderation BERT deployment blocked by missing Vault secret

## Task
Diagnose the failure of `moderation-bert@default` in VK test. Read-only investigation; no repair or deployment authorized.

## Findings
Nomad deployment `3354a364-07b7-cb6a-a088-c28c3f8833e1`, job version2, image `registry.youdo.sg/data/moderation-bert:0.1.1` has zero healthy allocations. Snapshot: eight failed and one starting. Latest allocation `49a885dd-d48d-322e-9c81-0a3df0fbe0b1` waits for a template. Previous allocation `b70c9132-7981-f1d1-650d-9dc4845ba59c` failed with:

```text
Template failed: vault.read(secret/ds/moderation-bert): no secret exists at secret/ds/moderation-bert
```

The main task has never started. Prestart `fetch` completed with exit0. The template destination `secrets/clickhouse-bi.env` references `.Data.CLICKHOUSE_USERNAME` and `.Data.CLICKHOUSE_PASSWORD` at that path. Independent authenticated GET to VK Vault `/v1/secret/ds/moderation-bert` returned404; no secret values were printed.

## Actions and evidence
Read-only Nomad job summary, allocations, deployments, evaluations, template references, and Vault existence check. Generated evidence: `~/ai-data/moderation-bert-diagnosis/`. Shell DNS failed in sandbox; approved network reads succeeded outside sandbox. No application execution logs exist for the unstarted main task.

## Status and risks
Diagnosis complete; no external changes. Restore the intended Vault configuration or correct the referenced path only with separate authorization; tracked in central TODO. No background diagnostic commands remain; Nomad continues its own retry cycle. No new preference or correction arose; retrieved applicable rules were followed by restricting this task to diagnosis.

## Portable lesson
None.

## Task metrics: moderation-bert-diagnosis-20261116

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "moderation-bert-diagnosis-20261116",
  "created": "2026-11-16T14:48:01.507256+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "diagnosis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Nomad template error and independent Vault GET404; no external mutation",
  "updated": "2026-11-16T14:48:01.507308+03:00"
}
```
