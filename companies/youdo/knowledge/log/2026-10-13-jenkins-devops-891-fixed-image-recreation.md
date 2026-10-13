---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, recovery, docker, gitlab]
---
# DevOps-891: fixed controller image published and recreated verification passed

## Task

Finish the persistent controller Git correction under DevOps-891 by publishing the merged image and verifying an actual controller recreation.

## Context

User explicitly authorized «Можешь merge делать и пересоздать контролле для проверки.» MR17 merged96a754a6abe44c4049b61cee287ab07d1c46ef15 from source3419ae2d98aeb611bfeb04967788c3eea8b8489b. No tag or additional infrastructure mutation was requested.

## Actions

[Master pipeline140773](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins/-/pipelines/140773) succeeded: build3222952SUCCESS, duration1885.37seconds (31m25s), latest3222953SUCCESS. Registry master/latest both resolve sha256:458ac695b4114f0f3f837a3c99294c1a82e629ab2b53b1be2ea35c97a9425e71, independently matched to exact pipeline push traces before deployment.

Approved recreate-fixed-controller.sh execution on root@10.18.26.8 guarded old container239180c9d8f2503e95edae05f85806654840a41772280c79d74daa563d224859, pulled the verified digest, scanned15image layers (root Git metadata0, image startup hooks empty), wrote protected /data/jenkins/compose-devops-891-image.yml mode0600 containing only services.jenkins.image pinned to that digest, and ran docker-compose base+override up -d --no-deps --force-recreate jenkins. No raw compose environments or credentials were printed.

## Findings

New containercc6f744294ff77471b765d30e543883ea738dc3108e0abb2b23734dc8a7758c4 has imageID sha256:458ac695b4114f0f3f837a3c99294c1a82e629ab2b53b1be2ea35c97a9425e71. All mount signatures, including anonymous volume, were preserved; /data UUID unchanged with131GiBfree preflight. Recovery-hook hash unchanged, mode0600.

Post-recreation authenticated API confirms Jenkins2.555.1,11jobs,116active plugins, queue0, quiet=true, controller10executors and AutoTest5online. Root .git and credential.interactive are absent without a post-recreation manual unset. Stored-credential Git parameter GET returns205branches with master, matching baseline. Public HTTPS/login through corporate OpenVPN tun0 returns200 from138.16.201.238. Persistent image correction and recreation verification are complete; AutoTest actual checkout and downstream functional tests remain unverified.

Measured slow CI included master preparation approximately407seconds, slow base-image pulls and Python PGO compilation. Source MR job preparation was1070seconds, a separate measurement. Bandwidth throttling as cause is unproven. Runner105 uses mirror.gcr.io rather than Nexus for this image path; no Docker API compatibility error was observed.

## Changes

Approved image master/latest publication and controller recreation, protected digest override, local helpers under ~/ai-data/jenkins-recovery and KB records. No tags, unrelated infrastructure changes, tracker comments, job retries/cancellations or runner changes. See [plan/approval ledger](2026-10-13-jenkins-devops-891-exclude-git-metadata-plan.md).

## Risks and limits

Canonical Ansible and base compose still refer to old2-555-1-2; runtime uses the protected digest override. Future base-only automation could restore the old image. Align approved deployment configuration later under existing deferred Ansible publication work; no repository adaptation was made now. Broader recovery remains open in ~/ai/TODO.md.

## Portable lesson

[Exclude copied Git metadata from Docker build contexts](../../../../general/knowledge/docker/git-metadata-in-build-context.md).

## YouTrack comment actualization

The user explicitly requested updating the existing task comment. Updated DevOps-891 comment74-124638 in place, preserving unrelated repository/results entries and the existing structure. Controller version restoration remains historical; current master/latest digest, MR17 merge, successful pipeline140773 and verified controller recreation/Git205 are now recorded. The remaining Ansible image-pin synchronization is stated. No dated supplement or duplicate comment was created. The publisher guarded the previous text SHA and independently verified exact returned text. Receipt: updated1791910089885, SHA25658b21000ea1d816c2836f5d840faa4b7e6c40e06a91a024536088ccf23d78fd2. Local current-comment cache was refreshed.
