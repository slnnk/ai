---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, skills, research, knowledge-base]
---
# Local agents: skills, rules and knowledge retrieval research

## Summary
Research completed against official documentation and original repositories, with a bounded read-only local inventory. The most promising proposals are instruction loading/conflict audit, evaluation of existing skills, selected Terraform/DevOps guidance and bounded local review. A subsequent user-requested Context Awesome expansion added configuration lint, section-level search and explicit code/documentation dependency checks. The consolidated section below rates eight approaches and 21 implementations and records source-scoped popularity snapshots, without treating installation counts as quality ratings. Hooks and improved retrieval need focused pilots. These are fit-based recommendations, not a popularity ranking or measured performance results. No skill installation, runtime configuration change or evaluation model run was performed. The central TODO contains the single decision item for optional pilots.

## Task and context
The user requested research into additional local rules, skills and knowledge-base approaches for Claude Code, Codex and portable use. Existing permissions, task-only changes, two Git/MR approvals, explicit-only superpowers and Markdown as canonical knowledge remain unchanged. OpenAI Docs was used for current Codex documentation; independent research covered Claude, universal tools and local inventory. Public primary sources were inspected on October 19; links to mutable upstream main branches describe that observation, not pinned installation artifacts.

## Local observations
- Shared AGENTS.md: 175 lines, 10,508 bytes, above the local lint warning of 5.5 KiB. This is an optimization candidate, not proof of truncation or incorrect behavior. Codex's documented default aggregate instruction limit is 32 KiB; Claude recommends a target below 200 lines per instruction file.
- Shared instruction symlinks for Codex/Claude/Gemini and the four custom skill links for Codex/Claude resolve correctly. This is filesystem verification, not proof that every runtime loaded each rule or skill.
- Installed CLI versions: Codex 0.163.0 and Claude Code 2.1.293. `codex review --help` confirms local review options for uncommitted changes, base branch and commit. No model-backed review was run.
- No explicit hooks/MCP sections were found in the inspected Codex user configuration, or hooks/permissions keys in Claude user settings. Plugin, managed and other runtime hooks were not exhaustively audited.
- Existing infrastructure already supplies scoped rule retrieval, Markdown frontmatter, keyword search, lint, indexes, stale-note reminders, tests, sync preview, token/read accounting and final TODO reconciliation. No retrieval-miss or latency benchmark exists in this investigation.

## Consolidated usefulness and popularity assessment (2026-10-19)

Requested by the user after the initial and awesome-list research. Usefulness is a subjective 1-10 recommendation for the existing DevOps/shared-KB setup, considering task fit, compatibility, maintenance/cost and duplication. It is not a measured quality result, external user rating or popularity-derived score. A technique can be worth borrowing even when installing its full source package scores lower.

Public popularity observations were retrieved on October 19, including cached pages. Rounded `k/K/M` values are retained as displayed; only explicitly marked API values are exact. Stars belong to the whole GitHub repository. Claude Marketplace publishes plugin installs, not a numeric satisfaction score on the inspected cards. No comparable official public Codex plugin rating/install leaderboard was verified. skills.sh counts are third-party install metrics across supported hosts, not Codex-only or Claude-only active users. Unknown metrics mean unverified/unavailable, never zero.

### Locally applicable approaches

| Approach | Usefulness /10 | Local application |
| --- | ---: | --- |
| Behavior and trigger evaluation of existing skills | 9 | Small sanitized scenario suite; identical task/model settings; correctness, unwanted actions, time and tokens. |
| Audit instruction loading, conflicts and scope | 9 | Verify active sources, reduce duplicated procedural text; retain all authorization/safety requirements. |
| Shared Markdown as canonical knowledge with scoped retrieval | 9 | Already present; preserve current layers and correction lookup rather than add a competing memory store. |
| Independent local read-only review | 8 | Use existing Codex review on task-only diff; compare findings against concrete evidence. |
| Narrow lifecycle hooks and explicit-only skill controls | 8 | Host-specific tested adapters; no automatic permission approval, no blanket shell regex enforcement. |
| Retrieval benchmark plus conditional section-level SQLite FTS5/BM25 | 8 | Known questions/expected paths; evaluate recall, snippets, latency before adding models. |
| Explicit linked-block / value checks | 6 | Use only for truly coupled duplicated values/docs; mechanical consistency not semantic truth. |
| Default vector database or automatic second memory store | 3 | No measured need established; extra indexing and competing canonical state. |

### Skills, tools and concrete implementations

| Candidate | Type | Usefulness /10 | Repository stars | Other popularity | Recommendation |
| --- | --- | ---: | --- | --- | --- |
| [Anthropic skill-creator / evals](https://github.com/anthropics/skills) | skill / evaluation workflow | 9 | 182.2k | [skills.sh: 409.8K](https://www.skills.sh/anthropics/skills/skill-creator) (individual skill installs) | Compare existing custom skills against baseline; avoid conflicting duplicate name. |
| [agnix](https://github.com/agent-sh/agnix) | local CLI / LSP | 8 | 455 | Not verified / not applicable | Report-only configuration lint; does not prove semantics or permissions. |
| [HashiCorp Terraform skills](https://github.com/hashicorp/agent-skills) | skill pack | 8 | 900 | [skills.sh: 12.3K / 8.6K](https://www.skills.sh/hashicorp/agent-skills/terraform-style-guide) (terraform-style-guide / terraform-test installs) | Select narrow guidance; preserve pinned versions and approve state/apply separately. |
| [cc-devops-skills](https://github.com/akin-ozer/cc-devops-skills) | skill pack | 8 | 325 | [skills.sh: 16.1K total; 517 / 456](https://www.skills.sh/akin-ozer/cc-devops-skills) (pack total; gitlab-ci-validator / logql-generator) | Cached catalogue from last month; selective references, avoid forced plans/extra edits/dependency installs. |
| [PR Review Toolkit](https://github.com/anthropics/claude-plugins-official) | plugin / specialized agents | 7 | 43.1k | [Claude Marketplace: 114856](https://claude.com/marketplace/plugins/pr-review-toolkit) (plugin installs) | Use selected reviewers; full wrapper is GitHub-centric and includes editing agents. |
| [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | knowledge preparation CLI | 6 | 15.2k | Not verified / not applicable | Borrow section-level FTS5; full generator needs Python3.10+ and optional model usage. |
| [Agent Skills specification / skills-ref](https://github.com/agentskills/agentskills) | standard / reference tooling | 7 | 26.3k | Not verified / not applicable | Metadata validation useful; reference library describes itself as demonstration tooling. |
| [Context7](https://github.com/upstash/context7) | documentation CLI / MCP / skills | 7 | 63.3k | [skills.sh: 23.8K total; find-docs 8.9K](https://www.skills.sh/upstash/context7) (pack installs and individual skill installs) | Use versioned public documentation queries; not a local knowledge database. |
| [BlockWatch](https://github.com/mennanov/blockwatch) | local dependency-check CLI | 6 | 29 | Not verified / not applicable | Explicit co-edit/value links only; markers required; not semantic TODO verification. |
| [QMD](https://github.com/tobi/qmd) | local Markdown retrieval CLI / MCP | 6 | 30483 | [skills.sh: 4.0K](https://www.skills.sh/tobi/qmd/qmd) (qmd skill installs) | Pilot after retrieval benchmark; hybrid adds models and indexing. |
| [ccusage](https://github.com/ccusage/ccusage) | local usage-report CLI | 6 | 19.1k | Not verified / not applicable | Independent token-total comparison; not replacement for KB-read classification. |
| [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) | cross-agent review plugin | 6 | 34.4k | Not verified / not applicable | Optional manual read-only review; automatic Stop gate can consume limits in loops. |
| [Hookify](https://github.com/anthropics/claude-plugins-official) | rules / hook plugin | 6 | 43.1k | [Claude Marketplace: 60376](https://claude.com/marketplace/plugins/hookify) (plugin installs) | Narrow warnings/checks; regex is not shell parsing or approval tracking. |
| [Superpowers](https://github.com/obra/superpowers) | workflow skill pack | 6 | 302057 | [skills.sh: 3.6M](https://www.skills.sh/obra/superpowers) (total installs across 15 skills) | Keep explicit-only; broad worktree/testing workflows need existing local scope rules. |
| [Codex Security verify-fix](https://github.com/openai/plugins) | security verification skill / plugin | 6 | 7.5k | Not verified / not applicable | Explicit supplied finding verification; package includes references/MCP and own licensing. |
| [Cross-Code Organizer](https://github.com/mcpware/cross-code-organizer) | configuration dashboard | 5 | 383 | Not verified / not applicable | View-only audit candidate; UI may be excessive; resolution accuracy not benchmarked. |
| [Security Guidance](https://github.com/anthropics/claude-plugins-official) | hook / model review plugin | 5 | 43.1k | [Claude Marketplace: 241800](https://claude.com/marketplace/plugins/security-guidance) (plugin installs) | Read README cost scope; some model review usage absent from Claude transcript totals. |
| [CLAUDE.md Management](https://github.com/anthropics/claude-plugins-official) | instruction audit / learning plugin | 4 | 43.1k | [Claude Marketplace: 287247](https://claude.com/marketplace/plugins/claude-md-management) (plugin installs) | Duplicates current learning/KB; prefer built-in prompt audit first. |
| [Redcon](https://github.com/natiixnt/redcon) | context / command-output CLI | 4 | 9 | Not verified / not applicable | Only saved-log pilot; runner can stop command on output budget; FSL licensing. |
| [Vercel skills CLI / skills.sh](https://github.com/vercel-labs/skills) | discovery / distribution tooling | 5 | 35583 | Not verified / not applicable | Discovery not quality rating; existing installer already covers basic need. |
| [Context Awesome](https://github.com/bh-rat/context-awesome) | awesome-list discovery service | 6 | 61 | Not verified / not applicable | Trace candidates to original sources; no hosted MCP integration installed. |

### Metric source and precision notes

- GitHub API exact snapshots: [Codex 129,904](https://api.github.com/repos/openai/codex), [Superpowers 302,057](https://api.github.com/repos/obra/superpowers), [QMD 30,483](https://api.github.com/repos/tobi/qmd), [Vercel skills 35,583](https://api.github.com/repos/vercel-labs/skills). Codex's repository stars describe the whole CLI, not the local review feature, so they are not assigned to that approach.
- Remaining repository stars are the displayed snapshots at each linked repository. For shared repos, the same stars are intentionally repeated with no implication that each subskill/plugin earned them independently.
- The Claude Skill Creator card was unavailable directly; an older indexed marketplace count was excluded from the current table. The table uses the directly inspected skills.sh skill counter instead.
- cc-devops skills.sh data is a fetched cached view marked last month, not a guaranteed live counter. Context7 values use one pack page consistently because separately cached skill pages differ slightly. BlockWatch and Context Awesome GitHub pages were marked crawled three and five days earlier respectively.
- Sources for catalogue semantics: [Claude directory help](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory), [Codex plugin documentation](https://learn.chatgpt.com/docs/plugins), [skills.sh directory](https://www.skills.sh/). Public badges/verification are not satisfaction ratings.
- Claude [session-report](https://claude.com/marketplace/plugins/session-report) appeared during metric collection with 11,694 installs, but its implementation was not reviewed; it remains unscored discovery rather than an endorsed candidate.

### Deliverables and decision status

Machine-readable snapshot: `~/ai-data/agent-research/2026-10-19/assessment.csv` and `assessment.json`, with source, scope, observed precision, runtime and recommendation for every scored implementation. The single central pilot-selection item references this consolidated assessment; the research is complete, and installation/configuration/benchmark work remains optional and unapproved. The dated token/Git/November reviews are unaffected.

## Selected skills and capabilities

| Candidate and source | Value for this setup | Assessment and boundaries |
| --- | --- | --- |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Evaluation against no-skill or old-skill baselines, trigger tests and time/token comparisons. | Highest-value methodology for existing custom skills. Python scripts; description optimization uses Claude CLI. Existing same-name Codex skill does not imply identical evaluation support. Avoid installing a conflicting duplicate name; pilot the evaluation approach on sanitized scenarios. |
| [HashiCorp Terraform skills](https://github.com/hashicorp/agent-skills/blob/main/SKILLS.md) and [style skill](https://github.com/hashicorp/agent-skills/blob/main/plugins/terraform/skills/terraform-style-guide/SKILL.md) | Official subject-specific guidance, portable skill content and host-specific plugin manifests. | Best subject-specific pilot: scoped review using existing pinned versions. Upstream latest-version recommendations and recursive formatting must not expand the task. The [refactor skill](https://github.com/hashicorp/agent-skills/blob/main/plugins/terraform/skills/refactor-module/SKILL.md) discusses state changes and apply-based tests: existing external-action approval rules remain essential. |
| [Native Codex local review](https://learn.chatgpt.com/docs/code-review) | Review local branch/commit/working changes without a GitHub-centric publication wrapper. | A built-in capability rather than another skill. Installed CLI help confirms availability. Useful fit for GitLab checkouts; bound the review to task changes so unrelated dirty files are excluded. Running the review would use model resources and was not part of this research. |
| [Claude pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/README.md) | Specialized reviewers for silent failures, misleading comments and tests. | Select report-only reviewer concepts. The [wrapper](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/commands/review-pr.md) uses GitHub CLI and includes editing/refactoring agents; do not adopt it unchanged. Local failure analysis is valuable for scripts and partial API success. |
| [Codex Security verify-fix](https://github.com/openai/plugins/blob/main/plugins/codex-security/skills/verify-fix/SKILL.md) | Verification of a supplied security finding with evidence and explicit inconclusive outcome. | Explicit-request-only, repository-verification-only workflow; cannot equate closed ticket/passing unrelated tests with a fix. The full plugin has companion references, MCP/app dependencies and its own licensing; a bare copied SKILL is not the complete package. Lower priority than ordinary local review. |
| [Claude hookify](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/README.md) | Small deterministic warnings/guards described as local rules. | Python regex hooks, not shell parsing or proof of approval. Consider a few tested checks/reminders; blanket git denial conflicts with daily sync and approved publication. |
| [Agent Skills specification](https://agentskills.io/specification) and [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) | Portability and metadata validation for existing custom skills. | Structural validation is useful but does not establish correct behavior. skills-ref explicitly describes itself as demonstration tooling, so it should not become an assumed production enforcement boundary. |
| [QMD](https://github.com/tobi/qmd) and its [skill](https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md) | Local Markdown keyword/hybrid retrieval with CLI/MCP. | Optional experiment only if known questions expose misses in kb_find. Node/Bun runtime and local models for hybrid features add downloads/storage. Keep Markdown canonical and put generated indexes outside Git; index a bounded knowledge corpus rather than home directories or secret files. |

## Approaches with higher expected value than indiscriminate installation

### Audit and layer instructions
Current [Claude memory documentation](https://code.claude.com/docs/en/memory) provides `/doctor prompt-audit`, available from 2.1.283. The installed version meets the documented minimum; availability also depends on bundled-skill settings and was not runtime-tested. Audit can report conflicting/outdated instructions without applying edits. Verify actual active sources first. Keep the single shared canonical source, and put host-specific invocation metadata in adapters. Shortening AGENTS is a proposal; do not remove permission rules merely to hit a byte target.

[Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) describes metadata-first loading, supported symlink discovery and `policy.allow_implicit_invocation: false`. [Claude skills documentation](https://code.claude.com/docs/en/skills) describes its own invocation controls. The portable SKILL format does not imply identical hooks, allowed-tools or loading semantics. A technically enforced explicit-only mode for selected skills is worth investigating without modifying vendor bundles or changing existing permissions.

### Evaluate real behavior
Construct a small sanitized fixture set: CI infrastructure failure versus assertion failure; planning versus implementation; mixed staged changes; cancelled work versus stale note; fake secret; API write succeeded but verification GET failed; positive and negative skill triggers. Compare identical model/task settings with and without a skill or between revisions. Record correct result, unwanted invocation, extra actions, time and token usage. Format lint, a passed role-play or successful installation does not prove fresh-session rule activation. This is a proposed benchmark, not an evaluation already performed.

### Add narrowly scoped technical checks
Both [Codex hooks](https://learn.chatgpt.com/docs/hooks) and [Claude hooks](https://code.claude.com/docs/en/hooks) can attach to runtime events. Candidate uses are scoped lint/reminders and small tested operation checks. No auto-approval behavior is proposed. Hook coverage differs by runtime/tool and is not a complete enforcement boundary; lifecycle handlers must avoid loops. A completion hook can check records/links, but cannot prove semantic note-to-TODO reconciliation. Pilot in the actual installed harness rather than assuming CLI documentation applies to every UI.

### Measure retrieval before adding a database
Use 10-20 real questions with expected note paths. Compare recall in the first five results, stale-note confusion, returned text size and latency. Improve keyword aliases/filtering or evaluate SQLite FTS/BM25 before local embeddings if that solves observed misses. QMD can provide a measured alternative while Markdown remains canonical. No evidence from this investigation establishes a need to migrate to a vector database or introduce a second autonomous memory store.

## Candidates to defer or reject for now
- [Official Claude code-review command](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md): GitHub-centric and can post comments, so it conflicts with the current local/GitLab review and explicit publication workflow if used unchanged.
- [claude-md-management](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/README.md): audit ideas are useful, but another learning store duplicates existing agent-learning; current built-in prompt audit is a better first investigation.
- [security-guidance](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/security-guidance/README.md): conditional only. Model-backed layers add requests, and its README states direct Stop-review usage is absent from Claude transcript/cost totals. Account for this before enabling, given the user's token reporting.
- [Flux skills](https://github.com/fluxcd/agent-skills): official and narrowly focused, but Flux usage was not established in this environment. Not a default Kubernetes add-on.
- [stoleas/ansible-skills](https://github.com/stoleas/ansible-skills): third-party author claims and dependencies need further audit; full skeleton/Molecule patterns may expand minimal-change tasks. Prefer existing linters and a narrow local workflow before adopting the whole package.
- [Vercel skills CLI](https://github.com/vercel-labs/skills): useful discovery/distribution tooling, not proof of quality. Prefer selected audited sources and pinned revisions, avoid bulk installation. Existing superpowers is already present and remains explicit-only.

## Source freshness
The [old OpenAI skills catalog](https://github.com/openai/skills) is marked deprecated and directs current examples to [openai/plugins](https://github.com/openai/plugins). This is a concrete reason to verify canonical upstream sources instead of treating old top-skills articles as current guidance.

## Recommendation and decision status
Suggested sequence: bounded instruction audit, small behavior benchmark, then one subject-specific or review pilot. Hooks and retrieval changes follow measured gaps. The single optional pilot-selection item lives in the central TODO; the research itself is complete. No installation or implementation permission is implied by this report.

## Changed files and checks
Created this research log, recorded research completion and one optional pilot-selection decision in TODO, rebuilt indexes and appended a final sync summary. No runtime rules/skills/configuration were modified. Link/frontmatter lint and note-to-TODO reconciliation apply to these bookkeeping records; no claim of demonstrated skill quality or new runtime enforcement is made.

## Risks and limits
This is source review and bounded inventory, not a supply-chain audit, complete plugin scan, popularity survey or benchmark. Runtime availability, dependencies, licensing, trigger behavior and cost need checking for the specific selected revision and host before installation. Local config inspection did not reveal secret values in output; transcripts and credentials were not mined.

## Awesome-list expansion requested by the user

The user explicitly requested expanding discovery with [Context Awesome](https://www.context-awesome.com/). Its homepage, browse index and indexed list pages were inspected. Query-string browse searches and attempted Codex-specific indexed pages were unavailable through the web tool, so no successful MCP search or confirmed indexing of the Codex-specific lists is claimed. No Context Awesome MCP installation or runtime configuration change was made.

Discovery routes actually inspected:
- [Context Awesome: awesome-claude-code](https://www.context-awesome.com/list/hesreallyhim/awesome-claude-code) to [hesreallyhim's original list](https://github.com/hesreallyhim/awesome-claude-code): linting, DevOps, memory and configuration tooling.
- [Context Awesome: awesome-claude-skills](https://www.context-awesome.com/list/ComposioHQ/awesome-claude-skills) to [Composio's original list](https://github.com/ComposioHQ/awesome-claude-skills): skill-generation and automation candidates.
- [Context Awesome: awesome-vibe-coding](https://www.context-awesome.com/list/filipecalegario/awesome-vibe-coding) to [the original list](https://github.com/filipecalegario/awesome-vibe-coding): versioned documentation and configuration inspection.
- [Context Awesome: awesome-mcp-servers](https://www.context-awesome.com/list/punkpeye/awesome-mcp-servers) to [the original list](https://github.com/punkpeye/awesome-mcp-servers): context/output tooling.
- Additional Codex sources inspected directly on GitHub: [awesome-codex-cli](https://github.com/RoggeOhta/awesome-codex-cli) and [awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills). Their inclusion in the Context Awesome index was not established.

The lists are discovery sources; the assessments below use each original repository or actual SKILL. Their popularity, listed update times and inclusion do not establish quality, security or compatibility.

### Additional candidates verified at their original sources

| Candidate | Useful capability and fit | Boundary / recommendation |
| --- | --- | --- |
| [agnix](https://github.com/agent-sh/agnix) | Local CLI/LSP for AGENTS, CLAUDE, SKILL, hooks and MCP/config validation; found through awesome-claude-code's linting section. | Highest-priority new audit candidate. Start CLI-only in report/preview mode, without fixes; compare rules to installed runtime versions. Complements kb_lint, which focuses on knowledge notes. Does not prove instruction semantics or actual permission compliance. |
| [cc-devops-skills](https://github.com/akin-ozer/cc-devops-skills) | DevOps skill pack with Claude/Codex manifests; relevant examples are GitLab CI validation, Bash validation and LogQL/PromQL. Discovered through awesome-claude-code. | Select narrow references instead of adopting the whole pack. Actual [LogQL skill](https://github.com/akin-ozer/cc-devops-skills/blob/main/devops-skills-plugin/skills/logql-generator/SKILL.md) mandates an intake/plan-confirmation flow. Actual [GitLab validator](https://github.com/akin-ozer/cc-devops-skills/blob/main/devops-skills-plugin/skills/gitlab-ci-validator/SKILL.md) can install PyYAML, suggests extra improvements and allows optional Docker pipeline execution. These do not supersede minimal scope or external-action permissions. |
| [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | Builds source-linked skills/references from documentation and other inputs; found through Composio's list. Its [section search index](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/features/SKILL_SEARCH_INDEX.md) uses SQLite FTS5/BM25 with file/anchor/snippet retrieval. | Most useful as a design reference or small public-document pilot, not a replacement knowledge system. Generator needs Python 3.10+; generated search script can run using Python stdlib. Model enhancement adds model usage. Do not automatically crawl internal sources or turn all KB files into always-loaded skills. |
| [BlockWatch](https://github.com/mennanov/blockwatch) | Rust CLI uses explicit markers to require related code/docs blocks to change together or compare values. Found through awesome-claude-code. | Useful only for genuinely coupled duplicated values/policies. Deterministic local mode needs no model; separate check-ai uses a model. Requires source markers; removing a block removes its rule, and unsupported extensions are skipped. This is not semantic note-to-TODO reconciliation. Integration skill source could not be fetched; assessment is based on the CLI README. |
| [Context7](https://github.com/upstash/context7) | Version-aware documentation retrieval, via CLI/skill or MCP. Discovered through awesome-vibe-coding. | External documentation service, not local KB. Local client does not imply local backend. CLI needs Node 22.13+; key recommended for limits. Limit use to relevant version questions with neutral queries. Do not adopt a blanket always-use rule or send internal configs. |
| [OpenAI Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) | Discovered through awesome-codex-cli. Commands for normal and adversarial read-only review through the local Codex runtime; also has separate task delegation/session handoff. | Optional convenience if working from Claude. Existing Codex authentication/runtime are reused; Node 18.18+ required. Read-only review is the narrow pilot; rescue/editing delegation is different scope. Upstream explicitly warns its optional Stop review gate can loop and drain usage quickly, so no automatic gate is proposed. |
| [ccusage](https://github.com/ccusage/ccusage) | Discovered through awesome-codex-cli. Reports local Claude/Codex and other CLI usage by date/session, with JSON and offline modes. | Candidate independent comparison for token_usage totals. It does not replace custom KB-read classification or establish actual subscription billing. No package was run and parity against local transcripts was not tested. |
| [Cross-Code Organizer](https://github.com/mcpware/cross-code-organizer) | Discovered through awesome-vibe-coding; renamed from Claude Code Organizer. Inspection UI for instructions/skills/hooks/MCP, conflicts and shadowing. | Could help visualize config, but may be excessive for a one-time audit. Editing/moving/deleting configurations is separate from viewing. Runtime-resolution and token-estimate accuracy are unverified author claims here. |

### Lower-priority findings and conflicts
[bringyour-migration-auditor](https://github.com/unitedideas/bringyour-mcp/blob/main/skills/bringyour-migration-auditor/SKILL.md), found in awesome-codex-skills, supplies a useful checklist for advisory-versus-enforced behavior after migration. It is migration-specific, and its sample recursive grep can print matching secret-bearing lines despite its prose warning not to print secrets; do not execute those examples unchanged.

[Redcon](https://github.com/natiixnt/redcon), discovered through awesome-mcp-servers, is a possible context/output-budget experiment on saved logs. Its command runner can stop processes at an output limit; do not wrap live diagnostics or infrastructure operations without a separate controlled pilot. Claimed savings are unmeasured here; current licensing is FSL-1.1-MIT rather than ordinary MIT.

Composio's GitLab/SaaS automations add an external Rube/Composio connection and write-capable workflows. No need was established beyond the existing local gitlab-workflow. Some catalogue installation paths are stale, reinforcing the need to verify original runtime docs. A reviewed third-party [Postgres skill](https://github.com/sanjay3290/ai-skills/blob/main/skills/postgres/SKILL.md) recommends read-only sessions but stores passwords in JSON, conflicting with the user's credential storage convention; it is not a default candidate.

### Revised recommendation and reconciliation
The additional discovery strengthens the case for a small instruction/configuration audit, with agnix as an optional report-only tool. Other promising pilots are selected cc-devops-skills references and section-level keyword retrieval, evaluated on known questions. BlockWatch and cross-agent review are conditional conveniences. These recommendations extend the existing central pilot-selection item; no independent backlog was created in this note, no packages were installed and no runtime settings changed. The existing dated October/November reviews remain open and unaffected.

## Proposed trial order (user requested plan, not implementation)

The user requested a recommended sequence after clarifying that the candidate list mixes installations, adapted skills and borrowed techniques. This section is a proposal. Preparing it does not authorize installing packages, changing runtime rules, running model-backed benchmarks or editing company repositories. The central pilot-selection item remains open.

| Step | Pilot | Adoption mode | Evidence / exit criterion |
| ---: | --- | --- | --- |
| 1 | agnix and active-instruction audit | Install an isolated/pinned CLI for a report-only trial; inspect actual rule loading. | Small actionable findings report, findings checked against installed host versions; no automatic fixes. Record the initial state before changes. |
| 2 | Existing-skill evaluation fixtures | Borrow the skill-creator evaluation approach; build a small local sanitized fixture set. | Baseline results for planning vs implementation, correct/incorrect triggers, partial API success, mixed staging and cancelled TODO work; correctness, extra actions, time and tokens recorded. |
| 3 | Rule and skill-description corrections | Implement only justified findings from step1; use step2 as regression checks. | Preserve permission/scope requirements; reduce duplication where useful; demonstrate unchanged intended behavior and improved triggering in fresh sessions. No arbitrary byte-target cleanup. |
| 4 | Independent local review | Use existing Codex review; selectively adapt report-only PR Review Toolkit concepts if needed. | Review task-only diffs; evidence-backed useful findings, manageable false positives, no unrequested edits or publication. The Claude-to-Codex plugin is optional convenience later. |
| 5 | One DevOps skill | Adapt one narrow cc-devops skill, starting with LogQL on saved examples. | Compare with baseline and deployed Loki syntax/context; fewer query mistakes without mandatory planning prompts or expanded changes. GitLab CI and HashiCorp Terraform pilots follow only if subject-specific skills prove valuable. |
| 6 | Knowledge retrieval benchmark and section-level search | Evaluate known questions with kb_find; borrow FTS5/BM25 indexing design from Skill Seekers if gaps justify it. | Compare expected note retrieval in top5, stale-note confusion, snippet size and latency on the same questions. QMD is a later alternative only if simpler retrieval is insufficient. |
| 7 | Narrow lifecycle hooks and explicit-only invocation | Prefer small host-specific implementation; Hookify is optional if it simplifies the exact need. | Start one nonblocking reminder/check, test coverage and exclusions including ai-sync; no extra permissions, approval bypass or stop loops. Promote a blocker only after false-positive testing. |
| 8 | BlockWatch | Optional local CLI trial for a few genuinely coupled blocks/values. | Demonstrate a known missed co-edit caught without routine noise. Do not treat joint editing as semantic TODO correctness. Skip if no meaningful duplication is identified. |
| 9 | Additional convenience tools | ccusage for token-total cross-check, Context7 for actual versioned public-doc questions; install/use only after selecting the concrete need. | No duplicated mandatory reporting; verify metric windows/units. Coordinate token comparison with the existing October21 task. Context7 is external documentation retrieval, not local knowledge storage. |

The initial recommended batch is steps1-3: establish current configuration, establish behavior baseline, then make measured corrections. Later steps are conditional pilots; a failed or low-value trial can end without installing every candidate. Each adopted tool should have a pinned revision, minimal scope, comparable baseline and a simple removal/rollback path.

For now defer full-pack installation, automatic review loops, new competing memory stores, Redcon on live commands, Security Guidance model hooks, CLAUDE.md Management and configuration dashboards. Existing Superpowers remains explicit-only. The pending selection and original dated reviews remain represented in TODO.

## Pilot1 completion (2026-10-19)
The user explicitly approved agnix plus instruction-loading audit. The [pilot record](2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md) supersedes earlier pending-selection statements for step1: agnix0.59.0 installed in isolation, selected lint classified, native offline Codex prompt loading verified for three cwd, Claude filesystem/cache inspected. Configuration fixes and later trials remain unapproved; central TODO now tracks choosing among remaining steps2-9.

## Pilot2 completion (2026-10-19)
The user subsequently authorized step2. The [evaluation record](2026-10-19-knowledge-base-skill-evaluation-pilot.md) supersedes earlier pending-selection statements for step2: bounded Codex paired scenarios and native activation probes completed; the small directed sample demonstrated no incremental quality gain. Claude-specific evaluation is blocked by organization subscription access and separately tracked in central TODO. Step3-9 implementation remains unapproved. Canonical skills and global rules were not modified.

## Step3 completion (2026-10-19)
The user subsequently authorized the audited local-rule fixes. The [correction record](2026-10-19-knowledge-base-local-rule-corrections.md) supersedes earlier pending/deferred statements for the stale Claude cache, ambiguous canonical paths and KB-cwd Codex duplication: all three were corrected and verified; five fresh regression sessions passed17/17 checks, native loading is one full policy copy in three directories, and agnix reports0errors. Approval policy and canonical skills remain intact. Claude model-backed evaluation remains blocked separately; later steps4-9 still require selection.
