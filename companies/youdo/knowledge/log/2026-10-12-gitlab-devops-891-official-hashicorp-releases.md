---
system: gitlab
status: verified
checked: 2026-10-12
tags: [nomad, awx, base-images, training]
---
# DevOps-891: official HashiCorp releases for Nomad and AWX

## Summary

User requested replacing the failing Yandex HashiCorp mirror in the Nomad image and AWX image with releases.hashicorp.com. Three URL-only substitutions prepared on explicitly approved branches; Both full no-cache builds passed and runtime version/import checks passed. Changes committed, pushed and MRs created after explicit publication authorization; merges/image releases pending.

## Task and context

[DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891/Recovery-Vosstanovit-bazovye-obrazy). [Nomad job3218387](https://gitlab.youdo.sg/sysadmins/nomad/-/jobs/3218387) exited4 at wget after APT; [AWX job3217914](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217914) returnedHTTP504/curl22. Nomad master/latest are absent, blocking nomad-n-tools and ansible-playbook. These dependent images are not changed in this task.

## Actions and changed files

Fetched both origin/master refs read-only, clean existing checkouts. Replaced two ENV URL hosts in /home/slnnk/git/nomad/Dockerfile and one Nomad URL host in /home/slnnk/git/base-images/awx-ee/24.6.1/Dockerfile. Nomad1.5.3, Levant0.3.3 and AWX24.6.1 unchanged. No download-policy, timeouts, CI or unrelated refactoring changes. Whitespace checks passed. Nomad --no-cache build passed and network-disabled smoke reports Nomad1.5.3/Levant0.3.3. Independent code review confirms only the3URL replacements and no material issues. Full local docker builds use --no-cache and task-specific images devops-891-nomad:official / devops-891-awx:official; output stored in ai-data/gitlab-recovery/devops-891-{nomad,awx}-official-build.log.

## Training record and CI effects

Proposed and explicitly approved branch DevOps-891-use-official-hashicorp-releases in both repos, from origin/master1affea3 (nomad) and b223c4c (base-images). User confirmed both branches before changes. Created branches and scoped edits only. Stage2 proposal pending: same commit `use official hashicorp release urls` and MR title `DevOps-891 Use official HashiCorp release URLs` in both repos, source approved branch/targetmaster. Both MR preference inspections: squashfalse, assigna.solonenko; source deletion onmerge true per observed preference. No user corrections.

Nomad branch name does not match feature* build filter: branch/MR publication runs no image build. User merge to master will automatically build/publish master then latest. Base-images builds only tags: branch/MR and merge do not publish AWX; release requires separately authorized recreation of awx-ee/24.6.1. Project MR settings and actual final check results will be included in publication proposal.

## Risks and remaining work

Only URL migration is authorized. All build/runtime checks and publication completed; user merges/image release verification remain pending; live items in ~/ai/TODO.md. No image deployment or dependent-image rebuild has been requested in this task.

## Final validation and publication

Nomad full no-cache build exited0; network-disabled runtime reports Nomad1.5.3/Levant0.3.3. AWX full no-cache build exited0 after Galaxy collections and hvac install; ordinary-user1000 Nomad version and hvac import pass with networkdisabled. Galaxy step was slow, public API respondedHTTP200; it ultimately completed successfully. No additional changes were made to address that delay. Diff/whitespace checks and independent review passed.

User explicitly requested publication if Nomad checks were clean; this condition was satisfied. Staged diffs contained exactly the task Dockerfile in each repo, three URL substitutions total; no pre-staged or unrelated changes. Commit message in both: `use official hashicorp release urls`; MR title in both: `DevOps-891 Use official HashiCorp release URLs`; source approved branch, targetmaster. Nomad commit1067d30a7d78cd2060b5714f107061bc3ec85560 / [MR6](https://gitlab.youdo.sg/sysadmins/nomad/-/merge_requests/6). AWX commitd90806fd731679453f6ae50dc121ba49907058c9 / [MR39](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/39). Remote SHA/source/target verified; assigneda.solonenko, squashfalse/source-delete-on-merge true. Current SHAs have no pipelines, consistent with CI rules. Both checkouts clean. SSH uses previously verified trusted IP host-key alias, strict verification enabled.

No agent merge, tag moves, production/shared-host changes or registry publication. After user merge, Nomadmaster CI publishes master/latest; AWX requires separately authorized recreation of awx-ee/24.6.1. Restore dependent nomad-n-tools and ansible-playbook only after parent manifests/digests are verified. No broader permission inferred.

## User merges and final successful retries

User merged both MRs while final open-MR verification was running: that helper returned Open MR not found; subsequent explicit GETs confirmed merged states. Nomad merge4b0d090475b3391cbcc22bed8ca2f73cd6c7e603 launched pipeline140627. Initial job3218411 failed at silent official-URL wget with exit8/server-response error; exact HTTP status not recorded because diagnostics were hidden. The user later reported repairing the build. Job3218414 on the same source succeeded; master/latest both digest sha256:b1cafbab2d5151519874bbd37ce704481a69f1e017093a6123160fe48755adba, matching build trace. Underlying runtime/network repair was not established and no geographic/proxy cause is asserted.

User requested AWX tag recreation after merge39: verifiedmaster8759867266ee1a757a1ac979251aed3467c3021a; awx-ee/24.6.1 oldSHAb9c534d... deleted/recreated on verifiedmaster. Pipeline140628 initiallyrunning, now job3218417success; awx-ee:24.6.1 digest sha256:43f8a8c1833380fcca584fe5532275c7170395f441652f584690debe73c862be matches trace. No latest alias requested for AWX.

User also rebuilt ansible-playbook job3218416/pipeline109157 on unchanged master9beb474f0d4a1ebabba44cbed5505f2a5fd4281f: successful, master/latest both digest sha256:9ae2813a0b0bd9ee38f85277b3aa44cfab3efe0be707654704d60e00c87bee4f, matching trace. Duplicate user link checked once.

Only known remaining recovery image is nomad-n-tools:1.1/latest. Both authenticated manifest GETs return404; latest tag pipeline86975 is a historical2022success, not a recovery build. Nomadlatest parent is now verified available, so local coordinator entry changed from blocked to waiting, retaining tagSHAdd2a304f6333aed240d8c23cac7a900ac6725358. No child pipeline was launched during this status check. Current inventory55successful/3seeded/1waiting/1excluded; no active base-image builds. Generated sanitized traces are recovery-latest-{3218414,3218416,3218417}.txt. Live remaining action in shared TODO.

## Final recovery completion

The remaining nomad-n-tools entry is now released; final registry reconciliation69/69passed and pulled runtime passed. See [completion evidence](2026-10-12-gitlab-devops-891-final-nomad-tools.md).
