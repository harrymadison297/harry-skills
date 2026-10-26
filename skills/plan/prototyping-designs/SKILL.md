---
name: prototyping-designs
description: Build throwaway code to answer one design question that talking cannot settle, such as whether a state model or a UI layout feels right. Use when a spec or design question needs something running.
disable-model-invocation: true
---

# Prototype

Some questions cannot be settled on paper. A prototype settles them cheaply and leaves no code that someone might ship by accident.

## Process

1. **Write the question** in one sentence, and what answer would change the spec. If no answer would change anything, do not build.
2. **Pick the form.** Logic or state: a small terminal program the user can drive. UI: one page with two or three variants side by side.
3. **Build the least that answers it.** Work in a scratch directory outside the source tree. Skip tests, error handling, and structure. Speed is the point.
4. **Run it with the user.** Let them use it, and watch what they do, not only what they say.
5. **Record the decision** in the `Decisions` section of `spec.md`: the question, the answer, and the one thing the prototype showed that surprised you.
6. **Delete the code.** Keep only the decision, so nothing from the prototype leaks into the build.

## Done when

The question has an answer in `spec.md`, and the prototype directory is gone.
