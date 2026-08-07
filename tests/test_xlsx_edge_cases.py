"""Edge-case coverage for .xlsx parsing on both the Python loader
(faircode.loaders.read_table) and the browser profiler engine's
parseXLSX() (#187).

Run from the repo root: pytest tests/test_xlsx_edge_cases.py -q
"""

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

from faircode.loaders import read_table

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

requires_openpyxl = pytest.mark.skipif(
    importlib.util.find_spec("openpyxl") is None,
    reason="optional 'excel' extra not installed",
)


def _run_js_parse(tmp_path, workbook_path):
    completed = subprocess.run(
        ["node", "scripts/engine-js.js", "profile-xlsx", str(workbook_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    return completed


def _copy_fixture(tmp_path):
    src = FIXTURES / "adult_sample.xlsx"
    dst = tmp_path / "input.xlsx"
    dst.write_bytes(src.read_bytes())
    return dst

def test_headers_only_xlsx_js(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["age", "sex", "income"])

    path = tmp_path / "headers_only.xlsx"
    wb.save(path)

    result = _run_js_parse(tmp_path, path)

    assert result.returncode != 0
    assert "The workbook contains no usable data." in result.stderr

def test_empty_workbook_js(tmp_path):
    wb = openpyxl.Workbook()

    path = tmp_path / "empty.xlsx"
    wb.save(path)

    result = _run_js_parse(tmp_path, path)

    assert result.returncode != 0
    assert "The workbook contains no usable data." in result.stderr

def test_empty_first_sheet_populated_second_sheet_js(tmp_path):
    wb = openpyxl.Workbook()

    first = wb.active
    first.title = "Empty"

    second = wb.create_sheet("Data")
    second.append(["age", "sex"])
    second.append([20, "F"])

    path = tmp_path / "second_sheet.xlsx"
    wb.save(path)

    result = _run_js_parse(tmp_path, path)

    assert result.returncode != 0
    assert "The workbook contains no usable data." in result.stderr

def test_hidden_first_sheet_js(tmp_path):
    wb = openpyxl.Workbook()

    first = wb.active
    first.title = "Hidden"
    first.sheet_state = "hidden"

    second = wb.create_sheet("Visible")
    second.append(["age", "sex"])
    second.append([20, "F"])

    path = tmp_path / "hidden_first.xlsx"
    wb.save(path)

    result = _run_js_parse(tmp_path, path)

    assert result.returncode != 0
    assert "The workbook contains no usable data." in result.stderr

@requires_openpyxl
def test_headers_only_xlsx_python(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["age", "sex", "income"])

    path = tmp_path / "headers_only.xlsx"
    wb.save(path)

    df = read_table(str(path))

    assert list(df.columns) == ["age", "sex", "income"]
    assert df.empty
@requires_openpyxl
def test_empty_workbook_python(tmp_path):
    wb = openpyxl.Workbook()

    path = tmp_path / "empty.xlsx"
    wb.save(path)

    df = read_table(str(path))

    assert df.empty
    assert list(df.columns) == []
@requires_openpyxl
def test_empty_first_sheet_populated_second_sheet_python(tmp_path):
    wb = openpyxl.Workbook()

    first = wb.active
    first.title = "Empty"

    second = wb.create_sheet("Data")
    second.append(["age", "sex"])
    second.append([20, "F"])

    path = tmp_path / "second_sheet.xlsx"
    wb.save(path)

    df = read_table(str(path))

    assert df.empty
@requires_openpyxl
def test_hidden_first_sheet_python(tmp_path):
    wb = openpyxl.Workbook()

    first = wb.active
    first.title = "Hidden"
    first.sheet_state = "hidden"

    second = wb.create_sheet("Visible")
    second.append(["age", "sex"])
    second.append([20, "F"])

    path = tmp_path / "hidden_first.xlsx"
    wb.save(path)

    df = read_table(str(path))

    assert df.empty
