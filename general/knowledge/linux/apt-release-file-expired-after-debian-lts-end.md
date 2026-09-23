---
system: linux
status: verified
checked: 2026-09-08
tags: [apt, debian, valid-until, lts, docker, dotnet]
---
# apt update: "Release file ... is expired" for a Debian suite after its LTS ended

## Symptom

Inside a container based on an old Debian release (for example the
`mcr.microsoft.com/dotnet/aspnet:6.0` image on bullseye), `apt update` fails:

```text
E: Release file for http://deb.debian.org/debian-security/dists/bullseye-security/InRelease is expired (invalid since 13h ...). Updates for this repository will not be applied.
```

The main suite still works, only `<codename>-security` fails, and the error
age grows by the hour.

## Cause

APT checks the `Valid-Until` field of the `InRelease` file. Debian stops
regenerating the security suite metadata when the release leaves LTS, so the
last published file simply expires. It is not a clock problem on the host:

```bash
date -u
curl -fsSL http://deb.debian.org/debian-security/dists/bullseye-security/InRelease | sed -n '1,12p'
grep -R --line-number bullseye-security /etc/apt/sources.list /etc/apt/sources.list.d
```

If `Valid-Until` in the output is in the past and matches the reported age,
the repository is dead, and `archive.debian.org` may not have picked up the
security suite yet (it returned 404 at the time of the check).

## Fix

Preferred: move to a supported base image. For .NET there are bookworm
variants of even the unsupported runtimes, for example
`mcr.microsoft.com/dotnet/aspnet:6.0-bookworm-slim` or a pinned
`6.0.36-bookworm-slim`; this drops the dead Debian suite without retargeting
the application, but does not restore support for the runtime itself.

Temporary workarounds, in decreasing order of acceptability:

1. Remove or comment out only the `<codename>-security` line; no more
   security updates, but the build is honest about it.
2. `apt-get -o Acquire::Check-Valid-Until=false update` as a short emergency
   bypass; it hides the freshness check and still delivers no new fixes.

## Limits

- Debian 11 LTS ended 2026-08-31; the same happens to every release at its LTS
  end and to Ubuntu ESM-only releases.
- Do not "fix" the host clock; the check compares against the file's own date.
