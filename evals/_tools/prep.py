import os, sys, json, re, shutil, secrets, glob
S='/tmp/claude-1001/-home-cuongtc9-skills/9d056fae-1388-4280-a01a-6d3181b883e9/scratchpad'
REPO='/home/cuongtc9/skills/skills'
RUNS=f'{S}/w'
MAP=f'{S}/blind/map.json'
MATT='/home/cuongtc9/.claude/plugins/cache/claude-plugins-official/mattpocock-skills/1.3.1/skills'
SKILLS={ # skill under test -> config -> directory with SKILL.md (None = nothing)
 'spec-it': {'new':f'{REPO}/skills/spec-it','old':f'{S}/spec-it-workspace/skill-v0','matt':f'{MATT}/engineering/to-spec','none':None},
}
NOTE={'matt':"There is no issue tracker in this project, so write the spec to the file named in the request instead of publishing it, and skip the triage label."}
def prompt_for(skill, case):
    body=open(f"{REPO}/evals/{skill}/{case}/prompt.md").read().split('---',2)[2].strip()
    body=re.sub(r"\n\nInput files:.*$","",body,flags=re.S)
    body=body.replace(" Write your reply to reply.md.","")
    return body
def main(skill, configs):
    m=json.load(open(MAP)) if os.path.exists(MAP) else {}
    cases=sorted(os.listdir(f"{REPO}/evals/{skill}"))
    out=[]
    for case in cases:
        for cfg in configs:
            rid=secrets.token_hex(4)
            base=f"{RUNS}/{rid}"; os.makedirs(base+'/work')
            shutil.copytree(f"{REPO}/evals/{skill}/{case}/files", base+'/work', dirs_exist_ok=True)
            src=SKILLS[skill][cfg]
            guide=None
            if src:
                shutil.copytree(src, base+'/guide', ignore=shutil.ignore_patterns('evals','graders','*.pyc'))
                guide=base+'/guide/SKILL.md'
            msg=prompt_for(skill,case)
            lines=[f"I am working in {base}/work ."]
            if guide:
                lines.append(f"Use the instructions in {guide} for this (read it first, and any file it links to)." + (" "+NOTE[cfg] if cfg in NOTE else ""))
            lines.append(f'My request: "{msg}"')
            p="\n\n".join(lines)
            m[rid]={'skill':skill,'case':case,'config':cfg,'base':base}
            out.append((rid,p))
    json.dump(m,open(MAP,'w'),indent=1)
    json.dump(out,open(f"{S}/blind/prompts_{skill}.json",'w'),indent=1)
    for rid,p in out: print(rid, m[rid]['case'][:14], m[rid]['config'])
main(sys.argv[1], sys.argv[2].split(','))
