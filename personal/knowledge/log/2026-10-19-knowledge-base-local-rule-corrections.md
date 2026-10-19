---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, instructions, agnix, regression]
---
# Knowledge base: audited local instruction and cache corrections

## Summary
Step3 explicitly authorized and completed: disambiguated repository/skill/map paths in shared AGENTS, replaced obsolete Claude cache policy with canonical pointers, and removed the extra Codex copy of global rules when cwd is the KB repository. Native offline loading is now one complete policy copy in each of three tested directories, with all four custom skills discoverable. Five fresh skill-enabled regression sessions passed17/17 artifact assertions. Approval rules and external-action restrictions remain intact. Actual Claude session behavior remains unverified because access is blocked, tracked separately in central TODO.

## Task and context
The user requested step3 from the [original trial order](2026-10-19-knowledge-base-agent-capabilities-research.md): implement justified fixes from [pilot1](2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md), then check behavior using [pilot2 scenarios](2026-10-19-knowledge-base-skill-evaluation-pilot.md). Pilot2 did not demonstrate an incremental quality benefit or justify deleting skills or broad policy compression. This task addresses confirmed ambiguity, duplication and obsolete cached guidance only.

## Changes
- `~/ai/AGENTS.md`: startup repository lookup explicitly selects current or personal catalog; catalog maintenance explicitly names the relevant layer. Three links that were interpreted relative to Claude's runtime symlink directory are now portable, unambiguous home-based paths to the canonical skill and workflow map. Permission statements were preserved.
- `~/ai/AGENTS.override.md`: a small KB-workspace override tells Codex to apply the full canonical policy already loaded through its global link. If that policy is absent, it explicitly requires reading `~/ai/AGENTS.md` before work. It adds no exceptions, permissions or competing policy. Global agent symlinks were not moved or replaced.
- `~/.claude/projects/-home-slnnk/memory/ai-knowledge-base-git-policy.md`: obsolete ignored-file and publication-handoff claims replaced with a canonical pointer to AGENTS, README Daily sync and the current gitignore. Original origin-session metadata retained, modification date updated. No new consent is implied by cache text.
- `~/.claude/projects/-home-slnnk/memory/MEMORY.md`: changed only the matching cache-description line; the unrelated team-configuration entry remains byte-identical.

Original task-touched files are backed up under `~/ai-data/agent-audit/2026-10-19-stage3/before/`. History is retained in the earlier pilot notes and private generated backups. The cache is runtime-local and outside KB Git; the canonical correction and rationale are recorded here.

## Loading verification
The override follows [official Codex AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md): one selected instruction file per project directory, with project override preferred over project AGENTS. It does not replace the separate global policy file. The installed runtime, rather than documentation alone, was tested with `codex debug prompt-input` through the existing sanitized probe helper. It saves counts and hashes, never raw prompts.

| cwd | Full canonical copies before | After | Four custom skill metadata entries |
|---|---:|---:|---|
| `/home/slnnk` | 1 | 1 | all present |
| `/home/slnnk/ai` | 2 | 1 | all present |
| `/home/slnnk/git/selectel-tf` | 1 | 1 | all present |

The KB-cwd rendered prompt shrank from38505 to28349 bytes; this is serialized prompt size, not billed tokens or a promised cost reduction. Probes are offline and make no model call. The outer sandbox's read-only Codex runtime initially blocked startup; the same command succeeded with approved host execution. No Codex configuration, model, global override or global instruction-link migration was introduced. A different PC still needs the installation/setup work already in central TODO; absent global policy is covered by the project pointer's required read, not automatically inlined by the runtime.

## Agnix verification
Manually ran retained agnix0.59.0 in report-only JSON mode on the original eight inputs plus the new override. Before:3errors/5warnings/1info. After:0errors/4warnings/2info, exit0. Three REF-002 errors and the ambiguous-repository-path warning disappeared. New CDX-AG-008 info correctly documents intentional project override precedence. Remaining prompt-engineering prohibitions and the service-tier warning are the previously classified advisory findings; they do not justify changing user consent, secret handling or model settings. The generic overview information remains advisory. No auto-fix, hooks or mandatory gate was installed.

## Behavioral verification
Reused the strengthened pilot2 runner unchanged, in a fresh generated output directory, with the skill-enabled condition and identical synthetic tasks. Five independent Codex exec sessions completed, all17assertions passed:
- task-scoped correction changes only the requested response, not permanent rules;
- explicitly authorized durable correction preserves existing project scope and rule;
- discussion causes no implementation;
- requested edit preserves foreign content and the synthetic staged-state representation;
- a created MR receipt followed by GET403 retains MR identity, does not plan duplicate creation, and leaves pipeline verification unknown.

An independent review inspected all event logs and exact before/after changes. Writes were limited to the respective fixture's response.md, rules.md, app.txt or decision.json. No Git command, external API/network call or publication occurred. Existing four skill files and both runtime settings files match their pilot1 SHA256 hashes. Both supervised approvals and external-state consent rules retain their meaning. The unchanged global consent paragraphs remain canonical, not copied into the cache.

Regression tokens reported natively:324793 input+output, including cached input; per-run timing and cache counters are retained. Existing configured model and authentication were reused. This is a single-repeat synthetic regression, not proof of real Git-index protection, API recovery reliability, approval UI behavior or Claude runtime behavior. Claude's known organization access failure was not retried because account access was not changed by this task.

## Artifacts and key commands
Generated artifacts: `~/ai-data/agent-audit/2026-10-19-stage3/`: before snapshots/hashes, `codex-before.json`, `codex-after.json`, `agnix-after.json`, unchanged runtime/skill hash assertions, `run_regression.py`, `regression/summary.json` and per-run events/fixtures/grading/timing.

```bash
python3 ~/ai-data/agent-audit/probe_codex_instructions.py --help
python3 ~/ai-data/agent-audit/2026-10-19-stage3/run_regression.py --help
```

The regression wrapper refuses to overwrite an existing attempt. No automatic model calls or scheduled checks were added. Rollback, if separately requested, consists of restoring only the task-touched files from the before snapshots and removing the task-created project override; preserve subsequent changes. No rollback was performed.

## Status and risks
Step3 complete on October19. Earlier statements that these fixes were unapproved or deferred are historical and superseded by this user request and result. [Central TODO](../../../TODO.md) tracks choosing step4-9, installation on another PC and the separate blocked Claude evaluation. No new live task list is kept here. Optional broad cleanup and expanded adversarial/repeated scenarios remain proposals. KB lint completed with0errors and6existing warning categories (global AGENTS size and five older company notes with Cyrillic prose). Indexes rebuilt with0missing frontmatter in the affected personal layer; no broad instruction compression or unrelated note edits were justified. There is no new standalone portable recipe or duplicate system map.
