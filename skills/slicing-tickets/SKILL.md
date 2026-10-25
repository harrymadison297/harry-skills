---
name: slicing-tickets
description: Step 3 of the feature workflow. Cuts an approved spec and architecture into small vertical tickets with blocking edges and e2e scenarios, and prints the ticket graph. Also re-cuts tickets when a build proved the plan wrong. Use after architecture.md is approved.
disable-model-invocation: true
---

# Slice

Cut the plan into pieces one agent can build, review, and verify in a fresh context. Large pieces cannot be reviewed. Small tickets with their own pass-or-fail checks let the agent work alone and a reviewer judge each piece.

## Rules

| Rule | Detail |
|---|---|
| Vertical | A ticket is a narrow path through every layer the feature touches (schema, API, CLI, UI). Never one layer only. |
| Small | It can be demonstrated on its own and fits one context. |
| Ordered | It lists the tickets that block it, and only those that truly do. |
| Walking skeleton | `T01` is the thinnest slice that runs one real test path. Every other ticket waits for it, except preparation tickets. |
| Preparation first | A refactor or a new test tool is its own ticket and goes first. A mechanical change across the codebase, such as a rename, is cut as expand, migrate in batches, then contract. |
| E2E scenario | Each ticket carries user actions, what the user observes, and the environments, chosen from `verify-<app>`. Pick every environment where this ticket's change could behave differently (operating system, paths, permissions, deployment), not the cheapest one. Make it strict enough that a half-working system fails it. |
| Review label | `Review: human` for tickets touching a public contract, data, security, or logic that tests catch poorly. `T01` is always `human`. Otherwise `auto`. |

## Ticket file

Write `docs/features/<feature>/tickets/T01-<slug>.md`, each with `Status: draft`:

```
# T04: <what the user sees>

Status: draft | todo | parked | done
Review: auto | human
Blocked by: T01, T02 (or none)
Journey: J1.2
Criteria: AC3, AC5

## What to build      (user's view, in GLOSSARY.md terms)
## Where              (one or two sentences, module names from architecture.md)
## Tests              (one line per approved seam: what it catches and misses)
## E2E scenario
Environments: local, vm-ubuntu
1. <action by the real surface> -> verify: <what you observe>
## Out of scope
## Notes
```

## Process

1. Read `spec.md` and `architecture.md`. Cover every `AC` with at least one ticket.
2. Write the tickets, then run `python3 scripts/graph.py docs/features/<feature>/tickets` and show the graph. Fix any cycle or orphan it reports.
3. Hand back to `build-a-feature` for gate 3. The user approves the scenarios here, and the agent cannot change them later.

## Re-cut mode

Run when a ticket was parked because the plan was wrong and the user fixed `spec.md` or `architecture.md`. `done` tickets stay unless the fix makes them wrong. Rewrite or delete unfinished tickets, add new ones, and re-run the graph. Parked tickets return to `todo` only after the re-cut.

## Done when

Every criterion has a ticket, the graph has no cycle, and each ticket has an e2e scenario and a review label.
