---
system: base-images
status: verified
checked: 2026-06-26
tags: [base-images, dockerfile, dotnet-sdk-10, nbgv, nuget, review]
---
# base-images: microsoft/dotnet-sdk/10.0 Dockerfile review

## Task

- Date: 2026-06-26
- Repository: /home/slnnk/git/base-images
- File: microsoft/dotnet-sdk/10.0/Dockerfile

## Findings

Observed:
- Uses mcr.microsoft.com/dotnet/sdk:10.0-resolute.
- Installs nbgv into /tools without explicit version pin.
- Removes nuget.org source after installing nbgv.
- /tools is not added to PATH in this Dockerfile.

Review notes:
- Pin nbgv version for reproducible builds.
- Consider ENV PATH including /tools if nbgv is expected to be called as nbgv.
- Removing nuget.org after tool install is intentional if downstream restores must use only injected/corporate NuGet config, but document this because base image will otherwise have no public default source.
- If preserving source metadata matters, disable source instead of remove; remove is stricter.

## Changes

Update 2026-06-26:
- Combined nbgv installation and nuget.org source removal into one RUN command to reduce image layers.

## Portable lesson

none
