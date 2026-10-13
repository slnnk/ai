---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nuget, recovery]
---
# NuGet recovery inspection and action plan

## Summary

Read-only inspection: restored Nexus has empty default NuGet repositories but lacks legacy nuget/nuget-private names and the nuget user required by both services. Public static indexes return200 while their package endpoints return404. Plan only; no remote configuration changes performed.

## Goal and architecture

Restore existing NuGet consumer URLs and credentials without service repository edits. Use separated hosted/cache blob stores, a nuget.org V3 proxy, private hosted repository and combined group; create one consolidated nx-nuget role analogous to nx-maven/nx-docker. Existing temporary anonymous access remains enabled until the separately tracked recovery follow-up.

## Evidence and consumers

Live GitLab default master root NuGet.Config in youdo/microservices/youdo.business and youdo/youdo uses https://nexus.youdo.com/repository/nuget/index.json and https://nexus.youdo.com/repository/nuget-private/index.json. Each uses Username=nuget with ClearTextPassword present. In-memory comparison confirms the same Nexus password across all four entries in the two live master configs. Secret values are not recorded; credential source is the private GitLab file via authorized API GET. youdo/youdo also references BaGet at http://baget.youdo.sg/v3/index.json with a separate user. These external service files were not changed. Top youdo group variable keys include NUGET_SOURCE and NUGET_TOKEN; values not recorded.

Current Nexus users: admin, anonymous, gitlab(nx-docker), maven(nx-maven). No nuget user/role exists. Active realms NexusAuthenticatingRealm and DockerToken. Nuget-hosted, nuget.org-proxy and nuget-group are online, all use default storage, each asset listing empty with continuationToken=null. Proxy remote https://api.nuget.org/v3/index.json, versionV3. Group members nuget-hosted and nuget.org-proxy. Other Docker/Maven stores exist.

Public nginx exact locations /repository/nuget/index.json and /repository/nuget-private/index.json both alias /var/www/nuget/index.json. All static resources point to https://nexus.youdo.com/repository/nuget/v3/*. Prefix locations forward unchanged URI to msk3-nexus.youdo.corp. Public newtonsoft.json version endpoints for both legacy repositories return404; internal default hosted/group indexes return200.

## Action plan

1. Prepare API payloads outside service repositories in ~/ai-data/nexus-recovery. Recheck default NuGet repositories are still empty immediately before any deletion; preserve existing policies/HTTP settings. Validate payloads against current downloaded OpenAPI. Review credential consistency between both live configurations; existing CI username stays nuget and password is reused in memory only.
2. Create File blob stores nuget-hosted and nuget-cache under existing Nexus data storage. Replace verified-empty defaults as needed: hosted nuget-private on nuget-hosted, proxy nuget.org-proxy to official nuget.org V3 on nuget-cache, group nuget on nuget-cache with member order nuget-private then nuget.org-proxy. Remove obsolete empty nuget-hosted/nuget-group only as part of reviewed replacement scope; default blob store remains for unrelated formats.
3. Create one nx-nuget role with NuGet browse/read and add/edit restricted to nuget-private; no admin/delete. Create active user nuget with the compatible existing service credential. No separate read role. Do not assume group NUGET_TOKEN is the same as a login password: trace publishing before configuring API-key access. NuGetApiKey realm and nx-apikey-all are needed only if the existing publication path uses Nexus NuGet API keys; preserve current realms when enabling that reviewed extension. New instance API-key compatibility cannot be presumed.
4. Verify compatibility without nginx edits first. Retain working hostname upstream and existing static aliases for fast recovery. Both public static indexes currently direct clients to group nuget, so preserving that behavior serves reads but does not prove private hosted publication discovery. Check returned resources, HTTP/HTTPS behavior and package endpoints after repository initialization. If publication requires a corrected hosted index, prepare a narrowly reviewed nginx correction; do not perform blanket routing changes.
5. Test public NuGet index, versions, registration and actual .nupkg download for representative public dependency; verify JSON and ZIP content. Verify private exact package/version availability independently. Validate nuget Basic authentication with a feed GET and confirm the authenticated principal nuget in the Nexus request log; ordinary anonymous-readable feed200 alone does not prove password correctness. Perform authenticated writes only as a separately approved publication test with an agreed package/version.
6. Recover missing private packages from backup/artifact caches or reviewed source rebuilds with original versions; then run representative dotnet restore for both services in isolated local output/cache directories. NuGet configuration restoration alone does not reconstruct hosted contents. Check BaGet separately because the second project also depends on it. Record actual restore results; no claim of a full successful build until checked.

## Checks, risks and execution boundary

No repository edits, Nexus writes, nginx changes, CI retry or package publication performed. API steps require explicit execution authorization for the reviewed external action. No git commit/push authorized. Existing credential-bearing configs stay private; notes contain locations and variable names only. Outstanding actions live in ~/ai/TODO.md. Temporary anonymous read covers private content until disabled; current plans do not expand that existing role.

## Sources

Sonatype NuGet repositories: https://help.sonatype.com/en/nuget-repositories.html
Client configuration and API-key privilege/realm: https://help.sonatype.com/en/configure-nuget-with-nexus.html
