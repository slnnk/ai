---
system: base-images
status: verified
checked: 2026-06-26
tags: [base-images, harica, ca-certificates, openssl, docker, verification]
---
# HARICA root CA check for changed base images

Date: 2026-06-26
Repository: /home/slnnk/git/base-images

## Task

User requested verification that all Docker images with git changes contain `harica_tls_rsa_root_ca_2021` after build.

## Context

Changed image Dockerfiles checked:
- microsoft/aspnet-6/6.0/Dockerfile
- microsoft/aspnet/10.0/Dockerfile
- microsoft/aspnet/6.0-focal/Dockerfile
- microsoft/aspnet/6.0/Dockerfile
- microsoft/aspnet/8.0/Dockerfile
- microsoft/aspnet/8.0-libreoffice/Dockerfile
- microsoft/dotnet-aspnet/5.0/Dockerfile
- microsoft/dotnet-aspnet/6.0/Dockerfile

Relevant git change: `microsoft/dotnet-aspnet/5.0/harica_tls_rsa_root_ca_2021.crt` is deleted; HARICA now comes from the `ca-certificates` package/base distribution rather than an explicit COPY.

## Actions

Build notes:
- Built with Docker from repo root using each changed Dockerfile.
- Used `--pull=false` and Docker cache where available.
- Tagged `microsoft/aspnet/8.0` as `registry.youdo.sg/youdo/base-images/microsoft/aspnet:8.0` so `microsoft/aspnet/8.0-libreoffice` inherited the freshly built local base image.

Verification command shape:
- Ran each image with Docker and scanned `/etc/ssl/certs/*.pem` and `/usr/local/share/ca-certificates/*.crt`.
- Parsed subjects with `openssl x509 -in "$file" -noout -subject`.
- Searched for `HARICA TLS RSA Root CA 2021`.

## Findings

Result:
- All eight changed images contain `/etc/ssl/certs/HARICA_TLS_RSA_Root_CA_2021.pem`.
- Subject observed: `C = GR, O = Hellenic Academic and Research Institutions CA, CN = HARICA TLS RSA Root CA 2021` (spacing varies by OpenSSL/base image).

## Open items

Risks/TODO:
- This confirms the locally built result on 2026-06-26. Future base image or package repository changes should be rechecked, especially for EOL .NET/Debian images.
- Background on which Debian releases ship this root: [`2026-06-23-base-images-dotnet-aspnet-5-harica-ca.md`](2026-06-23-base-images-dotnet-aspnet-5-harica-ca.md).

## Portable lesson

[`~/ai/general/knowledge/docker/verify-root-ca-present-in-image.md`](../../../../general/knowledge/docker/verify-root-ca-present-in-image.md)
