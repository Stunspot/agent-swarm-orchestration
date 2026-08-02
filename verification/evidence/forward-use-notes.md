# Fresh-context forward-use notes

**Package:** Agent Swarm Orchestration 0.1.0  
**Mode:** three independently dispatched fresh-context Codex agents; read-only requests; package supplied without expected answers

## Small metadata consistency task

The agent completed the comparison directly and reported that the YAML description and OpenAI default prompt described the same capability. It did not manufacture a swarm for the trivial task.

**Evidence level:** agent-reported behavior inspected in the returned message; no filesystem mutation requested or reported.

## Package closure and eval-contamination task

The agent inspected the runtime package and found one material path defect: the original validation command resolved from the task working directory rather than the skill root. The root repaired `SKILL.md` to resolve the validator and template from the loaded skill root. A follow-up fresh turn executed the resolved packaged command from another working directory and returned exit 0 with `VALID cd-agent-swarm-plan/v1`.

The agent also reported that runtime resources were present and that `ASO-*`, `expected_behaviors`, `failure_signals`, and suite-specific content remained confined to `canonical/evals/`.

**Evidence level:** initial defect was agent-reported and reproduced by the worker; repaired path was locally inspected and revalidated; eval-contamination result remains agent-reported pending root search.

## Conflicting validator claims

The agent inspected the validator and resolved the disagreement in favor of the narrower claim: the validator catches basic dependency-graph defects and declared simultaneous write-surface collisions among active workers. It does not prove that sequential handoff began from reconciled bytes. The root added that boundary to the runtime skill.

**Evidence level:** agent-reported source interpretation; root inspection of the validator and unit tests supports the same bounded claim.

## Forward-use disposition

The exercises support possibility of direct restraint, useful defect discovery, changed-route repair, evidence-conflict resolution, and claim calibration under the named runtime. They do not establish consistent behavior across the full eval suite or a fresh installed Codex host.
