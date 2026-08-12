"""Validate that every path pattern in .github/CODEOWNERS still matches a
file or directory actually tracked in the repo (#207) - the same spirit as
tests/test_manifest.py's row_filters validation (#168), applied to the
review-routing config instead of an audit manifest.

Run from the repo root:  pytest tests/test_codeowners.py -q
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CODEOWNERS_PATH = REPO_ROOT / ".github" / "CODEOWNERS"


def _tracked_files():
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def _parse_codeowners_paths():
    """Return [(line_no, pattern, owners)] for every non-comment, non-blank line."""
    entries = []
    for line_no, raw in enumerate(CODEOWNERS_PATH.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        entries.append((line_no, parts[0], parts[1:]))
    return entries


def _pattern_matches_a_tracked_path(pattern, tracked):
    """Mirror gitignore-style CODEOWNERS matching closely enough to validate
    the small set of pattern shapes this repo actually uses: an anchored
    file (/a/b.ext), an anchored directory (/a/b/), and a **/name glob."""
    if pattern.startswith("**/"):
        name = pattern[len("**/"):]
        return any(Path(t).name == name for t in tracked)

    anchored = pattern.lstrip("/")
    if pattern.endswith("/"):
        prefix = anchored.rstrip("/") + "/"
        return any(t.startswith(prefix) for t in tracked)

    return anchored in tracked


def test_codeowners_file_exists():
    assert CODEOWNERS_PATH.is_file(), ".github/CODEOWNERS is missing"


def test_every_codeowners_path_matches_a_tracked_file_or_directory():
    tracked = _tracked_files()
    entries = _parse_codeowners_paths()
    assert entries, "no path entries found in .github/CODEOWNERS"

    stale = [
        f"{CODEOWNERS_PATH.relative_to(REPO_ROOT)}:{line_no}: pattern {pattern!r} "
        f"matches no tracked file or directory"
        for line_no, pattern, _owners in entries
        if not _pattern_matches_a_tracked_path(pattern, tracked)
    ]
    assert not stale, "Stale CODEOWNERS entries:\n" + "\n".join(stale)


def test_every_codeowners_entry_names_at_least_one_owner():
    entries = _parse_codeowners_paths()

    missing_owners = [
        f".github/CODEOWNERS:{line_no}: {pattern!r} has no owner listed"
        for line_no, pattern, owners in entries
        if not owners
    ]
    assert not missing_owners, "\n".join(missing_owners)


def test_every_codeowners_owner_is_a_valid_github_handle():
    handle_re = re.compile(r"^@[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
    entries = _parse_codeowners_paths()

    bad = [
        f".github/CODEOWNERS:{line_no}: {pattern!r} has a malformed owner {owner!r}"
        for line_no, pattern, owners in entries
        for owner in owners
        if not handle_re.match(owner)
    ]
    assert not bad, "\n".join(bad)
