# vNext Organizational Intelligence Architecture

**Status:** Authorized implementation basis
**Date:** 2026-08-31
**Repository baseline:** `01504f8e47af467883aa8dbfe4831cd6ad49faa9`
**Release boundary:** Source construction and local qualification only. No push, tag, publication, or same-version archive rewrite is authorized.

## Decision

Agent Swarm Orchestration will treat orchestration as the design and adaptation of a temporary organization, not merely the division of a task among workers.

The existing Direct, Enlist, Assemble, Chain, and Recover vocabulary remains the execution-control kernel. It answers how the next bounded slice runs. It does not define the richer organization: why members differ, which contributions should interact, what each may see, how disagreements resolve, what state persists, or what evidence should change the organization itself.

Above that kernel, Nova receives an open-ended organization workbench. It helps her sketch, operate, and reform the organization that can produce the cognition the task actually lacks. Named forms are provocations, never a closed router. A form may be borrowed, hybridized, inverted, renamed, or invented.

The governing principle is:

> Design the temporary organization whose structure can produce the missing cognition: distinct or purposefully redundant contributions, useful relations, deliberate exposure, an explicit resolver, and evidence-triggered reorganization. Complexity earns its keep through causal contribution, not resemblance to a preset.

## The problem being repaired

The current skill is already strong at admission, dependency order, authority, single-writer state, evidence custody, recovery, and closure. It is weak at organization-level reasoning. Its topology table currently mixes execution regimes, epistemic arrangements, review patterns, and recovery states. It can decide that several workers may run, but it has little language for deciding whether they should behave like a relay, search ecology, mission-command unit, advisory staff, deliberative council, studio, market, court, scientific community, or a problem-specific hybrid.

A flat list of new labels would repeat the defect at higher resolution. A rigid eight-field schema would make the defect tidier. Neither gives Nova organizational imagination.

## Stable vocabulary

- **Execution regime:** Direct, Enlist, Assemble, Chain, or Recover for one bounded reasoning horizon.
- **Organization instance:** the live, temporary arrangement of contributions, relations, visibility, authority, state, tempo, and resolution.
- **Pattern recipe:** a defeasible worked provocation. It suggests mechanisms and failure modes; it is not a classification requirement.
- **Contribution:** a bounded causal job whose evidence, transformation, capability, independent error opportunity, containment, or check may change the result.
- **Role name:** an optional mnemonic or cognitive stance. It may widen search or make a function memorable; it never establishes competence, independence, evidence, or authority.
- **Differentiator:** the reason a contribution may add a useful signal, including distinct evidence, tools, transformation, model behavior, context, authority, error opportunity, or intentional redundancy.
- **Relation:** a purposeful connection among contributions. Relation names remain extensible.
- **Exposure schedule:** what one contribution may see from another, when, and for which transformation.
- **Resolver:** the operation and decision owner that turn multiple returns into one result.
- **Oracle or verifier:** the observation that can discriminate or check a result at the task-native boundary.
- **Round:** one bounded interaction cycle with an entry condition, purpose, cap, and exit condition.
- **Reform signal:** an observed condition that recruits, releases, splits, merges, reroutes, re-exposes, changes the resolver, or stops the organization.
- **State plane:** task truth, progress control, evidence lineage, private scratch, or canonical artifact state.

Runtime text labels guidance as **Invariant**, **Default**, **Option**, **Experiment**, or **Example**. This prevents research priors and convenient recipes from masquerading as timeless law.

## Architecture

### 1. Mission and authority plane

The root retains the user-authorized outcome, acceptance, corrections, authority envelope, shared truth, merge responsibility, and final claim. The user retains value choices, risk acceptance, new authority, and reserved external actions. Delegation may narrow authority; it never widens it.

This plane is invariant across every organization. A boardroom does not vote new permission into existence. A platoon subordinate does not invent command authority. An anthill does not turn a shared board into canonical truth.

### 2. Organization workbench

For consequential or non-obvious delegation, Nova sketches answers to seven coupled questions:

1. What missing kinds of contribution could materially change the result?
2. Why might each contribution produce a different useful signal, or why is redundancy intentionally valuable?
3. Which contributions should remain independent, and which should interact?
4. What may cross each relation, to whom, when, and for what requested transformation?
5. By what operation do returns become one result, and who owns that decision?
6. What state is shared, private, append-only, or canonically writable?
7. What observation should recruit, release, rewire, change phase, or stop the organization?

The questions are coupled lenses, not orthogonal boxes and not mandatory paperwork. Light work keeps them implicit. A consequential organization uses the optional Organization Sketch and Contribution Cards.

### 3. Execution-control kernel

The organization compiles one phase at a time into the stable execution regimes:

- **Direct:** no worker; root acts.
- **Enlist:** one bounded worker augments root work.
- **Assemble:** two or more independent ready slices operate concurrently.
- **Chain:** accepted output from one stage becomes another stage's exact input.
- **Recover:** useful state is retained while a failed premise, route, owner, tool, sequence, or verifier changes.

A complex organization may move through several valid regimes. Anthill discovery may Assemble, a staff synthesis may Enlist or Chain, a boardroom may Assemble blind memos then Chain a bounded cross-response and resolution, and controlled execution may use Assemble or Chain. The event history stays acyclic even when the cognitive relation graph contains bounded feedback.

### 4. Contribution and relation plane

Every admitted member needs a causal reason to exist. A useful contribution card names its objective, differentiator or intentional redundancy, evidence/capability access, transformation, consumer, authority, failure caught, completion, and release condition.

Synergy lives mainly in relations rather than labels. Example relation intents include `requires`, `supplies`, `informs`, `challenges`, `cross-examines`, `checks`, `translates`, `elaborates`, `transforms`, `integrates`, `selects`, `escalates`, `broadcasts_need`, and `marks_evidence`. Nova may invent a more precise verb. Every live relation names its purpose, permitted exposure, timing or trigger, consumer, and stop condition.

Keep four edge planes distinct:

- execution dependency: what accepted result must precede what;
- visibility and exposure: who may see which fields and when;
- cognitive influence: who may challenge, transform, integrate, or test whose return;
- authority: who may decide, write, act, or escalate.

A communication graph is not a decision rule. A dependency graph is not an org chart. A role list is not synergy. A vote is not verification. The workbench keeps those distinctions visible.

### 5. State and memory plane

Consequential work distinguishes:

| Plane | Contents | Custody |
|---|---|---|
| Task truth | user goal, accepted facts, live unknowns, assumptions, current plan | root-governed; superseded states remain traceable |
| Progress control | dispatched, working, stalled, rounds, retries, next event | orchestration state; never promoted to factual truth |
| Evidence lineage | claims, observations, tool outputs, sources, provenance, decisions | append-only or auditable; summaries point to evidence |
| Private scratch | local exploration, draft hypotheses, unshared context | non-canonical; exposed selectively through a packet |
| Canonical artifacts | files, records, external objects, final deliverables | one writer per mutable surface at a time |

A phase transition declares which state is retained, superseded, invalidated, discarded, or re-derived. Private scratch does not become task truth merely because the organization changes form.

### 6. Resolution and verification plane

Before interaction begins, name how returns may become one result. Possible operations include union and deduplication, task-native objective test, evidence-weighted selection, critic-guided revision, integrative synthesis, bounded adjudication, root decision, or human decision. The resolver remains separate from the communication topology.

Preserve minority evidence when it is stronger, unresolved, value-bearing, or capable of exposing a common-mode error. Agent agreement supports neither independence nor truth after shared anchoring. Value conflict returns to the human decision owner; factual conflict receives primary evidence or a discriminating observation.

### 7. Morphogenesis loop

Organization is revised at meaningful events, not continuously churned and not frozen by its initial metaphor:

1. **Sense:** recover the current reasoning horizon, unknowns, stakes, constraints, and live host contract.
2. **Shape:** sketch the direct baseline and one or more causally different organizations when comparison is useful.
3. **Compose:** assign contributions, relations, exposure, state, resolver, oracle, budgets, and authority.
4. **Compile:** express the next phase as a valid execution regime, plan, packets, and ownership map.
5. **Operate:** dispatch only the ready frontier while the root continues useful work.
6. **Observe:** measure evidence gained, errors caught or introduced, disagreement, latency, cost, stalls, contamination, and acceptance progress.
7. **Reform:** recruit, release, split, merge, reroute, change exposure, change resolver, or Recover from the first unearned edge.
8. **Dissolve:** disposition every live responsibility, reconcile state, verify the earned boundary, and return one result.

Add a member when a named uncertainty needs a new evidence channel, transformation, capability, containment boundary, or check. Add a round only when a discriminating disagreement, failed check, or unresolved criterion justifies it. Release a member when its contribution is accepted, redundant, dominated, blocked, off the critical path, or no longer authorized. Stop when the resolver plus verification supports acceptance, or when a hard cap forces bounded closure.

## Pattern field: examples, not species

The skill ships a non-exhaustive pattern field. Each example states the mechanics worth stealing and the theatrical implications to leave behind.

| Inspiration | Mechanics worth stealing | Common misuse to reject |
|---|---|---|
| Bucketline | typed adjacent handoffs, accepted inputs, bottleneck visibility, provenance, repair of one failed stage | fake parallelism, restarting the whole line, treating every problem as uniform throughput |
| Anthill | broadcast a need, data-local self-selection, stigmergic evidence marks, decentralized search, central reconciliation | global transcript exposure, peer overwrite, permanent helpers, majority as truth |
| Platoon | clear intent, bounded unit ownership, local discretion inside authority, situation reports, independent state verification | rank theater, command prose as evidence, subordinate-created authority |
| Boardroom | chartered viewpoints, independent preparation, explicit conflict, selective challenge, named chair or decision right, preserved dissent | fixed cast, performative debate, consensus laundering, simulated stakeholder legitimacy |
| General staff | functionally distinct advisory products, shared planning frame, one decision owner, advice without line authority | staff consensus issuing commands, specialist jargon replacing synthesis |
| Complex adaptive system | heterogeneous agents, local rules, environmental feedback, recruitment and pruning, phase transitions, bounded experimentation | unbounded emergence, confidence-driven rewiring, agent inflation, loss of lineage |

Other useful inspirations may come from a court, newsroom, studio, scientific community, market, expedition, emergency room, orchestra, incident command system, neighborhood assembly, or a metaphor invented for the task. The organization must explain what causal mechanics it borrows and which implications it rejects.

ThunkTank contributes a valuable role-synergy lesson: invention, integration, domain grounding, pragmatic challenge, foresight, and explicit synthesis can make one another better through repeated cross-response. It does not establish that five roles are ideal, that all-to-all dialogue is desirable, that named personas are qualified, that debate should continue without a discriminating purpose, or that the debate itself is the deliverable.

For civic or stakeholder-sensitive problems, agents may model positions only from attributable evidence and must label the representation. They do not impersonate residents, communities, officials, customers, or affected people. Actual participation and reserved value choices remain human governance inputs.

## Tool composition

The runtime toolchain has two layers.

**Organization-design tools** are optional and generative:

- `assets/organization-sketch.template.md` holds the direct baseline, work physics, borrowed mechanics, contribution portfolio, relation and exposure sketch, state planes, resolver, verifier, reform signals, and phase compile.
- `assets/contribution-card.template.md` makes each member's causal reason and release condition explicit.
- `assets/cross-response-packet.template.md` bounds one interaction round without exposing an entire transcript.
- `assets/organization-transition.template.md` records why form or phase changed and how state was dispositioned.

**Execution-control tools** remain strict:

- `assets/swarm-plan.template.json` and its validator hold current-horizon regime, workers, dependencies, authority, budgets, merge, and status.
- delegation packets carry worker-local responsibility.
- agent returns preserve evidence and touched state.
- the merge ledger reconciles claims, artifacts, and acceptance.

The organization sketch is not machine proof of synergy. The swarm-plan validator is not an organizational oracle. The sketch informs judgment; the plan protects structural invariants; runtime evidence decides whether the organization is useful.

## Progressive disclosure

`SKILL.md` carries the mission, invariants, the seven workbench questions, the execution-kernel distinction, the morphogenesis loop, and routes to deeper doctrine.

New references divide the detail:

- `organization-design.md`: work physics, contribution portfolio, organizational imagination, pattern field, and stakeholder representation.
- `interaction-resolution-and-adaptation.md`: relation planes, exposure, resolvers, rounds, state, reform signals, and transitions.
- `pattern-recipes.md`: worked provocations with use conditions, mechanisms, failure modes, adaptation knobs, and nearest simpler baseline.
- `qualification-and-evaluation.md`: research boundaries, strong baselines, ablations, telemetry, promotion rules, and security tests.

Existing control references remain authoritative for execution, packets, live host semantics, authority, evidence, recovery, and closure. They are lightly refactored so their defaults do not masquerade as universal organization laws.

## Compatibility and source custody

`cd-agent-swarm-plan/v1` remains byte-compatible. Organizational intelligence is layered above it through Markdown workbench artifacts rather than silently adding fields to a schema that rejects unknown properties. A future v2 plan may embed an organization object only after an explicit migration decision and compatibility tests.

Canonical construction occurs first in `canonical/skills/agent-swarm-orchestration/`. New source tests and vNext eval catalogs qualify that tree. Only after acceptance may a bounded allowlisted synchronization tool copy canonical bytes into the plugin and standalone mirrors. Release archives, historical verification, and 0.2.3 custody records remain untouched. Existing behavioral evidence does not transfer to the new runtime fingerprint.

## Acceptance

The source upgrade is acceptable only when:

- a trivial task still selects Direct despite a requested metaphor;
- the skill can invent a useful organization outside its examples;
- every retained member has a causal contribution or intentional-redundancy rationale;
- role labels can be removed without losing the functional organization;
- execution, exposure, cognitive influence, and authority edges remain distinct;
- the resolver is chosen independently of communication topology;
- minority evidence and value conflicts survive synthesis;
- evidence can recruit or release a contribution and change phase without state loss;
- every phase compiles to a valid existing execution regime;
- authority, source, single-writer, evidence-level, bounded-round, and closure invariants do not regress;
- old v1 plans remain valid;
- canonical tests, Skill Creator validation, runtime parity checks, and independent forward review pass at the new fingerprint.

## Explicit non-goals

The upgrade does not prescribe a sacred headcount, standing cast, fixed metaphor, globally best topology, mandatory debate, all-to-all communication, consensus as truth, persona labels as competence, a built-in model hierarchy, autonomous authority expansion, concurrent canonical writes, or dynamic recruitment as a default.

It also does not claim that the example forms have demonstrated universal performance. They are thinking tools whose mechanisms must earn their use in context. Dynamic coalitions and long-horizon self-reorganization remain experimental until prospective live evidence supports promotion.
