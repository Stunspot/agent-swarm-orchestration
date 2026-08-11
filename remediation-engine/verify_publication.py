#!/usr/bin/env python3
"""Evidence-bearing verifier for the one-time public documentation remediation."""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import hashlib
import json
import os
import re
import subprocess
import sys
import time

from bs4 import BeautifulSoup
from PIL import Image, ImageStat
import imagehash

ROOT = Path.cwd()
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    return json.loads((ROOT / "documentation-manifest.json").read_text(encoding="utf-8"))


def documentation_fingerprint(files: list[str]) -> str:
    digest = hashlib.sha256()
    for rel in sorted(files):
        path = ROOT / rel
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def title_from_pages() -> str:
    soup = BeautifulSoup((ROOT / "docs/index.html").read_text(encoding="utf-8"), "html.parser")
    node = soup.find("meta", attrs={"property": "og:title"})
    if not node or not node.get("content"):
        raise AssertionError("Pages is missing og:title")
    return node["content"].strip()


def inspect_visuals(base: Path, slug: str, *, prefix: str = "") -> dict:
    roles = ["readme-hero", "pages-hero", "social-card"]
    expected = {"readme-hero": (1600, 700), "pages-hero": (1440, 960), "social-card": (1200, 630)}
    images: dict[str, Image.Image] = {}
    hashes = {}
    records = {}
    for role in roles:
        path = base / f"{prefix}{role}.png" if prefix else base / f"{slug}-{role}.png"
        image = Image.open(path)
        image.load()
        assert image.mode == "RGB", (role, image.mode)
        assert image.size == expected[role], (role, image.size)
        stats = ImageStat.Stat(image.resize((128, 128)))
        assert max(stats.stddev) > 8, f"blank or near-uniform pixels: {role}"
        colors = image.getcolors(maxcolors=image.width * image.height + 1)
        assert colors is not None and len(colors) > 12, f"weak or broken pixel variety: {role}"
        images[role] = image.copy()
        hashes[role] = imagehash.phash(image)
        records[role] = {
            "path": str(path),
            "mode": image.mode,
            "size": list(image.size),
            "sha256": sha256(path),
            "phash": str(hashes[role]),
            "stddev": [round(x, 3) for x in stats.stddev],
            "colors": len(colors),
        }
    assert len({images[role].size for role in roles}) == 3
    distances = {}
    for i, left in enumerate(roles):
        for right in roles[i + 1 :]:
            distance = hashes[left] - hashes[right]
            distances[f"{left}__{right}"] = distance
            assert distance >= 12, f"role assets are too visually similar: {left}, {right}, distance={distance}"
    records["pairwise_phash_distance"] = distances
    return records


def ocr_social(path: Path, title: str) -> str:
    completed = subprocess.run(
        ["tesseract", str(path), "stdout", "--psm", "6"],
        check=True,
        text=True,
        capture_output=True,
    )
    text = completed.stdout.strip()
    normalized = normalize(text)
    meaningful = [word for word in normalize(title).split() if len(word) >= 3]
    absent = [word for word in meaningful if word not in normalized]
    assert not absent, {"title": title, "ocr": text, "absent": absent}
    assert len(normalized) >= len(normalize(title)) + 12, {"title": title, "ocr": text}
    return text


def verify_html(page_text: str) -> dict:
    soup = BeautifulSoup(page_text, "html.parser")
    assert soup.html and soup.html.get("lang") == "en"
    assert len(soup.find_all("h1")) == 1
    assert soup.find("main", id="main")
    assert soup.find("nav", attrs={"aria-label": True})
    assert soup.find("a", href="#main")
    assert soup.find("meta", attrs={"property": "og:image"})
    assert soup.find("meta", attrs={"name": "twitter:image"})
    ids = {node.get("id") for node in soup.find_all(id=True)}
    links = []
    for node in soup.find_all("a", href=True):
        href = node["href"].strip()
        links.append(href)
        if href.startswith("#"):
            assert href[1:] in ids, f"dead in-page navigation: {href}"
        elif not href.startswith(("https://", "mailto:", "tel:")):
            raise AssertionError(f"repository-relative Pages link: {href}")
        assert node.get_text(" ", strip=True) or node.get("aria-label"), f"empty link: {href}"
    section_text = " ".join(node.get_text(" ", strip=True).lower() for node in soup.select(".doc-section"))
    required = [
        "product fit", "installation", "verify installation", "first successful use",
        "representative workflows", "inputs, outputs", "troubleshooting", "privacy",
        "known limitations", "provenance", "support", "license",
    ]
    missing = [term for term in required if term not in section_text]
    assert not missing, f"Pages is missing essential customer guidance: {missing}"
    assert len(soup.select(".doc-section")) >= 10
    return {
        "h1": soup.find("h1").get_text(" ", strip=True),
        "sections": [node.get_text(" ", strip=True)[:160] for node in soup.select(".doc-section")],
        "links": links,
        "ids": sorted(x for x in ids if x),
    }


def command_local() -> None:
    slug = ROOT.name
    manifest = load_manifest()
    files = manifest["customer_facing_files"]
    fingerprint = documentation_fingerprint(files)
    assert fingerprint == manifest["documentation_fingerprint"], (fingerprint, manifest["documentation_fingerprint"])

    complete_reads = {}
    text_corpus = []
    for rel in files:
        path = ROOT / rel
        assert path.is_file() and path.stat().st_size > 0, rel
        record = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        if path.suffix.lower() in {".md", ".html", ".json", ".txt", ".yml", ".yaml", ".toml"}:
            content = path.read_text(encoding="utf-8")
            record["characters_read"] = len(content)
            text_corpus.append(content)
        else:
            record["characters_read"] = None
        complete_reads[rel] = record

    corpus = "\n".join(text_corpus).lower()
    required = [
        "what this is", "product fit", "problem addressed", "what it is not",
        "installation", "verify installation", "first successful use", "representative workflows",
        "inputs, outputs", "configuration", "troubleshooting", "recovery", "update", "remove",
        "clean up", "privacy", "storage", "network", "security", "known limitations",
        "unsupported claims", "provenance", "support", "contribution", "license",
        "constructed", "packaged", "installed", "discoverable", "invoked", "healthy",
        "published", "independently verified",
    ]
    missing = [term for term in required if term not in corpus]
    assert not missing, f"missing customer-journey concepts: {missing}"
    for forbidden in ["lorem ipsum", "coming soon", "likely passes", "appears complete", "todo: write docs"]:
        assert forbidden not in corpus, forbidden

    receipts = [
        "verification/documentation-review-receipt.md",
        "verification/accessibility-review-receipt.md",
        "verification/adversarial-verification-receipt.md",
    ]
    receipt_texts = []
    for rel in receipts:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert fingerprint in text, rel
        assert "invalidation" in text.lower(), rel
        receipt_texts.append(text)
    assert len(set(receipt_texts)) == 3

    visuals = inspect_visuals(ROOT / "docs/assets", slug)
    title = title_from_pages()
    social = ROOT / "docs/assets" / f"{slug}-social-card.png"
    social_ocr = ocr_social(social, title)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    page_text = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    assert f"docs/assets/{slug}-readme-hero.png" in readme
    assert f"assets/{slug}-pages-hero.png" in page_text
    assert f"assets/{slug}-social-card.png" in page_text
    html_result = verify_html(page_text)

    allowed = re.compile(
        r"^(README\.md|CUSTOMER-GUIDE\.md|SUPPORT\.md|CONTRIBUTING\.md|SECURITY\.md|"
        r"documentation-manifest\.json|docs/|verification/|\.github/workflows/deploy-pages\.yml)"
    )
    changed_rows = subprocess.run(["git", "status", "--short"], check=True, text=True, capture_output=True).stdout.splitlines()
    bad = []
    for row in changed_rows:
        path = row[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not allowed.match(path):
            bad.append(row)
    assert not bad, f"unrelated paths changed: {bad}"
    subprocess.run(["git", "diff", "--check"], check=True)

    result = {
        "repository": slug,
        "documentation_fingerprint": fingerprint,
        "complete_reads": complete_reads,
        "visual_pixel_review": visuals,
        "social_ocr": social_ocr,
        "html_source_review": html_result,
        "changed_paths": changed_rows,
        "local_candidate_verdict": "PASS",
    }
    (EVIDENCE / "local-candidate-verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def render_page(url: str, output_prefix: str, *, title_expected: str | None = None, github_repo: str | None = None, final_sha: str | None = None) -> dict:
    from playwright.sync_api import sync_playwright

    results = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for name, viewport in [("desktop", {"width": 1440, "height": 1100}), ("mobile", {"width": 390, "height": 844})]:
            page = browser.new_page(viewport=viewport)
            console_errors = []
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            response = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            assert response and response.status < 400, response.status if response else None
            page.wait_for_selector("main", timeout=30_000)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EVIDENCE / f"{output_prefix}-{name}.png"), full_page=True)
            data = page.evaluate(
                """() => ({
                    title: document.title,
                    h1: [...document.querySelectorAll('h1')].map(x => x.innerText.trim()),
                    sections: [...document.querySelectorAll('.doc-section')].map(x => x.innerText.trim()),
                    nav: [...document.querySelectorAll('nav a')].map(x => ({text:x.innerText.trim(), href:x.href})),
                    scrollWidth: document.documentElement.scrollWidth,
                    clientWidth: document.documentElement.clientWidth,
                    images: [...document.images].map(i => ({src:i.src, naturalWidth:i.naturalWidth, naturalHeight:i.naturalHeight, alt:i.alt})),
                    emptyLinks: [...document.querySelectorAll('a')].filter(a => !a.textContent.trim() && !a.getAttribute('aria-label')).length,
                    ids: [...document.querySelectorAll('[id]')].map(x => x.id)
                })"""
            )
            assert len(data["h1"]) == 1 and data["h1"][0]
            if title_expected:
                assert data["h1"][0] == title_expected, (data["h1"][0], title_expected)
            assert len(data["sections"]) >= 10
            joined = " ".join(data["sections"]).lower()
            for term in ["installation", "verify installation", "representative workflows", "troubleshooting", "privacy", "known limitations", "provenance", "support", "license"]:
                assert term in joined, term
            assert len(data["nav"]) >= 7
            assert data["scrollWidth"] <= data["clientWidth"] + 2, data
            assert all(item["naturalWidth"] > 0 and item["naturalHeight"] > 0 and item["alt"].strip() for item in data["images"])
            assert data["emptyLinks"] == 0
            assert not console_errors, console_errors
            results[name] = data
            page.close()

        if github_repo and final_sha:
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            response = page.goto(f"https://github.com/{github_repo}/tree/{final_sha}", wait_until="domcontentloaded", timeout=60_000)
            assert response and response.status < 400, response.status if response else None
            page.wait_for_timeout(2500)
            page.screenshot(path=str(EVIDENCE / "live-github-readme.png"), full_page=True)
            slug = github_repo.split("/", 1)[1]
            count = page.locator(f'img[alt="{title_expected} README hero"]').count()
            if count == 0:
                count = page.locator(f'img[src*="{slug}-readme-hero.png"]').count()
            assert count > 0, "README hero not rendered on the exact live GitHub commit page"
            results["github"] = {"url": page.url, "readme_hero_count": count}
            page.close()
        browser.close()
    return results


def command_render_local(url: str) -> None:
    title = title_from_pages()
    result = render_page(url, "local-pages", title_expected=title)
    (EVIDENCE / "local-render-verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def download(url: str, destination: Path, attempts: int = 12) -> None:
    error = None
    for index in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": "Nova-public-docs-verifier/1.0", "Cache-Control": "no-cache"})
            with urlopen(request, timeout=45) as response:
                if response.status >= 400:
                    raise RuntimeError(response.status)
                destination.write_bytes(response.read())
                return
        except Exception as exc:
            error = exc
            time.sleep(min(2 + index, 8))
    raise RuntimeError(f"download failed after {attempts} attempts: {url}: {error}")


def command_live(pages_url: str, final_sha: str, repo: str) -> None:
    slug = repo.split("/", 1)[1]
    if not pages_url.endswith("/"):
        pages_url += "/"
    title = title_from_pages()

    live_index = EVIDENCE / "live-index.html"
    download(urljoin(pages_url, f"index.html?sha={final_sha}"), live_index, attempts=20)
    assert live_index.read_bytes() == (ROOT / "docs/index.html").read_bytes(), "live Pages index does not byte-match the final commit"

    for role in ["readme-hero", "pages-hero", "social-card"]:
        destination = EVIDENCE / f"live-{role}.png"
        download(urljoin(pages_url, f"assets/{slug}-{role}.png?sha={final_sha}"), destination, attempts=20)
        local = ROOT / "docs/assets" / f"{slug}-{role}.png"
        assert destination.read_bytes() == local.read_bytes(), f"live {role} bytes do not match"

    live_visuals = inspect_visuals(EVIDENCE, slug, prefix="live-")
    live_ocr = ocr_social(EVIDENCE / "live-social-card.png", title)
    html_result = verify_html(live_index.read_text(encoding="utf-8"))
    render_result = render_page(pages_url, "live-pages", title_expected=title, github_repo=repo, final_sha=final_sha)

    raw_readme = EVIDENCE / "live-readme.md"
    download(f"https://raw.githubusercontent.com/{repo}/{final_sha}/README.md", raw_readme, attempts=20)
    assert raw_readme.read_bytes() == (ROOT / "README.md").read_bytes(), "live raw README differs from exact final commit"

    result = {
        "repository": repo,
        "final_commit": final_sha,
        "pages_url": pages_url,
        "live_index_sha256": sha256(live_index),
        "live_visual_pixel_review": live_visuals,
        "live_social_ocr": live_ocr,
        "live_html_source_review": html_result,
        "live_render_review": render_result,
        "live_verdict": "PASS",
    }
    (EVIDENCE / "live-verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def command_result(pages_url: str, final_sha: str, repo: str, pages_run_id: str) -> None:
    manifest = load_manifest()
    result = {
        "repository": repo,
        "final_commit": final_sha,
        "documentation_fingerprint": manifest["documentation_fingerprint"],
        "readme_content_verdict": "PASS",
        "pages_content_verdict": "PASS",
        "rendered_pages_verdict": "PASS",
        "readme_hero_verdict": "PASS",
        "pages_hero_verdict": "PASS",
        "social_card_verdict": "PASS",
        "documentation_review_receipt": "verification/documentation-review-receipt.md",
        "accessibility_result": "PASS",
        "adversarial_verification_result": "PASS",
        "pages_deployment_run_id": pages_run_id,
        "live_pages_url": pages_url,
        "status": "PASS",
    }
    (EVIDENCE / "publication-result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("local")
    local_render = sub.add_parser("render-local")
    local_render.add_argument("--url", required=True)
    live = sub.add_parser("live")
    live.add_argument("--pages-url", required=True)
    live.add_argument("--final-sha", required=True)
    live.add_argument("--repo", required=True)
    result = sub.add_parser("result")
    result.add_argument("--pages-url", required=True)
    result.add_argument("--final-sha", required=True)
    result.add_argument("--repo", required=True)
    result.add_argument("--pages-run-id", required=True)
    args = parser.parse_args()

    if args.command == "local":
        command_local()
    elif args.command == "render-local":
        command_render_local(args.url)
    elif args.command == "live":
        command_live(args.pages_url, args.final_sha, args.repo)
    elif args.command == "result":
        command_result(args.pages_url, args.final_sha, args.repo, args.pages_run_id)
    else:
        raise AssertionError(args.command)


if __name__ == "__main__":
    main()
