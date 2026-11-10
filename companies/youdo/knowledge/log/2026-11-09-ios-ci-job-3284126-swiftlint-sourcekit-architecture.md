---
system: ios-ci
status: verified
checked: 2026-11-09
tags: [swiftlint, sourcekit, architecture]
---
# iOS job 3284126: Intel SwiftLint cannot load ARM SourceKit

## Task
Tracked under [DevOps-911](https://youtrack.youdo.com/youtrack/issue/DevOps-911), as specified by the user on 2026-11-09.

Diagnose [Unit tests job 3284126](https://gitlab.youdo.sg/team-youdo-ios/YouDoApp/-/jobs/3284126), then connect to the runner for verification. The user subsequently authorized ARM SwiftLint installation and explicitly requested a Homebrew update.

## Context
Runner `idcn-10`, GitLab runner ID 93, SSH `iosdev@192.168.30.144`; pipeline 142560, MR 3283, SHA `7f13df1a01915d4002c504f9ffd26c1b608c653e`. Trace and metadata saved in `~/ai-data/ios-ci/3284126/`. Related earlier failure: [Ruby Prism architecture mismatch](2026-11-09-ios-ci-job-3283802-ruby-prism-architecture.md). This is a separate native binary from the repaired Ruby extension.

## Actions
Read GitLab job metadata and trace, inspected the existing local checkout without changes, then used read-only SSH commands to inspect Xcode, SwiftLint, SourceKit and the Homebrew installation receipt. Reproduced dynamic loading with the existing x86_64 Ruby and `Fiddle.dlopen`; no build, lint run, installation or CI retry.

## Findings
- Job failed during `build-for-testing` in the `YDFoundation` SwiftLint script. `SourceKittenFramework/library_wrapper.swift:58` reports `Fatal error: Loading sourcekitdInProc.framework/Versions/A/sourcekitdInProc failed`; SwiftLint then exits with `Illegal instruction: 4`. Tests and JUnit generation were not reached.
- Selected developer directory: `/Applications/Xcode.app/Contents/Developer`; Xcode 27.2 build 27B52; Swift 6.4.2; host arm64.
- `/usr/local/bin/swiftlint` links to `/usr/local/Cellar/swiftlint/0.63.2/bin/swiftlint`. Version 0.63.2, Mach-O x86_64. Homebrew receipt confirms an x86_64 bottle. `/opt/homebrew/bin/swiftlint` does not exist.
- `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/sourcekitdInProc.framework/Versions/A/sourcekitdInProc` exists. Both `file` and `lipo -archs` report only arm64.
- Loading that exact library in the existing x86_64 Ruby reproduces `mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')`. This confirms the architecture mismatch behind the SourceKit loader failure; the library is present.
- Proposed remedy: provide a native arm64 SwiftLint and ensure the CI script resolves that binary. No installation command or PATH change has been executed. Exact installation route requires review before any remote mutation.

## Changes
ARM Homebrew updated from 5.1.14 to 7.0.13 and ARM SwiftLint 0.65.1 installed under `/opt/homebrew`. No repository or GitLab changes.

## Status and risks
DevOps-911 was closed by the user on 2026-11-09 after the job succeeded. Repairs and scoped runner checks are complete; no further task work remains. No additional remote verification or tracker mutation was performed for this closure notification. Earlier pending states below are historical and superseded by the completion and closure records.

Repair complete and verified on the runner; see the follow-up below. All task SSH commands exited; no background operations remain. No CI retry or full project build was performed. CLT/pkgconf follow-up completed after the approved plan below; central TODO entry is closed.

## Approved installation and Homebrew update
The user requested ARM SwiftLint installation with `Установи`, paused to discuss the Homebrew failure, then requested `Обнови homebrew`. Earlier diagnosis-only and proposed-remedy statements above are historical.

Initial Homebrew 5.1.14 commands `brew install swiftlint` and `brew install --force-bottle swiftlint` both failed with `unknown or unsupported macOS version: :dunno`. No portable release installation was executed.

Ran `/usr/bin/arch -arm64 /opt/homebrew/bin/brew update`. Homebrew itself updated to 7.0.13, downloaded its own portable Ruby 4.0.9 and now recognizes macOS 27 / `arm64_golden_gate`. The update command exited 1 during a subsequent pkgconf reinstallation because installed Command Line Tools are version `26.0.0.0.1.1757719676`, too old for this macOS. No Command Line Tools update/removal or unrelated package upgrade was performed; pkgconf reinstallation completion is not claimed.

Then ran `HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 /usr/bin/arch -arm64 /opt/homebrew/bin/brew install swiftlint`. It poured `swiftlint--0.65.1.arm64_golden_gate.bottle.1.tar.gz` successfully, exit 0. The old Intel SwiftLint remains installed separately. The existing project script already prepends `/opt/homebrew/bin:/usr/local/bin` to PATH, so no repository edit is needed.

Final verification with that exact PATH:
- `command -v swiftlint`: `/opt/homebrew/bin/swiftlint`.
- `swiftlint version`: `0.65.1`.
- `file /opt/homebrew/Cellar/swiftlint/0.65.1/bin/swiftlint`: Mach-O arm64.
- `brew --version`: Homebrew 7.0.13.
- Piped a small valid Swift struct into `swiftlint lint --use-stdin --no-cache --reporter xcode` from `/tmp`: `Done linting! Found 0 violations, 0 serious in 1 file.`, exit 0. The previous SourceKit loader crash did not recur.

SwiftLint version increased from 0.63.2 to 0.65.1, so full-project lint results may change. Full CI results remain unverified. Homebrew 7 also warns that existing tap `xcodesorg/made` is ignored until explicitly trusted; no trust changes were made. Follow-up maintenance is now scoped to DevOps-911; exact CLT installation is proposed below and has not been executed.

## DevOps-911: CLT and pkgconf plan
User clarified that these job repairs belong to DevOps-911 and asked for an immediate CLT/pkgconf remediation proposal. Read-only `softwareupdate --list` offers exactly `Command Line Tools for Xcode 27.2-27.2`, title `Command Line Tools for Xcode 27.2`, size `521120KiB`, recommended. Installed receipt remains CLT 26. Active developer directory remains the full Xcode application.

`brew list --versions pkgconf` reports 2.5.1; `/opt/homebrew/bin/pkg-config` and `pkgconf` both link into that keg, and `pkg-config --version` succeeds. Existing pkgconf is functional; the post-update rebuild is blocked by CLT age, not a missing executable.

Proposed order: install only the named CLT 27.2 update through `sudo -n /usr/sbin/softwareupdate --install "Command Line Tools for Xcode 27.2-27.2"`; verify receipt and unchanged Xcode selection; complete `brew update` and, if its migration has not already repaired pkgconf, reinstall only pkgconf. Suppress automatic unrelated dependent upgrades for a scoped reinstall. Verify pkgconf version and system SDK lookup, Homebrew update exit status and SwiftLint stdin lint. A complete CI retry remains a separate external action. No OS upgrade, tool-directory deletion or bulk package upgrade is included. No CLT/pkgconf mutation was executed in that planning step. The approved execution below supersedes this pending status; central TODO now marks it complete.

## DevOps-911: approved CLT and pkgconf completion
The user approved the concrete CLT27.2 installation and follow-up Homebrew/pkgconf plan with `Сделай`. Executed `sudo -n /usr/sbin/softwareupdate --install "Command Line Tools for Xcode 27.2-27.2"` over SSH. Download and installation completed, exit 0, without a reboot. Receipt `com.apple.pkg.CLTools_Executables` now reports `27.2.0.0.1792721180`; CLT clang is 21.0.0 targeting arm64-darwin27.2.0. `xcode-select -p` still selects `/Applications/Xcode.app/Contents/Developer`; Xcode27.2/27B52 is unchanged.

Executed `HOMEBREW_NO_INSTALL_CLEANUP=1 HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 /opt/homebrew/bin/brew update --quiet`, exit 0. Homebrew automatically reinstalled pkgconf3.0.10 from source to repair the macOS version mismatch. Configure, make and make install all succeeded; no separate reinstall was needed. This completes the previously failing update step. No bulk package upgrades, CommandLineTools directory removal, OS upgrade, tap trust change or CI retry.

Final verification, exit 0:
- Homebrew7.0.13; pkgconf3.0.10; SwiftLint0.65.1.
- `pkg-config` resolves to `/opt/homebrew/bin/pkg-config` and reports3.0.10.
- `pkgconf --dump-personality` reports Homebrew macOS27 search paths and `/Library/Developer/CommandLineTools/SDKs/MacOSX27.sdk/usr/include`.
- `brew test pkgconf` passed validation/version/library/flags checks against a test module, compiled and ran a C client, and resolved `libcurl` libraries.
- The same CI PATH resolves `/opt/homebrew/bin/swiftlint`; stdin lint of a small Swift struct passed with0violations. No SourceKit crash.

`brew test` automatically enabled Homebrew developer mode and installed its test/developer Ruby dependencies under `/opt/homebrew/Library/Homebrew/vendor/bundle`; these are separate from CI rbenv Ruby3.2.2. Restored developer mode with `brew developer off` and verified `brew developer state`: disabled. All task SSH commands finished; no background operations remain.

CLT/pkgconf repair and scoped runner verification are complete. Full CI/unit test results remain unverified because no job retry was authorized or performed. The earlier optional tap-trust warning is unchanged and outside this repair. The task-affected central backlog entry is closed; no additional implementation is commissioned.

## DevOps-911 comment publication
At the user's explicit request, added the reviewed repair summary to DevOps-911 as comment `74-125376`. The user requested removal of the user-confirmation sentence; it was omitted. The issue had no existing comments. POST succeeded and a subsequent GET verified the exact stored text. Issue status and other fields were not changed. Local publication receipt is `~/ai-data/ios-ci/3284126/youtrack-comment.json`. All commands completed; no background work remains.

## Portable lesson
none
