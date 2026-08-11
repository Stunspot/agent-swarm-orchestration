#!/usr/bin/env python3
"""Render deterministic public presentation assets for Agent Swarm Orchestration."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DOCS_ASSETS = ROOT / "docs" / "assets"
PLUGIN_ASSETS = ROOT / "plugins" / "agent-swarm-orchestration" / "assets"
ARTWORK_SOURCE = ROOT / "tools" / "artwork-source"
FONT_ROOT = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_ROOT / name
    if not path.is_file():
        raise FileNotFoundError(f"required font not found: {path}")
    return ImageFont.truetype(str(path), size=size)


def add_left_readability(base: Image.Image, *, end_x: int, strength: int = 230) -> Image.Image:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pixels = overlay.load()
    for x in range(end_x):
        progress = x / max(1, end_x - 1)
        alpha = int(strength * (1 - progress**2))
        for y in range(base.height):
            pixels[x, y] = (3, 8, 24, alpha)
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def draw_hex(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, fill: tuple[int, int, int, int], outline: tuple[int, int, int, int]) -> None:
    import math

    cx, cy = center
    points = [
        (cx + radius * math.cos(math.radians(60 * index - 30)), cy + radius * math.sin(math.radians(60 * index - 30)))
        for index in range(6)
    ]
    draw.polygon(points, fill=fill, outline=outline, width=3)


def render_social_card() -> None:
    target = DOCS_ASSETS / "aso-social-card.png"
    base = Image.open(ARTWORK_SOURCE / "aso-social-card-base.png").convert("RGBA")
    if base.size != (1200, 630):
        raise ValueError(f"unexpected social-card source size: {base.size}")

    image = add_left_readability(base, end_x=760, strength=244)
    draw = ImageDraw.Draw(image)
    cyan = (111, 231, 247, 255)
    white = (246, 248, 255, 255)
    muted = (190, 204, 227, 255)
    gold = (250, 184, 76, 255)

    draw.rounded_rectangle((72, 64, 420, 106), radius=21, fill=(9, 25, 53, 235), outline=(71, 151, 185, 180), width=2)
    draw.text((94, 73), "COLLABORATIVE DYNAMICS  /  AUGMENT", font=font("seguisb.ttf", 18), fill=cyan)
    draw.text((72, 152), "Agent Swarm", font=font("segoeuib.ttf", 68), fill=white, stroke_width=1, stroke_fill=(4, 10, 28, 255))
    draw.text((72, 232), "Orchestration", font=font("segoeuib.ttf", 68), fill=white, stroke_width=1, stroke_fill=(4, 10, 28, 255))
    draw.rectangle((74, 326, 202, 332), fill=gold)
    draw.text((72, 362), "Parallel cognition. One accountable root.", font=font("segoeui.ttf", 29), fill=muted)
    draw.text((72, 514), "Authority  •  ownership  •  evidence  •  recovery", font=font("seguisb.ttf", 20), fill=(164, 184, 218, 255))
    image.convert("RGBA").save(target, format="PNG", optimize=True)


def render_plugin_screenshot() -> None:
    target = PLUGIN_ASSETS / "aso-social-card.png"
    width, height = 1400, 875
    image = Image.new("RGBA", (width, height), (3, 8, 24, 255))

    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((720, 70, 1420, 820), fill=(34, 169, 233, 95))
    glow_draw.ellipse((930, 250, 1510, 940), fill=(156, 83, 232, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    image = Image.alpha_composite(image, glow)
    draw = ImageDraw.Draw(image)

    for x in range(0, width, 70):
        draw.line((x, 0, x, height), fill=(63, 111, 151, 20), width=1)
    for y in range(0, height, 70):
        draw.line((0, y, width, y), fill=(63, 111, 151, 20), width=1)

    cyan = (111, 231, 247, 255)
    white = (246, 248, 255, 255)
    muted = (184, 200, 227, 255)
    gold = (250, 184, 76, 255)

    draw.text((82, 74), "COLLABORATIVE DYNAMICS", font=font("seguisb.ttf", 22), fill=cyan)
    draw.text((82, 140), "Agent Swarm", font=font("segoeuib.ttf", 74), fill=white)
    draw.text((82, 226), "Orchestration", font=font("segoeuib.ttf", 74), fill=white)
    draw.text((82, 337), "Coordinate many minds without losing", font=font("segoeui.ttf", 31), fill=muted)
    draw.text((82, 378), "mission, authority, ownership, or evidence.", font=font("segoeui.ttf", 31), fill=muted)

    features = [
        ("ADMIT", "the lightest capable topology"),
        ("PACKET", "bounded work with one writer"),
        ("RECONCILE", "reports against observed evidence"),
        ("RECOVER", "from the first unearned edge"),
    ]
    for index, (label, body) in enumerate(features):
        y = 505 + index * 70
        draw.rounded_rectangle((82, y, 218, y + 42), radius=12, fill=(11, 34, 64, 255), outline=(63, 153, 188, 180), width=2)
        draw.text((101, y + 8), label, font=font("seguisb.ttf", 17), fill=cyan)
        draw.text((246, y + 7), body, font=font("segoeui.ttf", 23), fill=white)

    draw = ImageDraw.Draw(image)
    draw_hex(draw, (1055, 434), 305, (2, 12, 34, 255), (111, 231, 247, 130))

    icon = Image.open(PLUGIN_ASSETS / "aso-icon.png").convert("RGBA")
    icon = icon.resize((530, 530), Image.Resampling.LANCZOS)
    icon.putalpha(icon.getchannel("A").point(lambda value: int(value * 0.92)))
    image.alpha_composite(icon, (790, 170))

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((852, 730, 1260, 796), radius=22, fill=(6, 19, 44, 235), outline=(250, 184, 76, 180), width=2)
    draw.text((895, 747), "ONE ROOT. EARNED PARALLELISM.", font=font("seguisb.ttf", 21), fill=gold)

    image.save(target, format="PNG", optimize=True)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments not in ([], ["--check"]):
        print("usage: render_presentation_assets.py [--check]", file=sys.stderr)
        return 2
    targets = [
        DOCS_ASSETS / "aso-social-card.png",
        PLUGIN_ASSETS / "aso-social-card.png",
    ]
    before = {path: file_sha256(path) for path in targets}
    render_social_card()
    render_plugin_screenshot()
    print("Rendered docs/assets/aso-social-card.png (1200x630)")
    print("Rendered plugins/agent-swarm-orchestration/assets/aso-social-card.png (1400x875)")
    if arguments == ["--check"]:
        after = {path: file_sha256(path) for path in targets}
        if before != after:
            for path in targets:
                print(f"NONDETERMINISTIC {path.relative_to(ROOT).as_posix()} {before[path]} -> {after[path]}")
            return 1
        print("DETERMINISTIC presentation assets unchanged after regeneration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
