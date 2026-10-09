#!/usr/bin/env python3
"""Verify this extracted kit's bytes and nested skill parity, not activation or behavior."""
import argparse,hashlib,json,sys,zipfile
from pathlib import Path
from archive_paths import assert_unlinked,check_tree,check_members
def verify(root):
    root=assert_unlinked(root)
    custody=json.loads((root/'package-custody.json').read_text(encoding='utf-8'))
    expected=custody['files']
    actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'} and p.relative_to(root).as_posix()!='package-custody.json'}
    if set(actual)!=set(expected):raise ValueError('file set mismatch')
    for name,path in actual.items():
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected[name]:raise ValueError(f'hash mismatch: {name}')
    check_tree(root,list(actual.values()))
    skill=root/'codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration'
    source={p.relative_to(skill).as_posix():p.read_bytes() for p in skill.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'}}
    with zipfile.ZipFile(root/f"claude/agent-swarm-orchestration-v{custody['version']}.zip") as z:
        entries=[(i.filename,z.read(i)) for i in z.infolist() if not i.is_dir()]
        check_members(entries)
        prefix='agent-swarm-orchestration/'
        if any(not n.startswith(prefix) for n,_ in entries):raise ValueError('wrong Claude top level')
        if {n[len(prefix):]:b for n,b in entries}!=source:raise ValueError('Claude/Codex runtime mismatch')
    return {'valid':True,'files':len(actual),'runtime_files':len(source),'boundary':'Exact package bytes and channel parity only'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
    try:print(json.dumps(verify(a.root),indent=2))
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as e:print(f'INVALID: {e}');return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
