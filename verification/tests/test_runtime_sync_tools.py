from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_PATH = REPO_ROOT / "tools" / "sync_runtime_trees.py"
PARITY_PATH = REPO_ROOT / "tools" / "check_runtime_parity.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sync_runtime_trees = _load_module("sync_runtime_trees", SYNC_PATH)
check_runtime_parity = _load_module("check_runtime_parity", PARITY_PATH)


class RuntimeSyncToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="aso-runtime-sync-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "canonical" / "skills" / "agent-swarm-orchestration"
        self.destinations = {
            "plugin": self.root / "plugins" / "agent-swarm-orchestration" / "skills" / "agent-swarm-orchestration",
            "codex": self.root / "release" / "codex" / "agent-swarm-orchestration",
            "claude": self.root / "release" / "claude" / "agent-swarm-orchestration",
        }
        self.relative_destinations = {
            "plugin": Path("plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration"),
            "codex": Path("release/codex/agent-swarm-orchestration"),
            "claude": Path("release/claude/agent-swarm-orchestration"),
        }
        self.source.mkdir(parents=True)
        for destination in self.destinations.values():
            destination.mkdir(parents=True)

        patches = (
            mock.patch.object(sync_runtime_trees, "ROOT", self.root),
            mock.patch.object(sync_runtime_trees, "SOURCE", self.source),
            mock.patch.object(sync_runtime_trees, "DESTINATIONS", self.destinations),
            mock.patch.object(sync_runtime_trees, "EXPECTED_RELATIVE_DESTINATIONS", self.relative_destinations),
            mock.patch.object(check_runtime_parity, "SOURCE", self.source),
            mock.patch.object(check_runtime_parity, "DESTINATIONS", self.destinations),
        )
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def _write_source(self, relative: str, content: str) -> None:
        target = self.source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def _write_destination(self, name: str, relative: str, content: str) -> None:
        target = self.destinations[name] / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def _mirror_source(self) -> None:
        source_files = sync_runtime_trees.files_under(self.source)
        for destination in self.destinations.values():
            for relative, source_path in source_files.items():
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source_path.read_bytes())

    def test_sync_check_returns_drift_exit_and_does_not_mutate(self) -> None:
        self._write_source("runtime.txt", "canonical")
        self._mirror_source()
        self._write_destination("plugin", "runtime.txt", "drifted")

        stdout = io.StringIO()
        with mock.patch.object(sys, "argv", [str(SYNC_PATH)]), contextlib.redirect_stdout(stdout):
            result = sync_runtime_trees.main()

        report = json.loads(stdout.getvalue())
        self.assertEqual(1, result)
        self.assertEqual("check", report["mode"])
        self.assertEqual(["runtime.txt"], report["parity"]["plugin"]["changed"])
        self.assertEqual("drifted", (self.destinations["plugin"] / "runtime.txt").read_text(encoding="utf-8"))

    def test_parity_main_returns_zero_then_one(self) -> None:
        self._write_source("runtime.txt", "canonical")
        self._mirror_source()

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(0, check_runtime_parity.main())
        self.assertTrue(json.loads(stdout.getvalue())["valid"])

        self._write_destination("claude", "runtime.txt", "drifted")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(1, check_runtime_parity.main())
        self.assertEqual(["runtime.txt"], json.loads(stdout.getvalue())["checks"]["claude"]["changed"])

    def test_managed_dirty_continuation_is_explicit_and_rejects_noncanonical_paths(self) -> None:
        self._write_source("runtime.txt", "new")
        self._mirror_source()
        self._write_destination("plugin", "runtime.txt", "old")
        plans = {name: sync_runtime_trees.plan_for(path) for name, path in self.destinations.items()}
        plugin_path = self.relative_destinations["plugin"].as_posix() + "/runtime.txt"
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=(" M " + plugin_path + "\0").encode("utf-8"),
            stderr=b"",
        )
        with mock.patch.object(sync_runtime_trees.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "already dirty"):
                sync_runtime_trees.assert_destination_git_clean(plans)
            accepted = sync_runtime_trees.assert_destination_git_clean(
                plans,
                accept_managed_dirty=True,
            )
        self.assertEqual([{"status": " M", "path": plugin_path}], accepted)

        extra = self.destinations["plugin"] / "extra.txt"
        extra.write_text("user", encoding="utf-8")
        extra_path = self.relative_destinations["plugin"].as_posix() + "/extra.txt"
        completed.stdout = ("?? " + extra_path + "\0").encode("utf-8")
        with mock.patch.object(sync_runtime_trees.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "no canonical source counterpart"):
                sync_runtime_trees.assert_destination_git_clean(
                    plans,
                    accept_managed_dirty=True,
                )

    def test_no_prune_refuses_removal_and_preserves_extra_file(self) -> None:
        self._write_source("runtime.txt", "canonical")
        self._write_destination("plugin", "runtime.txt", "canonical")
        self._write_destination("plugin", "extra.txt", "preserve me")
        plan = sync_runtime_trees.plan_for(self.destinations["plugin"])

        with self.assertRaisesRegex(RuntimeError, "explicit --prune"):
            sync_runtime_trees.apply_plan(self.destinations["plugin"], plan, prune=False)

        self.assertEqual("preserve me", (self.destinations["plugin"] / "extra.txt").read_text(encoding="utf-8"))

    def test_explicit_prune_removes_only_planned_extra_file(self) -> None:
        self._write_source("runtime.txt", "canonical")
        self._write_destination("plugin", "runtime.txt", "canonical")
        self._write_destination("plugin", "extra.txt", "remove me")
        plan = sync_runtime_trees.plan_for(self.destinations["plugin"])

        sync_runtime_trees.apply_plan(self.destinations["plugin"], plan, prune=True)

        self.assertFalse((self.destinations["plugin"] / "extra.txt").exists())
        self.assertTrue(sync_runtime_trees.parity(self.destinations["plugin"])["valid"])

    def test_file_symlink_target_is_refused_without_touching_referent(self) -> None:
        self._write_source("runtime.txt", "canonical")
        outside = self.root / "outside.txt"
        outside.write_text("sentinel", encoding="utf-8")
        link = self.destinations["plugin"] / "runtime.txt"
        try:
            link.symlink_to(outside)
            reparse_detection = contextlib.nullcontext()
        except (NotImplementedError, OSError):
            link.write_text("simulated file-link", encoding="utf-8")
            real_lstat_or_none = sync_runtime_trees._lstat_or_none

            def simulated_reparse_metadata(path):
                info = real_lstat_or_none(path)
                if path == link and info is not None:
                    return mock.Mock(
                        st_mode=info.st_mode,
                        st_file_attributes=sync_runtime_trees.REPARSE_ATTRIBUTE,
                    )
                return info

            reparse_detection = mock.patch.object(
                sync_runtime_trees,
                "_lstat_or_none",
                side_effect=simulated_reparse_metadata,
            )

        with reparse_detection, self.assertRaisesRegex(RuntimeError, "reparse entry refused"):
            sync_runtime_trees.apply_plan(
                self.destinations["plugin"],
                {"copy": ["runtime.txt"], "remove": []},
            )

        self.assertEqual("sentinel", outside.read_text(encoding="utf-8"))

    def test_directory_symlink_is_rejected_when_supported(self) -> None:
        target = self.root / "outside-directory"
        target.mkdir()
        (target / "payload.txt").write_text("sentinel", encoding="utf-8")
        link = self.source / "linked-directory"
        try:
            link.symlink_to(target, target_is_directory=True)
        except (NotImplementedError, OSError) as exc:
            self.skipTest(f"directory symlink unavailable: {exc}")

        with self.assertRaisesRegex(RuntimeError, "reparse directory is forbidden"):
            sync_runtime_trees.files_under(self.source)

    @unittest.skipUnless(os.name == "nt", "Windows junction probe")
    def test_directory_junction_is_rejected_when_supported(self) -> None:
        target = self.root / "junction-target"
        target.mkdir()
        link = self.source / "junction"
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            self.skipTest(f"junction creation unavailable: {result.stderr or result.stdout}")

        with self.assertRaisesRegex(RuntimeError, "reparse directory is forbidden"):
            sync_runtime_trees.files_under(self.source)


    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_destination_parent_junction_inserted_after_planning_refuses_copy_without_touching_referent(self) -> None:
        self._write_source("nested/runtime.txt", "canonical")
        self._write_destination("plugin", "nested/runtime.txt", "drifted")
        destination = self.destinations["plugin"]
        plan = sync_runtime_trees.plan_for(destination)
        self.assertEqual(["nested/runtime.txt"], plan["copy"])

        link = destination / "nested"
        (link / "runtime.txt").unlink()
        link.rmdir()
        outside = self.root / "outside-copy"
        outside.mkdir()
        referent = outside / "runtime.txt"
        referent.write_text("sentinel", encoding="utf-8")
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(outside)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            self.skipTest(f"junction creation unavailable: {result.stderr or result.stdout}")

        with self.assertRaisesRegex(RuntimeError, "reparse point is forbidden"):
            sync_runtime_trees.apply_plan(destination, plan)

        self.assertEqual("sentinel", referent.read_text(encoding="utf-8"))

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_destination_parent_junction_inserted_after_planning_refuses_removal_without_touching_referent(self) -> None:
        self._write_source("runtime.txt", "canonical")
        self._write_destination("plugin", "runtime.txt", "canonical")
        self._write_destination("plugin", "nested/extra.txt", "planned extra")
        destination = self.destinations["plugin"]
        plan = sync_runtime_trees.plan_for(destination)
        self.assertEqual(["nested/extra.txt"], plan["remove"])

        link = destination / "nested"
        (link / "extra.txt").unlink()
        link.rmdir()
        outside = self.root / "outside-remove"
        outside.mkdir()
        referent = outside / "extra.txt"
        referent.write_text("sentinel", encoding="utf-8")
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(outside)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            self.skipTest(f"junction creation unavailable: {result.stderr or result.stdout}")

        with self.assertRaisesRegex(RuntimeError, "reparse point is forbidden"):
            sync_runtime_trees.apply_plan(destination, plan, prune=True)

        self.assertEqual("sentinel", referent.read_text(encoding="utf-8"))

    def test_process_interrupts_roll_back_the_multi_destination_transaction(self) -> None:
        self._write_source("runtime.txt", "new")
        self._write_source("created.txt", "created")
        for name in self.destinations:
            self._write_destination(name, "runtime.txt", "old")

        real_apply = sync_runtime_trees.apply_plan
        for interruption in (KeyboardInterrupt, SystemExit):
            with self.subTest(interruption=interruption.__name__):
                def interrupt_second_destination(destination, plan, **kwargs):
                    if destination == self.destinations["codex"]:
                        raise interruption("synthetic transaction interruption")
                    return real_apply(destination, plan, **kwargs)

                with (
                    mock.patch.object(sys, "argv", [str(SYNC_PATH), "--apply"]),
                    mock.patch.object(sync_runtime_trees, "assert_destination_git_clean", return_value=[]),
                    mock.patch.object(sync_runtime_trees, "apply_plan", side_effect=interrupt_second_destination),
                    self.assertRaises(interruption),
                ):
                    sync_runtime_trees.main()

                for destination in self.destinations.values():
                    self.assertEqual("old", (destination / "runtime.txt").read_text(encoding="utf-8"))
                    self.assertFalse((destination / "created.txt").exists())
    def test_stage_and_verify_uses_temp_roots_without_committing(self) -> None:
        self._write_source("runtime.txt", "canonical")
        for name in self.destinations:
            self._write_destination(name, "runtime.txt", "drifted")
        plans = {name: sync_runtime_trees.plan_for(destination) for name, destination in self.destinations.items()}

        sync_runtime_trees.stage_and_verify(plans, prune=False)

        for destination in self.destinations.values():
            self.assertEqual("drifted", (destination / "runtime.txt").read_text(encoding="utf-8"))
            self.assertFalse(sync_runtime_trees.parity(destination)["valid"])

    def test_apply_mode_stages_then_reaches_parity(self) -> None:
        self._write_source("runtime.txt", "canonical")
        for name in self.destinations:
            self._write_destination(name, "runtime.txt", "drifted")

        stdout = io.StringIO()
        with (
            mock.patch.object(sys, "argv", [str(SYNC_PATH), "--apply"]),
            mock.patch.object(sync_runtime_trees, "assert_destination_git_clean", return_value=[]),
            contextlib.redirect_stdout(stdout),
        ):
            self.assertEqual(0, sync_runtime_trees.main())

        report = json.loads(stdout.getvalue())
        self.assertEqual("apply", report["mode"])
        for destination in self.destinations.values():
            self.assertTrue(sync_runtime_trees.parity(destination)["valid"])

    def test_rollback_restores_changed_created_and_pruned_files(self) -> None:
        self._write_source("runtime.txt", "new")
        self._write_source("created.txt", "created")
        for name in self.destinations:
            self._write_destination(name, "runtime.txt", "old")
            self._write_destination(name, "extra.txt", f"extra-{name}")
        before = {
            name: {relative: path.read_bytes() for relative, path in sync_runtime_trees.files_under(destination).items()}
            for name, destination in self.destinations.items()
        }
        plans = {name: sync_runtime_trees.plan_for(destination) for name, destination in self.destinations.items()}
        snapshots = sync_runtime_trees.snapshot_for_rollback(plans)

        for name, destination in self.destinations.items():
            sync_runtime_trees.apply_plan(destination, plans[name], prune=True)
        sync_runtime_trees.rollback(snapshots)

        after = {
            name: {relative: path.read_bytes() for relative, path in sync_runtime_trees.files_under(destination).items()}
            for name, destination in self.destinations.items()
        }
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
