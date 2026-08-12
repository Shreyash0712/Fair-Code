import importlib.util
import json

import pytest

from faircode.cli import main

requires_openpyxl = pytest.mark.skipif(
    importlib.util.find_spec("openpyxl") is None,
    reason="optional 'excel' extra not installed",
)


def test_profile_fail_under_returns_nonzero_and_explains_score(tmp_path, capsys):
    path = tmp_path / "skewed.csv"
    path.write_text("sex\n" + "M\n" * 80 + "F\n" * 20, encoding="utf-8")

    exit_code = main(["profile", str(path), "--fail-under", "90"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Representation score:" in captured.out
    assert "representation score 72/100 is below --fail-under 90" in captured.err


def test_profile_fail_under_keeps_json_output_machine_readable(tmp_path, capsys):
    path = tmp_path / "balanced.csv"
    path.write_text("sex\nM\nF\nM\nF\n", encoding="utf-8")

    exit_code = main(["profile", str(path), "--json", "--fail-under", "90"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out)["overall_score"] == 100
    assert captured.err == ""


def test_profile_fail_under_equal_threshold_returns_zero(tmp_path, capsys):
    path = tmp_path / "balanced.csv"
    path.write_text("sex\nM\nF\nM\nF\n", encoding="utf-8")

    exit_code = main(["profile", str(path), "--fail-under", "100"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Representation score: 100/100" in captured.out
    assert captured.err == ""


def test_compare_fail_on_drift_returns_nonzero_and_explains(tmp_path, capsys):
    path_a = tmp_path / "a.csv"
    path_a.write_text("sex\n" + "M\n" * 50 + "F\n" * 50, encoding="utf-8")
    path_b = tmp_path / "b.csv"
    path_b.write_text("sex\n" + "M\n" * 90 + "F\n" * 10, encoding="utf-8")

    exit_code = main(["compare", str(path_a), str(path_b), "--fail-on-drift"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "representation drift detected" in captured.err
    assert "--fail-on-drift" in captured.err


def test_compare_without_fail_on_drift_still_returns_zero(tmp_path, capsys):
    path_a = tmp_path / "a.csv"
    path_a.write_text("sex\n" + "M\n" * 50 + "F\n" * 50, encoding="utf-8")
    path_b = tmp_path / "b.csv"
    path_b.write_text("sex\n" + "M\n" * 90 + "F\n" * 10, encoding="utf-8")

    exit_code = main(["compare", str(path_a), str(path_b)])

    assert exit_code == 0


def test_compare_fail_on_drift_returns_zero_when_stable(tmp_path, capsys):
    path_a = tmp_path / "a.csv"
    path_a.write_text("sex\nM\nF\nM\nF\n", encoding="utf-8")
    path_b = tmp_path / "b.csv"
    path_b.write_text("sex\nM\nF\nM\nF\n", encoding="utf-8")

    exit_code = main(["compare", str(path_a), str(path_b), "--fail-on-drift"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""


def test_compare_applies_map_override_to_both_datasets(tmp_path, capsys):
    path_a = tmp_path / "a.csv"
    path_a.write_text("gndr\n" + "M\n" * 8 + "F\n" * 2, encoding="utf-8")
    path_b = tmp_path / "b.csv"
    path_b.write_text("gndr\n" + "M\n" * 5 + "F\n" * 5, encoding="utf-8")

    exit_code = main(["compare", str(path_a), str(path_b), "--json", "--map", "gndr=sex"])

    captured = capsys.readouterr()
    assert exit_code == 0
    result = json.loads(captured.out)
    assert [d["name"] for d in result["dimensions"]] == ["gndr"]
    assert [d["kind"] for d in result["dimensions"]] == ["sex"]


def test_compare_without_map_leaves_column_generically_categorical(tmp_path, capsys):
    path_a = tmp_path / "a.csv"
    path_a.write_text("gndr\n" + "M\n" * 8 + "F\n" * 2, encoding="utf-8")
    path_b = tmp_path / "b.csv"
    path_b.write_text("gndr\n" + "M\n" * 5 + "F\n" * 5, encoding="utf-8")

    exit_code = main(["compare", str(path_a), str(path_b), "--json"])

    captured = capsys.readouterr()
    assert exit_code == 0
    result = json.loads(captured.out)
    assert [d["kind"] for d in result["dimensions"]] == ["categorical"]


@requires_openpyxl
def test_profile_xlsx_reports_ignored_sheets(tmp_path, capsys):
    import openpyxl

    path = tmp_path / "multi_sheet.xlsx"
    wb = openpyxl.Workbook()
    first = wb.active
    first.title = "Data"
    first.append(["sex"])
    first.append(["M"])
    first.append(["F"])
    wb.create_sheet("Notes")
    wb.create_sheet("Extra")
    wb.save(path)

    exit_code = main(["profile", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Read sheet 'Data' - 2 other sheet(s) ignored." in captured.err


@requires_openpyxl
def test_profile_xlsx_single_sheet_stays_silent(tmp_path, capsys):
    import openpyxl

    path = tmp_path / "single_sheet.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(["sex"])
    ws.append(["M"])
    ws.append(["F"])
    wb.save(path)

    exit_code = main(["profile", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "ignored" not in captured.err
