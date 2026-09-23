---
system: base-images
status: verified
checked: 2026-06-26
tags: [base-images, dockerfile, dotnet-6, dotnet-tool, nu1202, dotnet-trace, dotnet-monitor]
---
# base-images: dotnet diagnostics tools in .NET 6 images

Date: 2026-06-26
Repository: /home/slnnk/git/base-images

## Context

- Build command: docker build -t test -f microsoft/aspnet/6.0/Dockerfile .
- Failure occurs in SDK build stage while installing dotnet diagnostic tools.

## Findings

- microsoft/aspnet/6.0/Dockerfile installs dotnet-trace, dotnet-counters, dotnet-dump and dotnet-gcdump without --version.
- dotnet tool install resolves the latest NuGet package version. In the observed build, dotnet-trace resolved to 9.0.661903.
- dotnet-trace 9.0.661903 supports net8.0, while the build stage uses mcr.microsoft.com/dotnet/sdk:6.0, so restore fails with NU1202.
- The later runtime-stage apt/curl step is shown as CANCELED because BuildKit cancels parallel work after the build-stage failure; it is not the root cause in this log.

Next steps:
- Pin .NET 6 compatible versions of diagnostic tools in .NET 6 Dockerfiles, or build the tools using a newer SDK only if the resulting tools are compatible with the target runtime.
- Check sibling Dockerfiles microsoft/aspnet-6/6.0/Dockerfile and microsoft/aspnet/6.0-focal/Dockerfile; they use the same unpinned pattern.

## Actions

Update 2026-06-26:
- Checked NuGet flat-container indexes for dotnet-trace, dotnet-counters, dotnet-dump and dotnet-gcdump.
- Latest available 6.0-compatible package line found in all four indexes: 6.0.351802.
- NuGet API endpoints used:
  - https://api.nuget.org/v3-flatcontainer/dotnet-trace/index.json
  - https://api.nuget.org/v3-flatcontainer/dotnet-counters/index.json
  - https://api.nuget.org/v3-flatcontainer/dotnet-dump/index.json
  - https://api.nuget.org/v3-flatcontainer/dotnet-gcdump/index.json

## Changes

Implementation 2026-06-26:
- Updated microsoft/aspnet/6.0/Dockerfile build stage: added ARG DOTNET_DIAGNOSTIC_TOOLS_VERSION=6.0.351802.
- Pinned dotnet-trace, dotnet-counters, dotnet-dump and dotnet-gcdump installs to that ARG.
- Verified with: docker build -t test -f microsoft/aspnet/6.0/Dockerfile .
- Build succeeded; tools installed with version 6.0.351802.

Implementation 2026-06-26 for focal:
- Updated microsoft/aspnet/6.0-focal/Dockerfile build stage by analogy with microsoft/aspnet/6.0/Dockerfile.
- Added ARG DOTNET_DIAGNOSTIC_TOOLS_VERSION=6.0.351802.
- Pinned dotnet-trace, dotnet-counters, dotnet-dump and dotnet-gcdump to that ARG; current 6.0 Dockerfile also includes dotnet-monitor with the same ARG, so focal was aligned to it.
- Verified with: docker build -t test-focal -f microsoft/aspnet/6.0-focal/Dockerfile .
- Build succeeded. NuGet warning: exact dotnet-monitor 6.0.351802 was not found, approximate best match dotnet-monitor 6.1.0 was installed.

## Portable lesson

[`~/ai/general/knowledge/dotnet/dotnet-tool-install-nu1202-pin-diagnostic-tools.md`](../../../../general/knowledge/dotnet/dotnet-tool-install-nu1202-pin-diagnostic-tools.md)
