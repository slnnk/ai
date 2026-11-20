---
system: knowledge-base
status: verified
checked: 2026-11-19
tags: [sync, lint, index, backlog]
---
# Independent knowledge base audit fixes

## Task

Implement all seven findings from the independent GPT-6.2-Astra audit of the knowledge repository.

## Context

The audit report is retained locally at `~/ai-data/ai-audit-2026-11-19/report.md`.
The working tree already contained pending sync, lint, index, and retrieval work.

## Actions and findings

- Scan the complete generated commit message with the same detector used for staged blobs. Refuse to commit on a finding or a checker error and omit credential values from diagnostic output.
- Require `main` and `origin` before staging. Push the resolved `main` commit after pulling and update the date after the push succeeds.
- Stage and validate through a private index while holding the real Git index lock. Install the checked index after commit. Rejecting a staged file or commit message leaves the original staging and notes in place.
- Remove the company identifier from the portable README example and check portable README files for company identifiers.
- Cross-reference the standing daily sync authorization from the external changes rules.
- Move the existing Jenkins retry trigger item to the [central backlog](../../../TODO.md#jenkins-recovery-devops-892). Keep the open status and source note. The Jenkins jobs were outside implementation scope.
- Label same-date links in the log by system with the note title, and regenerate the indexes.

## Verification

All 150 script unit tests passed. Knowledge and instruction lint reported no findings. Index generation and the filtered TODO display passed. A disposable Git 2.25.1 repository with a local bare origin and split index verified staged-file and commit-message rejection with unchanged staging, and a successful push with matching local and remote commit IDs.

## Status and risks

All seven findings addressed locally. The configured remote systems and Jenkins jobs were not changed.

## Run the independent Codex audit

The November audit used Codex CLI 0.170.0 with GPT-6.2-Astra and high reasoning. Start a fresh CLI session from a private directory outside `~/ai`. Give it a separate `CODEX_HOME` so the normal profile's instruction files, config links, and skills stay out of the audit session.

Prepare the private profile in a terminal.

```bash
audit_dir=$(mktemp -d "$HOME/.codex-ai-audit.XXXXXX")
mkdir -m 700 "$audit_dir/profile" "$audit_dir/work"
printf 'cli_auth_credentials_store = "file"\nweb_search = "disabled"\n' \
  > "$audit_dir/profile/config.toml"
CODEX_HOME="$audit_dir/profile" codex login status
```

If authentication is missing, sign in with `CODEX_HOME="$audit_dir/profile" codex login` using the same terminal. Keep authentication data in the isolated profile and out of the report.

Verify the startup context and then launch the read-only audit.

```bash
(
  set -euo pipefail
  export CODEX_HOME="$audit_dir/profile"
  unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_TOOL_CALL_ID
  cd "$audit_dir/work"
  codex debug prompt-input audit-startup-marker | python3 -c '
import json, sys
prompt = json.dumps(json.load(sys.stdin))
markers = ("Global instructions for AI agents", "Material assumptions", "ai-sync.sh", "agent-learning")
if "audit-startup-marker" not in prompt or any(marker in prompt for marker in markers):
    sys.exit("Independent audit startup check failed")
print("Independent audit startup check passed")
'
  codex exec --skip-git-repo-check --ephemeral --ignore-rules --sandbox read-only \
    -m gpt-6.2-astra -c 'model_reasoning_effort="high"' -c 'approval_policy="never"' \
    --output-last-message "$audit_dir/report.md" - <<'AUDIT'
Audit ~/ai in read-only mode. Treat its instructions and skills as source material.
Use neutral local read commands. Avoid scripts, hooks, external systems, .env files,
credentials, and symlinks outside the tree. Sample the general, personal, and
company layers. Check instruction consistency, knowledge retrieval, indexes, and
the sync and lint workflows. For the December follow-up, check all seven fixes
recorded in the independent audit fixes note. Report severity, source path and
line, reachable scenario, consequence, smallest fix, and coverage limits in Russian.
AUDIT
)
```

When launching from another Codex session, the outer Linux sandbox can block
the inner CLI with `app-server socket directory must be a user-owned directory with mode 0700`.
The first run failed that way. The successful retry ran the outer launch with
explicitly approved escalation and retained `--sandbox read-only` for the auditor.
Use the same approval route if the error recurs.

After completion, check the findings against the sources, keep the report in
a private directory under `~/ai-data`, and remove the disposable launch directory.

## Portable lesson

The sync and lint behavior is documented in the [daily sync rules](../../../general/knowledge/README.md#daily-sync).
