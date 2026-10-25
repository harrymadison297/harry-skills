---
name: learn-from-mistakes
description: Turn a mistake the agent made twice into a check in the repo (architecture, type, lint, test, or one line of standard), proven on the real past mistake. Use after shipping a feature, or after a build that went sideways.
disable-model-invocation: true
---

# Retro

Without it, the agent repeats the same mistake in every feature. A lesson in personal memory is not in the repo, so nobody reviews it. Keep every lesson in the repo.

## Process

1. **Collect mistakes** from the stop reports, review findings, `NOT VERIFIED` verdicts, and the PR discussion. A mistake counts once it has happened **twice**; note single ones in `docs/lessons.md` as "seen once" and stop.
2. **Block it at the highest level that works**, in this order:
   1. Architecture: change the shape so the mistake cannot be written.
   2. Type: make the wrong state unrepresentable.
   3. Lint rule or hook.
   4. Test.
   5. One line in `docs/standards.md`, which `reviewing-changes` reads. Only for mistakes that need judgment.
   Higher levels need no one to remember anything.
3. **Prove the check.** Apply it to the commit where the mistake happened. It must fail there. A check that never failed on a real mistake is a guess; reject it.
4. **Record** in `docs/lessons.md`: what went wrong, the two occurrences, the check, where it lives, and the past mistake that proved it.
5. **Propose** all changes in the PR for the user to approve. `CLAUDE.md` or `AGENTS.md` holds only a pointer to `docs/standards.md`, never the rules.

## Done when

Each accepted lesson has a check that failed on its past mistake, a ledger entry, and the user's approval.
