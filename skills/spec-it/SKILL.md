---
name: spec-it
description: Step 1 of the feature workflow. Turns a finished interview into spec.md with journeys, numbered acceptance criteria, how each journey is checked end to end, non-goals, and decisions. Use after ask-until-clear has settled what to build, before any design or code.
disable-model-invocation: true
---

# Spec

Agree on what to build before anyone discusses how. This skill writes down what the interview settled, in a file the user approves. It does not interview: a gap is a question for `ask-until-clear`, and an invented answer would be an assumption the user never saw.

## Process

1. **Read** the interview, the glossary and the ADRs (paths are in the `Workflow files` block of `CLAUDE.md` or `AGENTS.md`), and the code the feature touches. Run `understand-this-code` if you need more of it.
2. **Find the gaps.** Check each section of the template below against what was settled. Anything missing goes under `Open questions` with your recommended answer. Do not fill it with a guess, and do not fix it by interviewing.
3. **Write** `docs/features/<feature>/spec.md` with `Status: draft`, using the glossary's words. Say what the system does, never how: tables, ports, libraries, and file paths belong to the architecture step.
4. **Check** the file against "Done when". If `Open questions` is not empty, say so and hand back to `ask-until-clear`.

## spec.md

```
# <Feature>
Status: draft

## Goal
## Journeys
### J1 <name>
J1.1 <one concrete run>
  Check: <surface (CLI, API, browser, device)>, <environment>, <what you observe>
## Acceptance criteria
AC1 (J1.1): <passes or fails>
## Non-goals
## Decisions
## Open questions
```

| Section | Content |
|---|---|
| Goal | The problem and the user, in a few sentences |
| Journeys | `J1`, `J2`: a path a user takes to reach a goal. Each concrete run is a test path, `J1.1`, `J1.2`. The user can be a person, an API caller, a scheduled job, or another system. For a pure refactor, the journey is the existing behavior that must stay the same. |
| `Check:` line | Under every test path: the real surface it is driven through, the environment it runs in, and what you observe. The user approves it here, so later steps cannot make it weaker. |
| Acceptance criteria | `AC1`, `AC2`: each passes or fails, names its test path, and uses no subjective word ("fast", "intuitive"). A non-functional need is a criterion too, with a threshold and a way to measure it. |
| Non-goals | What this feature does not do, including what the interview ruled out |
| Decisions | Each decision the interview settled, in one line with its reason, and the ADR if there is one. Do not restate an ADR. |
| Open questions | What the interview did not settle, each with your recommended answer |

## Done when

- Every journey has at least one test path, and every test path has a `Check:` line.
- Every criterion names a test path, and one test or one e2e step can check it.
- Nothing in the file says how it will be built.
- `Open questions` is empty. If it is not, the user cannot approve the spec yet. Hand back to `build-a-feature` for gate 1.
