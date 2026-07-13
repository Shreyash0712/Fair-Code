"""Command-line interface for the Fair Code dataset profiler.

    faircode profile data.csv
    faircode profile data.tsv
    faircode profile data.xlsx
    faircode profile data.csv --json
    faircode profile data.csv --html report.html
    faircode compare train.csv prod.csv
    faircode compare train.csv prod.csv --json

Uses only stdlib argparse + pandas (no heavyweight profiling dependency).
Reading .xlsx additionally requires the optional 'openpyxl' extra.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .compare import compare
from .detect import VALID_KINDS
from .loaders import read_table
from .profiler import parse_reference, profile
from .proxy import proxy_hints
from .report import compare_to_terminal, to_html, to_json, to_terminal

_MAP_CHOICES = VALID_KINDS + ("ignore",)


def _parse_map(pairs):
    """Parse repeated --map COL=KIND flags into an {column: kind} override dict."""
    overrides = {}
    for pair in pairs or []:
        if "=" not in pair:
            print(f"error: invalid --map '{pair}', expected COL=KIND", file=sys.stderr)
            raise SystemExit(2)
        col, kind = pair.split("=", 1)
        kind = kind.strip().lower()
        if kind not in _MAP_CHOICES:
            print(f"error: invalid --map kind '{kind}' for column '{col.strip()}'; "
                  f"choose from {', '.join(_MAP_CHOICES)}", file=sys.stderr)
            raise SystemExit(2)
        overrides[col.strip()] = kind
    return overrides


def _read_or_exit(path: str):
    """Read a table, or print a plain error and raise SystemExit(2)."""
    try:
        return read_table(path)
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except Exception as exc:  # noqa: BLE001 - surface any parse failure plainly
        print(f"error: could not read dataset {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="faircode",
        description="Audit a tabular dataset for demographic representation.",
    )
    parser.add_argument("--version", action="version",
                        version=f"faircode {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("profile", help="profile a dataset for demographic imbalance")
    p.add_argument("csv", help="path to the dataset file (.csv, .tsv, or .xlsx)")
    p.add_argument("--json", action="store_true", help="emit JSON to stdout")
    p.add_argument("--html", metavar="PATH",
                   help="write a standalone HTML report to PATH")
    p.add_argument("--map", action="append", metavar="COL=KIND",
                   help="force a column's dimension when auto-detection misses it; "
                        "KIND is one of " + ", ".join(_MAP_CHOICES) + " (repeatable)")
    p.add_argument("--cross", metavar="COLA,COLB",
                   help="cross these two columns for the intersectional gap "
                        "(default: the first two detected dimensions)")
    p.add_argument("--reference", metavar="PATH",
                   help="score against a reference baseline CSV (columns: column,group,share)")
    p.add_argument("--proxy-hints", action="store_true",
                   help="flag strongly-associated column pairs via chi-squared (needs scipy)")
    p.add_argument("--min-share", type=float, metavar="F",
                   help="under-representation threshold (default 0.05)")
    p.add_argument("--intersection-floor", type=float, metavar="F",
                   help="near-empty intersection-cell threshold (default 0.01)")
    p.add_argument("--imbalance-flag", type=float, metavar="F",
                   help="imbalance-ratio flag threshold (default 3.0)")
    p.add_argument("--missing-flag", type=float, metavar="F",
                   help="missing-data flag threshold (default 0.05)")

    c = sub.add_parser("compare",
                       help="compare two datasets for representation drift")
    c.add_argument("csv_a", help="baseline dataset A (.csv, .tsv, or .xlsx)")
    c.add_argument("csv_b", help="current dataset B (.csv, .tsv, or .xlsx)")
    c.add_argument("--json", action="store_true", help="emit JSON to stdout")

    args = parser.parse_args(argv)

    if args.command == "profile":
        df = _read_or_exit(args.csv)

        opts = {
            "min_share": args.min_share,
            "intersection_floor": args.intersection_floor,
            "imbalance_flag": args.imbalance_flag,
            "missing_flag": args.missing_flag,
        }
        if args.cross:
            parts = [c.strip() for c in args.cross.split(",")]
            if len(parts) != 2 or not all(parts):
                print("error: --cross expects two column names: COLA,COLB",
                      file=sys.stderr)
                return 2
            opts["cross"] = parts
        if args.reference:
            try:
                opts["reference"] = parse_reference(_read_or_exit(args.reference))
            except ValueError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 2

        result = profile(df, _parse_map(args.map), opts)

        if args.proxy_hints:
            try:
                result["proxy_hints"] = proxy_hints(df, result["dimensions"])
            except RuntimeError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 2

        if args.html:
            with open(args.html, "w", encoding="utf-8") as fh:
                fh.write(to_html(result))
            print(f"HTML report written to {args.html}", file=sys.stderr)

        if args.json:
            print(to_json(result))
        else:
            print(to_terminal(result))
        return 0

    if args.command == "compare":
        result = compare(
            profile(_read_or_exit(args.csv_a)),
            profile(_read_or_exit(args.csv_b)),
            name_a=args.csv_a, name_b=args.csv_b,
        )
        if args.json:
            print(to_json(result))
        else:
            print(compare_to_terminal(result))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
