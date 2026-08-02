# Host matrix

Version 0.1.0 has one target: Codex. “Targeted,” “packaged,” “installed,” “discovered,” “invoked,” and “healthy” are different states.

| Surface | Codex 0.1.0 state | Evidence and customer action |
|---|---|---|
| Canonical source | Present | `canonical/skills/agent-swarm-orchestration/` contains the maintained 17-file skill. The current package fingerprint is `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`. |
| Installable folder | Generated and statically validated | `release/codex/agent-swarm-orchestration/` contains 17 files observed byte-identical to canonical source. Copy this folder through the installation method supported by your Codex host. |
| ZIP transport | Generated and topology-checked | `release-assets/agent-swarm-orchestration-v0.1.0.zip` contains one top-level `agent-swarm-orchestration/` folder and 17 files. Its SHA-256 is `1889b0b1f20a4cc98c9ccf3c95d7a1b64cea0e4524cf3e16b00b90ccd2cf6683`. Extraction is not installation. |
| Installation | Not performed in retained product evidence | Follow [Installation](INSTALLATION.md), then inspect the exact destination folder. |
| Skill discovery | Not tested on a clean host | Start a fresh task or reload when your Codex version requires it, then observe whether the host resolves the skill. |
| Explicit invocation | Not tested on an installed clean host | Request `$agent-swarm-orchestration` by name and observe whether the skill's topology logic is applied. |
| Implicit routing | Declared in package metadata; not tested | Do not assume discovery or routing from metadata alone. Use explicit invocation for the first check. |
| Collaboration tools | Supplied by the live Codex task, not by the package | Inspect current tool presence, schemas, slots, context forks, messaging, waiting, interruption, and lifecycle before dispatch. If a required tool is absent, return an exact prepared delta as `CAPABILITY-LIMITED`; do not relabel missing capability as missing authority. |
| Swarm Plan validation | Script and template locally tested | Python 3 can run `scripts/validate_swarm_plan.py`; a pass covers declared structure only. |
| Eval catalog | Present | 20 cases: ten explicitly coached regressions and ten natural qualifications. Evals are evidence definitions, not live-host execution. |
| Natural Codex decision qualification | 10 of 10 PASS under independent TestForge semantic review | Ten fresh, no-history, pinned `gpt-5.6-sol` subjects each completed one isolated natural case. They described orchestration decisions only; no target action or live collaboration primitive executed. |
| Prompted qwen regression | `NOT_DEMONSTRATED`; 9 of 10 | The exact-fingerprint `qwen35:latest` run failed ASO-009 for claiming that no files changed without authoritative post-state readback. This is negative regression evidence, not qwen transfer. |
| Natural qwen qualification | Negative smaller-model transfer evidence | The retained run did not pass all indispensable gates and belongs to an earlier package fingerprint. It does not qualify qwen transfer or the Codex host. |
| Private source-custody review | Preliminary `PASS_WITH_CONDITIONS / READY_WITH_RESIDUAL_RISK` | The remaining TestForge conditions are evidence and documentation custody refreshes. This does not establish installation, discovery, invocation, health, or customer readiness. |
| Background execution | Not provided | Work does not continue after the Codex task ends through this package. |
| Public availability | Not published | Local release artifacts do not establish public distribution. |
| Customer outcomes | Not tested | Measure success in the customer's task and environment before making an outcome claim. |

Other agent harnesses and persistent external swarm services are outside version 0.1.0.

## What to verify in your environment

1. The exact installed folder and its 17 files.
2. Codex discovery in a fresh task.
3. Explicit skill invocation.
4. The live collaboration-tool contract for that task.
5. Direct restraint on a trivial task and earned orchestration on independent work.
6. Single-writer behavior, evidence reconciliation, and clean worker closure.
7. Removal or rollback before depending on the package for consequential work.

Record the Codex version, environment, task, outputs, and untested paths with every claim.
