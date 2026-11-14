---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, learning, retrieval, design]
---
# P0.2: learning mechanisms and search compared with the current KB

## Task

## Context

## Actions

## Findings

## Changes

## Open items

## Portable lesson

none

## Summary

P0.2 is complete as a documentary comparison of seven learning systems and search options.
Keep layered Markdown, agent-learning, scoped rules, current search and task metrics.
Recommend one bounded next design: retrieve a relevant decision example before choosing
an implementation, with rationale, scope and a negative applicability condition.
Borrow lifecycle separation from TellOnce, incremental curation from ACE and staged
expansion from Claude-Mem; do not install these products to borrow the mechanisms.
P0.1 includes read-but-violated rules, so neither more memory nor better recall alone
establishes a fix. Expected behavioral benefit remains a hypothesis for P1.4.
Codex integrations exist in current TellOnce, Claude-Mem and Hindsight sources, but
none was installed or demonstrated in this host. Letta/Hermes change the runtime.
Keep FTS5 conditional on lexical scaling evidence and QMD on semantic retrieval evidence.
No migration, hook, observer, index, client setting or global instruction was changed.
P1.1/P1.2/P1.3 retain design/implementation ownership; P1.4/P1.5 own trials/adoption.

## Task, scope and acceptance

User request: execute central knowledge-base task P0.2 on November14.
Authorized: research, mechanism comparison, one bounded design and local bookkeeping.
Not authorized by this task: installing candidates, switching runtime, launching model
trials, scheduled observation, external ingestion or changing operating instructions.
Sources: [reconciled goal](2026-11-14-agents-personalized-learning-backlog.md#clarifications-and-current-goal),
[P0.1 cases and metric contract](2026-11-14-agents-p01-decision-cases-metrics.md),
[growth assessment](2026-11-14-agents-personalized-learning-backlog.md#knowledge-growth-assessment).

Acceptance: compare capture, scope/storage, delivery before decisions, enforcement and
evaluation for all seven; include real compatibility evidence and its limits, data/model
routes, maintenance, duplicate writers and rollback; distinguish retained/borrowed/conditional
mechanisms and rejected alternatives; choose one bounded design without claiming measured gains.

## Current baseline and supported gap

Canonical local sources inspected: shared AGENTS.md, README retrieval/maintenance rules,
agent-learning SKILL.md and operations reference, agent_learning.py query/mutation paths,
kb_find.py ranking/rendering, existing P0.1 and retrieval outcome notes.

| Mechanism | Current capability | Supported limitation |
| --- | --- | --- |
| Capture | Main agent records explicit decisions/corrections, stable keys/events, provenance and canonical links; inferred patterns await confirmation | Agent-mediated timing; no independent complete capture coverage established |
| Scope/storage | Layered Markdown; global, personal/current, exact repository and task-ID isolation; rejected/superseded evidence retained | Narrative decision examples are not a separate automatically delivered library |
| Before decisions | Required scoped query/read at entry and before consequential action types; topical/key ranking, pagination and canonical targets | Retrieval/read is distinct from choosing an appropriate approach |
| Enforcement | Instruction and approval boundaries; local lint and explicit outcome verification | No general machine oracle for engineering simplicity; lint does not enforce judgment |
| Evaluation | Rule-task outcomes plus task-level first/final results, corrections, costs/unknowns and daily evidence review | Incomplete historical coverage; no completed unseen correction-transfer comparison |

P0.1 C01 and C03 document loaded rules followed by conflicting actions. C02 exposes an
assumption creating a whole dependency chain; its precise prior read state is unknown.
C04 introduces a task preference and must not become a repeated-violation statistic.
These observations support testing decision application, not assuming capture is the
sole problem or inferring missing reads from missing logs.

The [November14 retrieval result](2026-11-14-knowledge-base-rules-retrieval-stability.md#verification-and-status)
already reports72saved conditions without regression: operational top5 is12/12 and
visible answer anchors8/12 in each layer mode; literal Russian variants still miss.
The [historical baseline](2026-11-04-knowledge-base-retrieval-baseline.md#summary)
used a frozen566-note corpus; that size is historical, not a current inventory.
Current query preparation, scoped decision banners, ranking, coherent sections and
coverage/continuation are implemented. Do not propose reimplementing them.

## Seven learning mechanisms

Source facts below are documented capabilities; choices in the last column are this
assessment. Learning here updates external context/skills, not model weights.
No vendor benchmark is treated as a result on this user's tasks.

| Candidate | Capture and scoped storage | Delivery before a decision | Enforcement and evaluation | Disposition |
| --- | --- | --- | --- | --- |
| [TellOnce](https://raw.githubusercontent.com/YujunZhou/tellonce/main/README.md) | Correction extraction; local SQLite/rules; background recording on by default | Local progressive rule retrieval; optional model matching | Optional enforcement/judging; research evaluation differs from local use | Borrow separation of acquisition, delivery and compliance. Retain current provenance/scope store; no second rule writer |
| [ECC continuous-learning-v2](https://raw.githubusercontent.com/affaan-m/ECC/main/skills/continuous-learning-v2/SKILL.md) | Tool/prompt observations, background observer, project/global atomic instincts | Instincts evolve into skills/commands | Confidence includes non-correction and inactivity; promotion across projects | Borrow compact trigger/action/evidence shape only where missing. Reject silence-based validation, automatic scope promotion and age decay of explicit rules |
| [Letta Code](https://raw.githubusercontent.com/letta-ai/letta-code/main/README.md) | Stateful agent, editable/versioned MemFS and scoped skills | Persistent memory plus message search | Agent reflection and version history do not prove compliance with user judgment | Retain as conditional P3.1 runtime candidate; no whole-system replacement justified |
| [Hermes](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md) | Curated memory and learned/refined procedural skills | Persistent context plus session recall | Self-improvement claims require task-specific external validation | Borrow reusable procedure/experience distinction; alternative runtime only if smaller changes fail |
| [ACE](https://raw.githubusercontent.com/ace-agent/ace/main/README.md) | Generator feedback, Reflector and Curator; incremental playbook edits | Updated playbook conditions subsequent generation | Framework supports adaptation/evaluation; feedback quality controls the lesson | Borrow narrow evidence-linked updates preserving prior rationale. No additional three-role model pipeline |
| [Claude-Mem](https://raw.githubusercontent.com/thedotmack/claude-mem/main/README.md) | Hooks feed observer; SQLite observations/summaries and Chroma search | Project context plus index → timeline → selected details | Memory/search is not a general user-rule compliance oracle | Borrow staged expansion; conditional capture/retrieval component only if a measured gap remains |
| [Hindsight](https://raw.githubusercontent.com/vectorize-io/hindsight/main/README.md) | Retain extracts facts/experiences; banks, observations and synthesized models | Recall combines semantic, keyword, graph and temporal retrieval; reflect synthesizes | Published memory benchmarks do not establish local correction transfer | Conditional structured-memory integration; do not make inferred beliefs canonical instructions |

## Compatibility, data flow and operating cost

Evidence level: local CLI command reports `codex-cli 0.169.0`, with a read-only PATH-alias
warning. The active tool host runs orchestration calls; its hook dispatch/trust and
final-output interception were not exercised. A compatible CLI on disk does not establish
that a plugin can observe this host, nested tool calls or every final answer.
No candidate was installed, no model worker launched and no test dialogue sent to it.

| Candidate | Client evidence and coverage limit | Data/model route and maintenance | Duplicate ownership and rollback requirement |
| --- | --- | --- | --- |
| TellOnce | [Codex port](https://raw.githubusercontent.com/YujunZhou/tellonce/main/codex/docs/README.md): audit default; interactive text advisory outside wrapper, no Codex shadow judge; hook trust required | Redacted turns → detached CLI model → local rule store; extraction/judge and wrapper retries add usage; local retrieval itself needs no model | Existing learning capture would overlap. Any future trial needs one writer, recursion exclusions and frozen rules. Disable recording, remove exact registrations/wrapper, preserve exported state; default per-project uninstall retains global hooks |
| ECC | Its v2 skill documents Claude lifecycle observation; [Codex config](https://raw.githubusercontent.com/affaan-m/ECC/main/.codex/config.toml) proves configuration assets, not observer parity. [Install manifest](https://github.com/affaan-m/ECC/blob/main/manifests/install-modules.json) omits Codex from hooks-runtime targets | Observations → observer model → instincts/evolved artifacts; process supervision, model calls and scope heuristics need maintenance | Would overlap rule extraction/skills. Do not run parallel writers; rollback would stop observer, remove its registrations and restore generated artifacts from a reviewed snapshot |
| Letta Code | Separate harness, not a native add-on to this session; local/cloud modes are documented | Cloud is default; local storage/backend does not imply local inference. [Dreaming](https://docs.letta.com/configuration/memory) uses background subagents and optional extra review, adding tokens | MemFS could diverge from KB. Trial needs separate namespace/read-only KB import and a reviewed export path; stop dreaming/runtime and return to unchanged client/KB |
| Hermes | Separate harness. [Memory tool source](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/tools/memory_tool.py) loads profile-scoped memory/user files as frozen session-start context | Local files/session DB → configured agent model; skill learning consumes agent turns. [Session-search source](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/tools/session_search_tool.py) currently returns actual DB messages without LLM calls, despite broader README summarization wording | Profile isolation is not our task/repo policy. Keep any trial profile separate; stop runtime and preserve/review learned files before importing anything |
| ACE | Python adaptation framework with train/validation/test/eval modes; no native integration demonstrated | Task execution/feedback → reflection model → curator → playbook; extra calls, integration code and feedback calibration | A curator would duplicate canonical rule updates. Borrow incremental editing in existing workflow; an eventual trial requires frozen playbook/export and removal of its caller to roll back |
| Claude-Mem | [Platform guide](https://github.com/thedotmack/claude-mem/blob/main/docs/public/platform-integration.mdx) names Codex CLI; [adapter source](https://raw.githubusercontent.com/thedotmack/claude-mem/main/src/cli/adapters/codex.ts) normalizes hook payloads/context output. Native support is documented, host coverage untested | Tool activity → local worker → chosen observer provider → DB/search. Bun/Node/vector runtime and observer add upkeep; README says telemetry defaults on and cloud sync is opt-in | Duplicate observation summaries and stale competing context. Future trial needs explicit provider/data route and one canonical writer; stop worker, remove only added hooks/MCP settings, retain DB backup |
| Hindsight | [Legacy Codex integration](https://hindsight.vectorize.io/sdks/integrations/codex) is retired; [Coding Agents plugin](https://hindsight.vectorize.io/sdks/integrations/coding-agents) documents Codex hooks/MCP with `codex_hooks = true` | Repo history/sessions → per-repo bank on selected server/daemon/cloud; extraction and default reflect consume model work; plugin also has automatic update/page refresh behavior | A shared repo bank does not enforce task-only rules. Second synthesized pages would compete with KB; future trial needs isolated bank, pinned version, bounded ingestion and no KB write-back. Disable/unregister plugin; retain bank/export before any deletion |

All model-backed extraction/reflection can send note/session content to the configured
provider even when its database is local. No external route is selected here. Exact
cost, latency, storage growth and observed event coverage are unknown until measured.
“No extra service” does not mean free: the main agent still spends reading/curation tokens.

## Search choices

Search is a replaceable read layer; it is not the authority for permissions, explicit
rules or cancellations. Prefer exact identifiers and scope filters before relevance
ranking, and read current canonical sources before acting on derived snippets.

| Option | Benefit and boundary | Cost, integration and rollback | Decision |
| --- | --- | --- | --- |
| Current `kb_find.py` + scoped `agent_learning.py` | Exact technical/identifier matches, section/source/decision coverage; active global obligations remain discoverable independently of topic | Existing CLI and plain files; scans corpus, no retrieval model. Query preparation still translates Russian concepts | Retain now; target decision delivery/application rather than reopen completed ranking fixes |
| [SQLite FTS5](https://www.sqlite.org/fts5.html) | Embedded tokenized full text, BM25 and snippets; faster indexed lexical access is plausible. Unicode tokenization is not translation, semantic search or an exact-substring substitute | Build a derived section index plus scope/provenance metadata and update/delete consistency. Local SQLite build must support FTS5. Keep literal-ID path and canonical decision renderer; rebuild index or bypass it on mismatch | Conditional simplest lexical index if measured scan latency/growth is a bottleneck; does not by itself address Russian paraphrases or read-but-violated rules |
| [QMD](https://raw.githubusercontent.com/tobi/qmd/main/README.md) | CLI/MCP; BM25, vectors and hybrid reranking can retrieve conceptual paraphrases. Russian benefit is unmeasured and depends on embedding/query models | Node/Bun, local GGUF models, embeddings/reranking and reindex maintenance; larger footprint than FTS5. Index only permitted Markdown, preserve exact identifiers, task filters and decision banners outside similarity selection | Conditional semantic-search arm only after real prepared-query misses; no installation now. Keep index regenerable under ai-data and disable/bypass without modifying Markdown |

Claude-Mem/Hindsight are not equivalent alternatives to a lightweight index: their
capture, models and synthesized storage expand responsibility. They remain conditional
only when those additional responsibilities match an observed gap. Letta/Hermes add a
runtime change too. A latency claim or expected semantic gain here is an inference,
not a benchmark result. Never import `.env` or raw transcripts merely to populate an index.

## Recommended bounded design

Working proposal: decision examples delivered through the existing retrieval workflow.
This is a design for P1, not a new active operating rule or installed feature.

1. Retain one canonical rule and linked source evidence. Reuse the P0.1 before/after
   examples rather than duplicate the same correction in another store. An example
   records trigger, rejected approach, chosen approach, rationale, applicability and
   an explicit condition under which the rejected approach would be justified.
2. At approach selection, use existing scope/task/repo filtering and prepared technical
   queries. Retrieve a compact current rule and at most two relevant example sections
   initially; expand source context when rationale/exception/decision is incomplete.
   The cap is a proposed experiment control, not permission to omit mandatory rules.
   Keep operational current-state retrieval distinct from historical judgment evidence.
3. In the working decision, tie the planned mechanism to the available analogous
   solution/tool and actual constraint. If an assumption creates a whole workaround,
   expose the simpler compatible alternative before implementing the chain. Existing
   material-assumption and approval rules govern any choice needing user input;
   ordinary reversible decisions remain autonomous. Avoid a repetitive user-facing form.
4. At closeout, update the existing example/rule evidence with observed first-attempt
   and recovered outcome. Reuse agent_learning/agent_metrics; do not add a second
   collector, confidence score or background observer. Agent-inferred generalizations
   remain proposals until confirmed; task decisions stay task-scoped.

Data flow: correction/source → existing task log and linked canonical rule → scoped
query → selected source sections → implementation choice → observed result → existing
rule/task evaluation. Markdown stays canonical; any later search cache is derived and
read-only with respect to rules. The same main agent owns updates, using stable event
IDs; indexes do not promote rules or write back learned beliefs.

Expected benefit: a concrete precedent with rationale can constrain the next engineering
choice more usefully than restating “keep it simple.” This directly targets C01/C02;
C03/C04 require scope/non-applicability handling so extra examples do not spread task
preferences. The benefit is a falsifiable design hypothesis, not demonstrated transfer.

Retain: existing storage, provenance, exact scope, permission boundaries, search fixes,
regression artifacts, daily metrics and historical evidence. Borrow: TellOnce's separate
acquisition/delivery/compliance stages, ACE's small evidence-backed curation deltas,
Claude-Mem's index-to-detail expansion and Hermes's separation of procedures/history.
Do not integrate a new runtime/store at this stage. Replace only a demonstrated
redundant instruction fragment in the eventual reviewed P1.3 diff; this task replaces none.

## Rejected alternatives and conditional escalation

- Install all seven, or select TellOnce first by reputation: duplicate stores/writers,
  new data/model routes and unmeasured benefit for the actual failure.
- Treat confidence, repeated patterns or silence as approval: contradicts explicit
  versus inferred scope and evidence requirements; causes C03-type overgeneralization.
- Use stronger similarity search as the sole rule selector: can omit mandatory rules,
  cancellations and exact identifiers, while leaving loaded-rule violations unchanged.
- Enforce engineering simplicity with text matching or a post-tool blocker: no sound
  oracle for necessity; a check after an irreversible action cannot prevent that action.
  Existing narrow deterministic checks remain appropriate for objectively testable rules.
- Migrate everything to Letta/Hermes now: current evidence does not show a benefit
  unavailable through a smaller intervention; runtime/model changes confound attribution.
- Add full reflection/curation/observation workers now: more model work and another
  writer before capture/delivery timing has been shown to be the remaining bottleneck.

P2.1 stays conditional if a P1 comparison demonstrates missed capture or late delivery:
select one compatible mechanism and first prove host events/trust, pre-action timing,
no duplicate/recursive capture, scoped exclusions and stop/rollback. TellOnce is relevant
for compliance timing; Claude-Mem/Hindsight for demonstrated capture/recall needs; ECC
requires a verified observer route for this client. This is not an order to run them.
P3.1 stays conditional on persistent limitations that smaller changes cannot address.

## Verification plan and downstream ownership

P1.1 owns the compact delivery specification; P1.2 owns necessity/assumption handling;
P1.3/F5/F7 owns one minimal canonical diff and removal of actual redundancies. No
additional backlog owner is created. This comparison is an input, not adoption approval.

P1.4 must freeze learned state and use P0.1 positive/negative cases in fresh matched
sessions, with independent unseen-case selection and model/effort/fixture controls.
Measure first delivered correctness, substantial interventions, inappropriate rule
transfer, evidenced unnecessary work, complete reading/model/retry cost and unknowns.
Rule retrieval/read and behavior are separate observations; preserve initial failures.
No correctness/scope regression or critical permission/false-completion event is
acceptable as a price for lower corrections. Agree case count/repetitions/budget before
a run; retain immutable baselines and include evaluator overhead. P1.5 decides adoption.

If search is later changed, use the saved retrieval suite plus source-backed paraphrase,
exact-ID, current-versus-history, task exclusion, cancelled-decision and distractor cases.
Missing cases remain pending. Run the existing synthetic/saved checks only when triggered
by actual search/output/query-instruction changes; none were made in P0.2.

Rollback for the proposed P1 change: restore only the reviewed task-specific skill/prompt
hunk and bypass any derived cache. Keep canonical knowledge, examples, cancellation
history, original metrics and failed outcomes. Do not use blanket checkout/reset or
remove accumulated knowledge. No runtime rollback is needed for this research task.

## Evidence limits and source status

Sources accessed November14; public main branches and documentation are mutable.
Before any installation/trial, pin the selected revision, recheck relevant adapter
contracts and record actual host behavior. This assessment is not a release audit.
TellOnce/Claude-Mem/Hindsight support must not be described as demonstrated integration
here; ECC's general Codex assets must not be mistaken for full continuous-learning-v2
hook parity. Letta/Hermes were compared as alternative harnesses, not installed add-ons.
Hermes session-search implementation is more specific than README marketing wording.

Some guessed documentation URLs returned404/unavailable (ECC .codex README,
Claude-Mem standalone Codex guide, Hermes memory guide); conclusions use accessible
primary repository sources/platform guide instead, not those failed requests.
No source provided measurements for this KB, so maintenance/model overhead is qualitative.

## Actions, checks and final status

- Required daily sync exited0 without reminders/output. Daily metrics status confirms
  the November14 review complete, no pending snapshot; no unrelated review was repeated.
- Retrieved all23applicable background-global learning records with an untruncated
  query; read their canonical operating policy and relevant learning/retrieval sections.
- Inspected P0.1, current retrieval implementation and latest saved measurement, then
  primary sources for all seven candidates plus QMD/FTS5. No subagents were started.
- Changed only this assessment, the existing parent design status, central P0.2 status,
  derived indexes, task metrics/rule outcome evidence and the final sync note.
- Acceptance review checked the seven candidates, current/FTS5/QMD search, five learning
  stages, client/data/cost/ownership/rollback, bounded design and rejected alternatives.
  Semantic review confirmed that recommendations remain hypotheses and no measured
  transfer/adoption is asserted. P0.2 is closed under Knowledge base; P1/P2/P3 remain
  open in their original owners. `todo.py --query P0.2` returns only open P2.1/P3.1
  cross-references, not a duplicate P0.2 task; a closed task needs no display-cache title.
- `kb_lint.py`: exit0, zero errors/warnings. Index rebuild follows the final note write.
  No instruction/skill/settings edit occurred, so instruction lint and search regression
  runs are not triggered by this documentation-only task.
- Existing discussion-scope and final-note/TODO rules received one evidenced outcome
  each for this task. No new inferred proposal was promoted to an active instruction.
  Task metrics keep first-delivery assessment and resource use unknown; documentary
  final completion is author-checked and is not independent transfer evidence.

Task-scoped conclusion: recommend the bounded existing-workflow design above; expected
transfer remains unproven. P0.2 research is complete; P1/P2/P3 remain in central TODO,
with their existing dependencies and separate execution/adoption decisions preserved.
No installation, external write, model trial, hook/configuration or instruction edit.
No background command or agent remains.

## Portable lesson

Separate remembering, delivering relevant experience before a choice, and demonstrating
that the choice honors it. More memory is not evidence of better engineering judgment.

## Task metrics: kb-p02-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "kb-p02-20261114",
  "created": "2026-11-14T03:14:31.397017+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "research-design",
  "model": "gpt-6",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Task acceptance inventory and source-backed comparison in this note; documentary completion checked by the author, no independent behavioral transfer evaluation. First delivery is not yet externally assessed; usage/time remain unknown.",
  "updated": "2026-11-14T03:14:31.397061+03:00"
}
```
