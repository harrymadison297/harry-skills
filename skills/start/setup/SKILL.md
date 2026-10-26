---
name: setup
description: Record where this repo already keeps its glossary, coding standard, ADRs, and instructions for running the app, as one pointer block in CLAUDE.md or AGENTS.md. Use when a repo has docs the workflow should reuse, or when those docs have moved.
disable-model-invocation: true
---

# Prepare the repo

The other skills read a glossary, a coding standard, ADRs, and a way to run the app. A repo that already has them has its own names and places. This skill tells the skills where to look, so none of them creates a second copy.

## Process

1. **Find** each item in the repo, and follow the repo's own convention over any default:

| Item | Usual places |
|---|---|
| Glossary | `GLOSSARY.md`, `docs/glossary.md` |
| Coding standard | `docs/standards.md`, `CONTRIBUTING.md`, lint config |
| ADRs | `docs/adr/`, `docs/decisions/` |
| How to run the app | `docs/how-to-run.md`, README, Makefile, package scripts |

2. **Show** the block below, listing only what exists, and wait for a yes.
3. **Write** it into `CLAUDE.md`, or `AGENTS.md` if that is the one that exists. If neither exists, ask which to create. Update an existing block in place and leave the rest of the file alone.

```markdown
## Workflow files

- Glossary: `GLOSSARY.md`
- Coding standard: `docs/standards.md`
- ADRs: `docs/adr/`
- Run the app: `docs/how-to-run.md`
```

## Running again

Compare the block with the repo, show the difference, and apply what the user approves.

## Nothing found

Do nothing and say so. The skills that need a file create it when they have something to put in it.
