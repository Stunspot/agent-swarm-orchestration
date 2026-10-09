#!/usr/bin/env python3
"""Build all 0.3.1 restoration channels together in a new directory; never replaces releases."""
import argparse,hashlib,json,os,tempfile
from pathlib import Path
import build_release as release
import build_customer_kit as customer
from archive_paths import assert_chain,check_tree
def build(output):
    output=assert_chain(output,allow_missing=True)
    if not output.is_relative_to(release.ROOT):raise ValueError("candidate must remain under the source repository")
    if os.path.lexists(output):raise ValueError(f'refusing existing candidate: {output}')
    output.parent.mkdir(parents=True,exist_ok=True)
    customer.preflight()
    package=json.loads((release.ROOT/'package-manifest.json').read_text())
    if package['version']!=release.VERSION or package['runtime_version']!=release.VERSION:raise ValueError('release identity mismatch')
    if release.tree_digest(release.SKILL_SOURCE)!=package['runtime_fingerprint']:raise ValueError('canonical fingerprint mismatch')
    from sync_runtime_trees import parity,DESTINATIONS
    if not all(parity(p)['valid'] for p in DESTINATIONS.values()):raise ValueError('canonical runtime mirror mismatch')
    # Staging lives on the destination volume. No final directory exists until every channel passes.
    with tempfile.TemporaryDirectory(prefix='.aso-candidate-',dir=output.parent) as temporary:
        staging=Path(temporary);bundle=staging/'bundle';bundle.mkdir()
        # build_zip records repository-relative paths; this staging directory must stay in repository custody.
        records=[]
        for source,name in [(release.PLUGIN_SOURCE,f'Plugin-Agent-Swarm-Orchestration-v{release.VERSION}.zip'),(release.SKILL_SOURCE,f'Skill-agent-swarm-orchestration-v{release.VERSION}.zip'),(release.SKILL_SOURCE,f'claude/agent-swarm-orchestration-v{release.VERSION}.zip')]:
            record=release.build_zip(source,bundle/name,'agent-swarm-orchestration')
            record['path']=name;records.append(record)
        kit=bundle/f'Agent-Swarm-Orchestration-v{release.VERSION}.zip'
        customer_record=customer.build(staging/'customer',kit,bundle/f'claude/agent-swarm-orchestration-v{release.VERSION}.zip')
        import verify_package
        customer_record['check']=verify_package.verify(staging/'customer');customer_record['zip']=kit.name
        custody={'format':'cd-augment-archive-custody/v1','product':'agent-swarm-orchestration','version':release.VERSION,'generated_at':'2026-10-06','archives':records,'customer':customer_record}
        (bundle/'archive-custody.json').write_text(json.dumps(custody,indent=2)+'\n',encoding='utf-8')
        (bundle/'checksums.sha256').write_text(''.join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(bundle).as_posix()}\n" for p in sorted(bundle.rglob('*.zip'))),encoding='utf-8')
        check_tree(bundle,[p for p in bundle.rglob('*') if p.is_file()])
        if os.path.lexists(output):raise ValueError('candidate appeared during build; preserving it')
        os.rename(bundle,output)
    return {'candidate':str(output),'customer_sha256':hashlib.sha256((output/kit.name).read_bytes()).hexdigest()}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    try:print(json.dumps(build(a.output_dir),indent=2))
    except (OSError,ValueError,RuntimeError) as e:print(f'BUILD FAILED: {e}');return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
