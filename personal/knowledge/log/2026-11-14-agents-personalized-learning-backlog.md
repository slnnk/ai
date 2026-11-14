---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, learning, research, backlog]
---
# Personalized agent learning: research and reconciled backlog

## Task and authorization

The user wants agents to learn their engineering judgment from corrections, reducing
unnecessary implementation and human steering while preserving result quality.
Session 01a1d727-6401-7be0-ab41-a4ea664e6a74 initially prohibited all changes.
On November 14 the user lifted those session restrictions and explicitly requested
preparing TODO tasks and reconciling existing work. This authorizes this bookkeeping;
it does not select a product, authorize pilot execution or installation, cancel older
explicit decisions, or change standing publication/deployment permissions.

## Findings from the discussion

The examined deployment dialogue showed an unnecessary downloader after incomplete
inspection of the available image tools, speculative configuration-format support,
and piecemeal simplification after repeated user corrections. A database credential
choice also created substantial ordering logic: changing that choice required the
user's decision, but the agent could have exposed the simpler alternative earlier.
Company details and primary evidence remain in the
[existing company task log](../../../current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md#before_script-simplified-to-git-clone-script-simplification-discussed).
The existing simplest-sufficient-solution failure record is retained; this discussion
is not another independent occurrence or a second outcome for that task.

Proposed direction: keep concise before/after decision examples with rationale and
scope; retrieve them before approach selection; compare existing platform behavior
before adding mechanisms; reassess assumptions that cause whole dependency chains;
evaluate first attempts on subsequent tasks, separately from user-assisted recovery.
Do not translate a single task exception into a universal ban or equate fewer lines
with correctness. These are design proposals, not newly installed global rules.

## Research assessment

Official documentation, selected skill/source files and papers were inspected online
on November 14. No packages were installed, benchmark runs launched or production
integrations tested. Public branches are mutable; pin and verify a revision before
any future trial. Local storage does not imply local model processing.

| Candidate | Documented mechanism | Assessment for this user |
| --- | --- | --- |
| [TellOnce](https://github.com/YujunZhou/tellonce) | Correction-derived scoped rules, lifecycle updates, automatic injection and optional enforcement. | Candidate for mechanism comparison, not a selected tool; the earlier first-candidate ranking was an assistant recommendation. Default mode records/retrieves; deterministic content rules are not supplied. Codex support is experimental and final-output coverage differs. |
| [ECC continuous-learning-v2](https://github.com/affaan-m/everything-claude-code/blob/main/skills/continuous-learning-v2/SKILL.md) | Hook observations, background extraction, scoped atomic behaviors and confidence scores. | Potential observation mechanism; silence-based confidence and promotion heuristics conflict with existing explicit-evidence policy. Background observers require a separate decision. |
| [Letta Code](https://github.com/letta-ai/letta-code) | Stateful agent, versioned memory and learned skills; local backend available. | Conditional alternative if an existing-agent integration is insufficient; a different runtime, not a transparent add-on. |
| [Hermes](https://github.com/NousResearch/hermes-agent) | Persistent memory, session recall, skill creation and refinement. | Alternative for reusable procedures; not evidence of the user's engineering judgment being learned. |
| [ACE](https://github.com/ace-agent/ace) | Generation, reflection and incremental playbook curation. | Research design reference requiring integration, not a drop-in local solution. |
| [Claude-Mem](https://github.com/thedotmack/claude-mem) and [Hindsight](https://github.com/vectorize-io/hindsight) | Automated experience capture and context retrieval. | Consider only if retrieval is the demonstrated bottleneck; do not stack memory systems without evidence. |

[TellOnce research](https://arxiv.org/abs/2606.13174) evaluates later tasks with frozen
learned state; its published gains are not local measurements.
[PAST-Bench](https://arxiv.org/abs/2608.04003) reports uneven model/capability-dependent
benefits from retained experience. These support measuring transfer rather than
counting saved notes. The current learning skill already specifies provenance,
scope, explicit versus inferred rules and first-attempt outcomes; duplication alone
would not address the demonstrated implementation-selection failure.

## Reconciliation decisions

The sole live work list is [central TODO](../../../TODO.md#knowledge-base).

- Existing E02/E05/E06 supply scope, skill-use and decision-transfer evaluation;
  E12 supplies the targeted lifecycle integration. The new personalized-learning
  tasks own this bounded application; the old experiment selector retains other
  optional cases, not another run of the same work.
- Existing [F5/F7 methodology scope](2026-11-05-knowledge-base-agent-methodology-review.md) remains the owner of canonical instruction/skill reconciliation.
  Its scope now includes a minimal proposed learning-workflow diff, examples and
  pre-implementation solution selection. No parallel rewrite task was created.
- The November 20 company review remains one existing dated task. It should use
  first-attempt corrections and recovered outcomes from the deployment case;
  it is not contingent on selecting or installing a new tool.
- E01 model-delegation follow-ups and the Claude evaluation extension stay closed.
  Scoped startup/resumption was implemented November 14 and its optional evaluation
  was explicitly declined. Historical E07/E08 recommendations do not reopen that work.
- Completed retrieval ranking/coverage fixes stay completed. A future behavioral
  transfer test does not imply the fixed-script retrieval benchmark remains broken.
- Secret-scanner F2/F4 and factual staleness checks stay independent. They are not
  prerequisites for this learning comparison without a demonstrated dependency.

## Clarifications and current goal

The user questioned the TellOnce-first narrowing, whether useful solutions could be
combined, whether years of local knowledge work would be replaced, and whether the
original five proposals and goal had been recorded. The initial backlog hid several
of those proposals inside F5/F7. On the same date the user requested prioritizing
both tasks and pilots and displaying a detailed list. This authorizes backlog/design
updates, not executing the proposed pilots. No product choice is inferred.

Goal: agents should increasingly apply the user's engineering judgment to new tasks
on the first attempt, with fewer substantial corrections and unnecessary actions,
while maintaining correct results and existing permissions. Preserve useful local
knowledge and mechanisms; assess small repairs, borrowed approaches and compatible
components before any full replacement proposal. A complete migration would require
separate evidence and a user decision. Combining mechanisms is an option; changing
one factor at a time is an evaluation method, not a one-product architecture rule.

## Prioritized design

The ordered actionable entries live only in [TODO](../../../TODO.md#knowledge-base).
Priority labels specify dependency and expected value, not approval to execute.

| Priority | Design deliverable | Dependency and completion evidence |
| --- | --- | --- |
| P0.1 | Decision examples and failure diagnosis (original direction1). | Small source-backed before/after set with rationale and scope; distinguish observable failure stages; define separate unseen and negative cases and success criteria. Reuse the already examined deployment dialogue. |
| P0.2 | Compare mechanisms from all seven solutions against current capabilities. | Based on P0.1 gaps; one table of retained, borrowed, integrated or replaced mechanisms with compatibility, cost, ownership and data flow. No preferred product selected and no installation required for the desk assessment. |
| P1.1 | Relevant experience before choosing the approach (original direction2). | Minimal delivery/retrieval design justified by P0 findings; current sources and bounded context. Existing retrieval fixes remain complete. |
| P1.2 | Necessity checking before implementation (original direction3). | Minimal workflow design that checks existing analogues/tools, justifies deviations and exposes expensive assumptions before code is written; no blanket checklist or extra gate. |
| P1.3 | Consolidate ineffective or redundant instructions (original direction5). | Existing F5/F7 owns one coherent proposed diff for the selected mechanisms, including P1.1/P1.2. Preserve its source/import, scope and dependency concerns. A demonstrated mechanism gap may be fixed; do not add rules solely to restate them. |
| P1.4 | Pilot correction transfer (original direction4). | Compare current setup with one selected bounded change on unseen fresh-session cases. Criteria, case count, repetitions and budget agreed before a run. Successful transfer preserves correctness/scope and reduces substantial steering or unnecessary actions; small trials are directional evidence. |
| P1.5 | Adoption decision after any selected pilot. | Retain, revise or reject from actual behavior and maintenance cost. This decision occurs after P1.4 if it suffices; it does not wait for optional P2.1/P3.1. Preserve knowledge and one owner per mechanism. |
| P2.1 | Conditional lifecycle integration pilot. | Only for a remaining capture/delivery/check-timing gap demonstrated by P1.4. One compatible hook/tool; measure coverage, false positives, duplicate/recursive execution and all overhead. Skip if unnecessary. |
| P3.1 | Conditional alternative-runtime pilot. | Only for a persistent gap not resolved more simply. Choose Letta or Hermes for one comparison; account for migration and model/runtime confounding. No cancelled model-delegation or Claude trial is reopened. |

P1.2 preparation completed on November14: [necessity-check design](2026-11-14-agents-p12-necessity-design.md)
connects analogous solutions and verified capabilities to concrete requirements,
surfaces assumptions causing workarounds and preserves autonomous routine choices.
Eight documentary checks cover necessary and unnecessary complexity; no behavioral
trial or active instruction change was performed. P1.3 retains canonical-diff ownership.

Pilot1 example outcomes: recognize existing tools rather than add a downloader;
inspect the established deployment pattern; question an assumption that creates a
large workaround; avoid speculative format support; retain necessary complexity when
requirements actually demand it. Source-specific company evidence stays in its layer
and fixtures must be sanitized. Passing a known training case is not held-out transfer.

Measure first-attempt artifact correctness, substantial user corrections, unnecessary
actions, missed constraints and total time/token cost including capture and judging.
Keep model/effort/fixtures matched where possible, freeze learned state for the transfer
phase and include cases where a prior correction must not apply. No production writes,
background observers or automatic blockers are enabled by this prioritization.

The already scheduled November20 company review remains independent and is not delayed
by pilot preparation. Its evidence may inform P0.1 and later adoption, without creating
a second dated review. Other optional experiments and general KB maintenance remain
outside this focused priority sequence; previously cancelled work stays cancelled.

## Changes and status

Recorded the discussion/research, added four bounded follow-ups, clarified three
existing TODO entries and superseded stale scope statements in the existing experiment
and ECC notes. Preserved unrelated working-tree changes. Rule/skill/settings code is
unchanged. Affected TODO rendering verified all four new and three revised titles under their intended heading paths. No missing display-cache entries remain for the affected sections. Knowledge lint passed with zero errors/warnings before final record validation. Existing learning records capture the observed permission and reconciliation outcomes; no new global rule was created. All task commands completed; no background operations remain.

## Portable lesson

The existing [correction-learning recipe](../../../general/knowledge/agents/correction-learning.md)
remains the portable procedure; this note records personal evaluation proposals.

## Prioritization bookkeeping outcome

Replaced the four narrow follow-ups and expanded F5/F7 wording with nine ordered,
source-linked tasks and conditional pilot entries. The generic experiment selector
was placed after this focused sequence. The [merged experiment design](2026-11-06-knowledge-base-merged-agent-experiments.md) and [earlier practice assessment](2026-11-05-knowledge-base-developer-best-practices-research.md) retain the original design provenance. The earlier record of four new tasks describes
the previous revision, not the current count. All five original directions are now
explicitly mapped; TellOnce is no longer a predetermined first implementation.
No agent instruction, skill implementation, runtime setting or package was changed.

## Knowledge growth assessment

The user asked how growing rules, logs and knowledge affect agents and which practices
or ready-made components could help. Read-only November14 inventory counted706
Markdown files excluding INDEX.md (73 general,106 personal,527 current), about5096KiB
in total. This includes the general knowledge README, explaining the one-file difference
from generated note counts. Shared AGENTS.md was5618bytes, README47199bytes and
agent-learning SKILL.md9851bytes. File bytes are not tokens and do not establish actual
startup payload, latency or answer-quality degradation.

Inference: at this size, storage capacity alone does not justify a new service. The
more relevant risks are excessive context loading, historical decisions competing
with current ones, duplicated instructions and procedural overhead. An unloaded
file does not directly consume model context. Retrieval and indexing still have
scaling costs, but no performance bottleneck was measured here.

Existing [retrieval fixes](2026-11-14-knowledge-base-rules-retrieval-stability.md)
already prioritize exact/topic/scope matches, limit long-log dominance, expose
coverage and preserve scope/cancellation semantics. The unchanged72-condition suite
passed; natural Russian literal variants remain a documented limitation. Existing
[scoped reading](2026-11-14-knowledge-base-scoped-startup-resumption.md) is implemented;
its cancelled startup/resumption evaluation must not be reopened by this assessment.

Proposed design requirements for existing P1.1/P1.3:

- Maintain a small always-applicable instruction core; load task/action-specific
  details and examples on demand. Do not depend on similarity search for mandatory
  permissions and prohibitions. Report incomplete retrieval rather than silently
  omit applicable rules to meet an arbitrary count.
- Treat current system state, reusable procedures, decision examples and historical
  task evidence as distinct retrieval roles. Prefer the current answer for operational
  questions; retain historical logs and explicit access to them for causal analysis.
  This does not require moving or deleting the existing files.
- Search an index, inspect a coherent section with source/date/scope, then expand only
  when needed. Preserve reasons, exceptions and cancellations in summaries. Keep one
  canonical rule; repeated incidents add evidence instead of another global instruction.
- Consolidate touched knowledge after meaningful changes and review bounded stale
  material through existing maintenance. Explicit rules do not expire because unused;
  old operational facts may require revalidation. No global automatic rewrite is chosen.
- If literal matching fails on demonstrated paraphrase or cross-language cases, compare
  exact/BM25 and hybrid retrieval while retaining exact identifiers and scope filters.
  Markdown remains canonical; any index must be regenerable and updated on changes.
- If a retrieval change is selected, assess answer and applicable-decision visibility
  with irrelevant-history distractors plus reading volume and cost. Extend the relevant
  E06/learning cases; do not introduce a new E07/E08 startup/resumption evaluation.

Sources read:

- [Anthropic context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents): just-in-time loading, representative examples and compact tool results.
- [Anthropic memory components](https://www.anthropic.com/research/components-of-agent-memory): distinguish transcripts, notes, representations and injected context; consolidation is model-dependent.
- [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988): studied context files did not generally improve task success and increased inference cost; this is not a result measured on this user's system or grounds to remove permission rules.
- [QMD](https://github.com/tobi/qmd): local Markdown retrieval with BM25, vectors, reranking and CLI/MCP; a conditional search-layer candidate, not a new canonical memory or selected installation.
- [SQLite FTS5](https://www.sqlite.org/fts5.html): embedded full-text ranking/snippets, a possible simpler index if a lexical scaling need is demonstrated; not semantic understanding or a complete ready-made agent learning solution.

TellOnce/ACE address other parts of the learning loop. Claude-Mem/Hindsight remain
possible capture/retrieval candidates already in P0.2; choose by demonstrated gaps
and total overhead. No additional mandatory pilot or platform migration follows from
growth alone. Updated existing TODO design requirements rather than duplicate them.

## Effectiveness metrics proposal

The user asked whether agents should collect metrics to guide improvement. Inspected
existing helpers: token_usage.py reports token categories and heuristic requested KB
reads, not task correctness, exact historical read bytes or currency cost.
agent_learning.py report currently shows68records and45current-revision applicable
rule evaluations (38pass,7fail), excluding3historical evaluations. Source inspection
confirms these count evaluation events across rules, not unique tasks; this ratio
must not be presented as an overall task success rate or representative coverage.

Proposed minimal task-level record in existing task evidence: stable task ID/type,
model and workflow revision, verified first-delivery and final outcome (unknown allowed),
substantial corrections with source references, repeated rule failures, demonstrated
unnecessary work, available usage/duration and missing evidence. Several turns,
commits or rules for one task do not create several task successes. Deduplicate
corrections and preserve original failure separately from recovery. Required approval,
useful clarification and changed user requirements are not errors. Extra tool calls
or removed code are diagnostic clues, not automatically waste.

Primary measures: verified first-delivery success among assessed eligible tasks;
substantial corrective interventions per task; repeated violations per applicable
rule-task opportunity; evidenced unnecessary work; full resource use per comparable
verified result. Always report assessed/eligible counts, unknowns and observation
period; zero eligible cases means undefined, not100%. Permission violations and
false completion are separate critical events, not offsets in a weighted score.
Final outcome must remain visible so low cost or fewer interventions cannot conceal
failure. Compare task types and model/workflow revisions rather than aggregate unlike
work. Track total and cache token categories, retries and evaluator cost; distinguish
user waiting from active duration when observable, otherwise mark the limit. Do not
invent human time savings or token prices.

Use automatic counters and outcome checks where possible, source-backed semantic
labels where needed, and bounded human review of ambiguous cases. Agent self-reports
are not independent verification; an optional model judge requires calibration and
its own cost accounting, not default background execution. Start with the existing
helpers and one concise task record, not a new dashboard/service or transcript copy.
The November20 review can use available evidence and disclose gaps; no new recurring
schedule or pilot is selected. P0.1 owns definitions and baseline design, P1.4 owns
comparative measurement, P1.5 owns evidence-based adoption. Implementation remains
proposed, not performed.

Reference: [Anthropic agent evaluations](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
distinguishes tasks, repeated trials, observed outcomes and code/model/human graders.
The proposed local metrics are an engineering recommendation, not measured gains.

## Daily metrics implementation decision

The user subsequently requested daily collection and analysis and selected the first
active agent interaction, without a background model. The
[implemented mechanism](2026-11-14-agents-daily-metrics-learning.md) now replaces the
previous proposed-only status for collection. The broader case-set, metric calibration,
quality/transfer pilots and adoption decisions remain pending. The first daily baseline
identified missing historical task coverage and the need to distinguish newly stated
preferences from repeated known-rule violations; P0.1 and the existing November20
review own these issues. This does not authorize the conditional tool/runtime pilots.

## P0.1 preparation completed November 14

[Prepared cases and calibrated metrics](2026-11-14-agents-p01-decision-cases-metrics.md)
complete P0.1: four historical examples, six prospective transfer/negative specifications,
observable failure-stage distinctions, metric denominators and explicit unknowns.
Company evidence stays in its layer. This supersedes earlier statements that case
preparation remains open; no behavioral transfer improvement, pilot execution or
selected mechanism follows. P0.2 and the existing P1 owners remain open in central TODO.

## P0.2 comparison completed November 14

[Seven-mechanism and search comparison](2026-11-14-agents-p02-learning-search-comparison.md)
completes P0.2. It recommends retaining the current canonical KB/agent-learning and
testing compact, scoped decision-example delivery before implementation choices.
The design borrows selected mechanisms without installing products; client support,
model/data routes, duplicate writers, overhead and rollback limits are documented.
Current primary sources describe Codex support for Claude-Mem and the replacement
Hindsight Coding Agents plugin; TellOnce's wrapper coverage remains limited. These
updates supersede narrower earlier compatibility impressions, not historical evidence.
FTS5/QMD remain optional derived search layers for demonstrated lexical/semantic gaps.
P1.1/P1.2/P1.3 retain the minimal design/diff scope, P1.4/P1.5 evaluation/adoption,
and P2.1/P3.1 remain conditional. No tool, pilot, migration or workflow change is selected
by completing this comparison; expected behavioral benefit remains a hypothesis.
This supersedes the earlier statement that P0.2 remains open.

## P1.1 delivery design completed November 14

[Scoped experience delivery design](2026-11-14-agents-p11-experience-delivery-design.md)
completes P1.1 preparation: delivery before approach selection, separate current-state
and historical roles, scoped examples with rationale/exceptions, bounded section
expansion, explicit coverage and conditional growth verification. The smallest proposed
change uses the existing agent-learning pre-action step and P0.1 examples; no search
backend or permanent instruction was changed. This supersedes the earlier open design
status for P1.1 only. P1.2/P1.3 own the remaining combined design/diff, P1.4/P1.5 own
selected trials and adoption. Behavioral benefit remains unmeasured.

## P1.3 reconciliation prepared November 14

[Canonical reconciliation](2026-11-14-agents-p13-canonical-reconciliation.md) completes
P1.3 preparation: one exact candidate patch for eight existing files, combining P1.1
and P1.2 with F5/F7 import, evidence, template and dependency corrections. Canonical
lookup, provenance, task-only lint scope, permissions and history are preserved.
Patch application, generated-log behavior, skill syntax, local dependencies and
instruction lint passed; active instructions were not changed. P1.4/P1.5 retain
selection, behavioral trials and adoption. This supersedes the earlier open P1.3
preparation status only; no measured transfer benefit is claimed.
