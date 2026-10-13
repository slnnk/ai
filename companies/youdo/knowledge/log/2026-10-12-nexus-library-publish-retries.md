---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nuget, recovery, gitlab]
---
# Coworking and RabbitHole publication retries

## Summary

User chose retry-first recovery: run library publish jobs and investigate actual failures instead of checking all dependencies beforehand. Coworking three retries failed; dependency RabbitHole1.4.2 was then restored after an explicitly approved NuGet role assignment for gitlab. RabbitHole1.4.1/1.4.2/1.4.3 and Coworking1.0.7/1.3.3/1.3.4 are now present in Nexus; later sections record completed recovery and separate approvals.

## Authorization and context

User asked starting Coworking, then explicitly directed publication job retries before dependency analysis, and then selected RabbitHole. Separate async approval explicitly authorized adding nx-nuget to Nexus user gitlab while retaining nx-docker. No Git changes, new tag creation, service deployment or API-key/CI variable changes authorized or performed.

## Coworking actions and findings

Read-only audit mapped1.0.7 tag4eb06b35/pipeline26424/original job2458975 (prior126552 success);1.3.3 tag947a3c6f/pipeline61265/job144466;1.3.4 tag62ddfa3f/pipeline118511/job2323508. Version comes from CI tag; publish builds/restores/packs itself, no prior artifacts needed.

Ran retry_coworking.py --retry for all three after user direction. New jobs3218616/3218617 fail runner_system_failure: microsoft/dotnet:2.1-sdk manifest unknown. Independent DockerHub manifest GET404 MANIFEST_UNKNOWN verified. New1.3.4 job3218618 fails NU1101 RabbitHole package absent; matching source snapshot requires1.4.2. Coworking1.3.3 source requiresRabbitHole1.4.1;1.0.7 RabbitLink.Serialization.Json0.5.1 is confirmed public.

Historical Coworking1.0.7/1.3.3 CI reads NUGET_SOURCE/NUGET_TOKEN; group youdo/Lib sets sourceBaGet, overriding parent Nexus source. Their committed config also uses BaGet. Current Coworking1.3.4 shared publish template uses SDK6 registry image and Basic auth gitlab via existing NEXUS_DOCKER_USER/PASSWORD. Existing nuget user is not the publishing identity used by that template.

## RabbitHole actions and findings

Required versions1.4.1/1.4.2/1.4.3.1.4.2 current tag8c430ed8 pipeline118506/original2323503; old pipeline61365 refers to another historical tag SHA, not selected. Retry3218619 reached publish and failed403 Nexus private. User explicitly approved gitlab role addition. Ran allow_gitlab_nuget.py --apply: PUT succeeded, initial verification mistakenly compared role list order; fixed to compare sets and independent GET confirmed roles nx-docker+nx-nuget. Existing user/password and role definitions preserved; no admin/delete granted.

Retried failed1.4.2 publish ->3218670 success. Public Nexus group lists1.4.2; downloaded rabbithole.1.4.2.nupkg HTTP200,78097bytes, ZIP CRC/nuspec id/version verified. No failures claimed for transient download warning lines recovered within successful job.

1.4.1 historical pipeline60073/job135065 uses SDK3.1 and BaGet/API-key publication. Retry3218622 still running at checkpoint.1.4.3 old pipeline118505/job2323502 canceled has sameSHA as current1.4.2; tag1.4.3 GET404 but historical job tag=true. Retry3218623 reaches compile, then MSB4044 GetAssemblyVersion missing NuGetVersion. Missing current tag is a possible cause of empty CI tag-derived version, pending detailed verification. No tag recreated or CI variable overridden yet.

## Changed files, risks and evidence

GitLab publish retries and approved Nexus user role assignment only; no repository file edits. Local ai-data/nexus-recovery helpers/results contain sanitized metadata, no credential values/raw secret-bearing traces. Coworking retry IDs and RabbitHole status JSON preserve URLs/results. Need protect restoration version identity when recovering historical jobs. Existing temporary anonymous remains enabled; separate disable TODO retained. Active Nexus realms unchanged (NuGetApiKey not enabled).

## RabbitHole completed after explicit approvals

User approved a one-off pipeline creation for1.4.3: ref1.4.2 with CI_COMMIT_TAG=1.4.3, after verifying SHA8c430ed8f1bd3700e0743dc68c6ae8834b2e58f5 equals the historical1.4.3 source. Pipeline140646/job3218762 succeeded. No Git refs or project files changed.1.4.3 package78109bytes was initially downloaded/ZIP/nuspec verified before the later metadata-only preference.

Old1.4.1 job3218622 stalled on restore for more than10minutes with BaGet configured. Prepared local source from exact tag1.4.1 SHAfea9c0e73d225cf03f89ccf49ba4cae37b226c0d. Temporary source uses only selectedsrc/buildprops/license/readme files and a public-source NuGet.Config; repository untouched. Built on locally cached SDK6.0-jammy instead of historicalSDK3.1, targetnetstandard2.0. Package78144bytes SHA2568657b0b6e76a4ea9db7c8fd2fc37426cd475d1e626de983dc0ba8d2ddf1b83ef; ZIP/nuspec/version/direct dependencies verified. Initial local run used the wrong UID and failed first-use NuGet data-directory permission; corrected to1001:1001 and temporary XDG directories, then build succeeded.

User separately approved publishing this reviewed local1.4.1 rebuild and canceling3218622. Canceled job with API and GET-confirmedcanceled. Published main nupkg with Basic usernuget via environment-only credentials in an ephemeral local container; no API key or credential config written. PUTCreated, public download digest initially confirmed. NuGet API-key realm is not required for this observed Basic publication path.

## User speed preferences and Coworking completion

User requested avoiding package downloads: after publication, check only version appearance in Nexus metadata. Applied immediately to subsequent Coworking verification and canonical Nexus/context guidance. Existing local build artifact ZIP/nuspec validation remains appropriate before explicit upload approval. No full restore/build of consumers performed.

After RabbitHole restored, retried Coworking1.3.4 failed job3218618 ->3218902success; metadata lists1.3.4. Historical1.0.7/1.3.3 CI remained blocked by unavailableSDK2.1 image. Prepared local packages from exact source tags:1.0.7SHA4eb06b35ab2177a4a195d1f50b13e3121c431ee6,1.3.3SHA947a3c6f8cd49677bf2559de248de1017f1d464e; SDK6.0-jammy,targetnetstandard2.0. Both builds/ZIP/nuspec checks succeeded.1.0.7 package12545bytes SHA256ffd4381eca80c2e0a2c51d479b7e49a46f36df101725f5c0456fa2ac5b5a4fb8;1.3.3 package14071bytes SHA25672abbc66a8f40d75fa52d73f52217646590e9ee8847e33b9fe90c2a365fce769. Dependencies match original source declarations, includingRabbitLink.Serialization.Json0.5.1 andRabbitHole1.4.1 respectively. These are source rebuilds, not claims of original binary identity.

User explicitly approved publishing both reviewed Coworking packages. Uploaded main nupkgs with Basic usernuget; both PUTCreated and public version metadata200/present. No package download after the metadata-only instruction. Repository files/branches/tags unchanged; no service deployments or CI source/API-key variables changed.

## Recovery status

RabbitHole1.4.1,1.4.2,1.4.3 restored; Coworking1.0.7,1.3.3,1.3.4 restored. Original inventory52IDs143pairs is a historical snapshot; current pending list50IDs137pairs after these six restores. CSV rows annotated restored rather than discarding required-version evidence. Old CI recovery adjustments remain separate work if requested; no optional CI refactor performed.
