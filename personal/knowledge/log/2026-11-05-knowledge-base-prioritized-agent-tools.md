---
system: knowledge-base
status: verified
checked: 2026-11-05
tags: [agents, skills, tools, research, priorities]
---
# Prioritized agent methodology, skills and tools recommendations

## Summary

The user requested concrete skills, rules and tools suitable for the existing agent
methodology and a complete recommendation list ordered by priority. This dated
snapshot combines unresolved findings from the current dialogue with new candidates;
it does not introduce permanent policy. The dialogue-only recording scope remains.
Twenty recommendations are ordered by observed risk, breadth of usefulness,
integration effort and overlap with existing capabilities. Ranks 1–5 address known
defects; 6–12 improve validation and context management; 13–18 are scoped candidates;
19–20 are deferred until a specific need appears. Ranking is an engineering judgment,
not a measured improvement or popularity score. F1 is already fixed and excluded from
unfinished work. No tools, skills, hooks, plugins or runtime settings were installed.
The central TODO remains the sole live backlog and references this evidence snapshot.

## Task

Search for skills, rules, tools and related capabilities that could benefit our local
agent workflows, then return the full combined set of recommendations sorted by
priority. Research and recording apply within the current dialogue. Installation,
activation and implementation are not authorized by this request.

## Context

- [Original methodology findings](2026-11-05-knowledge-base-agent-methodology-review.md).
- [Developer practices and scope correction](2026-11-05-knowledge-base-developer-best-practices-research.md).
- [Completed F1 fix](2026-11-05-knowledge-base-sync-checker-failure-stop.md).
- [Earlier research](2026-10-19-knowledge-base-agent-capabilities-research.md) remains
  historical; its cancelled Claude pilot is not reopened.
- [Central TODO](../../../TODO.md), Knowledge base, contains the current action status.

## Actions and inventory

Applied skill-installer to fetch the current OpenAI curated catalog read-only through
its official helper. Used primary maintainer repositories/docs and inspected actual
candidate SKILL.md files rather than selecting by repository popularity. Independent
review covered skills, validation/eval tooling and context tools; parent owned writes.

Confirmed local skill entries: agent-learning, android-dig, gitlab-workflow and rp.
OpenAI skill-creator/openai-docs/skill-installer are present under the system directory.
Catalog `installed` annotations only inspect the catalog's expected install location;
they incorrectly appear false for an available system skill such as openai-docs and
must not be used as a complete runtime inventory. Available plugin skills also remain
subject to their explicit invocation rules.

Managed agnix exists at `~/.local/share/agnix/current/agnix`, although not on PATH.
Terraform is on PATH. Gitleaks, ShellCheck, Lychee, Promptfoo and Repomix were not found
on PATH; this does not prove absence from every environment/container. Existing
unittest and fake-Git tests, KB search/lint, instruction lint, indexes and sync are
retained. No new model-backed evaluation or third-party scanner was run.

## Complete priority snapshot

These ranks identify recommendations in this dialogue; original review IDs F2–F7
remain in parentheses. The rows are evidence and selection options, not a second
independent live task list. Current status is maintained in central TODO.

| Rank | Recommendation | Purpose and concrete limit | Effort / condition |
| --- | --- | --- | --- |
| 1 | Scan publishable staged content with Gitleaks (F2) | Cover non-Markdown text and use index bytes; stop on findings and scanner failure. Distinguish diff scanning from a full staged-file/snapshot scan. | Medium; highest priority |
| 2 | Reject unavailable inputs and incomplete checks (F4) | Validate requested roots/layers and distinguish empty results from failed inspection in existing helpers. | Small–medium; known defect |
| 3 | Preserve exact and task-relevant learning results (F3) | Prioritize exact keys/applicability; globals must not consume the entire result quota. | Small–medium; known defect |
| 4 | Reconcile canonical instructions and scope (F5) | Resolve rp/import/template conflicts; preserve dialogue/task scope and one owner per rule. | Medium; known contradictions |
| 5 | Validate instruction dependencies, trial Lychee (F7) | Repair known dead path; cover instruction/reference targets and anchors, first offline. | Small–medium; local path compatibility required |
| 6 | Behavior suite using native Codex JSON events | Extend existing pilot with explicit/implicit/negative skill cases and actual outcomes; reuse OpenAI skill-creator instead of replacing it. | Medium; separate model-run decision |
| 7 | Improve KB ranking against the saved suite (F6) | Keep canonical answers visible as logs grow; retain the accepted baseline and decision presentation. | Medium; measured ranking regression |
| 8 | Scope startup context and bound tool output | Load applicable procedures/sections; expose truncation, result coverage and routes to detail. | Medium; preserve essential boundaries |
| 9 | Compact task resumption state | Goal, authorized scope, decisions, uncertainty, checks and next permitted step in the existing task record. | Small; no second backlog |
| 10 | Bounded delegation, task-appropriate models and one coordinator | Use independent-work/volume criteria; trial a lower-cost model for narrow tasks, with coordinator verification and ownership of shared sync/TODO/index changes. | Small–medium; routing is proposed, not configured |
| 11 | Compare procedural simplifications | Change one component at a time; correctness/permissions first, then time, reads and tokens. | Medium; needs an agreed comparison set |
| 12 | ShellCheck for changed shell scripts | Add a report-only static check alongside bash syntax and meaningful regression tests. | Small; no bulk auto-fix or hook installation |
| 13 | OpenAI cli-creator | Reuse its interface design for durable Python helpers, bounded JSON and read/write separation. | Scoped pilot; do not rewrite every helper or copy runtime/path defaults |
| 14 | HashiCorp terraform-style-guide and terraform-test | HCL review and module plan/mock assertions while preserving pinned providers and task scope. | Scoped Terraform task; tests can create resources by default |
| 15 | OpenAI security-threat-model; targeted security-best-practices | Inspect trust boundaries in agent tools; language-specific review only where supported. | Explicit security task; not a secret scanner or whole-stack guarantee |
| 16 | Context7 | Version-aware public documentation when existing official-doc search is insufficient. | Conditional; hosted queries and privacy/coverage constraints |
| 17 | Serena | Symbol/reference navigation in a selected large code repository. | Conditional; LSP dependencies, language support and privacy configuration |
| 18 | OpenAI playwright | Reproducible browser investigation when APIs/connectors do not cover the workflow. | Conditional; browser/runtime dependencies and existing write approvals |
| 19 | Promptfoo | Broader provider comparisons and evaluation reporting when the native runner becomes insufficient. | Defer for a small single-client suite |
| 20 | Repomix | Export a limited, reviewed context snapshot to an agent without direct filesystem access. | Defer until an actual export need; no daily full-KB packing |

## Candidate evidence and integration boundaries

### Gitleaks and ShellCheck

[Gitleaks](https://github.com/gitleaks/gitleaks) supports Git, directory and stdin
scanning. Current [Git command code](https://raw.githubusercontent.com/gitleaks/gitleaks/master/cmd/git.go)
and [source reader](https://raw.githubusercontent.com/gitleaks/gitleaks/master/sources/git.go)
show that `git --staged` reads staged diff hunks, not the entire snapshot. For full
changed-file coverage the integration must inspect staged blobs, not working files.
Default exit 1 can mean findings or failure: both must stop publication with distinct
diagnostics. Use redacted reports, a reviewed pinned version and narrow fixture
exceptions; test non-Markdown formats, partial staging and scanner errors. This
complements existing KB structure/layer checks, not a guarantee of detecting every secret.

[ShellCheck](https://github.com/koalaman/shellcheck) provides static shell diagnostics
and standalone binaries. Proposed first use is reporting on changed shell scripts.
It does not establish end-to-end correctness of the sync gate; retain behavioral
fixtures and explained, narrowly scoped suppressions.

### Lychee

[Lychee CLI documentation](https://lychee.cli.rs/guides/cli/) documents `--offline`
and fragment checking through `--include-fragments`. Before adopting it, check our
absolute paths, `~`, `current` symlink and heading conventions with isolated examples.
Inline-code paths are not ordinary Markdown links: normalize dependencies into
checkable references or validate those paths explicitly. External URL checks are a
separate choice. Link correctness cannot prove rule applicability or factual freshness.

### Native evaluation and Promptfoo

[Current Codex non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
and local help support JSON events and structured final output. Use a small Python
runner with isolated fixtures, respecting sandbox/approval restrictions. Older eval
examples containing `--full-auto` must not be copied without checking current options;
current documentation marks it unsupported. [OpenAI's skill-eval method](https://developers.openai.com/blog/eval-skills)
provides useful positive/negative case patterns. A trace and a formatted answer do
not alone establish correct final state.

[Promptfoo coding-agent evaluation](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/)
supports Codex integrations, assertions and traces. Its app-server provider launches
its own process. [Installation](https://www.promptfoo.dev/docs/installation/) currently
requires Node.js at least 22.22.0. This adds configuration and storage; consider it
when provider comparisons exceed a small native runner. [Custom exec providers](https://www.promptfoo.dev/docs/providers/custom-script/)
return text, so JSON printed to stdout is not automatically a structured provider result.

### Skills from OpenAI and HashiCorp

[OpenAI cli-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/cli-creator/SKILL.md)
fits durable CLI interfaces and separates read/write jobs. Its default Rust/new-folder
and credential-location suggestions must not override existing Python helpers, paths
or the layer `.env` policy. A narrow helper change may not warrant invoking it at all.

[HashiCorp style guidance](https://raw.githubusercontent.com/hashicorp/agent-skills/main/plugins/terraform/skills/terraform-style-guide/SKILL.md)
and [terraform-test](https://raw.githubusercontent.com/hashicorp/agent-skills/main/plugins/terraform/skills/terraform-test/SKILL.md)
are official focused candidates. Do not automatically upgrade providers from their
examples. Terraform tests default to apply and can create real resources; select
explicit plan/mock cases for an initial pilot and verify version support (mocks need
Terraform 1.7+). These skills do not grant external-action permission.

[OpenAI security-threat-model](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-threat-model/SKILL.md)
is an explicit-request analysis of trust boundaries and plausible abuse paths.
[security-best-practices](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-best-practices/SKILL.md)
has specialized support for Python, JavaScript/TypeScript and Go; it does not provide
equivalent guidance for the entire .NET/HCL/Ansible/shell stack. Neither replaces secret scanning.

[OpenAI playwright](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/playwright/SKILL.md)
uses browser CLI automation, snapshots and traces. It requires runtime/browser setup,
does not replace Android Appium and is distinct from a Playwright Test suite. Route
sanitized artifacts to `~/ai-data/`; external form submissions retain their approvals.

### Context7, Serena and Repomix

[Context7](https://github.com/upstash/context7) supplies external library documentation;
check actual library/version coverage on relevant questions. Ordinary local stdio MCP
still uses a hosted backend. Its [privacy policy](https://context7.com/docs/security/data-privacy)
describes LLM reranking and anonymous query retention outside Enterprise. Use neutral
public-documentation queries. A separately licensed [on-premise deployment](https://context7.com/docs/enterprise/on-premise)
exists but its operational overhead is not justified here as a replacement for local KB search.

[Serena](https://github.com/oraios/serena) offers symbol/reference tools through language
servers. Its [language matrix](https://oraios.github.io/serena/01-about/020_programming-languages.html)
includes Terraform and explicit Markdown support; Ansible is experimental and lacks
key symbol/reference/rename capabilities. Language dependencies need maintenance.
[Startup telemetry](https://oraios.github.io/serena/01-about/070_privacy.html) is enabled
by default and can be disabled; project data returned to the agent remains a separate
processing channel. Keep canonical memory in `~/ai` and review tool permissions for
the chosen project. This does not replace ordinary text search.

[Repomix](https://github.com/yamadashy/repomix) packages selected files with filtering
and token accounting. [CLI privacy](https://repomix.com/guide/privacy) differs from
uploading through its website. [Secretlint checks](https://repomix.com/guide/security)
do not remove the need to inspect exported material. Experimental [code compression](https://repomix.com/guide/code-compress)
omits implementation details; do not use that output as the sole source for script
correctness or permission reviews. Export snapshots also need freshness management.

## Candidates not recommended for immediate adoption

- Another universal instruction linter: managed agnix is already integrated. Keep it
  alongside kb_lint and targeted tests; no demonstrated replacement need was found.
- Replacing the available OpenAI skill-creator with [Anthropic's same-name skill](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md).
  Its A/B-eval ideas are useful, but its [trigger runner](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/scripts/run_eval.py)
  invokes Claude and writes Claude command files. It is not a drop-in Codex runner and
  does not authorize reopening the cancelled Claude evaluation.
- The current [OpenAI Sentry skill](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/sentry/SKILL.md)
  before a separate integration review. The new CLI supports [self-hosted endpoints](https://cli.sentry.dev/self-hosted/),
  but [explain/plan commands](https://cli.sentry.dev/commands/issue/) initiate AI analysis.
  A read-only label alone does not establish that every command is an ordinary GET.
- GitHub-specific publication shortcuts for a GitLab workflow, blanket Superpowers
  activation, mass skill-pack installation and an unmeasured vector-database migration.
- Applying model-specific recommendations, framework defaults or foreign secret paths
  as new permanent local policy without an implementation decision.

## Subagent model selection follow-up

The user asked whether delegating simpler subtasks to cheaper models is implemented.
Follow-up recorded on 2026-11-06 after the local date rollover. Read-only inspection
in the current dialogue found no subagent model/default reasoning settings
in `~/.codex/config.toml`, no custom TOML files in `~/.codex/agents/`, and no
`~/ai/.codex/config.toml`. The user config selects `gpt-6-astra` with `xhigh` reasoning
for its default model; this file alone does not prove a live UI session's effective
model, because a session may override it.

The actual subagent creation calls in this dialogue omitted model/effort overrides
and inherited the parent context/model. They therefore did not implement cheaper-model
routing. Portable prompts contain advisory `small`/`mid` labels, including Haiku/Sonnet
examples, but no concrete automatic mapping was configured or used here.

[Current OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
documents inherited model/reasoning defaults and explicit per-agent/default model
selection, including a lower-cost model for narrow work. Exact availability and runtime
selection must be verified in the selected client; a general capability is not proof
that a local configuration is active in this session.

Rank 10 now includes a proposed measured routing trial: simple extraction, inventory
and focused source lookup may use a lower-cost model; consequential reasoning and
final verification remain with a suitably capable coordinator. Give helpers compact
scoped context and compare correctness, retries, total tokens/cost and elapsed time.
Do not assume a lower per-token price or more parallelism reduces end-to-end cost.
No model settings, permanent routing rule or runtime agent were changed for this
question. It remains a current-dialogue proposal in the existing central TODO entry.

## Central backlog reconciliation

| Existing central group | Ranks and treatment |
| --- | --- |
| Automation checks F2/F4 | 1–2; Gitleaks is the concrete scanner candidate |
| Retrieval F3/F6 | 3 and 7; preserve exact-key/answer visibility |
| Instruction consistency F5/F7 | 4–5; Lychee is a candidate, existing scope rules retained |
| Context and coordination | 6 and 8–11; existing skill-creator/native CLI first |
| Earlier optional-agent-pilot selection | 12–20; updated with this dated shortlist, no installation permission |

This table is a point-in-time mapping. No source-note checkbox list is introduced.
Future completion is reflected in central TODO and dated outcomes here, preserving
historical rankings without pretending they remain current automatically.

## Changes and verification

Created this source-backed ranking and linked it to existing source notes and central
TODO entries; refreshed only affected display titles. Checked the current curated
catalog, local skill paths, selected executable availability and primary source text.
No deployment, model-run, install, hook configuration or permanent instruction edit
was made. API keys and secret values were not requested or printed.

## Status and risks

On 2026-11-06 the user requested further experiment ideas merged with the older
optional pilots. The [consolidated E01–E14 design](2026-11-06-knowledge-base-merged-agent-experiments.md)
maps this recommendation ranking to controlled comparisons, including model costs,
dialogue scope and concurrency. It introduces no installation or execution permission;
the twenty-item ranking is retained as dated selection evidence.

Research completed 2026-11-05. All twenty recommendations remain selection proposals;
the next action needs an implementation request. Local effectiveness has not been
measured for newly researched candidates. Tool upstream main branches and live docs
can change; review and pin the selected version at implementation time. All research
agents and commands finished; no background operations remain.

## Portable lesson

none
