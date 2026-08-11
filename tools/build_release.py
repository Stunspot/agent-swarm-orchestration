#!/usr/bin/env python3
"""Build deterministic Agent Swarm Orchestration 0.2.1 release archives."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.1"
FIXED_TIME = (2026, 8, 11, 0, 0, 0)
OUT = ROOT / "release-assets" / f"v{VERSION}"
PLUGIN_SOURCE = ROOT / "plugins" / "agent-swarm-orchestration"
SKILL_SOURCE = ROOT / "canonical" / "skills" / "agent-swarm-orchestration"
CLAUDE_OUT = ROOT / "claude-ai" / f"agent-swarm-orchestration-v{VERSION}.zip"


def is_release_file(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return (
        path.is_file()
        and "__pycache__" not in rel.parts
        and path.suffix not in {".pyc", ".pyo"}
    )


def files_under(root: Path) -> list[Path]:
    return sorted(
        (p for p in root.rglob("*") if is_release_file(p, root)),
        key=lambda p: p.relative_to(root).as_posix(),
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in files_under(root):
        rel = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def build_zip(source: Path, target: Path, top_level: str) -> dict[str, object]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    members: list[str] = []
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in files_under(source):
            rel = PurePosixPath(top_level) / PurePosixPath(path.relative_to(source).as_posix())
            name = rel.as_posix()
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
            members.append(name)
    return {
        "path": target.relative_to(ROOT).as_posix(),
        "sha256": sha256_file(target),
        "size": target.stat().st_size,
        "member_count": len(members),
        "top_level": top_level,
        "source": source.relative_to(ROOT).as_posix(),
        "source_tree_sha256": tree_digest(source),
        "members_use_posix_paths": all("\\" not in member for member in members),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plugin_zip = OUT / f"Plugin-Agent-Swarm-Orchestration-v{VERSION}.zip"
    skill_zip = OUT / f"Skill-agent-swarm-orchestration-v{VERSION}.zip"

    records = [
        build_zip(PLUGIN_SOURCE, plugin_zip, "agent-swarm-orchestration"),
        build_zip(SKILL_SOURCE, skill_zip, "agent-swarm-orchestration"),
        build_zip(SKILL_SOURCE, CLAUDE_OUT, "agent-swarm-orchestration"),
    ]
    custody = {
        "format": "cd-augment-archive-custody/v1",
        "product": "agent-swarm-orchestration",
        "version": VERSION,
        "generated_at": "2026-08-11",
        "archives": records,
    }
    custody_path = OUT / "archive-custody.json"
    custody_path.write_text(json.dumps(custody, indent=2) + "\n", encoding="utf-8", newline="\n")

    checksum_lines = [
        f"{record['sha256']}  {Path(str(record['path'])).name}" for record in records if str(record["path"]).startswith("release-assets/")
    ]
    checksum_lines.append(f"{records[2]['sha256']}  ../../{records[2]['path']}")
    (OUT / "checksums.sha256").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps(custody, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
