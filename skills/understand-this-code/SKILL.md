---
name: understand-this-code
description: Explain how the code you are about to change works, why it has its current shape, and what a change could break, proving safety claims by running code. Use before changing unfamiliar code, and when spec or architect needs to know what the code already answers.
disable-model-invocation: true
---

# Explore

The agent should know the old code before it changes it. This skill is read-only.

## Answer three questions

1. **How does it work?** Trace the path from the entry point through the code that the change touches. Cite `file:line`. Name the modules and their interfaces.
2. **Why is it shaped this way?** Read `git log` and `git blame` on the key files, the ADRs, and the PR history. A strange shape often guards a past bug; say which one if you can find it.
3. **What could a change break?** List callers, tests, external contracts (API, CLI flags, file formats), and stored data that depend on it. Search for usages rather than assuming.

## Prove, do not assert

For any claim about safety or behavior ("nothing else calls this", "this returns null on empty"), run something that shows it: a grep with its result, a test run, a one-line script. Quote the output. A claim you did not run is marked "unverified".

## Output

A short note, in the user's words from `GLOSSARY.md`: the three answers, then what to preserve and what to avoid. No file changes beyond a scratch script you delete.
