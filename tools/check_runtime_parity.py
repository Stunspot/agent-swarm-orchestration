#!/usr/bin/env python3
"""Read-only parity check for canonical and tracked Agent Swarm runtime trees."""

from __future__ import annotations

import json

from sync_runtime_trees import DESTINATIONS, SOURCE, assert_layout, files_under, parity, tree_fingerprint


def main() -> int:
    assert_layout()
    checks = {name: parity(destination) for name, destination in DESTINATIONS.items()}
    valid = all(bool(check["valid"]) for check in checks.values())
    print(json.dumps({
        "format": "aso-runtime-parity/v2",
        "valid": valid,
        "canonical_files": len(files_under(SOURCE)),
        "canonical_fingerprint": tree_fingerprint(SOURCE),
        "checks": checks,
    }, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
