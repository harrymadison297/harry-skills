---
name: research
description: Answer a technical question from primary sources (official docs, specs, source code, changelogs) and save the answer with citations. Use when a decision depends on an API, library, protocol, or platform fact that must not come from memory.
disable-model-invocation: true
---

# Research

An agent that answers from memory can state a wrong API fact with confidence. A cited note lets the user check the source.

## Process

1. **State the question** so one note answers it. Split a broad question into several notes.
2. **Use primary sources only.** Official docs, specifications, the library's source, release notes, and issue trackers of the project itself. A blog post or a forum answer may point you to a primary source, but never counts as one.
3. **Check the version.** Note the version of the thing you read and the version the repo uses. A fact true for another major version is a wrong fact.
4. **Run what you can.** If a few lines of code settle the claim, run them and quote the output. Running beats reading.
5. **Write** `docs/features/<feature>/research/<slug>.md`:

```
# <question>
## Answer        (2 to 5 sentences)
## Evidence      (each claim, with a link or file:line, and the version)
## Not verified  (what you could not confirm)
```

If the work is long, run it as a background agent and keep going.

## Done when

Every claim in `Answer` has a cited source, and `Not verified` lists the rest honestly.
