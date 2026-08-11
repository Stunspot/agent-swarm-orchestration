#!/usr/bin/env python3
"""Validate Agent Swarm Orchestration documentation and presentation custody."""

from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.1"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n", f"not a PNG: {path}"
    return struct.unpack(">II", header[16:24])


def documentation_fingerprint(paths: list[str]) -> tuple[str, list[dict[str, str]]]:
    records = [{"path": rel, "sha256": sha256(ROOT / rel)} for rel in paths]
    mapping = {item["path"]: item["sha256"] for item in records}
    canonical = json.dumps(mapping, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest(), records


def main() -> int:
    docs = read_json("documentation-manifest.json")
    package = read_json("package-manifest.json")
    authorship = read_json("documentation-authorship.json")
    review = read_json("documentation-review.json")
    accessibility = read_json("documentation-accessibility-review.json")
    visual = read_json("verification/visual-review-v0.2.1.json")

    assert docs["version"] == VERSION
    assert package["version"] == VERSION
    assert package["runtime_fingerprint"] == "8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5"

    governed = list(docs["customer_docs"]) + ["docs/index.html", "docs/style.css", "documentation-manifest.json"]
    assert len(governed) == len(set(governed)), "duplicate governed documentation path"
    for relative in governed:
        assert (ROOT / relative).is_file(), f"missing governed documentation: {relative}"

    fingerprint, records = documentation_fingerprint(governed)
    assert fingerprint == authorship["documentation_fingerprint"], "authorship fingerprint mismatch"
    assert records == authorship["files"], "authorship file hash records mismatch"
    assert review["documentation_fingerprint"] == fingerprint
    assert accessibility["documentation_fingerprint"] == fingerprint
    assert review["verdict"] == "REVIEW_PASS"
    assert not review["open_content_findings"]
    assert all(item["verdict"] == "PASS" for item in review["journey_verdicts"])
    assert accessibility["verdict"] == "REVIEW_PASS_WITH_CONDITIONS"
    assert authorship["hesperos_lint"]["result"] == "PASS_WITH_DOCUMENTED_LEGAL_EXCEPTION"

    html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    css = (ROOT / "docs/style.css").read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    hrefs = re.findall(r'\bhref="([^"]+)"', html)
    required_ids = {"top", "main", "product", "shapes", "use", "install", "recover", "evidence", "support"}
    assert required_ids <= ids, f"missing Pages sections: {sorted(required_ids - ids)}"
    assert not [href for href in hrefs if href.startswith("#") and href[1:] not in ids]
    assert not [href for href in hrefs if "/blob/" in href and "/blob/main/" not in href]
    for source in re.findall(r'\bsrc="([^"]+)"', html):
        if not source.startswith(("http://", "https://")):
            assert (ROOT / "docs" / source).is_file(), f"missing Pages asset: {source}"
    for token in (
        "What it prevents",
        "First successful use",
        "Expected output shape",
        "Install and verify",
        "Configuration, troubleshooting, and recovery",
        "Privacy, security, and evidence",
        "Support, contribution, and terms",
        "Agent Swarm Orchestration",
        "Parallel cognition. One accountable root.",
    ):
        assert token in html, f"Pages journey token missing: {token}"
    for token in (".skip-link", ":focus-visible", "prefers-reduced-motion", "overflow-x: auto"):
        assert token in css, f"accessibility CSS token missing: {token}"
    assert not re.search(r"\.nav-links\s*\{[^}]*display\s*:\s*none", css, re.S), "navigation hidden by CSS"

    manifest_visuals = {item["path"]: item for item in docs["visual_assets"]}
    reviewed_visuals = {item["path"]: item for item in visual["assets"]}
    for relative, item in manifest_visuals.items():
        path = ROOT / relative
        assert png_size(path) == (item["width"], item["height"]), f"wrong image dimensions: {relative}"
        assert reviewed_visuals[relative]["sha256"] == sha256(path), f"visual receipt hash mismatch: {relative}"
    core = [manifest_visuals[path] for path in (
        "docs/assets/aso-readme-banner.png",
        "docs/assets/aso-pages-hero.png",
        "docs/assets/aso-social-card.png",
    )]
    assert len({(item["width"], item["height"]) for item in core}) == 3
    assert len({item["width"] / item["height"] for item in core}) == 3
    assert len({reviewed_visuals[item["path"]]["sha256"] for item in core}) == 3
    social = manifest_visuals["docs/assets/aso-social-card.png"]
    assert social["required_text"] == ["Agent Swarm Orchestration", "Parallel cognition. One accountable root."]

    plugin = read_json("plugins/agent-swarm-orchestration/.codex-plugin/plugin.json")
    assert plugin["version"] == VERSION
    custody = read_json("release-assets/v0.2.1/archive-custody.json")
    assert custody["version"] == VERSION and custody["generated_at"] == "2026-08-11"
    for archive in custody["archives"]:
        path = ROOT / archive["path"]
        assert path.is_file(), f"missing archive: {archive['path']}"
        assert sha256(path) == archive["sha256"], f"archive hash mismatch: {archive['path']}"

    print(f"DOCUMENTATION RELEASE VALID agent-swarm-orchestration v{VERSION}")
    print(f"DOCUMENTATION FINGERPRINT {fingerprint}")
    print(f"GOVERNED FILES {len(governed)}; VISUALS {len(manifest_visuals)}; JOURNEY GATES {len(review['journey_verdicts'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
