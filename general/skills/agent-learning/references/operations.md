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

Read the returned canonical target. Query is deterministic filtering, not semantic search: try a stable key/system or alternate keywords. Global rules remain discoverable alongside specific results. Omitted scope retrieves global rules, plus an exact repository match when supplied; choose current/personal explicitly for layer-wide rules. Increase `--limit` when the result says it was truncated.

After observing an applicable outcome:

```bash
python3 ~/ai/general/scripts/agent_learning.py verify \
  --key discussion-before-implementation --scope global \
  --event-id example-evaluation-1 --outcome pass \
  --source 'Observed isolated planning scenario; no implementation files changed.' \
  --rule-loaded yes
```

Use `fail` with an evidence-based `--cause` for a violation and `not-applicable` outside scope. A successful record/query/lint command does not demonstrate behavior. Missing or moved canonical targets require repair.

## Maintenance

The helper owns its machine format and serializes updates under a lock; use its operations. No historical export, external write, permission expansion, or deletion follows from this workflow. Actions live only in `~/ai/TODO.md`. Run `kb_lint.py` and `build_index.py` after significant work and append `.sync-notes`. Daily sync handles publication; do not commit manually.
