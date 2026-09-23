---
system: base-images
status: verified
checked: 2026-06-26
tags: [base-images, dockerfile, aspnet-10, review, diagnostic-tools, ca-certificates]
---
# base-images: microsoft/aspnet/10.0 Dockerfile review

## Task

- Date: 2026-06-26
- Repository: /home/slnnk/git/base-images
- Context: user asked for improvement suggestions for microsoft/aspnet/10.0/Dockerfile.

## Findings

Observed:
- Dockerfile is currently untracked in git status.
- Uses mcr.microsoft.com/dotnet/sdk:10.0.301-resolute as build stage and mcr.microsoft.com/dotnet/aspnet:10.0.9-resolute as runtime.
- Installs dotnet diagnostic tools without explicit versions.
- Installs ca-certificates, wget, curl, dnsutils, netcat-traditional and downloads Russian trusted CA certs from gu-st.ru.
- Unlike microsoft/aspnet/8.0/Dockerfile, it does not set ASPNETCORE_HTTP_PORTS=80 / ASPNETCORE_URLS=http://*:80 and does not install fonts/System.Drawing packages.

Potential improvements:
- Pin diagnostic tool versions or centralize them via ARGs for reproducibility.
- Add wget hardening: --https-only, --secure-protocol=TLSv1_2, retries/timeouts, certificate filename normalization, or checksum validation if checksums are available.
- Consider using curl only or wget only to reduce packages.
- Decide explicitly whether port 80 compatibility env vars are required for existing services; .NET 8+ official images default to 8080 unless overridden.
- Confirm whether fonts/libgdiplus/OpenSSL security-level compatibility from 8.0 image is still required.
- Consider labels/comments documenting why Russian root CA certs and netcat-traditional are included.
- Add build smoke test: docker build plus checks for dotnet tools and CA presence.

## Changes

Update 2026-06-26:
- Changed microsoft/aspnet/10.0/Dockerfile: combined five dotnet tool install RUN layers into one multiline RUN using apt-style && and backslash continuations.
- No image build was run for this small syntax-only Dockerfile edit.
- Replaced wget with curl for CA certificate downloads and removed wget from runtime package list.
- Formatted runtime apt package installation as a multiline list.
- Added comment documenting Russian root CAs requirement.
- curl remains in runtime intentionally as a debug tool.

## Open items

- The missing port-80 environment defaults later caused a health-check failure for a .NET 10 consumer; see [`2026-09-18-youdo-mcp-test-nomad-healthcheck.md`](2026-09-18-youdo-mcp-test-nomad-healthcheck.md).

## Portable lesson

[`~/ai/general/knowledge/dotnet/aspnet-container-default-port-8080-healthcheck.md`](../../../../general/knowledge/dotnet/aspnet-container-default-port-8080-healthcheck.md)
