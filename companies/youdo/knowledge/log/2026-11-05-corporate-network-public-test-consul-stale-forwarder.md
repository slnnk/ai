---
system: corporate-network
status: verified
checked: 2026-11-05
tags: [dns, bind, consul, vpn]
---
# VPN BIND public-test.consul forwards to an unresponsive DNS server

## Task
Diagnose why nomad.service.public-test.consul fails through the system resolver while direct queries to 172.28.0.8 and 172.28.0.9 succeed. Investigation only.

## Context
User identified VPN host 172.28.0.200; root SSH confirms sc-gateway2.youdo.corp. Its VPN interface is 172.30.63.1. Local systemd-resolved routes consul through that VPN DNS server.

## Actions
Read-only DNS comparisons from the workstation and SSH probes on the VPN gateway. Inspected listeners, the relevant BIND configuration and named-checkconf. No remote state changes.

## Findings
- Workstation queries to 172.28.0.8 and 172.28.0.9 both return NOERROR and A 10.18.26.63 in about 27 ms.
- Queries to 172.30.63.1 time out over UDP and TCP for this name; systemd-resolved eventually returns SERVFAIL. The same VPN DNS answers nomad.service.vk-test.consul and ya.ru.
- named listens on 172.30.63.1:53, 172.28.0.200:53 and 127.0.0.1:53.
- /etc/bind/named.conf.local:21-25 defines public-test.consul as a forward zone with forward only and the sole forwarder 10.16.26.65.
- From the gateway, direct UDP53 queries to 10.16.26.65 time out, both 172.28.0.8 and 172.28.0.9 return A 10.18.26.63, and local BIND at 127.0.0.1 times out.
- named-checkconf exits successfully. This is a forwarding destination failure, not a syntax error. Why 10.16.26.65 does not answer was not investigated.

## Changes
Only this knowledge log and the central backlog proposal. No infrastructure or repository task configuration changed.

## Status and risks
Diagnosis complete. Proposed replacement of this zone's forwarders with 172.28.0.8 and 172.28.0.9 is recorded in [central TODO](../../../../TODO.md); implementation and BIND reload require explicit user approval. No background diagnostic operations remain.

## Portable lesson
none

## Canonical Ansible source audit

Follow-up requested by the user on 2026-11-05. Applied the gitlab-workflow investigation workflow. Existing checkout /home/slnnk/git/automation-services has unrelated local changes, preserved. Fetched origin without switching branches; fresh origin/master is 0c6a8b1c (2026-11-02), while checkout HEAD is ff104e33. Relevant gateway role, playbook and group variables have no diff against origin/master.

- inventories/prod_selectel/hosts:143-147 puts sc-gateway2.youdo.corp (172.28.0.200) in msk3_gateway, a child of gateway.
- gateway.yml:19-30 applies role bind to gateway hosts.
- inventories/prod_selectel/group_vars/gateway:89-91 supplies bind_forward_zones public-test.consul with 10.16.26.65; the same stale address is present in fresh origin/master.
- roles/bind/templates/named.conf.local.j2:1-6 renders that dictionary directly as forward-only zones. roles/bind/tasks/main.yml:29-35 writes /etc/bind/named.conf.local and notifies restart bind. The handler restarts bind9.
- Thus the live faulty zone matches canonical Ansible input: the problem is stale inventory data, not a template transformation or proven failure to apply the role. Reapplying the unchanged role would retain the broken destination.
- inventories/vkcloud_public_test/group_vars/nomad_agent_test:23 already uses /public-test.consul/10.18.26.63. Direct use of that destination from the VPN gateway has not been checked; successful gateway probes of 172.28.0.8 and 172.28.0.9 remain the verified alternative.
- inventories/yandex/group_vars/ipsec:177-179 also contains 10.16.26.65, but applicability/runtime state of that separate inventory was not investigated.

The central backlog proposal now includes fixing canonical gateway inventory before applying the scoped role. This investigation grants no repository edits or deployment permission.

## DevOps-907 repository preparation proposal

User created DevOps-907 and requested repository changes. Read-only gateway checks confirm direct 10.18.26.63:53 returns NOERROR/A 10.18.26.63 over both UDP and TCP. This validates using the destination already declared by the VK public-test inventory instead of chaining through 172.28.0.8/.9.

First supervised gate proposal: existing /home/slnnk/git/automation-services checkout; new branch DevOps-907-fix-public-test-dns from origin/master 0c6a8b1c; change only inventories/prod_selectel/group_vars/gateway public-test.consul forwarder from 10.16.26.65 to 10.18.26.63. Approval pending; no task repository edits or branch mutations performed. Unrelated checkout modifications remain preserved. Publication and runtime apply are separate stages.

## DevOps-907 approved local implementation

The user explicitly approved the proposed repository, branch, base and one-line change. Created DevOps-907-fix-public-test-dns from origin/master 0c6a8b1c in the existing checkout. Changed only inventories/prod_selectel/group_vars/gateway:91 from 10.16.26.65 to 10.18.26.63. All pre-existing unrelated tracked/untracked changes were preserved; the index is empty.

Validation: YAML parses, comparison against HEAD confirms only the intended zone forwarder differs, and the complete named.conf.local Jinja template renders successfully with the updated inventory. Scoped git diff --check passes. Whole-checkout diff --check reports pre-existing trailing whitespace in unrelated roles/gitlab-runner/templates/cron-docker-clean.j2; left untouched. Direct DNS from the gateway was already verified over UDP and TCP. No Ansible apply, service restart, stage, commit, push or MR occurred. No background operations remain.

Local preparation is complete. Publication and runtime application remain subject to their separate approvals; see central TODO. The earlier pending first-gate proposal is superseded by this explicit approval and implementation.

## DevOps-907 publication proposal

Prepared ready MR proposal and snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-907/automation-services/. Repository sysadmins/automation-services; source DevOps-907-fix-public-test-dns; target master; commit and MR summary: fix public-test consul dns forwarder (MR title prefixed DevOps-907). Description is a short Russian problem/change paragraph plus the task link. Read-only GitLab inspection: project216, default master, no matching open MR, assignee a.solonenko, squash default off; recent source deletion preferences true.

Actual reviewed task diff is only gateway inventory 10.16.26.65 to 10.18.26.63. Empty existing index; unrelated checkout edits preserved and bound by snapshot. Scoped whitespace check passed; earlier YAML/template/UDP/TCP checks remain applicable.

CI review: complete .gitlab-ci.yml contains only Molecule nginx/consul/nomad tests and no includes or deployment/release steps. First push of a new branch excludes the three jobs. Inventory-only changes do not automatically select role tests; optional manual molecule-nomad can be exposed for other pipeline contexts. No manual CI jobs or runtime actions proposed.

Second supervised approval pending. No commit, push or MR creation performed. No background operations remain.

## DevOps-907 approved publication outcome

User explicitly confirmed the complete second-stage publication proposal. Snapshot check matched before staging. Staged only inventories/prod_selectel/group_vars/gateway, inspected the entire index and committed cedd1283487a6f49677c18ad53a5fd9325748fc6 with the approved message. Resulting commit contains one insertion and one deletion in that file only. Unrelated tracked and untracked modifications were preserved; index is empty.

Initial sandbox push failed during DNS resolution; read-only ls-remote outside the sandbox confirmed no source branch before retry. Approved push outside the sandbox succeeded. Created ready [MR !1388](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1388), source DevOps-907-fix-public-test-dns to master, assigned a.solonenko, squash false, remove-source-branch true. Creation helper verified identity/content/SHA; a separate verify invocation confirmed the expected SHA, title, description and source/target. [Pipeline142384](https://gitlab.youdo.sg/sysadmins/automation-services/-/pipelines/142384) is skipped. No manual jobs triggered.

Publication complete. No merge, Ansible apply or BIND restart performed; the DNS runtime issue therefore remains until separately approved deployment. All task background commands finished. Earlier pending publication status is superseded by this approval and verified outcome; remaining work is represented in central TODO.

## DevOps-907 user-reported merge and approved manual runtime fix

The user reported MR !1388 merged and explicitly requested a manual fix on the VPN server. Read-only preflight on 172.28.0.200 confirmed the old zone still present, named active, valid configuration and successful direct UDP query to 10.18.26.63.

Applied one guarded remote operation after describing the exact change: saved /etc/bind/named.conf.local.DevOps-907.20261105T143236.bak, replaced only the public-test.consul zone forwarder 10.16.26.65 with 10.18.26.63, ran named-checkconf, successfully reloaded with rndc reload and cleared the exact name using rndc flushname nomad.service.public-test.consul. The operation had backup restoration on validation/reload failure; rollback was not needed. named remained active. No full Ansible playbook or unrelated role was executed.

Post-change workstation checks: queries through VPN DNS 172.30.63.1 over UDP and TCP return NOERROR/A 10.18.26.63; default dig through systemd-resolved also returns NOERROR/A 10.18.26.63; getent ahostsv4 returns the same address. Control nomad.service.vk-test.consul returns its expected three master addresses. The original DNS symptom is resolved on the observed VPN/system resolver path. MR merge is user-reported, not independently re-fetched during this runtime change.

Task complete, central TODO entry closed. All task commands finished; no background operations remain. Earlier pending runtime/merge statuses are superseded by the reported merge and verified manual repair above. The backup remains on the gateway for recovery if needed.

## User-approved task comment

The user explicitly requested posting their exact Russian text to DevOps-907. Created YouTrack comment 74-125183 and GET-verified exact text equality. No task state change was requested or performed. The central backlog remains closed based on the completed repair. All commands completed.
