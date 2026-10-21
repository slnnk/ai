---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [lint, agnix, instructions, audit]
---
# Knowledge base lint warning review

## Summary

User requested an audit of current warnings, not implementation. Full KB lint:0errors/6warnings. Forced agnix0.59.0:9files/0errors/4warnings/2informational findings. All findings are classified below; no instruction, configuration, linter or historical evidence was changed. Two deduplicated correction proposals were added to the central TODO.

## Classification and disposition

| Finding | Evidence | Disposition |
| --- | --- | --- |
| KB size x1 | Shared AGENTS.md12189bytes versus5632threshold;6557bytes over. | Valid optimization warning, not proof of truncation. Propose moving detailed procedures to README, preserving mandatory rules, permissions and links. |
| KB language x5 | Exact source evidence counted as prose because inline code is not excluded. | False positives; preserve source strings. Propose targeted language-check/markup correction. [Company audit](../../../current/knowledge/log/2026-10-20-knowledge-base-language-warning-audit.md). |
| PE-006 x3 | Global Claude instruction alias lines95,100,152: secret handling, personal data and explicit consent for Git mutations. | Intentional policies; retain. Context includes permitted storage/access and read-only alternatives. No weakening to satisfy prompt-style heuristics. |
| CDX-CFG-025 x1 | Codex config line3 service_tier default. Installed rule explanation itself lists default as a good example and marks autofix unsafe. | Tool/schema inconsistency, not a confirmed settings defect. Retain setting; no tier/billing change. Prior installed-CLI offline parsing accepted it; no new model/API probe conducted. |
| AGM-004 info | Global policy file has no conventional project overview. | Inapplicable generic recommendation; purpose/layout already present. |
| CDX-AG-008 info | KB-root AGENTS.override.md shadows AGENTS.md. | Intentional, previously implemented to avoid duplicate instruction loading; retain. |

## Instruction-size proposal

The largest sections are after-work bookkeeping2244bytes, backlog1718bytes, Git1444bytes, supervised Git training1307bytes and external changes1049bytes. Move procedural details and display contracts into the existing README sections with explicit read triggers. Keep secret handling, authorization boundaries, both Git approvals and task-scope rules directly visible. Preserve effective content, then check links, KB lint and forced agent lint. This is a proposal; no compression or policy change performed.

## Evidence and commands

Ran ai-sync, kb_lint.py, agent_lint.py --force, scoped learning lookup, section-size accounting and local agnix explain for PE-006/CDX-CFG-025/AGM-004/CDX-AG-008. Read the affected instruction lines and prior audit classifications. Report: ~/ai-data/agnix/report.json. [Prior classifications](2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md), [previous corrections](2026-10-19-knowledge-base-local-rule-corrections.md).

## Reconciliation and limits

Central TODO contains the two correction proposals with source links; advisory findings are recorded here without creating fake remediation tasks. No automatic rule suppressions, package updates, external changes or model calls. Existing warnings remain visible until a separately requested implementation. No universal future-warning policy was installed.

## Subsequent outcome: 2026-10-20

The user subsequently requested the shortening proposal's implementation. It is now
[completed](2026-10-20-knowledge-base-shorten-shared-agents.md): AGENTS.md5593bytes,
size warning removed, permissions preserved and conditional README reads explicit.
The audit statements above describe the original read-only stage. The language-check proposal was still open at that stage. The user then explicitly
requested both parts; the [targeted correction](2026-10-20-knowledge-base-language-inline-code-fix.md)
is now implemented with 11 passing regression tests and full KB lint at 0 errors/0 warnings.
The original audit findings above are preserved as historical evidence.

The user later requested positive wording for the three historical PE-006 policies,
with the rule retained. [Implementation and control check](2026-10-20-knowledge-base-positive-policy-wording.md)
confirmed the pre-edit baseline already had no PE-006 after shortening; the new wording
also passes, and a negative-only control still triggers the enabled rule.

[Service-tier verification](2026-10-20-knowledge-base-service-tier-validation.md) subsequently
confirmed CDX-CFG-025 as an overly restrictive agnix0.59.0 check: current official schema
explicitly includes default/priority examples, both rejected by the linter; Codex0.163.0
accepts them in an offline configuration-loading probe. No model/API request or setting change.

Subsequently implemented by explicit user request: [local lint compatibility recheck](2026-10-20-knowledge-base-agnix-service-tier-compatibility.md).
The rule remains enabled; valid default/priority values pass, invalid values still warn.
The original agnix binary is unchanged; the corrected runner is used by ai-sync.
