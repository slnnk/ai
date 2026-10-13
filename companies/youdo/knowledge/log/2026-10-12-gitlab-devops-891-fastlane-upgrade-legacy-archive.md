---
system: gitlab
status: verified
checked: 2026-10-12
tags: [base-images, fastlane, training]
---
# DevOps-891: latest Fastlane plugins and legacy ASP.NET archive follow-up

## Summary

Fastlane2.241.0, Huawei1.1.3 and RuStore1.1.0 updated, dependency activation fixed and released under0.0.9/latest. Legacy ASP.NET6 Debian security archive follow-up merged and released under6.0/latest. All release digests match CI traces. Base-images recovery now54successful/3seeded/1failed/1blocked/1excluded. Gradle Android18/latest also verified. Remaining Nomad master/latest images are absent, blocking nomad-n-tools and ansible-playbook; AWX download failure remains.

## Task and context

[DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891/Recovery-Vosstanovit-bazovye-obrazy). User asked for latest Fastlane and all plugins, then explicitly requested push in both repos. Six preceding legacy releases succeeded; old legacy ASP.NET6 tag now reached Debian Security404 after its existing tool-version pin resolved the initial failure.

## Implementation and checks

Fastlane latest versions verified against official RubyGems API on2026-10-12. Dockerfile/Gemfile pin Fastlane2.241.0, Pluginfile pins Huawei1.1.3/RuStore1.1.0 and lockfile is resolved with existing Bundler2.6.9/platforms. Plugin install uses BUNDLE_FROZEN=true bundle install. The larger lock diff contains transitive dependencies of requested upgrades. Full local build passed. Network-disabled checks passed for direct and bundled Fastlane, lane enumeration and explicit plugin requires; loaded Faraday2.14.4 and abbrev0.1.2. No store lanes executed, credentials mounted or untracked files read/copied.

Legacy ASP.NET6 changes only two Debian security source URL substitutions before first APT update. Full no-cache build and all pinned tool/runtime checks passed. The prior successful cached local build did not test current package availability; CI exposed that gap. See the portable [APT archive validation recipe](../../../../general/knowledge/linux/debian-eol-apt-repositories.md) for fresh-build requirements. Independent review found no blocking issues and requested direct Fastlane validation, which passed.

## Training record and publication

Fastlane continued on already approved open MR6 branch DevOps-891-restore-fastlane-build under explicit new user scope. Base branch DevOps-891-archive-legacy-aspnet from origin/master f5f31c2 proposed and explicitly approved before editing. User requested push after receiving actual version/scope/check status; commits `update fastlane and plugins` (ba402cadfb2488d4841da210433b5f084e722d0f) and `use debian archive for legacy aspnet` (a4f6fcbf42418d4cc3bc5f89f327efc713fb1f7f) contain only4Fastlane paths and1base Dockerfile. Unrelated3untracked Fastlane files preserved.

After push, separately presented/approved MR creation and metadata actions because the user's push request did not explicitly cover them. Created [base MR38](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/38), title DevOps-891 Use Debian archive for legacy ASP.NET; updated [Fastlane MR6](https://gitlab.youdo.sg/sysadmins/devops-tools/mobile/fastlane-docker/-/merge_requests/6), title DevOps-891 Update Fastlane and plugins and final Russian one-paragraph/task-link description. Source/target master, assignee a.solonenko, squashfalse/source-delete-on-merge true verified. No agent merge or tag writes beyond explicitly requested actions.

User merged MR38: mergeSHA b223c4c0b8dd2efa22024d891f5117f75b11a3d6; requested recreation of only microsoft/aspnet-6/6.0+latest. OldSHA f5f31c2, newtag exactly verifiedmaster; pipeline140625/job3218404 succeeded. Version6.0 and latest both digest sha256:5882ff1f20f0b0a7cfa3f56eaf9513373dda79cbaa9646fa260eab85586de19c, matchingtrace.

Fastlane MR branch pipeline140623/job3218402 succeeded and digest matchestrace. User merged MR6, independently verified mergeSHA75a83f782a0528db74552d63569d029d1a25e950, then supplied successful release job3218403/pipeline140624/ref0.0.9. Source verifies updated versions/frozen installer, no plugin-activation warning. Version0.0.9/latest both digest sha256:0104d89492506033fea060ed95a84676130f0b5278fd634e5a386ca019320f10, matchingtrace. This agent did not mutate the Fastlane release ref; the user supplied the successful release job.

## Additional discovered image recovery

User rebuilt [Android Gradle pipeline118913](https://gitlab.youdo.sg/sysadmins/devops-tools/gradle/-/pipelines/118913), fresh build job3218400, masterSHA4990136b2d72858c40adf4a7531ecde067687124. Authenticated18/latest manifests both digest sha256:57ddf9a61415b00b872c58a851d9ef47b3bb5779e06cc00aa518d91225c74a67, matching available job traces. Latest job2334752 is historical; do not claim it was newly executed.

User found [ansible-playbook job3218401](https://gitlab.youdo.sg/sysadmins/ansible-playbook/-/jobs/3218401), project363/masterSHA9beb474f0d4a1ebabba44cbed5505f2a5fd4281f. Fails before build because parent registry.youdo.sg/sysadmins/nomad:master is absent. CI builds onlymaster and publishes master/latest. No changes prepared in this repository; restore the Nomad parent first. Final reads: Nomad job3218387failed/script_failure, authenticated master/latest manifests both404.

## Changed files and evidence

Five scoped repo files, this log, existing GitLab/Android maps, repo catalog and shared TODO; local recovery state updated preserving attempts. Generated sanitized traces, version metadata and validations are in /home/slnnk/ai-data/gitlab-recovery. final-releases-20261012.json captures both releases; legacy-release-verification-20261012.json captures six earlier release digest/alias checks. Remaining live actions only in ~/ai/TODO.md.
