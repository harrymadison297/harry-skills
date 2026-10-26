# ADR format

ADRs live in the ADR folder as `0001-slug.md`, `0002-slug.md`, and so on. Take the highest number in the folder and add one.

```md
# <Short title of the decision>

<1-3 sentences: the context, what was decided, and why.>
```

An ADR can be one paragraph. Its value is recording that a decision was made and why. Add a `Status` line (`proposed | accepted | deprecated | superseded by ADR-NNNN`), `Considered options`, or `Consequences` only when they add something a reader needs.

## When to write one

All three must hold:

1. **Hard to reverse.** Changing your mind later costs something real.
2. **Surprising without context.** A later reader will ask "why did they do it this way?"
3. **A real trade-off.** There were true alternatives, and you chose for specific reasons.

If any is missing, skip it.

## What qualifies

- The shape of the architecture (a monorepo, an event-sourced write model).
- How contexts talk to each other (domain events, not synchronous HTTP).
- Technology that locks you in (database, message bus, auth provider), not every library.
- Boundaries and scope, including the explicit "no".
- A deliberate departure from the obvious path (manual SQL instead of an ORM, and why).
- Constraints not visible in the code (compliance, a partner contract).
- A rejected alternative whose rejection is not obvious.
