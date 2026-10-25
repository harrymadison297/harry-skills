import json, re, glob, os, shutil, sys
S='/tmp/claude-1001/-home-cuongtc9-skills/9d056fae-1388-4280-a01a-6d3181b883e9'
SC=S+'/scratchpad'; skill=sys.argv[1]; tag=sys.argv[2]
REPO='/home/cuongtc9/skills/skills'
m=json.load(open(f"{SC}/blind/map.json"))
found={}
for f in glob.glob(f"{S}/tasks/*.output"):
    txt=open(f,errors='ignore').read(6000)
    mm=re.search(r"scratchpad/w/([0-9a-f]{8})/", txt)
    if mm and mm.group(1) in m and m[mm.group(1)]['skill']==skill: found[mm.group(1)]=f
print(len(found),"transcripts matched")
for rid,f in found.items():
    r=m[rid]; d=f"{SC}/g/{tag}/{r['case']}/{r['config']}"
    os.makedirs(d+'/outputs',exist_ok=True)
    shutil.copytree(r['base']+'/work', d+'/outputs/project', dirs_exist_ok=True)
    calls=["# Transcript (tool calls)\n"]; last=""
    for raw in open(f,errors='ignore'):
        try: ev=json.loads(raw)
        except Exception: continue
        msg=ev.get('message',ev); c=msg.get('content') if isinstance(msg,dict) else None
        if msg.get('role')=='assistant' and isinstance(c,list):
            texts=[x.get('text','') for x in c if x.get('type')=='text']
            for x in c:
                if x.get('type')=='tool_use':
                    if 'Handback' in (x.get('name') or ''): last=x.get('input',{}).get('message',last)
                    else: calls.append(f"- {x.get('name')}: {json.dumps(x.get('input',{}))[:300]}")
            if texts and not last: last="\n".join(texts)
    open(d+'/transcript.md','w').write("\n".join(calls)+"\n")
    open(d+'/outputs/reply.md','w').write(last)
for case in set(v['case'] for v in m.values() if v['skill']==skill):
    body=open(f"{REPO}/evals/{skill}/{case}/prompt.md").read().split('---',2)[2].strip()
    body=re.sub(r"\n\nInput files:.*$","",body,flags=re.S)
    a=[open(g).read().split('---',2)[2].strip() for g in sorted(glob.glob(f"{REPO}/evals/{skill}/{case}/graders/*.md"))]
    os.makedirs(f"{SC}/g/{tag}/{case}",exist_ok=True)
    json.dump({"eval_name":case,"prompt":body,"assertions":a},open(f"{SC}/g/{tag}/{case}/eval_metadata.json","w"),indent=1)
