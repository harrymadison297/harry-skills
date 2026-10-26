---
name: evaluating-skill
description: Creates an eval set for one skill, runs it blind on the chosen models against a no-skill baseline, grades it, and reports what the skill adds. Use when a skill is new, was edited, or its behavior is in doubt.
disable-model-invocation: true
---

# Eval a skill

Prove that a skill changes what a model does. Every case is an ordinary request, so a pass shows real behavior. File formats are in [references/case-format.md](references/case-format.md). `scripts/prep.py` and `scripts/collect.py` do steps 4 and 5.

```
- [ ] 1 Intent
- [ ] 2 Cases
- [ ] 3 Approval
- [ ] 4 Run
- [ ] 5 Collect
- [ ] 6 Grade
- [ ] 7 Classify
- [ ] 8 Report
```

## Steps

1. **Intent.** List the skill's branches: each route, stop, and done-when. Write in five lines what it must do, must never do, and where it stops for the user. Ask the user about any branch where the skill's text and their goal may differ.
2. **Cases.** Write 3 to 6, one branch each: the main path, every stop-and-ask, a boundary where the skill does nothing, and a trap. A case is a small repo with a git history, a request worded as the user would type it, and one assertion per file.
   - *State* assertions check the final repo; use a script when one can decide.
   - *Trace* assertions check the tool calls.
   - *Reply* assertions check the final report.

   Each assertion must be able to fail, and every fact it quotes must match the fixture and this machine. A run lasts one turn with no human, so stopping to ask is a valid end; where the request pre-approves, writing is expected. For a model-invoked skill, add cases whose request should start the skill and cases whose request should not.
3. **Approval.** Show the intent, the assertions, and this table, then wait for a yes. Run nothing before it.

   | Case | Branch | Request | Expected |
   |---|---|---|---|

   Under it, name the models: *tested* (the ones the user plans to use; default Haiku), *grader* (a different model), and the configurations (`with`, `none`, and `old` when improving). After results, edit a case only if the eval was wrong; record the edit and rerun that case.
4. **Run.** `python scripts/prep.py --evals evals/<skill> --skill <skill dir> --out <scratch> --configs with,none` (add `old=<snapshot dir>` when improving) builds one run directory per case and configuration under a random id. Start every run in one turn as a background subagent on a tested model, with its prompt from `<scratch>/blind/prompts.json` unchanged. A run never learns it is tested.
5. **Collect.** `python scripts/collect.py --evals evals/<skill> --out <scratch> --tasks <transcript dir> --tag <name>` writes one folder per run. A transcript that touched the eval folders is a leak: discard that run. Stop each listed leftover process by PID.
6. **Grade.** Use one grader subagent per skill and configuration, a few at a time. A grader runs each script assertion in the run's `project/` folder, judges the rest from the transcript and the final project, fails an assertion the evidence does not show, and writes `grading.json`. It also lists assertions that always pass, outcomes nothing checks, and assertions the fixture contradicts.
7. **Classify** each failure as *skill* (its text allows or causes it), *eval* (wrong fact, misread intent, grader error), or *model* (ignored a clear instruction). Fix eval faults and rerun those cases.
8. **Report** the pass rate per configuration and case, the failures by cause, and what the skill adds over `none`. If `none` passes 90% or more, say the skill adds little and name the assertions that separate the two. State the caveats: runs per case, graders from one model family, assertions written by the skill's author. Propose skill changes as a list. Edit the skill only when the user asks, then rerun with `old` as the baseline.

## Done when

The user approved the table, intent, and assertions before any run; every case ran under `with` and `none`; every failure has a cause; no run left a process behind; the report states the caveats.
