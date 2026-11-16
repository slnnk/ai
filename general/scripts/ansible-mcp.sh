#!/usr/bin/env bash
# Launch the shared Ansible MCP installation for one explicitly selected project.
set -euo pipefail

workspace=$(realpath -- "${1:?Usage: ansible-mcp.sh PROJECT_DIRECTORY}")
runtime="$HOME/ai-data/ansible-mcp"
venv="$workspace/.ansible-venv"
node="$runtime/node_modules/node/bin/node"
server="$runtime/node_modules/@ansible/ansible-mcp-server/dist/cli.cjs"

[[ -d "$workspace" && -x "$venv/bin/python" && -x "$node" && -f "$server" ]] || {
    echo "Ansible MCP requires the shared installation and PROJECT/.ansible-venv." >&2
    exit 1
}

export WORKSPACE_ROOT="$workspace"
export VIRTUAL_ENV="$venv"
export PATH="$venv/bin:$runtime/node_modules/node/bin:$PATH"
cd -- "$workspace"
exec "$node" "$server" --stdio
