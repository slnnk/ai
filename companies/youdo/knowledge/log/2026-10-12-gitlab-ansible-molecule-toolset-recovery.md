---
system: gitlab
status: verified
checked: 2026-10-12
tags: [docker, molecule, registry, recovery, training]
---
# Ansible Molecule toolset recovery investigation

## Task

User identified another missing base image and requested fixing https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset. Branch and scoped local repository changes approved; repository publication completed after separate approval. User subsequently supplied successful pipeline140669 and requested updating the existing DevOps-891 recovery comment. Master/latest CI publication and the requested comment update are now verified.

## Context

Initial investigation: GitLab project437, default branch master, no open MRs; clean existing checkout /home/slnnk/git/ansible-molecule-toolset on master at8f69b7d. Subsequent task publication is recorded below. Related recovery ticket DevOps-891 was closed by the user earlier on2026-10-12; no tracker state changed. The missing latest image blocked automation-services pipeline140665/job3219595 before Molecule tests.

## Actions

Read repository Dockerfile, requirements.txt and .gitlab-ci.yml and previous image-recovery notes. GitLab GET inspection confirmed pipeline67413 on master8f69b7d; retried build job3219476 exits100 during APT update.

## Findings

Verified root cause: Debian Buster repository Release files for buster, buster-updates and buster/updates return404. Both Dockerfile stages use quay.io/pycontribs/python:3.8-slim-buster, so each stage needs source correction before its first APT update. Proposed minimal recovery retains Python3.8 and existing pinned requirements and redirects archived Debian repositories, following the [archive recipe](../../../../general/knowledge/linux/debian-eol-apt-repositories.md). A full no-cache build is required to verify current package availability.

Existing CI uses docker:stable/docker:dind and standard CI_REGISTRY_USER/PASSWORD authentication. Build filters permit feature* branches, master and tags; latest publishing permits master and tags. A DevOps task branch will not build or publish through the existing filters; merging to master automatically publishes master and latest. CI edits are outside the user's final requested scope.

Confirmed secondary build blocker: the forced ansible-galaxy installation fails with exit250 and a modern Galaxy API KeyError under pinned Ansible core2.11. The unquoted community.docker:>=1.8.0 argument also undergoes shell output redirection. The [official Ansible4.4 release dependencies](https://github.com/ansible-community/ansible-build-data/blob/main/4/ansible-4.4.0.deps) already bundle community.docker1.9.0, satisfying the requested >=1.8.0. Its [official compatibility metadata](https://github.com/ansible-collections/community.docker/blob/1.9.0/meta/runtime.yml) requires Ansible>=2.9.10, compatible with core2.11. Removing the redundant forced collection reinstall preserves the pinned distribution's existing collection; no package upgrade or replacement introduced.

## Training record

Branch DevOps-891-restore-molecule-toolset in the existing ansible-molecule-toolset checkout, base/target master. Stage1 explicitly approved by the user; branch created clean from master8f69b7d. Read-only remote ls-remote confirmed master8f69b7d. At this stage, no publication approval or external writes had occurred; subsequent stage2 approval/publication is recorded below. Existing recovery ticket closure is recorded rather than silently reopened.

User initially requested restoring bind removed by the last commit (bind9-dnsutils changed to dnsutils). A temporary local bind9-dnsutils change reached final-stage APT and failed with exit100 during the first full no-cache build. Read-only official Debian index inspection confirmed bind9-dnsutils exists in archived buster-backports. Before adding any backports source, the user explicitly corrected the scope: retain master content and only repair the build. The temporary package change was reverted; final scope preserves original dnsutils, adds no backports and changes no packages or CI configuration. This is a task-specific correction, not expanded authorization.

Second full no-cache build with original dnsutils passed APT updates and installation in both stages, then failed250 at the redundant forced Galaxy install; log /tmp/devops-891-molecule-build-master.log. Removed that one failing reinstall line as a necessary build fix, retaining the bundled compatible collection and all original package versions. Final Dockerfile scope is two-stage APT archive correction plus removal of the redundant Galaxy line.

Final build `docker build --progress=plain -t devops-891-molecule:verify .` succeeded exit0. It reused unchanged builder layers freshly validated in the preceding no-cache attempt; the changed final RUN layer rebuilt its complete APT update/install and existing Dockerfile command checks. Local image digest sha256:9005e2045da0b9112b4d10b14fbf06bb26f889f350ad8c855b9c43181afead17; log /tmp/devops-891-molecule-build-galaxy.log. User explicitly requested build validation only, with no additional runtime tests; none performed. git diff --check passed, diff contains only Dockerfile12insertions/3deletions, index empty.

Stage2 proposal: commit `fix molecule toolset build`; MR title `DevOps-891 restore molecule toolset build`; source DevOps-891-restore-molecule-toolset, target master. MR description: one Russian paragraph explaining archived Debian Buster sources and removal of redundant community.docker installation because pinned Ansible already includes it, followed only by https://youtrack.youdo.com/issue/DevOps-891. User explicitly approved publication after reviewing the final scope and checks. Staged only Dockerfile and inspected the actual staged diff. Committed81f3a8e29940ef6aa9bf84974535047d21c55739 with the approved message, pushed the approved branch and created [MR1](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/merge_requests/1) with the approved title/source/target. Helper verified remote SHA and MR parameters: assignee a.solonenko, squashfalse, remove source branch true; project settings preserved. No pipelines for published SHA, consistent with existing filters. Local checkout clean. Branch push/MR causes no image build; user merge to master automatically publishes master/latest. No merge or release performed or authorized by publication approval.

## Changes

One scoped local repository file: Dockerfile APT source correction in both stages and removal of one redundant forced Galaxy install. KB investigation log and local clone registration; short references added to the existing Nexus system map and shared backlog.

## Risks and limits

Local build and existing Dockerfile checks passed. CI jobs confirm master/latest image publication; no independent manifest digest verification or additional runtime tests performed in this follow-up. Automation-services Molecule tests have not been rerun; retry was not requested. Open work stays in ~/ai/TODO.md.

## Master image publication verified

User supplied [pipeline140669](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/pipelines/140669). GitLab GET confirms success on master SHAaad593fd36c8e036184303519c5da81217398306; [build3219854](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/jobs/3219854) and [latest3219855](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/jobs/3219855) succeeded, publishing master and latest respectively. This verifies release through actual master CI; no agent merge, release trigger or Molecule retry performed. The user-reported successful release closes the image-publication backlog item.

## Existing YouTrack comment updated

The user explicitly requested updating the task comment after the successful image pipeline. Read live DevOps-891 comment74-124638 by a.solonenko (5429characters), preserved its text and added the toolset repository/work bullets: MR1, archived APT sources in both stages, removal of redundant Galaxy reinstall, retained versions/packages and successful pipeline140669/jobs3219854/3219855. Updated the existing comment rather than creating a duplicate. Subsequent GET verified exact approved/requested text, same comment ID/author,6280characters, updated1791819119780. Issue state unchanged. Receipt and current body saved in /home/slnnk/ai-data/gitlab-recovery/devops-891-posted-comment.json and devops-891-recovery-comment.txt. No Molecule test success claimed.

## Portable lesson

none
