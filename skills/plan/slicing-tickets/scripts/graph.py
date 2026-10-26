#!/usr/bin/env python3
"""Print the ticket graph: status, review label, blockers, and which tickets are ready.

Usage: graph.py <tickets-dir>
Exits 1 on a cycle or a blocker that has no ticket file.
"""
import re
import sys
from pathlib import Path


def field(text, name):
    m = re.search(rf"^{name}:\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def load(folder):
    tickets = {}
    for path in sorted(Path(folder).glob("T*.md")):
        text = path.read_text()
        tid = re.match(r"(T\d+)", path.name).group(1)
        blockers = re.findall(r"T\d+", field(text, "Blocked by"))
        tickets[tid] = {
            "status": field(text, "Status"),
            "review": field(text, "Review"),
            "blockers": blockers,
            "title": (re.search(r"^#\s*(.*)$", text, re.M) or [None, path.stem])[1],
        }
    return tickets


def find_cycle(tickets):
    state = {}

    def visit(t, trail):
        if state.get(t) == "done":
            return None
        if state.get(t) == "open":
            return trail[trail.index(t):] + [t]
        state[t] = "open"
        for b in tickets[t]["blockers"]:
            if b in tickets and (c := visit(b, trail + [t])):
                return c
        state[t] = "done"
        return None

    for t in tickets:
        if c := visit(t, []):
            return c
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tickets = load(sys.argv[1])
    problems = []
    for tid, t in tickets.items():
        for b in t["blockers"]:
            if b not in tickets:
                problems.append(f"{tid} is blocked by {b}, which has no file")
    if cycle := find_cycle(tickets):
        problems.append("cycle: " + " -> ".join(cycle))

    for tid, t in tickets.items():
        # Ready means todo with every blocker done; computed here, stored nowhere.
        ready = t["status"] == "todo" and all(
            tickets.get(b, {}).get("status") == "done" for b in t["blockers"]
        )
        blocked = ", ".join(t["blockers"]) or "none"
        mark = "READY" if ready else ""
        print(f"{tid} [{t['status']}] review={t['review']} blocked-by={blocked} {mark}  {t['title']}")
    for p in problems:
        print("ERROR:", p, file=sys.stderr)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
