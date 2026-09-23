---
system: ios-ci
status: verified
checked: 2026-06-25
tags: [ios, fastlane, swiftlint, xcodebuild, unit-tests, IOS-4990]
---
# YouDoApp IOS-4990 SwiftLint failure in Unit tests

## Task

Find why the GitLab/Fastlane `Unit tests` job of YouDoApp branch `IOS-4990` fails in the SwiftLint build phase and make the raw SwiftLint diagnostics visible in CI.

## Context

Date: 2026-06-25
Project/repo: /home/slnnk/git/YouDoApp
Branch: IOS-4990
Context: GitLab/Fastlane Unit tests job failed during `scan(build_for_testing: true)` with Xcode exit 65. Local full CI log was provided as repo-root file `log`.

## Findings

- Failure point in `log`: `PhaseScriptExecution SwiftLint` in target `YDFoundation` from project `YDMainApp`.
- Script used by generated project: `YDFoundation/Main/Scripts/SwiftLint.sh`.
- Script runs `swiftlint lint --reporter xcode` if `swiftlint` is installed.
- The provided fastlane/xcpretty log does not include the actual SwiftLint diagnostic lines, only the failed build phase summary.
- Local environment has no `swiftlint` and no `xcodebuild`, so full reproduction was not possible here.

## Actions

- Checked branch state and recent commits. Branch: `IOS-4990`; recent commits include multiple lint-fix commits.
- Compared branch against `origin/develop` and searched added Swift lines for likely error-level rules: `URL(string:)`, `print`, `Date()`, `TimeZone.current`, `UIWebView`, long lines, long identifiers.
- Ran `git diff --check origin/develop` and found trailing whitespace in added lines.
- Removed trailing whitespace in affected files:
  - `YDFoundation/Main/Sources/YDAPIClient/Info/ResultStatusCode.swift`
  - `YDFoundation/Main/Sources/YDUICommon/Modules/ShiftSupplyList/ViewModel/ShiftSupplyListViewModel.swift`
  - `YDFoundation/Main/Sources/YDUICommon/Modules/ShiftSupplyWebView/View/ShiftSupplyWebViewController.swift`
  - `YDFoundation/Main/Sources/YDUICommon/Modules/ShiftSupplyWebView/View/ShiftSupplyWebViewOutput.swift`
  - `YDFoundation/Main/Sources/YDUICommon/Modules/ShiftSupplyWebView/ViewModel/ShiftSupplyWebViewModel.swift`
  - `YDFoundation/Main/Sources/YDUICommon/Modules/TasksList/Interactor/TasksListInteractor.swift`
  - `YDFoundation/Main/Sources/YDUIKit/Cells/ReferenceLinkCell/ReferenceLinkCell.swift`
  - `YDFoundation/Main/Sources/YDUIKit/Views/TumblerControl/TumblerControl.swift`
  - `YDMainApp/Main/Modules/YDAllTasksScenes/Modules/ShiftSupplyTask/ShiftSupplyOfferOnboarding/Presenter/ShiftSupplyOfferOnboardingModelsBuilder/ShiftSupplyOfferOnboardingModelsBuilder.swift`
  - `YDMainApp/Main/Modules/YDAllTasksScenes/Modules/ShiftSupplyTask/ViewModel/ShiftSupplyTaskViewModel.swift`

## Verification

- `git diff --check`: clean.
- `git diff origin/develop --check`: clean after edits.
- No local SwiftLint/Xcode verification due missing tools in this environment.

## Open items

- Rerun CI Unit tests job or run SwiftLint on macOS CI host to confirm.
- If job still fails, retrieve raw xcodebuild/SwiftLint output because current formatted log hides the exact SwiftLint diagnostics.

## Changes: Fastlane log output

Added `XCODEBUILD_LOG_PATH = 'artifacts/buildlogs'` and helper `print_latest_xcodebuild_log(lines: 500)` to `fastlane/Fastfile`.

Updated Unit tests lane:
- `scan(build_for_testing: true)` is now wrapped in `begin/rescue`.
- Both build-for-testing and test-without-building `scan` calls use `buildlog_path: XCODEBUILD_LOG_PATH`.
- On `scan` failure, Fastlane prints the last 500 lines of the newest raw xcodebuild log before failing the lane.

Verification:
- `ruby -c fastlane/Fastfile`: Syntax OK.
- `git diff --check fastlane/Fastfile`: clean.

## Findings and changes: log2 analysis

User provided second CI output as repo-root `log2`.

Findings from `log2`:
- Fastlane raw log printing works and printed `/artifacts/buildlogs/YDMainApp-YDMainApp.log`.
- The printed tail includes `Done linting! Found 128 violations, 1 serious in 3052 files.`
- The single serious SwiftLint diagnostic is not visible because only the last 500 lines were printed; the serious violation likely occurred earlier in the 3030-file lint output.

Action:
- Updated `print_latest_xcodebuild_log` in `fastlane/Fastfile` to scan the full raw xcodebuild log and print all SwiftLint diagnostic lines matching `.swift:<line>:<column>: warning/error`, plus the `Done linting!` summary, before printing the tail.

Verification:
- `ruby -c fastlane/Fastfile`: Syntax OK.
- `git diff --check fastlane/Fastfile`: clean.

## Portable lesson

none
