#!/usr/bin/env python3
"""Build the complete versioned customer kit from current host packages."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
ROOT=Path(__file__).resolve().parents[1]
DOCS=('README.md','START-HERE.md','INSTALLATION.md','WORKFLOWS.md','SUPPORT.md','TROUBLESHOOTING.md','TRUST-AND-LIMITS.md','SECURITY.md','LICENSE.md','ATTRIBUTION.md','DATA-AND-PRIVACY.md','TERMS-OF-USE.md','TRADEMARKS.md','provenance.md','host-matrix.md')
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',type=Path,required=True);args=p.parse_args()
 stage=args.stage.resolve();m=json.loads((ROOT/'package-manifest.json').read_text(encoding='utf-8'));version=m['version']
 target=ROOT/f'release-assets/v{version}/Agent-Swarm-Orchestration-v{version}.zip'
 if stage.exists() or target.exists():raise RuntimeError('Refusing to overwrite stage or versioned customer archive')
 (stage/'codex/.agents/plugins').mkdir(parents=True)
 shutil.copy2(ROOT/'.agents/plugins/marketplace.json',stage/'codex/.agents/plugins/marketplace.json')
 shutil.copytree(ROOT/'plugins/agent-swarm-orchestration',stage/'codex/plugins/agent-swarm-orchestration',ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo'))
 (stage/'claude').mkdir();claude=f'agent-swarm-orchestration-v{version}.zip';shutil.copy2(ROOT/'claude-ai'/claude,stage/'claude'/claude)
 for name in (*DOCS,f'RELEASE-NOTES-v{version}.md'):shutil.copy2(ROOT/name,stage/name)
 shutil.copytree(ROOT/'docs',stage/'docs')
 for name in ('START-HERE.md','INSTALLATION.md'):
  file=stage/name;t=file.read_text(encoding='utf-8');t=t.replace('release/codex/agent-swarm-orchestration/','codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration/').replace('release/claude/agent-swarm-orchestration/',f'the extracted agent-swarm-orchestration/ folder from claude/{claude}').replace('claude-ai/','claude/')
  if name=='INSTALLATION.md':t=t.replace('codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration','codex plugin marketplace add "/path/to/extracted-kit/codex" --json')
  file.write_text(t,encoding='utf-8',newline='\n')
 (stage/'provenance').mkdir();shutil.copy2(ROOT/'package-manifest.json',stage/'provenance/repository-package-manifest.json')
 m['source_manifest']='provenance/repository-package-manifest.json';m['custody']='customer-kit derivative; repository source and historical evidence retained separately'
 m['distributions']={'codex_plugin':{'path':'codex/plugins/agent-swarm-orchestration','marketplace':'codex/.agents/plugins/marketplace.json'},'codex_standalone':{'path':'codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration'},'claude_standalone':{'archive':f'claude/{claude}'},'customer_documentation':{'entrypoint':'START-HERE.md','installation':'INSTALLATION.md','host_matrix':'host-matrix.md'}}
 for key in ('map','build_state','release_baseline','canonical_skills','canonical_evals','customer_docs_manifest'):m.pop(key,None)
 (stage/'package-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED) as z:
  for file in sorted((p for p in stage.rglob('*') if p.is_file()),key=lambda p:p.relative_to(stage).as_posix()):
   name=f'agent-swarm-orchestration-v{version}/'+file.relative_to(stage).as_posix();i=zipfile.ZipInfo(name,(2026,9,5,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,file.read_bytes())
 digest=hashlib.sha256(target.read_bytes()).hexdigest().upper();target.with_suffix('.zip.sha256').write_text(f'{digest}  {target.name}\n',encoding='utf-8',newline='\n')
 print(json.dumps({'version':version,'zip':str(target),'sha256':digest,'stage':str(stage)}))
if __name__=='__main__':main()