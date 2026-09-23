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
    -h|--help) sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
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

# 2. stage and inspect
git add -A || fail "git add"
if git diff --cached --name-only | grep -qE '(^|/)\.env$'; then
  git reset -q; fail "a .env file is staged; check .gitignore"
fi
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
  git diff --cached --name-status | python3 - "$TODAY" "$NOTES" > "$MSG" <<'PY' || fail "compose commit message"
import re, sys, pathlib, subprocess
today, notes_path = sys.argv[1], sys.argv[2]
status_word = {"A": "added", "M": "updated", "D": "removed", "R": "renamed"}

def meta(path):
    """Return (system, title) from a note's frontmatter and first H1, or (None, None)."""
    p = pathlib.Path(path)
    if p.suffix != ".md" or not p.exists() or p.name in ("INDEX.md",):
        return None, None
    system = title = None
    try:
        for line in p.read_text(errors="replace").splitlines()[:40]:
            m = re.match(r"^system:\s*(\S+)", line)
            if m and not system: system = m.group(1)
            if line.startswith("# ") and not title: title = line[2:].strip()
            if system and title: break
    except OSError:
        pass
    return system, title

def area(path):
    parts = pathlib.Path(path).parts
    if parts[0] == "companies" and len(parts) > 2: return parts[1]
    if parts[0] in ("general", "personal") and len(parts) > 2 and parts[1] == "knowledge": return f"{parts[0]}/{parts[2]}"
    return parts[0]

files, areas = [], []
for line in sys.stdin:
    cols = line.rstrip("\n").split("\t")
    st, path = cols[0][0], cols[-1]
    if path.endswith("INDEX.md") or path == ".gitignore":
        continue
    system, title = meta(path) if st != "D" else (None, None)
    label = area(path)
    if system and label.startswith("companies/") is False and "/" not in label and system != label:
        label = f"{label}/{system}"
    if label not in areas: areas.append(label)
    files.append((st, path, title))

notes = []
np = pathlib.Path(notes_path)
if np.exists():
    notes = [l.strip() for l in np.read_text(errors="replace").splitlines() if l.strip()]

subject_areas = ", ".join(areas[:4]) + (" ..." if len(areas) > 4 else "")
print(f"Sync {today}: {subject_areas or 'index and housekeeping'}")
print()
if notes:
    print("Work recorded by agents:")
    for n in notes:
        print(f"- {n.lstrip('-* ')}")
    print()
if files:
    print("Files:")
    for st, path, title in files:
        w = status_word.get(st, st)
        print(f"- {w} {path}" + (f": {title}" if title else ""))
PY
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
