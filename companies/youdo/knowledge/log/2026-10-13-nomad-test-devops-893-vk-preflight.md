---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, vault, consul, s3, csi, recovery]
---
# DevOps-893 VK deployment preflight steps 1 through 3

## Task

Run deployment preflight steps1–3 for DevOps-893. User subsequently stopped additional preflight and requested rapid deployment one service at a time, diagnosing failures when encountered. No repository or external state changes have been performed.

## Context

See [deployment plan](2026-10-13-nomad-test-devops-893-vk-deployment-plan.md) and [access results](2026-10-13-nomad-test-devops-893-vk-access.md). VK Cloud API credentials were explicitly deferred by the user; no cloud API authentication attempted. Empty bootstrap data remains permitted.

## Actions

GET-only Vault schema/policy checks, Nomad config/node/resources/allocations/client stats, Consul monitoring policy; S3 HEAD bucket checks; TCP PostgreSQL ports and read-only SELECT1 login attempt. Delegated source audit and read-only SSH host inspection. SSH works as `youdo` with `sudo -n`; root authentication is rejected. Task-local known_hosts records newly accepted keys. No container pulls, submissions, credential issuance, configuration edits or service restarts.

Filtered diagnostic artifacts under `~/ai-data/nomad-vk-access/`: `preflight.json`, `integration.json`, `storage.json`, `postgres.json`, `hosts.json`, `registry.json`, and their CLI probe scripts. No secret values stored in artifacts; schema checks emitted field names only. Used administrative operator `VK_TEST_*` tokens from `current/.env`.

## Findings

- Grafana Postgres/OAuth/LDAP, oauth2-proxy and Loki/Tempo/Mimir S3 secrets exist with required nonempty fields. `secret/vk/csi` and policy `vk-csi` absent. Policies monitoring/resources/oauth2-proxy present. CloudWatch secret has only an empty AWS_ACCESS_KEY; remaining AWS fields absent. Current Alloy config does not use the AWS fields, although its module injects them unconditionally; decide minimal target treatment during implementation.
- All three Nomad servers have Vault enabled at `http://vault.service.vk-test.consul:8200`, with token configured and no token role. Existing server tokens return403 for lookup-self, capabilities-self and S3 secret reads. This fails verification of integration; restored/stale tokens are a hypothesis, not a proven cause. No replacement or test token issued.
- Vault Consul engine points to local127.0.0.1:8500; monitoring role references Consul policy monitoring. That policy exists with write prefixes monitoring/mimir/loki. Actual dynamic issuance untested because it creates a token.
- Eight Nomad clients ready/eligible on1.5.3:128cores,514400MiB scheduler RAM, no jobs or allocations across namespaces. Actual available RAM about474.6GiB; each root filesystem has86.6GiB free. Ports80/8080 free all8. Docker healthy, privileged and volumes enabled. Current source reservation baseline about22600CPU units/55052MiB including the old CSI reservation, excluding Loki init defaults; ample aggregate capacity, final scheduling checked per job.
- OpenStack metadata reachable on all inspected hosts; actual UUIDs retrieved and zoneMS1 reported. Nomad AWS-style instance attributes are not the Cinder Nova UUID. VK API quota/type list remains untested as agreed.
- Client Docker auth contains registry.youdo.sg; Nexus auth absent, but current active images do not use Nexus. Four GGR image manifests available. Private `registry.youdo.sg/data/prom-ruller:1.2.2` HEAD404 after successful authentication. CSI candidate `registry.k8s.io/provider-os/cinder-csi-plugin:v1.34.1` manifest available; Nomad/VK functionality still untested.
- Existing S3 bucket HEAD200 from workstation for `youdo-loki-test`, `youdo-tempo-test`, `youdo-mimir-test`, `youdo-mimir-ruler-test`, all at storage.yandexcloud.net with target Vault credentials. Migration is not currently required just for reachability. Object reads/writes and client-side signed access untested; no old data deleted or buckets changed.
- Grafana source hardcodes Consul-discovered postgres port5433; actual VK5432 open and5433 refused. SELECT1 using Vault credentials from workstation rejected by pg_hba.conf; this does not establish client-subnet rejection. Client01 has no psql; did not install it.

## Changes

KB bookkeeping only. Updated rollout direction: stop extra preflight, prepare/deploy Traefik first (no Vault/CSI dependency), then Redis and subsequent services individually. Fix diagnosed issues only when their owning service is addressed. Existing plan remains reference inventory; its exhaustive preflight gates are superseded by the user's instruction.

## Status

Preflight stopped at user request after findings above. Before repository edits, supervised branch approval is still required: proposed `DevOps-893-recover-nomad-on-vk` in `/home/slnnk/git/terraform` from `origin/master`. No approval yet. Each concrete runtime mutation needs the applicable explicit approval. Remaining work tracked in `~/ai/TODO.md`.

## Portable lesson

none
