---
system: home-network
status: verified
checked: 2026-11-15
tags: [docker, media, cleanup]
---
# PC media copies removed after home-server migration

## Task

The user corrected the stale old-IP follow-up: media services already run on the home server and the old PC copies may be stopped and deleted. This authorizes local cleanup only.

## Context

[Home network](../systems/home-network.md). The existing deployment and indexer migration records establish home-01 at 192.168.168.2 as the active media host. No home-server or router change was requested or made.

## Actions

Local Docker inspection found Jackett and TorrServer exited, FlareSolverr running, all with unless-stopped restart policies. Stopped FlareSolverr, removed the three containers with docker rm -v, removed their three image tags and image layers, and removed the empty home-media network. Deleted /home/slnnk/ai-data/jackett. The FlareSolverr anonymous volume was removed with its container.

## Findings

The local default Docker daemon now has no containers or images. The anonymous FlareSolverr volume no longer exists. No matching service launcher was found in the inspected systemd/autostart/cron locations; the user systemd directory does not exist. TorrServer data is root-owned: sudo -n failed because a password is required. Its approximately 120 KiB directory remains, including configuration, log and torrent metadata. No new privileged container or ownership workaround was attempted.

## Changes

Closed the obsolete old-PC-address task as superseded by home-server deployment and user confirmation. Tracked the remaining privileged local-data deletion in [central TODO](../../../TODO.md); closed it after user execution and local absence verification. Updated the current system-map endpoints and preserved historical deployment evidence.

## Status and risks

Runtime removal complete. Initially local file cleanup was partial; the command below required an authenticated local terminal:

```bash
sudo rm -rf -- /home/slnnk/ai-data/torrserver
```

User reported executing the command2026-11-15; local test confirmed the directory is absent. All authorized PC media removal is now complete. No task command or background operation remains running. Home-server playback diagnosis remains separate and unresolved. No remote health check or modification was made.

## Portable lesson

none
