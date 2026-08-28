"""Render captured stdout from an audit's fair.py/unfair.py as a terminal-
style PNG screenshot (dark background, monospace text) - matching the visual
style of the existing fair.png/unfair.png files each audit folder ships,
which README.md documents as "terminal output" screenshots.

Usage: python3 scripts/render_terminal_png.py <input.txt> <output.png>
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "assets" / "fonts" / "IBMPlexMono-Regular.ttf"
FONT_SIZE = 15
LINE_HEIGHT = 21
PAD_X = 18
PAD_Y = 16
BG_COLOR = (40, 42, 53)
TEXT_COLOR = (248, 248, 243)
MAX_WIDTH_CHARS = 92


def render(text: str, out_path):
    lines = text.rstrip("\n").split("\n")
    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)

    # Measure with a scratch image, since char width needs a real font metric.
    scratch = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(scratch)
    char_width = draw.textlength("M", font=font)

    max_line_len = max((len(line) for line in lines), default=0)
    width = int(PAD_X * 2 + char_width * min(max_line_len, MAX_WIDTH_CHARS))
    height = PAD_Y * 2 + LINE_HEIGHT * len(lines)

    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    y = PAD_Y
    for line in lines:
        draw.text((PAD_X, y), line, font=font, fill=TEXT_COLOR)
        y += LINE_HEIGHT

    img.save(out_path)


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <input.txt> <output.png>", file=sys.stderr)
        raise SystemExit(2)
    text = Path(sys.argv[1]).read_text()
    render(text, sys.argv[2])


if __name__ == "__main__":
    main()
