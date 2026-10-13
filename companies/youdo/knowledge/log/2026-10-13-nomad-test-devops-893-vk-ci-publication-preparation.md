---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [terraform, gitlab-ci, vk-cloud, DevOps-893]
---
# DevOps-893 VK CI and publication preparation

## Summary

User requested CI preparation and reviewed publication; explicitly excluded external application migration from DevOps-893. Added plan:vk-test and manual master-only apply:vk-test. Existing branch is approved; no new branch or worktree. Local implementation complete, publication awaits the second-stage supervised approval.

## Context

Repository ~/git/terraform; branch DevOps-893-recover-nomad-on-vk from origin/master34b581b. Existing vk-test copied and deployed under prior approvals. Preserve user-edited nomad.tf and Alloy version/resources. State terraform/vkcloud-terraform; eight jobs and disposable ceph-ssd lifecycle previously verified.

## Actions

- Extended .gitlab-ci.yml with 27 lines for two VK jobs using the existing image, dind runner tag, tflint and summary command. Plan runs automatically alongside existing plans. Apply restricted to master and manual. Apply follows the repository pattern by replanning on invocation rather than applying a saved artifact.
- Reused inherited group secrets NOMAD_TOKEN_VK_TEST and CONSUL_TOKEN_VK_TEST. Read-only metadata: both masked, unprotected, environment_scope=*. No values exposed or GitLab variable mutations.
- terraform fmt modified only alignment in vk-test/monitoring.tf, retaining user-selected values. No production/Yandex file edits.
- terraform fmt -check passed; terraform validate passed outside provider-socket sandbox. Existing hcl2.enabled deprecation warning remains unchanged. Full untargeted plan: No changes.
- GitLab project160 CI Lint dry_run/master valid=true, errors=[], expected manual apply:vk-test included. Three pre-existing warnings refer only to existing Yandex/public/production apply rules. No pipeline created by lint.
- Tflint unavailable locally; no claim of a local tflint run. CI retains existing tflint command/image pattern. Real runner execution follows publication, not lint.
- Fresh read-only review found no critical CI/backend/scope problems. Two literal password assignments match the existing tracked Yandex source and are retained under the user's explicit copy-as-is instruction; values not printed/persisted in notes or generated review artifacts. Optional source secret cleanup is outside this change.
- git diff --check passed. Exact publish scope: .gitlab-ci.yml plus 17 untracked vk-test files, 1200 new lines including provider lock, total18files. .terraform/, state, plans and secret files excluded. Manifest of explicit paths and hashes prepared under ai-data/nomad-vk-access/publication-manifest.json. User changes within the requested root retained for explicit publication review.

## Proposed publication

- Repository sysadmins/terraform, project160, default target master.
- Source DevOps-893-recover-nomad-on-vk; no existing open MR for this branch.
- Commit: restore nomad services in vk cloud.
- MR title: DevOps-893 restore Nomad services in VK Cloud.
- MR body prepared at ~/ai-data/nomad-vk-access/mr-description.md: one short Russian paragraph and task link only.
- Assignee a.solonenko; preserve project squash default_off and source-branch-removal false.
- Push will trigger existing plan jobs plus plan:vk-test. No automatic VK apply; master-only manual apply after merge. No merge, apply, production/Yandex deployment, GitLab variable write or external application migration covered by publication approval.
- Approval pending: no staging, commit, push or MR mutation executed. One second-stage yes covers explicit18paths staging, commit, branch push and MR creation together.

## Findings

CI uses the same Consul backend path as the converged manual deployment. New GitLab secrets are not needed. External applications/volumes and migration are explicitly outside DevOps-893.

## Changes

Local .gitlab-ci.yml and formatting of vk-test/monitoring.tf. Previous task vk-test local additions remain untracked. Updated existing system map, original plan scope and live backlog. No remote state changes.

## Publication approval and material CI discrepancy

User approved the proposed18file publication with Да. Before staging, current path hashes matched the generated manifest and the index was empty. Staged content matched that manifest, but its CI content included local disabling of four existing Yandex jobs that was not disclosed in the reviewed +27line summary. The exact staged stat was18files,1259insertions/32deletions, with CI59insertions/32deletions. The author failed to reconcile this stat with the reviewed scope before committing.

Local commit 22e451e8171320f914598aacda85773b49daccb6 (restore nomad services in vk cloud) created. Push/MR creation stopped immediately after inspecting actual committed CI diff. No external publication or pipeline created. Existing four Yandex plan/apply blocks are commented; VK and production plans remain, VK apply is master-only manual. This material CI effect needs renewed user approval before publication. Current MR description updated to disclose the disabled Yandex jobs.

Staged diff --check reported10trailing-whitespace findings in copied files. All exact lines were verified present in existing yandex-test counterparts and retained under explicit copy-as-is requirement. Earlier unstaged --check covered only tracked CI; it did not validate untracked copied files. No extra cleanup performed.

## Final publication

User reconfirmed publication with Да after disclosure of the disabled four Yandex jobs. Pushed22e451e8171320f914598aacda85773b49daccb6 to origin/DevOps-893-recover-nomad-on-vk; clean checkout tracks that remote branch. Created https://gitlab.youdo.sg/sysadmins/terraform/-/merge_requests/440 targetingmaster, title DevOps-893 restore Nomad services in VK Cloud, assignee a.solonenko, squashfalse. Readback description exact_match=true. No merge or apply performed.

Pipeline140765 started: https://gitlab.youdo.sg/sysadmins/terraform/-/pipelines/140765. Last read: running; plan:vk-test3222675running, plan:production3222676pending, apply:production3222677created (manual). apply:vk-test absent on task branch due master-only rule. CI result still pending; no pass claim. User asked why production plan ran: existing plan:production has no branch/path rules and is included on every branch push; retained existing behavior. No authorization to cancel pipeline or change production job rules was inferred from that question.

## Production plan history

User asked whether unrestricted production plan was introduced recently. git log -L for the plan:production block confirms predecessor plan lost only:master in commit5eda0c3 on2018-09-21, titled terraform plan on every push. It was renamed/expanded to plan:production in commitd21ae51 on2019-01-11, preserving no branch restriction. Last block changes c2ba9cc on2024-10-15 added tflint; this task did not modify the production block.

Fresh MR verify observed pipelines140765 and140766 both status=manual. This is pipeline status only; individual plan-job success is not yet independently read back.

## Actual VK CI plan and user-run apply

Read job3222675 plan:vk-test: success, duration37.48s, Terraform1.7.5, Nomadprovider2.3.1, plan0add/8change/0destroy. In-place updates span all eight jobs; all15unchangedattributes hidden per block, no changed attribute paths in trace. Fresh local1.9.4fullplan still No changes before the subsequent apply. Delegated in-memory trace/provider-source review found no injected terraform_version metadata in provider source; version-rootcause remains unproven. No raw trace or secret values saved.

User supplied https://gitlab.youdo.sg/sysadmins/terraform/-/jobs/3222681. This is apply:vk-test, status success, duration10.23s, Terraform1.7.5. Its own plan0add/8change/0destroy was applied; trace shows successful modifications. Agent did not trigger apply/retry/merge.

Official Terraform1.7.5 binary downloaded locally under ai-data/nomad-vk-access and SHA256 checked against official release manifest for reproduction. Reproduction plan failed before reading state because Consul hostname resolution stopped working locally, despite network escalation. Ordinary Nomad DNS probes also failed. No force-unlock, disabling locks, configuration change or infrastructure mutation attempted.

Direct read-only Nomad GET via known master10.18.26.11 succeeded after user-run CI apply: alloy8running, alloy-traces1, consul-exporter1, jaeger-agent8, kafka-schema-registry1, redis16, traefik2-service3, CSI8running. CSI also retains8historicalfailedallocations. Fresh plugin counts NodesHealthy8/Expected8 and ControllersHealthy8/Expected8.46runningallocations total. Sanitized summary in ai-data/nomad-vk-access/post-ci-apply-status.json. No new service addresses discovered.

CI apply and runtime health verified. Post-apply full-plan convergence cannot yet be claimed due local DNS failure; earlier CI/local plan discrepancy remains uncharacterized beyond the hidden eight in-place updates.

## YouTrack work comment

User explicitly requested adding a work summary to DevOps-893. Posted comment74-124648 and verified exact text by GET readback. Comment covers VK root/state, eight deployed jobs, exclusions, Vault integration, SSD lifecycle, manual CI, successful CI plan/apply and post-apply health, MR/job links, current convergence/DNS limitation and exclusion of external applications. Issue state unchanged. Prepared nonsecret comment text and publication receipt under ai-data/nomad-vk-access/youtrack-comment.md and youtrack-comment-result.json.

## User closure and waived follow-up

User explicitly said plan convergence verification is unnecessary and proposed differing Terraform versions as likely cause. This remains a hypothesis: local1.9.4 versus CI1.7.5; no further reproduction or convergence checks required. Updated existing YouTrack comment74-124648 to remove the outstanding-check paragraph and state the version hypothesis; exact readback verified. Removed the live follow-up item from ~/ai/TODO.md. User then reported closing DevOps-893; recorded as user-reported closure, without changing YouTrack status through the agent. No open DevOps-893 work remains.
