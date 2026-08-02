# Install Agent Swarm Orchestration in Codex

This guide installs version 0.1.0 as one self-contained Codex skill folder. The distribution has been generated and statically validated, but the procedure has not been exercised on a clean customer host. Confirm the skill location and reload behavior for your current Codex version before treating installation as complete.

## Before you begin

You need:

- a Codex installation that supports local skills;
- permission to add one folder to the skill location used by that installation;
- either the released folder or the ZIP from this product;
- live Codex collaboration tools when you want the skill to create or coordinate agents;
- Python 3 only if you want to run the optional Swarm Plan validator.

Back up an existing `agent-swarm-orchestration` installation before replacing it. Keep that backup outside the destination folder so removal and rollback remain unambiguous.

## Choose the correct package surface

Use one of these customer distribution surfaces:

- **Released folder:** `release/codex/agent-swarm-orchestration/`
- **ZIP archive:** `release-assets/agent-swarm-orchestration-v0.1.0.zip`

Do not install the whole product root. The `canonical/` tree is maintained source, while the release folder and ZIP are customer transport surfaces.

## Install from the released folder

1. Find the local skill directory used by your Codex installation.

   In Codex setups that use the user-level `%USERPROFILE%\.codex\skills` directory, the final path would be `%USERPROFILE%\.codex\skills\agent-swarm-orchestration`. If your installation uses another managed location, follow that host configuration instead.

2. Copy the entire `release/codex/agent-swarm-orchestration` folder into the Codex skill directory.

3. Confirm the resulting folder has `SKILL.md` directly inside it:

   ```text
   <Codex skill directory>/agent-swarm-orchestration/SKILL.md
   ```

4. Confirm the folder contains 17 files. Keep the `agents`, `assets`, `examples`, `references`, `scripts`, and `tests` subfolders with `SKILL.md`.

5. Reload Codex or start a fresh task if your host requires a new session to discover local skills.

**Expected result:** Codex can resolve the skill name `agent-swarm-orchestration`. Because clean-host discovery has not been tested for this release, only an observed result in your host establishes this step.

## Install from the ZIP

1. Before extraction, calculate the archive SHA-256:

   ```powershell
   Get-FileHash -Algorithm SHA256 .\agent-swarm-orchestration-v0.1.0.zip
   ```

   The expected value is `1889b0b1f20a4cc98c9ccf3c95d7a1b64cea0e4524cf3e16b00b90ccd2cf6683`, which is also recorded in `release-assets/checksums.sha256`. If the value differs, stop and obtain the package again from the authorized source.

2. Extract `agent-swarm-orchestration-v0.1.0.zip` to a temporary location.
3. Confirm the archive produces one top-level folder named `agent-swarm-orchestration`.
4. Confirm `SKILL.md` is directly inside that folder, not inside a second nested folder with the same name.
5. Copy the extracted folder into the skill directory used by your Codex installation.
6. Reload Codex or start a fresh task if required by the host.

**Expected result:** the installed tree matches the released folder shape and contains 17 files.

## Check discovery and first invocation

Start a new task and enter:

```text
Use $agent-swarm-orchestration to decide whether this task earns multiple agents: compare three independent folders read-only, then return one evidence-backed recommendation. Explain the selected topology briefly and keep the root responsible for verification.
```

A successful check requires both of these observations:

1. Codex recognizes the named skill rather than treating `$agent-swarm-orchestration` as unknown text.
2. Codex applies the skill's admission logic. It may choose direct work if the actual task does not justify a swarm.

If the task genuinely needs agents, also confirm that the current Codex task exposes collaboration tools. The skill reads their live names, schemas, concurrency, waiting, messaging, interruption, and lifecycle behavior at task time; the package does not supply those tools.

## Optionally validate a Swarm Plan

Copy `assets/swarm-plan.template.json` to a working file, edit the copy, and run the packaged validator from the skill root:

```text
python <skill-root>/scripts/validate_swarm_plan.py <path-to-your-swarm-plan.json>
```

Successful output is:

```text
VALID cd-agent-swarm-plan/v1
```

The validator checks declared fields, dependency references and cycles, terminal-state consistency, and concurrent active write collisions. It does not judge whether the task truly deserves agents, whether a packet has enough context, whether returned claims are true, or whether a sequential writer started from reconciled bytes.

## Remove the skill

1. Preserve any customer-created plans or ledgers stored inside the installed folder by moving copies to a separate working location.
2. Remove only the exact installed `agent-swarm-orchestration` folder from the Codex skill directory.
3. Reload Codex or start a fresh task if the host caches skill discovery.
4. Confirm the folder is absent. If your Codex host exposes a skill list, confirm the skill is no longer listed there.

Removing the folder does not cancel already running agents, undo files they changed, or roll back external actions. Reconcile those surfaces separately before removal.

## Roll back a replacement

1. Remove the replacement folder only after preserving any evidence you need.
2. Restore the previously backed-up `agent-swarm-orchestration` folder to the same host skill location.
3. Reload the host if required.
4. Confirm the restored `SKILL.md` and expected version bytes are present before resuming work.

If any copy, removal, or reload result is uncertain, stop with the installed state marked **unknown**, inspect the exact destination folder, and continue only from observed bytes. See [Troubleshooting](TROUBLESHOOTING.md) for recovery paths.
