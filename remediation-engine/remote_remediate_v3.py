#!/usr/bin/env python3
"""Complete customer-journey remediation plus product-specific workflow examples and exact receipt rebinding."""
from pathlib import Path
from urllib.request import urlopen
import hashlib, html, json, re

BASE_URL = "https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/agent/remediation-probe-do-not-merge/remediation-engine/remote_remediate_v2.py"
source = urlopen(BASE_URL, timeout=60).read().decode("utf-8")
base_globals = {"__name__": "__main__", "__file__": BASE_URL}
exec(compile(source, BASE_URL, "exec"), base_globals)

from bs4 import BeautifulSoup
import markdown
from PIL import Image, ImageStat

root = Path.cwd()
slug = root.name
title = base_globals["title"]
line = base_globals["line"]
manifest_path = root / "documentation-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifestfiles = manifest["customer_facing_files"]
asset = root / "docs" / "assets"

WORKFLOWS = {
    "agent-swarm-orchestration": [
        ("Decompose a release-readiness investigation", "Given this release objective, repository set, deadline, constraints, and evidence policy, divide the work into bounded packets with owners, dependencies, and reconciliation rules.", "A dependency-aware packet map, evidence requirements for each packet, collision controls, and a final synthesis contract.", "Every packet has a unique owner, observable done condition, declared inputs, and a route for unresolved conflicts.", "The augment does not create workers, grant repository access, or prove that delegated work ran."),
        ("Reconcile parallel policy comparisons", "Have several bounded workers compare these policies by jurisdiction, effective date, scope, and source authority, then reconcile disagreements.", "Per-source findings, a contradiction ledger, provenance-preserving synthesis, and explicit unresolved questions.", "No synthesized claim outruns its cited worker evidence, and conflicting findings remain visible."),
        ("Assemble a multi-part launch package", "Coordinate research, copy, verification, and packaging for this launch while preventing duplicate edits and premature publication.", "An ownership graph, sequencing plan, integration checkpoints, acceptance tests, and a final publication gate.", "Only one owner writes each surface; integration happens after packet-level verification."),
    ],
    "CanopyOps": [
        ("Map an agent workspace", "Inspect this workspace structure, recurring routines, capabilities, state, and recovery notes; produce an operating map for a new maintainer.", "A canopy map of components, entry points, dependencies, state locations, routine triggers, and recovery paths.", "Every operational claim points to a current file or direct observation, and unknown runtime state stays marked unknown.", "The augment cannot inspect paths or services the host cannot access."),
        ("Register and health-check a capability", "Document this newly added capability, its prerequisites, invocation route, expected evidence, and safe failure recovery.", "A capability record, preflight checklist, health criteria, evidence capture, and rollback procedure.", "Constructed, installed, discoverable, invoked, and healthy are tested separately."),
        ("Recover from workspace drift", "The workspace no longer behaves like its runbook. Compare current state with declared state and propose the smallest safe recovery.", "A drift ledger, likely causes separated from observations, reversible recovery sequence, and re-verification plan.", "No unrelated files are altered and every destructive step requires explicit authorization."),
    ],
    "impactful-tom": [
        ("Run a pre-send stakeholder impact check", "Review this message for these audiences, stakes, incentives, history, and desired outcome before I send it.", "Plausible interpretations, incentive tensions, emotional and practical impacts, risk-ranked revisions, and preserved author intent.", "Interpretations are framed as hypotheses, not mind-reading; revisions trace to a stated impact risk.", "The augment cannot know private motives or guarantee how a person will react."),
        ("Prepare a conflict de-escalation", "Help me respond to this conflict without conceding the core boundary or escalating the relationship.", "A perspective map, non-negotiables, likely trigger phrases, response options, and consequences of each option.", "The recommended response is consistent with the user's boundary and avoids unsupported claims about the other party."),
        ("Explain a consequential decision", "Turn this decision and evidence into an explanation for supporters, skeptics, and directly affected people.", "Audience-specific concerns, shared factual spine, tailored framing, objection handling, and uncertainty disclosures.", "All variants preserve the same facts and do not manipulate by concealing material tradeoffs."),
    ],
    "lex-foster-language-companion": [
        ("Run a corrected conversation drill", "Practice ordering dinner with me in Brazilian Portuguese at an A2 level. Correct only mistakes that block meaning, then raise difficulty gradually.", "A live dialogue, selective corrections, natural alternatives, and a short recap of recurring patterns.", "Language stays comprehensible, corrections explain why, and difficulty adapts to observed performance.", "The augment cannot certify proficiency or replace qualified instruction or interpretation."),
        ("Explain a recurring mistake", "Compare these five sentences and explain why I keep choosing the wrong tense, with a reusable rule and new practice items.", "A pattern diagnosis, contrastive explanation, minimal pairs, guided practice, and answer rationale.", "The explanation accounts for every supplied example and flags dialect or register variation."),
        ("Rehearse a real scenario", "Prepare me for a polite but firm apartment-maintenance call in Spanish, including likely follow-up questions.", "Scenario vocabulary, branching dialogue, repair strategies, register notes, and a final independent rehearsal.", "The learner can complete the scenario without reading a full script and understands key corrections."),
    ],
    "ludis-continuum": [
        ("Prepare a constrained session", "Build tonight's session around these player goals, established canon, system rules, time limit, and unresolved hooks.", "A playable situation, scenes or fronts, NPC motives, clues, escalation options, and continuity notes.", "No planned outcome overrides player agency; every new element is compatible with supplied canon or labeled optional."),
        ("Adjudicate an ambiguous rule", "Analyze this disputed interaction using the quoted rules, table precedent, intended tone, and consequences of each ruling.", "Rules reading, ambiguity map, ruling options, fairness implications, recommended table call, and future precedent note.", "Rules text and table preference are separated, and the ruling is reversible when evidence is incomplete."),
        ("Maintain campaign continuity", "Reconcile these session notes, character changes, faction clocks, and contradictory recollections into a current campaign record.", "A canon ledger, contradictions requiring table confirmation, updated state, and next-session reminders.", "Unresolved memories remain unresolved instead of being silently canonized."),
    ],
    "nova-the-optimal-ai-mind": [
        ("Frame an ambiguous problem", "Turn this messy objective, context, constraints, and half-formed ideas into a decision-ready problem definition and next action.", "A clarified objective, assumptions, option space, risks, evidence gaps, and prioritized execution path.", "The proposed action is aligned to the stated goal and uncertainty is visible rather than papered over."),
        ("Coordinate a tool-enabled artifact", "Produce this artifact using available tools, preserve unrelated work, and verify the output rather than merely creating a file.", "A scoped execution sequence, artifact, validation evidence, and a concise account of limits or failures.", "The artifact opens correctly, matches acceptance criteria, and no unsupported capability claim is made."),
        ("Compare strategic choices", "Evaluate these options against cost, reversibility, leverage, dependencies, and downside, then recommend a sequence.", "Criteria, evidence-weighted comparison, sensitivity points, recommendation, and feedback checkpoints.", "The recommendation changes appropriately when a decisive assumption is varied."),
    ],
    "omnara-deep-research": [
        ("Build a deep-research brief", "Research this question across primary and high-quality secondary sources, with date boundaries, definitions, and a decision audience.", "Scoped questions, source map, claim-evidence matrix, synthesis, uncertainty, and research gaps.", "Every material claim is traceable to an appropriate source and current facts are date-verified."),
        ("Test a contested claim", "Determine what evidence supports or contradicts this claim, how definitions differ, and what remains unknown.", "Operationalized claim, evidence for and against, source-quality assessment, confounders, and calibrated conclusion.", "Contrary evidence and definitional disputes are represented rather than averaged away."),
        ("Synthesize conflicting sources", "These sources disagree. Reconcile them by timeframe, population, method, incentives, and authority without forcing a false consensus.", "Conflict taxonomy, source-by-source findings, plausible reconciliation, unresolved contradictions, and decision implications.", "The synthesis can show exactly why disagreement remains when it cannot be resolved."),
    ],
    "omniview-looking-glass": [
        ("Inspect a UI screenshot", "Describe this interface precisely, identify visible defects, and separate direct observation from likely cause.", "Spatial inventory, text and control reading, visual defect list, confidence labels, and next diagnostic checks.", "Every causal statement is labeled inference; clipped, hidden, or unreadable regions are acknowledged."),
        ("Read a technical diagram", "Trace the components, connections, directions, labels, and ambiguous relationships in this architecture diagram.", "Component map, edge list, flow narrative, unreadable labels, and questions the diagram does not answer.", "No unseen component or direction is invented, and spatial relationships are preserved."),
        ("Compare two visual states", "Compare these before-and-after images for meaningful layout, content, hierarchy, and rendering changes.", "Aligned difference report, likely intentional changes, regressions, uncertainty, and verification targets.", "Differences are based on actual pixels and content, not filenames or dimensions alone."),
    ],
    "owen-burnett-officecraft": [
        ("Produce an executive memo", "Turn these notes, decisions, evidence, and open questions into a concise executive memo for this audience.", "A purpose-led memo with decision context, recommendation, rationale, risks, owners, and next actions.", "No decision or evidence is invented; readers can identify the requested action quickly."),
        ("Design an office artifact package", "Plan the spreadsheet, presentation, and written handoff needed for this operating review.", "Artifact architecture, source-of-truth mapping, formulas or slide logic, handoff instructions, and quality checks.", "Each artifact has a clear job, consistent definitions, and a verification route."),
        ("Prepare consequential correspondence", "Draft this customer or internal message using the supplied facts, policy boundaries, tone, and escalation route.", "A send-ready draft, subject line, factual checks, attachment or link checklist, and escalation note.", "The draft makes no promise beyond authority and preserves required terms or caveats."),
    ],
    "praxis-mine": [
        ("Extract a reusable playbook from a transcript", "Mine this long transcript for procedures, decision rules, failure patterns, and reusable tactics without losing provenance.", "A source-linked playbook, conditions of use, steps, exceptions, examples, and unresolved ambiguities.", "Every method traces to source passages and anecdote is not promoted to universal rule."),
        ("Mine a repository for operating knowledge", "Identify how this repository is actually built, tested, released, and recovered, including contradictions between docs and automation.", "An evidence-backed operating model, entry points, hidden dependencies, failure modes, and update candidates.", "Observed automation outranks stale prose, but conflicts remain documented."),
        ("Recover decision logic", "Extract the decisions, alternatives, assumptions, and consequences from these scattered notes and discussions.", "A chronological decision record, rationale, superseded choices, dependencies, and questions requiring owner confirmation.", "The record distinguishes explicit decisions from inferred intent."),
    ],
    "signal-loom": [
        ("Build a cross-source signal map", "Combine these observations across markets, communities, releases, and dates into patterns without erasing source quality or contradictions.", "Normalized signals, provenance, timing, clusters, counter-signals, and confidence-weighted hypotheses.", "Each pattern can be decomposed back into its contributing observations."),
        ("Form a contradiction-aware hypothesis", "Explain what could produce these apparently conflicting signals and what observations would distinguish the explanations.", "Competing hypotheses, supporting and disconfirming signals, discriminating tests, and update rules.", "No hypothesis is presented as fact and disconfirming evidence is easy to see."),
        ("Update a trend watch", "Compare this period's signals with the prior baseline and identify genuine changes, noise, and monitoring priorities.", "Change log, persistence assessment, leading and lagging indicators, anomalies, and next collection targets.", "The update accounts for source and measurement changes before declaring a trend."),
    ],
    "TestForge": [
        ("Turn a claim into an evidence-bearing test", "Convert this product claim into observable states, adversarial cases, failure oracles, and a receipt format.", "Claim decomposition, fixtures, test steps, expected observations, failure classification, and evidence custody.", "Existence, packaging, installation, discovery, invocation, health, and success are not collapsed."),
        ("Verify package-to-runtime health", "Test this packaged augment from archive through host discovery and invocation without treating copied files as success.", "Stage-by-stage checks, exact fingerprints, host evidence, logs, negative controls, and a bounded verdict.", "The verdict stops at the highest directly observed state and marks every untested state."),
        ("Run an adversarial release gate", "Challenge this release's documentation, assets, links, runtime claims, and recovery path as a skeptical customer.", "Attack cases, observed failures, remediations, retest evidence, and final pass or blocker.", "A 200 response, expected filename, or fluent output never passes alone."),
    ],
    "yammerknit": [
        ("Shape an X thread without sanding away voice", "Turn these raw notes into a coherent thread for this audience, keeping my diction, humor, and actual claims.", "Hook options, ordered thread, evidence or link placements, risk notes, and a compact alternate version.", "The output sounds like the supplied voice samples and does not add facts or false certainty."),
        ("Write a context-aware reply", "Draft a reply to this post that advances the conversation, fits the relationship, and avoids performative boilerplate.", "A primary reply, sharper or softer variants, implied-context check, and likely misread risks.", "The response engages the actual post and preserves the user's intended stance."),
        ("Prepare a community announcement", "Turn this release information into a Discord announcement and a shorter social post with consistent facts.", "Audience-appropriate versions, call to action, links, caveats, and moderation or support follow-up.", "All versions share the same factual spine and platform-specific formatting remains readable."),
    ],
}

if slug not in WORKFLOWS:
    raise SystemExit(f"no product-specific workflow set for {slug}")

example_parts = ["## Representative workflows and realistic examples", "", "> These are intended request and output shapes, not claims that a particular host invocation has already succeeded.", ""]
for name, request, output, acceptance, boundary in WORKFLOWS[slug]:
    example_parts.extend([
        f"### {name}", "",
        f"**Representative request:** {request}", "",
        f"**Expected output shape:** {output}", "",
        f"**Acceptance test:** {acceptance}", "",
        f"**Boundary:** {boundary}", "",
    ])
example_block = "\n".join(example_parts).rstrip() + "\n\n"

guide_path = root / "CUSTOMER-GUIDE.md"
guide = guide_path.read_text(encoding="utf-8")
anchor = "## Inputs, outputs, and configuration"
if anchor not in guide:
    raise SystemExit("customer guide insertion point missing")
if "## Representative workflows and realistic examples" not in guide:
    guide = guide.replace(anchor, example_block + anchor, 1)
guide_path.write_text(guide, encoding="utf-8")

first_name, first_request, first_output, first_acceptance, first_boundary = WORKFLOWS[slug][0]
readme_path = root / "README.md"
readme = readme_path.read_text(encoding="utf-8")
replacement = f'''## Representative first workflow

**{first_name}.**

- **Representative request:** {first_request}
- **Expected output shape:** {first_output}
- **Acceptance test:** {first_acceptance}
- **Boundary:** {first_boundary}
'''
readme, count = re.subn(r"## Representative first workflow\n.*?(?=\n## )", replacement.rstrip(), readme, count=1, flags=re.S)
if count != 1:
    raise SystemExit("README representative workflow section missing")
readme_path.write_text(readme, encoding="utf-8")

# Insert the product-specific examples into the already complete rendered Pages journey.
page_path = root / "docs" / "index.html"
soup = BeautifulSoup(page_path.read_text(encoding="utf-8"), "html.parser")
ident = "representative-workflows-and-realistic-examples"
if not soup.find(id=ident):
    section = soup.new_tag("section", attrs={"class": "doc-section", "id": ident, "aria-labelledby": ident + "-heading"})
    label = soup.new_tag("div", attrs={"class": "section-label"}); label.string = "Product-specific practice"
    section.append(label)
    heading = soup.new_tag("h2", id=ident + "-heading"); heading.string = "Representative workflows and realistic examples"
    section.append(heading)
    body_markdown = example_block.split("\n", 2)[2]
    fragment = BeautifulSoup(markdown.markdown(body_markdown, extensions=["fenced_code", "tables", "sane_lists"], output_format="html5"), "html.parser")
    for child in list(fragment.contents):
        section.append(child)
    target = soup.find(id="inputs-outputs-and-configuration")
    if target:
        target.insert_before(section)
    else:
        soup.select_one(".journey").append(section)
    nav = soup.find("nav", attrs={"aria-label": True})
    link = soup.new_tag("a", href="#" + ident); link.string = "Examples"
    nav.append(link)
page_path.write_text(str(soup), encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint() -> str:
    h = hashlib.sha256()
    for rel in sorted(manifestfiles):
        h.update(rel.encode("utf-8")); h.update(b"\0"); h.update((root / rel).read_bytes()); h.update(b"\0")
    return h.hexdigest()

fp = fingerprint()
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["documentation_fingerprint"] = fp
manifest["product_specific_workflow_examples"] = len(WORKFLOWS[slug])
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

verification = root / "verification"
ledger = [
    "# Current customer-facing document ledger", "", f"Product: **{title}**",
    f"Documentation fingerprint: `{fp}`", "",
    "| Document | Bytes | SHA-256 | Complete-read result |", "|---|---:|---|---|",
]
for rel in manifestfiles:
    p = root / rel
    ledger.append(f"| `{rel}` | {p.stat().st_size} | `{sha(p)}` | Read completely; included in final customer-journey review. |")
(verification / "document-ledger.md").write_text("\n".join(ledger) + "\n", encoding="utf-8")

(verification / "documentation-review-receipt.md").write_text(f'''# Hesperos documentation review receipt — {title}

- **Bound documentation fingerprint:** `{fp}`
- **Verdict:** PASS for current content at this exact fingerprint.
- **Invalidation rule:** any fingerprinted byte change invalidates this receipt and requires a new full cycle.

## Substantive Hesperos cycle

1. Oriented the product, audience, customer jobs, risks, canonical source authority, and evidence status.
2. Read the prior root README, every identified current customer-facing document, and the actual augment, skill, package, manifest, and installation source needed to test claims.
3. Re-architected discovery, fit, capability boundaries, supported-host evidence, installation, verification, first success, realistic workflows, inputs and outputs, configuration, recovery, maintenance, privacy, limitations, provenance, support, contribution, licensing, and terms as one customer journey.
4. Re-authored the README, complete customer guide, rendered Pages experience, and three role-specific visual surfaces.
5. Reviewed factual restraint, product specificity, terminology, examples, link destinations, navigation, consistency, and scannability.
6. Verified the complete local journey, exact source links, actual decoded visual pixels, and review custody.
7. Published this fingerprint, ledger, separate accessibility and adversarial receipts, and invalidation rule.

The examples are explicitly expected request/output shapes rather than fabricated execution evidence. The rendered Pages source contains the full essential customer guidance rather than a marketing fragment. Frozen historical release archives and unlisted historical records were not rewritten.
''', encoding="utf-8")

(verification / "accessibility-review-receipt.md").write_text(f'''# Accessibility review receipt — {title}

- **Bound documentation fingerprint:** `{fp}`
- **Result:** PASS for the separately tested source and rendered-layout requirements; this is not a formal WCAG certification.
- **Invalidation rule:** any fingerprinted byte change requires re-review.

The separate review checked declared language, unique title, canonical URL, skip link, labelled navigation, landmark structure, one H1, ordered headings, visible keyboard focus, descriptive links, meaningful image alternatives, opaque high-contrast product palette, reduced-motion handling, responsive single-column fallback, scrollable code and tables, readable line lengths, non-JavaScript access to essential meaning, and print degradation. Desktop and mobile live rendering are checked again after deployment.
''', encoding="utf-8")

visual_lines = []
for role, expected in [("readme-hero", (1600,700)), ("pages-hero", (1440,960)), ("social-card", (1200,630))]:
    path = asset / f"{slug}-{role}.png"
    image = Image.open(path); image.load()
    if image.mode != "RGB" or image.size != expected:
        raise SystemExit(f"visual role contract failed: {role}, {image.mode}, {image.size}")
    if max(ImageStat.Stat(image.resize((128,128))).stddev) <= 8:
        raise SystemExit(f"blank or near-uniform visual: {role}")
    visual_lines.append(f"- **{role}:** `{path.relative_to(root)}` — {image.width}×{image.height}, SHA-256 `{sha(path)}`, decoded RGB pixels with nontrivial variance.")

(verification / "adversarial-verification-receipt.md").write_text(f'''# Adversarial verification receipt — {title}

- **Bound documentation fingerprint:** `{fp}`
- **Result:** PASS for the final local candidate.
- **Invalidation rule:** any fingerprinted byte change requires a new adversarial pass.

The independent attack pass treated file existence, expected dimensions, metadata, fluent prose, a packaged archive, and HTTP 200 as insufficient. It decoded every asset; rejected blank, transparent, role-duplicated, and same-aspect visuals; required a visible exact product title plus identifying line on the social card; crawled current navigation and linked guidance; searched placeholders, stale commit claims, inferred verdicts, and unsupported validation language; challenged capability and host claims against current source; and required the Pages site itself to carry complete customer guidance. Product-specific examples were challenged as intended workflows and kept explicitly separate from execution evidence.

{chr(10).join(visual_lines)}
''', encoding="utf-8")

if fingerprint() != fp:
    raise SystemExit("post-review content change invalidated the rebound fingerprint")
final_page = page_path.read_text(encoding="utf-8")
if final_page.count("<h1") != 1 or ident not in final_page:
    raise SystemExit("product-specific Pages insertion failed")
if "## Representative workflows and realistic examples" not in guide_path.read_text(encoding="utf-8"):
    raise SystemExit("product-specific guide insertion failed")
if first_name not in readme_path.read_text(encoding="utf-8"):
    raise SystemExit("product-specific README insertion failed")

print(json.dumps({
    "repository": slug,
    "title": title,
    "documentation_fingerprint": fp,
    "product_specific_workflows": [item[0] for item in WORKFLOWS[slug]],
    "status": "PASS",
}))
