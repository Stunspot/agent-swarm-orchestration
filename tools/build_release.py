#!/usr/bin/env python3
"""Build deterministic Agent Swarm Orchestration 0.3.1 release archives."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath
from archive_paths import assert_unlinked, check_tree, atomic_zip

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.1"
FIXED_TIME = (2026, 9, 1, 0, 0, 0)
GENERATED_AT = "2026-09-05"
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
    assert_unlinked(root)
    return sorted(
        (path for path in root.rglob("*") if is_release_file(path, root)),
        key=lambda path: path.relative_to(root).as_posix(),
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
    source.relative_to(ROOT)
    target.relative_to(ROOT)
    entries = check_tree(source, files_under(source), top_level)
    atomic_zip(entries, target, FIXED_TIME)
    members = [name for name, _ in entries]
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


def assert_release_ready() -> None:
    package = json.loads((ROOT / "package-manifest.json").read_text(encoding="utf-8"))
    plugin = json.loads((PLUGIN_SOURCE / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if package.get("status") not in {"public-release-candidate", "public-release-published"}:
        raise RuntimeError(f"package status is not release-ready: {package.get('status')}")
    if package.get("version") != VERSION or package.get("runtime_version") != VERSION or plugin.get("version") != VERSION:
        raise RuntimeError(
            "release identity mismatch: "
            f"builder={VERSION} package={package.get('version')} "
            f"runtime={package.get('runtime_version')} plugin={plugin.get('version')}"
        )
    canonical_fingerprint = tree_digest(SKILL_SOURCE)
    if package.get("runtime_fingerprint") != canonical_fingerprint:
        raise RuntimeError(
            f"runtime fingerprint mismatch: manifest={package.get('runtime_fingerprint')} canonical={canonical_fingerprint}"
        )
    if OUT.exists() or CLAUDE_OUT.exists():
        raise RuntimeError(f"refusing to overwrite existing version custody: {OUT} or {CLAUDE_OUT}")


def write_skill_companions(skill_record: dict[str, object]) -> None:
    archive_name = Path(str(skill_record["path"])).name
    expected = str(skill_record["sha256"]).upper()
    checksum_path = OUT / f"{archive_name}.sha256"
    checksum_path.write_text(f"{expected}  {archive_name}\n", encoding="utf-8", newline="\n")
    verify_path = OUT / f"Skill-agent-swarm-orchestration-v{VERSION}-VERIFY.txt"
    verify_text = f"""Agent Swarm Orchestration {VERSION} skill archive verification

Archive: {archive_name}
Expected SHA-256: {expected}

PowerShell:
(Get-FileHash -Algorithm SHA256 .\\{archive_name}).Hash

macOS/Linux:
shasum -a 256 {archive_name}

A matching SHA-256 establishes exact archive byte identity only. It does not establish installation, discovery, invocation, healthy behavior, or publication.
"""
    verify_path.write_text(verify_text, encoding="utf-8", newline="\n")


def main() -> int:
    assert_release_ready()
    OUT.mkdir(parents=True, exist_ok=False)
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
        "generated_at": GENERATED_AT,
        "archives": records,
    }
    custody_path = OUT / "archive-custody.json"
    custody_path.write_text(json.dumps(custody, indent=2) + "\n", encoding="utf-8", newline="\n")

    checksum_lines = [
        f"{record['sha256']}  {Path(str(record['path'])).name}"
        for record in records
        if str(record["path"]).startswith("release-assets/")
    ]
    checksum_lines.append(f"{records[2]['sha256']}  ../../{records[2]['path']}")
    (OUT / "checksums.sha256").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8", newline="\n")
    write_skill_companions(records[1])

    print(json.dumps(custody, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())