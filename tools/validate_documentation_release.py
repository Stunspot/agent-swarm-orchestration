#!/usr/bin/env python3
"""Validate Agent Swarm Orchestration 0.3.2 documentation and presentation custody."""

from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.2"
RUNTIME_FINGERPRINT = "62875296959f3ac6bcfbfc8f7222b10b6293446d33b8de3d097709471cb04732"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def documentation_fingerprint(paths: list[str]) -> tuple[str, list[dict[str, str]]]:
    records = [{"path": rel, "sha256": sha256(ROOT / rel)} for rel in paths]
    mapping = {item["path"]: item["sha256"] for item in records}
    canonical = json.dumps(mapping, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest(), records


def main() -> int:
    docs = read_json("documentation-manifest.json")
    package = read_json("package-manifest.json")
    assert docs["version"] == VERSION
    assert package["version"] == VERSION
    from sync_runtime_trees import tree_fingerprint, SOURCE
    assert package["runtime_fingerprint"] == tree_fingerprint(SOURCE)

    governed = list(docs["customer_docs"]) + ["docs/index.html", "docs/style.css", "documentation-manifest.json"]
    assert len(governed) == len(set(governed)), "duplicate governed documentation path"
    for relative in governed:
        assert (ROOT / relative).is_file(), f"missing governed documentation: {relative}"
    assert docs["reader_journey"][-1] == "RELEASE-NOTES-v0.3.2.md"
    assert "RELEASE-NOTES-v0.2.3.md" in docs["historical_customer_docs"]

    fingerprint, records = documentation_fingerprint(governed)
    assert len(records) == len(governed)

    html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    css = (ROOT / "docs/style.css").read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    hrefs = re.findall(r'\bhref="([^"]+)"', html)
    required_ids = {"top", "main", "product", "shapes", "try", "install", "recover", "trust", "help"}
    assert required_ids <= ids, f"missing Pages sections: {sorted(required_ids - ids)}"
    assert not [href for href in hrefs if href.startswith("#") and href[1:] not in ids]
    assert not [href for href in hrefs if "/blob/" in href and "/blob/main/" not in href]
    for source in re.findall(r'\bsrc="([^"]+)"', html):
        if not source.startswith(("http://", "https://")):
            assert (ROOT / "docs" / source).is_file(), f"missing Pages asset: {source}"
    for token in (
        "What it prevents",
        "Design the organization",
        "Execution kernel",
        "What a good run returns",
        "Install and verify",
        "Troubleshoot and recover",
        "Privacy, security, and evidence",
        "Support and contribution",
        "Agent Swarm Orchestration",
        "image/jpeg",
        "twitter:image:alt",
    ):
        assert token in html, f"Pages journey token missing: {token}"
    for token in (".skip-link", ":focus-visible", "prefers-reduced-motion", "overflow-x: auto"):
        assert token in css, f"accessibility CSS token missing: {token}"
    assert not re.search(r"\.nav-links\s*\{[^}]*display\s*:\s*none", css, re.S), "navigation hidden by CSS"

    for item in docs["visual_assets"]:
        path = ROOT / item["path"]
        assert image_size(path) == (item["width"], item["height"]), f"wrong image dimensions: {item['path']}"
    social = {item["path"]: item for item in docs["visual_assets"]}["docs/assets/aso-social-card.jpg"]
    assert social["required_text"] == ["Agent Swarm Orchestration", "Parallel cognition. One accountable root."]

    plugin = read_json("plugins/agent-swarm-orchestration/.codex-plugin/plugin.json")
    assert plugin["version"] == VERSION
    custody = read_json("release-assets/v0.3.2/archive-custody.json")
    assert custody["version"] == VERSION and custody["generated_at"] == "2026-10-12"
    for archive in custody["archives"]:
        path = ROOT / archive["path"]
        assert path.is_file(), f"missing archive: {archive['path']}"
        assert sha256(path) == archive["sha256"], f"archive hash mismatch: {archive['path']}"

    print(f"DOCUMENTATION STRUCTURE VALID agent-swarm-orchestration v{VERSION}")
    print(f"DOCUMENTATION FINGERPRINT {fingerprint}")
    print(f"GOVERNED FILES {len(governed)}; VISUALS {len(docs['visual_assets'])}; REQUIRED SECTIONS {len(required_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())