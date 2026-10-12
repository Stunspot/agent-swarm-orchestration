#!/usr/bin/env python3
"""Build a portable customer kit; use build_candidate.py for complete versioned custody."""
from __future__ import annotations
import argparse,hashlib,json,shutil
from pathlib import Path
from archive_paths import assert_chain,assert_unlinked,check_tree,atomic_zip
ROOT=Path(__file__).resolve().parents[1]
DOCS=('README.md','START-HERE.md','INSTALLATION.md','WORKFLOWS.md','SUPPORT.md','TROUBLESHOOTING.md','TRUST-AND-LIMITS.md','SECURITY.md','LICENSE.md','ATTRIBUTION.md','DATA-AND-PRIVACY.md','TERMS-OF-USE.md','TRADEMARKS.md','provenance.md','host-matrix.md','CONTRIBUTING.md','ARCHIVE-CUSTODY.md','PLAN-VALIDATION.md')
def preflight():
    assert_chain(ROOT)
    assert_chain(ROOT/'package-manifest.json');assert_chain(ROOT/'documentation-manifest.json')
    m=json.loads((ROOT/'package-manifest.json').read_text(encoding='utf-8'))
    docs=json.loads((ROOT/'documentation-manifest.json').read_text(encoding='utf-8'))
    names=sorted(set(DOCS)|set(docs['reader_journey'])|set(docs['historical_customer_docs']))
    for name in names:
        if not isinstance(name,str) or Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError(f"customer document escapes source: {name}")
    files=[ROOT/name for name in names]+[ROOT/'.agents/plugins/marketplace.json',ROOT/'package-manifest.json',ROOT/'tools/verify_package.py',ROOT/'tools/archive_paths.py']
    for path in files:
        assert_chain(path)
        if not path.is_file():raise ValueError(f'not a regular source file: {path}')
    # Only selected trees are in scope; unrelated evidence/archive directories are not copied.
    for source in [ROOT/'plugins/agent-swarm-orchestration',ROOT/'docs']:
        assert_unlinked(source)
        files.extend(p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'})
    from archive_paths import check_members
    check_members([(p.relative_to(ROOT).as_posix(),p.read_bytes()) for p in files])
    return m,names

def build(stage,target,claude_source):
    m,names=preflight();version=m['version']
    stage=assert_chain(stage,allow_missing=True)
    assert_chain(claude_source)
    if stage.exists():raise ValueError('Refusing existing customer staging directory')
    if target.exists():raise ValueError('Refusing existing customer archive')
    (stage/'codex/.agents/plugins').mkdir(parents=True)
    shutil.copy2(ROOT/'.agents/plugins/marketplace.json',stage/'codex/.agents/plugins/marketplace.json')
    shutil.copytree(ROOT/'plugins/agent-swarm-orchestration',stage/'codex/plugins/agent-swarm-orchestration',ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo'))
    (stage/'claude').mkdir();claude=f'agent-swarm-orchestration-v{version}.zip';shutil.copy2(claude_source,stage/'claude'/claude)
    for name in names:shutil.copy2(ROOT/name,stage/name)
    shutil.copytree(ROOT/'docs',stage/'docs')
    for name in names:
        file=stage/name;t=file.read_text(encoding='utf-8')
        if name=='README.md':
            # Source history and the current supplied archive have different custody.
            # Rewrite the whole map entry before translating installation paths.
            historical=f'- `claude-ai/{claude}` — current one-skill archive matching this release.'
            current=f'- `claude/{claude}` — current supplied one-skill archive, byte-matched to this kit’s runtime.'
            if t.count(historical)!=1:raise ValueError('Missing exact source current Claude map entry')
            t=t.replace(historical,current)
        t=t.replace('release/codex/agent-swarm-orchestration/','codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration/').replace('release/claude/agent-swarm-orchestration/',f'the extracted agent-swarm-orchestration/ folder from claude/{claude}')
        if name=='INSTALLATION.md':t=t.replace('codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration','codex plugin marketplace add "/path/to/extracted-kit/codex" --json')
        file.write_text(t,encoding='utf-8',newline='\n')
    (stage/'tools').mkdir()
    for name in ['verify_package.py','archive_paths.py']:shutil.copy2(ROOT/'tools'/name,stage/'tools'/name)
    (stage/'provenance').mkdir();shutil.copy2(ROOT/'package-manifest.json',stage/'provenance/repository-package-manifest.json')
    m['source_manifest']='provenance/repository-package-manifest.json';m['custody']='customer-kit derivative; historical evidence retained separately in source repository'
    m['distributions']={'codex_plugin':{'path':'codex/plugins/agent-swarm-orchestration','marketplace':'codex/.agents/plugins/marketplace.json'},'codex_standalone':{'path':'codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration'},'claude_standalone':{'archive':f'claude/{claude}'},'customer_documentation':{'entrypoint':'START-HERE.md','installation':'INSTALLATION.md','host_matrix':'host-matrix.md'}}
    for key in ('map','build_state','release_baseline','canonical_skills','canonical_evals','customer_docs_manifest'):m.pop(key,None)
    (stage/'package-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    paths=[p for p in stage.rglob('*') if p.is_file()]
    custody={'format':'aso-customer-custody/v1','version':version,'files':{p.relative_to(stage).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)},'verification_boundary':'Exact bytes and channel parity; no installation, model behavior or evidence authenticity claim.'}
    (stage/'package-custody.json').write_text(json.dumps(custody,indent=2)+'\n',encoding='utf-8')
    entries=check_tree(stage,[p for p in stage.rglob('*') if p.is_file()],f'agent-swarm-orchestration-v{version}')
    atomic_zip(entries,target)
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix('.zip.sha256').write_text(f'{digest.upper()}  {target.name}\n',encoding='utf-8')
    return {'version':version,'zip':str(target),'sha256':digest,'files':len(paths)+1}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--claude-archive',type=Path);a=p.parse_args()
    version=json.loads((ROOT/'package-manifest.json').read_text())['version']
    target=a.output or ROOT/f'release-assets/v{version}/Agent-Swarm-Orchestration-v{version}.zip'
    claude=a.claude_archive or ROOT/f'claude-ai/agent-swarm-orchestration-v{version}.zip'
    print(json.dumps(build(a.stage,target,claude),indent=2))
if __name__=='__main__':main()
