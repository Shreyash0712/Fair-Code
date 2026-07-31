import json

from faircode.cli import main


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
