#!/usr/bin/env python3
"""Validate public distribution, documentation, image, and archive custody surfaces."""

from __future__ import annotations

import json
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.2"
SKILL = ROOT / "canonical" / "skills" / "agent-swarm-orchestration"


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


def image_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    assert data[:2] == b"\xff\xd8", f"unsupported image format: {path}"
    offset = 2
    sof_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while offset < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9}:
            continue
        length = struct.unpack(">H", data[offset:offset + 2])[0]
        if marker in sof_markers:
            height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
            return width, height
        offset += length
    raise AssertionError(f"JPEG dimensions not found: {path}")
def validate_zip(path: Path, expected_tree: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert names, f"empty archive: {path}"
        assert all("\\" not in name for name in names), f"backslash member: {path}"
        assert all(name.startswith("agent-swarm-orchestration/") for name in names), f"wrong top level: {path}"
        extracted = {name.split("/", 1)[1]: archive.read(name) for name in names}
        assert extracted == expected_tree, f"archive parity failed: {path}"


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

    plugin = json.loads((ROOT / "plugins" / "agent-swarm-orchestration" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "agent-swarm-orchestration"
    assert plugin["version"] == VERSION
    assert plugin["skills"] == "./skills/"
    for key in ("composerIcon", "logo"):
        assert (ROOT / "plugins" / "agent-swarm-orchestration" / plugin["interface"][key]).resolve().is_file()

    expected_sizes = {
        ROOT / "docs" / "assets" / "aso-readme-banner.png": (1280, 640),
        ROOT / "docs" / "assets" / "aso-pages-hero.png": (1600, 900),
        ROOT / "docs" / "assets" / "aso-social-card.jpg": (1730, 909),
        ROOT / "plugins" / "agent-swarm-orchestration" / "assets" / "aso-icon.png": (512, 512),
        ROOT / "plugins" / "agent-swarm-orchestration" / "assets" / "aso-social-card.png": (1586, 992),
    }
    for path, expected in expected_sizes.items():
        assert image_size(path) == expected, f"wrong dimensions: {path} {image_size(path)} != {expected}"

    docs = json.loads((ROOT / "documentation-manifest.json").read_text(encoding="utf-8"))
    for rel in docs["reader_journey"]:
        assert (ROOT / rel).is_file(), f"missing documentation: {rel}"
    for item in docs["visual_assets"]:
        path = ROOT / item["path"]
        assert image_size(path) == (item["width"], item["height"])

    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for token in ("Skip to content", 'width="1600"', 'height="900"', "aso-social-card.jpg", "image/jpeg", "twitter:image:alt", "og:image:width", "og:image:height"):
        assert token in html, f"site token missing: {token}"

    custody_path = ROOT / "release-assets" / f"v{VERSION}" / "archive-custody.json"
    custody = json.loads(custody_path.read_text(encoding="utf-8"))
    assert custody["version"] == VERSION
    validate_zip(ROOT / "release-assets" / f"v{VERSION}" / f"Plugin-Agent-Swarm-Orchestration-v{VERSION}.zip", files(ROOT / "plugins" / "agent-swarm-orchestration"))
    validate_zip(ROOT / "release-assets" / f"v{VERSION}" / f"Skill-agent-swarm-orchestration-v{VERSION}.zip", canonical)
    validate_zip(ROOT / "claude-ai" / f"agent-swarm-orchestration-v{VERSION}.zip", canonical)

    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(SKILL / "tests"), "-v"], cwd=ROOT)
    assert result.returncode == 0, "validator tests failed"

    print("PUBLIC RELEASE VALID agent-swarm-orchestration v0.2.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
