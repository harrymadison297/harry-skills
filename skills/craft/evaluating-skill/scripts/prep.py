#!/usr/bin/env python3
"""Build blind run directories for an eval set.

usage: prep.py --evals evals/<skill> --skill skills/<group>/<skill> --out <scratch> [--configs with,none,old=<path>]

Writes <out>/w/<id>/work (the fixture, placed) and <out>/w/<id>/guide (the skill, for configs that have one),
<out>/blind/map.json (id -> case and config; never show it to an agent) and <out>/blind/prompts.json.
"""
import argparse, json, os, re, secrets, shutil, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('--evals', required=True)
p.add_argument('--skill', required=True)
p.add_argument('--out', required=True)
p.add_argument('--configs', default='with,none')
a = p.parse_args()
for k in ('evals', 'out', 'skill'):
    setattr(a, k, os.path.abspath(getattr(a, k)))

sources = {}
for c in a.configs.split(','):
    name, _, path = c.partition('=')
    sources[name] = a.skill if name == 'with' else (os.path.abspath(path) if path else None)
for name, path in sources.items():
    if name not in ('none',) and (not path or not os.path.isfile(os.path.join(path, 'SKILL.md'))):
        sys.exit(f"config {name}: no SKILL.md in {path}")

def request(case):
    text = open(f"{a.evals}/{case}/prompt.md").read().split('---', 2)[2].strip()
    return re.sub(r"\n\nInput files:.*$", "", text, flags=re.S)

os.makedirs(f"{a.out}/blind", exist_ok=True)
map_path = f"{a.out}/blind/map.json"
runs = json.load(open(map_path)) if os.path.exists(map_path) else {}
prompts = []
for case in sorted(os.listdir(a.evals)):
    if not os.path.isfile(f"{a.evals}/{case}/prompt.md"):
        continue
    for name, path in sources.items():
        rid = secrets.token_hex(4)
        base = f"{a.out}/w/{rid}"
        os.makedirs(f"{base}/work")
        subprocess.run(['bash', f"{a.evals}/{case}/place-files.sh"], cwd=f"{base}/work", check=True)
        lines = [f"I am working in {base}/work ."]
        if path:
            shutil.copytree(path, f"{base}/guide", ignore=shutil.ignore_patterns('evals', 'graders', '*.pyc'))
            lines.append(f"Use the instructions in {base}/guide/SKILL.md for this (read it first, and any file it links to).")
        lines.append(f'My request: "{request(case)}"')
        runs[rid] = {'case': case, 'config': name, 'base': base}
        prompts.append((rid, "\n\n".join(lines)))

json.dump(runs, open(map_path, 'w'), indent=1)
json.dump(prompts, open(f"{a.out}/blind/prompts.json", 'w'), indent=1)
for rid, _ in prompts:
    print(rid, runs[rid]['case'], runs[rid]['config'])
