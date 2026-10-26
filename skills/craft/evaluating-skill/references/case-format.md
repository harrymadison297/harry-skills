# Case format

Evals live outside the skill folder, in `evals/<skill>/<case>/`, so a subagent that reads the skill never sees its tests.

```
evals/<skill>/<case>/
  prompt.md        the request, as a user would type it
  case.yaml        what a good result looks like
  graders/NN-slug.md   one checkable statement per file
  files/           the starting project
  place-files.sh   copies files/ into the working directory and builds the git history
```

## prompt.md

Front matter, then the request and nothing else. No mention of evaluation, of the skill's name when the real user would not say it, or of the expected result.

```
---
tags: [<skill>]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Write, Edit, Bash]
---

<the request>
```

## case.yaml

```yaml
schema_version: "1.1"
name: <case>
context:
  scaffold_script: place-files.sh
expected_outcome: |
  <what a good run does, in three sentences or fewer, ending where the run should stop>
```

## graders/NN-slug.md

```
---
type: llm        # or: script
focus: trace     # or: state, reply
weight: 1
---

<one statement that is true or false from the evidence>
```

For `type: script`, put an executable `NN-slug.sh` beside the markdown file. It runs in the final project directory and exits 0 when the statement holds.

## place-files.sh

```bash
#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q -b main
git config user.name dev
git config user.email dev@example.com
git add -A
git commit -q -m "first version"
```

Add further commits for a history, and leave changes uncommitted when the case needs a dirty tree. Use `git commit --allow-empty` when a step may have nothing to commit.

## Fixture checklist

- Small and realistic, with a git history a real repo would have.
- Every fact an assertion quotes appears in the fixture; read the files again before you finish.
- Anything the prompt says about the machine (a tool is missing, a port is free) is checked on this machine.
- The fixture contains no hint that it is a test: no `eval`, `test-case`, or `fixture` in a path or a file.
- A run stays in its own directory. If the skill under test writes files, they land in the working directory.

## grading.json

One file per grader, keyed by case. The field names are fixed because viewers read them.

```json
{
  "<case>": [
    {"text": "<assertion>", "passed": true, "evidence": "<one line: a quote or a tool call>"}
  ]
}
```

## Results table

| Case | with | none | old |
|---|---|---|---|
| `<case>` | passed/total | passed/total | passed/total |

Add a row of means. Under the table, list each failed assertion with its cause: skill, eval, or model.
