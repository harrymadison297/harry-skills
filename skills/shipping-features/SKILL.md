---
name: shipping-features
description: Step 5 of the feature workflow. Reviews the whole feature, runs every journey on the finished branch in the environments that matter, writes the PR body, tags the evidence, and opens the pull request. Use when all tickets are done or parked.
disable-model-invocation: true
---

# Ship

Each ticket was judged alone. Only a pass over the whole feature finds the journey that broke between tickets. Write the PR body with `quill-technical-writing`.

## Process

1. **Review the whole diff.** Run `reviewing-changes` in whole-feature mode. Each serious finding becomes a fix ticket that goes through step 4.
2. **Run every journey.** On the finished branch, run every test path of every journey in `spec.md` (`J1.1`, `J1.2`, ...) via `prove-it-work`, in every environment where the whole feature could behave differently. Use the environments in `verify-<app>` and the ones the tickets already ran, and re-run a ticket's scenario only where the combined change makes an earlier result doubtful. Each failure becomes a fix ticket. Stop here until none remain.
3. **Write the PR body** (below).
4. **Tag.** Tag the last commit that still holds the evidence as `evidence/<feature>`, and push it. The links in the PR point to the tag, so a reviewer can open them after a squash merge.
5. **Clean up** in a new commit: delete `tickets/`, `stops/`, and `evidence/`. Stamp `spec.md` and `architecture.md` with "as of <commit>".
6. **Open the PR.** Offer `learn-from-mistakes` afterward.

## PR body

Up to about 60,000 characters (GitHub allows about 65,000).

1. A one-paragraph summary: what the user can now do.
2. Tickets ordered by risk: `Review: human` tickets and tickets with findings first. Each gets a short excerpt and a link to its evidence at the tag.
3. A matrix of tickets against environments, with the verdicts.
4. Parked tickets and why.
5. Notes: departures from the architecture, open RFCs.

## Done when

Every journey ran green on the final branch, the tag exists, and the PR is open. Give the user the link.
