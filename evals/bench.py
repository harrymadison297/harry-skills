#!/usr/bin/env python3
"""Benchmark the plan skills on one tested model, with the skill vs. without it.

Measures wall time, time to first token, turns, tokens, cost, response style and assertion pass rate.

  bench.py plugin --out DIR                      build DIR/plugin (only the plan skills)
  bench.py probe  --out DIR                      fixed cost of having the plugin installed (no skill called)
  bench.py run    --out DIR [--skills a,b] [--reps 2] [--jobs 4]
  bench.py grade  --out DIR [--skills a,b]       script graders + an Opus grader for the llm ones
  bench.py style  --out DIR [--skills a,b]       Opus compares each with/none reply pair
  bench.py report --out DIR --md FILE --json FILE

Cases live in evals/<skill>/<case>/ (see skills/craft/evaluating-skill/references/case-format.md).
Both configs run `claude -p` in a fresh copy of the case project, with settings, MCP servers and the
parent session's environment stripped, so the only difference between them is the plugin and the
slash command that calls the skill:
  none  prompt = the request                       no plugin
  with  prompt = /harry-skills:<skill> <request>   plugin = the plan skills
"""
import argparse, concurrent.futures as cf, glob, json, os, random, re, secrets, shutil, signal, statistics
import subprocess, sys, threading, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(REPO, 'evals')
PLAN = ['ask-until-clear', 'term-guard', 'understand-this-code', 'research',
        'prototyping-designs', 'spec-it', 'designing-architecture', 'slicing-tickets']
KEEP_ENV = {'CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST', 'CLAUDE_CODE_ORGANIZATION_UUID',
            'CLAUDE_CODE_ACCOUNT_UUID', 'CLAUDE_SESSION_INGRESS_TOKEN_FILE'}


def clean_env():
    env = {k: v for k, v in os.environ.items() if k in KEEP_ENV or not k.startswith('CLAUDE')}
    env['CLAUDE_CODE_ENTRYPOINT'] = 'sdk-cli'
    env.pop('CCR_ENABLE_TRACING', None)
    return env


def sh(cmd, cwd, timeout=60):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)


def parse_prompt(path):
    head, request = open(path).read().split('---', 2)[1:]
    tools = re.search(r'allowed_tools:\s*\[(.*?)\]', head)
    wall = re.search(r'timeout_seconds:\s*(\d+)', head)
    return {'tools': [t.strip() for t in tools.group(1).split(',')] if tools else ['Read', 'Glob', 'Grep', 'Write', 'Edit', 'Bash'],
            'timeout': int(wall.group(1)) if wall else 900}, request.strip()


def cases_of(skill):
    return sorted(d for d in os.listdir(f'{EVALS}/{skill}') if os.path.isfile(f'{EVALS}/{skill}/{d}/prompt.md')) \
        if os.path.isdir(f'{EVALS}/{skill}') else []


def load_events(rid, out):
    path = f'{out}/runs/{rid}/events.jsonl'
    return [json.loads(l) for l in open(path)] if os.path.exists(path) else []


def all_runs(out):
    runs = []
    for p in glob.glob(f'{out}/runs/*/meta.json'):
        runs.append(json.load(open(p)))
    return runs


# ---------------------------------------------------------------- plugin / probe

def cmd_plugin(a):
    root = f'{a.out}/plugin'
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(f'{root}/.claude-plugin')
    for s in PLAN:
        shutil.copytree(f'{REPO}/skills/plan/{s}', f'{root}/skills/{s}', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    json.dump({'name': 'harry-skills', 'version': '0.0.0', 'description': 'plan skills',
               'skills': [f'./skills/{s}' for s in PLAN]}, open(f'{root}/.claude-plugin/plugin.json', 'w'))
    print('plugin at', root)


def claude_cmd(a, prompt, config, tools):
    cmd = ['claude', '-p', prompt, '--model', a.model, '--effort', a.effort, '--output-format', 'stream-json', '--verbose',
           '--no-session-persistence', '--setting-sources', 'project', '--strict-mcp-config',
           '--permission-mode', 'bypassPermissions', '--max-budget-usd', str(a.budget), '--tools', ','.join(tools + ['Skill'])]
    if config == 'with':
        cmd += ['--plugin-dir', f'{a.out}/plugin']
    return cmd


def stream(cmd, cwd, timeout):
    """Run cmd, stamp every stdout line with seconds since start. Returns (events, wall_s, rc, timed_out, stderr)."""
    t0 = time.monotonic()
    err = open(os.path.join(cwd, '..', 'stderr.txt'), 'w')
    p = subprocess.Popen(cmd, cwd=cwd, env=clean_env(), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=err,
                         text=True, start_new_session=True)
    timed_out = []

    def kill():
        timed_out.append(1)
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
    timer = threading.Timer(timeout, kill)
    timer.start()
    events = []
    for line in p.stdout:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        e['_t'] = round(time.monotonic() - t0, 3)
        if e.get('type') == 'stream_event':
            events.append({'type': 'stream_event', '_t': e['_t']})  # keep only the arrival time
        else:
            events.append(e)
    rc = p.wait()
    timer.cancel()
    wall = time.monotonic() - t0
    try:
        os.killpg(p.pid, signal.SIGKILL)  # anything the run left behind
    except OSError:
        pass
    return events, wall, rc, bool(timed_out)


def cmd_probe(a):
    cmd_plugin(a)
    rows = []
    for config in ('none', 'with', 'none', 'with', 'none', 'with'):
        base = f'{a.out}/probe/{secrets.token_hex(3)}'
        os.makedirs(f'{base}/work')
        events, wall, rc, _ = stream(claude_cmd(a, 'Reply with exactly: pong', config, ['Read', 'Bash']), f'{base}/work', 120)
        m = metrics(events, {'wall_s': wall})
        rows.append({'config': config, **{k: m[k] for k in ('first_ctx', 'in_total', 'out', 'cost', 'ttft_ms', 'wall_s')}})
        print(rows[-1])
    json.dump(rows, open(f'{a.out}/probe.json', 'w'), indent=1)


# ---------------------------------------------------------------- run

def run_job(a, job):
    skill, case, rep, config = job
    rid = secrets.token_hex(4)
    base = f'{a.out}/w/{rid}'
    work = f'{base}/work'
    os.makedirs(work)
    cdir = f'{EVALS}/{skill}/{case}'
    sh(['bash', f'{cdir}/place-files.sh'], work)
    fm, request = parse_prompt(f'{cdir}/prompt.md')
    prompt = request if config == 'none' else f'/harry-skills:{skill} {request}'
    events, wall, rc, timed_out = stream(claude_cmd(a, prompt, config, fm['tools']), work, min(fm['timeout'], a.max_wall))
    os.makedirs(f'{a.out}/runs/{rid}')
    with open(f'{a.out}/runs/{rid}/events.jsonl', 'w') as f:
        for e in events:
            f.write(json.dumps(e) + '\n')
    files = []
    for line in sh(['git', 'status', '--porcelain', '-uall'], work).stdout.splitlines():
        path = line[3:].strip().strip('"')
        full = os.path.join(work, path)
        if os.path.isfile(full) and '__pycache__' not in path and not path.endswith('.pyc'):
            files.append({'path': path, 'status': line[:2].strip(), 'bytes': os.path.getsize(full)})
    blob = json.dumps(events)
    meta = {'rid': rid, 'skill': skill, 'case': case, 'rep': rep, 'config': config, 'model': a.model, 'effort': a.effort,
            'wall_s': round(wall, 2), 'rc': rc, 'timed_out': timed_out, 'files': files,
            'leak': (REPO + '/evals') in blob or 'harry-skills/evals' in blob, 'jobs': a.jobs}
    json.dump(meta, open(f'{a.out}/runs/{rid}/meta.json', 'w'), indent=1)
    res = next((e for e in reversed(events) if e.get('type') == 'result'), {})
    print(f"{skill}/{case} r{rep} {config}: {wall:.0f}s turns={res.get('num_turns')} cost={res.get('total_cost_usd')} rc={rc}"
          + (' TIMEOUT' if timed_out else ''), flush=True)


def cmd_run(a):
    if not os.path.isdir(f'{a.out}/plugin'):
        cmd_plugin(a)
    done = {(m['skill'], m['case'], m['rep'], m['config']) for m in all_runs(a.out) if m['rc'] == 0 and not m['timed_out']}
    rng = random.Random(7)
    jobs = []
    for skill in a.skills.split(','):
        for case in cases_of(skill):
            for rep in range(a.reps):
                pair = ['none', 'with']
                rng.shuffle(pair)  # neighbours in the queue run side by side, in a random order
                jobs += [(skill, case, rep, c) for c in pair if (skill, case, rep, c) not in done]
    print(len(jobs), 'runs to do on', a.model, 'effort', a.effort, 'jobs', a.jobs, flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for f in cf.as_completed([ex.submit(run_job, a, j) for j in jobs]):
            f.result()


# ---------------------------------------------------------------- metrics

EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿⭐✅❌]')
VI = re.compile('[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]', re.I)


def style_of(text):
    lines = text.splitlines()
    return {'words': len(text.split()), 'chars': len(text), 'lines': len([l for l in lines if l.strip()]),
            'headings': sum(1 for l in lines if re.match(r'\s*#{1,6}\s', l)),
            'bullets': sum(1 for l in lines if re.match(r'\s*([-*•]|\d+[.)])\s', l)),
            'table_rows': sum(1 for l in lines if l.strip().startswith('|')),
            'code_blocks': text.count('```') // 2, 'bold': text.count('**') // 2,
            'question_lines': sum(1 for l in lines if '?' in l), 'emoji': len(EMOJI.findall(text)),
            'vi_ratio': round(len(VI.findall(text)) / max(1, len(re.findall(r'[A-Za-zÀ-ỹ]', text))), 3)}


def metrics(events, meta):
    res = next((e for e in reversed(events) if e.get('type') == 'result'), {})
    u = res.get('usage') or {}
    m = {'duration_ms': res.get('duration_ms'), 'api_ms': res.get('duration_api_ms'), 'ttft_ms': res.get('ttft_ms'),
         'turns': res.get('num_turns'), 'cost': res.get('total_cost_usd'), 'is_error': bool(res.get('is_error', True)),
         'terminal': res.get('terminal_reason'), 'wall_s': meta.get('wall_s'),
         'in_fresh': u.get('input_tokens', 0), 'cache_create': u.get('cache_creation_input_tokens', 0),
         'cache_read': u.get('cache_read_input_tokens', 0), 'out': u.get('output_tokens', 0),
         'think': (u.get('output_tokens_details') or {}).get('thinking_tokens')}
    m['in_total'] = m['in_fresh'] + m['cache_create'] + m['cache_read']
    calls, tools, skills, narration, first = {}, {}, [], 0, {}
    for e in events:
        if e.get('type') != 'assistant':
            continue
        msg = e['message']
        mu = msg.get('usage') or {}
        calls[msg['id']] = mu.get('input_tokens', 0) + mu.get('cache_creation_input_tokens', 0) + mu.get('cache_read_input_tokens', 0)
        for c in msg.get('content', []):
            first.setdefault(c['type'], e['_t'])
            if c['type'] == 'tool_use':
                tools[c['name']] = tools.get(c['name'], 0) + 1
                if c['name'] == 'Skill':
                    skills.append((c.get('input') or {}).get('skill'))
            elif c['type'] == 'text':
                narration += len(c.get('text', ''))
    ctxs = list(calls.values())
    reply = res.get('result') or ''
    m.update(api_calls=len(ctxs), first_ctx=ctxs[0] if ctxs else None, peak_ctx=max(ctxs) if ctxs else None,
             tool_calls=sum(tools.values()), tools=tools, skill_calls=skills,
             narration_chars=max(0, narration - len(reply)), t_first_tool=first.get('tool_use'), t_first_text=first.get('text'),
             tool_s=round(meta['wall_s'] - (m['api_ms'] or 0) / 1000, 2) if meta.get('wall_s') else None,
             files_written=len(meta.get('files', [])), bytes_written=sum(f['bytes'] for f in meta.get('files', [])),
             reply=reply, **{'r_' + k: v for k, v in style_of(reply).items()})
    return m


# ---------------------------------------------------------------- grading

def opus(a, prompt, timeout=600):
    cmd = ['claude', '-p', prompt, '--model', a.grader, '--effort', 'medium', '--output-format', 'json', '--no-session-persistence',
           '--setting-sources', 'project', '--strict-mcp-config', '--disable-slash-commands', '--tools', '']
    p = subprocess.run(cmd, env=clean_env(), capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=timeout, cwd='/tmp')
    r = json.loads(p.stdout)
    text = r.get('result', '')
    blob = text[text.find('{'):text.rfind('}') + 1]
    return json.loads(blob), r.get('total_cost_usd', 0)


def clip(s, n):
    s = s if isinstance(s, str) else json.dumps(s)
    return s if len(s) <= n else s[:n] + f'... [{len(s) - n} more chars]'


def transcript(events, limit=26000):
    out = []
    for e in events:
        if e.get('type') == 'assistant':
            for c in e['message'].get('content', []):
                if c['type'] == 'text':
                    out.append('ASSISTANT: ' + clip(c['text'], 1500))
                elif c['type'] == 'tool_use':
                    out.append(f"TOOL {c['name']}: " + clip(c.get('input'), 350))
        elif e.get('type') == 'user':
            for c in e['message'].get('content', []):
                if isinstance(c, dict) and c.get('type') == 'tool_result':
                    out.append(('ERROR ' if c.get('is_error') else 'RESULT ') + clip(c.get('content'), 260))
    text = '\n'.join(out)
    return text if len(text) <= limit else text[:limit // 2] + '\n... [middle of transcript cut] ...\n' + text[-limit // 2:]


def project_view(work, meta):
    parts = []
    st = sh(['git', 'status', '--porcelain', '-uall'], work).stdout
    parts.append('git status --porcelain:\n' + (st or '(clean)'))
    diff = sh(['git', 'diff'], work).stdout
    if diff:
        parts.append('git diff (tracked files):\n' + clip(diff, 6000))
    for f in meta['files'][:6]:
        if f['status'] in ('??', 'A'):
            try:
                parts.append(f"new file {f['path']}:\n" + clip(open(os.path.join(work, f['path']), errors='ignore').read(), 5000))
            except OSError:
                pass
    return '\n\n'.join(parts)


def assertions(skill, case):
    items = []
    for g in sorted(glob.glob(f'{EVALS}/{skill}/{case}/graders/*.md')):
        head, text = open(g).read().split('---', 2)[1:]
        meta = dict(re.findall(r'^(\w+):\s*(\w+)', head, flags=re.M))
        stem = os.path.basename(g)[:-3]
        items.append({'id': stem, 'type': meta.get('type', 'llm'), 'focus': meta.get('focus', 'reply'),
                      'weight': int(meta.get('weight', 1)), 'text': text.strip(),
                      'script': g[:-3] + '.sh' if os.path.exists(g[:-3] + '.sh') else None})
    return items


def grade_one(a, meta):
    rid = meta['rid']
    work = f"{a.out}/w/{rid}/work"
    events = load_events(rid, a.out)
    _, request = parse_prompt(f"{EVALS}/{meta['skill']}/{meta['case']}/prompt.md")
    items, results, cost = assertions(meta['skill'], meta['case']), {}, 0
    llm = []
    for it in items:
        if it['type'] == 'script' and it['script']:
            try:
                r = sh(['bash', it['script']], work, 60)
                results[it['id']] = {'passed': r.returncode == 0, 'evidence': f'script exit {r.returncode}: ' + clip((r.stdout + r.stderr).strip(), 160)}
            except subprocess.TimeoutExpired:
                results[it['id']] = {'passed': False, 'evidence': 'script timed out'}
        else:
            llm.append(it)
    if llm:
        res = next((e for e in reversed(events) if e.get('type') == 'result'), {})
        prompt = (
            "You grade one run of an AI coding assistant against assertions. Judge only from the evidence below. "
            "An assertion the evidence does not show is FAILED. Do not reward length or polish; check the statement itself. "
            "The run was one turn with no human present, so stopping to ask the user a question is a valid way to end.\n\n"
            f"## The user's request\n{request}\n\n## Assertions\n"
            + '\n'.join(f"- id {i['id']} (focus: {i['focus']}): {i['text']}" for i in llm)
            + f"\n\n## Transcript (tool calls in order, long values clipped)\n{transcript(events)}\n\n"
            f"## Final reply\n{clip(res.get('result') or '(none)', 9000)}\n\n## Final state of the project\n{project_view(work, meta)}\n\n"
            'Answer with ONLY this JSON: {"results":[{"id":"<id>","passed":true|false,"evidence":"<one line, a quote or a tool call>"}]}')
        try:
            out, cost = opus(a, prompt)
            for r in out['results']:
                results[r['id']] = {'passed': bool(r['passed']), 'evidence': r.get('evidence', '')}
        except Exception as ex:  # keep going; the missing ones show up as ungraded
            print('grader failed', meta['skill'], meta['case'], rid, repr(ex)[:200], flush=True)
    rows = []
    for it in items:
        r = results.get(it['id'])
        rows.append({'id': it['id'], 'type': it['type'], 'weight': it['weight'], 'text': it['text'],
                     'passed': None if r is None else r['passed'], 'evidence': '' if r is None else r['evidence']})
    json.dump({'rid': rid, 'grader_cost': cost, 'rows': rows}, open(f'{a.out}/runs/{rid}/grading.json', 'w'), indent=1)
    print('graded', meta['skill'], meta['case'], meta['config'], f"{sum(1 for r in rows if r['passed'])}/{len(rows)}", flush=True)


def cmd_grade(a):
    skills = a.skills.split(',')
    todo = [m for m in all_runs(a.out) if m['skill'] in skills and not os.path.exists(f"{a.out}/runs/{m['rid']}/grading.json")
            and m['rc'] == 0 and not m['timed_out']]
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for f in cf.as_completed([ex.submit(grade_one, a, m) for m in todo]):
            f.result()


def cmd_style(a):
    runs = all_runs(a.out)
    rng = random.Random(11)
    todo = []
    for skill in a.skills.split(','):
        for case in cases_of(skill):
            pair = {m['config']: m for m in runs if m['skill'] == skill and m['case'] == case and m['rep'] == 0 and m['rc'] == 0}
            if len(pair) == 2 and not os.path.exists(f'{a.out}/styles/{skill}__{case}.json'):
                todo.append((skill, case, pair))

    def one(skill, case, pair):
        order = ['none', 'with']
        rng.shuffle(order)
        _, request = parse_prompt(f'{EVALS}/{skill}/{case}/prompt.md')
        views = []
        for label, cfg in zip('AB', order):
            m = pair[cfg]
            ev = load_events(m['rid'], a.out)
            res = next((e for e in reversed(ev) if e.get('type') == 'result'), {})
            tools = metrics(ev, m)['tools']
            views.append(f"### Assistant {label}\nTool calls: {json.dumps(tools)}\nFiles written: {[f['path'] for f in m['files']] or 'none'}\n"
                         f"Final reply:\n{clip(res.get('result') or '(none)', 7000)}\n"
                         + (f"\nFirst written file:\n{clip(open(os.path.join(a.out, 'w', m['rid'], 'work', m['files'][0]['path']), errors='ignore').read(), 3500)}" if m['files'] else ''))
        prompt = ("Two AI coding assistants got the same request, one turn, no human present. Describe HOW they differ in the way they respond: "
                  "what each does first, how much it asks versus does, structure and length of the reply, tone, what it writes to disk, "
                  "where it stops. Be concrete and short. Do not guess which one used any special instructions.\n\n"
                  f"## Request\n{request}\n\n" + '\n\n'.join(views) +
                  '\n\nAnswer with ONLY this JSON: {"differences":["<=5 short concrete bullets"],"better_for_user":"A|B|tie","why":"<one sentence>"}')
        out, cost = opus(a, prompt)
        out['mapping'] = dict(zip('AB', order))
        out['cost'] = cost
        os.makedirs(f'{a.out}/styles', exist_ok=True)
        json.dump(out, open(f'{a.out}/styles/{skill}__{case}.json', 'w'), indent=1)
        print('styled', skill, case, flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for f in cf.as_completed([ex.submit(one, *t) for t in todo]):
            f.result()
    for skill in a.skills.split(','):  # one synthesis per skill
        parts = sorted(glob.glob(f'{a.out}/styles/{skill}__*.json'))
        if not parts or os.path.exists(f'{a.out}/styles/{skill}.summary.json'):
            continue
        notes = []
        for p in parts:
            s = json.load(open(p))
            inv = {v: k for k, v in s['mapping'].items()}
            notes.append({'case': os.path.basename(p)[len(skill) + 2:-5], 'with_is': inv['with'], 'none_is': inv['none'],
                          'differences': s['differences'], 'better_for_user': s['better_for_user'], 'why': s['why']})
        out, _ = opus(a, "Below are per-case comparisons of two assistants (one called 'with', one 'none'; the letters map via with_is/none_is). "
                      "Summarize in at most 4 short bullets how the 'with' assistant's way of responding differs from 'none' across the cases, "
                      "and say in one sentence which the user is better served by and where it is not.\n"
                      + json.dumps(notes, ensure_ascii=False) + '\nAnswer with ONLY this JSON: {"bullets":["..."],"verdict":"..."}')
        json.dump(out, open(f'{a.out}/styles/{skill}.summary.json', 'w'), indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- report

def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fmt(x, nd=0):
    return '-' if x is None else (f'{x:,.{nd}f}' if nd else f'{x:,.0f}')


def delta(none, with_, pct=True):
    if none in (None, 0) or with_ is None:
        return '-'
    return f'{(with_ / none - 1) * 100:+.0f}%'


def collect(a):
    rows = []
    for m in all_runs(a.out):
        ev = load_events(m['rid'], a.out)
        mt = metrics(ev, m)
        g = f"{a.out}/runs/{m['rid']}/grading.json"
        gr = json.load(open(g)) if os.path.exists(g) else None
        w = sum(r['weight'] for r in gr['rows']) if gr else None
        mt['pass_w'] = sum(r['weight'] for r in gr['rows'] if r['passed']) / w if gr and w else None
        mt['pass_n'] = sum(1 for r in gr['rows'] if r['passed']) if gr else None
        mt['n_assert'] = len(gr['rows']) if gr else None
        mt['grader_cost'] = gr['grader_cost'] if gr else 0
        rows.append({**m, **mt, 'grading': gr['rows'] if gr else None})
    return rows


def cmd_report(a):
    rows = collect(a)
    ok = [r for r in rows if r['rc'] == 0 and not r['timed_out'] and not r['is_error']]
    bad = [r for r in rows if r not in ok]
    skills = [s for s in PLAN if any(r['skill'] == s for r in ok)]
    probe = json.load(open(f'{a.out}/probe.json')) if os.path.exists(f'{a.out}/probe.json') else []
    L = []
    w = L.append
    model = rows[0]['model'] if rows else '?'
    effort = rows[0]['effort'] if rows else '?'
    w(f'# Plan skills on {model}: with the skill vs. without\n')
    w(f'Effort `{effort}`, {len(ok)} good runs of {len(rows)}. Medians over {max((r["rep"] for r in ok), default=0) + 1} rep(s) of every case; '
      '`Δ` is `with` against `none`. Raw numbers: `evals/bench-plan-results.json`.\n')
    fp = f'{a.out}/findings.md'
    if os.path.exists(fp):
        w(open(fp).read().rstrip() + '\n')
    w('## Headline: does the skill cost more, and does it help\n')
    w('| Skill | cases×reps | pass none → with | wall s none → with (Δ) | TTFT s | turns | output tok (Δ) | input tok, all calls (Δ) | cost $ none → with (Δ) |')
    w('|---|---|---|---|---|---|---|---|---|')
    agg = {}
    for s in skills:
        n = [r for r in ok if r['skill'] == s and r['config'] == 'none']
        k = [r for r in ok if r['skill'] == s and r['config'] == 'with']
        g = lambda rs, key: med([r[key] for r in rs])
        pn, pk = [r['pass_w'] for r in n if r['pass_w'] is not None], [r['pass_w'] for r in k if r['pass_w'] is not None]
        agg[s] = (n, k)
        w(f"| `{s}` | {len(n)}/{len(k)} | {fmt(100 * statistics.mean(pn)) if pn else '-'}% → {fmt(100 * statistics.mean(pk)) if pk else '-'}% "
          f"| {fmt(g(n, 'wall_s'))} → {fmt(g(k, 'wall_s'))} ({delta(g(n, 'wall_s'), g(k, 'wall_s'))}) "
          f"| {fmt((g(n, 'ttft_ms') or 0) / 1000, 1)} → {fmt((g(k, 'ttft_ms') or 0) / 1000, 1)} "
          f"| {fmt(g(n, 'turns'))} → {fmt(g(k, 'turns'))} "
          f"| {fmt(g(n, 'out'))} → {fmt(g(k, 'out'))} ({delta(g(n, 'out'), g(k, 'out'))}) "
          f"| {fmt(g(n, 'in_total'))} → {fmt(g(k, 'in_total'))} ({delta(g(n, 'in_total'), g(k, 'in_total'))}) "
          f"| {fmt(g(n, 'cost'), 3)} → {fmt(g(k, 'cost'), 3)} ({delta(g(n, 'cost'), g(k, 'cost'))}) |")
    allN = [r for s in skills for r in agg[s][0]]
    allK = [r for s in skills for r in agg[s][1]]
    if allN and allK:
        g = lambda rs, key: med([r[key] for r in rs])
        w(f"| **all** | {len(allN)}/{len(allK)} |  | {fmt(g(allN, 'wall_s'))} → {fmt(g(allK, 'wall_s'))} ({delta(g(allN, 'wall_s'), g(allK, 'wall_s'))}) | | "
          f"{fmt(g(allN, 'turns'))} → {fmt(g(allK, 'turns'))} | {fmt(g(allN, 'out'))} → {fmt(g(allK, 'out'))} ({delta(g(allN, 'out'), g(allK, 'out'))}) "
          f"| {fmt(g(allN, 'in_total'))} → {fmt(g(allK, 'in_total'))} ({delta(g(allN, 'in_total'), g(allK, 'in_total'))}) "
          f"| {fmt(g(allN, 'cost'), 3)} → {fmt(g(allK, 'cost'), 3)} ({delta(g(allN, 'cost'), g(allK, 'cost'))}) |")
    w('\n**Totals over every run** (sums, not medians; the medians above hide the long runs):\n')
    w('| Skill | wall s none → with | output tok none → with | input tok none → with | cost $ none → with |')
    w('|---|---|---|---|---|')
    tot = {'none': [0, 0, 0, 0], 'with': [0, 0, 0, 0]}
    for s in skills:
        row = {}
        for cfg, rs in (('none', agg[s][0]), ('with', agg[s][1])):
            row[cfg] = [sum(r['wall_s'] for r in rs), sum(r['out'] for r in rs), sum(r['in_total'] for r in rs), sum(r['cost'] or 0 for r in rs)]
            tot[cfg] = [x + y for x, y in zip(tot[cfg], row[cfg])]
        w(f"| `{s}` | {fmt(row['none'][0])} → {fmt(row['with'][0])} ({delta(row['none'][0], row['with'][0])}) | {fmt(row['none'][1])} → {fmt(row['with'][1])} ({delta(row['none'][1], row['with'][1])}) "
          f"| {fmt(row['none'][2])} → {fmt(row['with'][2])} ({delta(row['none'][2], row['with'][2])}) | {fmt(row['none'][3], 2)} → {fmt(row['with'][3], 2)} ({delta(row['none'][3], row['with'][3])}) |")
    w(f"| **all** | {fmt(tot['none'][0])} → {fmt(tot['with'][0])} ({delta(tot['none'][0], tot['with'][0])}) | {fmt(tot['none'][1])} → {fmt(tot['with'][1])} ({delta(tot['none'][1], tot['with'][1])}) "
      f"| {fmt(tot['none'][2])} → {fmt(tot['with'][2])} ({delta(tot['none'][2], tot['with'][2])}) | {fmt(tot['none'][3], 2)} → {fmt(tot['with'][3], 2)} ({delta(tot['none'][3], tot['with'][3])}) |")
    w('\n`input tok` sums every API call of the run (context is re-read each turn), cache reads included, so it grows with turns. '
      '`cost` is what the CLI billed at list price after cache discounts.\n')

    w('## Where the time and tokens go\n')
    w('| Skill | first-call context none → with | skill text added (tok) | API calls | peak context | tool calls | tool-wait s (wall − API) | time to first tool s |')
    w('|---|---|---|---|---|---|---|---|')
    for s in skills:
        n, k = agg[s]
        g = lambda rs, key: med([r[key] for r in rs])
        w(f"| `{s}` | {fmt(g(n, 'first_ctx'))} → {fmt(g(k, 'first_ctx'))} | {fmt((g(k, 'first_ctx') or 0) - (g(n, 'first_ctx') or 0))} "
          f"| {fmt(g(n, 'api_calls'))} → {fmt(g(k, 'api_calls'))} | {fmt(g(n, 'peak_ctx'))} → {fmt(g(k, 'peak_ctx'))} "
          f"| {fmt(g(n, 'tool_calls'))} → {fmt(g(k, 'tool_calls'))} | {fmt(g(n, 'tool_s'), 1)} → {fmt(g(k, 'tool_s'), 1)} "
          f"| {fmt(g(n, 't_first_tool'), 1)} → {fmt(g(k, 't_first_tool'), 1)} |")
    if probe:
        pn = med([p['first_ctx'] for p in probe if p['config'] == 'none'])
        pk = med([p['first_ctx'] for p in probe if p['config'] == 'with'])
        w(f"\nInstall overhead with no skill called (a `pong` prompt, {len(probe) // 2} runs each): first-call context {fmt(pn)} → {fmt(pk)} tokens, "
          f"so the plan plugin's skill list costs {fmt(pk - pn)} tokens per session. `skill text added` above includes this.\n")

    w('## How it responds\n')
    w('| Skill | reply words | headings | bullets | table rows | question lines | files written | bytes written | narration chars between tools |')
    w('|---|---|---|---|---|---|---|---|---|')
    for s in skills:
        n, k = agg[s]
        g = lambda rs, key: med([r[key] for r in rs])
        c = lambda key: f"{fmt(g(n, key))} → {fmt(g(k, key))}"
        w(f"| `{s}` | {c('r_words')} | {c('r_headings')} | {c('r_bullets')} | {c('r_table_rows')} | {c('r_question_lines')} "
          f"| {c('files_written')} | {c('bytes_written')} | {c('narration_chars')} |")
    w('\nEach cell is `none → with`.\n')
    for s in skills:
        sp = f'{a.out}/styles/{s}.summary.json'
        if os.path.exists(sp):
            sm = json.load(open(sp))
            w(f'**`{s}`**')
            for b in sm.get('bullets', []):
                w(f'- {b}')
            w(f"- Verdict: {sm.get('verdict', '')}\n")

    w('## Quality: assertions\n')
    w('| Skill | Case | none passed | with passed | failed only under `none` | failed only under `with` |')
    w('|---|---|---|---|---|---|')
    fails = []
    for s in skills:
        for case in cases_of(s):
            cell = {}
            for cfg in ('none', 'with'):
                rs = [r for r in ok if r['skill'] == s and r['case'] == case and r['config'] == cfg and r['grading']]
                cell[cfg] = rs
            def tally(rs):
                if not rs:
                    return '-'
                return f"{statistics.mean(r['pass_n'] for r in rs):.1f}/{rs[0]['n_assert']}"
            only = {'none': [], 'with': []}
            ids = {x['id'] for r in cell['none'] + cell['with'] for x in r['grading']}
            for i in sorted(ids):
                rate = {cfg: [next((x['passed'] for x in r['grading'] if x['id'] == i), None) for r in cell[cfg]] for cfg in cell}
                ok_n = sum(1 for v in rate['none'] if v) / max(1, len(rate['none']))
                ok_w = sum(1 for v in rate['with'] if v) / max(1, len(rate['with']))
                if ok_n < ok_w:
                    only['none'].append(i)
                elif ok_w < ok_n:
                    only['with'].append(i)
                for cfg in cell:
                    for r, v in zip(cell[cfg], rate[cfg]):
                        if not v:
                            x = next((x for x in r['grading'] if x['id'] == i), {})
                            fails.append((s, case, cfg, r['rep'], i, x.get('text', ''), x.get('evidence', '')))
            w(f"| `{s}` | `{case}` | {tally(cell['none'])} | {tally(cell['with'])} | {', '.join(only['none']) or '-'} | {', '.join(only['with']) or '-'} |")
    w('\nPass counts are the mean over reps. Graders: script assertions run on the final project; llm assertions judged by '
      f"`{a.grader}` (a different model from the one tested).\n")

    w('## Failed assertions\n')
    w('| Skill / case | Config | Rep | Assertion | Evidence |')
    w('|---|---|---|---|---|')
    for s, case, cfg, rep, i, text, ev in fails:
        w(f"| `{s}/{case}` | {cfg} | {rep} | `{i}`: {clip(text, 120)} | {clip(ev.replace('|', '/'), 140)} |")

    w('\n## Run health\n')
    leaks = [r for r in rows if r.get('leak')]
    w(f'- Runs not counted (non-zero exit, timeout or error result): {len(bad)}' + ''.join(f"\n  - `{r['skill']}/{r['case']}` r{r['rep']} {r['config']}: rc={r['rc']} timeout={r['timed_out']} terminal={r.get('terminal')}" for r in bad))
    w(f'- Transcripts that named the real eval folder: {len(leaks) or "none"}')
    nofile = [r for r in ok if r['config'] == 'with' and r['first_ctx'] and agg.get(r['skill']) and
              r['first_ctx'] - (med([x['first_ctx'] for x in agg[r['skill']][0]]) or 0) < 450]
    w(f"- `with` runs whose first-call context is under 450 tokens larger than `none` (the skill may not have loaded): {len(nofile) or 'none'}")
    spend = sum(r['cost'] or 0 for r in rows)
    gspend = sum(r['grader_cost'] or 0 for r in rows)
    styles = sum(json.load(open(p)).get('cost', 0) for p in glob.glob(f'{a.out}/styles/*__*.json'))
    w(f'- Spend: tested runs ${spend:.2f}, assertion grading ${gspend:.2f}, style comparison ${styles:.2f}')
    w(f"- Parallel runs at a time: {max((r['jobs'] for r in rows), default='?')}. Wall times include queueing on the shared network and are noisy; compare medians, not single runs.\n")

    w('## Per case\n')
    w('| Skill / case | cfg | n | wall s | turns | out tok | in tok | cost $ | reply words | files | pass |')
    w('|---|---|---|---|---|---|---|---|---|---|---|')
    for s in skills:
        for case in cases_of(s):
            for cfg in ('none', 'with'):
                rs = [r for r in ok if r['skill'] == s and r['case'] == case and r['config'] == cfg]
                if rs:
                    g = lambda key: med([r[key] for r in rs])
                    w(f"| `{s}/{case}` | {cfg} | {len(rs)} | {fmt(g('wall_s'))} | {fmt(g('turns'))} | {fmt(g('out'))} | {fmt(g('in_total'))} | {fmt(g('cost'), 3)} "
                      f"| {fmt(g('r_words'))} | {fmt(g('files_written'))} | {fmt(100 * (g('pass_w') or 0))}% |")
    open(a.md, 'w').write('\n'.join(L) + '\n')
    slim = [{k: v for k, v in r.items() if k not in ('reply',)} for r in rows]
    json.dump(slim, open(a.json, 'w'), indent=1, ensure_ascii=False)
    print('wrote', a.md, a.json)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('cmd', choices=['plugin', 'probe', 'run', 'grade', 'style', 'report'])
    p.add_argument('--out', required=True)
    p.add_argument('--skills', default=','.join(PLAN))
    p.add_argument('--model', default='claude-sonnet-5-5')
    p.add_argument('--grader', default='claude-opus-5-5')
    p.add_argument('--effort', default='high')
    p.add_argument('--reps', type=int, default=2)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--budget', type=float, default=4.0)
    p.add_argument('--max-wall', type=int, default=900, dest='max_wall')
    p.add_argument('--md', default=f'{EVALS}/bench-plan-sonnet-5-5.md')
    p.add_argument('--json', default=f'{EVALS}/bench-plan-results.json')
    a = p.parse_args()
    a.out = os.path.abspath(a.out)
    os.makedirs(a.out, exist_ok=True)
    {'plugin': cmd_plugin, 'probe': cmd_probe, 'run': cmd_run, 'grade': cmd_grade, 'style': cmd_style, 'report': cmd_report}[a.cmd](a)
