---
system: nginx
status: verified
checked: 2026-11-15
tags: [ansible, robots]
---
# nginx default robots policy

## Task
Add an exact robots.txt location denying all crawlers by default; inventory may disable it or supply custom content.

## Context and approval
Existing checkout /home/slnnk/mygit/ansible, master at b857c7e. Proposed reuse of master from current HEAD; user approved implementation. Existing untracked files preserved. Publication and deployment were not requested.

## Changes
Role nginx defaults, argument specs, validation, HTTP template and README; repository AGENTS.md documents the policy. nginx_robots_enabled defaults to true; nginx_robots_content defaults to User-agent wildcard and Disallow slash on separate lines. Host/group vars override these inputs. Exact location also applies to HTTP redirect sites; custom templates must implement the policy explicitly.

## Verification
Local nginx syntax and real HTTP status/body checks passed for defaults, disabled handling and custom text including quotes and backslash. Fixture nginx processes stopped. VPN, relay and DNS syntax checks passed. Jackett syntax check stopped because inventory has no jackett group. Agent lint: zero errors, one CDX-AG-005 warning on repository AGENTS.md. Initial sandbox checks failed on Ansible temporary-directory access; elevated local checks provided the results above.

## Status and risks
Local implementation complete. No publication, deployment or background operations. No additional session action requested; no task-specific TODO entry requires reconciliation. Server behavior remains unverified until a separately authorized deployment.

## Portable lesson
none
