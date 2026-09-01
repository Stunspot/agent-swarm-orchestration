from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "validate_source_development.py"
SPEC = importlib.util.spec_from_file_location("validate_source_development", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SourceDevelopmentCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aso-source-custody-")
        self.root = Path(self.temporary.name)
        source = self.root / MODULE.RUNTIME_RELATIVE
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text("source\n", encoding="utf-8")
        for relative in MODULE.MIRRORS.values():
            destination = self.root / relative
            destination.mkdir(parents=True)
            (destination / "SKILL.md").write_text("source\n", encoding="utf-8")

        fingerprint = MODULE.tree_digest(source)
        self.original_fingerprint = MODULE.RUNTIME_FINGERPRINT
        MODULE.RUNTIME_FINGERPRINT = fingerprint

        plugin_path = self.root / "plugins/agent-swarm-orchestration/.codex-plugin/plugin.json"
        plugin_path.parent.mkdir(parents=True, exist_ok=True)
        self.write_json(plugin_path, {"version": MODULE.VERSION})

        eval_path = self.root / "canonical/evals/eval-manifest-vnext.yaml"
        eval_path.parent.mkdir(parents=True, exist_ok=True)
        self.write_json(eval_path, {
            "target_package_version": MODULE.VERSION,
            "target_runtime_fingerprint": fingerprint,
        })

        self.package_path = self.root / "package-manifest.json"
        self.package = {
            "version": MODULE.VERSION,
            "runtime_version": MODULE.VERSION,
            "status": "source-development",
            "runtime_fingerprint": fingerprint,
            "release_baseline": copy.deepcopy(MODULE.BASELINE),
            "distributions": {
                name: {"status": status}
                for name, status in MODULE.DISTRIBUTION_STATUSES.items()
            },
            "authority": copy.deepcopy(MODULE.SOURCE_AUTHORITY),
            "evidence": copy.deepcopy(MODULE.EVIDENCE_DENIALS),
        }
        self.write_json(self.package_path, self.package)

        self.baseline_hashes = {}
        for index, relative in enumerate(MODULE.BASELINE_HASHES):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f"baseline-{index}".encode("utf-8"))
            self.baseline_hashes[relative] = MODULE.sha256(path)

    def tearDown(self):
        MODULE.RUNTIME_FINGERPRINT = self.original_fingerprint
        self.temporary.cleanup()

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def validate(self):
        return MODULE.validate_metadata(self.root, self.baseline_hashes)

    def test_valid_source_development_contract(self):
        report = self.validate()
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual("source-development-unreleased", report["state"])
        self.assertIn("public release", report["claims_not_established"])

    def test_fingerprint_mismatch_is_rejected(self):
        self.package["runtime_fingerprint"] = "0" * 64
        self.write_json(self.package_path, self.package)
        self.assertFalse(self.validate()["valid"])

    def test_plugin_version_mismatch_is_rejected(self):
        self.write_json(
            self.root / "plugins/agent-swarm-orchestration/.codex-plugin/plugin.json",
            {"version": "0.2.3"},
        )
        self.assertTrue(any("plugin manifest" in error for error in self.validate()["errors"]))

    def test_distribution_status_mismatch_is_rejected(self):
        self.package["distributions"]["codex_plugin"]["status"] = "release-candidate"
        self.write_json(self.package_path, self.package)
        self.assertTrue(any("distribution statuses" in error for error in self.validate()["errors"]))

    def test_authority_expansion_is_rejected(self):
        self.package["authority"]["public_publication"] = True
        self.write_json(self.package_path, self.package)
        self.assertTrue(any("public_publication" in error for error in self.validate()["errors"]))

    def test_extra_authority_key_is_rejected(self):
        self.package["authority"]["deployment"] = True
        self.write_json(self.package_path, self.package)
        self.assertTrue(any("authority contract differs" in error for error in self.validate()["errors"]))

    def test_extra_distribution_is_rejected(self):
        self.package["distributions"]["production"] = {"status": "published"}
        self.write_json(self.package_path, self.package)
        self.assertTrue(any("distribution keys differ" in error for error in self.validate()["errors"]))

    def test_contradictory_evidence_is_rejected(self):
        self.package["evidence"]["installation"] = "not-performed; performed successfully"
        self.write_json(self.package_path, self.package)
        self.assertTrue(any("evidence.installation" in error for error in self.validate()["errors"]))

    def test_mirror_drift_is_rejected(self):
        (self.root / MODULE.MIRRORS["claude"] / "SKILL.md").write_text("drift\n", encoding="utf-8")
        self.assertTrue(any("claude runtime mirror differs" in error for error in self.validate()["errors"]))

    def test_frozen_baseline_mutation_is_rejected(self):
        relative = next(iter(self.baseline_hashes))
        (self.root / relative).write_bytes(b"changed")
        self.assertTrue(any("frozen custody hash changed" in error for error in self.validate()["errors"]))

    def test_development_release_artifact_is_rejected(self):
        artifact = self.root / "release-assets/v0.3.0-dev"
        artifact.mkdir(parents=True)
        self.assertTrue(any("unreleased development artifacts exist" in error for error in self.validate()["errors"]))


if __name__ == "__main__":
    unittest.main()