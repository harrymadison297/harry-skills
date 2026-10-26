---
name: prove-it-work
description: Run the real system in each required environment, drive it through a ticket's e2e scenario by its real surface (CLI, API, browser), save evidence, and report VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Use after review, in a fresh subagent.
disable-model-invocation: true
---

# Verify

Passing tests prove the code does what the tests say. They do not prove the system works for a user. Run it the way a user would, and keep the proof. Run in a fresh subagent.

## Process

1. **Read** the ticket's `E2E scenario` and `docs/how-to-run.md`. The ticket lists the environments to run. If the change touches something the list misses, add that environment and say so in the report.
2. **For each environment**, separately:
   1. Start the real system as `docs/how-to-run.md` says. Use the built artifact, not the dev shortcut, unless the ticket says otherwise.
   2. Run each scenario step through its real surface: type the CLI command, send the HTTP request, click in the browser. Do not call internal functions.
   3. After each step, compare what you observed with the `verify:` line.
   4. Save evidence to `evidence/T04/<environment>/`: command transcripts, response bodies, screenshots, logs. A step without evidence is not verified.
   5. Clean up as `docs/how-to-run.md` says.
3. **Report** one verdict per environment. One environment never offsets another.

## Verdicts

| Verdict | Meaning |
|---|---|
| `VERIFIED` | Every step did what the scenario says, with evidence |
| `NOT VERIFIED` | The system did the wrong thing. Quote the step, the expected, and the observed. |
| `INCONCLUSIVE` | No verdict possible: the environment or the verify tooling broke. Say which and why. |

## Rules

- Never edit the scenario. The user approved it. If it is wrong, report that as `NOT VERIFIED` with the reason.
- If a feature needs a tool that `docs/how-to-run.md` lacks (a fixture, a driver), extend `docs/how-to-run.md` and say so.
- Do not fix product code here. Report only.
- Report what you saw, not what you expect to see. A step that was skipped is `INCONCLUSIVE`, not passed.
