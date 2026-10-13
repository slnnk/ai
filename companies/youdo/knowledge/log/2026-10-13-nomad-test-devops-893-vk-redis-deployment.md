---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, terraform, redis, vk-cloud, recovery]
---
# DevOps-893 VK Redis deployment for sixteen stands

## Task

Apply the reviewed Redis-only plan after user `Примени apply`. Explicit scope corrections: sixteen stands test,test1–test15; test16/test17 excluded and redis-autotest removed locally. Empty initial data allowed.

## Context

Existing approved branch DevOps-893-recover-nomad-on-vk; separate root vk-test; Consul backend terraform/vkcloud-terraform. Traefik already running. No other deployment covered by this approval.

## Actions

Executed `python3 ~/ai-data/nomad-vk-access/terraform_stage.py apply --service redis` against the previously saved plan. Terraform completed1add/0change/0destroy, jobID redis. GET verification via probe.py --redis:16/16 allocations/tasks running,16cache registrations passingTCPchecks. No runtime fixes needed.

## Findings

Redis image redis:6, one group per stand,500CPU/1024MiB each. Consul service cache, stand tags test/test1–test15, host ports1900–1915. Direct node placements and tag-qualified DNS route names recorded in current/service-addresses.env; DNS names follow Consul naming from registered tags, not an extra resolution test.

Next independent plan prepared for nomad_job.jaeger-agent:1add/0change/0destroy. Source-as-is systemjob, jaegertracing/jaeger-agent:1.62.0,100CPU/100MiB pereligibleclient, reporter tempo-jaeger.dev.youdo.corp:80 unchanged. No Jaeger apply approval or execution yet.

## Changes

Updated service address map with16Redis endpoints and observation/verification comments, Nomad system map, backlog and deployment log. No repository modifications beyond previously approved stand exclusions; no git publication.

## Status and risks

Redis deployment verified healthy at the observation time. TCPhealth does not assert arbitrary application workloads or persistence across restarts. User requested source behavior preserved and service-by-service recovery. Next Jaeger agent apply requires its own approval; remaining work tracked in ~/ai/TODO.md.

## Portable lesson

none
