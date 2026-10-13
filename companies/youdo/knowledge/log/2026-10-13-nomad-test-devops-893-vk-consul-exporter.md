---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, consul, vault, vk-cloud, recovery]
---
# DevOps-893 Consul exporter Vault dependency failure and local fix

## Task

User approved next Consul exporter apply with `Да`. Execute and diagnose actual failures under the requested individual-service recovery workflow.

## Context

vk-test root, state terraform/vkcloud-terraform, approved branch DevOps-893-recover-nomad-on-vk. Traefik/Redis/Jaeger agents already running. Exporter copied from source with monitoring Vault policy but without secret-consuming templates.

## Actions

Executed terraform_stage.py apply --service consul-exporter; Terraform1add/0change/0destroy, job registered. GET allocation check found failed/dead allocation c7095901-7154-3691-cb8b-7bd252265605 on vk-ms1-nomad-agent-test-01. No exporter Consul service registration.

Actual task event: Vault server failed to derive task token; auth/token/lookup returned403 with permission denied and invalid token. This confirms a broken Nomad server Vault credential beyond the earlier preflight hypothesis. Examined job: unused vault policy monitoring, no template/secret dependencies. Prepared minimal local fix by removing only the vault block from vk-test/jobs/consul-exporter.hcl; no global integration changes.

Regenerated targeted saved plan1update/0add/0destroy. Job validation passed with inherited task-network deprecation warning. Replacement apply requires its own explicit approval; it has not run.

## Findings

User requested a fresh master-configuration check after Alloy traces deployment. Read /etc/nomad.d/server.hcl on10.18.26.11/.12/.13 via youdo+sudo and compared effective running Nomad /agent/self on each actual IP. All three have Vault enabled, correct VK Vault URL and token configured. GET lookup-self using each on-disk server token returns403 with invalid token/permission denied. Thus integration EXISTS in both files and effective config; authentication is broken. Initial localhost API probe failed because127.0.0.1:4646 is not the actual API bind; actual-IP probes allHTTP200. No remote edits/reloads or token creation performed; token values never printed/stored. Evidence: ai-data/nomad-vk-access/masters-vault.json and masters_vault_probe.py.

Exporter never started because the copied Vault declaration forced token derivation, although this job consumes no Vault secrets. Removing that unnecessary declaration avoids the unused dependency for this service. Other jobs that consume secrets still require repair of the shared Nomad→Vault credential. No administrative token injected into workloads and no token issued/replaced.

## Changes

Local Consul exporter job: removed4-line Vault block only. No images/resources/ports/args changed. Terraform state now owns registered failed job. Service address map has no new exporter endpoint because no registration exists. No git publication or remote configuration edits.

## Status

User explicitly approved the corrective apply with `Да`. Executed saved update plan:0add/1change/0destroy. Active allocation6961c7b2-6e64-0a96-d65c-ad09a953728f running on vk-ms1-nomad-agent-test-08,10.18.26.35:28270. Consul health passing, GET /metrics HTTP200 and consul_up=1. Historical failed allocations are desired stop. Healthy endpoint recorded in service-addresses.env. This result supersedes the prior pending/failed status below; shared Vault credential is still unrepaired.

Next Kafka Schema Registry plan prepared:1add/0change/0destroy, one allocation,500CPU/512MiB, confluentinc/cp-schema-registry:8.1.0. Required local target correction: bootstrap from kafka-test01.ru-central1.internal:9092 to kafka.service.vk-test.consul:9092. No Schema Registry apply yet; approval pending.

Initial approved apply completed, exporter allocation failed. Minimal updated plan awaits approval; service not claimed healthy. Track remaining deployment and shared Vault repair in ~/ai/TODO.md.

## Portable lesson

none
