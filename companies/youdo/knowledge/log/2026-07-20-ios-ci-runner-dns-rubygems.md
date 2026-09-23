---
system: ios-ci
status: verified
checked: 2026-07-20
tags: [ios, macos, runner, dns, rubygems, bundler, github, http2, firebase, oauth, fastlane, disk]
---
# iOS runner DNS instability for RubyGems

## Task

Diagnose intermittent Bundler `getaddrinfo` failures on the iOS GitLab runner `idcn-10.local`, then the follow-up GitHub HTTP/2 clone failures, Firebase App Distribution OAuth timeouts and the runner disk exhaustion that appeared during the same two days.

## Context

- Date: 2026-07-20
- Host: `iosdev@192.168.50.10`, hostname `idcn-10.local`
- Context: YouDoApp iOS/macOS runner. Bundler intermittently fails with `Unable to download data from https://rubygems.org/ - SocketError: Failed to open TCP connection to rubygems.org:443 (getaddrinfo: nodename nor servname provided, or not known)`.

## Actions: checks performed

Commands were run over SSH from the local Codex session.

- `scutil --dns`: active resolver for Ethernet is `192.168.50.1`, search domain `youdo.loc`, interface `en0`.
- `/etc/resolv.conf`: generated file, also points to `nameserver 192.168.50.1`.
- `ifconfig en0`: `192.168.50.10/24`, active `1000baseT <full-duplex>`.
- `route -n get default`: default gateway `192.168.50.1` via `en0`.
- `ping -c 20 -i 0.2 192.168.50.1`: 0% packet loss, RTT avg about 0.52 ms.
- One-shot `dscacheutil -q host -a name rubygems.org`, `nslookup rubygems.org`, `nc -vz -G 5 rubygems.org 443`, and `curl -Iv --connect-timeout 8 https://rubygems.org/specs.4.8.gz` succeeded.

## Findings

- Repeated direct DNS queries to the configured resolver are unstable:
  - `dig +tries=1 +time=1 @192.168.50.1 rubygems.org A +short`: 27 failures out of 60 in one run.
  - Repeat comparison: `192.168.50.1` had 8 failures out of 30.
- External DNS resolvers through the same gateway were stable in the same test:
  - `dig +tries=1 +time=1 @1.1.1.1 rubygems.org A +short`: 0 failures out of 30.
  - `dig +tries=1 +time=1 @8.8.8.8 rubygems.org A +short`: 0 failures out of 30.
- DNS-over-TCP to `192.168.50.1` also had failures: `dig +tcp +tries=1 +time=2 @192.168.50.1 rubygems.org A +short`: 4 failures out of 30.
- TCP/443 to external endpoints remained stable while DNS to `192.168.50.1` was failing:
  - `rubygems.org`, `github.com`, `google.com`, `api.github.com`: all `nc -vz -G 3 <host> 443` succeeded.

## Conclusion

The runner itself has working Ethernet link and external TCP connectivity. The intermittent Bundler error is consistent with DNS lookup failures. Evidence points to the configured local DNS resolver or DNS forwarding on `192.168.50.1`, not to RubyGems availability or generic internet outage from the runner.

## Open items: recommended next steps

- Check DNS service / router / forwarder on `192.168.50.1` for overload, rate limits, upstream resolver errors, or packet filtering.
- As a mitigation for the runner, consider temporarily setting Ethernet DNS servers to stable external resolvers, for example `1.1.1.1 8.8.8.8`, if this does not break internal `youdo.loc` resolution.
- If internal domains are required, configure a stable local caching resolver or split DNS instead of relying solely on the unstable `192.168.50.1` forwarder.

## Follow-up: expected DNS 10.16.20.3

User clarified that the runner was expected to use DNS `10.16.20.3`.

Additional checks on 2026-07-20:

- `networksetup -getdnsservers Ethernet` currently returns only `192.168.50.1`.
- `ipconfig getpacket en0` DHCP ACK advertises DNS `{192.168.60.10, 192.168.50.1}` and domain `youdo.loc`; it does not advertise `10.16.20.3`.
- `scutil --dns` still shows active resolver `192.168.50.1` for Ethernet.
- `dig @10.16.20.3 rubygems.org A +short` returns `10.255.0.47`.
- Repeated `dig @10.16.20.3 rubygems.org A +short`: 0 failures out of 30.
- `ping 10.16.20.3`: 10/10 replies, avg about 4.74 ms.

Updated conclusion: the runner is misconfigured or has lost the intended DNS setting. Correct DNS appears to be `10.16.20.3`; current active DNS is `192.168.50.1`, which is unstable and resolves `rubygems.org` to public Fastly IPs instead of the corporate/internal `10.255.0.47` endpoint.

Recommended remediation: set Ethernet DNS on `idcn-10.local` to `10.16.20.3` and verify `scutil --dns`, then rerun Bundler. Also check why DHCP/manual network profile no longer applies the expected DNS.

## Remediation applied

On 2026-07-20, configured persistent DNS for macOS network service `Ethernet`:

```bash
sudo networksetup -setdnsservers Ethernet 10.16.20.3
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Verification after change:

- `networksetup -getdnsservers Ethernet`: `10.16.20.3`.
- `scutil --dns`: resolver #1 and scoped `en0` resolver use `10.16.20.3`, search domain `youdo.loc`.
- `dscacheutil -q host -a name rubygems.org`: `10.255.0.47`.
- `dig rubygems.org A +short`: `10.255.0.47`.
- `curl -Iv --connect-timeout 8 https://rubygems.org/specs.4.8.gz`: resolved `rubygems.org` to `10.255.0.47`, connected on TCP/443, TLS verification OK.

Note: `networksetup -setdnsservers` writes the DNS setting to the macOS network service configuration, so it should persist across reboot. If it resets again, check DHCP/profile/MDM scripts or network configuration management that may overwrite Ethernet DNS.

## Follow-up: GitHub submodule clone HTTP/2 failures

User reported a later SwiftPM/Git submodule failure while cloning Realm Core submodules:

- `external/catch` from `https://github.com/catchorg/Catch2.git`
- `tools/vcpkg/ports` from `https://github.com/microsoft/vcpkg.git`
- Error class: `RPC failed; curl 92 HTTP/2 stream ... was not closed cleanly: CANCEL`, `unexpected disconnect while reading sideband packet`, `early EOF`, `invalid index-pack output`.

Additional checks on 2026-07-20 after DNS remediation:

- `scutil --dns`: active DNS remains `10.16.20.3`.
- `github.com` resolves to `140.82.121.4`; `codeload.github.com` resolves to `140.82.121.9`.
- `nc`/`curl -I` to `github.com` and `codeload.github.com` succeeded.
- `objects.githubusercontent.com` showed one initial TCP/SSL timeout, then later repeated TCP check had 0 failures out of 20.
- `git config --global --get-regexp '^(http|url)\.'`: no relevant global Git HTTP config was set.
- Git version: Apple Git `2.50.1`, libcurl `8.7.1`, curl uses nghttp2 and negotiates HTTP/2 by default.
- Test `git clone --depth 1 https://github.com/catchorg/Catch2.git`: 5/5 successful with default HTTP/2.
- Test `git -c http.version=HTTP/1.1 clone --depth 1 https://github.com/catchorg/Catch2.git`: 5/5 successful.

Conclusion: this is no longer the previous DNS failure. It is an intermittent GitHub HTTPS transfer interruption during Git smart HTTP pack fetch, with HTTP/2 stream cancellation. A practical runner-level mitigation, if it repeats, is to force Git HTTP/1.1 globally:

```bash
git config --global http.version HTTP/1.1
```

This avoids Git/libcurl HTTP/2 streams for GitHub clones. It was not applied during this follow-up; only diagnostics were run.

## Follow-up: objects.githubusercontent.com DNS cache

User clarified that `objects.githubusercontent.com` must resolve to `10.255.0.53`.

Checks on 2026-07-20:

- Active Ethernet DNS remains `10.16.20.3`.
- `dig @10.16.20.3 objects.githubusercontent.com A +short`: `10.255.0.53`.
- `dig objects.githubusercontent.com A +short`: `10.255.0.53`.
- Before cache flush, macOS system resolver (`dscacheutil`) and `curl` still used stale public GitHub IPs `185.199.108.133`-`185.199.111.133`.
- After `sudo dscacheutil -flushcache` and `sudo killall -HUP mDNSResponder`, `dscacheutil -q host -a name objects.githubusercontent.com` returns `10.255.0.53`.
- `curl -Iv --connect-timeout 8 https://objects.githubusercontent.com/` resolves to `10.255.0.53`, connects on TCP/443, TLS verification OK.

Conclusion: after switching DNS to `10.16.20.3`, macOS retained stale resolver cache for `objects.githubusercontent.com`. Cache flush corrected system resolver behavior for Git/curl.

## Follow-up: Firebase App Distribution CI bundle

User clarified that Fastlane and plugins are installed by GitLab CI via `.gitlab-ci.yml`.

Checks:

- CI `.rbenv` before_script runs `rbenv global 3.2.2`, `gem install bundler`, `bundle install`.
- The failing runner workspace `/Users/iosdev/builds/6gfbuVYj/0/team-youdo-ios/YouDoApp` is detached at commit `79e819ca`.
- In that workspace:
  - `Gemfile`: `fastlane`, `2.225.0`.
  - `fastlane/Pluginfile`: `fastlane-plugin-firebase_app_distribution`, `0.9.1`.
  - generated `Gemfile.lock`: `fastlane (2.225.0)`, `fastlane-plugin-firebase_app_distribution (0.9.1)`, `googleauth (1.8.1)`, `signet (0.21.0)`, `BUNDLED WITH 2.6.9`.
- Current local checkout differs: `Gemfile` has `fastlane 2.237.0` and `fastlane/Pluginfile` has firebase plugin `1.0.0`.

Conclusion: the Firebase error in the provided CI log comes from the bundle installed by that specific GitLab job, not from the runner's system gems. The job used firebase plugin `0.9.1`, whose auth helper contains an unsafe `error.response.status` access. This can mask the original Firebase/Google auth/network error when `Signet::AuthorizationError#response` is nil.

## Follow-up: cocoapods-binary usage check

Checked repository `/home/slnnk/git/YouDoApp` after Bundler conflict between `fastlane >= 2.227.1` and `cocoapods-binary 0.4.4` over incompatible `xcpretty` versions.

Search scope:

- `.gitlab-ci.yml`
- `fastlane/Fastfile`
- `Gemfile`
- Ruby, shell, YAML files
- Pod-related files up to depth 5

Findings:

- `cocoapods-binary` appears only in `Gemfile`.
- No `Podfile` found in the repository scan.
- No CI command for `pod install`, `bundle exec pod`, `pod update`, `pod repo`, or `pod binary` found.
- No Fastfile usage of CocoaPods actions or `pod` commands found.
- No `cocoapods-binary` DSL usage found: `all_binary!`, `binary!`, `set_binary`, `set_use_source_pods`, `use_source_pods`, `:binary`.

Conclusion: based on repository, CI, and Fastfile search, `cocoapods-binary` is not used by current build/test/release flows and is likely a stale Gemfile dependency. Removing it should unblock Fastlane versions that require `xcpretty ~> 0.4.1`, subject to CI validation.

## Follow-up: removed stale cocoapods-binary dependency

On 2026-07-20, removed `gem 'cocoapods-binary', '0.4.4'` from repository `Gemfile` in `/home/slnnk/git/YouDoApp`.

Reason:

- `cocoapods-binary >= 0.4.4` requires `xcpretty ~> 0.3.0`.
- `fastlane >= 2.227.1` requires `xcpretty ~> 0.4.1`.
- Current `Gemfile` pins `fastlane 2.232.0`, so Bundler cannot resolve with `cocoapods-binary 0.4.4` present.
- Repository/CI/Fastfile/generate.sh scan did not find actual `cocoapods-binary` usage.

Verification:

- Local machine did not have `bundle` command available, so local `bundle install` could not run.
- Verified on runner `iosdev@192.168.50.10` in a temporary directory with equivalent Gemfile minus `cocoapods-binary` using rbenv Ruby `3.2.2`.
- `bundle install` completed successfully.
- Resolved relevant versions: `fastlane 2.232.0`, `xcpretty 0.4.1`, `fastlane-plugin-firebase_app_distribution 1.0.0`.

## Follow-up: Firebase plugin 1.0.0 still masks auth error

User reported the same CI failure after updating Fastlane/Firebase plugin.

Checks on runner workspace `/Users/iosdev/builds/6gfbuVYj/0/team-youdo-ios/YouDoApp`:

- Commit: `19235c3e`.
- `Gemfile`: `fastlane 2.237.0`, no `cocoapods-binary`.
- `fastlane/Pluginfile`: `fastlane-plugin-firebase_app_distribution 1.0.0`.
- `Gemfile.lock`: `fastlane 2.237.0`, `fastlane-plugin-firebase_app_distribution 1.0.0`, `googleauth 1.17.1`, `signet 0.22.0`, `xcpretty 0.4.1`.
- Installed plugin code still contains unsafe `error.response.status` at `lib/fastlane/plugin/firebase_app_distribution/helper/firebase_app_distribution_auth_client.rb:139`.

Conclusion: plugin `1.0.0` still has the same error reporting bug. A `Signet::AuthorizationError` with nil `response` is raised while fetching service account credentials/access token; the plugin then raises `NoMethodError: undefined method 'status' for nil:NilClass`, masking the original auth/network error.

Repository change made locally:

- Added `print_exception_details(error)` in `fastlane/Fastfile` to print exception class/message, response status/body when present, backtrace, and chained causes.
- Added a monkey patch for `Fastlane::Auth::FirebaseAppDistributionAuthClient#error_details` to handle nil `response` safely.
- Replaced `UI.error ex` in `build_beta` rescue with `print_exception_details(ex)`.
- Verified `ruby -c fastlane/Fastfile`: `Syntax OK`.

Next failing CI run should show the original `Signet::AuthorizationError` cause instead of only the secondary nil `status` failure.

## Follow-up: Firebase auth timeout root cause and retry

The next CI run with improved exception printing exposed the original Firebase failure:

- Secondary plugin error: `NoMethodError: undefined method 'status' for nil:NilClass` in `firebase_app_distribution_auth_client.rb:139`.
- Root cause chain:
  - `Google::Auth::AuthorizationError: Unexpected error: #<Faraday::TimeoutError wrapped=#<Errno::ETIMEDOUT: Operation timed out>>`
  - `Faraday::TimeoutError: Operation timed out`
  - `Errno::ETIMEDOUT: Operation timed out`
- Failure happens during `service_account_credentials.fetch_access_token!`, i.e. while requesting OAuth access token from Google before Firebase upload.
- In the same job one earlier `firebase_app_distribution` step succeeded; the later one failed during a new auth/token request. This indicates intermittent Google OAuth HTTPS timeout, not invalid credentials.

Checks from runner after the failure:

- Active DNS: `10.16.20.3`.
- `oauth2.googleapis.com` resolves to `64.233.165.95` via system resolver and `10.16.20.3`.
- `192.168.50.1` still timed out for DNS and should not be used.
- `curl -Iv --connect-timeout 8 --max-time 20 https://oauth2.googleapis.com/token`: connected, TLS OK, HTTP/2 response received.
- Repeated GET/HEAD-style checks to token endpoint: 20/20 OK.
- Repeated POST checks with dummy payload to token endpoint: 20/20 OK, HTTP 400 expected, response in ~0.42s.

Conclusion: no persistent outage was observed after the job. The Firebase failure is intermittent HTTPS read timeout when fetching Google OAuth token.

Repository change made locally:

- Added `retry_firebase_app_distribution(max_attempts: 3)` to `fastlane/Fastfile`.
- Wrapped the `firebase_app_distribution(...)` call in `build_beta` ad-hoc branch with that retry helper.
- Retry logs exception details, waits 15s before attempt 2 and 30s before attempt 3, then re-raises if all attempts fail.
- Also added an explicit `require` for the Firebase auth helper so the nil-safe `error_details` monkey patch can apply when the plugin is available.
- Verified `ruby -c fastlane/Fastfile`: `Syntax OK`.

## Follow-up: reverted local Fastfile changes and flushed runner DNS cache

On user request, reverted local Fastfile diagnostic/retry changes. Local repository status became clean.

Flushed DNS cache on `iosdev@192.168.50.10`:

```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Verification after flush:

- Ethernet DNS remains `10.16.20.3`.
- `oauth2.googleapis.com` resolves via system resolver and `dig @10.16.20.3` to `10.255.0.54`.
- `firebaseappdistribution.googleapis.com` resolves via system resolver and `dig @10.16.20.3` to `10.255.0.33`.
- `objects.githubusercontent.com` remains `10.255.0.53`.
- `rubygems.org` remains `10.255.0.47`.
- Quick curl checks connected to the internal IPs:
  - `https://oauth2.googleapis.com/token`: remote IP `10.255.0.54`, HTTP 404 for HEAD/GET-style check, TLS OK.
  - `https://firebaseappdistribution.googleapis.com/`: remote IP `10.255.0.33`, HTTP 404 for root path, TLS OK.

## Follow-up: Firebase auth still times out after internal DNS update

User reported another CI failure at 2026-07-20 19:00 MSK. The improved log still shows:

- `Google::Auth::AuthorizationError: Unexpected error: #<Faraday::TimeoutError wrapped=#<Errno::ETIMEDOUT: Operation timed out>>`
- The timeout happens in Ruby `Net::HTTP` while reading the HTTP status line from the OAuth token response.
- Failing operation remains `service_account_credentials.fetch_access_token!`, before Firebase upload.

Checks immediately after:

- `oauth2.googleapis.com` resolves via system resolver to `10.255.0.54`.
- `dig @10.16.20.3 oauth2.googleapis.com A +short`: `10.255.0.54`.
- `curl` POST checks to `https://oauth2.googleapis.com/token`: 10/10 OK, HTTP 400 expected for dummy invalid request, remote IP `10.255.0.54`, ~0.46s.
- Ruby `Net::HTTP` POST checks with dummy JWT-bearer-style payload: 10/10 OK, HTTP 400 expected, ~0.45-0.51s.

Conclusion: DNS is correct and immediate post-failure probes through Ruby and curl work. The CI issue is intermittent timeout on the internal Google OAuth route/proxy `10.255.0.54` while handling the real service-account token request. Check logs/metrics on the DNS/proxy/gateway backing `10.255.0.54` around 2026-07-20 19:00:42 MSK for requests from `192.168.50.10` to `oauth2.googleapis.com/token`.

## Follow-up: real service account token request

User provided a temporary service account JSON at `/tmp/g.json` on runner.

Test executed on `iosdev@192.168.50.10` using rbenv Ruby `3.2.2` and `googleauth`, without printing token or JSON contents:

- DNS: `oauth2.googleapis.com` resolves to `10.255.0.54`.
- File exists: `/tmp/g.json`, 2356 bytes.
- Performed real `Google::Auth::ServiceAccountCredentials.fetch_access_token!` with scope `https://www.googleapis.com/auth/cloud-platform`.

Result:

- Attempt 1: `Google::Auth::AuthorizationError` wrapping `Faraday::TimeoutError` / `Errno::ETIMEDOUT`, time `130.291s`.
- Attempt 2: same timeout, time `138.929s`.
- Attempt 3: same timeout, time `129.859s`.
- Remaining attempts were interrupted manually after the pattern was confirmed.

Conclusion: real service-account OAuth token exchange reproducibly times out through internal `oauth2.googleapis.com -> 10.255.0.54`. Earlier dummy POST requests to the same endpoint returned quickly, so this is specific to the real JWT bearer token request path/content or to how the internal proxy handles/forwards it. If credentials were simply invalid, Google would normally return a quick HTTP 400/401 JSON error rather than no HTTP status line until read timeout.

Next checks should be on the internal proxy/gateway behind `10.255.0.54` for POST `/token` requests from `192.168.50.10` during the test window around 2026-07-20 19:06-19:15 MSK.

## Follow-up: direct OAuth token exchange test

User asked to try a direct request.

Performed a precise real JWT-bearer OAuth token exchange using `/tmp/g.json`, without printing the JWT or access token:

- Generated service-account JWT locally in memory/file with Ruby stdlib (`json`, `openssl`, `base64`).
- Sent `POST https://oauth2.googleapis.com/token` via `curl --resolve` to specific IPs.
- Redacted `access_token` from output.

Results:

- `10.255.0.54`: HTTP 200, token type Bearer, expires in 3599s, total ~0.468s.
- `64.233.165.95`: HTTP 200, total ~0.440s.
- `142.250.150.95`: HTTP 200, total ~0.436s.
- `142.251.1.95`: HTTP 200, total ~0.420s.

Then repeated the original Ruby `googleauth` path:

- Attempt 1: OK, ~0.115s.
- Attempt 2: OK, ~0.092s.
- Attempt 3: OK, ~0.089s.

Conclusion: credentials in `/tmp/g.json` are valid. Both direct curl token exchange and Ruby `googleauth` currently work. Earlier timeouts were transient or stateful behavior on the OAuth route/proxy/connection path, not an invalid token/key.

## Follow-up: recheck through corporate DNS

User requested another check through the corporate DNS path.

Results on `iosdev@192.168.50.10`:

- Ethernet DNS: `10.16.20.3`.
- System resolver `oauth2.googleapis.com`: `10.255.0.54`.
- `dig @10.16.20.3 oauth2.googleapis.com A +short`: `10.255.0.54`.
- Real curl JWT token exchange through normal DNS, no `--resolve`:
  - Attempt 1: HTTP 200, remote IP `10.255.0.54`, ~0.482s.
  - Attempt 2: HTTP 200, remote IP `10.255.0.54`, ~0.468s.
  - Attempt 3: HTTP 200, remote IP `10.255.0.54`, ~0.479s.
- Ruby `googleauth` `fetch_access_token!` through normal DNS:
  - 5/5 OK, token type Bearer, ~0.084-0.108s.

Conclusion: as of this check, the normal corporate DNS route `oauth2.googleapis.com -> 10.255.0.54` works for both direct curl JWT exchange and the same Ruby googleauth path used by Fastlane.

## Follow-up: CI credentials file compared with user test file

After another CI failure at 2026-07-20 19:39 MSK, checked the still-present CI file `/tmp/firebase_credentials.json` against user-provided `/tmp/g.json`.

Safe metadata:

- Both files are service account JSON for `project_id=firebase-appios`.
- Both use `client_email=fastlane@firebase-appios.iam.gserviceaccount.com`.
- Both use the same `private_key_id=<redacted, key identifier of the Firebase service account>`.
- Both have the same private key SHA-256 hash (value recorded in terminal output but not repeated here as an operational secret-adjacent fingerprint beyond the session need).
- Files differ only in JSON bytes/formatting size/hash.

Cross-check script `/tmp/oauth_check.rb` generated real JWT bearer requests without printing JWT/access tokens:

- curl with `/tmp/g.json`: HTTP 200 via `10.255.0.54`, ~0.520s.
- curl with `/tmp/firebase_credentials.json`: HTTP 200 via `10.255.0.54`, ~0.489s.
- Ruby `googleauth` alternating files:
  - `/tmp/g.json`: OK but took `62.22s` on one run.
  - `/tmp/firebase_credentials.json`: OK, ~0.095s.
  - `/tmp/g.json`: OK, ~0.095s.
  - `/tmp/firebase_credentials.json`: OK, ~0.092s.

Conclusion: CI credentials and user-provided test credentials represent the same service-account key and both can obtain tokens. The issue is intermittent latency/stall in the OAuth token exchange path. A successful request can occasionally take tens of seconds; failing CI attempts time out around 120-140s while waiting for the HTTP status line. This reinforces that the root cause is network/proxy behavior around `oauth2.googleapis.com -> 10.255.0.54`, not invalid credentials.

## Follow-up: switched runner to public DNS for OAuth test

User requested switching DNS to public resolvers and testing 10 times.

Actions on `iosdev@192.168.50.10`:

```bash
sudo networksetup -setdnsservers Ethernet 1.1.1.1 8.8.8.8
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Verification:

- Ethernet DNS now: `1.1.1.1`, `8.8.8.8`.
- System resolver `oauth2.googleapis.com` returned public Google IPs, e.g. `209.85.233.95`.
- `dig` via public resolvers returned public Google IPs, not `10.255.0.54`.

Real OAuth token checks using `/tmp/firebase_credentials.json` and Ruby `googleauth`:

- 10 attempts, all OK.
- Timings: ~0.083-0.122s.
- Summary: `ok=10 fail=0`.

Conclusion: with public DNS bypassing the internal `10.255.0.54` route, real Google OAuth token fetch is fast and stable in this 10-attempt test. Runner is currently left configured with public DNS `1.1.1.1 8.8.8.8`; note this bypasses corporate DNS overrides for hosts such as `rubygems.org`, `objects.githubusercontent.com`, and Firebase/Google endpoints.

## Follow-up: public DNS long-spaced OAuth test

User requested 10 more checks with 10 seconds between attempts after switching runner to public DNS `1.1.1.1 8.8.8.8`.

Results:

- DNS remained public: `1.1.1.1`, `8.8.8.8`.
- System resolver for `oauth2.googleapis.com`: IPv4 `209.85.233.95` and IPv6 `2a00:1450:4010:c03::5f`.
- Long-spaced Ruby `googleauth` test with `/tmp/firebase_credentials.json`:
  - Attempt 1: `Google::Auth::AuthorizationError` / `Faraday::TimeoutError` / `Errno::ETIMEDOUT`, time `121.455s`.
  - Attempt 2: same timeout, time `129.679s`.
  - Test was interrupted after 2/2 failures to avoid waiting for all 10 attempts.
- Additional probes:
  - `curl -4 https://oauth2.googleapis.com/token` to `209.85.233.95` timed out during SSL connection after 8s.
  - `curl -6` displayed remote IP `::ffff:209.85.233.95` and returned HTTP 404 quickly.
  - Ruby `Addrinfo` order: IPv4 first (`209.85.233.95`), then IPv6 (`2a00:1450:4010:c03::5f`).
  - Ruby googleauth with an attempted IPv4-only Addrinfo monkey patch still timed out after `125.991s`.

Conclusion: public DNS is also not a reliable fix. The failure reproduces against public Google IPs too, with hangs during TLS/HTTP response reading. The issue is broader network path instability from runner `192.168.50.10` toward Google OAuth, not only the internal `10.255.0.54` DNS override.

## Follow-up: restored corporate DNS on ios runner

On 2026-07-21, restored macOS Ethernet DNS on `iosdev@192.168.50.10` to corporate resolver `10.16.20.3` and flushed resolver cache.

Commands executed:

```bash
sudo networksetup -setdnsservers Ethernet 10.16.20.3
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Verification:

- `networksetup -getdnsservers Ethernet`: `10.16.20.3`.
- `scutil --dns`: resolver #1 and scoped `en0` resolver use `10.16.20.3`, search domain `youdo.loc`.
- `dscacheutil -q host -a name oauth2.googleapis.com`: `10.255.0.54`.
- `dig +short oauth2.googleapis.com A`: `10.255.0.54`.

## Follow-up: 10 real curl OAuth token checks after restoring corporate DNS

On 2026-07-21, after restoring Ethernet DNS to `10.16.20.3`, ran 10 real JWT bearer OAuth token exchanges from `iosdev@192.168.50.10` using service account JSON `/tmp/g.json`. The JWT and access tokens were not printed or recorded. There was a 10 second sleep between attempts.

Initial state:

- `networksetup -getdnsservers Ethernet`: `10.16.20.3`.
- `dscacheutil -q host -a name oauth2.googleapis.com`: `10.255.0.54`.

Results:

- Attempts: 10.
- Success: 10.
- Failures: 0.
- HTTP status: all `200`.
- Remote IP: all `10.255.0.54`.
- Token response: Bearer token present, `expires_in=3599`; token value was not recorded.
- `curl time_total` range: approximately `0.462-0.476s`; average approximately `0.467s`.
- Test window: approximately `2026-07-21 12:18:08-12:19:44 MSK`.

Conclusion: during this check, the corporate DNS route `oauth2.googleapis.com -> 10.255.0.54` was fast and stable for real curl-based OAuth token exchange with `/tmp/g.json`.

## Follow-up: CI failure after successful curl OAuth checks and Fastlane retry

On 2026-07-21, user provided a new CI failure log around `13:11:45-13:13:55 MSK` from `firebase_app_distribution`. The second Firebase upload attempt in the lane failed after about `129s`. The visible top-level error was again plugin bug `NoMethodError: undefined method status for nil:NilClass` in `fastlane-plugin-firebase_app_distribution-1.0.0`, but the printed cause chain showed the real failure:

- `Google::Auth::AuthorizationError: Unexpected error: #<Faraday::TimeoutError wrapped=#<Errno::ETIMEDOUT: Operation timed out>>`.
- Timeout occurs in Ruby `Net::HTTP` while reading the HTTP status line during `service_account_credentials.fetch_access_token!`.

Immediate post-failure check on `iosdev@192.168.50.10` at about `13:55 MSK`:

- Ethernet DNS remained `10.16.20.3`.
- `oauth2.googleapis.com` resolved to `10.255.0.54`.
- `/tmp/firebase_credentials.json` existed.
- A real curl JWT bearer token exchange with `/tmp/firebase_credentials.json` succeeded: HTTP `200`, remote IP `10.255.0.54`, total about `0.480s`; token value was not printed or recorded.

Conclusion: this reproduces the known intermittent OAuth token read timeout. The credentials and DNS were valid immediately after the failure. The failure is consistent with transient network/proxy/path behavior during the real OAuth request, not invalid credentials.

Repository change made locally in `/home/slnnk/git/YouDoApp/fastlane/Fastfile`:

- Added explicit `require fastlane/plugin/firebase_app_distribution/helper/firebase_app_distribution_auth_client` guarded by `LoadError`, so the nil-safe Firebase auth helper monkey patch can apply in CI before the action runs.
- Added `retryable_firebase_error?` to detect timeout/ETIMEDOUT in an exception cause chain.
- Added `retry_firebase_app_distribution(max_attempts: 3, **options)`, retrying only timeout-class failures with waits of 15s then 30s.
- Replaced direct `firebase_app_distribution(...)` in `build_beta` ad-hoc branch with `retry_firebase_app_distribution(...)`.

Verification:

- `ruby -c fastlane/Fastfile`: `Syntax OK`.
- `git diff --check fastlane/Fastfile`: clean.

## Follow-up: three CI retries timed out; switched Firebase service-account auth to curl token exchange

On 2026-07-21, user provided a CI log from about `15:23-15:30 MSK` after adding retry around Firebase App Distribution. All three `firebase_app_distribution` attempts failed while authenticating with `/tmp/firebase_credentials.json`:

- Attempt 1 failed after about `126s`, then retry waited `15s`.
- Attempt 2 failed after about `123s`, then retry waited `30s`.
- Attempt 3 failed after about `131s`.
- Each failure had the same cause chain: `Google::Auth::AuthorizationError` -> `Faraday::TimeoutError` -> `Errno::ETIMEDOUT` while Ruby `Net::HTTP` was reading the OAuth token response status line.
- The plugin still reported the secondary `NoMethodError: undefined method status for nil:NilClass`, confirming the earlier error_details monkey patch did not apply early/enough to the extended action module.

Immediate check on `iosdev@192.168.50.10` at about `15:37 MSK`:

- Ethernet DNS: `10.16.20.3`.
- `oauth2.googleapis.com`: `10.255.0.54`.
- Real curl JWT bearer token exchange with `/tmp/firebase_credentials.json`: HTTP `200`, remote IP `10.255.0.54`, total about `0.473s`; token value was not printed or recorded.

Conclusion: simple retry is insufficient when the Ruby googleauth/Net::HTTP path stalls repeatedly. Equivalent curl-based token exchange can still succeed immediately in the same network state.

Repository change made locally in `/home/slnnk/git/YouDoApp/fastlane/Fastfile`:

- Added `base64`, `openssl`, `open3`, `tempfile` stdlib requires.
- Replaced the earlier static monkey patch with `patch_firebase_app_distribution_auth_client!`, called immediately before Firebase action execution.
- The patch aliases the original plugin `get_service_account_credentials` and overrides it only for `type=service_account` JSON.
- For service account credentials, it generates a JWT bearer assertion locally and exchanges it using `curl` with `--connect-timeout 8 --max-time 150`, then sets `access_token`/`expires_in` on a normal `Google::Auth::ServiceAccountCredentials` object returned to Google API clients.
- JWT assertion is passed to curl via a temporary file and unlinked in `ensure`; JWT/access token values are not logged.
- Non-service-account auth and curl failure fall back to the original googleauth implementation.
- The nil-safe `error_details` patch is now applied via `module_eval` at the same time.

Verification:

- `ruby -c fastlane/Fastfile`: `Syntax OK`.
- `git diff --check fastlane/Fastfile`: clean.

## Follow-up: added retry inside curl OAuth token exchange

On 2026-07-21, added retry inside the curl-based Firebase service-account OAuth token exchange in `/home/slnnk/git/YouDoApp/fastlane/Fastfile`.

Details:

- `fetch_service_account_access_token_with_curl` now retries the curl token exchange.
- Default attempts: `3`.
- Override env var: `FIREBASE_OAUTH_TOKEN_CURL_MAX_ATTEMPTS`.
- Waits are linear: `10s`, then `20s` before the third attempt.
- JWT assertion is still passed through a temp file and unlinked; JWT/access token values are not logged.
- Outer `retry_firebase_app_distribution(max_attempts: 3)` remains in place as a second-level retry around the full Firebase action.

Verification:

- `ruby -c fastlane/Fastfile`: `Syntax OK`.
- `git diff --check fastlane/Fastfile`: clean.

## Follow-up: fixed Fastfile constant lookup for curl auth patch

On 2026-07-21, CI log showed the curl auth patch falling back to googleauth immediately with `NameError: uninitialized constant Fastlane::FastFile::SCOPE`. Cause: methods added with `module_eval` from Fastfile used Fastfile lexical constant lookup instead of plugin module constants.

Fix in `/home/slnnk/git/YouDoApp/fastlane/Fastfile`:

- Replaced bare `SCOPE` with `Fastlane::Auth::FirebaseAppDistributionAuthClient::SCOPE`.
- Replaced bare `TOKEN_CREDENTIAL_URI` with `Fastlane::Auth::FirebaseAppDistributionAuthClient::TOKEN_CREDENTIAL_URI`.

Verification:

- `ruby -c fastlane/Fastfile`: `Syntax OK`.
- `git diff --check fastlane/Fastfile`: clean.

## 2026-07-21 CI follow-up: Firebase OK, runner disk full

- Context: YouDoApp iOS GitLab runner `idcn-10.local` / `iosdev@192.168.50.10`, job for MR 3230, build `3026951`, version `4.225.0`.
- Firebase App Distribution upload succeeded after Fastfile workaround: IPA uploaded, release created/distributed, Crashlytics and AppMetrica dSYM uploads succeeded. No OAuth timeout reproduced in this run.
- New failure: second `gym` archive for `YDSettingsApp` failed with `No space left on device` while writing `VGSLUI.build/Objects-normal/arm64/NilImageHolder.o`. This is disk exhaustion, not a Swift/VGSL source error.
- Runner disk snapshot: `/System/Volumes/Data` 228Gi total, 204Gi used, 1.1Gi free, 100% capacity. Major consumers found: `~/builds/6gfbuVYj` 27G (`0` 14G, `1` 14G, `2` 77M), `~/Library/Developer/Xcode/DerivedData` 25G, `~/Library/Developer/Xcode/Archives` 12G, `~/Library/Caches` 4.4G.
- Simulator runtime mountpoints like `/Library/Developer/CoreSimulator/Volumes/iOS_*` show 98% because they are mounted runtime images; do not treat their internal free space as the primary build workspace free space. Clean via Xcode/simctl runtime/device management only if those runtimes are genuinely obsolete.
- Recommended cleanup order: old `DerivedData` entries, old `Archives` dates, stale runner workspace slot not used by the active job, then user caches/logs. Avoid deleting current build workspace while a job is running.

## 2026-07-21 runner cleanup

- Per user request, cleaned on `iosdev@192.168.50.10`: `~/Library/Developer/Xcode/DerivedData/*`, `~/Library/Developer/Xcode/Archives/*`, and `~/builds/6gfbuVYj/*` except active slot `0`.
- Disk result: `/System/Volumes/Data` changed from 228Gi total / 204Gi used / 1.3Gi free / 100% capacity to 228Gi total / 168Gi used / 37Gi free / 82% capacity.
- Remaining checked paths: `~/builds/6gfbuVYj/0` 14G; `DerivedData` 8K; `Archives` 8K.

## Portable lesson

- `~/ai/general/knowledge/git/http2-stream-cancel-curl-92-clone-failures.md`
- `~/ai/general/knowledge/macos/dns-change-stale-resolver-cache.md`
