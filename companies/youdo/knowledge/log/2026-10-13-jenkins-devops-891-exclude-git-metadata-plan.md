---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, gitlab-ci, docker, recovery]
---

# DevOps-891: exclude Git metadata from controller image build context

## Summary

The user requested the persistent controller image correction from the Jenkins recovery plan. Read-only investigation found Dockerfile `ADD ./ ./` and no `.dockerignore`, so the image includes build-context Git metadata. Implemented minimal local correction after explicit branch approval: a new `.dockerignore` containing `.git`. Build-context regression check passes; publication completed after explicit approval; MR17 is merged, master/latest image publication succeeded and the approved controller recreation passed Git/API acceptance. Persistent image correction is complete; deployment-source alignment remains a separate follow-up.

## Context and evidence

Repository `/home/slnnk/git/jenkins`, origin `git@gitlab.youdo.sg:sysadmins/devops-tools/jenkins.git`, clean checkout on `DevOps-776-python`. Fetch verified `origin/master` at `75865e16` matches published tag `2.555.1.2`. No ancestor/project AGENTS instructions were found. Dockerfile line9 copies the context; CI line32 builds from `.`. No tracked source writes `credential.interactive`; its originating CI setting remains an inference, while copying `.git` into the image is directly established. Runtime removal of that key previously restored credentialed branch discovery.

## Implementation plan

Goal: prevent build-checkout `.git` metadata and its local credential configuration from entering the Jenkins controller image.
Architecture: Docker excludes `.git` before the existing Dockerfile copies the build context. Keep Dockerfile, tools and other context files unchanged. Technology: Docker build context and GitLab CI. Execution: inline in the existing checkout; no worktree.

1. Obtain approval for branch `DevOps-891-exclude-git-metadata` in `/home/slnnk/git/jenkins` from `origin/master`, then create/switch to it and add only `.dockerignore` containing `.git`.
2. Inspect the actual task diff and run whitespace/context checks. Check that existing image build commands do not require copied repository metadata.
3. Present the exact diff, checks, commit/MR names and CI effects for publication approval under the supervised Git workflow.
4. After separately approved image release, verify a fresh image excludes `/.git` and the offending credential configuration. After separately approved controller recreation, repeat credentialed Git lookup. A normal restart of the already patched container is insufficient evidence.

## Approval boundaries and CI effects

User explicitly approved («Да») branch DevOps-891-exclude-git-metadata in the existing checkout from origin/master75865e16c836d43294aa4d08e7ae4ee6f9b4010e and the one-file local change. Branch creation and .dockerignore implementation are complete. User explicitly approved stage2 («Да»), covering the reviewed one-file staging, commit, push and MR creation. Those actions are complete; no merge/tag/image release or controller recreation occurred. Proposed task branch push runs only the existing noop MR job (including inherited registry login), not image build/publication. Master/tag pipelines publish both version and `latest`; release/tag, merge and runtime recreation require their own explicit approvals and are outside branch approval. Keep current quiet mode and recovery hook unchanged during preparation.

## Changed files and risks

Repository change is only committed `.dockerignore`, content `.git` plus newline; worktree/index clean, no unrelated modifications. Local verification helper: ~/ai-data/jenkins-recovery/verify-build-context.py. This KB note, Jenkins map, TODO and repos row were updated. Fresh-image behavior remains unverified until an approved build/release. Do not claim Jenkins is permanently corrected based on the existing runtime fix. Open work remains in `~/ai/TODO.md`.

## Verification and review

Docker SDK4.4.4 synthetic build-context check ran without a daemon or secrets: RED before correction exited1 with .git metadata PRESENT; GREEN after correction exited0 with metadata EXCLUDED. All four tracked payload files remained in the context. Whitespace diff check passed (no-index new-file diff exits1 normally, validated by wrapper assertion). Fresh review found no Critical/Important findings. These checks establish context exclusion only; fresh-image and recreation/Git lookup acceptance remain pending.

## Publication proposal and approval ledger

Proposed commit: `exclude git metadata from image build context`. MR title: `DevOps-891 Exclude git metadata from image build context`. Source: `DevOps-891-exclude-git-metadata`; target: `master`. Body prepared in ~/ai-data/jenkins-recovery/devops-891-git-metadata-mr-body.txt: one Russian paragraph and DevOps-891 task link. GitLab project391 read-only inspection confirms default master, squash default_on, remove_source_after_merge=true, assignee a.solonenko and no existing task MR. Preserve those project settings. User approval ledger: local branch/change approved «Да»; reviewed stage2 publication approved «Да» and executed. Branch push only invokes existing noop MR job with inherited registry login, with no image publication. Future master/tag pipelines publish both version and latest and require separate explicit approval for those effects.

## Publication result

Staged diff inspected: exactly .dockerignore, onefile/+1/-0, with empty index before staging. Commit3419ae2d98aeb611bfeb04967788c3eea8b8489b, `exclude git metadata from image build context`, contains only this file. Pushed approved branch and created [MR17](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins/-/merge_requests/17), source DevOps-891-exclude-git-metadata to master, title as proposed. Independent GET confirms SHA/settings: assignee a.solonenko, squash=true, remove_source_after_merge=true. Worktree clean. [Pipeline140771](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins/-/pipelines/140771) still running after more than10minutes, with only job3222945 `step to fix mr`; its noop script has not started. Runner106 `gitlab-runner-docker-2 (172.28.0.172)` is preparing executor/pulling docker:dind and docker:stable. Trace contains10lines with preparation/pull only, no checkout/script, explicit errors, network timeout, DNS/TLS or rate-limit markers. CI is pending runner image preparation, not passed; no image-build jobs. No job cancel/retry or runner change was authorized or performed. User subsequently authorized merge and controller recreation («Можешь merge делать и пересоздать контролле для проверки.»). Merge is complete; master image publication is in progress and recreation has not yet occurred. Controller runtime correction and quiet=true remain unchanged.

## Approved merge and release checkpoint

User authorization explicitly covers MR merge and controller recreation for verification; master pipeline version/latest image publication is an expected merge effect. Source pipeline140771/job3222945 finished SUCCESS: preparation1070seconds then checkout/script about3seconds. Slow image-pull cause remains unproven. SHA-guarded MR17 merge returned merged, mergeSHA96a754a6abe44c4049b61cee287ab07d1c46ef15, squashSHA3419ae2d98aeb611bfeb04967788c3eea8b8489b; squash/remove-source settings preserved. New [master pipeline140773](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins/-/pipelines/140773) has build3222952 running and latest3222953 created. BuildKit accepted the build and base-image downloads progressed; no obsolete API error was observed. Fixed-image publication remains pending.

## Recreation preparation and gates

Local helpers recreate-fixed-controller.sh and controller-release-status.py under ~/ai-data/jenkins-recovery validate exact pipeline/push digest provenance. Preflight confirms controllerID239180c9d8f2503e95edae05f85806654840a41772280c79d74daa563d224859, expected /data UUID and131GBfree; existing data mounts and quiet hook will be retained. Fresh API preflight confirms quiet=true, queue0, active executor tasks0,11jobs and nodes online. Local GET verify-git-parameter.py verifies stored-credential branch lookup via property/parameterDefinitions/allValueItems/values:205branches and master present before recreation. Initial zero result was an instrumentation parsing bug, not a Jenkins failure. Reviewer found no Critical/Important issues; final fresh controller/API/Git checks are still required after recreation. No fixed-image pull or controller recreation has occurred at this checkpoint.

## Final release and recreation result

Master pipeline140773/build3222952/latest3222953 all SUCCESS. Master/latest digest sha256:458ac695b4114f0f3f837a3c99294c1a82e629ab2b53b1be2ea35c97a9425e71 matched exact push traces and was deployed by approved guarded recreation. New containercc6f744294ff77471b765d30e543883ea738dc3108e0abb2b23734dc8a7758c4 preserves mounts, data UUID and quiet-hook hash/mode. API2.555.1/11jobs/116plugins/quiet=true/queue0; AutoTest5online. Root .git/credential setting absent without manual unset; stored-credential GET branch lookup205/master present. Persistent fix is complete. Prior pending checkpoint statements are historical. Canonical Ansible/base compose retain old version; runtime digest override must be reconciled under separate approved configuration work. See [final execution and evidence](2026-10-13-jenkins-devops-891-fixed-image-recreation.md).

## YouTrack comment actualization

The user explicitly requested updating the existing task comment. Updated DevOps-891 comment74-124638 in place, preserving unrelated repository/results entries and the existing structure. Controller version restoration remains historical; current master/latest digest, MR17 merge, successful pipeline140773 and verified controller recreation/Git205 are now recorded. The remaining Ansible image-pin synchronization is stated. No dated supplement or duplicate comment was created. The publisher guarded the previous text SHA and independently verified exact returned text. Receipt: updated1791910089885, SHA25658b21000ea1d816c2836f5d840faa4b7e6c40e06a91a024536088ccf23d78fd2. Local current-comment cache was refreshed.
