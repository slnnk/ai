---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, recovery, gitlab, acceptance]
---
# DevOps-892: controller job launch and credentialed GitLab checkout verified

## Task

Verify actual job launch and credentialed GitLab checkout within the user clarified recovery scope.

## Context

User explicitly replied «Да» to the proposed temporary cancelQuietDown action. test-git build was authorized for checkout-only acceptance. Restoring quiet mode requires a separate external-mutation approval and is not yet approved. Broader downstream infrastructure remains unavailable.

## Actions

Local helper ~/ai-data/jenkins-recovery/git-smoke.py uses Python3.12, does not output credentials/raw logs. POST cancelQuietDown returnedHTTP200; verified quietingDown=false and empty queue. POST /job/test-git/build returnedHTTP201, queue19115 and expectedbuild4. Read-only result inspection and final controller verification followed. No other job was launched; permanent recovery hook was unchanged.

## Findings

[test-git build4](https://build.youdo.sg/job/test-git/4/) completed SUCCESS in1130ms on the controller (builtOn empty). Revision a240575a6a360a908005fb3f1814fca13ee6e065 was checked out; fetch attempt and checkout revision were present with no Git authentication/network failure. This verifies actual job launch and credentialed GitLab checkout on controller only. AutoTest remains online with5executors; its actual checkout remains untested despite host DNS/HTTPS200 checks. Final verification: queue0, quietingDown=false and116active plugins.

## Changes

Authorized Jenkins state changes: temporary quiet-mode cancellation and checkout-only test-git build4. Local helper and KB log/map/TODO/index/sync-note updated. No repository task changes, deploy job, hook removal or quiet restoration occurred.

## Risks and limits

Quiet mode was subsequently restored after separate explicit user approval; current API verification is quietingDown=true. Permanent recovery hook remains and re-enables quiet mode on controller restart. Successful controller checkout does not verify AutoTest checkout or downstream functional workflows. Open work is tracked in ~/ai/TODO.md.

## Portable lesson

none

## Approved quiet-mode restoration

The user explicitly answered «Да» to restoring quiet mode after the successful smoke check. The helper checked the empty queue, issued POST /quietDown (HTTP200), then read /api/json?tree=quietingDown and confirmed true. No additional build was started; the persistent recovery hook remains unchanged. This supersedes the disabled-mode state recorded at smoke completion.
