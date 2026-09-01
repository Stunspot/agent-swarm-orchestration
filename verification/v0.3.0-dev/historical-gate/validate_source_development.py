#!/usr/bin/env python3
"""Validate the unreleased 0.3.0-dev source tree without making release claims."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.0-dev"
RUNTIME_FINGERPRINT = "e625a54f9facee4b093c6504cb7b8cc870a4e5e98443e6eebe60f320dc43eed2"
BASELINE = {
    "version": "0.2.3",
    "runtime_version": "0.1.0",
    "runtime_fingerprint": "8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5",
    "custody": "release-assets/v0.2.3/archive-custody.json",
    "checksums": "release-assets/v0.2.3/checksums.sha256",
}
BASELINE_HASHES = {
    "release-assets/v0.2.3/archive-custody.json": "cbd925ec4fcf33d24c59efd70f58e8959e9e22e113b2f8a6ab483780b3cd16a4",
    "release-assets/v0.2.3/checksums.sha256": "fda392c806f9c2df81bf7d6915b76a12cf8f8a3d37456f8822b49828ccad1650",
    "release-assets/v0.2.3/Plugin-Agent-Swarm-Orchestration-v0.2.3.zip": "00964d85a389571c6dfa561a3efff07e497caeaff04a8f5ad81f9354f39bfa8f",
    "release-assets/v0.2.3/Skill-agent-swarm-orchestration-v0.2.3.zip": "ab3ed058d8cb26b0ca70dcda39f9c1a622950f80bca379bb33c964306aef4886",
    "claude-ai/agent-swarm-orchestration-v0.2.3.zip": "ab3ed058d8cb26b0ca70dcda39f9c1a622950f80bca379bb33c964306aef4886",
}
DISTRIBUTION_STATUSES = {
    "codex_plugin": "source-development-unreleased",
    "codex_standalone": "source-development-unreleased",
    "claude_standalone": "source-development-unreleased",
    "frozen_release_assets": "retained-baseline-v0.2.3",
    "pages": "retained-baseline",
}
SOURCE_AUTHORITY = {
    "local_source_development": True,
    "installation": False,
    "public_publication": False,
    "external_action": False,
    "free_offer": False,
    "risk_acceptance": False,
}
EVIDENCE_DENIALS = {
    "installation": "not-performed-for-0.3.0-dev",
    "clean_host_discovery": "not-performed-for-0.3.0-dev",
    "clean_host_invocation": "not-performed-for-0.3.0-dev",
    "live_execution": "not-performed-for-vnext-control-cases-or-ablations",
    "publication": "not-authorized-or-performed-for-0.3.0-dev",
}
RUNTIME_RELATIVE = Path("canonical/skills/agent-swarm-orchestration")
MIRRORS = {
    "plugin": Path("plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration"),
    "codex": Path("release/codex/agent-swarm-orchestration"),
    "claude": Path("release/claude/agent-swarm-orchestration"),
}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
IGNORED_PARTS = {"__pycache__"}
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
CLAIMS_NOT_ESTABLISHED = [
    "public release",
    "installation or clean-host discovery",
    "live-control execution",
    "ablation superiority",
    "publication or deployment",
]


def read_json(path: Path, errors: list[str], label: str) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: {exc}")
        return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_reparse(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def files_under(root: Path) -> dict[str, Path]:
    if not root.is_dir() or is_reparse(root):
        raise RuntimeError(f"invalid or reparse-backed runtime root: {root}")
    result: dict[str, Path] = {}
    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        directory_path = Path(directory)
        if is_reparse(directory_path):
            raise RuntimeError(f"reparse directory refused: {directory_path}")
        for name in dirnames:
            candidate = directory_path / name
            if is_reparse(candidate):
                raise RuntimeError(f"reparse directory refused: {candidate}")
        for name in filenames:
            candidate = directory_path / name
            relative = candidate.relative_to(root)
            if is_reparse(candidate):
                raise RuntimeError(f"reparse file refused: {candidate}")
            if IGNORED_PARTS.intersection(relative.parts) or candidate.suffix in IGNORED_SUFFIXES:
                continue
            if not candidate.is_file():
                raise RuntimeError(f"non-regular runtime entry: {candidate}")
            result[relative.as_posix()] = candidate
    return result


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, path in sorted(files_under(root).items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def parity(source: Path, destination: Path) -> dict[str, Any]:
    source_files = files_under(source)
    destination_files = files_under(destination)
    missing = sorted(set(source_files) - set(destination_files))
    extra = sorted(set(destination_files) - set(source_files))
    changed = sorted(
        relative
        for relative in set(source_files).intersection(destination_files)
        if sha256(source_files[relative]) != sha256(destination_files[relative])
    )
    return {"valid": not (missing or extra or changed), "missing": missing, "extra": extra, "changed": changed}


def validate_metadata(root: Path = ROOT, baseline_hashes: dict[str, str] | None = None) -> dict[str, Any]:
    root = root.resolve()
    expected_hashes = BASELINE_HASHES if baseline_hashes is None else baseline_hashes
    errors: list[str] = []
    checks: dict[str, Any] = {}

    package = read_json(root / "package-manifest.json", errors, "package manifest")
    plugin = read_json(root / "plugins/agent-swarm-orchestration/.codex-plugin/plugin.json", errors, "plugin manifest")
    eval_manifest = read_json(root / "canonical/evals/eval-manifest-vnext.yaml", errors, "vNext eval manifest")

    if isinstance(package, dict):
        for field, expected in {
            "version": VERSION,
            "runtime_version": VERSION,
            "status": "source-development",
            "runtime_fingerprint": RUNTIME_FINGERPRINT,
        }.items():
            if package.get(field) != expected:
                errors.append(f"package manifest: {field} must be {expected}")
        if package.get("release_baseline") != BASELINE:
            errors.append("package manifest: release_baseline differs from frozen v0.2.3 identity")
        distributions = package.get("distributions")
        if not isinstance(distributions, dict):
            errors.append("package manifest: distributions must be an object")
        elif set(distributions) != set(DISTRIBUTION_STATUSES):
            errors.append(
                "package manifest: distribution keys differ: "
                + ", ".join(sorted(set(distributions).symmetric_difference(DISTRIBUTION_STATUSES)))
            )
        else:
            actual_statuses = {
                name: distributions[name].get("status") if isinstance(distributions[name], dict) else None
                for name in DISTRIBUTION_STATUSES
            }
            if actual_statuses != DISTRIBUTION_STATUSES:
                errors.append(f"package manifest: distribution statuses differ: {actual_statuses}")
        authority = package.get("authority")
        if authority != SOURCE_AUTHORITY:
            errors.append(f"package manifest: authority contract differs: {authority}")
        evidence = package.get("evidence")
        if not isinstance(evidence, dict):
            errors.append("package manifest: evidence must be an object")
        else:
            for field, expected in EVIDENCE_DENIALS.items():
                if evidence.get(field) != expected:
                    errors.append(
                        f"package manifest: evidence.{field} must equal the source-development denial {expected!r}"
                    )

    if isinstance(plugin, dict) and plugin.get("version") != VERSION:
        errors.append("plugin manifest: version must equal package source-development version")
    if isinstance(eval_manifest, dict):
        if eval_manifest.get("target_package_version") != VERSION:
            errors.append("vNext eval manifest: target_package_version mismatch")
        if eval_manifest.get("target_runtime_fingerprint") != RUNTIME_FINGERPRINT:
            errors.append("vNext eval manifest: target_runtime_fingerprint mismatch")

    source = root / RUNTIME_RELATIVE
    try:
        actual_fingerprint = tree_digest(source)
        checks["canonical_fingerprint"] = actual_fingerprint
        if actual_fingerprint != RUNTIME_FINGERPRINT:
            errors.append(f"canonical runtime fingerprint mismatch: {actual_fingerprint}")
        if isinstance(package, dict) and package.get("runtime_fingerprint") != actual_fingerprint:
            errors.append("package manifest fingerprint does not equal canonical bytes")
        mirror_checks = {name: parity(source, root / relative) for name, relative in MIRRORS.items()}
        checks["runtime_parity"] = mirror_checks
        for name, check in mirror_checks.items():
            if not check["valid"]:
                errors.append(f"{name} runtime mirror differs from canonical: {check}")
    except (OSError, RuntimeError) as exc:
        errors.append(f"runtime custody: {exc}")

    custody_checks: dict[str, Any] = {}
    for relative, expected in expected_hashes.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"frozen custody file missing: {relative}")
            custody_checks[relative] = None
            continue
        actual = sha256(path)
        custody_checks[relative] = actual
        if actual != expected:
            errors.append(f"frozen custody hash changed: {relative}")
    checks["frozen_v0.2.3"] = custody_checks

    forbidden = [
        root / "release-assets/v0.3.0-dev",
        root / "claude-ai/agent-swarm-orchestration-v0.3.0-dev.zip",
    ]
    present = [str(path.relative_to(root)) for path in forbidden if path.exists()]
    checks["forbidden_dev_release_artifacts"] = present
    if present:
        errors.append("unreleased development artifacts exist: " + ", ".join(present))

    return {
        "format": "aso-source-development-validation/v1",
        "valid": not errors,
        "version": VERSION,
        "runtime_fingerprint": RUNTIME_FINGERPRINT,
        "state": "source-development-unreleased",
        "checks": checks,
        "claims_not_established": CLAIMS_NOT_ESTABLISHED,
        "errors": errors,
    }


def run_command(root: Path, label: str, argv: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        argv,
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    return {
        "label": label,
        "returncode": completed.returncode,
        "last_output": lines[-1] if lines else "",
    }


def run_source_checks(root: Path = ROOT) -> list[dict[str, Any]]:
    python = sys.executable
    commands: list[tuple[str, list[str]]] = [
        ("eval-contract", [python, "-B", "-X", "utf8", "tools/validate_vnext_evals.py", "--dry-run"]),
        ("runtime-parity", [python, "-B", "-X", "utf8", "tools/check_runtime_parity.py"]),
        (
            "repository-tests",
            [
                python, "-B", "-X", "utf8", "-m", "unittest", "-v",
                "verification.tests.test_organization_workbench",
                "verification.tests.test_runtime_sync_tools",
                "verification.tests.test_vnext_eval_contracts",
                "verification.tests.test_source_development_custody",
            ],
        ),
        ("diff-check", ["git", "diff", "--check"]),
    ]
    for name, relative in [("canonical", RUNTIME_RELATIVE), *MIRRORS.items()]:
        commands.append(
            (
                f"{name}-runtime-tests",
                [python, "-B", "-X", "utf8", "-m", "unittest", "discover", "-s", str(relative / "tests"), "-v"],
            )
        )
    return [run_command(root, label, argv) for label, argv in commands]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true", help="Skip subprocess test execution; intended for isolated validator tests.")
    args = parser.parse_args()

    report = validate_metadata(ROOT)
    if not args.metadata_only:
        commands = run_source_checks(ROOT)
        report["command_checks"] = commands
        failed = [item["label"] for item in commands if item["returncode"] != 0]
        if failed:
            report["valid"] = False
            report["errors"].append("command checks failed: " + ", ".join(failed))
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())