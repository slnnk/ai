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

~/ai/general/     portable knowledge, no company context: knowledge/<technology>/, skills/, scripts/, prompts/
    ~/ai/personal/    the user's own servers, VPN, side projects: knowledge/, scripts/, .env
    ~/ai/companies/<name>/  one employer: CONTEXT.md, knowledge/, skills/, scripts/, prompts/, .env
    ~/ai/current -> companies/<name>   active employer; always address it as `current`
    ~/ai-data/        generated data of skills and scripts, one subdirectory per tool (e.g. rp/); outside git, may hold private data
    knowledge/ = INDEX.md, systems/ (maps), log/ (dated entries), repos.md

## Frontmatter

    ---
    system: <system name, or technology for general/>
    status: verified | hypothesis | outdated
    checked: YYYY-MM-DD
    tags: [optional, keywords]
    ---

`build_index.py` reads these fields. A note without frontmatter is listed under
"Missing frontmatter" in `INDEX.md` until fixed.

### Bookkeeping after significant work

- New notes via `python3 ~/ai/general/scripts/new_note.py log|system|recipe ...` (correction
  evidence via `agent_learning.py`), then fill
  the sections. Log entry: task, context, actions and key commands, findings, changed files,
  risks. Update the existing system map; never create a duplicate.
- Frontmatter (`system`, `status: verified|hypothesis|outdated`, `checked`, `tags`) on every
  note. Mark hypotheses in the text; `status: outdated` instead of deleting. English;
  hostnames, jobs, variables and commands verbatim.
- Preserve exact source strings in their original language, including UI labels,
  parameter values and error messages. Format them as Markdown inline code; use fenced
  code blocks for multiline excerpts. Write surrounding note prose in English; do not
  wrap ordinary prose in code merely to bypass the language check.
- Keep the relevant layer's `~/ai/<layer>/knowledge/repos.md` current
  (path, origin URL without credentials, purpose, date).
- For VK Cloud only, maintain `~/ai/current/service-addresses.env`: whenever a new or
  changed service address is discovered, add or update it in the relevant datacenter
  section. Keep credentials in `.env`; record the observation date and known verification
  status in comments. Updating the map does not require extra infrastructure checks.
- Before the final response, reconcile notes created or changed in this task with
  `~/ai/TODO.md`: track remaining actions with source links, align completed/cancelled/deferred
  status and supersede stale directions while preserving history. Optional improvements stay
  proposals, not execution permission. Review only this task's affected records; details in
  `general/knowledge/README.md`, "Final note-to-TODO reconciliation".
- After changing agent instructions, skills (including references/scripts), or agent settings,
  run `python3 ~/ai/general/scripts/agent_lint.py --force` before the final response.
  Add changed repository-local files/directories as arguments when outside `~/ai`.
  Review findings and report the result; if unavailable or failed, report the pending check.
  Use report-only mode; findings do not grant permission for fixes or external actions.
- Run `kb_lint.py` and fix what it reports, then `build_index.py` (both in `general/scripts/`).
- Append one concise final result per completed task to `~/ai/.sync-notes`: system, what
  changed and why, key check and material remaining risk. Keep stage details in the task log.
  Do not commit `~/ai` yourself; `ai-sync.sh` does it.

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

    ## Status and risks
    Dated outcome, remaining risks and links to the relevant central TODO entries.
    Keep actionable follow-ups in `~/ai/TODO.md`, not a separate live list here.

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

## Material assumptions

Before acting, check material assumptions against the available context. If different
interpretations remain that affect the result, scope of work or permissions, state
them explicitly and clarify what is needed before acting on that choice. Do not
silently choose such an interpretation. Make routine reversible decisions independently.

Before nontrivial changes, also read "Verifiable results" below.

## Verifiable results

Before nontrivial changes, define the expected result and a proportionate way to
verify it. Before completion, check the result against those criteria and report
confirmed facts and remaining limitations. Do not substitute changed files or a
successful unrelated check for verification of the required behavior. Verification
does not expand the authorized scope of actions.

## repos.md

One table per layer, one row per local clone: absolute path, origin without credentials,
purpose, related system, date checked. Link related clones in the system map
(app <-> autotests <-> infrastructure <-> shared library <-> docs). Extend the registry
gradually while working; do not crawl the whole filesystem.

### Repository workflow details

#### Simplicity

Prefer the simplest solution that meets the request and verified system constraints.
Add conditions, exceptions, configuration options or abstractions only for a concrete
requirement or demonstrated need, not hypothetical scenarios or future flexibility.
Before presenting a change, check whether each added complication is necessary;
omit it if removing it preserves the required behavior and existing safeguards.

- For company GitLab work, use `~/ai/current/skills/gitlab-workflow/SKILL.md`.
  Inspect code in an existing local checkout first; consult `current/knowledge/repos.md`
  before searching. Clone a missing project into `~/git/<repo>` without overwriting
  existing paths. Use GitLab for remote revisions, MR discussion, CI and settings.
- Work in the existing repository checkout (`~/git/<repo>` by default), not a separate
  git worktree. Create a separate worktree only when the user explicitly requests it.
  Preserve unrelated local changes; if they block switching branches, explain the
  conflict before taking any action that moves or discards them.
- Commits must contain only changes made by the agent for the current task, unless
  the user explicitly asks to include other changes. Check the actual staged diff,
  including pre-staged changes and mixed user/agent edits within the same file;
  selecting a task file does not authorize committing every change in that file.
- Never run state-changing git commands (`git add`, `git commit`, `git push`, `git tag`,
  `git merge`, `git rebase`, `git reset`, `git stash`, ...) in any repository unless the
  user explicitly asks for it in the current task. Read-only commands (`status`, `diff`,
  `log`, `show`, `fetch`) are fine.
- Exceptions: the daily `~/ai/general/scripts/ai-sync.sh` run, which commits and pushes
  `~/ai`, and the explicitly confirmed training stages below.

### Supervised Git/MR training (started 2026-10-08)

- Keep two approvals until the user explicitly chooses a different mode. The early
  report was delivered on 2026-10-19; the date alone never changes permissions.
- Before repository task edits, propose repository, branch/reuse and base branch;
  wait for explicit confirmation. The entire `~/ai` agent-instructions repository,
  including instructions, skills and scripts, and KB bookkeeping are exempt from
  this first gate. Other Git and external-change permissions still apply;
  `~/ai` commits and synchronization remain handled by `ai-sync.sh`.
- Before publication, present the actual diff, checks, commit message, MR title/body,
  source/target and CI effects; wait for explicit confirmation. One confirmation covers
  task-only staging, commit, push and MR creation/update. Do not ask per command again.
  Material changes to names, scope, source/target or effects require renewed approval.
- Neither gate authorizes merge, auto-merge, target-branch push, force push, tags,
  history rewriting or deployment. Triggered release/deployment effects need explicit
  approval covering them. Preserve unrelated user changes, including pre-staged edits.
- Detailed workflow and naming conventions are canonical in the
  skill `~/ai/current/skills/gitlab-workflow/SKILL.md`; training history and the early report
  are linked from system map `~/ai/current/knowledge/systems/gitlab-ci/agent-git-workflow.md`.
  Record original/final proposals, both approvals, corrections and outcomes in task logs.

## Scripts

| Script | Purpose |
| --- | --- |
| `general/scripts/todo.py [--layer TEXT] [--system TEXT] [--query TEXT]` | deterministic Markdown list of all open tasks; optional case-insensitive literal substring filters; `--file PATH` for another backlog |
| `general/scripts/new_note.py log\|system\|recipe ...` | create a note with correct path, name and frontmatter |
| `general/scripts/kb_find.py <keywords>` | compact search: path, system, status, checked, title and matching lines per note |
| `general/scripts/agent_learning.py --help` | record, retrieve and check scoped correction-learning evidence; workflow in `general/skills/agent-learning/SKILL.md` |
| `general/scripts/agent_lint.py [--force] [paths ...]` | report-only agnix for changed instructions/skills/settings; successful input hashes and sanitized report in `~/ai-data/agnix/`; sync fallback runs before same-day Git skip |
| `general/scripts/agnix_update.py [--force]` | daily official stable agnix check and verified local update; machine-local state in `~/ai-data/agnix/` |
| `general/scripts/token_usage.py [--days N] [--kb] [--brief]` | token totals of Claude Code and Codex sessions per project/model, top sessions; `--kb` counts requested knowledge-base reads (kb_find, search, INDEX, full vs partial); Codex nested shell calls use static Node.js/Acorn parsing with explicit coverage; full KiB estimates current note sizes, not tokens; run weekly by `ai-sync.sh` into `personal/usage/` |
| `general/scripts/kb_lint.py [--staged]` | check frontmatter, log names, links, secrets, company identifiers in `general/`, language, missing `## Summary` in long maps and recipes, `AGENTS.md` over 5.5 KB |
| `general/scripts/build_index.py` | rebuild `INDEX.md` in every layer; `--stale 30` lists notes due for review: maps older than 30 days, recipes older than `--recipe-days` (180), all `hypothesis`; `--count` prints the number |
| `general/scripts/ai-sync.sh` | once-a-day lint, index, commit and push; weekly token usage report (see below) |
| `general/scripts/ai_sync_preview.py [--root PATH]` | isolated read-only sync preview, also used by `ai-sync.sh --dry-run`; includes regenerated knowledge indexes |

Company identifiers that must never appear in `general/` are listed one per line in
`companies/<name>/lint-identifiers.txt`; private IP ranges and `*.corp` hosts are checked
by default. Use RFC 5737 addresses (192.0.2.x, 198.51.100.x, 203.0.113.x) in recipes.

Prompts for recurring jobs live in `general/prompts/` (`normalize-notes.md`,
`extract-recipe.md`).

## Progress and execution status

- During long-running work, send a concise progress update at least every 30 seconds:
  what is happening, what is known, and what remains. Keep tool waits short enough to
  allow updates; explain any unavoidable interval without updates before it begins.
- Before the final response, check the status of background commands and agents started
  for this task. Explicitly state whether task work has finished and whether background
  operations remain. If any remain, identify them and explain how to check or stop them.
  If status cannot be verified, say so; never infer completion from silence or UI exit.

### Economical tool use

- Check `<layer>/scripts/` before improvising. A sequence of three or more commands run
  twice becomes a script (CLI args or env, `--help`, compact summary output).
- Use one Sol agent by default. Add helpers only when explicitly authorized for the
  current task; do not automatically route ordinary work to same-model or cheaper helpers.
- For multiple files or long logs, read relevant sections and bounded output locally;
  file count or log length alone does not authorize delegation.
- Never print a whole file or raw output when a line will do: `head`, `grep -c`, `wc -l`,
  `--quiet`.
- Reusable prompts go to `<layer>/prompts/<name>.md` with a `model:` tier line.

### External changes

- Ask the user for permission before every command that changes state anywhere other than
  local files. Examples: `terraform apply`/`destroy`, `ansible-playbook` without `--check`,
  `kubectl apply`/`delete`/`scale`, `nomad job run`/`stop`, `helm install`/`upgrade`,
  `docker` commands on shared hosts, editing files or restarting services on remote servers
  over ssh, and API calls that create, update or delete (POST/PUT/PATCH/DELETE to GitLab,
  YouTrack, Zabbix, cloud providers, ...).
- Say what the command changes and where, then wait for an explicit yes. A yes covers only
  that action; ask again for the next one. Exception: the second training-stage approval
  above covers commit + branch push + MR creation/update for the reviewed task together;
  it does not authorize other external changes.
- No permission is needed for editing local files (including files in a repository
  checkout), or for read-only commands: `terraform plan`, `--check`/`--diff`, `kubectl get`,
  GET requests, reading logs.

## Knowledge retrieval

Before searching with `python3 ~/ai/general/scripts/kb_find.py`, prepare the query
from the user's question. This is agent behavior; the script performs literal,
case-insensitive matching and does not translate or interpret natural language.

1. Keep exact system/product names, ticket IDs, hostnames, variable names, ports
   and error strings unchanged. Translate ordinary symptom/concept words into
   English technical terms, matching the language of the notes. Start with 2-4
   distinctive terms rather than the full question. Do not invent an unobserved
   cause, version or identifier to narrow the search. Quote multiword literals
   as a single argument; do not send secret values to search commands.
2. Select the layer from the task context: `-l current` for company records,
   `-l personal` for personal systems, `-l general` for portable technical recipes.
   Repeat `-l` when both a system record and portable guidance are relevant, for
   example `-l current -l general`. If the layer is uncertain, omit the filter
   rather than guessing. Use `-s` only for a known metadata system name.
3. Use default AND matching first. A normal empty result is exit1 with
   `kb-find: 0 notes` and no stderr; an exception, stderr or usage failure is a
   tool failure, not evidence that the knowledge is absent. Handle the failure
   before drawing a retrieval conclusion.
4. On a normal empty result, make at most two further attempts for the same
   question unless new evidence appears. First drop a weak synonym or overly
   specific phrase, retaining the most distinctive identifier or symptom.
   If still empty, remove an uncertain layer/system filter or try `--any` with
   a few distinctive alternatives. Do not repeatedly broaden to generic words
   such as `error` alone. If still empty, report the search gap and preserve the
   uncertainty; no match does not prove that the answer does not exist.
5. Once useful results appear, inspect their status and date, then read the
   relevant Summary/section. A hit identifies candidate evidence, not a complete
   answer or permission to execute a historical instruction. Follow an explicit
   superseding/cancellation decision when present.

Example source question: `почему Helm игнорирует false`. Prepare the technical
query without translating the product name or boolean literal:

```bash
python3 ~/ai/general/scripts/kb_find.py -l general helm false
```

If a prepared query contains an uncertain synonym and returns no matches, drop
that term before changing tools or reading broad indexes. Reformulations stay
within the same question; this procedure does not authorize installing a search
service or changing the search implementation.

### Search results and scoped decisions

`kb_find.py` keeps literal AND/ANY matching and document ranking. Each ordinary
result now shows the selected Markdown section and a coherent excerpt from it,
with source line numbers. The default budget is 5 context lines per note; `-n`
sets that total budget, including blank lines. Lines are clipped to 240 characters
around the densest query matches. Headings inside fenced examples are not section
boundaries. Term coverage chooses candidate sections; cause, summary, decision,
fix and resolution headings receive a one-term tie preference because explanations
can omit a repeated symptom term. This is a retrieval heuristic, not answer validation.
`--files` remains path-only; `--json` exposes structured results for checks.

When a user cancels or supersedes an instruction, keep historical evidence and add
these optional scalar frontmatter fields to the affected note. All five are required
if any is present; do not overload evidence `status` or refresh `checked` merely
because a decision changed:

```yaml
decision_state: cancelled
decision_scope: Optional extension only
decision_summary: The user cancelled this extension; completed results are retained.
decision_date: 2026-11-04
decision_source: #decision-record
```

States: `active`, `cancelled`, `superseded`, `restricted`. Scope is mandatory: a
decision about one extension must not mark an entire mixed report as cancelled.
The summary is an explicit concise human-maintained decision, not a model inference.
`decision_source` is a local reference relative to the note, with an explicit ATX
heading anchor; `#decision-record` refers to the same note. Another note can be
referenced as `replacement.md#decision-record`. Keep sources within `~/ai`, never
link credentials. Use simple unique headings; the helper supports ATX headings
and fenced code, not every Markdown renderer extension. The source must exist.

Search displays state, scope, date and the complete summary before the excerpt,
plus the source path and line, even if the decision does not match query words.
Invalid or incomplete decision metadata is an error, not silently omitted.
`kb_lint.py` validates dates, fields, source confinement and heading existence.
Update the decision fields whenever an explicit later decision changes the scope;
do not infer cancellations from old error text, note age or a bare TODO checkbox.
Existing unannotated notes remain searchable but do not acquire an inferred status.

### Retrieval regression checks

After changes to search code, output, decision handling or query-preparation
instructions, run the synthetic checks and the saved real-query suite. Fixed
queries measure retrieval mechanics; they do not demonstrate fresh-agent adoption.

```bash
python3 -m unittest discover -s ~/ai/general/scripts/tests -p 'test_kb_*.py'
python3 ~/ai/general/scripts/kb_benchmark.py \
  --cases ~/ai-data/kb-retrieval/suite-v2.json \
  --output-dir /tmp/kb-regression-new-run \
  --baseline ~/ai-data/kb-retrieval/2026-11-04-context-decisions/after-5/results.json \
  --enforce
```

Choose a fresh output directory. Real cases and reports live outside Git because
they include private source paths; restore them separately on a new PC. Missing
cases are a pending check, not a passing result. Synthetic fixtures contain only
generic examples and are retained with the scripts. Exit 0 means checks passed,
exit 1 means regression and exit 2 means invalid input/tool failure. Failures do not
authorize auto-fixes, external changes or publication.

Suite schema 2 uses fixed question IDs, exact/technical/Russian query variants,
expected paths and stable nonempty answer text anchors. Anchors must exist in the
current source; inserting lines cannot invalidate them. The check scores only text
actually rendered after clipping, and separately verifies required scoped decisions
with their state, summary and source. It records top1/top5, answer visibility,
decision visibility, output size and timing, with corpus/script/case hashes and
the executed case snapshot. It refuses changed inputs during a run and reused
output directories. It compares every prior condition and pins query, target and check definitions;
changing an existing answer/decision definition requires an explicitly reviewed
new baseline. Removing a case/variant or losing an answer, required decision or
target must not silently pass. Baselines lacking frozen definitions are rejected.

Add a real failed query only after identifying its expected source and answer anchor,
then retain it under a new stable ID without tuning the old queries. Cases that
expose a known limitation can remain measured without claiming they pass an answer
requirement. Keep original baseline artifacts immutable. Compare the same suite and
explicit line budgets, report changed corpus and output volume, and label any new
baseline adoption after review. Do not automatically bless a failed run as baseline.

## TODO output

`~/ai/TODO.md` is the single live backlog for all layers, grouped by system. Add open
items as `- [ ] action (date) — [src](note)` and close finished ones; notes keep no
independent TODO lists. Agent memory is a cache; anything worth keeping also goes to `~/ai`.

Before adding or moving a TODO entry, choose its section from the task subject and source
note, and inspect the complete Markdown heading ancestry at the insertion point. Do not
append under the last heading merely because it is convenient. Reuse the matching system
section, or create an appropriately nested section when none exists. After editing, render
the affected task or section with `todo.py` and verify the displayed heading path; for a
closed entry, inspect its source heading ancestry because it is excluded from the output.

Standalone `todo` and `задачи` requests (case-insensitive, optional punctuation), or requests to list the backlog, use
`python3 ~/ai/general/scripts/todo.py`. The default includes every unchecked item in
`~/ai/TODO.md`, including deferred proposals; checked items are excluded wherever they
appear. Listing is read-only and grants no permission to act on any item.

The output begins with `Открытые задачи: N`, followed by Russian heading paths and
ordinary `- description` bullet lists in file order. Use short Russian action titles,
typically 6–12 words and at most 120 characters. No blank lines between items in a group;
keep a blank line before each heading and before its list. Preserve useful task IDs and
explicit deferral/proposal labels. Implementation details and full permission conditions
remain in source TODO; listing grants no execution permission. Omit dates, checkboxes,
source references and completed historical detail. Do not
omit tasks, reorder or prioritize. Markdown headings define groups; free-standing prose
is not a task. Fenced examples are ignored. Source TODO entries remain unchanged.
With no matches, return `Открытых задач нет.`; a read error is an error, not zero tasks.

Russian descriptions live in `~/ai-data/todo/display-ru.json`, outside Git: `tasks` maps
SHA-256 of each complete original entry to its Russian description, and `headings` maps
original headings to Russian labels. This is a derived presentation cache, not another
backlog. Only entries still open in TODO are displayed. Changed source text invalidates
its description; stale text is never silently reused. No translation API is called.

After editing TODO entries, agents refresh affected descriptions in the same task. If a
list request exits with status 2, run `todo.py --missing` with the same filters, translate
only the returned entries/headings, merge strings into the cache while preserving other
keys, and rerun. Keep each title on one line, at most 120 characters, with no bullet
prefix, date or link. Overlong titles require refresh instead of silent truncation.
Do not infer completion or merge separate source items when shortening descriptions.
`--display PATH` overrides the cache location. With a current cache, list requests need
one script call and no model translation of the full backlog.

Use filters only when the user requests a subset: `--layer` matches the top heading,
`--system` matches lower headings, `--query` matches headings or item text. All matches
are case-insensitive literal substrings; combined filters use AND. Query also searches
cached Russian descriptions. Return the complete
script stdout as the final Markdown answer without a code fence or extra commentary.
Within a session, track proposals, questions and tasks raised by either participant,
including items introduced in prose or across several turns, not only an initial list.
After resolving any one item, show all remaining unresolved session items in the final
response, preserving their original wording, order, numbering, grouping and formatting
where present. Trigger this only when the underlying question is actually settled or work
on a task/proposal is completed. Explaining details, answering a clarification, reporting
status, or discussing a possible approach does not resolve the underlying item; omit the
remaining-items list in those replies. Use the agreed parent task/question as the unit
of completion, not each user message, tool call or verification step. A requested check
inside an ongoing discussion (for example, confirming a credential works while deciding
how to supply it) remains intermediate work and must not trigger the list. Before appending
one, identify which agreed parent item actually closed; if none closed, omit it.
When the trigger applies, render the remaining action items as an explicit list. A file
count, a broad statement that work remains, or a promise to list it later is not a substitute.
Do not treat recording a correction during such a
discussion as completion of the underlying work. Remove resolved or explicitly cancelled items; retain deferred items with
their deferral context. If none remain, say so. Do not add unrelated backlog items or treat
listing as permission to execute. The complete-stdout-only rule above still applies to
explicit backlog listing requests; it does not authorize adding session items to that output.

## Indexes

`python3 ~/ai/general/scripts/build_index.py` rewrites `knowledge/INDEX.md` in every
layer (`general`, `personal`, `current`). Run it after adding or renaming notes.

## Final note-to-TODO reconciliation

Before the final response after substantial work, review only the notes created or changed
for that task, including its work log and affected system maps, against `~/ai/TODO.md`.

1. Ensure remaining actions are represented in the central backlog with source-note links;
   reuse existing entries rather than creating duplicates. Notes retain dated status, risks
   and links, not independent live task lists.
2. Mark completed items closed only when supported by the actual result. Distinguish work
   the user cancelled or explicitly closed without action from work that was implemented.
3. Keep deferred work open with its deferral context, date or resumption condition when
   known. Respect the user's decision to stop; do not revive cancelled diagnostics.
4. Supersede stale directions with a dated final status or explicit reference to the later
   outcome, preserving historical actions and decisions instead of silently rewriting them.
5. Label optional improvements as proposals for a decision. Recording an item never grants
   permission to implement it or change external systems.

Check that the final response agrees with these records. Report unresolved ambiguity as
such; do not invent completion, user decisions or authorization. Do not scan unrelated
notes, perform additional infrastructure checks or change external task trackers as part
of this reconciliation. This is an agent review of meaning; link/format lint alone cannot
prove that statuses agree.

## Daily sync

`~/ai/general/scripts/ai-sync.sh` is called by agents at the start of every task. On the
first call of a day it rebuilds indexes, commits everything, pulls with rebase and pushes to
all remotes, then writes the date to `~/ai/.last-sync`. Before lint and the daily Git skip,
normal invocations run `agnix_update.py`: once per local calendar day, check the official
latest stable release and update the local binary when newer. This is authorized local
maintenance; it requires no repeated confirmation. No unattended timer is installed:
the check happens on the first normal agent sync call of the day. A failed check/update
leaves its successful date unchanged for retry and does not block lint or Git sync.
Normal invocations then run `agent_lint.py` when watched agent inputs changed since its last
successful check. Later calls the same day therefore catch new instruction edits while
skipping Git work. Identical successfully checked inputs produce no lint output.

Before publication, staged KB lint must finish with its final summary and the matching
exit status (0 without errors, 1 with findings). A checker crash, incomplete output or
inconsistent status stops sync before commit/pull/push, shows the checker diagnostics,
and preserves staged changes, `.sync-notes` and the prior sync date. Completed nonsecret
findings remain report-only; detected credentials still block publication.

The commit subject lists the touched areas (`Sync 2026-09-24: youdo, general/linux`).
After each completed task, append one concise final summary to `~/ai/.sync-notes`:
`- <system>: <final result and why>; <key check>; <material remaining risk if any>`.
Keep intermediate steps, commands and approval evidence in the task log rather than adding
separate work lines for each stage. Do not combine unrelated tasks into one result.
The message helper removes exact duplicate records, groups distinct records by system
without dropping descriptions, and adds file counts with up to eight reference-note paths.
Additional changed paths remain available through `git show --stat`.
`.sync-notes` is emptied after the commit; both state files are per machine and ignored.

`--force` runs regardless of the date. `--dry-run` uses a disposable copy of the Git index
and object storage, computes rebuilt knowledge indexes in memory and prints the proposed
working-tree changes without changing files, staging, Git objects or sync state. It never
commits, pulls or pushes. Weekly usage reports and monthly TODO updates are not generated
in this preview; the output states that limitation. External Git object alternates and repositories containing split-index shared files cause
a safe preview failure rather than accessing mutable shared Git storage.
`--status` prints the last sync date. A failed push leaves the commit local and the state
file untouched, so the next call retries. Agents never run `git commit` in `~/ai` themselves.

`~/ai` is one private repository; `origin` fetches from GitHub and pushes to both GitHub and
GitFlic (a separate `gitflic` remote also exists).
The company layer and the `current` symlink are tracked in it; `.gitignore` excludes `.env`,
the sync state files and generated Python bytecode (`__pycache__/`, `*.py[co]`). Do not ignore `companies/` or split it into a nested repository.

Monthly staleness review starts in November 2026. On the first agent session/sync in a
new month with notes due, regardless of the day of the month, `ai-sync.sh` adds or refreshes
`Monthly staleness review YYYY-MM` in `TODO.md` "Knowledge base" and prints a proposal.
The agent offers the review and waits for user agreement before reviewing notes.
Do not repeat the proposal on subsequent successful syncs in the same month. The pending
task remains in TODO.md until addressed; the review is not run automatically.

Dated reminders: an open `TODO.md` item written as `- [ ] due YYYY-MM-DD: ...` is printed by
`ai-sync.sh` as `reminder:` on every daily sync from that date until the item is closed.

## Agent instruction lint

After changing agent instructions, skills (including their references and scripts), or
agent settings, agents must run `python3 ~/ai/general/scripts/agent_lint.py --force`
before the final response, review the findings and report the result. Pass additional
repository-local instruction files or directories as arguments for work outside `~/ai`.
For an additional directory, instruction/skill entry points and skill resources are
included; pass its settings files explicitly as additional arguments. This is a local
report-only check: no model calls, installation, auto-fix or permission expansion.

The default inventory covers shared AGENTS/CLAUDE/GEMINI instruction files, SKILL.md
entry points and their text/code resources, KB-local Claude/Codex settings and Claude
rule directories, global Claude/Codex instructions/settings (including Claude local settings/rules),
user skill links in `.codex/skills`, `.claude/skills` and `.agents/skills`, `.agnix.toml`,
the KB rule README and lint/sync implementation. Runtime links are watched for rewiring.
Equivalent entry points are deduplicated while preserving instruction filenames whose
names select different tool rules (for example AGENTS.md versus CLAUDE.md). System and
plugin skill catalogs are not inventoried. Agnix runs with the KB root as a deterministic
working directory; its root configuration is included in the fingerprint. Deleted files invalidate the previous snapshot. Only supported entry points
are passed to agnix; resource changes trigger rechecking their SKILL.md. This static
lint does not replace behavioral tests or external approval.

The helper prefers `~/.local/share/agnix/current/agnix`, then the legacy
`~/.local/share/agnix/v0.59.0/agnix`, then `agnix` on PATH; `--agnix`
overrides it. Machine-local state/report/lock are in `~/ai-data/agnix/` (outside Git).
Only successful complete checks update input hashes. Warnings are recorded once per
unchanged successful snapshot; errors, missing binary, execution failure or changed
inputs during checking leave a retry pending. The compact JSON report retains rule IDs,
severity, file and line, omitting raw settings, source snippets and diagnostic messages.
Use rule explanations and the specific affected file to investigate findings safely.

For every agnix version, the helper rechecks CDX-CFG-025 warnings against the official Codex
schema's `default` and `priority` examples. It validates TOML and the exact diagnostic
line in a scanned `.codex/config.toml`; invalid values and all other findings remain.
TOML parsing uses Python's `tomllib` or installed `tomli`; missing parsing support keeps
the original warning. Accepted compatibility findings are omitted from stdout and the
report diagnostics; their count remains in report metadata for audit. The exception
does not depend on the agnix version.

By user decision, the helper also omits informational AGM-004 (missing project overview)
for the canonical root `AGENTS.md`, which contains shared policy rather than project
context, and informational CDX-AG-008 (shadowed instructions) for that same file while
its sibling `AGENTS.override.md` exists to avoid duplicate loading. These exceptions do
not cover other files, warning/error severities or other rules. The native binary and
rules stay enabled; direct binary runs remain unfiltered.

Every normal `ai-sync.sh` invocation performs the change-aware fallback before checking
today's Git sync date. Its lint failure is visible but does not block Git synchronization.
An unchanged successful snapshot is skipped; this is change-triggered rather than one
scan per calendar day. `ai-sync.sh --dry-run`, `--status` and `--help` do not invoke the
helper or write lint state. The explicit post-edit `--force` check always reruns and can
also satisfy the next sync fallback. A newly installed PC can run `agnix_update.py` to
install the current stable binary; normal sync also installs it when absent. The updater
uses the official GitHub release API (`agent-sh/agnix`), excludes drafts/prereleases and
never downgrades. It checks the archive against the API SHA-256 and verifies
`agnix --version` before atomically switching the `current` symlink. Previous version
directories remain available. Supported targets are Linux x86_64 musl/aarch64 GNU and
macOS x86_64/arm64; missing assets, missing digests and unsupported targets are visible
failures. Machine-local `update.json` and `update.lock` live in `~/ai-data/agnix/`.
Concurrent updates are locked; successful daily checks skip repeated network access.
`agnix_update.py --force` bypasses that date check; sync's `--force` only bypasses the Git
date. Sync's read-only modes never run updates.

## Connecting an agent

Agent-specific directories (`~/.codex`, `~/.claude`, `~/.gemini`) hold only symlinks into
`~/ai` plus the agent's own runtime state.

- Instructions: symlink to `~/ai/AGENTS.md` from `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`,
  `~/.gemini/GEMINI.md`.
- Skills: one symlink per directory from `~/ai/general/skills/` and `~/ai/current/skills/`
  into the agent's skills folder (`~/.codex/skills/`, `~/.claude/skills/`).
- Switching employer: create `companies/<new>/`, repoint `current`, redo skill symlinks.

The portable `general/skills/agent-learning/` workflow is linked into the Codex and
Claude skill directories. Shared instructions also direct Gemini to read its `SKILL.md`
explicitly; this does not assume native Gemini skill discovery or automatic hooks.
Corrections use the same layered knowledge base, not separate per-agent memories.
