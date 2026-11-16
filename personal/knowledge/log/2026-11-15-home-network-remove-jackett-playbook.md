---
system: home-network
status: verified
checked: 2026-11-15
tags: [ansible, jackett]
---
# Remove obsolete Jackett VPS playbook

## Task and authorization
User confirmed Jackett now runs through home.yml and explicitly requested removal of the obsolete standalone playbook. Continued in the previously approved existing master checkout /home/slnnk/mygit/ansible; unrelated untracked files preserved.

## Changes
Removed playbooks/jackett.yml. Updated repository AGENTS.md and nginx, Docker and Jackett role READMEs to remove references and obsolete standalone VPS deployment instructions. Role jackett, home.yml and inventory unchanged.

## Verification
home.yml syntax check passed. No references to playbooks/jackett.yml remain in repository instructions, roles, playbooks or tests. File absence and whitespace check passed. Agent lint returned zero errors and one CDX-AG-005 warning on repository AGENTS.md. Initial sandbox sync state/network failures resolved by elevated sync.

## Status and risks
Local cleanup complete; no publication or deployment. No running background operations or remaining session requests. No task-related open backlog entry to close. Historical logs remain historical.

## Portable lesson
none
