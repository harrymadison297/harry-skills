# GLOSSARY.md format

```md
# <Context name>

<One or two sentences: what this context is and why it exists.>

## Language

**Order**:
A request from a customer to buy something.
_Avoid_: Purchase, transaction

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

- **Be opinionated.** When several words name one concept, pick the best and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences. Say what the thing is, not what it does.
- **Only project-specific terms.** General programming words (timeout, error type) do not belong. Ask: is this concept unique to this project?
- **Group terms** under subheadings when clusters appear. Otherwise a flat list is fine.
- If `GLOSSARY-MAP.md` exists at the root, the repo has several contexts. Read it to find the right glossary, and ask when it is unclear which one applies.
