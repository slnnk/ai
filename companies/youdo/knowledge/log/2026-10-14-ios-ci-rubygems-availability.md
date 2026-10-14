---
system: ios-ci
status: verified
checked: 2026-10-14
tags: [ios-ci, dns, rubygems]
---
# RubyGems availability from idcn-10

## Summary

At 15:10–15:12 MSK, a repeat check from idcn-10 (192.168.30.144) passed ordinary HTTPS requests for the RubyGems home page, full and compact indexes, fastlane metadata and the fastlane 2.240.0 gem download. Ethernet DNS remains 172.28.0.200; both RubyGems hosts still resolve to 10.255.0.47. At 11:02 MSK the same corporate destination/path timed out while a public-IP bypass worked. Current availability is verified; the earlier failure and recovery cause remain unverified. No remote settings were changed.

## Context

The user requested prior history and a current availability check. Previous evidence: [July DNS incident](2026-07-20-ios-ci-runner-dns-rubygems.md) and [October DNS recovery](2026-10-12-ios-ci-runner-offline-dns-unreachable.md).

## Actions and findings

- Read-only SSH as iosdev; networksetup -getdnsservers Ethernet returned 172.28.0.200.
- curl GETs for https://rubygems.org/, /specs.4.8.gz, /api/v1/gems/fastlane.json and https://index.rubygems.org/versions all returned HTTP000 after approximately8seconds at TCP connection establishment. DNS lookup times were0.004–0.093seconds; no TLS connection was established.
- dig +tries=1 +time=2 rubygems.org A and the corresponding index.rubygems.org query returned10.255.0.47; index uses a CNAME to rubygems.org.
- dig @1.1.1.1 rubygems.org A returned151.101.1.227,151.101.65.227,151.101.129.227,151.101.193.227.
- curl --resolve rubygems.org:443:151.101.193.227 https://rubygems.org/ returned HTTP200 in0.168seconds from the same runner, preserving hostname/SNI and certificate verification.
- Workstation default HTTPS returned HTTP200 via151.101.193.227 in0.289seconds.
- Official https://status.rubygems.org reported core download/application/index services operational; Fastly London LCY was under maintenance. This does not explain the corporate private-address timeout.

## Repeat check at 15:10–15:12 MSK

- User requested a fresh RubyGems availability check on the iOS runner. Read-only SSH target: iosdev@192.168.30.144, hostname idcn-10.local.
- `networksetup -getdnsservers Ethernet` returned 172.28.0.200; `dscacheutil` and Ruby `Addrinfo.getaddrinfo` returned 10.255.0.47 for rubygems.org and index.rubygems.org.
- `curl -sS -L -o /dev/null --connect-timeout 8 --max-time 20` used ordinary DNS and certificate verification. Home page: HTTP 200 in 0.702 s. `/specs.4.8.gz`: HTTP 200, 6,277,183 bytes in 2.216 s. `/api/v1/gems/fastlane.json`: HTTP 200 in 0.537 s.
- `https://index.rubygems.org/versions`: HTTP 200, 23,593,299 bytes in 5.176 s; `/info/fastlane`: HTTP 200, 1,250,113 bytes in 1.415 s.
- `https://rubygems.org/gems/fastlane-2.240.0.gem`: HTTP 200, 1,197,568 bytes in 1.416 s. Every request connected to 10.255.0.47; downloaded bodies were discarded, no gem installed.
- These checks establish current endpoint/download availability, not a complete bundle install or CI job result. No fix was applied; the cause of restored access remains unknown.

## Changed files and limits

Only this local evidence note, the existing GitLab system map and knowledge indexes were updated. SSH/curl/dig were read-only; no DNS changes, package installs, CI jobs or remote configuration changes were performed. The public-IP check covered the home page only and does not establish a full bundle install. Internal endpoint10.255.0.47 ownership and availability were not investigated.
