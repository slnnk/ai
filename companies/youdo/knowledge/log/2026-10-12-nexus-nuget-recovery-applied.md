---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nuget, recovery]
---
# NuGet recovery steps 1-4 applied and verified

## Summary

User explicitly authorized steps1-4 of the [NuGet recovery plan](2026-10-12-nexus-nuget-recovery-plan.md). NuGet stores, repositories and compatible CI identity were restored, with public metadata/package reads and authenticated principal verified. Private package restoration and full service restore remain outside this execution scope.

## Authorization and actions

Approval: user said to execute1-4. Ran local `apply_nuget.py` read-only preflight then `apply_nuget.py --apply`; both exited0. Re-read both live master NuGet.Config files and compared all Nexus credentials in memory. Username nuget and existing password matched; no values persisted. Repository payloads recursively checked against downloaded OpenAPI required fields/types/enums, filtering unsupported GET fields and optional nulls. Plan saved outside git at ~/ai-data/nexus-recovery/nuget-plan.json with no secrets.

Rechecked assets of all three defaults were empty with no continuation token; created File blob stores nuget-hosted/nuget-cache with relative paths under existing /nexus-data/blobs. Deleted only verified-empty nuget-group, nuget-hosted and nuget.org-proxy. Created hosted nuget-private using nuget-hosted store (ALLOW policy), V3 proxy nuget.org-proxy using nuget-cache to https://api.nuget.org/v3/index.json, and group nuget using nuget-cache with members nuget-private then nuget.org-proxy. Existing storage/HTTP/cache policies retained except requested store/name/membership changes. GET-verified exact relevant fields for all repositories.

Created one role ID/name nx-nuget: nx-repository-view-nuget-*-browse/read and nx-repository-view-nuget-nuget-private-add/edit; no inherited roles, delete or admin permission. Created active user nuget with the existing service password and sole role nx-nuget, source default; GET verified role permissions/user status and assignment. Required service email placeholder ci@youdo.com, no email sent.

## Verification

`verify_nuget.py` exited0. Both public legacy indexes HTTP200 with valid NuGet resources. Authenticated https://nexus.youdo.com/repository/nuget/v3/content/newtonsoft.json/index.json returns200 and includes13.0.3. Registration path /v3/registration/5/newtonsoft.json/index.json returns200 JSON with items. Anonymous .nupkg download of Newtonsoft.Json13.0.3 returns200,2441966 bytes; ZIP CRC and nuspec identity/version validated. Nexus request.log independently shows authenticated principal nuget for the marked metadata request, proving the existing password works despite anonymous being enabled. No package push or full dotnet restore executed.

## Configuration boundaries and remaining limits

No nginx edits/reloads: existing static service indexes and hostname upstream retained. Both public index aliases currently resolve resources through group nuget, preserving previous read behavior. Package publishing discovery/API-key compatibility not validated; hosted publishing may require follow-up and NuGetApiKey realm if API-key method is selected. Active realms unchanged; no token/key regenerated. Anonymous remains enabled per earlier approval. Hosted nuget-private starts empty; package recovery remains necessary for private dependencies. BaGet availability and complete restores of both services remain unverified.

## Changed files and risks

Nexus stores/repositories/role/user only, plus local execution/verification helpers and KB bookkeeping. No service repository changes, git publication, CI retry or remote network change. Plaintext credentials already exist in private consumer config; record only their location. Temporary anonymous grants repository reads and must be disabled after recovery/credential setup per existing TODO.
