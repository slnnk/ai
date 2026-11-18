---
system: codex
status: verified
checked: 2026-11-18
tags: [codex, configuration, performance]
---
# Codex global configuration performance review

## Task

Review the global Codex configuration and identify useful settings for everyday operation, including latency and resource use. The first response covered performance. The user clarified that the requested review also covered practical settings beyond speed. This clarification applies to this task. The user requested a discussion and review.

## Context

The global configuration for Codex CLI 0.170.0 is linked from `~/.codex/config.toml` to [the canonical file](../../codex/config.toml). The file sets `gpt-6.2-sol`, reasoning `medium`, service tier `default`, a context window of 872,000 and an automatic compaction threshold of 800,000. Project, per-invocation and managed settings can affect the effective values. See [configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence).

## Actions

Parsed the canonical TOML and checked the symlink. Compared the relevant settings with the current OpenAI manual, the locally cached model catalog and `codex features list`. Read only selected event types and numeric usage fields from the local session cohort. No new model requests or startup benchmarks were run.

## Findings

- Keep Sol with `medium` and Standard as the global defaults. For short scoped tasks with an easy correctness check, `codex -c 'model_reasoning_effort="low"'` is a per-invocation option. The local Sol catalog advertises both effort levels and defaults to `medium`. Lower effort may reduce reasoning work. Compare total elapsed time, reasoning tokens, correctness and any rework before promoting it to a default. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
- Use `/fast` selectively in supported ChatGPT-authenticated CLI sessions when generation latency matters. It retains the selected model and effort. The config spelling is `service_tier = "fast"`, mapped to the request tier `priority`. For Sol, Fast uses 2× included usage or credits at the published ChatGPT rates. Ultrafast requires account or workspace eligibility, uses 6× included usage and is advertised at up to 4.5× Standard generation speed for GPT-6.2. Whole-task speed and local entitlement were unmeasured. [Speed controls](https://learn.chatgpt.com/docs/agent-configuration/speed), [pricing](https://learn.chatgpt.com/docs/pricing#speed-multipliers).
- Keep the current context configuration for latency purposes. The local catalog advertises 500,000 default context tokens, an 872,000 maximum and 95% effective capacity. The 82 active-session files for November 12–18 included 12 Sol sessions with usage. Across 669 recorded Sol usage events with positive last-input counts, the median model input was 87,455 tokens, the 90th percentile was 171,072 and the maximum was 195,806. The reported effective window was 828,400. Cached input accounted for 98.2% of the summed input across those records. Event records can repeat a usage snapshot, the sample excludes archived sessions and the aggregate is neither billed usage nor a latency measurement. Lowering the configured window or compaction threshold above these observed inputs would offer no expected benefit for this sample. A substantially lower threshold could add compaction work and lose detail in long sessions.
- Tune MCP only if delays appear specifically at startup. The global configuration has HetrixTools with a 30-second startup timeout and OpenAI Developer Docs with the default per-server startup timeout. The reference documents a separate default 1,000 ms grace for optional servers during initial tool-catalog construction. Startup timeouts bound failure waits. Moving an infrequently used integration to a trusted project scope would reduce its global initialization and tool surface, at the cost of availability in other directories. No startup delay was measured. [MCP configuration](https://learn.chatgpt.com/docs/config-file/config-reference).
- The installed CLI reports `shell_snapshot` already enabled. Leave `tool_output_token_limit` and `project_doc_max_bytes` at defaults. Lower global limits can remove diagnostic output or instructions. Bound individual verbose command output and split unrelated work into fresh threads if prompt growth becomes a problem.

## Everyday configuration

- Terminal notifications and navigation. The existing footer already shows model, effort, directory, thread, run state, context, limit, tokens and task progress. Use `/statusline` to adjust it and `/title` to display project and thread in terminal tabs. Built-in notifications default to enabled and unfocused. An explicit `tui.notifications = ["approval-requested"]` narrows alerts to approvals. Include `agent-turn-complete` to keep completion notifications as well. Delivery depends on terminal support. Use `codex --no-alt-screen` to try native terminal scrollback. The equivalent persistent setting is `tui.alternate_screen = "never"`. [Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced), [CLI slash commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli).
- Reasoning by workflow. Optional `plan_mode_reasoning_effort = "high"` increases the effort for native Plan Mode when the plan itself needs deeper reasoning. Optional `review_model` pins the model for `/review`. With no override, review uses the current session model. Pin a different model only if that distinction is useful on repeated reviews. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
- Repeatable profiles. Use a separate `~/.codex/deep.config.toml` containing the few desired overrides, for example `model_reasoning_effort = "high"`, and start with `codex --profile deep`. Trusted project settings take precedence over profiles. For a single run use a flag or `-c`. On CLI 0.170.0, an isolated `codex mcp list` comparison showed a dummy server entry only when the profile was selected. The check verified profile loading and config acceptance. It did not start a server or test the interactive UI or model behavior. [Profiles](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles), [precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence).
- Scope tools and access. Keep reusable MCP servers global and repository-specific integrations in trusted project configuration, as with [Ansible MCP](../../codex/ansible/config.toml). Use `enabled_tools` or `disabled_tools` only if a particular server exposes a tool set wider than that workflow needs. For one-off inspection use `codex --sandbox read-only` when shell writes are unnecessary. For live public sources use `codex --search` when freshness matters. The documented default is cached search. Keep environment filtering, additional writable roots, memories and hooks tied to a concrete use case. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic).

## Local instruction loading

The user clarified that the remaining interest was whether configuration can improve local rule loading, without a specific recurring problem.

- Keep the default `project_doc_max_bytes` of 32 KiB. It caps the combined project instruction chain. Increase it when a specific repository demonstrably truncates useful instructions. The shared `AGENTS.md` is 5,618 bytes and the KB project override is 404 bytes. An isolated offline render with CLI 0.170.0 and the real instruction files showed one complete global copy in both the home directory and the KB root, plus one project override only in the KB root. The probe used a temporary Codex home with a link to the actual global instructions. It did not audit every repository or benchmark rule adherence.
- Leave `project_doc_fallback_filenames` and `project_root_markers` unset. The former is useful for an existing repository convention when no `AGENTS.md` is present at that directory level. The latter is useful for a documented non-Git root marker. The current shared-file link and small KB override already address duplicate loading.
- Keep skill discovery enabled. `skills.max_context_tokens` limits the initial skill catalog. Change it only if discovery is losing relevant entries or a measured catalog is unnecessarily large. `skills.config` can disable a particular unused skill when appropriate. The explicit-request convention for Superpowers is already in the shared rules.
- `model_instructions_file` replaces the built-in base instructions. It is unsuitable for adding the shared local policy. Hooks can enforce a specific mechanically testable rule after an observed recurring failure. Keep the existing scoped instructions and lint workflow while no such need has been identified.

Sources include [AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and the [previous duplicate-loading correction](2026-10-19-knowledge-base-local-rule-corrections.md).

## Changes

Recorded the broader review under the existing closed investigation in [the backlog](../../../TODO.md#knowledge-base). The global configuration and runtime link were unchanged.

## Status and risks

The user declined the settings proposed in the everyday configuration review. The additional local instruction review found no setting that needs enabling for the checked setup. On 2026-11-18 the user explicitly closed the task and decided to keep the current configuration. No follow-up is pending. No end-to-end notification or model test was run. No background operations remain.

## Portable lesson

none

## Task metrics: codex-config-performance-review-2026-11-18

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "codex-config-performance-review-2026-11-18",
  "created": "2026-11-18T23:20:44.539308+03:00",
  "first_result": "fail",
  "final_result": "pass",
  "state": "closed",
  "kind": "research",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": 1,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "The first review covered speed only. The clarified local-instructions review verified one complete global copy from home and the KB root in an isolated CLI render.",
  "updated": "2026-11-18T23:28:31.543960+03:00"
}
```
