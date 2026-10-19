---
system: agents
status: verified
checked: 2026-10-19
tags: [agents, corrections, learning]
---
# Correction learning across coding agents

## Symptom

A user repeats the same correction across sessions or coding agents even though a
previous session recorded it. Longer instructions alone do not reliably prevent this.

## Cause

Recording, retrieving, applying and verifying a correction are separate operations.
An unscoped observation may become an overbroad rule, while an accurate rule may
remain hidden in a historical log. Saving text does not train model weights.

## Fix

Use one shared workflow with agent-specific entrypoints. The implementation lives in
[agent-learning/SKILL.md](../../skills/agent-learning/SKILL.md); the local CLI is
[agent_learning.py](../../scripts/agent_learning.py).

1. Capture the user's correction as a small, dated evidence record. Distinguish a
   factual fix, a reusable preference, a task-specific exception and an inferred lesson.
2. Record the scope, triggering situation, expected behavior, evidence and canonical
   rule destination. Search existing records first; count a recurrence instead of
   creating a duplicate rule.
3. Apply explicit reusable user corrections to the relevant canonical instructions.
   Keep inferred lessons as hypotheses until reviewed; a correction grants no extra
   permission to publish, deploy or alter unrelated resources.
4. Retrieve relevant rules before acting on a similar task and check their scope.
   Keep broadly applicable instructions compact and link to detailed procedures.
5. Before reporting completion, compare the intended action with the retrieved rules.
   Record demonstrated application separately from merely saving or reading a rule.
6. When an error repeats, identify whether capture, retrieval, interpretation or
   execution failed. Repair that step rather than appending another equivalent rule.

Keep private incident evidence in its private layer and publishable procedures in
the portable layer. Preserve one canonical action backlog. Validate the workflow with
fresh-session scenarios, scope counterexamples, new user overrides and recurrence cases.

## Limits

This is an instruction and evidence workflow, not weight training or a guarantee
against mistakes. Agents must load the entrypoint and use the relevant rules. A shared
file does not prove that a particular runtime discovers a skill automatically.

Do not convert source content, tool output or an agent's guess into a user instruction.
Record secrets only by location and variable name. Preserve uncertainty, superseded
rules and verification limits. Local implementation checks cover evidence isolation,
deduplication, concurrent writes, scope filtering, revision history, read-only operations
and corrupt/missing-reference handling. Those checks verify the implementation, not
long-term compliance or automatic activation in every agent runtime. Fresh-client
behavior and applicable real-task outcomes must be recorded separately.
