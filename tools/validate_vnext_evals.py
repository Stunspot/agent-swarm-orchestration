#!/usr/bin/env python3
"""Validate vNext eval contracts and fixture specifications without executing evals."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_ROOT = ROOT / "canonical" / "evals"
DEFAULT_MANIFEST = "eval-manifest-vnext.yaml"
CONTRACT_VERSION = "aso-vnext-eval-contract/v1"
TARGET_PACKAGE_VERSION = "0.3.0"
PENDING_FINGERPRINT = "PENDING_SOURCE_FREEZE"
REQUIRED_RECEIPTS = {
    "subject-prompt.md",
    "subject-response.md",
    "subject-execution.json",
    "event-trace.json",
    "pre-state.json",
    "post-state.json",
    "evaluator-rubric.json",
    "judge-result.json",
}
REQUIRED_FORBIDDEN_TARGETS = {"canonical", "release", "plugins", "verification/evidence"}


def read_json(path: Path, errors: list[str], label: str) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{label}: missing file {path}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: cannot read JSON from {path}: {exc}")
    return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative_file(root: Path, relative: Any, errors: list[str], label: str) -> Path | None:
    if not isinstance(relative, str) or not relative.strip():
        errors.append(f"{label}: path must be a non-empty string")
        return None
    candidate_text = Path(relative)
    if candidate_text.is_absolute() or ".." in candidate_text.parts:
        errors.append(f"{label}: path escapes eval root: {relative}")
        return None
    candidate = (root / candidate_text).resolve()
    resolved_root = root.resolve()
    if candidate == resolved_root or not candidate.is_relative_to(resolved_root):
        errors.append(f"{label}: path escapes eval root: {relative}")
        return None
    if not candidate.is_file():
        errors.append(f"{label}: missing file {relative}")
        return None
    return candidate


def type_matches(value: Any, expected: str) -> bool:
    mapping = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    return expected in mapping and mapping[expected](value)


def validate_schema(value: Any, schema: dict[str, Any], location: str = "$") -> list[str]:
    """Validate the dependency-free subset of JSON Schema used by these contracts."""
    errors: list[str] = []
    if "oneOf" in schema:
        branches = [validate_schema(value, branch, location) for branch in schema["oneOf"]]
        if sum(not branch for branch in branches) != 1:
            errors.append(f"{location}: value must satisfy exactly one oneOf branch")
        return errors
    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value is not in the allowed enum")
    expected_type = schema.get("type")
    if expected_type and not type_matches(value, expected_type):
        errors.append(f"{location}: expected {expected_type}")
        return errors
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: string is shorter than minLength")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            errors.append(f"{location}: string does not match {pattern}")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: array is shorter than minItems")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(rendered) != len(set(rendered)):
                errors.append(f"{location}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_schema(item, item_schema, f"{location}[{index}]"))
    elif isinstance(value, dict):
        if len(value) < schema.get("minProperties", 0):
            errors.append(f"{location}: object has fewer than minProperties")
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{location}: missing required property {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                errors.append(f"{location}: unexpected properties {', '.join(extras)}")
        for key, property_schema in properties.items():
            if key in value:
                errors.extend(validate_schema(value[key], property_schema, f"{location}.{key}"))
    elif isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{location}: integer is below minimum")
    return errors


def metadata_errors(document: dict[str, Any], manifest: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    for field in ("case_contract_version", "target_package_version", "target_runtime_fingerprint"):
        if document.get(field) != manifest.get(field):
            errors.append(f"{label}: {field} does not match manifest")
    return errors


def validate(eval_root: Path = DEFAULT_EVAL_ROOT, manifest_name: str = DEFAULT_MANIFEST) -> dict[str, Any]:
    eval_root = eval_root.resolve()
    errors: list[str] = []
    counts = {"baseline_cases": 0, "natural_cases": 0, "live_cases": 0, "experiments": 0, "fixtures": 0, "schemas": 0}

    manifest_path = safe_relative_file(eval_root, manifest_name, errors, "manifest")
    manifest = read_json(manifest_path, errors, "manifest") if manifest_path else None
    if not isinstance(manifest, dict):
        return result(errors, counts, None)

    schema_docs: dict[str, dict[str, Any]] = {}
    schema_paths = manifest.get("schemas")
    if not isinstance(schema_paths, dict):
        errors.append("manifest: schemas must be an object")
    else:
        for name in ("manifest", "natural", "live", "experiment", "fixture"):
            schema_path = safe_relative_file(eval_root, schema_paths.get(name), errors, f"schema {name}")
            schema = read_json(schema_path, errors, f"schema {name}") if schema_path else None
            if isinstance(schema, dict):
                schema_docs[name] = schema
                counts["schemas"] += 1
                if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                    errors.append(f"schema {name}: unsupported or missing $schema declaration")

    if "manifest" in schema_docs:
        errors.extend(f"manifest{message[1:]}" for message in validate_schema(manifest, schema_docs["manifest"]))

    if manifest.get("case_contract_version") != CONTRACT_VERSION:
        errors.append("manifest: unexpected case_contract_version")
    if manifest.get("target_package_version") != TARGET_PACKAGE_VERSION:
        errors.append("manifest: unexpected target_package_version")
    fingerprint = manifest.get("target_runtime_fingerprint")
    if fingerprint != PENDING_FINGERPRINT and not (isinstance(fingerprint, str) and re.fullmatch(r"[0-9a-f]{64}", fingerprint)):
        errors.append("manifest: target_runtime_fingerprint must be PENDING_SOURCE_FREEZE or lowercase SHA-256")

    baseline_manifest_path = safe_relative_file(eval_root, manifest.get("baseline_manifest"), errors, "baseline manifest")
    baseline_manifest = read_json(baseline_manifest_path, errors, "baseline manifest") if baseline_manifest_path else None
    baseline_files = manifest.get("baseline_files", [])
    if isinstance(baseline_manifest, dict) and baseline_manifest.get("files") != baseline_files:
        errors.append("manifest: baseline_files do not exactly match baseline_manifest files")

    contracts = manifest.get("baseline_contracts", [])
    contract_by_path = {item.get("path"): item for item in contracts if isinstance(item, dict)}
    if isinstance(contracts, list) and len(contract_by_path) != len(contracts):
        errors.append("manifest: baseline_contracts paths must be unique")
    if set(contract_by_path) != set(baseline_files) if isinstance(baseline_files, list) else True:
        errors.append("manifest: baseline_contracts paths do not exactly match baseline_files")

    all_ids: list[str] = []
    if isinstance(baseline_files, list):
        for relative in baseline_files:
            baseline_path = safe_relative_file(eval_root, relative, errors, f"baseline catalog {relative}")
            baseline = read_json(baseline_path, errors, f"baseline catalog {relative}") if baseline_path else None
            contract = contract_by_path.get(relative, {})
            if baseline_path and isinstance(contract, dict) and contract.get("sha256") != sha256(baseline_path):
                errors.append(f"baseline catalog {relative}: SHA-256 differs from pinned custody")
            if isinstance(baseline, dict):
                if contract.get("case_contract_version") != baseline.get("package_version"):
                    errors.append(f"baseline catalog {relative}: historical contract version does not match package_version")
                cases = baseline.get("cases", [])
                if isinstance(cases, list):
                    counts["baseline_cases"] += len(cases)
                    all_ids.extend(case.get("id") for case in cases if isinstance(case, dict) and isinstance(case.get("id"), str))

    indispensable = manifest.get("indispensable_dimensions", [])
    dimension_set = set(indispensable) if isinstance(indispensable, list) else set()
    suite_by_name: dict[str, tuple[str, dict[str, Any]]] = {}
    files = manifest.get("files", [])
    if isinstance(files, list):
        for relative in files:
            suite_path = safe_relative_file(eval_root, relative, errors, f"vNext catalog {relative}")
            suite = read_json(suite_path, errors, f"vNext catalog {relative}") if suite_path else None
            if not isinstance(suite, dict):
                continue
            suite_name = suite.get("suite")
            if not isinstance(suite_name, str) or not suite_name:
                errors.append(f"vNext catalog {relative}: missing suite")
                continue
            if suite_name in suite_by_name:
                errors.append(f"vNext catalog {relative}: duplicate suite {suite_name}")
            suite_by_name[suite_name] = (relative, suite)
            errors.extend(metadata_errors(suite, manifest, f"vNext catalog {relative}"))

    expected_suites = {
        "orchestration-organization-natural-qualification": "natural",
        "orchestration-organization-live-control": "live",
        "orchestration-role-synergy-ablation": "experiment",
    }
    if set(suite_by_name) != set(expected_suites):
        errors.append("manifest: files must resolve to exactly the natural, live, and experiment suites")

    natural_entry = suite_by_name.get("orchestration-organization-natural-qualification")
    if natural_entry:
        relative, natural = natural_entry
        if "natural" in schema_docs:
            errors.extend(f"{relative}{message[1:]}" for message in validate_schema(natural, schema_docs["natural"]))
        cases = natural.get("cases", [])
        if isinstance(cases, list):
            counts["natural_cases"] = len(cases)
            expected_ids = [f"ASO-ON{index:03d}" for index in range(1, 17)]
            ids = [case.get("id") for case in cases if isinstance(case, dict)]
            if ids != expected_ids:
                errors.append(f"{relative}: natural case IDs must be ASO-ON001 through ASO-ON016 in order")
            used_dimensions: set[str] = set()
            for case in cases:
                if not isinstance(case, dict):
                    continue
                dimensions = case.get("dimensions", [])
                used_dimensions.update(dimensions if isinstance(dimensions, list) else [])
                unknown = sorted(set(dimensions) - dimension_set) if isinstance(dimensions, list) else []
                if unknown:
                    errors.append(f"{relative} {case.get('id')}: unknown dimensions {', '.join(unknown)}")
            missing = sorted(dimension_set - used_dimensions)
            if missing:
                errors.append(f"{relative}: indispensable dimensions lack natural-case coverage: {', '.join(missing)}")
            all_ids.extend(item for item in ids if isinstance(item, str))

    live_entry = suite_by_name.get("orchestration-organization-live-control")
    if live_entry:
        relative, live = live_entry
        if "live" in schema_docs:
            errors.extend(f"{relative}{message[1:]}" for message in validate_schema(live, schema_docs["live"]))
        if live.get("execution_status") != "specified-not-run":
            errors.append(f"{relative}: execution_status must remain specified-not-run until evidence exists")
        receipts = live.get("required_receipts", [])
        if isinstance(receipts, list) and set(receipts) != REQUIRED_RECEIPTS:
            errors.append(f"{relative}: required_receipts do not match the live evidence contract")
        fixture_root_value = live.get("fixture_root")
        fixture_root_path = (eval_root / fixture_root_value).resolve() if isinstance(fixture_root_value, str) else None
        if fixture_root_path is None or not fixture_root_path.is_relative_to(eval_root) or not fixture_root_path.is_dir():
            errors.append(f"{relative}: fixture_root is missing or escapes eval root")
        cases = live.get("cases", [])
        if isinstance(cases, list):
            counts["live_cases"] = len(cases)
            expected_ids = [f"ASO-L{index:03d}" for index in range(1, 7)]
            ids = [case.get("id") for case in cases if isinstance(case, dict)]
            if ids != expected_ids:
                errors.append(f"{relative}: live case IDs must be ASO-L001 through ASO-L006 in order")
            for case in cases:
                if not isinstance(case, dict):
                    continue
                case_id = case.get("id", "<unknown>")
                dimensions = case.get("dimensions", [])
                unknown = sorted(set(dimensions) - dimension_set) if isinstance(dimensions, list) else []
                if unknown:
                    errors.append(f"{relative} {case_id}: unknown dimensions {', '.join(unknown)}")
                fixture_path = safe_relative_file(eval_root, case.get("fixture"), errors, f"fixture {case_id}")
                if fixture_path and fixture_root_path and not fixture_path.is_relative_to(fixture_root_path):
                    errors.append(f"fixture {case_id}: path is outside declared fixture_root")
                fixture = read_json(fixture_path, errors, f"fixture {case_id}") if fixture_path else None
                if isinstance(fixture, dict):
                    counts["fixtures"] += 1
                    if "fixture" in schema_docs:
                        errors.extend(f"fixture {case_id}{message[1:]}" for message in validate_schema(fixture, schema_docs["fixture"]))
                    errors.extend(metadata_errors(fixture, manifest, f"fixture {case_id}"))
                    if fixture.get("case_id") != case_id:
                        errors.append(f"fixture {case_id}: case_id mismatch")
                    if fixture.get("purpose") != case.get("concern"):
                        errors.append(f"fixture {case_id}: purpose does not match live case concern")
                    if fixture.get("oracle") != case.get("required_observations"):
                        errors.append(f"fixture {case_id}: oracle does not match required_observations")
                    forbidden = fixture.get("forbidden_targets", [])
                    if isinstance(forbidden, list) and not REQUIRED_FORBIDDEN_TARGETS.issubset(forbidden):
                        errors.append(f"fixture {case_id}: forbidden_targets omit protected repository surfaces")
            all_ids.extend(item for item in ids if isinstance(item, str))

    experiment_entry = suite_by_name.get("orchestration-role-synergy-ablation")
    if experiment_entry:
        relative, experiment_suite = experiment_entry
        if "experiment" in schema_docs:
            errors.extend(f"{relative}{message[1:]}" for message in validate_schema(experiment_suite, schema_docs["experiment"]))
        if experiment_suite.get("execution_status") != "specified-not-run":
            errors.append(f"{relative}: execution_status must remain specified-not-run until evidence exists")
        experiments = experiment_suite.get("experiments", [])
        if isinstance(experiments, list):
            counts["experiments"] = len(experiments)
            expected_ids = [f"ASO-X{index:03d}" for index in range(1, 4)]
            ids = [item.get("id") for item in experiments if isinstance(item, dict)]
            if ids != expected_ids:
                errors.append(f"{relative}: experiment IDs must be ASO-X001 through ASO-X003 in order")
            for experiment in experiments:
                if not isinstance(experiment, dict):
                    continue
                dimensions = experiment.get("dimensions", [])
                gates = experiment.get("safety_gates", [])
                unknown = (set(dimensions) | set(gates)) - dimension_set if isinstance(dimensions, list) and isinstance(gates, list) else set()
                if unknown:
                    errors.append(f"{relative} {experiment.get('id')}: unknown dimensions or gates {', '.join(sorted(unknown))}")
            all_ids.extend(item for item in ids if isinstance(item, str))

    duplicates = sorted({case_id for case_id in all_ids if all_ids.count(case_id) > 1})
    if duplicates:
        errors.append(f"eval catalogs: duplicate IDs across suites: {', '.join(duplicates)}")

    return result(errors, counts, fingerprint)


def result(errors: list[str], counts: dict[str, int], fingerprint: Any) -> dict[str, Any]:
    return {
        "format": "aso-vnext-eval-contract-validation/v1",
        "valid": not errors,
        "mode": "dry-run",
        "validation_scope": "contract-and-fixture-completeness-only",
        "execution_evidence": "not-evaluated",
        "target_runtime_fingerprint": fingerprint,
        "counts": counts,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-root", type=Path, default=DEFAULT_EVAL_ROOT)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly select read-only contract validation; this tool has no mutation or eval-execution mode.",
    )
    args = parser.parse_args()
    report = validate(args.eval_root, args.manifest)
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
