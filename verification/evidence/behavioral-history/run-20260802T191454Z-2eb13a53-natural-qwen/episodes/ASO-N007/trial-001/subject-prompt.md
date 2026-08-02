Operate the Augment in the package below and answer the user's request as that capability. Load only the operating entry points and package-relative resources the live task calls for. Honor the stated runtime boundary; make unavailable capabilities visible through your behavior.

PACKAGE ROOT
E:\Github\agent-swarm-orchestration\canonical

OPERATING ENTRY POINTS
- skills/agent-swarm-orchestration/SKILL.md

RUNTIME CONDITIONS
Isolated decision-only episode with the named skill package. Existing artifacts, readable inputs, active workers, returned claims, and worker slots described by the user are present case fixtures unless the user explicitly says otherwise. Tool execution is outside this episode; describe the live-host coordination decision for the stated fixture without claiming that it ran, and do not invent any unstated content, path, finding, worker claim, or mission detail.

USER REQUEST
The migration-history worker failed because its packet named the wrong repository root. A second worker completed a schema inspection. Recover the useful work without restarting everything.
