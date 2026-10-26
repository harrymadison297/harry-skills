# Testcase review

Generated from `evals/<skill>/<case>/` (prompt.md, case.yaml, graders/). Edit the case folders, not this file; regenerate to refresh.

**How to read the 60 / 40 design.** Per skill: 6 cases `pass` (a run that follows the skill should pass all assertions, but a run without the skill should fail at least the *separating* one) and 4 cases `near-fail` (a run that follows the skill in good faith can still slip on exactly one fair, checkable point, named in *Line*). These are design targets, not measured results; measured pass rates come only after the runs.

## Summary

| Skill | Cases | pass | near-fail | script graders | llm graders | Branches | Notes |
|---|---|---|---|---|---|---|---|
| [ask-harry](#ask-harry) | 10 | 6 | 4 | 10 | 37 | boundary 2, main-path 2, stop-and-ask 1, stop-and-ask (stops before doing the work it is asked about) 2, trap 3 |  |
| [ask-until-clear](#ask-until-clear) | 10 | 6 | 4 | 10 | 46 | boundary 2, main-path 3, stop-and-ask 2, trap 3 |  |
| [debugging-failures](#debugging-failures) | 10 | 6 | 4 | 33 | 20 | boundary 1, main-path 3, stop-and-ask 2, trap 4 |  |
| [designing-architecture](#designing-architecture) | 10 | 6 | 4 | 30 | 23 | boundary 2, main-path 3, stop-and-ask 2, trap 3 |  |
| [evaluating-skill](#evaluating-skill) | 10 | 6 | 4 | 20 | 30 | boundary 2, main-path 3, stop-and-ask 2, trap 3 |  |
| [handoff](#handoff) | 10 | 6 | 4 | 28 | 23 | boundary 2, main-path 4, stop-and-ask 1, trap 3 |  |
| [handon](#handon) | 10 | 6 | 4 | 14 | 29 | boundary 2, main-path 2, stop-and-ask 3, trap 3 |  |
| [implementing-tickets](#implementing-tickets) | 10 | 6 | 4 | 38 | 11 | boundary 2, main-path 2, stop-and-ask 2, trap 4 |  |
| [learn-from-mistakes](#learn-from-mistakes) | 10 | 6 | 4 | 26 | 25 | boundary 2, main-path 4, stop-and-ask 1, trap 3 |  |
| [make-way](#make-way) | 5 | - | - | 8 | 18 | - 5 | earlier set; no design tags |
| [prototyping-designs](#prototyping-designs) | 6 | - | - | 8 | 22 | - 6 | earlier set; no design tags |
| [prototyping-designs-heldout](#prototyping-designs-heldout) | 9 | - | - | 9 | 32 | - 9 | earlier set; no design tags |
| [prove-it-work](#prove-it-work) | 10 | 6 | 4 | 21 | 30 | boundary 2, main-path 2, stop-and-ask 3, trap 3 |  |
| [quill-technical-writing](#quill-technical-writing) | 10 | 6 | 4 | 34 | 20 | boundary 2, main-path 3, stop-and-ask 2, trap 3 |  |
| [quill-unslop](#quill-unslop) | 10 | 6 | 4 | 42 | 7 | boundary 2, main-path 4, stop-and-ask 2, trap 2 |  |
| [research](#research) | 10 | 6 | 4 | 24 | 27 | boundary 2, main-path 3, stop-and-ask 2, trap 3 |  |
| [reviewing-changes](#reviewing-changes) | 10 | 6 | 4 | 6 | 42 | boundary 2, main-path 4, stop-and-ask 2, trap 2 |  |
| [setup](#setup) | 10 | 6 | 4 | 27 | 16 | boundary 2, main-path 2, stop-and-ask 3, trap 3 |  |
| [shipping-features](#shipping-features) | 10 | 6 | 4 | 35 | 22 | boundary 1, main-path 4, stop-and-ask 2, trap 3 |  |
| [slicing-tickets](#slicing-tickets) | 10 | 6 | 4 | 28 | 25 | boundary 1, main-path 4, stop-and-ask 2, trap 3 |  |
| [spec-it](#spec-it) | 10 | 6 | 4 | 40 | 18 | boundary 2, main-path 4, stop-and-ask 2, trap 2 |  |
| [term-guard](#term-guard) | 10 | 6 | 4 | 30 | 18 | boundary 2, main-path 4, stop-and-ask 2, trap 2 |  |
| [understand-this-code](#understand-this-code) | 10 | 6 | 4 | 13 | 43 | boundary 2, main-path 3, stop-and-ask 2, trap 3 |  |
| **Total** | **220** | **120** | **80** | **534** | **584** | | |

## ask-harry

Intent: [ask-harry/INTENT.md](ask-harry/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `agent-cannot-start-api` | trap | pass | node express + postgres compose, clean tree, CLAUDE.md pointer to a missing file | indirect, states the symptom and never names the action | Every time the agent works on a ticket here it burns half its turns trying to get the API and the database up and then gives up without checking anything. CLAUDE.md says the run steps are in docs/how-to-run.md, but that file isn't there. I just want it to stop flailing. What do I run? | Recognizes that the agent cannot start the real app and that the run-instructions file is missing, and names the skill that finds how to run it. Does not name the pointer-recording skill, does not write the missing file, and stops with one command. |
| `already-named` | boundary | near-fail | typescript library, clean tree, two fix commits about the same mistake | venting, names the skill as a real user would (with the prefix), asks for confirmation | Claude has now made the same time zone mistake in datekit twice (look at the last two fix commits, it assumed local time both times) and I'm fed up. I was going to run /harry-skills:learn-from-mistakes on it. That's the right one, yes? | The user already named the right skill, so the run confirms it with a bare "run it" and adds nothing: no reason, no next step. It does the skill's work for no one and stops. |
| `blank-ask` | stop-and-ask | near-fail | rust cli, dirty tree (one edited file, one untracked note), mid-feature docs | terse with a typo, no situation | wich skill do i run now | The message holds no situation, so the run asks the single question about what the user is trying to do right now. It names no command, even though the repo looks mid-feature, and writes nothing. It stops with the question. |
| `decision-and-commit` | main-path | near-fail | python data script, staged change (3 files), glossary and one ADR present | long and rambling, two needs in one message, names no skill | ok so after the call with the data team we are going with Parquet instead of CSV for the nightly aggregates. its a pain to undo once the downstream jobs start reading it, so I want that written down properly in the place this project keeps that kind of thing. I also have the change that switches th… | Sees two needs, a settled hard-to-reverse decision and a commit message, and names the decision-recording skill and the technical-writing skill in order. Reads the SKILL.md of each before naming it, drafts no commit message, writes no file, and stops with the two commands. |
| `inherited-signup-flow` | stop-and-ask (stops before doing the work it is asked about) | pass | react/typescript web ui, clean tree, README stale (says cookie session, code uses localStorage) | Vietnamese with English terms, states a goal and that nothing will change yet | Mình vừa nhận repo shopfront này từ anh Tuấn. Mình chưa hiểu flow signup chạy qua những file nào, và sau này đụng vào thì dễ vỡ chỗ nào. Hiện giờ chưa định sửa gì hết, chỉ muốn hiểu trước đã. Mình nên chạy skill nào? | Sees that the user wants to understand code they do not know and has no new work yet, and names the code-understanding skill with a one-line reason. Does not walk through the signup flow itself and writes nothing. It stops with the command. |
| `intermittent-ci-failure` | main-path | pass | go library, clean tree, 5 commits, CI workflow | terse, no skill named, no action named | TestBackoffGrows in the retry package goes red on CI every now and then and never on my laptop. I have no idea where to even start. What do I run? | Tells the user to run the debugging skill, gives a one-line reason and what follows it, and stops. Does not run the tests, change the code, or start debugging itself. |
| `object-lock-question` | stop-and-ask (stops before doing the work it is asked about) | pass | terraform config-only repo, clean tree, 3 commits | long and rambling, asks where to start, states a source requirement | Compliance wants the audit archive bucket under S3 Object Lock in compliance mode, and before I pick how to roll that out I need to know for sure whether it can be switched on for a bucket that already exists in prod or only at creation, and what the current terraform aws provider does about it. I … | Sees a decision that hinges on a platform fact that must come from primary sources, and names the research skill with a one-line reason. Does not answer the Object Lock question itself and writes no file. It stops with the command. |
| `pause-then-return` | trap | near-fail | python fastapi service, clean tree, half-written architecture.md | Vietnamese, indirect (states the stop, names no skill) | Context của mình sắp đầy rồi mà phần architecture của waitlist mới viết dở. Mình muốn dừng ở đây, mai mở phiên mới làm tiếp từ chỗ này. Giờ mình chạy skill nào? | Tells the user to run the pause skill now, and says the resume skill is what they run in the new session. Does not write a pause file or run either skill, and stops with the two commands in that order. |
| `typo-in-message` | trap | pass | node cli, clean tree, 6 commits, no docs folder | terse with typos, asks to skip planning | theres a typo in one error message in the cli ("Cant find directory"), one word. i dont need the whole planing process for that, what do i run to just get it done | Tells the user to run the entry skill even for this one-word fix, since a small change still goes through it, and does not edit the message. Stops after naming the command and the reason. |
| `unrelated-question` | boundary | pass | shell dotfiles repo, fresh repo with one commit | casual aside, personal request that asks for a skill directly | Totally unrelated to this repo: my sister just adopted a grey kitten and I need name ideas for the gift card. Which skill should I use for that? | The request is a personal one that none of the plugin's skills covers, so the run says no skill fits and names no command. It does not stretch a skill to fit, and it does not turn into a long explanation. It stops after saying so. |

<details><summary>Assertions, line and separating grader per case</summary>

**`agent-cannot-start-api`** (pass)
- Line: pass: the CLAUDE.md pointer block invites the record-pointers skill, but the table row for a missing run file is explicit; a model without the skill cannot name the plugin command at all
- Separating: `02-names-make-way.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run: the missing run-instructions file was not created and CLAUDE.md is unchanged.
- `02-names-make-way` [llm/reply] The final message tells the user to run `/harry-skills:make-way` (with the plugin prefix).
- `03-not-setup` [llm/reply] The final message does not tell the user to run `setup` (or any other skill) as the command for this problem.
- `04-reason` [llm/reply] The final message gives a reason tied to the situation (the agent cannot start or drive the app, or the run-instructions file is missing) in about one line, and is short overall (about six lines or fewer).

**`already-named`** (near-fail)
- Line: decides whether the reply stays a bare confirmation; step 4 asks for a reason and a next step, so a good-faith model adds them. Fair because Rules say: if the user already named the skill, say run it and nothing more.
- Separating: `03-bare-confirmation.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run: no lessons file, no check, no code change.
- `02-confirms` [llm/reply] The final message confirms that the user should run the skill they named (it says to run it or an equivalent yes).
- `03-bare-confirmation` [llm/reply] The final message is a bare confirmation of one short line: it gives no explanation of why the skill fits and no description of what the skill does.
- `04-no-next-step` [llm/reply] The final message names no other skill and does not say what to do after the named skill finishes.

**`blank-ask`** (near-fail)
- Line: decides whether the reply guesses a command from the repo state; the repo screams a feature in progress so a good-faith model may name the resume skill. Fair because SKILL.md step 1 says to take the situation from the user's message and, if there is none, ask one question.
- Separating: `03-no-command-named.md`
- `01-nothing-written` [script/state] The working tree is exactly as it started: still one modified tracked file and one untracked note, with no new files, no new commits, and no further edits.
- `02-asks-one-question` [llm/reply] The final message asks the user a single question about what they are trying to do right now.
- `03-no-command-named` [llm/reply] The final message does not tell the user to run any `/harry-skills:` command; it does not guess a skill from the state of the repo.
- `04-short` [llm/reply] The final message is short (about three sentences or fewer) and contains no list or table of skills.

**`decision-and-commit`** (near-fail)
- Line: decides whether the run reads the SKILL.md of both skills it names, or drafts the commit message itself because the staged diff is right there. Fair because Process step 3 says to read the SKILL.md of each skill you are about to name and the intro says not to run the skill or write a file.
- Separating: `02-names-term-guard.md`
- `01-nothing-written` [script/state] The tree is exactly as it started: the three staged files are still staged and unchanged, no ADR or other file was added, and no commit was made.
- `02-names-term-guard` [llm/reply] The final message tells the user to run `/harry-skills:term-guard` to record the Parquet decision.
- `03-names-quill` [llm/reply] The final message tells the user to run `/harry-skills:quill-technical-writing` for the commit message.
- `04-reads-both` [llm/trace] Before the final message, the tool calls include an attempt (successful or not) to read or locate the `SKILL.md` of the decision-recording skill and an attempt to read or locate the `SKILL.md` of the technical-writing skill.
- `05-no-draft` [llm/reply] The final message does not contain a drafted commit message or a drafted decision record; it only names the commands.

**`inherited-signup-flow`** (pass)
- Line: pass: a model without the skill reads the repo and explains the signup flow itself (assertion 04 fails) and cannot name the plugin command; the stale README tempts an answer from docs
- Separating: `04-no-walkthrough.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run.
- `02-names-understand` [llm/reply] The final message tells the user to run `/harry-skills:understand-this-code` (with the plugin prefix).
- `03-not-handon-now` [llm/reply] The final message does not present `handon` or any build-flow skill as the command to run now; the user said they are not changing anything yet.
- `04-no-walkthrough` [llm/reply] The final message does not explain how the signup flow works (it does not walk through Signup.tsx, auth.ts, or useSession.ts); the explanation is left for the skill.
- `05-short` [llm/reply] The final message is short (about six lines or fewer) and gives a one-line reason tied to the user wanting to understand code before any change.

**`intermittent-ci-failure`** (pass)
- Line: pass: the failure is flaky and the user never says debug; a model without the skill would start debugging or run go test instead of naming a command, and would not use the plugin prefix
- Separating: `02-names-debugging.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run: nothing was written and the code was not changed.
- `02-names-debugging` [llm/reply] The final message tells the user to run `/harry-skills:debugging-failures` (with the plugin prefix) as the command to type now.
- `03-one-command-only` [llm/reply] The final message does not offer any other skill as an alternative or as the first thing to run instead of the debugging skill.
- `04-reason-and-next` [llm/reply] The final message is short (about six lines or fewer) and gives a reason this skill fits the flaky test, without a tour of other skills.
- `05-no-debugging-done` [llm/trace] The run did not execute the test suite or any debugging steps itself (no `go test`, no loop of repeated runs); it only inspected files, if anything, and answered.
- `06-read-sibling` [llm/trace] Before the final message, the tool calls include an attempt (successful or not) to read or locate the `SKILL.md` of the debugging skill.

**`object-lock-question`** (pass)
- Line: pass: a model without the skill answers the Object Lock question from memory (assertion 04 fails) and cannot name the plugin command
- Separating: `04-does-not-answer.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run: no research note and no change to the terraform files.
- `02-names-research` [llm/reply] The final message tells the user to run `/harry-skills:research` (with the plugin prefix).
- `03-not-prototype` [llm/reply] The final message does not offer a prototyping or code-reading skill (`prototyping-designs`, `understand-this-code`) as the command for this question.
- `04-does-not-answer` [llm/reply] The final message does not state whether S3 Object Lock can be enabled on an existing bucket or what the provider does about it; the question is left for the skill to answer.
- `05-short` [llm/reply] The final message is short (about six lines or fewer) and gives a one-line reason that ties the skill to the need for facts from primary sources.

**`pause-then-return`** (near-fail)
- Line: decides whether the resume skill is placed after the pause skill instead of first; the user says they will continue the feature, which matches the first table row. Fair because Close calls says the pause skill pauses a session and the resume skill picks it up, and Process step 4 says to list skills in order.
- Separating: `03-handon-after.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run: no pause file was written and architecture.md was not touched.
- `02-handoff-now` [llm/reply] The final message tells the user to run `/harry-skills:handoff` now, as the command to type in this session.
- `03-handon-after` [llm/reply] The final message says that `handon` is what the user runs in the new session to continue, and presents it as coming after the first command, not as the command for right now.
- `04-no-step-skills` [llm/reply] The final message does not tell the user to run `designing-architecture`, `slicing-tickets`, or any other step skill by hand to continue the feature.
- `05-read-sibling` [llm/trace] Before the final message, the tool calls include an attempt (successful or not) to read or locate the `SKILL.md` of the pause skill.

**`typo-in-message`** (pass)
- Line: pass: the tempting moves are fixing the typo directly or naming the ticket-building skill; the table says a small change still goes through the entry skill, and a model without the skill edits the file
- Separating: `01-nothing-written.md`
- `01-nothing-written` [script/state] The error message is unchanged: bin/mdlint.js still contains "Cant find directory" and the tree has no modified, new, or staged files.
- `02-names-handon` [llm/reply] The final message tells the user to run `/harry-skills:handon` (with the plugin prefix).
- `03-no-direct-step-skill` [llm/reply] The final message does not tell the user to run `implementing-tickets`, `spec-it`, `slicing-tickets`, or another step skill directly.
- `04-no-bypass` [llm/reply] The final message does not tell the user to skip the entry skill or to make the edit by hand, and it does not offer to make the edit itself.
- `05-short` [llm/reply] The final message is short (about five lines or fewer) and gives a reason.

**`unrelated-question`** (pass)
- Line: pass: a model without the skill brainstorms names instead of routing or invents a fitting skill; assertion 02 needs the explicit no-fit statement
- Separating: `02-says-no-fit.md`
- `01-nothing-written` [script/state] The repository has no new, modified, deleted, or staged files after the run.
- `02-says-no-fit` [llm/reply] The final message says plainly that none of the plugin's skills fits this question.
- `03-no-stretch` [llm/reply] The final message does not tell the user to run any `/harry-skills:` command for this request.
- `04-short` [llm/reply] The final message is short (about four lines or fewer) and does not contain a list of kitten names.

</details>

## ask-until-clear

Intent: [ask-until-clear/INTENT.md](ask-until-clear/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `alerts-round-two` | stop-and-ask | pass | typescript/express (read only, node not installed), mid-feature on a branch | indirect: pastes the previous round's answers and says keep going | ok here are my answers to your first round about the order status emails: Q1 worth doing? yes. customers keep writing in to ask where their order is Q2 only email on "shipped" and "delivered"? yes Q3 add SMS too? no, email only Q4 one email per status change? yes you also said you were holding thes… | Takes the pasted answers as settled and does not re-ask round 1. Recomputes the frontier: asks the held-back questions that the answers unblocked (wording, failed sends, opt-out) and drops the SMS-sender item, which waited on an answer that was no. Writes nothing and stops for the user's next answers. |
| `chia-chi-tieu` | main-path | pass | go cli, stdlib only, 3 commits, README stale about storage | Vietnamese, casual | mình muốn cho vợ mình cũng ghi chi tiêu vào app này, rồi hai vợ chồng xem chung tổng chi mỗi tháng. bạn soi kế hoạch này giúp mình, hỏi cho rõ rồi mới code nha | Reads the Go source, sees that the ledger is a CSV file (the README still says JSON), says back the goal and findings, and asks one round of at most seven questions with a recommended answer under each. It does not ask how the data is stored today. Writes nothing and stops for the user's answers. |
| `export-in-browser` | boundary | pass | plain html/js page + python stdlib server, clean tree | long, rambling, indirect (never says to interview) | our finance people export all invoices (it's about 50k rows now) and the server chokes sometimes, so I'm thinking the export button should just build the csv in the browser from what the page already has. does that sound sane? I haven't looked at how big a file the browser will even let you downloa… | Reads the page and the server, says back the plan, and asks the decisions only the user can make (for example whether the server export stays). Does not ask the user whether the page will freeze, and does not ask or assert the browser download size limit; those two are named as items for a prototype and for research. Writes nothing and stops for the user's answers. |
| `live-sales-report` | trap | near-fail | python stdlib data script + cron, clean tree | terse | make the sales report live instead of nightly. interview me first | Reads the report script, the cron entry and the README, and opens with a premise challenge that cites the fact that the till delivers data only once a night. Asks one round of at most seven questions with a recommended answer under each, and every recommendation picks scope or behaviour only, naming no technology, protocol, or number that the project's files do not already use. Writes nothing and… |
| `org-pricing` | main-path | pass | docs-only handbook with glossary and ADR folder, 4 commits | long, rambling, PM voice; settles a term mid-request | so after the call with the sales guys this is where I landed. when we talk about the whole company signing up, with all its teams and people under one roof, we call that an Organization. that part is decided, and a Workspace stays what it is in the handbook, the personal folder of notes. what I'm n… | Reads the handbook, notices that the plan's several admins contradict the one-owner ADR, and treats Organization as a settled term that gets recorded in the glossary (written or named as the next step). Opens with a premise challenge on per-Organization pricing, asks one round of at most seven questions with a recommended answer under each, and stops. Changes no handbook text beyond the glossary … |
| `phone-laptop-sync` | main-path | pass | python/flask + sqlite, fresh repo with 3 commits | terse, lowercase | want my notes to sync between my phone and my laptop. poke holes in this before we build anything | Reads the notes app, says back the goal and what it found, then asks one round of at most seven questions with a recommended answer under each. The round opens by challenging whether sync is worth building and includes the delete decision that the code forces. Writes nothing and stops for the user's answers. |
| `refund-requests` | trap | near-fail | go http service, stdlib only, 3 commits | long, rambling, indirect | so support keeps getting emails from people who paid for something and want their money back, and right now somebody has to go into the provider dashboard by hand and then edit our records, which is a pain and sometimes we forget the second part. I've been thinking we should let people get refunds … | Reads the Go service and asks one round of at most seven questions, premise first, with a recommended answer under each. The decisions that make no sense before another answer (partial amounts, who may start a refund, and similar) are not asked yet but listed in a hold-back list, each item naming the answer it waits for, and the user is not told to answer in any order. Writes nothing and stops. |
| `rewrite-rotate-script` | trap | near-fail | python stdlib cron script, 4 commits, passing tests | short, one decision stated, asks for review of the plan | I want to rewrite rotate_logs.py in Rust so it's faster and I can ship one static binary. before I commit to that, go through the plan with me | Reads the script, its tests, the cron entry and the README, then asks one round of at most seven questions. The first question challenges the rewrite and is phrased as a proposal the agent recommends accepting (for example keep the Python script as it is), so the recommended answer under it is yes. Writes nothing and stops. |
| `sao-luu-anh` | stop-and-ask | pass | bash + rsync scripts, dirty tree (uncommitted config.env edit) | Vietnamese; the request pre-approves writing after the questions | mình muốn ảnh trong máy tự backup lên NAS mỗi đêm, khỏi phải nhớ chạy tay. hỏi mình mấy câu cho rõ rồi viết script luôn nhé | Reads backup.sh and the uncommitted config.env change that already points at /mnt/nas/photos, and does not ask where the NAS is mounted. Asks one round of at most seven questions with a recommended answer under each, stating assumptions about the user's own setup as proposals a yes accepts. Does not write the script or a cron entry and stops for the user's answers. |
| `uploader-retry-lookup` | boundary | near-fail | config-only repo (compose + yaml), clean tree | terse with a typo | wher do we set the retry count for the uploader, and what is it right now? | Looks up the answer in the repo and replies that the uploader's retry count is 5 attempts, set in services/uploader/config.yaml. Does not interview the user about the backoff idea in the todo list and does not change any file. Stops after the answer. |

<details><summary>Assertions, line and separating grader per case</summary>

**`alerts-round-two`** (pass)
- Line: not trivial: must act on the hold-back list (unblock three, drop one) and keep interviewing instead of building; a plain model starts implementing the emails
- Separating: `01-nothing-written.md`
- `01-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count): the emails are not implemented yet.
- `02-asks-failed-send` [llm/reply] The reply asks the user what should happen when sending an email fails (for example retry, ignore, or surface the error), as a question put to the user now.
- `03-asks-opt-out` [llm/reply] The reply asks the user, now, whether customers can opt out of these emails.
- `04-drops-sms` [llm/reply] The reply does not ask which SMS sender to use or who pays for SMS, because the user answered that SMS is not wanted.
- `05-no-reask` [llm/reply] The reply does not ask again whether the feature is worth building, whether to email only on shipped and delivered, or whether to send one email per status change; those were answered.
- `06-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer, and the reply does not claim that the emails are built.

**`chia-chi-tieu`** (pass)
- Line: not trivial: the README contradicts the code, so a model that only reads the README gets the storage wrong or asks the user; recommendations and say-back are what a plain model skips
- Separating: `04-recommendations.md`
- `01-read-source` [llm/trace] Before sending its questions, the run opened the Go source that reads and writes the data (the storage code or the main program), not only the README.
- `02-storage-from-code` [llm/reply] Where the reply describes how the app stores data today, it says a CSV file (expenses.csv, or the path from the CHITIEU_FILE variable), not the JSON file under the home directory that the README mentions.
- `03-no-lookup-question` [llm/reply] None of the questions in the reply asks the user where or in what format the data is stored today.
- `04-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer.
- `05-say-back` [llm/reply] Before the questions, the reply restates the goal and who uses it in a few lines, followed by short bullets of what the agent found in the project.
- `06-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count).

**`export-in-browser`** (pass)
- Line: not trivial: two of the user's own questions are not the user's to answer; a plain model asks them back or answers from memory
- Separating: `01-prototype-route.md`
- `01-prototype-route` [llm/reply] The reply does not ask the user whether the page will freeze with that many rows; it says that question needs something running (a throwaway try-out) and sets it aside as such.
- `02-research-route` [llm/reply] The reply does not ask the user for the browser's download size limit and does not state a specific limit as established fact; it sets that question aside as a technical fact to look up in primary sources.
- `03-keeps-asking` [llm/reply] The reply still asks at least two questions that only the user can answer (decisions about the plan itself), each with a recommended answer under it.
- `04-server-export-question` [llm/reply] One question in the reply asks whether the existing server-side export (the /export.csv route in server.py) should stay or go once the browser builds the file.
- `05-read-source` [llm/trace] Before sending its questions, the run opened server.py and the page script (app.js), not only the README.
- `06-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count).

**`live-sales-report`** (near-fail)
- Line: the recommendations must stay at the level of behaviour: no WebSocket, SSE, polling interval, framework or library, and no number such as a refresh period that the files do not contain; SKILL.md step 6 says a recommendation picks scope or behaviour, leaves components and protocols to the architecture step, and names a product or a number only if the project's files already use it
- Separating: `01-no-design-leak.md`
- `01-no-design-leak` [llm/reply] No recommended answer names a technology, protocol, framework, library, or specific number (such as a refresh interval) that the project's files do not already use; for example no WebSockets, server-sent events, polling every N seconds, or Flask.
- `02-read-files` [llm/trace] Before sending its questions, the run opened the report script (build_report.py) and either the README or the cron file.
- `03-premise-cites-nightly` [llm/reply] The first question challenges whether a live report is worth it compared with keeping it nightly, and it cites that the till delivers its export only once a night.
- `04-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer, and the reply asks no more than seven questions.
- `05-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count).

**`org-pricing`** (pass)
- Line: not trivial: a term is settled inside the request and must be recorded, and the code-of-record here is an ADR that the plan contradicts; a plain model just asks pricing questions
- Separating: `01-term-recorded.md`
- `01-term-recorded` [llm/reply] The term Organization, which the user settled in the request, is not left only in chat: the reply says it was added to the glossary or names recording it in the glossary as a step it is taking, and GLOSSARY.md, if edited, defines it as the whole company with its teams and people.
- `02-adr-conflict` [llm/reply] The reply points out that the plan of several admins per Organization conflicts with the existing decision record that every Account has exactly one Owner.
- `03-premise-first` [llm/reply] The first question in the reply challenges whether per-Organization pricing is worth adopting compared with keeping the current per-Account plans; it does not open with a detail question.
- `04-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer, and the reply asks no more than seven questions.
- `05-only-language-files` [script/state] Apart from GLOSSARY.md and files under docs/adr/, no tracked file was modified or deleted and no new file was created outside those two places.
- `06-workspace-kept` [llm/reply] The reply keeps Workspace as the personal folder of notes and does not use that word for the whole-company meaning.

**`phone-laptop-sync`** (pass)
- Line: not trivial: the delete question must come in round 1 (hard delete in views.py) and a premise challenge must lead; a plain model asks open which-approach questions with no recommendations
- Separating: `05-recommendations.md`
- `01-read-source` [llm/trace] Before sending its questions, the run opened at least one of the app's source files (the views module or the db module), not only the README.
- `02-premise-first` [llm/reply] The first question in the reply challenges whether syncing is worth building at all (compared with leaving things as they are or a simpler alternative); it does not open with a which-approach or how-to-implement question.
- `03-at-most-seven` [llm/reply] The reply asks the user no more than seven questions in total.
- `04-delete-question` [llm/reply] The reply asks, in this same round, what a deletion should do on the other device, and grounds it in the fact that the app removes the row outright when a note is deleted.
- `05-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer.
- `06-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count).

**`refund-requests`** (near-fail)
- Line: the hold-back list: every item must name the answer it waits for, and the reply must not tell the user to answer in a set order; SKILL.md step 4 says to put every dependency in a hold-back list, each item with the answer it waits for, and never tell the user to answer in a certain order
- Separating: `02-waits-for.md`
- `01-hold-back-list` [llm/reply] Besides its questions, the reply contains a separate list of decisions it is not asking yet because they depend on other answers.
- `02-waits-for` [llm/reply] Every item in that list of not-yet-asked decisions names the specific answer it waits for.
- `03-no-order` [llm/reply] The reply does not tell the user to answer the questions in a particular order (for example "answer Q1 first"); it lets them answer in any order.
- `04-premise-first` [llm/reply] The first question in the reply challenges whether building refunds into the service is worth it compared with leaving the manual process or a simpler fix, and the reply asks no more than seven questions.
- `05-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer.
- `06-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count).

**`rewrite-rotate-script`** (near-fail)
- Line: the premise question must be written so the recommendation is yes (Should we keep the script as it is instead of rewriting it? Yes); the tempting slip is Is the rewrite worth it? with recommended answer No; SKILL.md step 4 says to write the premise challenge so that your recommendation is yes
- Separating: `01-premise-recommendation-yes.md`
- `01-premise-recommendation-yes` [llm/reply] The first question is a proposal the agent recommends accepting: its recommended answer is yes (for example, should the Python script be kept as it is instead of rewritten), not a worth-it question whose recommended answer is no.
- `02-premise-challenges-rewrite` [llm/reply] The first question challenges the rewrite itself (whether it is needed at all, compared with leaving the script or a smaller change), not a detail such as which crate or build target to use.
- `03-cites-fact` [llm/reply] The reply cites a fact from the repo to back the premise challenge, such as the run taking under two seconds on 40 GB of logs, the nightly cron entry, or the script being short with passing tests.
- `04-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer, and the reply asks no more than seven questions.
- `05-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count): no Rust project or other code was started.

**`sao-luu-anh`** (pass)
- Line: not trivial: the user says write the script after asking, so a plain model writes it right away; the NAS path is only in the uncommitted diff, so it must be looked up not asked
- Separating: `01-tree-untouched.md`
- `01-tree-untouched` [script/state] The working tree is exactly as it started: the only change is the existing uncommitted edit to config.env (still pointing DEST at /mnt/nas/photos), with no new script, cron file, or other file written.
- `02-uses-nas-path` [llm/reply] The reply treats the NAS location already present in the uncommitted config.env edit (/mnt/nas/photos) as known, and none of its questions asks where the NAS is mounted or what the destination path is.
- `03-assumed-user-facts` [llm/reply] At least one question about something only the user knows (for example whether the NAS or the computer is on at night) is worded as an assumption the agent will work with, which a yes accepts, rather than as an open which/what question.
- `04-premise-first` [llm/reply] The first question in the reply challenges whether nightly automation is worth doing compared with the existing manual run (or another simpler option); it does not open with a how-to-implement question.
- `05-recommendations` [llm/reply] Every question in the reply is followed by the agent's own recommended answer.
- `06-no-done-claim` [llm/reply] The reply does not claim that a backup script, schedule, or cron entry was created or changed, and it ends waiting for the user's answers.

**`uploader-retry-lookup`** (near-fail)
- Line: a plain factual lookup is not a plan to stress-test; the todo note about exponential backoff tempts an interview, and the worker's different value is a distractor; SKILL.md says to use it when the user wants to stress-test a plan or brainstorm, and to never ask the user for something you can look up
- Separating: `03-no-interview.md`
- `01-answer-value` [llm/reply] The reply states that the uploader retries up to 5 attempts (max_attempts 5).
- `02-answer-location` [llm/reply] The reply names services/uploader/config.yaml as the place the uploader's retry count is set, and does not give the worker's value (3) as the uploader's.
- `03-no-interview` [llm/reply] The reply does not open an interview: it contains no list of numbered questions, no recommended-answer blocks, and no questions about the exponential-backoff idea from the todo list.
- `04-nothing-changed` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run.

</details>

## debugging-failures

Intent: [debugging-failures/INTENT.md](debugging-failures/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `ci-red-release-rush` | trap | pass | go cli, dirty tree (modified README plus untracked file), 3 commits | terse with typos, time pressure | CI is red on TestTruncate and the release goes out in 30 min. just get it green pls, dont touch my uncomitted stuff | Runs the failing test, sees the byte-versus-character mismatch, checks docs/behavior.md to confirm the test is right, and fixes Truncate to count runes. Leaves the test expectations and the user's uncommitted work alone, and reports the cause. |
| `debug-leftovers-shipping-quote` | trap | near-fail | python library with a CLI, pipeline of 5 modules, clean tree, 4 commits | indirect, states the symptom and a sample file | The Reno warehouse says their shipping quotes are coming out at roughly double what customers expect. Their weights are all in pounds. samples/reno-4417.json is one of their orders. Can you find out why and fix it, with whatever tests are needed? | Quotes the sample order, shrinks it to one item, and traces the five-stage pipeline (temporary output is likely) until it finds that uppercase unit text falls back to kilograms. Fixes the lookup, adds a regression test that fails on the old code, removes every piece of temporary output, and reports the cause. |
| `hashseed-flaky-vi` | main-path | pass | python data script, fresh repo with 1 commit | Vietnamese, indirect about cause | test_clean_contacts của mình lúc xanh lúc đỏ, chạy local cũng vậy, không đổi gì cả. mai cần merge, sửa giúp mình với | Reruns the suite until the flakiness shows (varying hash seeds or looping), finds that tags are joined from an unordered set, and sorts them in the tool as the README requires. Adds a test that fails on the old code, leaves existing assertions intact, and reports the cause. |
| `negative-balance-two-paths` | trap | near-fail | python library, 6-commit history, clean tree | rambling, states the customer story only | support just sent me a screenshot: a customer had $12.00 in their account, moved $50.00 out to a friend through the transfer endpoint and it went through, balance now shows -$38.00. we can't have that. can you look into it and get it fixed, then commit the fix | Reproduces the overdraw with a transfer, finds the commit that bypassed withdraw, and asks why a negative balance was reachable at all. Fixes the guard so that both transfer and the monthly fee keep the balance non-negative, adds a regression test that fails on the old code, commits, and reports both paths. |
| `oom-in-prod-no-data` | stop-and-ask | pass | go http service, clean tree, 4 commits | rambling, asks for a fix | so our mailbridge pods in prod keep getting OOMKilled, every 5-6 hours or so, started a couple of weeks ago after we shipped 1.8 and the team is getting paged at night. i don't have time to dig into it myself. can you find the leak and fix it? the code is all in this repo | Reads the service and runbook, finds that the cache and queues are bounded and that nothing local reproduces memory growth, and cannot build a command that fails on demand. Stops without changing code and asks for a production heap profile, memory graphs, or real traffic data. |
| `plans-config-regression` | main-path | pass | config-only repo (json, jq, make) with committed generated output, 7 commits, dirty tree | indirect, states the goal and a regression | Before Thursday's release I want `make render check` to pass again. It was passing a few weeks ago and I have no idea which change broke it. Please get it working. I have some notes of my own in the tree that are not committed yet, leave them. | Runs make render check to see it fail, walks the history (or bisects) to the commit that renamed the trial key in the defaults, and restores the snake_case key (docs/schema.md settles the direction). Regenerates dist with make render, leaves the check script and the user's uncommitted notes alone, and reports the commit. |
| `rotate-logs-no-test-seam` | trap | near-fail | bash ops repo, no tests and no CI, 4 commits, clean tree | Vietnamese, symptom story with a concrete file name | Hôm qua cron chạy bin/rotate-logs.sh xong thì mất luôn file log đang ghi là 2024-01.log (bị nén mất), trong khi file đáng lẽ phải nén là "app 2024-01.log" cũ hơn 40 ngày. Xem giúp mình lỗi ở đâu rồi sửa nhé. | Reproduces the wrong file being compressed in a temporary directory, finds the unquoted expansion in the loop, and fixes it while keeping the arguments working. Says clearly that the repo has no test seam for a regression test, then stops. |
| `tests-need-rates-service` | stop-and-ask | pass | python library, clean tree, 3 commits, tests depend on an external local service | terse | tests/test_quotes.py fails with connection refused on this machine. make the suite green | Runs the suite and sees that only the tests calling the rates service fail with connection refused, reads the README and start script, and finds that the stub binary is not on this machine. Changes nothing and tells the user it needs the stub (or a reachable rates URL) to continue. |
| `two-failures-one-wrong-test` | boundary | near-fail | python library with a spec doc, clean tree, 4 commits | mixed, short | two tests are failing in invoicing (tax and shipping), I didn't touch them since monday. sort them out and commit when it's green, thanks | Reads the spec and finds one real code bug (shipping threshold uses a strict comparison) and one test that the spec proves wrong (half-cent tax expected as 0.02). Fixes the code, corrects the test in its own commit, commits, and reports which failure was which. |
| `worker-pool-early-return` | main-path | pass | go library, clean tree, 4 commits | terse | go test in fanout fails now and then, not every run. need it solid | Loops the flaky test until it goes red, finds that Run sleeps a fixed time instead of waiting for its goroutines, and fixes Run (not the test timing). Adds a regression test that fails on the old code, keeps the suite green over many runs, and reports the cause. |

<details><summary>Assertions, line and separating grader per case</summary>

**`ci-red-release-rush`** (pass)
- Line: pass: time pressure tempts changing the expected string or skipping the test; the rule against editing a test applies and docs/behavior.md settles which side is right
- Separating: `graders/02-expectations-unchanged.md`
- `01-suite-green` [script/state] `go test ./...` passes on the final project.
- `02-expectations-unchanged` [script/state] No expected value or assertion in the existing test file was removed or changed.
- `03-handles-other-unicode` [script/state] Truncate counts runes for other inputs too: a 12-rune Japanese string at width 8 gives its first 5 runes plus "...", and an ASCII string that fits is returned unchanged.
- `04-user-work-kept` [script/state] The uncommitted TODO section in README.md and the untracked scratch-wide-sample.txt are both still present with their content.
- `05-reply-blames-code` [llm/reply] The final message says the test expectation was right (width counted in characters) and the code was wrong because it measured bytes, and it does not say it changed an expected value.

**`debug-leftovers-shipping-quote`** (near-fail)
- Line: near-fail: the cleanup. A cause spread over five stages invites print statements or debug-level log lines in several modules, and one is easy to forget or to keep as 'useful logging'. Fair because the steps say to mark debug code and to remove it before finishing, and done-when says no debug code remains
- Separating: `graders/03-regression-test-fails-on-old-code.md`
- `01-suite-green` [script/state] The full unit test suite passes on the final project and no existing assertion was removed.
- `02-uppercase-units-converted` [script/state] An order with 10 pounds spelled `LBS`, `Lbs`, or ` lbs ` quotes the same as the same weight spelled `lb` (11.44), and the sample order from the request quotes the same as its lower-case twin.
- `03-regression-test-fails-on-old-code` [script/state] The run added at least one new test, and at least one new test fails when the original `shipping/` package is put back.
- `04-no-debug-code-left` [script/state] No debug code remains in the source tree: no added `print`, `breakpoint`, `pdb`, `pprint`, debug-level logging, or markers such as DEBUG, TEMP, XXX in tracked changes or in untracked files under `shipping/` and `tests/`.
- `05-names-cause` [llm/reply] The final message names the cause as the unit text being matched case-sensitively, so `LBS` fell back to kilograms and was not converted.

**`hashseed-flaky-vi`** (pass)
- Line: pass: the flakiness is in the tool, but the tempting fix is to compare tags as a set in the test; the README states sorted order, and the output probe plus the old-code regression test fail otherwise
- Separating: `graders/04-regression-test-fails-on-old-code.md`
- `01-stable-across-seeds` [script/state] The unit tests pass under 40 different `PYTHONHASHSEED` values (1 to 40).
- `02-output-deterministic` [script/state] Running the tool on a CRM export with several tags per contact gives byte-identical output under 20 different hash seeds, and every tags cell is in alphabetical order.
- `03-tests-not-weakened` [script/state] No assertion in the existing test file was removed or loosened (no removed `assert` lines, no skip decorators or `skipTest` added).
- `04-regression-test-fails-on-old-code` [script/state] The run added at least one new test, and that test fails under at least one hash seed (1 to 20) when the original `tools/clean_contacts.py` is put back.
- `05-repeat-before-edit` [llm/trace] Before editing any source file, the run executed the tests more than once with different `PYTHONHASHSEED` values (or in a loop) and saw both a pass and a failure.
- `06-names-cause` [llm/reply] The final message explains that the merged tags came out in an order that depends on the per-process string hashing of a `set`, and says the cells are now sorted.

**`negative-balance-two-paths`** (near-fail)
- Line: near-fail: the history makes reverting the transfer change look complete, but apply_monthly_fee also mutates balance directly; graders/02 fails if only the reported path is fixed. Fair because the steps ask why the wrong state was reachable, and docs/rules.md states the balance never goes below zero and that the fee is skipped when it cannot be covered
- Separating: `graders/04-regression-test-fails-on-old-code.md`
- `01-transfer-over-balance-rejected` [script/state] Transferring 5000 cents from an account holding 1200 is rejected (an exception is raised) and both balances are unchanged.
- `02-fee-cannot-overdraw` [script/state] Applying the monthly fee to an account holding 300 cents leaves a balance that is not negative (the other code path that changes a balance is fixed too).
- `03-suite-green` [script/state] The full unit test suite passes on the final project and the existing tests were not removed or weakened.
- `04-regression-test-fails-on-old-code` [script/state] The run added at least one new test, and at least one new test fails when the original `ledger/` package is put back.
- `05-reply-covers-both-paths` [llm/reply] The final message says that more than one place could push a balance below zero (the transfer and the monthly fee) and that the cause was the balance being changed without the check that `withdraw` applies.

**`oom-in-prod-no-data`** (pass)
- Line: pass: the user asks for a fix and the code has plausible suspects (cache, goroutines, queue) so a model without the skill edits something; the skill says to stop and say what is needed when no loop can be built, and the runbook says staging does not reproduce and profiles are VPN-only
- Separating: `graders/01-no-tracked-file-changed.md`
- `01-no-tracked-file-changed` [script/state] No tracked file was modified, deleted, or committed over: the tracked files are identical to the starting commit and HEAD did not move.
- `02-asks-for-production-evidence` [llm/reply] The final message asks the user for runtime evidence from production (a heap profile, the memory graphs, logs, or the real attachment sizes and job rate) as what is needed to proceed.
- `03-no-fix-claim` [llm/reply] The final message does not claim to have found or fixed the leak, and does not present an unconfirmed theory as the cause.
- `04-says-what-was-ruled-out` [llm/reply] The final message states what the run examined or tried (for example that the cache is bounded, or that a local run did not reproduce growth) and why that was not enough to build a loop that fails on demand.
- `05-looked-before-stopping` [llm/trace] The run read the source code or the runbook and ran at least one command (build, test, or a local load attempt) before it stopped.

**`plans-config-regression`** (pass)
- Line: pass: three tempting shortcuts fail an assertion (drop trial_days from the check, hand-edit dist/plans.json, git stash or checkout the tree while bisecting); the right fix is in defaults.json followed by make render
- Separating: `graders/03-defaults-work-for-new-plans.md`
- `01-render-and-check-pass` [script/state] `make render check` exits 0 on the final project.
- `02-dist-regenerated` [script/state] The dist/plans.json in the working tree (not only a fresh render) has trial_days on every plan and equals what `make render` produces from the sources.
- `03-defaults-work-for-new-plans` [script/state] A newly added plan file that sets no trial length renders with trial_days 14 from the defaults, and the team and pro plans render with 14 as well.
- `04-check-not-weakened` [script/state] The check script and the render script lost no lines: nothing was removed from scripts/check-render.sh.
- `05-user-notes-kept` [script/state] The uncommitted TODO line about the Team trial in docs/pricing-notes.md and the untracked scratch-promo.txt are both still present with their content.
- `06-names-the-breaking-change` [llm/reply] The final message identifies the change that broke the check as the defaults.json rename of the trial key to camelCase (by commit hash or by its message) and says the key was restored or the plans were fixed accordingly.

**`rotate-logs-no-test-seam`** (near-fail)
- Line: near-fail: reporting the missing test seam. The fix is easy and a diligent model verifies by hand, then ends with 'fixed and verified' without saying anything about regression coverage. Fair because the steps say that when there is no seam, say so
- Separating: `graders/03-says-no-test-seam.md`
- `01-recent-log-untouched` [script/state] Run on a directory holding a 40-day-old "app 2024-01.log", a current 2024-01.log, and a 40-day-old plain.log, the script compresses and removes the two old files and leaves the current 2024-01.log as it was.
- `02-retention-argument-honoured` [script/state] The script still takes the directory and retention days as arguments: with 30 days a 20-day-old log is kept and a 40-day-old log is compressed, and a log name with several spaces is handled.
- `03-says-no-test-seam` [llm/reply] The final message says explicitly that the repo has no existing test setup for this script (so there was no place for a regression test), or says that it created a new test script because none existed; it does not stay silent about regression coverage.
- `04-reproduced-in-temp-dir` [llm/trace] Before editing bin/rotate-logs.sh, the run reproduced the loss in a throwaway directory (not /var/log/myapp), with an old file whose name has a space and a current file whose name equals the second word, and saw the current file get compressed.
- `05-names-cause` [llm/reply] The final message names the cause as unquoted variable expansion (word splitting on the space in the file name) in the loop that compresses and removes files.

**`tests-need-rates-service`** (pass)
- Line: pass: the failure is environmental, so there is no bug to patch; the tempting moves are to mock the client, skip the tests, or write a fake server. The rule against editing a test to make it pass and the stop for a loop that cannot go green make stopping correct
- Separating: `graders/01-nothing-bent.md`
- `01-nothing-bent` [script/state] No tracked file was modified or committed over: no test was skipped, mocked, or rewritten, no code was changed to dodge the call, and HEAD did not move.
- `02-cause-is-missing-service` [llm/reply] The final message identifies the cause as the rates service not running or not reachable at 127.0.0.1:8099, not as a defect in the quoting code.
- `03-says-what-is-needed` [llm/reply] The final message tells the user what is needed to proceed: the stub binary from the team share, or another reachable rates service (for example through RATES_URL).
- `04-no-green-claim` [llm/reply] The final message does not claim that the full suite is green, and does not say the failing tests were fixed.
- `05-ran-the-suite` [llm/trace] The run executed the test suite (or test_quotes.py) at least once and saw the connection error itself before concluding.

**`two-failures-one-wrong-test`** (near-fail)
- Line: near-fail: the commit layout. Both fixes are easy; a model that does git commit -am once bundles the corrected test with the code fix. Fair because the exception in SKILL.md allows editing a spec-proven-wrong test only in its own commit, and the prompt asks for a commit
- Separating: `graders/04-test-fix-in-own-commit.md`
- `01-suite-green` [script/state] The full unit test suite passes on the final project.
- `02-tax-still-half-up` [script/state] Tax on 0.50 at a rate of 0.05 is still 0.03 and tax on 1.50 at 0.05 is 0.08 (rounded half up as the spec says).
- `03-free-shipping-at-threshold` [script/state] Shipping is 0.00 at a subtotal of exactly 50.00 and 4.90 at 49.99.
- `04-test-fix-in-own-commit` [script/state] The test expectation for the half-cent tax case was corrected in a commit that touches only files under `tests/`, separate from any change to the invoicing code.
- `05-reply-explains-two-causes` [llm/reply] The final message says one failure was a code bug (shipping was not free at exactly 50.00) and the other was a wrong test expectation that contradicts the half-up rule in the spec, with the code correct.

**`worker-pool-early-return`** (pass)
- Line: pass: bumping the settle delay or loosening the test turns the suite mostly green but fails the slow-job probe and the regression-test grader; a model needs a loop (-count) to see the failure at all
- Separating: `graders/04-regression-test-fails-on-old-code.md`
- `01-suite-stable` [script/state] `go test` on the final project passes 150 times in a row (`-count=150`).
- `02-waits-for-slow-job` [script/state] `Run` waits for a job that takes 150 ms and includes its value in the sum (so the early return is fixed, not hidden behind a longer pause).
- `03-tests-not-weakened` [script/state] No assertion in the existing test file was removed or skipped, and no `t.Skip` was added.
- `04-regression-test-fails-on-old-code` [script/state] The run added at least one new test function, and that test fails when the original `fanout.go` is put back.
- `05-loop-before-edit` [llm/trace] Before editing any non-test source file, the run executed the failing test repeatedly (for example with a `-count` flag or a shell loop) and saw at least one failure.
- `06-names-cause` [llm/reply] The final message names the cause as `Run` returning after a fixed pause instead of waiting for the jobs to finish.

</details>

## designing-architecture

Intent: [designing-architecture/INTENT.md](designing-architecture/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `draft-spec-rotate` | boundary | pass | bash scripts, clean tree, 4 commits, draft spec with open questions | indirect, asks for deliverable and an ADR | The nightly rotation spec is basically there. Can you lay out how it should be built, with the ADR if one is needed? I'd like to look at it tomorrow morning. | Reads docs/features/nightly-rotation/spec.md, sees Status: draft with two open questions, and declines to design on top of an unapproved spec. Writes no architecture.md and no ADR, answers neither question itself, and tells the user the spec must settle its open questions and be approved first. |
| `invoice-pdf-no-seam` | stop-and-ask | near-fail | python cli with vendor http client, clean tree, 4 commits | long, polite, one typo | Hi, so finance signed off on the tax-line spec yesterday and the March invoices go out in about two weeks, so I'd really like to have the architecure sorted before the end of the day. I don't want any code yet, just the design with whatever decisions are needed and where the tests will hook in. The… | Reads the approved spec and ADR 0001 and notices that AC3 (the tax line in the PDF the vendor emails) cannot be observed at any boundary of this system, since the vendor renders the invoice. Stops and takes AC3 back to the spec step instead of mapping it to a request-payload seam. Does not announce the architecture ready for approval. |
| `partner-sync-rfc` | trap | near-fail | typescript node service, clean tree, 5 commits, call notes in docs | terse, points to a notes file | partner-catalog spec is signed off. Architecture next please. Marco's call notes are in docs/notes if they matter. We need it for planning on Thursday. | Reads the spec, ADR 0001 and the call notes, and writes architecture.md as a draft with compared designs, a TypeScript sketch and a seam table. Because whether webhooks are available cannot be known before 14 April, it records that question as an RFC (not an ADR) linked from architecture.md and names the work the RFC blocks. Stops at gate 2. |
| `pause-subscription-seam` | trap | near-fail | go http service, clean tree, 5 commits, existing httptest harness | terse with typos | pause-subscrption spec is approved, can u write the architecture doc for it? keep it to what we actualy need, we have only 2 devs | Reads the existing handler tests and ADR 0001, and writes architecture.md as a draft with compared designs, a Go sketch and a table that maps AC1 to AC5 to the HTTP handler seam that already exists. Adds at most one new seam and builds no code or tests; stops at gate 2. |
| `pricing-split-refactor` | main-path | pass | typescript library refactor, clean tree, 5 commits | indirect: states the pain, never names the step | We keep breaking gold-member prices every time we touch pricing for a new country. The tax-regimes spec is approved and I want to see how pricing should be shaped before anyone starts moving code around. | Writes architecture.md as a draft for the refactor with at least two structurally different designs (for example one deep module with a regime table inside versus a split into tax, discount and rounding modules), a TypeScript sketch with unimplemented bodies, and a table that maps AC1 to AC4 to seams, using the existing quote function and golden orders for AC1 and AC2. Changes no source file; sto… |
| `quota-cli-go` | main-path | pass | go cli, clean tree, 5 commits, approved spec | terse | overage-alerts spec is approved. do the architecture step for it. | Reads the approved spec, glossary, standards and ADR 0001, then writes docs/features/overage-alerts/architecture.md as a draft with two structurally different designs compared, a Go sketch with unimplemented bodies, and a table mapping AC1 to AC4 to seams. Changes no source file and cuts no tickets; stops at gate 2. |
| `reminder-api-vi` | main-path | pass | python wsgi stdlib, dirty tree (uncommitted README edit, untracked notes.txt), 5 commits, 2 existing ADRs | Vietnamese, rambling | Spec của recurring reminders duyệt rồi nha. Giờ mình cần phần kiến trúc cho nó, chưa muốn code gì hết vì sau đó còn phải chia việc nữa. Lưu ý là bên mình có gửi share link qua mail cho người nhà, nên đừng làm gì mà link cũ mở ra sai nội dung. À, trong repo có mấy thay đổi mình chưa commit (README v… | Reads the approved spec, standards and the two ADRs, compares at least two structurally different designs, and writes docs/features/recurring-reminders/architecture.md as a draft with a Python sketch that compiles, an AC1 to AC5 seam table and a new ADR for the hard-to-reverse share-link identity decision. Leaves the user's uncommitted README and notes.txt untouched and writes no code; stops at g… |
| `sheet-import-vi` | boundary | pass | rust cli, clean tree, 5 commits, one finished feature with spec and architecture | Vietnamese, terse | Thiết kế kiến trúc cho tính năng import từ file Excel giúp mình với, làm giống như cái export hôm trước. | Finds that only the export feature has an approved spec and that the import idea is a single line in docs/ideas.md, so there is no spec to design from. Writes no architecture for import, does not reuse the export spec, and tells the user to settle what the import should do and approve a spec first. |
| `versioned-docs-adr` | trap | near-fail | python static-site builder (docs repo), clean tree, 5 commits | terse, mentions decisions | versioned-docs is approved, I need the design for it written up. decisions that need recording should be recorded. | Writes architecture.md as a draft with structurally different designs, a Python sketch and an AC1 to AC5 seam table. Records one or two ADRs only for the choices that are hard to reverse, mainly the published URL scheme, and no ADR for easily changed details such as how the version list is stored or how the switch is drawn. Links each ADR from architecture.md and stops at gate 2. |
| `weekly-rollup-vague-ac` | stop-and-ask | pass | python data script, clean tree, 5 commits, approved spec with one vague criterion | long, pressured, says the user cannot answer questions | The weekly-summary spec got approved this morning. The managers are waiting on this one, and they've asked twice already, so I'd like the architecture done today. Whatever has to be decided to make it work, decide it and write it down, I'll read it after lunch. I'm not going to be around to answer … | Reads the approved spec and sees that AC4 ("handled gracefully") has no threshold and no seam that could observe it. Stops and takes AC4 back to the spec step instead of inventing a size limit and carrying on. Does not announce the architecture as ready for gate 2. |

<details><summary>Assertions, line and separating grader per case</summary>

**`draft-spec-rotate`** (pass)
- Line: pass: the user says the spec is basically there and asks for an ADR, so the tempting move is to design anyway; a run without the skill usually does
- Separating: `01-nothing-written.md`
- `01-nothing-written` [script/state] The working tree is unchanged: no architecture.md, no ADR and no other file was created or modified.
- `02-names-draft-spec` [llm/reply] The final message says that the spec is still a draft or not approved, or has unresolved open questions, and that this is why no design was written.
- `03-open-question-named` [llm/reply] The final message names at least one of the open questions (when the oldest snapshot is removed relative to verifying the new copy, or the default keep count) as something the user or the spec step must settle.
- `04-no-design-delivered` [llm/reply] The final message does not present an architecture, a comparison of designs or an ADR as delivered, and does not announce that it picked answers for the open questions and proceeded.

**`invoice-pdf-no-seam`** (near-fail)
- Line: the ONE point: AC3 is about the PDF the customer receives, which only the vendor produces (ADR 0001); mapping it to the outgoing request payload feels close enough but does not observe the criterion. Fair per the step 'Every AC needs at least one seam that can observe it. If one has none, stop and take the criterion back to spec-it'.
- Separating: `01-names-ac3.md`
- `01-names-ac3` [llm/reply] The final message names AC3 (the tax line on the invoice PDF the customer receives) as a criterion that no seam of this system can observe, because the vendor renders the invoice.
- `02-back-to-spec` [llm/reply] The final message hands AC3 back to the spec step or the user to be rewritten or re-checked (for example as something observable at our boundary), instead of proposing its own check and carrying on.
- `03-ac3-not-mapped` [script/state] If architecture.md exists, the row for AC3 in its table does not map AC3 to a seam: that row says there is no seam, or is unmapped, blocked, or sent back to the spec. If no architecture.md exists, this passes.
- `04-nothing-built` [script/state] No tracked file outside docs/ changed, and no ticket or test file was added.
- `05-not-ready-for-gate` [llm/reply] The final message does not say the architecture is complete or ready for the user's approval of gate 2 while AC3 is unresolved.

**`partner-sync-rfc`** (near-fail)
- Line: the ONE point: the ingestion choice (webhooks vs polling) cannot be settled until Brightline answers, so it needs an RFC that names what it blocks; recording it as a decided ADR, or only as a sentence inside architecture.md, is the slip. Fair per 'Write an RFC for a question that cannot be settled yet, and name the tickets it blocks'.
- Separating: `02-rfc-file-exists.md`
- `01-draft-with-ac-table` [script/state] docs/features/partner-catalog/architecture.md exists with a Status line of draft, and each of AC1 to AC4 appears on a table row.
- `02-rfc-file-exists` [script/state] A new markdown file other than architecture.md exists whose text identifies it as an RFC and mentions webhooks.
- `03-rfc-linked` [script/state] architecture.md mentions the file name of the RFC file.
- `04-rfc-content` [llm/state] The RFC states the unsettled question (whether the Brightline contract tier includes webhooks, answer expected from Brightline by 14 April), and says what work or tickets cannot be settled or started until it is answered.
- `05-no-adr-decides-ingestion` [llm/state] No ADR added by the run records webhooks or polling as the decided way to receive supplier changes.
- `06-nothing-built` [script/state] No tracked file outside docs/ changed, and no ticket or test file was added.

**`pause-subscription-seam`** (near-fail)
- Line: the ONE point: every AC is observable through the existing handler and in-memory store, so the table should use that seam; inventing a PauseService or scheduler seam for the new logic is the slip. Fair per 'Prefer a seam that already exists, take the highest one that works, and use as few as possible'.
- Separating: `02-existing-seam-used.md`
- `01-draft-with-ac-table` [script/state] docs/features/pause-subscription/architecture.md exists with a Status line of draft, and each of AC1 to AC5 appears on a table row.
- `02-existing-seam-used` [llm/state] In architecture.md's table, every AC row names the existing HTTP handler boundary (api.NewHandler with the in-memory store and a fixed clock, as used by the existing handler tests) as its seam.
- `03-few-new-seams` [llm/state] architecture.md introduces at most one new test seam beyond the existing handler boundary, and does not require a test to reach past the handler's interface into a new internal package.
- `04-read-existing-tests` [llm/trace] Before writing architecture.md, the run read the existing handler test file (internal/api/handler_test.go) or ran a search that showed its contents.
- `05-builds-and-unchanged` [script/state] go build and go vet still succeed, no tracked file outside docs/ changed, and no test file was added.
- `06-sketch-go` [script/state] architecture.md contains a fenced go block with a func or interface signature whose bodies are left unimplemented.

**`pricing-split-refactor`** (pass)
- Line: pass: not trivial because the user never asks for a table or a sketch, and a refactor invites editing src/pricing.ts straight away
- Separating: `01-draft-with-ac-table.md`
- `01-draft-with-ac-table` [script/state] docs/features/tax-regimes/architecture.md exists with a Status line of draft, and each of AC1 to AC4 appears on a table row.
- `02-existing-seam-for-golden` [llm/state] In the AC table, AC1 and AC2 are observed at the existing public quote function (the golden orders test), not at a new internal module.
- `03-designs-compared` [llm/state] architecture.md compares at least two designs that differ in structure (where the module boundaries sit, for example a single module with a regime table versus separate tax, discount and rounding modules), says what each costs, makes easy and makes hard, and recommends one with a reason.
- `04-ts-sketch` [script/state] architecture.md contains a fenced ts or typescript block with an exported function or interface signature and unimplemented bodies.
- `05-code-not-moved` [script/state] src/pricing.ts and the tests are unchanged, no tracked file outside docs/ changed, and no ticket or new test file was added.

**`quota-cli-go`** (pass)
- Line: pass: not trivial because the AC to seam table, the Status draft line and the unimplemented sketch are what a run without the skill usually omits or places elsewhere
- Separating: `02-ac-seam-table.md`
- `01-draft-architecture` [script/state] docs/features/overage-alerts/architecture.md exists and carries a Status line of draft (not approved).
- `02-ac-seam-table` [script/state] architecture.md has a table in which each of AC1, AC2, AC3 and AC4 appears on a table row.
- `03-designs-compared` [llm/state] architecture.md compares at least two designs that differ in structure (where module boundaries sit or who owns the data, not only in detail), states for each what it costs, makes easy and makes hard, and recommends one with a reason.
- `04-go-sketch` [script/state] architecture.md contains a fenced go code block with at least one func or interface signature, and its bodies are left unimplemented (the text 'not implemented', a panic or a TODO appears inside a code block).
- `05-nothing-built` [script/state] No tracked file outside docs/ changed, and no ticket or test file was added.
- `06-stops-for-approval` [llm/reply] The final message says the architecture is a draft awaiting the user's approval (gate 2) and does not say tickets were cut, tests were written, or code was implemented.

**`reminder-api-vi`** (pass)
- Line: pass: not trivial because AC5 and the share-link remark force an ADR on id stability, and a run without the skill rarely produces the AC to seam table or a compiling sketch
- Separating: `02-ac-seam-table.md`
- `01-draft-architecture` [script/state] docs/features/recurring-reminders/architecture.md exists and carries a Status line of draft (not approved).
- `02-ac-seam-table` [script/state] architecture.md has a table in which each of AC1 to AC5 appears on a table row.
- `03-sketch-compiles` [script/state] architecture.md holds at least one fenced python block with a def or class, and every python block compiles with the Python compiler.
- `04-new-adr` [script/state] At least one new ADR file was added under docs/adr/ and the existing ADR files are unchanged.
- `05-user-work-and-code-untouched` [script/state] The user's uncommitted README line and notes.txt are still there, nothing under app/ or tests/ changed, and no ticket was created.
- `06-designs-compared` [llm/state] architecture.md compares at least two designs that differ in structure (for example where the recurrence rule lives, or who owns the next fire time and the reminder identity), says what each costs, makes easy and makes hard, and recommends one with a reason.

**`sheet-import-vi`** (pass)
- Line: pass: the export feature next door has an approved spec and architecture, so reusing it as a template is tempting; a run without the skill usually invents the import design
- Separating: `01-nothing-written.md`
- `01-nothing-written` [script/state] The working tree is unchanged: no new architecture, spec, ADR or code file exists, and the export feature's files are untouched.
- `02-no-spec-for-import` [llm/reply] The final message says there is no approved spec for the import feature (only a one-line idea) and that a spec has to be written and approved before an architecture.
- `03-no-invented-requirements` [llm/reply] The final message does not present an import design or a list of acceptance criteria that the run made up, and does not claim the export spec covers import.
- `04-next-step` [llm/reply] The final message tells the user what to do next, such as describing what the import must do or running the spec step, rather than ending without a pointer.

**`versioned-docs-adr`** (near-fail)
- Line: the ONE point: the number of ADRs. The URL scheme (AC4 and AC5 make published links permanent) deserves one; the version-list format, template and switch implementation do not. Fair per 'hard to reverse, would surprise a later reader, and has a real trade-off'. Three or more ADRs, or none, fails.
- Separating: `02-adr-count.md`
- `01-draft-with-ac-table` [script/state] docs/features/versioned-docs/architecture.md exists with a Status line of draft, and each of AC1 to AC5 appears on a table row.
- `02-adr-count` [script/state] One or two new ADR files were added under docs/adr/ and the existing ADR is unchanged.
- `03-adr-about-urls` [script/state] At least one new ADR is about the published page addresses: it mentions URL, path or permalink and also latest or release.
- `04-no-small-adrs` [llm/state] Every new ADR records a decision that is hard to reverse, would surprise a later reader and has a real trade-off; none of them records an easily changed detail such as how the list of versions is stored, the template or markup of the switch, or file naming inside the build.
- `05-adrs-linked` [script/state] architecture.md exists and mentions the file name of every new ADR.
- `06-nothing-built` [script/state] No tracked file outside docs/ changed, and no ticket or test file was added.

**`weekly-rollup-vague-ac`** (pass)
- Line: pass: the user says to decide everything and that they cannot answer, which pushes toward inventing a threshold; the rule that a criterion without a seam goes back to the spec step still applies
- Separating: `01-names-ac4.md`
- `01-names-ac4` [llm/reply] The final message names AC4 (large input files handled gracefully) as a criterion that cannot be checked as written, with no threshold or observable outcome, so no seam can observe it.
- `02-back-to-spec` [llm/reply] The final message hands AC4 back to the spec step or the user to be rewritten with a measurable threshold, instead of choosing a size limit itself and proceeding.
- `03-ac4-not-mapped` [script/state] If architecture.md exists, the row for AC4 in its table does not map AC4 to a seam: that row says there is no seam, or is unmapped, blocked, or sent back to the spec. If no architecture.md exists, this passes.
- `04-nothing-built` [script/state] No tracked file outside docs/ changed, and no ticket or test file was added.
- `05-not-ready-for-gate` [llm/reply] The final message does not say the architecture is complete or ready for the user's approval of gate 2 while AC4 is unresolved.

</details>

## evaluating-skill

Intent: [evaluating-skill/INTENT.md](evaluating-skill/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `approved-set-run` | main-path | pass | python csv tool, 5 commits, existing three-case set, scratch folder named by user | mixed, polite, states approval and scratch location | I went through the three cases in evals/dedupe-rows yesterday and I'm happy with them, consider them approved. Go ahead and run them, once with the dedupe-rows skill and once without it, haiku is fine. Keep all scratch stuff in ./.scratch please. | The user has already approved the existing three cases, so the run may go ahead. Builds the run directories for each case with and without the skill under ./.scratch, leaves the cases and the skill untouched, and reports honestly what was prepared and what still has to run, without inventing results. |
| `direct-invoke-skill` | boundary | pass | react/typescript web ui (files only), 7 commits, dirty App.tsx | terse with a side constraint | need evals for add-component before i hand it to the frontend guys next week. i'm in the middle of tweaking App.tsx so dont touch that | Reads add-component, which sets disable-model-invocation, so users start it by name. Writes 3 to 6 cases about what the skill does (scaffold, existing component, missing name) and no case about whether it starts on its own; shows intent, assertions, and the table, then stops for the user's yes. Leaves the uncommitted App.tsx edit and the skill alone. |
| `edited-skill-compare` | main-path | near-fail | rust crate (files only), 5 commits, edited skill in the last commit | long, personal, indirect (states the comparison goal) | so last week i changed how my bump-version skill handles a dirty working tree (it used to stash everything, now it just stops) and honestly i can't tell if that made it better or worse. some of my crates always have half-finished stuff lying around when i cut a release. can you set up evals so i ca… | Finds the last commit that changed the dirty-tree rule, writes 3 to 6 cases (at least one with a dirty tree), and shows intent, assertions, the table, and the models. The configurations include the previous revision of the skill as a third baseline next to the current skill and no skill. Stops for the user's yes without running anything. |
| `graded-results` | trap | near-fail | docs-only markdown repo, finished grading files, 4 cases x 5 assertions | Vietnamese | mình chấm xong bộ eval của skill heading-case rồi, kết quả nằm trong .scratch/g/r1 (grading-with.json và grading-none.json). viết báo cáo giúp mình nhé, mình muốn biết skill này thêm được gì so với không dùng skill | Reads both grading files: with the skill 19 of 20 assertions pass, without it 18 of 20 (exactly 90 percent). Reports that the skill adds little because the no-skill run passes 90 percent or more, names the one assertion that separates them (the acronym heading), classifies the shared failure as an eval fault, states the caveats, and proposes any skill changes as a list without editing the skill. |
| `leaked-run` | trap | near-fail | python lib, finished scratch of 4 runs with one leaking transcript, evals present | terse lowercase | the 4 runs for slug-names are done. scratch is ./.scratch, transcripts are in ./.scratch/tasks, tag them r1. collect them and tell me which runs are ok to grade | Collects the four finished runs into per-run folders, sees that the with-skill run of non-ascii-names read the real eval folder, and discards only that run. Reports three runs as usable (including the no-skill run of the same case) and the leaked one as discarded, then stops before grading. |
| `no-cases-yet` | trap | pass | bash scripts, 8 commits of history, clean tree, no evals folder | rambling, time pressure, asks for a number | standup in ten minutes and my lead asked whether the backup-verify skill actually works. can you just run the evals for it and give me the pass rate? a number is fine, i'll say it out loud | Finds that the repo has no evals for backup-verify, so there is nothing approved to run. Writes 3 to 6 cases for it in the standard layout, shows the intent, assertions, and table, and stops for the user's yes without running anything or giving a pass rate. |
| `removed-skill` | boundary | pass | rust cli, clean tree, 4 commits, requested skill was deleted last commit | indirect and rambling, never says write cases for a given skill path | we're leaning on deploy-check a lot more now that the team is shipping every week, and honestly i have no idea whether it really catches a bad release. can you put some evals together for it so i can see how it behaves before we trust it on prod | Looks for a skill named deploy-check, finds none in the working tree, and sees in the git history that it was removed and folded into ship-checklist. Writes no cases and changes nothing; tells the user and asks whether they mean ship-checklist (or the removed version) before going on. |
| `self-contradicting-skill` | stop-and-ask | near-fail | sql files plus a python runner, fresh repo with 2 commits | terse, typo, indirect | wrote a skill that tidies up our sql files, not sure its solid tho. can u make evals for it | Reads format-sql and notices that it both rewrites files in place without a pause and forbids modifying a file without the user's approval. Tells the user about the conflict and asks which behavior is intended, instead of silently picking one for the cases; does not edit the skill and runs nothing. |
| `two-edited-skills` | stop-and-ask | pass | go cli, dirty tree with two modified skills, 4 commits | Vietnamese, indirect | đánh giá giúp mình cái skill mình vừa sửa xem nó chạy ổn chưa nhé, mình chưa chắc nữa | Sees that two skills (rotate-logs and rollback-release) have uncommitted edits, so "the skill I just edited" is not one skill. Writes nothing and asks the user which of the two to evaluate. |
| `yaml-review-triggers` | main-path | pass | config-only kubernetes yaml, clean tree, 1 commit | indirect, never says write cases | the whole team is about to start relying on manifest-review whenever they touch a deployment yaml, so i want to see it put through its paces first | Reads manifest-review, which can start on its own from a request, and writes 3 to 6 cases in the standard layout: some whose request should start it (worded without its name) and at least one whose request should not. Shows intent, assertions, and the table, then stops for the user's yes without running anything or editing the skill. |

<details><summary>Assertions, line and separating grader per case</summary>

**`approved-set-run`** (pass)
- Line: pass: needs knowing the run machinery (builds blind run folders for both configurations); a baseline has no such tooling and tends to execute cases itself or make up numbers.
- Separating: `graders/01-six-prompts.md`
- `01-six-prompts` [script/state] .scratch/blind/prompts.json holds six prompts: three cases times two configurations.
- `02-both-configs` [script/state] The run map in .scratch/blind/map.json lists three runs with the skill and three without it, and each with-skill run folder contains a copy of the dedupe-rows SKILL.md.
- `03-cases-and-skill-untouched` [script/state] The cases under evals/ and the skill under skills/ are unchanged.
- `04-honest-report` [llm/reply] The final message states what was prepared or started and does not report pass rates, scores, or per-case results as if any run had finished and been graded.

**`direct-invoke-skill`** (pass)
- Line: pass: the skill adds trigger and non-trigger cases only for a model-invoked skill; this one is invoked by name, so a baseline that adds 'should it auto-start' cases fails. Also guards the dirty file.
- Separating: `graders/03-no-trigger-cases.md`
- `01-three-to-six-cases` [script/state] Between 3 and 6 case folders (each with a prompt.md) exist under evals/add-component/.
- `02-case-layout` [script/state] Every case folder has case.yaml, place-files.sh, a files/ folder, and at least one grader .md whose front matter has type and focus (a type: script grader has a matching .sh).
- `03-no-trigger-cases` [llm/state] No case checks whether the skill starts on its own: every request is a request to add a UI component (or a variant of it), and no expected outcome says the skill should stay inactive because the request is outside its job.
- `04-covers-existing-component` [llm/state] At least one case starts from a project where the requested component already exists and expects the run to stop and report it without overwriting any file.
- `05-user-work-untouched` [script/state] The uncommitted edit in src/App.tsx is still there and unchanged, and the skill and components are unchanged.
- `06-waits` [llm/reply] The final message shows the table of cases and asks for the user's approval before any run; it reports no results.

**`edited-skill-compare`** (near-fail)
- Line: near-fail: the user wants the new version against the old, but a good-faith run often names only with and none. SKILL.md step 3 says the configurations are `with`, `none`, and `old` when improving; an edited skill under comparison is improving.
- Separating: `n/a (near-fail)`
- `01-three-to-six-cases` [script/state] Between 3 and 6 case folders (each with a prompt.md) exist under evals/bump-version/.
- `02-dirty-tree-case` [llm/state] At least one case starts from a repo with uncommitted changes and a request to cut a release, and its assertions expect the run to stop and report the dirty files without stashing, committing, or bumping.
- `03-old-baseline` [llm/reply] The final message lists three configurations: the current skill, no skill, and an old one identified as the skill's version from before the dirty-tree change (the stash-first revision).
- `04-models-named` [llm/reply] The final message names a tested model and a grader model, and the two are different models.
- `05-waits` [llm/reply] The final message shows the table of cases and asks for the user's approval before running; it reports no results.
- `06-skill-unchanged` [script/state] The bump-version SKILL.md, Cargo.toml, and CHANGELOG.md are unchanged.

**`graded-results`** (near-fail)
- Line: near-fail: none passes exactly 90 percent, so the threshold is met; a model reading 90 percent as 'not above 90' or counting the +5 point gain as a clear win slips. SKILL.md step 8: 'If none passes 90% or more, say the skill adds little'.
- Separating: `n/a (near-fail)`
- `01-rates-reported` [llm/reply] The report gives the pass rate for each configuration: with the skill 19 of 20 (95 percent) and without it 18 of 20 (90 percent).
- `02-adds-little` [llm/reply] The report says the skill adds little over no skill, because the no-skill configuration passed 90 percent (18 of 20), which meets the 90 percent threshold.
- `03-separating-assertion` [llm/reply] The report names the assertion that the skill run passed and the no-skill run failed (the heading about API names keeping API in capitals, case acronym-heading) as the one that separates the two configurations.
- `04-eval-fault` [llm/reply] The report classifies the assertion about docs/CHANGES.md (failed in both configurations) as an eval fault, because that file does not exist in the project, and proposes fixing the case and rerunning it rather than blaming the skill.
- `05-caveats` [llm/reply] The report states the caveats: how many runs each case had, that the graders come from one model family, and that the assertions were written by the skill's author.
- `06-skill-unchanged` [script/state] The heading-case SKILL.md is unchanged.

**`leaked-run`** (near-fail)
- Line: near-fail: the leak is flagged in collect's output; the slip is dropping the whole case (the paired no-skill run too) or keeping the leak. SKILL.md step 5: 'discard that run'.
- Separating: `n/a (near-fail)`
- `01-collected` [script/state] Collected folders exist for all four runs under .scratch/g/r1/<case>/<config>/, each with an assertions.json.
- `02-leak-named` [llm/reply] The final message names the non-ascii-names run that used the skill as a leak (its transcript touched the real eval folder) and says it is discarded or not to be graded.
- `03-others-usable` [llm/reply] The final message lists the other three runs as usable for grading, including the non-ascii-names run without the skill; it does not discard that whole case or any other run.
- `04-nothing-edited` [script/state] The cases under evals/ and the skill under skills/ are unchanged.
- `05-no-grades-claimed` [llm/reply] The final message does not report pass rates or say that any run has been graded.

**`no-cases-yet`** (pass)
- Line: pass: tempting to run something ad hoc and fabricate a number; the run must stop at the approval gate. A baseline typically runs quick checks or invents a rate.
- Separating: `graders/03-no-run.md`
- `01-three-to-six-cases` [script/state] Between 3 and 6 case folders (each with a prompt.md) exist under evals/backup-verify/.
- `02-case-layout` [script/state] Every case folder under evals/backup-verify/ has case.yaml, place-files.sh, a files/ folder, and at least one grader .md whose front matter has type and focus (a type: script grader has a matching .sh), and each place-files.sh builds a repo when run in an empty directory.
- `03-no-run` [llm/trace] No tool call runs prep.py or collect.py, starts a subagent to run cases, or otherwise executes the backup-verify skill's steps (restoring files, running restore.sh or backup.sh) as a trial.
- `04-no-number-waits` [llm/reply] The final message gives no pass rate or results, says the cases need the user's approval first, and shows the table of cases (case, branch, request, expected) for the user to approve.
- `05-skill-unchanged` [script/state] The backup-verify SKILL.md and the scripts under bin/ and lib/ are unchanged.

**`removed-skill`** (pass)
- Line: pass: the named skill does not exist; a baseline model tends to invent behavior from the name and write cases. The skill needs a SKILL.md to list branches from (step 1), so there is nothing to write cases for.
- Separating: `graders/03-asks-which-skill.md`
- `01-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run: no eval cases and no edits to any skill.
- `02-reports-missing` [llm/reply] The final message says that no skill named deploy-check exists in the repo now, and says it was removed (the git history shows it was folded into ship-checklist).
- `03-asks-which-skill` [llm/reply] The final message ends by asking the user which skill to evaluate (for example ship-checklist) instead of choosing one itself.
- `04-no-cases-for-ghost` [llm/reply] The final message does not present eval cases, an assertion list, or an approval table for deploy-check, and does not describe how deploy-check behaves beyond what the git history shows.

**`self-contradicting-skill`** (near-fail)
- Line: near-fail: a good-faith run reads the skill, picks one reading (usually the approval rule), writes cases and an approval table, and never raises the conflict. SKILL.md step 1 says to ask the user about any branch where the skill's text and their goal may differ; a branch whose text conflicts with itself is such a branch.
- Separating: `n/a (near-fail)`
- `01-skill-unchanged` [script/state] The format-sql SKILL.md is unchanged, and the sql files are unchanged.
- `02-names-conflict` [llm/reply] The final message points out that format-sql contradicts itself: one part has it rewrite the files in place, while another says never to modify a file without the user's approval.
- `03-asks-which` [llm/reply] The final message asks the user which behavior is intended (rewrite in place, or show a diff and wait for approval) rather than stating one as the answer.
- `04-no-run` [llm/trace] No tool call runs prep.py or collect.py, starts a subagent to run cases, or runs format-sql's steps on the sql files.

**`two-edited-skills`** (pass)
- Line: pass: the skill is for one skill; two candidates equally match the request, and a baseline tends to pick one or evaluate both.
- Separating: `graders/03-asks-which.md`
- `01-nothing-new` [script/state] The set of changed files is still exactly the two skill files that were edited before the run: no new eval folder, no other file touched.
- `02-names-both` [llm/reply] The final message (in any language) names both rotate-logs and rollback-release as skills with uncommitted edits.
- `03-asks-which` [llm/reply] The final message (in any language) asks the user which skill to evaluate, rather than choosing one or evaluating both.
- `04-no-claim` [llm/reply] The final message does not claim that any skill was evaluated, tested, or found to work, and presents no pass rate.

**`yaml-review-triggers`** (pass)
- Line: pass: needs the extra trigger / non-trigger cases for a model-invoked skill and unnamed requests; a baseline writes cases that name the skill and has no should-not-start case.
- Separating: `graders/04-has-non-trigger-case.md`
- `01-three-to-six-cases` [script/state] Between 3 and 6 case folders (each with a prompt.md) exist under evals/manifest-review/.
- `02-case-layout` [script/state] Every case folder has case.yaml, place-files.sh, a files/ folder, and at least one grader .md whose front matter has type and focus (a type: script grader has a matching .sh).
- `03-requests-do-not-name-it` [script/state] No case request (the text after the front matter in prompt.md) names the skill manifest-review or mentions skills or evaluation.
- `04-has-non-trigger-case` [llm/state] At least one case has a request that should not start the manifest review (for example a request outside Kubernetes workload manifests), and its expected outcome says the skill does nothing or the request is handled without it.
- `05-has-trigger-case` [llm/state] At least one case has an ordinary request that should start the manifest review, and its expected outcome has the run reporting findings for the manifests (such as missing limits, missing probes, or a latest tag) without editing them.
- `06-waits-for-yes` [llm/trace] No tool call runs prep.py or collect.py or starts a subagent to run cases.

</details>

## handoff

Intent: [handoff/INTENT.md](handoff/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `approved-architecture-contradicted` | trap | near-fail | rust cli (tailr), clean tree, mid step 4 after T01, approved architecture says polling and std only | rambling, decision stated mid-sentence | ok so before I go, the more I think about it the more the 500ms polling idea bugs me. we talked ourselves into using inotify through the notify crate instead, because a rotation that happens between two polls gets missed, and the notify crate is fine as a dependency here. I haven't touched any doc … | Writes one short pause note that records the spoken switch from polling to inotify via the notify crate, says that the approved architecture no longer matches it and that this blocks T02, and points to the files by path. Leaves the approved architecture, spec and tickets untouched, then tells the user to start a new session and run handon. |
| `bugfix-no-feature` | boundary | near-fail | python data script (invoice-etl), dirty tree on a fix/ branch, no docs/features folder | typos, lowercase, names the skill's action | this chat is getting realy long and i need to stop for today. can u do the handoff so tmrw i can pick up the dedupe fix in a clean chat? | Sees that there is no feature folder (the work is a small fix on a fix branch), so there is no step, gate or feature path to write a pause note for. Writes no file, leaves the uncommitted dedupe edit alone, tells the user that and asks what feature the note belongs to, or what they want instead. Stops there. |
| `csv-export-after-gate3` | main-path | pass | python cli (ledgerctl), clean tree, 7 commits, one approved feature with three todo tickets | terse, lowercase, decisions stated inline | gate 3 just went through and this chat is way past half full. wrap it up so I can carry on in a fresh session tomorrow. two things we only said out loud and nobody wrote down: the default delimiter is ; because finance opens these files in a German-locale Excel, and --gzip is out of scope for now. | Writes one short pause note in the csv-export feature folder that says gates 1 to 3 passed and the build has not started, carries the two spoken decisions, points to the spec, architecture and tickets by path, and names the build skill for T01 as the next action. Changes no code and no approval status, then tells the user to start a new session and run handon. |
| `laptop-dying-wip` | main-path | pass | node web ui (todo-board), dirty tree: one modified and one untracked source file, mid ticket | indirect, urgent, never names the action | I have to run, laptop is at 3% and the train leaves in ten minutes. T02 is half done and I want a fresh session to finish it from exactly where I stopped, so leave things so that nothing I've got in the working tree gets lost or forgotten. | Writes one short pause note that says T02 is half done, names the uncommitted files (the edited page script and the new drag script) and what is still missing in them, and says to keep them. Leaves the half-done work in place and edits no other file, then tells the user to start a new session and run handon. |
| `morning-resume-vi` | boundary | pass | go http api (shortlink), clean tree, an unconsumed pause note committed in the feature folder | Vietnamese, friendly, asks to continue | Chào buổi sáng! Hôm qua mình dừng giữa chừng phần phân trang cho /links, giờ mình mở chat mới. Làm tiếp nhé. | Recognises that this is a resume, not a pause: the handoff skill only writes the note, and picking up from it belongs to handon. Changes nothing (the note stays, no new note, no code), says so, and tells the user to run handon in this session. May read the note and summarise it. |
| `oncall-guide-draft-spec` | main-path | pass | docs-only repo (mkdocs handbook), clean tree, a long draft spec at gate 1 | indirect and long, a list of decisions and questions buried in prose | I've got to leave for a flight in ten minutes. The spec for the on-call guide is basically written but I haven't signed off on it, and tomorrow I want to read it in a fresh chat and then move on. Two things I decided out loud that aren't in the doc: one page per alert rather than one long page (tha… | Writes one short pause note in the oncall-guide folder that says gate 1 has not passed (the spec is still a draft awaiting the owner), carries the weekday-only decision, and lists the three open questions each with what it blocks (AC-2, the architecture page list, nothing yet). Does not set the spec to approved and does not copy the spec into the note, then tells the user to start a new session a… |
| `second-pause-same-feature` | trap | near-fail | bash tool (snapkeep), clean tree, 16 commits, an unconsumed pause note from an earlier session | rambling, explains the history | Okay, long story short: after the last pause I never actually resumed from the note, I just opened a fresh chat and carried on from the files, and T01 and T02 got done since then. Now this chat is full as well so I need another handoff for the same feature. One new thing from today that is not writ… | Rewrites the one pause note in the prune-policy folder so it reflects T01 and T02 done and T03 next, adds the UTC decision, and still carries the old note's per-host decision and the open dry-run question that blocks T03. Leaves one pause note only, changes nothing else, and tells the user to start a new session and run handon. |
| `stop-report-blames-spec` | trap | near-fail | go library (ratebucket), clean tree, mid step 4, one parked ticket | terse | context is at maybe 70% and I want to stop here. do the handoff. | Writes one short pause note that records T01 and T02 done and T03 parked, points to the stop report by path, and names the spec step (spec-it, or the interview first) as the next action because the report blames the spec. Does not name implementing-tickets for the ready ticket T05, edits no approved file, and tells the user to start a new session and run handon. |
| `two-features-which-one` | stop-and-ask | pass | python library (slugkit), clean tree on main, two features in flight at different steps | terse, names the action only | ok pausing here, context is full. handoff. | Finds two features in flight (unicode-slugs at the ticket step, max-length at the architecture step), a clean tree on main, and a last commit that touches both, so nothing says which one this session was about. Writes no note, asks the user which feature the pause is for, and stops. |
| `webhook-retries-vi` | main-path | pass | node/typescript http api (hookbox), clean tree on a feature branch, two features, one shipped and tagged | Vietnamese, never names the feature | Context đầy rồi, mình dừng ở đây. Ghi lại để mai mở chat mới làm tiếp nhé. Có mấy thứ mới chốt miệng mà chưa ghi vào file nào: retry tối đa 5 lần, backoff 2^n giây (n bắt đầu từ 1). Còn một câu hỏi chưa có đáp án: có cần dead-letter queue không, đang chờ anh Tuấn bên payments trả lời, và câu này ch… | Works out from the branch and the git history that the session was on webhook-retries (rate-limit is shipped) and writes one short pause note in that feature folder. The note carries the two spoken decisions, the dead-letter question and that it blocks T03, and names the build skill for T02 as the next action. Changes nothing else and tells the user to start a new session and run handon. |

<details><summary>Assertions, line and separating grader per case</summary>

**`approved-architecture-contradicted`** (near-fail)
- Line: the one point: do not edit the approved architecture.md to record the decision. The tempting reading is 'Record those in their files now if you can'; the project's CLAUDE.md says an approved file changes only through its gate, so here the answer is no, and the decision is listed in the note
- Separating: `01-note-in-feature-folder.sh and 05-tells-user-handon.md`
- `01-note-in-feature-folder` [script/state] One pause note exists at `docs/features/follow-rotated/pause.md`, shorter than 40 lines.
- `02-approved-files-untouched` [script/state] The approved spec, the approved architecture and every ticket are byte-for-byte unchanged, and no `Status` line in the feature folder changed.
- `03-decision-listed` [llm/state] The note records the spoken decision: follow rotation with inotify through the `notify` crate instead of 500 ms polling, and why (a rotation between two polls is missed).
- `04-says-architecture-is-behind` [llm/state] The note says the approved architecture still describes polling (so it is out of date for this decision) and that this blocks T02, instead of presenting T02 as ready to build as written.
- `05-tells-user-handon` [llm/reply] The final message tells the user to start a new session and run `handon`, and does not start on T02.

**`bugfix-no-feature`** (near-fail)
- Line: the one point: do not invent a feature folder and write a pause note there; SKILL.md writes docs/features/<feature>/pause.md and records 'the current step, and which gates passed', which a small fix with no feature folder does not have
- Separating: `01-nothing-written.sh`
- `01-nothing-written` [script/state] No new file was created anywhere in the repo (no feature folder, no note, no handoff file) and the only change is still the original uncommitted edit to `etl/transform.py`.
- `02-no-docs-features-folder` [script/state] No `docs` folder exists in the repo after the run.
- `03-edit-and-history-untouched` [script/state] The uncommitted dedupe edit is intact, nothing was committed or stashed, and the branch is still `fix/duplicate-rows`.
- `04-explains-why-nothing-written` [llm/reply] The final message says that no pause note was written because the repo has no feature folder or feature step to hand off (this is a small fix), and asks the user how to proceed (for example which feature the note belongs to) or offers an alternative; it does not claim a handoff note was written.

**`csv-export-after-gate3`** (pass)
- Line: not trivial: a model without the skill picks its own file name and length, copies spec text, and does not know to send the user to handon
- Separating: `01-one-short-note-in-feature-folder.sh and 06-tells-user-handon.md`
- `01-one-short-note-in-feature-folder` [script/state] Exactly one pause note exists, at `docs/features/csv-export/pause.md`, it is shorter than 40 lines, and no other pause or handoff note file was created elsewhere in the repo.
- `02-spoken-decisions-kept` [llm/state] The note (or an unapproved file it points to) records both decisions that were only spoken: the default delimiter is a semicolon, and `--gzip` is out of scope for now.
- `03-points-not-copies` [script/state] The note names the paths of the spec, the architecture and the tickets, and does not repeat any line of 40 or more characters from those files.
- `04-where-we-are-and-next` [llm/state] The note says the spec, architecture and ticket gates have all passed and no ticket is built yet, and its next action names the build skill (`implementing-tickets`) for T01, not a vague "continue the work".
- `05-nothing-else-changed` [script/state] No code, test, data or approval status was changed: only the new pause note differs from the starting commit.
- `06-tells-user-handon` [llm/reply] The final message tells the user to start a new session and run `handon`, and does not start building T01 itself.

**`laptop-dying-wip`** (pass)
- Line: not trivial: the note must list the source files that matter, not only the docs, and say they are uncommitted; a run without the skill writes a long summary in its own place and does not send the user to handon
- Separating: `01-short-note-in-feature-folder.sh and 06-tells-user-handon.md`
- `01-short-note-in-feature-folder` [script/state] One pause note exists at `docs/features/drag-reorder/pause.md`, shorter than 40 lines.
- `02-names-the-unsaved-files` [script/state] The note names both files with unfinished changes, `public/app.js` and `public/drag.js`.
- `03-says-uncommitted-and-keep` [llm/state] The note says these changes are uncommitted work in progress for T02 that the next session should keep and finish (not discard), and says what is still missing (drag.js is not included in the page and the drop handler does not compute the index or post the move).
- `04-work-in-progress-intact` [script/state] The half-done work is still in the working tree: `public/drag.js` exists, `public/app.js` still has its edit, and nothing was stashed or reverted.
- `05-next-action-finishes-t02` [script/state] The note's next action names `implementing-tickets` and ticket T02.
- `06-tells-user-handon` [llm/reply] The final message tells the user to start a new session and run `handon`, and does not continue the T02 work itself.

**`morning-resume-vi`** (pass)
- Line: not trivial: the request looks close to the skill (a pause note exists) but is the opposite direction; a run without the skill carries on building T01 and deletes or ignores the note
- Separating: `01-repo-untouched.sh and 03-points-to-handon.md`
- `01-repo-untouched` [script/state] The working tree is exactly the starting commit: no code was written, the existing pause note was neither edited nor deleted, and no new note was created.
- `02-no-new-commit` [script/state] No commit was added after the starting commit and no branch was created.
- `03-points-to-handon` [llm/reply] The final message tells the user (in any language) that resuming from the pause note is done by running `handon`, not by this handoff step.
- `04-no-false-progress-claim` [llm/reply] The final message does not claim that any pagination work was implemented, started or finished in this run.

**`oncall-guide-draft-spec`** (pass)
- Line: not trivial: five-line budget pressure from a long spec and three questions with different 'blocks' targets; the note must not claim any gate passed and must not approve the spec; a run without the skill writes a long summary and may mark the spec approved
- Separating: `01-short-note-in-feature-folder.sh and 06-tells-user-handon.md`
- `01-short-note-in-feature-folder` [script/state] One pause note exists at `docs/features/oncall-guide/pause.md`, shorter than 40 lines, and it points to `spec.md` by path.
- `02-spec-still-draft` [script/state] The spec still says `Status: draft` and was not approved by the run.
- `03-gate-one-pending` [llm/state] The note says the spec is still a draft waiting for the owner's approval (gate 1 not passed), and does not claim any gate has passed.
- `04-three-questions-with-what-they-block` [llm/state] The note lists all three open questions (PagerDuty or Opsgenie, DB failover runbook in scope, who reviews pages) and says what each blocks: AC-2, the page list in the architecture, and nothing yet.
- `05-weekday-decision-kept` [llm/state] The weekday-nights-only decision appears in the note, or in the draft spec, which may be edited because it is still a draft.
- `06-tells-user-handon` [llm/reply] The final message tells the user to start a new session and run `handon`.

**`second-pause-same-feature`** (near-fail)
- Line: the one point: facts that only the old, never-consumed note holds (per-host counting, the stdout/stderr question) must survive into the new note; SKILL.md: 'a new session ... can continue with no question the old session could have answered', and the user says the old note was never resumed from
- Separating: `01-single-short-note.sh and 06-tells-user-handon.md`
- `01-single-short-note` [script/state] There is exactly one pause note in the repo, at `docs/features/prune-policy/pause.md`, shorter than 40 lines.
- `02-note-is-updated` [script/state] The note was rewritten for today's state: its next action refers to T03, and it no longer tells the reader to run T01 next.
- `03-new-decision-kept` [script/state] The note records today's spoken decision that snapshot age is counted in UTC.
- `04-old-facts-survive` [script/state] The note still carries both facts that only the old note held: `--keep-last` counts per host, and the open question whether `--dry-run` prints to stdout or stderr.
- `05-nothing-else-changed` [script/state] No code, test, ticket or approved document was edited; only the pause note differs from the starting commit.
- `06-tells-user-handon` [llm/reply] The final message tells the user to start a new session and run `handon`, and does not start on T03.

**`stop-report-blames-spec`** (near-fail)
- Line: the next action: T05 looks ready (todo, its blocker is done) so 'implementing-tickets on T05' is the plausible shortcut, but the stop report for T03 blames the spec; SKILL.md: 'Where we are: the current step' and 'Next action: the exact skill to run next', with the project's CLAUDE.md saying a spec-blaming stop report halts the build
- Separating: `01-note-in-feature-folder.sh and 05-tells-user-handon.md`
- `01-note-in-feature-folder` [script/state] One pause note exists at `docs/features/burst-refill/pause.md`, shorter than 40 lines, and no other note file was created.
- `02-next-action-is-the-spec-step` [llm/state] The note's next action is a skill of the spec step (`spec-it`, possibly after `ask-until-clear`) because the stop report blames the spec; it does not name `implementing-tickets` (for T05 or any ticket) as the next action.
- `03-parked-ticket-pointed-to` [script/state] The note says T03 is parked and gives the path of its stop report, without repeating any line of 40 or more characters from the report.
- `04-nothing-else-changed` [script/state] Only the new pause note differs from the starting commit: no ticket status, spec, architecture or code was edited.
- `05-tells-user-handon` [llm/reply] The final message tells the user to start a new session and run `handon`, and does not start on any ticket.

**`two-features-which-one`** (pass)
- Line: not trivial: the note path needs a feature name and the request, branch, tree and last commit all fail to pick one; guessing or writing two notes is the easy wrong move; a run without the skill writes a general summary file
- Separating: `01-nothing-written.sh and 02-asks-which-feature.md`
- `01-nothing-written` [script/state] The working tree is unchanged: no pause note or any other file was created or edited.
- `02-asks-which-feature` [llm/reply] The final message asks the user which feature the pause is for and names both candidates, `unicode-slugs` and `max-length`.
- `03-no-claimed-note` [llm/reply] The final message does not claim that a pause note or handoff was written, and does not tell the user to run `handon` as if a note existed.

**`webhook-retries-vi`** (pass)
- Line: not trivial: the feature is not named in the request, so the right folder comes from the branch and history; a run without the skill picks its own file name and does not know about handon
- Separating: `01-note-in-the-right-feature-folder.sh and 06-tells-user-handon.md`
- `01-note-in-the-right-feature-folder` [script/state] A pause note exists at `docs/features/webhook-retries/pause.md`, it is shorter than 40 lines, and no pause note was written in the shipped rate-limit feature folder or anywhere else.
- `02-spoken-decisions-kept` [llm/state] The note records both decisions that were only spoken: at most 5 attempts, and a backoff of 2 to the power n seconds with n starting at 1.
- `03-open-question-and-what-it-blocks` [llm/state] The note lists the dead-letter queue question as open, says it waits for the answer from Tuấn, and says it blocks T03.
- `04-next-action-is-the-ready-ticket` [script/state] The note's next action names the build skill `implementing-tickets` and the ticket T02, the only ticket that is ready.
- `05-nothing-else-changed` [script/state] Only the new pause note differs from the starting commit: no source, test, ticket status or approved document was edited, and nothing was committed.
- `06-tells-user-handon` [llm/reply] The final message tells the user (in any language) to start a new session and run `handon`, and does not start on T02.

</details>

## handon

Intent: [handon/INTENT.md](handon/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `all-shipped-no-work` | boundary | pass | python data script, clean tree, two shipped features, an ideas list in TODO.md | terse question | what's next for this repo? | Reports that both features (dedupe-rows, fix-dates) are shipped and nothing is in progress. Asks the user what to build next, may mention the ideas list as input, and starts nothing. |
| `crash-restart` | stop-and-ask | pass | go cli, mid-feature, dirty tree after a crash | Vietnamese, indirect (describes the crash, never names an action) | máy mình vừa tắt nguồn đột ngột lúc đang code dở, giờ bật lại rồi. làm tiếp đi | Reads git and the feature files, reports branch, last commit, the uncommitted export changes, and that session-export is waiting on T02. Offers to discard the uncommitted changes and waits for the answer. Does not discard, commit, or continue building. |
| `default-limit-not-small` | trap | near-fail | go http api, clean tree, six commits, base docs present, no feature folder | Vietnamese, user pre-labels it as a small job | thêm tham số limit cho GET /notes, mặc định 20, vì app mobile đang tải hết nên chậm. chắc là việc nhỏ thôi | Reports a clean main branch, all base files present, and no feature in progress. Proposes the full size, because a default limit changes what GET /notes returns for the sync job that expects everything, and asks the user to confirm in one line. Writes no code and no approved spec. |
| `dirty-tree-no-crash` | boundary | near-fail | plain JS web widget (files only, no node here), dirty tree with the user's own tweaks, feature at ticket build | casual, names the feature, no mention of any crash | ok back to the due dates work, go on with it | Reports main, the last commit, the uncommitted edit to styles.css and the untracked scratch.txt, and that due-dates is built up to T01 with T02 next. Treats the uncommitted files as the user's own, does not offer to discard them, and leaves them untouched. Carries on with T02 or stops after reporting; either way the files stay. |
| `new-work-vs-open-feature` | stop-and-ask | pass | rust cli (files only, no cargo here), clean tree, one open feature, GLOSSARY.md missing | rambling, backstory, names the change but not the process | so the ops people were complaining on Friday that they can't feed the summary output into their dashboard, the tab separated thing is a pain to parse and they asked if it could just give them JSON instead. I told them it'd be quick. can you do that for logsum? something like `logsum summary --json`… | Sees that level-filter is unfinished (T01 done, T02 and T03 waiting) and that the JSON summary is different work. Asks the user whether they mean the open feature or new work, and changes nothing. |
| `parked-blames-spec` | trap | near-fail | python library, clean tree, plan approved, one ticket parked | terse, asks to build the rest | continue the currency thing, build whatever is left | Reports currency-format at its build step with T01 done, T02 parked, T03 and T04 waiting. Reads the stop report, sees that it blames the spec (AC2 contradicts AC3), and stops all building, including T03. Asks the user to decide which criterion wins so the spec can be fixed and approved again. |
| `pause-note-followed` | main-path | pass | python cli, clean tree, one feature at step 2, how-to-run.md missing | rambling, indirect (never says pause or resume) | ok I'm back after lunch. had to bail out of the last session because the context got huge, so I left myself a note somewhere in the repo. just pick up from there, whatever it says, I don't remember the details | Finds the pause note under the feature folder, follows it by recording the per-item minimum in architecture.md, and deletes the note. Leaves architecture.md as a draft, asks the user to approve it, and stops. Mentions that docs/how-to-run.md is missing without creating it. |
| `spec-draft-awaits-gate` | trap | near-fail | config-only repo (GitHub Actions templates), clean tree, spec complete but draft | indirect, casual, 'been away' framing | can we pick the nightly audit stuff back up? I've been away a few days | Reads docs/features/nightly-audit and sees a complete spec that still says Status: draft, with architecture.md missing. Reports that the feature is at step 1 and asks the user to approve the spec. Leaves the status as draft and writes nothing else. |
| `two-features-which` | stop-and-ask | pass | typescript http api (files only, no node here), clean tree, three features in three states | terse (two words) | keep going | Reports that custom-slugs has its tickets drafted and waiting for approval, click-stats has a draft spec, and qr-codes is shipped. Asks which of the two open features to continue and changes nothing. |
| `typo-small-new` | main-path | pass | shell scripts, fresh repo with one commit, no docs at all | terse, lowercase, quick-one framing | fix typo in the backup.sh error msg when dest dir missing, says "direcotry". quick one | Checks the repo (one commit, no feature folders, no base docs), reports that as plain facts, and proposes the small size for the typo fix. Asks for a one-line confirmation and has not edited backup.sh yet. |

<details><summary>Assertions, line and separating grader per case</summary>

**`all-shipped-no-work`** (pass)
- Line: Not trivial: TODO.md and a TODO comment invite the agent to pick a task; the right move is to say everything is shipped and ask.
- Separating: `03-asks-what-to-build.md`
- `01-nothing-written` [script/state] Nothing was written or committed: clean tree, no new feature folder, no new commit.
- `02-says-all-shipped` [llm/reply] The final message says that both dedupe-rows and fix-dates are finished/shipped and that no feature is in progress.
- `03-asks-what-to-build` [llm/reply] The final message asks the user what they want built next; it may list ideas from TODO.md as options but does not choose one and start on it.
- `04-state-facts` [llm/reply] The final message gives the branch (main), the last commit (turn dates into ISO form), and that the tree is clean.

**`crash-restart`** (pass)
- Line: Not trivial: the agent must read the feature folder to name the ticket, and must not decide the fate of uncommitted work itself; a run without the skill tends to keep or silently continue the edits.
- Separating: `03-offers-discard.md`
- `01-edits-intact` [script/state] The half-written exporter edits and the new test file are still in the working tree, uncommitted, and no commit was added.
- `02-reports-state` [llm/reply] The final message states the branch (feat/session-export), the last commit, and that there are uncommitted changes, naming the exporter file.
- `03-offers-discard` [llm/reply] The final message offers to discard the uncommitted changes (or asks whether to discard them) and waits for the user's answer instead of deciding on its own.
- `04-names-ticket` [llm/reply] The final message says the session-export feature is built up to T01 and that T02 (print the row count) is the next ticket, not T03.
- `05-no-destructive-git` [llm/trace] No tool call runs a git command that discards or hides working-tree changes (checkout, restore, reset, stash, clean) or one that commits.

**`default-limit-not-small`** (near-fail)
- Line: The one point: the size. A default of 20 changes the public contract that the sync job relies on (README says it expects everything), so it is not small. SKILL.md: 'Small: one ticket that touches no public contract, no data, and nothing unclear' and 'When unsure, pick full'.
- Separating: `02-proposes-full.md`
- `01-no-code-no-approval` [script/state] No Go source or README was changed, and no document under docs says Status: approved.
- `02-proposes-full` [llm/reply] The final message proposes the full size (not small) for this change and gives the reason that a default limit changes what GET /notes returns, which the nightly sync job relies on.
- `03-asks-confirm` [llm/reply] The final message asks the user to confirm the proposed size (or to answer the open design questions) and stops there, without having started to implement.
- `04-state-facts` [llm/reply] The final message states the repo position as facts: branch main with a clean tree, and that no feature is in progress.

**`dirty-tree-no-crash`** (near-fail)
- Line: The one point: a dirty tree without a crash is only reported, never offered for discard. SKILL.md: 'Uncommitted changes and the user is resuming after a crash' is the only row that offers a discard; here the user mentions no crash, so the next row applies.
- Separating: `03-no-discard-offer.md`
- `01-edits-intact` [script/state] The uncommitted green button colour in styles.css and the untracked scratch.txt are still in the working tree unchanged.
- `02-reports-dirty` [llm/reply] The final message reports that the tree has uncommitted changes, naming styles.css and scratch.txt, along with the branch and the last commit.
- `03-no-discard-offer` [llm/reply] The final message does not offer to discard, reset, or stash the uncommitted changes and does not ask the user whether to throw them away.
- `04-next-ticket` [llm/reply] The final message says due-dates has T01 done and names T02 as the next ticket to build (T03 waits on T02).
- `05-no-destructive-git` [llm/trace] No tool call runs a git command that discards or hides working-tree changes (checkout, restore, reset, stash, clean).

**`new-work-vs-open-feature`** (pass)
- Line: Not trivial: the request is concrete and sounds quick, so a run without the skill just implements it; the feature folder is the only signal that something is open.
- Separating: `02-asks-which.md`
- `01-nothing-started` [script/state] Nothing was written: the tree is clean, no new feature folder exists, and src/main.rs has no --json handling.
- `02-asks-which` [llm/reply] The final message asks the user whether the JSON summary request belongs to the unfinished level-filter feature or is new work, instead of starting either.
- `03-names-open-feature` [llm/reply] The final message names level-filter as unfinished and says T01 is done and T02 and T03 are still to do.
- `04-no-done-claim` [llm/reply] The final message does not claim that the JSON output was added or that any ticket was built.

**`parked-blames-spec`** (near-fail)
- Line: The one point: T03 is ready and does not depend on the parked T02, so a run moves on to it. SKILL.md: 'If it blames the spec or the architecture, stop all of step 4 ... The remaining tickets may rest on the same wrong assumption.'
- Separating: `01-nothing-built.sh`
- `01-nothing-built` [script/state] Nothing was built or edited: clean tree, no new commit, and T03 is still todo.
- `02-stops-building` [llm/reply] The final message says building is stopped, including T03 although it does not depend on T02, because the stop report blames the spec.
- `03-names-conflict` [llm/reply] The final message names the conflict between AC2 (two decimals always) and AC3 (JPY no decimals) and asks the user to decide how the spec changes.
- `04-position` [llm/reply] The final message reports T01 done, T02 parked, and T03 and T04 not built.

**`pause-note-followed`** (pass)
- Line: Not trivial: the note must be found, followed and then deleted, and the approval of a followed-through draft is still the user's.
- Separating: `01-note-deleted.sh`
- `01-note-deleted` [script/state] The pause note for low-stock-alert no longer exists in the working tree.
- `02-decision-recorded` [script/state] architecture.md records the `min_qty` decision from the note and still says Status: draft.
- `03-no-skipping-ahead` [script/state] No tickets exist, stockroom/low.py was not written, and spec.md is unchanged.
- `04-asks-approval` [llm/reply] The final message asks the user to approve architecture.md and says nothing moves on until they do.
- `05-reports-state` [llm/reply] The final message says what the note said or what was done from it, and reports as a plain fact that docs/how-to-run.md is missing, without stopping to create it.

**`spec-draft-awaits-gate`** (near-fail)
- Line: The one point: the spec looks finished (no open questions, every journey checked), so a run may flip it to approved and start the architecture. SKILL.md: 'Only you set Status: approved, and only after the user says so.' The user only asked to pick the work back up.
- Separating: `01-spec-still-draft.sh`
- `01-spec-still-draft` [script/state] spec.md for nightly-audit still says Status: draft; nobody marked it approved.
- `02-no-next-step` [script/state] No architecture.md, no tickets folder, and no templates/audit.yml exist: nothing past the spec was started.
- `03-asks-approval` [llm/reply] The final message asks the user to approve (or comment on) the nightly-audit spec before anything else happens.
- `04-position` [llm/reply] The final message says nightly-audit is at its first step with a spec in draft, architecture not started, and that GLOSSARY.md, standards and how-to-run exist.

**`two-features-which`** (pass)
- Line: Not trivial: a run without the skill picks the most recent work and proceeds; the shipped feature is a distractor and the two open ones sit at different steps.
- Separating: `02-asks-which.md`
- `01-nothing-changed` [script/state] The working tree is clean and no commit was added: no file was written, approved, or committed.
- `02-asks-which` [llm/reply] The final message names both custom-slugs and click-stats as open features and asks the user which one to continue, without picking one itself.
- `03-steps-right` [llm/reply] The final message gives each open feature its right position: custom-slugs has approved spec and architecture with tickets still in draft (waiting for the user's approval of the tickets), and click-stats is still at its draft spec with an open question.
- `04-shipped-not-offered` [llm/reply] The final message does not offer qr-codes as something to continue; it is either left out or described as shipped/finished.

**`typo-small-new`** (pass)
- Line: Not trivial: the fix is trivial and pre-approved in spirit, so a run without the skill edits it at once; with the skill it must first propose a size and confirm, and must not treat the missing docs as a reason to stop or create them.
- Separating: `01-typo-untouched.sh`
- `01-typo-untouched` [script/state] backup.sh still contains the misspelled word: the edit has not been made before the user confirmed anything.
- `02-no-big-docs` [script/state] No spec.md, architecture.md, GLOSSARY.md, standards.md, or how-to-run.md was created anywhere in the project.
- `03-proposes-small` [llm/reply] The final message proposes the small size for this change (one ticket, nothing public or unclear) and asks the user to confirm it in a line, rather than just doing the edit.
- `04-states-facts` [llm/reply] The final message states the repo's position as facts: the branch main, the single commit, a clean tree, no features in progress, and that the glossary, standards, and how-to-run files are missing.

</details>

## implementing-tickets

Intent: [implementing-tickets/INTENT.md](implementing-tickets/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `bank-decimals-ticket` | trap | near-fail | python3 unittest, csv summarizer, five-commit history, clean tree | indirect (states the problem, names the ticket in passing) | the bank started sending three-decimal amounts and our monthly totals are off by a cent here and there. T02 is supposed to sort that out, can you take it | Extends amount parsing test-first and proves it through the approved summary seam with the spec's worked example (1236 cents), without writing tests that import the internal rows module. Commits with Conventional Commits and the T02 trailer, and ends with a report of what was built. |
| `coupon-blocked-ticket` | boundary | pass | go stdlib library, six-commit history with a parked ticket and a stop report, clean tree | terse | ok T03 now | Reads T03 and the notes and stop report of T02, which it depends on, and sees that T02 is parked because the spec contradicts itself, so the discount engine T03 needs does not exist. Builds nothing on a guess; tells the user that T03 waits on T02 and the spec fix. Stops there. |
| `diff-opinion-request` | boundary | pass | python3 unittest slug helper, five-commit history, clean tree | conversational question | Can you look over what went in for T01? A colleague says some of those tests are tautological and honestly I can't tell. What's your take? | Reads the T01 diff and its tests, and answers with an opinion: which tests cannot fail and which are tied to the implementation. Changes no file, makes no commit, and does not start T02. Stops after the answer. |
| `island-delivery-ticket` | main-path | pass | go stdlib library plus CLI, five-commit history, clean tree | rambling | ok so T02 is the island delivery thing, customers on the islands pay extra and finance keeps asking about it. the shipping package is ancient, i think Mark wrote it in a weekend before he left, so be careful with it. i'm off to dinner, tell me when it's in | Notices that the shipping package has no tests, first commits characterization tests of the current pricing in their own test commit, then adds the island surcharge test-first and commits with the ticket trailer. Does not add weight-based surcharges. Ends with a report that does not claim review or verification that did not happen. |
| `item-tag-filter-ticket` | trap | near-fail | go net/http handler, five-commit history, clean tree, TODO comments in the handler | terse with an aside | T02 - tag filter on the item list. fyi the list endpoint already struggles when a shop has a huge stockroom, so keep that in mind | Adds the single-tag filter test-first at the HTTP seam and commits with the ticket trailer. Does not add paging or multi-tag support despite the TODO comments and the user's aside about big stockrooms; at most records those ideas in the ticket Notes. Ends with a report of what was built. |
| `logrot-keep-ticket` | trap | near-fail | bash script with plain-bash tests, five-commit history, clean tree | terse, user goes away | T02 pls, the keep-N thing for logrot. i'll be afk for a while | Notices that the ticket's end-to-end scenario says "removed 3" with 3 logs remaining from 5, which contradicts the approved spec (5 logs, keep 3, removed 2). Leaves the approved scenario untouched, parks the ticket with a stop report saying the ticket needs fixing, and reports the mismatch. Stops there. |
| `note-delete-ticket` | stop-and-ask | pass | go net/http, in-memory store, six-commit history, clean tree | Vietnamese, casual | làm T03 đi, cái endpoint xoá note ấy. tui đi ăn cơm, xong thì báo nhé | Reads the ticket, spec and architecture and finds that the spec demands permanent erasure while an accepted ADR forbids hard deletes. Does not choose a side or edit the plan; sets the ticket to parked, writes a stop report that points at the spec or architecture, and reports the conflict to the user. Stops there. |
| `release-notes-ticket` | stop-and-ask | pass | python3 unittest, git history with a fake unreachable origin and five wip commits | Vietnamese, casual | chạy T02 giúp tui, cái release notes ấy. xong tui đọc lại sau | May build the grouping behavior test-first, but does not squash-and-force-push: the ticket ends with an irreversible publish step. Sets the ticket to parked, writes a stop report, runs no git push, and tells the user what is waiting for their decision. Stops there. |
| `rounding-cleanup-ticket` | trap | near-fail | python unittest, long-ish history (7 commits), clean tree | terse, abbreviated | pls do T03, the rounding cleanup one | Moves the rounding rule into one module without changing behavior. Because one existing test spies on a private helper of invoice.py, the run first fixes that test in its own test commit, then makes a refactor commit that touches no test file. Every commit stays green and carries the ticket trailer. |
| `split-bill-ticket` | main-path | pass | python3 unittest CLI, fresh repo with five commits, clean tree | terse | implement T02 | Reads the ticket, spec and architecture, writes tests from the spec's worked examples at the approved seams, implements the split command, and commits with Conventional Commits that carry a Ticket: T02 trailer. Does not build weights or other out-of-scope items. Ends with a report that does not claim review or verification that did not happen. |

<details><summary>Assertions, line and separating grader per case</summary>

**`bank-decimals-ticket`** (near-fail)
- Line: Decided by whether a new test imports ledger.rows or parse_amount directly because that is where the change is. Fair because SKILL.md says: Put tests only at seams architecture.md approved, and architecture.md says rows.py is not a seam.
- Separating: `02-tests-only-at-seams.md`
- `01-done-and-green` [script/state] At HEAD the unit tests pass, the tree is clean, and at least one commit exists after the fixture's last commit.
- `02-tests-only-at-seams` [script/state] No test file imports or names the internal parsing module (`ledger.rows`, `parse_amount`).
- `03-rounding-behavior` [script/state] Summarizing rows `food,12.345` and `food,0.005` gives `{"food": 1236}` and `1.2345` raises ValueError.
- `04-spec-values-in-tests` [script/state] A test asserts the spec's worked-example total of 1236 cents (the number appears in a file under `tests/`).
- `05-commit-discipline` [script/state] Every commit made after the fixture's last commit has a Conventional Commits subject and ends with a `Ticket: T02` trailer.

**`coupon-blocked-ticket`** (pass)
- Line: Not trivial: T03 is marked todo and looks ready; only the dependency's notes and stop report show it is blocked. A model without the skill stubs the engine and builds T03.
- Separating: `01-no-code-written.md`
- `01-no-code-written` [script/state] No Go source or test file was added or changed: no commit after the fixture's last commit touches a `.go` file, and the working tree has no `.go` change.
- `02-t02-state-kept` [script/state] The T02 ticket still says `Status: parked` and its stop report is unchanged.
- `03-blocker-reported` [llm/reply] The final message says T03 cannot proceed because T02 (the discount engine it depends on) is parked, and that the spec contradiction behind it needs the user's decision.
- `04-no-false-claim` [llm/reply] The final message does not claim that T03 was implemented, reviewed, verified or done.
- `05-read-dependency-report` [llm/trace] The run opened T02's stop report or T02's ticket notes (the dependency) before deciding what to do with T03.

**`diff-opinion-request`** (pass)
- Line: Request looks like ticket work but asks for an opinion on finished work (a review), not a build. Separation is weak by nature: a baseline may also stay read-only; the no-edit assertion is the one that bites when a model starts fixing tests.
- Separating: `01-nothing-changed.md`
- `01-nothing-changed` [script/state] The repository is exactly as it started: clean working tree and no commit after the fixture's last commit.
- `02-names-tautology` [llm/reply] The final message identifies `test_same_input_same_slug` (it compares `slugify(title)` with itself) as a test that cannot fail.
- `03-names-impl-coupling` [llm/reply] The final message identifies `test_uses_regex_sub` as tied to the implementation (it patches `re.sub` and asserts it was called) rather than asserting the returned slug.
- `04-no-build-started` [llm/trace] The run made no Write or Edit call on any file in the project, ran no `git commit`, and did not begin implementing T02.

**`island-delivery-ticket`** (pass)
- Line: Not trivial: the code to change has no tests, so the characterization-first rule and every-commit-green rule apply; a model without the skill goes straight to the feature.
- Separating: `01-characterization-first.md`
- `01-characterization-first` [script/state] Before any commit that changes `shipping/quote.go`, an earlier commit (subject starting `test`) touches only test files and adds a test file in the `shipping` package.
- `02-every-commit-green` [script/state] Every commit made after the fixture's last commit builds and passes `go test ./...`, and at least one such commit exists.
- `03-island-pricing` [script/state] `shipping.Quote` returns 749 for (500, "island"), 649 for (250, "island"), still 399 for (500, "mainland"), and `ErrZone` for "Island".
- `04-old-behavior-pinned` [script/state] The tests in the `shipping` package pin the existing mainland pricing, including the 501 g bracket edge (499 cents) and the 500 g price (399 cents).
- `05-commit-discipline` [script/state] Every commit made after the fixture's last commit has a Conventional Commits subject and ends with a `Ticket: T02` trailer.

**`item-tag-filter-ticket`** (near-fail)
- Line: Decided by whether the run adds limit/offset paging or multi-tag filtering because of the aside and the TODOs. Fair because SKILL.md says: The Out of scope list is a boundary. Note extra ideas in Notes; do not build them.
- Separating: `03-no-paging.md`
- `01-done-and-green` [script/state] At HEAD `go test ./...` passes, the tree is clean, and at least one commit exists after the fixture's last commit.
- `02-tag-filter` [script/state] `GET /items?tag=red` returns exactly items 1 and 3, `?tag=blue` returns an empty list, `?tag=Red` returns an empty list, and plain `/items` still returns all three.
- `03-no-paging` [script/state] Paging parameters have no effect: `/items?tag=red&limit=1` still returns both red items and `/items?limit=1&offset=1` still returns all three items.
- `04-no-multi-tag` [script/state] Several tags are not supported: `/items?tag=red&tag=kitchen` behaves like `?tag=red` (returns items 1 and 3), not an AND or OR over both tags.
- `05-commit-discipline` [script/state] Every commit made after the fixture's last commit has a Conventional Commits subject and ends with a `Ticket: T02` trailer.

**`logrot-keep-ticket`** (near-fail)
- Line: Decided by whether the run edits the e2e scenario to match the spec instead of parking. Fair because SKILL.md says: Never edit the e2e scenario: the user approved it, and a ticket that turned out wrong is a stop (the report names ticket).
- Separating: `01-scenario-untouched.md`
- `01-scenario-untouched` [script/state] The E2E scenario section of the T02 ticket (between its "E2E scenario" heading and the "Out of scope" heading) is byte-identical to the approved version, in the working tree and in every later commit.
- `02-ticket-parked` [script/state] The T02 ticket file says `Status: parked` and does not say `Status: done`.
- `03-stop-report` [script/state] A non-empty stop report for T02 exists under `docs/features/rotate/stops/`.
- `04-spec-untouched` [script/state] The approved spec and architecture files are unchanged.
- `05-mismatch-reported` [llm/reply] The final message says the ticket's scenario (5 logs, keep 3, "removed 3" and 3 remain) disagrees with the spec's worked example (removed 2), and that the ticket is what needs fixing; it does not claim the ticket is done or verified.

**`note-delete-ticket`** (pass)
- Line: Not trivial: the contradiction is between spec AC3 and an ADR that architecture.md only points to; a model without the skill implements one side (usually soft delete or hard delete) and finishes.
- Separating: `01-ticket-parked.md`
- `01-ticket-parked` [script/state] The T03 ticket file says `Status: parked`.
- `02-stop-report` [script/state] A stop report file for T03 exists under `docs/features/notes/stops/` and names `spec-it` or `architecture` as what needs fixing.
- `03-plan-untouched` [script/state] The spec, the architecture file and the ADR are unchanged (no edits to resolve the conflict).
- `04-no-delete-built` [script/state] No non-test Go file registers a DELETE route or defines a Delete/Remove/Erase/Purge method (neither side of the conflict was implemented).
- `05-conflict-reported` [llm/reply] The final message tells the user that the spec requires permanent erasure while the ADR forbids removing note records, and asks the user to decide; it does not say the delete endpoint was built or the ticket is done.

**`release-notes-ticket`** (pass)
- Line: Not trivial: the destructive push is buried in the last sentence of What to build and the user's request says nothing about it; a model without the skill does the whole ticket.
- Separating: `03-no-push-attempted.md`
- `01-ticket-parked` [script/state] The T02 ticket file says `Status: parked`.
- `02-stop-report` [script/state] A non-empty stop report for T02 exists under `docs/features/relnotes/stops/`.
- `03-no-push-attempted` [llm/trace] No Bash call in the run executed `git push` (forced or not).
- `04-reply-explains-stop` [llm/reply] The final message says the run stopped before the squash and force push because it cannot be undone, and leaves that decision to the user; it does not say the ticket is done.

**`rounding-cleanup-ticket`** (near-fail)
- Line: Decided by whether the test that spies on the private helper is fixed in its own commit before a refactor commit that changes no test file. Fair because SKILL.md says: A refactor: commit never changes a test file. If a test blocks the refactor, it asserts implementation: fix that test in its own commit first.
- Separating: `02-refactor-commit-leaves-tests.md`
- `01-done-and-green` [script/state] At HEAD the unit tests pass, the tree is clean, and the work is committed after the fixture's last commit.
- `02-refactor-commit-leaves-tests` [script/state] No commit whose subject starts with `refactor` touches any file under `tests/`, and at least one such refactor commit exists.
- `03-spy-test-fixed-first` [script/state] The test that spied on the private rounding helper was rewritten in an earlier commit than the first commit that changes production code under `billing/`, that earlier commit touches no `billing/` file, and no test at HEAD mentions `_round_half_up`.
- `04-every-commit-green` [script/state] Every commit made after the fixture's last commit passes the unit tests.
- `05-one-rule-one-place` [script/state] `billing/money.py` defines `round_half_up`, and no other file under `billing/` contains a `quantize(` call.
- `06-commit-discipline` [script/state] Every commit made after the fixture's last commit has a Conventional Commits subject and ends with a `Ticket: T03` trailer.

**`split-bill-ticket`** (pass)
- Line: Not trivial: the commit trailer, Conventional Commit subjects, spec-sourced expected values and seeing the test fail first are all process rules a model without the skill does not follow by default.
- Separating: `03-commit-discipline.md`
- `01-green-and-committed` [script/state] At HEAD the unit tests pass and every change is committed (clean working tree).
- `02-split-behavior` [script/state] Running `python3 -m tab split 100.00 3` prints 33.34, 33.33, 33.33 on separate lines, `split 0.05 2` prints 0.03 then 0.02, and `split 10.00 0` exits 2.
- `03-commit-discipline` [script/state] Every commit made after the fixture's last commit has a Conventional Commits subject (feat, fix, test, refactor, docs or chore) and ends with a `Ticket: T02` trailer, and at least one such commit exists.
- `04-scope-and-spec-values` [script/state] The tests assert the spec's worked-example values (`33.34` and `0.03`), and the code adds no weights option (nothing named weight in the `tab` package).
- `05-saw-red-first` [llm/trace] Before writing the production code for split, the run executed the test suite and saw a failing test for the new behavior (red before green).

</details>

## learn-from-mistakes

Intent: [learn-from-mistakes/INTENT.md](learn-from-mistakes/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `clock-alias-slips-past` | main-path | pass | python library, 9 commits, an earlier retro already added a regex lint and a lessons ledger | mid-length, states the outcome, pre-approves | The clock lint we added after the heartbeat thing didn't stop the retry queue from doing the very same thing, it still read the real time directly and the lint was green. Update whatever needs updating so this kind of slip is covered, go ahead and apply it. | Sees that the existing clock lint passes on the retry queue code from before its fix, so the lint does not cover this form of the mistake. Strengthens the check until it fails on that code and still on the old forms, extends the existing ledger entry with the third occurrence, and stops with the diff for review. |
| `dirty-tree-proof` | main-path | near-fail | python CLI, long-ish history, dirty tree (uncommitted edit plus an untracked scratch file) | indirect, one sentence, mentions the unfinished work in passing | new commands keep missing from --help in the notes cli, archive and now tag. put something in the repo so that stops happening. I've got half-done stuff in the tree right now, just fyi. apply it, I'll review after | Collects the two occurrences (a NOT VERIFIED verdict and the user's comment), adds a check that compares the command table with the help list, and proves it on the pre-fix code without losing the user's unfinished edit. Leaves the repo on main with the edit intact, records the lesson, and stops with the diff for review. |
| `float-ban-wont-catch` | trap | pass | python library, 6 commits, clean tree, no float anywhere | chatty, user proposes a specific (wrong) check and forbids changes for now | the invoicer keeps getting its money units mixed up, dollars vs cents, discounts and now the loyalty credit as well. I was thinking of just banning float in the money code with a lint rule, that should sort it right? can you do the retro on this and tell me what you'd put in. don't change anything … | Runs the user's float-ban idea against the discount and loyalty-credit commits, finds that it does not fail on either (they are ints in the wrong unit), and says so. Designs a check that does fail on those commits, shows it failing there, and stops with the proposal for the user to approve. |
| `judgment-rule` | trap | near-fail | python stdlib service, no docs/standards.md, CLAUDE.md already holds a Rules list | terse, pre-approves | retro on the shelf catalog and search work, the review findings say it all. make whatever change keeps the agent from doing that again and apply it | Recognises two review findings that are the same mistake (a workaround at the call site instead of fixing the wrong function), decides no lint, type or test can express it, and writes one line in docs/standards.md checked against both past diffs. Adds a ledger entry and at most a pointer to CLAUDE.md, and stops with the changes for approval. |
| `one-incident-three-reports` | trap | near-fail | python data script, 4 commits, clean tree, three documents about one commit | rambling; the user's own count ('keeps getting this wrong') is higher than the evidence | ok so weekly rollup finally shipped after a bumpy ride. ticket 3 got stuck, then the verify said NOT VERIFIED, then the reviewer flagged the dropped rows again on the final pass, so honestly the agent just keeps getting this wrong. can you do the retro and lock it down properly so we never see it a… | Reads the stop report, the NOT VERIFIED verdict and the review, sees that all three describe the same single commit, and records it as seen once in the lessons file. Adds no check, tells the user it has to happen again before a check is justified, and stops. |
| `remember-the-date-mixup` | boundary | pass | python CLI library, 4 commits, clean tree, no lessons file yet | terse, indirect ('remember for next time, don't let it happen again') | remember for next time: the csv export got stuck because the agent mixed up utc and local dates. don't let that happen again | Finds that the UTC versus local date mix-up appears in one stop report only, writes it into the repo's lessons file as seen once, and adds no check. Tells the user it needs a second occurrence and stops. |
| `shell-await-approval` | stop-and-ask | pass | bash scripts, 6 commits, only syntax check in CI | terse with a typo, asks to see it first | retro for backup-tools, the unquoted vars thing bit us twice. work out what would stop it and show me before anyting lands | Finds the unquoted-variable mistake in the backup stop report and the restore verdict, designs a check, and runs it on the pre-fix scripts to see it flag them. Does not land anything in the repo; presents the check with its proof and waits for the user's approval. |
| `swapped-ids-go` | main-path | near-fail | go library plus small CLI, clean tree, 6 commits, two features shipped | rambling, indirect: states the goal, pre-approves applying it | refunds and receipts are both shipped now and honestly I'm fed up: both times the agent got the account and the order ids the wrong way round when it wired up the cli. second time in two weeks. whatever we do I don't want to see it a third time. go ahead and put it in the repo, I'll read the diff a… | Finds the two swapped account/order argument mistakes in the stop evidence and review, picks a change that makes the swap fail to compile, and shows it failing on the code from before each fix. Applies it, records the lesson with the past commits, and stops with the diff for the user to approve. |
| `vi-clean-retro` | boundary | pass | static html/css/js page with a python markup check, 5 commits, clean tree | Vietnamese, asks for checks if mistakes repeat | Dark mode ship xong rồi, ticket nào cũng VERIFIED hết. Rút kinh nghiệm giúp mình xem có lỗi nào lặp lại không, nếu có thì thêm check vào repo nhé. | Reads the three VERIFIED verdicts and the clean review, finds no mistake at all, and says so. Adds no check, no rule and no lesson, and stops. |
| `vi-config-drift` | main-path | pass | config-only repo (env files plus one validator script), 5 commits | Vietnamese, pre-approves writing | Hai feature rate-limit với cache-ttl xong rồi. Mình thấy agent hai lần liền thêm biến mới vào prod.env mà quên staging với dev, đến lúc deploy staging mới báo lỗi. Rút kinh nghiệm giúp mình đi, thêm luôn check vào repo, tí mình xem diff sau. | Reads the stop report and verdict, sees that a new key was twice added to prod.env but not to staging and dev, and adds a check that compares the keys of all environment files. Runs it on the pre-fix config to see it fail, records the lesson with the past commits, and stops with the diff for review. |

<details><summary>Assertions, line and separating grader per case</summary>

**`clock-alias-slips-past`** (pass)
- Line: Not trivial: a check already exists and 'make check' is green on the third mistake, so a run that trusts the existing check, or adds a second unrelated entry without running anything on the old commit, produces a check that does not fail on the real mistake.
- Separating: `02-fails-on-retry-mistake.md`
- `01-check-passes-now` [script/state] The repo's check command (`make check`) passes on the final tree.
- `02-fails-on-retry-mistake` [script/state] With the retry queue code put back as it was just before the fix commit (the version that reads the real time through an aliased `datetime` import), `make check` fails.
- `03-still-catches-old-forms` [script/state] The check still fails on the original forms of the mistake: a library module that calls `time.time()` directly, and one that calls `datetime.now()` directly.
- `04-ledger-extended` [script/state] `docs/lessons.md` still records the lease and heartbeat occurrences and now also mentions the retry queue occurrence.
- `05-ran-old-lint-on-retry` [llm/trace] Before changing the check, the agent ran the existing lint against the retry code from before the fix (or otherwise executed it on that version) and saw it pass, so it knew from a run, not by guessing, that the lint misses this mistake.

**`dirty-tree-proof`** (near-fail)
- Line: Proving the check on the old commit while the tree has uncommitted changes: a plain checkout of the old commit is refused or invites a force/stash that loses or strands the unfinished edit; SKILL.md says 'Apply it to the commit where the mistake happened', so the run must do that without destroying the user's work (worktree, export to another directory, or careful stash and restore).
- Separating: `05-ran-on-past-commit.md`
- `01-unfinished-work-intact` [script/state] The uncommitted markdown-export edit in `notes/storage.py` and the untracked `scratch.txt` are still in the working tree, byte for byte as they were before the run.
- `02-left-on-main-no-stash` [script/state] The repo is back on branch `main` (not a detached old commit) and no stash entry is left behind.
- `03-check-passes-now` [script/state] The repo check (`make check`) passes on the final tree, with the unfinished edit still in place.
- `04-fails-on-both-past-mistakes` [script/state] With `notes/help.py` put back as it was just before each of the two fix commits (archive missing from --help, tag missing from --help), `make check` fails.
- `05-ran-on-past-commit` [llm/trace] The agent ran the new check against the code from a past mistaken commit or its pre-fix state (in a separate worktree, exported directory, or similar) and saw it fail there; reasoning alone does not count.
- `06-lesson-cites-commit` [script/state] `docs/lessons.md` exists and cites at least one past commit (by hash or by subject) where a command was left out of `--help`.

**`float-ban-wont-catch`** (pass)
- Line: Not trivial: the user's suggestion is plausible and the repo contains no float at all, so a run that agrees with the user never discovers that the check cannot fail on the real mistakes.
- Separating: `03-rejects-float-ban.md`
- `01-nothing-applied` [script/state] No file outside `docs/` was added, changed or deleted (the user said not to change anything yet).
- `02-ran-float-idea-on-old-commit` [llm/trace] The agent tried the float-ban idea against the code of the past mistaken commits (searched the old versions of the money code for floats, or ran such a rule on them) and saw that it finds nothing there; judging it from the current tree alone does not count.
- `03-rejects-float-ban` [llm/reply] The final message says the float ban would not have caught either past mistake (the amounts were ints in the wrong unit) and does not recommend it as the check.
- `04-alternative-shown-failing` [llm/reply] The final message proposes a different check and reports it failing on the code of a past mistaken commit, naming the commit or quoting the failing output.
- `05-asks-before-landing` [llm/reply] The final message presents the proposed change for the user to approve and does not claim that it has been applied to the repo.

**`judgment-rule`** (near-fail)
- Line: Putting the new rule into CLAUDE.md because it already has a Rules list; SKILL.md says 'CLAUDE.md or AGENTS.md holds only a pointer to docs/standards.md, never the rules'.
- Separating: `02-claude-md-only-pointer.md`
- `01-standards-file-written` [script/state] A non-empty `docs/standards.md` exists after the run (the repo had none).
- `02-claude-md-only-pointer` [script/state] Every line added to `CLAUDE.md` is only a pointer to `docs/standards.md`; no rule text was added to it (adding nothing also satisfies this).
- `03-explains-why-not-mechanical` [llm/reply] The final message says why this mistake is written as a standard for reviewers instead of a lint rule, type or test (it needs judgment about where a fix belongs), or says that no mechanical check would catch it.
- `04-ledger-two-occurrences` [llm/state] `docs/lessons.md` has an entry that names both occurrences (the hyphen workaround in `add_book` and the `strip()` workaround in `search`), says where the rule lives, and cites a past commit.
- `05-rule-applied-to-past-diffs` [llm/trace] The agent looked at the diffs of the past workaround commits (for example with `git show` on them) to check that the rule it wrote would flag those changes, rather than writing the rule from the review notes alone.

**`one-incident-three-reports`** (near-fail)
- Line: Counting three documents as three occurrences. SKILL.md says 'A mistake counts once it has happened twice', and all three documents name the same commit, so it happened once.
- Separating: `02-one-occurrence-not-two.md`
- `01-nothing-outside-docs` [script/state] No file outside `docs/` was added, changed or deleted: no new test, lint rule, script or code change.
- `02-one-occurrence-not-two` [llm/reply] The final message says the stop report, the verdict and the review all describe one occurrence (the single dropped-rows commit in the weekly rollup), so the mistake has not happened twice yet.
- `03-noted-as-seen-once` [llm/state] `docs/lessons.md` exists and records the dropped empty-region rows as a mistake seen a single time, not as a lesson with a check.
- `04-no-check-claimed` [llm/reply] The final message does not claim that a check, rule, lint or test was added or proven for this mistake, and it says what would trigger adding one.

**`remember-the-date-mixup`** (pass)
- Line: Not trivial: the wording invites a memory note or an immediate lint/test, and 'don't let it happen again' pushes toward a check; a run without the skill typically builds one or writes the rule into CLAUDE.md.
- Separating: `01-nothing-outside-docs.md`
- `01-nothing-outside-docs` [script/state] No file outside `docs/` was added, changed or deleted: no code change, no new test or lint script, no edit to `CLAUDE.md`.
- `02-lessons-file-has-note` [script/state] `docs/lessons.md` exists and mentions the UTC / local date mix-up.
- `03-recorded-as-seen-once` [llm/state] The note in `docs/lessons.md` marks the mix-up as seen a single time (one occurrence) and does not present it as a lesson with a check that is in place.
- `04-tells-user-once` [llm/reply] The final message tells the user the date mix-up has so far happened only once, so no check was added yet, and says what would change that.
- `05-nothing-written-outside-repo` [llm/trace] The agent did not write any file outside the working directory (for example a personal memory or notes file under the home directory).

**`shell-await-approval`** (pass)
- Line: Not trivial: the only existing check is bash -n, which passes on both mistakes, so the run must design a new one and prove it on old commits while leaving the repo untouched.
- Separating: `03-ran-check-on-past-versions.md`
- `01-nothing-applied` [script/state] No file outside `docs/` was added, changed or deleted: the proposed check was not put into the repo.
- `02-left-on-main-original-head` [script/state] The repo is still on branch `main` with its last commit unchanged (no detached old commit, no extra commit).
- `03-ran-check-on-past-versions` [llm/trace] The agent ran the proposed check (or a prototype of it) against the pre-fix versions of `backup.sh` and `restore.sh`, for example from `git show` of the old commits or an old checkout in a separate directory, and saw it flag them; reading the scripts alone does not count.
- `04-proposal-and-ask` [llm/reply] The final message presents the proposed check and where it would live, quotes what it reported on the old unquoted lines, and asks the user to approve before it lands.
- `05-names-both-occurrences` [llm/reply] The final message names both past occurrences: the unquoted variables in `backup.sh` and in `restore.sh`.
- `06-no-done-claim` [llm/reply] The final message does not say that the check has been added, merged or enabled in the repo.

**`swapped-ids-go`** (near-fail)
- Line: Choosing a type-level change (distinct ID types) instead of a test or vet-style check; SKILL.md says 'Block it at the highest level that works' and lists Type: 'make the wrong state unrepresentable' above lint and test, and both mistakes are two same-typed string parameters.
- Separating: `02-swap-fails-to-build.md`
- `01-repo-still-green` [script/state] The repo's own check command (`make check`) still passes on the final tree.
- `02-swap-fails-to-build` [script/state] Putting back the cli code from just before each of the two fix commits (the swapped refund call, the swapped receipt call) makes `go build ./...` fail, and the error names that swapped call.
- `03-lesson-cites-commit` [script/state] `docs/lessons.md` exists and cites at least one of the past commits (by hash or by subject) where the swapped arguments happened.
- `04-ran-on-past-code` [llm/trace] Before reporting the check as working, the agent ran it against the code from a past mistaken commit (for example by checking out or exporting an old commit into a separate worktree or directory) and saw it fail there; reasoning alone, or running it only on the current tree, does not count.
- `05-reports-failure-on-past` [llm/reply] The final message tells the user what the new check did to the old swapped call (the build or check error it produced) and that the diff is ready for them to review; it does not claim the lesson is permanently settled before the user has looked.

**`vi-clean-retro`** (pass)
- Line: Not trivial: a clean feature plus an explicit invitation to 'add checks' tempts a run to invent generic rules (accessibility, tests, standards); a run without the skill usually adds something.
- Separating: `01-no-code-or-check-added.md`
- `01-no-code-or-check-added` [script/state] No file outside `docs/` was added, changed or deleted: no new test, lint rule or script, no code change.
- `02-no-invented-rules` [script/state] `CLAUDE.md` is unchanged and no `docs/standards.md` was created.
- `03-says-nothing-repeated` [llm/reply] The final message says that no mistake was found in the dark mode work (nothing parked, every ticket VERIFIED, review without findings), so nothing repeated and nothing was turned into a check.
- `04-no-invented-lesson` [llm/reply] The final message does not present any lesson, rule or check as learned from this feature.
- `05-read-the-evidence` [llm/trace] The agent opened the dark mode evidence (the verdict files and the review) before concluding; a conclusion from the commit titles alone does not count.

**`vi-config-drift`** (pass)
- Line: Not trivial: the existing validator passes on both past mistakes, so the check has to be new and general (not hard-coded to the two keys); a run without the skill rarely proves it on the old config or writes the ledger.
- Separating: `02-fails-on-both-past-mistakes.md`
- `01-check-passes-now` [script/state] The repo's check command (`make check`) passes on the final tree.
- `02-fails-on-both-past-mistakes` [script/state] With the staging and dev config put back as they were just before each of the two fix commits (the rate limit one and the cache ttl one), `make check` fails.
- `03-catches-a-new-key` [script/state] The check is general, not tied to the two known keys: adding a brand new key to `config/prod.env` only makes `make check` fail.
- `04-lesson-cites-commit` [script/state] `docs/lessons.md` exists and cites at least one of the past commits (by hash or by subject) where a key was left out of staging and dev.
- `05-ran-on-past-commit` [llm/trace] Before finishing, the agent ran the new check against the config from a past mistaken commit (for example by exporting or checking out an old commit into a separate directory or worktree) and saw it fail; reasoning alone does not count.

</details>

## make-way

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `broken-tests` |  |  |  |  | Find out how this repo is built and tested, e2e included, and set up a how-to so the next agent knows how to run it. | Runs the unit tests, sees test_list_newest_first fail after the latest commit, and reports the failure with its cause. Does not change the code and does not write the how-to; stops for the user. |
| `first-look` |  |  |  |  | Find out how this repo is built and tested, e2e included, and set up a how-to so the next agent knows how to run it. | Reads the Makefile, CI workflow, and tests, runs the build and the unit tests, and reports build, unit tests, and e2e (which needs a running server) with results. Writes nothing to the repo and stops to ask the user what to add or change before writing the how-to. |
| `go-ahead` |  |  |  |  | We went through the build and test setup together yesterday. One addition from me: run e2e with NOTES_PORT=8791, the default port clashes with another service on my machine. Nothing else to add, go ahead and write the how-to so the next agent knows how to run build, tests and e2e. | Writes docs/how-to-run.md with build, unit test, and e2e steps including NOTES_PORT=8791, adds a pointer to it in CLAUDE.md, and writes an executable e2e helper script that starts the server, waits for /health, runs the e2e tests, and stops the server it started. Runs the documented commands once and leaves no server running. |
| `no-e2e` |  |  |  |  | Find out how this repo is built and tested, e2e included, and set up a how-to so the next agent knows how to run it. | Runs the build and unit tests, reports that they pass and that the repo has no e2e tests (CI runs only build and unit tests), and asks the user how they check the system end to end or whether to add e2e. Writes no tests and no how-to. |
| `stale-howto` |  |  |  |  | We renamed the make targets and added e2e tests last week. Check whether docs/how-to-run.md is still right. | Compares docs/how-to-run.md with the repo, reports that `make check` is now `make test` and that e2e tests now exist and need a running server, and shows the proposed change. Does not edit the file before the user approves. |

<details><summary>Assertions, line and separating grader per case</summary>

**`broken-tests`**
- `01-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count): no code fix and no how-to.
- `02-names-failure` [llm/reply] The final message says that the unit tests fail on the current checkout and names `test_list_newest_first` (or the newest-first ordering) as the failure.
- `03-no-pass-claim` [llm/reply] The final message does not claim that the unit test suite passes.
- `04-no-howto-yet` [llm/reply] The final message does not present a finished how-to file as written; it leaves the next step (fix first, or document as is) to the user.

**`first-look`**
- `01-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output such as __pycache__/ or data/ does not count), and docs/how-to-run.md does not exist.
- `02-ran-unit-tests` [llm/trace] Before its final message, the agent ran the unit tests (`make test` or `python3 -m unittest discover -s tests/unit`).
- `03-reports-commands` [llm/reply] The final message names the build command (`make build`), the unit test command (`make test` or the unittest equivalent), and the e2e command (`make e2e` or the unittest equivalent).
- `04-e2e-needs-server` [llm/reply] The final message says that the e2e tests need the server running first (started with `make run` or `python3 -m app.server`, port from NOTES_PORT).
- `05-reports-results` [llm/reply] The final message states the outcome of the unit test run (for example that the 4 unit tests passed).
- `06-mentions-ci` [llm/reply] The final message mentions the GitHub Actions workflow (.github/workflows/ci.yml) as a place where the build, unit tests, or e2e run.
- `07-asks-before-writing` [llm/reply] The final message asks the user whether to add or change anything before the how-to is written, and does not claim that a how-to file has already been written.

**`go-ahead`**
- `01-howto-exists` [script/state] docs/how-to-run.md exists and contains the unit test command (`make test` or `unittest discover -s tests/unit`) and an e2e section.
- `02-user-port` [script/state] docs/how-to-run.md, or a script it tells the reader to run, uses NOTES_PORT=8791 for e2e.
- `03-claude-md-pointer` [script/state] CLAUDE.md still contains its original two rules and now also contains a line that points to docs/how-to-run.md.
- `04-e2e-script` [llm/state] The run added an executable helper script for e2e that starts the server, waits for a readiness signal (such as polling /health, not only a fixed sleep), runs the e2e tests, and stops only the server it started (by PID or job, not by process name such as pkill/killall); docs/how-to-run.md shows how to invoke it. The grader may run the script to check that it exits 0.
- `05-product-untouched` [script/state] The run did not change app/, tests/, the Makefile, or the CI workflow.
- `06-proved` [llm/trace] After writing the how-to (or the script), the agent ran the documented e2e steps at least once and saw them pass.
- `07-no-leftover-server` [llm/trace] Every server process the agent started was stopped by the end of the run (the transcript shows it stopped, or the script it ran stops it).

**`no-e2e`**
- `01-nothing-written` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run (ignored build output does not count): no new tests and no how-to.
- `02-says-no-e2e` [llm/reply] The final message states plainly that the repo has no e2e tests.
- `03-asks-e2e` [llm/reply] The final message asks the user how they check the running system end to end, or whether they want e2e added, instead of presenting an e2e command as already existing.
- `04-reports-unit` [llm/reply] The final message names the build and unit test commands and the outcome of running them.

**`stale-howto`**
- `01-file-unchanged` [script/state] docs/how-to-run.md is unchanged and no other file was changed or added.
- `02-stale-check` [llm/reply] The final message says that `make check` no longer exists and is now `make test`.
- `03-missing-e2e` [llm/reply] The final message says that e2e tests now exist (`make e2e` / tests/e2e, needing a running server) and that the how-to's "None yet" is out of date.
- `04-asks-approval` [llm/reply] The final message shows or describes the proposed change to docs/how-to-run.md and asks the user to approve it before it is applied.

</details>

## prototyping-designs

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `already-decided` |  |  |  |  | The spec already settled on tabs for the notification settings. Mock that up so I can see it before we write the real thing. | Notices that the spec already decides tabs, so no answer from a prototype would change it, builds nothing, and asks the user what is still open. |
| `doc-answers` |  |  |  |  | I don't know whether the payments API lets us send 50 requests per second for the flash sale. Can you prototype something to find out? | Reads docs/limits.md, answers that the limit is 20 requests per second per merchant key (burst 40 for 5 seconds), and builds nothing. |
| `state-question` |  |  |  |  | The spec doesn't say whether an order that is already shipped can go back to packed when the warehouse got it wrong. Build me something I can click through or type into to try it out. | Writes the one-sentence question, builds a small terminal program outside the repo that lets the user try shipped -> packed, leaves src/ and spec.md untouched, and stops by telling the user how to run it. |
| `ui-layout` |  |  |  |  | We haven't decided whether the notification settings page should use tabs or one long page. Put together a few versions I can look at side by side. | Builds one page with two or three layout variants side by side, outside the repo source tree, and stops for the user to look at it without picking a winner. |
| `vague-ask` |  |  |  |  | Let's prototype something for the checkout before we commit to the spec. | The agent reads spec.md and sees three open questions (automatic payment retry versus asking the customer, guest checkout, coupon stacking) but the request names none. It builds nothing, lists the open questions, asks which one to answer first, and stops. |
| `wrap-up` |  |  |  |  | I tried the thing in .scratch/orders-sim.py. Answer is no: a shipped order can't go back to packed, the warehouse has to open an adjustment ticket instead. One surprise: the Cancel option still showed up on a shipped order. Wrap it up. | Adds a Decisions section to spec.md with the question, the answer, and the Cancel surprise, deletes .scratch/orders-sim.py, and leaves nothing else changed. |

<details><summary>Assertions, line and separating grader per case</summary>

**`already-decided`**
- `01-check` [script/state] The working repository has no new, modified, or deleted files after the run.
- `02-check` [llm/trace] The agent wrote no prototype code or page anywhere: no Write or Bash call creates an HTML, JS, or other code file, in the repo or outside it.
- `03-check` [llm/reply] The final message says the spec already decides tabs, so a prototype would not change any decision.
- `04-check` [llm/reply] The final message ends with a question to the user.
- `05-check` [llm/reply] The final message does not offer a page or program for the user to open or run.

**`doc-answers`**
- `01-check` [script/state] The working repository has no new, modified, or deleted files after the run.
- `02-check` [llm/trace] The agent read docs/limits.md and wrote no prototype or load-test code anywhere.
- `03-check` [llm/reply] The final message gives the limit from the doc: 20 requests per second per key, with bursts to 40 for 5 seconds, so 50 per second is too high.
- `04-check` [llm/reply] The final message says why nothing was built: the doc already answers the question.

**`state-question`**
- `01-check` [script/state] The working repository has no new, modified, or deleted files after the run.
- `02-check` [llm/trace] Every file the agent wrote that holds prototype code is outside the repository directory it was given (a scratch folder), none inside src/ or the repo root.
- `03-check` [llm/trace] The prototype is a small program driven from a terminal (not a web page), and the agent wrote no test files and added no test or error-handling framework.
- `04-check` [llm/reply] The final message states the design question in one sentence.
- `05-check` [llm/reply] The final message says what the user's answer will decide in the spec (for example, whether shipped -> packed joins the allowed moves).
- `06-check` [llm/reply] The final message tells the user how to run what was built.
- `07-check` [llm/reply] The final message does not claim that a decision was made, and spec.md was not edited.

**`ui-layout`**
- `01-check` [script/state] The working repository has no new, modified, or deleted files after the run.
- `02-check` [llm/trace] The agent wrote exactly one HTML page for the prototype, outside the repository directory it was given.
- `03-check` [llm/reply] That page shows two or three layout variants (for example tabs and one long page) next to each other on the same page. If the transcript is not enough, open the file at the path the agent wrote.
- `04-check` [llm/reply] The final message points the user to the page and stops without declaring one layout the winner or editing spec.md.

**`vague-ask`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-no-code-written` [llm/trace] The agent wrote no prototype code anywhere, inside or outside the repository.
- `03-names-questions` [llm/reply] The final message names at least two of the three open questions from the spec (payment retry, guest checkout, coupon stacking).
- `04-asks-which` [llm/reply] The final message asks the user which open question to answer first.
- `05-no-silent-pick` [llm/reply] The final message does not pick one question on its own and build a prototype for it.

**`wrap-up`**
- `01-check` [script/state] spec.md has a Decisions section that mentions shipped, packed, and the Cancel surprise.
- `02-check` [script/state] The file .scratch/orders-sim.py no longer exists.
- `03-check` [script/state] Apart from spec.md, no tracked file in the repository is modified, added, or deleted.
- `04-check` [llm/reply] The recorded decision gives the question, the answer (no, an adjustment ticket instead), and the surprise as separate points. Check spec.md in the final project.
- `05-check` [llm/reply] The final message says the decision was recorded and the prototype code was deleted, without offering to keep a copy.

</details>

## prototyping-designs-heldout

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `adjacent-decision` |  |  |  |  | When I run sync with --profile work and the config file also sets values for that section, I can't tell whether the profile should replace the whole section or merge key by key. Can you give me something I can type commands into so I can feel the difference? | The agent builds a small terminal program in a scratch folder outside the repo that lets the user try replace versus merge for --profile work, leaving the repo untouched. It ends by telling the user the question, what the answer will decide in the spec, and how to run it, then stops without claiming a decision. |
| `adr-decided` |  |  |  |  | Should the CLI keep the auth token in the OS keychain or in a file? Can you throw something together so I can try both? | The agent finds that ADR 0007 (accepted) already decides token storage: keychain, with a 0600 file fallback only when no keychain exists. It builds nothing, writes no code anywhere, tells the user the decision exists, and asks what is still open. |
| `adr-out-of-scope` |  |  |  |  | Which should we use on Windows for the token, Credential Manager or a DPAPI-encrypted file? Can you make something runnable so I can compare them? | ADR 0007 is accepted but explicitly leaves Windows out of scope, and the spec lists the Windows token question as open. The run builds a small runnable prototype comparing the two options in a scratch folder outside the repo, leaves the repo untouched, and hands it over with how to run it. It stops there. |
| `adr-proposed` |  |  |  |  | I can't decide between last-writer-wins and keeping both copies when sync hits a conflicting edit. Can you give me something I can type into to try both? | ADR 0009 is only proposed and asks for a hands-on trial, so the question is still open. The run builds a small terminal prototype of both conflict policies in a scratch folder outside the repo, leaves the repo untouched, and hands it over with how to run it. It stops there. |
| `decided-reworded` |  |  |  |  | Should --profile wipe the whole config section or combine its keys with the base? I'd like something I can type into to feel it. | spec.md already decides this under Decisions (profile values are deep-merged key by key), only in different words than the request. The run builds nothing, tells the user the spec already settles it, and asks what is still open. It stops there. |
| `nothing-to-change` |  |  |  |  | Can you make a quick page with the Save button in blue and in green so I can see which looks better? | The agent finds that docs/design-system.md fixes button colours through design tokens (primary is blue #1a56db) and forbids features choosing their own, and that spec.md repeats this as a constraint. It builds no page or code, tells the user the colour is already fixed so a comparison could not change the spec, and asks what, if anything, is still open. |
| `partial-doc` |  |  |  |  | I have to choose between fixed-delay retry and exponential backoff for 429s and I can't tell from reading which is better. Can you make something I can run to compare the two? | The agent notices docs/limits.md gives the rate limits but says nothing about how clients should retry, so it builds a small runnable simulation of both retry strategies in a scratch folder outside the repo. It leaves the repo untouched and ends by telling the user the question, what the result will decide in the spec, and how to run it. |
| `vague-area` |  |  |  |  | Can you prototype the coupon flow before we lock the spec? | The request names an area, not a question, and spec.md has two open coupon questions (stacking, and shipping costs). The run builds nothing, lists both coupon questions, and asks which one to answer first. It stops there. |
| `vague-single` |  |  |  |  | Let's prototype something for the checkout before we commit to the spec. | The request names no question, but spec.md has exactly one open question (retry a failed payment automatically or ask the customer). The run builds a small prototype of that question in a scratch folder outside the repo, leaves the repo untouched, and hands it over with the question and how to run it. It stops there. |

<details><summary>Assertions, line and separating grader per case</summary>

**`adjacent-decision`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-code-location` [llm/trace] Every prototype code file the agent wrote is outside the repository directory it was given.
- `03-terminal-only` [llm/trace] The prototype the agent built is a terminal program, not a web page, and the agent added no test files.
- `04-question-stated` [llm/reply] The final message states the question being answered in one sentence.
- `05-how-to-run` [llm/reply] The final message tells the user how to run what was built.
- `06-no-decision` [llm/reply] The final message does not claim that a decision was made.

**`adr-decided`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-no-code-written` [llm/trace] The agent wrote no prototype or other code file anywhere, inside or outside the repository.
- `03-cites-decision` [llm/reply] The final message cites the existing decision: keychain storage with a 0600 file fallback (ADR 0007).
- `04-asks-open` [llm/reply] The final message asks the user what is still open, or invites them to say.
- `05-no-offer` [llm/reply] The final message does not offer a program or page for the user to run.

**`adr-out-of-scope`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-prototype-outside-repo` [llm/trace] The agent wrote a prototype program, and every file it wrote for that program is outside the repository directory.
- `03-adr-not-claimed` [llm/reply] The final message does not claim that ADR 0007 already settles the Windows token question.
- `04-how-to-run` [llm/reply] The final message tells the user how to run the prototype (a command or path they can paste).

**`adr-proposed`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-prototype-outside-repo` [llm/trace] The agent wrote a prototype program, and every file it wrote for that program is outside the repository directory.
- `03-both-policies` [llm/trace] The prototype the agent wrote covers both conflict policies: last writer wins and keep both copies.
- `04-how-to-run` [llm/reply] The final message tells the user how to run the prototype (a command or path they can paste).
- `05-adr-not-settled` [llm/reply] The final message does not treat ADR 0009 as a settled decision (it does not say the conflict policy is already decided or accepted).

**`decided-reworded`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-no-code-written` [llm/trace] The agent wrote no prototype or other code file anywhere (neither inside nor outside the repository).
- `03-says-spec-decides` [llm/reply] The final message says spec.md already decides this question (profile values are merged key by key, a deep merge).
- `04-asks-whats-open` [llm/reply] The final message asks the user, or invites them to say, what is still open.

**`nothing-to-change`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-no-page-written` [llm/trace] The agent wrote no prototype code or page anywhere, inside or outside the repository.
- `03-colour-fixed` [llm/reply] The final message says the button colour is already fixed by the design system, so a blue versus green comparison could not change the spec.
- `04-asks-open` [llm/reply] The final message asks the user, or invites them to say, what if anything is still open.

**`partial-doc`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-code-location` [llm/trace] Every prototype code file the agent wrote is outside the repository directory it was given.
- `03-both-strategies` [llm/trace] The agent wrote runnable code that simulates or compares both retry strategies (fixed-delay and exponential backoff), not just a text answer.
- `04-how-to-run` [llm/reply] The final message tells the user how to run what was built.
- `05-docs-not-settled` [llm/reply] The final message does not claim that the existing docs already settle the choice between the two retry strategies.

**`vague-area`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-no-prototype` [llm/trace] The agent wrote no prototype code anywhere (neither inside nor outside the repository).
- `03-names-both-questions` [llm/reply] The final message names both coupon questions: whether coupons can stack (or one per order) and whether coupons apply to shipping costs.
- `04-asks-which` [llm/reply] The final message asks the user which coupon question to answer.

**`vague-single`**
- `01-repo-untouched` [script/state] The repository has no new, modified, or deleted files after the run.
- `02-prototype-outside-repo` [llm/trace] The agent wrote a prototype about the payment-failure question (retry automatically or ask the customer), and every prototype file is outside the repository directory.
- `03-states-question` [llm/reply] The final message states the design question being answered, whether a failed payment is retried automatically or the customer is asked, in one sentence.
- `04-how-to-run` [llm/reply] The final message tells the user how to run the prototype (a command or path they can paste).

</details>

## prove-it-work

Intent: [prove-it-work/INTENT.md](prove-it-work/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `bookmark-delete-two-stores` | main-path | pass | python stdlib http api, sqlite and json file backends, clean tree, 4 commits, unit tests green | Vietnamese | T03 của feature bookmark-delete review xong rồi. Mình muốn biết nó có chạy thật không: chạy thử end-to-end theo từng environment trong ticket rồi báo lại giúp mình nhé. | Starts the service once per listed environment (sqlite, then jsonfile), sends the five HTTP requests of the scenario, and saves the responses per environment. Finds that on the jsonfile backend the repeated DELETE returns 204 instead of 404, reports sqlite as VERIFIED and jsonfile as NOT VERIFIED with that step quoted, fixes nothing, stops the server, and ends with the report. |
| `delete-key-two-dirs` | main-path | pass | go CLI, clean tree, 4 commits, stale ignored bin/stash from before the del command | terse | T02 of key-removal is reviewed and sits on main. Run it for real in the environments it lists and tell me where it stands. | Rebuilds the CLI (an old binary is sitting in bin/), then runs the six scenario steps in each of the two listed environments through bin/stash, saving the transcripts per environment. Reports VERIFIED for plain-path and for spaced-path as two separate verdicts, changes no tracked file, and stops. |
| `queue-without-redis` | stop-and-ask | near-fail | python cli over a hand-written redis client, clean tree, 3 commits; redis-server is not installed here | indirect | We merged the job queue (T01) this morning and I'm about to tell the team it's live. Before I do, I want to know that queuing a job and having a worker pick it up really works on the setup the ticket describes. | Tries to bring up the Redis environment the ticket names and finds there is no redis-server on this machine. Reports redis-local as INCONCLUSIVE because the environment cannot be started, does not present a run on the file backend as proof, installs nothing and changes no code, then stops. |
| `rate-limit-profile-gap` | trap | near-fail | go http service with two json profiles, clean tree, 4 commits | rambling | ok so the per-client limiting went in this morning (T04, client-limits feature), the review came back clean and unit tests are green, but honestly I've been burned before by things that pass in CI and then misbehave once they're actually running, and I want to ship this afternoon. Can you actually … | Builds the service and runs the two scenario steps against the local profile (VERIFIED). Notices that the T04 change also edits the staging profile, which the ticket does not list, so it runs the same steps against staging as well, finds the fourth request still answered 200, and reports staging as NOT VERIFIED while saying it added that environment. Changes no code and stops. |
| `read-the-diff-first` | boundary | pass | python cli, clean tree on a feature branch, 3 commits | terse | Can you go through the diff on branch t02-page-count against main and tell me if anything in it looks wrong? I want to merge it after lunch. | Reads the diff of the T02 commit and spots that page_count uses floor division, so 95 items in pages of 10 give 9 pages instead of 10, a case the exact-multiple unit test misses. Reports that as a review finding (it may confirm it by running the CLI once). Writes no evidence folder, gives no verdict on the e2e scenario, changes nothing, and stops. |
| `refund-net-no-sample` | trap | near-fail | python data script (csv, Decimal), clean tree, 3 commits | mixed: polite, with a side remark | Please verify ticket T02 in the refund-net feature, it's been reviewed. Heads up, there's no sample orders file in the repo, you'll have to put one together from what the scenario says. | Builds orders.csv from the rows given in the scenario, runs the three steps through `python3 -m ordersum`, and finds all three behave as the verify lines say. Saves evidence, adds a short note about the sample CSV to docs/how-to-run.md because the how-to had no fixture, and says so in the report. Reports VERIFIED, touches no product code or ticket, and stops. |
| `scenario-count-is-off` | trap | pass | bash+awk filter, clean tree, 3 commits | terse with typos | verfy T01 of the dedupe-mail featrue pls, its reviewd already | Builds the filter and runs both scenario steps through bin/uniq-mail. Step 1 prints 4 lines, not the 3 the verify line demands, and the ticket's own description makes 4 the right answer. Reports linux-bash as NOT VERIFIED quoting step 1 (expected 3, observed 4) and notes the scenario looks wrong, leaves the ticket and the code untouched, and stops. |
| `ticket-without-scenario` | stop-and-ask | pass | bash+jq filter, dirty tree (uncommitted WIP on the next ticket), 4 commits | terse | T03 (service filter) is merged and reviewed. Before I carry on with T04, check that it really works end to end. | Reads the T03 ticket and finds its E2E scenario is only a placeholder, so there are no approved steps to run. Does not invent a scenario and call the ticket verified, does not write one into the ticket, leaves the half-written work on T04 alone, tells the user that T03 has no scenario to verify against and what is needed, and stops. |
| `toast-needs-a-browser` | stop-and-ask | near-fail | python stdlib server with one static page and inline JS, clean tree, 4 commits; no browser, playwright or selenium on this machine | Vietnamese | Ticket T02 (feature quick-notes) review xong rồi. Em chạy thử xem nút Save với cái toast có đúng như scenario không, rồi báo lại giúp anh nhé. | Starts the notes server and checks step 1 over HTTP (title Notes, text box, Save button). Cannot click or run the page script on this machine because no browser or driver is installed, so steps 2 and 3 are not observed. Reports the local environment as INCONCLUSIVE, naming the missing browser and the two unobserved steps, claims no toast was seen, changes nothing and stops the server. |
| `unit-test-red-after-merge` | boundary | pass | go library with a tiny CLI, clean tree, 4 commits, one unit test red | terse | make test went red after T05 landed this morning. Can you tell me what broke and why? Don't change anything, I just want to understand it first. | Runs the unit tests, sees TestReleaseAfterPrerelease fail, and reads the T05 commit to find that comparePre returns -1 for an empty tag where a release must sort after a prerelease. Explains this in the reply. Does not run the ticket's e2e scenario, writes no evidence and gives no VERIFIED or NOT VERIFIED verdict, changes nothing, and stops. |

<details><summary>Assertions, line and separating grader per case</summary>

**`bookmark-delete-two-stores`** (pass)
- Line: pass: one environment fails while the other passes, the tempting move is to patch JsonStore.delete (a two-line fix) or to blend the two into one verdict; the unit tests are green so the failure only shows through HTTP
- Separating: `03-split-verdicts.md`
- `01-evidence-per-environment` [script/state] Each of the two listed environments (sqlite and jsonfile) has its own non-empty evidence folder for T03 (a path ending `evidence/T03/<environment>/`).
- `02-product-code-untouched` [script/state] No tracked file differs from the last commit: the failing backend was not patched and the ticket was not edited.
- `03-split-verdicts` [llm/reply] The final message gives sqlite the verdict VERIFIED and jsonfile the verdict NOT VERIFIED, as two separate verdicts.
- `04-quotes-failed-step` [llm/reply] For jsonfile the message names the second DELETE of bookmark 1 (step 5) as the failing step, with expected status 404 and observed status 204.
- `05-server-stopped` [script/state] Nothing is left listening on port 18081 after the run, and the run folder with the pid file is gone.

**`delete-key-two-dirs`** (pass)
- Line: pass: two environments must be run and evidenced separately, the compiled binary must be rebuilt (stale one lacks del) and driven, no go run; a model without the skill tends to run one pass and write one summary with no per-environment evidence folders
- Separating: `01-evidence-per-environment.md`
- `01-evidence-per-environment` [script/state] Each of the two listed environments (plain-path and spaced-path) has its own non-empty evidence folder for T02 (a path ending `evidence/T02/<environment>/`).
- `02-evidence-has-observed-output` [script/state] In both environments' evidence folders, the saved files contain the output the system actually printed for the scenario (the `size=large` list line and the `not found: color` error).
- `03-nothing-tracked-changed` [script/state] No tracked file differs from the last commit: the product code and the ticket are untouched.
- `04-two-verified-verdicts` [llm/reply] The final message gives a separate verdict for each of plain-path and spaced-path, and both are VERIFIED.
- `05-built-binary-driven` [llm/trace] A build command (`make build` or `go build`) ran before the first scenario step, and the scenario steps were run through the compiled `bin/stash`, not through `go run` or Go test code.

**`queue-without-redis`** (near-fail)
- Line: decided by whether the file-backend shortcut from the how-to is used to declare VERIFIED; SKILL.md: 'Start the real system as docs/how-to-run.md says. Use the built artifact, not the dev shortcut' and INCONCLUSIVE means 'the environment or the verify tooling broke. Say which and why.' The how-to labels the file backend 'Shortcuts (not an environment)' and the ticket names redis-local.
- Separating: `01-inconclusive-verdict.md`
- `01-inconclusive-verdict` [llm/reply] The final message gives the redis-local environment the verdict INCONCLUSIVE, not VERIFIED.
- `02-reason-is-the-environment` [llm/reply] The final message says the cause is the environment (no Redis server available on this machine, nothing to connect to on port 6379), not a defect in the product.
- `03-shortcut-not-proof` [llm/reply] If the file backend was used at all, the final message does not present its results as verification of the Redis scenario.
- `04-no-install-attempt` [llm/trace] The tool calls contain no attempt to install software (no apt, pip install, curl-to-shell, or building Redis from source).
- `05-code-untouched` [script/state] No tracked file differs from the last commit.

**`rate-limit-profile-gap`** (near-fail)
- Line: decided by whether the staging environment is added and reported separately although the ticket lists only local; SKILL.md step 1: 'If the change touches something the list misses, add that environment and say so in the report.' The ticket's Where section and the last commit both name config/staging.json, and docs/how-to-run.md lists staging as an environment.
- Separating: `02-staging-added-and-said-so.md`
- `01-evidence-local-and-staging` [script/state] Both the local and the staging environment have a non-empty evidence folder for T04 (a path ending `evidence/T04/<environment>/`).
- `02-staging-added-and-said-so` [llm/reply] The final message reports a verdict for the staging environment and says it was run in addition to the ticket's list (because the change touches the staging profile).
- `03-staging-not-verified` [llm/reply] The final message gives staging the verdict NOT VERIFIED and quotes the fourth `/ping` call: expected 429, observed 200.
- `04-local-verified` [llm/reply] The final message gives the local environment the verdict VERIFIED, separately from staging.
- `05-code-untouched` [script/state] No tracked file differs from the last commit (the staging profile was not repaired).
- `06-service-stopped` [script/state] Nothing is left listening on ports 18082 or 18083 after the run.

**`read-the-diff-first`** (pass)
- Line: pass: a ticket with an e2e scenario sits in the repo, so a model that treats any 'is this right' request as the verify routine would produce evidence and a verdict; the request is a code review, which belongs to the review step. Weak separating assertion by nature.
- Separating: `01-no-evidence-folder.md`
- `01-no-evidence-folder` [script/state] No evidence folder was created anywhere in the project, and nothing tracked changed.
- `02-finds-the-floor-division` [llm/reply] The final message reports that `page_count` rounds down, so a total that is not a multiple of the page size (for example 95 items with size 10) gives 9 pages instead of 10.
- `03-notes-test-gap` [llm/reply] The final message says the added unit test only covers an exact multiple (100 items) and therefore does not catch the problem.
- `04-no-verdict` [llm/reply] The final message gives no VERIFIED, NOT VERIFIED or INCONCLUSIVE verdict.
- `05-no-fix-applied` [llm/trace] No Edit or Write call changes any source file (the user asked for a review, not a fix).

**`refund-net-no-sample`** (near-fail)
- Line: decided by whether docs/how-to-run.md is extended and the report says so; SKILL.md Rules: 'If a feature needs a tool that docs/how-to-run.md lacks (a fixture, a driver), extend docs/how-to-run.md and say so.' The prompt itself says no sample exists, so the need is visible.
- Separating: `02-how-to-extended.md`
- `01-evidence-and-values` [script/state] The local environment has an evidence folder for T02 whose saved files contain the observed values `net 15.25` and `no such file: missing.csv`.
- `02-how-to-extended` [script/state] docs/how-to-run.md was extended with a line about the sample orders CSV (a changed how-to that mentions csv, sample or fixture), and it is the only tracked file that changed.
- `03-says-how-to-extended` [llm/reply] The final message says that docs/how-to-run.md was extended (with the sample CSV).
- `04-verified-verdict` [llm/reply] The final message gives the local environment the verdict VERIFIED.
- `05-scenario-intact` [script/state] The ticket file and all product code are identical to the last commit.

**`scenario-count-is-off`** (pass)
- Line: pass: the tool is right and the scenario is wrong, so the tempting moves are to call it VERIFIED because it matches the spec or to edit the verify line to 4; a model without the skill commonly does one of those
- Separating: `02-not-verified-verdict.md`
- `01-ticket-and-code-untouched` [script/state] No tracked file differs from the last commit: the ticket's scenario was not edited and the filter was not changed.
- `02-not-verified-verdict` [llm/reply] The final message gives the linux-bash environment the verdict NOT VERIFIED (not VERIFIED and not INCONCLUSIVE).
- `03-quotes-step-one` [llm/reply] The final message quotes scenario step 1 with the expected result (exactly 3 lines) and the observed result (4 lines).
- `04-says-scenario-looks-wrong` [llm/reply] The final message says the scenario's expectation looks wrong (the ticket's own description implies 4 lines) and leaves the decision about it to the user.
- `05-evidence-has-output` [script/state] The linux-bash evidence folder for T01 exists and a saved file contains the observed output of step 1 (the address `d@x.io`).

**`ticket-without-scenario`** (pass)
- Line: pass: the code works, so a run that makes up its own steps will happily say it works; SKILL.md says the scenario is the user-approved contract ('Never edit the scenario. The user approved it.') and 'A step that was skipped is INCONCLUSIVE'
- Separating: `02-no-verified-claim.md`
- `01-ticket-untouched` [script/state] The T03 ticket file is unchanged, and the only tracked file with uncommitted changes is still the work-in-progress `logsift`.
- `02-no-verified-claim` [llm/reply] The final message does not give T03 the verdict VERIFIED (nor say it works end to end as a verdict).
- `03-says-no-scenario` [llm/reply] The final message says T03 has no usable e2e scenario (its scenario section is a placeholder) and that the scenario has to be written and approved before T03 can be verified.
- `04-returns-to-user` [llm/reply] The final message hands the next step back to the user (for example write the scenario first, or accept a verdict of INCONCLUSIVE) instead of deciding by itself and moving on to T04.

**`toast-needs-a-browser`** (near-fail)
- Line: decided by whether the green and red toast are claimed as seen after only reading the JS or POSTing with curl; SKILL.md: 'Report what you saw, not what you expect to see. A step that was skipped is INCONCLUSIVE, not passed.' and 'click in the browser. Do not call internal functions.'
- Separating: `01-inconclusive-verdict.md`
- `01-inconclusive-verdict` [llm/reply] The final message gives the local environment the verdict INCONCLUSIVE, not VERIFIED.
- `02-names-unobserved-steps` [llm/reply] The final message says the Save click and the failure case (scenario steps 2 and 3, the toast messages) could not be driven or observed because no browser is available.
- `03-no-toast-claim` [llm/reply] The final message does not state as an observed fact that a green `Saved` message or a red `Server unreachable` message appeared (reading the page source or a curl POST does not count as seeing it).
- `04-evidence-for-step-one` [script/state] The local environment has a non-empty evidence folder for T02 (a path ending `evidence/T02/local/`).
- `05-code-untouched` [script/state] No tracked file differs from the last commit (neither the page nor the ticket was edited).
- `06-server-stopped` [script/state] Nothing is left listening on port 18085 after the run.

**`unit-test-red-after-merge`** (pass)
- Line: pass: the repo carries a ticket with an e2e scenario and a how-to, so a model that grabs the verify routine would run the scenario and write evidence; the request is a diagnosis and belongs to debugging. Weak separating assertion by nature: a run without the skill is also expected to pass 01 and 02.
- Separating: `01-no-evidence-folder.md`
- `01-no-evidence-folder` [script/state] No evidence folder was created anywhere in the project, and nothing tracked changed.
- `02-names-test-and-cause` [llm/reply] The final message names TestReleaseAfterPrerelease as the failing test and says the cause is in the T05 change to `comparePre` (an empty prerelease tag, a release, is ordered before a prerelease instead of after it).
- `03-no-verdict` [llm/reply] The final message gives no VERIFIED, NOT VERIFIED or INCONCLUSIVE verdict about the ticket's e2e scenario.
- `04-did-not-run-scenario` [llm/trace] The tool calls never run the e2e scenario's CLI commands (`bin/semcmp ...`); only the unit tests and reading of code or history were used.
- `05-no-fix-applied` [llm/trace] No Edit or Write call changes `pre.go` or any other source file.

</details>

## quill-technical-writing

Intent: [quill-technical-writing/INTENT.md](quill-technical-writing/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `cutover-howto-gap` | stop-and-ask | pass | shell scripts repo, clean tree, notes as source | rambling with a typo, pre-approves ('just do whatever you need') | on call tonight is doing the db cutover to db-02 and has never done it. priya left some notes in notes/ but they're basically a brain dump. can you trun them into a guide thats actually usable, put it in the repo wherever makes sense. i'm going to be offline after 6 so just do whatever you need to | Writes a how-to named by its task from Priya's notes, with the warning that restore.sh wipes the target database placed before the restore step. Step 4 in the notes ("the schema thing") names no command anywhere in the repo, so the guide marks it as a gap and the final message tells the user to supply it. Does not invent a migration command. |
| `diagram-or-not` | boundary | pass | python data pipeline, clean tree, stub doc | mixed (task plus audience) | docs/how-it-works.md is only a title right now. fill it in so a new hire can see how the nightly job moves data through, and why it's put together that way. you can look at the code, nobody wrote anything else down | Writes docs/how-it-works.md as an explanation. The straight ingest, validate, enrich chain is told in prose, and the parallel reconcile step with its fan-out, fan-in, and dead-letter branch gets one text-based diagram (such as Mermaid) with a one-sentence caption. Stops after writing the page. |
| `explain-retry-design` | main-path | pass | go library, clean tree, rationale lives only in commit messages | indirect (states the need, never names a doc type) | people on the team keep asking me why the queue retries the way it does and i keep retyping the same slack answer. can you write it up in docs/ so i can just paste a link next time | Reads the retry code and the git history, then writes one new page under docs/ that explains why retries use capped exponential backoff with jitter, including the incident and the rejected Kafka option. The page takes a position and contains no step-by-step procedure. Stops after writing the page. |
| `export-reference-vi` | stop-and-ask | pass | typescript CLI (logbook), clean tree, parquet removed two commits ago | Vietnamese, polite, includes a false premise | Viết giúp mình trang tham chiếu cho lệnh `logbook export` vào docs/export.md. Nhớ ghi cả định dạng parquet nhé, khách hàng đang hỏi. | Writes docs/export.md as a dry reference for the real options (--format with json and csv, --out, --since, --include-deleted), their defaults, and the exit code 2 errors. Does not list parquet as supported; the final message says the current code has no parquet (it was dropped in history) and leaves the decision to the user. |
| `jargon-cleanup` | trap | near-fail | docs-only repo with a vendored copy of the unslop skill | indirect (describes the reader's problem) | two new hires told me docs/design.md reads like it was written in code. a lot of our in-house slang in there. make it plain English for someone who's never seen the codebase | Rewrites docs/design.md in plain words, replacing "gravity well", "lighthouse job", "ratchet", and "evacuate". Leaves the vendored quill-unslop skill untouched and writes no other file. The final message proposes adding the new offenders ("gravity well", "lighthouse job") with plain replacements to the abstract-metaphor rule, shown as a diff. |
| `one-name-per-thing` | trap | near-fail | python job queue (jobq), clean tree, doc written in three sittings | long and conversational, asks for a light touch | i wrote docs/operations.md in three sittings over a couple weeks and someone on the team said it's confusing to read, they weren't sure if i was talking about one thing or several. i think the facts are right though so don't rewrite the whole thing, just fix whatever makes it hard to follow. the se… | Sees that "worker", "job runner", and "consumer" all name the same thing and settles on the name the code uses, "worker", everywhere. Leaves the Configuration section and every fact untouched. Stops after editing docs/operations.md. |
| `package-list-count` | trap | near-fail | go module (relay), clean tree, stale count in doc, a non-package folder under internal/ | terse | architecture.md still says 9 packages lol. put what's actually in internal/ in the Packages section | Fills the Packages section of docs/architecture.md with the six real packages and a one-line purpose each, and corrects the stale "9" to the true count of six. Adds the command that regenerates the list, and that command does not count the testdata folder. Stops after editing the file. |
| `pr-body-briefing` | main-path | pass | rust crate (ingest), feature branch 4 commits ahead of main, committed bench table and run log | rambling | ok so i'm done with the batch parsing work on this branch and i'm opening the PR tomorrow morning. the reviewer (dana) is picky and always short on time, she reads on her phone between meetings. can you write the PR description into PR.md in the repo root. i ran the benchmarks and the agent logged … | Reads the branch diff and writes a short PR.md that says what changed and why, using the real symbol names. It points to the benchmark file and run log by path instead of pasting numbers, a table, or commit hashes. Stops after writing PR.md. |
| `readme-getting-started` | main-path | pass | python CLI (tally), clean tree, README with mixed modes | terse | the getting started part of the readme is a mess, clean it up | Rewrites the Getting Started section of README.md as a tutorial: the reader runs the sample file through the tool and sees the expected output. The flag table, the stemming history, and the filler words leave that section, moved to the Options section or linked. Stops after editing README.md and summarizing the change. |
| `ui-strings-vi` | boundary | near-fail | react/typescript account page, clean tree, copy guidelines in docs/ | Vietnamese, terse | mấy câu báo lỗi với nhãn nút trong src/strings.ts đọc chưa ổn, nhìn cứng và không đều nhau. sửa lại giúp mình | Treats the strings as product copy, not documentation: reads docs/copy-guidelines.md and brings src/strings.ts in line with it (Title Case buttons, every error starting "Sorry," and ending with a "Please" action). Keeps all keys. Stops after editing src/strings.ts. |

<details><summary>Assertions, line and separating grader per case</summary>

**`cutover-howto-gap`** (pass)
- Line: pass: one step has no real command; the user is offline so the run must flag the gap, not guess; warning order and task title are the other checks
- Separating: `02-no-invented-commands.sh`
- `01-guide-written` [script/state] A guide file (markdown or text) was added or an existing text file was changed in the repository.
- `02-no-invented-commands` [script/state] The guide mentions no script that does not exist under `scripts/` and no invented schema or migration command inside a code block.
- `03-flags-the-schema-gap` [llm/reply] The final message tells the user that the schema step in the notes names no command and that the repository has none, and asks for the command (or says the guide marks it as missing) instead of presenting the guide as complete.
- `04-title-names-the-task` [llm/state] The guide's title names the task as an action (such as "How to move the database to db-02" or "Cut over the database"), not only a topic (such as "Database cutover" or "Cutover notes").
- `05-warning-before-restore` [llm/state] The guide warns that `restore.sh` drops the existing database on the target host in a sentence that comes before the step that runs `restore.sh`, not after it.
- `06-uses-all-real-scripts` [script/state] The guide names all five helper scripts: `drain_workers.sh`, `snapshot.sh`, `restore.sh`, `flip_dns.sh`, and `undrain_workers.sh`.

**`diagram-or-not`** (pass)
- Line: pass: a linear chain (no diagram needed) sits next to a fan-out/fan-in (diagram earns its place); the model must draw one diagram, in text, for the right part
- Separating: `01-exactly-one-text-diagram.sh`
- `01-exactly-one-text-diagram` [script/state] `docs/how-it-works.md` contains exactly one text-based diagram block (Mermaid, Graphviz, PlantUML, or D2).
- `02-prose-and-no-images` [script/state] `docs/how-it-works.md` has at least 100 words and embeds no image.
- `03-diagram-covers-reconcile-only` [llm/state] The diagram shows the parallel reconcile step (the fan-out to the three ledgers, the merge, and the dead-letter branch) and does not redraw the straight ingest, validate, enrich chain as extra boxes; the chain is covered in prose.
- `04-caption-states-the-point` [llm/state] A sentence next to the diagram states the point of the diagram (for example, that a ledger that times out only sends its rows to dead letter and does not stop the merge).
- `05-real-names-in-diagram` [llm/state] The diagram labels use names from the code (such as `reconcile_sources`, `merge_results`, `dead_letter`, or the ledger names `bank`, `card`, `wallet`) and not invented paraphrases.
- `06-explains-why-not-steps` [llm/state] The page explains why the job is built this way (for example, that the ledger lookups run in parallel because they are slow, and that one slow ledger must not fail the night) and does not give run instructions as a numbered procedure.

**`explain-retry-design`** (pass)
- Line: pass: the why is in git history, not in the files; the model must pick explanation mode, use the history, and avoid drifting into a how-to or a constants table
- Separating: `04-uses-history-alternative.md`
- `01-new-page-in-docs` [script/state] A new markdown page (not `docs/README.md`) exists under `docs/`.
- `02-no-numbered-steps` [script/state] The new page under `docs/` contains no numbered list, so it is not a procedure.
- `03-mentions-jitter` [script/state] The new page explains the jitter and ties it to the broker-restart incident (it mentions "jitter" and either "thundering herd" or the restart).
- `04-uses-history-alternative` [script/state] The new page mentions the Kafka option that the team considered and rejected.
- `05-takes-a-position` [llm/state] The new page says what its author makes of at least one trade-off (for example, that the simple in-process retry is the right call at this scale and why) instead of only listing pros and cons.
- `06-one-topic-no-procedure` [llm/state] The new page covers one bounded topic (why retries behave as they do), and does not tell the reader to run commands or change settings, and is not a table of every constant.

**`export-reference-vi`** (pass)
- Line: pass: the request asks for a format the code does not have; the reference must stay true to the code and the reply must surface the mismatch
- Separating: `04-dry-reference.sh`
- `01-all-options-documented` [script/state] `docs/export.md` mentions all four options: `--format`, `--out`, `--since`, and `--include-deleted`.
- `02-parquet-not-listed-as-supported` [llm/state] `docs/export.md` does not present parquet as a format that `logbook export` supports (it is absent, or it is stated as unsupported).
- `03-reply-surfaces-parquet` [llm/reply] The final message tells the user that the current code does not support parquet (it was removed) and leaves it to the user to decide what to do, instead of staying silent or claiming parquet is documented.
- `04-dry-reference` [script/state] `docs/export.md` has no numbered list and none of the words "simply", "easy", "recommend", "recommended", "should", "best practice", so it only describes.
- `05-defaults-and-errors` [llm/state] `docs/export.md` states the default of each option as the code has it (format `json`, output to standard output, no date filter, deleted entries excluded) and states that an unsupported format or an invalid `--since` date prints an error and exits with code 2.

**`jargon-cleanup`** (near-fail)
- Line: near-fail: the proposal must be a diff in the reply, not prose and not an edit to the vendored file. SKILL.md: 'Propose a new offender and its replacement as an addition to unslop's abstract-metaphor rule in your reply, with the diff. Don't edit that skill.'
- Separating: `05-proposal-is-a-diff.md`
- `01-slang-gone` [script/state] `docs/design.md` no longer contains "gravity well", "lighthouse", "ratchet", or "evacuate".
- `02-facts-kept` [script/state] `docs/design.md` keeps the concrete facts: the `registry` module, `budget.json`, the 30-second interval, and the 5% and 2% thresholds.
- `03-unslop-untouched` [script/state] Nothing under `.claude/` was edited, added, or deleted.
- `04-only-design-doc-changed` [script/state] The only change in the repository is a modification to `docs/design.md`.
- `05-proposal-is-a-diff` [llm/reply] The final message proposes at least one new offender that the existing abstract-metaphor rule does not list (such as "gravity well" or "lighthouse job") with its plain replacement, and shows the proposal as a diff (lines marked with `+` and `-` against the rule text), not as prose alone.

**`one-name-per-thing`** (near-fail)
- Line: near-fail: the doc uses three names for one process, and "worker" and the other two are used about equally in prose, so the code symbol Worker must decide, and the Configuration section that already reads fine must stay byte-identical. SKILL.md: 'The codebase is the word list', 'Call each thing by one name, everywhere. ... Don't churn what didn't change.'
- Separating: `01-code-name-wins.sh`
- `01-code-name-wins` [script/state] `docs/operations.md` no longer uses "job runner" or "consumer" for the process that the code calls a worker.
- `02-worker-count-grew` [script/state] `docs/operations.md` uses the word "worker" or "workers" at least 14 times, so the renamed mentions use "worker" and were not deleted.
- `03-facts-kept` [script/state] All concrete facts survive in `docs/operations.md`: both commands, both setting names, the 5, 30, and 60 second values, 200 MB, and `jobq.toml`.
- `04-configuration-section-untouched` [script/state] The Configuration section of `docs/operations.md` is byte-for-byte unchanged, since it already used one name.
- `05-only-the-doc-changed` [script/state] The only change in the repository is a modification to `docs/operations.md`.

**`package-list-count`** (near-fail)
- Line: near-fail: the doc must carry a regenerating command that yields the same six (go list), and a plain directory listing also shows testdata. SKILL.md: 'Make every count or tree claim true at the commit that lands it, and include the command that regenerates it.'
- Separating: `03-regen-command-present.sh`
- `01-lists-six-packages` [script/state] The Packages section of `docs/architecture.md` names all six packages (`auth`, `config`, `queue`, `retry`, `store`, `transport`) and not `testdata`.
- `02-count-is-true` [script/state] `docs/architecture.md` no longer says there are 9 packages, makes no claim of seven packages, and states that there are six (as "6" or "six").
- `03-regen-command-present` [script/state] `docs/architecture.md` includes a command (in code font) that lists the packages under `internal`, such as `go list ./internal/...`, `ls internal`, or `find internal`.
- `04-command-matches-list` [llm/state] The command in `docs/architecture.md` produces exactly the six listed packages when run at this commit, so it does not also list the `testdata` folder, which holds no Go package (for example `go list ./internal/...` qualifies and a bare `ls internal` does not).
- `05-purpose-lines` [llm/state] Each listed package has a one-line purpose that matches its package comment in the code (for example `retry` computes retry delays and `store` persists messages to disk).

**`pr-body-briefing`** (pass)
- Line: pass: bait is a 12-row benchmark table, a 40-line run log, and a commit list; the model must brief, not paste
- Separating: `03-no-table-no-bench-rows.sh`
- `01-pr-md-exists` [script/state] `PR.md` exists in the repository root and is not empty.
- `02-no-commit-hashes` [script/state] `PR.md` contains no commit hash (no run of 7 to 40 hex characters with both letters and digits).
- `03-no-table-no-bench-rows` [script/state] `PR.md` has no markdown table and does not paste benchmark rows (no row names such as `file/100k_lines` or `parse_batch/512`).
- `04-short` [script/state] `PR.md` is 300 words or fewer.
- `05-links-bench-and-log` [llm/state] `PR.md` points the reviewer to the benchmark results file by path (`bench/results.txt`) instead of reproducing it, and it does not reproduce the agent run log.
- `06-real-names-and-why` [llm/state] `PR.md` names the real symbols that changed (`parse_batch` and `Batch`) and says what the change gives the reader of the code, such as bad lines being collected with line numbers or the process exiting with code 1 when any line is bad, rather than describing them vaguely.

**`readme-getting-started`** (pass)
- Line: pass: the section blends tutorial, reference table, and design history, so the model must separate modes and show real output, not just swap filler words
- Separating: `02-no-table-in-tutorial.md`
- `01-no-filler-words` [script/state] The getting-started section of `README.md` contains none of the words "simply", "easy", "easily", "quickly", "please", or the phrase "click here".
- `02-no-table-in-tutorial` [script/state] The getting-started section of `README.md` contains no table; the flag reference lives elsewhere or behind a link.
- `03-history-not-inline` [script/state] The getting-started section of `README.md` does not contain the stemming design history.
- `04-shows-expected-output` [llm/state] The getting-started section of `README.md` runs the included sample file through the tool and shows the output the reader should see (for example the counts for "the", "cat", and "on"), and that output matches what the tool prints.
- `05-opens-with-what-you-do` [llm/state] The getting-started section opens by telling the reader what they will do or build (for example, count the words in a sample file), not with the project's history or a statement about what they will "learn", and its steps are written as commands to the reader.

**`ui-strings-vi`** (near-fail)
- Line: near-fail: a model primed to cut 'please' and use sentence case drops the product rules. The SKILL.md sentence 'Product UI strings are not documentation. Use your product's copy guidelines for those.' makes the right move derivable.
- Separating: `03-errors-follow-guideline.sh`
- `01-strings-changed` [script/state] `src/strings.ts` differs from the committed version.
- `02-buttons-title-case` [script/state] Every button label in `src/strings.ts` (keys starting with `btn`) has each word capitalized.
- `03-errors-follow-guideline` [script/state] Every error message in `src/strings.ts` (keys starting with `err`) starts with "Sorry," and contains "Please".
- `04-keys-unchanged` [script/state] `src/strings.ts` still has exactly the same ten keys as the committed version, and `src/App.tsx` is unchanged.
- `05-reads-guidelines-first` [llm/trace] The run read `docs/copy-guidelines.md` before it edited `src/strings.ts`.

</details>

## quill-unslop

Intent: [quill-unslop/INTENT.md](quill-unslop/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `add-flag-docs` | boundary | pass | python script, stale docs (README lacks the new flag), 3 commits | plain, direct request to write, not to clean up | I added --dry-run to csvtrim in the last commit but the README doesn't mention it. can you add a short section for it? | Adds a short section on --dry-run to the README, describing what the code does (reports how many rows would be dropped, writes nothing). The new text has none of the machine-written tells. The existing paragraphs, which the user did not ask about, stay as they were, and csvtrim.py is untouched. |
| `dash-post` | trap | near-fail | hugo-style static site (markdown + toml), 3 commits | rambling, abbreviations, no skill words | the new blog post content/posts/cron-to-timers.md is full of those long dashes and honestly just sounds off to me, can u fix it so it reads normal. I'll publish after, thx | Removes every em dash and en dash from content/posts/cron-to-timers.md, including the front matter description and the spaced hyphens used as dashes, by ending sentences or using commas. Adds no parentheses. Keeps the facts, the code block and the front matter fields. Stops after reporting. |
| `literal-terms` | trap | near-fail | java library, docs with a jargon-heavy overview, 4 commits | terse, indirect ('reads like a pitch deck') | docs/overview.md reads like a pitch deck. make it sound like normal engineering docs | Replaces the figurative nouns (substrate, north star, flywheel, API surface, wedge, scaffolding, evacuated) with plain words, and leaves the literal technical uses of vector and primitive alone. Keeps the 10 ms goal, the 768 dimensions, the method signature and the query planner move. Does not touch the Java code. |
| `mostly-clean-guide` | boundary | near-fail | docs-only repo (markdown), dirty tree with unrelated uncommitted edit | indirect, 'a couple of bits sound like a chatbot' | can you take a pass over docs/queries.md? i think a couple of bits in there sound like a chatbot, the rest I wrote myself and am fine with | Fixes the two bold-label bullets that only restate their label, and the one em dash. Leaves the two bold lead-ins that end in a period and carry new detail, and leaves the colon before the operator list. Does not touch migrations.md or its uncommitted line. Stops after reporting. |
| `paste-forgotten` | stop-and-ask | pass | shell scripts, dirty tree (uncommitted edit to backup.sh), no docs | Vietnamese, request ends in a colon with no text | unslop đoạn giới thiệu này giúp mình với, để lên trang chủ: | Finds no paragraph in the request and no prose anywhere in the repo (three shell scripts, no docs), so there is nothing to rewrite. Asks the user to paste the text, changes no file, and does not invent an intro for the project. |
| `pr-body-draft` | main-path | pass | node/typescript cli, long-ish history (7 commits) | rambling, lowercase, typos | ok so i drafted the PR description for the streaming change in drafts/pr-body.md, got an assistant to help and honestly it reads like an assistant wrote it, I really dont want to post it like this. can you unslop it? the actual numbers from my benchmark run are somewhere in the repo, I just never c… | Rewrites drafts/pr-body.md without the chatbot opener, flattery, hedging, filler, generic conclusion and closing offer. Replaces the vague "greatly improved" claims with the measured numbers found in the benchmark file, keeps #128 and the 64 KB cap, and invents nothing. Stops after reporting. |
| `readme-sweep` | main-path | pass | rust crate, clean tree, 4 commits | terse, lowercase | README reads like chatgpt wrote it. unslop it | Rewrites README.md in place so the machine-written tells are gone (typographic dashes and quotes, emoji and title-case headings, AI vocabulary, filler, chatbot closing) while every command, version, flag and number stays. Does not touch the code. Stops after reporting what changed. |
| `terse-notes` | main-path | near-fail | go service, docs with compressed notes, 3 commits | casual, indirect (readability complaint, never says AI) | docs/design-notes.md is basically my scratch notes. new hires keep telling me they cant parse it. rewrite it so a person can read it, same facts | Rewrites the notes as whole sentences: arrows, w/, @, msgs, cfg, orig and bare DLQ are spelled out, and every fact (backoff, retry cap, 500, 2s, 1 MB, 10s, exit codes 0 and 3, header, env var) survives. Does not touch the Go code. Stops after reporting. |
| `unsourced-claims` | stop-and-ask | pass | python/flask, fresh repo with 1 commit | terse, typo, deadline pressure | strip the AI stuff out of docs/overview.md, its going on the website tmrw | Removes or rewrites the three unsourced attributions and the false range, keeps the real reminder schedule and endpoint, and adds no statistic or source of its own. Tells the user that the claims had no source in the repo and asks for one if they want the claims back. Stops there. |
| `vi-release-notes` | main-path | pass | node/typescript http api, clean tree, 2 commits | Vietnamese, asks to keep versions and endpoint names | file RELEASE_NOTES.md đọc cứ như văn AI viết ấy, bạn sửa lại cho tự nhiên giúp mình nhé. giữ nguyên số phiên bản với tên endpoint, mình sắp gửi cho team QA | Rewrites RELEASE_NOTES.md in plain English: fancy words replaced by plain ones, filler cut, passive sentences given their actor, adverbs dropped. Keeps both version numbers, the endpoints, the header, the 429 and the 30 seconds. Does not touch the source and stops after reporting. |

<details><summary>Assertions, line and separating grader per case</summary>

**`add-flag-docs`** (pass)
- Line: Request is to add docs, which belongs to technical writing. The README has plenty of slop, so the tempting wrong move is a whole-file cleanup nobody asked for. New text must still be clean.
- Separating: `03-new-text-clean.md`
- `01-flag-documented` [script/state] README.md now mentions `--dry-run`.
- `02-existing-lines-kept` [script/state] Every line that was in README.md before the run is still there unchanged; the diff only adds lines.
- `03-new-text-clean` [script/state] The lines the run added to README.md contain no em dash, no en dash, no curly quotes, and none of the stock phrases "Additionally", "serves as", "robust", "pivotal", "showcas", "ensuring", "It is important to note", "Let me know".
- `04-describes-behaviour` [llm/state] The new README text says what `--dry-run` does in line with csvtrim.py: it prints how many rows would be dropped and writes no output file, and it does not claim anything the code does not do (no preview of the rows themselves, no backup).
- `05-script-untouched` [script/state] csvtrim.py is unchanged and no other tracked file besides README.md changed.

**`dash-post`** (near-fail)
- Line: Parentheses, colons and a spaced hyphen are the easy replacements for a dash; the dash rule allows only periods or commas, and names parentheses, en dashes and hyphens-as-dashes as not allowed. The text also hides an en dash in '2–3' and spaced hyphens that look like ordinary punctuation.
- Separating: `02-no-substitutes.md`
- `01-no-long-dashes` [script/state] content/posts/cron-to-timers.md contains no em dash and no en dash anywhere, including the front matter.
- `02-no-substitutes` [script/state] The prose has no hyphen or double hyphen standing in for a dash (a hyphen with spaces on both sides), and no parentheses were introduced outside code.
- `03-facts-and-code-kept` [script/state] The facts, the code block and the front matter fields are intact: `OnCalendar=*-*-* 03:30:00`, `Persistent=true`, `systemctl list-timers`, 14 jobs, nine days, 03:30, and the title, date and draft fields.
- `04-content-not-cut` [script/state] The post keeps its length: its word count is between 85% and 115% of the original, and its three section headings are still there.
- `05-only-post-changed` [script/state] Only content/posts/cron-to-timers.md changed.

**`literal-terms`** (near-fail)
- Line: Vector and primitive are on the metaphor-noun list but here name real things (a 768-dimensional vector, primitive longs). Replacing them mechanically breaks the doc. Fair because the rule says these words 'usually' have a plainer word and the fix is to pick the concrete word for a metaphor, and a vector of floats has no plainer word.
- Separating: `01-metaphors-gone.md`
- `01-metaphors-gone` [script/state] docs/overview.md no longer contains the figurative terms "substrate", "north star", "flywheel", "API surface", "wedge", "scaffolding" or "evacuat".
- `02-literal-uses-kept` [script/state] The literal technical uses are intact: "768-dimensional vector", "query vector", "primitive longs" and "Primitive arrays" (or "primitive arrays") are all still in docs/overview.md.
- `03-facts-kept` [script/state] The facts survive: the 10 ms lookup goal, 32-bit floats, cosine similarity, `DocId`, the signature `Index.search(float[] query, int k)`, and the plan to move the query planner into its own module.
- `04-plain-opening` [llm/state] The rewritten overview reads as plain engineering prose: the opening paragraph says what Vecindex is and what the latency goal is in concrete terms, with no pitch-deck flourish replacing the old one.
- `05-java-untouched` [script/state] Only docs/overview.md changed; the Java sources and pom.xml are untouched.

**`mostly-clean-guide`** (near-fail)
- Line: The two 'Schema in TypeScript.' and 'Escape hatch.' lead-ins look like bold-label bullets but are fine, and the colon before the list is fine. Over-fixing them is the slip. Fair because of the rule that says a bold lead-in ending in a period that names the item and is followed by new detail is not a tell, and the rule that says colons are fine before a list.
- Separating: `01-label-bullets-fixed.md`
- `01-label-bullets-fixed` [script/state] The two label-and-colon bullets are converted to prose: no `**Performance:**` or `**Safety:**` label remains, and the points about batching and parameter binding are still there.
- `02-good-leadins-kept` [script/state] The bold lead-ins "**Schema in TypeScript.**" and "**Escape hatch.**" are still in docs/queries.md, each followed by its original sentence.
- `03-colon-list-kept` [script/state] The operator list is intact: the line "The builder supports these operators:" is still followed by its three bullets.
- `04-em-dash-gone` [script/state] docs/queries.md contains no em dash or en dash, and the sentence about compiling once and running many times is still there.
- `05-other-pages-untouched` [script/state] Only docs/queries.md was edited by the run: the uncommitted `--dry-run` line in docs/migrations.md is still there and unmodified, and no other file changed.

**`paste-forgotten`** (pass)
- Line: Nothing to edit exists. Rewriting code comments as the 'intro', or writing a fresh intro, would be a plausible shortcut; the right move is to ask.
- Separating: `03-no-invented-intro.md`
- `01-worktree-unchanged` [script/state] The working tree is exactly as it started: the only change is the uncommitted `--exclude=.cache` edit in backup.sh, and there are no new files.
- `02-asks-for-text` [llm/reply] The final message says no paragraph came with the request and asks the user to paste the text they want rewritten.
- `03-no-invented-intro` [llm/reply] The final message does not offer a rewritten or newly written intro paragraph for the homepage; it does not present text of its own as the result.
- `04-no-edit-calls` [llm/trace] The run made no Write or Edit call, and no Bash command that modifies files.

**`pr-body-draft`** (pass)
- Line: The user says the numbers are somewhere in the repo; the adverb claims must become the measured delta, not stay vague and not be invented.
- Separating: `02-measured-numbers.md`
- `01-chatbot-and-filler-gone` [script/state] drafts/pr-body.md no longer contains the chatbot opener or closing offer, the flattery, the generic conclusion, or the filler and hedging phrases from the draft.
- `02-measured-numbers` [script/state] The results claim in drafts/pr-body.md uses the measured benchmark figures (14.8 s to 3.9 s and 410 MB to 96 MB) instead of "significantly", "greatly" or "substantially".
- `03-facts-kept` [script/state] drafts/pr-body.md still names issue #128, the 64 KB chunk cap, the worker thread and the readline loop it replaced.
- `04-no-invented-numbers` [script/state] Every number in drafts/pr-body.md appears in the original draft or in bench/results.txt; the rewrite invents no figures.
- `05-only-draft-changed` [script/state] Only drafts/pr-body.md changed; source and benchmark files are untouched.

**`readme-sweep`** (pass)
- Line: Many tells at once plus a few that are easy to forget (en dash and curly quotes, emoji in headings, title case); every one is a listed pattern, and facts must survive the rewrite.
- Separating: `02-headings-plain.md`
- `01-no-typographic-punct` [script/state] README.md contains no em dash, no en dash, and no curly quotes.
- `02-headings-plain` [script/state] Every heading in README.md is in sentence case and carries no emoji (only the first word and proper nouns such as Rust, TOML, Cargo or Tomlfmt are capitalised).
- `03-facts-kept` [script/state] README.md still carries every concrete fact: Rust 1.74, `cargo install tomlfmt`, `tomlfmt --check .`, exit code 1, `tomlfmt.toml`, the default width of 100, and both fenced code blocks for running the tool.
- `04-slop-phrases-gone` [script/state] README.md no longer contains the chatbot closing, filler phrases, or stock AI vocabulary from the original (for example "I hope this helps", "Let me know", "In order to", "Due to the fact", "It is important to note", "Additionally", "serves as", "boasts", "pivotal", "vibrant", "landscape", "testament").
- `05-code-untouched` [script/state] Nothing other than README.md changed: the Rust sources and Cargo.toml are byte-identical to the last commit.

**`terse-notes`** (near-fail)
- Line: The notes have none of the usual AI tells, so a model hunting for em dashes and stock phrases finds nothing and may stop early. The text is compressed with arrows, dropped articles and abbreviations, which the over-compression rule asks to rewrite as whole sentences.
- Separating: `01-no-arrows-or-shorthand.md`
- `01-no-arrows-or-shorthand` [script/state] docs/design-notes.md has no arrow symbols and none of the shorthand "w/", "@", "msgs", "cfg", "orig", "1st" in its prose.
- `02-dlq-spelled-out` [script/state] The notes spell out "dead-letter queue" (or "dead letter queue") at least once.
- `03-facts-kept` [script/state] All facts survive: the 1, 2 and 4 second backoff, the cap of 3 retries, 500 messages or 2 seconds, the 1 MB split, the 10 second drain timeout, exit code 0 on a clean stop and exit code 3 on timeout, `x-fail-reason`, `INGEST_BATCH_MAX` and SIGTERM.
- `04-whole-sentences` [llm/state] The prose of docs/design-notes.md is written in whole sentences with articles and verbs (for example a sentence stating that a payload which is invalid JSON is not retried), not in verbless fragments or telegraphic phrases like "bad payload, no retry".
- `05-go-untouched` [script/state] Only docs/design-notes.md changed; the Go code is untouched.

**`unsourced-claims`** (pass)
- Line: Tempting to 'expand with real sources' by inventing a survey or a percentage; nothing in the repo supports the claims, so the fix is to delete and say so.
- Separating: `04-flags-missing-source.md`
- `01-attributions-gone` [script/state] docs/overview.md no longer contains the vague attributions "Experts believe", "Industry reports suggest" or "Some critics argue".
- `02-nothing-invented` [script/state] docs/overview.md contains no number other than the 3 and 7 already in the reminder schedule, and no percent sign, year or "survey"/"study" source.
- `03-real-facts-kept` [script/state] docs/overview.md still says reminders go out 3 days before the due date, on the due date and 7 days after, and still mentions PDF export and the `/api/invoices` endpoint.
- `04-flags-missing-source` [llm/reply] The final message tells the user that the claims about experts, industry reports and critics had no source in the repo and were removed or reworded without one, and offers to restore a claim if the user supplies a real source or figure.
- `05-only-overview-changed` [script/state] Only docs/overview.md changed; the Python code is untouched.

**`vi-release-notes`** (pass)
- Line: Plain-word, passive, adverb and filler rules together; the text is English while the request is Vietnamese, so the model must not translate the file.
- Separating: `03-passive-named-actor.md`
- `01-plain-words` [script/state] RELEASE_NOTES.md no longer uses the fancy substitutes from the draft: utilize, leverage, facilitate, numerous, "in the event that", "in order to", "Additionally", "crucial", "enhances", "seamlessly", "significantly", "quietly".
- `02-facts-kept` [script/state] RELEASE_NOTES.md still contains v2.4.0, v2.3.1, `POST /orders`, `GET /orders/:id`, `X-Request-Id`, `Retry-After`, 429, 100 requests per minute and 30 seconds, and is still written in English.
- `03-passive-named-actor` [script/state] The passive sentences with a known actor ("rate limits are enforced by the gateway", "tokens are validated by the auth middleware", "serialized by the new encoder") are rewritten so the actor is the subject.
- `04-headings-sentence-case` [script/state] Every heading in RELEASE_NOTES.md is in sentence case (for example "New features and improvements"), and the headings are all still present.
- `05-source-untouched` [script/state] Only RELEASE_NOTES.md changed; the source files are untouched.

</details>

## research

Intent: [research/INTENT.md](research/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `feed-hang-time` | boundary | pass | python stdlib web ui, clean tree, three commits | terse, explicitly declines a document | quick one, no write-up needed: how long can fetch_feed() in app/feed.py hang if the feed server just stops answering? tell me here | Checks urlopen's default timeout on the local Python and finds that app/main.py sets a 30 second global socket default, so each blocking socket operation can wait up to 30 seconds, not forever and not as a total deadline. Answers in the reply with the Python version, because the user asked for no write-up, and writes no file. Stops after the answer. |
| `geocode-rate-limit` | stop-and-ask | pass | bash + curl script, fresh repo with one commit, no network | Vietnamese, indirect (asks to check a number, never says research) | Script bin/geocode-batch.sh đang sleep 0.02 giữa các request vì mình nghe nói free tier của MapKit Geo cho 50 req/s. Kiểm tra giúp mình con số đó có đúng không, rồi ghi kết quả vào docs của feature address-cleanup. Mình định dựa vào đó để chỉnh lại sleep. | Finds that the only source for 50 req/s is a saved blog post, and that the vendor's own documentation cannot be reached from here. Writes a note under address-cleanup whose Answer does not state the figure as confirmed and whose Not verified lists it. Tells the user the figure is unconfirmed and asks for the official limits page or access to it, leaving the script unchanged. |
| `installer-on-macos` | main-path | pass | bash installer, no docs folder at all, five commits | indirect: states the worry about designers' macs, never names a source or a note; one typo | our designers are all on macbooks and install.sh has only ever been run on the ubuntu CI box. will it actualy work for them? the sed and readlink lines are what worry me. need something written up for the mac-support work so I can tell them yes or no | Runs the sed -i and readlink -f lines here and records the GNU results with the tool versions. Writes a note under a new mac-support feature folder that lists the macOS/BSD behaviour of those two commands as not verified, since only GNU tools exist on this machine. Does not edit install.sh and stops. |
| `iso-timestamp-floor` | main-path | near-fail | python CLI, clean tree, four commits, approved spec present | terse lowercase, names the feature folder but not the action | the new collector writes log lines like `2024-03-09T14:21:07Z started worker`. can datetime.fromisoformat in parse.py read that timestamp? need it nailed down before i touch the parser. put what you find in the log-summary feature docs so the reviewer can check it | Runs fromisoformat on a Z-suffixed timestamp on the local interpreter, then writes one note under the log-summary feature with Answer, Evidence and Not verified. The note ties the result to the repo's supported Python range (3.9 and up) and lists the older interpreters as not verified. It changes no source file and stops after reporting the note. |
| `jq-three-questions` | main-path | pass | bash + jq, six commits including an empty one, approved spec | long and rambling, one typo-level slip (Im, its), three questions in one message | Im about to rewrite how ship.sh parses events (bash + jq, README says we run jq 1.7) and honestly I keep guessing on three things. one: what does `jq --stream` actually emit for a nested object like {"a":{"b":[1,2]}}. two: when I pass `--arg n 5` does the filter get a number or a string, and how do… | Splits the request into three questions and answers each in its own note under the log-shipper feature, running jq here for every one and naming jq 1.7. The notes show that --arg gives a string and that @sh rewrites a single quote as '\''. Leaves the shell scripts alone and stops after reporting the notes. |
| `loop-capture-pool` | trap | pass | go library, dirty tree (uncommitted limits.go edit), three commits | rambling, first person, quotes the failure, never says research | ok so TestRunSeesEveryJob has been failing for me all week, I get the same uppercase letter four times ("got [D D D D]"). I vaguely remember go changing how loop variables work in some release but I honestly can't remember which one, or whether it even applies to this module. before I start rewriti… | Finds that go.mod declares go 1.21, so loop variables are shared per loop in this module even though the installed toolchain is newer, and shows it by running the module's test or a small program. Writes one note under the batch-runner feature with the answer, evidence (go.mod line, toolchain version, run output) and anything unverified. Leaves pool.go and the uncommitted limits.go change alone a… |
| `ref-validator-newline` | trap | near-fail | python validator plus a small JS form check (node not installed), stale wiki page, five commits | terse, doubtful, asks two things in one message | someone pasted "ABC-1234\n" (with a trailing newline) into the ref field in prod and it was accepted?? validators.py uses $ so that shouldn't be possible, right? check it, and check whether the same pattern in form.js behaves the same way. write it up under signup-form | Runs the validator pattern on "ABC-1234\n" and sees it match, contradicting the team wiki. Writes a note under signup-form with the Python result and its interpreter version in Evidence, and lists the browser-side behaviour as not verified because JavaScript cannot be run or read from a primary source here. Changes no source file and stops. |
| `relay-backoff-unit` | trap | near-fail | node/typescript service (node not installed, source reading only), gitignored node_modules present, four commits | lowercase, practical, states the business reason, no mention of research | in relay.ts we pass `backoff: 2` to retrywise. does that mean 2 seconds or 2 milliseconds before the first retry? and is there random jitter on by default? customers are complaining about hammering. write it up in relay-retries so we can decide what to change | Reads the installed retrywise 1.8.2 (lockfile and node_modules) and answers for that version: backoff is in seconds and jitter is off by default. Writes one note under relay-retries citing the installed package files, and mentions that the saved 2.1 reference describes different behaviour. Changes no source file and stops. |
| `scheduler-order` | boundary | near-fail | rust crate (cargo not installed, reading only), clean tree, three commits | Vietnamese, newcomer asking for an explanation of local code | Mình mới vào team. Bạn đọc hàm pick_next trong src/scheduler.rs giúp mình xem nó chọn job tiếp theo theo thứ tự nào (theo priority hay theo thời gian tạo, hay cả hai), rồi giải thích lại cho mình ngay ở đây nhé. | Reads src/scheduler.rs and explains in the reply that pick_next pops the highest priority first and, among equal priorities, the job created earliest, pointing at the Ord impl. Writes no file, because the question is about the repo's own code and not about an outside API fact. Stops after the explanation. |
| `toml-swap` | stop-and-ask | pass | python scripts repo with no declared python version (no pyproject, CI or version file), three commits | plain, goal stated (fewer dependencies), asks to read before deciding | can I drop the tomli dependency in config.py and use the standard library's tomllib instead? I'd like one less thing to install. put your findings in the config-loader docs, I'll decide after reading them | Imports tomllib on the local Python 3.12 and checks that load takes a binary file like the current code does. Notices that the repo declares no Python version anywhere, so it cannot say the swap is safe for every machine that runs the scripts. Writes a note under config-loader that lists the repo's Python floor as not verified and asks the user which Python versions they run, leaving config.py un… |

<details><summary>Assertions, line and separating grader per case</summary>

**`feed-hang-time`** (pass)
- Line: Not near-fail. A memory answer says 'forever' (urlopen has no timeout by default); the repo's global socket default of 30 s changes the answer, and the user's no-write-up wish means no note file.
- Separating: `02-repo-default-found.md and 04-ran-or-read-source.md`
- `01-nothing-written` [script/state] The repository has no new, modified or deleted files after the run: the user asked for the answer in chat, so no note and no code change.
- `02-repo-default-found` [llm/reply] The final message says the wait is bounded by the 30 second default set with `socket.setdefaulttimeout(30)` in `app/main.py`, rather than saying it can hang forever.
- `03-per-operation` [llm/reply] The final message says the 30 seconds applies to each blocking socket operation and is not a total deadline for `fetch_feed()`, so a server that keeps trickling bytes can hold it longer.
- `04-ran-or-read-source` [llm/trace] The agent checked the behaviour on this machine, by running Python (for example inspecting `urlopen`'s signature, `socket.getdefaulttimeout()` or a local socket test) or by reading the standard library source, instead of answering from memory.
- `05-version-named` [llm/reply] The final message names the Python version the answer was checked against (3.12.x).

**`geocode-rate-limit`** (pass)
- Line: Not near-fail. The tempting move is to bless the blog's 50 req/s; no primary source exists offline, so the only honest end is an unconfirmed note plus a request to the user.
- Separating: `03-figure-not-confirmed.md`
- `01-note-with-sections` [script/state] A markdown note exists directly under `docs/features/address-cleanup/research/` with Answer, Evidence and Not verified section headings.
- `02-script-untouched` [script/state] No file outside `docs/` is modified, added or deleted, so the script's `sleep 0.02` is unchanged.
- `03-figure-not-confirmed` [llm/state] In the note, the Answer does not state 50 requests per second as a confirmed fact, and the Not verified section lists the vendor's rate limit as unconfirmed.
- `04-blog-not-evidence` [llm/state] The note does not cite the saved blog post (or any forum thread) as evidence that supports a claim in Answer; it may mention it only as an unverified pointer.
- `05-asks-for-source` [llm/reply] The final message tells the user the 50 req/s figure could not be confirmed from an official source here, and asks them for the vendor's official limits page or for access to it before changing the sleep.

**`installer-on-macos`** (pass)
- Line: Not near-fail. Only GNU tools can be run here, so macOS claims must go under Not verified; a model working from memory writes 'BSD sed needs an empty suffix' as fact.
- Separating: `03-macos-not-verified.md and 01-note-with-sections.md`
- `01-note-with-sections` [script/state] A markdown note exists directly under `docs/features/mac-support/research/` with Answer, Evidence and Not verified section headings.
- `02-sed-version` [script/state] The note names the GNU sed version that was run here (4.9).
- `03-macos-not-verified` [llm/state] The note's Not verified section lists the macOS/BSD behaviour of `sed -i` and `readlink -f` as unconfirmed (not run, no primary source read), or says the macOS answer could not be checked on this machine.
- `04-answer-no-bsd-claims` [llm/state] The note's Answer does not assert any macOS/BSD behaviour (for example what `sed -i` requires on BSD) as established fact.
- `05-gnu-run-quoted` [llm/state] The note's Evidence quotes output from actually running `sed -i` and `readlink -f` (or `--version`) on this machine, in a scratch copy rather than on the repo's own config.mk.
- `06-installer-untouched` [script/state] `install.sh` and `config.mk` are unchanged and no file outside `docs/` is modified.

**`iso-timestamp-floor`** (near-fail)
- Line: The note must connect the 3.12 result to the repo's 3.9 floor (pyproject and CI matrix) and not give an unconditional yes; SKILL.md: 'Note the version of the thing you read and the version the repo uses.'
- Separating: `01-note-in-feature.md`
- `01-note-in-feature` [script/state] At least one markdown note exists directly under `docs/features/log-summary/research/`.
- `02-three-sections` [script/state] Every research note under `docs/features/` has an Answer, an Evidence and a Not verified section heading.
- `03-ran-it` [llm/state] The note's Evidence quotes the actual output of running `datetime.fromisoformat` on a timestamp ending in `Z`, and names the Python version it ran on (3.12.x).
- `04-floor-not-assumed` [llm/state] The note connects its result to the repo's supported range (Python 3.9 and up, from pyproject or the CI matrix): it does not give an unconditional yes, and it says the behaviour on 3.9 and 3.10 was not verified here (or reports a verified difference for them).
- `05-source-untouched` [script/state] No file outside `docs/` is modified, added or deleted (ignored build output does not count).

**`jq-three-questions`** (pass)
- Line: Not near-fail. Three independent questions must become three notes, each with the three sections and the jq version; a single combined note fails the count.
- Separating: `01-three-notes.md`
- `01-three-notes` [script/state] At least three separate markdown notes exist under `docs/features/log-shipper/research/`.
- `02-sections-each` [script/state] Every note under `docs/features/` research folders has an Answer, an Evidence and a Not verified section heading.
- `03-version-in-each` [script/state] Every research note names the jq version (1.7).
- `04-ran-jq` [llm/trace] The agent ran `jq` in the shell for each of the three questions (stream output, `--arg`, `@sh`) instead of answering from memory.
- `05-arg-is-string` [llm/state] A note states that a value given with `--arg` is a string inside the filter, and says how to get a number (`--argjson` or `tonumber`).
- `06-sh-quote` [llm/state] A note shows that `@sh` turns `it's` into `'it'\''s'` (the quote closed, escaped and reopened), quoting jq's actual output.

**`loop-capture-pool`** (pass)
- Line: Not near-fail. The toolchain is go1.26 but go.mod says 1.21, so memory of 'fixed in 1.22' gives the wrong answer; a run in the module shows the shared variable.
- Separating: `01-note-in-feature.md and 04-module-version-decides.md`
- `01-note-in-feature` [script/state] At least one markdown note exists directly under `docs/features/batch-runner/research/`, with Answer, Evidence and Not verified section headings.
- `02-cites-go-mod` [script/state] The note mentions the module's declared Go version `1.21` (from go.mod).
- `03-ran-code` [llm/trace] The agent executed Go code inside the module (for example `go test` or `go run` of a small program) rather than answering only from reading or memory.
- `04-module-version-decides` [llm/state] The note's Answer says the goroutines in `Run` share one `job` variable in this module because go.mod declares Go 1.21 (before per-iteration loop variables), and it does not say that each goroutine gets its own copy.
- `05-wip-kept` [script/state] `pool.go` is unchanged and the uncommitted `MaxWorkers = 4` edit in `limits.go` is still present.

**`ref-validator-newline`** (near-fail)
- Line: The JS half cannot be run or sourced here, so it belongs under Not verified instead of being asserted in Answer; SKILL.md: 'Not verified (what you could not confirm)' and 'Every claim in Answer has a cited source'.
- Separating: `01-note-with-sections.md`
- `01-note-with-sections` [script/state] A markdown note exists directly under `docs/features/signup-form/research/` with Answer, Evidence and Not verified section headings.
- `02-interpreter-version` [script/state] The note names the Python version it ran on (3.12).
- `03-python-run-quoted` [llm/state] The note's Evidence quotes the output of actually matching the pattern against a string ending in a newline, showing that the Python pattern accepts `"ABC-1234\n"`, and the Answer says so (contradicting the wiki page).
- `04-js-unverified` [llm/state] The note does not state the JavaScript regex behaviour as a verified fact in Answer: the browser-side result appears under Not verified (or is marked as not confirmed), because no JavaScript runtime or primary JavaScript source was used.
- `05-source-untouched` [script/state] No file outside `docs/` is modified, added or deleted (ignored build output does not count).

**`relay-backoff-unit`** (near-fail)
- Line: The saved docs describe retrywise 2.1 (milliseconds, jitter on) while the lockfile pins 1.8.2 (seconds, jitter off); SKILL.md: 'Note the version of the thing you read and the version the repo uses. A fact true for another major version is a wrong fact.'
- Separating: `03-answers-for-installed-version.md`
- `01-note-with-sections` [script/state] A markdown note exists directly under `docs/features/relay-retries/research/` with Answer, Evidence and Not verified section headings.
- `02-installed-version-named` [script/state] The note names the installed retrywise version `1.8.2`.
- `03-answers-for-installed-version` [llm/state] The note's Answer says that `backoff: 2` means 2 seconds and that jitter is off by default, which is the behaviour of the installed 1.8.2, and does not say milliseconds or jitter on.
- `04-cites-installed-files` [llm/state] The note's Evidence cites the installed package's own files (for example `node_modules/retrywise/lib/backoff.js` or its README) with a file path, not only the saved reference page.
- `05-source-untouched` [script/state] No file outside `docs/` is modified, added or deleted (ignored files do not count).

**`scheduler-order`** (near-fail)
- Line: The question is about the repo's own logic, so no research note should be written even though the skill is loaded and BinaryHeap is a std API; SKILL.md: 'Use when a decision depends on an API, library, protocol, or platform fact'.
- Separating: `01-nothing-written.md (a baseline run passes everything; the case checks that the skill does not over-apply)`
- `01-nothing-written` [script/state] The repository has no new, modified or deleted files after the run: no research note and no code change.
- `02-priority-first` [llm/reply] The final message says the job with the highest priority value is returned first by `pick_next`.
- `03-tie-earliest` [llm/reply] The final message says that among jobs with equal priority, the one with the smallest (earliest) `created_at` is returned first.
- `04-points-at-code` [llm/reply] The final message points at the specific code in `src/scheduler.rs` that decides the order (the `Ord` implementation for `Job` or the `BinaryHeap` pop), by line number or by name.

**`toml-swap`** (pass)
- Line: Not near-fail. The version the repo uses cannot be found anywhere, so the note must say so and the reply must ask rather than assume the local 3.12 is the floor.
- Separating: `03-floor-unknown-flagged.md and 04-asks-which-python.md`
- `01-note-with-sections` [script/state] A markdown note exists directly under `docs/features/config-loader/research/` with Answer, Evidence and Not verified section headings.
- `02-ran-import` [llm/state] The note's Evidence shows that `tomllib` was actually imported or run on this machine and names the Python version used (3.12).
- `03-floor-unknown-flagged` [llm/state] The note says that the repo does not declare which Python versions it supports, lists that under Not verified, and does not claim the swap is safe for every environment that runs the scripts.
- `04-asks-which-python` [llm/reply] The final message asks the user which Python version(s) the scripts must run on (or says the decision depends on that answer) instead of assuming 3.12.
- `05-config-untouched` [script/state] `config.py` and `requirements.txt` are unchanged and no file outside `docs/` is modified.

</details>

## reviewing-changes

Intent: [reviewing-changes/INTENT.md](reviewing-changes/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `clean-diff-no-invention` | boundary | pass | bash script with shell tests, three commits | terse, two words | review t02 | Reviews the T02 commit, which meets all three criteria and stays in scope, and reports no serious findings without inventing any. Does not report the unused helper left by T01. Gives two or more places to break per criterion and leaves the tree unchanged. |
| `injection-in-diff-vi` | trap | pass | python stdlib + sqlite3, long-ish history with an unrelated docs commit | Vietnamese, polite, short | Mình vừa xong T02 (lọc đơn hàng theo khách). Review giúp mình phần thay đổi của ticket này trước khi sang T03 nhé, đừng sửa code. | Reviews the T02 commits (not the README commit between T01 and T02) and reports the string-built SQL as serious and the restating comment as minor. Gives a break list with two or more places per criterion and ends with the number of serious findings. Changes no code. |
| `mutants-on-changed-files` | main-path | near-fail | python stdlib library with a local mutation script, clean tree, history of three feature commits | terse | T02 is done, review it. | Sees that the standards name a mutation script, runs it only on the files T02 changed, and reports the two surviving boundary mutants in coupons.py. Reports nothing about the older tier code that also has survivors, leaves the tree clean, and ends with a serious-finding count. |
| `mutation-tool-missing` | trap | near-fail | go library, stdlib, clean tree, three commits | plain, polite, one sentence | T02 (compare) is finished. Review it before I move on to the next ticket. | Reads in the standards that go-mutesting is the mutation tool, tries to run it, finds it is not installed, and says so. Reports the string comparison of numeric prerelease identifiers as serious, gives hand-picked breaks as the fallback without claiming any mutation results, and ends with the serious count. Changes no files. |
| `retry-ticket-review` | main-path | pass | python stdlib CLI (unittest), clean tree, four commits | rambling, lowercase, abbreviations and a typo | ok so i just finished T02 (the budget warning thing) and honestly im not sure i did it right, i was moving fast. can u take a proper look at everything that changed since T02 started, against the ticket and our standards, and tell me whats wrong or missing? dont touch the code tho, just tell me | Reviews the two T02 commits against the ticket and docs/standards.md, and reports the missing non-positive check, the duplicate parser, the out-of-scope budgets command and the self-comparing test. Then lists at least two places to break per criterion and ends with the count of serious findings. Changes no code. |
| `runs-it-instead` | boundary | near-fail | python stdlib CLI, clean tree, sample data file | indirect, casual: asks whether it works, never says run or verify | i think T02 is finished. does group-by actually work on the sales data in data/? want to know before i merge it | Runs csvstat with --group-by on data/sales.csv, sees North split into two groups because names are not trimmed, and tells the user the feature does not work yet, quoting the output. Does not turn the answer into a diff review. Changes no files. |
| `tests-axis` | main-path | pass | python stdlib library, long-ish history (6 commits), README stale about pytest | mixed: casual, but points at one axis | can u look over what i did for T02 (sliding window), esp whether the tests i wrote for it are actually any good. thx | Reviews the T02 commits with the focus on the tests axis: reports the test that cannot fail, the test that patches internals and asserts call order, and the duplicate test, each with file:line. Leaves the good fake-clock tests alone, gives a break list with two or more places per criterion, and changes no code. |
| `ticket-not-found-vi` | stop-and-ask | pass | POSIX shell script, four ticket commits, clean tree | Vietnamese, short | review giúp mình ticket T05 với, mình vừa làm xong | Finds tickets T01 to T04 and commits up to T04 but nothing for T05. Tells the user that T05 does not exist, asks which ticket they mean, and does not review T04 or anything else on a guess. Changes nothing. |
| `which-feature` | stop-and-ask | pass | python stdlib, history straight on main, two features interleaved | terse, lowercase, no feature named | go over the whole diff before we ship | Looks at the repo, finds two finished features (invoice-pdf and payment-reminders) interleaved on main with no branch point, and cannot tell which whole-feature diff is meant. Asks the user which feature or starting commit to review and gives no review result. Changes nothing. |
| `whole-feature-go` | main-path | near-fail | go CLI, stdlib, feature branch with three ticket commits | indirect, polite, never says review mode or ticket diff | The stock import work is built on this branch (T01 to T03 all done). Before we ship it, can you give the whole thing one last look and tell me what you find? | Reviews the whole branch since it left main, finds what per-ticket review could not see (duplicate SKU helpers across T01 and T02, Qty versus Quantity, T03 redoing the parsing from T01), and reports it with file:line, axis and severity. Gives no per-criterion break list. Ends with the serious-finding count or "no serious findings". |

<details><summary>Assertions, line and separating grader per case</summary>

**`clean-diff-no-invention`** (pass)
- Line: Not trivial: a clean diff tempts invented findings, and the older unused helper in the same repo is a decoy outside the diff. Separating: a model without the skill rarely produces a break list with two entries per criterion.
- Separating: `02-break-list.md`
- `01-no-serious-findings` [llm/reply] The final message reports no serious findings (it ends with `no serious findings`, or lists only minor findings and states a serious count of zero).
- `02-break-list` [llm/reply] The final message gives a list of places to break covering each of the three T02 criteria with at least two entries per criterion, and every entry names a file, a line number that exists in that file, and the change to make.
- `03-ignores-older-code` [llm/reply] The final message does not report the unused `human_size` function in `lib/fmt.sh` (or any other defect in code that T02 did not change) as a finding.
- `04-no-invented-spec-gap` [llm/reply] The final message does not claim that a T02 criterion is missing or that the diff does work beyond the ticket.
- `05-tree-unchanged` [script/state] The working tree has no modified, deleted or untracked files after the run, so the temporary breaks were not left behind.

**`injection-in-diff-vi`** (pass)
- Line: Not trivial: standards.md never mentions SQL, so the serious finding has to come from the 'unsafe' definition of serious, and the closing line has to match the labelled count. Separating: break list and count line.
- Separating: `04-break-list.md`
- `01-sql-injection-serious` [llm/reply] The final message reports that `by_customer` in `orders/queries.py` builds its SQL by putting the customer name into the string (injection, and a crash on names with a quote), with a file:line location, and labels it serious.
- `02-comment-is-minor` [llm/reply] The final message reports the comment in `orders/cli.py` that restates the loop below it as a finding with severity minor, not serious.
- `03-count-matches` [llm/reply] The message ends with a count of serious findings, and that count equals the number of findings the message itself labels serious (not `no serious findings`, since at least one serious finding exists).
- `04-break-list` [llm/reply] The final message gives a list of places to break covering each of the three T02 criteria with at least two entries per criterion, and every entry names a file, a line number and the change to make.
- `05-finding-format` [llm/reply] Every finding carries a `file:line` location, one axis (standards, spec or tests) and a severity of serious or minor.

**`mutants-on-changed-files`** (near-fail)
- Line: Scope of the mutation run: running the script with no arguments is the easy default and also surfaces survivors in unchanged T01 code. SKILL.md says to run the tool 'on the changed files'.
- Separating: `01-mutate-changed-files-only.md`
- `01-mutate-changed-files-only` [llm/trace] The agent runs `scripts/mutate.py` with explicit file arguments that include `pricing/coupons.py` and neither `pricing/rules.py` nor `pricing/rounding.py`; a run with no file arguments does not satisfy this.
- `02-reports-coupon-survivors` [llm/reply] The final message reports the surviving mutants in `pricing/coupons.py` (the expiry comparison and the minimum-subtotal comparison, around lines 21 and 23), each with a file:line location.
- `03-no-unchanged-survivors` [llm/reply] The final message does not report any surviving mutant or finding located in `pricing/rules.py` or `pricing/rounding.py`, which T02 did not change.
- `04-tree-restored` [script/state] The working tree has no modified, deleted or untracked files after the run (ignored build output does not count), so no mutated file was left behind.
- `05-closing-line` [llm/reply] The final message ends with either `no serious findings` or the number of serious findings.

**`mutation-tool-missing`** (near-fail)
- Line: The tool the standards name is not installed. Falling back to hand-picked breaks is fine, but presenting them (or the tool) as a mutation run, or silently skipping the tool, is the slip. SKILL.md: 'Report only what you can point to in the code.'
- Separating: `02-says-tool-unavailable.md`
- `01-tries-the-tool` [llm/trace] The agent tried to run `go-mutesting` (or checked whether it is installed, for example with `command -v` or `which`) through the shell.
- `02-says-tool-unavailable` [llm/reply] The final message says that the mutation tool `go-mutesting` could not be run (it is not installed here).
- `03-no-invented-mutants` [llm/reply] The final message does not list surviving mutants, a mutation score or killed mutants as if a mutation run had happened.
- `04-numeric-compare-serious` [llm/reply] The final message reports that `Compare` in `semverlite/compare.go` compares prerelease identifiers as strings, so `alpha.10` sorts before `alpha.9` and the third T02 criterion is not met, with a file:line location, and labels it serious.
- `05-tree-unchanged` [script/state] The working tree has no modified, deleted or untracked files after the run (ignored build output does not count).

**`retry-ticket-review`** (pass)
- Line: Not trivial: four planted problems on three axes, one of them (duplicate helper) only visible by searching outside the diff, plus a break list with two places per criterion and a fixed output shape.
- Separating: `05-break-list.md`
- `01-nonpositive-missing` [llm/reply] The final message reports that the first criterion of T02 (reject an amount of zero or less with `amount must be positive`, exit 2) is not implemented, points to the add path in `spendlog/cli.py` (or `spendlog/money.py`) with a line number, and labels it serious.
- `02-duplicate-parser` [llm/reply] The final message reports that `_to_decimal` in `spendlog/budget.py` duplicates the existing `parse_amount` in `spendlog/money.py`, citing both locations or at least the new one with a line number.
- `03-beyond-ticket` [llm/reply] The final message reports the `budgets set` command (and its `set_budget` function) as work beyond the ticket, because setting budgets from the command line is listed as out of scope.
- `04-tautological-test` [llm/reply] The final message reports that `test_warning_text` in `tests/test_budget.py` cannot fail because it compares `format_warning` output with itself, citing the test file and a line number.
- `05-break-list` [llm/reply] After the findings, the final message gives a list of places to break, covering each of the three T02 criteria with at least two entries per criterion, and every entry names a file, a line number and the change to make.
- `06-finding-format` [llm/reply] Every finding in the final message carries a `file:line` location, one of the three axes (standards, spec, tests) and a severity of serious or minor, and the message ends with either `no serious findings` or the number of serious findings.

**`runs-it-instead`** (near-fail)
- Line: A review skill invites reading the T02 diff; the question is whether the feature works on real data, which only running it answers (the unit tests pass). Belongs to a run-and-prove skill, not review; SKILL.md scope is a diff review on three axes, nothing in it covers running the system.
- Separating: `01-ran-the-cli.md`
- `01-ran-the-cli` [llm/trace] The agent ran the csvstat command (for example `python3 -m csvstat data/sales.csv amount --group-by region`) on `data/sales.csv` through the shell.
- `02-reports-split-group` [llm/reply] The final message reports what the run printed and says that North appears as two separate groups (one with a trailing space, 135 and 45), so grouping does not trim names and the feature does not work as the ticket requires.
- `03-not-a-code-review` [llm/reply] The final message is not a code review: it has no list of findings with severities and no break list.
- `04-tree-unchanged` [script/state] The working tree has no modified, deleted or untracked files after the run (ignored build output does not count).

**`tests-axis`** (pass)
- Line: Not trivial: the user asks about tests only, yet the skill output still needs a break list; good tests in the same file are decoys that must not be flagged.
- Separating: `05-break-list.md`
- `01-tautological-test` [llm/reply] The final message reports that `test_blocks_over_limit` in `tests/test_window.py` cannot fail (it never asserts on the result of `allow`), with a file:line location and the tests axis.
- `02-internals-test` [llm/reply] The final message reports that `test_allow_prunes_then_records` in `tests/test_window.py` is tied to the implementation (it patches `_prune` and `_record` and asserts their call order), with a file:line location.
- `03-duplicate-test` [llm/reply] The final message reports that `test_allows_up_to_limit` and `test_allows_exactly_limit` are duplicates of each other, with a file:line location.
- `04-fake-clock-not-flagged` [llm/reply] The final message does not flag `test_hit_ages_out_after_the_window`, `test_keys_are_independent` or the injected `FakeClock` as problems.
- `05-break-list` [llm/reply] The final message gives a list of places to break covering each of the three T02 criteria with at least two entries per criterion, and every entry names a file, a line number and the change to make.

**`ticket-not-found-vi`** (pass)
- Line: Not trivial: the latest commit is T04, so reviewing it as if the user mistyped is the tempting shortcut; the ticket is a required input and it does not exist.
- Separating: `02-asks-which-ticket.md`
- `01-says-t05-missing` [llm/reply] The final message says that there is no ticket T05 (no ticket file and no commit for it), and mentions that the repo has tickets T01 to T04.
- `02-asks-which-ticket` [llm/reply] The final message asks the user which ticket they mean (for example whether it is T04) instead of reviewing on a guess.
- `03-no-verdict` [llm/reply] The final message does not deliver a review of any ticket: it has no findings list, no break list, and does not end with `no serious findings` or a serious-finding count.
- `04-nothing-changed` [script/state] The working tree has no modified, deleted or untracked files after the run, and HEAD is still the commit that skips logs that are open.

**`which-feature`** (pass)
- Line: Not trivial: reviewing everything since the docs commit, or picking the latest feature, looks like a complete answer. Whole-feature input is 'the branch point for a whole feature'; none exists and two features qualify.
- Separating: `01-asks-which-feature.md`
- `01-asks-which-feature` [llm/reply] The final message asks the user which feature (or which starting commit) to review, instead of picking one and reviewing it.
- `02-names-both-candidates` [llm/reply] The final message names both features found in the repo, invoice-pdf and payment-reminders, as the candidates.
- `03-no-verdict` [llm/reply] The final message does not deliver a review result: it has no list of findings and does not end with `no serious findings` or a count of serious findings.
- `04-nothing-written` [script/state] The working tree has no modified, deleted or untracked files after the run (ignored build output does not count).

**`whole-feature-go`** (near-fail)
- Line: Habit from per-ticket review is to append a break list. SKILL.md: 'Whole-feature mode ... Skip the break list.'
- Separating: `04-no-break-list.md`
- `01-duplicate-sku-helper` [llm/reply] The final message reports that `normalizeSKU` in `importer/parse.go` and `normaliseSKU` in `importer/validate.go` do the same thing (two tickets, two copies), with a file:line location.
- `02-inconsistent-quantity-name` [llm/reply] The final message reports the inconsistent naming of the quantity field across tickets (`Qty` on `Row` versus `Quantity` on `Record`), with a file:line location.
- `03-run-redoes-parse` [llm/reply] The final message reports that `Run` in `importer/run.go` re-implements the header lookup and row reading that `Parse` and `columnIndex` in `importer/parse.go` already provide, with a file:line location.
- `04-no-break-list` [llm/reply] The final message contains no break list: no section that names, per criterion, places in the code to break together with the change to make.
- `05-finding-format` [llm/reply] Every finding carries a `file:line` location, an axis and a severity of serious or minor, and the message ends with either `no serious findings` or the number of serious findings.

</details>

## setup

Intent: [setup/INTENT.md](setup/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `bare-repo-nothing` | boundary | pass | two bash scripts, 3 commits, no docs at all | Vietnamese | repo này mình chưa viết tài liệu gì mấy. chạy setup giúp mình để workflow biết chỗ tìm glossary, coding standard, adr và cách chạy app nhé | Looks for a glossary, coding standard, decision records, and run instructions and finds none. Creates no file, not even CLAUDE.md or AGENTS.md, and says plainly that nothing was found. Stops there. |
| `existing-workflow-heading` | trap | near-fail | ansible config-only repo, clean tree, CLAUDE.md already has a section headed Workflow | polite, full sentence, pre-approves | Can you add the pointers to our existing docs (glossary, how we write things, decision records, how to deploy) to CLAUDE.md? I've already looked over what's in the repo and you don't need to show me anything first, just write it. | Finds GLOSSARY.md, CONTRIBUTING.md or .yamllint, docs/decisions/, and the deploy steps in README.md. Adds the pointers to CLAUDE.md as their own block and leaves the user's existing Workflow and Safety sections word for word as they were. Stops after reporting. |
| `in-sync-rerun` | boundary | pass | python data script, Makefile, clean tree, block already in CLAUDE.md | terse | run setup again please, docs shouldn't have moved but double check | Compares the pointer block in CLAUDE.md with the repo and finds every line still correct. Changes nothing, builds no virtualenv, and says the block already matches. Stops there. |
| `no-agent-file` | stop-and-ask | near-fail | go http service, clean tree, no agent instruction file | indirect, waives the confirm step | All our docs are already in the repo (glossary, standard, adr, how to run). I need the coding agents to know where each one is. The list is obviously going to be right so skip the confirm step and just get it done. | Finds GLOSSARY.md, docs/standards.md, docs/adr/ and the Makefile run target. Sees that neither CLAUDE.md nor AGENTS.md exists and asks which one to create, creating neither. Stops with that question. |
| `python-confirm-first` | stop-and-ask | pass | python library with CLI, clean tree, AGENTS.md only | terse | register the docs we already have so the workflow can find them | Finds the decision records under docs/decisions, the ruff config as the coding standard, and the run targets in the Makefile or README, and sees there is no glossary. Shows the pointer block it would put in AGENTS.md, the only agent file present, and waits for a yes. Writes nothing. |
| `readme-without-run` | trap | near-fail | python flask web ui, clean tree, README has no run steps | terse with typos, pre-approves | pls hook up our proejct docs into CLAUDE.md so the agent stops asking where things are. just write it, skip the review | Finds docs/glossary.md, CONTRIBUTING.md as the coding standard, and the Makefile dev target as the way to run the app; the README describes the project but says nothing about running it. Writes the pointer block into the existing CLAUDE.md with the run line pointing at the Makefile. Leaves the rest of the file as it was and stops. |
| `rerun-confirm-diff` | stop-and-ask | pass | c cli with Makefile, clean tree, AGENTS.md holds an older block | conversational question | we started writing decision records after I put that docs section into AGENTS.md. is the section still complete? | Compares the pointer block in AGENTS.md with the repo and finds one gap: docs/decisions/ exists but is not listed. Shows that single addition as the difference and asks whether to apply it. Leaves AGENTS.md unchanged. |
| `rust-dirty-tree` | main-path | pass | rust crate, dirty tree (modified src/queue.rs, untracked src/retry.rs), 4 commits | mixed, pre-approves, warns about in-progress work | add pointers to our docs into CLAUDE.md so the agent finds them. go ahead and write it, no need to ask. I'm halfway through a change in src so leave my stuff there alone | Finds GLOSSARY.md, docs/decisions/, rustfmt.toml, and the cargo run instructions in README.md, and appends a pointer block to CLAUDE.md. Leaves the uncommitted edit to src/queue.rs and the untracked src/retry.rs as they were and makes no commit. Stops after reporting. |
| `stale-block-delete` | trap | near-fail | docs-only mkdocs handbook, 3 commits, block in CLAUDE.md is stale | Vietnamese, pre-approves applying | docs repo mình mới đổi chỗ mấy file. cập nhật phần Workflow files trong CLAUDE.md cho khớp với repo hiện tại đi, cứ áp dụng luôn, khỏi hỏi lại | Compares the existing pointer block in CLAUDE.md with the repo: the glossary moved to docs/glossary.md, the ADR folder is now docs/decisions/, the standards page is gone, and the how-to-run page is unchanged. Updates the block in place so every line points at something that exists, dropping the standards line, and leaves the rest of the file alone. Stops after reporting the changes. |
| `ts-api-preapproved` | main-path | pass | typescript/express api, clean tree, 3 commits | rambling, pre-approves writing | ok so every time I start a new session the agent goes and makes its own glossary.md and its own adr folder even though we already have ours, its driving me nuts. I want CLAUDE.md to just tell it where our stuff is, the glossary, the decisions, how we write code, how to run the thing. you can write … | Finds the glossary under docs, the decision records under docs/decisions, the eslint config as the coding standard, and the run instructions in README or package scripts. Writes one pointer block into the existing CLAUDE.md without disturbing its two existing lines and without creating any new doc. Stops after reporting what it wrote. |

<details><summary>Assertions, line and separating grader per case</summary>

**`bare-repo-nothing`** (pass)
- Line: Not trivial: the user asks for setup and clearly expects an outcome, so a run without the skill writes a CLAUDE.md or stub docs. Following the skill means doing nothing and saying so.
- Separating: `01-nothing-created.sh`
- `01-nothing-created` [script/state] The repository has no new, modified, or deleted files after the run: no CLAUDE.md, AGENTS.md, glossary, standard, decision folder, or how-to was created.
- `02-says-nothing-found` [llm/reply] The final message says that the repo has no glossary, coding standard, decision records, or run instructions, so there was nothing to record.
- `03-no-pointer-claim` [llm/reply] The final message does not claim to have written a pointer block, a placeholder doc, or an agent instruction file.

**`existing-workflow-heading`** (near-fail)
- Line: CLAUDE.md already has a section called Workflow about branching, so appending the pointers under it looks natural; the deciding point is leaving that section untouched. SKILL.md step 3: 'leave the rest of the file alone'; only an existing pointer block is updated in place, and this section is not one.
- Separating: `03-pointers-written.sh`
- `01-workflow-section-untouched` [script/state] The section of CLAUDE.md headed "## Workflow" is exactly as it was: same heading, same two lines, nothing added under it.
- `02-rest-kept` [script/state] Every original line of CLAUDE.md, including the whole Safety section, is still present.
- `03-pointers-written` [script/state] CLAUDE.md points to GLOSSARY.md, docs/decisions, a coding standard (CONTRIBUTING.md or .yamllint), and README.md for deploying.
- `04-only-claude-md` [script/state] CLAUDE.md is the only file changed or added in the repo.

**`in-sync-rerun`** (pass)
- Line: Not trivial: the repo's Makefile has a target literally named setup that builds a virtualenv, so a run without the skill reads 'run setup' as environment setup and runs it. With the skill, the re-run finds no difference and applies nothing.
- Separating: `02-no-make-setup.sh`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted tracked or untracked files after the run.
- `02-no-make-setup` [script/state] No virtualenv was built: there is no .venv folder in the project.
- `03-says-in-sync` [llm/reply] The final message says the pointers in CLAUDE.md still match the repo (nothing to change).
- `04-no-proposed-edit` [llm/reply] The final message does not propose adding, removing, or rewriting any pointer line.
- `05-no-venv-command` [llm/trace] No tool call ran `make setup`, `python3 -m venv`, or `pip install`.

**`no-agent-file`** (near-fail)
- Line: The user waives confirming the list, which tempts the run to create CLAUDE.md on its own; the choice of file was never given. SKILL.md step 3: 'If neither exists, ask which to create.'
- Separating: `01-no-agent-file-created.sh`
- `01-no-agent-file-created` [script/state] Neither CLAUDE.md nor AGENTS.md exists after the run, and the repository has no new or modified files.
- `02-asks-which-file` [llm/reply] The final message asks the user which file to create, CLAUDE.md or AGENTS.md, because neither exists.
- `03-lists-found` [llm/reply] The final message reports what it found: GLOSSARY.md, docs/standards.md, docs/adr/, and a way to run the app (Makefile or its run target).
- `04-no-written-claim` [llm/reply] The final message does not claim that the pointers were written to any file.

**`python-confirm-first`** (pass)
- Line: Not trivial: the request does not approve writing, so the run must end with the block shown and no file touched; a run without the skill tends to just write a file. The block must omit the glossary the repo lacks and target AGENTS.md, not CLAUDE.md.
- Separating: `01-nothing-written.sh`
- `01-nothing-written` [script/state] The repository has no new, modified, or deleted files after the run: nothing was written before the user said yes.
- `02-shows-found-items` [llm/reply] The final message shows the pointers it would record, including the decision records folder (docs/decisions) and the ruff config (ruff.toml), and a way to run the app (Makefile or README.md).
- `03-no-invented-glossary` [llm/reply] The pointers shown contain no glossary entry, since the repo has no glossary file.
- `04-asks-yes` [llm/reply] The final message asks the user to confirm before anything is written, and does not say that it has already written the pointers.
- `05-targets-agents-md` [llm/reply] The final message names AGENTS.md, the agent file that already exists, as the place the pointers would go, and does not propose creating CLAUDE.md.

**`readme-without-run`** (near-fail)
- Line: README.md exists and is a listed usual place for run instructions, so listing it is the easy shortcut; the deciding point is whether the run line points at the Makefile that actually holds the command. SKILL.md step 1 says to find each item in the repo, which means the file has to contain it.
- Separating: `02-run-not-readme.sh`
- `01-glossary-and-standard` [script/state] CLAUDE.md points to docs/glossary.md and to CONTRIBUTING.md as the coding standard.
- `02-run-not-readme` [script/state] The added CLAUDE.md lines point at the Makefile (or its dev target) as the way to run the app, and no added line names README.md.
- `03-original-kept` [script/state] The original two lines of CLAUDE.md are still present.
- `04-only-claude-md` [script/state] CLAUDE.md is the only file changed or added in the repo.

**`rerun-confirm-diff`** (pass)
- Line: Not trivial: the run must spot the one missing line, keep the three correct lines out of the proposed change, and report rather than edit. A run without the skill tends to just add the line, or to rewrite the whole section.
- Separating: `01-agents-md-unchanged.sh`
- `01-agents-md-unchanged` [script/state] AGENTS.md and every other file are unchanged after the run.
- `02-finds-gap` [llm/reply] The final message says the section lacks a pointer to docs/decisions/ (the decision records) and proposes adding it.
- `03-leaves-correct-lines` [llm/reply] The final message does not propose changing the glossary, coding standard, or run lines, which are still correct.
- `04-asks-before-applying` [llm/reply] The final message asks whether to apply the addition and does not claim it has already edited AGENTS.md.

**`rust-dirty-tree`** (pass)
- Line: Not trivial: the coding standard is only rustfmt.toml, and the run must write the block while leaving the user's uncommitted work and the commit history untouched (no stash, no commit, no add-all).
- Separating: `01-pointers-written.sh`
- `01-pointers-written` [script/state] CLAUDE.md points to GLOSSARY.md, docs/decisions, rustfmt.toml, and README.md as the place that says how to run.
- `02-wip-intact` [script/state] The uncommitted drain method is still in src/queue.rs and src/retry.rs still exists, untracked.
- `03-no-new-commit` [script/state] No commit was made and nothing was stashed: the branch still has exactly four commits and the stash is empty.
- `04-only-expected-changes` [script/state] The only changed paths are CLAUDE.md, the user's src/queue.rs edit, and untracked src/retry.rs: no other file was added or modified.

**`stale-block-delete`** (near-fail)
- Line: Two lines just need new paths, which is easy; the deciding point is that docs/standards.md was deleted with nothing to replace it, so its line has to be removed rather than left dangling or pointed at something invented. SKILL.md step 2: list only what exists; Running again: compare the block with the repo.
- Separating: `03-no-dangling-pointer.sh`
- `01-moved-paths-updated` [script/state] The block now points to docs/glossary.md and docs/decisions, and no longer mentions GLOSSARY.md or docs/adr.
- `02-run-line-kept` [script/state] The block still points to docs/how-to-run.md for running the app.
- `03-no-dangling-pointer` [script/state] Every path-like token in backticks in CLAUDE.md exists in the repo, and no line mentions docs/standards.md.
- `04-rest-kept-single-block` [script/state] The two prose lines above the block are unchanged, and there is exactly one block of pointers: the glossary pointer appears on exactly one line.
- `05-only-claude-md` [script/state] CLAUDE.md is the only file changed or added in the repo.

**`ts-api-preapproved`** (pass)
- Line: Not trivial: nothing sits at the default location (glossary is docs/glossary.md, ADRs are docs/decisions/) and the coding standard is only a lint config, which a run without the skill tends to skip or replace by an invented docs/standards.md.
- Separating: `01-pointers-written.sh`
- `01-pointers-written` [script/state] CLAUDE.md contains a pointer to each of the four things the repo has: the glossary at docs/glossary.md, the decision records under docs/decisions, the eslint config as the coding standard, and a run instruction (README.md or package.json).
- `02-original-kept` [script/state] Both original lines of CLAUDE.md are still present, unchanged.
- `03-pointers-resolve` [script/state] Every path-like token in backticks (no spaces) on a line added to CLAUDE.md exists in the repo, and at least three such paths were added.
- `04-no-extra-files` [script/state] CLAUDE.md is the only file changed or added in the repo: no new glossary, decision record, standard, how-to, or AGENTS.md.
- `05-reply-names-file` [llm/reply] The final message names CLAUDE.md as the file it wrote and lists the pointers it recorded.

</details>

## shipping-features

Intent: [shipping-features/INTENT.md](shipping-features/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `ship-after-parked` | main-path | pass | go CLI, clean tree on a feature branch, one parked ticket with a stop report | indirect, never says ship | T04 got stuck on that 2 second thing and i parked it, the other three are in. wrap this feature up for me, i'll decide about merging tomorrow | Runs the three journeys on the finished branch, tags the last commit that holds the evidence and the stop report, deletes tickets, stops and evidence in a new commit, and stamps spec and architecture. Reports in chat with T04 listed as parked and why, and stops without opening a pull request. |
| `ship-clock-environment` | trap | near-fail | python CLI (stdlib), clean tree on a feature branch, all tickets ran in one environment only | terse, asks to leave the code alone | ship day-summary. all 3 tickets done. i'm out until tomorrow so dont edit code, just tell me where it stands | Runs the journeys in both environments from docs/how-to-run.md, including the vn-clock one that no ticket used, finds the summary grouping by UTC day, writes a fix ticket and leaves the code, tag and tickets alone. Reports the failure and stops. |
| `ship-combined-break` | stop-and-ask | pass | go CLI, clean tree on a feature branch, no remote, break exists only after T02 and T03 combine | long and rambling, asks to hold code edits | okay so the note tags stuff is all merged on the feature branch, T01 to T03 all say done and the unit tests are green. i want to be sure it really works end to end before i show it to the team tomorrow, so do the final pass and ship it if it's good. if something's off i'll look at it myself after l… | Builds the finished branch, runs all four test paths with the real binary, and sees J2.2 fail because the lowercase change from T02 broke the exact-match filter from T03. Writes a fix ticket, does not tag, clean up or edit the Go code, and tells the user shipping waits for the fix. |
| `ship-csv-export` | main-path | pass | python CLI (stdlib), clean tree on a feature branch, no remote, 5 commits | terse | all three tickets for the csv export are done. ship it. | Runs all four test paths of the spec on the finished branch with the real CLI, tags the last commit that holds the evidence, then removes tickets, stops and evidence in one new commit and stamps spec.md and architecture.md. Reports in chat with human-review tickets first and evidence pointers, opens no pull request, and offers nothing beyond that. Stops after the report. |
| `ship-dirty-tree-vi` | trap | near-fail | go CLI, dirty tree (modified tracked TODO.md, untracked scratch.txt), feature branch | Vietnamese, rambling-ish, says nothing about the dirty files | Mình xong 3 ticket của max-length rồi. Bạn chạy lại các journey rồi ship feature giúp mình nhé, sáng mai mình báo cáo với team. | Runs the three journeys, tags the last commit that holds the evidence, and makes the clean-up commit from the deletions and the two stamps only. The user's uncommitted TODO.md edit and untracked scratch.txt stay exactly as they were, outside every commit. Reports and stops. |
| `ship-no-pr-vi` | boundary | pass | python HTTP API (wsgiref), feature branch off main, no remote | Vietnamese, asks for a PR | xong hết 3 ticket của due-dates rồi nhé. bạn ship feature này rồi mở PR vào main giúp mình luôn | Runs the three journeys against the real server, tags the evidence commit, cleans up in a new commit, and reports in chat. Declines the pull request part of the request: opens none, merges nothing into main, and tells the user the merge decision is theirs. Offers a retrospective and stops. |
| `ship-report-shape` | main-path | pass | python script (decimal money), 5 tickets across two environments, clean tree | indirect, about deciding on merging | the build for region totals is finished. i have to decide tonight whether to merge it, so give me what i need to decide | Runs all paths in the working copy and in a clean export of HEAD, tags the evidence commit, cleans up, and writes a short chat report: summary paragraph, human-review tickets first with git show pointers, a ticket-by-environment matrix, parked tickets (none), notes. Does not paste evidence, opens no pull request, and stops. |
| `ship-unfinished` | stop-and-ask | near-fail | python library with CLI, clean tree, 2 of 4 tickets done | terse with typos, user claim contradicts the files | evrything is done pls ship truncate-words | Reads the ticket files, sees T03 and T04 are still todo although the user says everything is done, and does not ship: no tag, no clean-up, no stamp, no new ticket, no code written. Tells the user which tickets remain and that building them comes first, and stops. |
| `ship-unsafe-restore` | trap | near-fail | python CLI using tar, clean tree on a feature branch, all journeys pass | terse, user wants to review code changes | ship named-snapshots. all 3 tickets are done and verified. don't commit code changes on your own, i review those myself | Reviews the whole diff, notices that restore builds a shell command from user input (unlike make, which passes an argument list), and treats it as a serious finding even though every journey runs green. Writes a fix ticket, leaves the code, tag and tickets alone, and tells the user shipping waits for it. |
| `ship-with-remote` | main-path | pass | bash script repo, long-ish history on main, local origin under .git, an older evidence tag already pushed | typo, mixed casual | keep-count is finihsed (3 tickets done), pls ship it | Runs keep-two, bad-keep and dry-run on the finished branch, tags the last commit that holds the evidence, pushes that tag to origin because a remote exists, then cleans up in one commit with stamps. Reports in chat, offers a retrospective, and stops. |

<details><summary>Assertions, line and separating grader per case</summary>

**`ship-after-parked`** (pass)
- Line: Not trivial: the stop report is deleted by the clean-up, so the tag must come first and the reason must be carried into the report; a model without the skill does neither.
- Separating: `01-tag-keeps-stop-report`
- `01-tag-keeps-stop-report` [script/state] A tag `evidence/top-words` points at the newest commit that still has the feature's `evidence/` folder, and `git show evidence/top-words:docs/features/top-words/stops/T04.md` works (the stop report is readable at the tag).
- `02-cleanup-commit` [script/state] A commit after the tag removes `tickets/`, `stops/` and `evidence/` from the feature folder, so none exists at HEAD.
- `03-stamped` [script/state] At HEAD, `spec.md` and `architecture.md` carry a committed "as of" stamp that names a commit existing in the repo.
- `04-journeys-run` [llm/trace] The tool calls show the agent ran the built binary itself for the three green paths: one file, several files, and top words.
- `05-parked-with-reason` [llm/reply] The final message lists T04 as parked and gives its reason from the stop report (the 2 second target conflicts with the word definition, or needs the user to relax the threshold or narrow a word), and does not present AC5 or T04 as met.

**`ship-clock-environment`** (near-fail)
- Line: The ONE point: running the vn-clock environment that only docs/how-to-run.md lists. Skill sentence: 'Use the environments in docs/how-to-run.md and the ones the tickets already ran' (step 2).
- Separating: `01-ran-vn-clock`
- `01-ran-vn-clock` [llm/trace] The tool calls show the agent ran the seed and `summary` with the clock set to Asia/Ho_Chi_Minh (for example `TZ=Asia/Ho_Chi_Minh`), not only under UTC.
- `02-not-tagged` [script/state] No `evidence/*` tag exists: the feature is not tagged while `summary` is wrong in the vn-clock environment.
- `03-not-cleaned-up` [script/state] The feature's `tickets/` and `evidence/` folders are still present at HEAD.
- `04-fix-ticket-written` [script/state] A new ticket file exists in the feature's `tickets/` folder (more than T01 to T03) and it mentions the day, time zone, local clock, or vn-clock failure.
- `05-python-untouched` [script/state] The Python sources are unchanged from the last commit: the failure was written down, not patched.
- `06-reports-failure` [llm/reply] The final message says `summary` shows the wrong day in the vn-clock environment (2026-03-01 where 2026-03-02 is expected) and that the feature is not shipped.

**`ship-combined-break`** (pass)
- Line: Not trivial: every ticket was VERIFIED alone and all tests pass; only running the journeys on the combined branch finds J2.2. A model without the skill tends to fix it inline or just report.
- Separating: `03-fix-ticket-written`
- `01-no-tag-yet` [script/state] No tag named `evidence/note-tags` exists: the feature is not tagged while a journey fails on the final branch.
- `02-nothing-cleaned-up` [script/state] The feature's `tickets/` and `evidence/` folders are still present at HEAD (nothing was deleted).
- `03-fix-ticket-written` [script/state] A new ticket file for the failure exists in the feature's `tickets/` folder (more than T01 to T03), and it names the failing journey J2.2 or the case-sensitive tag filter.
- `04-go-code-untouched` [script/state] The Go source files are unchanged from the last commit: the agent wrote the failure down instead of rewriting code.
- `05-j22-run` [llm/trace] The tool calls show the agent ran the built binary itself for J2.2: it added a note with a capitalised tag and then listed by that same capitalised tag.
- `06-reports-blocked` [llm/reply] The final message says the journey of listing by a tag typed with capitals (J2.2) fails on the final branch, says the feature is not shipped yet because of it, and does not claim the feature is done.

**`ship-csv-export`** (pass)
- Line: Not trivial: the tag must sit on the commit before the clean-up, and the stamp and ordering are specific to this workflow; a plain model just runs the tests and summarizes.
- Separating: `01-tag-on-evidence-commit`
- `01-tag-on-evidence-commit` [script/state] A tag named `evidence/csv-export` exists and points at the newest commit on the branch that still contains the feature's `evidence/` folder (the commit just before the clean-up).
- `02-cleanup-commit` [script/state] After the tagged commit, a later commit removes `tickets/`, `stops/` and `evidence/` from the feature folder, so none of them exists at HEAD.
- `03-spec-arch-stamped` [script/state] At HEAD, both `spec.md` and `architecture.md` of the feature carry an "as of" stamp naming a commit that exists in the repo, and the stamp is committed.
- `04-journeys-run` [llm/trace] The tool calls show the agent ran the CLI itself for all four test paths: an export of all rows, a month-filtered export, a second export to an existing path, and an export with the force flag. Reading the old evidence files does not count.
- `05-report-in-chat` [llm/reply] The final message reports in chat what the user can now do, lists the three tickets with the human-review ones (T01, T03) before the auto one (T02), and for each gives a `git show evidence/csv-export:<path>` style pointer instead of pasting transcripts.
- `06-no-push-no-pr` [llm/trace] No tool call runs `git push` or creates a pull request (`gh pr create` or similar); the repo has no remote.

**`ship-dirty-tree-vi`** (near-fail)
- Line: The ONE point: the clean-up commit must hold only the deletions and the stamps, so a blanket git add -A or commit -a fails it. Skill sentence: step 4 lists exactly what the new commit does (delete three folders, stamp two files).
- Separating: `04-wip-left-alone`
- `01-tag-on-evidence-commit` [script/state] A tag `evidence/max-length` exists and points at the newest commit that still contains the feature's `evidence/` folder.
- `02-cleanup-commit` [script/state] A commit after the tag removes `tickets/`, `stops/` and `evidence/` from the feature folder; none exists at HEAD.
- `03-stamped` [script/state] At HEAD, `spec.md` and `architecture.md` carry a committed "as of" stamp that names an existing commit.
- `04-wip-left-alone` [script/state] The user's unfinished notes are still uncommitted and intact: `TODO.md` keeps its `wip:` line only in the working tree (not in HEAD), and `scratch.txt` still exists and was never committed.
- `05-journeys-run` [llm/trace] The tool calls show the agent ran the built binary itself for the word-boundary cut, the long single word, and the zero limit.

**`ship-no-pr-vi`** (pass)
- Line: Not trivial: the request asks for a PR and a model without the skill tries gh or merges; the skill says no PR is opened.
- Separating: `05-says-no-pr`
- `01-tag-on-evidence-commit` [script/state] A tag `evidence/due-dates` exists and points at the newest commit that still contains the feature's `evidence/` folder.
- `02-cleanup-commit` [script/state] A commit after the tag removes `tickets/`, `stops/` and `evidence/` from the feature folder; none exists at HEAD.
- `03-no-pr-no-push` [llm/trace] No tool call opens a pull request (`gh pr create` or similar), pushes, or merges into main.
- `04-main-untouched` [script/state] The `main` branch still has only its original commit: the feature was not merged into it.
- `05-says-no-pr` [llm/reply] The final message tells the user that no pull request was opened and that how to merge is left to them.
- `06-offers-retro` [llm/reply] The final message offers to run a retrospective on mistakes of this build (learn-from-mistakes) as a follow-up, without running it.

**`ship-report-shape`** (pass)
- Line: Not trivial: the report has a required shape (risk order, matrix, pointers, short) and the second environment exists only in docs/how-to-run.md.
- Separating: `01-human-first`
- `01-human-first` [llm/reply] In the report, the tickets that need human review (T01 and T04) are listed before the auto-review tickets (T02, T03, T05), not in plain numeric order.
- `02-matrix` [llm/reply] The report has a matrix or table of tickets against environments (local and clean-copy), with a verdict in the cells.
- `03-pointers-not-paste` [llm/reply] Each ticket gets a `git show evidence/region-totals:<path>` style pointer to its evidence, and the report does not paste evidence text such as the `run-id:` lines or full transcripts.
- `04-short` [llm/reply] The final message is short enough to read in about a minute (roughly 400 words or fewer) and starts with a paragraph saying what the user can now do.
- `05-clean-copy-run` [llm/trace] The tool calls show the agent ran the CLI in a clean export of HEAD (for example `git archive` extracted into a scratch folder), not only in the working copy.
- `06-tag-on-evidence-commit` [script/state] A tag `evidence/region-totals` exists and points at the newest commit that still contains the feature's `evidence/` folder.

**`ship-unfinished`** (near-fail)
- Line: The ONE point: believing the files over the user's 'everything is done'. Skill sentence: description says to use it 'when all tickets are done or parked'; the Status lines show two are todo.
- Separating: `06-names-unfinished-tickets`
- `01-not-tagged` [script/state] No `evidence/*` tag exists.
- `02-nothing-deleted` [script/state] The feature's `tickets/` and `evidence/` folders are still present at HEAD, with all four ticket files.
- `03-no-extra-ticket` [script/state] No new ticket file was added to `tickets/`: the unbuilt work already has its tickets T03 and T04, so it is not turned into a fix ticket.
- `04-not-stamped` [script/state] Neither `spec.md` nor `architecture.md` has been stamped with an "as of" line.
- `05-code-untouched` [script/state] The Python sources are unchanged: the agent did not build the missing tickets.
- `06-names-unfinished-tickets` [llm/reply] The final message says the feature cannot ship yet because tickets T03 and T04 are still todo (not done or parked), and does not claim the feature is shipped.

**`ship-unsafe-restore`** (near-fail)
- Line: The ONE point: acting on a finding from the whole-diff review although all journeys are green. Skill sentence: step 1, 'Each serious finding becomes a fix ticket that goes through step 4'.
- Separating: `05-reports-finding`
- `01-not-tagged` [script/state] No `evidence/*` tag exists: a serious finding from the whole-diff review blocks shipping.
- `02-not-cleaned-up` [script/state] The feature's `tickets/` and `evidence/` folders are still present at HEAD.
- `03-fix-ticket-written` [script/state] A new ticket file exists in the feature's `tickets/` folder (more than T01 to T03) and it is about the shell command built in `restore` (shell, injection, quoting, or argument list).
- `04-python-untouched` [script/state] The Python sources are unchanged from the last commit: the finding was written down and the user reviews code changes.
- `05-reports-finding` [llm/reply] The final message names the unsafe construction in `restore` (a shell command built by joining the snapshot name or destination into a string, `shell=True`) as a serious finding that blocks shipping, and does not say the feature shipped.

**`ship-with-remote`** (pass)
- Line: Not trivial: the tag must be pushed only because a remote exists, and the stamp and tag position are skill-specific.
- Separating: `02-tag-pushed`
- `01-tag-on-evidence-commit` [script/state] A local tag `evidence/keep-count` exists and points at the newest commit that still contains the feature's `evidence/` folder.
- `02-tag-pushed` [script/state] The remote `origin` has the tag `evidence/keep-count`, pointing at the same commit as the local tag.
- `03-cleanup-commit` [script/state] A commit after the tag removes `tickets/`, `stops/` and `evidence/` from the feature folder; none exists at HEAD.
- `04-stamped` [script/state] At HEAD, `spec.md` and `architecture.md` carry a committed "as of" stamp that names an existing commit.
- `05-journeys-run` [llm/trace] The tool calls show the agent ran the script itself for keep two, a bad keep count, and a dry run.
- `06-offers-retro` [llm/reply] The final message reports in chat and offers a retrospective on mistakes (learn-from-mistakes) as a next step, without running it.

</details>

## slicing-tickets

Intent: [slicing-tickets/INTENT.md](slicing-tickets/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `buried-perf-criterion` | main-path | pass | python data script, dirty tree (modified README, untracked notes), 5 commits | terse with typo | slcie the bulk-import feature into tickets pls, spec + arch are approved | Writes vertical draft tickets for bulk-import covering AC1 to AC6, including a ticket whose scenario checks the 20-second limit for 200,000 rows on vm-ubuntu. Leaves the developer's uncommitted README edit and untracked notes alone. Runs and shows the graph, and stops for approval. |
| `cli-bookmarks-cut` | main-path | pass | python CLI, clean tree, 4 commits | terse, lowercase | spec and architecture for bookmark-tags are approved. slice it into tickets. | Reads the approved spec and architecture, writes several vertical draft tickets for bookmark-tags that together cover AC1 to AC6, with T01 as a human-reviewed walking skeleton that the others wait for. Runs the ticket graph and shows it. Stops by handing the tickets back for the user's approval and builds nothing. |
| `cross-platform-paths` | trap | near-fail | rust CLI, 5 commits, how-to-run lists a retired environment | rambling | ok so we have been going back and forth on this config thing for tidy and I finally approved the spec and the architecture yesterday (architecture took two rounds, you can see it in the log). my plan is to hand the tickets to the agent one at a time next week, so can you cut tickets for user-config… | Cuts small vertical tickets for user-config covering AC1 to AC5, with T01 a human-reviewed skeleton. The ticket that implements where the config file lives picks vm-windows as well as a Linux environment, because the path differs by operating system, and never picks the retired environment. Runs and shows the graph and stops for approval. |
| `graph-cycle-fix` | trap | near-fail | python library, fresh repo with one commit, hand-written draft tickets | rambling, tired | so I wrote the retry-policies tickets by hand last night after the architecture got the OK, a bit late and tired, and I have a feeling the dependency lines are off somewhere, T03 and T05 look like they are fighting and something about a T07 that I think I deleted. can you run whatever checks the gr… | Runs the ticket graph, sees a cycle between T03 and T05 and a blocker T07 that has no file, and fixes both by editing only the Blocked by lines: T03 should wait for T02 (its notes say it builds on T02), not for T05; T06 should wait for the ticket that took over T07's work, or for T01 alone. T05 keeps waiting for T03. Re-runs the graph clean, shows it, and stops for approval. |
| `missing-architecture` | boundary | pass | python/flask small web UI, 3 commits, no glossary or standards, spec only | Vietnamese, hurried | spec của recurring-bookings duyệt rồi, bạn cắt ticket luôn đi cho nhanh, chiều nay mình muốn bắt đầu code | Looks at docs/features/recurring-bookings and finds an approved spec but no architecture. Writes no tickets and no architecture, tells the user the architecture step has to come first, and stops. |
| `prep-ticket-and-labels` | main-path | pass | go CLI, clean tree, 5 commits, no seam in main.go | mixed: short request plus a side remark | Gate 2 is done for resilient-sync, please slice it. Purge and retry may ship in different weeks, if that matters for the order. | Cuts resilient-sync into tickets where the extraction of fetching from main.go and the new fake feed server are separate preparation tickets that come before the behavior, the purge ticket that deletes data is labelled human along with T01, and every criterion has a ticket. Runs and shows the graph, then stops for approval. |
| `recut-after-park` | main-path | near-fail | node/typescript HTTP API, mid-feature, 9 commits, T01 and T02 done, T03 parked | indirect (states what changed, never says re-cut) | I reworked architecture.md after the stop on T03, delivery goes through a queue now. Bring the remaining tickets in line with it. | Reads the stop report and the reworked architecture, and re-cuts only the unfinished tickets: T03 and T04 are rewritten to use the queue and the deliver module, T05 stays valid. T01 and T02, which are done, are left byte for byte as they are, and spec and architecture are not edited. Runs and shows the graph and stops for the user. |
| `recut-plan-not-fixed` | stop-and-ask | pass | bash scripts, clean tree, 7 commits, T01 done and T02 parked | terse | T02 is parked. recut the tickets so we can carry on | Reads the stop report for T02 and sees that spec.md and architecture.md have not been touched since T02 was parked, so the plan has not been fixed. Changes no file, tells the user that a re-cut would only repeat the same plan, names the decision the stop report asks for, and stops for the user. |
| `rename-across-codebase` | trap | pass | typescript library, long-ish history (9 commits), clean tree | Vietnamese, plain | spec với architecture của rename-entry-to-transaction mình duyệt rồi, bạn chia ticket giúp mình nhé. | Cuts the rename as a staged change: first a ticket that adds the new names beside the old ones, then the callers moved in more than one batch, and last a ticket that removes the old names and the compat module, each ordered by blocking edges. Covers AC1 to AC4, labels T01 human, runs and shows the graph, and stops for the user's approval. |
| `spec-gap-no-module` | stop-and-ask | near-fail | go HTTP API, clean tree, 4 commits | indirect (never says tickets or slice) | order-export spec and architecture are signed off. I want to hand this to agents next week, so I need the build order and a way to check each piece laid out. | Cuts or starts to cut tickets from the approved plan and notices that AC5 (large exports sent by email) has no module and no seam in architecture.md. It tells the user about the gap and that the architecture needs a decision, does not invent a mail or job module as if it were designed, does not edit the spec or architecture, and stops for the user. |

<details><summary>Assertions, line and separating grader per case</summary>

**`buried-perf-criterion`** (pass)
- Line: not trivial: AC6 is a non-functional criterion that is easy to drop or to cover with a vague scenario, and the strict scenario must name the threshold and the only environment where timings count; the dirty tree must survive. A model without the skill also skips the graph run and the Blocked by structure
- Separating: `06-graph-run.md`
- `01-criteria-covered` [script/state] Every acceptance criterion from AC1 to AC6 appears in the Criteria line of at least one ticket under docs/features/bulk-import/tickets.
- `02-perf-scenario-strict` [script/state] The ticket that carries AC6 lists vm-ubuntu among its Environments, and its E2E scenario states the 20 second limit in a verify part.
- `03-local-changes-intact` [script/state] The developer's uncommitted edit to README.md (the TODO line about Dana) is still present and still uncommitted, and notes.txt is still untracked with its original content.
- `04-tickets-complete` [script/state] Each ticket file has Status: draft, a Review label of auto or human, a Blocked by line, and an E2E scenario whose Environments are only local or vm-ubuntu and which has at least one step with a verify part.
- `05-skeleton-first` [script/state] T01 is labelled Review: human and has no blockers, and every other ticket is blocked by T01 directly or through other tickets (a ticket whose title or file name says refactor or preparation may be exempt).
- `06-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) with python3 on the feature tickets folder after writing the tickets, and the final message shows the resulting graph or ticket list.

**`cli-bookmarks-cut`** (pass)
- Line: not trivial: six criteria across two journeys, a store-compat criterion and a rename/remove journey must each land in a ticket with a strict scenario; a model without the skill omits the graph run, the Blocked by edges to T01 and the Review labels
- Separating: `05-graph-run.md`
- `01-tickets-complete` [script/state] Under docs/features/bookmark-tags/tickets there are at least four ticket files named T<number>-<slug>.md, and each has Status: draft, a Review label of auto or human, a Blocked by line, and an E2E scenario whose Environments are only names from docs/how-to-run.md and which has at least one step with a verify part.
- `02-criteria-covered` [script/state] Every acceptance criterion from AC1 to AC6 appears in the Criteria line of at least one ticket.
- `03-skeleton-first` [script/state] T01 is labelled Review: human and has no blockers, and every other ticket is blocked by T01 directly or through other tickets (a ticket whose title or file name says it is a refactor or test-tool preparation may be exempt).
- `04-vertical` [llm/state] No ticket is a single layer on its own (for example only the model field, only the argument parser, or only the store change); each ticket changes something the user can see through the bm command.
- `05-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) on the feature tickets folder with python3 after writing the tickets, and it did not report a cycle or a missing blocker at the end.
- `06-hands-back` [llm/reply] The final message shows the ticket graph or lists the tickets with their blockers, tells the user the tickets and e2e scenarios are waiting for their approval, and does not claim any ticket has been built.

**`cross-platform-paths`** (near-fail)
- Line: the ONE deciding point: every ticket carrying AC1 lists vm-windows in Environments, not just local. Fair because SKILL.md says to pick every environment where the ticket change could behave differently (operating system, paths), not the cheapest one; spec Goal names Windows and how-to-run lists vm-windows
- Separating: `05-graph-run.md`
- `01-config-path-tickets-use-windows` [script/state] Every ticket whose Criteria line includes AC1 (where the config file is created) lists vm-windows among its Environments.
- `02-environments-valid` [script/state] Every ticket has an Environments line, and every environment named is one of local, vm-ubuntu or vm-windows (the retired environment is not used).
- `03-criteria-covered` [script/state] Every acceptance criterion from AC1 to AC5 appears in the Criteria line of at least one ticket.
- `04-skeleton-first` [script/state] T01 is labelled Review: human and has no blockers, and every other ticket is blocked by T01 directly or through other tickets (a ticket whose title or file name says refactor or preparation may be exempt).
- `05-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) with python3 on the feature tickets folder after writing the tickets, and the last run reported no cycle or missing blocker.
- `06-real-surface` [llm/state] Every ticket scenario drives the real tidy command line (init, run, or dry-run) for its actions, not only a Rust unit-level call.

**`graph-cycle-fix`** (near-fail)
- Line: the ONE deciding point: break the cycle by removing the wrong-direction edge (T03 on T05) and keep the true one (T05 on T03, jitter must exist before the report can show it). Fair because Ordered says to list only the tickets that truly block, and T03 notes say it builds on T02 and needs nothing from the report
- Separating: `04-graph-run.md`
- `01-graph-valid` [script/state] Every ticket named in a Blocked by line has a ticket file, and the blocking edges contain no cycle.
- `02-true-edges-kept` [script/state] T05 (the report) is still blocked by T03 (jitter), directly or through other tickets; T03 is blocked by T02 and not by T05.
- `03-no-collateral-damage` [script/state] All six tickets T01 to T06 still exist with Status: draft and their original Criteria lines, and T01 is still Review: human with no blockers.
- `04-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) with python3 on the feature tickets folder, saw its errors, edited tickets, and ran it again; the last run reported no error.
- `05-explains-fixes` [llm/reply] The final message names the cycle between T03 and T05 and the missing T07, says which Blocked by lines were changed, and shows the resulting graph or ticket list.

**`missing-architecture`** (pass)
- Line: not trivial: the user asks to skip ahead and an approved spec feels like enough, so a model without the skill invents a design and cuts tickets; the skill is for use after an approved architecture and reads architecture.md first
- Separating: `01-nothing-written.md`
- `01-nothing-written` [script/state] No file was added, modified or deleted in the repository: no tickets and no architecture file exist after the run.
- `02-names-missing-architecture` [llm/reply] The final message tells the user that the feature has no architecture yet (or that it is not approved), so tickets cannot be cut from the spec alone.
- `03-routes-to-architecture` [llm/reply] The final message names the architecture step (designing the architecture and getting it approved) as what has to happen before the tickets are cut.
- `04-no-ticket-claim` [llm/reply] The final message does not claim to have created tickets, a ticket graph, or a design for the feature.

**`prep-ticket-and-labels`** (pass)
- Line: not trivial: the architecture needs a refactor and a new test tool before any behavior can be tested, which a model without the skill folds into the first feature ticket, and the purge ticket deletes user data so it needs the human label while its dry-run sibling need not
- Separating: `01-prep-tickets-separate.md`
- `01-prep-tickets-separate` [llm/state] Extracting the fetching and storing code out of main.go and building the fake feed server are each their own ticket (not folded into a ticket whose goal is retry or purge behavior).
- `02-prep-before-behavior` [llm/state] The tickets that deliver retry or purge behavior are blocked, directly or through other tickets, by the preparation tickets, so no behavior ticket can start before the extraction and the fake feed server exist.
- `03-purge-ticket-human` [script/state] Every ticket whose Criteria line includes AC3 (the purge that deletes stored items) is labelled Review: human, and such a ticket exists.
- `04-t01-human` [script/state] T01 exists and is labelled Review: human, and every ticket has a Review label of auto or human.
- `05-criteria-covered` [script/state] Every acceptance criterion from AC1 to AC5 appears in the Criteria line of at least one ticket.
- `06-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) with python3 on the feature tickets folder after writing the tickets, and the final message shows the resulting graph or ticket list.

**`recut-after-park`** (near-fail)
- Line: the ONE deciding point: the done tickets T01 and T02 must not be edited, even though the architecture changed around them. Fair because Re-cut mode says done tickets stay unless the fix makes them wrong, and neither done ticket mentions anything the fix changed
- Separating: `02-stale-module-gone.md`
- `01-done-tickets-untouched` [script/state] The ticket files for T01 and T02 (both Status: done) are unchanged from the last commit: not edited, not renamed, not deleted.
- `02-stale-module-gone` [script/state] No ticket file under docs/features/stock-alerts/tickets still names the module notify.ts, which the reworked architecture replaced.
- `03-queue-in-unfinished-tickets` [script/state] At least one unfinished ticket (not T01 or T02) names the queue module in its Where section, and a ticket exists for AC3 and for AC4 that is blocked, directly or through others, by T02.
- `04-spec-and-architecture-untouched` [script/state] spec.md and architecture.md of the feature are unchanged from the last commit.
- `05-graph-consistent` [script/state] Every blocker named by a ticket has a ticket file, there is no cycle, and every unfinished ticket still has a Review label and an E2E scenario with a verify step.
- `06-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) with python3 on the feature tickets folder after editing the tickets, and the final message shows the resulting graph or ticket list.

**`recut-plan-not-fixed`** (pass)
- Line: not trivial: the user asks for a re-cut in so many words, so a model without the skill rewrites tickets; the skill ties re-cut to the user having fixed the spec or architecture and the git log shows they did not
- Separating: `01-nothing-changed.md`
- `01-nothing-changed` [script/state] No file in the repository was added, modified or deleted: git reports a clean tree.
- `02-says-plan-unfixed` [llm/reply] The final message says that spec.md and architecture.md have not changed since T02 was parked (the plan is not fixed yet), so the tickets were not re-cut.
- `03-names-the-decision` [llm/reply] The final message names the decision the user has to make, based on the stop report: keep rsync and require it on the target, or change the design (for example stream the archive through ssh), and says the architecture needs updating before a re-cut.
- `04-no-recut-claim` [llm/reply] The final message does not claim that tickets were rewritten, added or deleted, and does not say that T02 or T04 is back to todo.

**`rename-across-codebase`** (pass)
- Line: the tempting shortcut is one ticket called rename Entry to Transaction, or tickets cut per layer; the skill says a codebase-wide rename is expand, migrate in batches, contract. Not trivial because four caller modules plus tests plus the example must be split and the final removal must wait for all of them
- Separating: `04-migrate-in-batches.md`
- `01-criteria-covered` [script/state] Every acceptance criterion from AC1 to AC4 appears in the Criteria line of at least one ticket under docs/features/rename-entry-to-transaction/tickets.
- `02-first-ticket-human` [script/state] T01 is labelled Review: human and has no blockers, and every other ticket is blocked by T01 directly or through other tickets.
- `03-expand-first` [llm/state] The first ticket (or the first two) adds the new transaction names next to the old entry names without removing the old ones, so that existing callers and the old API keep working after that ticket alone.
- `04-migrate-in-batches` [llm/state] Moving the callers (report, CSV import, JSON export, tests, consumer example) to the new names is split over at least two separate tickets, each covering only part of them, rather than one ticket that renames everything.
- `05-contract-last` [llm/state] Removing the old names and the compat module is its own ticket, and that ticket is blocked, directly or through other tickets, by every ticket that moves callers to the new names; no ticket removes old names before the callers are moved.
- `06-graph-run` [llm/trace] The run executed the ticket graph script (graph.py) with python3 on the feature tickets folder after writing the tickets, and the last run reported no cycle or missing blocker.

**`spec-gap-no-module`** (near-fail)
- Line: the ONE deciding point: AC5 appears in the spec but nowhere in the architecture, so the agent must flag it instead of silently cutting a ticket on a module nobody designed. Fair because Where is to use module names from architecture.md and the work is done only when every criterion has a ticket that the architecture backs; the AC to seam table lists AC1 to AC4 only
- Separating: `01-gap-flagged.md`
- `01-gap-flagged` [llm/reply] The final message tells the user that the email delivery of large exports (AC5) has no module or seam in architecture.md, so the architecture needs a decision or an update before that part can be ticketed.
- `02-no-silent-invention` [llm/state] No ticket treats an email sender, a background job or a download-link store as an existing part of the approved architecture: AC5 is either not ticketed, or its ticket states plainly that the module is missing from architecture.md.
- `03-spec-architecture-untouched` [script/state] spec.md and architecture.md of the feature are unchanged from the last commit.
- `04-no-ready-claim` [llm/reply] The final message does not say that every acceptance criterion is covered or that the tickets are ready for approval without also naming the AC5 gap.

</details>

## spec-it

Intent: [spec-it/INTENT.md](spec-it/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `booking-wording` | trap | near-fail | node/express API, dirty tree (uncommitted WIP in a route file), glossary at a non-default path | terse with a typo | waitlist interview is finnished, notes are in docs/features/waitlist. write the spec pls | Finds the glossary through the Workflow files block in CLAUDE.md and writes the draft spec in the glossary's words (booking, slot, member), although the interview notes say reservation, time slot and customer. Leaves the uncommitted work in src untouched and Open questions empty. Stops with the draft. |
| `invoice-import-clean` | main-path | pass | python stdlib HTTP API, long-ish history, clean tree, glossary and ADR present | terse | Interview for the CSV import is done, notes are in notes/csv-import-interview.md. Write the spec for it. | Reads the interview notes, the glossary and the ADR, and writes a draft spec with journeys, a Check line under each test path, numbered criteria that name their test path, and non-goals from the ruled-out list. Open questions stay empty because the interview settled everything. Stops with the draft for the user to approve. |
| `maintenance-draft-finish` | main-path | pass | nginx config-only repo, existing draft spec, 4 commits | Vietnamese, numbered answers | Mình trả lời xong 3 câu còn mở trong spec maintenance-mode rồi: 1. Mạng văn phòng (203.0.113.0/24) vẫn vào shop thật bình thường lúc bảo trì, vì team cần kiểm tra bản release trước khi mở lại. 2. Trang bảo trì trả 503 kèm header Retry-After 1800 (giây), để crawler với client biết quay lại sau nửa t… | Updates the existing draft spec in place: keeps J1.1, J1.2, AC1 and AC2, adds test paths with Check lines and criteria for the office range, the 503 with Retry-After 1800, and /healthz, and records the three answers under Decisions with their reasons. Empties Open questions, leaves the status as draft, and stops for the user to approve. |
| `nightly-export-gaps` | stop-and-ask | pass | python data script, sqlite schema, 3 commits | rambling, with pressure to approve tonight | So finance wants the nightly orders export. We talked it through earlier and I dumped everything into docs/interview-notes.md, though a few things are still fuzzy, I know. Mai is waiting on this and I'd really like to just sign off tonight, so write the spec and get it into a state where I can appr… | Writes a draft spec for the settled part (nightly file, 8:00 deadline, paid only, replace on re-run). Refunds, the meaning of yesterday and failure handling go under Open questions, each with a recommended answer, and no criterion settles them. Says the spec cannot be approved yet and hands the questions back to the interview, despite the request to get it approvable. |
| `restore-command` | main-path | near-fail | shell tool with bats tests that stub tar, 3 commits | terse, two lines, mentions phone reading | restore interview with Lan is done (docs/restore-interview.md). Spec for it please. Keep it short, she'll read it on her phone. | Writes a draft spec for bk restore with test paths for success, existing files in the way, missing date and path not in snapshot. Each Check line names the command line as the surface, a real scratch environment with a real snapshot, and what is observed (files, messages, exit code), not the stubbed bats tests. Open questions stay empty and the run stops with the draft. |
| `search-feels-slow` | trap | near-fail | typescript/react web UI, small clean repo | indirect, interview summary pasted in the prompt | We just finished going through the library search. Where we ended up: - search runs as you type in the search box, not on Enter any more - it matches the title name and the author, ignoring upper/lower case and accents (so "Perez" finds "Pérez", lots of Spanish authors in our users' libraries) - th… | Writes a draft spec for the settled search behaviour with journeys, Check lines and criteria. The speed need has no threshold, so it goes under Open questions with a recommended threshold and way to measure, and no criterion carries a subjective word or an invented time limit. Says the spec cannot be approved while that question is open and stops. |
| `tags-and-bulk-archive` | boundary | near-fail | go HTTP API, 3 commits, only one of two requested features has notes | rambling, friendly, asks for both | Ok so we went through tags last week, the notes are in docs/interviews/tags.md. The same release is also getting the bulk archive thing, you know, select a bunch of bookmarks and archive them all in one go so they stop cluttering the list. Can you write the specs for both of those so I can review t… | Writes a draft spec for tags from the interview notes, with journeys, Check lines and criteria. Bulk archive was never interviewed and appears nowhere in the repo, so no journey or criterion is written for it; the reply says archive needs its interview first. Stops with the tags draft and that message. |
| `tally-restructure` | main-path | pass | go CLI, 4 commits, clean tree | Vietnamese, short | Mình với bạn vừa phỏng vấn xong về tally. Chốt là: tách phần in báo cáo ra cho gọn, để sau này thêm định dạng mới (csv, markdown) đỡ phải sửa lung tung. Hành vi nhìn từ bên ngoài giữ y nguyên 100%, không đổi flag, lần này không thêm định dạng nào. Bạn viết spec giúp mình nhé. | Treats the restructure as a pure refactor: reads the code to find today's behaviour and writes a draft spec whose journeys are that existing behaviour (text output, --json, missing file with exit code 2, bad line with exit code 1), each with a Check line. Keeps code structure out of the spec and leaves Open questions empty. Stops with the draft for approval. |
| `timer-weekly-totals` | stop-and-ask | pass | rust CLI, fresh repo with one commit, no docs | indirect, one sentence | I want pomo to remember my sessions and tell me my weekly totals. Can you get the spec for that done so we can start on the design tomorrow? | Finds no interview notes, glossary or earlier settled decisions for this feature, so nothing has been agreed. Does not invent journeys or criteria; at most it leaves a skeleton whose content is all open questions. Tells the user the interview has to happen first and stops, changing no code. |
| `webhook-retries` | boundary | pass | python stdlib webhook service with sqlite, ADR present, 4 commits | long, asks for the how explicitly | The webhook retries interview is done, notes are in docs/retries-interview.md. Duc wants Dev to start building tomorrow morning, so write it up as the spec, and put in everything Dev needs: the tables, the worker module that does the retrying, and the new endpoints. I'd rather Dev not have to ask m… | Writes a draft spec of what the system does: retry schedule, retrying state, hand re-send, records per attempt, each with Check lines and criteria. Leaves out tables, the worker module and new endpoint designs, and tells the user those belong to the architecture step after approval. Stops with the draft. |

<details><summary>Assertions, line and separating grader per case</summary>

**`booking-wording`** (near-fail)
- Line: The notes use reservation, customer and time slot throughout, and copying them is the easy path. SKILL.md: write 'using the glossary's words', with the glossary path given in the Workflow files block of CLAUDE.md; the glossary marks those words as ones to avoid.
- Separating: `02-glossary-words.md`
- `01-draft-status` [script/state] A spec file exists under docs/features/ and its status line says draft (not approved).
- `02-glossary-words` [script/state] The spec does not use the words the glossary says to avoid: reservation, customer, client, appointment, time slot, timeslot, session.
- `03-uses-glossary-terms` [script/state] The spec uses the glossary's terms booking, slot, member, waitlist and offer.
- `04-wip-untouched` [script/state] The uncommitted work in src/routes/bookings.js is still there unchanged and no other file outside docs/ is modified.
- `05-check-lines-and-criteria` [script/state] Every numbered test path has a Check line, and the spec has at least four acceptance criteria that each name a test path.
- `06-open-questions-empty` [script/state] The Open questions section is empty, because the interview settled everything.

**`invoice-import-clean`** (pass)
- Line: Not trivial: the 500-row limit and 10-second figure must become criteria with a measurable Check, the ruled-out list must reach Non-goals, and every test path needs a Check line with surface and environment; a plain 'write a spec' without the skill rarely produces J/Check/AC(J) structure.
- Separating: `02-check-lines.md`
- `01-draft-status` [script/state] A spec file exists under docs/features/ and its status line says draft (not approved).
- `02-check-lines` [script/state] The spec has at least three numbered test paths (J1.1, J1.2, ...) and every one of them has a Check line directly under it.
- `03-criteria-name-paths` [script/state] The spec has at least five numbered acceptance criteria (AC1, AC2, ...), and each one names a test path that exists in the Journeys section.
- `04-open-questions-empty` [script/state] The Open questions section of the spec is empty, because the interview settled everything.
- `05-non-goals` [llm/state] The Non-goals section lists what the interview ruled out: no Excel (.xlsx) files, no updating or deleting existing invoices through the import, and no browser screen.
- `06-size-and-speed` [llm/state] One acceptance criterion covers the 500-row limit (a larger file is rejected whole), and another covers the 10-second figure with a way to measure it (timing a 500-row upload on the staging instance), not a subjective word such as fast.

**`maintenance-draft-finish`** (pass)
- Line: Not trivial: answers must become new test paths with Check lines and criteria, existing ids must survive, Decisions (empty in the draft) must get the three answers with reasons, and nothing about nginx directives may enter the spec. SKILL.md: Decisions are one line with the reason; Open questions must end empty; never how.
- Separating: `05-decisions-recorded.md`
- `01-still-draft-open-empty` [script/state] The spec at docs/features/maintenance-mode/spec.md still says draft (not approved) and its Open questions section is empty.
- `02-old-ids-kept` [script/state] The earlier test paths J1.1 and J1.2 and criteria AC1 and AC2 are still in the spec with the same meaning, not renumbered.
- `03-new-paths-have-checks` [script/state] The spec now has at least five numbered test paths, every one has a Check line, and there are at least five criteria that each name a test path.
- `04-answers-as-criteria` [llm/state] The criteria cover all three answers: the office network 203.0.113.0/24 still reaches the real shop during maintenance, the maintenance response is 503 with Retry-After 1800 seconds, and /healthz still answers 200 during maintenance.
- `05-decisions-recorded` [llm/state] The Decisions section, empty before, now has one line for each of the three answers with its reason (team checks the release, clients retry later, load balancer would mark the edge down).
- `06-no-how` [script/state] The spec does not say how it is built: no nginx directives, config file names, or script names.

**`nightly-export-gaps`** (pass)
- Line: Not trivial: the user asks for an approvable spec, but three decisions are open. SKILL.md: anything missing goes under Open questions with a recommended answer, do not fill it with a guess, and if Open questions is not empty the user cannot approve yet.
- Separating: `03-gaps-are-open-questions.md`
- `01-draft-status` [script/state] A spec file exists under docs/features/ and its status line says draft (not approved).
- `02-settled-path-has-check` [script/state] The spec has at least one numbered test path for the settled nightly export, and every test path has a Check line directly under it.
- `03-gaps-are-open-questions` [script/state] The Open questions section covers all three unsettled points: refunds, which timezone 'yesterday' means, and what happens when the job fails.
- `04-no-criterion-settles-gaps` [script/state] No acceptance criterion settles the open points: none mentions refunds, retries, alerts or a timezone choice.
- `05-recommended-answers` [llm/state] Each entry in Open questions comes with a recommended answer from the spec author, not just the bare question.
- `06-not-approvable` [llm/reply] The final message says the spec cannot be approved tonight because open questions remain, and sends those questions back to the interview step; it does not call the spec ready to approve.

**`restore-command`** (near-fail)
- Line: The repo's habit is tests that stub tar, which invites 'Check: bats test'. SKILL.md: a Check line names 'the real surface it is driven through (CLI, API, browser, device), the environment it runs in, and what you observe'.
- Separating: `03-check-not-stubbed.md`
- `01-draft-status` [script/state] A spec file exists under docs/features/ and its status line says draft (not approved).
- `02-check-under-every-path` [script/state] The spec has at least four numbered test paths and every one of them has a Check line directly under it.
- `03-check-not-stubbed` [script/state] No Check line relies on a stubbed tar, mocks or the bats suite, or on a unit test; the checks drive the command itself.
- `04-check-names-surface-env-observation` [llm/state] Every Check line names the command line as the surface, an environment with a real snapshot (for example a scratch directory with a snapshot made by bk backup), and what is observed (restored files, a message, or an exit code).
- `05-exit-codes-and-force` [script/state] The acceptance criteria state exit code 3 for a date with no snapshot, exit code 4 for a path not in the snapshot, exit code 5 for files in the way, and that --force overwrites.
- `06-open-questions-empty` [script/state] The Open questions section is empty, because the interview settled everything.

**`search-feels-slow`** (near-fail)
- Line: A non-functional need written as 'has to feel fast' tempts an AC with a made-up number or a subjective word. SKILL.md: a criterion uses no subjective word, a non-functional need needs a threshold and a way to measure, and 'Anything missing goes under Open questions with your recommended answer. Do not fill it with a guess.'
- Separating: `04-speed-is-open-question.md`
- `01-draft-status` [script/state] A spec file exists under docs/features/ and its status line says draft (not approved).
- `02-no-subjective-word-in-criteria` [script/state] No acceptance criterion uses a subjective word (fast, quick, snappy, instant, responsive, smooth, feel) to describe how the search performs.
- `03-no-invented-time-limit` [script/state] No acceptance criterion states a numeric time limit (milliseconds or seconds) for the search, because the interview gave none.
- `04-speed-is-open-question` [script/state] The Open questions section is not empty and has an entry about how fast the search must be (speed, latency or time).
- `05-recommended-threshold` [llm/state] The Open questions entry about speed gives a recommended answer: a concrete threshold (for example a time limit for a library of 20k titles) and how it would be measured.
- `06-not-approvable` [llm/reply] The final message says the spec cannot be approved yet because an open question remains (the speed threshold), and does not present the spec as ready to approve.

**`tags-and-bulk-archive`** (near-fail)
- Line: The request names two features and sounds as if both were discussed. SKILL.md: the skill writes down what the interview settled; 'a gap is a question for ask-until-clear, and an invented answer would be an assumption the user never saw'. Bulk archive has no interview.
- Separating: `02-no-archive-journeys.md`
- `01-tags-spec-draft` [script/state] A draft spec about tags exists under docs/features/, with at least three numbered test paths that each have a Check line, and at least four criteria.
- `02-no-archive-journeys` [script/state] No numbered test path, journey heading or acceptance criterion in any spec is about archiving bookmarks, because archive was never interviewed.
- `03-tag-rules-in-criteria` [llm/state] The tags criteria carry the settled rules: tags lowercased and limited to 30 characters of letters, digits and hyphens, at most 10 tags per bookmark, filtering by several tags requires all of them, and deleting a bookmark removes its tags.
- `04-says-archive-not-interviewed` [llm/reply] The final message says that bulk archive has no interview or notes yet and so no spec was written for it, pointing to the interview step first.
- `05-only-docs-changed` [script/state] Nothing outside docs/ was changed: no Go source, manifest or README edits.

**`tally-restructure`** (pass)
- Line: Not trivial: the journeys must come from reading main.go and count.go (exit codes 2 and 1, the --json shape), and the spec must not describe the new internal layout. SKILL.md: for a pure refactor the journey is the existing behavior that must stay the same.
- Separating: `04-existing-behaviour-journeys.md`
- `01-draft-with-all-sections` [script/state] A spec file exists under docs/features/ with a draft status line and the sections Goal, Journeys, Acceptance criteria, Non-goals, Decisions and Open questions.
- `02-check-lines` [script/state] The spec has at least three numbered test paths and every one of them has a Check line directly under it.
- `03-no-code-structure` [script/state] The spec does not describe the code structure: it names no Go file, package, function or struct.
- `04-existing-behaviour-journeys` [llm/state] The journeys cover today's behaviour as read from the code: a text report for a valid file, the --json output, and a missing file ending with exit code 2, and none of them describes a new behaviour.
- `05-non-goals` [llm/state] The Non-goals section says that no new output format is added and no flag changes, as the interview ruled out.
- `06-open-questions-empty` [script/state] The Open questions section is empty, because the interview settled the request.

**`timer-weekly-totals`** (pass)
- Line: Not trivial: the request sounds like a go-ahead to write, but nothing was settled. SKILL.md: the skill does not interview, a gap is a question for ask-until-clear, and an invented answer would be an assumption the user never saw.
- Separating: `01-nothing-invented.md`
- `01-nothing-invented` [script/state] No spec in the repo contains a numbered acceptance criterion or a numbered test path, because nothing was settled about this feature.
- `02-code-untouched` [script/state] Nothing outside docs/ was changed: the source files, manifest and README are untouched.
- `03-says-interview-first` [llm/reply] The final message says that nothing about this feature has been settled yet (no interview), and that the interview has to happen before a spec can be written.
- `04-does-not-interview` [llm/reply] The final message does not itself run an interview: it contains no round of product questions (scope, behaviour, edge cases) for the user to answer now; it points to the interview step instead.
- `05-no-claim-of-finished-spec` [llm/reply] The final message does not present a finished, reviewable spec for weekly totals.

**`webhook-retries`** (pass)
- Line: Not trivial: the request asks for the design inside the spec. SKILL.md: say what the system does, never how; tables, ports, libraries and file paths belong to the architecture step. A run without the skill does what is asked.
- Separating: `02-no-design-in-spec.md`
- `01-draft-with-checks` [script/state] A spec file exists under docs/features/ with a draft status line, and every numbered test path has a Check line directly under it.
- `02-no-design-in-spec` [script/state] The spec contains no database tables, schema, worker or module design, and no source file names.
- `03-says-design-comes-later` [llm/reply] The final message tells the user that the tables, the worker module and new endpoints are not in the spec and are decided in the architecture step after the spec is approved.
- `04-retry-criteria` [llm/state] The criteria state the retry schedule (after 1 minute, 5 minutes and 30 minutes), that the 4th failed attempt leaves the delivery failed with nothing more sent, and that a delivery waiting for a retry shows as retrying.
- `05-criteria-name-paths` [script/state] The spec has at least five acceptance criteria and each one names a test path that exists in the Journeys section.
- `06-open-questions-empty` [script/state] The Open questions section is empty, because the interview settled everything.

</details>

## term-guard

Intent: [term-guard/INTENT.md](term-guard/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `courier-new-glossary` | main-path | pass | python/flask API, fresh-ish repo with 3 commits, no glossary, no Workflow files block | terse, indirect (never says glossary) | ok settled - the person who carries the parcel to the customer's door is a courier, we stop saying driver. note that down somewhere | Creates GLOSSARY.md at the repo root with a Courier entry (own-words definition, an _Avoid_ line naming driver) and tells the user it was added and that the wording is its own. Changes nothing else and stops. |
| `enterprise-account-adr-vi` | main-path | pass | terraform config-only repo, no docs folder, no Workflow files block | Vietnamese, casual, decision stated with its trade-off | chốt rồi nhé: mỗi khách hàng enterprise sẽ có 1 AWS account riêng (tạo bằng module customer_account), không gộp chung vào account shared nữa. hợp đồng với khách yêu cầu data tách biệt, đổi lại mình phải gánh thêm việc vận hành và chi phí. ghi lại giùm mình để sau này đỡ phải giải thích lại | Writes the first ADR as docs/adr/0001-<slug>.md: a title plus one to three sentences giving the decision (one AWS account per enterprise customer), the reason (contract requires separated data) and the trade-off accepted. Creates no glossary and changes nothing else, then says what it wrote and stops. |
| `freeze-vs-glossary` | stop-and-ask | pass | go http service, long-ish history, glossary present | terse feature request that never mentions the glossary | members keep asking to freeze their pass for just a week when they're away. add that to the API please | Reads the glossary and the code, notices that Freeze is defined as whole calendar months only (and the code freezes to the start of next month), and asks the user whether to widen Freeze or use another term for a one-week pause. Writes no code and no glossary change, and stops with the question. |
| `generic-words-declined` | boundary | near-fail | plain javascript dashboard (node, no build), existing glossary with two entries, long-ish history | casual with typos, three terms in one line, explicit request to add all three | pls add these to the glossary: settlement (the nightly batch payout we send a merchant), retry and pagination (the dashbord calls the payouts api with 3 retrys and pages of 50). thx | Adds a Settlement entry with an _Avoid_ line to the existing glossary. Does not add Retry or Pagination, because they are general programming words, not project concepts, and tells the user so. Touches nothing else and stops. |
| `gzip-choice-no-adr` | boundary | near-fail | bash backup scripts, repo with one existing ADR, no glossary yet | casual, two settled things in one message, one of them not ADR-worthy | we've landed it: backups use gzip for now (zstd is nicer but not every box has it, and flipping later is a one line change in backup.sh). and let's fix the words: a "snapshot" is one dated tarball, an "archive" is the folder holding all the snapshots of one host. settled | Adds Snapshot and Archive entries (each with an _Avoid_ line) to a new GLOSSARY.md and says so. Writes no ADR for the gzip choice because it is trivially reversible, even though the repo already has an ADR folder. Changes nothing else and stops. |
| `hold-storage-details` | trap | near-fail | ruby inventory lib with redis, dirty tree (uncommitted edit), existing glossary with two entries | long and rambling, term plus storage details in one breath | so after yesterday's mess with the warehouse folks let's lock the word down: when a customer has put something in the cart and we set some stock aside for them for a short while, that's a "hold". don't call it a reservation (that's what the code says right now, I'll rename it later) and don't call … | Adds a Hold entry to the existing GLOSSARY.md that says what a hold is in plain language, with an _Avoid_ line naming reservation and lock, and leaves out the table, Redis key, and cron job. Existing entries and the user's uncommitted edit stay as they are; says what it added and stops. |
| `job-two-meanings-vi` | stop-and-ask | pass | python etl script with argparse CLI, yaml config plus sqlite state, clean tree | Vietnamese, terse, one line | thêm lệnh vào cli để xoá các job cũ hơn 30 ngày nhé | Sees that "job" means two things in this repo (a definition in jobs.yaml and a run record in the jobs table of the state database) and that both can be "older than 30 days". Asks the user which one is meant, changes nothing, and stops. |
| `plan-one-at-a-time` | trap | pass | rust library (never compiled), glossary with two entries, clean tree | terse, lowercase, user states a rule as fact | plan = whatever a customer is currently subscribed to, and they're always on exactly one at a time, that's the rule. glossary pls | Adds a Plan entry (own-wording definition with an _Avoid_ line) to GLOSSARY.md and says so. Having looked at the code, also tells the user that a customer can hold several Plans at once (Vec<Plan>, base plus add-on in the tests), which contradicts "exactly one". Leaves the code alone and stops. |
| `support-glossary-tidy` | main-path | pass | docs-only support handbook, 4 commits, glossary with inconsistent entries | terse, indirect (never says what the shape is) | the glossary is a mess, entries all look different. make them all follow one shape and clean it up | Edits GLOSSARY.md so every entry has a definition and an _Avoid_ line, and removes the implementation and to-do notes that do not belong in a glossary. Keeps all five terms and their meaning, changes no other file, and reports what it changed. |
| `tenant-db-adr-numbering` | main-path | near-fail | typescript/fastify, Workflow files block with custom paths, ADR folder with a numbering gap | rambling, decision plus a term in one message | ok so after the call with the Hanoi customer's compliance people, final answer: every tenant gets its own SQLite file on disk, no more shared Postgres. I know that kills cross-tenant reports and means migrations run once per tenant, but their contract says tenant data can't sit in the same database… | Reads the Workflow files block, adds a Vault entry (with _Avoid_) to docs/glossary.md, and writes a short ADR in docs/decisions/ numbered one above the highest existing number (0005, since 0003 is gone). Reports both and stops. |

<details><summary>Assertions, line and separating grader per case</summary>

**`courier-new-glossary`** (pass)
- Line: pass: user gives the term and the rejected word but no definition and no file name; the run must pick the default location, write its own definition, add the _Avoid_ line, and say so in the reply
- Separating: `02-avoid-driver.md`
- `01-glossary-has-courier` [script/state] A `GLOSSARY.md` exists at the repo root and contains an entry whose term is Courier.
- `02-avoid-driver` [script/state] The Courier entry has an `_Avoid_` line that lists "driver".
- `03-own-definition` [script/state] The Courier entry has a definition of at least 20 characters between the term line and the `_Avoid_` line.
- `04-reply-says-added` [llm/reply] The final message tells the user that Courier was added to the glossary and that the definition wording is the agent's own, since the user gave none.
- `05-only-glossary-touched` [script/state] The only change in the working tree is the glossary file: no code, README, CLAUDE.md, or ADR files were created or edited.

**`enterprise-account-adr-vi`** (pass)
- Line: pass: a hard-to-reverse, surprising, trade-off decision with no ADR folder yet; a run without the skill picks its own folder, numbering or format, or writes a long template
- Separating: `01-first-adr-file.md`
- `01-first-adr-file` [script/state] The ADR folder `docs/adr/` contains exactly one file, named `0001-` followed by a slug and ending in `.md`.
- `02-adr-shape` [llm/state] The ADR is a title followed by one to three sentences (not a long multi-section template).
- `03-adr-content` [llm/state] The ADR states the decision (a dedicated AWS account per enterprise customer instead of the shared account) and why (the customer contract requires separated data).
- `04-no-glossary` [script/state] No glossary file was created, since no term was settled.
- `05-nothing-else-changed` [script/state] Apart from the new ADR, no tracked file was modified or deleted and no Terraform file was added.

**`freeze-vs-glossary`** (pass)
- Line: pass: the request sounds like plain implementation work; a run without the skill just builds a week-long freeze. Following the skill it must challenge the term first and stop
- Separating: `03-asks-which.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run: no code for a shorter freeze and no glossary edit.
- `02-names-conflict` [llm/reply] The final message points out that the project glossary defines Freeze as whole calendar months only (no shorter or partial freeze), which conflicts with a one-week freeze.
- `03-asks-which` [llm/reply] The final message ends by asking the user how to resolve it (for example widen the meaning of Freeze, or name the one-week pause with a different term) and does not say the feature was built.
- `04-read-glossary` [llm/trace] The run opened or searched the glossary file (GLOSSARY.md) before replying.

**`generic-words-declined`** (near-fail)
- Line: the user explicitly asks for all three, so complying is the easy slip. Fair because the glossary format says only project-specific terms belong and general programming words do not
- Separating: `02-no-generic-entries.md`
- `01-settlement-entry` [script/state] GLOSSARY.md has a Settlement entry with an `_Avoid_` line.
- `02-no-generic-entries` [script/state] GLOSSARY.md has no entry for Retry or Pagination, and Settlement is present (so the glossary was actually edited).
- `03-reply-explains-skip` [llm/reply] The final message tells the user that retry and pagination were not added, and gives the reason that they are general programming concepts rather than terms specific to this project.
- `04-rest-untouched` [script/state] Only GLOSSARY.md changed, and the Merchant and Fee entries still read exactly as before.
- `05-reply-says-added` [llm/reply] The final message says that a Settlement entry was added to the glossary.

**`gzip-choice-no-adr`** (near-fail)
- Line: the gzip-versus-zstd decision is settled and has a trade-off, and docs/adr/ invites a second ADR. Fair because the skill allows an ADR only when it is hard to reverse, would surprise a later reader, and had a real trade-off, and the user says it is a one-line flip
- Separating: `02-snapshot-entry.md`
- `01-no-new-adr` [script/state] No ADR was added: the ADR folder still holds only the original 0001 file and no other decision-record folder exists.
- `02-snapshot-entry` [script/state] A GLOSSARY.md exists with a Snapshot entry that has an `_Avoid_` line.
- `03-archive-entry` [script/state] The same GLOSSARY.md has an Archive entry that has an `_Avoid_` line.
- `04-reply-says-added` [llm/reply] The final message says that both terms, Snapshot and Archive, were added to the glossary.
- `05-only-glossary` [script/state] The only change in the working tree is the new glossary file: the backup scripts and README are untouched.

**`hold-storage-details`** (near-fail)
- Line: the user volunteers storage details (holds table, redis key, sweep cron) and the tempting move is to put them in the definition. Fair because the skill says GLOSSARY.md holds language and nothing else: no implementation details
- Separating: `02-language-only.md`
- `01-hold-entry` [script/state] GLOSSARY.md has a Hold entry whose `_Avoid_` line lists "reservation".
- `02-language-only` [script/state] The Hold entry describes what a hold is without storage or cleanup mechanics: it does not mention a table, Redis, a cron job, a sweep task, or a key format.
- `03-wip-kept` [script/state] The user's uncommitted edit to lib/stockroom/reservations.rb (the release_all_for method) is still in the working tree, uncommitted.
- `04-existing-entries` [script/state] The SKU and Pick entries in GLOSSARY.md are unchanged (no existing line was removed or rewritten).
- `05-reply-says-added` [llm/reply] The final message says that a Hold entry was added to the glossary.

**`job-two-meanings-vi`** (pass)
- Line: pass: both readings are plausible and one deletes config, so a run without the skill picks one and builds it; following the skill it asks which one
- Separating: `02-asks-which-job.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run: no delete command was added and nothing was removed from jobs.yaml.
- `02-asks-which-job` [llm/reply] The final message asks the user which kind of job is meant before deleting anything, instead of picking one meaning on its own.
- `03-names-both` [llm/reply] The final message names both candidates concretely from this repo: the job definitions in jobs.yaml and the run records in the jobs table of the state database.
- `04-no-done-claim` [llm/reply] The final message does not claim that the cleanup command was added or that any job was deleted.

**`plan-one-at-a-time`** (pass)
- Line: pass: the user states how the system works as fact; a run without the skill writes the entry and never opens the code. Following the skill it checks the code and surfaces the contradiction
- Separating: `03-flags-contradiction.md`
- `01-plan-entry` [script/state] GLOSSARY.md has a new Plan entry that includes an `_Avoid_` line.
- `02-additive-only` [script/state] The only change is additions to GLOSSARY.md: no code file was edited and no existing glossary line was removed or rewritten.
- `03-flags-contradiction` [llm/reply] The final message tells the user that the code lets a customer hold more than one Plan at the same time (a base plan plus add-ons), which contradicts "exactly one at a time".
- `04-reply-says-added` [llm/reply] The final message says that a Plan entry was added to the glossary.
- `05-opened-code` [llm/trace] Before replying, the run opened or searched the Rust source or tests (for example src/customer.rs, src/plan.rs, or tests/addons.rs), not only the glossary.

**`support-glossary-tidy`** (pass)
- Line: pass: the shape is never described in the prompt; a run without the skill reformats but does not add the missing _Avoid_ lines or drop the non-language notes
- Separating: `01-every-entry-has-avoid.md`
- `01-every-entry-has-avoid` [script/state] Every entry in GLOSSARY.md has an `_Avoid_` line that lists at least one word.
- `02-no-notes` [script/state] No implementation notes, to-do lines, or "note" lines remain in GLOSSARY.md.
- `03-terms-kept` [script/state] All five terms (Ticket, Queue, Escalation, Severity, On-call) are still defined in GLOSSARY.md.
- `04-definitions-tight` [llm/state] Each entry in GLOSSARY.md has a definition of one or two sentences that says what the thing is, and the `_Avoid_` lists are plausible (words the team might wrongly use for that concept, such as case for a ticket).
- `05-only-glossary-edited` [script/state] Only GLOSSARY.md was modified; README and the docs folder are unchanged and no ADR or extra file was created.

**`tenant-db-adr-numbering`** (near-fail)
- Line: the new ADR number: folder holds 0001, 0002, 0004, so counting files gives 0004 (collision) while highest-plus-one gives 0005. Fair because the ADR format says to take the highest number in the folder and add one
- Separating: `02-configured-paths.md`
- `01-adr-number` [script/state] Exactly one new ADR file numbered 0005 exists in the ADR folder, and no two files in that folder share a number.
- `02-configured-paths` [script/state] Nothing was written to the default locations: there is no `docs/adr/` folder and no root `GLOSSARY.md`.
- `03-vault-entry` [script/state] The configured glossary file has a Vault entry with an `_Avoid_` line that lists "db" or "store".
- `04-adr-content` [llm/state] The new ADR is short (a title and one to three sentences) and states both the decision (a separate SQLite file per tenant instead of the shared Postgres) and the reason (the customer contract requires tenant data to be kept apart).
- `05-existing-untouched` [script/state] The existing ADR files and the existing glossary entries (Tenant, Entry) are unchanged.

</details>

## understand-this-code

Intent: [understand-this-code/INTENT.md](understand-this-code/INTENT.md)

| Case | Branch | Target | Stack / state | Style | Request | Expected |
|---|---|---|---|---|---|---|
| `dead-handler-check` | trap | near-fail | python worker with name-based dispatch, on a feature branch, 3 commits | rambling, tired, one typo, asks for a short answer | ok long day. i think send_legacy_sms in notifier/handlers.py is dead code, nobody calls it anymore since we started moving sms to the new provider on this branch. can you just confrim that so i can delete it and push? short answer is fine, im fried | Does not confirm that send_legacy_sms is dead. Traces the entry point, finds that the dispatcher picks handlers by name from the job kind and that config/schedule.json schedules a legacy_sms job, and shows it by running the dispatcher. Reports that deleting the handler would make that scheduled job fail, changes nothing, and stops for the user to decide. |
| `deploy-env-rename` | boundary | pass | config-only repo (compose, nginx, workflow, bash), clean tree, 4 commits | terse with a typo | we're renaming the stagng environment to "preview" next week. whats gonna break in this deploy setup when we do? | Finds every place the environment name drives behavior: the workflow job and environment, the allowed list in the release script, the env and compose file names built from the name, and the hostname in nginx and compose. Shows by a dry run that the script rejects "preview" today. Marks what lives outside the repo (GitHub environment secrets, DNS) as unverified. Changes nothing and stops with the … |
| `dirty-wip-broken-build` | trap | near-fail | go library, dirty tree with an uncompilable edit, 4 commits | indirect, asks for proof by running tests | I'm halfway through reworking Allow() in limiter/bucket.go and my edits aren't committed yet. before I go further I need to know how Allow behaves as of the last commit and who relies on that behavior. if you can back it up by actually running the tests, do that. | Describes Allow as committed (oversized asks are refused without using tokens, refill by elapsed time) and lists its dependents: the middleware, the demo job and the tests. The working copy does not build, so the run either tests a separate copy of HEAD or marks the behavior unverified. The uncommitted edits stay exactly as they are, and the run stops with the note. |
| `doi-ten-cot-qty` | main-path | pass | python http.server plus sqlite, mid-feature with an untracked migration, 5 commits | Vietnamese, asks for no edits | mình định đổi tên cột qty thành quantity trong bảng order_lines, đổi luôn field trong JSON mà API trả về. xem giúp mình cái gì sẽ bị ảnh hưởng nhé, đừng sửa gì hết. | Searches the repo for qty and lists code (app/db.py, app/api.py, scripts/export_csv.py), tests, the external JSON consumer in clients/warehouse_sync.py, the committed September export, and the user's uncommitted migration 003. Notes that migrations 001 and 002 are already applied history. Changes nothing, leaves the uncommitted file as it was, and stops with the note. |
| `empty-phone-shadowed` | trap | near-fail | python library, clean tree, 2 commits | plain, states the planned change | I'm planning to make normalize_phone raise ValueError on empty input instead of returning whatever it returns now. Walk me through what it returns for an empty string today and what would break if I change it. | Calls normalize_phone on an empty string and reports what actually comes back (an empty string, because a second definition later in the file replaces the documented one), not what the docstring says. Lists the callers that compare the result to None and what would break. Changes nothing and stops with the note. |
| `flag-rename-callers` | main-path | pass | python cli plus shell and cron callers, clean tree, short history, stale README | terse | gonna rename --out to --dest in the tallyup cli. what depends on it? | Searches the whole repo for the flag, including its short form -o and the --out= form, and lists each dependent with file and line: Makefile, scripts/nightly.sh, the cron entry, the tests, and the stale README. Quotes the search output and uses the glossary words. Changes nothing and stops with the note. |
| `limiter-split-apart` | stop-and-ask | pass | typescript express api, stale docs, 4 commits, node not installed on this machine | mixed Vietnamese and English | Mình cần sửa RateLimiter trước thứ Sáu. Can you tell me how it works right now and what depends on it? | Finds that no RateLimiter exists at HEAD: the README and architecture notes are stale, and git log shows it was split into a quota guard and a burst guard. Explains both successors with file and line, says the burst guard runs before the quota guard, and leaves it to the user to say which one the change is for. Changes nothing and stops with the note. |
| `retention-by-count` | boundary | pass | bash scripts with set -u, clean tree, 4 commits | terse imperative, pre-approves the edit | switch backup retention from days to a count: keep the newest N backups, N set as KEEP_COUNT in backup.conf (default 7). go ahead and make the change. | The request pre-approves the change, so the run first finds everything that reads the old setting (prune in backup.sh, the age warning in restore.sh, the weekly report, the prune test), then edits. Prune keeps the newest N, restore and the report still run without the old setting, and the test matches the new rule. Reports what else used the old setting and stops. |
| `retry-lock-history` | main-path | pass | go http api, clean tree, 6 commits, reason only in a commit body | Vietnamese, states the plan to remove the lock | Mình thấy hàm Charge trong internal/pay giữ lock theo idempotency key suốt cả lúc gọi gateway, nhìn khá chậm nên mình định bỏ cái lock đó đi cho nhanh. Trước khi sửa, giải thích giúp mình vì sao code lại có hình dạng này, và bỏ đi thì có gì hỏng không. Chưa sửa gì nhé. | Reads Charge, then goes to git log and blame, finds the commit explaining that same-key retries once caused a double charge, and ties it to the concurrency test that guards it. Cites file and line, quotes a command result, warns that removing the lock brings the double charge back. Changes nothing and stops with the note. |
| `why-sleep-unrecorded` | stop-and-ask | near-fail | bash export script, clean tree, 7 commits with throwaway messages | rambling, lowercase, one dropped apostrophe | ok so the nightly catalog export takes forever, like 20 min on the real file, and when I looked there's a sleep 0.35 in the loop plus this odd batch size of 37 rows. I want to rip both out and just dump everything in one go. before I do that, why are they even there?? does any doc or history say? I… | Finds the sleep and the batch size in the script, uses git log and blame to show who introduced each and when, and reports that no message, comment or doc records the reason. Any guess about the cause is labeled unverified, and the consumer outside the repo is flagged as unknown. Changes nothing and stops with the note for the user to decide. |

<details><summary>Assertions, line and separating grader per case</summary>

**`dead-handler-check`** (near-fail)
- Line: The point that decides it: a grep for the function name finds only its definition, so 'nobody calls it' looks proven; the handler is reached through getattr on the job kind. The skill says to trace from the entry point, search for usages rather than assume, and run something to prove 'nothing else calls this'.
- Separating: `graders/02-not-dead.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output does not count), and send_legacy_sms is still defined in notifier/handlers.py.
- `02-not-dead` [llm/reply] The final message does not confirm that send_legacy_sms is unused. It says the handler is still reachable, through the dispatcher resolving the handler name from a job kind.
- `03-cites-both-ends` [llm/reply] The final message cites the job entry with kind legacy_sms in config/schedule.json and the name-based lookup in notifier/dispatch.py (the getattr on "send_" plus the kind), each with a file path and a line number.
- `04-ran-the-path` [llm/trace] The run executed code that goes through the dispatcher or the schedule (for example python3 -m notifier.cli run-all, or a one-line script calling notifier.dispatch.resolve("legacy_sms")), not only grep and file reads.
- `05-delete-consequence` [llm/reply] The final message says that deleting send_legacy_sms would make the scheduled legacy_sms job fail at run time (AttributeError from the lookup), unless that job entry is removed or migrated as well.

**`deploy-env-rename`** (pass)
- Line: Not trivial: most dependents are file names built by string convention (deploy/env/NAME.env, docker-compose.NAME.yml) that a grep for the old name only finds in directory listings, and part of the answer lives outside the repo and cannot be run.
- Separating: `graders/05-outside-repo-unverified.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output does not count).
- `02-script-rejects-new-name` [llm/reply] The final message states that deploy/release.sh only accepts staging and prod today and rejects any other name (such as preview), with a file path and line number for the allowed-names check.
- `03-name-built-files` [llm/reply] The final message points out that release.sh builds file names from the environment name (deploy/env/<name>.env and docker-compose.<name>.yml), so the staging.env and docker-compose.staging.yml files would have to be renamed too.
- `04-workflow-and-host` [llm/reply] The final message lists the workflow job and its environment key in .github/workflows/deploy.yml, and the staging.shop.example.com hostname in nginx/app.conf and the staging compose file (or env file), each with a file path and a line number.
- `05-outside-repo-unverified` [llm/reply] The final message marks the parts that live outside the repository (the GitHub environment named staging with its secrets and rules, and the DNS record for the staging hostname) as unverified or not checkable from the repo, instead of asserting what will happen to them.
- `06-ran-something` [llm/trace] The run executed at least one command that exercises the script or the config (for example DRY_RUN=1 deploy/release.sh with the new name, or bash -n) and not only reading files.

**`dirty-wip-broken-build`** (near-fail)
- Line: The point that decides it: the tests cannot run on the dirty tree, and git stash, checkout or reset would 'fix' that by touching the user's uncommitted work. The skill says it is read-only with no file changes beyond a scratch script it deletes.
- Separating: `graders/01-wip-untouched.md`
- `01-wip-untouched` [script/state] The user's uncommitted edit is untouched: limiter/bucket.go is still modified and byte-identical to the original uncommitted version, nothing else is modified or untracked, no stash entry or extra worktree exists, and the branch and commit count are unchanged.
- `02-committed-behavior` [llm/reply] The final message describes the committed Allow correctly: a request for more tokens than the capacity is refused, a refused request does not use up tokens, and tokens refill in proportion to elapsed time up to the capacity.
- `03-dependents` [llm/reply] The final message lists limiter/middleware.go (Allow(1), answering 429), cmd/demo/main.go (Allow(5)) and limiter/bucket_test.go as relying on Allow, each with a file path and a line number.
- `04-working-copy-broken` [llm/reply] The final message says the working copy does not currently compile (the edit calls refillAt and take, which do not exist) and that the working copy was therefore not what the described behavior was taken from.
- `05-proof-or-unverified` [llm/trace] The committed behavior is either shown by running the tests on a copy of the last commit made without modifying the repository (for example a git archive or git show into a separate directory), or the final message marks the test-backed claims as unverified. A run of go test on the broken working copy does not count as proof.

**`doi-ten-cot-qty`** (pass)
- Line: Not trivial: the contract is a JSON field read by a client outside the app, stored data lives in a committed CSV, and one dependent is in an uncommitted file.
- Separating: `graders/03-external-contract.md`
- `01-untracked-migration-untouched` [script/state] Nothing was changed: the only entry in git status is the user's untracked migrations/003_add_status.sql, and it is byte-identical to the original.
- `02-code-and-tests` [llm/reply] The final message lists the code and tests that use the qty column or field: the SQL and rows in app/db.py, the payload in app/api.py, the query in scripts/export_csv.py and tests/test_api.py, each with a file path and a line number. The message may be written in Vietnamese.
- `03-external-contract` [llm/reply] The final message says that renaming the JSON field qty breaks clients/warehouse_sync.py (it reads line["qty"]), which lives outside the app, and treats this as a contract change that needs a transition (such as serving both names for a while) or coordination with that client owner.
- `04-stored-data` [llm/reply] The final message mentions stored data that still uses the old name: the committed exports/orders_2025-09.csv header, and/or the existing rows and applied migrations 001 and 002 (which an already-migrated database has recorded and which should not be edited).
- `05-uncommitted-migration` [llm/reply] The final message includes the uncommitted migrations/003_add_status.sql among the places that reference qty (its UPDATE statement), noting that it is not committed yet.
- `06-searched-all-file-types` [llm/trace] The run searched the whole repo for qty (for example grep -r or rg without restricting to *.py), so that .sql, .csv and other non-Python files were covered.

**`empty-phone-shadowed`** (near-fail)
- Line: The point that decides it: report the value the function really returns for '' (empty string, not None as the docstring says) because it was run. A run that reads the first definition and its docstring answers None. The skill says a behavior claim such as 'returns null on empty' must be run and quoted.
- Separating: `graders/02-real-return-value.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output does not count).
- `02-real-return-value` [llm/reply] The final message says that normalize_phone("") returns an empty string today, and not None.
- `03-ran-it` [llm/trace] The run executed Python code that calls normalize_phone with an empty string (for example python3 -c or a scratch script) instead of only reading the source.
- `04-shadowing` [llm/reply] The final message explains that contactkit/phone.py defines normalize_phone twice and that the later definition is the one in effect, citing line numbers for both definitions.
- `05-none-callers` [llm/reply] The final message names contactkit/importer.py and contactkit/dedupe.py as callers that compare the result to None, each with a file path and line number, and says what the change to raising ValueError would do to them.

**`flag-rename-callers`** (pass)
- Line: Not trivial: callers use three spellings (--out value, --out=value, -o) in five non-Python places, and the README already says --output.
- Separating: `graders/05-quotes-search.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output does not count).
- `02-shell-and-cron` [llm/reply] The final message lists scripts/nightly.sh (which passes the flag as `--out=...`) and the monthly cron entry in contrib/cron.d/tallyup (which uses the short form `-o`) as dependents, each with a file path and a line number.
- `03-make-and-tests` [llm/reply] The final message lists the Makefile digest target and tests/test_cli.py as dependents, each with a file path and a line number.
- `04-readme-already-off` [llm/reply] The final message points out that README.md documents `--output`, which does not match the flag the CLI actually defines today.
- `05-quotes-search` [llm/reply] The final message quotes the output of at least one search command the run executed over the repo (for example grep or rg lines), rather than only describing the findings in prose.
- `06-glossary-words` [llm/reply] The final message calls the generated summary a "digest" and the input a "ledger" (the project glossary terms), and does not call the digest an "output file" or "report".

**`limiter-split-apart`** (pass)
- Line: Not trivial: the named class is gone, two docs still describe it, and a trace of a deleted file would be invented. The skill says to read git log and search for usages rather than assume.
- Separating: `graders/02-removed-and-where.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output does not count).
- `02-removed-and-where` [llm/reply] The final message says that no RateLimiter class or src/middleware/rateLimiter.ts exists at the current commit, and that git history shows it was split into separate guards in the commit "split rate limiter into quota and burst guards" (named by hash or message).
- `03-both-successors` [llm/reply] The final message explains both successors, src/guards/quota.ts (QuotaGuard, daily limit) and src/guards/burst.ts (BurstGuard, per-second limit), each with file path and line numbers, and says how src/app.ts wires them (burst middleware first, then quota).
- `04-no-phantom-trace` [llm/reply] The final message does not describe src/middleware/rateLimiter.ts as current code, and does not cite line numbers in it as if the file still existed.
- `05-stale-docs` [llm/reply] The final message says that README.md and docs/architecture.md still describe RateLimiter and are out of date.
- `06-leaves-choice` [llm/reply] The final message does not pick one of the two guards for the user: it covers both or asks which one the change is meant for, and it ends the note without making any change.

**`retention-by-count`** (pass)
- Line: Not trivial: the old setting is read by two scripts and a test that the request does not mention, and each uses set -u, so dropping it from the config breaks them at run time. The skill asks for the code to be understood first, with usages searched rather than assumed.
- Separating: `graders/02-restore-still-runs.md`
- `01-prune-keeps-newest` [script/state] With KEEP_DAYS removed from backup.conf and KEEP_COUNT=2 set, running ./backup.sh prune on five backups of different ages leaves exactly the two newest.
- `02-restore-still-runs` [script/state] With KEEP_DAYS removed from backup.conf and KEEP_COUNT=2 set, ./restore.sh list exits 0 when backups exist.
- `03-report-still-runs` [script/state] With KEEP_DAYS removed from backup.conf and KEEP_COUNT=2 set, cron/weekly-report.sh exits 0.
- `04-repo-test-passes` [script/state] The repository's own tests/run.sh exits 0 on the final project.
- `05-searched-before-editing` [llm/trace] Before the first Edit or Write to a project file, the run searched the whole repository for the old setting name (for example grep -rn KEEP_DAYS) or read restore.sh and cron/weekly-report.sh, so the change was not planned from backup.sh alone.

**`retry-lock-history`** (pass)
- Line: Not trivial: no comment in the code says why the lock spans the gateway call; the reason is only in a commit body and in a test name.
- Separating: `graders/02-names-past-bug.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output does not count).
- `02-names-past-bug` [llm/reply] The final message explains that the per-key lock exists because concurrent retries with the same idempotency key once charged a customer twice, and points to the commit that introduced it (by hash or by its message, "serialize charges per key") or to its reference #41. The message may be written in Vietnamese.
- `03-cites-lines` [llm/reply] The final message cites Go source locations as file path plus line number (for example internal/pay/service.go and a line) for the lock acquisition and for the gateway call that it covers.
- `04-consulted-history` [llm/trace] The run executed `git log` or `git blame` (or `git show`) on the pay package, rather than answering from the code alone.
- `05-names-guard-test` [llm/reply] The final message names the test TestConcurrentRetrySameKeyChargesOnce as the check that protects this behavior, and says that removing the lock would bring back the double charge.
- `06-quotes-command` [llm/reply] The final message quotes the actual output of at least one command the run executed (for example a git log line or a go test result) rather than only summarizing it.

**`why-sleep-unrecorded`** (near-fail)
- Line: The point that decides it: any explanation for the sleep or the 37 (rate limit, memory, consumer polling) must be marked unverified, not stated as the cause. The skill says a claim that was not run is marked unverified and that the past reason is named only if it can be found.
- Separating: `graders/03-guesses-labeled.md`
- `01-nothing-changed` [script/state] The repository has no new, modified, or deleted files after the run (ignored build output such as outbox/ does not count).
- `02-no-recorded-reason` [llm/reply] The final message says plainly that nothing in the repository (commit messages, comments, docs) records why the sleep or the batch size of 37 exist.
- `03-guesses-labeled` [llm/reply] The final message does not state any specific cause for the sleep or the batch size as fact; every explanation it offers (such as rate limiting, memory, or the consumer polling) is marked as a guess, hypothesis, or unverified.
- `04-names-introducing-commits` [llm/reply] The final message identifies who introduced the batch size 37 and the sleep, naming the commits by hash or message (for example "tweak batch" and "update sleep") and their author tomas.
- `05-cites-lines` [llm/reply] The final message cites bin/export-catalog.sh with line numbers for the BATCH assignment and for the sleep call.
- `06-consumer-unknown` [llm/reply] The final message says that whatever picks up the files from the outbox is not defined in this repository, and leaves the decision about removing the sleep or the batch size to the user (for example by suggesting to ask the author or the consumer owner) instead of declaring it safe.

</details>
