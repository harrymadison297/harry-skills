# Plan skills on claude-sonnet-5-5: with the skill vs. without

Effort `high`, 128 good runs of 128. Medians over 2 rep(s) of every case; `Δ` is `with` against `none`. Raw numbers: `evals/bench-plan-results.json`.

## Findings (read first)

**Concrete example.** `slicing-tickets/settle-up-cut`, same request, same model:

| | wall s | turns | output tok | cost $ | bytes written |
|---|---|---|---|---|---|
| none (2 runs) | 40, 43 | 4, 7 | 5.4k, 5.7k | 0.12, 0.13 | 8.7k, 7.1k |
| with (2 runs) | 176, 106 | 22, 8 | 23.9k, 14.8k | 0.42, 0.28 | 17.0k, 15.3k |

With the skill, Sonnet 5.5 ran the graph script, cross-checked scenarios and wrote longer tickets. The opposite example is `prototyping-designs/limiter-vague-vi`: without the skill it built a 15 KB simulator over 260 s ($0.35); with the skill it stopped after 16 s ($0.05) and asked which of three open questions to settle.

**Does the skill make it cost much more?** On average, moderately; per skill, it depends on whether the skill makes the model do more work or stop earlier.

| Group | Skills | Cost with vs none | Why |
|---|---|---|---|
| Much more | `slicing-tickets` (+112%), `designing-architecture` (+63%), `understand-this-code` (+43%) | +40% to +112% | More turns: it runs scripts, type-checks sketches, runs test suites, and writes longer documents |
| Slightly more | `ask-until-clear` (+28%), `research` (+15%), `spec-it` (+10%) | +10% to +28% | Longer, more structured replies |
| Cheaper | `prototyping-designs` (-37%), `term-guard` (-8%) | -8% to -37% | The skill stops and hands back instead of building |
| **All 8** | | **+27%** ($8.41 → $10.66), **+31%** output tokens, **+15%** wall, **+41%** input tokens (all calls) | |

The skill text itself is not the cost: it adds 0.8k to 1.4k tokens to the first call (about 1% to 2% of a 60k to 250k run), and merely installing the plan plugin adds 190 tokens. The cost comes from the extra turns and the longer output the skill triggers. Time to first token did not change (1.2 s to 1.8 s in every skill). [Deduce: the extra turns come from the skill's verify steps, because the "with" replies cite more executed checks]

**How the response differs** (Opus compared each pair, order shuffled; one comparison per case, so treat the labels as a hypothesis):

| | none | with |
|---|---|---|
| Posture | Commits to a stated assumption and ships | Stops, asks, or defers more (`held back` lists, `not ready to approve`, hands back to a gate) |
| Reply | Prose and lists, decisive, names the concrete trap | Longer, templated, process vocabulary (gates, skill names, `Check:` lines) |
| Evidence | Reads code more than it runs it | Runs more: probes, test suites, graph scripts, sketch type-checks |
| Preferred for the user | `term-guard`, `spec-it`, `designing-architecture` (3 of 4), `prototyping-designs` | `ask-until-clear` (premise checks), `understand-this-code`, `research`, `slicing-tickets` |

**Does it help?** Weighted assertion pass rate: none 70.7% → with 87.1%. Read this with care: Opus wrote the assertions from the skill text, so they reward the behaviors the skill imposes. It shows the skill changes the model's behavior in the intended direction, not that the output is better in every case. The skills gain most where the skill's stop-and-ask is the point (`prototyping-designs/limiter-vague-vi` 1.0 → 5.0 of 5, `spec-it/pomo-weekly-gaps` 1.0 → 5.0 of 6, `term-guard/credit-two-meanings-vi` 1.5 → 5.0 of 5).

**Failures that happen only with the skill, by cause:**

| Failure | Runs | Cause | Note |
|---|---|---|---|
| `prototyping-designs` changed `spec.md` / an ADR (`reopen-net-zero`, `levels-btree-proposed`) | 3 | Eval | Step 6 of the skill says to record the decision in `Decisions`; the script grader forbids any tracked change. The grader should allow the decision file |
| `spec-it` listed open questions on an interview that said "none left" (`invoice-csv-import`, `parcel-webhook-retries`) | 4 | Skill or eval, needs a human look | The skill found real gaps the notes never settled; the eval assumed none. Either the skill over-asks or the fixture hid gaps |
| `ask-until-clear/client-retry-check` interviewed instead of answering from the code | 2 | Skill | The boundary case: the code already answers the question, yet it asked 5 questions |
| `term-guard/loan-rule-vs-code` did nothing, not even the unambiguous `Desk::overdue` | 2 | Skill or model | It stopped on the contradicting definition; the half of the task that was clear was not done |
| `term-guard/tracking-id-ulid-adr` wrong ADR number | 1 | Model | |
| three `understand-this-code` llm checks (one is a clipped-transcript grader limit) | 3 | Model or grader noise | Single-rep, not repeated |

**Caveats.**
- 4 cases × 2 reps per skill, so each cell is 8 runs. Medians are shown, sums in the totals table. Only 2 reps cannot separate small gaps (under about 20%).
- Wall time ran 4 runs in parallel on a shared network. A single run can be off by a lot: the `none` runs of `prototyping-designs` spent 100 to 220 s waiting on tools they started themselves.
- The skill was called by explicit slash command. Whether `ask-until-clear` and `term-guard` trigger on their own was not tested. Only the 8 plan skills were installed, so hand-backs to `handon` pointed at nothing.
- Sonnet 5.5 at effort `high`, tools limited to the case's list plus `Skill`, no network, no subagents. Other effort levels will change time and tokens.
- Graders are one model family (Opus), llm graders saw a clipped transcript. The fixtures and assertions were written by Opus reading the skills.
- `python3 -m pytest` does not work on this machine (plain `pytest` does), which may cost some runs an extra turn in both configurations.
- Before the runs I relaxed one grader after reading the skill: `prototyping-designs/reopen-net-zero` 02 no longer requires reporting the prototype's output (step 5 hands the prototype to the user). Every other case is as Opus wrote it, including the grader faults listed above, which were left in so the numbers match what was run.

## Headline: does the skill cost more, and does it help

| Skill | cases×reps | pass none → with | wall s none → with (Δ) | TTFT s | turns | output tok (Δ) | input tok, all calls (Δ) | cost $ none → with (Δ) |
|---|---|---|---|---|---|---|---|---|
| `ask-until-clear` | 8/8 | 76% → 92% | 21 → 24 (+14%) | 1.5 → 1.2 | 5 → 5 | 2,022 → 2,552 (+26%) | 37,938 → 44,000 (+16%) | 0.065 → 0.078 (+20%) |
| `term-guard` | 8/8 | 77% → 82% | 32 → 21 (-34%) | 1.8 → 1.7 | 4 → 5 | 4,194 → 2,290 (-45%) | 60,319 → 49,456 (-18%) | 0.106 → 0.077 (-28%) |
| `understand-this-code` | 8/8 | 86% → 88% | 13 → 22 (+61%) | 1.7 → 1.8 | 5 → 6 | 1,240 → 2,384 (+92%) | 54,251 → 61,350 (+13%) | 0.057 → 0.082 (+44%) |
| `research` | 8/8 | 96% → 98% | 55 → 66 (+21%) | 1.4 → 1.3 | 10 → 12 | 6,009 → 7,613 (+27%) | 161,787 → 200,023 (+24%) | 0.150 → 0.181 (+21%) |
| `prototyping-designs` | 8/8 | 65% → 94% | 60 → 28 (-54%) | 1.4 → 1.4 | 8 → 6 | 5,641 → 3,139 (-44%) | 134,240 → 67,332 (-50%) | 0.144 → 0.085 (-41%) |
| `spec-it` | 8/8 | 34% → 66% | 49 → 75 (+51%) | 1.3 → 1.7 | 6 → 8 | 5,830 → 9,558 (+64%) | 66,899 → 77,732 (+16%) | 0.133 → 0.194 (+46%) |
| `designing-architecture` | 8/8 | 51% → 86% | 83 → 146 (+76%) | 1.2 → 1.4 | 8 → 12 | 10,200 → 18,724 (+84%) | 81,203 → 249,911 (+208%) | 0.201 → 0.344 (+71%) |
| `slicing-tickets` | 8/8 | 80% → 91% | 36 → 63 (+75%) | 1.5 → 1.6 | 4 → 6 | 4,171 → 8,479 (+103%) | 65,359 → 111,066 (+70%) | 0.106 → 0.178 (+68%) |
| **all** | 64/64 |  | 41 → 40 (-3%) | | 6 → 7 | 5,080 → 4,636 (-9%) | 66,899 → 77,732 (+16%) | 0.124 → 0.120 (-3%) |

**Totals over every run** (sums, not medians; the medians above hide the long runs):

| Skill | wall s none → with | output tok none → with | input tok none → with | cost $ none → with |
|---|---|---|---|---|
| `ask-until-clear` | 237 → 213 (-10%) | 15,504 → 23,048 (+49%) | 356,172 → 405,105 (+14%) | 0.50 → 0.64 (+28%) |
| `term-guard` | 247 → 236 (-4%) | 33,900 → 28,422 (-16%) | 580,222 → 541,751 (-7%) | 0.83 → 0.76 (-8%) |
| `understand-this-code` | 121 → 180 (+49%) | 12,614 → 20,834 (+65%) | 419,348 → 576,137 (+37%) | 0.47 → 0.67 (+43%) |
| `research` | 440 → 482 (+9%) | 48,320 → 56,188 (+16%) | 1,262,154 → 1,559,832 (+24%) | 1.19 → 1.36 (+15%) |
| `prototyping-designs` | 1,033 → 534 (-48%) | 68,930 → 34,997 (-49%) | 1,228,053 → 1,011,587 (-18%) | 1.43 → 0.91 (-37%) |
| `spec-it` | 536 → 585 (+9%) | 67,406 → 74,321 (+10%) | 637,535 → 688,409 (+8%) | 1.34 → 1.48 (+10%) |
| `designing-architecture` | 718 → 1,151 (+60%) | 87,541 → 143,663 (+64%) | 723,129 → 2,140,052 (+196%) | 1.64 → 2.68 (+63%) |
| `slicing-tickets` | 365 → 874 (+139%) | 44,478 → 116,075 (+161%) | 578,141 → 1,220,032 (+111%) | 1.02 → 2.16 (+112%) |
| **all** | 3,697 → 4,254 (+15%) | 378,693 → 497,548 (+31%) | 5,784,754 → 8,142,905 (+41%) | 8.41 → 10.66 (+27%) |

`input tok` sums every API call of the run (context is re-read each turn), cache reads included, so it grows with turns. `cost` is what the CLI billed at list price after cache discounts.

## Where the time and tokens go

| Skill | first-call context none → with | skill text added (tok) | API calls | peak context | tool calls | tool-wait s (wall − API) | time to first tool s |
|---|---|---|---|---|---|---|---|
| `ask-until-clear` | 11,011 → 12,392 | 1,380 | 3 → 3 | 15,237 → 17,156 | 4 → 4 | 1.8 → 1.7 | 3.0 → 3.1 |
| `term-guard` | 11,088 → 12,243 | 1,154 | 4 → 4 | 20,012 → 17,524 | 3 → 4 | 2.2 → 1.6 | 2.6 → 3.2 |
| `understand-this-code` | 11,074 → 11,866 | 792 | 4 → 4 | 15,774 → 18,671 | 4 → 5 | 1.6 → 1.9 | 2.5 → 2.8 |
| `research` | 11,160 → 12,013 | 852 | 9 → 10 | 24,692 → 27,404 | 10 → 10 | 3.8 → 2.7 | 3.3 → 3.5 |
| `prototyping-designs` | 11,078 → 11,976 | 897 | 7 → 4 | 23,702 → 17,844 | 8 → 6 | 16.2 → 1.6 | 3.0 → 3.0 |
| `spec-it` | 11,376 → 12,778 | 1,402 | 4 → 4 | 22,721 → 28,401 | 5 → 8 | 1.6 → 1.5 | 2.8 → 2.7 |
| `designing-architecture` | 11,362 → 12,442 | 1,080 | 5 → 9 | 28,004 → 39,301 | 6 → 12 | 1.4 → 3.0 | 3.0 → 3.4 |
| `slicing-tickets` | 11,429 → 12,860 | 1,430 | 4 → 6 | 21,722 → 27,096 | 3 → 5 | 1.5 → 1.5 | 3.0 → 3.3 |

Install overhead with no skill called (a `pong` prompt, 3 runs each): first-call context 8,632 → 8,822 tokens, so the plan plugin's skill list costs 190 tokens per session. `skill text added` above includes this.

## How it responds

| Skill | reply words | headings | bullets | table rows | question lines | files written | bytes written | narration chars between tools |
|---|---|---|---|---|---|---|---|---|
| `ask-until-clear` | 388 → 604 | 0 → 1 | 12 → 10 | 0 → 0 | 6 → 6 | 0 → 0 | 0 → 0 | 54 → 89 |
| `term-guard` | 265 → 334 | 0 → 0 | 6 → 7 | 0 → 0 | 0 → 1 | 4 → 1 | 9,725 → 1,183 | 14 → 86 |
| `understand-this-code` | 262 → 450 | 0 → 2 | 7 → 11 | 0 → 0 | 0 → 0 | 1 → 1 | 972 → 972 | 30 → 56 |
| `research` | 298 → 326 | 0 → 0 | 4 → 6 | 0 → 2 | 0 → 0 | 1 → 1 | 4,010 → 4,446 | 262 → 218 |
| `prototyping-designs` | 505 → 356 | 0 → 0 | 9 → 6 | 0 → 4 | 0 → 2 | 0 → 0 | 0 → 0 | 185 → 82 |
| `spec-it` | 325 → 371 | 0 → 0 | 8 → 10 | 0 → 0 | 0 → 6 | 2 → 1 | 9,875 → 8,716 | 64 → 0 |
| `designing-architecture` | 416 → 476 | 0 → 0 | 11 → 12 | 0 → 0 | 0 → 0 | 2 → 2 | 8,798 → 11,626 | 72 → 232 |
| `slicing-tickets` | 335 → 427 | 0 → 0 | 4 → 6 | 3 → 6 | 0 → 0 | 2 → 3 | 3,540 → 7,672 | 60 → 77 |

Each cell is `none → with`.

**`ask-until-clear`**
- 'With' turns follow-ups into numbered Q&A pairs, each with its own proposed answer and stated assumptions (often marked with emoji), where 'none' asks open questions or gives short suggestion lists.
- 'With' adds an explicit 'held back' or dependency section listing the decisions it is deferring until earlier answers arrive, which keeps it staged but also makes it decline or postpone the actual grilling.
- 'With' grounds its replies more in the code (file:line refs, named functions, structured 'what I understand' summaries) and sometimes questions the premise, e.g. the 500-link quota versus the claimed overload, or deploy-side fixes.
- 'With' is longer, more templated and more procedural, while 'none' is shorter, more conversational, and sometimes more concrete on implementation details and ambiguities.
- Verdict: The user is better served by 'with' when the task calls for premise-checking or disciplined staged clarification (rate-limit-links, and roughly a tie on recurring-tasks), but not on narrow factual checks or explicit 'grill me' requests, where its self-answered, heavily structured Q&A is overlong or defers what was asked (client-retry-check, fx-rates-cache).

**`term-guard`**
- 'With' tends to stop and ask clarifying questions or re-open settled definitions instead of implementing (credit and loan cases), while 'none' commits to a stated assumption and ships tested code.
- 'With' leans on existing project docs (glossary, ADRs) and terminology framing, while 'none' puts decisions and rationale directly into code comments and tests.
- When both implement, 'with' formats replies as bolded bullet status reports, whereas 'none' mixes prose with lists and explains test intent a bit more clearly.
- 'With' raises narrower caveats (naming overlap, guessable routes), whereas 'none' surfaces higher-stakes issues (PII exposure, ULID timestamp leak) and applies changes more thoroughly.
- Verdict: The user is better served by 'none' in all four cases, especially when no human is available to answer questions; 'with' is never clearly better here, and its edge (careful terminology and fitting changes to existing docs) would only matter if a user were present to resolve its questions.

**`understand-this-code`**
- 'With' verifies claims empirically far more often: it runs code against real sample data, runs tests, checks old commits, and diffs outputs. 'None' mostly reasons from reading code and diffs.
- 'With' gives longer, sectioned replies with headers, quoted snippets, commit hashes/authors and file:line references. 'None' is more compact and leads with the bottom line.
- 'With' is more explicit about scope and limits: what it didn't check, what's speculation, clean git status and deleted temp files, and caveats like orphaned code or downstream importers.
- 'With' adds more surrounding context (data flow, blast radius, edge cases, keep/avoid lists) and ends with targeted decision questions. 'None' ends with simpler options, an offer to act, or a recommendation to ask people.
- Verdict: The user is generally better served by 'with' when correctness hinges on evidence, such as hidden crashes or the reason behind behavior, but not when the user asked for brevity or the task is simple (the tired-user SMS case and the trivial rename), where its extra length is padding.

**`research`**
- 'With' leans harder on its own experiments, such as scratch-copy probes, controlled bisection and front-vs-back traces, where 'none' more often relies on reading code and docs.
- 'With' attaches more precise evidence: commit hashes, printed values, failure rates (0/40 vs 40/40), file:line cites and results tables.
- 'With' tends to lead with a blunt verdict and close with explicit caveats, items to confirm or a direct decision question; 'none' closes more briefly or ties the result back to the user's stated worry.
- 'With' is sometimes weaker on user-facing impact and scope: it missed the store-deletion consequence and the CI patch-version drift, and it made an extra Edit, while 'none' covered those and stayed strictly in scope.
- Verdict: The user is better served by 'with' on investigative questions where root cause or a design choice needs firm evidence (retry-front-or-back, seed-after-bump), but not on narrower checks where 'none' gave the same correct answer with clearer practical consequences and tighter scope (reminder-timeout-cap, tar-filter-swap).

**`prototyping-designs`**
- 'With' often holds back from the requested work: it stops to ask which question to prototype (limiter) or declines the mock-up because an ADR already decided the matter (schedule), where 'none' just builds it.
- 'With' measures less (one depth, no synthetic books, reasoning in place of a reproduced deadlock), though it sometimes adds a useful angle such as the end-to-end replay cost or a single spec-level root-cause fix.
- 'With' handles artifacts inconsistently: it edited an ADR in the repo unasked and deleted its prototype in one case, but left rerunnable scratch scripts in another; 'none' consistently keeps reproducible work isolated outside the repo.
- 'With' gives shorter, less hedged replies that often end by asking the user to choose, while 'none' gives longer, data-heavy reports with explicit caveats and a concrete recommendation.
- Verdict: The user is better served by 'none', which did the requested prototyping with reproducible, non-invasive evidence; the exception is the reopen-net-zero case, a tie where 'with' matched it and added a reusable script and a simpler fix.

**`spec-it`**
- 'With' reads and investigates the codebase more before writing (more Globs/Reads), while 'none' writes sooner with less exploration.
- 'With' leaves unresolved points as open questions (6–8, each with a recommendation) and declares the spec 'draft/not ready to approve'; 'none' settles them with stated defaults or assumptions and presents a spec ready for review or approval.
- 'With' keeps specs strictly behavioural in a journey/test-path/'Check:' format and defers design, glossary edits and tests to later process steps; 'none' adds concrete design (endpoints, status codes, data fields), edits the glossary and runs tests when it is relevant.
- 'With' ends by pointing to workflow skills (ask-until-clear, term-guard, gates) and its replies use process jargon; 'none' ends by asking the user to confirm the specific judgment calls it made, in plainer prose.
- Verdict: The user is better served by 'none' in most cases, because it delivers usable, approvable specs and answers the design questions asked, flagging its assumptions instead of blocking on process; the exception is the court-waitlist case, where 'with''s deeper reading and refusal to quietly assume answers to real gaps (such as the uncommitted cancel cutoff) made it the better choice.

**`designing-architecture`**
- 'With' verifies more before writing: it type-checks code sketches in scratch copies and runs the test suites (cargo, npm, go, pytest), while 'none' often skips tests on the grounds that only docs changed.
- 'With' splits the output into more artifacts (an architecture doc plus separate ADRs or RFCs, sometimes in folders it creates), while 'none' tends to write one self-contained design doc with change tables, test plans, and concrete details.
- 'With' frames results around process and readiness (seams, gate 2, skill routing, sending items back to spec-it, declaring a design blocked), while 'none' commits to concrete decisions and ends with targeted questions and an offer to proceed.
- 'None' more often names concrete specifics that matter for the next step: the exact bug line, silent price-change traps, work splits with fixed interfaces, exit codes, and spec gaps. 'With' sometimes reasons more abstractly or reinterprets a requirement, such as its stateless quota design that can lose alerts.
- Verdict: The user is generally better served by 'none', whose concrete and decisive designs fit their goals of acting today and splitting the work (it won 3 of 4 cases); 'with' was better only in partner-sync-rfc, where its sketch verification, test run, per-blocker RFCs and extra design question gave stronger planning input.

**`slicing-tickets`**
- 'with' leans on process: it cites gates, status lines, review/journey metadata and approval rules, and treats deviations such as early ticket cuts as needing explicit consent.
- 'with' investigates and verifies more. It runs graph-check scripts, cross-checks scenario arithmetic, and surfaces extra blockers like the missing graph.py.
- 'with' slices work into vertical, user-visible behaviors with detailed numbered e2e scenarios. 'none' tends to slice by layer, which allows more parallel work, and grounds itself more in code-level pitfalls.
- 'with' replies are longer, more formal and more structured with headed sections. They end with a single recommended path plus numbered asks, where 'none' tends to offer a menu of options or more compact summaries.
- Verdict: The user is generally better served by 'with', since its verified, concrete, gated plans are closer to ready to act on, but not under time pressure: there 'none's crisp option menu with an immediately actionable partial path, and its compact code-level findings, served the user as well or better.

## Quality: assertions

| Skill | Case | none passed | with passed | failed only under `none` | failed only under `with` |
|---|---|---|---|---|---|
| `ask-until-clear` | `client-retry-check` | 5.0/5 | 4.0/5 | - | 04-no-interview |
| `ask-until-clear` | `fx-rates-cache` | 3.5/6 | 6.0/6 | 02-premise-recommended-yes, 03-no-cache-design-now, 05-recommendations | - |
| `ask-until-clear` | `rate-limit-links` | 4.5/5 | 5.0/5 | 04-recommendations | - |
| `ask-until-clear` | `recurring-tasks` | 3.5/6 | 6.0/6 | 02-completion-question, 04-premise-first, 05-recommendations | - |
| `term-guard` | `credit-two-meanings-vi` | 1.5/5 | 5.0/5 | 01-nothing-changed, 02-asks-which-credit, 03-names-both, 04-no-done-claim | - |
| `term-guard` | `loan-rule-vs-code` | 4.0/4 | 2.0/4 | - | 01-overdue-works, 02-loan-entry |
| `term-guard` | `promo-rounding-no-adr` | 5.0/5 | 5.0/5 | - | - |
| `term-guard` | `tracking-id-ulid-adr` | 4.0/5 | 3.5/5 | - | 02-adr-numbered-0005 |
| `understand-this-code` | `empty-phone-shadowed` | 6.0/6 | 5.5/6 | - | 06-test-wrong-reason |
| `understand-this-code` | `legacy-sms-not-dead` | 4.0/5 | 4.5/5 | 04-ran-the-path | - |
| `understand-this-code` | `per-line-rounding-why` | 4.5/6 | 5.5/6 | 05-ran-the-numbers, 06-what-breaks | 03-no-invented-reason |
| `understand-this-code` | `rename-qty-field` | 4.0/5 | 4.0/5 | 04-reports-template | 05-ran-invoice |
| `research` | `reminder-timeout-cap` | 5.0/5 | 5.0/5 | - | - |
| `research` | `retry-front-or-back` | 4.0/5 | 4.5/5 | 03-asks-grounded-question | - |
| `research` | `seed-after-bump` | 6.0/6 | 6.0/6 | - | - |
| `research` | `tar-filter-swap` | 6.0/6 | 6.0/6 | - | - |
| `prototyping-designs` | `levels-btree-proposed` | 5.0/5 | 4.0/5 | - | 01-repo-untouched |
| `prototyping-designs` | `limiter-vague-vi` | 1.0/5 | 5.0/5 | 01-repo-untouched, 02-nothing-built, 04-asks-which, 05-no-pick | - |
| `prototyping-designs` | `reopen-net-zero` | 6.0/6 | 5.5/6 | - | 01-product-untouched |
| `prototyping-designs` | `schedule-shape-decided` | 2.5/5 | 5.0/5 | 01-repo-untouched, 02-no-mockups, 05-no-handover | - |
| `spec-it` | `court-waitlist-wording` | 3.0/6 | 3.5/6 | 05-paths-checks-criteria | 01-draft-no-open-questions |
| `spec-it` | `invoice-csv-import` | 3.0/6 | 5.0/6 | 02-check-lines, 03-criteria-name-paths, 06-checks-drive-real-api | 01-draft-no-open-questions |
| `spec-it` | `parcel-webhook-retries` | 2.0/6 | 2.5/6 | 01-draft-structure, 04-retry-criteria | 06-open-questions-empty |
| `spec-it` | `pomo-weekly-gaps` | 1.0/6 | 5.0/6 | 01-draft-for-settled-part, 02-gaps-are-open-questions, 03-no-criterion-settles-gaps, 04-recommended-answers, 05-not-approvable-yet | - |
| `designing-architecture` | `invoice-vat-no-seam` | 4.0/5 | 5.0/5 | 05-not-ready-for-gate | - |
| `designing-architecture` | `partner-sync-rfc` | 1.0/6 | 5.0/6 | 01-draft-with-ac-table, 02-rfc-file-exists, 03-rfc-content, 05-ts-sketch-parses | - |
| `designing-architecture` | `quota-cli-go` | 5.5/6 | 6.0/6 | 04-designs-compared | - |
| `designing-architecture` | `shipping-refactor-vi` | 1.0/6 | 4.0/6 | 01-draft-with-ac-table, 02-python-sketch-compiles, 03-designs-compared | - |
| `slicing-tickets` | `link-expiry-draft-arch` | 5.0/5 | 5.0/5 | - | - |
| `slicing-tickets` | `promo-recut-not-fixed` | 5.0/5 | 5.0/5 | - | - |
| `slicing-tickets` | `rename-tag-to-label` | 4.5/6 | 5.5/6 | 04-migrate-in-batches, 05-contract-last | - |
| `slicing-tickets` | `settle-up-cut` | 3.0/6 | 4.5/6 | 01-ticket-graph, 03-e2e-scenarios | - |

Pass counts are the mean over reps. Graders: script assertions run on the final project; llm assertions judged by `claude-opus-5-5` (a different model from the one tested).

## Failed assertions

| Skill / case | Config | Rep | Assertion | Evidence |
|---|---|---|---|---|
| `ask-until-clear/client-retry-check` | with | 0 | `04-no-interview`: The reply answers instead of interviewing: it does not put two or more questions to the user about how retries should be... [122 more chars] | The reply has five question-plus-recommendation blocks (❓ Q1–Q5, each followed by a ➡️ answer) about retry design and scope. |
| `ask-until-clear/client-retry-check` | with | 1 | `04-no-interview`: The reply answers instead of interviewing: it does not put two or more questions to the user about how retries should be... [122 more chars] | Reply contains Q1–Q5 design questions each followed by a recommended answer (➡️) |
| `ask-until-clear/fx-rates-cache` | none | 0 | `02-premise-recommended-yes`: The first question is written as a proposal the agent recommends accepting, so its recommended answer is yes (for exampl... [161 more chars] | Q1 "Which binary were you timing?" is an open question. It is not a proposal, and no recommended "Yes" answer is given. |
| `ask-until-clear/fx-rates-cache` | none | 1 | `02-premise-recommended-yes`: The first question is written as a proposal the agent recommends accepting, so its recommended answer is yes (for exampl... [161 more chars] | Q1 is an open question, 'Which build are you running? ... Is the slow run from a different branch, a release you installed earlier, or `carg... [70 more chars] |
| `ask-until-clear/fx-rates-cache` | none | 0 | `03-no-cache-design-now`: The reply does not ask the user, as a question to answer now, to choose a cache capacity, an eviction policy, an expiry ... [151 more chars] | Q5 asks now: "If you still want one, what's the invalidation story? ... Would you reload `rates.csv` on change?" |
| `ask-until-clear/fx-rates-cache` | none | 0 | `05-recommendations`: The reply asks the user between one and seven questions, and every one of them is followed by the agent's own recommende... [15 more chars] | The five questions, e.g. Q2 "What does 'painfully slow' mean in numbers?", have no recommended answer after them. |
| `ask-until-clear/fx-rates-cache` | none | 1 | `05-recommendations`: The reply asks the user between one and seven questions, and every one of them is followed by the agent's own recommende... [15 more chars] | Q2 'what's the input? ... What do your real export's rows look like?' and Q4 have no recommended answer from the agent. Not every question i... [18 more chars] |
| `ask-until-clear/rate-limit-links` | none | 1 | `04-recommendations`: The reply asks the user between two and seven questions, and every one of them is followed by the agent's own recommende... [15 more chars] | Q6 "Should any owner be exempt or get a different limit? For example, a per-owner override..." gives no recommended answer of the agent's ow... [2 more chars] |
| `ask-until-clear/recurring-tasks` | none | 1 | `02-completion-question`: In this round the reply asks what completing a recurring task should do (for example create the next occurrence as a new... [189 more chars] | The reply states the completion behavior as a decision ('Hướng mình đề xuất: sinh task kế tiếp ngay khi done'). None of the numbered questio... [51 more chars] |
| `ask-until-clear/recurring-tasks` | none | 0 | `02-completion-question`: In this round the reply asks what completing a recurring task should do (for example create the next occurrence as a new... [189 more chars] | The completion behavior is stated as a settled proposal ("Khi `done`, tool tạo một task mới...") placed before "những chỗ mình cần bạn chốt"... [32 more chars] |
| `ask-until-clear/recurring-tasks` | none | 1 | `04-premise-first`: The first question in the reply challenges whether recurring tasks are worth building at all, compared with leaving tdo ... [136 more chars] | The first question is '1. Tính ngày kế tiếp từ đâu?', which is about implementation. Nothing questions whether recurring tasks are worth bui... [6 more chars] |
| `ask-until-clear/recurring-tasks` | none | 0 | `04-premise-first`: The first question in the reply challenges whether recurring tasks are worth building at all, compared with leaving tdo ... [136 more chars] | The first question is "**1. Tính \"lần sau\" từ đâu?**", which is about implementation. Whether the feature is worth building is never quest... [6 more chars] |
| `ask-until-clear/recurring-tasks` | none | 0 | `05-recommendations`: The reply asks the user between two and seven questions, and every one of them is followed by the agent's own recommende... [15 more chars] | The sub-question "'Đầu tháng' là mùng 1, hay ngày làm việc đầu tiên của tháng?" has no recommended answer, and Q5 ends "Bạn chọn cái nào, ha... [31 more chars] |
| `term-guard/credit-two-meanings-vi` | none | 1 | `01-nothing-changed`: The repository has no new, modified, or deleted files and no new commit after the run: no expiry code, no endpoint, no t... [26 more chars] | script exit 1:  |
| `term-guard/credit-two-meanings-vi` | none | 0 | `01-nothing-changed`: The repository has no new, modified, or deleted files and no new commit after the run: no expiry code, no endpoint, no t... [26 more chars] | script exit 1:  |
| `term-guard/credit-two-meanings-vi` | none | 1 | `02-asks-which-credit`: The final message asks the user which kind of credit should expire after 90 days (the money credit on a billing account,... [108 more chars] | The reply picks one meaning without asking: "Bạn nói "số credit" nên mình hiểu là loại đếm số buổi." |
| `term-guard/credit-two-meanings-vi` | none | 0 | `02-asks-which-credit`: The final message asks the user which kind of credit should expire after 90 days (the money credit on a billing account,... [108 more chars] | The run picked one meaning without asking: "Mình hiểu 'credit' là credit của class pack (số buổi), không phải store credit tính bằng cents t... [16 more chars] |
| `term-guard/credit-two-meanings-vi` | none | 0 | `03-names-both`: The final message names both meanings concretely from this repo: the account credit balance in internal/billing (Account... [144 more chars] | It mentions "store credit tính bằng cents trong `billing`" and class pack credits, but never names Account.CreditCents, AddCredit, Pack.Cred... [14 more chars] |
| `term-guard/credit-two-meanings-vi` | none | 1 | `04-no-done-claim`: The final message does not claim that credit expiry, its tests, or the expiring-soon endpoint were implemented. | "Credit của class pack giờ hết hạn sau 90 ngày kể từ ngày mua pack, và có endpoint trả về số credit sắp hết hạn trong 7 ngày tới. `go vet` v... [28 more chars] |
| `term-guard/credit-two-meanings-vi` | none | 0 | `04-no-done-claim`: The final message does not claim that credit expiry, its tests, or the expiring-soon endpoint were implemented. | "Credit của class pack giờ hết hạn sau 90 ngày kể từ ngày mua, và có endpoint mới `GET /members/{id}/packs/expiring`. `gofmt`, `go vet` và `... [24 more chars] |
| `term-guard/loan-rule-vs-code` | with | 0 | `01-overdue-works`: `cargo test` passes, and through the existing Desk API `desk.overdue(Day(20))` (or with a plain day number) returns exac... [169 more chars] | script exit 1:  |
| `term-guard/loan-rule-vs-code` | with | 1 | `01-overdue-works`: `cargo test` passes, and through the existing Desk API `desk.overdue(Day(20))` (or with a plain day number) returns exac... [169 more chars] | script exit 1:  |
| `term-guard/loan-rule-vs-code` | with | 0 | `02-loan-entry`: GLOSSARY.md has a Loan entry with a definition and an `_Avoid_` line that lists "checkout" or "borrowing". | script exit 1:  |
| `term-guard/loan-rule-vs-code` | with | 1 | `02-loan-entry`: GLOSSARY.md has a Loan entry with a definition and an `_Avoid_` line that lists "checkout" or "borrowing". | script exit 1:  |
| `term-guard/tracking-id-ulid-adr` | with | 1 | `02-adr-numbered-0005`: The decision went into the ADR folder named in CLAUDE.md: docs/decisions/ holds exactly one new file, numbered 0005 (one... [147 more chars] | script exit 1:  |
| `term-guard/tracking-id-ulid-adr` | none | 0 | `05-adr-content`: The new ADR in docs/decisions/ is short (a title and roughly one to three sentences, not a long multi-section template) ... [237 more chars] | docs/decisions/0005-public-tracking-id.md is untracked, so it is absent from the git diff, and the Bash call that wrote it is clipped; its t... [50 more chars] |
| `term-guard/tracking-id-ulid-adr` | none | 1 | `05-adr-content`: The new ADR in docs/decisions/ is short (a title and roughly one to three sentences, not a long multi-section template) ... [237 more chars] | docs/decisions/0005-public-tracking-id.md is untracked and absent from the git diff, and the glossary Bash call that likely wrote it is clip... [76 more chars] |
| `term-guard/tracking-id-ulid-adr` | with | 0 | `05-adr-content`: The new ADR in docs/decisions/ is short (a title and roughly one to three sentences, not a long multi-section template) ... [237 more chars] | The ADR body is clipped in the transcript ('cat > docs/decisions/000... [623 more chars]') and the untracked file is not in the diff; the fi... [194 more chars] |
| `term-guard/tracking-id-ulid-adr` | with | 1 | `05-adr-content`: The new ADR in docs/decisions/ is short (a title and roughly one to three sentences, not a long multi-section template) ... [237 more chars] | docs/decisions/0005-public-tracking-id-is-a-ulid.md is untracked, so its contents never appear in the diff. Its length and wording can't be ... [167 more chars] |
| `understand-this-code/empty-phone-shadowed` | with | 0 | `06-test-wrong-reason`: The final message points out that test_empty_returns_none in tests/test_phone.py passes even though the function does no... [143 more chars] | Reply only says the assertFalse tests "sẽ lỗi vì có exception"; it never says they currently pass only because "" is falsy, so the green sui... [32 more chars] |
| `understand-this-code/legacy-sms-not-dead` | none | 1 | `04-ran-the-path`: The run executed code that goes through the worker's lookup or the schedule (for example `python3 -m notifier run paymen... [197 more chars] | The only tool calls were Grep, Grep, Read worker.py and Read schedule.json. Nothing ran the worker lookup or the schedule. |
| `understand-this-code/legacy-sms-not-dead` | none | 0 | `04-ran-the-path`: The run executed code that goes through the worker's lookup or the schedule (for example `python3 -m notifier run paymen... [197 more chars] | Tool calls were only Grep, Grep, Read worker.py, Read schedule.json; nothing was executed |
| `understand-this-code/legacy-sms-not-dead` | with | 0 | `04-ran-the-path`: The run executed code that goes through the worker's lookup or the schedule (for example `python3 -m notifier run paymen... [197 more chars] | "I didn't run `run_job` or the tests. The conclusion comes from reading `worker.py` and the schedule"; the only tool calls were Grep, git gr... [15 more chars] |
| `understand-this-code/per-line-rounding-why` | with | 1 | `03-no-invented-reason`: The final message does not present any motive for per-line rounding as the known or recorded reason. Every motive it off... [297 more chars] | Opens with "There is a reason" and says "The per-line commit fixes that mismatch" as fact; it suggests asking finance, never Minh Hoang or t... [20 more chars] |
| `understand-this-code/per-line-rounding-why` | none | 1 | `05-ran-the-numbers`: The run executed node code that computes totals both ways or on the old and new code (a one-liner, a scratch script, the... [200 more chars] | Only git log/show, Grep and cat were run. No node execution happened; the 339 vs 338 figures come from reading the test diff. |
| `understand-this-code/per-line-rounding-why` | none | 0 | `05-ran-the-numbers`: The run executed node code that computes totals both ways or on the old and new code (a one-liner, a scratch script, the... [200 more chars] | The only tool calls were git log/show, cat and Grep. No node code was run, so the 3.39 vs 3.38 figures were not produced by execution. |
| `understand-this-code/per-line-rounding-why` | none | 0 | `06-what-breaks`: The final message names the test in test/pricing.test.js that pins the per-line result (net 339 for three discounted mug... [182 more chars] | It mentions the invoice.js use of lineTotalCents and that lines would add to 3.39 vs Net 3.38. It notes the test went from 338 to 339 but ne... [47 more chars] |
| `understand-this-code/rename-qty-field` | none | 1 | `04-reports-template`: The final message says that internal/render/templates/invoice.tmpl referred to the field by name (`.Qty`), that this ref... [107 more chars] | Reply says "The template refers to `.Qty` by name, and the compiler doesn't check that... It now uses `.Quantity`" but never says the existi... [24 more chars] |
| `understand-this-code/rename-qty-field` | none | 0 | `04-reports-template`: The final message says that internal/render/templates/invoice.tmpl referred to the field by name (`.Qty`), that this ref... [107 more chars] | Reply says "A missed rename there would only fail when an invoice is printed, not at compile time, so I changed it too"; it never says the e... [39 more chars] |
| `understand-this-code/rename-qty-field` | with | 0 | `04-reports-template`: The final message says that internal/render/templates/invoice.tmpl referred to the field by name (`.Qty`), that this ref... [107 more chars] | Final reply says "`invoice.tmpl:5` reads `.Qty` by name at runtime, so the compiler can't check it. I renamed it to `.Quantity`" but never s... [38 more chars] |
| `understand-this-code/rename-qty-field` | with | 1 | `05-ran-invoice`: After its last edit to the code or template, the run executed the invoice command in text mode (for example `go run ./cm... [140 more chars] | The only post-edit tool call is the sed/gofmt/grep Bash command, clipped at "[260 more chars]". No visible part of the trace runs `go run ./... [108 more chars] |
| `research/retry-front-or-back` | none | 1 | `03-asks-grounded-question`: The final message asks the user to choose, or asks for the constraint that decides it, with a question tied to this code... [203 more chars] | The reply asks no question. It gives a recommendation plus the conditional "If completion order within a shot matters, go with front", and e... [74 more chars] |
| `research/retry-front-or-back` | none | 0 | `03-asks-grounded-question`: The final message asks the user to choose, or asks for the constraint that decides it, with a question tied to this code... [203 more chars] | The final reply asks no question. It gives a recommendation ("Recommendation: front.") and a conditional ("If that matters more to you than ... [95 more chars] |
| `research/retry-front-or-back` | with | 1 | `03-asks-grounded-question`: The final message asks the user to choose, or asks for the constraint that decides it, with a question tied to this code... [203 more chars] | Final reply ends with a recommendation ("My recommendation: front") and a 'Not verified' list; it asks the user no question about FIFO vs. h... [22 more chars] |
| `prototyping-designs/levels-btree-proposed` | with | 0 | `01-repo-untouched`: The repository is unchanged: no tracked file was added, modified, or deleted, no commit was added or rewritten, and no n... [73 more chars] | script exit 1: changes outside ignored paths:
 M docs/adr/0005-btreemap-price-levels.md |
| `prototyping-designs/levels-btree-proposed` | with | 1 | `01-repo-untouched`: The repository is unchanged: no tracked file was added, modified, or deleted, no commit was added or rewritten, and no n... [73 more chars] | script exit 1: changes outside ignored paths:
 M docs/adr/0005-btreemap-price-levels.md |
| `prototyping-designs/limiter-vague-vi` | none | 1 | `01-repo-untouched`: The repository is unchanged: no tracked file was added, modified, or deleted, no commit was added or rewritten, and no n... [73 more chars] | script exit 1: changes outside ignored paths:
?? experiments/README.md
?? experiments/evict_test.go
?? experiments/lock_test.go
?? experimen... [21 more chars] |
| `prototyping-designs/limiter-vague-vi` | none | 0 | `01-repo-untouched`: The repository is unchanged: no tracked file was added, modified, or deleted, no commit was added or rewritten, and no n... [73 more chars] | script exit 1: changes outside ignored paths:
?? proto/locks/locks_test.go
?? proto/retry/retry_test.go
?? proto/shard/shard_test.go |
| `prototyping-designs/limiter-vague-vi` | none | 1 | `02-nothing-built`: The agent built no prototype: no Write, Edit, or Bash call creates or changes a Go file or any other program, benchmark,... [140 more chars] | TOOL Write: experiments/lock_test.go, evict_test.go, retryafter_test.go created and run with go test -bench |
| `prototyping-designs/limiter-vague-vi` | none | 0 | `02-nothing-built`: The agent built no prototype: no Write, Edit, or Bash call creates or changes a Go file or any other program, benchmark,... [140 more chars] | TOOL Bash: mkdir -p proto/shard proto/locks proto/retry && cat > proto/shard/shard_test.go <<'EOF' ... |
| `prototyping-designs/limiter-vague-vi` | none | 1 | `04-asks-which`: The final message asks the user which open question to settle first (or which one the prototype should answer), in any l... [8 more chars] | Only question is 'Bạn muốn mình cập nhật phần "Open questions" thành "Decisions" theo các kết quả trên không?' — not asking which question t... [14 more chars] |
| `prototyping-designs/limiter-vague-vi` | none | 0 | `04-asks-which`: The final message asks the user which open question to settle first (or which one the prototype should answer), in any l... [8 more chars] | Only closing question is 'sửa design doc ... hoặc chuyển bản lazy refill + sweeper vào `limiter/`... bạn muốn làm cái nào?', not which open ... [24 more chars] |
| `prototyping-designs/limiter-vague-vi` | none | 1 | `05-no-pick`: The final message does not present results from a prototype, benchmark, or deadlock experiment, and does not announce th... [54 more chars] | 'Mình đã làm prototype cho cả 3 câu hỏi mở... Một mutex mất khoảng 950 ns/op' and 'Mình dựng đúng thiết kế đó và nó treo sau khoảng 1 giây' |
| `prototyping-designs/limiter-vague-vi` | none | 0 | `05-no-pick`: The final message does not present results from a prototype, benchmark, or deadlock experiment, and does not announce th... [54 more chars] | 'Mình đã làm prototype cho cả 3 câu hỏi mở trong design doc.' plus benchmark table and 'deadlock sau ~0.6s' |
| `prototyping-designs/reopen-net-zero` | with | 1 | `01-product-untouched`: The repository is unchanged: no tracked file was added, modified, or deleted, no commit was added or rewritten, and no n... [73 more chars] | script exit 1: changes outside ignored paths:
 M spec.md |
| `prototyping-designs/schedule-shape-decided` | none | 1 | `01-repo-untouched`: The repository is unchanged: no tracked file was added, modified, or deleted, no commit was added or rewritten, and no n... [73 more chars] | script exit 1: changes outside ignored paths:
?? scratch/schedule-shapes.ts |
| `prototyping-designs/schedule-shape-decided` | none | 1 | `02-no-mockups`: The agent wrote no mock-up or prototype code: no Write, Edit, or Bash call creates or changes a .ts, .js, or other code ... [185 more chars] | TOOL Write: {"file_path": ".../work/scratch/schedule-shapes.ts", ...} created the mockup file |
| `prototyping-designs/schedule-shape-decided` | none | 0 | `02-no-mockups`: The agent wrote no mock-up or prototype code: no Write, Edit, or Bash call creates or changes a .ts, .js, or other code ... [185 more chars] | Bash: cat > /tmp/schedule-mock/mock.ts <<'EOF' // Throwaway mock: two shapes for scheduled sends, same billing caller. |
| `prototyping-designs/schedule-shape-decided` | none | 1 | `05-no-handover`: The final message does not hand over a mock-up: apart from quoting the developer's own two one-line snippets, it shows o... [111 more chars] | "`scratch/schedule-shapes.ts` is untracked ... `node scratch/schedule-shapes.ts` runs it" plus builder code block with billingDefaults/idemp... [9 more chars] |
| `prototyping-designs/schedule-shape-decided` | none | 0 | `05-no-handover`: The final message does not hand over a mock-up: apart from quoting the developer's own two one-line snippets, it shows o... [111 more chars] | "It's at `/tmp/schedule-mock/mock.ts`, outside the repo." and shows new builder code with `.create()` and a billing caller |
| `spec-it/court-waitlist-wording` | none | 1 | `01-draft-no-open-questions`: A new spec file exists (under docs/features/ or anywhere else in the repo), its status line says draft rather than appro... [146 more chars] | script exit 1: FAIL: no status line saying draft in ['docs/features/waitlist/spec.md'] |
| `spec-it/court-waitlist-wording` | with | 1 | `01-draft-no-open-questions`: A new spec file exists (under docs/features/ or anywhere else in the repo), its status line says draft rather than appro... [146 more chars] | script exit 1: FAIL: open questions listed: 1. **Who can join?** The notes only cover joining a booked Slot. What if the Member already hold... [55 more chars] |
| `spec-it/court-waitlist-wording` | with | 0 | `01-draft-no-open-questions`: A new spec file exists (under docs/features/ or anywhere else in the repo), its status line says draft rather than appro... [146 more chars] | script exit 1: FAIL: open questions listed: 1. **Offer to a member at 3 upcoming bookings (J3.4).** Their accept is refused. Does the offer ... [55 more chars] |
| `spec-it/court-waitlist-wording` | none | 1 | `02-no-interview-words`: The spec does not use the words docs/language/terms.md marks to avoid (reservation/reserve, customer, client, player, ti... [248 more chars] | script exit 1: FAIL: interview words in the spec: customer, invite |
| `spec-it/court-waitlist-wording` | with | 0 | `02-no-interview-words`: The spec does not use the words docs/language/terms.md marks to avoid (reservation/reserve, customer, client, player, ti... [248 more chars] | script exit 1: FAIL: interview words in the spec: queue |
| `spec-it/court-waitlist-wording` | none | 1 | `05-paths-checks-criteria`: The spec has at least four numbered test paths that each have a Check line, and at least five numbered acceptance criter... [51 more chars] | script exit 1: FAIL: 0 numbered test paths, need at least 4 |
| `spec-it/court-waitlist-wording` | none | 0 | `05-paths-checks-criteria`: The spec has at least four numbered test paths that each have a Check line, and at least five numbered acceptance criter... [51 more chars] | script exit 1: FAIL: 0 numbered test paths, need at least 4 |
| `spec-it/court-waitlist-wording` | none | 1 | `06-checks-drive-real-api`: The spec's Check lines drive the real courtly HTTP API (for example POST /bookings, DELETE /bookings/{id}, GET /members/... [254 more chars] | The visible spec has no Check lines against a running server (no `go run . -demo`, no observed status or MAIL output). Its acceptance exampl... [116 more chars] |
| `spec-it/court-waitlist-wording` | none | 0 | `06-checks-drive-real-api`: The spec's Check lines drive the real courtly HTTP API (for example POST /bookings, DELETE /bookings/{id}, GET /members/... [254 more chars] | The spec's acceptance checks section is clipped ('Accepting... [1912 more chars]'), so the evidence shows no Check line that drives POST /bo... [106 more chars] |
| `spec-it/court-waitlist-wording` | with | 1 | `06-checks-drive-real-api`: The spec's Check lines drive the real courtly HTTP API (for example POST /bookings, DELETE /bookings/{id}, GET /members/... [254 more chars] | Check lines only say e.g. "Check: API, club service with demo data and a clock the tester can set, observe the response...". They name no HT... [249 more chars] |
| `spec-it/court-waitlist-wording` | with | 0 | `06-checks-drive-real-api`: The spec's Check lines drive the real courtly HTTP API (for example POST /bookings, DELETE /bookings/{id}, GET /members/... [254 more chars] | Check lines say "API, club service with a recording mailer and a settable clock" and "mail log shows..."; none names a real endpoint (POST /... [109 more chars] |
| `spec-it/invoice-csv-import` | with | 1 | `01-draft-no-open-questions`: A new spec file exists (under docs/features/ or anywhere else in the repo), its status line says draft rather than appro... [146 more chars] | script exit 1: FAIL: open questions listed: The interview notes say "None left", but these were not settled. Each has a recommended answer. ... [55 more chars] |
| `spec-it/invoice-csv-import` | with | 0 | `01-draft-no-open-questions`: A new spec file exists (under docs/features/ or anywhere else in the repo), its status line says draft rather than appro... [146 more chars] | script exit 1: FAIL: open questions listed: The interview closed with "none left", but these were never asked. Each has a recommended answer... [55 more chars] |
| `spec-it/invoice-csv-import` | none | 0 | `02-check-lines`: The spec has at least three numbered test paths (J1.1, J1.2, ...; as headings, list items or table rows) and every one o... [60 more chars] | script exit 1: FAIL: 0 numbered test paths, need at least 3 |
| `spec-it/invoice-csv-import` | none | 1 | `02-check-lines`: The spec has at least three numbered test paths (J1.1, J1.2, ...; as headings, list items or table rows) and every one o... [60 more chars] | script exit 1: FAIL: 0 numbered test paths, need at least 3 |
| `spec-it/invoice-csv-import` | none | 0 | `03-criteria-name-paths`: The spec has at least five numbered acceptance criteria (AC1, AC2, ...), each one names a test path (J1.1, ...) that exi... [115 more chars] | script exit 1: FAIL: 0 numbered criteria, need at least 5 |
| `spec-it/invoice-csv-import` | none | 1 | `03-criteria-name-paths`: The spec has at least five numbered acceptance criteria (AC1, AC2, ...), each one names a test path (J1.1, ...) that exi... [115 more chars] | script exit 1: FAIL: 0 numbered criteria, need at least 5 |
| `spec-it/invoice-csv-import` | none | 0 | `06-checks-drive-real-api`: The spec's Check lines drive the real ledgerline HTTP API with an API key (for example curl or a script sending the X-Ap... [331 more chars] | Acceptance criteria are abstract (e.g. '7. Each rule of the table is covered by a test of a row that breaks only that rule'); no Check lines... [64 more chars] |
| `spec-it/invoice-csv-import` | none | 1 | `06-checks-drive-real-api`: The spec's Check lines drive the real ledgerline HTTP API with an API key (for example curl or a script sending the X-Ap... [331 more chars] | The visible acceptance criteria are outcome statements such as "A valid file of N rows (1 to 500) issues N invoices... `GET /invoices` lists... [110 more chars] |
| `spec-it/parcel-webhook-retries` | none | 0 | `01-draft-structure`: A new spec file exists (anywhere in the repo) with a status line saying draft, at least four numbered test paths that ea... [117 more chars] | script exit 1: FAIL: no status line saying draft in ['docs/features/webhook-retries/spec.md'] |
| `spec-it/parcel-webhook-retries` | none | 1 | `01-draft-structure`: A new spec file exists (anywhere in the repo) with a status line saying draft, at least four numbered test paths that ea... [117 more chars] | script exit 1: FAIL: no status line saying draft in ['docs/features/webhook-retries/spec.md'] |
| `spec-it/parcel-webhook-retries` | none | 0 | `02-no-design-in-spec`: The spec says what parcelpost does, not how it is built: it names no source file or module (such as webhooks.js or a sch... [264 more chars] | script exit 1: FAIL: design in the spec: field name 'ParcelError'; field name 'allSettled'; field name 'createServer'; field name 'deliveryI... [54 more chars] |
| `spec-it/parcel-webhook-retries` | none | 1 | `02-no-design-in-spec`: The spec says what parcelpost does, not how it is built: it names no source file or module (such as webhooks.js or a sch... [264 more chars] | script exit 1: FAIL: design in the spec: field name 'ParcelError'; field name 'createServer'; field name 'deliveryId'; field name 'fakeMerch... [54 more chars] |
| `spec-it/parcel-webhook-retries` | with | 1 | `02-no-design-in-spec`: The spec says what parcelpost does, not how it is built: it names no source file or module (such as webhooks.js or a sch... [264 more chars] | script exit 1: FAIL: design in the spec: field name 'nextAttemptAt'; new route '/deliveries/:id/resend' |
| `spec-it/parcel-webhook-retries` | with | 0 | `02-no-design-in-spec`: The spec says what parcelpost does, not how it is built: it names no source file or module (such as webhooks.js or a sch... [264 more chars] | script exit 1: FAIL: design in the spec: field name 'deliveryId'; field name 'nextAttemptAt'; new route '/merchants/:merchantId/deliveries/:... [18 more chars] |
| `spec-it/parcel-webhook-retries` | none | 0 | `03-says-design-comes-later`: The final message tells the user that the store fields, where the retry logic lives and how it wakes up, and the re-send... [137 more chars] | The final reply says the opposite: it puts the design in the spec ('Store fields: Each delivery gets `attempts[]`...', 'a polling loop every... [122 more chars] |
| `spec-it/parcel-webhook-retries` | none | 1 | `03-says-design-comes-later`: The final message tells the user that the store fields, where the retry logic lives and how it wakes up, and the re-send... [137 more chars] | Final reply says the spec "makes the design calls in sections 2 to 7" and details store fields, retries.js polling loop, and POST /deliverie... [57 more chars] |
| `spec-it/parcel-webhook-retries` | with | 1 | `03-says-design-comes-later`: The final message tells the user that the store fields, where the retry logic lives and how it wakes up, and the re-send... [137 more chars] | The reply defers the store fields and retry location/wake-up to 'the architecture step', but says the re-send bodies 'weren't settled in the... [88 more chars] |
| `spec-it/parcel-webhook-retries` | with | 0 | `03-says-design-comes-later`: The final message tells the user that the store fields, where the retry logic lives and how it wakes up, and the re-send... [137 more chars] | The reply defers store fields, module placement and wake-up to the architecture step, but says "The only exception is the re-send request an... [105 more chars] |
| `spec-it/parcel-webhook-retries` | none | 0 | `04-retry-criteria`: The spec's numbered criteria state the settled behaviour from the interview: retries 1, 5 and 30 minutes after a failed ... [348 more chars] | The spec has no numbered criteria of its own. It defers to the interview ('Its numbered points (S1-S8) are the requirements; this file decid... [124 more chars] |
| `spec-it/parcel-webhook-retries` | none | 1 | `04-retry-criteria`: The spec's numbered criteria state the settled behaviour from the interview: retries 1, 5 and 30 minutes after a failed ... [348 more chars] | Section 1 'Behaviour (settled in the interview)' states 1/5/30 min retries, `retrying` with next due time, `failed` after 4th, one-attempt r... [117 more chars] |
| `spec-it/parcel-webhook-retries` | with | 1 | `04-retry-criteria`: The spec's numbered criteria state the settled behaviour from the interview: retries 1, 5 and 30 minutes after a failed ... [348 more chars] | The numbered acceptance criteria are clipped ('[7036 more chars]'); the visible journeys and the Edit's bullet list don't show numbered crit... [80 more chars] |
| `spec-it/parcel-webhook-retries` | with | 1 | `06-open-questions-empty`: A spec file exists and lists no open question (its Open questions section, if there is one, is empty or says none), beca... [37 more chars] | script exit 1: FAIL: open questions listed: The interview settled the behavior above. It did not settle the items below, which you asked to ... [56 more chars] |
| `spec-it/parcel-webhook-retries` | with | 0 | `06-open-questions-empty`: A spec file exists and lists no open question (its Open questions section, if there is one, is empty or says none), beca... [37 more chars] | script exit 1: FAIL: open questions listed: Q1. **The re-send call.** The interview says Support re-sends "through the API" but does not giv... [56 more chars] |
| `spec-it/pomo-weekly-gaps` | none | 0 | `01-draft-for-settled-part`: A new spec file for `pomo week` exists (anywhere in the repo) with a status line saying draft, at least two numbered tes... [117 more chars] | script exit 1: FAIL: 0 numbered test paths, need at least 2 |
| `spec-it/pomo-weekly-gaps` | none | 1 | `01-draft-for-settled-part`: A new spec file for `pomo week` exists (anywhere in the repo) with a status line saying draft, at least two numbered tes... [117 more chars] | script exit 1: FAIL: 0 numbered test paths, need at least 2 |
| `spec-it/pomo-weekly-gaps` | none | 0 | `02-gaps-are-open-questions`: The spec's Open questions section (or an equivalent unresolved / to-decide section) covers all three points the intervie... [102 more chars] | script exit 1: FAIL: no Open questions section with content |
| `spec-it/pomo-weekly-gaps` | none | 1 | `02-gaps-are-open-questions`: The spec's Open questions section (or an equivalent unresolved / to-decide section) covers all three points the intervie... [102 more chars] | script exit 1: FAIL: no Open questions section with content |
| `spec-it/pomo-weekly-gaps` | none | 0 | `03-no-criterion-settles-gaps`: No acceptance criterion, test path or Check line settles an open point: none fixes Monday or Sunday as the start of the ... [110 more chars] | script exit 1: FAIL: no criteria or test paths to inspect |
| `spec-it/pomo-weekly-gaps` | none | 1 | `03-no-criterion-settles-gaps`: No acceptance criterion, test path or Check line settles an open point: none fixes Monday or Sunday as the start of the ... [110 more chars] | script exit 1: FAIL: no criteria or test paths to inspect |
| `spec-it/pomo-weekly-gaps` | with | 1 | `03-no-criterion-settles-gaps`: No acceptance criterion, test path or Check line settles an open point: none fixes Monday or Sunday as the start of the ... [110 more chars] | script exit 1: FAIL: settles an open point: AC4 (J1.1): A session that started on Sunday of the current week is counted. |
| `spec-it/pomo-weekly-gaps` | none | 0 | `04-recommended-answers`: Each entry under the spec's Open questions carries a recommended answer from the spec author (for example "Recommend: Mo... [46 more chars] | spec.md has no 'Open questions' section; the unresolved items appear as settled choices under 'Decisions for approval' ("The week starts on ... [60 more chars] |
| `spec-it/pomo-weekly-gaps` | none | 1 | `04-recommended-answers`: Each entry under the spec's Open questions carries a recommended answer from the spec author (for example "Recommend: Mo... [46 more chars] | Open items under 'Not in this version' list only bare questions, e.g. "Open: only the week before, or any week? And how does she ask (a flag... [39 more chars] |
| `spec-it/pomo-weekly-gaps` | none | 0 | `05-not-approvable-yet`: The final message tells the user the spec cannot be approved tonight because open questions remain (week start, earlier ... [155 more chars] | Final reply: "Bạn cần quyết ba chỗ trước khi duyệt" plus "Duyệt spec nghĩa là chấp nhận Linh chưa xem lại được"; it frames the spec as appro... [79 more chars] |
| `spec-it/pomo-weekly-gaps` | none | 1 | `05-not-approvable-yet`: The final message tells the user the spec cannot be approved tonight because open questions remain (week start, earlier ... [155 more chars] | Final reply says "Để duyệt được ngay tối nay, mình chốt phần 'đã settled'..." and treats Sunday as decided, offering items to check while ap... [62 more chars] |
| `spec-it/pomo-weekly-gaps` | with | 1 | `05-not-approvable-yet`: The final message tells the user the spec cannot be approved tonight because open questions remain (week start, earlier ... [155 more chars] | The reply opens with 'Tối nay bạn chưa duyệt được ngay', but then offers a shortcut: 'Nếu đồng ý hết đề xuất, bạn chỉ cần trả lời "ok hết"… ... [129 more chars] |
| `designing-architecture/invoice-vat-no-seam` | none | 1 | `05-not-ready-for-gate`: The final message does not present the architecture as complete or ready for the user's approval while AC3 is unresolved... [1 more chars] | The reply ends "Say when you want me to start on the code. The order is the member parser and `money.rs` first...", which presents the desig... [56 more chars] |
| `designing-architecture/invoice-vat-no-seam` | none | 0 | `05-not-ready-for-gate`: The final message does not present the architecture as complete or ready for the user's approval while AC3 is unresolved... [1 more chars] | Ends with "Say when you want me to start on the code." This presents the design as ready to approve and move to code, and AC3 is never named... [27 more chars] |
| `designing-architecture/partner-sync-rfc` | none | 1 | `01-draft-with-ac-table`: An architecture document for partner-catalog exists (docs/features/partner-catalog/architecture.md, or another markdown ... [157 more chars] | script exit 1: docs/features/partner-catalog/architecture.md status: draft missing rows: ['AC3', 'AC4'] |
| `designing-architecture/partner-sync-rfc` | none | 0 | `01-draft-with-ac-table`: An architecture document for partner-catalog exists (docs/features/partner-catalog/architecture.md, or another markdown ... [157 more chars] | script exit 1: docs/features/partner-catalog/architecture.md status: draft missing rows: ['AC1', 'AC2', 'AC4'] |
| `designing-architecture/partner-sync-rfc` | none | 1 | `02-rfc-file-exists`: A new markdown file other than the architecture document exists whose name or title identifies it as an RFC and whose te... [116 more chars] | script exit 1: no new RFC file about the Brightline channel; new markdown files: docs/adr/0002-poll-the-supplier-changes-feed.md
docs/featur... [34 more chars] |
| `designing-architecture/partner-sync-rfc` | none | 0 | `02-rfc-file-exists`: A new markdown file other than the architecture document exists whose name or title identifies it as an RFC and whose te... [116 more chars] | script exit 1: no new RFC file about the Brightline channel; new markdown files: docs/adr/0002-supplier-sync-polls-the-changes-feed.md
docs/... [53 more chars] |
| `designing-architecture/partner-sync-rfc` | none | 1 | `03-rfc-content`: The RFC states the unsettled question (whether our Brightline contract includes the Enterprise sync add-on, that is webh... [206 more chars] | Only docs/adr/0002 and architecture.md were written (git status); no RFC file exists, so none is linked from the architecture document. |
| `designing-architecture/partner-sync-rfc` | none | 0 | `03-rfc-content`: The RFC states the unsettled question (whether our Brightline contract includes the Enterprise sync add-on, that is webh... [206 more chars] | Only architecture.md and ADR 0002 were created (git status shows just those two files); no RFC was written or linked from the architecture d... [3 more chars] |
| `designing-architecture/partner-sync-rfc` | none | 1 | `04-no-adr-decides-ingestion`: No ADR added by the run records webhooks, or polling the changes feed, as the decided way to receive Brightline's produc... [100 more chars] | ADR 0002: "We run supplier sync by polling Brightline's changes feed with a cursor, not by receiving webhooks." |
| `designing-architecture/partner-sync-rfc` | none | 0 | `04-no-adr-decides-ingestion`: No ADR added by the run records webhooks, or polling the changes feed, as the decided way to receive Brightline's produc... [100 more chars] | ADR 0002 'Supplier sync polls Brightline's changes feed; no webhooks yet' records polling the changes feed as the decided ingestion method. |
| `designing-architecture/partner-sync-rfc` | with | 0 | `04-no-adr-decides-ingestion`: No ADR added by the run records webhooks, or polling the changes feed, as the decided way to receive Brightline's produc... [100 more chars] | The run added docs/adr/0002-brightline-sync-polls-the-changes-feed.md: 'We read Brightline's changes feed ... on a timer, and we do not buil... [26 more chars] |
| `designing-architecture/partner-sync-rfc` | with | 1 | `04-no-adr-decides-ingestion`: No ADR added by the run records webhooks, or polling the changes feed, as the decided way to receive Brightline's produc... [100 more chars] | Run added docs/adr/0002-brightline-sync-polls-the-changes-feed-in-process.md: 'We poll the changes feed from a module in the catalog process... [55 more chars] |
| `designing-architecture/partner-sync-rfc` | none | 1 | `05-ts-sketch-parses`: The architecture document holds a TypeScript sketch: at least one fenced ts or typescript block declares an interface, t... [248 more chars] | script exit 1: docs/features/partner-catalog/architecture.md blocks: 0 syntax errors: [] declares: False refers to existing code: False |
| `designing-architecture/partner-sync-rfc` | none | 0 | `05-ts-sketch-parses`: The architecture document holds a TypeScript sketch: at least one fenced ts or typescript block declares an interface, t... [248 more chars] | script exit 1: docs/features/partner-catalog/architecture.md blocks: 0 syntax errors: [] declares: False refers to existing code: False |
| `designing-architecture/quota-cli-go` | none | 0 | `04-designs-compared`: The architecture document compares at least two designs that differ in structure, built on the existing code (for exampl... [286 more chars] | architecture.md only says "we add a history file. See ADR 0002 for the options considered"; ADR 0002 lists the rejected options with their d... [226 more chars] |
| `designing-architecture/shipping-refactor-vi` | none | 0 | `01-draft-with-ac-table`: An architecture document for carrier-rules exists (docs/features/carrier-rules/architecture.md, or another markdown file... [153 more chars] | script exit 1: no architecture document |
| `designing-architecture/shipping-refactor-vi` | none | 1 | `01-draft-with-ac-table`: An architecture document for carrier-rules exists (docs/features/carrier-rules/architecture.md, or another markdown file... [153 more chars] | script exit 1: no architecture document |
| `designing-architecture/shipping-refactor-vi` | none | 0 | `02-python-sketch-compiles`: The architecture document holds a Python code sketch: at least one fenced python block defines a class or function and r... [204 more chars] | script exit 1: no architecture document |
| `designing-architecture/shipping-refactor-vi` | none | 1 | `02-python-sketch-compiles`: The architecture document holds a Python code sketch: at least one fenced python block defines a class or function and r... [204 more chars] | script exit 1: no architecture document |
| `designing-architecture/shipping-refactor-vi` | none | 0 | `03-designs-compared`: The architecture document compares at least two designs that differ in structure, starting from the existing `quote()` i... [303 more chars] | The doc recommends per-carrier modules and lists rejected alternatives (data table, base class, add tests), but each alternative gets only i... [78 more chars] |
| `designing-architecture/shipping-refactor-vi` | none | 1 | `03-designs-compared`: The architecture document compares at least two designs that differ in structure, starting from the existing `quote()` i... [303 more chars] | The visible doc only details the per-carrier-module design. The alternatives appear only as a one-line rejection in the reply ('vì sao không... [122 more chars] |
| `designing-architecture/shipping-refactor-vi` | none | 0 | `04-no-tickets`: No ticket or task breakdown was produced: neither the architecture document, nor any other file the run wrote, nor the f... [97 more chars] | Final reply: "**Chia việc cho buổi họp** (bảng 4 bước trong tài liệu). 1. Thêm các dòng golden... 2. Một người viết phần refactor... 3. Mỗi ... [28 more chars] |
| `designing-architecture/shipping-refactor-vi` | none | 1 | `04-no-tickets`: No ticket or task breakdown was produced: neither the architecture document, nor any other file the run wrote, nor the f... [97 more chars] | The final reply has '**Việc chia cho cuộc họp sáng mai** 1. Bổ sung các dòng golden... Task này phải merge trước... 2. Chuyển code... 3. Rev... [39 more chars] |
| `designing-architecture/shipping-refactor-vi` | with | 0 | `04-no-tickets`: No ticket or task breakdown was produced: neither the architecture document, nor any other file the run wrote, nor the f... [97 more chars] | Final reply item 3 splits the work for the meeting: 'sau bước test nền và bước khung ... việc chuyển ba hãng độc lập nhau nên có thể giao ch... [11 more chars] |
| `designing-architecture/shipping-refactor-vi` | with | 1 | `04-no-tickets`: No ticket or task breakdown was produced: neither the architecture document, nor any other file the run wrote, nor the f... [97 more chars] | The final reply lays out handable work items for the meeting: 'Hai việc ở điểm 1 và 2 đi trước... Rồi một thay đổi dựng khung (errors.py, re... [129 more chars] |
| `designing-architecture/shipping-refactor-vi` | none | 0 | `05-existing-seams`: In the architecture document's criteria-to-seam table, every one of AC1 to AC4 is observed at an existing public boundar... [202 more chars] | The criteria-to-seam table is not visible in the clipped design.md, so there is no evidence that AC1 to AC4 are each observed at quote(), av... [46 more chars] |
| `designing-architecture/shipping-refactor-vi` | none | 1 | `05-existing-seams`: In the architecture document's criteria-to-seam table, every one of AC1 to AC4 is observed at an existing public boundar... [202 more chars] | No criteria-to-seam table mapping AC1–AC4 to quote()/available_carriers()/main()/golden test appears in the visible design.md content; the d... [36 more chars] |
| `designing-architecture/shipping-refactor-vi` | with | 0 | `05-existing-seams`: In the architecture document's criteria-to-seam table, every one of AC1 to AC4 is observed at an existing public boundar... [202 more chars] | architecture.md is clipped ('[5187 more chars]') before any criteria-to-seam table, so where AC1 to AC4 are observed cannot be verified |
| `designing-architecture/shipping-refactor-vi` | with | 1 | `05-existing-seams`: In the architecture document's criteria-to-seam table, every one of AC1 to AC4 is observed at an existing public boundar... [202 more chars] | The architecture.md content is clipped ('[7120 more chars]'), so no criteria-to-seam table mapping AC1–AC4 to quote()/available_carriers()/m... [45 more chars] |
| `slicing-tickets/rename-tag-to-label` | none | 1 | `02-ticket-graph`: Every ticket states what blocks it (possibly "none"), every blocker it names exists, the blocking edges have no cycle, t... [174 more chars] | script exit 1: FAIL: T01 (docs/features/rename-tag-to-label/tickets/T01-library-label-api.md) states no blocker line |
| `slicing-tickets/rename-tag-to-label` | with | 1 | `02-ticket-graph`: Every ticket states what blocks it (possibly "none"), every blocker it names exists, the blocking edges have no cycle, t... [174 more chars] | script exit 1: FAIL: T02 does not wait for T01 |
| `slicing-tickets/rename-tag-to-label` | none | 0 | `04-migrate-in-batches`: Moving the code over to the label names is split across at least two tickets, each naming the real files it changes (amo... [246 more chars] | The batches are cut by layer: T01 is library-only and T03 is CLI-only. T01 leaves the jot command half renamed: "The CLI output strings are ... [67 more chars] |
| `slicing-tickets/rename-tag-to-label` | none | 0 | `05-contract-last`: Removing the tag names from the code (renaming the `tags` field, leaving the old names only as deprecated wrappers in sr... [160 more chars] | Moving the old names into compat.rs and removing their bodies happens in the first ticket, not the last. T01: "src/compat.rs (new...): #[dep... [115 more chars] |
| `slicing-tickets/settle-up-cut` | none | 1 | `01-ticket-graph`: At least three settle-up tickets were written (one file per ticket under docs/features/settle-up/, or T01, T02, ... sect... [324 more chars] | script exit 1: FAIL: T02 does not wait for T01 |
| `slicing-tickets/settle-up-cut` | none | 0 | `01-ticket-graph`: At least three settle-up tickets were written (one file per ticket under docs/features/settle-up/, or T01, T02, ... sect... [324 more chars] | script exit 1: FAIL: T02 does not wait for T01 |
| `slicing-tickets/settle-up-cut` | none | 1 | `03-e2e-scenarios`: Every settle-up ticket has an end-to-end scenario section in which at least one step drives the real command (`python3 -... [253 more chars] | script exit 1: FAIL: T01 has no end-to-end scenario section |
| `slicing-tickets/settle-up-cut` | none | 0 | `03-e2e-scenarios`: Every settle-up ticket has an end-to-end scenario section in which at least one step drives the real command (`python3 -... [253 more chars] | script exit 1: FAIL: T01 has no end-to-end scenario section |
| `slicing-tickets/settle-up-cut` | with | 0 | `03-e2e-scenarios`: Every settle-up ticket has an end-to-end scenario section in which at least one step drives the real command (`python3 -... [253 more chars] | script exit 1: FAIL: T02 scenario never runs the tabby command |
| `slicing-tickets/settle-up-cut` | none | 1 | `04-vertical-real-code`: Every ticket is a vertical slice that ends in behavior a user can see through the tabby command and names the real modul... [354 more chars] | T01 is only the pure function: "No printing, no ledger access", and T02 is only the ledger format: "Do not change `net_balances` or `cli.py`... [59 more chars] |
| `slicing-tickets/settle-up-cut` | none | 0 | `04-vertical-real-code`: Every ticket is a vertical slice that ends in behavior a user can see through the tabby command and names the real modul... [354 more chars] | T01 is 'plan_transfers (the settle algorithm)... Pure function, no ledger or I/O', T02 is ledger format only, and T03 is balances only; thes... [87 more chars] |
| `slicing-tickets/settle-up-cut` | with | 0 | `04-vertical-real-code`: Every ticket is a vertical slice that ends in behavior a user can see through the tabby command and names the real modul... [354 more chars] | T04 is a ledger-format-only layer: 'Nothing creates a payment yet; that is T05. This ticket only makes the file format ready for payments.' ... [39 more chars] |
| `slicing-tickets/settle-up-cut` | with | 1 | `04-vertical-real-code`: Every ticket is a vertical slice that ends in behavior a user can see through the tabby command and names the real modul... [354 more chars] | T04's code is only the ledger format: its Where section lists only `tabby/ledger.py` ("FORMAT_VERSION = 2, load() accepts 1 and 2, save() al... [165 more chars] |

## Run health

- Runs not counted (non-zero exit, timeout or error result): 0
- Transcripts that named the real eval folder: none
- `with` runs whose first-call context is under 450 tokens larger than `none` (the skill may not have loaded): none
- Spend: tested runs $19.07, assertion grading $7.54, style comparison $1.29
- Parallel runs at a time: 4. Wall times include queueing on the shared network and are noisy; compare medians, not single runs.

## Per case

| Skill / case | cfg | n | wall s | turns | out tok | in tok | cost $ | reply words | files | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| `ask-until-clear/client-retry-check` | none | 2 | 17 | 8 | 1,829 | 44,320 | 0.057 | 360 | 0 | 100% |
| `ask-until-clear/client-retry-check` | with | 2 | 23 | 7 | 2,552 | 44,000 | 0.074 | 549 | 0 | 67% |
| `ask-until-clear/fx-rates-cache` | none | 2 | 63 | 7 | 2,025 | 58,197 | 0.072 | 408 | 0 | 57% |
| `ask-until-clear/fx-rates-cache` | with | 2 | 17 | 5 | 1,775 | 65,420 | 0.078 | 329 | 0 | 100% |
| `ask-until-clear/rate-limit-links` | none | 2 | 13 | 3 | 1,062 | 37,729 | 0.051 | 349 | 0 | 92% |
| `ask-until-clear/rate-limit-links` | with | 2 | 26 | 5 | 2,654 | 51,942 | 0.078 | 650 | 0 | 100% |
| `ask-until-clear/recurring-tasks` | none | 2 | 25 | 4 | 2,836 | 37,840 | 0.068 | 564 | 0 | 57% |
| `ask-until-clear/recurring-tasks` | with | 2 | 40 | 4 | 4,544 | 41,189 | 0.088 | 732 | 0 | 100% |
| `term-guard/credit-two-meanings-vi` | none | 2 | 42 | 4 | 6,714 | 60,319 | 0.135 | 326 | 5 | 25% |
| `term-guard/credit-two-meanings-vi` | with | 2 | 15 | 4 | 1,538 | 41,043 | 0.059 | 344 | 0 | 100% |
| `term-guard/loan-rule-vs-code` | none | 2 | 23 | 4 | 2,662 | 56,408 | 0.080 | 245 | 4 | 100% |
| `term-guard/loan-rule-vs-code` | with | 2 | 24 | 4 | 2,658 | 42,826 | 0.077 | 353 | 0 | 60% |
| `term-guard/promo-rounding-no-adr` | none | 2 | 18 | 6 | 1,954 | 60,534 | 0.063 | 173 | 2 | 100% |
| `term-guard/promo-rounding-no-adr` | with | 2 | 19 | 6 | 2,166 | 67,729 | 0.074 | 187 | 2 | 100% |
| `term-guard/tracking-id-ulid-adr` | none | 2 | 40 | 8 | 5,620 | 112,849 | 0.134 | 308 | 10 | 83% |
| `term-guard/tracking-id-ulid-adr` | with | 2 | 59 | 8 | 7,850 | 119,277 | 0.172 | 365 | 10 | 67% |
| `understand-this-code/empty-phone-shadowed` | none | 2 | 25 | 8 | 2,972 | 64,852 | 0.081 | 562 | 0 | 100% |
| `understand-this-code/empty-phone-shadowed` | with | 2 | 33 | 10 | 4,182 | 95,770 | 0.120 | 660 | 0 | 93% |
| `understand-this-code/legacy-sms-not-dead` | none | 2 | 8 | 5 | 871 | 35,559 | 0.039 | 130 | 2 | 83% |
| `understand-this-code/legacy-sms-not-dead` | with | 2 | 14 | 5 | 1,466 | 53,635 | 0.056 | 193 | 2 | 92% |
| `understand-this-code/per-line-rounding-why` | none | 2 | 14 | 4 | 1,360 | 49,851 | 0.062 | 384 | 0 | 79% |
| `understand-this-code/per-line-rounding-why` | with | 2 | 23 | 6 | 2,656 | 61,350 | 0.084 | 628 | 0 | 86% |
| `understand-this-code/rename-qty-field` | none | 2 | 13 | 6 | 1,104 | 59,412 | 0.052 | 140 | 5 | 83% |
| `understand-this-code/rename-qty-field` | with | 2 | 21 | 6 | 2,113 | 77,314 | 0.076 | 304 | 5 | 83% |
| `research/reminder-timeout-cap` | none | 2 | 10 | 3 | 1,094 | 23,503 | 0.039 | 172 | 0 | 100% |
| `research/reminder-timeout-cap` | with | 2 | 10 | 2 | 1,069 | 24,766 | 0.040 | 218 | 0 | 100% |
| `research/retry-front-or-back` | none | 2 | 77 | 11 | 7,052 | 181,518 | 0.172 | 318 | 1 | 83% |
| `research/retry-front-or-back` | with | 2 | 66 | 12 | 7,613 | 211,386 | 0.181 | 326 | 1 | 92% |
| `research/seed-after-bump` | none | 2 | 44 | 10 | 5,202 | 144,052 | 0.133 | 298 | 1 | 100% |
| `research/seed-after-bump` | with | 2 | 71 | 12 | 7,696 | 174,992 | 0.180 | 329 | 1 | 100% |
| `research/tar-filter-swap` | none | 2 | 88 | 12 | 10,812 | 282,003 | 0.251 | 366 | 2 | 100% |
| `research/tar-filter-swap` | with | 2 | 93 | 16 | 11,716 | 368,771 | 0.280 | 357 | 1 | 100% |
| `prototyping-designs/levels-btree-proposed` | none | 2 | 60 | 8 | 5,641 | 134,240 | 0.144 | 498 | 0 | 100% |
| `prototyping-designs/levels-btree-proposed` | with | 2 | 77 | 14 | 8,458 | 237,692 | 0.199 | 352 | 1 | 83% |
| `prototyping-designs/limiter-vague-vi` | none | 2 | 266 | 16 | 19,392 | 276,218 | 0.344 | 668 | 4 | 17% |
| `prototyping-designs/limiter-vague-vi` | with | 2 | 16 | 6 | 1,628 | 45,717 | 0.055 | 308 | 0 | 100% |
| `prototyping-designs/reopen-net-zero` | none | 2 | 148 | 6 | 4,148 | 106,986 | 0.107 | 532 | 0 | 100% |
| `prototyping-designs/reopen-net-zero` | with | 2 | 161 | 10 | 6,248 | 190,224 | 0.154 | 414 | 0 | 93% |
| `prototyping-designs/schedule-shape-decided` | none | 2 | 43 | 10 | 5,284 | 96,581 | 0.119 | 464 | 0 | 42% |
| `prototyping-designs/schedule-shape-decided` | with | 2 | 13 | 3 | 1,164 | 32,161 | 0.045 | 358 | 0 | 100% |
| `spec-it/court-waitlist-wording` | none | 2 | 41 | 5 | 4,886 | 77,752 | 0.114 | 277 | 4 | 50% |
| `spec-it/court-waitlist-wording` | with | 2 | 91 | 8 | 11,148 | 98,450 | 0.214 | 356 | 4 | 57% |
| `spec-it/invoice-csv-import` | none | 2 | 40 | 11 | 5,080 | 64,152 | 0.118 | 298 | 1 | 43% |
| `spec-it/invoice-csv-import` | with | 2 | 50 | 8 | 6,182 | 67,606 | 0.134 | 352 | 1 | 86% |
| `spec-it/parcel-webhook-retries` | none | 2 | 134 | 6 | 17,430 | 109,965 | 0.300 | 448 | 2 | 29% |
| `spec-it/parcel-webhook-retries` | with | 2 | 77 | 9 | 10,133 | 100,417 | 0.197 | 448 | 1 | 36% |
| `spec-it/pomo-weekly-gaps` | none | 2 | 52 | 6 | 6,308 | 66,899 | 0.139 | 366 | 1 | 14% |
| `spec-it/pomo-weekly-gaps` | with | 2 | 74 | 8 | 9,697 | 77,732 | 0.195 | 389 | 1 | 86% |
| `designing-architecture/invoice-vat-no-seam` | none | 2 | 83 | 6 | 10,200 | 74,465 | 0.201 | 478 | 1 | 83% |
| `designing-architecture/invoice-vat-no-seam` | with | 2 | 129 | 12 | 17,019 | 237,139 | 0.322 | 530 | 2 | 100% |
| `designing-architecture/partner-sync-rfc` | none | 2 | 65 | 11 | 8,084 | 81,203 | 0.161 | 404 | 2 | 14% |
| `designing-architecture/partner-sync-rfc` | with | 2 | 162 | 24 | 19,402 | 364,862 | 0.374 | 472 | 4 | 86% |
| `designing-architecture/quota-cli-go` | none | 2 | 89 | 7 | 10,677 | 76,690 | 0.194 | 349 | 2 | 93% |
| `designing-architecture/quota-cli-go` | with | 2 | 127 | 10 | 15,130 | 178,718 | 0.275 | 448 | 2 | 100% |
| `designing-architecture/shipping-refactor-vi` | none | 2 | 123 | 8 | 14,809 | 129,206 | 0.264 | 464 | 1 | 14% |
| `designing-architecture/shipping-refactor-vi` | with | 2 | 158 | 14 | 20,280 | 289,307 | 0.368 | 594 | 2 | 57% |
| `slicing-tickets/link-expiry-draft-arch` | none | 2 | 14 | 3 | 1,532 | 24,315 | 0.045 | 298 | 0 | 100% |
| `slicing-tickets/link-expiry-draft-arch` | with | 2 | 17 | 4 | 1,814 | 27,742 | 0.056 | 324 | 0 | 100% |
| `slicing-tickets/promo-recut-not-fixed` | none | 2 | 27 | 4 | 2,522 | 63,760 | 0.090 | 336 | 0 | 100% |
| `slicing-tickets/promo-recut-not-fixed` | with | 2 | 19 | 4 | 2,014 | 56,185 | 0.078 | 456 | 0 | 100% |
| `slicing-tickets/rename-tag-to-label` | none | 2 | 100 | 8 | 12,663 | 126,110 | 0.247 | 400 | 4 | 79% |
| `slicing-tickets/rename-tag-to-label` | with | 2 | 260 | 18 | 34,842 | 324,018 | 0.596 | 532 | 8 | 93% |
| `slicing-tickets/settle-up-cut` | none | 2 | 42 | 6 | 5,522 | 74,886 | 0.127 | 324 | 6 | 43% |
| `slicing-tickets/settle-up-cut` | with | 2 | 141 | 15 | 19,366 | 202,070 | 0.349 | 427 | 6 | 71% |
