---
name: shipping-features
description: Step 5 of the feature workflow. Reviews the whole feature, runs every journey on the finished branch in the environments that matter, tags the evidence, and reports the result in chat. Opens no pull request. Use when all tickets are done or parked.
disable-model-invocation: true
---

# Ship

Each ticket was judged alone. Only a pass over the whole feature finds the journey that broke between tickets. Write the report with `quill-technical-writing`.

## Process

1. **Review the whole diff.** Run `reviewing-changes` in whole-feature mode. Each serious finding becomes a fix ticket that goes through step 4.
2. **Run every journey.** On the finished branch, run every test path of every journey in `spec.md` (`J1.1`, `J1.2`, ...) via `prove-it-work`, in every environment where the whole feature could behave differently. Use the environments in `docs/how-to-run.md` and the ones the tickets already ran, and re-run a ticket's scenario only where the combined change makes an earlier result doubtful. Each failure becomes a fix ticket. Stop here until none remain.
3. **Tag.** Tag the last commit that still holds the evidence as `evidence/<feature>`. Push the tag only if the repo has a remote. Evidence is read with `git show evidence/<feature>:<path>`, so it survives the clean up and a squash merge.
4. **Clean up** in a new commit: delete `tickets/`, `stops/`, and `evidence/`. Stamp `spec.md` and `architecture.md` with "as of <commit>".
5. **Report** in chat (below). Open no pull request: the user decides how to merge. Offer `learn-from-mistakes` afterward.

## Report

Keep it short enough to read in under a minute. Link evidence, do not paste it.

1. A one-paragraph summary: what the user can now do.
2. Tickets ordered by risk: `Review: human` tickets and tickets with findings first. Each gets a short excerpt and the `git show` path to its evidence at the tag.
3. A matrix of tickets against environments, with the verdicts.
4. Parked tickets and why.
5. Notes: departures from the architecture, open RFCs.

## Done when

Every journey ran green on the final branch, the tag exists, and the report is in chat.
