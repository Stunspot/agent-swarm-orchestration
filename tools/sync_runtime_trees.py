#!/usr/bin/env python3
"""Safely synchronize canonical runtime bytes into the three tracked mirrors."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "canonical" / "skills" / "agent-swarm-orchestration"
DESTINATIONS = {
    "plugin": ROOT / "plugins" / "agent-swarm-orchestration" / "skills" / "agent-swarm-orchestration",
    "codex": ROOT / "release" / "codex" / "agent-swarm-orchestration",
    "claude": ROOT / "release" / "claude" / "agent-swarm-orchestration",
}
EXPECTED_RELATIVE_DESTINATIONS = {
    "plugin": Path("plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration"),
    "codex": Path("release/codex/agent-swarm-orchestration"),
    "claude": Path("release/claude/agent-swarm-orchestration"),
}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
IGNORED_PARTS = {"__pycache__"}
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def _is_reparse(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def _assert_relative(relative: Path) -> None:
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise RuntimeError(f"unsafe relative path: {relative}")


def _lstat_or_none(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _stat_is_reparse(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def _assert_no_reparse_chain(root: Path, target: Path, *, allow_missing: bool = False) -> None:
    try:
        relative = target.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"path escapes repository: {target}") from exc
    components = [root]
    current = root
    for part in relative.parts:
        current = current / part
        components.append(current)
    for index, current in enumerate(components):
        info = _lstat_or_none(current)
        if info is None:
            if allow_missing and index > 0:
                continue
            raise RuntimeError(f"required synchronization root is missing: {current}")
        if _stat_is_reparse(info):
            raise RuntimeError(f"reparse point is forbidden in synchronization roots: {current}")


def files_under(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    if not root.is_dir() or _is_reparse(root):
        raise RuntimeError(f"invalid runtime root: {root}")
    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        directory_path = Path(directory)
        if _is_reparse(directory_path):
            raise RuntimeError(f"reparse directory is forbidden: {directory_path}")
        for name in list(dirnames):
            candidate = directory_path / name
            if _is_reparse(candidate):
                raise RuntimeError(f"reparse directory is forbidden: {candidate}")
        for name in filenames:
            candidate = directory_path / name
            relative = candidate.relative_to(root)
            if _is_reparse(candidate):
                raise RuntimeError(f"reparse file is forbidden: {candidate}")
            if IGNORED_PARTS.intersection(relative.parts) or candidate.suffix in IGNORED_SUFFIXES:
                continue
            if not candidate.is_file():
                raise RuntimeError(f"non-regular runtime entry: {candidate}")
            result[relative.as_posix()] = candidate
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, path in sorted(files_under(root).items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest()


def assert_layout() -> None:
    expected = {name: ROOT / relative for name, relative in EXPECTED_RELATIVE_DESTINATIONS.items()}
    if DESTINATIONS != expected:
        raise RuntimeError("destination allowlist changed")
    if len(set(DESTINATIONS.values())) != len(DESTINATIONS):
        raise RuntimeError("destinations must be distinct")
    for target in (SOURCE, *DESTINATIONS.values()):
        _assert_no_reparse_chain(ROOT, target)
        files_under(target)


def plan_for(destination: Path) -> dict[str, list[str]]:
    source_files = files_under(SOURCE)
    destination_files = files_under(destination)
    copy = sorted(
        relative
        for relative, source_path in source_files.items()
        if relative not in destination_files or source_path.read_bytes() != destination_files[relative].read_bytes()
    )
    remove = sorted(set(destination_files) - set(source_files))
    return {"copy": copy, "remove": remove}


def _safe_join(root: Path, relative_text: str) -> Path:
    relative = Path(relative_text)
    _assert_relative(relative)
    target = root.joinpath(*relative.parts)
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"path escaped allowlisted root: {relative_text}") from exc
    return target


def _prepare_safe_parent(root: Path, target: Path) -> None:
    _assert_no_reparse_chain(root, target.parent, allow_missing=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    _assert_no_reparse_chain(root, target.parent)


def _assert_safe_target_if_present(root: Path, target: Path) -> os.stat_result | None:
    info = _lstat_or_none(target)
    if info is not None:
        if _stat_is_reparse(info):
            raise RuntimeError(f"reparse entry refused: {target}")
        _assert_no_reparse_chain(root, target)
    return info


def apply_plan(destination: Path, plan: dict[str, list[str]], *, source: Path | None = None, prune: bool = False) -> None:
    source = SOURCE if source is None else source
    if plan["remove"] and not prune:
        raise RuntimeError(f"unexpected destination files require explicit --prune: {plan['remove']}")
    for relative in plan["copy"]:
        source_path = _safe_join(source, relative)
        target_path = _safe_join(destination, relative)
        _assert_no_reparse_chain(source, source_path)
        source_info = source_path.lstat()
        if not stat.S_ISREG(source_info.st_mode):
            raise RuntimeError(f"unsafe source-file target: {source_path}")
        payload = source_path.read_bytes()
        _prepare_safe_parent(destination, target_path)
        _assert_safe_target_if_present(destination, target_path)
        _assert_no_reparse_chain(destination, target_path.parent)
        target_path.write_bytes(payload)
    for relative in plan["remove"]:
        target_path = _safe_join(destination, relative)
        _assert_no_reparse_chain(destination, target_path)
        target_info = target_path.lstat()
        if not stat.S_ISREG(target_info.st_mode):
            raise RuntimeError(f"unsafe extra-file target: {target_path}")
        _assert_no_reparse_chain(destination, target_path)
        target_path.unlink()


def parity(destination: Path, *, source: Path | None = None) -> dict[str, Any]:
    source = SOURCE if source is None else source
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


def destination_git_changes() -> list[dict[str, str]]:
    relative_paths = [str(path.relative_to(ROOT)) for path in DESTINATIONS.values()]
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all", "--", *relative_paths],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace") if isinstance(result.stderr, bytes) else str(result.stderr)
        raise RuntimeError(f"git status failed: {stderr.strip()}")
    payload = result.stdout if isinstance(result.stdout, bytes) else result.stdout.encode("utf-8")
    changes: list[dict[str, str]] = []
    for record in payload.split(b"\0"):
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise RuntimeError(f"unrecognized git status record: {record!r}")
        status = record[:2].decode("ascii", errors="replace")
        path = record[3:].decode("utf-8", errors="strict").replace("\\", "/")
        if any(marker in status for marker in ("R", "C", "U")):
            raise RuntimeError(f"rename, copy, or conflict is not accepted in runtime destinations: {status} {path}")
        changes.append({"status": status, "path": path})
    return changes


def assert_destination_git_clean(
    plans: dict[str, dict[str, list[str]]] | None = None,
    *,
    accept_managed_dirty: bool = False,
) -> list[dict[str, str]]:
    changes = destination_git_changes()
    if not changes:
        return []
    rendered = "\n".join(f"{item['status']} {item['path']}" for item in changes)
    if not accept_managed_dirty:
        raise RuntimeError("destination trees are already dirty; reconcile before synchronization:\n" + rendered)
    if plans is None:
        raise RuntimeError("managed-dirty continuation requires the inspected synchronization plans")

    source_files = files_under(SOURCE)
    roots = {
        name: relative.as_posix().rstrip("/") + "/"
        for name, relative in EXPECTED_RELATIVE_DESTINATIONS.items()
    }
    for item in changes:
        status = item["status"]
        if any(character not in {" ", "M", "A", "D", "?"} for character in status):
            raise RuntimeError(f"unsupported dirty status for managed continuation: {status} {item['path']}")
        matches = [
            (name, prefix)
            for name, prefix in roots.items()
            if item["path"].startswith(prefix)
        ]
        if len(matches) != 1:
            raise RuntimeError(f"dirty path is outside one exact runtime destination: {item['path']}")
        name, prefix = matches[0]
        relative = item["path"][len(prefix):]
        _assert_relative(Path(relative))
        if relative not in source_files:
            raise RuntimeError(f"dirty destination path has no canonical source counterpart: {item['path']}")
        destination_file = _safe_join(DESTINATIONS[name], relative)
        destination_info = _assert_safe_target_if_present(DESTINATIONS[name], destination_file)
        already_equal = False
        if destination_info is not None:
            if not stat.S_ISREG(destination_info.st_mode):
                raise RuntimeError(f"dirty managed destination is not a regular file: {destination_file}")
            _assert_no_reparse_chain(DESTINATIONS[name], destination_file)
            already_equal = sha256(destination_file) == sha256(source_files[relative])
        if relative not in plans[name]["copy"] and not already_equal:
            raise RuntimeError(f"dirty path is neither in the inspected copy plan nor already canonical: {item['path']}")
    return changes


def snapshot_for_rollback(plans: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, bytes | None]]:
    snapshots: dict[str, dict[str, bytes | None]] = {}
    for name, plan in plans.items():
        destination = DESTINATIONS[name]
        entries: dict[str, bytes | None] = {}
        for relative in sorted(set(plan["copy"] + plan["remove"])):
            target = _safe_join(destination, relative)
            info = _assert_safe_target_if_present(destination, target)
            if info is None:
                entries[relative] = None
            elif stat.S_ISREG(info.st_mode):
                _assert_no_reparse_chain(destination, target)
                entries[relative] = target.read_bytes()
            else:
                raise RuntimeError(f"unsafe rollback snapshot target: {target}")
        snapshots[name] = entries
    return snapshots


def rollback(snapshots: dict[str, dict[str, bytes | None]]) -> None:
    for name, entries in snapshots.items():
        destination = DESTINATIONS[name]
        for relative, prior in entries.items():
            target = _safe_join(destination, relative)
            if prior is None:
                info = _assert_safe_target_if_present(destination, target)
                if info is not None:
                    if not stat.S_ISREG(info.st_mode):
                        raise RuntimeError(f"unsafe rollback removal target: {target}")
                    _assert_no_reparse_chain(destination, target)
                    target.unlink()
            else:
                _prepare_safe_parent(destination, target)
                _assert_safe_target_if_present(destination, target)
                _assert_no_reparse_chain(destination, target.parent)
                target.write_bytes(prior)


def stage_and_verify(plans: dict[str, dict[str, list[str]]], *, prune: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="aso-runtime-sync-") as temporary:
        stage_root = Path(temporary)
        for name, destination in DESTINATIONS.items():
            staged = stage_root / name
            staged.mkdir(parents=True)
            for relative, source_path in files_under(destination).items():
                target = _safe_join(staged, relative)
                _assert_no_reparse_chain(destination, source_path)
                payload = source_path.read_bytes()
                _prepare_safe_parent(staged, target)
                target.write_bytes(payload)
            apply_plan(staged, plans[name], prune=prune)
            check = parity(staged)
            if not check["valid"]:
                raise RuntimeError(f"staged parity failed for {name}: {check}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply the allowlisted file-level synchronization. Default is a drift check.")
    parser.add_argument("--prune", action="store_true", help="With --apply, remove individually identified extra files after staging and validation.")
    parser.add_argument("--accept-managed-dirty", action="store_true", help="With --apply, continue only when every dirty destination path maps to canonical source and is in the inspected plan or already canonical.")
    args = parser.parse_args()
    if args.prune and not args.apply:
        parser.error("--prune requires --apply")
    if args.accept_managed_dirty and not args.apply:
        parser.error("--accept-managed-dirty requires --apply")

    assert_layout()
    source_fingerprint = tree_fingerprint(SOURCE)
    plans = {name: plan_for(path) for name, path in DESTINATIONS.items()}
    checks_before = {name: parity(path) for name, path in DESTINATIONS.items()}
    drift = not all(check["valid"] for check in checks_before.values())

    if not args.apply:
        print(json.dumps({
            "format": "aso-runtime-sync/v2",
            "mode": "check",
            "source": str(SOURCE),
            "source_fingerprint": source_fingerprint,
            "plan": plans,
            "parity": checks_before,
        }, indent=2))
        return 1 if drift else 0

    accepted_managed_dirty = assert_destination_git_clean(plans, accept_managed_dirty=args.accept_managed_dirty)
    if any(plan["remove"] for plan in plans.values()) and not args.prune:
        raise RuntimeError("extra files detected; inspect the plan and rerun with explicit --prune only if each removal is intended")
    stage_and_verify(plans, prune=args.prune)
    if tree_fingerprint(SOURCE) != source_fingerprint:
        raise RuntimeError("canonical source changed during staging")

    snapshots = snapshot_for_rollback(plans)
    try:
        for name, destination in DESTINATIONS.items():
            apply_plan(destination, plans[name], prune=args.prune)
        assert_layout()
        checks_after = {name: parity(path) for name, path in DESTINATIONS.items()}
        if not all(check["valid"] for check in checks_after.values()):
            raise RuntimeError(f"post-apply parity failed: {checks_after}")
    except BaseException:
        rollback(snapshots)
        raise

    print(json.dumps({
        "format": "aso-runtime-sync/v2",
        "mode": "apply",
        "source": str(SOURCE),
        "source_fingerprint": source_fingerprint,
        "accepted_managed_dirty": accepted_managed_dirty,
        "plan": plans,
        "parity": checks_after,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
