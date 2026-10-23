---
system: nexus
status: verified
checked: 2026-10-22
tags: [android, maven, cyberity]
---
# Cyberity SDK 1.31.2 publication assessment

## Task
Assess internal publication of the supplied AAR and whether the Android application requires changes.

## Context
Existing checkout `/home/slnnk/git/android-youdo4`; [Nexus map](../systems/nexus.md).

## Actions
Fetched `origin/develop` read-only; inspected commit `f6a32d9594ec0739acd2a276cf1508f23a7f4f41` without switching the clean `DevOps-833-fix-hotfix` checkout. Checked both Downloads archives and attempted an upstream POM GET with a five-second connection timeout.

## Findings
- `buildSrc/src/main/kotlin/Dependencies.kt:78` declares `ru.cyberity.cbr:cyberity-mobile-sdk:1.31.2`; `doc-validation-impl/build.gradle.kts:42` consumes it.
- Root `build.gradle.kts:3,35` and `buildSrc/build.gradle.kts:16` already use `https://nexus.youdo.com/repository/maven-public/`.
- `/home/slnnk/Downloads/cyberity-mobile-sdk-1.31.2.aar` and the `(1)` duplicate are identical: 5,089,814 bytes, SHA256 `9c0ef9dde01a1d30f195735814bc774d675425ea29d52dc8f84a86c1f76e5f68`. Both pass ZIP integrity checks; no POM/module descriptor or embedded libs directory was found.
- No local Gradle artifact cache entry for these coordinates was found. Direct upstream POM GET timed out; dependencies remain unknown.
- Application changes should be unnecessary if the AAR and correct dependency POM are published under the existing coordinates to `maven-releases`, already a member of the configured public group. Current Nexus membership was taken from the existing verified map, not refreshed this session. An empty generated POM cannot establish dependency compatibility.
- Primary reference: [Android library publication](https://developer.android.com/build/publish-library/upload-library) explains that AAR dependency metadata is supplied separately through a POM. [Vendor installation](https://developers.cyberity.ru/android-sdk/android-sdk/) confirms the same coordinates.

## Android runner cache check (2026-10-22)
Read-only SSH to the dedicated application runner `172.28.0.175` confirmed Docker executor, `disable_cache = false`, and mounts `/data/cache:/cache` and `/data/daemon.json:/etc/docker/daemon.json:ro`. `/data/cache` is empty, `/root/.gradle` and `/home/gradle/.gradle` do not exist, `docker volume ls` returns no volumes, and `docker ps -aq` returns no retained containers. The inspected Android `origin/develop` CI has no cache declaration or Gradle home persistence. No recoverable Cyberity POM was found on this runner; this does not establish cache contents on other runners or developer machines.

## Developer cache result and AAR dependency assessment (2026-10-22)
User reports the developer found only the AAR, no POM. A local constant-pool class-reference scan of `classes.jar` confirms external references to AndroidX CameraX core/video/view/lifecycle, ML Kit, Picasso, Markwon, Kotlin serialization/coroutines, OkHttp/logging and Retrofit, among others. Only Cyberity namespaces are implemented by classes in this JAR. This proves the supplied SDK is not self-contained; an empty dependency POM is not an established replacement. Exact Maven artifact versions cannot be recovered reliably from these class references. A generated POM is viable if its dependency declarations can be recovered from vendor publication/build metadata or reconstructed and validated against an application release build and SDK flow. No build or publication was performed.

## AAR-only publication applied (2026-10-22)
User explicitly requested publication of only the AAR followed by a build check, superseding dependency metadata as a publication prerequisite. Prepared helper `/home/slnnk/ai-data/nexus-recovery/cyberity-1.31.2/publish_aar.py`; fresh preflight confirmed hosted RELEASE repository online, public group membership, and absent AAR/POM/module. After describing the exact single-file upload, the approved escalated command performed one PUT to `http://msk3-nexus.youdo.corp/repository/maven-releases/ru/cyberity/cbr/cyberity-mobile-sdk/1.31.2/cyberity-mobile-sdk-1.31.2.aar`, HTTP201. No POM was generated or uploaded.

Initial post-upload search check did not match because Nexus asset paths include a leading slash; a checksum sidecar GET also returned404. No upload was repeated. Final read-only helper `verify_aar.py` normalizes the asset path and passed: hosted/public-group HEAD200, length5089814, assets API SHA256 identical to the supplied AAR, hosted POM HEAD404. Public consumer URL: `https://nexus.youdo.com/repository/maven-public/ru/cyberity/cbr/cyberity-mobile-sdk/1.31.2/cyberity-mobile-sdk-1.31.2.aar`. Group verification used the internal Nexus endpoint; public hostname was not rechecked.

## Reconstructed POM draft (2026-10-22)
User supplied 32 dependency rows from MVNRepository. Prepared local `/home/slnnk/ai-data/nexus-recovery/cyberity-1.31.2/cyberity-mobile-sdk-1.31.2.pom` with packaging AAR and original left-column versions, excluding available updates. XML parsing, coordinates and 32 unique dependencies checked. The pasted list omits its section heading/scopes; all scopes are provisional compile, marked by a POM comment. This is a reconstruction, not an original vendor POM; optional flags/exclusions and completeness are unverified. No POM upload or build was performed. Follow-up screenshot `/tmp/codex-clipboard-lyUA18.png` confirms `Compile Dependencies (0)` and `Runtime Dependencies (32)`. Updated all 32 scopes to runtime and removed the provisional-scope comment; XML, coordinates, packaging and scope-count checks passed. Original-version completeness, exclusions and optional flags remain limited to the supplied page evidence. Existing central build/dependency-validation action remains open; At that draft stage POM publication had not yet been requested; the later approved upload below supersedes this.

## Reconstructed POM publication applied (2026-10-22)
User explicitly confirmed publication of the prepared POM next to the AAR. Helper `/home/slnnk/ai-data/nexus-recovery/cyberity-1.31.2/publish_pom.py --publish` verified coordinates/packaging, 32 unique runtime dependencies, group membership, absent hosted POM and existing AAR before one PUT. Nexus returned201. Hosted and public-group POM GET both returned200 and identical SHA256 `221ee83a31f5d83e6e4a8a20644267180707e72c639289658520604944392eeb`. Assets API independently confirmed POM SHA256 and the original AAR SHA256 unchanged. Helper exited0. This POM is reconstructed from user-provided MVNRepository evidence, not downloaded from the vendor. No dependency resolution, build or runtime check performed.

## Android build 3243556: subsequent Fotoapparat blocker (2026-10-22)
Read-only GitLab inspection: [job3243556](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/jobs/3243556), feature/staging, pipeline141325, MR2913 SHA `e0a32918adb5986a72a9e9ea5498e60f8e4b527d`, runner116. Ran11:25:54-11:33:45MSK; failed `script_failure` after7m29s and4842tasks. Final failure is `:youdoapp:checkBetaDuplicateClasses` resolving `:youdoapp:betaRuntimeClasspath`: missing `io.fotoapparat:fotoapparat:2.7.0` JAR at Nexus Maven public path. This is artifact resolution, not an actual duplicate-class finding. No Cyberity failure is reported; doc-validation metadata/manifest tasks ran, but neither application build nor SDK runtime is validated.

Nexus returns a992-byte POM with no packaging and three AAR dependencies under group `io.fotoapparat.fotoapparat`: adapter-rxjava, adapter-rxjava2, fotoapparat, all2.7.0. JitPack returns the same dependency structure and no main JAR (404); Maven Central POM/JAR/AAR all404. SciJava tested public POM/JAR404. Existing checkout independently uses `LibraryVersions.fotoapparat` in camera-impl; local reference is corroborating context, not exact failed-SHA inspection.

Found main JAR at `https://maven.moxtra.com/nexus/content/groups/public/io/fotoapparat/fotoapparat/2.7.0/fotoapparat-2.7.0.jar`. Downloaded locally into `/home/slnnk/ai-data/nexus-recovery/fotoapparat-2.7.0/`:286bytes, valid ZIP containing only `META-INF/MANIFEST.MF`, SHA1 `dfbfbf7d90d51f6fed5975338cd39290fa1d578f` matches mirror checksum, SHA256 `c02d1c2ccf4d1d6720017cbd918af1226a61a7694099cec9c55f43821e996c03`. Mirror POM byte-identical to current Nexus POM. This is an aggregator/empty JAR paired with dependency-bearing POM, not the camera implementation. Prepared local restoration candidate only; no upload, CI retry or project edit. Restoring this JAR can address the observed missing asset, but does not establish availability of every subsequent dependency.

## Moxtra Maven proxy applied (2026-10-22)
User explicitly requested creation of the proposed Moxtra proxy instead of manual Fotoapparat upload. Local plan and helper: `/home/slnnk/ai-data/nexus-recovery/moxtra-proxy/plan.json`, `manage_proxy.py`. Fresh GET preflight confirmed no `maven-moxtra`; cloned existing `maven-jitpack` proxy settings without authentication, changed only name and remote URL to `https://maven.moxtra.com/nexus/content/groups/public/`; existing blob store `maven-cache`, MIXED version policy, PERMISSIVE layout. Nexus-host SSH HEAD to upstream JAR returned200/286bytes.

Described and obtained escalated approval for each external action: proxy POST returned201 and config GET matched; group PUT returned204 and exact membership GET matched. `maven-moxtra` appended as ninth/last public-group member; all eight prior members preserved in order. No routing rules, roles, existing upstreams or application settings changed. No manual Fotoapparat artifact publication and no CI retry.

Verification: direct proxy and public group JAR/POM HTTP200. First metadata check found no JAR asset after HEAD-only probing; actual286-byte JAR GET then populated cache. JAR SHA256 and cached assets metadata match reviewed mirror checksum `c02d1c2ccf4d1d6720017cbd918af1226a61a7694099cec9c55f43821e996c03`; both POM reads match reviewed metadata. Final consumer URL `https://nexus.youdo.com/repository/maven-public/io/fotoapparat/fotoapparat/2.7.0/fotoapparat-2.7.0.jar` HEAD returned200/286bytes; verification helper exited0. Earlier proposal to upload the mirror JAR is superseded by the proxy implementation. Build/SDK validation remains open.

## Fotoapparat Central publication clarification (2026-10-22)
Primary project [issue413](https://github.com/RedApparat/Fotoapparat/issues/413) records the JCenter migration problem. Maintainer dmitry-zaitsev said on2021-12-10 that migration off JCenter was planned; the issue does not establish completed Central publication. A2022-03-13 report states2.7.0 cannot resolve using only Google and Central. Current direct Maven Central POM/JAR/AAR404 checks above support absence of these exact coordinates today, without claiming that no historical publication ever occurred or that every Fotoapparat coordinate is absent. A Maven-formatted repository and the MVNRepository catalog are distinct from Maven Central; public repository presence does not imply Central publication. No configuration change or new action follows from this explanation.

## Current JCenter availability checked (2026-10-22)
Direct streamed GET/header checks for Fotoapparat2.7.0 POM/AAR/JAR at `https://jcenter.bintray.com/io/fotoapparat/fotoapparat/2.7.0/` each return301 to the same path at `https://repo1.maven.org/maven2/`, followed by404. No files downloaded. [JFrog shutdown notice](https://jfrog.com/blog/jcenter-sunset/) states final redirect on2024-08-15 and explicitly notes that some JCenter-only packages are absent from Central. JCenter proxying therefore cannot recover this version today. Existing Moxtra proxy remains the verified available workaround; no configuration change or new backlog action.

## Fotoapparat maintenance assessment (2026-10-22)
Upstream [releases](https://github.com/RedApparat/Fotoapparat/releases) still lists2.7.0 as latest; [master history](https://github.com/RedApparat/Fotoapparat/commits/master/) lists the latest commits on2021-12-10 and release2.7.0 on2019-03-02. Together with unresolved JCenter migration issue413, this supports an assessment of effectively inactive maintenance, not an official abandonment declaration. Web-rendered history was available; direct GitHub API retrieval was unavailable through the browser tool. Proxy recovery restores download availability; it does not establish ongoing upstream compatibility fixes. No migration work requested or performed.

## Additional Fotoapparat hosted publication applied (2026-10-22)
User explicitly requested publishing Fotoapparat additionally in Nexus analogously to Cyberity, after proxy recovery. Described that the main JAR is an aggregator and publication includes its three mandatory implementation modules. Prepared `/home/slnnk/ai-data/nexus-recovery/fotoapparat-2.7.0/hosted-plan.json` using unmodified Moxtra files; all source SHA1 sidecars, POM coordinates and ZIP integrity checks passed. Eight target assets were absent from `maven-releases`, which remains the first `maven-public` member.

Reviewed/escalated publication command `publish_hosted.py --publish` uploaded eight files, each PUT201: main `io.fotoapparat:fotoapparat:2.7.0` JAR286bytes/POM992bytes and `io.fotoapparat.fotoapparat` modules `fotoapparat` AAR314784bytes/POM2543bytes, `adapter-rxjava` AAR11889bytes/POM1779bytes, `adapter-rxjava2` AAR16084bytes/POM1789bytes. All POMs retained exactly, including original types, scopes and external dependencies. Standard AndroidX/Kotlin/test dependencies were not republished.

Initial verification stopped because a HEAD response omitted optional Content-Length; no upload retry. Corrected verifier to permit absent length and ran `publish_hosted.py --verify-only`: all eight hosted asset SHA256 values match local plan, hosted/group HEAD200 for all assets, public HTTPS main JAR and POM HEAD200, exit0. No binary downloads used for post-publication verification. Receipt and source files remain in the same ai-data directory. Moxtra proxy retained as additionally requested; no repository/project edits or CI retry. This later explicit publication supersedes the earlier decision to use only the proxy as the recovery mechanism.

## Moxtra source identity (2026-10-22)
Moxtra renamed itself Moxo on2022-03-07, per its [company-issued announcement](https://www.prnewswire.com/news-releases/moxtra-rebrands-as-moxo-releases-2022-digital-resilience-report-uncovering-opportunities-to-automate-and-streamline-high-value-client-interaction-processes-301496786.html). It develops client collaboration/workflow automation software; see [official company page](https://www.moxo.com/company). Its [official GitHub organization](https://github.com/Moxtra) links moxo.com and references the maven.moxtra.com infrastructure in SDK distribution repository descriptions. Moxtra is a third-party retained artifact source in this recovery, not the upstream Fotoapparat project. The required eight Fotoapparat files are now separately hosted in our releases repository; this identity research grants no configuration changes or further action.

## Changes
Cyberity AAR/reconstructed POM and eight Fotoapparat2.7.0 files uploaded to Nexus releases. Created maven-moxtra proxy and appended it to maven-public after explicit approval. No Android application/Git changes, build or CI retry.

## Status and risks
2026-10-22: AAR and user-reviewed reconstructed POM publication complete, hosted/group availability and checksums verified. Earlier AAR-only/POM-absent status is historical and superseded. Android build3243556 failed on a separate missing Fotoapparat2.7.0 JAR, subsequently made available through the approved Moxtra proxy and additionally published with its three AAR modules and unchanged POMs to hosted releases; SDK runtime validation and subsequent build remain open in the Nexus section of [central TODO](../../../../TODO.md). Vendor POM exclusions/optional flags and full dependency resolution remain unverified. Upstream timeout persists; both local assets are now available through the public Maven group.

## Portable lesson
none
