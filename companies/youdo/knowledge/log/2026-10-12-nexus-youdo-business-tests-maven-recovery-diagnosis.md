---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, maven, gitlab-ci, b2b]
---
# Business autotest Maven recovery dependency cycle

## Summary

Maven snapshot recovery completed through a dependency-closed temporary bootstrap, full artifact replacement and one bounded final validation pass. All three master pipelines are green; final main builds/publications and separately approved `autotests:latest` updates succeeded. Hosted/public Maven metadata agrees, and each latest registry tag matches its freshly built pipeline tag digest. Source dependency cycles remain unchanged. Original `verify-modules` diagnosis: compilation/build checks without tests or artifact publication.

## Task and context

The user is restoring Maven libraries and reported [job3219500](https://gitlab.youdo.sg/youdo/Test/youdo-business-tests/-/jobs/3219500), also asking what the retried verify job does. Fresh Nexus configuration and temporary anonymous reads are already restored; this diagnosis concerns missing private snapshots.

## Actions and key commands

Authenticated GET requests read GitLab project/job/pipeline metadata, job traces and CI/source files. Credential values were kept in memory and omitted from notes. API routes: `GET /api/v4/projects/480/jobs/3219500`, job trace endpoints and repository-file GETs.

## Findings

- Project480 `build` job3219500 belongs to pipeline137904, MR!262, ref `refs/merge-requests/262/head`, commit `ab6813a3` from September3 (`monorepo-api-ui-tests`). It fails resolving `b2b:youdo-business-tkb-tests:1.0.0-SNAPSHOT` and `b2b:youdo-business-sber-proxy-tests:1.0-SNAPSHOT`.
- `verify-modules` job3219502 fails on the same dependencies. Its command is `gradle clean build compileTestJava compileTestKotlin --refresh-dependencies -x test --console=plain`. It checks API/UI module compilation/build while excluding tests; it does not publish Maven artifacts.
- `publish-maven` runs only on `master`. Master pipeline137380 at `0da09367` has historical successful jobs `publish-maven`3092181, `build`3092180 and `update latests`3092182 from August27, not October12. Master also has implementation dependencies on TKB/Sber; switching the pipeline alone does not remove the recovery block.
- TKB project536 build3219485/pipeline139740 and Sber project578 build3219490/pipeline133551 both fail resolving `b2b:youdo-business-tests:1.0.0-SNAPSHOT`. Together with the main suite failures, this verifies a circular build bootstrap dependency among private artifacts.

## Master retry evidence (2026-10-12)

The user supplied master pipeline137380. Its latest `publish-maven` retry3219549 failed at17:49:09 MSK and `build` retry3219548 failed at17:49:43 MSK on October12. Publication failed at its first command `gradle :jar`, in `compileKotlin`, resolving the same `b2b:youdo-business-tkb-tests:1.0.0-SNAPSHOT` and `b2b:youdo-business-sber-proxy-tests:1.0-SNAPSHOT`; it never reached upload. Historical successful jobs3092180/3092181/3092182 date to August27.

The user reports having rebuilt TKB/Sber. A fresh GET check verified their latest build jobs: TKB project536 job3219485 failed on October12 at17:25:12 MSK; Sber project578 job3219490 failed at17:30:38 MSK. Both fail resolving `b2b:youdo-business-tests:1.0.0-SNAPSHOT`. Neither project has a publication job from today: latest TKB `publish-maven`3190165 succeeded September29 at01:12:31 MSK; latest Sber `publish-maven`2949545 succeeded June6 at23:22:50 MSK.

GET checks of version-level `maven-metadata.xml` for TKB `1.0.0-SNAPSHOT` and Sber `1.0-SNAPSHOT` through both `maven-public` and `maven-snapshots` returned404 in all four cases. No packages were downloaded. The current missing snapshots and source dependency cycle are verified; recovery outcome remains open. No retry was authorized or performed.

## Dependency introduction history (verified 2026-10-12)

Read-only GitLab GETs inspected all master `build.gradle.kts` commit histories and diffs for the relevant dependency additions: project480 had56 commits, project536 had9, project578 had8. Each of the four additions includes both `implementation` and `testImplementation`.

| Dependency edge | First addition | Date (MSK) | Merge evidence |
| --- | --- | --- | --- |
| TKB536 → main suite480 | `a3f6388384ed0f1fd30df7984da1606baef721a6` (initial commit) | 2024-07-12 14:45:25 | No associated MR found |
| Main suite480 → TKB536 | `8f723d1b21bd6129b792ca5129b2d3e8c58aeffe` | 2024-09-30 12:26:56 | MR!193 targeted master; merged12:26:56.997 |
| Sber578 → main suite480 | `6db235fffa688269305535b3f94b68a1bd1e8f89` (initial commit) | 2026-02-09 14:11 | No associated MR found |
| Main suite480 → Sber578 | `0f1959a265d9cb15dd0faaf1b83ceb7a5555649b` | 2026-02-12 21:38:02 | MR!238 targeted master; merged21:38:03.585 |

The TKB cycle was established on2024-09-30 and the Sber cycle on2026-02-12. These changes predate the current Nexus recovery and DevOps-832 work. It is an inference that pre-existing published artifacts masked a fresh-repository bootstrap problem; this history does not independently prove that explanation. No repository edits or external changes were performed.

## Static recovery proposal (not executed)

The immediate pre-TKB-dependency main-suite candidate `f15c4d4b0f8a4c71cc893658735fd1520949fe71` (2024-09-24) is incompatible with inspected current TKB/Sber main sources: its `DataProvider` lives under `api.data.providers`, while consumers import `api.data.factory.DataProvider`; Sber additionally requires `api.data.factory.DataGenerator`. The old candidate also retains Tochka/Billing dependencies.

A static audit identifies11 current main-suite Java sources whose internal dependency closure does not import TKB/Sber/Tochka/Billing:

- `api.data.factory.DataProvider` and `DataGenerator`.
- `api.data.utils.DateUtil`.
- `api.data.factory.legalDataProvider.LegalDataProvider`, `InnIndividualProvider`, `ULDataProvider`.
- `api.data.enums.Account`, `Card`, `Sbp`.
- `api.data.enums.entity.PaymentType`.
- `api.data.contracts.ContractParam`.

External requirements include Javafaker, Datafaker, Apache Commons Lang3 and Lombok annotation processing; Java17 supports the switch expressions used. Exact source revision and dependencies must be pinned and compilation validated before publication. The reduced jar would use the normal `b2b:youdo-business-tests:1.0.0-SNAPSHOT` coordinate temporarily; it is incomplete for ordinary suite/test consumers.

Proposed recovery sequence:

1. Compile the dependency-closed current common sources into a bootstrap jar and explicitly publish it under the normal main-suite coordinate.
2. Run TKB/Sber CI `publish-maven` only. Inspected jobs run `gradle :jar` followed by `:publishMavenPublicationToNexusRepository`; no custom jar dependency on test compilation was found.
3. Publish the full current main-suite artifact, immediately replacing the incomplete bootstrap.
4. Run full TKB/Sber build and publication against the full current main-suite artifact.
5. Run final full main-suite build and publication.

The initial TKB/Sber build jobs compile test sources and can require additional main-suite APIs omitted by the bootstrap; the initial stage therefore proposes publication only. Static closure compatibility does not prove a successful compile or full dependency resolution. Upstream plugin/lib and public dependencies still must resolve. This is an untested recovery proposal: no bootstrap compilation/publication was performed, no repository changes approved, and no external changes authorized or performed.

## Local bootstrap preparation and compatibility validation (2026-10-12)

The user gave the instruction `Сделай` after the recovery proposal. This authorized the local preparation; the explicit rule requiring approval for external state changes still applies. No repository mutation or external publication/retry was performed. External publication approval is pending.

Prepared isolated artifacts and source snapshots under `/home/slnnk/ai-data/nexus-recovery/maven-bootstrap-20261012/`; source repositories were not switched or edited. Bootstrap sources are pinned to main-suite `0da09367`. Gradle8.7/JDK17 compiled11 Java sources into13 class files, producing an18,007-byte jar with SHA256 `301a86940a14c425143735d6195a1b323d025f670ce9258368dce6f81528721f`.

Local Maven publication metadata and POM were verified for normal coordinate `b2b:youdo-business-tests:1.0.0-SNAPSHOT`; timestamped artifact version is `1.0.0-20261012.151039-1`. A local Gradle init script exclusively resolves the bootstrap module from the isolated local Maven tree and prohibits test/precondition/report/publication tasks in the validation graph. Both main-only validations passed against that bootstrap:

- TKB `71ead24d90c172fecc9c23d9fbf1f492bfb643a7`: `:jar`, BUILD SUCCESSFUL in2m50s,74 class files.
- Sber `caab39732012784a1e760036aa48a61d19bc0a81`: `:jar`, BUILD SUCCESSFUL in1m31s,73 class files.

Evidence: `bootstrap-verification.json` records provenance, checksums and passed validation results. The prepared `publish_bootstrap.py` default dry run verified the checksums. It retrieves existing GitLab group34 Maven credentials into memory and does not print credential values. Pending approval, the concrete publication command is:

```bash
python3 /home/slnnk/ai-data/nexus-recovery/maven-bootstrap-20261012/publish_bootstrap.py --publish
```

That command would publish the normal main-suite snapshot into Nexus `maven-snapshots`; it has not been run. The partial artifact is for recovery only: first TKB/Sber CI actions must publish main jars, rather than run full build/tests against the incomplete main-suite API. Full main-suite publication and subsequent full build/publication checks remain pending, each subject to applicable external approval. Earlier proposal-only wording describes the state before these successful local validations.

## Approved bootstrap Nexus publication (2026-10-12)

The user explicitly answered yes to the reviewed bootstrap Nexus publication. Root ran the prepared `publish_bootstrap.py --publish`; Gradle reported BUILD SUCCESSFUL in8s. GET metadata checks through both `maven-snapshots` and `maven-public` confirm main-suite timestamped snapshot `1.0.0-20261012.151934-1`, with `lastUpdated=20261012151934`. Checks read metadata only; no package downloads were performed.

The incomplete main-suite bootstrap is now live and is a recovery artifact, not a complete replacement for the normal suite API. Full-artifact replacement and recovery completion remain pending. This publication approval did not authorize CI retries.

TKB remote master is `6ae621aa48f8325de0eb43913cedfe8e4eb88398`; GitLab comparison against validated local `71ead24d90c172fecc9c23d9fbf1f492bfb643a7` returned `straight:true`, `compare_timeout:false`, `diffs:[]`, verifying identical trees. Proposed TKB publication target is job3190165, pipeline139740 at6ae621a; proposed Sber publication target is job2949545, pipeline133551 atcaab397. Neither CI retry has been authorized or performed. A separate approval question for TKB publication is pending under the external-actions rule; Sber and later recovery stages also require their applicable approvals. The recovery TODO remains open. Earlier pending-publication statements describe the prior state and are superseded by this approved bootstrap publication.

## Approved first TKB/Sber publications and full-suite retry (2026-10-12)

The user separately approved retrying TKB publication3190165, creating job3219856 on master6ae621a/pipeline139740, and explicitly approved restarting Sber publication2949545, creating job3219857 on mastercaab397/pipeline133551. Both requests targeted `publish-maven` only; no build or `update latests` actions were requested.

TKB3219856 succeeded at18:27:19 MSK and Sber3219857 succeeded at18:28:10 MSK. GET Maven metadata through both hosted `maven-snapshots` and group `maven-public` verified TKB `1.0.0-20261012.152716-1` and Sber `1.0-20261012.152806-1`.

The user separately approved publishing the full main suite conditional on both publications succeeding. Once that condition was verified, root retried main-suite publication3219549; POST returned job3219858, pending, on master0da09367/pipeline137380. Full-suite publication outcome is still pending; until it succeeds, the incomplete bootstrap remains the live main-suite artifact. The recovery TODO remains open.

A repeat TKB publication approval question is pending; repeat Sber publication and later build actions are not yet authorized. These outcomes supersede the earlier first-phase pending-retry statements. Main-suite publication approval does not cover additional retries or image-tag updates.

## Full artifact restored; bounded final validation pass (2026-10-12)

Main-suite publication3219858 succeeded at18:34:20 MSK: main compilation completed in4m44s and publication in1s. Hosted/group GET metadata confirms full main-suite snapshot `1.0.0-20261012.153418-2`. The temporary incomplete bootstrap is no longer the latest snapshot. Overall recovery validation remains open until the final jobs finish.

The user separately approved repeat TKB publication and repeat Sber publication conditional on full-suite publication succeeding, and individually approved TKB/Sber/main-suite build retries with Docker pipeline-tag overwrite effects described. The user also separately approved final main-suite publication conditional on the second TKB/Sber publications succeeding. These are explicit per-action approvals, not permission for indefinite retries.

Following verified full-suite publication, each approved phase2 action was executed once: TKB second publication3219859, Sber second publication3219860, TKB build3219861 and Sber build3219862; all were running around18:35 MSK. The separately approved final main-suite build (source3219548) and final publication (source3219858) have not yet been performed; their prerequisite is successful second TKB/Sber publications.

The user asked whether the process was looping. Root clarified this is one bounded final validation pass; status polling is read-only and does not retry jobs. No additional retry beyond the reviewed actions is authorized. Earlier statements that bootstrap remains the latest artifact are superseded by the verified full replacement. The overall recovery TODO stays open until final validation outcomes are known.

## Changed files

This log, the current Nexus system map, `~/ai/TODO.md`, generated KB indexes and `.sync-notes` only.

## Risks and limits

Historical success does not establish that artifacts exist after Nexus recovery. A reviewed bootstrap recovery plan is required before publication or CI retries; no such external actions were performed during this diagnosis. The dependency cycle is verified; a particular source recovery/bootstrap method has not yet been validated.

## Additional recovery context reported by the user

On 2026-10-12 the user reported rebuilding some Maven libraries under `https://gitlab.youdo.sg/youdo/Test` and also `https://gitlab.youdo.sg/team-youdo-testers/autotest-core`. This is user-reported recovery activity; the exact libraries, job outcomes, and resulting Nexus publications were not independently verified in this check. The message was informational and did not authorize additional retries or external changes.

## Reusable lesson

Publishable generic procedure: [Recover mutually dependent Maven snapshots](../../../../general/knowledge/maven/circular-snapshot-bootstrap-recovery.md). It describes verified bootstrap/main-jar/publication phases and does not claim the still-pending final full builds have completed.

## Final approved actions and verified completion (2026-10-12)

Second TKB publication3219859 succeeded at18:37:40 MSK and second Sber publication3219860 at18:36:25 MSK. Their metadata was checked before the conditionally approved final main-suite actions: publication3219863 and build3219864. Main-suite publication succeeded at18:43:10 MSK and build at18:47:45 MSK; TKB build3219861 succeeded at18:41:06 MSK; Sber build3219862 at18:38:16 MSK.

The user explicitly requested restarting latest updates, authorizing all three aliases. TKB `update latests`3219865 and Sber3219866 succeeded at18:46:47 MSK; main-suite3219867 succeeded at18:50:27 MSK after its build. These approvals covered registry alias changes, not deployment or test execution.

`final_readonly_check.py` passed. Evidence `/home/slnnk/ai-data/nexus-recovery/maven-bootstrap-20261012/final-verification.json`, checked2026-10-12T15:52:11Z, verifies:

| Project | Green pipeline | Final publication | Final build | Latest update | Current Maven snapshot | Registry source tag |
| --- | --- | --- | --- | --- | --- | --- |
| business | 137380 | 3219863 | 3219864 | 3219867 | `1.0.0-20261012.154307-3` | `master-2686` |
| tkb | 139740 | 3219859 | 3219861 | 3219865 | `1.0.0-20261012.153739-2` | `master-98` |
| sber | 133551 | 3219860 | 3219862 | 3219866 | `1.0-20261012.153623-2` | `master-18` |

Hosted `maven-snapshots` and group `maven-public` metadata are consistent for all three. Registry tag metadata confirms each `latest` digest equals the source pipeline tag digest:

- business: `sha256:e63c0acff99768544c1b2d3bf4015ba8dde0eeb613f04c986e353df79b45fc79`.
- tkb: `sha256:c405610b0af163e5d2b068724cc6626c1b53d06de12dfc1744dec904148e66e4`.
- sber: `sha256:92ebc813f07e27196d26a71b56ea6346a0842389df94453296a534207a4ee39e`.

Verification used GitLab GETs, Maven metadata and registry tag metadata only; no package/image downloads. Builds exclude test execution; no deployment was performed. The source dependency cycles were not changed, and no architecture fix was requested. Matching bootstrap recovery TODO is closed; no further retries are planned. All earlier pending-state statements record chronology and are superseded by these verified results.
