---
system: youdo-mcp
status: verified
checked: 2026-09-21
tags: [vault, openiddict, pfx, certificates, nomad, production, DevOps-861]
---
# youdo-mcp: OpenIddict PFX keys in Vault

## Task

Define and prepare the OpenIddict signing/encryption certificate secrets in Vault for the youdo-mcp production Nomad job (ticket `DevOps-861`).

## Context

- Date: 2026-09-21.
- Repository: `/home/slnnk/git/youdo-mcp`.
- Production runtime: Nomad job `youdo-mcp`, file `devops/production.hcl`.
- Vault path: `secret/dotnet/youdo-mcp`; standard Nomad policy `dotnet` grants `secret/dotnet/*`.
- Storage layout is consistent with Vault KV v1: Nomad template reads `.Data.OpenIddictSigningPfxBase64` and `.Data.OpenIddictEncryptionPfxBase64`.

## Findings

### Required keys

- `OpenIddictSigningPfxBase64`: base64 of a passwordless self-signed RSA-2048 PFX used for token signing.
- `OpenIddictEncryptionPfxBase64`: base64 of a separate passwordless self-signed RSA-2048 PFX used for token encryption.

For the initial pre-OAuth deployment both keys may contain non-empty placeholders so that the path and template fields exist. Replace both values with real, distinct certificates before OAuth stage T2.1. Do not store certificate payloads or private keys in tickets, Git, shell history, or this knowledge base.

Use `vault kv put secret/dotnet/youdo-mcp ...` to create/replace the record. This command replaces the complete record at that path, so preserve any unrelated existing fields if they appear later. Validate key names without printing values using JSON output piped to `jq` and selecting only `.data | keys[]` (KV v1).

Related checklist: `devops/DEPLOY-CHECKLIST.md`, ticket `DevOps-861`.

## Actions

### Generated certificates (2026-09-21)

Two distinct passwordless PFX files were generated locally for handoff to the operator. Both decode successfully and contain RSA-2048 keys.

- Signing certificate: valid 2026-09-21 through 2028-09-20; SHA-256 fingerprint `C8:66:E1:EC:2A:52:F0:D2:10:55:7F:99:6D:77:33:8A:24:F4:FE:41:13:2B:1B:EF:21:39:DF:5A:39:B1:45:6C`; critical key usage `Digital Signature`.
- Encryption certificate: valid 2026-09-21 through 2028-09-20; SHA-256 fingerprint `D0:A1:2B:FC:17:89:52:34:A0:E3:FC:27:D7:BB:08:D0:A5:0C:B2:DF:C2:D8:A1:21:F1:78:6A:B7:AF:A5:4D:E0`; critical key usage `Key Encipherment, Data Encipherment`.
- Pending: operator uploads both base64 payloads to Vault and removes the temporary local handoff directory afterward.

### Replacement certificates: 100-year validity (2026-09-21)

A replacement pair was generated as distinct passwordless self-signed RSA-2048 PFX payloads. The exact validity interval is 100 calendar years (36,524 days), from 2026-09-21 20:42:52 UTC through 2126-09-21 20:42:52 UTC.

- Temporary handoff directory: `/tmp/youdo-mcp-openiddict-100y-final.68VN7g` (mode `0700`). It contains only the two Base64 payload files, each mode `0600`; intermediate raw private keys, CSRs, certificates, and binary PFX copies were removed.
- Signing certificate fingerprint: `09:C9:A2:0D:70:CD:7B:70:13:88:25:7F:03:0E:40:BB:34:FF:77:94:8F:82:BA:36:0D:D1:77:2F:A1:EC:D8:5B`; critical key usage `Digital Signature`; critical basic constraints `CA:FALSE`.
- Encryption certificate fingerprint: `D3:5C:87:98:3D:81:FE:22:7D:10:41:9A:38:40:BE:27:0A:DB:8B:54:B6:85:12:C8:40:68:60:EF:EE:A7:1E:E8`; critical key usage `Key Encipherment, Data Encipherment`; critical basic constraints `CA:FALSE`.
- Both Base64 payloads were decoded and verified: the embedded private key matches the certificate public key, and each certificate has exactly one Basic Constraints extension.

## Open items

- Upload the replacement values to Vault and remove the temporary handoff directory after successful deployment verification.

## Portable lesson

none
