"""Read a tabular dataset file, extending faircode.loaders with formats
added after the paper freeze (.json, .parquet).

`faircode/loaders.py` is on the frozen file list in CLAUDE.md and must stay
byte-identical to what the paper's benchmark was run against - the benchmark
harness (`faircode/benchmark.py`) reads its CSVs directly via `pd.read_csv`
and never imports it, so it has no bearing on any published number, but the
file itself is still not touched. New formats live here instead and delegate
to the frozen `read_table()` for everything it already handles.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pandas as pd

from .loaders import SNIFF_SAMPLE_BYTES, _sniff_delimiter
from .loaders import read_table as _read_table_frozen


def read_table(path: str) -> pd.DataFrame:
    if path == "-":
        # No file extension to dispatch on for a stdin stream, so always
        # sniff - the same fallback loaders.read_table() uses for an
        # unrecognized/missing extension on a real file.
        content = sys.stdin.read()
        delimiter = _sniff_delimiter(content[:SNIFF_SAMPLE_BYTES])
        return pd.read_csv(io.StringIO(content), sep=delimiter)

    suffix = Path(path).suffix.lower()

    if suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            # pandas' own parser error for malformed JSON (e.g. a truncated
            # file) is an internal/version-specific message. Fail fast with
            # a clear message instead, mirroring the JS engine's parseJSON().
            raise ValueError(f"Unsupported JSON format (not valid JSON: {exc}).") from exc
        # Detect split-orient ({"columns": [...], "data": [...]}, optionally
        # "index") from the parsed shape rather than trying the default
        # (records) orientation first and catching its ValueError: a split
        # file that omits the optional "index" key parses without error
        # under the default orientation too - as two columns literally named
        # "columns" and "data" - so the ValueError this used to rely on
        # never fires, and the wrong shape comes back silently.
        if isinstance(parsed, dict) and {"columns", "data"} <= parsed.keys():
            return pd.read_json(path, orient="split")
        return pd.read_json(path)

    if suffix == ".parquet":
        try:
            return pd.read_parquet(path)
        except ImportError as exc:
            raise RuntimeError(
                "reading .parquet files requires the 'pyarrow' package "
                "(install with: pip install faircode[parquet])"
            ) from exc

    return _read_table_frozen(path)


def get_xlsx_sheet_info(path: str) -> tuple[str, list[str]] | None:
    """For an .xlsx file, return (sheet_name_read, other_sheet_names_ignored).

    `read_table()` always reads pandas' default sheet (index 0, via the
    frozen `loaders.read_table()`) - this only inspects what else is in the
    workbook so callers can tell a user which sheet was actually profiled,
    mirroring the web profiler's `parseXLSX()` (#182). Returns None for a
    non-.xlsx path, or if the workbook can't be opened - `read_table()`'s own
    error path already surfaces the real problem in that case.
    """
    if Path(path).suffix.lower() != ".xlsx":
        return None
    try:
        book = pd.ExcelFile(path)
    except Exception:
        return None
    if not book.sheet_names:
        return None
    return book.sheet_names[0], book.sheet_names[1:]
