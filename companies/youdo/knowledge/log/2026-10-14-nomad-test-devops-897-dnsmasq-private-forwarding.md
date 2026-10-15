---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [dnsmasq, dns, vk-cloud, ansible]
---
# DevOps-897: repair Nomad client private DNS forwarding

## Task

User requested checking automation-services master, manually fixing DNS on VK Nomad clients and preparing an MR if Ansible lacks the correct configuration. Then asked what machine owns10.18.20.65. Runtime modification authorization is the explicit manual-fix request; repository training approvals remain separate.

## Context

automation-services checkout remains DevOps-892-restore-jenkins-on-vk with unrelated Jenkins/runner/inventory changes preserved. Fetch updated origin/master bffef350 ->71c37b2f. Target file inventories/vkcloud/group_vars/nomad_agent_test is identical to master. Previous DNS checks are in [live DNS investigation](2026-10-14-nomad-test-devops-897-vk-private-dns-check.md).

## Actions

Read project AGENTS.md, delegated multi-file Ansible audit, inspected fetched master. Used local helpers in /home/slnnk/ai-data/mssql-vk-dns/ for scoped Neutron GET discovery and parallel SSH probes/repairs. No credentials printed or saved.

Baseline probe across all8clients: configured local dnsmasq cannot resolve tested mcs.local names, Consul DNS works, direct10.18.20.65 UDP DNS times out, direct10.18.20.3 resolves. Agent01 also confirmed TCP53 to10.18.20.65 times out.

Manual repair replaced only server=/mcs.local/10.18.20.65 with server=/mcs.local/10.18.20.3 in /etc/dnsmasq.d/consul.conf. Pilot agent01 then seven remaining clients; validated complete config with dnsmasq --test --conf-dir=/etc/dnsmasq.d,.dpkg-dist,.dpkg-old,.dpkg-new and restarted only dnsmasq. Evidence: before.json, pilot.json, remaining.json under /home/slnnk/ai-data/mssql-vk-dns/.

## Findings

Neutron confirms10.18.20.65 is a service port owned by network:dns, not an ordinary VM. Port14b2e14d-375d-4967-9ae6-f120d70d3568, network shared_network996906a7-99ca-42e7-a916-632cc7eb6a28, domain mcs.local.; port IPs10.18.20.65/10.18.24.252/10.18.26.252, reported port status DOWN. Service port status alone is not proof of DNS service health. subnet-main10.18.20.0/24 enables private DNS and advertises10.18.20.3 as DNS nameserver.

10.18.20.3 is the company IPsec/BIND gateway (inventory vkcloud_ipsec_address), not the VK built-in DNS service itself. Repository gateway config forwards mcs.local to vkcloud_dns_servers=[10.18.20.65]. Current queries through gateway succeed; direct client-to-cloud DNS address does not. Gateway-to-upstream reachability was not directly tested; successful replies could be cached.

Master already contains the mcs.local rule introduced in bf93eb79, but client rule bypasses the working gateway. Minimal pending repository patch is a one-line change in inventories/vkcloud/group_vars/nomad_agent_test:22. General all-scope cloud DNS values and other service groups remain outside scope.

All8clients fixed and verified: agent01/.34,02/.38,03/.37,04/.30,05/.15,06/.10,07/.21,08/.35 (all10.18.26). dnsmasq active8/8; local configured DNS resolves Jenkins controller10.18.26.8 and agent10.18.26.26 on8/8; Consul nomad.service.vk-test.consul returns three master IPs on8/8; system getent resolves controller on8/8. No SQL VM recreation or container DNS test performed.

Pilot incident: helper initially placed backup consul.conf.devops897.bak inside conf-dir, causing systemd dnsmasq checkconfig to fail with illegal repeated keyword. Standalone dnsmasq --test had not loaded the complete config directory. Agent01 service temporarily failed; initial original-config rollback still failed because the backup was included. Moved backup outside conf-dir, corrected helper validation, re-applied and restored active service with all verification passing. Other clients were untouched until successful pilot. Backups now /var/backups/dnsmasq-consul.conf.devops897.bak on all8hosts. No ongoing outage recorded.

## Changes

Remote: one DNS rule and dnsmasq restart on8Nomad clients; per-host backups outside included directory. Local: generated helpers/evidence and nomad-private-dns.patch only; repository files untouched pending branch approval. KB/system map, service-addresses.env, TODO/index/sync bookkeeping updated.

Prepared artifact patch at /home/slnnk/ai-data/mssql-vk-dns/nomad-private-dns.patch; YAML parse and existing consul.conf template render passed, resulting server lines preserve Consul and general10.18.20.3 rules with mcs.local through10.18.20.3.

Branch proposal: automation-services / DevOps-897-fix-nomad-private-dns / origin/master71c37b2f. Async question sent before repo edits; user replied with the10.18.20.65 identity question, not approval. Branch not created. Proposed commit fix nomad private dns forwarding; MR title DevOps-897 Fix Nomad private DNS forwarding; source proposed task branch ->master. Proposed MR description: route mcs.local requests from VK Nomad clients through existing IPsec/BIND gateway, then task link only (Russian paragraph at publication). Publication not yet approved/performed.

## Follow-up: repository update and all Nomad nodes (2026-10-14)

User explicitly requested updating the repository and all Nomad nodes. Extended read-only checks to the three masters10.18.26.11/.12/.13. All3already use systemd-resolved127.0.0.53 with upstream10.18.20.3 and domain mcs.local; no dnsmasq installed. Private controller/agent names, Consul names and getent pass3/3. No master configuration change needed. Together with repaired8clients, normal DNS verified11/11. Evidence masters-verified.json.

User approved moving the existing local inventories/yandex/main.tf change through a three-way branch switch. Created DevOps-897-fix-nomad-private-dns from origin/master71c37b2f. switch --merge produced a conflict only in formatting the commented terraform/yandex-network path; both sides share active terraform/yandex-test-infra. User explicitly chose local formatting and approved conflict-index cleanup. Removed conflict markers preserving local formatting and ran git restore --staged only for this path; index empty, no unmerged paths, unrelated edits remain unstaged and outside task commit.

Actual repository diff: inventories/vkcloud/group_vars/nomad_agent_test:22 replaces only /mcs.local/10.18.20.65 with /mcs.local/10.18.20.3. Ansible _dnsmasq.yml --syntax-check passed (existing inventory-name warnings only), actual YAML parse/consul.conf template render passed, targeted git diff --check passed. Independent review: no blockers. CI review: first branch push skips all3Molecule jobs; inventory-only changes do not trigger nginx/consul automatic jobs, Nomad job is optional manual/allow_failure; no deployment job. No commit/push/MR yet; publication proposal remains fix nomad private dns forwarding / DevOps-897 Fix Nomad private DNS forwarding / task branch ->master, awaiting stage2approval.

## Approved publication and user merge (2026-10-14)

User explicitly answered Yes to the reviewed commit/push/MR action. Verified index empty before staging, staged only inventories/vkcloud/group_vars/nomad_agent_test, inspected actual staged diff (one insertion/one deletion), and committed fix nomad private dns forwarding as06d4821ac51d6dc3c3a2e8d89f3e5470e938770f. Pushed approved branch and created [MR1374](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1374), title DevOps-897 Fix Nomad private DNS forwarding, target master, assignee current user, squash=false, source branch removal=true. Description is the approved short Russian paragraph plus task URL only; exact remote description comparison passed.

Post-publication open-MR lookup stopped finding the MR because the user had already merged it at14:40:42MSK. Direct read-only MR GET confirms merged state, task SHA, exactly one changed path and merge commit454ef804d3d8ea67503f4f27d54037bcdc691b8c. Fetched master71c37b2f ->454ef804 and confirmed the mcs.local10.18.20.3 rule in origin/master. Agent performed no merge or deployment. MR-event pipeline140836 is skipped. Unrelated working-tree changes remain unstaged/preserved; task index empty after commit.

## Risks and limits

Manual fix is now persisted in merged master. Direct cloud DNS networking and other groups were not modified. Normal dnsmasq restarts briefly interrupt local DNS; pilot interruption disclosed and corrected. Future SQL VM registration/recreation and container DNS behavior remain outside this DNS repair verification.

## Portable lesson

none

### Gateway forwarding verified live, 2026-10-15

Read-only SSH to `youdo@10.18.20.3` (`ipsec-vm`) confirmed `/etc/bind/named.conf.local` and `named-checkconf -p` both define `zone "mcs.local"` with `type forward`, `forward only`, and sole upstream `10.18.20.65`. A direct UDP query from the gateway to that upstream returned authoritative `NOERROR`, `vk-ms1-sql-test.mcs.local A 10.18.26.17`, TTL86400. This verifies current gateway-to-cloud DNS reachability, beyond the earlier cache-only possibility. No configuration changed. Runner-origin queries through `10.18.20.3` succeed, while Windows DNS `.8`/`.9` still return `NXDOMAIN`.
