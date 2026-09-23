---
system: linux
status: verified
checked: 2026-09-08
tags: [apt, debian, eol, lts, valid-until, archive.debian.org, Check-Valid-Until, docker, dotnet]
---
# apt fails for a Debian release after its LTS ended: expired Release file, then 404

## Symptom

Inside a container or host on an old Debian release `apt-get update` fails in one of two
ways, depending on how long ago the release left LTS.

Stage 1, weeks to months after LTS end: only the security suite fails, and the reported
age grows by the hour.

```text
E: Release file for http://deb.debian.org/debian-security/dists/bullseye-security/InRelease is expired (invalid since 13h ...). Updates for this repository will not be applied.
```

Stage 2, later: the suites are removed from the mirrors and every source returns 404.

```text
E: The repository 'http://deb.debian.org/debian buster Release' does not have a Release file.   (404)
E: The repository 'http://deb.debian.org/debian-security buster/updates Release' ... (404)
E: The repository 'http://deb.debian.org/debian buster-updates Release' ... (404)
```

Typical carriers are old runtime images such as `mcr.microsoft.com/dotnet/aspnet:6.0`
(bullseye) or `mcr.microsoft.com/dotnet/aspnet:3.1` (buster).

## Cause

APT checks the `Valid-Until` field of `InRelease`. Debian stops regenerating the security
suite metadata when the release leaves LTS, so the last published file expires (stage 1).
Later the suites are deleted from `deb.debian.org` and `security.debian.org` and survive only
on `archive.debian.org`, whose `Release` files are frozen with an expired `Valid-Until`
(stage 2). It is never a clock problem on the host:

```bash
date -u
curl -fsSL http://deb.debian.org/debian-security/dists/bullseye-security/InRelease | sed -n '1,12p'
grep -R --line-number bullseye-security /etc/apt/sources.list /etc/apt/sources.list.d
```

If `Valid-Until` in the output is in the past and matches the reported age, the repository
is dead. `archive.debian.org` may lag behind and return 404 for the security suite for a
while after stage 1 begins.

## Fix

Preferred: move to a supported base image. For .NET there are bookworm variants of even the
unsupported runtimes, for example `mcr.microsoft.com/dotnet/aspnet:6.0-bookworm-slim` or a
pinned `6.0.36-bookworm-slim`; this drops the dead Debian suite without retargeting the
application, but does not restore support for the runtime itself.

Stage 1 workarounds, in decreasing order of acceptability:

1. Remove or comment out only the `<codename>-security` line; no more security updates, but
   the build is honest about it.
2. `apt-get -o Acquire::Check-Valid-Until=false update` as a short emergency bypass; it hides
   the freshness check and still delivers no new fixes.

Stage 2: rewrite the sources to the archive before the first `apt-get update`:

```dockerfile
RUN sed -i -e 's|deb.debian.org/debian-security|archive.debian.org/debian-security|g' \
           -e 's|security.debian.org/debian-security|archive.debian.org/debian-security|g' \
           -e 's|deb.debian.org/debian|archive.debian.org/debian|g' \
           -e '/buster-updates/d' /etc/apt/sources.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --no-install-recommends <packages> \
 && rm -rf /var/lib/apt/lists/*
```

`<codename>-updates` does not exist on the archive; delete that line. Images that use
`/etc/apt/sources.list.d/debian.sources` (deb822) need the same substitution in that file.
Verify with a plain `docker build`; the build must complete and the image must contain the
packages you added.

## Limits

- Both workarounds keep an EOL distribution alive without security updates. They are a
  stop-gap for legacy runtimes that cannot move; the real fix is a supported base image.
- Debian 11 LTS ended 2026-08-31; the same happens to every release at its LTS end and to
  Ubuntu ESM-only releases.
- Do not "fix" the host clock; the check compares against the file's own date.
- `snapshot.debian.org` is an alternative when you need a specific point in time, but it is
  rate-limited and slow for builds.
- Package versions on the archive are frozen; upgrades (for example to a newer
  `ca-certificates`) are not available through it.
