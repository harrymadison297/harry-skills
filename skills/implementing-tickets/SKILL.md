---
name: implementing-tickets
description: Step 4 of the feature workflow. Builds one ready ticket in a fresh context with TDD at the approved seams, then runs review and verify, and marks it done with evidence or parks it with a stop report. Use when flow hands over a ticket.
disable-model-invocation: true
---

# Implement

Turn one ticket into working, reviewed, and verified code. Small tickets in fresh contexts keep you in the range where you reason well. The checks and stop rules let you run without the user.

## Read, and nothing else

The ticket, `spec.md`, `architecture.md`, `docs/standards.md`, `GLOSSARY.md`, and the notes and git log of the tickets this one depends on. Read nothing from the planning conversation: whatever mattered is in those files.

## Loop

1. **Pin old behavior.** If the code you are about to change has no tests, write characterization tests first, in their own `test:` commit.
2. **TDD at the approved seams.** Write one failing test, make the smallest change that passes it, repeat. Take expected values from the spec or a worked example, never from a run of the code under test, or the test only echoes the code. Put tests only at seams `architecture.md` approved.
3. **Refactor** with green tests. A `refactor:` commit never changes a test file. If a test blocks the refactor, it asserts implementation: fix that test in its own commit first.
4. **Review.** Spawn a fresh subagent running `reviewing-changes` on the ticket diff. Fix every serious finding, then go back to step 2 for new behavior. Then do the breaks it lists: break the code at each place, confirm a test fails, undo the break. A break no test catches means a missing test.
5. **Verify.** Spawn a fresh subagent running `prove-it-work` on the ticket. Act on the verdict (below).
6. **Finish.** When all three checks hold, make the final commit: set `Status: done` and add the evidence.

## Three checks before done

| Check | Condition |
|---|---|
| Tests | Every criterion has a test that failed before it passed, and every break the reviewer chose is caught |
| Review | No serious finding |
| Verify | Every e2e step `VERIFIED`, with evidence, in every environment the ticket lists |

| Verdict | Do this |
|---|---|
| `VERIFIED` | Move on |
| `NOT VERIFIED` | Back to step 2. Counts as an attempt. |
| `INCONCLUSIVE` | Repair the verify tooling in its own `test:` commit and rerun. Not an attempt on the code. Two in a row with the same cause park the ticket. |

## Rules

- **Every commit is green.** Use Conventional Commits and end with a `Ticket: T04` trailer.
- **The plan is a contract.** A change to the spec, the architecture, or an ADR goes in its own `docs:` commit before the code that needs it, and you report it. Never edit the e2e scenario: the user approved it.
- **Stay inside the ticket.** The `Out of scope` list is a boundary. Note extra ideas in `Notes`; do not build them.
- **Log each attempt** in `Notes` before starting the next. An attempt is one fix plus a rerun of the failed check.

## Stop rules

Set `Status: parked` and write `stops/T04.md` when:

- three attempts failed, or fixing one failure caused another;
- the ticket needs a decision only the user can make, including a spec, architecture, or ticket that turned out wrong;
- the next step cannot be undone (force push, deploy, data deletion).

The report states what happened, what you tried, and what needs fixing: `nothing`, `ticket`, `spec-it`, or `architecture`. Then stop. `build-a-feature` decides what comes next.
