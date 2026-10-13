---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nomad, ansible, gitlab-ci]
---
# Persist Nexus Docker credentials for three Nomad clients

## Summary

Common Nexus Docker auth for all hosts whose Nomad role writes Docker config is published in MR1371, together with Docker28.5.2 DinD pin for allthree Molecule jobs. Latest approved commit f4018c2bf2e1d08cb2bf4c739bf64b3b667c4853 on DevOps-890-nexus-docker-auth targets master. Password is sourced from controller environment NEXUS_DOCKER_PASSWORD, never stored in git. Static checks/review pass; full Molecule verification not run after the latest commit: user explicitly declined the proposed manualjob start. Earlier three-host scope and CI-image/API blockers below are historical.

## Task and context

User requested persisting the approved runtime client changes in automation-services. Existing checkout has unrelated runner/Terraform modifications, preserved. User approved the bounded design and reuse of DevOps-890-update-jenkins-images with master as proposed base by replying Yes. No separate worktree or branch switch used.

## Changed files

- roles/nomad/templates/docker_auth_config.json.j2: optional Nexus entry when nomad_client_nexus_docker_user defined; preserve registry/user-agent.
- roles/nomad/tasks/docker-auth.yml: nonempty Nexus user/password guard before file writes; no_log on secret-bearing template.
- inventories/prod_selectel/host_vars/msk3-nomad01.youdo.corp.yml
- inventories/prod_selectel/host_vars/msk3-nomad02.youdo.corp.yml
- inventories/prod_selectel/host_vars/msk3-nomad03.youdo.corp.yml

Each new host file supplies docker username and env lookup password. Group-wide configuration avoided because cluster_docker_clients also includes172.24.0.14/msk3-nomad06. No new secret in repository.

## Validation

Ansible Templar fixture failed before implementation because Nexus entry missing. Final actual inventory/template rendering passes for11/12/13: expected docker credentials and original registry credentials/user-agent;14 has no Nexus entry. Executed real new assert task locally with fixtures: nonempty accepted, empty rejected before writes. cluster_docker.yml syntax-check passes with preexisting unmatched nomad_master_test/nomad_agent_test warnings for selected prod_selectel inventory. Scoped git diff --check passes. Full-tree diff check flags existing unrelated runner cron trailing whitespace, not changed. Molecule not installed locally; existing molecule-nomad CI runs on role changes. Read-only reviewer found no blocking scoped issue. No runtime apply/check or secret output. Five task files,23 additions/1 deletion including new files; index untouched.

## Training record

Task DevOps-890 recovery context; repo automation-services. Proposed and approved reuse DevOps-890-update-jenkins-images/master, existing checkout. Stage1 approval: user Yes to branch/design proposal. Proposed commit configure nexus auth for nomad clients; provisional MR title DevOps-890 Configure Nexus Docker auth for Nomad clients. Stage2/publication not requested or approved; no git state-changing commands executed. Full eventual MR scope needs re-evaluation against current live target because local HEAD is absent remotely.

## Publication limitation and stale GitLab references

Current GitLab project216 master SHA7cff3d8c7006a0a2bf58b9b224a329326f921dbf. Source branch API404; local HEAD3ad647f0ff6ed5b8d17e14f42401b0577a5ede21 API404. Existing KB MR1368 recovery link now points to merged AP-2347-vk-freeipa, not the earlier described recovery MR; old IDs are not safe to reuse after restore. Read-only git fetch origin master failed because GitLab ECDSA host key differs from known_hosts. No host-key entry removed, no verification bypass, no branch/base mutation. Cached origin/master diff includes the earlier local Jenkins recovery commit, so cannot claim that a future MR contains only Nexus task files until source/base is resolved. User informed. Next publication proposal must reflect actual current source/target diff and checks.

## Risks and limits

Ansible controller must provide NEXUS_DOCKER_PASSWORD; missing value now stops explicitly instead of overwriting the manual Nexus configuration. AWX/Jenkins execution environment injection not configured in this task. Local repository changes still uncommitted, no MR created, no remote apply. Existing runtime configuration on clients11/12/13 verified separately in [operational log](2026-10-12-nexus-sorm-runner-image-auth.md).

## Execute request: SSH verification and current base reconciliation

User said Execute after local completion/publication limitation. Live root SSH to trusted138.16.203.174 independently confirms ECDSA fingerprint SHA256:B8orh9AIJGui+bDHs9P6YqsDRhCCIIiEVnCB8WoLT9A matching known_hosts IP entry and prior verified notes. Fetch succeeded using GIT_SSH_COMMAND ssh StrictHostKeyChecking=yes HostKeyAlias=138.16.203.174 HostKeyAlgorithms=ecdsa-sha2-nistp256; no verification bypass or known_hosts mutation. origin/master now7cff3d8c. Cached old master was ahead of restored target; existing local branch would include13 unrelated network/Jenkins files, not just five task paths.

Read-only checks show no dirty tracked path differs between HEAD and current origin/master; Nomad role base identical and new host_vars absent on target. Clean new branch can preserve all working-tree changes in existing checkout without stash/reset/worktree. Proposed corrected source DevOps-890-nexus-docker-auth from origin/master7cff3d8c, targetmaster; source change requires renewed user confirmation under supervised training rules. Proposed commit configure nexus auth for nomad clients, MR title DevOps-890 Configure Nexus Docker auth for Nomad clients. New-branch/publication approval pending. Expected first-push CI rules skip three Molecule jobs on zero before-SHA; later role changes can run molecule-nomad, no deployment jobs present. Molecule unavailable locally remains explicit check limitation.

Proposed MR body:

```text
Добавлена авторизация Nexus в Docker-конфигурацию Nomad clients172.24.0.11,172.24.0.12 и172.24.0.13 с пользователем docker. Пароль берётся из переменной окружения NEXUS_DOCKER_PASSWORD; существующая авторизация GitLab registry сохраняется. Task link https://youtrack.youdo.com/issue/DevOps-890.
```

## Initial publication completed, then user broadened scope

User approved corrected branch+publication proposal by replying Yes. Created DevOps-890-nexus-docker-auth from restored origin/master7cff3d8c in existing checkout; all unrelated working-tree changes preserved. Re-ran rendering4hosts and playbook syntax after base switch. Staged exactly five approved paths, inspected full staged diff, checked no NEXUS_DOCKER_PASSWORD value. Committed2c25176772194d2c5179bd015dd348d809a3b481 (configure nexus auth for nomad clients), pushed using strict verified HostKeyAlias. Created MR1371 targetingmaster, title DevOps-890 Configure Nexus Docker auth for Nomad clients, assigneda.solonenko, squashfalse/deletebranchonmerge true. Remote exact five paths/description/SHA verified, open non-draft. Pipeline140662 skipped by first-push rules. First helper publish used short expectedSHA and stopped before write; fullSHA retry succeeded. No merge/deployment.

MR: https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1371

Before final handoff, user corrected scope: config must apply to everyone, not just three Nomad clients. Interpretation stated to user: all consumers of Nomad role that create Docker auth config. Local correction on approved current branch moves nomad_client_nexus_docker_user=docker and env passwordlookup to role defaults, deletes three task-created host_vars and aligns guard with existing registry-password-defined writing condition. Final target diff has only three Nomad role files,18additions/1deletion. All hosts writing config need controller environment password; host-specific inventory settings remain overrideable. No Jenkins/runner role changes.

Correction checks: rendered11/12/13/14 plus generic fixture with bothregistrycredentials; actual assert task accepts password, rejects empty when configwritten, skips when registrycredentials absent. Actual include_role tasks_fromdocker-auth without registrycredentials and without NEXUS_DOCKER_PASSWORD passes with changed0, matching Moleculefixture. Playbook syntax/scoped diffcheck and follow-up read-only review pass; Molecule still unavailable locally. Existing unrelated changes preserved. Proposed corrective commit configure nexus auth for all nomad hosts; proposed MR title DevOps-890 Configure Nexus Docker auth for Nomad hosts. Corrected publication approval pending; second push would automatically run molecule-nomad under existing rules, no deploymentjob. Do not publish until reviewed scope/title/CI effects approved.

## Corrected publication approved and applied

User explicitly confirmed the corrective publication proposal: Confirmed. Inspected exact staged diff: roles/nomad/defaults/main.yml, roles/nomad/tasks/docker-auth.yml and deletion of three task-created host_vars; no other staged paths or secret literal. Committed5c623f522afb01e3ce6e1b3f24a1c66897e87e44 (configure nexus auth for all nomad hosts), pushed same approved branch with strict verified SSH alias. PUT updated MR1371 title to DevOps-890 Configure Nexus Docker auth for Nomad hosts and rewrote short Russian description around final common role behavior, tasklink retained. GET verifies final target diff exactly defaults/main.yml, tasks/docker-auth.yml and templates/docker_auth_config.json.j2, no host_vars; approved SHA/source/target and otherMRmetadata preserved. No merge/deployment/CI manual retry.

Push pipeline140665 initiallyrunning, job3219595 molecule-nomad running. MR pipeline140666 skipped, optional manualjob3219596 by existing fallbackrule. CI final result pending. Existing unrelated working-tree changes remain unstaged.

## Corrected CI result

Push pipeline140665 job3219595 molecule-nomad failed after30s during executor preparation: manifest for registry.youdo.sg/sysadmins/ansible-molecule-toolset:latest not found, manifest unknown. Molecule never started; this is a missing CI build image in restored registry, not evidence of a role test failure. No retry, image rebuild/publication or unrelated CI code modification authorized/performed. Local checks/review remain passed; full Molecule verification remains blocked by the image prerequisite. MR still published with approved common configuration. Missing toolset recovery tracked separately in live backlog.

## User-built CI image verified

User reported building the missing toolset image. GET project-scoped Registry tag endpoint confirms sysadmins/ansible-molecule-toolset:latest HTTP200, digestsha256:becdf509311b3a6135ef09c1618a0067a91056ad75497a4c8767e1eb2d30d93a. No image downloaded. Pipeline140665 still has failedjob3219595, MR1371 open at5c623f52. No retry yet: manual CI retry is excluded from prior publication approval and requires explicit separate authorization. First unscoped registry tag endpoint returned404; corrected project-scoped endpoint establishes presence, so404 is not artifact-absence evidence.

## Approved CI retry outcome

User explicitly approved retry by replying Yes. Preflight confirmed job3219595 remains latest failed molecule-nomad in pipeline140665; POSTretry created job3219868. Watched GET until terminalfailed after55.68s. Restored toolset image pulled successfully, digestbecdf509311b3a6135ef09c1618a0067a91056ad75497a4c8767e1eb2d30d93a. New failure before Molecule: Docker client API1.39 too old for daemon minimum1.40. CI service is unpinned docker:dind. Live toolset default-branch Dockerfile uses quay.io/pycontribs/python:3.8-slim-buster and apt-installed docker.io (line45); registry image availability is now resolved, Docker client/service compatibility remains blocking. Exact binary/daemon release numbers not independently inspected, no claim about them. No additional retry, image build, CI file change or deployment authorized/performed. Job https://gitlab.youdo.sg/sysadmins/automation-services/-/jobs/3219868.

## Same-MR Docker API compatibility correction prepared

User asked how to resolve the CI client API1.39/minimum1.40 conflict. Official Docker API matrix shows Docker28.5 daemon supportsAPI1.24-1.51, compatible with existing client1.39. Offered minimal DinD28.5.2 pin versus independent toolset CLI upgrade; user instructed doing the pin in the same MR. Existing branch/MR reused, .gitlab-ci.yml previously clean and index empty. Local edit replaces floating docker:dind with docker:28.5.2-dind for allthree Molecule jobs nginx/consul/nomad; no other code changed. DockerHub public tagmetadataGET200 confirms amd64 image exists. GitLabCI Lint without simulation validtrue/errors[]/warnings[]. Dry-run reports resultingempty pipeline because existing rules exclude jobs in simulation; this is not a syntax failure. Scoped whitespace check passes. Final targetdiff fourfiles21additions4deletions, no host_vars or unrelated dirtyfiles.

Proposed corrective commit pin molecule dind to docker 28.5.2; proposed MR title DevOps-890 Configure Nexus Docker auth and pin Molecule DinD; same sourceDevOps-890-nexus-docker-auth/targetmaster. Short Russian MR description prepared to describe common auth plus fixed DinD version; only tasklink follows. Publication approval pending for changedscope/title/CIeffect. Since only .gitlab-ci.yml changes, existing role-path rules do not automatically schedule Molecule; new compiled pipeline/manualjob needed after publication, old failedjob retry would retain previous docker:dind service. No additional retry/jobplay or imagepull performed. Manual CI start still requires separate explicit approval, not inferred from publication.

References: https://docs.docker.com/reference/api/engine/#api-version-matrix ; https://docs.docker.com/engine/release-notes/28/ . Lint summaries ~/ai-data/nexus-recovery/molecule-dind-28-ci-syntax.json and molecule-dind-28-ci-lint.json.

## Approved DinD pin publication completed

User approved commit/push/MR update by replying Yes. Staged only .gitlab-ci.yml after confirming indexempty, inspected exact three service substitutions. Committedf4018c2bf2e1d08cb2bf4c739bf64b3b667c4853 (pin molecule dind to docker28.5.2), pushed approved branch with strict SSH alias. MR1371 title/description updated to DevOps-890 Configure Nexus Docker auth and pin Molecule DinD; original source/target/settings/assignee preserved. GET verifies currentSHA and exactlyfour files: .gitlab-ci.yml plusthree Nomadrole files. Pipeline140672skipped/manualmolecule-nomad3219872; pipeline140673skipped/manual3219873. No manualjob played, no merge/deploy. Request explicit permission to play pushpipelinejob3219872 for full validation of new compiled CI config. Static CI syntax/tag metadata and scoped whitespace checks passed.

## Manual CI start declined

User explicitly replied Not needed to the proposed manualstart of job3219872. Job not played; no other CI action executed. Latest MR1371/f4018c2b remains published with static checks passed and full Molecule validation unexecuted. Record this as declined, never as CI success. Publication task complete; merge/deploy still user-controlled.
