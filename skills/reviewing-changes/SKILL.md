---
name: reviewing-changes
description: Review a ticket diff or a whole feature in a fresh subagent on three axes (standards, spec, tests) and choose the places where the code should break. Use after implementing a ticket, and once over the whole diff before shipping.
disable-model-invocation: true
---

# Review

The agent that wrote the code is the worst judge of it. Run this in a fresh subagent with no memory of the build, so it has no attachment to the code.

## Input

The diff since a fixed point (the ticket's first commit, or the branch point for a whole feature), plus the ticket, `spec.md`, and `docs/standards.md`.

## Three axes

1. **Standards.** Check the diff against `docs/standards.md` and common smells. Find slop: duplicate code, a helper that already exists elsewhere, needless abstractions, defensive code for cases that cannot happen, comments that restate the code. Search the repo before calling something new.
2. **Spec.** Check the diff against the ticket's criteria and `Out of scope` list. Report missing requirements and work beyond the ticket.
3. **Tests.** Find tests that cannot fail (tautological), tests tied to the implementation (they mock internals, assert call order), and duplicate tests. A test should fail when behavior breaks and survive when only the internals change.

## Places to break

For each criterion, pick at least two places where the code should break: a boundary condition, a branch, an error path. If `docs/standards.md` names a mutation tool, run it on the changed files instead and report the surviving mutants. You pick the places, not the author, because an author picks breaks that existing tests already catch.

## Whole-feature mode

Used by `shipping-features`. Skip the break list. Look for what per-ticket review cannot see: duplicate helpers across tickets, inconsistent names, a ticket that redoes earlier work.

## Output

A list of findings, each with `file:line`, the axis, and a severity: `serious` (wrong, missing, or unsafe; blocks done) or `minor`. Then the break list: file, line, and the change to make. End with "no serious findings" or the count. Report only what you can point to in the code.
