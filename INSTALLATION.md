# Install Agent Swarm Orchestration

Version 0.3.2 contains one skill. Choose the Codex plugin to install it through a marketplace, or choose a standalone package to install the skill directly.

| Your host and preference | Choose |
|---|---|
| Codex with plugin management | [Codex plugin](#install-the-codex-plugin) |
| Codex with a project or personal skills folder | [Standalone Codex skill](#install-the-standalone-skill-in-codex) |
| Claude or another host that accepts Agent Skills uploads | [One-skill ZIP](#install-the-skill-in-claude-or-another-host) |

Your host must support the installation method you choose. It must also expose worker controls in the current task if you want the skill to dispatch agents. Python 3 is optional for checking packages and plans. Back up an existing standalone skill folder outside the install destination before replacing it.

## Install the Codex plugin

The plugin bundles the skill and registers it with Codex. Run these commands in a terminal with the Codex CLI.

### From this repository's marketplace

```text
codex plugin marketplace add Stunspot/agent-swarm-orchestration --ref main --sparse .agents --sparse plugins/agent-swarm-orchestration
codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
```

This route uses the current `main` branch. To install from the fixed 0.3.2 download, use the next route.

### From the downloaded kit

1. [Download and verify the complete kit](#download-and-check-the-complete-kit).
2. Open your terminal in the extracted folder containing `START-HERE.md`.
3. Register its `codex` directory as the marketplace and install the plugin.

   ```text
   codex plugin marketplace add ./codex
   codex plugin add agent-swarm-orchestration@cd-agent-swarm-orchestration
   ```

If you already registered `cd-agent-swarm-orchestration`, check [which source Codex is using](TROUBLESHOOTING.md#marketplace-command-succeeds-but-the-skill-is-not-recognized) before switching sources. After installation, [check discovery in a new task](#check-discovery-and-try-the-skill).

## Install the standalone skill in Codex

1. Get the complete `agent-swarm-orchestration` folder. In the GitHub checkout, it is `release/codex/agent-swarm-orchestration`. In the complete kit, it is `codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration`. The [standalone skill ZIP](https://github.com/Stunspot/agent-swarm-orchestration/releases/download/v0.3.2/Skill-agent-swarm-orchestration-v0.3.2.zip) also contains this folder.
2. Copy that folder into `.agents/skills/` in your project, or into `~/.agents/skills/` for your user account. On Windows, `~` here means your user profile. For the current project, the resulting path is `.agents/skills/agent-swarm-orchestration/SKILL.md`.
3. Keep the other files and folders alongside `SKILL.md`, then [check discovery in a new task](#check-discovery-and-try-the-skill).

## Install the skill in Claude or another host

Use the [Claude skill ZIP](https://github.com/Stunspot/agent-swarm-orchestration/releases/download/v0.3.2/Claude-agent-swarm-orchestration-v0.3.2.zip) or the same ZIP at `claude/agent-swarm-orchestration-v0.3.2.zip` inside the complete kit. Upload it through your host's custom skill installer, if available. For a folder-based installer, use the single `agent-swarm-orchestration` folder containing `SKILL.md`. The GitHub checkout also provides it at `release/claude/agent-swarm-orchestration`.

Enable the skill if your host has an enable control, then [check discovery in a new task](#check-discovery-and-try-the-skill). Host settings and availability vary. The archive layout was checked for 0.3.2. Live Claude activation was not tested for this release.

## Check discovery and try the skill

1. Open a new task and find Agent Swarm Orchestration in your host's skill list or picker. In the Codex CLI or IDE, type `$` or use `/skills` to find and select it.
2. Give it a real task with a clear result. The [read-only example in Start here](START-HERE.md#try-a-read-only-comparison) lets you test it without changing files.
3. Look for a decision about whether to delegate and one checked result. Working directly is a valid outcome. If your host cannot find the skill or start workers, see [Troubleshooting](TROUBLESHOOTING.md).

## Download and check the complete kit

1. Download the [0.3.2 kit with updated guides](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.2/documentation-20261111/Agent-Swarm-Orchestration-v0.3.2.zip) and its [SHA-256 checksum](https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/main/release-assets/v0.3.2/documentation-20261111/Agent-Swarm-Orchestration-v0.3.2.zip.sha256).
2. Compare the ZIP's SHA-256 with the checksum file before extracting. On Windows, run `Get-FileHash -Algorithm SHA256 ./Agent-Swarm-Orchestration-v0.3.2.zip` from the download directory. On macOS or Linux, use `shasum -a 256 Agent-Swarm-Orchestration-v0.3.2.zip`. Use the checksum from the same download source as the ZIP. If the hashes differ, download the matching pair again before using the package.
3. Extract the ZIP. Open the resulting `agent-swarm-orchestration-v0.3.2` folder, which contains `START-HERE.md`, `codex`, and `claude`.
4. If Python 3 is available, run `python tools/verify_package.py` from that folder. This checks the extracted files against the kit's manifest and compares the Codex and Claude skill copies.

## Validate a saved plan

From the installed skill folder, run `python scripts/validate_swarm_plan.py path/to/swarm-plan.json`. Replace the example path with your plan file. `VALID cd-agent-swarm-plan/v1` means the plan passed its structural checks. [Plan validation](PLAN-VALIDATION.md) explains how to interpret the reported control state and mission outcome.

## Remove or roll back

For a Codex plugin install, run `codex plugin remove agent-swarm-orchestration@cd-agent-swarm-orchestration`. For a standalone installation, remove the installed skill folder, or use your host's custom skill removal control. Open a fresh task and check that the skill is absent. If it still appears, check whether you also installed it by another route.

To roll back, restore your backed-up standalone folder or reinstall from a verified older package source. Start a fresh task and repeat the discovery and first-use checks. Any worker runs, file edits, or external actions made while the skill was installed need their own follow-up.
