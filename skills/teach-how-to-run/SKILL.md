---
name: teach-how-to-run
description: Write the repo's verify-<app> skill, a catalogue of the environments the real system can run in, with how to start it, drive it by its real surface, and clean up, then prove it by running one real action. Use from setup, or when verify-<app> is missing or out of date.
disable-model-invocation: true
---

# Setup verification skill

`prove-it-work` can only run the real system if something tells it how. This skill writes that, for an agent that reads it cold in the middle of a ticket and has never seen the app.

## 1. Read the repo, ask only what you cannot see

- **Surface**: what a user touches (CLI, API, browser, desktop app, library). List every surface if there are several.
- **Run**: the repo's own start command (scripts, Makefile, README), ports, env vars, seed data, auth.
- **Drive**: an existing harness first (Playwright, expect scripts, curl-able endpoints). Otherwise a generic one: browser, tmux or PTY, plain HTTP.
- **Environments**: which ones exist or the user can test in (their machine, a container, a VM, other operating systems). Ask for those you cannot observe.
- **Isolate**: whether two instances can run side by side (ports, data dirs). If not, say so in the skill, because driving a shared instance can corrupt the user's session.

If the checkout does not build or start, report why and stop. A skill written against a broken base teaches wrong steps.

## 2. Write

Write `.claude/skills/verify-<app>/SKILL.md`. It needs frontmatter (`name: verify-<app>` and a `description` naming the app and its surface), because without it the skill never registers.

One section per environment, with a name. Do not rank the environments or say when to run them: each ticket chooses its own. Each section holds:

- **Needs**: tools, a VM, an operating system, credentials.
- **Start**: the exact command, and the signal that the system is usable, not only that a process answers. It must work from an empty data dir.
- **Drive**: real commands, selectors, or requests from this repo. Prefer stable handles (ARIA labels, route paths, prompt strings) over coordinates.
- **Clean up**: stop only what you started, never by process name. Never delete `evidence/`.

State the proof rules once at the top: use the real user path, not internal setters or test-only endpoints, and check side effects (files, rows, messages) as well as what is visible. Any helper script is executable and its invocation is shown in the body.

## 3. Prove

In one environment, start the system, drive one real action, clean up, and check that the evidence still exists. If it fails, fix the skill and clean up after each failed attempt. A skill that was never run is a guess.

Mark every environment you did not run as `not yet run`. If you proved it in a stand-in (a container for a VM), list the setup steps the stand-in did that the target will not do, because those steps are still unverified.

## Running again

Update only: show the diff and apply what the user approves. Never overwrite the file wholesale.

## Done when

The file has frontmatter, every environment has Needs, Start, Drive, and Clean up, and one real action ran once.
