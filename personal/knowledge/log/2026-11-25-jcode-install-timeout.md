---
system: jcode
status: verified
checked: 2026-11-25
tags: [linux, install]
---

# Jcode v1.1.2 installation on Linux

## Task and findings

The installation stopped showing progress after `launcher: /home/slnnk/.local/bin/jcode`. The initial request for the script completed. At that point the script next requests `/releases/v1.1.2/download-bases` and downloads the release asset. Both use silent curl with a connection timeout and no total transfer timeout. The download-bases probe returned a partial HTML page and hit the explicit 30-second timeout in this run. The exact command state during the original attempt was unavailable. [Installer](https://jcode.sh/install)

## Actions and verification

Downloaded the Linux x86_64 tarball and SHA256SUMS directly from GitHub. The archive passed `sha256sum -c`. Extracted and ran the launcher from a scratch directory, then installed the checked launcher and its companion ELF into `~/.jcode/builds/versions/1.1.2`. Used the official stable symlink layout through `~/.jcode/builds/stable/jcode` and `~/.local/bin/jcode`. The login shell already includes that directory on PATH. [Release v1.1.2](https://github.com/1jehuang/jcode/releases/tag/v1.1.2)

## Status

A fresh login shell resolved the launcher and printed `jcode v1.1.2 (4f874c9ea)`. This verifies local installation and CLI startup. Provider login was outside the request. No pending installation steps or background operations.

## Task metrics: jcode-v1.1.2-install-linux-2026-11-25

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "jcode-v1.1.2-install-linux-2026-11-25",
  "created": "2026-11-25T00:32:36.830768+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "investigation",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "GitHub release checksum verified and new login shell ran jcode --version.",
  "updated": "2026-11-25T00:32:36.830815+03:00"
}
```
