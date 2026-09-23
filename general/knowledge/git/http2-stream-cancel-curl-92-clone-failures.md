---
system: git
status: verified
checked: 2026-08-31
tags: [git, github, http2, curl, submodule, swiftpm, ci]
---
# Git clone/fetch from GitHub dies with "curl 92 HTTP/2 stream ... CANCEL"

## Symptom

Intermittent failures while cloning or fetching large repositories or submodules over HTTPS,
typically inside CI dependency resolution (Swift Package Manager, CocoaPods, Go modules):

```
error: RPC failed; curl 92 HTTP/2 stream 5 was not closed cleanly: CANCEL (err 8)
error: 8 bytes of body are still expected
fetch-pack: unexpected disconnect while reading sideband packet
fatal: early EOF
fatal: fetch-pack: invalid index-pack output
```

A retry usually succeeds; DNS, TCP/443 and `curl -I https://github.com` all look healthy at the
time of the check, and the same clone works 5/5 when repeated by hand.

## Cause

The HTTP/2 stream carrying the smart-HTTP pack transfer is cancelled mid-download. It is a transport
interruption between the client (libcurl with nghttp2 negotiating HTTP/2 by default) and GitHub or an
intermediate proxy/firewall, not a repository or credential problem. Observed with Apple Git 2.50.1,
curl 8.7.1, nghttp2 1.68.0 on macOS; also seen on Linux.

## Fix

Force Git to use HTTP/1.1 for the affected user or job:

```bash
# for the CI user
git config --global http.version HTTP/1.1
# or for a single command
git -c http.version=HTTP/1.1 clone --depth 1 https://github.com/org/repo.git
```

For tools that spawn git themselves (SwiftPM, xcodebuild), the global setting for the runner user is
what takes effect. Add a retry around the dependency-resolution step and keep a local or shared
dependency cache so a single cancelled stream does not fail the whole job.

## Limits

- This only removes the HTTP/2 stream layer; if the underlying path drops TCP connections the
  HTTP/1.1 transfer will still fail (but usually with clearer errors).
- Changing the runner user's global git config affects every job on that runner; agree it with the
  team or scope it to the job via `-c`/`GIT_CONFIG_*` environment variables.
- Verify first with a quick A/B: five clones with default settings vs. five with
  `-c http.version=HTTP/1.1`. If both succeed, the fault is intermittent and the fix is a mitigation,
  not a proof of cause.
