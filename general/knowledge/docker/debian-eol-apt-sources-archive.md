---
system: docker
status: verified
checked: 2026-06-26
tags: [apt, debian, buster, eol, archive.debian.org, Check-Valid-Until, dotnet]
---
# `apt-get update` returns 404 for a Debian release removed from the mirrors

## Symptom

Building on an old base image (for example `mcr.microsoft.com/dotnet/aspnet:3.1`, Debian 10
buster) fails at the first `apt-get update`:

```text
E: The repository 'http://deb.debian.org/debian buster Release' does not have a Release file.   (404)
E: The repository 'http://deb.debian.org/debian-security buster/updates Release' ... (404)
E: The repository 'http://deb.debian.org/debian buster-updates Release' ... (404)
```

## Cause

After a Debian release leaves LTS, its suites are first left to expire (see
`linux/apt-release-file-expired-after-debian-lts-end.md`) and later **removed** from
`deb.debian.org` / `security.debian.org`. They survive only on `archive.debian.org`, whose
`Release` files are frozen and have an expired `Valid-Until`, so APT also needs the validity
check disabled.

## Fix

Rewrite the sources before the first `apt-get update` in the Dockerfile:

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

- This keeps an EOL distribution alive without security updates. It is a stop-gap for
  legacy runtimes that cannot move; the real fix is a supported base image.
- `snapshot.debian.org` is an alternative when you need a specific point in time, but it is
  rate-limited and slow for builds.
- Package versions on the archive are frozen; upgrades (for example to a newer
  `ca-certificates`) are not available through it.
