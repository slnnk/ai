#!/usr/bin/env bash
# Show what changed in the team repo claude-code-config-infra since the commit recorded
# in the local index note, so the index can be refreshed.
set -euo pipefail

REPO="${TEAM_REPO:-/home/slnnk/git/claude-code-config-infra}"
INDEX="${TEAM_REPO_INDEX:-$HOME/ai/current/knowledge/systems/team-config-repo.md}"
BRANCH="${TEAM_REPO_BRANCH:-origin/main}"
FETCH=1

usage() {
    cat <<EOF
Usage: $(basename "$0") [--no-fetch] [--help]

Reads indexed_commit from the frontmatter of $INDEX, runs a read-only
git fetch in $REPO and prints the files under indexed paths (docs/, skills/,
CLAUDE.md, README.md, .env.example) changed between indexed_commit and $BRANCH.

Env: TEAM_REPO, TEAM_REPO_INDEX, TEAM_REPO_BRANCH.
After refreshing the index, set indexed_commit to the printed head commit.
EOF
}

for arg in "$@"; do
    case "$arg" in
        --no-fetch) FETCH=0 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "unknown argument: $arg" >&2; usage >&2; exit 2 ;;
    esac
done

base=$(sed -n 's/^indexed_commit: *//p' "$INDEX" | head -1)
[ -n "$base" ] || { echo "indexed_commit not found in $INDEX" >&2; exit 1; }

[ "$FETCH" -eq 1 ] && git -C "$REPO" fetch -q origin
head=$(git -C "$REPO" rev-parse --short "$BRANCH")

if [ "$(git -C "$REPO" rev-parse "$base")" = "$(git -C "$REPO" rev-parse "$BRANCH")" ]; then
    echo "index is current: $head"
    exit 0
fi

echo "indexed: $base  head: $head  commits: $(git -C "$REPO" rev-list --count "$base..$BRANCH")"
git -C "$REPO" diff --name-status "$base" "$BRANCH" -- docs skills CLAUDE.md README.md .env.example \
    | grep -v '^[AMDR][0-9]*[[:space:]]docs/projects/' || echo "(no indexed files changed)"
echo "local checkout behind $BRANCH: $(git -C "$REPO" rev-list --count "HEAD..$BRANCH")"
