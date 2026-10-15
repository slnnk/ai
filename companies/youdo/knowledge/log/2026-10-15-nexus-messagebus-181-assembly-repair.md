---
system: nexus
status: verified
checked: 2026-10-15
tags: [nexus, nuget, jenkins, monolith]
---
# Historical MassTransit1.8.1 assembly identity correction

## Summary

User explicitly authorized local build and Nexus publication after forbidding monolith source changes. Rebuilt and replaced only YouDo.Extensions.MessageBus.MassTransit1.8.1 from exact historical Extensions tagSHA4ff3a7590042b2a53ca9e7e709e9d0dab776ec95. NuGet version remains1.8.1; assembly identity and references now use historical1.0.0.0, matching the release-selected MessageBus1.9.1 DLL. Existing Net1.8.1 DLL assembly1.8.1.0 successfully satisfies the candidate reference1.0.0.0 in a local .NET6 binding probe. No other package, repository policy, source branch, Git ref, CI job or service was changed by this correction.

## Context and cause

Exact monolith release139914 selects MessageBus1.9.1, MassTransit1.8.1 and Net1.8.1. Initial fallback builder build_historical_nuget.py added Version=<tag> together with PackageVersion=<tag>. Original Extensions1.8.1 CI uses PackageVersion only. The override changed assembly identities, producing an incompatible MessageBus reference1.8.1.0 while selected base191 DLL is1.0.0.0. [Original runtime diagnosis](2026-10-15-jenkins-monolith-messagebus-assembly-mismatch.md).

## Build and checks

- Clean isolated source copied from the already verified181 snapshot, excluding obj/bin/.git; source itself unchanged. Provenance recorded in ~/ai-data/nexus-recovery/extensions-181-assembly-repair-20261015/provenance.json.
- Reused next-libraries/build_exact_native.py with version-modepackage, SDK6-jammy, historical Release configuration and PackageVersion1.8.1 only. Artifact contains netstandard2.1 DLL. Dependencies remain MessageBus/Net>=1.8.1 and MassTransit/MassTransit.RabbitMQ7.2.2.
- Metadata parser confirms candidate assembly1.0.0.0, references MessageBus1.0.0.0 and Net1.0.0.0. Existing selected191 MessageBus assembly1.0.0.0 and181 Net assembly1.8.1.0 unchanged.
- Offline default AssemblyLoadContext probe in separate processes reproduces old FileNotFoundException for MessageBus1.8.1.0. Candidate resolves both references and loads all21types including reflected methods, constructors and properties. Custom-resolver draft was replaced with default runtime binding before publication; initial local UID/XDG permission issues corrected. This is a binding/reflection check, not full service startup.
- Independent read-only review found no blockers. Runtime recorded as .NET6 family, without asserting a patch version that was not inspected.

## Publication and verification

- Existing nuget-private storagewritePolicyALLOW GET-confirmed. Scoped publisher refuses any baseline except the diagnosed old SHA2561808e5323460ae081c511fdc230fcdfe3d12aa5f53df8f2b19d0a1392074cfad and guards exact target/version/new artifact hash.
- First upload through public index failed and asset checksum remained old. GET confirmed public private index lacks PackagePublish resource while internal index exposes PackagePublish/2.0.0. Safely retried same authorized replacement through historical internal endpoint after verifying failed receipt and unchanged old checksum; no policy mutation or component deletion.
- Final NuGet push exit0. Nexus REST asset metadata SHA256 matches candidate9f557ada75b1032044635dc2ba0169b2d049e8cadc2e21cb643a778c154aad9f; public version indexHTTP200 includes1.8.1. Verification uses metadata only, no downloaded packages.
- Authentication route reused existing nuget identity from GitLab youdo.business NuGet.Config, retrieved in memory with current/.env GitLab token. Credentials supplied only via child environment; no values printed or stored. Secret-free publish config and nonsecret receipts retained locally.

## Files and limits

Local helpers publish_messagebus_assembly_repair.py and verify_messagebus_assembly_repair.py, candidate source/artifact, compatibility logs and publication receipts under ~/ai-data/nexus-recovery. No repository checkout edits or commits. Monolith artifacts/images were not rebuilt and existing package caches were not cleared; a fresh restore/rebuild is required before the corrected bytes can reach deployed services. Changing a published version requires selected consumer caches to be refreshed, not a blanket cache deletion.
