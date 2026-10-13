---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, consul, vault, vk-cloud, access]
---
# DevOps-893 VK access verification and service address map

## Task

DevOps-893 follow-up: verify newly supplied `VK_TEST_*` tokens in `current/.env` and provide a separate address map grouped by datacenter.

## Context

Existing [deployment plan](2026-10-13-nomad-test-devops-893-vk-deployment-plan.md). User added `VK_TEST_VAULT_TOKEN`, `VK_TEST_NOMAD_TOKEN`, `VK_TEST_CONSUL_TOKEN`; only variable names and auth metadata were printed. No external state changes authorized or performed.

## Actions

Executed `~/ai/general/scripts/ai-sync.sh`; no output/reminders. Created read-only probe `~/ai-data/nomad-vk-access/probe.py` with CLI env/output options and optional service catalog. Sandbox DNS failed; approved elevated execution successfully reached internal services. All network calls used GET. Saved filtered results to `~/ai-data/nomad-vk-access/result.json`, excluding token values, raw configs and secret payloads.

## Findings

- Vault `http://vault.service.vk-test.consul:8200`: health and lookup-self HTTP200, version1.21.4, initialized/unsealed/active, token policy `root`, TTL0.
- Nomad `http://nomad.service.vk-test.consul:4646`: token type `management`, leader `10.18.26.11:4647`, eight ready/eligible clients in `vk-test`, version1.5.3. Default namespace job/CSI volume lists empty; CSI plugin list empty. API access and declared permissions verified; no writes used to test them.
- Consul `http://consul.service.vk-test.consul:8500`: token `global-management`, leader `10.18.26.13:8300`, datacenter `vk-test`. `terraform/vk-test?keys` returns404, so no target state keys currently exist.
- Target Vault has `secret/` KVv1, `kv/` KVv2 and Consul/Nomad/database engines. Engine presence does not establish role correctness. GET policy collection returned405; policy inventory was not verified by that request. Admin token validity is independently confirmed by lookup-self.
- Catalog services: Consul, Nomad/client, Vault, Postgres/C2C, Postgres/B2B, Kafka, elastic-b2b and elasticsearch. Consul checks pass except `elasticsearch` on10.18.26.32:9201 (critical). `elastic-b2b` on the same host:9200 passes. RabbitMQ exists as a node only, without a registered rabbitmq service.
- App endpoints were recorded from catalog/checks, not independently authenticated at application level. Full capacity, registry access, Nomad→Vault integration and actual application secret schemas remain to verify.

## Changes

Created nonsecret [service-addresses.env](../../service-addresses.env), currently containing only the verified VK datacenter section, API URLs, catalog IPs/ports and health limitations. Credentials remain separately in `current/.env`. Updated system map and deployment plan to reference these results and actual variable names. No repository edits, branch changes, secret updates or runtime deployment.

## Status

Access checks and address map complete. Remaining deployment prerequisites stay tracked in `~/ai/TODO.md`.

## Portable lesson

none
