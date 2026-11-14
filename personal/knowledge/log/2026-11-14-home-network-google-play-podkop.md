---
system: home-network
status: verified
checked: 2026-11-14
tags: [google-play, podkop, dns]
---
# Google Play downloads restored by podkop routing

## Task

Investigate Google Play application downloads failing on the home network.
The user closed the preceding VK advertising discussion without requesting
further testing; that issue must not remain an active diagnostic task.

## Context

Cudy/podkop selective routing and the existing VPS AdGuard Home resolver.

## Actions

Read-only SSH inspected live user rules and summarized Google-related DNS logs,
without printing client addresses. The command exited successfully. Asked about
the download symptom and comparison with mobile Internet; those questions became
unnecessary when the user reported a successful routing change.

## Findings

User rules contain only ||ad.mail.ru^ and ||an.yandex.ru^. Observed requests for
play.googleapis.com, play-fe.googleapis.com, android.clients.google.com and
multiple gvt1.com download hosts had no blocking rule recorded. Some advertising
hosts were blocked. This is bounded log evidence, not proof that DNS never fails.

The user enabled Google Play in podkop and confirmed downloads now work.
This supports a routing/path problem as the working explanation; exact direct
path failure, selected domains and packet-level behavior were not verified.

## Changes

The user changed router routing. The agent made no runtime or repository changes.
Updated this log and the existing home-network map only.

## Status and risks

Resolved based on user confirmation. No further diagnosis requested or scheduled,
no new backlog item required. All diagnostic commands exited and no task background
operations remain. Earlier VK discussion is closed without claiming complete ad
removal or verifying the user's manual rules across all clients.

## Portable lesson

none
