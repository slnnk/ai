---
system: gitlab
status: verified
checked: 2026-10-12
tags: [registry, fastlane, training]
---
# DevOps-891: Fastlane image manifest publication

## Summary

The image in job3218390 built successfully but push rejected an OCI index referencing a missing child image manifest. Minimal provenance opt-out is ready, full local build and direct Fastlane startup/lane enumeration passed; registry acceptance remains unverified until CI. Separate explicit bundle-exec startup exposes a preexisting missing abbrev dependency.

## Task and context

User added [job3218390](https://gitlab.youdo.sg/sysadmins/devops-tools/mobile/fastlane-docker/-/jobs/3218390) to [DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891/Recovery-Vosstanovit-bazovye-obrazy). Project503, `/home/slnnk/git/fastlane-docker`, master/tag0.0.9 commit82705653.

## Evidence and actions

Latest cache image was absent, so cache imported nothing; Ruby3.4.4-bullseye/Fastlane2.227.2/plugins installed. Trace exported image manifest dea7e2f797316a347283f6af18dca76c37db4fcf312cd741842a656ef435fead, attestation and manifest list. Layers pushed, then registry rejected exactly the image manifest as unknown. Disabling cache has no supporting evidence. Underlying registry/client handling was not proven; --provenance=false is a controlled compatibility workaround, not a confirmed storage repair.

Added --provenance=false to both docker build commands in .gitlab-ci.yml. Docker documents provenance opt-out: https://docs.docker.com/build/metadata/attestations/ . GitLab describes missing children during manifest-list push: https://docs.gitlab.com/user/packages/container_registry/troubleshoot_container_registry/ . Full local build with this flag passed. Parsed CI YAML and whitespace check passed. Direct fastlane --version reports2.227.2 and fastlane lanes exits0, matching Android CI command style. Ruby version and bundle check pass. Extra bundle exec fastlane --version fails because highline2.0.3 requires undeclared abbrev under Ruby3.4; secondary UpdateChecker NameError masks original LoadError. No Gemfile/lockfile changes in this CI-only scope; separate actionable item is in shared TODO.

Validation context was made with git archive of tracked Dockerfile/Gemfile/lockfile/fastlane paths only. Existing untracked .codex, README and service-account JSON were neither read, copied nor changed. Logs live in /home/slnnk/ai-data/gitlab-recovery/devops-891-fastlane-{build,smoke,direct-smoke}.log.

## Training record and publication effects

Stage1 user approved branch DevOps-891-restore-fastlane-build from origin/master by reply "Да, создать ветку". Created approved branch and changed only CI YAML. Stage2 proposed commit `disable provenance for fastlane image builds`, MR `DevOps-891 Disable provenance for Fastlane image builds`, source approved branch, target master; approval pending. No git staging, commit/push/MR/tag or registry mutation. MR pipeline build dev will build and publish an image under the source-branch tag; it does not update latest/version0.0.9 or run store lanes. Later version tag pipeline separately updates version and latest. Assign a.solonenko, squash false, source deletion on merge true according to inspected project settings.

## Limits

No registry push verification yet, so runtime image publication remains unresolved. Local classic image store does not reproduce the original containerd-attestation push path. Independent reviewer agrees the minimal workaround is plausible but requires remote CI verification. No changes to release-store logic, Ruby/Fastlane versions or cache policy.

## Published CI workaround result and new requested scope

Stage2 user approved publication with "Сделай", explicitly including MR branch-image publication. Committed only CI YAML as ab82e55990ecbd350875414303406134444e3f12 and created [MR6](https://gitlab.youdo.sg/sysadmins/devops-tools/mobile/fastlane-docker/-/merge_requests/6). Remote SHA/settings verified; three unrelated untracked files preserved. MR pipeline140615/job3218391 succeeded and published source-branch image; authenticated registry digest matches trace sha256:879a6897be1c27ce26d2aa31b7dba2ed038ea9dff826060fc2033a86f06876cd. The manifest workaround is now verified in actual CI.

Plugin activation warning: plain fastlane install_plugins installed global RuStore1.1.0 requiring Faraday2 while old Fastlane loaded Faraday1.10.6, despite Pluginfile/lockfile pin1.0.6. Builder exits0 after warning; store plugin activation is not established by image publication. User asked to update Fastlane to latest and then all plugins. Continuing on already approved open MR branch; expanded changes will require renewed publication approval. RubyGems API on2026-10-12 verified Fastlane2.241.0 (2026-10-10), Huawei1.1.3 and RuStore1.1.0. Fastlane now declares Faraday~>2.7 and abbrev~>0.1. Dockerfile/Gemfile/Pluginfile pins updated locally; plugin installation uses frozen bundle install rather than a global unlocked plugin installer; lockfile generation and full build validation ongoing.

## Final follow-up

Superseded intermediate recovery state: all seven legacy releases and updated Fastlane0.0.9/latest are now verified; see [final release evidence and remaining blockers](2026-10-12-gitlab-devops-891-fastlane-upgrade-legacy-archive.md).
