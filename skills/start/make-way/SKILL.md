---
name: make-way
description: Finds how a repo builds, runs its tests, and runs its e2e checks, runs them once, and reports what works for the user to correct. After the user confirms, writes docs/how-to-run.md so later agents can run them. Use before the first build, from setup, or when docs/how-to-run.md is missing or out of date.
disable-model-invocation: true
---

# Write the how-to-run

Later agents (`prove-it-work`, ticket subagents) read `docs/how-to-run.md` cold to build, test, and drive the real system. This skill finds what the repo already has, checks it by running it, and reports to the user. It writes the how-to only after the user has seen the report.

```
- [ ] 1 Find
- [ ] 2 Run
- [ ] 3 Report, then stop
- [ ] 4 Write
- [ ] 5 Prove
```

If `docs/how-to-run.md` already exists, follow [Running again](#running-again) instead.

## 1. Find

Read the repo's own files: package scripts, Makefile, CI workflows, compose files, test configs, README, CLAUDE.md or AGENTS.md. For each of **build**, **tests**, and **e2e**, note:

- the exact command, and where it runs (this machine, a container, CI only);
- what it needs first: tools, env vars, ports, seed data, a running server;
- for e2e: how the system is started, how to tell it is ready, how it is stopped.

E2E means driving the running system through its real surface (HTTP, CLI, browser). If nothing in the repo does that, e2e is `none found`. Never invent a command the repo does not have.

## 2. Run

Run the build and the tests once on this machine, each with a timeout. Run e2e too when what it needs is here: start the system, wait for its ready signal, run, then stop only the process you started, by its PID.

Do not install tools, change code, or fix a failure. A failure is a finding for the report.

## 3. Report, then stop

Write nothing to the repo yet. Reply in this shape:

```
Build:  <command> — passed | failed: <first error line> | not run: <why>
Tests:  <command> — <N> passed | <M> failed: <test names> | not run: <why>
E2E:    <command, and how the system is started first> — <result> | none found
Where:  this machine; CI (<workflow file>: what it runs); container; ...
Gaps:   missing tools, CI-only steps, anything only the user knows
Next:   <your questions> Anything to add or change before I write docs/how-to-run.md?
```

Then stop and wait for the user.

Go straight to step 4 only when the request already says what to add and to go ahead (for example "nothing else to add, write it"). Even then, stop after the report if the build or the tests fail: a how-to written against a broken checkout teaches wrong steps.

## 4. Write

Write `docs/how-to-run.md`, with the user's additions. Keep only what an agent needs to copy and run:

````markdown
# How to run <app>

## Build
```
<command>        # expect: <what success prints>
```

## Tests
```
<command>        # expect: <N> tests OK
```

## E2E
Needs: <tools, env vars, ports>
```
<command or script>   # expect: <what success prints>
```
Clean up: <how to stop what was started>

## Environments
- This machine: proven <date>
- CI (`<workflow file>`): not run here
````

Write a helper script only when the e2e sequence is easy to get wrong, such as start a server, wait until it is ready, run the tests, stop it. Put it in `scripts/` (or the repo's own scripts folder) and make it executable. It must:

- use a fresh data dir or file, never the user's;
- wait on a real ready signal (a health endpoint, a log line), not a fixed sleep;
- stop only the PID it started, also when the tests fail (`trap`);
- exit non-zero when a step fails.

Show the script's invocation in the how-to.

Then point to the how-to from CLAUDE.md, or AGENTS.md if that is the file the repo has. Add or update this line under `## Workflow files` (create the heading if missing) and leave the rest of the file alone:

```markdown
- Run the app: `docs/how-to-run.md`
```

## 5. Prove

Run every command in the how-to once, exactly as written. Fix the how-to or the script until each one passes, and clean up after every attempt. Leave no process running. Mark anything you could not run here (CI only, another OS) as `not run here`.

## Running again

When `docs/how-to-run.md` exists, do steps 1 and 2, then compare. Report each difference (a command that no longer exists, a new test suite, a changed port) and the edit you propose, as a diff. Stop and wait. Apply only what the user approves; never rewrite the file wholesale.

## Done when

- The user saw the report before anything was written.
- `docs/how-to-run.md` has Build, Tests, E2E (or `none found`, as the user agreed), and Environments.
- CLAUDE.md or AGENTS.md points to it.
- Every command in it ran once here, or is marked `not run here`, and nothing is left running.
