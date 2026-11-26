---
system: jcode
status: verified
checked: 2026-11-25
tags: [agents, benchmark]
---

# Jcode and Codex CLI paired benchmark

## Task and configuration

Compare the installed Jcode v1.1.2 and Codex CLI 0.171.0 on paired synthetic tasks and connect Jcode to the shared knowledge base.

Linked `~/.jcode/prompt-overlay.md` to `~/ai/AGENTS.md` and linked the four custom skills from the same canonical paths as Codex. Verified that the imported skill copies matched their targets before moving them to `~/.jcode/skills-before-ai-links.kSIhL8`. Linked `~/.jcode/config.toml` to the [tracked Jcode settings](../../jcode/config.toml), including medium reasoning and no requested priority tier. Updated the [machine setup guide](../../../general/knowledge/knowledge-base/setup-another-pc.md#3-connect-instruction-and-skill-entry-points).

## Method

Five synthetic cases cover two Python edits, log diagnosis, configuration comparison and a small diff review. Each case gets three runs per client with fresh directories and sessions, alternating order, `gpt-6.2-sol`, and medium reasoning. Independent assertions and exact decoded JSON grade the results. Both clients use ChatGPT OAuth with matching account IDs. Actual backend tier or routing cannot be established from requested settings. Codex uses a temporary configuration with the shared instruction and skill links, without the normal MCP configuration.

The isolated Jcode profile rejected the requested model, but the installed profile accepted it and returned the expected smoke response. Codex could run inference in an isolated profile inside the external sandbox, but nested filesystem writes failed. A workspace-write smoke test succeeded with the external sandbox removed and Codex's own sandbox enabled. Discarded smoke and diagnostic passes from benchmark statistics.

## Results

The paired series completed all 30 attempts with 15 of 15 passing the external check on each CLI, without manual interventions. Medians for Jcode and Codex respectively were 9.12 and 9.30 seconds, 50,796 and 189,128 KiB peak RSS, 7,395 and 39,196 total input tokens, 4,608 and 33,280 cached input tokens, and 84 and 95 output tokens. Total time was 212.98 and 187.07 seconds. Codex was faster in 6 of 6 Python-edit pairs. Jcode was faster in 6 of 6 log and diff review pairs. Configuration comparison split 2 to 1 in favor of Jcode.

Jcode's JSON report returns only the last response usage. Summed persisted per-response usage for each Jcode session and checked the last response against the JSON report before comparison with Codex turn totals. Token and memory results characterize these headless setups. Peak RSS does not represent concurrent daemon or process-tree memory.

Jcode accessed knowledge-base files beyond the fixture in two Python edits, and in the third deduplication attempt also invoked the same-day sync helper despite the synthetic prompt's restriction. Both edits still passed the independent output checks. No analogous shell commands were observed in the Codex traces. The different sandbox policies matter when interpreting this behavior.

## Status

The instruction lint returned zero findings. The benchmark command exited successfully and no benchmark subprocesses remain. The runner, aggregation script, final raw client output and normalized `results.csv` are retained under `~/ai-data/jcode-codex-benchmark-2026-11-25/` for audit. Discarded transient profiles, smoke and failed setup logs and temporary fixtures.

## Upstream reuse assessment

Jcode provides structured tool events in headless NDJSON, including tool execution and completion. Its observable-outcome approach fits the existing paired benchmark. The useful extension is to grade task boundaries separately from artifact correctness, using only evidence visible in the captured runtime events. The two Jcode departures above supply concrete examples. Approval and filesystem enforcement remain separate from report-only grading. [Wrapper events](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/WRAPPERS.md) · [Measurement approach](https://github.com/1jehuang/jcode/blob/v1.1.2/docs/HARNESS.md#hill-climbable-measurements)

Jcode uses agentgrep, a standalone code-navigation CLI, to retrieve enclosing symbols or relevant file regions. It is a candidate for repository navigation with ambiguous symbols or call paths. The current exact-text and scoped KB search paths already serve their established roles. Local benefit has not been measured. [Jcode integration](https://github.com/1jehuang/jcode/blob/v1.1.2/crates/jcode-app-core/src/tool/agentgrep.rs) · [Agentgrep CLI](https://github.com/1jehuang/agentgrep)

Provider cache miss diagnostics and WebSocket prewarming are tied to the runtime. The local token usage helper already distinguishes cached and uncached traffic. The benchmark does not isolate a benefit from either optimization. This assessment records options without adoption or a new run.

## Task metrics: jcode-codex-cli-benchmark-2026-11-25

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "jcode-codex-cli-benchmark-2026-11-25",
  "created": "2026-11-25T00:47:23.165059+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "investigation",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Verified shared Jcode links and zero lint findings; 30 judged runs finished, with two Jcode departures from fixture scope recorded.",
  "updated": "2026-11-25T00:53:55.495956+03:00"
}
```
