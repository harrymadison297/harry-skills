---
name: handoff
description: Compress the current session into a short handoff document so a fresh context can continue. Use after a gate when the context is over half full, or when the user wants to stop and resume later.
disable-model-invocation: true
---

# Pause

Steps 1 to 3 share one context, so it fills up. The next step should start from the files, not from the conversation.

## Process

1. **Point, do not copy.** Anything already in a file (spec, architecture, tickets, ADRs, research) is referenced by path. Copying it creates a second version that drifts.
2. **Write** `docs/features/<feature>/pause.md`, under 40 lines:
   - Goal, in one or two sentences.
   - Where we are: the current step, and which gates passed.
   - Decisions made in conversation that no file records yet. Record those in their files now if you can; list the rest here.
   - Open questions and what each one blocks.
   - Next action: the exact skill to run next.
   - Paths of every file that matters.
3. **Tell the user** to start a new session and run `build-a-feature`. `build-a-feature` reads `pause.md` first, then deletes it.

## Done when

A new session that reads only `pause.md` and the files it lists can continue with no question the old session could have answered.
