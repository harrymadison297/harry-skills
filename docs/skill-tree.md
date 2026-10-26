# Skill tree

The target wiring of the skills after `ask-until-clear` and `term-guard` replace the interview inside `spec-it`. Items marked *(proposed)* are not agreed yet.

```
handon                                   entry point; checks the repo, reports it, routes to the next skill; only it writes "approved"
│
├─ base (once, lazy)
│   ├─ setup                             writes the "Workflow files" block into CLAUDE.md/AGENTS.md; does nothing in an empty repo
│   └─ make-way                          creates verify-<app>; called only when prove-it-work needs it and it is missing
│
├─ A. CLARIFY ──────────────────────────  one continuous context, until gate 2
│   ask-until-clear                      interview in rounds; the first question challenges the premise
│   ├─ term-guard                        writes glossary terms and ADRs the moment they settle
│   ├─ understand-this-code              reads the code before asking
│   ├─ prototyping-designs               a question that talking cannot settle gets a throwaway build
│   └─ research                          technical facts from primary sources
│
├─ B. SPEC ─────────────────────────────
│   spec-it                              synthesizes only: journeys, numbered criteria, non-goals,
│   │                                    and HOW each journey is checked end to end
│   └─ GATE 1: you approve journeys and the e2e check
│
├─ C. ARCHITECTURE ─────────────────────
│   designing-architecture               what it touches, what it affects, how the architecture changes
│   ├─ ask-until-clear                   when a decision needs discussion
│   ├─ understand-this-code
│   ├─ term-guard                        ADRs for hard-to-reverse decisions
│   └─ GATE 2: you approve the architecture
│
│   ═══════════ from here the agent runs without stopping ═══════════
│
├─ D. SLICE (no gate) ──────────────────
│   slicing-tickets                      each ticket scenario traces back to an approved test path
│                                        (J1.1, AC3) and is never weaker than it
│
├─ E. BUILD (loop over tickets; a fresh subagent per ticket) ──
│   implementing-tickets                 TDD at the approved seams
│   ├─ delete before you add; no speculative code            (proposed)
│   ├─ machine checks: lint, types, dead code, duplicates    (proposed)
│   ├─ reviewing-changes                 fresh subagent: standards, spec, tests, places to break
│   └─ prove-it-work                     runs the real system in the environments the ticket lists
│       └─ make-way                      only when verify-<app> is missing
│
│       a parked ticket parks its dependents; independent tickets continue
│       the whole loop stops only when the stop report blames the spec or the architecture
│
├─ F. CLOSE ────────────────────────────
│   shipping-features
│   ├─ reviewing-changes                 whole-feature mode
│   ├─ a cleanup pass that fixes         (proposed)
│   ├─ prove-it-work                     every journey on the finished branch
│   ├─ quill-technical-writing           the PR body, risky tickets first, with evidence
│   └─ GATE 3: you approve the PR
│
└─ after shipping
    └─ learn-from-mistakes               turns a repeated mistake into a check in the repo
```

Used when the situation calls for it, not tied to a step:

```
debugging-failures   shares its stop rules with implementing-tickets; offers learn-from-mistakes
handoff              compresses the session when context fills; handon reads pause.md back
quill-unslop         removes patterns that read as machine-written
```
