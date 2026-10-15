---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, nexus, nuget, monolith, vk-test]
---
# Monolith runtime failure from mixed MessageBus assembly identities

## Summary

Release pipeline139914 successfully built artifacts and images, but test5 service startup fails with MessageBus assembly binding errors. Exact source chooses MessageBus NuGet1.9.1 and MessageBus.MassTransit1.8.1. Existing recovered package binaries have incompatible assembly identities: base1.0.0.0 versus MassTransit reference1.8.1.0. Package content SHA512 matches the packages installed by build_release3225571, establishing the actual consumed pair. This proves runtime incompatibility; it does not prove that Nexus recovery changed the original base assembly identity.

## Evidence

- Release SHA f89090ed12073eacceef6d05530cf2df53b764e5, pipeline139914; [build_release3225571](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3225571) restored the matching package content hashes. Build succeeded; no MSB3277 matches. Restore HTTP429 was retried successfully.
- Nomad deployment3e2177ba-876c-5298-f718-3a635d8b8883 for youdo-test5: pre-migrations exit0; representative svc-finance FileLoadException0x80131040 for MessageBus1.8.1.0 and webseocms FileNotFoundException for the same identity. Services restart and exhaust retries; image pull is not the observed cause.
- Read-only PE/CLI metadata parser /tmp/jenkins-messagebus-metadata.py inspected already existing local nupkg DLLs without execution or downloading packages: MessageBus1.9.1 contains AssemblyVersion1.0.0.0; MassTransit1.8.1 contains AssemblyVersion1.8.1.0 and AssemblyRef MessageBus1.8.1.0.
- Existing artifacts for matched MessageBus/MassTransit1.9.1 both have assembly1.0.0.0 and matching references. Matched1.8.1 artifacts use1.8.1.0; matched1.9.2 use1.9.2.0.
- Original Extensions1.9.1 CI at ccecf08b5380d584a7f17926a7b9f3c3c754a4f5 used only PackageVersion on dotnet pack; inspected source has no explicit AssemblyVersion. Therefore1.0.0.0 follows historical source configuration. Original published binaries were not available for comparison.

## Actions and limits

User authorized read-only diagnosis of monolith build logs and possible Nexus recovery relationship. No monolith source edit, new build, package publication, cache mutation or deployment retry performed. Minimal candidate is aligning the MessageBus/MassTransit package pair in the monolith, then checking source/API compatibility and rebuilding artifacts/images. Do not overwrite existing MessageBus1.9.1 with a guessed assembly identity: matched1.9.1 consumers expect1.0.0.0.

## Related work

[Static rebuild and deployment](2026-10-15-jenkins-static-release-rebuild.md). Local recovery metadata: ~/ai-data/nexus-recovery/extensions-191-build/provenance.json and artifacts; no secrets recorded.

## User correction and recovery-only option

User explicitly forbids monolith source changes. Dependency alignment proposal is not approved. Original CI for both Extensions1.8.1 and1.9.1 supplied PackageVersion only; recovered1.8.1 assembly version may originate from fallback Version override. Candidate without source changes: reconstruct affected1.8.1 packages using original versioning flags, verify their assembly references against the exact release, then separately approve Nexus replacement/cache refresh/rebuild. Exact package scope and historical binary identity still require verification; no overwrite or build initiated.

## Verified fallback versioning difference

Existing helper build_historical_nuget.py line51 adds both Version=<tag> and PackageVersion=<tag>; original Extensions1.8.1 CI line39 sets only PackageVersion. Recovery181 manifest identifies this fallback build root. MassTransit181 assembly references both MessageBus1.8.1.0 and Net1.8.1.0; its project uses ProjectReference for these libraries, so reproducing original packaging flags changes referenced assembly identities too. Prepare/inspect full reference graph before deciding the minimal replacement set. Do not assume replacing MassTransit alone restores every service or overwrite all181 packages indiscriminately.
