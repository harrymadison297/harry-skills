---
name: designing-architecture
description: Step 2 of the feature workflow. Writes architecture.md with a code sketch, at least two compared designs, the test seams, and ADRs for hard-to-reverse decisions. Use after spec.md is approved and before any slicing or code.
disable-model-invocation: true
---

# Architect

Decide the shape of the system, and which boundaries the tests will watch, before code grows around it. The shape is cheapest to change now. Read [references/deep-modules.md](references/deep-modules.md) for the vocabulary.

## Process

1. **Read** the approved `spec.md`, `GLOSSARY.md`, `docs/standards.md`, and existing ADRs. Run `understand-this-code` on the code you will touch.
2. **Compare at least two designs** that differ in structure (where the module boundaries sit, who owns the data), not only in detail. For each: what it costs, what it makes easy, what it makes hard. Recommend one and say why.
3. **Sketch the chosen design**: types, function signatures, module boundaries, in real code of the repo's language. Leave bodies "not implemented". The sketch is a contract: a later step that must depart from it reports the departure.
4. **Pick the seams.** A **seam** is a public boundary where a test observes behavior without touching the inside. Prefer a seam that already exists, take the highest one that works, and use as few as possible, so tests survive refactors.
5. **Map criteria to seams.** Every `AC` needs at least one seam that can observe it. If one has none, stop and take the criterion back to `spec-it`.
6. **Record decisions.** Write an ADR in `docs/adr/` for a decision that is hard to reverse, would surprise a later reader, and has a real trade-off. Write an RFC for a question that cannot be settled yet, and name the tickets it blocks.
7. **Write** `docs/features/<feature>/architecture.md` with `Status: draft`: designs compared, chosen design, sketch, a table of `AC -> seam`, and links to the ADRs and RFCs.

## Done when

The sketch compiles or type-checks if the language allows it, every criterion maps to a seam, and each hard decision has an ADR. Hand back to `handon` for gate 2. No ticket is cut and no test is written before approval.
