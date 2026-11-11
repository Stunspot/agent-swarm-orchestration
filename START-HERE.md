# Start here with Agent Swarm Orchestration

Use Agent Swarm Orchestration when an AI task may benefit from independent checks, parallel work on different parts, or a handoff between specialists. The lead agent (the **root**) decides how to organize the work and stays responsible for the final answer. For a short task or a single shared edit, it may do the work directly.

## Install the skill

[Choose your installation method](INSTALLATION.md). In Codex, you can install the plugin from this repository's marketplace or install the skill folder directly. In Claude or another Agent Skills host, use the one-skill ZIP if the host supports skill uploads. Every route delivers the same skill.

## Try a read-only comparison

1. Open a new task where your assistant can read several relevant files or folders. For this example, use a project with billing, search, and notifications, or substitute three areas you have.
2. In the Codex CLI or IDE, use this prompt. In other interfaces, select or name the installed skill using the host's skill controls and use the rest of the prompt.

   ```text
   Use $agent-swarm-orchestration to compare how billing, search, and notifications handle retries. Keep the work read-only. Decide which parts, if any, to delegate. Check conflicting findings against the source and return one comparison with the biggest risk.
   ```

3. Look for one comparison with source references, a brief reason for using workers or working directly, and any differences the evidence could not settle.

The skill uses the collaboration controls available in the current task. If the host has no worker controls, the assistant can do the comparison directly or prepare a delegation plan for later. A prepared plan has the status `PREPARED — NOT DISPATCHED`.

## If you get stuck

If the host cannot find the skill, check [installation and discovery](INSTALLATION.md#check-discovery-and-try-the-skill). If the skill loads but no workers start, see [why the skill may work directly](TROUBLESHOOTING.md#the-skill-loads-but-does-not-create-agents). For conflicting findings or uncertain edits, see [Troubleshooting](TROUBLESHOOTING.md).

Once the first task works, use [Workflows](WORKFLOWS.md) for parallel work, sequential handoffs, independent review, and recovery. [Plan validation](PLAN-VALIDATION.md) explains how to check a saved plan or resume stopped work.
