#!/usr/bin/env python3
"""Fails if the generated site files (explainer pages, sitemap, OG images,
llms-full.txt) are out of date relative to their sources.

Used by .github/workflows/build-explainers.yml, run *after* the workflow's
own `build_explainers.py`/`generate_og_images.py` steps have already
regenerated everything fresh into the working tree - this script then
checks whether that fresh regeneration actually matches what's committed.

Text-based generated files (explainer HTML, explainers-data.js, sitemap.xml,
llms-full.txt) are compared byte-for-byte via `git diff` - they've never
shown any platform-dependent variation.

PNGs are compared by *decoded pixel content*, not raw file bytes. Pillow's
`optimize=True` (and even a fixed `compress_level`) runs zlib's deflate,
and different zlib builds bundled into different platforms' Pillow wheels
can produce different compressed bytes for identical pixel data - a
macOS-generated commit can then never byte-match CI's Ubuntu-side fresh
regeneration, even though the image is genuinely up to date (see #262,
where this was first hit, and the follow-up where a fixed compress_level
turned out not to fix it either). Decoding both sides and comparing pixels
is the check that actually reflects "is this image current."

Run locally:  python3 scripts/check_generated_files_current.py
Exit code:    0 = everything current, 1 = something is genuinely stale.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image
import io

ROOT = Path(__file__).resolve().parent.parent

TEXT_GLOBS = [
    "explainers/*.html",
    "assets/explainers-data.js",
    "sitemap.xml",
    "llms-full.txt",
]
PNG_GLOBS = [
    "assets/og/*.png",
    "assets/og-light/*.png",
]


def _tracked_paths(pattern):
    out = subprocess.run(
        ["git", "ls-files", pattern], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [ROOT / line for line in out.splitlines() if line.strip()]


def _git_show(rel_path):
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel_path}"], cwd=ROOT, capture_output=True, check=False
    )
    return result.stdout if result.returncode == 0 else None


def _pixels_differ(rel_path, working_path):
    committed_bytes = _git_show(rel_path)
    if committed_bytes is None:
        return True, "not committed at HEAD (new file)"

    try:
        committed_img = Image.open(io.BytesIO(committed_bytes)).convert("RGBA")
        working_img = Image.open(working_path).convert("RGBA")
    except Exception as exc:
        return True, f"could not decode: {exc}"

    if committed_img.size != working_img.size:
        return True, f"size differs: committed {committed_img.size} vs fresh {working_img.size}"
    if committed_img.tobytes() != working_img.tobytes():
        return True, "pixel content differs"
    return False, None


def main():
    stale = []

    for pattern in TEXT_GLOBS:
        for path in _tracked_paths(pattern):
            rel = path.relative_to(ROOT)
            diff = subprocess.run(
                ["git", "diff", "--quiet", "--", str(rel)], cwd=ROOT
            ).returncode
            if diff != 0:
                stale.append((rel, "content differs (text diff)"))

    for pattern in PNG_GLOBS:
        for path in _tracked_paths(pattern):
            rel = path.relative_to(ROOT)
            differs, reason = _pixels_differ(str(rel), path)
            if differs:
                stale.append((rel, reason))

    if stale:
        print("Generated files are out of date - run 'make build-explainers' locally and commit the result.")
        for rel, reason in stale:
            print(f"  {rel}: {reason}")
        return 1

    print("Generated files are up to date (text diff exact, PNGs compared by decoded pixel content).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
