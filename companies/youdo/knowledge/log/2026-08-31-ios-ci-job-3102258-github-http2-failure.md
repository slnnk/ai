---
system: ios-ci
status: verified
checked: 2026-08-31
tags: [ios, gitlab-ci, xcodebuild, swiftpm, git, github, http2, realm, job-3102258]
---
# YouDo iOS CI: job 3102258

## Task

Determine why the `Unit tests` job `3102258` of the iOS project failed and whether the failure belongs to the MR or to the infrastructure.

## Context

- Check date: 2026-08-31
- Project: `team-youdo-ios/YouDoApp`, GitLab project ID `65`
- Pipeline: `137687` (`!3248`, commit `e002df08`)
- Job: `3102258`, `Unit tests`, runner `idcn-10`, tag `Xcode16.0`
- Runner host: `iosdev@192.168.30.144`, hostname `idcn-10.local`

## Findings: summary

The job failed before the unit tests started: `xcodebuild` could not resolve the Swift Package Manager dependencies. During the checkout of `realm-core`, Git lost the HTTP/2 connection to GitHub several times while cloning submodules:

- `external/catch` -> `https://github.com/catchorg/Catch2.git`;
- `tools/vcpkg/ports` -> `https://github.com/microsoft/vcpkg.git`.

Key errors: `curl 92 HTTP/2 stream ... CANCEL`, `early EOF`, `invalid index-pack output`. After the retries `vcpkg` was not cloned, so `xcodebuild` finished with `Could not resolve package dependencies` and Fastlane showed the secondary error `Ошибка генерации проекта`.

This is an infrastructure/network failure while downloading from GitHub, not a test failure and not a defect found in the MR.

## Findings: runner checks

- Host uptime: 19 days; load average about `2.29 1.89 2.21`.
- macOS `26.4.1`, Apple Git `2.50.1`, curl `8.7.1`, nghttp2 `1.68.0`.
- The Data volume is 90% used, but about 22 GiB is available; there are no signs of ENOSPC in the trace.
- Proxy is off; there are no global/system Git HTTP overrides.
- `en0` showed no input/output errors at the time of the check.
- After the failure GitHub answered over HTTP/2 (`HTTP/2 301`) for both repository URLs.
- In the preserved `realm-core` checkout the Catch2 submodule was present, while `tools/vcpkg/ports` remained uninitialised.

## Open items: safe recovery and prevention

First action: retry the job, since access to GitHub has been restored. If the error repeats, check bypassing the problematic HTTP/2 path with `git config --global http.version HTTP/1.1` for the runner user, or set the configuration only in the CI job; the change requires separate approval. Retries around package resolution and a local/shared cache of SwiftPM dependencies are also useful.

Build checkout location: `/Users/iosdev/builds/6gfbuVYj/0/team-youdo-ios/YouDoApp`. Logs are available in the GitLab job trace; the JUnit artifact was not produced because the tests did not start.

## Portable lesson

- `~/ai/general/knowledge/git/http2-stream-cancel-curl-92-clone-failures.md`
