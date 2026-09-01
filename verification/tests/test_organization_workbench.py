from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "canonical" / "skills" / "agent-swarm-orchestration"
EVAL_ROOT = REPO_ROOT / "canonical" / "evals"


class OrganizationWorkbenchTests(unittest.TestCase):
    def test_skill_local_links_resolve(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        links = set(re.findall(r"`((?:references|assets)/[^`]+)`", text))
        self.assertGreaterEqual(len(links), 15)
        missing = sorted(link for link in links if not (SKILL_ROOT / link).is_file())
        self.assertEqual([], missing)

    def test_open_organization_tools_exist(self) -> None:
        required = {
            "assets/organization-sketch.template.md",
            "assets/contribution-card.template.md",
            "assets/cross-response-packet.template.md",
            "assets/organization-transition.template.md",
            "references/organization-design.md",
            "references/interaction-resolution-and-adaptation.md",
            "references/pattern-recipes.md",
            "references/qualification-and-evaluation.md",
            "examples/adaptive-civic-organization-example.md",
        }
        self.assertEqual([], sorted(path for path in required if not (SKILL_ROOT / path).is_file()))

    def test_v1_plan_contract_remains_closed_and_unchanged(self) -> None:
        schema = json.loads((SKILL_ROOT / "assets" / "swarm-plan.schema.json").read_text(encoding="utf-8"))
        self.assertEqual("cd-agent-swarm-plan/v1", schema["properties"]["format"]["const"])
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            ["direct", "enlist", "assemble", "chain", "recover"],
            schema["properties"]["regime"]["enum"],
        )
        self.assertNotIn("organization", schema["properties"])
        self.assertNotIn("pattern", schema["properties"])

    def test_vnext_eval_catalog_is_complete_and_unique(self) -> None:
        manifest = json.loads((EVAL_ROOT / "eval-manifest-vnext.yaml").read_text(encoding="utf-8"))
        for relative in manifest["baseline_files"] + manifest["files"]:
            self.assertTrue((EVAL_ROOT / relative).is_file(), relative)
        for dimension in (
            "contribution_causality",
            "exposure_control",
            "resolver_integrity",
            "state_transition_integrity",
            "organizational_non_rigidity",
        ):
            self.assertIn(dimension, manifest["indispensable_dimensions"])

        natural = json.loads(
            (EVAL_ROOT / "orchestration-organization-natural-qualification-cases.yaml").read_text(encoding="utf-8")
        )
        ids = [case["id"] for case in natural["cases"]]
        self.assertEqual(16, len(ids))
        self.assertEqual(16, len(set(ids)))
        self.assertEqual([f"ASO-ON{index:03d}" for index in range(1, 17)], ids)

    def test_examples_are_explicitly_non_exhaustive(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        design = (SKILL_ROOT / "references" / "organization-design.md").read_text(encoding="utf-8").lower()
        recipes = (SKILL_ROOT / "references" / "pattern-recipes.md").read_text(encoding="utf-8").lower()
        self.assertIn("never mistake the examples for a closed taxonomy", skill)
        self.assertIn("no list is complete", design)
        self.assertIn("invent another composition", recipes)

    def test_stakeholder_representation_boundary_is_present(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        example = (SKILL_ROOT / "examples" / "adaptive-civic-organization-example.md").read_text(encoding="utf-8").lower()
        for text in (skill, example):
            self.assertIn("stakeholder", text)
            self.assertIn("authorized", text)
        self.assertIn("no agent is authorized to speak *as* residents", example)


if __name__ == "__main__":
    unittest.main()
