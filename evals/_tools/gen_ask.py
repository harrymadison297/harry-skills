import os, textwrap
ROOT = '/home/cuongtc9/skills/skills/skills/ask-until-clear/evals'

def w(path, text, mode=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(text.lstrip('\n'))
    if mode: os.chmod(path, mode)

SETTINGS = """---
tags: [ask-until-clear]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

"""
PLACE = "#!/usr/bin/env bash\nset -eu\ncp -R \"$(dirname \"$0\")/files/.\" .\n"

COMMON = [
 ("01-restates-understanding", "The reply restates, in the assistant's own words, the goal, the user, and the problem it understood (a short preamble before the restatement is allowed), and invites the user to correct it. Summarizing the project files alone does not count."),
 ("02-challenges-premise", "The reply asks at least once whether this is the right problem to solve, or what happens if nothing is built."),
 ("03-numbered-with-recommendation", "The reply asks at least four numbered questions, and every numbered question has an explicit recommended answer or a stated assumption on its own line."),
 ("04-yes-accepts", "Every numbered question is a single decision phrased as a proposal or a yes/no question (not an either/or choice, and not an open 'what', 'which', or 'how many' question), so that a plain 'yes' accepts the recommended answer. A question about a fact only the user knows is allowed if the reply states an assumption that 'yes' accepts."),
 ("05-independent-questions", "No question in the round depends on the answer to another question in the same round."),
 ("06-reads-files-first", "The transcript shows the assistant reading project files before it writes its reply."),
 ("06b-question-names-a-file", "At least one numbered question names a specific file or a specific line of code from the project in its own text."),
 ("10-no-code-no-design", "The reply contains no code and no finished spec, and its recommended answers choose scope or behaviour without naming specific components, libraries, ports, protocols, or schema changes."),
 ("11-round-size", "The round has at most seven numbered questions."),
]

def grader(n, body):
    return f"---\ntype: llm\nfocus: trace\nweight: 1\n---\n\n{body}\n"

def case(name, prompt, outcome, specific, files):
    d = f"{ROOT}/{name}"
    names = ", ".join(sorted(p.split('/')[0] for p in files))
    w(f"{d}/prompt.md", SETTINGS + prompt.strip() + f"\n\nInput files: {names}\n")
    w(f"{d}/case.yaml", f'schema_version: "1.1"\nname: {name}\ncontext:\n  scaffold_script: place-files.sh\nexpected_outcome: |\n' + textwrap.indent(outcome.strip(), '  ') + "\n")
    w(f"{d}/place-files.sh", PLACE, 0o755)
    for fn, body in COMMON + specific:
        w(f"{d}/graders/{fn}.md", grader(fn, body))
    for p, t in files.items():
        w(f"{d}/files/{p}", t)

# ---------------- notes-offline-sync
case("notes-offline-sync",
"I want my notes app to work offline on my phone and sync with the laptop. Interview me before we write any spec. Ask your first round of questions and stop; I will answer after.",
"""The assistant restates the goal, challenges the premise, then asks one round of numbered, independent questions with recommended answers. It reads the code first and asks about the real problems in it (integer ids, hard deletes, last-write-wins), not about facts the code states.""",
[
 ("07-grounded-in-code", "At least one question is grounded in a specific finding in the code, such as the integer autoincrement ids in app/models.py (two offline devices would create colliding ids), the hard delete in app/routes.py (a deletion cannot be synced without a record of it), or the last-write-wins update."),
 ("08-does-not-ask-known-facts", "The reply does not ask the user for facts that the files already state, such as the web framework, the database, or whether notes belong to notebooks and tags."),
 ("09-covers-key-decisions", "The questions cover at least three of these decisions: what happens when the same note is edited on both devices; how a deletion on one device reaches the other; which data syncs (notes only, or also notebooks, tags, attachments); how devices identify themselves or sign in; whether sync is automatic or manual; how much data the offline copy must hold."),
],
{
"README.md": "# Notes\n\nA personal notes API. Flask + SQLite.\n\n    pip install -r requirements.txt\n    flask --app app run\n\nThe web client talks to this API. There is no mobile app yet.\n",
"requirements.txt": "flask\nflask-sqlalchemy\n",
"app/__init__.py": "from flask import Flask\nfrom .models import db\n\n\ndef create_app():\n    app = Flask(__name__)\n    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'\n    db.init_app(app)\n    from .routes import bp\n    app.register_blueprint(bp)\n    with app.app_context():\n        db.create_all()\n    return app\n",
"app/models.py": """from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

note_tags = db.Table(
    'note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)


class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    notes = db.relationship('Note', backref='notebook', cascade='all, delete-orphan')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='')
    body = db.Column(db.Text, default='')
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = db.relationship('Tag', secondary=note_tags, backref='notes')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
""",
"app/routes.py": """from flask import Blueprint, jsonify, request
from .models import db, Note

bp = Blueprint('notes', __name__)


@bp.get('/notes')
def list_notes():
    return jsonify([{'id': n.id, 'title': n.title, 'updated_at': n.updated_at.isoformat()} for n in Note.query.all()])


@bp.post('/notes')
def create_note():
    data = request.get_json()
    note = Note(title=data.get('title', ''), body=data.get('body', ''), notebook_id=data.get('notebook_id'))
    db.session.add(note)
    db.session.commit()
    return jsonify({'id': note.id}), 201


@bp.put('/notes/<int:note_id>')
def update_note(note_id):
    note = db.get_or_404(Note, note_id)
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.body = data.get('body', note.body)
    db.session.commit()
    return jsonify({'id': note.id})


@bp.delete('/notes/<int:note_id>')
def delete_note(note_id):
    note = db.get_or_404(Note, note_id)
    db.session.delete(note)
    db.session.commit()
    return '', 204
""",
})

# ---------------- esp32-battery-node
case("esp32-battery-node",
"The kitchen sensor node in this folder runs on USB power. I want it to run for months on a battery instead. Interview me before we write any spec. Ask your first round of questions and stop; I will answer after.",
"""The assistant restates the goal, challenges the premise, then asks one round of numbered, independent questions with recommended answers. It reads main.cpp first and asks about what the code makes hard (blocking Wi-Fi, a delay loop that never sleeps, no handling of failed publishes), and about decisions only the user can make (lifetime target, battery, behaviour when offline).""",
[
 ("07-grounded-in-code", "At least one question is grounded in a specific finding in src/main.cpp, such as the delay(10000) loop that never sleeps, the blocking Wi-Fi connect, the unchecked result of publish, or the fact that nothing survives a restart."),
 ("08-does-not-ask-known-facts", "The reply does not ask the user for facts that the files already state, such as the board (esp32dev), the sensor (DHT22), the pin, the framework (Arduino), or the protocol (MQTT)."),
 ("09-covers-key-decisions", "The questions cover at least three of these decisions: the target battery life and the battery's capacity or chemistry; how often to sample versus how often to report; what to do with samples when Wi-Fi or the broker is unavailable; what happens when the battery is low; how the firmware is updated without a cable; what besides a timer can wake the device; whether samples need real timestamps."),
],
{
"README.md": "# Kitchen node\n\nTemperature and humidity for the kitchen. Publishes to the home MQTT broker. Powered over USB today.\n",
"platformio.ini": "[env:esp32dev]\nplatform = espressif32\nboard = esp32dev\nframework = arduino\nmonitor_speed = 115200\nlib_deps =\n    adafruit/DHT sensor library\n    knolleary/PubSubClient\n",
"src/main.cpp": """#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHT_PIN 4
#define LED_PIN 2

const char* WIFI_SSID = "home";
const char* WIFI_PASS = "secret";
const char* MQTT_HOST = "192.168.1.10";

DHT dht(DHT_PIN, DHT22);
WiFiClient wifi;
PubSubClient mqtt(wifi);

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  mqtt.setServer(MQTT_HOST, 1883);
}

void loop() {
  if (!mqtt.connected()) {
    mqtt.connect("kitchen-node");
  }
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  char payload[64];
  snprintf(payload, sizeof(payload), "{\\"t\\":%.1f,\\"h\\":%.1f}", t, h);
  mqtt.publish("home/kitchen/climate", payload);
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);
  delay(10000);
}
""",
})

# ---------------- linux-zero-downtime-deploy
case("linux-zero-downtime-deploy",
"I want zero-downtime deploys of our app across our three Ubuntu servers. The deployment files are in this folder. Interview me before we write any spec. Ask your first round of questions and stop; I will answer after.",
"""The assistant restates the goal, challenges the premise, then asks one round of numbered, independent questions with recommended answers. It reads deploy.sh and the README first and asks about the real gaps (no health check, DNS round-robin with no load balancer, manual migrations, no previous release kept), not about facts the files state.""",
[
 ("07-grounded-in-code", "At least one question is grounded in a specific finding in the files, such as deploy.sh restarting the service on each host with no health check or draining, the DNS round-robin in the README with no load balancer, or migrations being run by hand."),
 ("08-does-not-ask-known-facts", "The reply does not ask the user for facts that the files already state, such as the operating system, the number of hosts, the host names, or that systemd runs the app."),
 ("09-covers-key-decisions", "The questions cover at least three of these decisions: how traffic is balanced and how a host leaves rotation during a deploy; how database migrations stay compatible with the old and the new version running together; how a rollback works; how long in-flight requests get to finish; how many hosts may be down at once; what triggers a deploy and who runs it; what counts as healthy."),
],
{
"README.md": "# Internal app\n\nRuns on three Ubuntu 22.04 VMs (web1, web2, web3). DNS round-robin sends users to any of them. Deploy with ./deploy.sh.\n\nDatabase changes: run migrations/ by hand on web1 before you deploy.\n",
"hosts": "web1\nweb2\nweb3\n",
"deploy.sh": "#!/usr/bin/env bash\nset -e\nfor host in $(cat hosts); do\n  rsync -az --delete ./app/ \"$host:/srv/app/\"\n  ssh \"$host\" 'sudo systemctl restart app'\ndone\n",
"app.service": "[Unit]\nDescription=Internal app\nAfter=network.target\n\n[Service]\nUser=app\nWorkingDirectory=/srv/app\nExecStart=/usr/bin/python3 /srv/app/server.py\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n",
"nginx.conf": "server {\n    listen 80;\n    location / {\n        proxy_pass http://127.0.0.1:8080;\n    }\n}\n",
"migrations/0001_init.sql": "CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT NOT NULL);\n",
"migrations/0002_add_email.sql": "ALTER TABLE users ADD COLUMN email TEXT;\n",
"app/server.py": "from http.server import BaseHTTPRequestHandler, HTTPServer\n\n\nclass H(BaseHTTPRequestHandler):\n    def do_GET(self):\n        self.send_response(200)\n        self.end_headers()\n        self.wfile.write(b'ok')\n\n\nHTTPServer(('127.0.0.1', 8080), H).serve_forever()\n",
})
print("ok")
