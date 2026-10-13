---
system: ios-ci
status: verified
checked: 2026-10-12
tags: [runner, dns, macos]
---
# idcn-10 runner offline: configured DNS unreachable

## Summary

At 19:43–19:44 MSK, idcn-10 (`iosdev@192.168.30.144`, runner ID 93) was running but unable to resolve `gitlab.youdo.sg` through its sole Ethernet DNS server `10.16.20.3`. Explicit public DNS resolved the current GitLab IP, and HTTPS with DNS bypass returned HTTP 200. Failure is in corporate DNS reachability; server downtime versus routing/firewall failure is not yet established. No remote settings changed.

## Context and actions

User requested diagnosis of an offline runner and suspected DNS. Read-only SSH checks inspected process, LaunchAgent, DNS, route, disk, recent errors and HTTPS connectivity.

- Process PID 737: `/usr/local/bin/gitlab-runner run --config /Users/iosdev/.gitlab-runner/config.toml --working-directory /Users/iosdev --service gitlab-runner --syslog`; launchctl exit status 0.
- Configured GitLab URL: `https://gitlab.youdo.sg`; shell executor.
- LaunchAgent: `/Users/iosdev/Library/LaunchAgents/gitlab-runner.plist`.
- Logs: `/Users/iosdev/gitlab-runner.err.log` and `/Users/iosdev/gitlab-runner.out.log`; error log actively updated at 19:44:08 MSK.
- Repeated errors: `lookup gitlab.youdo.sg: i/o timeout` while checking for jobs.

## Findings and key commands

- `scutil --dns` and `networksetup -getdnsservers Ethernet`: sole DNS `10.16.20.3`.
- `dig @10.16.20.3 +time=2 +tries=1 gitlab.youdo.sg`: UDP timeout; same with `+tcp` and for `example.com`.
- Direct query from the engineer workstation to `10.16.20.3` also timed out; workstation default DNS resolved GitLab successfully.
- `dig @1.1.1.1 +time=2 +tries=1 gitlab.youdo.sg`: NOERROR, A `138.16.203.174`, 178 ms.
- Normal curl to GitLab: resolving timeout, HTTP 000.
- `curl -sS -o /dev/null --resolve gitlab.youdo.sg:443:138.16.203.174 --connect-timeout 5 --max-time 10 -w '%{http_code} %{remote_ip}\n' https://gitlab.youdo.sg/users/sign_in`: HTTP 200, TLS validation passed.
- `route -n get 10.16.20.3`: gateway `192.168.30.1`, interface `en0`; ping 2/2 unanswered (ICMP alone does not establish server outage).
- Root filesystem has 49 GiB available.

## Changes and risks

Only local KB log, GitLab system map, TODO and sync notes updated. No restart, DNS replacement, runner registration, API mutation or remote write performed. Public DNS is a proven diagnostic bypass for GitLab, but replacing corporate DNS with public-only DNS could break internal names. Restoration or replacement needs explicit approval and verification of internal resolution. See [GitLab system map](../systems/gitlab.md) and the prior [DNS incident](2026-07-20-ios-ci-runner-dns-rubygems.md).

## Approved DNS change at 19:46 MSK

The user explicitly requested changing DNS to `10.18.20.3`. Executed `sudo -n networksetup -setdnsservers Ethernet 10.18.20.3` over SSH; exit 0. Independent `networksetup -getdnsservers Ethernet` and `scutil --dns` confirmed the new sole resolver. Direct UDP query to the new DNS timed out; normal HTTPS request to GitLab still failed resolving (HTTP 000). Thus the requested configuration change succeeded, but connectivity was not restored. No runner restart or further DNS changes authorized or performed.

## Alternative DNS verified at 21:30 MSK

After the user enabled their VPN, SSH to the Mac was reachable again. Direct queries from idcn-10 to `172.28.0.200` succeeded: `gitlab.youdo.sg` resolved to `138.16.203.174` over UDP (18 ms) and TCP (17 ms), both NOERROR. `example.com` also resolved (80 ms). The configured Ethernet resolver is still `10.18.20.3`; this test did not change host settings. The earlier SSH timeouts prevented DNS testing and are distinct from DNS query failures. Switching to the verified alternative has not been requested or performed.

## Approved recovery at 21:32 MSK

User explicitly requested setting Ethernet DNS to `172.28.0.200`. Executed `sudo -n networksetup -setdnsservers Ethernet 172.28.0.200`; exit 0. Fresh networksetup/scutil checks confirm the resolver, default `dig` resolves GitLab to `138.16.203.174`, and ordinary HTTPS returns HTTP 200 without bypass. Independent authenticated GET `/api/v4/runners/93` confirms `status: online`, `online: true`, `paused: false`, contacted_at `2026-10-12T21:32:15.149+03:00`. Runner reconnected without restarting. Earlier log tail still contained historical DNS errors and was not used as recovery evidence.

Before this change, direct lookup of `api.openai.com` through the chosen DNS returned A `10.255.0.31`, TTL 5 seconds, no AAAA answer. Recorded as observed DNS behavior only; API connectivity was not tested. Internal domain resolution was not separately validated.
