---
name: build-a-feature
description: Start or resume the feature workflow, from idea to merged pull request. Use when the user wants to build, change, or fix something in a repo, says "flow", "continue", "what's next", or comes back to a half-finished feature. Finds the current step from the files on disk and runs the next skill.
---

# Flow

Find where the feature stands, run the next skill, and hold the gates. The state lives in files and commits, so you can resume from any session. Keep no state file of your own: it would drift from the commits.

## 1. Locate

1. Read `git status` and `git log -20`. If there are uncommitted changes and the user is resuming after a crash, offer to discard them. The last commit is always green.
2. If `GLOSSARY.md`, `docs/standards.md`, or `.claude/skills/verify-*` is missing, run `setup` first.
3. Find the feature folder `docs/features/<feature>/`. Ask which feature only if several are unfinished.
4. If the folder has a `pause.md`, read it first, follow it, then delete it.

## 2. Size

Propose a size and let the user confirm it in one line.

- **Small**: one ticket that touches no public contract, no data, and nothing unclear. Write the ticket, show its e2e scenario, get a yes, then go to step 4 with no checkpoint.
- **Full**: everything else. Run all five steps.

When unsure, pick full. A wrong "small" skips the gates that catch a misunderstood journey.

## 3. Find the current step

The current step is the first row whose file is missing or still `Status: draft`.

| Step | File | Skill | Gate |
|---|---|---|---|
| 1 | `spec.md` | `spec-it` | Gate 1 |
| 2 | `architecture.md` | `designing-architecture` | Gate 2 |
| 3 | `tickets/T*.md` | `slicing-tickets` | Gate 3 |
| 4 | tickets not `done` | `implementing-tickets` | Checkpoints |
| 5 | all tickets `done` or `parked` | `shipping-features` | The PR |

Run that step's skill. Do not skip ahead, because a later file built on an unapproved earlier file is wasted work.

## 4. Gates

At a gate, stop and ask the user to approve the file. Only you set `Status: approved`, and only after the user says so. Writing it earlier turns the gate into a formality.

- Editing an approved file sets it back to `draft` and reruns its gate.
- At gate 3, set the tickets from `draft` to `todo`.
- After a gate, if the context is over half full, offer `handoff`. Steps 1 to 3 share one context, so the offer saves the next step from starting degraded.

## 5. Build loop (step 4)

A ticket is **ready** when it is `todo` and every ticket in its `Blocked by` is `done`. Compute this from the files.

1. Pick the next ready ticket. Run `implementing-tickets` on it in a fresh context (a subagent), so the build never reads the planning chat.
2. When it returns `done`, continue. If the ticket was `T01` or `Review: human`, stop at the checkpoint: show the diff and the evidence, and wait for "continue".
3. When it returns `parked`, read the stop report. If it blames the ticket, move on to tickets the parked one does not block. If it blames the spec or the architecture, stop all of step 4: fix that file with the user, rerun its gate, and run `slicing-tickets` in re-cut mode. The remaining tickets may rest on the same wrong assumption.
4. When no ready ticket is left, go to step 5.

## Done when

The PR is open and the user has the link. Say which step you ran, which file changed, and what the user must do next.
