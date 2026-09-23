---
system: base-images
status: verified
checked: 2026-06-26
tags: [base-images, dockerfile, dotnet-3.1, debian-buster, archive.debian.org, apt, eol]
---
# base-images: dotnet aspnet 3.1 buster archive

Date: 2026-06-26
Project: base-images
Repository: /home/slnnk/git/base-images
File: microsoft/dotnet-core-aspnet/3.1/Dockerfile

## Task

`docker build -t test -f microsoft/dotnet-core-aspnet/3.1/Dockerfile .` failed during `apt-get update` because the base image `mcr.microsoft.com/dotnet/aspnet:3.1` uses Debian buster repositories that are no longer available from regular `deb.debian.org` paths.

Observed errors:
- `http://deb.debian.org/debian buster Release` returned 404.
- `http://deb.debian.org/debian-security buster/updates Release` returned 404.
- `http://deb.debian.org/debian buster-updates Release` returned 404.

## Changes

Updated `microsoft/dotnet-core-aspnet/3.1/Dockerfile` to rewrite Debian apt sources to `archive.debian.org` before `apt-get update` and run update with `Acquire::Check-Valid-Until=false` for the archived EOL release.

## Actions

Verification, ran:

```sh
docker build -t test -f microsoft/dotnet-core-aspnet/3.1/Dockerfile .
```

Result: build completed successfully and created `docker.io/library/test`.

## Open items

Other .NET 3.1 or Debian buster based Dockerfiles may need the same archive-source handling if package installation is added or currently failing.

## Portable lesson

[`~/ai/general/knowledge/docker/debian-eol-apt-sources-archive.md`](../../../../general/knowledge/docker/debian-eol-apt-sources-archive.md)
