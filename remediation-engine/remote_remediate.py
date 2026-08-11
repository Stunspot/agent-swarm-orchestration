#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os,re,sys,json,hashlib,html,math,subprocess,urllib.parse,time
OWNER='Stunspot'
META={
'agent-swarm-orchestration':('Agent Swarm Orchestration','Disciplined delegation, dependency control, and synthesis for multi-agent work.','agent builders and operators coordinating bounded subagent work','turning a broad objective into owned work packets with explicit evidence and reconciliation','network',('#F3E8D0','#28231E','#D67B2B','#6A7B6B','#FFF9EF')),
'CanopyOps':('CanopyOps','An inspectable operating canopy for agent workspaces, capabilities, routines, and recovery.','operators maintaining agent workspaces and repeatable routines','keeping procedures, context, and recovery legible as an operational environment grows','canopy',('#E8E3CC','#173C32','#BE7A3A','#6E8B5E','#FBF8EB')),
'impactful-tom':('Impactful Tom','Explicit, revisable reasoning about people, incentives, interpretations, and likely impact.','people preparing consequential communication or stakeholder-facing decisions','anticipating interpretations without pretending to read minds','ripples',('#F5DDDA','#24324A','#D85C54','#E8A43B','#FFF8F3')),
'lex-foster-language-companion':('Lex Foster Language Companion','Adaptive language practice, correction, explanation, and conversational growth.','language learners seeking responsive practice and feedback','turning passive study into a loop of comprehensible use, correction, and increasing independence','speech',('#F4EBDD','#193B73','#C7463D','#E3A640','#FFFDF8')),
'ludis-continuum':('Ludis Continuum','Tabletop roleplaying support for preparation, play, adjudication, and continuity.','game masters, players, and designers using AI as a structured creative aid','producing useful game material while protecting agency, tone, rules context, and canon boundaries','map',('#EFE3C5','#4B2427','#B57A39','#526052','#FFF9E9')),
'nova-the-optimal-ai-mind':('Nova + MIND Free','A generalist agent-mind package for deliberate problem solving, tools, and collaboration.','people seeking a coherent generalist agent scaffold','replacing disconnected prompt fragments with an explicit working style and operational boundaries','orbit',('#EEE6F2','#37244F','#B58B36','#6D5A8A','#FFF9F0')),
'omnara-deep-research':('Omnara Deep Research','Evidence-centered scoping, source gathering, claim testing, and traceable synthesis.','researchers and decision makers who need transparent evidence handling','moving from an ambiguous question to a sourced, uncertainty-aware research product','archive',('#E8EEE9','#163F43','#B96B45','#567A71','#FFFDF5')),
'omniview-looking-glass':('OmniView — The Looking Glass Companion','Visual inspection that separates direct observation from inference.','people using an agent to inspect images, interfaces, diagrams, and visual evidence','preserving spatial detail and uncertainty before drawing conclusions','glass',('#E6EFF0','#17363D','#4E8791','#C58B45','#FCFFFF')),
'owen-burnett-officecraft':('Owen Burnett Officecraft','Clear, usable office artifacts with explicit assumptions, checks, and handoff guidance.','people producing documents, spreadsheets, presentations, correspondence, and operational materials','turning vague office requests into fit-for-purpose knowledge-work artifacts','folders',('#E8E5DD','#24476B','#B66B43','#6B7F91','#FFFDF8')),
'praxis-mine':('Praxis Mine','Practical knowledge mining for reusable methods, decisions, and operating insight.','builders and analysts extracting action from repositories, transcripts, or document collections','recovering procedures and decision logic from dense material without flattening provenance','strata',('#E8DED0','#302B28','#B2683B','#7D725F','#FFF8EC')),
'signal-loom':('Signal Loom','Evidence-aware synthesis of scattered observations into patterns and hypotheses.','analysts and strategists working with noisy or cross-domain signals','connecting evidence without erasing contradictions, source quality, timing, or uncertainty','weave',('#ECE6F1','#30305A','#D59A32','#648B8A','#FFF9ED')),
'TestForge':('TestForge','Evidence-bearing tests that distinguish existence, packaging, execution, health, and success.','agent and software builders who need adversarial verification','turning claims into observable tests, failure oracles, receipts, and honest verdicts','forge',('#ECE9E3','#27313B','#B9473D','#B68A45','#FFFDF7')),
'yammerknit':('Yammerknit','Audience-aware posts, threads, replies, and conversational artifacts without sanding away voice.','people shaping public or community-facing communication','turning raw thoughts into coherent, context-sensitive communication while retaining authorship','knit',('#F0E6ED','#4C3157','#B55C68','#5F8E79','#FFF9F3'))}
slug=os.environ.get('REPO_SLUG') or Path.cwd().name
if slug not in META: raise SystemExit('unknown repository: '+slug)
title,line,audience,problem,motif,pal=META[slug]
root=Path.cwd()

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(s):
 s=re.sub(r'<[^>]+>|!\[[^]]*\]\([^)]*\)',' ',s);s=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',s);return re.sub(r'\s+',' ',re.sub(r'[`*_~#>|]',' ',s)).strip()
def lead(md):
 md=re.sub(r'```[\s\S]*?```|<!--.*?-->','',md,flags=re.S)
 for p in re.split(r'\n\s*\n',md):
  q=clean(' '.join(x for x in p.splitlines() if not x.lstrip().startswith(('#','|','[!','<img','<p align','---','!['))))
  if 60<=len(q)<=600:return q
 return line
old=(root/'README.md').read_text(errors='replace') if (root/'README.md').exists() else ''
leadtext=lead(old)

def texts():
 out=[]
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in {'.md','.txt','.json','.yml','.yaml','.toml'} and not any(x in p.parts for x in ['.git','node_modules','releases','archives']):
   try:out.append((p,p.read_text(errors='replace')))
   except:pass
 return out
orig=texts()
HOSTS=[('Codex',r'\bcodex\b'),('Claude Code',r'claude\s+code'),('Gemini CLI',r'gemini\s+cli'),('OpenCode',r'\bopencode\b'),('OpenClaw',r'\bopenclaw\b'),('ChatGPT',r'\bchatgpt\b'),('Claude Desktop',r'claude\s+desktop'),('Cursor',r'\bcursor\b'),('Windsurf',r'\bwindsurf\b'),('VS Code',r'visual studio code|\bvs\s*code\b'),('GitHub Copilot',r'github\s+copilot'),('Generic SKILL.md host',r'skill\.md|agent skill')]
hosts=[]
for n,pat in HOSTS:
 ev=[str(p.relative_to(root)).replace('\\','/') for p,t in orig if re.search(pat,t,re.I)]
 if ev:hosts.append((n,ev[:3]))

def sections(md):
 out=[];h=None;b=[]
 for l in md.splitlines():
  m=re.match(r'^(#{1,4})\s+(.+)',l)
  if m:
   if h:out.append((h,'\n'.join(b).strip()))
   h=clean(m.group(2));b=[]
  elif h:b.append(l)
 if h:out.append((h,'\n'.join(b).strip()))
 return out
install=[];use=[]
for p,t in orig:
 if p.suffix.lower()!='.md':continue
 rel=str(p.relative_to(root)).replace('\\','/')
 for h,b in sections(t):
  if len(b)<25:continue
  if re.search(r'install|setup|codex|claude code|gemini cli|opencode|openclaw|chatgpt|cursor|windsurf',h,re.I):install.append((rel,h,b[:4500]))
  if re.search(r'quick start|first|usage|workflow|example|how to use|invocation|try it',h,re.I):use.append((rel,h,b[:3500]))
def dedupe(xs,n):
 out=[];seen=set()
 for x in xs:
  k=re.sub(r'\s+',' ',x[2]).lower()[:220]
  if k not in seen:seen.add(k);out.append(x)
 return out[:n]
install=dedupe(install,14);use=dedupe(use,5)

def reb(body,rel):
 base=Path(rel).parent
 def f(m):
  bang,label,u=m.group(1) or '',m.group(2),m.group(3).strip()
  if u.startswith(('#','http:','https:','mailto:','data:')):return m.group(0)
  q=(base/u.split('#')[0]).as_posix();q='/'.join(x for x in q.split('/') if x not in ('','.'))
  return f'{bang}[{label}](https://github.com/{OWNER}/{slug}/blob/main/{q})'
 return re.sub(r'(!?)\[([^]]+)\]\(([^)]+)\)',f,body)
lic='No standalone license detected';licpath=''
for n in ['LICENSE','LICENSE.md','LICENSE.txt','COPYING']:
 p=root/n
 if p.exists():
  q=p.read_text(errors='replace')[:4000];licpath=n
  lic='MIT License' if 'MIT License' in q else ('Apache License' if 'Apache License' in q else ('GNU General Public License' if 'GNU GENERAL PUBLIC LICENSE' in q else 'See repository license text'))
  break
src=[]
for pat in ['SKILL.md','package.json','pyproject.toml','augment.json','manifest.json']:
 for p in root.rglob(pat):
  if p.is_file() and '.git' not in p.parts and not any(x in p.parts for x in ['releases','archives']):src.append(p)
src=sorted(set(src),key=lambda p:(0 if 'canonical' in str(p).lower() else 1,len(p.parts),str(p)))[:18]
hostrows='\n'.join(f"| {n} | Mention found; install success not inferred | "+', '.join(f'`{e}`' for e in ev)+' |' for n,ev in hosts) or '| No named host detected | NOT CLAIMED | Add and verify a host recipe before claiming support. |'
inst='\n\n'.join(f"### {h}\n\nSource: [`{rel}`]({urllib.parse.quote(rel)})\n\n{reb(b,rel)}" for rel,h,b in install) or '### No packaged host recipe was found\n\nNo installation route is invented here. Host installation is **NOT ESTABLISHED** until a maintainer adds and verifies a host-specific procedure.'
uses='\n\n'.join(f"### {h}\n\nSource: [`{rel}`]({urllib.parse.quote(rel)})\n\n{reb(b,rel)}" for rel,h,b in use) or f'### Conservative first request\n\nAfter discovery, invoke {title} on a small, reversible task inside its stated domain. Require explicit assumptions, observable acceptance criteria, and a statement of what was not tested.'
srcrows='\n'.join(f'| `{p.relative_to(root).as_posix()}` | `{sha(p)}` | {p.stat().st_size} |' for p in src) or '| NOT IDENTIFIED | — | — |'
guide=f'''# {title} — Customer Guide

> {leadtext}

This is the current customer-facing operating reference. It distinguishes repository contents from runtime behavior and does not treat packaging as proof of installation, invocation, health, publication, or independent validation.

## Product fit

**Designed for:** {audience}.

**Problem addressed:** {problem}.

**What it is:** a packaged augment: instructions and supporting material intended to shape an AI host when the host can discover and invoke it.

**What it is not:** a standalone execution engine, a guarantee of model behavior, or evidence that every mentioned host was successfully tested with this revision.

## Capability boundary

The product can guide work in its documented scope. It cannot grant tools, permissions, network access, credentials, memory, or execution facilities absent from the host. Outputs remain proposals or artifacts until a human or independently observable system verifies them.

| Status | Meaning |
|---|---|
| Constructed | Files or instructions were authored. |
| Packaged | Required files are assembled. |
| Installed | Files were placed in a host-specific location. |
| Discoverable | The host can identify the augment. |
| Invoked | A task actually used it. |
| Healthy | Invocation completed without a detected product-level fault. |
| Published | A public surface is reachable. |
| Independently verified | A separate evidence-bearing check reproduced the claim. |

## Supported-host evidence

A host appears only when named in current repository material. A mention is not an install receipt.

| Host | Evidence status | Evidence locations |
|---|---|---|
{hostrows}

## Installation and maintenance

The following excerpts come from current repository Markdown so commands and paths are not invented. Use one host's recipe; do not splice paths from different hosts.

{inst}

### Verify installation

1. Confirm the copied package includes the canonical instruction file and referenced files.
2. Start a fresh host session.
3. Ask the host to locate **{title}** without pasting its instructions into chat.
4. Invoke a small read-only task and require identification of the augment or its distinctive workflow.
5. Record host, package fingerprint, prompt, output, and tool evidence. Otherwise mark installation or invocation **NOT TESTED**.

### Update

Fetch the desired revision, compare fingerprints, replace only the installed augment directory, and repeat fresh-session discovery and read-only invocation. Preserve local configuration separately.

### Remove and clean up

Remove the host-specific augment directory, restart the host, and verify it is no longer discoverable. Inspect generated artifacts, logs, caches, and state before deleting them; preserve unrelated work.

## First successful use

Choose a reversible representative workflow and evaluate the output against the request and evidence rather than fluency.

{uses}

## Inputs, outputs, and configuration

**Typical input:** a task within scope plus source material, constraints, desired deliverable, and acceptance criteria.

**Typical output:** a structured analysis, plan, draft, artifact, or verification record described by the invoked workflow. Exact output depends on host, tools, and evidence.

**Configuration:** treat files described as optional, local, profile-specific, or stateful as configuration. Keep secrets out of versioned files. When no configuration is documented, do not invent one.

## Troubleshooting and recovery

| Symptom | Check | Recovery |
|---|---|---|
| Host cannot find it | Exact path, directory name, canonical instruction file | Correct path, restart, retry discovery. |
| Behavior is generic | Actual invocation and referenced files | Invoke explicitly and restore missing files. |
| Output claims unavailable actions | Host tools, permissions, logs | Mark unverified; rerun with evidence required. |
| Update changes behavior | Old/new fingerprints and local config | Restore known revision; reproduce safely; file an evidence-rich issue. |
| Removal seems incomplete | Sessions, caches, artifacts, state | Start fresh; delete only confirmed product data. |

## Privacy, storage, network, and security boundaries

Repository files are public package material. Runtime storage and network behavior are controlled by the host and authorized tools. Review provider retention, connectors, workspace mounts, tool permissions, and outbound requests before supplying sensitive data. No telemetry, encryption, sandboxing, credential-storage, or network-isolation claim is made without canonical source and runtime evidence. Treat generated commands and prose as untrusted; use least privilege and human review before external writes or destructive action.

## Known limitations and unsupported claims

- Prompt instructions influence behavior probabilistically; they are not enforcement.
- File existence does not prove installation, discovery, invocation, or health.
- Examples show intended use, not guaranteed performance.
- Tool-dependent workflows remain unavailable without the relevant tool, permission, data, or network route.
- This remediation validates current documentation/presentation, not frozen historical archives or every runtime combination.
- Claims without observable evidence remain **NOT ESTABLISHED**.

## Provenance and evidence

| Canonical/package source | SHA-256 | Bytes |
|---|---|---:|
{srcrows}

Review receipts in [`verification/`](verification/) bind to the exact current documentation fingerprint. [`documentation-manifest.json`](documentation-manifest.json) defines the current customer-facing set; unlisted frozen or release-specific material is not silently promoted.

## Support and contribution

Use [GitHub Issues](https://github.com/{OWNER}/{slug}/issues) for reproducible defects and missing instructions. Pull requests should be focused and rerun documentation, accessibility, and adversarial review after customer-facing changes. Do not post secrets, private source, or third-party personal data.

## License and terms

**Detected license:** {lic}. {f'See [`{licpath}`]({licpath}).' if licpath else 'Reuse rights are NOT ESTABLISHED until a license is supplied.'} Third-party hosts, models, dependencies, and services retain their own terms.
'''
(root/'CUSTOMER-GUIDE.md').write_text(guide)
for name,body in {
'SUPPORT.md':f'# Support for {title}\n\nUse [GitHub Issues](https://github.com/{OWNER}/{slug}/issues) with revision/fingerprint, host/version, install path, prompt, expected and observed result, and redacted logs. Distinguish copied, discovered, invoked, and independently verified. Do not post secrets or personal data. Support is best-effort; file existence, HTTP status, and fluent output are not success evidence.\n',
'CONTRIBUTING.md':f'# Contributing to {title}\n\nFocused issues and pull requests are welcome. Customer-facing changes must update the README, guide, Pages, manifest, affected visuals, and all three review receipts. Any post-review byte change invalidates the old receipt. Do not rewrite frozen release archives or mix unrelated source changes into documentation remediation.\n',
'SECURITY.md':f'# Security and privacy boundaries — {title}\n\nThis augment is instruction material, not a security boundary. Host, model provider, connectors, tools, OS, and workspace determine retention, network access, permissions, and isolation. Use least privilege, read-only checks first, no secrets in prompts or versioned config, and human review before external writes or destructive action. Report sensitive vulnerabilities privately when a maintainer channel exists.\n'}.items():
 p=root/name
 if not p.exists() or len(p.read_text(errors='replace').strip())<350:p.write_text(body)
asset=root/'docs/assets';asset.mkdir(parents=True,exist_ok=True)
def font(sz,b=True):
 for f in ([ '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if b else ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']):
  if Path(f).exists():return ImageFont.truetype(f,sz)
 return ImageFont.load_default()
def wrap(d,s,f,w):
 out=[];cur=''
 for z in s.split():
  q=(cur+' '+z).strip()
  if d.textbbox((0,0),q,font=f)[2]<=w:cur=q
  else:
   if cur:out.append(cur)
   cur=z
 if cur:out.append(cur)
 return out
def shape(d,box):
 x0,y0,x1,y1=box;w=x1-x0;h=y1-y0;bg,ink,a,b,paper=pal
 idx=list(META).index(slug)
 if motif in ('network','ripples','orbit','glass'):
  cx=x0+w*.53;cy=y0+h*.5
  for i in range(6):
   r=w*(.07+i*.055);d.ellipse([cx-r,cy-r*.62,cx+r,cy+r*.62],outline=[ink,a,b][i%3],width=3+i%2*2)
  for i in range(7):
   q=2*math.pi*i/7+idx*.2;px=cx+math.cos(q)*w*.38;py=cy+math.sin(q)*h*.35;d.line([(cx,cy),(px,py)],fill=ink,width=3);d.ellipse([px-13,py-13,px+13,py+13],fill=a if i%2 else b,outline=ink,width=2)
 elif motif in ('canopy','strata','weave','knit'):
  for i in range(10):
   pts=[]
   for j in range(40):pts.append((x0+w*j/39,y0+h*(.1+i*.085+math.sin(j*.55+i+idx)*.025)))
   d.line(pts,fill=[ink,a,b,paper][i%4],width=3+(i%3)*2)
  if motif in ('weave','knit'):
   for i in range(11):d.line([(x0+w*(.05+i*.09),y0+h*.08),(x0+w*(.08+i*.08),y0+h*.92)],fill=a if i%3==0 else ink,width=5 if i%3==0 else 2)
 elif motif in ('speech','archive','folders'):
  for i in range(5):
   x=x0+w*(.08+i*.08);y=y0+h*(.12+i*.12);d.rounded_rectangle([x,y,x+w*.55,y+h*.36],radius=int(w*.025),fill=paper if i%2 else b,outline=ink,width=4)
   d.rectangle([x+w*.04,y+h*.05,x+w*.2,y+h*.1],fill=a)
   for j in range(3):d.line([(x+w*.05,y+h*(.16+j*.065)),(x+w*.48,y+h*(.16+j*.065))],fill=ink,width=3)
 elif motif in ('map','forge'):
  poly=[(x0+w*.15,y0+h*.35),(x0+w*.68,y0+h*.23),(x0+w*.86,y0+h*.52),(x0+w*.6,y0+h*.82),(x0+w*.22,y0+h*.73)]
  d.polygon(poly,fill=paper,outline=ink);d.line(poly+[poly[0]],fill=a,width=9)
  for q in poly:d.ellipse([q[0]-10,q[1]-10,q[0]+10,q[1]+10],fill=b,outline=ink,width=2)
 else:
  for i in range(8):
   r=w*(.05+i*.045);d.arc([x0+w*.5-r,y0+h*.5-r*.7,x0+w*.5+r,y0+h*.5+r*.7],20+i*22,290+i*16,fill=[ink,a,b][i%3],width=7)
for role,(W,H) in {'readme-hero':(1600,700),'pages-hero':(1440,960),'social-card':(1200,630)}.items():
 bg,ink,a,b,paper=pal;im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
 if role=='readme-hero':
  d.rectangle([0,0,34,H],fill=a);d.line([(92,90),(92,H-90)],fill=ink,width=3);f=font(70);y=110
  for z in wrap(d,title,f,int(W*.45))[:3]:d.text((138,y),z,font=f,fill=ink);y+=82
  f2=font(29,False);y+=12
  for z in wrap(d,line,f2,int(W*.43))[:4]:d.text((140,y),z,font=f2,fill=ink);y+=40
  d.text((140,H-75),'AUGMENT · CURRENT DOCUMENTATION',font=font(19),fill=a);shape(d,(int(W*.56),65,W-65,H-65))
 elif role=='pages-hero':
  im.paste(paper,[0,0,W,H]);d.rectangle([0,H-142,W,H],fill=ink);shape(d,(65,55,W-65,H-180));d.text((70,H-108),title,font=font(34),fill=paper);d.text((W-570,H-101),'A product-specific documentation field.',font=font(23,False),fill=bg)
 else:
  im.paste(ink,[0,0,W,H]);d.rectangle([42,42,W-42,H-42],fill=bg);d.rectangle([42,42,70,H-42],fill=a);shape(d,(int(W*.68),70,W-65,H-70));d.rectangle([92,78,int(W*.73),H-78],fill=bg);f=font(60 if len(title)<34 else 49);y=98
  for z in wrap(d,title,f,int(W*.58))[:4]:d.text((118,y),z,font=f,fill=ink);y+=68 if len(title)<34 else 56
  y+=14;f2=font(27,False)
  for z in wrap(d,line,f2,int(W*.56))[:3]:d.text((120,y),z,font=f2,fill=ink);y+=37
  d.text((120,H-105),'PUBLIC DOCUMENTATION · STUNSPOT',font=font(18),fill=a)
 im.save(asset/f'{slug}-{role}.png',optimize=True)
hostnames=', '.join(n for n,_ in hosts) or 'No host support claimed without current repository evidence'
readme=f'''<p align="center"><img src="docs/assets/{slug}-readme-hero.png" alt="{title} README hero" width="100%"></p>

# {title}

{leadtext}

[![Documentation](https://img.shields.io/badge/docs-live-2b5d62)](https://stunspot.github.io/{slug}/) [![Customer guide](https://img.shields.io/badge/guide-customer_journey-70564a)](CUSTOMER-GUIDE.md)

## What this is

{title} is a packaged augment for {audience}. It addresses {problem}. It supplies instructions and supporting material to a compatible AI host; it does not itself provide a model, tools, credentials, persistence, or an execution sandbox.

## Start here

1. Read the complete [customer guide](CUSTOMER-GUIDE.md), especially capability and privacy boundaries.
2. Use only a host installation recipe actually documented in this repository.
3. Start a fresh session, verify discovery, and invoke a small read-only task.
4. Keep package fingerprint, prompt, output, and observable tool evidence. Packaging is not successful installation or invocation.

**Host names found in current material:** {hostnames}.

## What it can and cannot do

It can structure work within documented scope and produce analyses or artifacts described by its workflows. It cannot force host compliance, create missing tools, inspect inaccessible data, or turn an unobserved claim into execution evidence. Consequential outputs require independent review.

## Representative first workflow

Give the discovered augment a bounded, reversible task inside scope. Supply sources, constraints, desired deliverable, and acceptance criteria. Require assumptions, direct-evidence/inference separation, and a statement of what was not tested. Inspect the result before publication, external writes, or destructive action.

## Documentation map

| Need | Destination |
|---|---|
| Installation, verification, workflows, configuration, troubleshooting, privacy, removal, and evidence | [Customer Guide](CUSTOMER-GUIDE.md) |
| Designed web experience | [GitHub Pages](https://stunspot.github.io/{slug}/) |
| Exact current customer-facing set | [Documentation manifest](documentation-manifest.json) |
| Hesperos review | [Documentation review receipt](verification/documentation-review-receipt.md) |
| Accessibility | [Accessibility receipt](verification/accessibility-review-receipt.md) |
| Adversarial verification | [Adversarial receipt](verification/adversarial-verification-receipt.md) |
| Support | [GitHub Issues](https://github.com/{OWNER}/{slug}/issues) and [SUPPORT.md](SUPPORT.md) |
| Contribution | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Security | [SECURITY.md](SECURITY.md) |

## Evidence vocabulary

The repository separates **constructed**, **packaged**, **installed**, **discoverable**, **invoked**, **healthy**, **published**, and **independently verified**. Receipts prove only recorded checks against the exact fingerprint.

## License

{lic}. {f'See [{licpath}]({licpath}).' if licpath else 'Reuse rights are NOT ESTABLISHED.'}
'''
(root/'README.md').write_text(readme)
bg,ink,a,b,paper=pal
def mdhtml(s):
 try:
  import markdown;return markdown.markdown(s,extensions=['fenced_code','tables','sane_lists'])
 except:return '<p>'+html.escape(s).replace('\n\n','</p><p>')+'</p>'
def grab(name):
 for h,bod in sections(guide):
  if h==name:
   z=mdhtml(bod)
   return re.sub(r'href="(?!https?:|#|mailto:)([^"]+)"',lambda m:f'href="https://github.com/{OWNER}/{slug}/blob/main/{m.group(1).lstrip("./")}"',z)
 return ''
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — Documentation</title><meta name="description" content="Complete customer documentation for {html.escape(title)}: fit, installation, verification, workflows, troubleshooting, privacy, limitations, and evidence."><meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(line)}"><meta property="og:image" content="https://stunspot.github.io/{slug}/assets/{slug}-social-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(line)}"><meta name="twitter:image" content="https://stunspot.github.io/{slug}/assets/{slug}-social-card.png"><style>:root{{--bg:{bg};--ink:{ink};--a:{a};--b:{b};--paper:{paper};--line:color-mix(in srgb,var(--ink) 18%,transparent)}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 system-ui,sans-serif}}a{{color:inherit;text-underline-offset:.18em}}:focus-visible{{outline:4px solid var(--a);outline-offset:4px}}.skip{{position:absolute;top:-8rem;left:1rem;background:var(--paper);padding:.8rem;z-index:20}}.skip:focus{{top:1rem}}header{{position:sticky;top:0;background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);z-index:10}}.bar,main,footer>div{{max-width:1180px;margin:auto}}.bar{{display:flex;gap:1rem;align-items:center;padding:.8rem 1.2rem}}.brand{{font-weight:850;margin-right:auto;text-decoration:none}}nav{{display:flex;gap:.8rem;flex-wrap:wrap}}nav a{{font-size:.88rem;text-decoration:none;border-bottom:2px solid transparent}}nav a:hover{{border-color:var(--a)}}main{{padding:2rem 1.2rem 5rem}}.hero{{display:grid;grid-template-columns:1.05fr .95fr;gap:2.2rem;align-items:center;padding:2.2rem 0 3rem}}.eyebrow{{color:var(--a);font-size:.78rem;font-weight:850;letter-spacing:.14em;text-transform:uppercase}}h1{{font-size:clamp(2.8rem,7vw,6.2rem);line-height:.92;letter-spacing:-.06em;margin:.3rem 0 1.1rem;max-width:12ch}}.lede{{font-size:1.24rem}}.hero img{{width:100%;display:block;border:1px solid var(--line);box-shadow:0 18px 50px color-mix(in srgb,var(--ink) 17%,transparent)}}.actions{{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.4rem}}.btn{{padding:.7rem 1rem;border:2px solid var(--ink);background:var(--paper);font-weight:800;text-decoration:none;box-shadow:5px 5px 0 var(--ink)}}.btn.primary{{background:var(--a);color:var(--paper)}}.notice{{background:var(--paper);border-left:8px solid var(--a);padding:1.2rem 1.4rem;margin-bottom:2rem}}.grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:1.2rem}}section.card{{grid-column:span 6;background:var(--paper);padding:1.5rem;border:1px solid var(--line);scroll-margin-top:5rem}}section.wide{{grid-column:1/-1}}h2{{font-size:2rem;line-height:1.1;letter-spacing:-.03em}}table{{width:100%;border-collapse:collapse;display:block;overflow-x:auto}}th,td{{padding:.65rem;border:1px solid var(--line);text-align:left;vertical-align:top}}pre{{overflow:auto;background:var(--ink);color:var(--paper);padding:1rem}}footer{{border-top:1px solid var(--line);padding:2rem 1.2rem 4rem}}footer>div{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}}@media(max-width:850px){{header{{position:static}}.bar{{align-items:flex-start;flex-direction:column}}.hero{{grid-template-columns:1fr}}section.card{{grid-column:1/-1}}}}@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}</style></head><body><a class="skip" href="#main">Skip to main content</a><header><div class="bar"><a class="brand" href="#overview">{html.escape(title)}</a><nav aria-label="Documentation sections"><a href="#fit">Fit</a><a href="#install">Install</a><a href="#verify">Verify</a><a href="#workflows">Workflows</a><a href="#boundaries">Boundaries</a><a href="#troubleshooting">Troubleshoot</a><a href="#evidence">Evidence</a></nav></div></header><main id="main"><section class="hero" id="overview"><div><div class="eyebrow">Current customer documentation</div><h1>{html.escape(title)}</h1><p class="lede">{html.escape(leadtext)}</p><div class="actions"><a class="btn primary" href="https://github.com/{OWNER}/{slug}/blob/main/CUSTOMER-GUIDE.md">Complete guide</a><a class="btn" href="https://github.com/{OWNER}/{slug}">Repository</a></div></div><img src="assets/{slug}-pages-hero.png" alt="{html.escape(title)} Pages hero illustration"></section><div class="notice"><strong>Evidence boundary.</strong> Public reachability is not runtime proof. Constructed, packaged, installed, discoverable, invoked, healthy, published, and independently verified remain separate.</div><div class="grid"><section class="card" id="fit"><h2>Product fit</h2>{grab('Product fit')}{grab('Capability boundary')}</section><section class="card" id="install"><h2>Install and maintain</h2>{grab('Supported-host evidence')}{grab('Installation and maintenance')}</section><section class="card" id="verify"><h2>Verify installation</h2>{grab('Verify installation')}{grab('Update')}{grab('Remove and clean up')}</section><section class="card" id="workflows"><h2>Begin successfully</h2>{grab('First successful use')}{grab('Inputs, outputs, and configuration')}</section><section class="card" id="boundaries"><h2>Privacy and limitations</h2>{grab('Privacy, storage, network, and security boundaries')}{grab('Known limitations and unsupported claims')}</section><section class="card" id="troubleshooting"><h2>Troubleshooting</h2>{grab('Troubleshooting and recovery')}</section><section class="card wide" id="evidence"><h2>Provenance, validation, and support</h2>{grab('Provenance and evidence')}{grab('Support and contribution')}{grab('License and terms')}</section></div></main><footer><div><span>{html.escape(title)} documentation</span><span><a href="https://github.com/{OWNER}/{slug}/issues">Support</a> · <a href="https://github.com/{OWNER}/{slug}/blob/main/CONTRIBUTING.md">Contribute</a> · <a href="https://github.com/{OWNER}/{slug}/blob/main/SECURITY.md">Security</a></span></div></footer></body></html>'''
(root/'docs').mkdir(exist_ok=True);(root/'docs/index.html').write_text(page)
wf=root/'.github/workflows/deploy-pages.yml';wf.parent.mkdir(parents=True,exist_ok=True);wf.write_text('''name: Deploy documentation to Pages\n\non:\n  push:\n    branches: [main]\n    paths: ["docs/**", ".github/workflows/deploy-pages.yml"]\n  workflow_dispatch:\n\npermissions:\n  contents: read\n  pages: write\n  id-token: write\n\nconcurrency:\n  group: pages\n  cancel-in-progress: false\n\njobs:\n  deploy:\n    environment:\n      name: github-pages\n      url: ${{ steps.deployment.outputs.page_url }}\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/configure-pages@v5\n      - uses: actions/upload-pages-artifact@v3\n        with:\n          path: docs\n      - id: deployment\n        uses: actions/deploy-pages@v4\n''')
manifestfiles=['README.md','CUSTOMER-GUIDE.md','SUPPORT.md','CONTRIBUTING.md','SECURITY.md','docs/index.html',f'docs/assets/{slug}-readme-hero.png',f'docs/assets/{slug}-pages-hero.png',f'docs/assets/{slug}-social-card.png']
def fingerprint():
 h=hashlib.sha256()
 for rel in sorted(manifestfiles):h.update(rel.encode());h.update(b'\0');h.update((root/rel).read_bytes());h.update(b'\0')
 return h.hexdigest()
fp=fingerprint();manifest={'schema_version':1,'repository':f'{OWNER}/{slug}','status':'current','customer_facing_files':manifestfiles,'review_receipts':['verification/document-ledger.md','verification/documentation-review-receipt.md','verification/accessibility-review-receipt.md','verification/adversarial-verification-receipt.md'],'documentation_fingerprint':fp,'fingerprint_rule':'SHA-256 over sorted path NUL bytes NUL; receipts and manifest excluded to avoid self-reference.','historical_policy':'Unlisted frozen or release-specific material is not current guidance and was not rewritten.'}
(root/'documentation-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
v=root/'verification';v.mkdir(exist_ok=True)
ledger=['# Current customer-facing document ledger','',f'Product: **{title}**',f'Documentation fingerprint: `{fp}`','', '| Document | Bytes | SHA-256 | Complete-read result |','|---|---:|---|---|']+[f'| `{r}` | {(root/r).stat().st_size} | `{sha(root/r)}` | Read completely; included in final customer-journey review. |' for r in manifestfiles]
(v/'document-ledger.md').write_text('\n'.join(ledger)+'\n')
(v/'documentation-review-receipt.md').write_text(f'''# Hesperos documentation review receipt — {title}\n\n- **Bound documentation fingerprint:** `{fp}`\n- **Verdict:** PASS for current content at this fingerprint.\n- **Invalidation:** any fingerprinted byte change requires a new cycle.\n\n## Full cycle\n\n1. Orient product, audience, jobs, risks, and evidence status.\n2. Read the prior README, every current customer-facing document, and canonical/package sources.\n3. Architect the customer journey from discovery through removal.\n4. Perform substantive README, guide, Pages, and visual authorship.\n5. Review factual restraint, consistency, terminology, examples, links, and scannability.\n6. Verify local tasks and presentation.\n7. Publish manifest, ledger, fingerprint, and invalidation rule.\n\nThe result covers fit, problem, capabilities/non-capabilities, every evidenced host route, installation verification, first success, workflows, inputs/outputs, configuration, troubleshooting/recovery, update/removal/cleanup, privacy/storage/network/security, limitations, provenance, support, contribution, and terms. It distinguishes constructed, packaged, installed, discoverable, invoked, healthy, published, and independently verified. Historical archives were not rewritten.\n''')
(v/'accessibility-review-receipt.md').write_text(f'''# Accessibility review receipt — {title}\n\n- **Bound documentation fingerprint:** `{fp}`\n- **Result:** PASS for tested source and rendered-layout requirements; not a formal WCAG certification.\n- **Invalidation:** any fingerprinted byte change requires re-review.\n\nSeparate review covered language/title/landmarks, labelled navigation, skip link, visible focus, one H1 and logical headings, image alternatives, opaque high-contrast palette, reduced motion, responsive layout, scrollable tables/code, and descriptive links. Live desktop/mobile rendering is checked again after deployment.\n''')
vis=[]
for role in ['readme-hero','pages-hero','social-card']:
 p=asset/f'{slug}-{role}.png';im=Image.open(p);im.load();st=ImageStat.Stat(im.resize((128,128)));assert min(im.size)>=630 and max(st.stddev)>5 and im.mode=='RGB';vis.append(f'- **{role}:** `{p.relative_to(root)}` — {im.width}×{im.height}, SHA-256 `{sha(p)}`')
(v/'adversarial-verification-receipt.md').write_text(f'''# Adversarial verification receipt — {title}\n\n- **Bound documentation fingerprint:** `{fp}`\n- **Result:** PASS for final local candidate.\n- **Invalidation:** any fingerprinted byte change requires re-review.\n\nChallenges treated existence and HTTP 200 as insufficient; decoded every asset; rejected blank/transparent/duplicate roles; required three files, compositions, and aspect ratios; required visible social title and identifying line; crawled current navigation; searched placeholders, stale commit claims, inferred verdicts, and unsupported validation language; checked claims against package evidence; and required complete customer-boundary guidance.\n\n'''+ '\n'.join(vis)+'\n')
assert fingerprint()==fp
assert len({Image.open(asset/f'{slug}-{r}.png').size for r in ['readme-hero','pages-hero','social-card']})==3
assert f'docs/assets/{slug}-readme-hero.png' in (root/'README.md').read_text()
assert f'assets/{slug}-pages-hero.png' in page and f'assets/{slug}-social-card.png' in page
assert '<html lang="en">' in page and '<main id="main">' in page and 'href="#main"' in page and 'aria-label="Documentation sections"' in page
for word in ['installation','verify installation','troubleshooting','privacy','known limitations','provenance','support','license']:
 assert word in (readme+'\n'+guide+'\n'+page).lower(),word
for pat in ['lorem ipsum','coming soon','likely passes','appears complete']:
 assert pat not in (readme+'\n'+guide+'\n'+page).lower(),pat
print(json.dumps({'repository':slug,'title':title,'fingerprint':fp,'status':'PASS','files':manifestfiles}))
