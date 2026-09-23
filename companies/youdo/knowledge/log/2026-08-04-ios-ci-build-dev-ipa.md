---
system: ios-ci
status: verified
checked: 2026-08-04
tags: [ios, fastlane, gitlab-ci, nexus, ipa, build_dev]
---
# YouDo iOS: IPA artifacts for `build_dev`

## Task

Make the development build publish IPA files instead of ZIP archives of `.app`.

## Context

- Date: 2026-08-04
- Repository: `/home/slnnk/git/YouDoApp`
- Context: Fastlane lane `build_dev`, GitLab CI job `Build development`, Nexus raw repository `ios`.

## Findings: task and reason

The development build must be published as IPA instead of ZIP with `.app`. `build_beta(method: "development")` already produced `build/YDMainApp.ipa` and `build/YDSettingsApp.ipa`, but `upload_app_to_storage` unpacked the IPA and re-archived the `.app` into a ZIP.

## Changes

- `fastlane/Fastfile`: removed the IPA unpacking and `.app.zip` packaging; the lane uploads the ready IPA files directly.
- Nexus objects: `gitlab_youdo.ipa` and `gitlab_youdo_settings.ipa` instead of the ZIP files of the same name.
- `.gitlab-ci.yml`: development artifacts replaced with `build/YDMainApp.ipa` and `build/YDSettingsApp.ipa`; `build/version.txt` kept.

## Actions: checks

- `ruby -c fastlane/Fastfile` — `Syntax OK`.
- Parsing `.gitlab-ci.yml` through Ruby YAML — successful.
- `git diff --check` — successful.

## Open items: risks and next step

- The full iOS build was not run locally; the `Build development` job must be checked on the macOS runner with provisioning profiles.
- Nexus consumers must switch to the new URLs with the `.ipa` extension.
- Access to Nexus is done through the CI variable `NEXUS_CREDS`; the secret value was not recorded.

## Portable lesson

none
