---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, kafka, vk-cloud, recovery]
---
# DevOps-893 VK Kafka Schema Registry deployment

## Task

User approved Kafka Schema Registry apply with `Да`. Deploy individually, diagnose runtime failures if they occur, maintain address map.

## Context

Approved DevOps-893 branch/root vk-test/state terraform/vkcloud-terraform. Source job preserved except required VK datacenter/host/bootstrap address substitutions. No shared Kafka server modifications authorized or performed.

## Actions

Executed terraform_stage.py apply --service kafka-schema-registry with reviewed saved plan:1add/0change/0destroy. GET verification: one allocation111e9032-267d-3aeb-e684-7dd86af946bc running on vk-ms1-nomad-agent-test-01. Consul schema-registry registration10.18.26.34:31264 health passing; GET /subjects HTTP200 with zero subjects. Recorded endpoints/health observations in service-addresses.env.

## Findings

Image confluentinc/cp-schema-registry:8.1.0,500CPU/512MiB. Bootstrap kafka.service.vk-test.consul:9092. Traefik Host rule kafka-schema-registry.vk-test.youdo.local configured; external DNS/routed URL untested. Empty subject list accepted under user's empty-data instruction. No writes performed to register example schemas.

Next proposed service Alloy traces uses grafana/alloy:v1.10.0,200CPU/512MiB, one allocation. Its copied resources Vault block has no secret-consuming template, same unnecessary dependency proven to fail exporter. Removed only that Vault block locally before planning; remaining trace config preserved. No Alloy traces apply yet.

## Changes

Schema Registry deployed and address map updated; local Alloy traces job removes unused Vault declaration. No Git publication or shared Vault repair.

## Status

Schema Registry verified running with healthy /subjects API. Next Alloy traces plan awaits approval; remaining work tracked in ~/ai/TODO.md.

## Portable lesson

none
