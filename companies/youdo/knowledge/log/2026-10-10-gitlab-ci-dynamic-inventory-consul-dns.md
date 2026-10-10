---
system: gitlab-ci
status: verified
checked: 2026-10-10
tags: [gitlab-runner, docker, dns, consul, dynamic-inventory]
---
# Dynamic inventory job 3217892: Consul DNS forwarding timeout

## Task

Diagnose [GitLab job 3217892](https://gitlab.youdo.sg/sysadmins/dynamic_inventory/-/jobs/3217892) using read-only GitLab and SSH checks. The user supplied runner access `ssh root@172.28.0.171`; no remote changes were authorized.

## Context

- Project: `sysadmins/dynamic_inventory`.
- The failed job ran on runner `172.28.0.172`; comparative checks used runners `172.28.0.171` and `.172`.
- General-purpose Docker runners are managed from `/home/slnnk/git/automation-services`.
- Related map: [Docker runner context](../systems/gitlab-ci/dynamic-kubernetes-runners.md).

## Actions

- Collected GitLab job metadata and trace through the existing read-only collector `~/ai/current/skills/android-dig/scripts/gitlab_job.py`; authentication comes from `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env`, with no secret values recorded.
- Read runner host and Docker DNS configuration; compared DNS replies from `172.28.0.6`, `.7`, `.8`, and `.9` using UDP and TCP queries.
- Checked Nomad `GET /v1/status/leader` from the host after resolution through the working host DNS servers.
- Read automation-services inventory and BIND role configuration without editing repository files.

## Findings

- The failure occurs when resolving `nomad.service.yandex-test.consul`, before inventory can query Nomad.
- Both checked runners use `172.28.0.8` and `.9` in Docker daemon DNS configuration, while host resolution uses `172.28.0.6` and `.7`.
- Queries to `.8` and `.9` for `nomad.service.yandex-test.consul` time out over both UDP and TCP. The same servers resolve `gitlab.youdo.sg` with `NOERROR` in about 60 ms. This identifies a failure affecting the Consul-zone resolution path rather than a complete DNS-server outage.
- `.6` and `.7` resolve the Nomad service to `10.16.28.11`, `.12`, and `.13`. Host `GET /v1/status/leader` succeeds; Nomad control-plane reachability is verified through that path.
- `inventories/prod_selectel/hosts:108` and `:109` identify `.6` and `.7` as `ipa6.youdo.corp` and `ipa7.youdo.corp`. The inventory does not identify `.8` and `.9` hosts.
- `inventories/prod_selectel/group_vars/gateway:67` still configures `yandex-test.consul` forwarders `10.16.26.11`, `.12`, and `.13`. That configuration applies to `sc-gateway2.youdo.corp` (`172.28.0.200`), not an established mapping to `.8` or `.9`.
- **Hypothesis:** a stale conditional forwarder or an unavailable upstream DNS path after Yandex test subnet recovery explains the `.8`/`.9` timeouts. The gateway configuration supports this possibility but does not establish the live `.8`/`.9` forwarding configuration.
- BIND role control points are `/etc/bind/named.conf.local` for zones, `/etc/bind/named.conf.options` for options, and `/etc/default/named` for runtime arguments.

### User DNS correction and first verification (about 15:18 MSK)

- The user confirmed that DNS servers `172.28.0.8` and `.9` run Windows and reported changing the `yandex-test.consul` forwarding targets to the new addresses. This is a user-performed external change; the agent made no DNS changes.
- Subsequent read-only checks from both runner hosts `.171` and `.172` still timed out after 3 seconds for UDP queries to each Windows DNS server for `nomad.service.yandex-test.consul`.
- Host DNS resolution and Nomad leader GET remain functional; the endpoint returned leader `10.16.28.11:4647`.
- The initial post-change checks do not demonstrate recovery. Longer and TCP DNS checks are pending.
- The old BIND gateway configuration is a separate repository finding and is not a verified direct cause on the Windows servers.

### Final read-only verification (15:18:47–15:18:59 MSK)

- Both runners produced the same result: UDP queries to `172.28.0.8` returned `SERVFAIL` after approximately 11–12 seconds; TCP queries to `172.28.0.9` returned `SERVFAIL` after approximately 11.8 seconds. Longer waits revealed a resolver failure response rather than only the earlier client-side timeout.
- Both Windows servers still resolved `gitlab.youdo.sg` to `89.169.136.178`.
- Direct `dig @10.16.28.11 -p 8600 nomad.service.yandex-test.consul` returned `NOERROR` and all three records `10.16.28.11`, `.12`, and `.13` in 4–8 ms from both runners. Consul DNS answers are available through the direct 8600 path.
- The Windows forwarding path remains unsuccessful after the user's correction. **Hypothesis:** the target DNS listener on UDP/TCP 53, firewall/routing from Windows, or conditional-forwarding configuration may prevent Windows from reaching a working upstream. No check establishes that destination port 53 is broken, and direct port 8600 success alone does not verify Windows forwarding on port 53.

### Direct upstream port comparison

- From runner `.172`, default-port UDP `dig @10.16.28.11`, `.12`, and `.13` for the Nomad name immediately returned `connection refused` on all three addresses. The direct Consul query on `.11:8600` had succeeded.
- A port mismatch is verified for the direct runner route: the new servers answer Consul DNS on 8600, while UDP 53 refuses queries. The exact Windows-to-upstream route remains untested; refusal alone does not distinguish a missing listener from an explicit firewall rejection.
- Windows DNS conditional forwarders normally target port 53. Candidate remediation is a DNS listener/proxy on the new servers' port 53 forwarding to Consul 8600, or forwarding the zone through an accessible resolver that already serves it, such as working FreeIPA `.6`/`.7`. These are proposals only; no remote change was performed or authorized.

### Confirmed recovery gap: missing dnsmasq on the new Nomad masters

- Read-only SSH checks identify `10.16.28.11`, `.12`, and `.13` as `yc-a-nomad-consul-master-test-01`, `-02`, and `-03`.
- All three have active Consul with external TCP/UDP `*:8600`, but `dnsmasq` is inactive. On `.12` and `.13`, `dpkg-query -W dnsmasq` exits 1: the dnsmasq package is absent. On `.11`, `/etc/dnsmasq.conf` and `/etc/dnsmasq.d/*.conf` are absent.
- `systemd-resolved` is active and provides TCP/UDP port 53 only on loopback `127.0.0.53`/`127.0.0.54`. It does not supply the external DNS listener required by Windows forwarding.
- `.11` has INPUT policy ACCEPT and no NAT 53 redirection entries. Combined with the missing proxy and available Consul 8600, this confirms an absent external port 53 DNS service rather than an established packet-drop cause.
- Repository evidence verifies the intended mechanism: `automation-services/cluster_docker.yml:10` includes role `dnsmasq`; `inventories/yandex/group_vars/nomad_master_test:18` chooses `consul.conf`; `roles/dnsmasq/defaults/main.yml:14` sets `/consul/127.0.0.1#8600`. The role renders `/etc/dnsmasq.d/consul.conf`, providing the intended dnsmasq port 53 to local Consul 8600 path.
- **Confirmed cause:** the recovered Nomad master servers lack the expected dnsmasq DNS proxy on port 53. Updating Windows forwarder IPs alone cannot restore that missing service. Restoring the intended dnsmasq role/configuration on the recovered masters is the concrete repair proposal; it requires explicit authorization and was not performed.

## Changes

### Terraform inventory investigation and temporary local inventory

- Read-only comparison: local yandex-tf branch commit `43ff422` is clean; fetched `origin/master` is `5958abf`. Relevant inventory integration files have identical content at both commits.
- `test-infra/ansible-hosts.tf:157` creates `ansible_host.nomad_master_test` from `local.nomad_master_ips`; `locals.tf:12` obtains the legacy `nomad_master_ips` output from `terraform/yandex-test-infra`. Current state has 12 legacy `ansible_host` resources with old `10.16.26.x` addresses.
- The recovery module separately publishes `recovery_hosts` with new `10.16.28.x` addresses and groups `nomad_master_test`/`cluster_docker`. No `ansible_host` resource consumes that output, so the Terraform inventory provider does not generate the new masters.
- The user's locally edited automation-services inventory backend was `terraform/yandex-dev-k8s-a` during the Helm schema failure, superseding the earlier checked-in network-backend observation. That Kubernetes state has no Ansible resources; stored Helm schema 1 conflicts with provider 3.3.0 schema 2. The user subsequently changed the backend to test-infra, whose legacy inventory remains unsuitable for recovered masters.
- Proposed Terraform branch `AP-2347-recovery-ansible-inventory`, repository yandex-tf, base `origin/master`; the user explicitly deferred that repair. Branch creation and repository changes were not approved or performed.
- The user requested a temporary inventory for the three masters. Created local artifact `/home/slnnk/ai-data/gitlab-diagnostics/nomad-dnsmasq-inventory/hosts.yml`, with `cluster_docker` containing child `nomad_master_test` and hosts `yc-a-nomad-consul-master-test-01/02/03` pointing to `10.16.28.11/12/13`. Adjacent `group_vars` symlinks the existing `automation-services/inventories/yandex/group_vars`.
- Read-only inventory graph confirms three hosts. Playbook `--list-hosts --list-tasks` confirms only eight dnsmasq tasks on those hosts with `--tags dnsmasq --skip-tags always` and explicit Docker prompt variables. No actual remote playbook run occurred.

Initial prepared command (superseded; failed when run by the user):

```bash
cd /home/slnnk/git/automation-services
ansible-playbook -i /home/slnnk/ai-data/gitlab-diagnostics/nomad-dnsmasq-inventory/hosts.yml cluster_docker.yml \
  --limit nomad_master_test --tags dnsmasq --skip-tags always \
  -e '{"nomad_client_docker_user":"nomad","nomad_client_docker_pass":""}'
```

The initial use of `--skip-tags always` was incorrect: it skipped implicit fact gathering as well as the Vault pre-task. Listing tasks did not catch the missing runtime facts. This command must not be reused.

### User run failed on missing facts; standalone playbook prepared

- The user executed the initial command. All three hosts failed rendering the resolver template because `ansible_default_ipv4` was undefined, with recap `ok=4 changed=3` before failure.
- According to the verified role task order, the partial user run installed dnsmasq, stopped/disabled systemd-resolved, and removed the `/etc/resolv.conf` symlink before the resolver-template failure. Recovery is not complete; no agent remote action occurred.
- Created standalone local playbook `/home/slnnk/ai-data/gitlab-diagnostics/nomad-dnsmasq-inventory/dnsmasq.yml`: targets `nomad_master_test`, `remote_user: root`, `become: true`, `gather_facts: true`, and only absolute role `/home/slnnk/git/automation-services/roles/dnsmasq`. No Vault pre-tasks, base_linux roles, or Docker prompts are included.
- `--syntax-check`, `--list-hosts`, and `--list-tasks` passed: three hosts and eight dnsmasq role tasks. This verifies local structure only; the corrected remote run has not been performed by the agent.

Corrected prepared command (requires no skip-tags):

```bash
ansible-playbook \
  -i /home/slnnk/ai-data/gitlab-diagnostics/nomad-dnsmasq-inventory/hosts.yml \
  /home/slnnk/ai-data/gitlab-diagnostics/nomad-dnsmasq-inventory/dnsmasq.yml
```

The role installs/starts dnsmasq, disables systemd-resolved, and replaces the host resolver configuration using existing group variables. These remote effects still require explicit approval for agent execution.

### Standalone rerun: missing-file conditional and local recovery pre-tasks

- The user's standalone rerun failed on all three hosts because `/etc/resolv.conf` was absent after the interrupted first run. The role tests `resolv_conf_stat.stat.islnk` without a default; Ansible stat omits that key when the file does not exist.
- Updated only the temporary standalone playbook: pre-tasks stat `/etc/resolv.conf` with `follow: false`, then render the repository resolver template only if `stat.exists` is false, owner/group root and mode 0644. This avoids changing repository task files.
- Syntax/list-hosts/list-tasks passed: ten tasks and three hosts. The rerun command remains the standalone command above, without `--tags` so recovery pre-tasks run.
- A further local review identified `ansible_managed_file` as a template dependency declared in repository-root `group_vars/all/base-vars`, outside the temporary playbook's inventory variables. Ensure the temporary playbook supplies that non-secret variable before the next remote run. Restoring the final self-address resolver before dnsmasq starts can also affect an uncached apt update; this is a potential sequencing concern, not a verified additional failure.
- The temporary playbook now explicitly defines `ansible_managed_file: '# Managed by Ansible'`; syntax-check passed again. The same standalone command is ready for the user's rerun; no agent remote changes occurred.
- The repository missing-file conditional repair is deferred: use a safe default for `stat.islnk` after a separate code-change request. No agent remote repair occurred.

- Local knowledge-base log, existing runner map, and central backlog updated.
- No repository task files, runner configuration, GitLab job, or remote service were changed by the agent. The user's partial remote playbook changes are recorded above.

## Open items

### Runtime recovery verified (2026-10-10 15:51:31 MSK)

- The user successfully applied the temporary standalone playbook; the agent then performed read-only verification.
- All three masters have active dnsmasq and Consul. dnsmasq listens externally on TCP/UDP `0.0.0.0:53` and `[::]:53`; Consul continues serving 8600. `/etc/resolv.conf` points to each master's own `10.16.28.11`, `.12`, or `.13` address.
- From both runners `.171` and `.172`, queries through both Windows DNS servers `.8` and `.9` for `nomad.service.yandex-test.consul` return `NOERROR` with all three current addresses in 0–8 ms.
- Nomad leader GET succeeds and returns `10.16.28.11:4647`. The DNS runtime incident is resolved; the corresponding DNS restoration backlog item is closed.
- No GitLab job retry, deployment, or remote mutation was performed by the agent. Job rerun success was not checked.

Deferred Terraform recovery inventory integration and the repository dnsmasq missing-file conditional correction remain tracked in `~/ai/TODO.md`. No agent-performed repository changes occurred.

## Portable lesson

none

## Approved YouTrack comment

The user reviewed the AP-2347 comment, requested first-person singular wording, and removed the temporary-inventory, verification, and deferred-work details. The revised text was explicitly approved and published as comment `74-124638`; a GET verified an exact text match.

Approved text:

```text
Восстановил DNS-разрешение зоны `yandex-test.consul`: обновил conditional forwarders на Windows DNS и установил dnsmasq на трёх восстановленных Nomad/Consul masters.
```

Issue: https://youtrack.youdo.com/youtrack/issue/AP-2347

## Approved service restoration comment

Read-only trace review confirmed Terraform job `3217896` (`apply:yandex-test`) succeeded with 11 added Nomad jobs, 0 changed and 0 destroyed. Because `detach = true`, this proves registration, not runtime health of all eleven jobs. Dynamic inventory job `3217893` succeeded with one healthy allocation and a successful deployment. Sources:

- https://gitlab.youdo.sg/sysadmins/terraform/-/jobs/3217896
- https://gitlab.youdo.sg/sysadmins/dynamic_inventory/-/jobs/3217893

The user approved the second AP-2347 comment after replacing the redeployment wording with deployed. Published comment `74-124639`; a subsequent GET verified exact text. Approved text:

```text
Восстановил в тестовом Nomad задания сервисов Redis, Redis Autotest, Traefik, OAuth2 Proxy, Kafka Schema Registry, Jaeger Agent, Alloy, Alloy Traces, Consul Exporter, CSI-плагина и Selenoid iOS GGR через Terraform. Развернул dynamic_inventory.
```
