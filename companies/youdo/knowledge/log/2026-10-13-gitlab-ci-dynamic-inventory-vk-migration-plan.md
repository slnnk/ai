---
system: gitlab-ci
status: verified
checked: 2026-10-14
tags: [dynamic-inventory, vk-cloud, nomad, consul]
---
# Dynamic inventory migration to VK: audit and proposed plan

## Task

Prepare a migration plan for [sysadmins/dynamic_inventory](https://gitlab.youdo.sg/sysadmins/dynamic_inventory) from Yandex Cloud to VK Cloud. Assigned to [DevOps-896](https://youtrack.youdo.com/youtrack/issue/DevOps-896) by the user on 2026-10-14. Migration plan plus the later approved local bootstrap implementation stage; publication was subsequently approved and completed; deployment is not approved.

## Context

Read-only GitLab audit of master at bb39065136fa08130aadc03edfd07c7f65542840, project110. Snapshot: `/home/slnnk/ai-data/dynamic-inventory/source`; no local checkout was registered at the initial audit; the existing checkout was registered on 2026-10-14. Target DC `vk-test`; known Nomad API `http://nomad.service.vk-test.consul:4646`. Latest [address map](../../service-addresses.env) records direct Nomad reachability but workstation Consul DNS failure; runner/container reachability remains unverified.

## Actions

Ran ai-sync.sh (no reminders), consulted context, backlog and repo registry, and delegated source reading. GitLab GET requests required execution outside the sandbox due to DNS restrictions. No external writes or repository changes. Public web access to private GitLab failed; authenticated API provided source. Consulted [OpenStack SDK configuration](https://docs.openstack.org/openstacksdk/latest/user/config/configuration.html) for authentication/configuration options; actual VK project settings still need verification.

## Findings

- `srv/main.py:172-191` uses Yandex Compute API, RUNNING filter and folder scope. SQL VM selection depends on `name.startswith('sql')`, second hyphen-separated name component, first NIC private IPv4 and `<stage>_sql0`. No metadata/label mapping exists.
- `srv/main.py:194-283` assembles Ansible JSON, `_meta.hostvars`, SQL/Windows/stage groups, static infrastructure addresses and calculated per-stage ports. Keep this contract shared across providers.
- GET returns the cached inventory; authenticated PUT rebuilds it. Initial cache is `{}`. `srv/updater.py` refreshes every69seconds after a30second delay. Failure and empty-result behavior need explicit validation before cutover.
- `Dockerfile.api` uses Python3.8.19 and yandexcloud. The final implementation uses direct VK Identity/Compute REST requests with pinned requests2.32.4 on Python3.8; no OpenStack SDK or Python version migration was required.
- `yandex-test.nomad` reads Consul `admin/dynamic_inventory/*` configuration and Vault `secret/admin/dynamic_inventory` cloud key. These are Yandex credentials, distinct from Nomad deployment credentials.
- `.gitlab-ci.yml` builds/pushes api,dns,updater images only on tags; staging and yandex-test deployment jobs are manual, tags-only. Branch/MR publication alone does not build release images. Tags/build/push/deploy require their own explicit approvals.
- `NOMAD_COUNT_HOSTS=7` is consumed by `range(1, NOMAD_COUNT_HOSTS)`, excluding7. VK has eight known clients. Confirm intended inventory membership, then minimally correct configuration/enumeration for that agreed set.
- DNS updater is absent from Yandex deployment and its periodic call is commented. Separate DNS implementation can delete records and only adds172.* addresses; do not activate it for10.18.* as part of this migration.

## Proposed migration plan

### User decisions (2026-10-14)

- Confirmed consumer: `test_inventory` in `automation-test-yandex`. The local checkout contains `test_inventory.sh`, which calls `http://dyninv.yandex-test.youdo.local/` using Basic authentication. The endpoint's current availability was not checked; credentials were not copied.
- Target stands: `test`, `test1` through `test15`. The user subsequently directed exclusion of `public-test` if the service source has no mentions. Read-only search of the saved source tree found none; `automation-test-yandex/inventories/public-test/hosts` instead explicitly defines its static SQL/docker/PostgreSQL/Rabbit hosts. Therefore `public-test` is excluded from the VK dynamic scope; this does not assert what previous live generated inventory contained.
- VK SQL VM naming contract: `vk-ms1-sql-{stand}`. Remove exactly the `vk-ms1-sql-` prefix and preserve the complete stand suffix, rather than using a positional hyphen split; do not reuse the old second-component split. Map, for example, `vk-ms1-sql-test1` to `test1_sql0`. VM existence, status and IPs remain unverified.
- VK test subnet is already documented as `10.18.26.0/24` in `automation-services/inventories/vkcloud/group_vars/all` (`vkcloud_test_subnet`), rechecked locally on 2026-10-14. SQL discovery should select private IPv4 from this subnet; the cloud network name/ID and actual SQL VM addresses are not yet verified. LAN is a separate `10.18.20.0/24` subnet.
- Required static bindings from `srv/main.py`: `LB_HOST` for `lb_host`/`{stand}_lb`, `POSTGRES_HOST` for `{stand}_postgres`, `LB_LOGREADER_HOST` for `{stand}_lb-logreader`, `RABBIT_HOST` for `{stand}_rabbit`, and `NOMADn_HOST` for `{stand}_nomadn`. There is no additional static-address variable for `{stand}_docker` or `{stand}_logreader`; these aliases are added to groups without corresponding hostvars in the audited assembler.
- Existing VK map and `automation-services/inventories/vkcloud/hosts` agree on C2C PostgreSQL `10.18.26.39` and RabbitMQ `10.18.26.7`. PostgreSQL B2B `10.18.26.44` is separate; the current assembler has only one `POSTGRES_HOST` binding. PostgreSQL service checks were passing on October13; RabbitMQ host was catalogued, but broker readiness was not verified.
- Nomad clients are `vk-ms1-nomad-agent-test-01` through `-08`, mapped respectively to `10.18.26.34`, `.38`, `.37`, `.30`, `.15`, `.10`, `.21`, `.35`. All eight were ready/eligible in the October13 Nomad API observation; October14 local inventory agrees. Use this discovered set when preparing VK enumeration instead of asking the user to supply hosts or carrying the old exclusive upper bound. The user initially requested preserving the exclusions, then added client08 on 2026-10-14: target `NOMAD_DISABLED_ID_HOSTS=5,6,7,8`; the intended included clients are 01, 02, 03 and 04. The observed Consul baseline remains `5,6,7`; no KV write has been performed.
- User confirmed `LB_HOST=10.18.20.97` on 2026-10-14. This sets `lb_host` and `{stand}_lb`; test routing has not been probed. User subsequently stated `LB_LOGREADER_HOST` is unused and must retain its existing value. Do not infer that it uses the same address. No branch, code, release or runtime action was approved by these contract decisions.

### SQL availability and bootstrap dependency (2026-10-14)

The user stated SQL VMs are not started yet because dynamic inventory is needed first. This is a runtime availability statement, not proof that cloud VM objects do or do not exist. Implementation and fixture validation can proceed without live SQL VMs; actual SQL private-IP mapping must be checked when they are available. Private IPv4 means reading an existing VM NIC address into `ansible_host`, not allocating a network or address.

The audited Yandex adapter selects RUNNING SQL VMs, and `get_inventory()` creates stage groups and their static LB/PostgreSQL/Rabbit/Nomad aliases only inside `for stage in result.keys()`. Therefore empty SQL discovery in the historical implementation returned global `lb_host` and empty service groups, with no `test`/`testN` groups. Starting only the adapted service would not resolve the user's bootstrap dependency under unchanged assembly behavior. Before implementation, define the required first-start output for the fixed stage set while SQL is absent; fixtures should cover that state. This behavior was subsequently authorized and implemented locally in the bounded bootstrap stage below: fixed infrastructure groups, with SQL hosts added only when discovered. Runtime changes remain unapproved.

### Existing VK Consul baseline (GET verified 2026-10-14)

User identified the existing `admin/dynamic_inventory/` prefix in VK Consul and stated only `DC` had been changed. A read-only GET confirmed `DC=vk-test` with the following legacy configuration. Output was restricted to a strict allowlist of nonsecret fields; no raw KV dump or credential values were persisted. Sandbox DNS failed; approved execution outside the sandbox succeeded. No KV writes occurred.

| Binding | Existing VK Consul value | Planned VK value/action |
|---|---|---|
| `VM_PROVIDER` | `yc` | Remove binding: VK-only service no longer selects a provider |
| `LB_HOST` | `10.16.20.35` | `10.18.20.97`, user confirmed |
| `POSTGRES_HOST` | `10.16.26.15` | C2C `10.18.26.39` |
| `RABBIT_HOST` | `10.16.26.17` | `10.18.26.7` |
| `LB_LOGREADER_HOST` | `172.26.0.111` | Preserve: unused per user |
| `NOMAD1_HOST`..`NOMAD6_HOST` | `10.16.26.11`, `.12`, `.13`, `.44`, `.54`, `.64` | Replace with discovered VK client mapping above |
| `NOMAD7_HOST` | empty | `10.18.26.21` |
| `NOMAD8_HOST` | absent | `10.18.26.35`, with supported enumeration |
| `NOMAD_DISABLED_ID_HOSTS` | `5,6,7` | Set target to `5,6,7,8`, per latest user decision on 2026-10-14; exclude clients05–08 |

`NOMAD_COUNT_HOSTS` is absent from this prefix and remains hardcoded as seven in the audited source. Source uses an exclusive range upper bound; simply setting a count to eight would still omit client08 unless enumeration is corrected. These are proposed configuration changes, not authorization to write Consul.

### Steps

1. **Complete the target inventory contract.** Use the confirmed consumer, target stands and VK naming rule above. Exclude `public-test` under the later user decision and source/static inventory evidence. Establish actual SQL VM/private-network addresses and static LB/Postgres/Rabbit/logreader/Nomad addresses, then produce an expected VK inventory fixture. Confirm the endpoint/authentication needed at cutover. AWX, Ansible and Jenkins are potential additional consumers only; do not infer their use or stage selection from the unrelated Redis deployment scope.
2. **Verify VK access and configuration.** Confirm project/region/Identity endpoint and available authentication method. Arrange service credentials with the required read permissions, stored in Vault; nonsecret parameters belong in VK Consul. Verify cloud API, Consul/Vault and DNS reachability from the actual runtime/CI paths. Authentication may require an Identity POST, so seek permission before live authentication; existing-token GET checks remain read-only.
3. **Implement the smallest provider adapter.** Modify `srv/main.py` and `Dockerfile.api`: use VK-only discovery, scoped/paginated Compute discovery, ACTIVE SQL VM selection using the exact `vk-ms1-sql-` prefix and agreed stand set, explicit private-network IPv4 selection and mapping of the full stand suffix to `<stand>_sql0`. Reuse the inventory assembler; the later explicit user instruction removes `one`/`yc` providers entirely. Handle malformed names, duplicate stage SQL mappings, missing addresses and cloud errors explicitly; an unsuccessful refresh must preserve the last valid cache. Protect against unintended empty inventory according to the expected fixture.
4. **Prepare VK runtime configuration.** Add `vk-test.nomad` using the existing API/updater pattern and new secret/configuration bindings, DC and routing. Set verified static addresses and the agreed Nomad host set. Update `.gitlab-ci.yml` with an explicit manual VK deployment job and VK Nomad variables. Remove obsolete staging/Yandex deployment templates under the later explicit user instruction; leave DNS deployment disabled. Decide the tag/release name and any CI-variable writes before publication.
5. **Verify offline and in isolation.** Fixture tests cover names/groups/ports, pagination, ACTIVE filtering, multiple networks, floating-IP exclusion, invalid/missing VM data, duplicates,401/403/timeouts, empty results and cache preservation. Validate image dependencies, rendered Nomad job and GitLab CI. After separate runtime approval, pilot API/updater with an isolated service/route; check first successful refresh and subsequent automatic refresh. Compare JSON and `ansible-inventory --list/--graph` with the fixture; do not run configuration playbooks.
6. **Cut over consumers after review.** Present actual diff, checks, branch/base, commit/MR and CI effects through the supervised workflow. Release tag, image publication, secret/KV writes, pilot deployment and route/consumer switching are separate externally changing actions requiring explicit approval. Switch only after nonempty expected inventory, correct VK IPs and automatic refresh are demonstrated.
7. **Observe and retain rollback.** Save previous image/job/config and known-good inventory without credentials. Verify consumers and repeated refreshes after cutover. Roll back route/job/config to the previous known-good service on regression; if Yandex is unavailable, restore the saved inventory through the agreed consumer mechanism. Do not promise recovery merely by redeploying the old Yandex adapter.

**Completion criteria:** VK VM discovery works without Yandex access; the agreed stages/groups/variables and private addresses match expectations; consumers accept the inventory; refresh failures preserve valid data; no DNS modification is introduced.

## Implementation approval (2026-10-14)

User approved proposed branch `DevOps-896-migrate-inventory-to-vk` from `origin/master` in the existing `/home/slnnk/git/dynamic_inventory` checkout, permitting branch creation/switch and local task edits. Read-only branch inspection confirmed the approved branch is active. Immediate implementation scope is removing the dependency of test-stage infrastructure inventory on running SQL VMs; full cloud-adapter/runtime scope remains governed by the plan and further review. Existing unrelated tracked Python bytecode modification and untracked scratch files must be preserved. No publication, KV write, release or runtime approval is implied.

## Current local implementation and checks (2026-10-14)

User provided `VK_AUTOMATION_USER`, `VK_AUTOMATION_PASSWORD` and `VK_PROJECT_ID` in `current/.env`, supplied `/home/slnnk/downloads/automation-openrc.sh`, and explicitly authorized local authentication/testing. Nonsecret RC configuration: Identity v3 `https://infra.mail.ru:35357/v3/`, region `RegionOne`, user domain `service-users`, public interface. User then explicitly requested removal of `one`/`yc` providers. This supersedes the original provider-preservation proposal and the initial bootstrap-only intermediate scope.

On approved branch `DevOps-896-migrate-inventory-to-vk` from freshly fetched `origin/master` `bb39065`, `srv/vk_cloud.py` now performs project-scoped Keystone authentication, chooses the public Compute catalog endpoint for RegionOne, paginates ACTIVE VMs, selects exact `vk-ms1-sql-` names for test/test1-test15, and selects one fixed IPv4 from `10.18.26.0/24`. Duplicate mappings, missing/ambiguous addresses and malformed pagination fail explicitly. `srv/main.py` always creates the fixed sixteen stages independently of SQL availability, adds real discovered SQL hosts, excludes public-test, enumerates Nomad01-08 and applies the agreed exclusion `5,6,7,8` (clients01-04 included). Legacy imports/provider settings are removed.

`Dockerfile.api` uses Python3.8 and requests (the verified build resolved requests2.32.4) and copies only main/vk modules. New `vk-test.nomad` prepares API/updater delivery, VK static settings, Consul configuration, existing Basic auth and Vault `secret/admin/dynamic_inventory` fields `VK_AUTOMATION_USER`/`VK_AUTOMATION_PASSWORD`; authenticated GET is not used for the HEAD health check. Old staging/Yandex Nomad templates are removed. CI has a VK-only manual tags deployment. DNS image build remains, with no DNS deployment.

The root implementer verified two real local API refreshes: PUT200/GET200, sixteen stand groups, sixteen docker aliases, sixty-four Nomad aliases (four per stand), zero SQL/windows hosts. No SQL VM was available in the discovered result; existing-address mapping for a live SQL VM remains to be checked after availability. No raw Consul dump or credential values were persisted. This was local service execution and authorized VK authentication/Compute reads, not deployment.

Ten regression tests passed, including refresh-failure cache preservation. An HTTP error-response defect was reproduced and fixed: headers now precede the error body, so updater clients can read failure responses. `git diff --check` passed. Offline Nomad validation reported zero warnings (driver validation was not performed); GitLab CI lint reported valid, two jobs, no errors/warnings. The local Python3.8 image build passed; final rebuilt image `sha256:9f7aefcf8b5b2fb1271a73c42624109f94b208268d72b9aeac61b29d35b22e36` also passed two real VK API/HTTP refreshes (PUT200, GET200; 16 stages, 16 docker aliases, 64 Nomad aliases, zero SQL/Windows hosts). The temporary local container was stopped and removed. Existing unrelated tracked bytecode and untracked scratch files remain preserved. At the end of local checks, no publication or external configuration/runtime changes had occurred; subsequent approved publication is recorded below.

## Reviewed publication completed (2026-10-14)

The user explicitly answered `Да` to the concrete reviewed commit/push/MR publication proposal. Fresh ten tests and staged diff checks passed; only the eight approved task paths were staged. Commit `265c2db2d59fd5501bb727b159e9641486a62408` (`migrate dynamic inventory to vk cloud`) was pushed on `DevOps-896-migrate-inventory-to-vk`. [MR !26](https://gitlab.youdo.sg/sysadmins/dynamic_inventory/-/merge_requests/26), title `DevOps-896 migrate dynamic inventory to VK Cloud`, targets `master`. API verification confirmed SHA, title, Russian paragraph/task-link description and branches. Assignee `a.solonenko`, squash disabled and source-branch removal enabled match project preferences.

The commit displays seven diff entries, 309 insertions and 348 deletions because Git detects `yandex-test.nomad` to `vk-test.nomad` as a rename; this represents the eight approved paths. Unrelated tracked bytecode and untracked scratch files remained unstaged. No pipeline was created (`pipelines=[]`), consistent with tags-only CI.

Publication is complete; no merge, tag, registry image publication, Consul/Vault/CI-variable write, deployment or consumer cutover was performed or authorized. Runtime still requires separately reviewed configuration/secret preparation, release and manual deployment, followed by consumer route switching and live SQL mapping when available.

## Approved runtime preparation and release (2026-10-14)

The user separately approved the external actions: one Consul transaction applying thirteen VK inventory configuration keys, Vault addition of VK automation credential fields while preserving existing YC fields, and project CI variables. Post-write checks verified configuration and credential matches without printing values. `NOMAD_VK_TEST_ADDR` uses the canonical DNS endpoint `http://nomad.service.vk-test.consul:4646`: the user explicitly corrected the initial direct-IP proposal. `NOMAD_VK_TEST_TOKEN` is masked, environment scope `vk-test`, protected=false for the current unprotected release tags. Effective CI credentials reached the DNS endpoint and confirmed eight ready clients in datacenter vk-test.

After separate explicit approvals, MR26 was merged as `2bc44941a042e51278d0d60d97690ed3516cc526`, then tag `release-0.56.4` created at that SHA. The authorized tag triggered three automatic image builds in pipeline140829. Build3224497 built all images, but failed on the first API push: uploaded layers followed by registry `blob unknown to registry` for child manifest `sha256:10643981bdd2ddc862870f6451a63b8b4bc58cd13d8a69b42b6354c2a04961b7`. Buildx had exported an OCI manifest list and attestation. Updater/DNS push commands were not reached; deployment3224498 was skipped. Registry/attestation compatibility is the working explanation, not proven merely by the error. No deployment occurred.

Rendered Nomad planning through the canonical DNS endpoint succeeded: index0, one API/updater group, scheduler allocated all tasks. Proposed next recovery action is one new pipeline for the unchanged release tag with pipeline-only `BUILDX_NO_DEFAULT_ATTESTATIONS=1`; the user subsequently approved it, and pipeline140830 was created at the same SHA with the override. Pipeline140830 and build3224499 succeeded; deploy3224500 is manual and awaits separate play approval. Trace confirmed published tag `release-0-56-4`: API `sha256:5d1da6bd1c45fc39ac77dfbaf1bed6b6691e0011576264b4f1d9b80d531b5e90`, DNS `sha256:b6dfd16648af71618540852146be7d2066048873a32a37b0a9101f48ad38b4fd`, updater `sha256:3636247ff6e3f0bf9851f77c09d6756037a0709605c1d25fda653f500f92ff6a`. No attestation manifest lines were present in the successful trace. This does not change code, tag or persistent project variables. It would not fix future default tag pipelines, so permanent CI compatibility remains a separately tracked follow-up.

## Approved VK deployment verified (2026-10-14)

The user explicitly approved manual deployment job3224500. It succeeded in pipeline140830 using `release-0-56-4`. Nomad job `dynamic-inventory` is running in default namespace/datacenter vk-test; successful deployment31ef75f5, allocation `dc1803c6-bbda-da03-6f66-3618e1adbeb4` on `vk-ms1-nomad-agent-test-06` (`10.18.26.10`). API and updater tasks are running without failure.

Read-only GET checks returned200 through canonical route `http://dyninv.vk-test.youdo.local/` and direct allocation endpoint `http://10.18.26.10:28068/`. Inventory contains sixteen stands, sixteen docker aliases, sixty-four Nomad aliases with expected clients01-04/static addresses, zero SQL/windows hosts and no public-test. Direct port/placement is an observed allocation snapshot, not a permanent service address.

The updater starts its scheduler after30seconds, then first refresh after the69second interval (~99seconds after task startup). API's initial cache is empty; the populated runtime inventory, with no manual runtime PUT, supports at least one successful automatic refresh. Repeated refreshes were not independently confirmed: Nomad log API returned200empty, and fs/ls verified API/updater stdout/stderr files all zero bytes. A bounded read-only SSH attempt asyoudo to10.18.26.10 with BatchMode/ConnectTimeout8 timed out; no host-key bypass or remote change was made. Do not claim two observed automatic PUT200 events.

The requested preparation/release/deployment is complete. `automation-test-yandex/test_inventory.sh` still references the old Yandex endpoint; consumer cutover is outside this runtime request and remains a separate open action. Live SQL mapping remains unverified until VMs are available. Permanent CI registry compatibility is also open: the successful release used a pipeline-only no-attestation override.

## Task comment published (2026-10-14)

The user requested a completion comment and explicitly approved the prepared text in `/home/slnnk/ai-data/dynamic-inventory/task-comment.txt`. Posted comment `74-124668` to DevOps-896 as `a.solonenko`; the response matched the approved text. The comment records completed implementation/configuration/release/deployment, MR/pipeline/service links, verification and remaining limits. No issue state change was requested or performed.

## User-reported task closure (2026-10-14)

The user reported DevOps-896 closed. Treat VK dynamic-inventory recovery as accepted complete. The previously documented consumer-cutover, live-SQL and repeated-refresh limitations do not reopen this task and must not be represented as verified or completed work. Any further work requires a separate request; the independent permanent CI compatibility proposal remains separately tracked. No YouTrack state mutation or additional runtime action was performed for this closure acknowledgment.

## Changes

Created this audit/plan, linked it from the existing GitLab system map and tracked implementation in the central backlog. On 2026-10-14, recorded the user's task assignment DevOps-896 and subsequent consumer/stand/VM-name decisions here and in the central backlog/system map. Read-only local inspection confirmed `test_inventory.sh` and the consumer's `inventories/public-test` directory; this was not a cloud or live-endpoint check. The source audit date above remains unchanged. The later stage1 branch/local-edit approval is recorded above; publication was subsequently approved and completed as recorded above. Source credentials were not copied into notes.

## Risks

VK VM naming and one consumer are confirmed by the user, while live SQL VM/address mapping, any additional consumers and deployed runtime/route behavior remain unverified. Authorized automation-user authentication and live Compute reads succeeded locally. `public-test` is now excluded by the user-directed source check; historical dynamic inclusion was not tested. Static addresses and eight-client enumeration prevent treating this as an SDK-only change. Source has embedded Basic authentication material; do not quote it or copy it into new health checks. Use the existing secret mechanism for any new deployment binding. Local VK-only implementation is prepared and checked as recorded above; publication, merge, reviewed configuration, image publication and approved deployment are complete; consumer cutover, live SQL mapping and repeated-refresh observation remain outstanding.

## Portable lesson

none
