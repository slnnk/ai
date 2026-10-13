---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, jaeger, vk-cloud, recovery]
---
# DevOps-893 VK Jaeger agent deployment and unused job cleanup

## Task

User approved the Jaeger agent apply with `Да`. Afterwards user edited vk-test/nomad.tf and requested deleting all unused job files. No further runtime action authorized by that cleanup request.

## Context

Approved branch DevOps-893-recover-nomad-on-vk; separate root vk-test; state terraform/vkcloud-terraform. Traefik and Redis already deployed. User requested source-as-is recovery with task-specific exclusions; preserve unrelated/user edits.

## Actions

Executed terraform_stage.py apply --service jaeger-agent; result1add/0change/0destroy. GET verification saved in ai-data/nomad-vk-access/jaeger-status.json:8/8allocations/tasks running,32jaeger-agent registrations and8metrics registrations across8clients. Updated address map from those observations, without extra remote checks.

For cleanup, inspected active jobspec references in current nomad.tf and monitoring.tf. Deleted11unreferenced vk-test/jobs files: selenoid-ggr-ios.hcl, filebeat-traefik.hcl, jaeger.hcl, tempo.hcl, oauth2-proxy.nomad, blackbox.nomad, baget.nomad, grafana.nomad, loki.hcl, filebeat.hcl, jaeger-index-cleaner.hcl. Active-reference/file-set comparison passed;7retained job files exactly match active root references. User-edited nomad.tf was not rewritten during cleanup.

## Findings

Jaeger system job preserves jaegertracing/jaeger-agent:1.62.0 and reporter tempo-jaeger.dev.youdo.corp:80. Per-node ports5775/6831/6832/5778/14271; job defines no application health checks. Registration/running evidence does not assert end-to-end trace delivery.

Remaining job files: alloy-traces.hcl, consul-exporter.nomad, csi-plugin.hcl, jaeger-agent.hcl, kafka-schema-registry.hcl, redis.hcl, traefik2.hcl. Inactive monitoring.tf comment blocks remain untouched and may mention removed files; they are not evaluated. No config files, shared modules or original yandex-test files deleted.

## Changes

User requested renaming the remaining Consul exporter job to HCL extension: vk-test/jobs/consul-exporter.nomad → consul-exporter.hcl; updated the jobspec reference in vk-test/monitoring.tf. File contents unchanged, no runtime action. Earlier file listings above describe the prior name.

Eleven local job deletions as explicitly requested; service-addresses.env expanded with Jaeger endpoints/observations; KB system map/backlog updated. No commit/push/MR, remote file edits or runtime removals. Interrupted next-service planning not treated as completed or approved.

## Status

Next Consul exporter-only plan regenerated from current user-edited configuration after .hcl rename:1add/0change/0destroy, one allocation, prom/consul-exporter:v0.13.0,20CPU/100MiB, inherited Vault policy monitoring. Saved consul-exporter.tfplan; apply not yet approved.

Jaeger deployment running on8clients; local unused-job cleanup complete. Further service plans/deployments tracked in ~/ai/TODO.md and require applicable approvals. Cleanup does not stop or remove any currently deployed service.

## Portable lesson

none
