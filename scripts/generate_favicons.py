#!/usr/bin/env python3
"""Regenerate favicon.ico, favicon-{16,32}x16.png, and apple-touch-icon.png
from logo.svg (#164).

Pillow can't rasterize arbitrary SVG, but logo.svg is deliberately just a
background rect + one centered circle - this parses that specific shape
with the stdlib's xml.etree and draws it with Pillow, rather than pulling
in a full SVG-rendering dependency (cairosvg/resvg) for one tiny icon.

If logo.svg ever grows more complex than a rect + circle, this raises
clearly instead of silently drawing the wrong thing - switch to an actual
SVG renderer at that point.

Run with: python3 scripts/generate_favicons.py
"""
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
LOGO_SVG = ROOT / "logo.svg"
SVG_NS = "{http://www.w3.org/2000/svg}"


def _parse_simple_logo(svg_path):
    root = ET.parse(svg_path).getroot()
    view_box = [float(v) for v in root.get("viewBox").split()]
    if view_box[:2] != [0.0, 0.0] or view_box[2] != view_box[3]:
        raise ValueError("logo.svg: expected a square viewBox starting at 0,0")

    children = list(root)
    rect = root.find(f"{SVG_NS}rect")
    circle = root.find(f"{SVG_NS}circle")
    if rect is None or circle is None or len(children) != 2:
        raise ValueError(
            "logo.svg is no longer just a background rect + one circle - "
            "update this script (or switch to a real SVG renderer) before regenerating icons."
        )

    return {
        "size": view_box[2],
        "bg": rect.get("fill"),
        "cx": float(circle.get("cx")),
        "cy": float(circle.get("cy")),
        "r": float(circle.get("r")),
        "fg": circle.get("fill"),
    }


def render(spec, px):
    scale = px / spec["size"]
    img = Image.new("RGB", (px, px), spec["bg"])
    draw = ImageDraw.Draw(img)
    cx, cy, r = spec["cx"] * scale, spec["cy"] * scale, spec["r"] * scale
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=spec["fg"])
    return img


def main():
    spec = _parse_simple_logo(LOGO_SVG)

    render(spec, 16).save(ROOT / "favicon-16x16.png")
    favicon_32 = render(spec, 32)
    favicon_32.save(ROOT / "favicon-32x32.png")
    render(spec, 180).save(ROOT / "apple-touch-icon.png")
    favicon_32.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32)])

    print("Regenerated favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png, "
          "and favicon.ico from logo.svg")


if __name__ == "__main__":
    main()
