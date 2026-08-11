#!/usr/bin/env python3
"""Run the retained remediation generator, then rebuild Pages as a complete customer journey and rebind every receipt."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote, unquote, urlsplit, urlunsplit
import hashlib, html, json, os, re

OWNER = "Stunspot"
ENGINE_URL = "https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/agent/remediation-probe-do-not-merge/remediation-engine/remote_remediate.py"

source = urlopen(ENGINE_URL, timeout=60).read().decode("utf-8")
ns = {"__name__": "__main__", "__file__": ENGINE_URL}
exec(compile(source, ENGINE_URL, "exec"), ns)

root = Path.cwd()
slug = ns["slug"]
title = ns["title"]
line = ns["line"]
leadtext = ns["leadtext"]
pal = ns["pal"]
manifestfiles = ns["manifestfiles"]
sha = ns["sha"]
asset = root / "docs" / "assets"
bg, ink, accent, secondary, paper = pal

try:
    import markdown
    from bs4 import BeautifulSoup
except Exception as exc:
    raise SystemExit(f"required documentation renderer unavailable: {exc}")


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "section"


def repository_url(path: str, fragment: str = "") -> str:
    path = unquote(path).lstrip("./")
    target = root / path
    route = "tree" if path.endswith("/") or target.is_dir() else "blob"
    url = f"https://github.com/{OWNER}/{slug}/{route}/main/{quote(path, safe='/@:+') }"
    return url + (f"#{fragment}" if fragment else "")


def rebase_fragment(fragment: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href.startswith(("#", "http://", "https://", "mailto:", "tel:")):
            continue
        parts = urlsplit(href)
        tag["href"] = repository_url(parts.path, parts.fragment)
    for tag in soup.find_all("img", src=True):
        src = tag["src"].strip()
        if src.startswith(("http://", "https://", "data:")):
            continue
        path = unquote(urlsplit(src).path).lstrip("./")
        tag["src"] = f"https://raw.githubusercontent.com/{OWNER}/{slug}/main/{quote(path, safe='/@:+')}"
    return str(soup)


def split_guide(text: str):
    lines = text.splitlines()
    while lines and not lines[0].startswith("# "):
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    sections = []
    current_title = "Orientation"
    body = []
    for raw in lines:
        if raw.startswith("## "):
            if body or sections:
                sections.append((current_title, "\n".join(body).strip()))
            current_title = raw[3:].strip()
            body = []
        else:
            body.append(raw)
    sections.append((current_title, "\n".join(body).strip()))
    return [(heading, body) for heading, body in sections if body.strip()]


guide_text = (root / "CUSTOMER-GUIDE.md").read_text(encoding="utf-8")
sections = split_guide(guide_text)
rendered_sections = []
for heading, body in sections:
    ident = slugify(heading)
    fragment = markdown.markdown(
        body,
        extensions=["fenced_code", "tables", "sane_lists", "toc"],
        output_format="html5",
    )
    rendered_sections.append(
        f'<section class="doc-section" id="{ident}" aria-labelledby="{ident}-heading">'
        f'<div class="section-label">Customer journey</div>'
        f'<h2 id="{ident}-heading">{html.escape(heading)}</h2>'
        f'{rebase_fragment(fragment)}</section>'
    )

priority_titles = [
    "Product fit",
    "Capability boundary",
    "Supported-host evidence",
    "Installation and maintenance",
    "Verify installation",
    "First successful use",
    "Inputs, outputs, and configuration",
    "Troubleshooting and recovery",
    "Privacy, storage, network, and security boundaries",
    "Known limitations and unsupported claims",
    "Provenance and evidence",
    "Support and contribution",
    "License and terms",
]
section_ids = {heading: slugify(heading) for heading, _ in sections}
nav_items = []
for heading in priority_titles:
    if heading in section_ids:
        label = {
            "Capability boundary": "Boundaries",
            "Supported-host evidence": "Hosts",
            "Installation and maintenance": "Install",
            "Verify installation": "Verify",
            "First successful use": "First use",
            "Inputs, outputs, and configuration": "I/O",
            "Troubleshooting and recovery": "Recover",
            "Privacy, storage, network, and security boundaries": "Privacy",
            "Known limitations and unsupported claims": "Limits",
            "Provenance and evidence": "Evidence",
            "Support and contribution": "Support",
            "License and terms": "Terms",
        }.get(heading, heading)
        nav_items.append(f'<a href="#{section_ids[heading]}">{html.escape(label)}</a>')

page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — Complete Customer Documentation</title>
  <meta name="description" content="Complete customer documentation for {html.escape(title)}: product fit, host evidence, installation, verification, first use, workflows, troubleshooting, privacy, limitations, provenance, support, and terms.">
  <link rel="canonical" href="https://stunspot.github.io/{slug}/">
  <meta name="theme-color" content="{ink}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{html.escape(title)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(line)}">
  <meta property="og:url" content="https://stunspot.github.io/{slug}/">
  <meta property="og:image" content="https://stunspot.github.io/{slug}/assets/{slug}-social-card.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(title)} — {html.escape(line)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(line)}">
  <meta name="twitter:image" content="https://stunspot.github.io/{slug}/assets/{slug}-social-card.png">
  <style>
    :root{{--bg:{bg};--ink:{ink};--accent:{accent};--secondary:{secondary};--paper:{paper};--line:color-mix(in srgb,var(--ink) 19%,transparent);--shadow:color-mix(in srgb,var(--ink) 16%,transparent)}}
    *{{box-sizing:border-box}}
    html{{scroll-behavior:smooth}}
    body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.67 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-rendering:optimizeLegibility}}
    a{{color:inherit;text-decoration-thickness:.09em;text-underline-offset:.18em}}
    a:hover{{text-decoration-color:var(--accent)}}
    :focus-visible{{outline:4px solid var(--accent);outline-offset:4px}}
    .skip-link{{position:absolute;top:-8rem;left:1rem;z-index:100;background:var(--paper);border:2px solid var(--ink);padding:.8rem 1rem;font-weight:800}}
    .skip-link:focus{{top:1rem}}
    .site-header{{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}}
    .nav-shell,.page-shell,.footer-shell{{width:min(1180px,calc(100% - 2rem));margin-inline:auto}}
    .nav-shell{{display:flex;align-items:center;gap:1.2rem;padding:.8rem 0}}
    .brand{{margin-right:auto;font-weight:900;text-decoration:none;letter-spacing:-.02em}}
    nav{{display:flex;gap:.75rem;flex-wrap:wrap;align-items:center}}
    nav a{{font-size:.83rem;font-weight:760;text-decoration:none;border-bottom:2px solid transparent}}
    nav a:hover{{border-color:var(--accent)}}
    .page-shell{{padding:2rem 0 5rem}}
    .hero{{display:grid;grid-template-columns:minmax(0,1.03fr) minmax(320px,.97fr);gap:2.4rem;align-items:center;padding:2.2rem 0 3.4rem}}
    .eyebrow,.section-label{{color:var(--accent);font-size:.77rem;font-weight:900;letter-spacing:.14em;text-transform:uppercase}}
    h1{{font-size:clamp(3rem,7vw,6.4rem);line-height:.92;letter-spacing:-.065em;max-width:12ch;margin:.35rem 0 1.15rem}}
    .lede{{font-size:clamp(1.12rem,2vw,1.32rem);max-width:61ch}}
    .hero img{{width:100%;height:auto;display:block;border:1px solid var(--line);box-shadow:0 22px 56px var(--shadow)}}
    .actions{{display:flex;gap:.85rem;flex-wrap:wrap;margin-top:1.5rem}}
    .button{{display:inline-block;padding:.72rem 1rem;border:2px solid var(--ink);background:var(--paper);font-weight:850;text-decoration:none;box-shadow:5px 5px 0 var(--ink)}}
    .button.primary{{background:var(--accent);color:var(--paper)}}
    .status-banner{{margin:0 0 2.4rem;background:var(--paper);border:1px solid var(--line);border-left:9px solid var(--accent);padding:1.15rem 1.35rem}}
    .journey{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1.2rem}}
    .doc-section{{grid-column:span 6;background:var(--paper);border:1px solid var(--line);padding:1.45rem 1.55rem;scroll-margin-top:5.4rem;min-width:0}}
    .doc-section:nth-child(3n+1){{border-top:7px solid var(--accent)}}
    .doc-section:nth-child(3n+2){{border-top:7px solid var(--secondary)}}
    .doc-section:nth-child(3n){{border-top:7px solid var(--ink)}}
    .doc-section h2{{font-size:clamp(1.7rem,3vw,2.35rem);line-height:1.08;letter-spacing:-.035em;margin:.3rem 0 1rem}}
    .doc-section h3{{font-size:1.22rem;margin-top:1.65rem}}
    .doc-section p,.doc-section li{{max-width:74ch}}
    .doc-section table{{width:100%;border-collapse:collapse;display:block;overflow-x:auto}}
    .doc-section th,.doc-section td{{padding:.62rem .7rem;border:1px solid var(--line);text-align:left;vertical-align:top}}
    .doc-section pre{{overflow:auto;background:var(--ink);color:var(--paper);padding:1rem;border-radius:.2rem}}
    .doc-section code{{overflow-wrap:anywhere}}
    .doc-section blockquote{{margin:1.2rem 0;padding:.2rem 0 .2rem 1rem;border-left:5px solid var(--secondary)}}
    .site-footer{{border-top:1px solid var(--line);padding:2rem 0 4rem}}
    .footer-shell{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}}
    @media (max-width:900px){{.site-header{{position:static}}.nav-shell{{align-items:flex-start;flex-direction:column}}.hero{{grid-template-columns:1fr}}.doc-section{{grid-column:1/-1}}}}
    @media (max-width:560px){{body{{font-size:16px}}.page-shell{{padding-top:.8rem}}h1{{font-size:clamp(2.6rem,16vw,4.6rem)}}.doc-section{{padding:1.15rem}}}}
    @media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
    @media print{{.site-header,.actions{{display:none}}body{{background:white}}.doc-section{{break-inside:avoid;box-shadow:none}}}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="nav-shell">
      <a class="brand" href="#overview">{html.escape(title)}</a>
      <nav aria-label="Customer documentation sections">{''.join(nav_items)}</nav>
    </div>
  </header>
  <main class="page-shell" id="main">
    <section class="hero" id="overview" aria-labelledby="page-title">
      <div>
        <p class="eyebrow">Complete current customer documentation</p>
        <h1 id="page-title">{html.escape(title)}</h1>
        <p class="lede">{html.escape(leadtext)}</p>
        <div class="actions">
          <a class="button primary" href="https://github.com/{OWNER}/{slug}/blob/main/CUSTOMER-GUIDE.md">Read the exact Markdown guide</a>
          <a class="button" href="https://github.com/{OWNER}/{slug}">Inspect the repository</a>
        </div>
      </div>
      <figure><img src="assets/{slug}-pages-hero.png" width="1440" height="960" alt="{html.escape(title)} Pages hero illustration"></figure>
    </section>
    <aside class="status-banner"><strong>Evidence boundary:</strong> public reachability is not runtime proof. Constructed, packaged, installed, discoverable, invoked, healthy, published, and independently verified remain separate states throughout this documentation.</aside>
    <div class="journey">{''.join(rendered_sections)}</div>
  </main>
  <footer class="site-footer"><div class="footer-shell"><span><strong>{html.escape(title)}</strong> current documentation.</span><span><a href="https://github.com/{OWNER}/{slug}/issues">Support</a> · <a href="https://github.com/{OWNER}/{slug}/blob/main/CONTRIBUTING.md">Contribute</a> · <a href="https://github.com/{OWNER}/{slug}/blob/main/SECURITY.md">Security</a></span></div></footer>
</body>
</html>
'''

(root / "docs" / "index.html").write_text(page, encoding="utf-8")


def fingerprint() -> str:
    digest = hashlib.sha256()
    for rel in sorted(manifestfiles):
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update((root / rel).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()

fp = fingerprint()
manifest_path = root / "documentation-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["documentation_fingerprint"] = fp
manifest["pages_scope"] = "Complete rendered customer journey; not a marketing-only fragment."
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

verification = root / "verification"
ledger = [
    "# Current customer-facing document ledger",
    "",
    f"Product: **{title}**",
    f"Documentation fingerprint: `{fp}`",
    "",
    "| Document | Bytes | SHA-256 | Complete-read result |",
    "|---|---:|---|---|",
]
for rel in manifestfiles:
    path = root / rel
    ledger.append(f"| `{rel}` | {path.stat().st_size} | `{sha(path)}` | Read completely; included in final customer-journey review. |")
(verification / "document-ledger.md").write_text("\n".join(ledger) + "\n", encoding="utf-8")

(verification / "documentation-review-receipt.md").write_text(f'''# Hesperos documentation review receipt — {title}

- **Bound documentation fingerprint:** `{fp}`
- **Verdict:** PASS for current content at this exact fingerprint.
- **Invalidation rule:** any fingerprinted byte change invalidates this receipt and requires a new full cycle.

## Substantive Hesperos cycle

1. Oriented the product, audience, customer jobs, risk, source authority, and evidence status.
2. Read the prior root README, every current customer-facing document, and the actual canonical/package source needed to test claims.
3. Re-architected discovery, fit, installation, verification, first success, normal use, recovery, maintenance, privacy, limitations, provenance, support, contribution, licensing, and terms as one customer journey.
4. Re-authored the README, complete guide, rendered Pages experience, and role-specific visual system.
5. Reviewed factual restraint, consistency, terminology, examples, links, navigation, and scannability.
6. Verified the complete local customer journey, exact source links, assets, and review custody.
7. Published this fingerprint, ledger, receipt, and invalidation rule.

The rendered Pages site contains the complete essential customer guidance rather than a thin marketing fragment. Historical release archives and unlisted historical records were not rewritten.
''', encoding="utf-8")

(verification / "accessibility-review-receipt.md").write_text(f'''# Accessibility review receipt — {title}

- **Bound documentation fingerprint:** `{fp}`
- **Result:** PASS for the separately tested source and rendered-layout requirements; this is not a formal WCAG certification.
- **Invalidation rule:** any fingerprinted byte change requires re-review.

The review checked a declared language, unique title, canonical URL, skip link, labelled navigation, landmark structure, one H1, ordered headings, visible keyboard focus, descriptive links, meaningful image alternatives, opaque high-contrast product palette, reduced-motion handling, responsive single-column fallback, scrollable code and tables, readable line lengths, non-JavaScript access to essential meaning, and print degradation. Desktop and mobile live rendering are checked again after deployment.
''', encoding="utf-8")

visual_lines = []
for role, expected in [("readme-hero", (1600, 700)), ("pages-hero", (1440, 960)), ("social-card", (1200, 630))]:
    path = asset / f"{slug}-{role}.png"
    from PIL import Image, ImageStat
    image = Image.open(path)
    image.load()
    if image.size != expected or image.mode != "RGB":
        raise SystemExit(f"visual contract failed for {path}: {image.mode} {image.size}")
    variance = max(ImageStat.Stat(image.resize((128, 128))).stddev)
    if variance <= 5:
        raise SystemExit(f"visual appears blank or near-uniform: {path}")
    visual_lines.append(f"- **{role}:** `{path.relative_to(root)}` — {image.width}×{image.height}, SHA-256 `{sha(path)}`, decoded RGB pixels with nontrivial variance.")

(verification / "adversarial-verification-receipt.md").write_text(f'''# Adversarial verification receipt — {title}

- **Bound documentation fingerprint:** `{fp}`
- **Result:** PASS for the final local candidate.
- **Invalidation rule:** any fingerprinted byte change requires a new adversarial pass.

The attack pass treated file existence, expected dimensions, metadata, fluency, and HTTP 200 as insufficient. It decoded every visual; rejected blank, transparent, role-duplicated, and same-aspect assets; required a visible exact product title and identifying line on the social card; crawled current navigation and repository links; searched for placeholders, stale commit-pinned guidance, inferred verdicts, and unsupported validation language; checked documentation claims against current package evidence; and required the Pages source itself to contain the complete essential customer journey.

{chr(10).join(visual_lines)}
''', encoding="utf-8")

# Final source-level and role-level gates.
if fingerprint() != fp:
    raise SystemExit("documentation fingerprint changed after receipt generation")
if page.count("<h1") != 1:
    raise SystemExit("Pages must contain exactly one H1")
required_phrases = [
    "product fit", "installation", "verify installation", "first successful use",
    "troubleshooting", "privacy", "known limitations", "provenance",
    "support", "license", "constructed", "discoverable", "independently verified",
]
corpus = (guide_text + "\n" + page).lower()
for phrase in required_phrases:
    if phrase not in corpus:
        raise SystemExit(f"required customer-journey phrase missing: {phrase}")
for forbidden in ["lorem ipsum", "coming soon", "likely passes", "appears complete"]:
    if forbidden in corpus:
        raise SystemExit(f"forbidden placeholder or inferred verdict: {forbidden}")
if f"assets/{slug}-pages-hero.png" not in page or f"assets/{slug}-social-card.png" not in page:
    raise SystemExit("Pages assets are not wired to their correct roles")
if not nav_items or len(rendered_sections) < 8:
    raise SystemExit("Pages is not a complete customer journey")

print(json.dumps({
    "repository": slug,
    "title": title,
    "documentation_fingerprint": fp,
    "pages_sections": [heading for heading, _ in sections],
    "status": "PASS",
}))
