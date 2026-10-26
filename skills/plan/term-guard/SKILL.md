---
name: term-guard
description: Sharpen a project's language and record decisions as they settle, in the glossary and the ADR folder. Use when a conversation uses fuzzy or conflicting terms, when a term or a hard-to-reverse decision is settled, or when writing or editing GLOSSARY.md or an ADR.
---

# Settle the terms

The same word for two things, or two words for one thing, makes tickets, tests, and code drift apart. Fix the language while the conversation is happening, and write it down at that moment.

## Where

Read the `Workflow files` block in `CLAUDE.md` or `AGENTS.md` for the glossary and the ADR folder. Without it, use `GLOSSARY.md` and `docs/adr/` at the repo root. Create a file only when you have something to write in it.

## During the conversation

- **Challenge against the glossary.** When a term conflicts with `GLOSSARY.md`, say so now: "The glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy words.** Propose one precise term for a vague or overloaded one: "Do you mean the Customer or the User?"
- **Ask which one when a word names two things.** If the user's word could mean two different things in the code or the product (a restart after power loss and a wake from sleep, one deploy and a whole rollout), ask which. Do not choose silently.
- **Test with scenarios.** Invent a concrete case that probes an edge between two concepts, and make the user say where the boundary is.
- **Check the code.** When the user says how something works, check it. Surface a contradiction: "The code cancels a whole Order, but you said a partial cancellation is possible."
- **Write it down when it settles.** When the user names a term, add it to the glossary right then, in your own words if they gave no definition, and say so in your reply. Do not batch. See [references/glossary-format.md](references/glossary-format.md).
- **Offer an ADR rarely.** Only when all three hold: the decision is hard to reverse, it would surprise a later reader, and there was a real trade-off. Write it in one to three sentences: the context, the decision, and why. See [references/adr-format.md](references/adr-format.md).

Every glossary entry has an `_Avoid_` line, even for a term the user just coined (list the words you rejected, or the ones you expect to drift in). `GLOSSARY.md` holds language and nothing else: no implementation details, no spec, no notes.
