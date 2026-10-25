import os, textwrap
ROOT = '/home/cuongtc9/skills/skills/skills/term-guard/evals'

def w(path, text, mode=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(text.lstrip('\n'))
    if mode: os.chmod(path, mode)

SETTINGS = """---
tags: [term-guard]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

"""
PLACE = "#!/usr/bin/env bash\nset -eu\ncp -R \"$(dirname \"$0\")/files/.\" .\n"
PROMPT = ("conversation.md holds our discussion so far and this project is in the current directory. "
          "Reply to my last message the way you would in the conversation, and update the project's docs as the conversation calls for. "
          "Write your reply to reply.md.")

def grader(body):
    return f"---\ntype: llm\nfocus: trace\nweight: 1\n---\n\n{body}\n"

def common(path_glossary, adr_dir, n_existing):
    nxt = f"{n_existing+1:04d}"
    return [
     ("04-edits-glossary-at-pointed-path", f"Glossary changes are made in {path_glossary}, the path named in CLAUDE.md, and no GLOSSARY.md is created at the repo root."),
     ("05-entry-format", "Each new or changed glossary entry has a bold term, a definition of one or two sentences, and an _Avoid_ line listing the rejected synonyms."),
     ("06-no-implementation-details", "The glossary contains no implementation details: no file names, function names, library names, table names, or code."),
     ("07-no-general-programming-terms", "The glossary does not gain general programming terms (such as timeout, retry, JSON, queue, or cache); it only gains terms specific to this project."),
     ("08-one-adr-for-the-real-decision", f"Exactly one new ADR file is added in {adr_dir}, numbered {nxt}, for the decision that is hard to reverse, surprising, and a real trade-off. No ADR is written for the trivial decision."),
     ("09-adr-is-short", "The new ADR is one to three sentences stating the context, the decision, and why, with no filler and no template headings that add nothing."),
     ("10-leaves-other-entries-alone", "Existing glossary entries and existing ADRs are unchanged, except where the conversation changes a term on purpose."),
    ]

def case(name, outcome, specific, files, path_glossary, adr_dir, n_existing):
    d = f"{ROOT}/{name}"
    names = ", ".join(sorted(p.split('/')[0] for p in files))
    w(f"{d}/prompt.md", SETTINGS + PROMPT + f"\n\nInput files: {names}\n")
    w(f"{d}/case.yaml", f'schema_version: "1.1"\nname: {name}\ncontext:\n  scaffold_script: place-files.sh\nexpected_outcome: |\n' + textwrap.indent(outcome.strip(), '  ') + "\n")
    w(f"{d}/place-files.sh", PLACE, 0o755)
    for fn, body in specific + common(path_glossary, adr_dir, n_existing):
        w(f"{d}/graders/{fn}.md", grader(body))
    for p, t in files.items():
        w(f"{d}/files/{p}", t)

CLAUDE_MD = "# Project\n\n## Workflow files\n\n- Glossary: `docs/glossary.md`\n- ADRs: `docs/decisions/`\n"
ADR1 = "# {t}\n\n{b}\n"

# ---------------- notes
case("notes-folder-vs-notebook",
"""The assistant notices that the user says 'folder' and 'memo' where the glossary says Notebook and Note, notices that the code deletes a notebook's notes outright while the user expects a trash, and asks the user to settle what 'trash' means. It records the settled terms in docs/glossary.md and writes one ADR for the decision to use client-generated UUIDs, but none for the date format.""",
[
 ("01-flags-term-conflict", "The reply points out that the user's words 'folder' and 'memo' (or 'page') conflict with the glossary terms Notebook and Note, and proposes the glossary terms as the canonical ones."),
 ("02-surfaces-code-contradiction", "The reply points out that the code deletes a notebook's notes together with the notebook (cascade delete in the models), which contradicts the user's expectation that deleted items go to a trash for 30 days."),
 ("03-asks-instead-of-guessing", "The reply asks the user a question to settle the new term 'trash' (what it holds, or whether it is a notebook, a state, or a view) instead of silently inventing a definition."),
 ("04b-adds-settled-term", "docs/glossary.md gains an entry for Replica, defined as one device's full copy of the notes."),
],
{
"CLAUDE.md": CLAUDE_MD,
"docs/glossary.md": """# Notes

A personal notes app: people write notes, group them in notebooks, and label them with tags.

## Language

**Note**:
A piece of writing with a title and a body.
_Avoid_: Memo, page

**Notebook**:
A named collection that owns notes.
_Avoid_: Folder, binder

**Tag**:
A label that can be attached to many notes across notebooks.
_Avoid_: Label, category
""",
"docs/decisions/0001-sqlite-for-storage.md": ADR1.format(t="SQLite for storage", b="The app is single-user, so we store everything in one SQLite file. A server database would add operations work for no benefit."),
"docs/decisions/0002-rest-api-for-the-client.md": ADR1.format(t="REST API for the client", b="The web client talks to the server over a plain REST API, so any later client can use the same endpoints."),
"app/models.py": """from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    notes = db.relationship('Note', backref='notebook', cascade='all, delete-orphan')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='')
    body = db.Column(db.Text, default='')
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
""",
"conversation.md": """# Conversation so far

**User:** For offline sync, I decided that notes get their ids on the device as UUIDs. I do not want to ever migrate ids again, and two devices must never hand out the same id. I know the server database is simpler with integer ids, but I am choosing UUIDs.

**Assistant:** Understood, UUIDs created on the device.

**User:** Also, show every date in the UI as ISO 8601, I just prefer it.

**Assistant:** Noted.

**User:** One more word for the docs: a Replica is one device's full copy of the notes. Please use "Replica" for that from now on.

**Assistant:** Noted.

**User (latest message):** Now the delete behaviour. When someone deletes a folder, its memos should sit in a trash for 30 days before they are really gone, and a sync retry should give up after a 30 second timeout. A page can sit in many folders, like a tag really.
""",
}, "docs/glossary.md", "docs/decisions/", 2)

# ---------------- esp32
case("esp32-reading-vs-sample",
"""The assistant notices that the user says 'measurement' and 'message' where the glossary says Sample and Report, notices that the firmware keeps nothing across restarts and ignores a failed publish while the user believes unsent samples are kept, and asks the user what survives a power loss. It records the settled terms in docs/glossary.md and writes one ADR for buffering in RTC memory, but none for the LED blink.""",
[
 ("01-flags-term-conflict", "The reply points out that the user's words 'measurement' (or 'reading') and 'message' conflict with the glossary terms Sample and Report, and proposes the glossary terms as the canonical ones."),
 ("02-surfaces-code-contradiction", "The reply points out that the firmware keeps no unsent sample (nothing survives a restart, and the result of publish is ignored), which contradicts the user's belief that a sample is kept until the next successful report."),
 ("03-asks-instead-of-guessing", "The reply asks the user whether 'next boot' (a restart after power loss) and a wake-up from sleep are the same event, or otherwise asks what survives each, instead of silently choosing."),
 ("04b-adds-settled-term", "docs/glossary.md gains an entry for Cycle, defined as one wake-up in which the node takes a sample, tries to report it, and goes back to sleep."),
],
{
"CLAUDE.md": CLAUDE_MD,
"docs/glossary.md": """# Kitchen node

Firmware for a battery sensor node that measures temperature and humidity and reports them to a home broker.

## Language

**Sample**:
One reading of temperature and humidity taken from the sensor.
_Avoid_: Measurement, reading, datapoint

**Report**:
One delivery of one or more samples to the broker.
_Avoid_: Message, upload, publish
""",
"docs/decisions/0001-arduino-framework.md": ADR1.format(t="Arduino framework on PlatformIO", b="We use the Arduino framework on PlatformIO because the sensor and MQTT libraries we need already exist for it."),
"docs/decisions/0002-mqtt-to-the-home-broker.md": ADR1.format(t="MQTT to the home broker", b="Samples go to the home MQTT broker, which the rest of the house already reads."),
"src/main.cpp": """#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

DHT dht(4, DHT22);
WiFiClient wifi;
PubSubClient mqtt(wifi);

void setup() {
  dht.begin();
  WiFi.begin("home", "secret");
  while (WiFi.status() != WL_CONNECTED) delay(500);
  mqtt.setServer("192.168.1.10", 1883);
}

void loop() {
  if (!mqtt.connected()) mqtt.connect("kitchen-node");
  char payload[64];
  snprintf(payload, sizeof(payload), "{\\"t\\":%.1f,\\"h\\":%.1f}", dht.readTemperature(), dht.readHumidity());
  mqtt.publish("home/kitchen/climate", payload);
  delay(10000);
}
""",
"conversation.md": """# Conversation so far

**User:** The node will sleep between cycles. We decided: unsent samples are kept in RTC memory, not written to flash. That means they are lost if power is cut, and I accept that, because flash wears out and the node reports often. I know writing to flash would be safer, but I am choosing RTC memory.

**Assistant:** Understood, unsent samples go to RTC memory.

**User:** Also make the LED blink once on every report, just so I can see it work.

**Assistant:** Noted.

**User:** One more word for the docs: a Cycle is one wake-up, where the node takes a sample, tries to report it, and goes back to sleep. Please use "Cycle" for that from now on.

**Assistant:** Noted.

**User (latest message):** Each time it wakes up it takes a measurement and sends the message, and if the Wi-Fi is down it just keeps the reading until the next boot, then retries with a 5 second timeout.
""",
}, "docs/glossary.md", "docs/decisions/", 2)

# ---------------- deploy
case("deploy-release-vs-rollout",
"""The assistant notices that the user says 'push', 'server', and 'node' where the glossary says Deploy and Host, notices that 'rollout' is on the Avoid list but the user means the whole sequence across hosts, notices that deploy.sh overwrites the app in place so no previous release exists to roll back to, and asks the user what 'rollout' should mean. It records the settled terms in docs/glossary.md and writes one ADR for release directories with an atomic symlink, but none for the log timestamps.""",
[
 ("01-flags-term-conflict", "The reply points out that the user's words 'push' and 'server' or 'node' conflict with the glossary terms Deploy and Host, and proposes the glossary terms as the canonical ones."),
 ("02-surfaces-code-contradiction", "The reply points out that deploy.sh overwrites /srv/app in place with rsync and keeps no previous release, which contradicts the user's claim that a rollback is just deploying the previous release."),
 ("03-asks-instead-of-guessing", "The reply asks the user whether 'rollout' means one deploy or the whole sequence of deploys across hosts (a term currently on the Avoid list), instead of silently choosing."),
 ("04b-adds-settled-term", "docs/glossary.md gains an entry for Rollback, defined as deploying an earlier release again on a host."),
],
{
"CLAUDE.md": CLAUDE_MD,
"docs/glossary.md": """# Internal app deployment

How the internal app reaches its servers.

## Language

**Release**:
An immutable, versioned build of the app.
_Avoid_: Version, package, build

**Deploy**:
Making one release the running version on one host.
_Avoid_: Push, rollout, ship

**Host**:
A virtual machine that runs the app.
_Avoid_: Node, server, box
""",
"docs/decisions/0001-systemd-supervises-the-app.md": ADR1.format(t="systemd supervises the app", b="The app runs as a systemd service, so it restarts on failure without extra tooling."),
"docs/decisions/0002-dns-round-robin.md": ADR1.format(t="DNS round-robin across hosts", b="Users reach the hosts through DNS round-robin, because we have no load balancer and three hosts do not justify one yet."),
"deploy.sh": "#!/usr/bin/env bash\nset -e\nfor host in $(cat hosts); do\n  rsync -az --delete ./app/ \"$host:/srv/app/\"\n  ssh \"$host\" 'sudo systemctl restart app'\ndone\n",
"hosts": "web1\nweb2\nweb3\n",
"conversation.md": """# Conversation so far

**User:** We decided how releases are stored: each release goes in its own directory under /srv/app/releases/<id>, and a symlink called current points at the live one, switched atomically. We keep the last five. I know rsync over one directory is simpler, but I am choosing release directories so a rollback is instant.

**Assistant:** Understood, release directories with an atomic symlink.

**User:** Also put a timestamp on every line of the deploy log.

**Assistant:** Noted.

**User:** One more word for the docs: a Rollback is deploying an earlier release again on a host. Please use "Rollback" for that from now on.

**Assistant:** Noted.

**User (latest message):** When we push a new version it should roll out to each server one node at a time, and a rollback is just deploying the previous release. The health check gets a 10 second timeout.
""",
}, "docs/glossary.md", "docs/decisions/", 2)
print("ok")
