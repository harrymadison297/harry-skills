import os, shutil, textwrap
SRC='/home/cuongtc9/skills/skills/skills/ask-until-clear/evals'
ROOT='/home/cuongtc9/skills/skills/skills/spec-it/evals'
def w(path,text,mode=None):
    os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w').write(text.lstrip('\n'))
    if mode: os.chmod(path,mode)
SETTINGS="---\ntags: [spec-it]\nmax_turns: 25\ntimeout_seconds: 600\nallowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]\n---\n\n"
PLACE="#!/usr/bin/env bash\nset -eu\ncp -R \"$(dirname \"$0\")/files/.\" .\n"
CLAUDE="# Project\n\n## Workflow files\n\n- Glossary: `docs/glossary.md`\n- ADRs: `docs/decisions/`\n"
def adr(t,b): return f"# {t}\n\n{b}\n"
def g(body): return f"---\ntype: llm\nfocus: trace\nweight: 1\n---\n\n{body}\n"

def common(feature):
    return [
     ("01-spec-file-draft", f"A file docs/features/{feature}/spec.md exists, and it contains the line 'Status: draft'."),
     ("02-journeys-with-test-paths", "The spec has at least two journeys, and each has numbered test paths in the form J1.1, J1.2."),
     ("03-check-line-per-test-path", "Every test path has a Check line that names a real surface (CLI, API, browser, or device), an environment, and what is observed."),
     ("04-numbered-criteria", "The acceptance criteria are numbered AC1, AC2, and so on, each names a test path, and each can pass or fail."),
     ("05-no-subjective-criteria", "No criterion relies on a subjective word (such as fast, quick, accurate, reliable, or smooth) without a number or threshold."),
     ("06-non-goals", "A Non-goals section lists what the interview ruled out."),
     ("08-gap-is-an-open-question", "The one question the interview never settled appears under Open questions together with a recommended answer, and the rest of the spec does not state an invented answer to it."),
     ("09-vague-requirement-handled", "The vague requirement from the interview is either given a measurable threshold that the interview supports, or put under Open questions with a recommended number. It is not left as a subjective criterion."),
     ("10-behaviour-not-design", "The journeys and criteria describe behaviour only. They name no tables, columns, ports, libraries, protocols, or file paths."),
     ("11-glossary-words", "The spec uses the glossary's terms and none of the words the glossary says to avoid."),
     ("12-does-not-interview", "The reply does not start a new interview. Its only questions are the entries under Open questions."),
     ("13-touches-only-the-spec", "Only the spec file is added; no code and no other project file is changed."),
    ]

def case(name, feature, outcome, specific, files, interview):
    d=f"{ROOT}/{name}"
    prompt=f"The interview is in docs/interview.md and the project is in the current directory. Write the spec for the feature '{feature}', in docs/features/{feature}/spec.md. Reply with a short note on what you wrote and anything that still needs my answer."
    w(f"{d}/prompt.md", SETTINGS+prompt+"\n\nInput files: CLAUDE.md, docs, and the project files\n")
    w(f"{d}/case.yaml", f'schema_version: "1.1"\nname: {name}\ncontext:\n  scaffold_script: place-files.sh\nexpected_outcome: |\n'+textwrap.indent(outcome.strip(),'  ')+"\n")
    w(f"{d}/place-files.sh", PLACE, 0o755)
    for fn,body in common(feature)[:6]+specific+common(feature)[6:]:
        w(f"{d}/graders/{fn}.md", g(body))
    src=f"{SRC}/{files}/files"
    shutil.copytree(src, f"{d}/files", dirs_exist_ok=True)
    for p,t in interview['extra'].items(): w(f"{d}/files/{p}", t)
    w(f"{d}/files/docs/interview.md", interview['text'])

# ---------- notes
case("spec-notes-offline-sync","offline-sync",
"""A spec.md with journeys such as editing offline, a conflict, and a delete, each test path with a Check line. Decisions record the answered items. Retention of deleted notes, which was never settled, is an open question with a recommendation, and 'sync should feel fast' becomes a measured threshold or an open question.""",
[
 ("07-decisions-captured","The Decisions section records at least five of these settled items, each with a reason: the phone uses the existing web client offline; the server is always reachable; v1 syncs notes only; a conflict keeps both versions with the older one as a separate note; a delete syncs and wins over an older edit; notes get ids on the device; sync runs automatically; one user with one token."),
],
"notes-offline-sync",
{'extra':{
 "CLAUDE.md":CLAUDE,
 "docs/glossary.md":"# Notes\n\nA personal notes app: people write notes, group them in notebooks, and label them with tags.\n\n## Language\n\n**Note**:\nA piece of writing with a title and a body.\n_Avoid_: Memo, page\n\n**Notebook**:\nA named collection that owns notes.\n_Avoid_: Folder, binder\n\n**Tag**:\nA label that can be attached to many notes across notebooks.\n_Avoid_: Label, category\n\n**Replica**:\nOne device's full copy of the notes.\n_Avoid_: Mirror, copy\n\n**Conflict copy**:\nThe older version, kept as a separate note when two replicas edited the same note.\n_Avoid_: Duplicate, backup\n",
 "docs/decisions/0001-sqlite-for-storage.md":adr("SQLite for storage","The app is single-user, so everything lives in one SQLite file."),
 "docs/decisions/0002-device-generated-ids.md":adr("Device-generated note ids","Notes get UUIDs created on the device, so two replicas never hand out the same id. Server-assigned integers were rejected because an offline replica cannot get one."),
 },
 'text':"""# Interview: offline sync

Round 1 (answered by the user)

**Q1 Is offline sync worth building, instead of making the notes reachable from anywhere?**
Yes. I need to edit with no signal, on a train, and see it on the laptop later.

**Q2 Should the phone use the existing web client, working offline, and not a new native app?**
Yes. One client for both.

**Q3 Should the notes live on a server that both devices can reach, and not only on the laptop?**
Yes. The laptop is often asleep.

**Q4 Should v1 sync only notes (title and body), with notebooks and tags still needing a connection?**
Yes.

**Q5 If the same note is edited on both replicas before they sync, should both versions be kept, the older as a conflict copy?**
Yes. I never want to lose text.

**Q6 Should a delete on one replica delete the note on the other, with a delete winning over an older edit and a newer edit bringing the note back?**
Yes.

**Q7 Should sync run on its own whenever the phone is online?**
Yes, and it should feel fast. I do not want to press a button.

**Q8 Is one user with one login token enough?**
Yes.

Held back, never asked: how long a deleted note is remembered before it can be forgotten.
"""})

# ---------- esp32
case("spec-esp32-battery-node","battery-node",
"""A spec.md with journeys such as a normal cycle, a network outage, and a low battery report, each test path with a Check line. Decisions record the answered items. Low-battery behaviour, which was never settled, is an open question with a recommendation, and 'readings should be accurate' becomes a measured threshold or an open question.""",
[
 ("07-decisions-captured","The Decisions section records at least five of these settled items, each with a reason: the node needs a battery because there is no outlet; it reports every five minutes; a battery should last at least six months; when the network is down it gives up after about ten seconds and sleeps; it never queues old samples; the topic and the t and h fields stay unchanged; it reports its battery level in each report; the firmware is updated over USB only; the LED does not blink in normal operation."),
],
"esp32-battery-node",
{'extra':{
 "CLAUDE.md":CLAUDE,
 "docs/glossary.md":"# Kitchen node\n\nFirmware for a battery sensor node that measures temperature and humidity and reports them to a home broker.\n\n## Language\n\n**Sample**:\nOne reading of temperature and humidity taken from the sensor.\n_Avoid_: Measurement, reading, datapoint\n\n**Report**:\nOne delivery of one or more samples to the broker.\n_Avoid_: Message, upload, publish\n\n**Cycle**:\nOne wake-up in which the node takes a sample, tries to report it, and goes back to sleep.\n_Avoid_: Loop, tick\n",
 "docs/decisions/0001-arduino-framework.md":adr("Arduino framework on PlatformIO","We use the Arduino framework on PlatformIO because the sensor and MQTT libraries we need already exist for it."),
 "docs/decisions/0002-mqtt-to-the-home-broker.md":adr("MQTT to the home broker","Reports go to the home MQTT broker, which the rest of the house already reads."),
 },
 'text':"""# Interview: battery node

Round 1 (answered by the user)

**Q1 Is a battery worth it, instead of a longer USB cable?**
Yes. There is no outlet where the node has to sit.

**Q2 Should the node run one cycle every five minutes?**
Yes.

**Q3 Should one battery last at least six months?**
Yes.

**Q4 Should the node give up after about ten seconds when the network is down, skip that report, and sleep until the next cycle, with no queue of old samples?**
Yes. A lost sample now and then is fine.

**Q5 Should every report also carry the battery level?**
Yes.

**Q6 Should the topic and the t and h fields stay exactly as they are?**
Yes. Home Assistant reads them.

**Q7 Should the firmware be updated over USB only, with no over-the-air update?**
Yes.

**Q8 Should the LED stay off during normal operation?**
Yes.

Extra remark from the user: the readings should be accurate.

Held back, never asked: what the node should do when the battery is nearly empty.
"""})

# ---------- deploy
case("spec-zero-downtime-deploy","zero-downtime-deploy",
"""A spec.md with journeys such as a normal deploy, a failing host, and a rollback, each test path with a Check line. Decisions record the answered items. How many past releases to keep, which was never settled, is an open question with a recommendation, and 'deploys should be quick' becomes a measured threshold or an open question.""",
[
 ("07-decisions-captured","The Decisions section records at least five of these settled items, each with a reason: people use the app during the day; zero downtime means no user-visible failed request in a normal deploy; requests in flight get thirty seconds to finish; DNS round-robin stays with no new load balancer; hosts are deployed one at a time and the deploy stops at the first unhealthy host; migrations must work with the previous release and run once before the first host; one command rolls all hosts back; a host counts as updated only after it answers a health request; a person runs deploys by hand."),
],
"linux-zero-downtime-deploy",
{'extra':{
 "CLAUDE.md":CLAUDE,
 "docs/glossary.md":"# Internal app deployment\n\nHow the internal app reaches its servers.\n\n## Language\n\n**Release**:\nAn immutable, versioned build of the app.\n_Avoid_: Version, package, build\n\n**Deploy**:\nMaking one release the running version on one host.\n_Avoid_: Push, ship\n\n**Rollout**:\nOne release going through all hosts, one deploy after another.\n_Avoid_: Wave, batch\n\n**Rollback**:\nDeploying an earlier release again on a host.\n_Avoid_: Revert, undo\n\n**Host**:\nA virtual machine that runs the app.\n_Avoid_: Node, server, box\n",
 "docs/decisions/0001-systemd-supervises-the-app.md":adr("systemd supervises the app","The app runs as a systemd service, so it restarts on failure without extra tooling."),
 "docs/decisions/0002-dns-round-robin.md":adr("DNS round-robin across hosts","Users reach the hosts through DNS round-robin, because three hosts do not justify a load balancer yet."),
 },
 'text':"""# Interview: zero-downtime deploys

Round 1 (answered by the user)

**Q1 Is this worth solving, or can deploys wait for quiet hours?**
Worth solving. People use the app all day.

**Q2 Should zero downtime mean no user-visible failed request in a normal deploy, with in-flight requests getting thirty seconds to finish?**
Yes.

**Q3 Should DNS round-robin stay, with no new load balancer?**
Yes.

**Q4 Should a rollout deploy one host at a time and stop at the first host that is not healthy, putting that host back on the previous release?**
Yes.

**Q5 Should every migration work with the previous release too, and run once, before the first host?**
Yes.

**Q6 Should one command return all three hosts to the last good release?**
Yes.

**Q7 Should a host count as updated only after it answers a health request?**
Yes.

**Q8 Should a person keep running deploys by hand from one machine, with no CI?**
Yes.

Extra remark from the user: deploys should be quick.

Held back, never asked: how many past releases to keep on each host.
"""})
print("ok")
