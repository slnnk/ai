#!/usr/bin/env bash
# ai-sync.sh — once-a-day commit and push of the ~/ai knowledge base.
#
# Agents call this at the start of every task. It is cheap and idempotent:
#   - if ~/ai/.last-sync already holds today's date, it exits immediately;
#   - otherwise it rebuilds the indexes, commits any changes, pulls with rebase,
#     pushes to all remotes and records today's date.
#
# Commit message: subject lists the touched areas (company, general/<tech>, ...);
# body contains the lines agents appended to ~/ai/.sync-notes ("what and why")
# followed by every changed note with its title. .sync-notes is emptied after the
# commit. Agents append with:  echo "- <system>: <what changed and why>" >> ~/ai/.sync-notes
#
# Usage:
#   ai-sync.sh            run if not yet run today
#   ai-sync.sh --force    run even if already synced today
#   ai-sync.sh --dry-run  show what would be committed, change nothing
#   ai-sync.sh --status   print the last sync date and exit
#
# Once a week (newest personal/usage/*.txt older than 7 days) it also writes a token usage
# report with general/scripts/token_usage.py --kb and adds a one-line summary to the commit.
#
# On the first sync of a month with notes due for review (build_index.py --stale 30) it adds
# a "Monthly staleness review YYYY-MM" item to TODO.md and prints a reminder line.
# Every daily sync prints open TODO.md items "- [ ] due YYYY-MM-DD: ..." whose date has come.
#
# Exit codes: 0 synced or nothing to do; 1 sync failed (state file not updated,
# so the next call retries); 2 usage error.
#
# The state file is per machine and is not tracked in git.

set -u
AI_ROOT="${AI_ROOT:-$HOME/ai}"
STATE="$AI_ROOT/.last-sync"
NOTES="$AI_ROOT/.sync-notes"   # one line per piece of work, appended by agents, cleared after commit
TODAY="$(date +%F)"
FORCE=0; DRY=0

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --dry-run) DRY=1 ;;
    --status) echo "last sync: $(cat "$STATE" 2>/dev/null || echo never)"; exit 0 ;;
    -h|--help) sed -n '2,/^set -u/{/^#/p}' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "ai-sync: unknown option $arg" >&2; exit 2 ;;
  esac
done

cd "$AI_ROOT" || { echo "ai-sync: $AI_ROOT not found" >&2; exit 1; }

if [ "$FORCE" -eq 0 ] && [ "$DRY" -eq 0 ] && [ "$(cat "$STATE" 2>/dev/null)" = "$TODAY" ]; then
  exit 0
fi

log() { echo "ai-sync: $*"; }
fail() { log "FAILED: $*"; exit 1; }

# 1. indexes
python3 general/scripts/build_index.py >/dev/null || fail "build_index.py"

# 1b. weekly token usage report: personal/usage/YYYY-MM-DD.txt when the newest is >= 7 days old.
# Failures here never block the sync.
USAGE_DIR="$AI_ROOT/personal/usage"
if [ "$DRY" -eq 0 ]; then
  last=$(ls "$USAGE_DIR"/????-??-??.txt 2>/dev/null | sort | tail -1)
  age=999
  [ -n "$last" ] && age=$(( ( $(date +%s) - $(date -d "$(basename "$last" .txt)" +%s) ) / 86400 ))
  if [ "$age" -ge 7 ] && mkdir -p "$USAGE_DIR" \
     && python3 general/scripts/token_usage.py --days 7 --kb > "$USAGE_DIR/$TODAY.txt.tmp" 2>&1; then
    mv "$USAGE_DIR/$TODAY.txt.tmp" "$USAGE_DIR/$TODAY.txt"
    brief=$(python3 general/scripts/token_usage.py --days 7 --brief 2>/dev/null)
    log "weekly $brief (personal/usage/$TODAY.txt)"
    echo "- knowledge-base: weekly $brief, report personal/usage/$TODAY.txt" >> "$NOTES"
  else
    rm -f "$USAGE_DIR/$TODAY.txt.tmp"
  fi
fi

# 1c. monthly staleness reminder: on the first sync of a month with notes due for review
# (maps > 30 days, recipes > 180 days, hypotheses), add one item to TODO.md "## Knowledge base"
# and print it. The item itself is the state: it is added once per month.
# Failures here never block the sync.
MONTH="$(date +%Y-%m)"
if [ "$DRY" -eq 0 ] && ! grep -q "Monthly staleness review $MONTH" TODO.md 2>/dev/null; then
  due=$(python3 general/scripts/build_index.py --stale 30 --recipe-days 180 --count 2>/dev/null)
  if [ "${due:-0}" -gt 0 ] 2>/dev/null && python3 - "$MONTH" "$due" <<'EOF'
import sys
month, due = sys.argv[1], sys.argv[2]
item = (f"- [ ] Monthly staleness review {month}: {due} notes due; list with "
        "`general/scripts/build_index.py --stale 30`; per note confirm, fix or set "
        f"`status: outdated`, bump `checked`; offer to the user, do not run unasked ({month}-01)\n")
text = open("TODO.md", encoding="utf-8").read()
head = "## Knowledge base\n\n"
if head not in text:
    sys.exit(1)
open("TODO.md", "w", encoding="utf-8").write(text.replace(head, head + item, 1))
EOF
  then
    log "staleness review due: $due notes (TODO.md, build_index.py --stale 30)"
    echo "- knowledge-base: monthly staleness review $MONTH added to TODO.md ($due notes due)" >> "$NOTES"
  fi
fi

# 1d. dated reminders: open TODO.md items "- [ ] due YYYY-MM-DD: ..." whose date has come
# are printed on every daily sync until they are closed. Agents pass them on to the user.
python3 - "$TODAY" <<'EOF' 2>/dev/null | while IFS= read -r line; do log "reminder: $line"; done
import re, sys
for line in open("TODO.md", encoding="utf-8"):
    m = re.match(r"- \[ \] due (\d{4}-\d{2}-\d{2}):\s*(.*)", line)
    if m and m.group(1) <= sys.argv[1]:
        text = m.group(2).strip()
        print(f"{m.group(1)} {text[:110]}{'...' if len(text) > 110 else ''}")
EOF

# 2. stage and inspect
git add -A || fail "git add"
if git diff --cached --name-only | grep -qE '(^|/)\.env$'; then
  git reset -q; fail "a .env file is staged; check .gitignore"
fi
# lint staged notes: a credential blocks the commit, other findings are reported and fixed later
LINT=/tmp/ai-sync-lint.$$
python3 general/scripts/kb_lint.py --staged > "$LINT" 2>&1
if grep -q '^E secret' "$LINT"; then
  grep '^E secret' "$LINT" >&2; rm -f "$LINT"; git reset -q
  fail "a staged note looks like it contains a credential; remove it and rerun"
fi
if grep -q '^[EW] ' "$LINT"; then
  log "lint findings to fix (commit proceeds):"; grep '^[EW] ' "$LINT" | sed 's/^/  /'
fi
rm -f "$LINT"

added=$(git diff --cached --name-status | grep -c '^A' || true)
modified=$(git diff --cached --name-status | grep -c '^M' || true)
deleted=$(git diff --cached --name-status | grep -c '^D' || true)
renamed=$(git diff --cached --name-status | grep -c '^R' || true)

if [ "$DRY" -eq 1 ]; then
  log "dry run: $added added, $modified modified, $deleted deleted, $renamed renamed"
  git diff --cached --name-status | sed 's/^/  /'
  git reset -q
  exit 0
fi

# 3. commit with a message built from agent notes and changed-note metadata
if ! git diff --cached --quiet; then
  MSG=/tmp/ai-sync-msg.$$
  git diff --cached --name-status | python3 general/scripts/ai_sync_message.py "$TODAY" "$NOTES" > "$MSG" \
    || fail "compose commit message"
  git commit -q -F "$MSG" || fail "git commit"
  log "$(head -1 "$MSG")"
  rm -f "$MSG"
  [ -f "$NOTES" ] && : > "$NOTES"
else
  log "nothing to commit"
fi

# 4. pull --rebase, then push to every remote URL of origin
export GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=8"
if git remote get-url origin >/dev/null 2>&1; then
  if ! git pull --rebase -q origin main 2>/tmp/ai-sync-pull.$$; then
    git rebase --abort 2>/dev/null
    cat /tmp/ai-sync-pull.$$ >&2; rm -f /tmp/ai-sync-pull.$$
    fail "pull --rebase; resolve manually in $AI_ROOT"
  fi
  rm -f /tmp/ai-sync-pull.$$
  if ! git push -q origin main 2>/tmp/ai-sync-push.$$; then
    cat /tmp/ai-sync-push.$$ >&2; rm -f /tmp/ai-sync-push.$$
    fail "push (commit is saved locally; will retry next run)"
  fi
  rm -f /tmp/ai-sync-push.$$
  log "pushed to all remotes"
fi

echo "$TODAY" > "$STATE"
exit 0
