# Skills for trustable code

A set of agent skills that take a feature from an idea to a pull request you can trust. You plan the work with the agent in a few steps and approve each plan. The agent then builds it alone, one small ticket at a time, and proves that the real system works.

The plugin is named `harry-skills` (version 0.1.0). It is a work in progress.

## The problems it targets

| Problem with agent coding | What the workflow does about it |
|---|---|
| The agent assumes a lot and ignores the user journey. | `ask-until-clear` interviews you until nothing is assumed. `spec-it` writes the journeys and numbered acceptance criteria, and you approve them. |
| Architecture is not modeled, approved, or documented. | `designing-architecture` writes `architecture.md` with a code sketch, compared designs, and ADRs. You approve it before any ticket is cut. |
| Test cases are never validated. | `reviewing-changes` picks places where the code should break. The agent breaks each one and confirms that a test fails. |
| The agent writes too much code before review, so review is impossible. | `slicing-tickets` cuts the plan into small vertical tickets. Each ticket is built and reviewed in a fresh context. |
| AI slop: recreated, duplicated, and junk code. | `reviewing-changes` checks each ticket against the coding standard, and once more over the whole feature. |
| Output is not tested in a real environment. | `prove-it-work` runs the real system through a CLI, an API, or a browser, as a user would, and saves the evidence. |
| The agent runs too long and drops from its smart zone into its dumb zone. | Tickets run in fresh contexts. `handoff` compresses a session when the context fills. |

## How it works

```
A. Clarify        ask-until-clear (+ term-guard)           interview until nothing is assumed
B. Spec           spec-it                                  Gate 1: you approve journeys and the e2e check
C. Architecture   designing-architecture                   Gate 2: you approve the architecture
D. Slice          slicing-tickets                          small vertical tickets, each with an e2e scenario
E. Build          implementing-tickets, per ticket         TDD, then reviewing-changes, then prove-it-work
F. Close          shipping-features                        Gate 3: you approve the pull request
```

From gate 2 on, the agent runs without stopping. It parks a ticket and writes a stop report when three attempts fail, when a decision is yours to make, or when the next step cannot be undone.

Start with `handon`. It checks git and the files on disk, tells you where the repo stands, and routes to the next skill. Run it again to resume a half-finished feature.

## Skills

| Skill | Purpose |
|---|---|
| `handon` | Entry point. Checks the repo state, reports it, and routes to the next skill. |
| `setup` | Records where the repo keeps its glossary, standards, ADRs, and run instructions. |
| `make-way` | Writes the repo's `verify-<app>` skill, which says how to start and drive the real system. |
| `ask-until-clear` | Interviews you in rounds until nothing about a plan is left assumed. |
| `term-guard` | Writes glossary terms and ADRs as soon as they settle. |
| `understand-this-code` | Explains the code you are about to change and what a change could break. |
| `research` | Answers a technical question from primary sources, with citations. |
| `prototyping-designs` | Builds throwaway code to answer a question that talking cannot settle. |
| `spec-it` | Writes `spec.md`: journeys, acceptance criteria, non-goals, and how each journey is checked. |
| `designing-architecture` | Writes `architecture.md`: sketch, compared designs, test seams, ADRs. |
| `slicing-tickets` | Cuts the plan into vertical tickets and prints the ticket graph. |
| `implementing-tickets` | Builds one ticket with TDD in a fresh context. |
| `reviewing-changes` | Reviews a diff in a fresh subagent on standards, spec, and tests. |
| `prove-it-work` | Runs the real system and reports `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`. |
| `shipping-features` | Reviews the whole feature, writes the PR body, and tags the evidence. |
| `learn-from-mistakes` | Turns a mistake made twice into a check in the repo. |
| `debugging-failures` | Builds a loop that fails on demand before it forms a theory. |
| `handoff` | Compresses the session into a document for a fresh context. |
| `quill-technical-writing` | Writing standard for docs, commit messages, and PR bodies. |
| `quill-unslop` | Removes patterns that read as machine-written. |

Most skills set `disable-model-invocation`, so you start them by name or through `handon`.

## Install

The plugin manifest is [.claude-plugin/plugin.json](.claude-plugin/plugin.json). To try it from a local clone:

```
claude --plugin-dir /path/to/skills
```

Skills are then available as `harry-skills:<skill>`, for example `/harry-skills:handon`.

## Documentation

| Page | Content |
|---|---|
| [docs/skill-tree.md](docs/skill-tree.md) | The target wiring: which skill calls which. |
| [docs/workflow.md](docs/workflow.md) | Each step, its skills, the gates, the ticket format, and the folder layout. |
| [docs/session-model.md](docs/session-model.md) | How sessions and contexts are split across the steps. |
| [docs/sources.md](docs/sources.md) | Where each skill's content came from, with licenses. |

`docs/skill-tree.md` is the newer design. Where `docs/workflow.md` differs, for example in what gate 3 approves, the skill tree wins.

## Evals

Test cases live in [evals/](evals/), outside the skill folders, so a subagent that reads a skill never sees its tests. They cover `ask-until-clear`, `term-guard`, and `spec-it`. See [evals/README.md](evals/README.md) for how to run them blind and for the last results.

## Credits

`ask-until-clear` and `term-guard` are adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). See [docs/sources.md](docs/sources.md).
