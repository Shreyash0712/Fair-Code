"""Tests for faircode.loaders: format-agnostic dataset reading (#59).

Run from the repo root:  pytest tests/ -q
"""

import importlib.util

import pandas as pd
import pytest

from faircode import profile
from faircode.loaders import _sniff_delimiter, read_table

requires_openpyxl = pytest.mark.skipif(
    importlib.util.find_spec("openpyxl") is None,
    reason="optional 'excel' extra not installed",
)


ROWS = {
    "patient_id": [1, 2, 3, 4],
    "sex": ["M", "F", "M", "F"],
    "age": [24, 31, 45, 62],
}


def _write_csv(path, sep=","):
    df = pd.DataFrame(ROWS)
    df.to_csv(path, sep=sep, index=False)
    return df


# ── Delimiter sniffing ───────────────────────────────────────────────────────
def test_sniff_delimiter_detects_tab():
    sample = "a\tb\tc\n1\t2\t3\n4\t5\t6\n"
    assert _sniff_delimiter(sample) == "\t"


def test_sniff_delimiter_detects_comma():
    sample = "a,b,c\n1,2,3\n4,5,6\n"
    assert _sniff_delimiter(sample) == ","


def test_sniff_delimiter_falls_back_to_comma_default():
    assert _sniff_delimiter("just one column\nno delimiter at all\n") == ","


# ── read_table by extension ──────────────────────────────────────────────────
def test_read_table_tsv(tmp_path):
    path = tmp_path / "data.tsv"
    _write_csv(path, sep="\t")
    df = read_table(str(path))
    assert list(df.columns) == ["patient_id", "sex", "age"]
    assert len(df) == 4


def test_read_table_csv(tmp_path):
    path = tmp_path / "data.csv"
    _write_csv(path, sep=",")
    df = read_table(str(path))
    assert list(df.columns) == ["patient_id", "sex", "age"]


@requires_openpyxl
def test_read_table_xlsx(tmp_path):
    path = tmp_path / "data.xlsx"
    pd.DataFrame(ROWS).to_excel(path, index=False)
    df = read_table(str(path))
    assert list(df.columns) == ["patient_id", "sex", "age"]
    assert len(df) == 4


def test_read_table_unknown_extension_sniffs_tabs(tmp_path):
    path = tmp_path / "data.txt"
    _write_csv(path, sep="\t")
    df = read_table(str(path))
    assert list(df.columns) == ["patient_id", "sex", "age"]


# ── Parity: profile() must produce identical results across formats ─────────
def test_tsv_and_csv_profile_identically(tmp_path):
    csv_path = tmp_path / "data.csv"
    tsv_path = tmp_path / "data.tsv"
    _write_csv(csv_path, sep=",")
    _write_csv(tsv_path, sep="\t")

    result_csv = profile(read_table(str(csv_path)))
    result_tsv = profile(read_table(str(tsv_path)))
    assert result_csv == result_tsv


@requires_openpyxl
def test_xlsx_and_csv_profile_identically(tmp_path):
    csv_path = tmp_path / "data.csv"
    xlsx_path = tmp_path / "data.xlsx"
    _write_csv(csv_path, sep=",")
    pd.DataFrame(ROWS).to_excel(xlsx_path, index=False)

    result_csv = profile(read_table(str(csv_path)))
    result_xlsx = profile(read_table(str(xlsx_path)))
    assert result_csv == result_xlsx
