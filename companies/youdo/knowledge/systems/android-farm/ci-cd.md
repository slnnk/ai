---
system: android-farm
status: verified
checked: 2026-08-19
tags: [android, gitlab-ci, gradle, fastlane, google-play, huawei, rustore, nexus, runner]
---
# YouDo Android: infrastructure and CI/CD map

## Verified job observation (2026-11-05)

[Job3278160 diagnosis](../../log/2026-11-05-android-farm-dig-job-3278160.md) confirms `gradle:18` runs on the DevOps-908 branch. Suite setup fails against the configured Houston mock `yandex-test` URL (404), while read-only checks of the documented `vk-test` endpoint return200. The Zabbix API missing-`dbversion` outage was subsequently resolved under [DevOps-909](../../log/2026-11-05-zabbix-docker-before-data-mount.md); authenticated Enabled Selenium inventory returned all three farm hosts at15:41:31 UTC. Historical farm correlation was not resumed. These observations do not establish master cutover or device health.

## Staleness review (2026-11-04)

Historical November4snapshot: the local product checkout was clean at `227f7518c341` on `DevOps-833-fix-hotfix`; November12verification below supersedes its unknown merge status. The 2026-10-12 image recovery is already recorded below. Newer [Maven recovery evidence](../../log/2026-10-22-nexus-cyberity-aar-publication-assessment.md) and [central backlog](../../../../../TODO.md) record restored Cyberity/Fotoapparat artifacts and the user confirmation on 2026-10-23 that Android builds work; SDK runtime remains unverified. August build/dependency details and suite counts must not be treated as a fresh November snapshot.

## Backlog verification — 2026-11-12

Fresh default develop3461102079 contains DevOps-833patch227f7518c3; YouTrack confirms Fixed/resolved. Hotfix Rustore producer/artifact and fastlane0.0.9changes are merged. Earlier statements below about pending merge are historical. The legacy hot-fix ref last ran July2022; no post-fix hotfix/store execution claimed. Store protections/digest pinning are separate optional proposals. Current APK publication still lacks curl HTTP-failure handling; Nexus storage/publication recovery already completed November5. [Full audit](../../log/2026-11-12-android-farm-backlog-relevance-audit.md).

## Summary

- Map of YouDo Android delivery: product build, store publication, and autotests on a device farm.
- Product pipeline: GitLab `team-youdo-android/android-youdo4` (project 79, `.gitlab-ci.yml`) builds on runner tag `gitlab-runner-android-dind01-runner` in image `registry.youdo.sg/sysadmins/devops-tools/gradle:18`.
- Flows: `feature` (MR to `develop`, `assembleBeta`), `regress` (`staging`, beta/release APK and AAB), `hotfix` (branch `hot-fix`). Manual jobs `regress_publish_google`/`_huawei`/`_rustore` publish through `fastlane-docker` (`0.0.9`, Google Play 30% staged rollout).
- Build-to-autotest: manual `publish_for_tests` jobs put the APK and version marker in Nexus `raw-private/android`; `youdo-android-testing` (project 69) runs on `gradle:12` via Selenium Grid `192.168.30.30:4444` and Appium hosts `.147`/`.148` in Kazan.
- Runner host: `gitlab-runner-android-dind01.youdo.corp` (`172.28.0.175`, prod_selectel), privileged Docker executor, managed by `automation-services` (`gitlab-runners.yml`, role `roles/gitlab-runner`).
- State: DevOps-833 is Fixed/resolved; its patch is merged into develop (verified2026-11-12). A new real hotfix/store run was not performed.
- Risks: manual store jobs have no `environment` or protected-environment controls; mutable image tags; `latest` of `fastlane-docker` moves on any Git tag; plaintext access material in runner host vars; an untracked Firebase JSON in the `fastlane-docker` worktree; credentials exposed in Nexus and report artifacts.
- Read "End-to-end delivery routes" for the flows, "Main Android application pipeline" for jobs, "Dedicated Android build runner" for the host, and "Gradle build image" and "fastlane-docker publication image" for images.
- Read "Google Play service-account key rotation" for the `GOOGLE_PLAY_JSON_KEY_DATA` procedure, "Autotest pipeline and farm" for tests, "Confirmed gaps and risks" for open issues, and "Change record: DevOps-833 hotfix CI fix" for the fix details.

- Last checked: 2026-08-13 (Europe/Moscow)
- Priority: delivery infrastructure, CI runners and images, artifact flow, publication, test execution, and operational ownership.
- Sources: local Git repositories plus read-only GitLab project/registry metadata.
- Facts below are current as of the check date unless explicitly marked as a risk or inference.

## End-to-end delivery routes

### Product build and store publication

```text
developer / GitLab event
  -> team-youdo-android/android-youdo4 pipeline
  -> dedicated Android Docker runner in Selectel
  -> internal Gradle build image from sysadmins/devops-tools/gradle
  -> APK/AAB GitLab artifacts
  -> manual publish job using fastlane-docker
  -> Google Play / Huawei AppGallery / RuStore
```

### Build-to-autotest route

```text
android-youdo4 feature/regression/hotfix build
  -> manual publish_for_tests job
  -> Nexus raw-private/android APK + version marker
  -> youdo-android-testing GitLab pipeline
  -> integration-test Docker runner
  -> Selenium Grid in Kazan office
  -> Appium host -> ADB -> physical device/emulator
  -> HTML/JUnit/screenshots/page-source artifacts
  -> reports.youdo.com + Yandex Object Storage
```

## Main Android application pipeline

- GitLab project: `team-youdo-android/android-youdo4`, project ID `79`, default branch `develop`.
- Local clone: `/home/slnnk/git/android-youdo4`.
- CI definition: `.gitlab-ci.yml` in that repository.
- Build runner tag: `gitlab-runner-android-dind01-runner`.
- Build image: `registry.youdo.sg/sysadmins/devops-tools/gradle:18`.
- Build outputs use application module `youdoapp`; current compile/target SDK is 36 and minimum SDK is 23.

### Feature flow

- Trigger: merge request targeting `develop`, subject to `.rules_feature`.
- `feature` builds `assembleBeta`; APK artifact expires after two weeks.
- `feature_browserstack` uploads the beta APK to BrowserStack and is allowed to fail.
- `feature_notify` resolves YouTrack issue information and sends a notification.
- Two manual `feature_publish_for_tests_job_{1,2}` jobs upload APK plus version metadata to Nexus using logical test slots 1 and 2.

### Regression/staging flow

- Trigger: branch/ref `staging`.
- `regress` builds beta and release artifacts for Google, Huawei, and RuStore:
  - beta APK variants;
  - release APK variants;
  - release AAB variants.
- Artifacts expire after two weeks.
- BrowserStack upload and notification jobs consume regression artifacts.
- Manual publication jobs consume artifacts from `regress`:
  - `regress_publish_google` -> Google Play;
  - `regress_publish_huawei` -> Huawei AppGallery;
  - `regress_publish_rustore` -> RuStore.
- Manual test-publication jobs upload the regression beta APK to the two Nexus test slots.

### Hotfix flow

- Trigger: branch exactly `hot-fix`.
- `hotfix` builds beta plus Google and Huawei release APK/AAB artifacts in the current default-branch configuration.
- Manual Huawei and RuStore publication jobs exist; there is no Google hotfix publication job in the inspected CI file.
- Hotfix test-publication jobs upload the beta APK to Nexus logical slots 1 and 2.
- Remediation prepared on local branch `DevOps-833-fix-hotfix` on 2026-08-13: the hotfix build now also runs `:youdoapp:assembleReleaseRustore`, copies the resulting release Rustore APK into a named GitLab artifact, and both hotfix store jobs use `fastlane-docker:0.0.9`. This remains a working-branch change until committed/merged and exercised by a real `hot-fix` pipeline.

## Dedicated Android build runner

- Infrastructure repository: `/home/slnnk/git/automation-services`.
- Inventory: `inventories/prod_selectel/hosts`.
- Host: `gitlab-runner-android-dind01.youdo.corp`, `172.28.0.175`, inventory group `gitlab_runners_dind_android`; placement is the `prod_selectel` environment.
- Host variables: `inventories/prod_selectel/host_vars/gitlab-runner-android.yml`.
- Managed through root playbook `gitlab-runners.yml` and role `roles/gitlab-runner`.
- Configured as a privileged Docker executor with concurrency 3, internal-registry authentication, `/data/cache`, and shared S3 cache in Yandex Object Storage.
- The Android product pipeline and store-publication jobs both request the dedicated Android runner tag rather than a generic Docker runner.

## Gradle build image

- GitLab project: `sysadmins/devops-tools/gradle`, project ID `378`, default branch `master`.
- Local clone: `/home/slnnk/git/gradle`.
- Registry: `registry.youdo.sg/sysadmins/devops-tools/gradle`.
- Registry includes tags `6.7.1`, `10`, `11`, `12`, `13`, `17`, `18`, and `latest` at the check date.
- Android application builds use tag `18`; Android autotests use older tag `12`.
- Image pipeline builds a tag based on `CI_PIPELINE_IID`; promotion to `latest` is a separate manual job for master/tags.
- Current repository Dockerfile is based on Gradle/JDK plus Android SDK tooling and AWS CLI. Do not infer the exact contents of historical tags `12` or `18` solely from the current Dockerfile; inspect their image metadata or historical commits when diagnosing image-specific failures.

## fastlane-docker publication image

2026-10-12 recovery verified: Fastlane MR6 merged,0.0.9/latest published with Fastlane2.241.0, Huawei1.1.3 and RuStore1.1.0 using frozen Bundler dependencies and provenance opt-out. Direct/bundled plugin loading passed, no release activation warnings; manifest digests match job3218403. Android Gradle18/latest also recovered and digest-verified. Store upload lanes were not executed during validation. See [final DevOps-891 evidence](../../log/2026-10-12-gitlab-devops-891-fastlane-upgrade-legacy-archive.md).

- GitLab project: `sysadmins/devops-tools/mobile/fastlane-docker`, project ID `503`, default branch `master`.
- Local clone: `/home/slnnk/git/fastlane-docker`.
- Registry: `registry.youdo.sg/sysadmins/devops-tools/mobile/fastlane-docker`.
- Verified registry tags include `0.0.3` through `0.0.9`, development branch tags, and `latest`.
- Current release tag `0.0.9` corresponds to the repository tag/HEAD that added Google Play publication.
- Image base and tooling at `0.0.9` source: Ruby `3.4.4-bullseye`, Fastlane `2.241.0`, Huawei plugin `1.1.3`, and RuStore plugin `1.1.0`.

### fastlane-docker image pipeline

- Runner tag: generic `dind`.
- Merge-request pipelines build and push an image tagged with `CI_COMMIT_REF_NAME`; they do not update `latest`.
- Git tag pipelines build the version tag and also push `latest`.
- Build uses the previous `latest` image as Docker layer cache when available.

### Store lanes

- `publish_google` uses `upload_to_play_store` with AAB, production track, 30% staged rollout, and `inProgress` release status. Metadata, images, and screenshots are skipped; Android CI copies release notes into Fastlane metadata before invoking the lane.
- `publish_huawei` uploads an AAB to Huawei AppGallery and submits it for review.
- `publish_rustore` uploads an APK to RuStore with immediate publication mode.
- Credentials and artifact paths are passed through GitLab CI variables. Record variable names and secret-storage locations only; never values.

### Google Play service-account key rotation

- Last checked against official Google documentation: 2026-08-19.
- `fastlane/google.Fastfile` expects the complete JSON service-account credential in `GOOGLE_PLAY_JSON_KEY_DATA`; a Google API key is not a substitute.
- Reuse the existing publishing service account unless its identity or permissions are being deliberately replaced. In Google Cloud IAM, create a new JSON key under the service account's **Keys** tab. The private key can only be downloaded once.
- Confirm that **Google Play Android Developer API** is enabled for the service account's Cloud project.
- In Play Console **Users and permissions**, the service-account email must have access to the target application and **Release to production, exclude devices, and use Play App Signing**. Avoid account-wide Admin access when app-scoped access is sufficient.
- Replace the protected GitLab CI/CD variable `GOOGLE_PLAY_JSON_KEY_DATA` with the complete new JSON document without printing or committing it. Verify that the variable's protection and environment scope still include the ref from which `regress_publish_google` runs.
- Run the normal build and manual `regress_publish_google` job. After successful API authentication and release creation, disable the replaced key, monitor for unexpected failures, and only then delete it. Keep the old key available for rollback until validation completes.
- If key creation is blocked, check the organization policy `iam.disableServiceAccountKeyCreation` and request a narrowly scoped exception or approved authentication alternative; do not work around the policy.

## Autotest pipeline and farm

- GitLab project: `youdo/Test/youdo-android-testing`, project ID `69`.
- Local clone: `/home/slnnk/git/youdo-android-testing`.
- Test image: `registry.youdo.sg/sysadmins/devops-tools/gradle:12`.
- Test runner observed in job `3065145`: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`; this is distinct from the Android product build runner.
- CI reads APK/version metadata from Nexus, selects stand `test` through `test17`, and chooses one of two Selenium/Appium pools by logical `JOB_ID`.
- Selenium Grid and device farm are in Kazan office subnet `192.168.30.0/24`; hub is `192.168.30.30:4444`, Appium hosts are `.147` and `.148`.
- Farm provisioning/configuration belongs to `automation-services/roles/adb_devices` and office inventory/host variables.

## Supporting Android infrastructure repositories

- `/home/slnnk/git/automation-services` — GitLab runners, farm hosts, SDK/AVD/Appium systemd units, ADB preparation, and monitoring integration.
- `/home/slnnk/git/android-exporter` — Prometheus exporter for ADB-connected devices; currently documents CPU and battery metrics.
- `/home/slnnk/git/android-docker-image` — Aerokube/Selenium Android container image tooling. It is adjacent Android infrastructure but is not referenced by the inspected `android-youdo4` or `youdo-android-testing` pipelines.
- `/home/slnnk/git/mstatic-android` — publishes Android static assets: Yandex Object Storage for test and Selectel S3-compatible storage for production.

## Confirmed gaps and risks

- The hotfix Fastlane-version mismatch and missing RuStore producer artifact were corrected locally on branch `DevOps-833-fix-hotfix`; GitLab CI Lint returned valid with no errors/warnings. The correction is not considered production-verified until committed/merged and a real hotfix build plus manual store job is executed.
- Store deployments are manual jobs but the inspected CI does not declare GitLab `environment`/protected-environment controls. Verify project-level protected branches/tags, variable protection, and job permissions before treating manual status alone as an approval boundary.
- Application and test pipelines pin mutable registry tags rather than image digests; rebuilding/replacing a tag can change CI behavior without a consumer repository diff.
- `fastlane-docker` publishes `latest` from any Git tag pipeline; consumers should remain version-pinned and promotion policy should be explicit.
- The local `fastlane-docker` worktree contains an untracked Firebase service-account JSON-like file. Its contents were deliberately not read. Move credentials to an approved secret store/GitLab protected file variable and ensure the file remains ignored and uncommitted.
- Android runner host variables contain access material in plaintext. Values are not recorded here. Rotate exposed credentials and migrate them to Ansible Vault or the approved secret store, then verify runner registration, registry pull, and S3 cache access.
- Nexus test artifacts and report artifacts have previously exposed credentials/tokens or public-read content; retain redaction and access-control work as part of the CI/CD backlog.

## Primary diagnostic entry points

- Product pipeline/config: `android-youdo4/.gitlab-ci.yml`.
- Build image: `gradle/{Dockerfile,.gitlab-ci.yml}` and GitLab Registry project 378.
- Store tooling: `fastlane-docker/{Dockerfile,.gitlab-ci.yml,fastlane/*.Fastfile}` and GitLab Registry project 503.
- Runner host/config: `automation-services/inventories/prod_selectel/hosts`, Android runner host vars, and `roles/gitlab-runner`.
- Test pipeline: `youdo-android-testing/.gitlab-ci.yml` plus job trace/JUnit/report artifacts.
- Device path: Grid state, Appium systemd journal, ADB, UiAutomator2 response, screenshots/page source, and device logcat.

## Change record: DevOps-833 hotfix CI fix

- Date: 2026-08-13.
- Repository/branch: `/home/slnnk/git/android-youdo4`, `DevOps-833-fix-hotfix`.
- Changed file: `.gitlab-ci.yml`.
- Added hotfix `RELEASE_RUSTORE_APK_NAME`, `:youdoapp:assembleReleaseRustore`, copy from `youdoapp/build/outputs/apk/releaseRustore/youdoapp-releaseRustore.apk`, and artifact retention.
- Updated `hotfix_publish_huawei` and `hotfix_publish_rustore` from `fastlane-docker:0.0.6` to `0.0.9`.
- Verification: `git diff --check`, Ruby/Psych YAML parse, static producer/consumer name comparison, and GitLab project 79 CI Lint all passed. No Gradle build was run because the repository's `AGENTS.md` explicitly forbids local builds/Gradle tasks.
- Remaining verification: commit/push the branch, review the MR, then run a real pipeline for branch `hot-fix`; confirm the RuStore APK artifact exists and both manual publication jobs start with image `0.0.9`. Store submission itself is an external side effect and should be invoked only in the approved release window.

## Autotest DEBUG logging constraint — 2026-11-12

The user clarified that Android test logs are emitted only in DEBUG mode. Retain DEBUG for the current autotest pipeline; the agent withdrew the blanket verbosity-reduction proposal because it could remove required test evidence. Historical job3282427trace overflow occurred amid repeated session errors; job3285160completed with a104MBtrace and no trace-limit failure. This does not establish that every future DEBUG run fits the limit. No logging implementation changed and no replacement logging task was added. Any future overflow diagnosis must preserve needed test logs and identify the actual excessive output first; it requires a concrete recurrence/request, not revival of this withdrawn proposal.

## DevOps-921 publication — 2026-11-12

The two .publish_for_tests curl uploads now have --fail on approved task branch DevOps-921-fail-apk-upload-on-http-errors, commit536493b67c. [MR2926](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/merge_requests/2926)Readyto develop, assigneda.solonenko, exactSHA/title/body verified. Local201/500behavior checks and GitLab CI Lintpassed. Pipeline142947running at final check; merge and actual Nexus execution not performed. Until merged the default-branch HTTP-error gap remains. [Evidence and approvals](../../log/2026-11-12-android-farm-devops-921-apk-http-errors.md).

## DevOps-921 integration accepted — 2026-11-12

User merged MR2926and closed DevOps-921. Read-only GET confirms merge8368aafeinto develop and YouTrackFixed. This supersedes the unmerged/default-branch gap stated in the publication snapshot above. Source commit536493b67ccontains both --fail additions; local HTTP checks and CI Lintpassed. Head pipeline142947canceled; no successful full-build or real Nexus-upload validation claimed. User-requested final comment is prepared and awaiting exact-text confirmation.

## DevOps-921 task summary completed — 2026-11-12

After exact-text and field-update approval, created YouTrack comment74-125544and saved MR2926URL in dedicated Merge Requestfield222-47. Both independently read back and verified. Final comment includes behavior only, omits local tests and MR sentence per task-specific user correction. DevOps-921is accepted complete; no additional runtime check is pending.

## Failed-suite download recurrence — 2026-11-12

Job3293803failed November11before tests with TestNGprologXMLparseerror after a27bytedownload from source3293664. Target download occurred during sourceartifactupload18:54:19–21MSK; exact source XML is now HTTP200/2743bytes/validsuite. Early-retry artifact-readiness race is strongly supported, but historical HTTPstatus/body unknown. Existing HTTP/XMLvalidation proposal remains; validation alone does not resolve readiness ordering. [Evidence](../../log/2026-11-12-android-farm-job3293803-failed-suite-download.md). No implementation/retry performed; cancelled preparation proposal stays cancelled.

## DevOps-922 retry-source wait published — 2026-11-12

Approved task branch DevOps-922-wait-for-source-job/commit6c18e1adadds finished_atpolling before failed-suite download (5secondinterval/5minutedeadline), accepts successful/failedsource and handles metadata/artifactHTTPerrors. [MR1165](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/merge_requests/1165)Readyto master, assigneda.solonenko; exactmetadata/SHAverified,10mockHTTP/timecasesandGitLabCILintpassed. Workflowweb/apionly, no automaticpipeline; no merge or realrerun. XMLsyntaxparser not added. [Approvals and evidence](../../log/2026-11-12-android-farm-devops-922-wait-source-job.md).

## DevOps-922 merged — 2026-11-12

User-merged MR1165confirmed as d603c3e5into master20:10MSK; earlier pending-integration state is superseded. DevOps-922stillInProgress; behavior-only comment draft prepared on request, MRfieldempty, no trackerwriteperformed. No real retry-suite run claimed.

## DevOps-922 comment published — 2026-11-12

User-approved revised summary created as comment74-125545and exact text independently verified. Includes problem and fix, no local-check details or MRintegration sentence. Issue stillInProgress, dedicatedMRfieldempty at readback; no state/fieldmutation. MR1165remains merged as recorded above.

## DevOps-922 MR attachment corrected — 2026-11-12

After user correction, filled dedicated Merge Requestfield222-47with MR1165URLand independently verified exact value. Comment74-125545unchanged. This supersedes earlier empty-field status/proposal; agent summary follow-up complete. Issue-state unchanged (lastobservedInProgress), no taskclosure claimed.

## Store release-control proposal cancelled — 2026-11-12

The user rejected the optional store-job environment protection and image-digest pinning proposal as unnecessary. Its central TODO is closed as cancelled, not implemented. Earlier protection/digest observations remain historical audit facts, not active remediation requests; do not recreate the proposal without a new user request. DevOps-833 remains complete. No code/settings/release changes performed. [Decision evidence](../../log/2026-11-12-android-farm-backlog-relevance-audit.md#store-ci-improvement-proposal-cancelled--2026-11-12).
