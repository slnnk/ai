---
system: gitlab-ci
status: verified
checked: 2026-10-13
tags: [dynamic-inventory, vk-cloud, nomad, consul]
---
# Dynamic inventory migration to VK: audit and proposed plan

## Task

Prepare a migration plan for [sysadmins/dynamic_inventory](https://gitlab.youdo.sg/sysadmins/dynamic_inventory) from Yandex Cloud to VK Cloud. Planning only; implementation and deployment are not approved.

## Context

Read-only GitLab audit of master at bb39065136fa08130aadc03edfd07c7f65542840, project110. Snapshot: `/home/slnnk/ai-data/dynamic-inventory/source`; no local checkout registered. Target DC `vk-test`; known Nomad API `http://nomad.service.vk-test.consul:4646`. Latest [address map](../../service-addresses.env) records direct Nomad reachability but workstation Consul DNS failure; runner/container reachability remains unverified.

## Actions

Ran ai-sync.sh (no reminders), consulted context, backlog and repo registry, and delegated source reading. GitLab GET requests required execution outside the sandbox due to DNS restrictions. No external writes or repository changes. Public web access to private GitLab failed; authenticated API provided source. Consulted [OpenStack SDK configuration](https://docs.openstack.org/openstacksdk/latest/user/config/configuration.html) for authentication/configuration options; actual VK project settings still need verification.

## Findings

- `srv/main.py:172-191` uses Yandex Compute API, RUNNING filter and folder scope. SQL VM selection depends on `name.startswith('sql')`, second hyphen-separated name component, first NIC private IPv4 and `<stage>_sql0`. No metadata/label mapping exists.
- `srv/main.py:194-283` assembles Ansible JSON, `_meta.hostvars`, SQL/Windows/stage groups, static infrastructure addresses and calculated per-stage ports. Keep this contract shared across providers.
- GET returns the cached inventory; authenticated PUT rebuilds it. Initial cache is `{}`. `srv/updater.py` refreshes every69seconds after a30second delay. Failure and empty-result behavior need explicit validation before cutover.
- `Dockerfile.api` uses Python3.8.19 and yandexcloud. Select a compatible pinned VK/OpenStack client; if required, propose the smallest Python version change rather than an unrelated runtime refactor.
- `yandex-test.nomad` reads Consul `admin/dynamic_inventory/*` configuration and Vault `secret/admin/dynamic_inventory` cloud key. These are Yandex credentials, distinct from Nomad deployment credentials.
- `.gitlab-ci.yml` builds/pushes api,dns,updater images only on tags; staging and yandex-test deployment jobs are manual, tags-only. Branch/MR publication alone does not build release images. Tags/build/push/deploy require their own explicit approvals.
- `NOMAD_COUNT_HOSTS=7` is consumed by `range(1, NOMAD_COUNT_HOSTS)`, excluding7. VK has eight known clients. Confirm intended inventory membership, then minimally correct configuration/enumeration for that agreed set.
- DNS updater is absent from Yandex deployment and its periodic call is commented. Separate DNS implementation can delete records and only adds172.* addresses; do not activate it for10.18.* as part of this migration.

## Proposed migration plan

1. **Lock the target inventory contract.** Identify all HTTP consumers (AWX, Ansible, Jenkins and scripts are candidates, not verified consumers), expected endpoint/authentication, active stages, actual SQL VM names, private network and static LB/Postgres/Rabbit/logreader/Nomad addresses. Produce an expected VK inventory fixture. Do not infer stage selection from the unrelated Redis deployment scope.
2. **Verify VK access and configuration.** Confirm project/region/Identity endpoint and available authentication method. Arrange service credentials with the required read permissions, stored in Vault; nonsecret parameters belong in VK Consul. Verify cloud API, Consul/Vault and DNS reachability from the actual runtime/CI paths. Authentication may require an Identity POST, so seek permission before live authentication; existing-token GET checks remain read-only.
3. **Implement the smallest provider adapter.** Modify `srv/main.py` and `Dockerfile.api`: add `VM_PROVIDER=vk`, scoped/paginated Compute discovery, ACTIVE SQL VM selection, explicit private-network IPv4 selection and stable mapping to existing stage/hostname fields. Reuse the inventory assembler and preserve existing providers. Base name/metadata mapping on step1 evidence. Handle malformed names, duplicate stage SQL mappings, missing addresses and cloud errors explicitly; an unsuccessful refresh must preserve the last valid cache. Protect against unintended empty inventory according to the expected fixture.
4. **Prepare VK runtime configuration.** Add `vk-test.nomad` using the existing API/updater pattern and new secret/configuration bindings, DC and routing. Set verified static addresses and the agreed Nomad host set. Update `.gitlab-ci.yml` with an explicit manual VK deployment job and VK Nomad variables. Keep existing deployments and DNS activation unchanged. Decide the tag/release name and any CI-variable writes before publication.
5. **Verify offline and in isolation.** Fixture tests cover names/groups/ports, pagination, ACTIVE filtering, multiple networks, floating-IP exclusion, invalid/missing VM data, duplicates,401/403/timeouts, empty results and cache preservation. Validate image dependencies, rendered Nomad job and GitLab CI. After separate runtime approval, pilot API/updater with an isolated service/route; check first successful refresh and subsequent automatic refresh. Compare JSON and `ansible-inventory --list/--graph` with the fixture; do not run configuration playbooks.
6. **Cut over consumers after review.** Present actual diff, checks, branch/base, commit/MR and CI effects through the supervised workflow. Release tag, image publication, secret/KV writes, pilot deployment and route/consumer switching are separate externally changing actions requiring explicit approval. Switch only after nonempty expected inventory, correct VK IPs and automatic refresh are demonstrated.
7. **Observe and retain rollback.** Save previous image/job/config and known-good inventory without credentials. Verify consumers and repeated refreshes after cutover. Roll back route/job/config to the previous known-good service on regression; if Yandex is unavailable, restore the saved inventory through the agreed consumer mechanism. Do not promise recovery merely by redeploying the old Yandex adapter.

**Completion criteria:** VK VM discovery works without Yandex access; the agreed stages/groups/variables and private addresses match expectations; consumers accept the inventory; refresh failures preserve valid data; no DNS modification is introduced.

## Changes

Created this audit/plan, linked it from the existing GitLab system map and tracked implementation in the central backlog. No proposed/final branch or ticket ID exists yet; no implementation/publication approval has been requested. Source credentials were not copied into notes.

## Risks

Actual VK VM naming, project/network scope, consumer list and credential permissions are not established. Static addresses and eight-client enumeration prevent treating this as an SDK-only change. Source has embedded Basic authentication material; do not quote it or copy it into new health checks. Use the existing secret mechanism for any new deployment binding. All migration steps above remain proposed.

## Portable lesson

none
