---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [jenkins, elasticsearch, vk, DevOps-894]
---

# DevOps-894 Jenkins Elasticsearch deployment test job plan

## Summary

Created the approved ES-only Jenkins test job and stable VK credentials. User-approved controller dnsmasq deployment fixed .local lookup; global Ansible dc correction published as d95b385 in Draft MR104. Jenkins check build3 and full thin/test5 build5 and thick/test build6 succeeded. Thick CSI disk/snapshot are40GiB from the configured thick seed; ES reports74,235,448 primary docs, healthy Nomad/Consul and expected single-node yellow. Working dynamic_deploy ES stage, canonical controller DNS source integration, DBA_Clean destination and AWX workflow remain separate pending actions; no merge performed.

## Task and context

User requested a plan for updating https://build.youdo.sg/job/dynamic_deploy/ and suggested a separate test job first; also asked how Jenkins should supply secrets to Ansible. Initial scope was investigation/planning. The user subsequently requested continuing with the Jenkins job and explicitly corrected inventory location and common Nomad token handling; local preparation is authorized.

## Actions and key commands

Inspected live job config through authenticated GET with sanitized output, existing inventory/README, and Jenkins/Ansible official credential/environment documentation. No credential values, private keys or raw job XML were saved in this note. Source paths: ~/git/automation-test-yandex/inventories/vk_es/{hosts,group_vars/all.yml,README.md}; playbooks/deploy/docker/deploy_es_nomad.yml.

## Findings

- Live job is an enabled WorkflowJob using inline CpsFlowDefinition; an SCM/JJB source for the Pipeline was not established.
- Agent label linux; custom workspace /data/jenkins/workspace/deploy_test_ansible_$TEST_INSTANCE/.
- Checkout uses the existing Jenkins SCM credential and branch */$AUTOMATION_BRANCH in automation-test-yandex. Default AUTOMATION_BRANCH is master.
- Restore / parallel / Restore Elastic Indexes is gated on ELASTIC == true, uses retry(2), the ansible installation, old INVENTORY=test_inventory.sh (autotest exception), deploy_es_nomad.yml and extras -l $TEST_INSTANCE -D. No credential binding was found. Last build 5818 reported SUCCESS; this is not evidence of VK deployment success.
- VK inventory has one logical local host vk_es. It reads VK_TEST_NOMAD_TOKEN, VK_TEST_CONSUL_TOKEN, VK_CSI_USER, VK_CSI_PASSWORD, VK_CSI_PROJECT_ID from controller process environment. Full deployment resets stand data. Cloud credentials are required for Cinder readiness, even though CSI provisions the disk.
- DevOps-894 files remain local/unpublished; Jenkins cannot checkout the local changes until branch publication is approved and performed. Subsequent global configuration migration is recorded below.

## User correction (2026-10-14)

The user requires test_inventory and is restoring it personally. This supersedes the proposed separate vk_es inventory for Jenkins. Do not implement a parallel inventory or take over inventory restoration. Before repository adaptation or Jenkins deployment, verify the restored inventory host/group selection, instance/instance_type mapping and VK variable contract; exact CLI selection remains dependent on its actual output. Secret values must continue to come from Jenkins Credentials, with environment lookups in the appropriate inventory/playbook variable layer.

## Proposed plan

1. Publish reviewed DevOps-894 task changes to the approved branch under the existing supervised Git approval workflow, preserving unrelated MSSQL changes.
2. Prepare a separate manual Pipeline named dynamic_deploy_es_vk_test (proposed name), with only automation-test-yandex checkout and ES deployment. Use its own workspace; no inherited component stages or automatic triggers. Pin the tested branch/commit. Explicit single-stand parameter and full-reset semantics. Use restored test_inventory as the source of stand selection and inventory variables. Verify mapping against known thick test/test1/test6 and thin test2-5/test7/test10-15; test8 and autotest/public-test need separate verification. The current playbook does not infer instance_type; adapt it minimally to the restored inventory contract where needed. Add disableConcurrentBuilds and a timeout that allows the existing readiness/deployment windows.
3. Bind Jenkins Secret text credentials to VK_TEST_NOMAD_TOKEN and VK_TEST_CONSUL_TOKEN; bind Username with password to VK_CSI_USER and VK_CSI_PASSWORD; supply VK_CSI_PROJECT_ID as nonsecret configuration. Reuse valid existing credentials after review; proposed IDs are not verified existing objects.
4. Invoke deploy_es_nomad.yml with restored test_inventory (current entrypoint test_inventory.sh). Preserve -l <selected-stand> if supported by its restored host/group output. Resolve instance and instance_type from inventory or pass only nonsecret missing values explicitly, based on the verified contract. Verify controller-local execution for API/CLI tasks and exactly one lifecycle execution for the selected stand, even if its inventory group contains multiple hosts. Use scoped credentials environment, set +x, no secret CLI extras or environment dumps, no automatic retry of a full reset. Retain no_log for tasks carrying tokens/passwords. Preserve current Ansible tool version until compatibility is verified.
5. Validate agent dependencies (Ansible/Nomad CLI, Jenkins plugins), network access and credential presence without values, then syntax/check mode. Check mode does not verify the remote lifecycle.
6. After approval of each remote run, validate one agreed thin stand, a separately approved thick stand, and a repeat full cycle. Confirm Jenkins fails on errors, successful Nomad deployment/healthy allocation, CSI lifecycle completion and credential-free logs/artifacts. Prevent concurrent job builds and cross-job reset of the same stand; avoid snapshot refresh overlaps.
7. After acceptance and publication of the playbook, change only the ES stage of dynamic_deploy: use the restored test_inventory and verified stand-selection/variable contract, credential binding and no full-reset retry. Preserve other stage inventory settings. Recheck working job on one agreed stand. Capture sanitized original Pipeline for configuration rollback; reverting job config does not restore deleted stand data.

## Changed files and risks

Only this KB note and KB bookkeeping are changed. Jenkins credentials/job edits and real deploy runs each require the user's explicit approval. Main risks are shared-workspace collision, concurrent reset, stale master playbook, destructive automatic retry and unintended propagation of old inventory parameters. DBA_Clean destination and AWX snapshot refresh remain separate work.

## Inventory endpoint update (2026-10-14)

User explicitly requested updating test_inventory to http://dyninv.vk-test.youdo.local. Replaced only the old endpoint host in ~/git/automation-test-yandex/test_inventory.sh on the already approved DevOps-894 branch; preserved the existing trailing slash and other file contents. bash -n passed; comparison against HEAD confirmed only the endpoint changed. No inventory execution, DNS/HTTP check, Git publication or Jenkins modification. Service address map updated as user-supplied/unprobed.


## Jenkins preparation and final user corrections (2026-10-14)

- User authorized continuing local preparation, required removing inventories/vk_es and adding its variables to global group_vars/all.yml, and required using the common nomad_token for all roles rather than es_nomad_token. These corrections supersede any earlier scoped-inventory or extra vars file proposal.
- Removed the three agent-created vk_es inventory files. Added the VK ES/cloud/seed variables to global group_vars/all.yml. Preserved the dynamic stand group's dc and existing thin/thick group_vars mapping. Common nomad_token now references lookup('env', 'VK_TEST_NOMAD_TOKEN'), replacing the legacy plaintext value. Other preexisting global variables are preserved. ES uses the common variable. Historical Git commits still contain the old literal; no history rewriting or rotation performed.
- Prepared ~/ai-data/devops-894-jenkins/Jenkinsfile and job-config.xml for proposed dynamic_deploy_es_vk_test. Uses linux label, existing SCM credential, task branch, test_inventory.sh and -l TEST_INSTANCE. Stand choices limited to14 previously tested stands. RECREATE_DATA=false defaults to check mode; explicit true enables full reset. No triggers/retry; independent Jenkins workspace, concurrency disabled,20minute timeout.
- Inventory guard verifies exactly one docker alias and instance/dc=vk-test, including the service's list-form docker group. Initial review found dictionary-only parsing; reproduced against service-shaped fixture, corrected and verified list/dict/zero/multiple/wrongdc scenarios. XML script matches Jenkinsfile, sandbox enabled. Groovy/Jenkins server validation was not available locally and has not been claimed.
- Proposed credentials metadata is stored in credentials-plan.json without values: devops-894-vk-nomad (Secret text, existing VK_TEST_NOMAD_TOKEN), devops-894-vk-consul (Secret text, existing VK_TEST_CONSUL_TOKEN), devops-894-vk-cloud (Username/password from dynamic-inventory automation credentials, mapped to VK_CSI_USER/PASSWORD). Nonsecret VK_PROJECT_ID mapped to VK_CSI_PROJECT_ID in Pipeline.
- User authorized using cloud data from dynamic-inventory. Canonical credential source: Vault secret/admin/dynamic_inventory keys VK_AUTOMATION_USER/VK_AUTOMATION_PASSWORD, accessed through VK_TEST_VAULT_TOKEN; project/auth URL/region/domain in Consul admin/dynamic_inventory/. Existing current/.env copy supplies the same key names. Automation credentials differ from the CSI credentials used for earlier ES validation; Cinder permission remains unverified.
- Current work station test_inventory invocation fails curl DNS resolution even after escalation. This does not establish service failure: prior runtime-verification-4.json records GET200/16stands/16docker aliases. Recent Jenkins metadata GETs timed out; existing credential IDs/plugin versions/agent state could not be reconfirmed.
- Verification: both ES entrypoints syntax-check passed after global move; thin/thick offline check mode passed with no remote lifecycle changes; after common token correction deployment syntax and thin check passed again. Global YAML keys unique, other old variables equal HEAD, no existing current/.env secret-key values found in new Pipeline/XML/global additions. Original repository contains other legacy secrets; no whole-repo secret-free claim.
- Git branch remains unpublished; no Jenkins credentials/job created and no Jenkins build or Nomad reset triggered. Next remote action proposed for approval: create the three described credentials. Job creation and later runs require separate approvals. No Git staging/commit/push performed; unrelated MSSQL modifications preserved.

## Credential naming approval and creation (2026-10-14)

User rejected task-prefixed credential IDs; proposed final names vk-test-nomad, vk-test-consul and vk-test-cloud. User explicitly approved their creation with “Да”. Updated local Jenkinsfile, job-config.xml and credentials-plan.json. Created all three via Jenkins standard system/global credential API; preflight confirmed all absent, existing credentials were never overwritten. Each creation followed by config GET verified expected implementation type (two Secret text, one Username/password); no values printed or saved to new artifacts. Used existing current/.env keys; cloud credentials are the dynamic-inventory automation account. Local create_credentials.py supports --help, plan by default, --apply and optional base URL; all raw error/response data suppressed. Sandbox DNS failed first; same command rerun with network escalation completed exit0. No job/build created and no Nomad lifecycle action performed. Job XML/source equality and final IDs checked. Git task branch still unpublished.

User supplied DNS evidence: canonical dyninv.vk-test.youdo.local resolves via proxy.service.vk-test.consul to10.18.26.21/10.18.26.30/10.18.26.10 at2026-10-14 14:15:30MSK. Prior workstation/sandbox resolver failure is not evidence of a dynamic-inventory service outage. HTTP was not checked by this DNS evidence.

## Jenkins test job creation approval and result (2026-10-14)

User explicitly approved creation of dynamic_deploy_es_vk_test without starting a build. Created via standard Jenkins createItem API from the reviewed local XML, only after confirming the job name absent; existing jobs are not updated by create_job.py. Network sandbox DNS failed; approved network escalation succeeded. Follow-up GET verified flow-definition type, exact Pipeline script, sandbox=true, empty triggers and expected parameter types/defaults/stand choices. API reports buildable=true, build_count0, lastBuildnull. URL: https://build.youdo.sg/job/dynamic_deploy_es_vk_test/. No build or deployment triggered. Existing dynamic_deploy unchanged.

Prepared next publication proposal: repository automation-test-yandex, source DevOps-894-deploy-elasticsearch-on-vk, target master; commit adapt elasticsearch deployment to vk cloud; Draft MR title DevOps-894 Deploy Elasticsearch on VK Cloud. Task changes include8modified/deleted tracked paths plus8new ES task/template files; unrelated MSSQL paths excluded. MR body in ai-data/devops-894-jenkins/mr-body.txt (one Russian paragraph and task link). Both ES entrypoints syntax pass, thin/thick offline check and inventory guard cases verified, diff --check passes. Fresh GitLab project530 GET confirms ci_config_path empty (default), jobs enabled; checkout has no .gitlab-ci.yml. No configured pipeline/deployment expected from these changes. User publication approval pending; Cinder automation-account permission and Jenkins agent runtime validation remain unverified, hence Draft. No merge or build approval inferred.

## Git publication approval and result (2026-10-14)

User explicitly approved reviewed commit/push/Draft MR publication with “Да”. Staged exactly16task paths, confirmed no pre-staged changes, compared mixed global vars and inventory against HEAD, verified original unrelated vars unchanged except approved common Nomad token env lookup, scanned added lines against existing secret-key values without printing them. Both ES syntax-checks and bash -n passed again; diff --check passed. Commit d66c21de316927b553eccd9458763b02a3cccced, message adapt elasticsearch deployment to vk cloud. Pushed approved branch DevOps-894-deploy-elasticsearch-on-vk and set its remote tracking branch. Created Draft: DevOps-894 Deploy Elasticsearch on VK Cloud, MR https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/104, targetmaster, assignee a.solonenko, squashfalse/source-removaltrue preserving project preferences. Separate verify returned exact source/target/SHA/title and pipelines[]. No merge, Jenkins build, tag or deployment. Unrelated six MSSQL modified paths and mssql_inventory.ini remain untouched/local. DNS sandbox failures for Git push/API publication resolved by network escalation; no publication scope change. Next proposed action: one Jenkins check-only build on test5 with RECREATE_DATA=false and AUTOMATION_BRANCH=DevOps-894-deploy-elasticsearch-on-vk, requiring its own explicit approval.

## First check build, quietDown approval and interpreter fix (2026-10-14)

User explicitly approved first test5 check-only Jenkins build: AUTOMATION_BRANCH=DevOps-894-deploy-elasticsearch-on-vk, RECREATE_DATA=false. Triggered queue19116 and persisted nonsecret receipt. Queue initially blocked with Jenkins is about to shut down; API confirmed quietingDown=true, nodes online and only this item queued. User explicitly instructed disabling quietingDown for active Jenkins use. POST cancelQuietDown succeeded, GET verifiedfalse; this enables normal controller scheduling, without restart.

Build https://build.youdo.sg/job/dynamic_deploy_es_vk_test/1/ then completed FAILURE in8743ms, approved parameters independently verified. Inventory guard failed exit127 at python3 not found on the linux-labelled built-in node. No Ansible stage or Nomad lifecycle operation reached. In-memory console scan found no known current/.env secret-key values; raw log was not saved/output. Controller Dockerfile compiles Python3.8.15 through make altinstall, installs Ansible via python3.8, and does not guarantee python3 alias. Read-only SSH confirmed Ansible installation nameansible/homeempty, therefore PATH-based tool selection.

Prepared minimal local Jenkinsfile correction: choose command -v python3 or command -v python3.8 and invoke that executable for the same inventory guard. No package install or repository edit. Shell syntax and Python compilation pass; job XML synchronized. before-python-fix.Jenkinsfile preserves the prior nonsecret source. fix_python_and_check.py is prepared to update only this reviewed script difference, refuse an unrelated remote Pipeline edit, verify the resulting script and trigger one separately approved test5 check-only retry with its own receipt. Remote correction and retry have NOT been executed; explicit approval requested for that composed action. No inference of full reset approval.


## Approved interpreter fix, build2 and exact DNS root cause (2026-10-14)

User explicitly approved interpreter fix and test5 check-only retry. Updated only the reviewed Pipeline script, GET verified it and triggered queue19118/build2 with task branch/test5/RECREATE_DATA=false. Build2 FAILURE2140ms: Python selection worked, test_inventory subprocess failed. Check and Recreate ES skipped; no known source secret values found in log. No Ansible/Nomad lifecycle operation reached.

Current workstation inventory succeeds curl0/16stands/16docker aliases. Current build2 script on controller10.18.26.8, inspected via Java PID41759 proc root, targets the VK URL; executing its curl argv on HOST with timeout15 returns exit6/DNS/stdout0. No Docker/nsenter or container-context curl used. Container resolver127.0.0.11 forwards host127.0.0.53. Host ens3 DNS10.18.20.3/domainmcs.local. Direct dig of dyninv to10.18.20.3 returns NOERROR/CNAME proxy.service.vk-test.consul/A10.18.26.10,.21,.30; getent proxy works. resolvectl query dyninv returns No appropriate name servers or networks for name found. Record exists; resolved lacks explicit .local routing. Official systemd docs require explicit search/routing domain for .local unicast DNS.

Prepared helper ai-data/devops-894-playbooks/fix_controller_inventory_dns.py (plan default tested; --apply not run). Exact proposed one runtime change: sudo resolvectl domain ens3 mcs.local '~vk-test.youdo.local' on10.18.26.8. Preserves server/current search domain; no restart or file write. Does not persist resolver/network restart. Rollback restores ens3 mcs.local. Helper verifies host getent/current inventory safely after action; no Jenkins build. Remote DNS mutation and next build require explicit approval. Persistent source configuration requires separately scoped work.

Local Pipeline diagnostics now classify curl exitcode/error class while suppressing raw response; XML synchronized, shell/Python syntax passed. This enhancement was NOT applied remotely. Do not reuse interpreter-only fix helper against this broadened local draft.


## User-approved dnsmasq deployment and successful check build3 (2026-10-14)

User explicitly instructed deploying dnsmasq and continuing testing. Prepared existing role apply confined to controller10.18.26.8; automation-services repository not edited. Standalone ai-data/devops-894-playbooks/jenkins-controller-dnsmasq.yml/.ini uses role overrides: default/mcs.local DNS10.18.20.3, Consul masters10.18.26.11/.12/.13#8600, DNSMASQ_EXCEPT empty so loopback listener serves running Docker's cached127.0.0.53 upstream. Actual apply exit0: ok10 changed8 failed0 unreachable0. Installs dnsmasq dependencies, stops/disables systemd-resolved, writes normal resolv.conf nameserver10.18.26.8/searchyoudo.local, default/config files, starts/enables/restarts dnsmasq. Runtime resolvectl route helper was NOT applied.

Read-only postverification: dnsmasq active/enabled, resolvedinactive/disabled, full dnsmasq --test exit0, dig127.0.0.53dyninv NOERROR/CNAME/A correct, getentexit0, exact current build2 inventory host-context curl0 validJSON16docker targets. No Docker restart/exec. Service config is persistent on host; matching overrides are in the standalone KB-data playbook, not repository Jenkins/group inventory yet. Canonical automation-services integration needs separately approved branch work.

Triggered authorized further check-only test5/taskbranch/RECREATE_DATA=false queue19120/build3. https://build.youdo.sg/job/dynamic_deploy_es_vk_test/3/ SUCCESS5531ms, parameters verified. Pipeline inventory guard oneVKdocker target, syntax/check stages completed, recap test5_dockerok3/changed0/failed0/skipped14. Full reset stage skipped. No known current/.env source secret-key value found in memory-only console scan. Legacy curl progress written to stderr is displayed as Ansible ERROR noise, despite resultSUCCESS; do not mistake for actual failed tasks.

Main local Jenkinsfile/XML restored to approved live interpreter-only variant; optional curl error-class diagnostic draft preserved separately and not deployed. Prepared run_check.py --recreate-data flag and full-build-4 receipt plan for test5/taskbranch, without --apply; no full build triggered. Next explicit approval requested for full test5 reset: stop old job, replace CSI disk from thin snapshot, wait Cinder and submit/wait Nomad deployment. Automation-account Cinder permission remains unverified until that run.


## Approved full test5 build4 and corrected common datacenter (2026-10-14)

User explicitly approved test5 full reset/RECREATE_DATA=true. Triggered queue19122/build4 with taskbranch. User sent Nomad placement screenshot. Read-only live Nomad job elasticsearch-test5 has Datacenters[yandex-test], correct test5-vk-csi-es volume and only implicit Consul version constraint; evaluation blocked with NodesEvaluated0. All8clients ready/eligible in vk-test. Build4 remains running waiting placement; no success claim.

Exact root cause reproduced: raw dynamic inventory test5.vars.dc=vk-test, but ansible-inventory -i test_inventory.sh --host test5_docker resolves dc=yandex-test because global group_vars/all.yml line5 overrides dynamic inventory group vars via default vars plugin precedence. No other dc override/ansiblecfg. User explicitly allowed correcting global dc. Local one-line change dc:yandex-test→vk-test made on the existing approved task branch. Real inventory resolve nowdcvk-test, instancetest5/type thin unchanged; actual ES template render has Datacenters[vk-test]. diff --check passed and diff is one insertion/one deletion in global file only.

Prepared publication proposal: commit set vk test datacenter on same approved task branch, push and update existing Draft MR104/master without title/scope additions. No CI config/new CI effects. New common dc affects all roles consuming it; this matches the user's provider/global-variable correction. Requires renewed publication approval before Git state changes. To continue promptly after publication, propose stopping waiting build4 then repeating the explicitly reviewed full test5 reset; those runtime effects must also be approved explicitly. Neither new commit/push nor cancel/retry has been executed.

## Approved dc publication, build4 stop and full retry5 (2026-10-14)

User explicitly approved all reviewed effects: one-line dc commit/push in same task branch/MR104, stop waiting build4 and repeat full test5 reset. Verified cached index empty and global file differs from HEAD only by dc line before staging; staged review/diff --check passed. Commit d95b3858daae19fc0c97566365bfa904ce8ce516, set vk test datacenter, one insertion/one deletion. Push succeeded; verify confirmed MR104 unchanged source/target/title/preferences and exact new SHA, pipelines[]. MSSQL changes not staged.

Build4 stop POST then GET verifiedABORTED/buildingfalse. Triggered approved fulltest5/RECREATE_DATA=true/taskbranch retry queue19124/build5. Current build5running; full deployment outcome still pending. No extra manual Nomad job or CSI command, no merge.

## Full thin build5 success and user-requested thick test6 (2026-10-14)

Fulltest5 build5 SUCCESS72115ms, true reset parameters verified, actual play recapok23/changed2/failed0; no known source secret-key values found in memory-only console scan. Read-only receipt nomad-build-5-verification.json confirms jobdcvk-test, successfuldeploymentb86e25e0, healthyalloc4339c2e9, elastic/headrunning/restarts0, CSI ExternalIDdcde620d-cc49-4dd8-b018-a2ec99231c9d WriteAllocs1/ReadAllocs0. Consul passinginstances1; ES yellow(one node), activeprimaries21, unassignedreplicas27, no timeout. End-to-end Jenkins thin deployment and automation-account Cinder-readiness authentication passed, no manual job/volume correction.

User then explicitly requested a large dataset/large disk test. Selected standtest, group_vars/test.yml instancetypethick and global capacity40GiB verified before trigger. Extended helper with whitelisted --stand and receipt validation, no job or repo changes. Triggered fulltrue/taskbranch/test queue19126/build6; result pending. Current full reset initially makes oldjob disappear404, expected during lifecycle; previous diskID baseline not captured before purge. No third-party stand touched.


## Full thick build6 success and independent verification (2026-10-14)

User-requested full thick/test build6 SUCCESS100608ms, taskbranch/test/RECREATE_DATA=true parameters verified. Inventory selected one testdocker target. Full Ansible recapok23/changed2/failed0; no known current/.env secret-key value found in in-memory console scan. No manual volume/job intervention or automatic full reset retry.

Read-only nomad-build-6-verification.json confirms CSI Capacity/Min/Max42949672960bytes(40GiB), ExternalID0e949be6-e645-48a5-b65e-e58c3ee54727, WriteAllocs1. Ready snapshotd81f5286-d448-46f8-ab11-cee63b655a16 is40GiB and ExternalSourceVolumeID6b8a8094-227f-4eb2-968c-5469e98fd92c matches configured thick seed. Deployment973dda02 successful/HealthyAllocs1; allocationhealthy, ES/headrunning/restarts0, Consulpassing1. ES yellow,21activeprimary shards/27unassigned replicas/one node/no timeout. Primary docs count74,235,448 verifies large prepared dataset. Build link https://build.youdo.sg/job/dynamic_deploy_es_vk_test/6/.

Test job validation for both thin and thick is complete. Working dynamic_deploy remains unchanged and MR104 remains Draft/unmerged. Controller DNS configs persist on host; canonical repository integration is recorded separately. Remaining migration work is the reviewed working-job ES stage update, DBA_Clean destination and AWX weekly workflow. Full build6 did not authorize changes to those systems or any merge.


## Approved merge and working Pipeline update; project ID follow-up (2026-10-14)

User explicitly instructed merging MR104 then updating dynamic_deploy. Merge succeeded after marking reviewed Draft ready, preserving merge preferences and testedSHA. Merge/masterSHA0bfc65c492d23f88f677803681cd4a8d7021e5e4; masterdcvk-test and common Nomad token env lookup verified. No local checkout switch/rewrite, MSSQL changes remain.

Working Pipeline update adds common VK_TEST_NOMAD_TOKEN credential at declarative environment scope for all roles; ESstage adds Consul/cloud bindings and nonsecret project environment, uses test_inventory.sh and preserves other stage contents/SCM/parameters. User first selected retry1 (one total attempt), then after explanation explicitly corrected to retry2 (first attempt plus one repeat). Final ESretry2. No build triggered. Initial XML POST lacked explicit UTF8charset/declaration, causing14Russian textfields to become reversible Latin1mojibake; exact script readback caught mismatch. Repair recovered reviewed payload via SHA proof, sent explicit UTF8charset+XMLdeclaration and verified script/humanfields/sandbox exactly. Final scriptSHA2565de6150fa4743f26d27ca66f0522db262dfff0bdb1d361ece5dadf2feb37e14f. Sandbox remainsfalse; changed script still needs exact approval before execution. Approval not granted automatically; no raw XML/source containing secrets saved.

User requested moving nonsecret VK_CSI_PROJECT_ID literal from Jenkins into repo. Current global vk_project_id uses environment lookup. Prepared ai-data/devops-894-jenkins/vk-project-id.patch (one-line literal replacement) outside repo; no repo edit yet. Since taskMR104 merged, propose follow-up branch DevOps-894-store-vk-project-id in automation-test-yandex from origin/master for approval. Then publish under training gate; remove corresponding project withEnv item from working Jenkins only after master contains the constant. Final script approval should follow that final configuration. This follow-up does not alter cloud credentials, targets or retry count.


## Approved project ID branch and local implementation (2026-10-14)

User approved proposed follow-up branch DevOps-894-store-vk-project-id in automation-test-yandex from origin/master. Fetched origin/master0bfc65c, recorded SHA256 of7unrelated local MSSQL files without copying contents, created/switched approved branch; all unrelated file hashes unchanged after switch/edit. One-line global vk_project_id environment lookup replaced with the user-supplied nonsecret project ID. Value equals the previously verified VK_PROJECT_ID account configuration. Both deployment/base-publication syntax checks and diff --check passed. No Git staging/commit/push, no Jenkins change or build.

Prepared publication proposal: commit store vk project id in ansible; MR title DevOps-894 Store VK project ID in Ansible; source DevOps-894-store-vk-project-id, targetmaster. MR body in ai-data/devops-894-jenkins/project-id-mr-body.txt, one Russian paragraph plus task link. Exactlyone global variable line changed; no CI config/new infrastructure effects. Publication approval pending, merge separately. Remove working Pipeline project environment only after constant is in master, then approve the final unsandboxed script if needed.

## Project ID publication (2026-10-14)

User explicitly approved the reviewed commit, push and MR creation. Staged diff contained only the single group_vars/all.yml project ID replacement; diff --check passed. Published commit 809e772da605c3b3922584d44696c9a9ad514584 (store vk project id in ansible) on DevOps-894-store-vk-project-id. Created and verified [MR105](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/105), title DevOps-894 Store VK project ID in Ansible, target master, assignee a.solonenko, squash false, source removal true. No pipeline reported. Existing seven unrelated MSSQL changes remain outside the commit. No merge, Jenkins update or build performed; these remain separate actions.

## Project ID merge (2026-10-14)

User separately approved merging MR105. Guarded merge of exact source SHA809e772 succeeded; merge/master SHA d98f04c65900e8e1fec6a658350c554e48015fe2. Remote master group_vars/all.yml verified: project ID equals the reviewed constant; dc and common Nomad token lookup remain correct. Receipt: ai-data/devops-894-jenkins/project-id-merge-receipt.json. No local branch switch, Jenkins change or build. Working Jenkins Pipeline project environment literal can now be removed under separate external-change approval.

## Final Jenkins configuration and script approval (2026-10-14)

User explicitly authorized steps1 and2: remove project environment literal and approve final dynamic_deploy script. Applied exactly one withEnv change, leaving ANSIBLE_DEBUG=false, retry(2), credentials and all other configuration intact. Full XML readback matched intended UTF8 payload. Final Pipeline SHA256 aeb21ece7c726f2a1e7a61228e7c6b35da3326c32589a8869f36f4bba1d86541. Sandbox remains false.

Guarded ScriptApproval matched the exact live script after verifying SHA256 and approved only its pending hash. Initial API attempt stopped before mutation because this installed version exposes PendingScript.script/hash fields rather than getScript/getHash methods. Corrected field access succeeded: approved=true, matching pending entries0, total pending3→2. Receipt ai-data/devops-894-jenkins/dynamic-deploy-approval-receipt.json contains metadata only. Other pending scripts were left intact. No build triggered; runtime acceptance of working dynamic_deploy remains pending.


## Working job minimal-run preflight (2026-10-14)

User asked what to prepare for a minimal ES acceptance run. Read-only authenticated Jenkins GET verified the final script SHA aeb21ece7c726f2a1e7a61228e7c6b35da3326c32589a8869f36f4bba1d86541, disabled=false and quietingDown=false. No job or infrastructure mutation performed.

Suggested preset: TEST_INSTANCE=test5 (thin, 5GiB), AUTOMATION_BRANCH=master, ELASTIC=true; RESTORE, REDIS, RABBIT, S3, NGINX, RESTORE_B2B_ELASTIC, WEB_STATIC, MICROSERVICES and SUGGESTIONS_REINDEX=false. Hidden BRANCH remains gitlab. This does not isolate ES: Stop service, Deploy monolith and Update buildsinfo are unconditional. Origin/master app_deploy requires valid MONOLITH_PIPELINE_ID and STATIC_PIPELINE_ID even with WEB_STATIC=false; it queries both projects' pipeline jobs before the static condition. Preserve compatible existing stand versions and available artifacts/images. Its missing-artifact/image handling may rebuild GitLab jobs. ES performs full data recreation with retry(2); select an available stand and avoid concurrent deploy/refresh. Separate dynamic_deploy_es_vk_test remains the established isolated ES test. Working-job runtime acceptance has not been performed.

Changed files: this log and the existing nomad-test system map; repository and Jenkins configuration unchanged. Remaining risk: unconditional app deployment can fail after stopping the app and resetting ES. No credentials or raw Pipeline saved.


## Completed-work YouTrack comment (2026-10-14)

At the user's explicit request, posted the completed-work report to DevOps-894, comment74-124669. Exact text verified by GET after POST; no duplicate found. Covered seed transfer/CSI, merged Ansible changes, Jenkins credentials/DNS, successful check/thin/thick builds, live Pipeline update and approval. Preserved the unperformed working-job acceptance and separate DBA_Clean/AWX/canonical DNS follow-ups. Local text/helper/metadata receipt: ai-data/devops-894-jenkins/completed-work-comment.txt, post_completed_work.py and completed-work-comment-receipt.json. No deployment or issue-status change.
