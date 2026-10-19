# Review correction learning

model: mid for a scoped evidence review; use a stronger model only for unresolved contradictions.

Read `~/ai/general/skills/agent-learning/SKILL.md` and use its review procedure.
Run `python3 ~/ai/general/scripts/agent_learning.py report` and select the relevant
system or rule keys. Review a bounded set (up to ten patterns unless requested otherwise).

For each pattern, read its evidence and canonical target. Identify whether it is an
explicit durable instruction, task direction, factual correction or inferred pattern;
whether another rule already covers it; and whether capture, retrieval or execution
failed. Count independent occurrences, not duplicated reports of the same event.
Give priority to violations after the canonical rule was available and loaded.

Apply unambiguous explicit corrections within the user's existing authorization.
Present uncertain inferences and actual conflicts as a compact batch with exact
proposed changes. Preserve scope, original evidence and superseded decisions.
Never broaden permissions, mine full histories or schedule reviews implicitly.

Verify readback and applicable behavioral outcomes separately. Report what is recorded,
linked, observed and still unverified; do not use quiet time as proof of success.
Put actionable work only in `~/ai/TODO.md`, linked to the existing evidence.
