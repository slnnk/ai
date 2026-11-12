---
system: nexus
status: verified
checked: 2026-11-11
tags: [nexus, nomad, gitlab-ci]
---
# MR1371 merge readiness review

## Task
Explain automation-services MR1371 and assess whether it can be merged. Investigation only; no merge, repository edits, CI run or deployment authorized.

## Findings
Live GitLab GET confirms open non-draft MR, source DevOps-890-nexus-docker-auth at f4018c2bf2e1d08cb2bf4c739bf64b3b667c4853, target master at 6d467c2e196f347bfe500bb96f0af0ce4e03f111. GitLab reports mergeable without conflicts, resolved blocking discussions and no approvals. Scope is four files: common Nomad Nexus auth defaults/assert/template and Docker28.5.2 DinD pin in three Molecule jobs. CI has no deployment jobs.

Latest pipeline140673 is skipped; previous pipeline140665 failed before tests. User declined the manual final-revision test in the [original work log](2026-10-12-nexus-automation-services-nomad-docker-auth.md). No full Molecule pass claimed.

NEXUS_DOCKER_PASSWORD must be supplied by the Ansible controller for role executions that write Docker auth. Injection into every consumer has not been verified. Missing value triggers the new assertion before Docker config writes.

Current master already added no_log:true and diff:false to the template task. Local read-only merge-tree simulation yields duplicate no_log:true keys because MR adds the same key before the existing when. Live master task bytes were confirmed identical to the local simulation target through GitLab GET. Values agree, but deduplication before merge is recommended; retain diff:false. Other three affected master files are unchanged since the MR base.

## Validation
Exact source inspected locally. Source diff whitespace check passes. Jinja fixture renders valid JSON both with and without Nexus auth and preserves GitLab registry credentials. No full Ansible/Molecule execution this session. All read-only network processes completed.

## Status and risks
Review complete. Recommend removing the duplicate key and ensuring controller secret injection before merging/applying. Existing central [MR1371 review/merge backlog item](../../../../TODO.md) remains open; no status change, merge or external mutation performed. No separate implementation proposal was executed.

## Portable lesson
none

## Live Vault delivery verified by user-run checks

User supplied complete successful output from the temporary read-only Ansible check for both inventory snapshots. VK inventory reads its Vault documents and verifies Nexus password binding on three nomad-consul-master-test hosts and eight nomad-agent-test hosts. Public-test reads three Vault documents and verifies the binding on public-test-linux. Every host reports changed0, failed0 and unreachable0. The assertion checks nonempty nomad_client_nexus_docker_pass and equality to vault_secrets['yandex'].nomad_client_nexus_docker_pass without printing credentials. This verifies Vault delivery from the user's Ansible controller for both inventories; it does not claim deployment of Docker config or verification from AWX/Jenkins.

Closed the actual Vault delivery TODO as completed. The public-test warning about unmatched nomad_master_test is expected because that inventory has only nomad_agent_test; public-test-linux was checked successfully. Existing VK inventory naming warnings did not prevent the checks. MR1371 source integration and requested Vault validation are complete; Molecule restoration remains closed without repair at user direction. The independently mentioned Runner171/172 persistence task remains open. No agent-launched commands or background operations remain.

## User-run live Vault check blocked by access

User supplied a screenshot of the temporary read-only playbook execution against inventories/vkcloud/hosts. CLI token lookup succeeds, but Vault reads fail and the existing rescue classifies permission denied for http://vault.service.vk-test.consul:8200 secret/ansible/*. Nexus binding assertion is not reached. Exact access cause (expired token, wrong cluster or insufficient policy) is not established. The second public-test command was chained with && and therefore did not run. Suggested next diagnostic is the existing scripts/vault-login.sh with the explicit VK endpoint and clearing any overriding VAULT_TOKEN, followed by rerunning both checks; repeated denial requires inspecting token capabilities without exposing the token. No login, token mutation, ACL edit or remote apply performed by the agent. Existing live-delivery TODO stays open.

## User decision: no Molecule restoration work

On November11 the user explicitly stated that the Molecule failures do not matter for this task and that they will request restoration if needed. Closed the compatibility follow-up in central TODO without repair. Preserve failed pipeline evidence; do not interpret this as passing tests or reopen Molecule restoration from historical failures. Scope: Molecule restoration only. The separate real Vault delivery verification remains unchanged. No further CI diagnosis, dependency changes or retry authorized or performed.

## User merge and final CI outcome verified

User reported merging MR1371. GitLab GET verifies merged state, merge commit a8b70e0177d581f77f72aa5e1312dabae2899ef3 and current master at that SHA, merged November11 at21:47:05MSK. Pipeline142819 finished failed. Nomad3294285 and Consul3294284 reach molecule test but fail the lint stage with ImportError: cannot import name 'render_group' from 'rich.console'. Nginx3294283 fails the dependency stage while resolving community.docker through the Galaxy v3 collection index, exit250. These are observed toolchain failures; no role test success claimed. No dependency fixes, retries or runtime changes performed in this follow-up.

Central TODO merge item is closed. The historical missing-image retry item is superseded by the current toolset compatibility failure, preserving its history and source. Added the unverified real Vault delivery for both VK inventories as a scoped follow-up; fixture checks do not establish a live Vault read or runtime apply. Runner171/172 DOCKER_AUTH_CONFIG persistence remains an independent existing item, outside MR1371. All local commands and CI jobs observed in this follow-up are terminal; no background operations remain.

## Approved publication completed on November 11

User explicitly approved the concrete publication proposal by replying Yes. Snapshot check matched before staging. Staged exactly the four local correction paths on top of the approved master merge. Complete index comparison against origin/master confirmed exactly seven approved MR paths; all other staged changes were imported master content, not unrelated local work. Reviewed the actual staged net diff; whitespace checks passed.

Created merge commit 41e5e18247993a211fcd67007ac43ecb4784a93b, parents f4018c2bf2e1d08cb2bf4c739bf64b3b667c4853 and d1b63f7081645161e82d9d2b5247e7679ad5ac6f, subject use vault nexus credentials for vk nomad hosts. Pushed the approved source branch using strict verified SSH HostKeyAlias. Updated existing MR1371 description from the approved body file, preserving title, source/target, assignee, ready state, squash false and source deletion setting. Helper verified exact remote SHA and metadata; independent GET verified the seven-file MR scope. No merge into master, release or deployment performed.

Pipeline142820 skipped. Push pipeline142819 is running with molecule-nginx3294283, molecule-consul3294284 and molecule-nomad3294285 all running at the last GET. This is not CI success. Status receipt: ~/ai-data/gitlab-workflow/mr1371-vk/published-status.json. Check or cancel via https://gitlab.youdo.sg/sysadmins/automation-services/-/pipelines/142819; no local background commands remain. Local merge is complete, index empty, and unrelated file hashes still match the saved snapshot. Actual Vault key retrieval/controller delivery remains unverified. Existing central MR1371 review/merge backlog remains open.

## Approved master integration and corrected VK bindings prepared

User explicitly approved local master integration on the existing MR1371 branch, removal of mistaken yandex bindings and adaptation of both VK inventories. Executed git merge --no-commit --no-ff origin/master d1b63f70 after saving the overlapping task work and temporarily restoring unrelated inventories/yandex/main.tf to HEAD; restored its original bytes afterward. Merge has no conflicts but remains in progress, with imported master changes staged and task corrections unstaged, pending publication approval. No merge commit or push performed. Do not stage unrelated work or abort/discard the prepared merge without discussing its preservation.

Final local corrections: bind nomad_client_nexus_docker_pass to vault_secrets['yandex'].nomad_client_nexus_docker_pass in vkcloud nomad_master_test and nomad_agent_test and vkcloud_public_test nomad_agent_test. Public-test Nomad group loads [vkcloud_public_test, common, yandex], retaining existing namespaces. Legacy yandex group_vars match master again. Updated assertion message and removed the merge-produced duplicate no_log while retaining master no_log:true/diff:false.

Actual Ansible Templar fixtures pass for all three groups, with VK Vault address, yandex in effective namespace list, Vault credential overriding conflicting environment, and existing registry entry retained. Where GitLab registry variables are absent from group_vars, the fixture supplies the existing cluster_docker.yml vars_prompt inputs; this is not verification of unattended execution. Strict YAML uniqueness, scoped diff check and unrelated local file hash checks pass. No live Vault read/runtime apply or full Molecule run. Proposal/body/snapshot prepared under ~/ai-data/gitlab-workflow/mr1371-vk/. Proposed single merge commit including corrections: use vault nexus credentials for vk nomad hosts. MR title/source/target retained; body explains final VK/Vault behavior. A subsequent push can run all three role Molecule jobs because merged master changes include their role paths; CI contains tests only, no deployment jobs. Publication approval remains pending. No background operations remain.

## Correct inventories identified from current master

User identified inventories/vkcloud and inventories/vkcloud_public_test as the intended targets. Fetch refreshed origin/master to d1b63f7081645161e82d9d2b5247e7679ad5ac6f without changing the checkout. The old MR source lacks the public-test inventory and the current VK Nomad groups; this caused the earlier misleading checkout-only conclusion. Current master has VK nomad_master_test and nomad_agent_test with vault_groups [common, yandex] and the VK test Vault endpoint. The VK agent already maps the GitLab registry password from yandex. Public-test has nomad_agent_test, but its all group loads only [vkcloud_public_test, common], so a yandex binding requires loading that namespace explicitly as well. No corrected repository edits yet: source/base reconciliation and changed file scope must be reviewed before implementation. The earlier local yandex additions are not the intended final change.

## User correction: deployment inventory differs from Vault namespace

User corrected the November11 implementation: test infrastructure moved to VK Cloud, so adding bindings only under inventories/yandex does not establish delivery to the active VK environment. The earlier proposal/approval did not validate that target selection. Agent incorrectly inferred deployment inventory from the Vault namespace yandex. Existing inventories/vkcloud/group_vars/all uses vault_groups [vkcloud, common]; the local Jenkins-specific VK group overrides this to [yandex, common] and the VK test Vault endpoint. No Nomad groups were found in the inspected static vkcloud hosts file. Therefore blindly moving the two lines to vkcloud is not a verified fix: identify the actual VK Nomad inventory and Vault loading route first. The two yandex additions remain local pending correction; no publication/runtime change occurred. Vault namespace yandex may remain valid independently of deployment provider.

## Approved yandex inventory Vault binding prepared on November 11

User explicitly confirmed the proposal to reuse automation-services branch DevOps-890-nexus-docker-auth/MR1371 targeting master, add the Vault binding to nomad_master_test and nomad_agent_test, update the assertion message, and retain environment lookup for other inventories. Added nomad_client_nexus_docker_pass referencing vault_secrets['yandex'].nomad_client_nexus_docker_pass in both existing group_vars files. Updated fail_msg to explain inventory Vault secrets or controller environment as supported sources. Prior approved local no_log deletion retained. No live Vault read or runtime apply performed.

Actual Ansible Templar fixture checks for both groups pass: Vault fixture overrides a conflicting environment fixture, rendered Nexus auth uses docker and the fixture Vault password, and GitLab registry auth remains unchanged. Other inventories retain the role environment default. Initial verification harness incorrectly expected JSON text where Ansible returned an already parsed dict; corrected harness accepts both forms and all checks pass. Three-way merge-file simulation of all three changed files against cached origin/master is clean; strict YAML parser rejects duplicates and confirms resulting template task has exactly one no_log:true and diff:false. Scoped whitespace check passes, unrelated local file bytes match the pre-task snapshot, and index remains empty.

Local task diff from source HEAD: two inventory additions, one assertion message replacement and prior one-line no_log deletion. Publication remains unapproved/unperformed: no commit, push, MR metadata update, manual CI, merge or deployment. The original central MR1371 item remains open; actual Vault delivery and Molecule verification are still unverified. No background operations remain.

## User-reported Vault key on November 11

User reports adding nomad_client_nexus_docker_pass to the yandex Vault secret alongside the existing GitLab registry password. Expected inventory binding is vault_secrets['yandex'].nomad_client_nexus_docker_pass. This is user-reported storage, not independently verified Vault content or controller delivery. No secret value recorded. The report alone does not authorize repository edits or external changes; adapting the existing MR remains a proposal.

## Nexus password verified on November 11

At the user's explicit request, verified the current/.env NEXUS_DOCKER_PASSWORD for Nexus user docker via read-only HTTPS requests. Anonymous HEAD for the previously recorded Docker manifest returned401; authenticated GET /v2/ and HEAD for the same manifest returned200. Password was read in memory only and not printed; no image downloaded or external configuration changed. This confirms current authentication and read access to the checked image, not Vault storage, controller injection or all registry privileges. User also proposed using the existing vault_fetch_tasks.yml/vault_secrets inventory mechanism instead of environment lookup; this remains a discussion proposal, without repository or Vault mutation approval. No background operations remain.

## Local duplicate-key correction approved and prepared on November 11

User requested fixing no_log and explicitly approved reuse of automation-services branch DevOps-890-nexus-docker-auth, targeting master. Existing checkout switched from DevOps-920-fix-private-dns-edns. Unrelated inventories/yandex/main.tf overlapped branch differences; explained before temporarily saving its bytes, switching with its HEAD content and restoring its exact original bytes. Snapshot under ~/ai-data/gitlab-workflow/mr1371-no-log/ confirms every unrelated modified/untracked file retained identical bytes; index remains empty.

Removed only the MR-added no_log line from roles/nomad/tasks/docker-auth.yml. Three-way git merge-file simulation against cached origin/master, whose affected file was live-verified unchanged earlier this task, merges cleanly. Strict duplicate-key YAML parsing passes; resulting Add docker auth config retains exactly one no_log:true and diff:false from master, and the Nexus assertion remains. Scoped git diff --check passes. This is a local one-line deletion, not a published fix: no commit, push, MR update, CI start, merge or deployment performed. Existing MR1371 backlog item remains open pending publication and the previously recorded controller-secret/CI limitations. No background operations remain.

## Recheck on November 11

Read-only GitLab GET confirms MR1371 remains open at f4018c2bf2e1d08cb2bf4c739bf64b3b667c4853, mergeable without conflicts, with latest pipeline140673 skipped. Current master is d1b63f7081645161e82d9d2b5247e7679ad5ac6f. All four affected master files match the previously inspected cached versions: common Nexus auth and DinD pin remain absent from master. The November9 duplicate-key and controller-secret findings therefore remain applicable. The MR still contains useful unmerged changes, but full Molecule validation and controller secret availability remain unverified. No merge, CI start, repository edit or deployment performed. Existing MR1371 TODO remains open; no new implementation permission was inferred from the user's questions.
