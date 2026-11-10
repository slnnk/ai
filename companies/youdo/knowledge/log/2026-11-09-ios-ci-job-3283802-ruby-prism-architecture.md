---
system: ios-ci
status: verified
checked: 2026-11-09
tags: [ruby, runner, architecture]
---
# iOS job 3283802: Ruby Prism native architecture mismatch

## Task
Tracked under [DevOps-911](https://youtrack.youdo.com/youtrack/issue/DevOps-911), as specified by the user on 2026-11-09 for these runner/job repairs.

Explain the failure of [Unit tests job 3283802](https://gitlab.youdo.sg/team-youdo-ios/YouDoApp/-/jobs/3283802). Diagnosis only; no remediation requested.

## Context
Runner `idcn-10` (ID 93), pipeline 142560, MR 3283, commit `7f13df1a01915d4002c504f9ffd26c1b608c653e`. Job failed on 2026-11-09 at 16:19 MSK after 28 seconds. Local checkout `/home/slnnk/git/YouDoApp` was inspected read-only; its cached HEAD `abc9cbaa411516f335ec5e5e0997a5982105507f` differs and the job SHA is absent locally. No remote fetch or source-code diagnosis was necessary for the explicit runtime failure.

## Actions
Read job metadata and full trace through GitLab GET. Evidence saved under `~/ai-data/ios-ci/3283802/`. No runner commands, CI retries, repository edits or external mutations.

## Findings
`rbenv global 3.2.2` is followed by `gem install bundler`. RubyGems documentation generation loads RDoc 8.1.0, RBS 4.1.3 and Prism 2.1.0. Loading `prism.bundle` fails with `mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')`. The Ruby process expects x86_64, while this native extension is arm64; how this mixed installation arose is unverified. The runner executable reports arm64; this does not establish the architecture of all subprocesses. `Successfully installed bundler-4.0.24` appears, but the command exits 1 due to the documentation hook. Build/test execution is not reached; the missing JUnit artifact is secondary.

## Changes
Diagnostic note and local evidence only.

## Status and risks
Runner repair completed on 2026-11-09 after explicit user approval. Prism 2.1.0 is now x86_64 and loads in the existing x86_64 Ruby 3.2.2. The original `gem install bundler` command passes, including documentation generation. The user subsequently reported that the job now works. This is user-reported recovery; the final CI status and full test results have not been independently verified. The agent performed no job retry. Earlier diagnosis-only status below is historical and superseded by the repair section. No background work remains. No additional implementation has been commissioned or added to the central backlog.

## Follow-up: Xcode update and read-only runner checks
The user reported a developer updated Xcode and asked for cause and repair guidance. Read-only SSH to `iosdev@192.168.30.144` confirmed:

- Host architecture `arm64`; Ruby binary is Mach-O x86_64, reporting Ruby 3.2.2 / `x86_64-darwin24`.
- Prism native bundle is Mach-O arm64. Ruby mtime: 2025-10-02 13:54:23; Prism mtime: 2026-11-09 16:07:52; Xcode.app mtime: 2026-11-09 14:40:58 (runner-local timestamps, not an installation audit trail).
- Selected Xcode 27.2 build 27B52, developer directory `/Applications/Xcode.app/Contents/Developer`.
- Prism Makefile has `CC = clang`, empty `ARCH_FLAG`, and `arch = x86_64-darwin24`. Its compiler commands omit `-arch`.
- Current `/usr/bin/clang -dumpmachine` returns `arm64-apple-darwin27.2.0`; explicit `-arch x86_64 -dumpmachine` returns `x86_64-apple-darwin27.2.0`.

The confirmed mechanism is an Intel Ruby loading an ARM extension built without an explicit architecture. The Xcode update plausibly exposed the existing configuration weakness when Prism was rebuilt; historical compiler selection and the installer command are unverified. An Xcode update alone is not evidence that existing native binaries were converted.

Proposed minimal repair, not executed: under the runner account and Ruby 3.2.2, run `ARCHFLAGS="-arch x86_64" gem pristine prism --version 2.1.0`, then check loading with `ruby -rprism -e 'puts Prism::VERSION'` and repeat the original Bundler command. RubyGems documents native extension rebuilding in [gem pristine](https://guides.rubygems.org/command-reference/). Success remains unverified; further incompatibilities may appear. CI prevention can explicitly set the native extension architecture while this Ruby remains x86_64. A full move to ARM Ruby requires a separate reviewed migration with fresh native gems. `gem install bundler --no-document` only bypasses the failing documentation path.

No repair, repository change, CI retry or other external mutation was performed. Guidance task complete; no newly commissioned implementation or backlog action. All SSH calls completed; no background work remains.

## Approved repair and verification
The user approved the proposed repair with `Сделай` and additionally reported a macOS update. `sw_vers` confirms macOS 27.2 build 26B123. This complements the observed mismatch between the old Ruby `x86_64-darwin24` and current toolchain `darwin27.2.0`; the precise update/installation history remains unverified.

A backup of the original native bundle was saved on the runner at `/tmp/prism-2.1.0-before-3283802-20261109163925.bundle`. The first attempt with `ARCHFLAGS="-arch x86_64" gem pristine prism --version 2.1.0` completed rebuilding but still produced arm64; the Ruby load check failed and prevented the following Bundler command. Do not treat ARCHFLAGS alone as a working fix for this Ruby installation.

The successful scoped repair used the existing rbenv Ruby 3.2.2 bin directory first in PATH, without changing the global Ruby selection:

```bash
export PATH="/Users/iosdev/.rbenv/versions/3.2.2/bin:$PATH"
export RBENV_VERSION=3.2.2
gem install prism --version 2.1.0 --platform ruby --no-document -- --with-cflags='-arch x86_64' --with-ldflags='-arch x86_64'
file /Users/iosdev/.rbenv/versions/3.2.2/lib/ruby/gems/3.2.0/gems/prism-2.1.0/lib/prism/prism.bundle
ruby -rprism -e 'puts "Prism loaded: #{Prism::VERSION}"'
gem install bundler
ruby -rrdoc -rrbs -rprism -e 'puts "Documentation dependencies loaded successfully"'
bundle --version
```

Results: native bundle `Mach-O 64-bit bundle x86_64`; Prism loaded `2.1.0`; Bundler `4.0.24` installed and documentation generated without error; RDoc/RBS/Prism load check passed; shell exit 0. There was no ARCHFLAGS environment variable in the final verification command, so the original Bundler installation succeeds without a persistent architecture override. Explicit build arguments are stored by RubyGems for this gem; other future native gem installations are outside the verified scope. No repository changes, persistent global environment overrides, CI retries or service restarts. All task SSH sessions finished.

## User confirmation
On 2026-11-09 the user reported `job теперь работает` after the runner repair. Record this as user-reported job recovery, without inferring a final successful pipeline or completed test suite. No further action was requested; no additional remote checks or mutations were performed. The repair is complete and no task backlog action remains.

## Portable lesson
none
