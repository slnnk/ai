---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, audit, agnix]
---
# Local agents: agnix and instruction-loading pilot

## Summary
Completed the explicitly approved first pilot. Installed agnix 0.59.0 in an isolated local directory from an official GitHub release and verified the archive against the release API SHA-256. Eight selected files produced nine diagnostics; manual classification found one ambiguous path, three symlink-relative link portability findings and five policy/advice/schema mismatches. A native offline Codex prompt renderer confirmed one copy of shared instructions from home and a representative repository, two copies when launched in the KB root, and all four custom skill metadata entries. Claude filesystem discovery is sound, but its fresh-session runtime context was not tested. A small stale Claude cache is a separate confirmed finding. No instruction/skill/runtime configuration fixes or model calls were performed.

## Task and authorization
The user requested "agnix + instruction-loading audit", step1 of the [proposed trial order](2026-10-19-knowledge-base-agent-capabilities-research.md). Scope: isolated tool installation, report-only lint, bounded instruction/skill discovery and a report. Subsequent evaluation or instruction correction stages were not authorized by this request. Existing company checkouts were inspected read-only; Git/MR approval gates are unchanged.

## Installation and commands
- Official release: [v0.59.0](https://github.com/agent-sh/agnix/releases/tag/v0.59.0), published 2026-10-17. Asset `agnix-x86_64-unknown-linux-musl.tar.gz`, SHA-256 `fc335bafef7bbe292fef5a28b11d659c53dde6ef46a24979ed0608d3592c0af5` matched the digest obtained through GitHub's release API.
- Installed binary: `~/.local/share/agnix/v0.59.0/agnix`; `--version` reports `agnix 0.59.0`. No global PATH link, editor extension, MCP or hook installation.
- Sandbox DNS blocked download; requested escalation and fetched release metadata/archive outside sandbox. An earlier npm metadata query hit the configured corporate registry and failed DNS; no npm package was installed. Native offline Codex render also required escalation because the sandbox's read-only Codex mount prevented startup bookkeeping.
- `agnix --dry-run --format json` is unsupported in this version. Initial invocation returned a usage error and no diagnostics; corrected to plain `--format json` without any fix flag. Hashes of all eight inputs remained unchanged.

Reproduction for the selected files:
```bash
~/.local/share/agnix/v0.59.0/agnix --format json \
  ~/ai/AGENTS.md ~/.claude/CLAUDE.md ~/.codex/config.toml ~/.claude/settings.json \
  ~/ai/general/skills/agent-learning/SKILL.md \
  ~/ai/current/skills/android-dig/SKILL.md \
  ~/ai/current/skills/gitlab-workflow/SKILL.md \
  ~/ai/current/skills/rp/SKILL.md
```
The diagnostic run exits1 because findings exist. This is not a clean/pass result and is not being promoted to a mandatory gate.

## agnix findings and manual classification

| Rule / location | Observation | Classification and disposition |
| --- | --- | --- |
| CDX-AG-005, AGENTS.md:27 | `knowledge/repos.md` is reported missing. | Genuine ambiguous shorthand in a layered KB. Intended `~/ai/current/knowledge/repos.md` exists and appears explicitly elsewhere. Candidate wording clarification for stage3; do not create a fake root knowledge directory. |
| REF-002 x3, ~/.claude/CLAUDE.md:119,152,153 | Relative links resolve under `.claude/current/` in agnix. | Symlink-relative Markdown portability issue. Canonical target is `~/ai/AGENTS.md`, and linked targets exist relative to it. Not proof that Claude failed to load the instructions/skills. Consider unambiguous links in stage3; do not duplicate the company tree in `.claude`. |
| PE-006 x3, ~/.claude/CLAUDE.md:88,93,131 | Negative secret/personal-data/Git rules. | Intentional user policies with positive alternatives and exceptions in context. Preserve them; no change just to satisfy stylistic heuristics. |
| CDX-CFG-025, ~/.codex/config.toml:3 | `service_tier = "default"` rejected in favor of fast/flex. | Unconfirmed schema/version mismatch. The same installed agnix rule explanation presents default as a good example and labels its fix unsafe. Installed Codex offline parsing accepts current configuration. Do not change billing/performance behavior based on this diagnostic; model/API tier acceptance was not tested. |
| AGM-004, AGENTS.md:1 | No project overview. | Inapplicable generic recommendation for a global user-policy file; layout/purpose already exist. |

Total: 8 inputs, 3 errors / 5 warnings / 1 info as classified by the linter, not nine confirmed defects. Four custom SKILL files produced no diagnostics in this selected run; this is not proof of behavior quality.

## Native Codex loading evidence
Installed Codex CLI0.163.0 provides `codex debug prompt-input`. A small local helper runs that offline renderer, captures JSON in memory and saves only sanitized counts/hashes. No raw prompt or model/API output was retained.

| Launch cwd | Copies of exact canonical AGENTS text | All four custom skill metadata entries |
| --- | ---: | --- |
| `~/` | 1 | yes |
| `~/ai` | 2 | yes |
| `~/git/selectel-tf` | 1 | yes |

The duplicate in `~/ai` is demonstrated, consistent with global `~/.codex/AGENTS.md` pointing at the same file that appears as the project instruction. It does not demonstrate a quality failure, but it adds duplicate instruction context. Other cwd behave as expected. Changing cwd for an individual shell command does not itself reinitialize an existing agent session.

User `CODEX_HOME` override is unset; no global AGENTS override or custom instruction-discovery options found. Home and the representative checkout have no competing project AGENTS files. Current `.agents/skills` user location is absent, but legacy `.codex/skills` links are usable in this installed runtime: the rendered metadata confirms discovery. Do not migrate paths solely because current docs list another preferred location.

The renderer proves the constructed input for these launches, not model adherence after a request is sent, not all plugin roots and not ongoing sessions launched earlier. See [official instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skills loading](https://learn.chatgpt.com/docs/build-skills).

## Claude loading and cache audit
Installed Claude Code2.1.293: `~/.claude/CLAUDE.md` is a valid symlink to the canonical AGENTS file (175 lines,10508 bytes). No competing home-level instruction files, user rule directory or visibility exclusions found. Four custom skills resolve to the canonical tree. No fresh interactive `/context` inspection or model-backed prompt audit was run; filesystem/configuration wiring is confirmed, actual fresh-session context loading remains unverified. This distinction follows [Claude memory/discovery documentation](https://code.claude.com/docs/en/memory).

A representative Terraform checkout has no project-local root instructions. The team configuration checkout has its own larger CLAUDE.md and project-specific worktree/orchestration rules. Project instructions have intended precedence; no company file was edited and this is not automatically classified as a conflict. Claude Superpowers installation was not established; Codex's installed skill catalogue alone is not evidence for Claude.

Confirmed stale cache: `~/.claude/projects/-home-slnnk/memory/ai-knowledge-base-git-policy.md` and its MEMORY.md pointer retain the old claim that gitignore only contains `.env`, plus obsolete publication handoff guidance. Current canonical rules and gitignore supersede them. Candidate stage3 correction: replace detailed cache policy with a short canonical pointer. Small index size does not demonstrate memory bloat; detailed notes are not assumed to be loaded automatically.

## Artifacts and changed files
Generated artifacts under `~/ai-data/agent-audit/2026-10-19/`: `agnix-report.json`, `agnix-stderr.txt`, `scan-manifest.json`, `codex-discovery-inventory.json`, `codex-prompt-probe.json`, and minimal release metadata/archive under downloads. The offline probe helper is `~/ai-data/agent-audit/probe_codex_instructions.py` with `--help` and sanitized output only. Installed binary is outside the KB repository. Persistent KB changes are this log, the research completion follow-up, TODO reconciliation and indexes/sync summary.

## Status and risks
Pilot1 is complete. The central TODO holds the next optional step selection and the stage3 findings; no new live task list is maintained here. Subsequent rule/cache fixes require the corresponding implementation request. No unrelated repository changes were staged, committed, pushed or discarded. No secrets were copied into the report. The SHA verifies the download against GitHub's release digest, not an independent security audit of the tool. Linter heuristics are useful signals, not authoritative instruction/permission semantics.

## User adoption decision (2026-10-19)
After discussing the results and distinguishing the linter from the broader audit, the user explicitly chose to keep agnix. Retain the isolated installed version as an optional manually invoked report-only check after instruction/skill/agent-setting changes. Review diagnostics before deciding on fixes. Do not enable auto-fix, every-start hooks or a mandatory completion gate on the basis of this decision. The rule/cache findings remain part of the separate proposed stage3 work, not authorized implementation.

## Portability follow-up requested (2026-10-19)
The user asked to add a task to document installation/setup rules for the AI knowledge repository on another PC. The isolated agnix binary is outside the synchronized repository; its version and provenance are documented, but automated provisioning is not implemented. The central TODO now tracks the requested documentation covering repository layout, agent links, prerequisites, secret/non-Git data handling, external tools and first-run checks. This request adds backlog scope only; no bootstrap implementation, installation on another machine or external change was performed.

## Step3 completion (2026-10-19)
The user subsequently authorized the audited local-rule fixes. The [correction record](2026-10-19-knowledge-base-local-rule-corrections.md) supersedes earlier pending/deferred statements for the stale Claude cache, ambiguous canonical paths and KB-cwd Codex duplication: all three were corrected and verified; five fresh regression sessions passed17/17 checks, native loading is one full policy copy in three directories, and agnix reports0errors. Approval policy and canonical skills remain intact. Claude model-backed evaluation remains blocked separately; later steps4-9 still require selection.

## Adoption mode superseded (2026-10-19)
The user subsequently explicitly requested mandatory post-edit agnix and the change-aware sync fallback. The [implementation record](2026-10-19-knowledge-base-agnix-enforcement.md) supersedes the optional/manual-only adoption direction above. Agents must run the report-only helper after changing agent instructions/skills/settings; normal sync also checks changed inputs before the same-day Git skip. Auto-fix and Git-blocking gates remain disabled. The prior personal learning record is historical/superseded; the current global rule points to AGENTS. This changes the adoption mode, not external publication permissions.
