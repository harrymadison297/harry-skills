---
name: ask-until-clear
description: Interview the user in rounds until nothing about a plan, idea, or decision is left assumed. Use when the user wants to stress-test a plan or brainstorm, or when another skill needs answers that only the user can give.
---

# Ask until clear

An agent that does not ask will assume, and it will assume the wrong thing. Interview until you and the user share one understanding, and nothing is left silently assumed.

## Process

1. **Read before you ask.** Read the code and docs that the idea touches. Never ask the user for something you can look up. Send a subagent for longer lookups, and do not wait for it: ask the questions that do not depend on it now.
2. **Say it back in a few lines.** State the goal, the user, and the problem as you understand them, then list what you found in the project as short bullets. The user corrects what is wrong. A stated guess is cheaper to fix than an open question.
3. **Map the decisions as a tree.** Every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are already settled. A question waits only if it makes no sense without another answer. A decision that the code forces on you (how things are identified, what a deletion means, what happens on failure) is on the frontier now, so ask it in round 1.
4. **Ask the frontier in one round of at most seven questions.** Put the question that blocks the most others first. Make the first one a challenge to the premise, written so that your recommendation is "yes": "Is X worth building, instead of just leaving things as they are or doing Y?" Ask whether the problem is worth solving, not which solution to pick. Put every dependency between decisions in a hold-back list, each item with the answer it waits for, and never tell the user to answer in a certain order.
5. **One decision per question, written so that "yes" accepts it.** If a sentence needs "and" or "or" to join two asks, split it or drop one. Phrase it as a proposal ("Should sync work only for notes in v1?"), not as "which" or "how many". Name the file or fact it rests on inside the question. Give your recommended answer under it:

```
❓ **Q2** - **Deletes**: `app/routes.py` deletes the row outright, so an offline device cannot tell "deleted" from "never existed". Should a delete sync to the other device?

➡️ Yes. A delete wins over an older edit, and a newer edit brings the note back.
```

6. **Recommend a choice, not a design.** A recommendation picks scope or behaviour. Leave components, protocols, schemas, and ports to the architecture step, and name a product or a number only if the project's files already use it. For a fact only the user knows, state the assumption you will work with ("I will assume an iPhone") so that "yes" accepts it, and never present a guess about their life as advice.
7. **Recompute the frontier** after each round. Settled decisions unblock the questions that waited.
8. **Settle language as it happens.** When a term or a hard-to-reverse decision is settled, run `term-guard`. Route what talking cannot settle: a question that needs something running goes to `prototyping-designs`, a technical fact goes to `research`.

## Done when

The frontier is empty, and the user confirms that you share one understanding. Do not act on it before that.
