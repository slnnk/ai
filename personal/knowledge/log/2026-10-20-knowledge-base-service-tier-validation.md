---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [agnix, codex, config]
---
# Knowledge base: service tier warning confirmed as stale agnix validation

## Task and context

User requested verification of the remaining CDX-CFG-025 warning on the local Codex
configuration. Installed Codex CLI0.163.0; agnix0.59.0. Configured model gpt-6.1-sol,
service_tier default. No runtime setting or rule was changed.

## Evidence

The current [official Codex configuration schema](https://learn.chatgpt.com/docs/config-schema.json)
defines service_tier as a string, explicitly giving default, priority and flex as examples,
with legacy fast also supported. The [reference](https://learn.chatgpt.com/docs/config-file/config-reference)
explains that fast maps to priority and other tier identifiers depend on the active model.

Reproduced agnix behavior using an isolated temporary .codex/config.toml with minimal
nonsecret inputs: default and priority trigger CDX-CFG-025; fast and flex pass; an invalid
control also triggers it. The diagnostic explicitly permits only fast and flex. Its explain
command nevertheless lists default as a good example, an internal inconsistency.

With a separate temporary CODEX_HOME and the same minimal four configurations, the
installed CLI command codex debug models --bundled returned valid JSON and exit0 for
default, priority, fast and flex. This demonstrates local configuration acceptance,
not request-time tier validation. No authentication material was copied and no model
request was made.

The existing cached catalog fetched2026-10-19 for gpt-6.1-sol advertises an optional
priority tier named Fast, with description 2x speed, increased usage. This optional-tier
list does not establish that the baseline default tier is invalid.

## Outcome and limits

CDX-CFG-025 on default is confirmed as an overly restrictive agnix0.59.0 configuration
check against the current official schema. Retain default and the rule; changing to fast
would change the requested service mode. No claim was made about server-side fulfillment
or billing in a new request. The investigation is complete, with no implementation or
new backlog action authorized by this verification request.

## Portable lesson

None; source links and bounded evidence are retained here.

Subsequently implemented by explicit user request: [local lint compatibility recheck](2026-10-20-knowledge-base-agnix-service-tier-compatibility.md).
The rule remains enabled; valid default/priority values pass, invalid values still warn.
The original agnix binary is unchanged; the corrected runner is used by ai-sync.
