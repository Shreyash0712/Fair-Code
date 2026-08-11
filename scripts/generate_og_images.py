#!/usr/bin/env python3
"""Generate branded 1200x630 OpenGraph/Twitter social-preview images.

Renders with Pillow using the site's actual web fonts (bundled OFL .ttf
files under assets/fonts/, matching Instrument Serif / Archivo / IBM Plex
Mono used by index.html and the explainer pages), on the same paper/ink
palette. One shared image for the homepage/profiler, one per explainer
(title baked in) so each page gets a unique, on-brand share card instead of
a generic fallback.

Fonts are bundled (not system fonts) so this runs identically in CI
(ubuntu-latest) and locally. Run with: python3 scripts/generate_og_images.py
"""
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "og"
FONTS_DIR = ROOT / "assets" / "fonts"
DATA_JSON = ROOT / "assets" / "explainers-data.json"

W, H = 1200, 630
BG = (21, 19, 13)          # --bg (dark)
ACCENT = (207, 111, 73)    # --accent (dark theme)
WHITE = (241, 233, 212)    # --white (dark theme)
MUTED = (141, 131, 103)    # --muted (dark theme)
MARK_GREEN = (79, 122, 91)  # #4F7A5B - the corrected-F crossbar accent, see logo.svg

# The "corrected F" mark's three rects, in their native 0-100 viewBox space
# (stem, top bar, accent crossbar) - kept in sync with logo.svg by hand,
# since this script draws it at OG-card scale rather than rasterizing the SVG.
MARK_SHAPES = [(32, 18, 45, 82), (32, 18, 74, 31)]  # stem, top bar (WHITE)
MARK_ACCENT = (32, 44, 68, 57)                      # crossbar (MARK_GREEN)


def draw_brand_mark(draw, x, y, height):
    """Draw the corrected-F mark with its top-left corner at (x, y), scaled
    so the mark (viewBox 0-100, tall side) renders at `height` px."""
    scale = height / 100
    for x0, y0, x1, y1 in MARK_SHAPES:
        draw.rectangle(
            (x + x0 * scale, y + y0 * scale, x + x1 * scale, y + y1 * scale),
            fill=WHITE,
        )
    x0, y0, x1, y1 = MARK_ACCENT
    draw.rectangle(
        (x + x0 * scale, y + y0 * scale, x + x1 * scale, y + y1 * scale),
        fill=MARK_GREEN,
    )
BORDER = (46, 42, 31)      # --border (dark theme)

TITLE_FONT = FONTS_DIR / "InstrumentSerif-Italic.ttf"
MONO_BOLD_FONT = FONTS_DIR / "IBMPlexMono-Bold.ttf"
MONO_FONT = FONTS_DIR / "IBMPlexMono-Regular.ttf"
SANS_FONT = FONTS_DIR / "Archivo[wdth,wght].ttf"


def mono_bold(size):
    return ImageFont.truetype(str(MONO_BOLD_FONT), size)


def mono(size):
    return ImageFont.truetype(str(MONO_FONT), size)


def title_font(size):
    return ImageFont.truetype(str(TITLE_FONT), size)


def sans(size, weight=400):
    f = ImageFont.truetype(str(SANS_FONT), size)
    f.set_variation_by_axes([100, weight])  # [width, weight]
    return f


def fit_title(draw, text, max_width, start_size, min_size):
    """Shrink font size until the title fits max_width on <= 2 lines."""
    size = start_size
    while size >= min_size:
        f = title_font(size)
        wrapped = textwrap.wrap(text, width=max(8, int(max_width / (size * 0.5))))
        if len(wrapped) <= 2 and all(draw.textlength(line, font=f) <= max_width for line in wrapped):
            return f, wrapped
        size -= 4
    f = title_font(min_size)
    return f, textwrap.wrap(text, width=max(8, int(max_width / (min_size * 0.5))))


def render_card(out_path, kicker, title, subtitle, footer="thefaircode.xyz"):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    margin = 88

    # brand mark: the corrected-F symbol + "Fair Code."
    draw_brand_mark(draw, margin, 70, 54)
    mark_font = title_font(36)
    draw.text((margin + 34, 68), "Fair Code", font=mark_font, fill=WHITE)
    fc_w = draw.textlength("Fair Code", font=mark_font)
    draw.text((margin + 34 + fc_w, 68), ".", font=mark_font, fill=ACCENT)

    # kicker
    kicker_font = mono_bold(20)
    draw.text((margin, 150), kicker.upper(), font=kicker_font, fill=ACCENT)

    # title (auto-fit, up to 2 lines)
    tfont, lines = fit_title(draw, title, W - margin * 2, 76, 40)
    y = 206
    line_height = tfont.size + 16
    for line in lines:
        draw.text((margin, y), line, font=tfont, fill=WHITE)
        y += line_height

    # subtitle
    if subtitle:
        sub_font = sans(25, 400)
        sub_lines = textwrap.wrap(subtitle, width=72)[:3]
        y += 16
        for line in sub_lines:
            draw.text((margin, y), line, font=sub_font, fill=MUTED)
            y += 37

    # footer rule + domain
    draw.line((margin, H - 84, W - margin, H - 84), fill=BORDER, width=1)
    foot_font = mono(18)
    draw.text((margin, H - 64), footer, font=foot_font, fill=MUTED)
    right_text = "Open-source · MIT licensed"
    draw.text((W - margin - draw.textlength(right_text, font=foot_font), H - 64),
               right_text, font=foot_font, fill=MUTED)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    render_card(
        OUT_DIR / "home.png",
        kicker="Algorithmic bias research · Open source",
        title="The bias is real. So is the fix.",
        subtitle="Open-source audits across criminal justice, hiring, lending, "
                 "healthcare, welfare, and tenant screening - with measurable "
                 "before/after fairness results.",
    )

    render_card(
        OUT_DIR / "profiler.png",
        kicker="Fair Code · Open Dataset Profiler",
        title="Audit any CSV for demographic imbalance",
        subtitle="Missing subgroups, skewed distributions, geographic under-sampling - "
                 "100% client-side, your data never leaves your browser.",
    )

    entries = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    for entry in entries:
        render_card(
            OUT_DIR / f"{entry['slug']}.png",
            kicker="Fair Code · Explainer",
            title=entry["title"],
            subtitle=entry["summary"],
        )

    print(f"Generated {2 + len(entries)} OG images in {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
