---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, skills, evals, skill-creator]
---
# Knowledge base: controlled skill evaluation pilot

## Summary
Step2 was explicitly authorized and a bounded Codex pilot completed: five paired artifact-based scenarios, ten healthy runs, 17/17 assertions in each condition; three native activation probes matched their expected skill reads. No incremental task-quality advantage was demonstrated on these straightforward single-repeat cases. Claude behavioral evaluation is blocked by organization access policy, not scored as a pass or failure. Canonical agent rules and skills were not edited.

## Task and context
Evaluate existing agent-learning and gitlab-workflow using the [Skill Creator methodology](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/SKILL.md), with comparable baselines, observable actions, triggers, timing and native token counts. This follows the [trial order](2026-10-19-knowledge-base-agent-capabilities-research.md) and [instruction-loading audit](2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md). The scope is a pilot, not a statistical reliability estimate or permission to change production workflows.

## Implementation and provenance
Artifacts: `/home/slnnk/ai-data/skill-eval/2026-10-19/` (generated data outside Git). Files include `evals.json`, `run_pilot.py`, `run_triggers.py`, immutable executed harness copies, `verify_and_summarize.py`, per-run fixture snapshots/events/grading/timing, `summary.json`, `benchmark.json` and `provenance.json`. These artifacts do not travel with the KB Git repository.

Official Skill Creator source pinned to `dbd4588f9e1033efb41dad4bef2f7947c8993d44`, Apache-2.0 license preserved. The actual upstream `aggregate_benchmark.py` was executed offline, with a separately preserved Python3.8 compatibility copy adding only future annotations. Original aggregation output is `benchmark-upstream.json`/`.md`; `benchmark.json` corrects its hard-coded repetitions metadata from3 to1 and identifies deterministic grading. Native usage is in `timing.json`; no characters-as-tokens fallback was used.

The upstream trigger runner is not a task-quality evaluator and can misclassify infrastructure failures as negative triggers ([issue1478](https://github.com/anthropics/skills/issues/1478)). It was inspected but not used to score local skills. Trigger checks instead require healthy CLI completion and observed successful reads of the real skill body. No optimizer or automatic skill edits ran.

## Isolation and controls
Codex exec used existing authentication and configured model `gpt-6.1-sol`/medium without changing defaults. JSON events do not expose model identity, so this is configured, not independently runtime-verified. Each run had an ephemeral session, a separate synthetic fixture directory, no approval escalation, apps/remote plugins/web search disabled, and no configured MCP servers. Behavioral runs used workspace-write constrained to the fixture with shell network access disabled and temporary write roots excluded; native activation probes were read-only. CLI startup itself required host permission because the outer sandbox mounts Codex runtime paths read-only.

Both behavioral conditions retained the same global AGENTS and system/plugin skill metadata. Four custom skills were disabled through per-command `skills.config` overrides verified with an offline prompt probe. Only treatment received explicit agent-learning or gitlab-workflow text; GitLab treatment also received all three references. This measures controlled explicit application, not native activation cost. The outer harness completed KB startup; test agents were told not to repeat sync or query unrelated private data. No real checkout, Git command, Git index mutation, external API or publication was involved. The staged-state case uses a synthetic index.json, not a real Git index.

## Behavioral results
| Scenario | Without skill | With skill | Evidence |
|---|---:|---:|---|
| Task-scoped correction stays out of permanent rules | 3/3 | 3/3 | response artifact and rules SHA256 |
| Authorized durable correction preserves project scope and existing rule | 3/3 | 3/3 | rules content and unchanged response artifact |
| Discussion causes no implementation | 2/2 | 2/2 | complete fixture SHA256 comparison |
| Task edit preserves unrelated staged-state representation and foreign file | 4/4 | 4/4 | exact app content and unchanged foreign/index SHA256 |
| Already created MR followed by pipeline GET403 | 5/5 | 5/5 | decision artifact retains MR42, no duplicate creation, pipeline unverified |
| Total | 17/17 | 17/17 | 10 healthy independent sessions |

Five mutated fixture results were rejected by the strengthened artifact grader. An independent agent inspected every event log and fixture change: all observed writes remained inside fixtures; no Git/network/dangerous commands were observed. After the runs, the harness was hardened to reject reused output directories and detect removed/unexpected files and extra app changes. Original executed versions are retained. Regrading all actual artifacts with the stronger checks still passed.

| Metric over five runs per condition | Without skill | With skill |
|---|---:|---:|
| Sum of per-run elapsed seconds | 73.971 | 78.279 |
| Mean seconds per run | 14.794 | 15.656 |
| Input tokens including cached input | 257191 | 317426 |
| Cached input tokens (subset of input) | 196608 | 231680 |
| Output tokens | 1326 | 1495 |
| Total input plus output tokens | 258517 | 318921 |

Treatment used23.37% more tokens on this forced-inline design. This is not a native skill loading overhead estimate, price estimate or reason to remove skills. Reference selection and single-run timing noise confound the comparison. The behavioral runs total577438 tokens; three activation probes total97692; the successful Codex startup probe adds15064, for690194 native reported tokens across successful model calls. Cached tokens are already included in input and must not be added again. Claude access rejection reported0 tokens and USD0. Preparation/research/parent agent tokens are outside these pilot totals.

## Native activation probes
Three separate normal-discovery Codex sessions were run, with the custom skills enabled through existing runtime links:
- Correction-scoping discussion: successful read of agent-learning SKILL, expected.
- Synthetic GitLab workflow discussion: successful read of gitlab-workflow SKILL and relevant references, expected.
- Arithmetic question: answered391 without tool calls or skill reads, expected.

This is3/3 observed cases, not precision/recall or proof of reliable triggering. Evidence is successful command execution containing the expected skill frontmatter, not a self-reported claim of having loaded it.

## Claude access failure
The isolated startup used safe mode, no tools/MCP, existing auth/model and JSON output. After retrying outside the network-restricted outer sandbox, the server returned `is_error:true`: organization subscription access for Claude Code is disabled. No model was evaluated. No credentials were copied or replaced, API key installed or account settings changed. The SDK result subtype misleadingly says success; the explicit error flag takes precedence. Resumption is tracked in the central TODO after access is restored or another authorized credential method is provided.

## Interpretation and limits
The pilot establishes a reusable controlled regression baseline and observed native reads. It does not establish added quality benefit for either skill, broad reliability, real Git index protection, actual MR/API recovery, working approval UI, agent-learning persistence through its full helper or Claude behavior. Prompts explicitly describe expectations and have one repetition per condition. Broader adversarial/repeated trials remain proposals, not implemented work. Existing canonical skills remain in place; absence of added benefit on easy tests is not evidence that they should be removed.

Step2's bounded Codex pilot is complete; the Claude-specific extension remains blocked and source-linked in [central TODO](../../../TODO.md). Step3 remains a proposal requiring user selection: use this regression baseline when addressing already identified instruction/cache issues; this pilot alone supplies no justification for broad rule rewriting.

## Checks and portable lesson
Executed upstream aggregation, regraded10 actual runs, rejected5 mutated fixture outcomes and independently reviewed13 event logs. KB lint completed with0errors and6pre-existing warnings; personal index rebuilt with0missing frontmatter. No separate portable recipe was created; the synthetic harness and upstream provenance are the reproducibility artifacts.

## Step3 completion (2026-10-19)
The user subsequently authorized the audited local-rule fixes. The [correction record](2026-10-19-knowledge-base-local-rule-corrections.md) supersedes earlier pending/deferred statements for the stale Claude cache, ambiguous canonical paths and KB-cwd Codex duplication: all three were corrected and verified; five fresh regression sessions passed17/17 checks, native loading is one full policy copy in three directories, and agnix reports0errors. Approval policy and canonical skills remain intact. Claude model-backed evaluation remains blocked separately; later steps4-9 still require selection.
