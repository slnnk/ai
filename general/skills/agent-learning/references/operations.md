# Operations

Use `python3 ~/ai/general/scripts/agent_learning.py <command> --help` for CLI details. `--root` before the command selects an isolated knowledge root for tests; normal operation uses `~/ai`, independently of cwd. Read-only operations must not initialize storage.

## Capture and link

Example with invented, non-sensitive evidence:

```bash
python3 ~/ai/general/scripts/agent_learning.py record \
  --key discussion-before-implementation --event-id example-session-message-4 \
  --scope global --system agent-learning --kind explicit \
  --summary 'Implementation started during a planning discussion.' \
  --expected 'Investigate and produce the requested plan; implement after a request to do so.' \
  --source 'User correction in example session, message 4' --agent codex
```

Make the authorized canonical edit, then link it:

```bash
python3 ~/ai/general/scripts/agent_learning.py link-rule \
  --key discussion-before-implementation --scope global --target ~/ai/AGENTS.md
```

Linking references a local document; it neither edits that file nor grants execution permission. Inferred hypotheses are not active rules. Resolve unclear meaning before promotion. Rejected conclusions remain historical evidence; adoption requires actual user evidence.

After a user accepts a previously inferred rule, make the authorized canonical edit and record that decision with the same key:

```bash
python3 ~/ai/general/scripts/agent_learning.py resolve \
  --key <existing-key> --scope <scope> --decision adopted \
  --source '<reference to the actual user decision>' --target <canonical-file.md> \
  --expected '<current approved behavior>'
```

Use `resolve` to revise an expectation, with an explicit decision source, rather than creating a new key. Use `--decision rejected` or `superseded` to retain history while excluding an abandoned rule from normal lookup; `query --include-history` exposes those records. Do not fabricate approval for an inferred rule. Prior evaluations remain historical evidence of their own rule revision, not proof of a changed rule. `link-rule` can repair a moved canonical reference after verifying the new file.

Mutation `--dry-run` previews changes without creating directories, locks, or timestamps. A source is provenance, never a shell command.

## Scope

- `global`: cross-agent operating preferences; evidence in personal knowledge.
- `current`: employer-specific evidence in the active current layer.
- `personal`: personal infrastructure and conventions.
- `repo`: exact repository identity and current/personal layer when recording. Supply `--repo` for retrieval.
- `kind=task`: requires `--task-id`; only retrieve with the matching task ID.
- `kind=inferred`: hypothesis, even when repeated; frequency is not authorization.
- `kind=fact`: factual correction; the canonical note retains verification limits.

Reuse a stable key and event ID when another agent reports the same correction. Different wording does not establish a new occurrence. Concurrency protection prevents lost writes; semantic duplication still needs judgment.

## Retrieval and verification

```bash
python3 ~/ai/general/scripts/agent_learning.py query --scope current --system deployment
python3 ~/ai/general/scripts/agent_learning.py query --scope personal --repo /path/to/checkout
python3 ~/ai/general/scripts/agent_learning.py report
python3 ~/ai/general/scripts/agent_learning.py check
```

Read the returned canonical target. Query is deterministic filtering, not semantic search: try a stable key/system or alternate keywords. Global rules remain discoverable alongside specific results. Omitted scope retrieves global rules, plus an exact repository match when supplied; choose current/personal explicitly for layer-wide rules. Exact key matches rank first, then topical matches, with matching task/repository/layer
specificity before recency. Scope and task-ID exclusion still happen before ranking;
active global rules remain included as background obligations. Coverage reports topical
and background-global counts. When truncated, follow the shell-quoted next command
(`--offset` with the original filters), or increase `--limit`. Pages assume an unchanged
store; query again from offset zero if records change. A targeted first page is not proof
that all global obligations or canonical rule text were read.

After observing an applicable outcome:

```bash
python3 ~/ai/general/scripts/agent_learning.py verify \
  --key discussion-before-implementation --scope global \
  --event-id example-evaluation-1 --outcome pass \
  --source 'Observed isolated planning scenario; no implementation files changed.' \
  --rule-loaded yes
```

Use `fail` with an evidence-based `--cause` for a violation and `not-applicable` outside scope. A successful record/query/lint command does not demonstrate behavior. Missing or moved canonical targets require repair.

## Task metrics and daily review

Use an existing task log and a stable task ID. `record` maintains one
`agent-task-metrics-json` block in that note; task metrics survive normal KB sync.
The command validates the store and refuses duplicate IDs across notes. Do not use
session ID alone when a session contains several tasks. Example with synthetic IDs:

```bash
python3 ~/ai/general/scripts/agent_metrics.py record \
  --source personal/knowledge/log/YYYY-MM-DD-agents-example.md \
  --task-id session-example-task1 --kind code --state open \
  --model MODEL --session-id SESSION --evidence 'Task request and scope in this note'
```

At completion use the same command/ID with `--state closed`, evidence-supported
`--first-result pass|fail|unknown` and `--final-result pass|partial|fail|unknown`.
Optional integer counters: `--corrections`, `--unnecessary-actions`, `--critical-events`,
`--tokens`, `--active-seconds`. Omitted counters remain unknown or retain their earlier
value; zero requires evidence. Count distinct substantive corrective interventions,
not required approvals/new requirements. Count unnecessary actions only when their
lack of purpose is supported by evidence. Tokens/time require task-attributable
measurements; never assign a whole multi-task session's usage to each task. Keep
source examples in the note and put only short references in `--evidence`.
`--first-result` describes the first substantive delivered result, not internal test
iterations. A recorded first failure cannot be overwritten by later success.

Normal sync runs `agent_metrics.py prepare` before its same-day Git skip. On first
use it snapshots the previous seven completed calendar days in the host timezone;
later runs cover the interval since the last reviewed boundary, excluding today.
An unfinished snapshot is reused until reviewed; absent days do not create fake
daily reviews. After a delayed review, remaining days enter the next review interval.
Generated snapshots and receipts live in `~/ai-data/agent-metrics/`; `status` is read-only.
Changed task snapshots are not additional tasks; do not sum daily counts as distinct
tasks. The existing token helper supplies a rolling seven-day session-cohort reference,
explicitly not an exact calendar-day or task cost. Missing data remains visible.

For a pending review, read its JSON and usage reference, then relevant source notes.
Use `new_note.py` for one dated analysis log, in the appropriate layer (company
examples belong in current). Include `## Findings`, `## Actions`, `## Limits` and the
snapshot SHA-256. State counts/denominators, unknown coverage, comparable trends if
available, concrete examples and narrowly supported conclusions. Existing learning
records own corrections; existing TODO items own proposed actions. Do not add new
rules merely to report a metric or infer improvement from silence.

```bash
python3 ~/ai/general/scripts/agent_metrics.py complete --source PATH_TO_REVIEW_NOTE
```

This records the saved review and suppresses further reminders that day. It verifies
the snapshot reference and note structure, not the truth of the analysis. Never call
it before doing the review; leave failed collection/review pending. No model or timer
is launched. Do not copy private raw logs or credentials into metrics. A missing
generated state after machine migration needs explicit reconciliation; never invent
a completed historical review.

## Maintenance

The helper owns its machine format and serializes updates under a lock; use its operations. No historical export, external write, permission expansion, or deletion follows from this workflow. Actions live only in `~/ai/TODO.md`. Run `kb_lint.py` and `build_index.py` after significant work and append `.sync-notes`. Daily sync handles publication; do not commit manually.
