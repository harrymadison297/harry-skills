# Evals

Test cases for the skills. They live here, outside the skill folders, so a subagent that reads a skill never sees its tests.

```
evals/
  <skill>/<case>/
    prompt.md        the request, as a user would type it
    case.yaml        what a good result looks like
    graders/NN-*.md  one checkable statement per file
    files/           the project the request is run against
    place-files.sh   copies files/ into a working directory
  _tools/            scripts that generate cases and run them blind
```

Skills covered: `ask-until-clear`, `term-guard`, `spec-it`. Each has three cases (a notes app with offline sync, an ESP32 battery node, zero-downtime deploys on Linux hosts).

## Run blind

A subagent under test must not be able to tell it is being tested, because that can change its behavior.

1. `_tools/prep.py <skill> new,old,matt,none` creates one run directory per case and configuration under a random id, copies the project and the skill into it, and writes a map from id to configuration that the agent never sees. The paths contain no configuration name and no word like eval.
2. Start one subagent per run with the prompt from the generated file. Word it like a normal request. Do not tell it to write its answer to a file.
3. `_tools/collect.py <skill> <tag>` reads each transcript, takes the final report, and builds the folder a grader reads.
4. Grade in separate subagents, a few at a time, so the session limit is not hit. Graders may know which configuration they are grading.

`gen_*.py` regenerate the cases. All of these scripts use absolute paths from the session that wrote them (`/tmp/.../scratchpad`, `/home/cuongtc9/skills/skills`). Change the path constants before reuse.

## Last results

Mean pass rate over the three cases of a skill. `new` is the current skill, `old` the previous draft, `matt` the reference skill from mattpocock/skills, `none` no skill.

| Skill | new | old | matt | none | Run |
|---|---|---|---|---|---|
| `spec-it` | 0.85 | 0.59 | 0.20 | 0.33 | blind |
| `ask-until-clear` (first round only) | 0.80 | 0.81 (v3) | 0.50 | 0.44 | not blind |
| `term-guard` | 0.91 | | 0.91 | 0.73 | not blind |

Caveats: three cases, one run each, graders from the same model family, and assertions written by the same author as the skills. For `spec-it`, the `matt` score is low mostly because it writes a different document format. Re-run `ask-until-clear` and `term-guard` blind before trusting their numbers.
