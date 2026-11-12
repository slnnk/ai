---
system: automation-services
status: verified
checked: 2026-11-11
tags: [gitlab-runner, jenkins, inventory, cleanup]
---
# automation-services local change audit

## Task
User requested reviewing and organizing all local automation-services changes shown in git status. Investigation authorized; no discard, move, branch switch, commit or publication approved in this turn.
## Context
Existing checkout on DevOps-890-nexus-docker-auth at41e5e182. Fresh origin/master a8b70e01 contains the merged MR1371. Eleven modified tracked files and twelve untracked files remain. None of the untracked paths is in master; none of the tracked local changes is already identical to master.
## Actions
Read bounded diffs and historical logs, inspected inventory variable resolution, fetched master read-only, and ran read-only SSH summaries on runner171/172/173 and VK Jenkins controller/agent. Runner173 probe failed; no live claims for that host. All processes completed. No repository files or remote services changed.
## Findings
Seven Jenkins files (jenkins.yml, three role task files, agent compose template and two VK recovery inventory files) originate from the October13 DevOps-892 recovery. Live VK controller10.18.26.8 runs the specified controller image; agent10.18.26.26 runs the specified agent image with WebSocket and a populated connection secret. Preserve/review this unpublished work. Recovery jenkins_start:false intentionally renders without startup; do not silently treat it as a normal service stop or replace it with true.

Four Docker/containerd files (runner install task, containerd template and two daemon templates) correspond to live171/172: root /data/containerd and insecure-registry network10.16.24.0/24. The cleanup cron template matches live hourly schedules at minutes10/20/30 on both hosts. Preserve and prepare these as runner work; live173 is unverified.

Three untracked prod_selectel runner host_vars contain meaningful runner/cache settings and embedded legacy credentials, but omit Nexus auth. A previous static-inventory-only diagnosis was incomplete: the June4 evidence explicitly selected these names for Terraform inventory, while static hosts use FQDN dind names. Do not rename or discard them solely based on static inventory. Dynamic state naming has not been freshly verified. Preserve seven current runner definitions and add the Nexus/Vault persistence work only after selecting the actual inventory route.

Six untracked prod_yandex files are older runner inventory data: a group file plus five host files. They differ from the Selectel variants in names, S3 credentials, extra config and some runner tokens/env entries. They are historical candidates for a protected archive, not proven byte duplicates or authorized deletions. No live Yandex inspection was done.

inventories/yandex/main.tf only changes comment formatting and has no Terraform behavior change. Propose reverting this one local hunk after approval.

roles/gitlab-runner/vars/main.yml uncomments a literal registration token. Do not publish it; propose reverting the local activation after approval. A raw tracked diff exposed the preexisting credential-bearing line during this audit, as happened in the older recovery log; no value is repeated in this note. Validity/rotation is not established or authorized by this investigation.
## Changes
Knowledge bookkeeping only. Existing runner persistence and Jenkins recovery TODO items retain their scope; this audit grants no implementation permission.
## Status and risks

Review complete, cleanup not yet executed. Recommended sequence: approve exact branch/base and scope, preserve a protected recoverable copy of the local state, remove only the two identified formatting/token-activation hunks, retain Jenkins and Selectel runner work for their separate task branches, and decide whether to archive old Yandex inventory after preserving unique contents. Detailed remaining work is tracked in central TODO, linked to this audit. No local background operations remain.
## Portable lesson

none

## User merge verified and related backlog reconciled

User reports merging MR1396 and asks which TODO tasks it affected. Fresh GitLab GET verifies merged state at457cf622c6ce4ebf2fe97eff501b4998d3363a2b (November11,23:34:35MSK), source b6ae6699. Two source tasks are complete: the local Jenkins/runner synchronization and runner171/172 Nexus auth persistence in configuration management. Updated those closed entries with merge evidence, retaining no-runtime-apply status.

The broader Finish Jenkins VK recovery item is only partially affected: primary VK inventory, selected image versions, Vault agent secret, WebSocket and the reviewed recovery role changes are now in master. Remaining workflow acceptance, backup, monitoring and canonical timezone/DNS alignment are not proven complete by this MR. Updated that existing item to supersede the old blanket Git-publication deferral only for the merged scope; keep all other deferrals/limits. No unrelated TODO closed, no new infrastructure checks, deploy, retry or external tracker mutation. No background operations remain.

## Final runner publication completed

User explicitly approved the final ten-file publication proposal. Snapshot check matched immediately before staging. Staged exactly the ten approved paths, inspected complete staged scope/diff, validated both new host_vars contain only Vault references in registry/cache credential fields and no registration-token file was included. Staged whitespace check passed. Created b6ae6699b85c2ada474088d1cc4a0d86a196c91e, sync docker runner configuration (tenfiles358insertions10deletions), verified committed paths and clean working tree, then pushed sync with strict verified SSH transport.

Updated existing [MR1396](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1396) title to the approved DevOps-892 Sync Jenkins and Docker runner configuration and replaced its body with the approved final-scope text. Guarded GET before PUT confirmed open state, source/target and SHA. GET readback and independent helper verify confirm exact SHA/title/body and preserved assignee a.solonenko, squash false, source deletion true and non-draft state. Pipelines142829/142830 skipped; no CI success or manual Molecule run claimed. No merge, target push, server apply, registration or service restart performed. Live Vault verification was explicitly waived by the user and not run.

Branch sync matches origin/sync (ahead0/behind0), index/worktree clean and no task background operations remain. All agreed local synchronization/publication work is complete. Closed the central sync publication and earlier runner171/172 configuration-persistence TODO items as source publication only, explicitly retaining no-runtime-apply status. This does not assert that running runners now use Nexus docker instead of their prior gitlab identity. The repo-wide Vault requirement remains documented; older project instruction alignment is outside this code publication and does not permit a new automatic repository sweep.

## User waived live Vault verification; final runner publication prepared

User explicitly declined remaining item1 (live Vault delivery verification), stating the keys are already added, and requested pushing remaining runner changes. Do not run or reopen that verification; creation is user-reported, not an agent-read success. Prepared the concrete final publication proposal under ~/ai-data/gitlab-workflow/sync-runner-publication/ for ten runner files, commit sync docker runner configuration, source sync to master, updated MR1396 title DevOps-892 Sync Jenkins and Docker runner configuration and a short Russian final-scope description with the DevOps-892 link. Exact field scan confirms all registry/cache credentials in the two untracked host_vars are Vault references; registration-token file unchanged, full whitespace check passes, index empty. Prior seven fixture/TOML/JSON checks and actual two-host Terraform list remain applicable. Optional manual Nomad CI only, no automatic runner tests or deployment jobs. New commit/title/body/scope require the final supervised publication confirmation; no commit, push, metadata change or background operation yet.

## Explicitly authorized existing runner secret replacement in uncommitted host_vars

User reports creating production Vault keys gitlab_runner_s3_access_key, gitlab_runner_s3_secret_key and gitlab_runner_registry_auth and explicitly requested replacing secrets only in uncommitted files. This authorizes the previously deferred migration specifically for the two untracked host_vars01/02, not a repository-wide rewrite. Replaced GitLab registry auth with vault_secrets['prod_selectel'].gitlab_runner_registry_auth and cache credentials with exact user-selected S3 key names. Existing Nexus docker auth continues using nexus_docker_password. Seven runner entries updated; all other file hashes, runner fields and non-auth environment entries unchanged, index empty.

Actual Ansible template fixture checks pass for all seven runner definitions with the four Vault keys; generated environment parses as TOML, auth parses as JSON, Nexus identity docker and both S3 values match fixtures. Sanitized inspection confirms all registry-auth/cache-credential fields in these two files are Vault references rather than literals. Real Vault contents remain user-reported, not independently read. No role logging expansion, edits to committed versions/other working files, commit, push, Vault write, remote apply or background operation. This supersedes the earlier preservation restriction only for the three specifically authorized fields in these two uncommitted files.

## Terraform group selector fixed and pending secrets disclosed

User approved the proposed selector change. Updated only the Linux host pattern in gitlab-runners.yml to gitlab_runners:gitlab-docker-runners. Syntax-check and full whitespace check pass. Actual Terraform --list-hosts now selects exactly gitlab-docker-runner-01 and02, no03; macOS zero. No role run or remote mutation. This closes the remaining numbered review finding; local runner publication remains unapproved/unperformed.

User then asked whether uncommitted changes contain secrets. Sanitized inspection confirms both untracked Selectel host_vars still contain the preexisting literal GitLab registry auth (base64 username:password), S3 access key and S3 secret key, repeated in four/three runner entries. These were deliberately restored following the user's earlier correction against an unrequested migration; do not claim the files are secret-free. New Nexus auth references production Vault nexus_docker_password and does not contain a literal password. No values printed. These legacy secret values must not be published without resolving the scope/policy conflict with the user; no automatic migration, Vault write or push authorized by the question. No background operations remain.

## Obsolete runner03 host_vars removed

User explicitly selected remaining item2, removal of inventories/prod_selectel/host_vars/gitlab-docker-runner-03.yml. Confirmed the file was untracked, saved a verified private mode0600 archive under ~/ai-data/gitlab-workflow/local-cleanup/runner03-20261111-*.tar.gz, then removed only that file. Host_vars01/02 hashes stayed unchanged. No tracked Git deletion, commit, push, remote config or background operation. The remaining review finding is the playbook group selector mismatch with Terraform inventory.

## Static Docker runner duplicates removed at user request

User clarified Terraform inventory is the operational source and explicitly requested removing the redundant static Docker hosts instead of renaming them. Removed exactly the three171/172/173 entries from inventories/prod_selectel/hosts; kept the empty group header/parent relationship and all DS/Android/other hosts unchanged. The dynamic01/02 host_vars remain present. This supersedes review finding3's rename proposal; finding2's static173 entry is also resolved, but the untracked obsolete03 host_vars file remains untouched. Exact diff and full whitespace checks pass. No Terraform state/provider source, runtime hostnames, registration, commit or push changed. No background operations remain.

## Review finding 4 fixed at user request

User selected only finding4 (cron trailing whitespace). Removed trailing spaces from exactly two lines in roles/gitlab-runner/templates/cron-docker-clean.j2. Tokenized cron lines are unchanged, retaining hourly schedules at10/20/30. All other modified/untracked file hashes remain identical. Full git diff --check passes. Review findings1–3 remain proposals, not implementation permission. No commit, push, runtime operation or background command performed.

## Review of remaining runner work with two current Docker hosts

User requested checking remaining changes and clarified only two Docker runner hosts currently exist. Read-only live comparison against171/172 confirms active services and four/three runner registrations, concurrent4 on each. Desired host_vars match all compared existing fields: names, executor/image/privilege, per-runner limits, extra config, non-auth environment, S3 endpoint/bucket/keys and GitLab registry auth. Planned Nexus identity differs intentionally: current runtime uses gitlab, desired code uses user-selected docker and production Vault nexus_docker_password. No values printed; sanitized comparison receipt at ~/ai-data/gitlab-workflow/sync-runner-nexus/live-review.json.

Both host Docker daemon JSON files, DinD daemon JSON files, containerd TOML and cleanup cron match the local templates exactly. Templates parse as JSON/TOML and changed task YAML parses. Full git diff --check flags only two preexisting trailing spaces in cron-docker-clean.j2; no fixes applied during this review. Shared role modifications are not scoped by host count automatically; future runtime apply must target the reviewed two hosts.

Read-only actual Terraform inventory resolves33hosts, including exactly gitlab-docker-runner-01 at171 (four definitions) and02 at172 (three definitions); no03. Terraform source also declares count2. This confirms the existing host_vars filenames are correct for the actual Terraform inventory, superseding prior uncertainty. Static prod_selectel/hosts still contains dind03/172.28.0.173 and the untracked gitlab-docker-runner-03.yml remains obsolete per the user's two-host statement; removal is proposed, not executed. Static01/02 FQDN names differ from Terraform aliases and therefore do not load the new files.

Critical invocation mismatch confirmed: gitlab-runners.yml targets gitlab_runners, whereas Terraform inventory groups these hosts as gitlab-docker-runners and has no matching umbrella group. Actual ansible-playbook --list-hosts using inventory.yml selected zero hosts for both plays. Proposed minimal correction is to add gitlab-docker-runners to the Linux play's host pattern, align static01/02 names with existing Terraform aliases, remove static03 and the obsolete local03 file, and trim the two cron trailing spaces. Preserve the existing runner definitions, credentials and all other settings. No repository file, Terraform state, remote configuration, runner registration or service was changed in this review; no background operations remain.

## User rejected unrequested secret migration; scope recovered

User corrected the prior implementation for changing things outside the requested Nexus task. Agent had wrongly treated the repository-wide Vault requirement as permission to migrate existing registry/S3 credentials and expand logging changes immediately. This was a scope failure; the earlier broad implementation is not the accepted final change.

Reverted the extra host-var Docker-auth map and registry/S3 references by rebuilding from the protected original snapshot, then added only nexus.youdo.com/docker auth from vault_secrets['prod_selectel'].nexus_docker_password to each existing DOCKER_AUTH_CONFIG (four entries on01, three on02). Every preexisting registry auth entry, S3 credential/setting and non-auth env item matches the original values. Restored config-runner.yml, config-runners.yml and register-runner.yml to HEAD; removed only the new loop label from install-ubuntu.yml, whose bytes again match the previous containerd snapshot. Removed new S3 log suppression from update-config-runner.yml; retained only no_log:true/diff:false for the Docker-auth environment task, as originally proposed. No additional Vault keys are required by this narrowed implementation.

Seven actual Ansible template cases plus TOML/JSON parsing pass; after removing the Nexus entry each rendered auth object equals the original object. Non-env runner dictionaries, including S3 settings, match exactly. Syntax and scoped whitespace checks pass, index empty. Changes remain local; no commit/push/Vault write/remote apply. Repo-wide Vault policy is retained, but unrelated legacy migration requires separate scope agreement. No background operations remain.

## Runner Nexus/Vault changes implemented locally

User explicitly requested implementing the runner changes on sync after specifying Nexus user docker and production secret/ansible/prod_selectel key nexus_docker_password. Updated the existing Terraform-inventory host_vars gitlab-docker-runner-01.yml and -02.yml, retaining four/three runner definitions and every nonsecret runner/cache/env setting. Shared per-host Docker auth maps render both registry.youdo.sg (existing encoded auth supplied via Vault key gitlab_runner_registry_auth) and nexus.youdo.com (docker plus nexus_docker_password). All seven environment entries serialize the map with to_json.

To satisfy the explicit repository-wide Vault requirement, replaced existing embedded GitLab registry auth and S3 cache literals in these two task files with production Vault references. Additional required keys are gitlab_runner_registry_auth (the existing base64 username:password auth string, not a new identity), gitlab_runner_cache_s3_access_key and gitlab_runner_cache_s3_secret_key. Their existence/content in production Vault is not verified; they must contain the current unchanged credentials before any apply. Do not silently substitute unrelated existing s3 keys. No Vault writes or secret values printed. Untouched host03 remains legacy migration work and was not added to this .171/.172 task.

Protected task output: no_log on config slurp/facts, copy, environment, S3 credentials, registration command construction/execution and final assembly; diff:false on credential-bearing writes; loop labels show runner names/config indices rather than raw secret-bearing dictionaries or config text. The previous local containerd installation hunk is preserved alongside the added registration loop label. Existing registration-token activation stays reverted.

Validation: actual Ansible Templar renders all seven definitions with fixture Vault values, decoded Nexus auth is docker:fixture, prior GitLab registry entry preserved through the fixture, generated TOML parsed by tomli and nested JSON validated. Original nonsecret settings and non-auth env entries are equal to protected pre-task snapshot data; former embedded credential strings are absent from both changed host_vars. Missing Vault keys reject rendering. Initial harness lacked toml (used installed tomli); a misplaced YAML document separator introduced during editing was caught and corrected before final validation. All seven changed files parse with strict duplicate-key checks, secret-bearing tasks have no_log, role playbook syntax and scoped whitespace checks pass. Other five existing local runner files retain original hashes; index empty. No full remote role --check, apply, registration, restart, commit or push performed. Runtime inventory routing and live Vault delivery remain unverified; no background operations remain.

## User-created production runner Nexus key name

User reports creating the runner Nexus password in production Vault secret/ansible/prod_selectel but chose key nexus_docker_password. The current task must therefore use vault_secrets['prod_selectel'].nexus_docker_password with Nexus user docker. This supersedes the previously proposed production key name nomad_client_nexus_docker_pass only; the VK Nomad key remains unchanged. Creation/value is user-reported and not independently read. No repository edit, Vault write, commit, push or runtime operation performed in this clarification; no background operations remain.

## User selected docker identity and existing Vault password for runner Nexus auth

For the current runner synchronization the user explicitly selected Nexus user docker and reuse of the password already added to Vault for Nomad, key nomad_client_nexus_docker_pass. This supersedes the earlier proposal to preserve Nexus user gitlab for the new Ansible configuration; it does not claim the running runners have changed identity. Current runtime entries remain as previously verified until an approved apply.

Runner prod_selectel inventory loads [prod_selectel, common] from http://vault.service.consul:8200; the previously verified Nomad key was read using the VK test Vault endpoint/yandex document. Attempted read-only key-presence checks for prod_selectel/common/yandex on production Vault via CLI failed at authentication/helper, including outside sandbox. No values printed, no secret absence inferred and no external writes performed. Reuse the same password, but verify an accessible production Vault reference before implementation; do not silently point runner inventory at VK Vault or duplicate/change credentials without approval. This is a source-route verification gap, not a requirement for a new Nexus account or password. No background operations remain.

## User repository-wide Vault requirement

User explicitly stated all secrets in this repository must be in Vault. Recorded a repo-scoped rule in the existing Vault system map and company context. Scope covers all automation-services secrets, not just Nexus or Jenkins; existing literals remain pending migration within approved sync work. The current repository AGENTS.md section5.3 still recommends encrypted Ansible Vault files and needs alignment with the newer user requirement before publication. No repository file, secret store or credential was changed in this policy turn. This decision does not authorize a bulk migration or external writes. Ongoing runner/Nexus work must reference production Vault, preserving active identities and values.

## User reverted registration token activation

User explicitly requested cancelling the local registration-token activation. Verified roles/gitlab-runner/vars/main.yml had exactly one changed line, uncommenting gitlab_runner_registration_token, then restored that line from HEAD without printing its value. The entire file now matches HEAD; all other modified/untracked file hashes stayed unchanged. Eight runner worktree files remain: installation/containerd, two daemon templates, cleanup cron and three Selectel host_vars. No commit, push or remote action performed; no background operations remain. This closes the token-activation cleanup subtask without claiming the historical literal was removed from repository history or rotated.

## Jenkins Vault cleanup publication completed

User explicitly approved the five-file publication proposal after reviewing scope, commit message, retained MR title/body and CI effects. Snapshot check matched. Staged exactly jenkins.yml, VK hosts and jenkins_servers group_vars, agent install task and agent compose template; inspected the actual full staged diff and passed staged whitespace checks. Created330a02e7fc06fc96383d1fc2b2c29155c9eeb576, use vault for jenkins agent secret (fivefiles5insertions15deletions), verified committed paths, and pushed sync.

Read-only helper verification confirms MR1396 source SHA330a02e7, unchanged approved title/body, sync to master, and preserved metadata. Pipelines142825 and142826 are skipped; no CI-success claim or manual test started. Changes now published include the Vault agent secret binding without environment fallback, removed legacy Yandex play and removed unused UUID assignments. All nine runner files remain unchanged locally; index empty. No merge, server configuration change, service restart, live Vault read or background command remains. Broader runner synchronization stays open in central TODO.

## Jenkins agent secret moved to inventory Vault binding locally

User reports adding jenkins_agent_secret to the yandex Vault document, continuing the agreed Jenkins synchronization and proposed Vault migration. Added jenkins_agent_secret referencing vault_secrets['yandex'].jenkins_agent_secret in VK group_vars/jenkins_servers. Agent Compose now uses jenkins_agent_secret directly; the prerequisite assertion checks that variable is nonempty without JENKINS_AGENT_SECRET environment fallback. No live secret retrieved or printed and no Vault write performed.

Ansible syntax-check and scoped whitespace checks pass. Actual Ansible Templar fixture uses the Vault fixture even with conflicting environment; empty/missing key is rejected rather than silently using environment. All nine runner hashes remain unchanged, index empty. Real Vault key content is user-reported, not independently read in this follow-up; controller/agent service not changed. These edits and prior removal of the legacy Yandex play and unused disk UUIDs remain local, uncommitted and not pushed to MR1396. No background operations remain.

## Existing Jenkins agent secret location verified

User could not find the suggested Jenkins secret line. Read-only SSH on10.18.26.26 confirms /data/jenkins-agent/docker-compose.yml exists and contains a nonempty JENKINS_SECRET assignment on line16; JENKINS_AGENT_NAME is on line19. Only field names, line numbers and nonempty flags were returned, never secret values. The file is on the deployed agent, not the local repository template. This supplies a verified source route for a proposed Vault key jenkins_agent_secret in the yandex document. No secret extraction into chat, Vault write, repository edit or service operation performed; no background operations remain.

## User removed unused recovery disk UUID inventory values

User requested removing jenkins_data_uuid if unused. Confirmed no references in the Jenkins role or playbook, then removed the two UUID assignments from the jenkins/jenkins-agent lines in inventories/vkcloud/hosts. Historical recovery disk identity evidence remains in the existing recovery logs. Actual list-hosts still selects exactly both hosts; scoped whitespace check passes. Local uncommitted corrections now comprise this removal and the previously requested legacy Yandex play deletion. Neither has been pushed to MR1396. No runtime or background operation performed.

## User removed legacy Yandex Jenkins support

After reviewing MR1396, user explicitly stated the legacy jenkins-yandex play is not needed. Removed only that play from jenkins.yml on existing sync branch; retained the VK play and all runner files. This task-scoped decision supersedes the earlier compatibility-retention choice. Syntax-check and list-hosts pass: one play selects exactly jenkins and jenkins-agent, with no absent Yandex group warning. Scoped whitespace check and all nine runner file hash checks pass. The deletion is local and uncommitted; no push/MR update or runtime operation performed. MR1396 still contains the legacy play until separately approved publication. No background operations remain.

## Sync Jenkins publication approved and completed

User explicitly approved the presented publication proposal by replying Yes. Snapshot matched before staging. Staged exactly the seven Jenkins paths, inspected the complete staged diff and verified no runner paths. Scoped staged whitespace check passed. Created commit1a29e8a1a2f3c8ee47ff15c822b7b1433b1f49b5, subject sync jenkins inventory and configuration (sevenfiles44insertions8deletions). Post-commit tree checks confirm exactly those seven task paths and final branch diff against origin/master of eight files including the historical Kafka file. The four historical local-master commits were included as explicitly requested earlier; no additional history rewrite.

Pushed sync with upstream origin/sync using strict verified SSH transport. Created [MR1396](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1396), title DevOps-892 Sync Jenkins configuration and Kafka heap, source sync, target master. Helper verifies exact source SHA, title, body and MR metadata; assignee a.solonenko, squash false, source deletion on merge true, non-draft. Pipeline list empty at verification, not CI success. No manual CI started, merge, deployment or target push performed.

All nine preserved runner worktree files still match the pre-task hash manifest, and index is empty. Their synchronization, Nexus auth persistence and registration-token activation cleanup remain pending in central TODO. Jenkins publication task complete; broader sync work remains open. No local background commands remain. User-selected branch name sync is a task-specific exception to normal ticket-prefixed naming, not a new global convention.

## Sync publication proposal prepared

User requested pushing sync and preparing an MR now, with remaining changes to be added later. Interpreted the current batch as the approved Jenkins work plus the four explicitly included historical commits, excluding all nine runner files. Existing branch sync has no open MR according to fresh GET. Prepared proposal/body/snapshot under ~/ai-data/gitlab-workflow/sync-publication/. Seven Jenkins task paths plus the already-committed Kafka file form the proposed final eight-file MR scope. Commit message sync jenkins inventory and configuration; proposed MR title DevOps-892 Sync Jenkins configuration and Kafka heap; source sync, target master; description explains Jenkins/Vault/WebSocket and historical Kafka2g, followed by the DevOps-892 link. Runner worktree hashes unchanged, index empty.

Fresh syntax-check/list-hosts and scoped whitespace checks pass; prior inventory and template fixtures remain applicable. CI rules inspected: initial sync push skips all three Molecule jobs; MR fallback may expose optional manual Nomad, not authorized/started. No deployment jobs. Publication not yet performed: exact commit/title/body proposal requires the second supervised confirmation. No background operations remain.

## User explicitly included the four local master commits in sync

After the Jenkins migration the user explicitly requested adding the four previously excluded local-master commits to sync. Verified sync HEAD was an ancestor of local master and the incoming tree delta was only inventories/yandex/host_vars/kafka-test01. Ran git merge --ff-only master on sync, advancing it from a8b70e01 to515373c3 without creating another commit. Branch sync now includes e1726fbf,9c78dc0a,a7712e48 and515373c3, with kafka_heap2g restored in its tree. This supersedes the earlier instruction/proposal to exclude those commits from this branch. All uncommitted Jenkins/runner file hashes stayed identical and index is empty. No push, remote mutation or runtime apply; no background operations remain. Future publication must disclose these user-approved historical commits and the added Kafka file.

## User-approved sync branch and Jenkins inventory integration

User explicitly chose branch sync instead of a task-specific Jenkins branch, intending to synchronize the other local work there later, and approved the proposed Jenkins changes. Created sync from origin/master a8b70e01 without incorporating the four local-master-only commits. All existing runner work remains byte-identical according to the saved hash manifest at ~/ai-data/gitlab-workflow/sync/runner-before.json. No commit or publication yet.

Moved VK Jenkins settings into inventories/vkcloud/group_vars/jenkins_servers. Main inventories/vkcloud/hosts now defines jenkins (10.18.26.8) and jenkins-agent (10.18.26.26), preserving host_type and data UUID values from the temporary inventory; common variables preserve root/Python access, image versions, WebSocket, startup-disabled recovery mode and VK Vault/yandex secret references. Deleted the now-redundant local jenkins-recovery.ini and jenkins-vkcloud group_vars after transferring their contents. No operating-system hostname or server configuration changed.

Initial group name jenkins collided with the controller host name jenkins: actual ansible-playbook --list-hosts selected only the controller. Corrected the technical group to jenkins_servers, retaining the user-approved machine names. First play targets jenkins:jenkins_servers and runs exactly once per VK host. An opt-in jenkins_test_stand flag preserves the former VK play behavior: Vault retrieval and Alloy enabled, base_linux skipped. Existing non-test jenkins defaults and the legacy jenkins-yandex play remain intact; no jenkins-vkcloud selector remains.

Syntax-check and actual list-hosts pass, selecting exactly two VK hosts and zero legacy Yandex hosts. Inventory assertions verify addresses, UUIDs, role types, connection settings and Vault route; Ansible Templar fixture verifies agent URL, WebSocket and secret injection. Conditional role selection fixtures cover both test and legacy defaults. Scoped diff check passes; all nine runner files retain original bytes, index empty. Ansible warnings for existing ipsec/prod-1c group/host names and absent legacy jenkins-yandex group do not prevent checks. No live apply, restart, remote rename or background operation performed. Jenkins local preparation is complete; broader runner synchronization and publication remain pending in central TODO.

## Kafka file absence investigation

User asked who deleted the old kafka-test01 file remotely. Fresh GitLab GET confirms master a8b70e01, commit9c78dc0a returns404, and master commits queried for inventories/yandex/host_vars/kafka-test01 return an empty list. Local full-history path search on origin/master and deletion search across available refs find no deletion commit. There is no evidence identifying a person deleting this file.

The [October11 GitLab restore verification](2026-10-11-gitlab-restored-server-verification.md) records backup metadata created2026-10-10T01:31:18Z (04:31:18MSK). Kafka commit9c78dc0a was authored/committed on October10 at13:05:33MSK, after that backup. The absence of the commit/file in the restored remote history is consistent with restoring a snapshot predating the change, rather than a file deletion. This is an evidence-based explanation, not attribution of a specific restore action/operator; the restore execution and exact repository backup cutoff were not independently re-audited. No Git mutations or restoration attempted.

## User reverted formatting and updated master

User reports reverting inventories/yandex/main.tf, switching to master and pulling. Local read-only checks confirm current branch master at515373c3 and no diff for inventories/yandex/main.tf. Six abandoned Yandex runner files remain absent. Remaining worktree contains ten modified tracked files and six untracked files (sixteen total), all belonging to the previously inventoried Jenkins/runner work. No additional cleanup or Git mutation performed by the agent in this follow-up. No background operations remain.

Read-only ancestry check also shows local master is four commits ahead of cached origin/master a8b70e01 and zero behind. This is separate from the sixteen uncommitted files. Do not infer that pull made local master identical to the remote or publish these commits without reviewing their scope and authorization.

## Four local master commits explained

Read-only log inspection identifies e1726fbf (October10 merge AP-2347-test-network, historical MR1366), 9c78dc0a (October10 Kafka heap change), a7712e48 (October10 merge AP-2347-kafka-test-heap, historical MR1367) and515373c3 (November11 local pull merge of current remote master into the old local master). Network-branch commits are already reachable from origin/master through another path; do not equate the merge commit's first-parent stat with a new pending network patch. Exact tree comparison origin/master..master has only one added line in inventories/yandex/host_vars/kafka-test01, setting Kafka heap to2GiB. No pending extra network patch appears in the final tree. No Git history or worktree changes performed. This explains local-only history, not authorization to push or reset it.

## User-cancelled Yandex runner inventory removed

User explicitly clarified that Yandex has no runners and will not have them; the local inventory was only updated during an abandoned attempt to run there. User authorized cancelling those changes. Removed exactly the six untracked runner files under inventories/prod_yandex: group_vars/gitlab-docker-runners.yml and host_vars/gitlab-runner-{android,docker-1,docker-2,docker-3,ds}.yml. No tracked files, other Yandex inventory, registration-token change, Selectel runner work or Jenkins work changed. This is user-cancelled work, not a completed Yandex rollout.

Before removal, created and verified a private mode0600 archive at ~/ai-data/gitlab-workflow/local-cleanup/prod-yandex-runners-20261111-221630.tar.gz. Member bytes matched the originals. Hashes confirm all unrelated modified/untracked files retained identical bytes. Restore only if requested, using the archive's relative paths from the repository root. Seventeen local changed/untracked files remain; cleanup of them is not yet authorized by this narrow cancellation. No commit, branch switch, publication or external operation performed. No background operations remain.
