---
system: android-farm
status: verified
checked: 2026-08-19
tags: [android, gitlab-ci, gradle, fastlane, google-play, huawei, rustore, nexus, runner]
---
# YouDo Android: infrastructure and CI/CD map

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

- GitLab project: `sysadmins/devops-tools/mobile/fastlane-docker`, project ID `503`, default branch `master`.
- Local clone: `/home/slnnk/git/fastlane-docker`.
- Registry: `registry.youdo.sg/sysadmins/devops-tools/mobile/fastlane-docker`.
- Verified registry tags include `0.0.3` through `0.0.9`, development branch tags, and `latest`.
- Current release tag `0.0.9` corresponds to the repository tag/HEAD that added Google Play publication.
- Image base and tooling at `0.0.9` source: Ruby `3.4.4-bullseye`, Fastlane `2.227.2`, Huawei plugin `1.0.30`, and RuStore plugin `1.0.6`.

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
