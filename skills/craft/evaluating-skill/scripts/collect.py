#!/usr/bin/env python3
"""Build one folder per finished run for a grader, and flag leaks and leftovers.

usage: collect.py --evals evals/<skill> --out <scratch> --tasks <dir of subagent *.output transcripts> --tag <name>

Writes <out>/g/<tag>/<case>/<config>/{reply.md, transcript.md, project/, graders/*.sh, assertions.json}.
"""
import argparse, glob, json, os, re, shutil

p = argparse.ArgumentParser()
p.add_argument('--evals', required=True)
p.add_argument('--out', required=True)
p.add_argument('--tasks', required=True)
p.add_argument('--tag', required=True)
a = p.parse_args()
for k in ('evals', 'out', 'tasks'):
    setattr(a, k, os.path.abspath(getattr(a, k)))

runs = json.load(open(f"{a.out}/blind/map.json"))
found = {}
for f in glob.glob(f"{a.tasks}/*.output"):
    head = open(f, errors='ignore').read(6000)
    m = re.search(r"/w/([0-9a-f]{8})/", head)
    if m and m.group(1) in runs:
        found[m.group(1)] = f
print(len(found), "transcripts matched of", len(runs))

def assertions(case):
    items = []
    for g in sorted(glob.glob(f"{a.evals}/{case}/graders/*.md")):
        script = g[:-3] + '.sh'
        items.append({'text': open(g).read().split('---', 2)[2].strip(),
                      'script': 'graders/' + os.path.basename(script) if os.path.exists(script) else None})
    return items

leaks = []
evals_root = os.path.dirname(a.evals)  # a run that names this path went looking for the real eval folders
for rid, f in found.items():
    r = runs[rid]
    d = f"{a.out}/g/{a.tag}/{r['case']}/{r['config']}"
    os.makedirs(d, exist_ok=True)
    shutil.copytree(r['base'] + '/work', d + '/project', dirs_exist_ok=True, symlinks=True)
    calls, reply = ["# Tool calls in order\n"], ""
    for raw in open(f, errors='ignore'):
        try:
            event = json.loads(raw)
        except ValueError:
            continue
        msg = event.get('message', event)
        content = msg.get('content') if isinstance(msg, dict) else None
        if not (isinstance(msg, dict) and msg.get('role') == 'assistant' and isinstance(content, list)):
            continue
        uses = [x for x in content if x.get('type') == 'tool_use']
        for x in uses:
            if 'Handback' in (x.get('name') or ''):
                reply = x.get('input', {}).get('message', reply)
            else:
                calls.append(f"- {x.get('name')}: {json.dumps(x.get('input', {}))[:400]}")
        texts = [x.get('text', '') for x in content if x.get('type') == 'text']
        if texts and not reply and not any('Handback' in (x.get('name') or '') for x in uses):
            reply = "\n".join(texts)
    transcript = "\n".join(calls) + "\n"
    open(d + '/transcript.md', 'w').write(transcript)
    open(d + '/reply.md', 'w').write(reply)
    request = open(f"{a.evals}/{r['case']}/prompt.md").read().split('---', 2)[2].strip()
    os.makedirs(d + '/graders', exist_ok=True)
    for sh in glob.glob(f"{a.evals}/{r['case']}/graders/*.sh"):
        shutil.copy(sh, d + '/graders/')
    json.dump({'request': request, 'assertions': assertions(r['case']),
               'original_files': f"{a.evals}/{r['case']}/files"}, open(d + '/assertions.json', 'w'), indent=1)
    if evals_root in transcript:
        leaks.append(f"{r['case']}/{r['config']}")

print("transcripts that named the real eval folder:", leaks or "none")
runroot = os.path.realpath(f"{a.out}/w")
for pid in filter(str.isdigit, os.listdir('/proc')):
    try:
        cwd = os.readlink(f"/proc/{pid}/cwd")
        if cwd.startswith(runroot):
            cmd = open(f"/proc/{pid}/cmdline").read().replace('\0', ' ')
            print(f"still running: pid {pid} in {cwd}: {cmd}")
    except OSError:
        pass
