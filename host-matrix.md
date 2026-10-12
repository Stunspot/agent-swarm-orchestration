# Host and distribution matrix

Version 0.3.2 separates packaged, installed, discoverable, invoked, healthy, integrated and published states. Exact file membership is recorded in package-custody.json. Older behavioral evidence does not transfer to changed instructions.

The paths in this table are relative to the extracted customer-kit root, beside START-HERE.md.

| Surface | Supplied object | What to verify |
|---|---|---|
| Codex marketplace | codex/.agents/plugins/marketplace.json and codex/plugins/agent-swarm-orchestration | Register the local kit, install the named plugin, then observe fresh-task discovery. |
| Standalone Codex | codex/plugins/agent-swarm-orchestration/skills/agent-swarm-orchestration | Copy the complete skill folder to the host's actual skill directory; confirm it loads. |
| Claude or one-skill host | claude/agent-swarm-orchestration-v0.3.2.zip | Upload the one-skill archive through the current host procedure, then observe invocation. |
| Package evidence | package-custody.json and tools/verify_package.py | Check exact file hashes, portable paths and Claude/Codex parity; this does not establish activation. |
| Documentation site source | docs/ | Local HTML and retained visual assets; deployment and public navigation require separate observation. |
| Nova Free and Nova Emergent | Component source and candidate handed to the edition owner | The owner selects exact bytes, rebuilds and verifies each edition; this repository does not mutate editions. |

Follow [Installation](INSTALLATION.md) for commands and recovery. Repository builders and separate standalone/plugin archives are described in [Archive custody](ARCHIVE-CUSTODY.md).

## Presentation surfaces

The README and site heroes, social card, plugin icon, listing image and distribution avatar retain their previously reviewed artwork. The repair changes runtime, packaging and prose; no new artwork is claimed.

## Runtime dependencies and tool drift

The skill has no mandatory third-party runtime dependency. Python 3 is optional for package and plan validation. The package supplies no agent-spawning, messaging, waiting, interruption, file, browser or network tools; it uses the controls exposed by the current host.

Host tool names, schemas, limits, context forks and lifecycle semantics can change. Inspect the live contract before relying on a named primitive. Returned workers may still occupy host slots even though they no longer count as running execution in the plan.

## Evidence vocabulary

Created means an object exists. Packaged means selected bytes and metadata were assembled. Installed means placed or registered. Discoverable means the host resolves it. Invoked means the task applied it. Healthy means exercised behavior met stated acceptance. Integrated means an edition selected and rebuilt the component. Published means a public destination exposes it. Verified means a credible check supports the named predicate.

One state does not silently imply the next. The repair's local executable and expert review evidence is not a fresh-host trial, a model trial or a participant study.
