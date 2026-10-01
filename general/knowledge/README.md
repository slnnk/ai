# Knowledge base rules and templates

Read `~/ai/AGENTS.md` first. This file holds the details that do not need to be in every
session's context.

## Layers

| Layer | Path | Lifetime | Contains |
| --- | --- | --- | --- |
| general | `~/ai/general/` | forever | technology recipes, portable skills, scripts, prompts |
| personal | `~/ai/personal/` | forever | the user's own servers, VPN, side projects |
| company | `~/ai/companies/<name>/`, active one via `~/ai/current` | one employer | system maps, work log, repos, company skills, `.env` |

Test for `general/`: could this file be pushed to a public repository right now? If it names
a company, a host, an IP, an internal URL, a ticket, a person or a secret, it cannot.

Inside `general/knowledge/` group by technology: `docker/`, `nomad/`, `gitlab-ci/`, `k8s/`,
`ansible/`, `terraform/`, `dotnet/`, `postgresql/`, `mssql/`, `linux/`, `android/`, ...
One recipe per file, `<topic>-<slug>.md`, no date in the name; the date lives in `checked`.

## Frontmatter

    ---
    system: <system name, or technology for general/>
    status: verified | hypothesis | outdated
    checked: YYYY-MM-DD
    tags: [optional, keywords]
    ---

`build_index.py` reads these fields. A note without frontmatter is listed under
"Missing frontmatter" in `INDEX.md` until fixed.

## Template: log entry (`knowledge/log/YYYY-MM-DD-<system>-<slug>.md`)

    ---
    system: nomad
    status: verified
    checked: 2026-09-22
    tags: [incident, canary]
    ---
    # Nomad: canary rollback stuck on <service>

    ## Task
    One paragraph: what was asked, ticket, environment.

    ## Context
    Repositories, hosts, jobs, pipelines involved. Links to system maps.

    ## Actions
    What was done, in order. Key commands in code blocks.

    ## Findings
    Verified facts. Hypotheses marked as such.

    ## Changes
    Files, configs, roles, playbooks, services, MRs.

    ## Open items
    Risks and next steps as of this date. Actionable items also go to `~/ai/TODO.md`.

    ## Portable lesson
    Link to `general/knowledge/...` if one was written, otherwise "none".

## Template: recipe (`general/knowledge/<technology>/<slug>.md`)

    ---
    system: docker
    status: verified
    checked: 2026-06-26
    tags: [apt, ppa, gpg]
    ---
    # add-apt-repository fails with "retrieving gpg key timed out"

    ## Symptom
    ## Cause
    ## Fix
    Minimal reproducible commands or config.
    ## Limits
    Where the fix does not apply, side effects, versions checked.

## Template: system map (`knowledge/systems/<system>.md`)

A living document for one system, updated in place. Sections; drop those that do not apply.

    # <System>

    ## Summary
    Required once the note grows over ~8 KB (kb_lint warns): 10-15 lines on what the
    system is, how it works, current state, main risks, and which section to read for what.
    ## Purpose
    ## Components
    Repositories with purpose: product code, autotests, shared test libraries, CI/CD,
    infrastructure config, Ansible roles and inventory, Helm/Terraform, helper services.
    ## Delivery path
    From code change to running service or test report: build, artifact, registry,
    delivery to environment, launch, tests, report, log storage.
    ## Control points
    CI project and job, runner, orchestrator, server, systemd unit, container, port,
    queue, schedule or manual command.
    ## Operations
    Per component: where to check status, config, logs; network and service
    dependencies; safe basic diagnostics.
    ## Boundaries
    What belongs to the system; what sits nearby but serves other purposes.
    ## Access
    Route only: bastion, VPN, inventory, role, service account, panel, vault path.
    Never the secret.
    ## Related log entries
    Newest first.

Separate verified facts, working hypotheses and outdated data. For changing data give
the date of the last check and update the map when repository and reality disagree.

## Template: Android device farm map

Extends the system map for Android autotest infrastructure. Cover where possible:

- app repository: branches and build variants, where APK/AAB is produced;
- autotest repository: frameworks, shared libraries, suite files, launch parameters,
  retry rules for failed tests;
- CI/CD project, pipeline/job, runner, variables selecting the stand, app version,
  Selenium/Grid and the Appium host set;
- APK source, publishing and download path, installation on device and dependencies
  (Nexus/registry/object storage, DNS, routing, credentials by reference only);
- execution chain: CI runner -> Selenium/Grid -> Appium node -> ADB -> emulator or device;
- farm machines: roles, inventory/host_vars, Appium and emulator services, ports,
  `systemPort`, logs, health-check commands;
- devices: ADB serial/UDID, model, vendor, Android version, host, service unit, special
  constraints; no unnecessary personal data;
- device preparation: boot and ADB authorization, wake/unlock, orientation, system panels
  and overlays, permissions, helper package install/removal, state cleanup;
- vendor firmware quirks affecting tests: power saving, process freezing, autostart,
  system shades, security apps, non-standard SystemUI;
- paths to reports, screenshots, page source, CI artifacts, Appium journal, logcat and
  host system logs;
- verified recovery procedure, criteria for returning a device to the Grid, rollback for
  non-standard changes.

## repos.md

One table per layer, one row per local clone: absolute path, origin without credentials,
purpose, related system, date checked. Link related clones in the system map
(app <-> autotests <-> infrastructure <-> shared library <-> docs). Extend the registry
gradually while working; do not crawl the whole filesystem.

## Scripts

| Script | Purpose |
| --- | --- |
| `general/scripts/new_note.py log\|system\|recipe ...` | create a note with correct path, name and frontmatter |
| `general/scripts/kb_find.py <keywords>` | compact search: path, system, status, checked, title and matching lines per note |
| `general/scripts/token_usage.py [--days N] [--kb] [--brief]` | token totals of Claude Code and Codex sessions per project/model, top sessions; `--kb` counts how agents read the knowledge base (kb_find, search, INDEX, full vs partial reads); run weekly by `ai-sync.sh` into `personal/usage/` |
| `general/scripts/kb_lint.py [--staged]` | check frontmatter, log names, links, secrets, company identifiers in `general/`, language, missing `## Summary` in long maps and recipes, `AGENTS.md` over 5.5 KB |
| `general/scripts/build_index.py` | rebuild `INDEX.md` in every layer; `--stale 30` lists notes due for review: maps older than 30 days, recipes older than `--recipe-days` (180), all `hypothesis`; `--count` prints the number |
| `general/scripts/ai-sync.sh` | once-a-day lint, index, commit and push; weekly token usage report (see below) |

Company identifiers that must never appear in `general/` are listed one per line in
`companies/<name>/lint-identifiers.txt`; private IP ranges and `*.corp` hosts are checked
by default. Use RFC 5737 addresses (192.0.2.x, 198.51.100.x, 203.0.113.x) in recipes.

Prompts for recurring jobs live in `general/prompts/` (`normalize-notes.md`,
`extract-recipe.md`).

## Indexes

`python3 ~/ai/general/scripts/build_index.py` rewrites `knowledge/INDEX.md` in every
layer (`general`, `personal`, `current`). Run it after adding or renaming notes.

## Daily sync

`~/ai/general/scripts/ai-sync.sh` is called by agents at the start of every task. On the
first call of a day it rebuilds indexes, commits everything, pulls with rebase and pushes to
all remotes, then writes the date to `~/ai/.last-sync`. Later calls the same day exit at once.

The commit subject lists the touched areas (`Sync 2026-09-24: youdo, general/linux`). The body
starts with the lines agents appended to `~/ai/.sync-notes` after each piece of work
(`- nomad-test: root disk full on agent-test-01, dnsmasq log-queries; recipe added`), then
lists every changed note with its title. `.sync-notes` is emptied after the commit; both
state files are per machine and ignored by git. `--force` runs
regardless of the date, `--dry-run` shows what would be committed, `--status` prints the
last sync date. A failed push leaves the commit local and the state file untouched, so the
next call retries. Agents never run `git commit` in `~/ai` themselves.

`~/ai` is one private repository; `origin` fetches from GitHub and pushes to both GitHub and
GitFlic (a separate `gitflic` remote also exists).
The company layer and the `current` symlink are tracked in it; `.gitignore` holds only `.env`
and the sync state files. Do not ignore `companies/` or split it into a nested repository.

Monthly staleness review: on the first sync of a month with notes due, `ai-sync.sh` adds
`Monthly staleness review YYYY-MM` to `TODO.md` "Knowledge base" and prints a reminder. The
agent offers the review to the user; checks are read-only.

Dated reminders: an open `TODO.md` item written as `- [ ] due YYYY-MM-DD: ...` is printed by
`ai-sync.sh` as `reminder:` on every daily sync from that date until the item is closed.

## Connecting an agent

Agent-specific directories (`~/.codex`, `~/.claude`, `~/.gemini`) hold only symlinks into
`~/ai` plus the agent's own runtime state.

- Instructions: symlink to `~/ai/AGENTS.md` from `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`,
  `~/.gemini/GEMINI.md`.
- Skills: one symlink per directory from `~/ai/general/skills/` and `~/ai/current/skills/`
  into the agent's skills folder (`~/.codex/skills/`, `~/.claude/skills/`).
- Switching employer: create `companies/<new>/`, repoint `current`, redo skill symlinks.
