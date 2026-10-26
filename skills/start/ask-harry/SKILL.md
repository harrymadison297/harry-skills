---
name: ask-harry
description: Name the skill to run right now for the situation the user describes. A router over the skills in this plugin. Use when the user does not know which skill fits or what comes next.
disable-model-invocation: true
---

# Ask Harry

The user does not remember every skill, so they ask. Take their situation, name the skill to run, say why, and stop. Do not run the skill, interview the user, or write a file.

Before you say what a skill does, or tell the user to skip one, read its `SKILL.md`. The tables below help you find a skill, not describe it. A sibling skill is at `../../<group>/<name>/SKILL.md`, relative to this file, where the group is `start`, `plan`, `build`, or `craft`.

## Process

1. **Take the situation** from the user's message. If there is none, ask one question: "What are you trying to do right now?"
2. **Find the row** below. Take the first one that fits. If two skills look alike, check Close calls.
3. **Read** the `SKILL.md` of each skill you are about to name.
4. **Reply** with the command, one line on why, and one line on what comes after it. If the situation takes several skills, list them in order and mark where the user decides.
5. **Stop.** The user types the command.

## Pick by situation

| Situation | Run |
|---|---|
| Build, change, or fix something in a repo, or resume a feature | `handon` |
| Stress-test a plan or an idea, with no feature started | `ask-until-clear` |
| A term is fuzzy or conflicts with the glossary, or a decision just settled | `term-guard` |
| You do not know how the code works, or what a change could break | `understand-this-code` |
| A decision depends on a fact about an API, a library, or a platform | `research` |
| A design question that talking cannot settle | `prototyping-designs` |
| Something is broken, flaky, slow, or regressed | `debugging-failures` |
| The context is filling up, or you want to stop and resume later | `handoff` |
| The repo already has a glossary, standard, or ADRs the skills should reuse | `setup` |
| The agent cannot start or drive the real app, or `docs/how-to-run.md` is missing | `make-way` |
| The agent made the same mistake twice | `learn-from-mistakes` |
| Write a doc, commit message, or PR body | `quill-technical-writing` |
| Text reads as machine-written | `quill-unslop` |
| Check whether a skill changes what a model does | `evaluating-skill` |

## Inside the feature flow

For anything in this list, tell the user to run `handon`. It checks the repo, finds the step, and runs the right skill. Only `handon` sets `Status: approved`, so starting a step by hand skips the gate.

| Step | Skills | Gate |
|---|---|---|
| 1 Spec | `ask-until-clear`, then `spec-it` | You approve the journeys and the e2e check |
| 2 Architecture | `designing-architecture` | You approve the architecture |
| 3 Slice | `slicing-tickets` | You approve the tickets and e2e scenarios |
| 4 Implement | `implementing-tickets`, which runs `reviewing-changes` and `prove-it-work` | You read the diff at each checkpoint |
| 5 Ship | `shipping-features` | You read the report |

## Close calls

- **`ask-until-clear` or `spec-it`.** `ask-until-clear` asks. `spec-it` writes what the interview settled and never asks.
- **`understand-this-code` or `research`.** The first reads your code. The second reads sources outside it.
- **`research` or `prototyping-designs`.** Use `research` when reading answers the question. Use `prototyping-designs` when something has to run.
- **`debugging-failures` or `implementing-tickets`.** Use `debugging-failures` for behavior that used to work or should work. Use `implementing-tickets` for a ticket that `handon` hands over.
- **`setup` or `make-way`.** `setup` records where the repo keeps its docs. `make-way` finds how the app is built and tested, reports it, and writes `docs/how-to-run.md`.
- **`handoff` or `handon`.** `handoff` pauses a session. `handon` picks it up.
- **`quill-technical-writing` or `quill-unslop`.** The first sets the standard for new text. The second cleans text that exists.
- **A small change.** Still `handon`. It proposes the size, and a small change skips steps 1 to 3.

## Rules

- Write each command with the plugin prefix: `/harry-skills:handon`.
- Name only skills from this plugin. This file is a map of them, not a scan of what is installed.
- If no skill fits, say so. Do not stretch one to fit.
- If the user already named the skill, say "run it" and nothing more.
- Keep the reply short. The user wants the next command, not a tour.

## Done when

The user has one command to type, a reason in one line, and what follows it.
