#!/usr/bin/env python3
"""Validate Agent Swarm Orchestration 0.3.2 local release-candidate custody."""

from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.2"
GENERATED_AT = "2026-09-05"
SKILL = ROOT / "canonical" / "skills" / "agent-swarm-orchestration"
OUT = ROOT / "release-assets" / f"v{VERSION}"
BASELINE_HASHES = {
    "release-assets/v0.2.3/archive-custody.json": "cbd925ec4fcf33d24c59efd70f58e8959e9e22e113b2f8a6ab483780b3cd16a4",
    "release-assets/v0.2.3/checksums.sha256": "fda392c806f9c2df81bf7d6915b76a12cf8f8a3d37456f8822b49828ccad1650",
    "release-assets/v0.2.3/Plugin-Agent-Swarm-Orchestration-v0.2.3.zip": "00964d85a389571c6dfa561a3efff07e497caeaff04a8f5ad81f9354f39bfa8f",
    "release-assets/v0.2.3/Skill-agent-swarm-orchestration-v0.2.3.zip": "ab3ed058d8cb26b0ca70dcda39f9c1a622950f80bca379bb33c964306aef4886",
    "claude-ai/agent-swarm-orchestration-v0.2.3.zip": "ab3ed058d8cb26b0ca70dcda39f9c1a622950f80bca379bb33c964306aef4886",
}


def files(root: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if not path.is_file() or "__pycache__" in rel.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        result[rel.as_posix()] = path.read_bytes()
    return result


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, payload in sorted(files(root).items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(payload).digest())
    return digest.hexdigest()


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


def validate_zip(path: Path, expected_tree: dict[str, bytes]) -> int:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert names, f"empty archive: {path}"
        assert len(names) == len(set(names)), f"duplicate archive member: {path}"
        assert all("\\" not in name for name in names), f"backslash member: {path}"
        assert all(name.startswith("agent-swarm-orchestration/") for name in names), f"wrong top level: {path}"
        assert all(not name.startswith("/") and ".." not in Path(name).parts for name in names), f"unsafe archive member: {path}"
        extracted = {name.split("/", 1)[1]: archive.read(name) for name in names}
        assert extracted == expected_tree, f"archive parity failed: {path}"
        return len(names)


def run(argv: list[str], label: str) -> None:
    completed = subprocess.run(argv, cwd=ROOT, text=True, encoding="utf-8", errors="replace")
    assert completed.returncode == 0, f"{label} failed"


def historical_main() -> int:
    package = json.loads((ROOT / "package-manifest.json").read_text(encoding="utf-8"))
    assert package["version"] == VERSION
    assert package["runtime_version"] == VERSION
    assert package["status"] == "public-release-candidate"
    canonical = files(SKILL)
    canonical_digest = tree_digest(SKILL)
    assert package["runtime_fingerprint"] == canonical_digest, "canonical runtime fingerprint does not match package manifest"

    mirrors = [
        ROOT / "release" / "codex" / "agent-swarm-orchestration",
        ROOT / "release" / "claude" / "agent-swarm-orchestration",
        ROOT / "plugins" / "agent-swarm-orchestration" / "skills" / "agent-swarm-orchestration",
    ]
    for target in mirrors:
        assert files(target) == canonical, f"runtime parity failed: {target}"

    plugin_root = ROOT / "plugins" / "agent-swarm-orchestration"
    plugin = json.loads((plugin_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "agent-swarm-orchestration"
    assert plugin["version"] == VERSION
    assert plugin["skills"] == "./skills/"
    for key in ("composerIcon", "logo"):
        assert (plugin_root / plugin["interface"][key]).resolve().is_file()

    marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    entries = {item["name"]: item for item in marketplace["plugins"]}
    assert entries["agent-swarm-orchestration"]["source"]["path"] == "./plugins/agent-swarm-orchestration"

    expected_sizes = {
        ROOT / "docs" / "assets" / "aso-readme-banner.png": (1280, 640),
        ROOT / "docs" / "assets" / "aso-pages-hero.png": (1600, 900),
        ROOT / "docs" / "assets" / "aso-social-card.jpg": (1730, 909),
        plugin_root / "assets" / "aso-icon.png": (512, 512),
        plugin_root / "assets" / "aso-social-card.png": (1586, 992),
    }
    for path, expected in expected_sizes.items():
        assert image_size(path) == expected, f"wrong dimensions: {path} {image_size(path)} != {expected}"

    docs = json.loads((ROOT / "documentation-manifest.json").read_text(encoding="utf-8"))
    assert docs["version"] == VERSION
    for rel in docs["reader_journey"]:
        assert (ROOT / rel).is_file(), f"missing documentation: {rel}"
    for item in docs["visual_assets"]:
        path = ROOT / item["path"]
        assert image_size(path) == (item["width"], item["height"])

    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for token in (
        "Skip to content", 'width="1600"', 'height="900"', "aso-social-card.jpg",
        "image/jpeg", "twitter:image:alt", "og:image:width", "og:image:height",
        "Design the organization", "Execution kernel", "What it prevents", "Install and verify",
    ):
        assert token in html, f"site token missing: {token}"

    custody_path = OUT / "archive-custody.json"
    custody = json.loads(custody_path.read_text(encoding="utf-8"))
    assert custody["format"] == "cd-augment-archive-custody/v1"
    assert custody["product"] == "agent-swarm-orchestration"
    assert custody["version"] == VERSION
    assert custody["generated_at"] == GENERATED_AT
    records = {record["path"]: record for record in custody["archives"]}

    expected_archives = [
        (OUT / f"Plugin-Agent-Swarm-Orchestration-v{VERSION}.zip", files(plugin_root), plugin_root),
        (OUT / f"Skill-agent-swarm-orchestration-v{VERSION}.zip", canonical, SKILL),
        (ROOT / "claude-ai" / f"agent-swarm-orchestration-v{VERSION}.zip", canonical, SKILL),
    ]
    assert len(records) == len(expected_archives)
    for path, expected_tree, source in expected_archives:
        member_count = validate_zip(path, expected_tree)
        relative = path.relative_to(ROOT).as_posix()
        record = records[relative]
        assert record["sha256"] == sha256(path)
        assert record["size"] == path.stat().st_size
        assert record["member_count"] == member_count == len(expected_tree)
        assert record["top_level"] == "agent-swarm-orchestration"
        assert record["source"] == source.relative_to(ROOT).as_posix()
        assert record["source_tree_sha256"] == tree_digest(source)
        assert record["members_use_posix_paths"] is True

    plugin_zip = OUT / f"Plugin-Agent-Swarm-Orchestration-v{VERSION}.zip"
    skill_zip = OUT / f"Skill-agent-swarm-orchestration-v{VERSION}.zip"
    claude_zip = ROOT / "claude-ai" / f"agent-swarm-orchestration-v{VERSION}.zip"
    expected_checksums = (
        f"{sha256(plugin_zip)}  {plugin_zip.name}\n"
        f"{sha256(skill_zip)}  {skill_zip.name}\n"
        f"{sha256(claude_zip)}  ../../claude-ai/{claude_zip.name}\n"
    )
    assert (OUT / "checksums.sha256").read_text(encoding="utf-8") == expected_checksums
    assert sha256(skill_zip) == sha256(claude_zip), "standalone skill and Claude archives must be byte-identical"

    companion = OUT / f"{skill_zip.name}.sha256"
    assert companion.read_text(encoding="utf-8") == f"{sha256(skill_zip).upper()}  {skill_zip.name}\n"
    verify = (OUT / f"Skill-agent-swarm-orchestration-v{VERSION}-VERIFY.txt").read_text(encoding="utf-8")
    for token in (skill_zip.name, sha256(skill_zip).upper(), "Get-FileHash", "shasum -a 256", "byte identity only"):
        assert token in verify, f"verification companion missing: {token}"

    for relative, expected in BASELINE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"frozen v0.2.3 custody changed: {relative}"

    run([sys.executable, "-B", "-X", "utf8", "tools/validate_vnext_evals.py", "--dry-run"], "vNext eval contract")
    run([sys.executable, "-B", "-X", "utf8", "tools/check_runtime_parity.py"], "runtime parity")
    run([sys.executable, "-B", "-X", "utf8", "-m", "unittest", "discover", "-s", str(SKILL / "tests"), "-v"], "runtime validator tests")

    print(f"PUBLIC RELEASE VALID agent-swarm-orchestration v{VERSION}")
    print(f"RUNTIME FILES {len(canonical)}; RUNTIME FINGERPRINT {canonical_digest}")
    print(f"ARCHIVES {len(expected_archives)}; CHECKSUM AND SIDECAR CUSTODY VALID")
    return 0


def main() -> int:
    import argparse, tempfile
    from archive_paths import assert_unlinked, check_members, assert_chain
    parser=argparse.ArgumentParser(description="Check exact candidate custody, source parity and structural tests; no public publication claim.")
    parser.add_argument("--candidate",type=Path,help="Versioned complete candidate directory; defaults to the current versioned release")
    args=parser.parse_args()
    if args.candidate is None:
        args.candidate = OUT
    candidate=assert_unlinked(args.candidate)
    package=json.loads((ROOT/"package-manifest.json").read_text(encoding="utf-8"))
    assert package["version"]==VERSION
    from sync_runtime_trees import tree_fingerprint, SOURCE, parity, DESTINATIONS
    assert package["runtime_fingerprint"]==tree_fingerprint(SOURCE)
    assert all(parity(path)["valid"] for path in DESTINATIONS.values())
    custody=json.loads((candidate/"archive-custody.json").read_text(encoding="utf-8"))
    assert custody["version"]==VERSION
    expected={(candidate/f"Plugin-Agent-Swarm-Orchestration-v{VERSION}.zip").relative_to(ROOT).as_posix():ROOT/"plugins/agent-swarm-orchestration",
              (candidate/f"Skill-agent-swarm-orchestration-v{VERSION}.zip").relative_to(ROOT).as_posix():SOURCE,
              (candidate/f"claude/agent-swarm-orchestration-v{VERSION}.zip").relative_to(ROOT).as_posix():SOURCE}
    assert len(custody["archives"])==len(expected)
    assert {x["path"] for x in custody["archives"]}==set(expected)
    for record in custody["archives"]:
        path=ROOT/record["path"];assert_chain(path)
        assert sha256(path)==record["sha256"]
        validate_zip(path,files(expected[record["path"]]))
    customer=candidate/custody["customer"]["zip"]
    if customer.parent!=candidate:raise ValueError("customer ZIP must be a direct candidate child")
    assert sha256(customer)==custody["customer"]["sha256"]
    with tempfile.TemporaryDirectory(prefix="aso-check-") as d:
        with zipfile.ZipFile(customer) as z:
            entries=[(i.filename,b"" if i.is_dir() else z.read(i)) for i in z.infolist()]
            check_members(entries)
            z.extractall(d)
        from verify_package import verify
        report=verify(Path(d)/f"agent-swarm-orchestration-v{VERSION}")
    run([sys.executable,"-B","-X","utf8","-m","unittest","discover","-s",str(SOURCE/"tests")],"runtime tests")
    print(json.dumps({"valid":True,"candidate":str(candidate),"customer":report,"boundary":"Exact candidate bytes, source parity and local executable checks only; public state and model behavior unobserved"},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())