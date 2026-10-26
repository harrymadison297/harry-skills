---
name: handon
description: Pick up a repo where it stands, the counterpart of handoff. Checks where things stand from git and the files on disk, tells the user in a few lines, then routes to the next skill. Use at the start of a session, when the user wants to build, change, or fix something in a repo, says "flow", "continue", "what's next", or comes back to a half-finished feature.
---

# Hand on

Look before you act. Check the repo, say where it stands, and route to the next skill. The state lives in files and commits, so you can hand on in any session. Keep no state file of your own: it would drift from the commits.

## Check

Read only. Change nothing and ask nothing until you have all of this.

1. `git status`, `git log -20`, and the current branch. The last commit is always green.
2. The base: `GLOSSARY.md`, `docs/standards.md`, and `docs/how-to-run.md`.
3. Every folder `docs/features/<feature>/`. For each one, find its current step (see Steps) and note any `pause.md`.

## Report

Tell the user in a few lines, before routing:

- the branch, the last commit, and whether there are uncommitted changes
- which base files are missing, as a fact only; a missing base file never changes the route
- each feature with its current step, or "none"
- what a `pause.md` says, if there is one

## Route

Take the first row that fits.

| Situation | Route |
|---|---|
| Uncommitted changes and the user is resuming after a crash | Offer to discard them, then check again |
| A folder has `pause.md` | Read it, follow it, then delete it |
| One unfinished feature, and the user says "continue" or names no new work | **Resume** it at its current step |
| Several unfinished features | Ask which one, then **resume** |
| The user describes new work while a feature is unfinished | Ask which one they mean |
| No unfinished feature, or the user describes new work | **New**: name the feature with the user, create `docs/features/<feature>/`, propose a size, start at step 1 |
| Every feature is shipped and the user gave no work | Say so and ask what to build |

A resume keeps the size it already has, so do not ask again.

## Size

For a new feature, propose a size and let the user confirm it in one line.

- **Small**: one ticket that touches no public contract, no data, and nothing unclear. Write the ticket, show its e2e scenario, get a yes, then go to step 4 with no checkpoint.
- **Full**: everything else. Run all five steps.

When unsure, pick full. A wrong "small" skips the gates that catch a misunderstood journey.

## Steps

The current step is the first row whose file is missing or still `Status: draft`.

| Step | File | Skill | Gate |
|---|---|---|---|
| 1 | `spec.md` | `ask-until-clear`, then `spec-it` | Gate 1 |
| 2 | `architecture.md` | `designing-architecture` | Gate 2 |
| 3 | `tickets/T*.md` | `slicing-tickets` | Gate 3 |
| 4 | tickets not `done` | `implementing-tickets` | Checkpoints |
| 5 | all tickets `done` or `parked` | `shipping-features` | The report |

Run that step's skill. Do not skip ahead, because a later file built on an unapproved earlier file is wasted work.

Step 1 has two skills in one context.

- **New feature**: run `ask-until-clear` first, until the user has settled what to build. Then `spec-it` writes only what the interview settled.
- **Resume with `spec.md` as `draft`**: the interview is done, so do not run it again. Run `spec-it` to finish the draft.
- **Resume with no `spec.md`**: the interview was lost with the old context. Run `ask-until-clear` again. Point it at `GLOSSARY.md` and the ADRs first, so what was already settled is not asked twice.

If `spec-it` returns with `Open questions`, go back to `ask-until-clear` in every case. Never let `spec-it` fill a gap with a guess.

## Gates

At a gate, stop and ask the user to approve the file. Only you set `Status: approved`, and only after the user says so. Writing it earlier turns the gate into a formality.

- Editing an approved file sets it back to `draft` and reruns its gate.
- At gate 3, set the tickets from `draft` to `todo`.
- After a gate, if the context is over half full, offer `handoff`. Steps 1 to 3 share one context, so the offer saves the next step from starting degraded.

## Build loop (runs Step 4)

A ticket is **ready** when it is `todo` and every ticket in its `Blocked by` is `done`. Compute this from the files.

1. Pick the next ready ticket. Run `implementing-tickets` on it in a fresh context (a subagent), so the build never reads the planning chat.
2. When it returns `done`, continue. If the ticket was `T01` or `Review: human`, stop at the checkpoint: show the diff and the evidence, and wait for "continue".
3. When it returns `parked`, read the stop report. If it blames the ticket, move on to tickets the parked one does not block. If it blames the spec or the architecture, stop all of step 4: fix that file with the user, rerun its gate, and run `slicing-tickets` in re-cut mode. The remaining tickets may rest on the same wrong assumption.
4. When no ready ticket is left, go to step 5.

## Done when

The user has seen the state report and the route you took. Say which step you ran, which file changed, and what the user must do next.
