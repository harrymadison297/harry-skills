---
type: llm
focus: trace
weight: 1
---

At least one question is grounded in a specific finding in the code, such as the integer autoincrement ids in app/models.py (two offline devices would create colliding ids), the hard delete in app/routes.py (a deletion cannot be synced without a record of it), or the last-write-wins update.
