---
name: debugging-failures
description: Fix a hard bug by first building a feedback loop that fails on demand, then testing hypotheses one at a time. Use when something is broken, flaky, slow, or regressed.
disable-model-invocation: true
---

# Debug

Agents guess at causes. A loop that reproduces the failure turns a guess into something provable. Build the loop before you form any theory.

## Process

1. **Build a loop**: one command that goes red on this bug, every time. A failing test, a script, a recorded request. For a flaky bug, loop it until the rate is high enough to see. Shrink the input until only the failing part remains. If you cannot build a loop, stop and tell the user what you need.
2. **Hypothesize.** Write 2 to 4 causes, each with a prediction: "if X, then changing Y makes the loop go green". Rank them. A hypothesis that predicts nothing is not worth testing.
3. **Test one change at a time**, cheapest and most likely first. Add temporary logging if it settles the question. Mark all debug code so you can remove it.
4. **Fix the root cause**, not the symptom. Ask why the wrong state was reachable.
5. **Lock it down.** Add a regression test at an existing seam that failed before the fix. If there is no seam, say so; that is a finding for `learn-from-mistakes`.
6. **Clean up.** Remove debug code. Run the full tests.

## Rules

- Do not edit a test to make it pass. The only exception is a test the spec proves wrong, in its own commit.
- Same stop rules as `implementing-tickets`: after three failed attempts, stop and report what you ruled out, and ask for help.

## Done when

The loop is green, a regression test covers the bug, and no debug code remains.
