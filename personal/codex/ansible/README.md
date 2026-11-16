# Ansible MCP pilot

These are the canonical personal settings linked from
`/home/slnnk/mygit/ansible/.codex/config.toml`. Do not put this integration in
global `~/.codex`. The shared launcher is
`~/ai/general/scripts/ansible-mcp.sh`; it takes the absolute project directory
as its one argument and uses that project's `.ansible-venv`.

Runtime dependencies live outside Git in `~/ai-data/ansible-mcp`.
To reproduce the verified installation, run:

```bash
npm install --prefix "$HOME/ai-data/ansible-mcp" --save-exact --no-audit --no-fund node@24.22.3 @ansible/ansible-mcp-server@26.6.0
```

The separate Node binary is used by the launcher; there is no need to change
the system Node version. The upstream MCP handshake version is `0.1.0` even
though the installed npm package version is `26.6.0`.

Open a new Codex session from the project and inspect `/mcp`.
Ask it to retrieve Ansible role best practices to try the connection.
Only the four tools in `enabled_tools` are exposed to Codex in this pilot.
The upstream server itself still implements additional tools; the allowlist
is a client policy rather than process isolation.

For another project, create a separate canonical project config under
`~/ai/personal/codex/`, change the launcher argument to that checkout, and
link it from the project's `.codex/config.toml`. Reuse the shared runtime.
Follow the destination repository's approval and instruction requirements.

The empty file that previously occupied the pilot project's `.codex` path is
preserved as `.codex.empty-backup`. To disable the connection, set
`enabled = false` in this config. No system service or background daemon was
installed. No playbooks were executed.
