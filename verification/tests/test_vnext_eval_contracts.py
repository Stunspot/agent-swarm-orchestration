from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = REPO_ROOT / "canonical" / "evals"
SKILL_ROOT = REPO_ROOT / "canonical" / "skills" / "agent-swarm-orchestration"
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_vnext_evals.py"
SPEC = importlib.util.spec_from_file_location("validate_vnext_evals", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

BASELINE_HASHES = {
    "orchestration-transfer-cases.yaml": "68e959618bfc6202c908d02715b7e2c1fa8ae8c2f948166c27455c76a68a9259",
    "orchestration-natural-qualification-cases.yaml": "5a2fc25f103574da32d6d6d7a15a0b58dd14d1913963d73f4056332318721bf2",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_tree_digest(root: Path = SKILL_ROOT) -> str:
    tree_hash = hashlib.sha256()
    files = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.relative_to(root).parts
            and path.suffix not in {".pyc", ".pyo"}
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    for path in files:
        tree_hash.update(path.relative_to(root).as_posix().encode("utf-8"))
        tree_hash.update(b"\0")
        tree_hash.update(hashlib.sha256(path.read_bytes()).digest())
    return tree_hash.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


class VNextEvalContractsTests(unittest.TestCase):
    def assert_fingerprint_matches_manifest_and_frozen_source(self, observed: object) -> None:
        manifest = read_json(EVAL_ROOT / "eval-manifest-vnext.yaml")
        expected = manifest["target_runtime_fingerprint"]
        self.assertEqual(expected, observed)
        if expected != "PENDING_SOURCE_FREEZE":
            self.assertRegex(str(expected), r"^[0-9a-f]{64}$")
            self.assertEqual(runtime_tree_digest(), expected)


    def copy_evals(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        copied = Path(temporary.name) / "evals"
        shutil.copytree(EVAL_ROOT, copied)
        return temporary, copied

    def test_baseline_catalogs_remain_byte_identical(self) -> None:
        self.assertEqual(
            BASELINE_HASHES,
            {relative: digest(EVAL_ROOT / relative) for relative in BASELINE_HASHES},
        )

    def test_current_contract_is_complete_but_not_execution_evidence(self) -> None:
        report = VALIDATOR.validate(EVAL_ROOT)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual("contract-and-fixture-completeness-only", report["validation_scope"])
        self.assertEqual("not-evaluated", report["execution_evidence"])
        self.assert_fingerprint_matches_manifest_and_frozen_source(report["target_runtime_fingerprint"])
        self.assertEqual(
            {
                "baseline_cases": 20,
                "natural_cases": 16,
                "live_cases": 6,
                "experiments": 3,
                "fixtures": 6,
                "schemas": 5,
            },
            report["counts"],
        )

    def test_final_lowercase_sha256_can_replace_pending_fingerprint(self) -> None:
        temporary, copied = self.copy_evals()
        self.addCleanup(temporary.cleanup)
        final_fingerprint = "a" * 64
        paths = [copied / "eval-manifest-vnext.yaml"]
        manifest = read_json(paths[0])
        paths.extend(copied / relative for relative in manifest["files"])
        paths.extend((copied / "fixtures" / "organization-vnext").glob("ASO-L*/case.json"))
        for path in paths:
            document = read_json(path)
            document["target_runtime_fingerprint"] = final_fingerprint
            write_json(path, document)
        report = VALIDATOR.validate(copied)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(final_fingerprint, report["target_runtime_fingerprint"])

    def test_duplicate_baseline_contract_is_rejected(self) -> None:
        temporary, copied = self.copy_evals()
        self.addCleanup(temporary.cleanup)
        manifest_path = copied / "eval-manifest-vnext.yaml"
        manifest = read_json(manifest_path)
        manifest["baseline_contracts"].append(dict(manifest["baseline_contracts"][0]))
        write_json(manifest_path, manifest)
        report = VALIDATOR.validate(copied)
        self.assertFalse(report["valid"])
        self.assertTrue(any("baseline_contracts paths must be unique" in error for error in report["errors"]))

    def test_tampered_baseline_fails_pinned_custody(self) -> None:
        temporary, copied = self.copy_evals()
        self.addCleanup(temporary.cleanup)
        baseline = copied / "orchestration-transfer-cases.yaml"
        baseline.write_bytes(baseline.read_bytes() + b" ")
        report = VALIDATOR.validate(copied)
        self.assertFalse(report["valid"])
        self.assertTrue(any("SHA-256 differs from pinned custody" in error for error in report["errors"]))

    def test_fixture_identity_mismatch_is_rejected(self) -> None:
        temporary, copied = self.copy_evals()
        self.addCleanup(temporary.cleanup)
        fixture_path = copied / "fixtures" / "organization-vnext" / "ASO-L001" / "case.json"
        fixture = read_json(fixture_path)
        fixture["case_id"] = "ASO-L002"
        write_json(fixture_path, fixture)
        report = VALIDATOR.validate(copied)
        self.assertFalse(report["valid"])
        self.assertTrue(any("fixture ASO-L001: case_id mismatch" in error for error in report["errors"]))

    def test_fixture_path_escape_is_rejected(self) -> None:
        temporary, copied = self.copy_evals()
        self.addCleanup(temporary.cleanup)
        live_path = copied / "orchestration-organization-live-cases.yaml"
        live = read_json(live_path)
        live["cases"][0]["fixture"] = "../outside.json"
        write_json(live_path, live)
        report = VALIDATOR.validate(copied)
        self.assertFalse(report["valid"])
        self.assertTrue(any("path escapes eval root" in error for error in report["errors"]))

    def test_unearned_execution_status_is_rejected(self) -> None:
        temporary, copied = self.copy_evals()
        self.addCleanup(temporary.cleanup)
        live_path = copied / "orchestration-organization-live-cases.yaml"
        live = read_json(live_path)
        live["execution_status"] = "passed"
        write_json(live_path, live)
        report = VALIDATOR.validate(copied)
        self.assertFalse(report["valid"])
        self.assertTrue(any("execution_status" in error for error in report["errors"]))


    def test_cli_dry_run_is_declared_and_honest(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR_PATH), "--dry-run"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual("dry-run", report["mode"])
        self.assertEqual("contract-and-fixture-completeness-only", report["validation_scope"])
        self.assertEqual("not-evaluated", report["execution_evidence"])
        self.assert_fingerprint_matches_manifest_and_frozen_source(report["target_runtime_fingerprint"])


if __name__ == "__main__":
    unittest.main()
