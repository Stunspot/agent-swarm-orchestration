#!/usr/bin/env python3
"""Validate current public surfaces and immutable 0.2.0 archive custody."""

from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.0"
SKILL = ROOT / "canonical" / "skills" / "agent-swarm-orchestration"
TOP_LEVEL = "agent-swarm-orchestration/"


def files(root: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if (
            not path.is_file()
            or "__pycache__" in rel.parts
            or path.suffix in {".pyc", ".pyo"}
        ):
            continue
        result[rel.as_posix()] = path.read_bytes()
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def read_archive(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert names, f"empty archive: {path}"
        assert all("\\" not in name for name in names), f"backslash member: {path}"
        assert all(name.startswith(TOP_LEVEL) for name in names), f"wrong top level: {path}"
        return {name.split("/", 1)[1]: archive.read(name) for name in names}


def validate_custody_record(record: dict[str, object]) -> tuple[Path, dict[str, bytes]]:
    path = ROOT / str(record["path"])
    assert path.is_file(), f"missing archive: {path}"
    assert sha256(path) == record["sha256"], f"archive hash drift: {path}"
    assert path.stat().st_size == record["size"], f"archive size drift: {path}"
    extracted = read_archive(path)
    assert len(extracted) == record["member_count"], f"archive member-count drift: {path}"
    assert record["top_level"] == TOP_LEVEL.rstrip("/"), f"custody top-level drift: {path}"
    assert record["members_use_posix_paths"] is True, f"custody path claim drift: {path}"
    return path, extracted


def validate_skill_archive(record: dict[str, object], canonical: dict[str, bytes]) -> None:
    path, extracted = validate_custody_record(record)
    assert extracted == canonical, f"frozen skill archive parity failed: {path}"


def validate_plugin_archive(record: dict[str, object], canonical: dict[str, bytes]) -> None:
    """Validate the frozen plugin without forcing mutable listing art to match it."""

    path, extracted = validate_custody_record(record)
    prefix = "skills/agent-swarm-orchestration/"
    archived_runtime = {
        name[len(prefix) :]: data
        for name, data in extracted.items()
        if name.startswith(prefix)
    }
    assert archived_runtime == canonical, f"frozen plugin runtime parity failed: {path}"

    plugin = json.loads(extracted[".codex-plugin/plugin.json"].decode("utf-8"))
    assert plugin["name"] == "agent-swarm-orchestration"
    assert plugin["version"] == VERSION
    assert plugin["skills"] == "./skills/"
    for key in ("composerIcon", "logo"):
        asset_path = plugin["interface"][key].removeprefix("./")
        assert asset_path in extracted, f"frozen plugin asset missing: {key}"


def main() -> int:
    package = json.loads((ROOT / "package-manifest.json").read_text(encoding="utf-8"))
    assert package["version"] == VERSION
    assert package["status"] in {"public-release-candidate", "public-release-published"}

    canonical = files(SKILL)
    for target in [
        ROOT / "release" / "codex" / "agent-swarm-orchestration",
        ROOT / "release" / "claude" / "agent-swarm-orchestration",
        ROOT / "plugins" / "agent-swarm-orchestration" / "skills" / "agent-swarm-orchestration",
    ]:
        assert files(target) == canonical, f"runtime parity failed: {target}"

    plugin = json.loads(
        (
            ROOT
            / "plugins"
            / "agent-swarm-orchestration"
            / ".codex-plugin"
            / "plugin.json"
        ).read_text(encoding="utf-8")
    )
    assert plugin["name"] == "agent-swarm-orchestration"
    assert plugin["version"] == VERSION
    assert plugin["skills"] == "./skills/"
    for key in ("composerIcon", "logo"):
        assert (
            ROOT / "plugins" / "agent-swarm-orchestration" / plugin["interface"][key]
        ).resolve().is_file()

    expected_sizes = {
        ROOT / "docs" / "assets" / "aso-readme-banner.png": (1280, 640),
        ROOT / "docs" / "assets" / "aso-pages-hero.png": (1600, 900),
        ROOT / "docs" / "assets" / "aso-social-card.png": (1200, 630),
        ROOT / "plugins" / "agent-swarm-orchestration" / "assets" / "aso-icon.png": (512, 512),
        ROOT / "plugins" / "agent-swarm-orchestration" / "assets" / "aso-social-card.png": (1200, 630),
    }
    for path, expected in expected_sizes.items():
        assert png_size(path) == expected, f"wrong dimensions: {path} {png_size(path)} != {expected}"

    docs = json.loads((ROOT / "documentation-manifest.json").read_text(encoding="utf-8"))
    for rel in docs["reader_journey"]:
        assert (ROOT / rel).is_file(), f"missing documentation: {rel}"
    for rel in docs["customer_docs"]:
        assert (ROOT / rel).is_file(), f"missing customer documentation: {rel}"
    for item in docs["visual_assets"]:
        path = ROOT / item["path"]
        assert png_size(path) == (item["width"], item["height"])

    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for token in (
        "Skip to content",
        'width="1600"',
        'height="900"',
        "aso-social-card.png",
        "og:image:width",
        "og:image:height",
        "Complete documentation journey",
    ):
        assert token in html, f"site token missing: {token}"

    custody_path = ROOT / "release-assets" / f"v{VERSION}" / "archive-custody.json"
    custody = json.loads(custody_path.read_text(encoding="utf-8"))
    assert custody["version"] == VERSION
    records = {record["path"]: record for record in custody["archives"]}
    plugin_path = f"release-assets/v{VERSION}/Plugin-Agent-Swarm-Orchestration-v{VERSION}.zip"
    skill_path = f"release-assets/v{VERSION}/Skill-agent-swarm-orchestration-v{VERSION}.zip"
    claude_path = f"claude-ai/agent-swarm-orchestration-v{VERSION}.zip"
    validate_plugin_archive(records[plugin_path], canonical)
    validate_skill_archive(records[skill_path], canonical)
    validate_skill_archive(records[claude_path], canonical)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(SKILL / "tests"), "-v"],
        cwd=ROOT,
    )
    assert result.returncode == 0, "validator tests failed"

    print("PUBLIC RELEASE VALID agent-swarm-orchestration v0.2.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())