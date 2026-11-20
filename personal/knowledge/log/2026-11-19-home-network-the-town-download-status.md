---
system: home-network
status: verified
checked: 2026-11-19
tags: [mediamanager, qbittorrent]
---
# Home network: The Town download status check

## Task

Check home-01 and investigate the MediaManager screenshot showing `error`
for The Town.

## Context

[Home network map](../systems/home-network.md#summary). MediaManager 1.12.3
uses the managed qBittorrent add-response compatibility bridge.

## Actions

Checked uptime, memory, filesystem, running services, kernel messages,
sanitized download events, the MediaManager database row and the qBittorrent
Web API for the same torrent hash.

## Findings

- MediaManager and PostgreSQL were healthy. qBittorrent and MiniDLNA were
  running. The media filesystem had 108 GiB free at 52% use.
- At 20:16 MSK, qBittorrent accepted the add. MediaManager immediately
  logged `No information found for torrent` three times within 270 ms.
  The lookup raced asynchronous registration. The same hash later appeared
  in qBittorrent and matched the MediaManager row, which had moved to
  `downloading` with `imported=false`.
- The Web API reported `downloading`, 3.9% of 25.66 GB, 9.56 MB/s and
  five connected seeds. The size of the incomplete file reflects allocation
  and is not proof of downloaded bytes.
- One qBittorrent log filter surfaced a Jackett API credential in diagnostic
  tool output. Credential values are omitted from this record.

## Changes

Read-only server diagnosis. No retry, restart, configuration or database
change was applied.

## Status and risks

All diagnostic operations finished. The user-started download remained active.
Completion, movie import and TV playback were outside the observed interval.
The transient registration race was identified and no repair was requested.

## Lampa torrent search diagnosis

The user reported that Lampa used the search text `The Town` and omitted
the desired extended BDRemux. Read-only inspection of the served application
confirmed the Jackett manual-results endpoint and that Lampa sends the
literal `Query` separately from movie metadata and category. The live
Jackett log recorded 94 releases for `The Town`, matching the reproduced
movie-card query. The RuTracker search returned 50 results for that broad
query, none matching the requested release. On the same Jackett endpoint
with Lampa movie parameters, `Город воров` returned 51 results and
`The Town 2010 BDRemux 1080p` returned four. Both included RuTracker's
`The Town [2010, BDRemux 1080p] (Extended cut)`, whose size matched the
existing download (25663293636 bytes). No configuration or download
operation was performed. TV search using the refined text was not observed.

## Portable lesson

none
