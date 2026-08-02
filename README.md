# Agent Swarm Orchestration 0.1.0

Agent Swarm Orchestration is a Codex skill from Collaborative Dynamics. It coordinates multiple agents only when divided cognition is expected to improve the accepted result after startup, duplicated reading, communication, merge, verification, latency, and token cost.

Its central promise is **parallel cognition without custody loss**: one root agent keeps the mission, authority envelope, evidence chain, shared-state integrity, merge, and final answer.

## What it does

The skill helps Codex:

- choose direct work, one delegate, independent parallel workers, a dependency chain, or recovery;
- map prerequisites, ready work, ownership, budgets, and stop conditions;
- give each worker a bounded packet with an exact deliverable and evidence burden;
- use the collaboration controls exposed by the current Codex task;
- continue safe, authorized work while reserving only an ungranted authority edge;
- distinguish missing authority from a missing source, tool, or capability;
- distinguish worker reports from observed or independently verified evidence;
- return an exact prepared delta when an authorized action cannot run, without claiming unobserved inspection;
- prevent simultaneous writers from owning the same mutable surface;
- sequence correctness-bearing changes before clarity, formatting, or polish on a shared artifact;
- reconcile conflicts and verify the integrated result;
- account for every worker before closing.

It does not create collaboration tools, run after the Codex task ends, or expand the user's authority.

## The five operating shapes

| Shape | Use it when |
|---|---|
| Direct | The root can complete small, sequential, same-surface, or shared-context-heavy work more safely and cheaply. |
| Enlist | One bounded worker can return a useful result while the root keeps the main task moving. |
| Assemble | Two or more independent, ready slices can run concurrently with separate write ownership. |
| Chain | One accepted result determines the next specialist's input. |
| Recover | Existing work is failed, stale, conflicting, interrupted, or based on a bad premise. |

## What is in the product

The product keeps three surfaces distinct:

- `canonical/skills/agent-swarm-orchestration/` is the maintained source skill.
- `release/codex/agent-swarm-orchestration/` is the generated Codex installation folder.
- `release-assets/agent-swarm-orchestration-v0.1.0.zip` is the transport archive containing one top-level `agent-swarm-orchestration/` folder.

The canonical and released skill folders each contain 17 files and were observed byte-identical during this documentation pass. The ZIP was observed to contain the same 17 relative files. This is package evidence, not proof that a customer host has installed, discovered, or invoked the skill.

The runtime skill includes:

- one `SKILL.md` entry point;
- seven progressive references;
- a Swarm Plan template and schema;
- Delegation Packet, Agent Return, and Merge Ledger templates;
- a Swarm Plan validator and ten unit tests;
- one worked competing-hypotheses example.

The product root also contains capability evals and retained construction evidence. Evals are build and regression material; they are not part of the 17-file runtime skill.

## Documentation map

| Your question | Read |
|---|---|
| Will this help, and how do I try it? | [Start here](START-HERE.md) |
| How do I install or remove it? | [Installation](INSTALLATION.md) |
| How do I use the common patterns? | [Workflows](WORKFLOWS.md) |
| Why is it not behaving as expected? | [Troubleshooting](TROUBLESHOOTING.md) |
| What may I trust, and what remains untested? | [Trust and limits](TRUST-AND-LIMITS.md) |
| What does the Codex target support? | [Host matrix](host-matrix.md) |
| What should I send for support? | [Support](SUPPORT.md) |

## Evidence boundary

The current package fingerprint is `8833af967b1faf2f1b1b92a5eda54129579a995c91965b73883bc1f8272768b5`. Static package validation, the included plan validator, ten validator tests, a valid template, byte parity across both 17-file runtime trees, and ZIP topology support that build. The release ZIP SHA-256 is `1889b0b1f20a4cc98c9ccf3c95d7a1b64cea0e4524cf3e16b00b90ccd2cf6683`.

The eval catalog contains 20 cases: ten explicitly coached regression cases and ten natural qualification cases. Ten fresh, no-history `gpt-5.6-sol` subjects each completed one isolated natural decision-only case. Independent TestForge semantic review passed all ten. This supports the package's orchestration decisions at the exercised boundary; those episodes did not execute target files, browsing, network actions, or live Codex collaboration tools.

The exact-fingerprint `qwen35:latest` prompted regression demonstrated 9 of 10 cases. ASO-009 failed because it claimed that no files changed without an authoritative post-state readback. The retained qwen natural qualification is also negative smaller-model transfer evidence. Neither qwen run establishes qwen transfer.

The current preliminary TestForge disposition is `PASS_WITH_CONDITIONS / READY_WITH_RESIDUAL_RISK` for private Codex source custody, conditioned on refreshing evidence and documentation custody. It is not a final live-host or customer-readiness verdict. See [Trust and limits](TRUST-AND-LIMITS.md) for the evidence classes, residuals, and exclusions.

The evidence does not establish installed-host discovery, clean-task invocation, live collaboration-tool behavior, accessibility conformance, public publication, universal reliability, universal savings, or customer success.
