---
system: nexus
status: verified
checked: 2026-10-14
tags: [nexus, pypi, python, gitlab, nomad, recovery]
---
# PyPI exact-version library batch recovery and Nomad cron image inventory

## Summary

All32required canonical PyPI versions are published and Nexus component checksums verified. Five modern versions have exact locked wheel/sdist bytes; eleven older Poetry versions have exact wheels only; ten requirements-only setuptools releases were rebuilt from exact source without historical-byte proof. The final six rebuilt versions required reviewed replacement hashes, now included in all five explicitly approved/merged consumer MRs. All five post-merge master pipelines succeeded; the earlier cgroup failures and timeout attempts are historical checkpoints superseded by approved Docker29.9.0 corrections/retries and successful CI. Daily pipelines are build-only with no automated test job. No remaining package/build/MR completion blocker is recorded for this audited scope.

Nomad read-only inventory covers160jobs,23periodic parent jobs and eight unique runtime image references. Final GET-only registry verification at2026-10-13T20:18:27Z confirms all8manifests available for the23original periodic jobs. Seven current configs match the images published during this recovery; cashflow:master was subsequently replaced by a newer successful CI build from another actor and was not overwritten. All32required PyPI versions are present, with five hash-repair MRs published; all five MRs (recommended78, task-quality57, daily8, ab50 and rowers79) were subsequently merged after explicit approvals. Ab master140800 succeeded including build/tests/lints; the user subsequently ran productiondeploy3223291 and its success was verified by GET (allocation/application health unverified). Rowers master140801 also succeeded with build/test/Nomad lint; all five merged consumer master pipelines are successful. Recommended master140796 and task-quality master140797 post-merge CI succeeded. Daily correction140798 build-only CI also succeeded; approved MR8 merge created master140799, which succeeded in its build-only CI. All three prior infrastructure-failing consumers now have successful master CI. No allocation/application health or periodic execution is claimed. The agent performed no deployment; the later user-executed ab production deploy was verified through GitLab job status.

## Task, authorization and actions

The user authorized continuation of library/image recovery and local fallback when CI was blocked. Work follows the existing exact-version source inventory and publication approvals; source/lock fixes, deployments and periodic job execution are outside this stage. Existing source release refs and historical build-tool versions were used. Packages with known mismatching hashes were initially held. After concrete hash-only consumer patches were reviewed and local branch preparation was approved, the seven substitute artifacts for six versions were separately approved for publication and verified through Nexus GET metadata.

Published modern versions: basis10.0.2 (previous stage), toster6.1.1, aio-service-client8.0.1, eventum5.0.1 and basis-fastapi2.1.0. Both wheel and sdist match consumer hashes.

Published exact-wheel-only Poetry versions (11): basis3.0.9/3.1.0/8.1.3, toster6.0.0, aio-service-client3.1.1/4.1.0/6.0.1, eventum3.0.4, basis-fastapi0.6.3 basis-aiohttp5.1.1 and eventum1.0.1. Source archives that did not match retained hashes were skipped. These versions satisfy the verified wheel artifacts; matching source archives are not claimed restored.

Published exact-source setuptools source archives for requirements-only consumers: castle1.0.1, iss1.0.1, basis2.1.0/3.0.4, toster4.1.0, aio-service-client2.2.2, eventum0.0.1 and basis-aiohttp2.1.1/2.2.3/2.9.0. Consumer hashes were absent, so the published checksums verify uploaded bytes against locally built manifests only.

## Findings and evidence

Eventum1.0.1 built naturally with poetry-core1.0.7 reproduces wheel SHA256 `12056581ce0b48b911cf7b197ba58a89f0cbd785e1191a9ad5ea863926aa603b`; approved publication succeeded and Nexus GET metadata verified this original wheel SHA256. The six originally hash-blocked versions are metronom3.2.3, castle5.2.0/5.2.1, basis2.1.2, toster4.2.0 and iss2.0.0. They have now been published with reviewed new hashes, with approved consumer lock repairs now published in five MRs. No integrity bypass was introduced.

Generated evidence in `~/ai-data/nexus-pypi-recovery/`: `local-uv-publication-results.json`, `local-poetry-publication-results.json`, `local-setuptools-publication-results.json`, corresponding publication-review files and per-release manifests under `remaining-libraries/`; previous basis/extraform verified manifests are linked from [basis execution](2026-10-13-nexus-pypi-basis-recovery.md). Packages were verified through Nexus component/checksum metadata without package downloads.

Live read-only Nomad evidence: `nomad-periodic-inventory.json`, `nomad-periodic-resolved-versions.json` and `nomad-cron-manifest-availability.json`. Unique image families are ab-pipeline, cashflow, daily-compilations-generator, extraform, nexus-cleaner, recommended-tasks-generator, rowers-ranker and youtrack_sprints_creator. Extraform image was published and digest-verified in the previous stage. Daily-compilations-generator, cashflow, nexus-cleaner and youtrack_sprints_creator local builds and separately approved publications completed successfully (exit0 each), covering15periodic tasks; independent manifest config checks match each local image. A published image makes bytes available to future pulls; it does not update current allocations, restart a job or force a periodic run.

## Consumer hash review proposal and additional probes

Bounded reconstruction probes varied legacy gzip/tar timestamp metadata without changing package source;10242toster candidates and11718basis candidates failed to reproduce the respective original hashes. No original artifact was found. This explains why the six versions needed the reviewed new-hash recovery path rather than exact-byte restoration.

Read-only GitLab GETs prepared concrete snapshot diffs for five repositories and seven refs, with15hash replacements only. Default `master` consumers are `data/ab-pipeline`, `data/rowers-ranker`, `data/recommended-tasks-generator`, `data/task-quality-control` and `data/daily-compilations`. Additional deployed-release snapshots are rowers-ranker0.19.3 and recommended-tasks-generator1.16.24. Full resolved source SHA/ref, original/proposed file SHA256 and candidate artifact hashes are recorded in `~/ai-data/nexus-pypi-recovery/consumer-approval-proposal.json`; original and proposed lockfiles plus unified diffs are under `consumer-lock-review/`. This covers all default-branch consumers identified by the62project audit and deployed releases selected by current Nomad inventory, not every historical consumer tag.

Proposed repository branch is `DevOps-891-restore-python-package-hashes`, base `master`, separately in each of the five projects. Existing lock versions, URLs, other hashes and Pipfile `_meta` are preserved. Pipfile single sdist hashes are replaced with one rebuilt sdist hash; metronom wheel and sdist hashes are replaced while its existing underscore filenames/URLs stay unchanged. Candidate file hashes were checked locally. Legacy Pipfile assets are hyphenated sdists without artifact URLs in those locks; eventual Nexus path is pending publication metadata, not claimed verified before upload.

Supervised Git training requires explicit user approval of repository/branch/base before checkout branch/source edits. Preparation of the proposal made no repository checkout edits, commits or external writes. The user subsequently confirmed preparation in all five repositories with branch `DevOps-891-restore-python-package-hashes` and base `master`; local implementation is recorded below. Existing release tags must not move: the rowers0.19.3 and recommended1.16.24 consumers need a separately approved new release/source/image policy; a master MR alone does not repair their historical release source. Blocked runtime images are ab-pipeline:master, recommended-tasks-generator:1.16.24 and rowers-ranker:0.19.3.

## Supervised consumer branch preparation

The user replied "Подтверждаю" to the explicit five-repository branch/base proposal. This authorizes local task branch creation and lock edits only. The approved branch is `DevOps-891-restore-python-package-hashes`, base `master`, independently in all five checkouts. `ab-pipeline` was cloned locally; the other existing checkouts were reused. Previous branches and resolved base commits are retained in `~/ai-data/nexus-pypi-recovery/consumer-branch-preparation-results.json`.

| Repository | Base commit | File | Hash replacements |
| --- | --- | --- | --- |
| data/ab-pipeline | ddc7bc422dc160e82301653ac12b9302acbd53dd | uv.lock | 2 |
| data/rowers-ranker | 3fa21fcb4f8b39e68e1b55313791a5ba719b634f | Pipfile.lock | 2 |
| data/recommended-tasks-generator | 55c20d0e9e80269c9a37a5fad2ab8178206884ba | Pipfile.lock | 3 |
| data/task-quality-control | ade4028556aff35224999671b411565e5af1cb91 | Pipfile.lock | 2 |
| data/daily-compilations | 55200335572b9b5c46def629d5dc99d35e627237 | Pipfile.lock | 1 |

All ten changes are hash-only replacements for the rebuilt artifacts. Original versions, artifact URLs and all other lock content remain unchanged. `git diff --check`, lock snapshot SHA256 and rebuilt-artifact hash checks pass for all five checkouts. This verifies the local patch and artifact identity; dependency installation, application tests and runtime behavior were not tested. Six rebuilt versions are now published with Nexus metadata verification, but complete consumer image builds are not yet claimed.

At the local preparation checkpoint no paths were staged, committed or pushed and no MR existed. The later stage-two approval and publication are recorded below. Proposed commit message is `restore python package hashes`; proposed MR title is `DevOps-891 restore python package hashes`, source `DevOps-891-restore-python-package-hashes`, target `master`, independently per repository. The eventual MR body must be one short Russian paragraph describing the hash repair followed by [DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891). CI review establishes that feature-branch pipelines in all five repositories automatically publish the branch image and `latest` before tests. Stage-two approval must explicitly cover these registry effects; it does not authorize merge or Nomad deployment. Feature-branch pipelines have no Nomad deployment.

Image evidence: per-project `cron-local-builds/*/manifest.json`, `cron-local-builds/*/publication-verification.json`, `cron-image-build-plan.json` and `free-cron-image-publication-plan.json`. All four publication verification files show `push_exit_code=0` and `remote_config_matches_local=true`. Published runtime references are daily-compilations-generator:0.6.9, cashflow:master, nexus-cleaner:0.0.10 and youtrack_sprints_creator:master. Together with extraform, registry coverage is five ofeight images and19of23periodic tasks. Missing images remain ab-pipeline:master (one task), recommended-tasks-generator:1.16.24 (two tasks) and rowers-ranker:0.19.3 (one task). Publication verifies registry availability only; no Nomad/app/default-CMD/deployment action or periodic execution was run.

## Reviewed rebuilt package publication

A separately approved publication command uploaded seven files for six source-version-verified releases: basis2.1.2, castle5.2.0/5.2.1, iss2.0.0 and toster4.2.0 source archives, plus metronom3.2.3 wheel and source archive. All seven Nexus component GET checksums match the reviewed rebuilt files; none match the retained original consumer hashes. Evidence is `~/ai-data/nexus-pypi-recovery/reviewed-rebuilt-package-publication-results.json`, which records each exact publisher source SHA, filename, old/new checksum, publication status and verification result. This brings version availability to32of32; it does not make unchanged hash-pinned consumers install successfully.

Local builds using the original Dockerfiles from all five approved consumer branches completed successfully with build exit0. Full pytest and application/runtime tests were not run. All five branches were subsequently published with approved commits and MRs; CI outcome remains pending. Three original periodic runtime image references remain unrestored; approved master repair branches do not repair the historical rowers-ranker0.19.3 and recommended-tasks-generator1.16.24 release locks, and their replacement release/image policy remains undecided.

## Stage-two publication review

The concrete review is `~/ai-data/nexus-pypi-recovery/consumer-publication-review.json`; Russian MR text is `consumer-mr-description.txt`. It covers only the five reviewed lock files and ten SHA256 replacements. Source is `DevOps-891-restore-python-package-hashes`, target `master`, commit `restore python package hashes`, title `DevOps-891 restore python package hashes` for each project. Dry-run publication tooling does not stage, commit, push or create an MR; those states were absent at the review checkpoint, before the subsequent explicit confirmation and execution recorded below.

All five local original-Dockerfile builds pass with exit0; evidence is `consumer-local-build-results.json` and per-project `consumer-local-builds/*/manifest.json`. Safe installed-package metadata checks pass with exit0 for all five projects, and installed internal package versions match expectations. The initial daily-compilations probe used unavailable `importlib.metadata` on its older Python; repeating with existing `pkg_resources` passed and verified basis2.1.2, without installing tools or changing source. Final aggregate `consumer-local-build-results.json` records all five successful builds, smoke results and installed versions; comparison with the expected versions passes. Final `git diff --check` passes in all five repositories; only the approved lock file is modified in each, staged changes are empty and no extra untracked files are present. Metadata smoke checks use no application imports and no application/default command; they run without network access. Full pytest was not run locally, and no database/test services were started. No consumer image was pushed.

CI review confirms that all five feature-branch pipelines automatically build and push their branch image and `latest`. In ab-pipeline, rowers-ranker, recommended-tasks-generator and task-quality-control, pytest runs after those registry publications; daily-compilations has no test job in this pipeline. Feature branches do not deploy to Nomad. The stage-two confirmation must explicitly cover automatic `latest` publication as well as the reviewed commit/push/MRs. No merge, target-branch push, tag movement or deployment is implied. Existing historical consumer tags retain their old hashes until a separate release/source/image decision.

The user explicitly instructed enabling shared runners for these five projects. Read-only prechecks showed they were already enabled in ab-pipeline582, rowers-ranker231, recommended-tasks-generator213 and daily-compilations204. Only task-quality-control208 had `shared_runners_enabled=false`, with no available project/group runners. The authorized project208 PUT enabled shared runners; independent final project GETs verify `shared_runners_enabled=true` in all five. Evidence is `consumer-shared-runners-enabled.json`. No pipeline retry, branch push or deployment was performed as part of this configuration change. Read-only MR settings checks found no existing task MRs in the five projects; squash remains disabled and the configured assignee is the user.

## Approved Git/MR publication

The user replied "Да" to the explicit stage-two proposal covering the five reviewed commits, task branch pushes, MR creation and automatic CI branch-image/`latest` publication effects. This approved the combined publication action only; no merge, target-branch push, historical tag movement, manual CI job, Nomad deployment or periodic execution was authorized.

The approved helper `publish_consumer_branches.py` completed all five publications. Commit message and MR title match the reviewed names; all MRs target `master` from `DevOps-891-restore-python-package-hashes`, assign `a.solonenko`, preserve squash disabled and source-branch removal enabled. Immediate independent GitLab GET checks verify the published commit SHAs and MR settings. Evidence is `consumer-git-publication-results.json`.

| Repository | Commit | MR | Pipeline |
| --- | --- | --- | --- |
| data/ab-pipeline | b9714406ae72fd5d94704f14c2ab75801c1d67e2 | [!50](https://gitlab.youdo.sg/data/ab-pipeline/-/merge_requests/50) | [140778](https://gitlab.youdo.sg/data/ab-pipeline/-/pipelines/140778) |
| data/rowers-ranker | 2735dcb935c28b3967a5dbdb296af65c1e9dae23 | [!79](https://gitlab.youdo.sg/data/rowers-ranker/-/merge_requests/79) | [140779](https://gitlab.youdo.sg/data/rowers-ranker/-/pipelines/140779) |
| data/recommended-tasks-generator | 5899dd9ef1c8f66d0973d347e9a630d56a63be6a | [!78](https://gitlab.youdo.sg/data/recommended-tasks-generator/-/merge_requests/78) | [140780](https://gitlab.youdo.sg/data/recommended-tasks-generator/-/pipelines/140780) |
| data/task-quality-control | c9792b22d75df976cb5671cb2888b30310c52fe0 | [!57](https://gitlab.youdo.sg/data/task-quality-control/-/merge_requests/57) | [140781](https://gitlab.youdo.sg/data/task-quality-control/-/pipelines/140781) |
| data/daily-compilations | a6592bb2959fd66cf7e54eb124372ab06c20fa02 | [!8](https://gitlab.youdo.sg/data/daily-compilations/-/merge_requests/8) | [140782](https://gitlab.youdo.sg/data/daily-compilations/-/pipelines/140782) |

Initial pipeline states were pending for ab-pipeline, recommended-tasks-generator, task-quality-control and daily-compilations, and running for rowers-ranker. These are initial observations only, not CI success or registry-publication verification. Fresh verification in `consumer-publication-verification.json` confirms all five remote SHAs, MR source/target/title/body matches, clean local checkouts and commits containing exactly the approved ten hashes across five lock files. All five pipelines140778–140782 are now running with build jobs running; shared runners are enabled in all five projects. CI completion and resulting registry image publication remain pending. No merge, deployment, manual job or retry was performed. Thirty-two package versions are available and five of eight periodic runtime image references remain verified; these MRs do not by themselves restore the three missing original runtime images or change existing allocations.

## Historical release-copy build approval and CI follow-up

The user explicitly confirmed local builds from the original historical releases rowers-ranker0.19.3 and recommended-tasks-generator1.16.24 with only their reviewed lock hashes changed. `build_cron_release_copies.py` retrieves exact GitLab tag archives, verifies each tag SHA and full source file membership, and checks that only `Pipfile.lock` differs. Repository checkouts, Git tags and existing MRs remain unchanged. This approval covers local source-copy/build work only; publishing the original runtime image tags still needs explicit approval.

Rowers-ranker0.19.3 source SHA `6d8806a5ddff4a9c9e5b29fb842487de7001b95b` local build succeeded with the unchanged original Dockerfile. Safe metadata checks passed, including castle5.2.1 and iss2.0.0. Local image ID is `sha256:d62bf19e413104d1db8115ab90689efa035b0e580959505cd6d131870d8b49d6`; size2527313414bytes. Evidence is `cron-release-local-builds/rowers-ranker/manifest.json`. Recommended-tasks-generator1.16.24 source SHA `55c20d0e9e80269c9a37a5fad2ab8178206884ba` also completed its original-Dockerfile build and safe metadata checks with exit0, including castle5.2.0, toster4.2.0 and iss2.0.0. Its image ID is `sha256:7c52ed4102952e62e78cc837896d0029d3b5e3656fd60da888b0c6c7289cede4`, size3705259585bytes. Aggregate evidence is `cron-release-local-build-results.json`: both tag SHAs are verified, all non-lock files/membership unchanged and only five reviewed hashes differ (rowers2/recommended3). No source-copy image publication, application/default-command run, full test suite, deployment or Git change occurred.

The prepared publication helper `publish_remaining_cron_image.py` targets three runtime references: ab-pipeline:master from the reviewed master-based source plus uv.lock repair, rowers-ranker:0.19.3 and recommended-tasks-generator:1.16.24 from the approved exact historical source copies plus hash repair. Ab-pipeline uses local image `sha256:9113901809941b9c79552c36f0826bca854e7e9398eab604a8a1e03b6234dfab` from approved master base `ddc7bc422dc160e82301653ac12b9302acbd53dd` plus the uv.lock repair. Dry-run registry preflights in `remaining-cron-image-publication-review.json` confirm all three exact runtime manifests are absent, with publication/default-command/deployment flags false. No push has occurred. Registry coverage remains5of8references/19of23periodic tasks until these publications are approved and verified. The final publication proposal targets exactly `registry.youdo.sg/data/ab-pipeline:master`, `registry.youdo.sg/data/rowers-ranker:0.19.3` and `registry.youdo.sg/data/recommended-tasks-generator:1.16.24`. No additional aliases, Git tags, CI retries, deployment or periodic execution are included.

At `2026-10-13T17:00:58Z`, `consumer-ci-current-status.json` records rowers-ranker pipeline140779 successful with build3223104, test3223105 and Nomad lint3223106 all successful. Its CI build trace records branch tag and `latest` pushed with digest `sha256:f9ceaec9d876f5b0c35d627fedabd89a944f8fb5bd6dc5d01dd8733d1f432f39`; this is a feature-branch image and does not verify the missing historical0.19.3 runtime tag.

Task-quality-control pipeline140781 failed in [build3223110](https://gitlab.youdo.sg/data/task-quality-control/-/jobs/3223110) at Dockerfile step7, `RUN pip install pipenv==2022.1.8`, with `cgroups: cgroup mountpoint does not exist: unknown`. Docker failed before pip ran; this is an infrastructure failure separate from recovered package hashes. Its test/lint jobs were skipped. No retry, runner restart or legacy DinD compatibility fix was performed; those changes are outside the hash-only patches and remain separate work. A subsequent October13 snapshot in the same `consumer-ci-current-status.json` supersedes the ab-pipeline state: pipeline140778 is fully successful, including build, tests, Nomad lint, Ruff and mypy. Rowers140779 remains fully successful; recommended140780 and daily140782 builds remain running, and task-quality-control remains infrastructure-failed with no retry or fix.

## Final automatic CI results and runtime publication progress

At `2026-10-13T19:03:29Z`, `consumer-ci-current-status.json` records ab-pipeline140778 and rowers-ranker140779 fully successful. Three automatic pipelines failed on infrastructure paths: task-quality-control build3223110 retained its cgroup failure before pip; recommended-tasks-generator [build3223107](https://gitlab.youdo.sg/data/recommended-tasks-generator/-/jobs/3223107) hit the one-hour execution timeout while pushing the branch image, after layers uploaded but without a final manifest success claim; daily-compilations [build3223113](https://gitlab.youdo.sg/data/daily-compilations/-/jobs/3223113) hit the one-hour timeout at `FROM python:3.7-buster` while pulling the base image. No code fix, CI retry or timeout/runner change was performed. All five local original-Dockerfile and safe installed-version checks had passed separately.

The separately approved runtime push of ab-pipeline:master completed with exit0. Independent remote manifest/config verification matches local config `sha256:9113901809941b9c79552c36f0826bca854e7e9398eab604a8a1e03b6234dfab`, recorded in its `runtime-publication-verification.json`. Registry runtime coverage is now6of8references/20of23periodic tasks at this checkpoint. Rowers0.19.3 publication is in progress and recommended1.16.24 follows; all-eight completion is not yet claimed.

## Default DNS verified and second runtime push complete

`default-pypi-dns-final-verification.json` verifies workstation default DNS resolves `pypi.youdo.local` to10.18.24.233 and ordinary HTTP `/simple/` reaches `http://pypi.youdo.local/repository/pypi/simple/` with200, without `--add-host` or forced-IP routing and without package downloads. This supersedes the earlier workstation stale-DNS observation. It does not verify every runner container resolver or the unused legacy root POST endpoint. The recovery deployment log and system map verify this address and runtime, but do not establish the recovery host cloud provider. The corporate hostname alone is not provider evidence; VK-only address-file scope remains unconfirmed, so the address map was not changed pending provider evidence.

The separately approved rowers-ranker:0.19.3 runtime push is complete with independent remote config matching local image `sha256:d62bf19e413104d1db8115ab90689efa035b0e580959505cd6d131870d8b49d6`; its `runtime-publication-verification.json` records the proof. Registry coverage is7of8runtime references/21of23periodic tasks at this checkpoint, including ab:master. Recommended-tasks-generator:1.16.24 publication remains in progress; no all-eight completion is claimed yet.

## Three remaining runtime publications completed

The separately approved three-tag batch completed with exit0. `remaining-cron-image-publication-results.json` and each image's `runtime-publication-verification.json` independently verify remote manifest/config identity against the reviewed local image. The exact source provenance and lock-only changes are preserved; no extra aliases, Git/source/tag mutation, merge, deployment or application/default command was run.

| Runtime reference | Manifest digest |
| --- | --- |
| `registry.youdo.sg/data/ab-pipeline:master` | `sha256:366e1f2a43246f3eb7b15c3b49439189c4b0e2defb2cb3765f061023bd8d7e22` |
| `registry.youdo.sg/data/rowers-ranker:0.19.3` | `sha256:571f7cfa29666251c4fb978fe9d3d3f13798b51862f7362443ca8e422f10d893` |
| `registry.youdo.sg/data/recommended-tasks-generator:1.16.24` | `sha256:389cc20294a056171a0345bab2013c8db23e5c65ef4a405f9c79745df7e1a5c1` |

All three final runtime tags are now published and config-verified. The final GET-only scan of all eight runtime references confirms every manifest is present; details and the later cashflow replacement are recorded below. The five hash MRs remain open/unmerged, with two successful pipelines and three separate infrastructure failures. This package/image availability recovery does not validate current allocations or execute any of the23periodic jobs.

## Final artifact availability verification

At `2026-10-13T20:18:27Z`, `nomad-cron-final-coverage-verification.json` records `available_images=8`, `unique_images=8` and `periodic_jobs=23`: all original runtime references from the inventory have manifests available. `matching_our_published_images=7` distinguishes current identity from availability. Seven configs match this recovery's publication proofs, including all three final pushes. No runtime image is missing from this inventory.

Cashflow:master is available with newer config `sha256:7b3e61575df7dbeea97c64113b26d4b1dcdfa1acdc47ff8b225bbdb29167be12`, replacing the earlier recovery image `sha256:e18f9b78c80d65a4b4214223604014aa72c514ef6be30200c90d4a264c15cc1a`. The exact current config appears in [successful later CI build3223227](https://gitlab.youdo.sg/youdo/finance/cashflow/-/jobs/3223227), pipeline140792, source SHA `20e641529b248ccaf888229b0af231e811d4642c`. This is a later external CI publication, not a recovery integrity mismatch or reason to overwrite the tag. The previous approved local publication proof remains historical evidence. A still later pipeline140793 build is successful, but the verified current registry config matches140792 at this snapshot.

The requested artifact recovery reaches32of32required PyPI versions and8of8runtime image references for23periodic jobs. Six rebuilt PyPI versions require the published consumer hash repairs; the five MRs remain unmerged. The latest checked hash-MR CI states are two full successes and three separate infrastructure failures (cgroup, push timeout, base-pull timeout), retained as separate backlog items. No merge, Nomad deployment, periodic trigger, application/default-command run, current-allocation health verification or CI retry was performed during this recovery. Verification used manifests/config metadata and package checksums, without package or image-layer downloads in the final pass.

## Detailed read-only CI failure audit

`consumer-ci-failure-detailed-evidence.json` refines the three failures without source, runner, host or CI mutations. Jobs queued for approximately one second; instance runners were active, online and unpaused, so these are execution failures rather than unavailable-runner queue delays.

Task-quality-control3223110 ran on runner105/172.28.0.171 with Docker client19.03.12 and DinD19.03.12. The first Dockerfile `RUN` failed launching its container with `cgroups: cgroup mountpoint does not exist`, before pip could execute. An incompatibility between this old DinD and the host cgroup setup is a hypothesis; host cgroupv2 was not verified and must not be stated as the confirmed cause.

Recommended-tasks-generator3223107 ran on runner105 with client25.0.5-git and DinD20.10. Its image build succeeded; the failure occurred in branch-image publication. Fourteen of15layers reached `Pushed`, while layer `6c4b3481bc28` did not, and no final manifest digest was reported before the one-hour job deadline. Executor preparation consumed22minutes9seconds of that deadline. The unfinished layer/upload or registry processing needs further evidence; neither a package-build failure nor a specific network cause is established.

Daily-compilations3223113 ran on runner106/172.28.0.172 with client19.03.12 and DinD19.03.12. All eight base-image layers reached `Download complete`, but only three reached `Pull complete` before the one-hour timeout. Executor preparation consumed10minutes18seconds. The block is in pull finalization/extraction/registration; a network download stall is not proven. As a positive control, rowers build3223104 succeeded on the same runner106 in8minutes16seconds using floating Docker/DinD images. This does not establish their exact modern versions without Docker runtime information, but it disproves that runner106 could not execute any build.

No retry, version pin, runner restart, timeout edit or application/source change was performed. These failures remain separately tracked infrastructure work after completed32-version/8-runtime-reference artifact availability recovery.

## Explicit recommended retry and task-quality DinD proposal

The user requested updating task-quality-control to fresh DinD and retrying the recommended-tasks-generator failure. The separately authorized GitLab retry POST for original build3223107 created [job3223259](https://gitlab.youdo.sg/data/recommended-tasks-generator/-/jobs/3223259) in pipeline140780 at the unchanged commit `5899dd9ef1c8f66d0973d347e9a630d56a63be6a`; an independent GET records pending. Evidence is `recommended-ci-retry.json`. This does not erase the original one-hour failed attempt or establish a successful retry. No other job was retried.

Read-only inspection found the task-quality-control checkout clean on existing `DevOps-891-restore-python-package-hashes`, with MR57 open against `master`. The proposed minimal build-job edit pins matching official `docker:29.9.0-cli` and `docker:29.9.0-dind`. Official release evidence identifies29.9.0 released October8, and read-only manifest checks confirm both Linux amd64 images available; `task-quality-dind-image-proposal.json` records availability. The two-line patch and proposed YAML are review artifacts in `task-quality-dind-proposed.patch` and generated proposal files under the recovery directory, not repository edits.

At the proposal checkpoint supervised approval was pending for reuse of the existing task branch in `data/task-quality-control` from base `master`; the subsequent user approval and local edit are recorded below. The previous hash-only publication approval does not cover this new CI source change. No repository edit, new commit, push, MR update, runner/host mutation or new CI run occurred while preparing the proposal. After branch reuse approval, the actual diff and checks plus automatic branch-image/`latest` CI effects need separate publication review.

## Approved task-quality branch reuse and local DinD edit

The user explicitly approved reusing `DevOps-891-restore-python-package-hashes` in `data/task-quality-control`, base `master`, for the minimal build-job DinD correction. Exactly two `.gitlab-ci.yml` lines were changed locally: build image `docker:29.9.0-cli` and build service `docker:29.9.0-dind`. The release job was left untouched. `git diff --check` passes; the new CI edit is not staged, committed or pushed.

At the local checkpoint stage-two publication remained pending. The reviewed commit was `update docker cli and dind`; MR57's proposed final title is `DevOps-891 restore python builds`. Its description must be one short Russian paragraph covering the existing lock-hash restoration and matching Docker client/DinD update, followed by the DevOps-891 task link. The publication review must cover the actual two-line CI diff, validation and automatic branch-image/`latest` effects. Branch-reuse approval authorizes local edits only, with no CI run, runner mutation or deployment.

## Approved task-quality DinD publication

Validation of the local two-line edit passed: PyYAML parsed the CI file, deep comparison against HEAD after substituting only build.image/build.services found no other semantic change, `git diff --check` passed and the index was empty before the approved publication.

The user explicitly approved stage-two publication with automatic branch-image/`latest` CI effects. Commit `1459a1f89e79388b8ac4d090badd04b221e81fe0` (`update docker cli and dind`) was pushed to the approved existing branch, and [MR57](https://gitlab.youdo.sg/data/task-quality-control/-/merge_requests/57) updated to `DevOps-891 restore python builds` with the approved one-paragraph Russian description and task link. Independent GitLab GETs verify remote SHA, title/body (GitLab trims its terminal newline), source/target and preserved squash disabled, source-branch removal enabled and assignee `a.solonenko`. The local checkout is clean. Evidence is `task-quality-dind-publication.json`.

New pipeline140795 and build3223277 are running; the build trace confirms executor `docker:29.9.0-cli` and service pull `docker:29.9.0-dind`. Test3223278 is created and CI completion remains pending; a running build does not yet verify the cgroup correction or publication success. Recommended retry3223259 also remains running in the latest independent GET stored in `recommended-ci-retry.json`. No merge, deployment, runner/host mutation or additional retry was performed.

## Recommended build retry succeeded

After the user reported completion, independent GitLab GET verifies recommended-tasks-generator retry3223259 succeeded, finished `2026-10-13T23:51:07+03:00`. The trace records successful final manifests for both `devops-891-restore-python-package-hashes` and `latest`, each digest `sha256:1a1ceb2c3d6a1704bb470ce07af0f3d25c0130c8415ab01340837857c71cca75`. Evidence is `recommended-ci-retry-final.json`. This confirms the repeated build/push succeeded with unchanged source; the first timeout was transient in outcome, but its root cause is still unproven.

Pipeline140780 remains running: test3223108 is running and Nomad lint3223109 succeeded, so full pipeline success is not yet claimed. Task-quality-control140795/build3223277 remains running with its test still created. No new retry, merge, deployment or source change was performed for this read-only confirmation.

## Recommended pipeline fully successful

Independent GET at `2026-10-13T20:56:40Z` confirms recommended-tasks-generator pipeline140780 succeeded, finished `2026-10-13T23:55:39+03:00`; retry build3223259, Nomad lint3223109 and test3223108 all succeeded. Evidence is `consumer-ci-followup-final.json`. This supersedes the pending test/pipeline checkpoint above; MR78 remains unmerged.

Task-quality-control pipeline140795/build3223277 remains running with its test created, and the separate daily-compilations base-pull timeout remains unresolved. No merge, deployment or further retry was performed.

## Explicitly approved recommended MR merge

The user explicitly approved merging recommended-tasks-generator MR78 into `master` after a direct permission question. Prechecks verified the MR opened, mergeable, not draft, discussions resolved and successful head pipeline140780. The scoped PUT `/projects/213/merge_requests/78/merge` used expected SHA `5899dd9ef1c8f66d0973d347e9a630d56a63be6a`, without squash override or settings changes.

Independent GET confirms MR78 merged at `2026-10-13T23:58:17.875+03:00`, merge commit/new master `1fa2457d0fdbc6f3f020c0a8b112b4b4baeba010`, previously `55c20d0e9e80269c9a37a5fad2ab8178206884ba`. Master [pipeline140796](https://gitlab.youdo.sg/data/recommended-tasks-generator/-/pipelines/140796) was created; its completion remains pending. Evidence is `recommended-mr-78-merge.json`. This separate approval covers only MR78 merge; other MRs were untouched, and no tag, manual deployment or periodic job action was performed.

## Task-quality DinD correction passes full CI

Independent GET at `2026-10-13T21:03:48Z` (October14 Moscow time) confirms task-quality-control build3223277 succeeded, finished `2026-10-13T23:59:44+03:00`, and pipeline140795 fully succeeded including test3223278. The trace records successful branch/`latest` manifests digest `sha256:b1f0871a6792b87be67e20b6b0d3c28a7b76c6ef6b7388b0a1eb45ff836af36f`; the earlier cgroup mountpoint error is absent. Evidence is `task-quality-dind-build-final.json`. The matching Docker29.9.0 client/DinD edit is verified by successful CI; this does not establish the host cgroup version or the exact original incompatibility mechanism.

MR57 remains unmerged and any merge needs explicit user authorization. Recommended master pipeline140796/build3223279 is still running with its test created, and the separate daily-compilations timeout remains open. No merge, deployment or additional retry was performed for this read-only verification.

## Explicitly approved task-quality MR57 merge

The user explicitly approved merging task-quality-control MR57 into `master` after successful head pipeline140795. Prechecks verified mergeability, non-draft status and all discussions resolved. The scoped merge PUT used expected SHA `1459a1f89e79388b8ac4d090badd04b221e81fe0`, without squash override or project/MR settings changes.

Independent GET verifies merged at `2026-10-14T00:04:57.139+03:00`, merge commit/current master `a51285b3d4493556a79a923065a6950b0904135f`, previously `ade4028556aff35224999671b411565e5af1cb91`. New [master pipeline140797](https://gitlab.youdo.sg/data/task-quality-control/-/pipelines/140797) was created and its completion remains pending. Evidence is `task-quality-mr-57-merge.json`. Other MRs were untouched; no tag, manual deployment or periodic job action was performed.

## Explicit daily-compilations retry

The user explicitly requested retrying the third failed build, daily-compilations3223113. The authorized POST `/projects/204/jobs/3223113/retry` created [job3223283](https://gitlab.youdo.sg/data/daily-compilations/-/jobs/3223283). Independent GET verifies pending status, unchanged pipeline140782 and source SHA `a6592bb2959fd66cf7e54eb124372ab06c20fa02`. Evidence is `daily-ci-retry.json`. No source or runner change accompanied this retry; the previous downloaded-base pull-finalization timeout remains historical evidence with unproven root cause. Retry success is not yet claimed.

## Daily retry reveals first-RUN cgroup failure

Fresh GET verifies daily-compilations retry3223283 failed with `script_failure`, finished October14 at00:07:14MSK; pipeline140782 remains failed. Evidence is `daily-ci-retry-current.json`. The retry passed its base-image pull, then failed launching the first `RUN` container at Dockerfile step3/7, `pip install pipenv==2020.11.15`, with `cgroups: cgroup mountpoint does not exist: unknown`. The trace confirms Docker CLI/service19.03.12. The absent `latest` cache warning was ignored by the existing `|| true` command and is not this failure; no push digest was recorded.

The proposed next minimal correction matches task-quality-control's successful client/DinD29.9.0 update, scoped to daily's build-job overrides while preserving inherited release references. Existing branch `DevOps-891-restore-python-package-hashes`, base `master`, MR8 requires explicit supervised reuse approval before repository editing; that approval is not yet requested/obtained at this checkpoint. No fix, source edit or additional retry was performed. The first attempt's base-pull timeout root cause remains unproven; this retry supplies a separate concrete container-launch failure.

## Recommended post-merge master CI succeeded

Independent GET verifies recommended-tasks-generator master pipeline140796 succeeded at merge SHA `1fa2457d0fdbc6f3f020c0a8b112b4b4baeba010`, finished October14 at00:08:12MSK. Build3223279 and test3223280 succeeded. Evidence is `recommended-master-ci-status.json`. This completes post-merge CI validation for the explicitly approved MR78 merge, without further source or remote changes.

## Approved daily branch reuse and local build overrides

The user approved reusing `DevOps-891-restore-python-package-hashes`, base `master`, in daily-compilations/MR8 for the minimal29.9.0 build fix. The precheck checkout was clean at `a6592bb2959fd66cf7e54eb124372ab06c20fa02`. Exactly three YAML lines were added in `.gitlab-ci.yml`: build-job image `docker:29.9.0-cli` and services list containing `docker:29.9.0-dind`. Existing global old Docker references remain unchanged, preserving release-job inheritance/behavior.

PyYAML parsing passes; deep comparison after removing the two added build fields equals HEAD, `git diff --check` passes and the index is empty. Evidence is `daily-dind-actual.patch` and `daily-dind-approved.gitlab-ci.yml`. MR8 GET verifies open, expected SHAa6592bb2, existing settings squash disabled and source-branch removal enabled. No commit, push or MR update occurred yet.

Stage-two publication approval remains pending: commit `update docker cli and dind`, MR title `DevOps-891 restore python builds`, existing source branch to `master`, body `daily-dind-mr-description.txt` containing one short Russian paragraph and task link. Push CI automatically publishes branch/`latest` images; this daily pipeline has no test job and feature branches do not deploy. The local approval does not authorize publication, merge or deployment.

## Approved daily Docker override publication

The user approved stage-two daily publication, including automatic branch-image/`latest` CI effects. `publish_daily_dind.py` prechecks verified the exact reviewed three-line YAML diff, empty index, remote source SHAa6592bb2 and open MR8. Commit `6e5c72a477b6340899c1435e5777d73e4922ef75` (`update docker cli and dind`) was pushed to the approved existing branch; MR8 title is now `DevOps-891 restore python builds` with the approved Russian paragraph and task link.

Independent GET verifies remote SHA, title/body after terminal-newline normalization, source/target and preserved squash disabled, source-branch removal enabled and unchanged assignee. The local checkout is clean. Evidence is `daily-dind-publication.json`. New [pipeline140798](https://gitlab.youdo.sg/data/daily-compilations/-/pipelines/140798) was created; completion remains pending. No merge or deployment was performed.

## Task-quality master and daily correction CI succeeded

Fresh independent GETs confirm task-quality-control master pipeline140797 succeeded, finished October14 at00:14:41MSK, with build3223281 and test3223282 successful. Master/`latest` trace digest is `sha256:48f271a4dc56e0c71c061cd70d33d08efebb737cf68e6aeecd42c053d04361d6`; evidence is `task-quality-master-ci-status.json`. This completes post-merge CI validation for MR57.

Daily-compilations correction pipeline140798 succeeded, finished00:16:24MSK. Build3223284 is the only job in this pipeline; there is no automated test job, so build success does not claim application-test coverage. Branch/`latest` trace digest is `sha256:851d4a7fdd77090b985e56ae543a548293032c63d14dc2a085ae587516d0287d`; evidence is `daily-dind-ci-status.json`. The matching Docker29.9.0 build overrides pass CI and the prior first-RUN cgroup symptom is resolved for this run; exact old host-level mechanism remains unproven.

Daily MR8 remains unmerged pending explicit user approval. Ab-pipeline and rowers-ranker MRs also remain unmerged. No merge, deployment, manual job or further retry was performed for these read-only confirmations.

## Explicitly approved daily MR8 merge

The user explicitly approved daily-compilations MR8 merge into `master`. Initial GET returned mergeability checking and caused no mutation; a fresh GET then confirmed mergeable, successful head pipeline140798, all discussions resolved and no draft state. The merge PUT used expected SHA `6e5c72a477b6340899c1435e5777d73e4922ef75` with no squash override.

Independent GET confirms merged October14 at00:18:57.787MSK, merge commit/new master `39b7fd86c433deeb70f442225d4d57278401867a`, previously `55200335572b9b5c46def629d5dc99d35e627237`. [Master pipeline140799](https://gitlab.youdo.sg/data/daily-compilations/-/pipelines/140799) was created; completion remains pending. Evidence is `daily-mr-8-merge.json`. Ab-pipeline and rowers-ranker MRs were untouched; no manual deployment or tag action occurred.

## Daily post-merge master CI succeeded

Independent GET at `2026-10-13T21:20:41Z` confirms daily-compilations master140799 succeeded at merge SHA `39b7fd86c433deeb70f442225d4d57278401867a`, finished October14 at00:20:13MSK. Build3223285 succeeded and is the sole job; no automated tests are present. The trace records final master/`latest` digest `sha256:0dd8eb937a52c68c053b0af4148340d5791a004fc67b3fc813d3741bdbde9b47`. Evidence is `daily-master-ci-status.json`.

All three consumers with earlier CI infrastructure failures are now separately approved/merged and verified by successful master CI: recommended140796, task-quality140797 and daily140799. Original timeout/cgroup evidence remains historical; exact timeout and host cgroup mechanisms are unproven. Ab-pipeline and rowers-ranker MRs remain unmerged. No further merge, deployment, tag or retry action was performed for this verification.

## Explicitly approved ab-pipeline and rowers merges

The user explicitly approved both ab-pipeline MR50 and rowers-ranker MR79 merges into `master`. Prechecks verified each expected source SHA, successful head CI, mergeable/non-draft status and resolved discussions; squash remained disabled. Each scoped merge PUT supplied its expected SHA and preserved MR settings.

Independent GET confirms ab MR50 merged October14 at00:22:15MSK, master `7a430478ce27a5c7528d952722aec7f27061cc4b` from prior `ddc7bc422dc160e82301653ac12b9302acbd53dd`; rowers MR79 merged00:22:17MSK, master `f754bce4a91036ceff74d1423f60f6d39574ac68` from prior `3fa21fcb4f8b39e68e1b55313791a5ba719b634f`. Evidence is `ab-rowers-mr-merges.json`. New master [ab pipeline140800](https://gitlab.youdo.sg/data/ab-pipeline/-/pipelines/140800) and [rowers pipeline140801](https://gitlab.youdo.sg/data/rowers-ranker/-/pipelines/140801) are running.

All five consumer MRs are now merged after explicit approvals. Three master pipelines already succeeded; these last two remain under verification. No manual deployment, Git tag action or periodic job execution occurred.

## Ab-pipeline post-merge master CI succeeded

Independent GET at `2026-10-13T21:24:48Z` confirms ab-pipeline master140800 succeeded, finished October14 at00:24:14MSK. Build3223286, test3223290, Nomad lint3223289, Ruff3223287 and mypy3223288 all succeeded; master/`latest` trace digest is `sha256:85eaaadbcf976304b0cb90bdc11d7a2a7758f6ef88300403e0d3795fd701d445`. Production deployment3223291 remains manual and untouched; successful CI does not authorize or imply deployment.

Rowers master140801 is still running: build3223292 running, test3223293 and lint3223294 created. Evidence is `ab-rowers-master-ci-status.json`. Four master pipelines are now successful, with only rowers completion pending. No manual deployment or additional retry was performed.

## User-executed ab production deployment verified

The user reported manually executing ab-pipeline production deployment. Read-only GitLab GET confirms `deploy:production`3223291 succeeded, started October14 at00:25:48MSK and finished00:25:53MSK; pipeline140800 remains successful. Evidence is `ab-user-production-deployment.json`. This deployment was executed by the user; the agent only verified its job status and performed no deployment mutation.

Earlier statements that this job remained manual/untouched describe the prior checkpoint and are superseded by the user action. Job success does not independently verify Nomad allocations or application health; those were not checked. Rowers master140801 remains running, build3223292 running with test/lint created. No additional agent deployment or retry occurred.

## Final rowers master CI succeeded

Independent GET confirms rowers-ranker master140801 succeeded at merge SHA `f754bce4a91036ceff74d1423f60f6d39574ac68`, finished October14 at00:29:58.275MSK. Build3223292, test3223293 and Nomad lint3223294 succeeded; master/`latest` trace digest is `sha256:7dbf90e3719d2133849b73c1b0d4f981f8df397cd720292f710dd4631a42b7b1`. Evidence is `rowers-master-ci-status.json`.

All five consumer MRs are explicitly approved/merged and all five post-merge master pipelines are successful. Thirty-two required PyPI versions and all eight audited cron runtime references were restored/available in the prior metadata verification. This does not infer actual cron/allocation/application health; only the user-executed ab production deployment CI-job success was separately verified. No agent deployment, additional merge, tag action or retry was performed for this final GET confirmation.

## Changes and risks

The user subsequently replied "Да" to the final explicit publication proposal for exactly three runtime image tags: `registry.youdo.sg/data/ab-pipeline:master`, `registry.youdo.sg/data/rowers-ranker:0.19.3` and `registry.youdo.sg/data/recommended-tasks-generator:1.16.24`. This authorizes those three registry pushes only, with no other aliases, job/deployment execution, merge or Git tag change. The publication batch subsequently completed; independent manifest/config verification for all three is recorded above.

Remote changes in this batch are approved library asset publication, seven separately approved cron runtime image pushes plus the earlier extraform publication, the approved task-quality-control shared-runner enablement and five approved task branch pushes/MR creations. Local changes are generated build/review/manifests, five approved consumer lock patches, this log, existing plan/system maps, live TODO and sync notes. Credentials remained in runtime secret access paths; no secret values were recorded. No application source change, deployment or periodic execution was performed. Approved hash-only commits and MRs are recorded above. CI scheduling cause remains undetermined after the earlier retry was canceled for local fallback; stale pending-queue flags were disproved by database reads.

Artifact restoration is partial despite32of32 version availability: version entries do not imply both artifact types restored for every version, and six versions require the prepared new consumer hashes. Requirements-only source-equivalent archives lack historical byte-identity proof. Complete consumer builds and running-allocation health are separate verification work. Artifact availability work is complete for the audited scope; unmerged consumer repairs, separate CI infrastructure failures and any later runtime verification are tracked only in `~/ai/TODO.md`.

## Portable lesson

[Recover exact locked Python distribution hashes](../../../../general/knowledge/python/reproducible-wheel-recovery.md).

## Later runtime audit

[October14 read-only runtime audit](2026-10-14-nexus-nomad-cron-runtime-audit.md) verifies four non-cleaner parents with post-restoration runs, eighteen without retained detailed runtime records and actual worker image IDs blocked by SSH authentication. Cleaner is explicitly ignored per user. Artifact availability does not imply all23periodic tasks ran new image bytes.
