import pytest

# Adjust the import path to match your package structure (e.g., faircode.report)
from faircode.report import compare_to_html, compare_to_terminal, to_html, to_terminal


@pytest.fixture
def mock_profile_result():
    return {
        "n_rows": 1250,
        "n_cols": 8,
        "overall_score": 88,
        "grade": "B+",
        "dimensions": [
            {
                "name": "Gender",
                "kind": "Demographic",
                "dimension_score": 85,
                "under_represented": ["Non-binary"],
                "n_groups": 2,
                "imbalance_ratio": 1.6,
                "missing_pct": 0.02,
                "skewness": 0.3,
                "groups": [
                    {
                        "label": "Female",
                        "share": 0.45,
                        "count": 562,
                        "ci_low": 0.42,
                        "ci_high": 0.48,
                    }
                ],
            }
        ],
        "flags": ["Gender under-representation detected"],
    }


@pytest.fixture
def mock_compare_result():
    return {
        "score_delta": -5,
        "a": {"name": "Dataset A", "overall_score": 90, "n_rows": 1000, "grade": "A"},
        "b": {"name": "Dataset B", "overall_score": 85, "n_rows": 1200, "grade": "B"},
        "added_dimensions": ["NewDim"],
        "removed_dimensions": ["OldDim"],
        "flags": ["High drift in Gender"],
        "dimensions": [
            {
                "name": "Gender",
                "kind": "Demographic",
                "drift_level": "significant",
                "psi": 0.125,
                "tvd": 0.082,
                "dimension_score_a": 92,
                "dimension_score_b": 85,
                "dimension_score_delta": -7,
                "groups": [
                    {
                        "label": "Female",
                        "status": "shifted",
                        "share_a": 0.50,
                        "share_b": 0.40,
                        "share_delta": -0.10,
                    }
                ],
            }
        ],
    }


def test_to_html_smoke(mock_profile_result):
    """Smoke test for profile report rendering."""
    html_out = to_html(mock_profile_result)

    assert html_out.startswith("<!DOCTYPE html>")
    assert "</html>" in html_out
    assert "Dataset Representation Profile" in html_out


def test_to_html_renders_key_figures(mock_profile_result):
    """Verify raw calculated metrics appear in the rendered HTML."""
    html_out = to_html(mock_profile_result)

    assert "1,250" in html_out
    assert "88/100" in html_out
    assert "B+" in html_out
    assert "Gender" in html_out


def test_compare_to_html_smoke(mock_compare_result):
    """Smoke test for comparison drift report rendering."""
    html_out = compare_to_html(mock_compare_result)

    assert html_out.startswith("<!DOCTYPE html>")
    assert "</html>" in html_out
    assert "Representation Drift" in html_out


def test_compare_to_html_renders_key_figures(mock_compare_result):
    """Verify key drift metrics appear in the comparison report."""
    html_out = compare_to_html(mock_compare_result)

    assert "PSI" in html_out
    assert "0.125" in html_out
    assert "0.082" in html_out
    assert "significant" in html_out
    assert "Dataset A" in html_out
    assert "Dataset B" in html_out


def test_to_terminal_smoke(mock_profile_result):
    """Smoke test for the default (no --json/--html) profile report."""
    out = to_terminal(mock_profile_result)

    assert out.startswith("=" * 20)
    assert "FAIR CODE - DATASET REPRESENTATION PROFILE" in out


def test_to_terminal_renders_key_figures(mock_profile_result):
    out = to_terminal(mock_profile_result)

    assert "1,250" in out
    assert "88/100" in out
    assert "B+" in out
    assert "Gender" in out
    assert "Female" in out
    assert "<- under-represented" not in out  # Female isn't in under_represented


def test_to_terminal_marks_under_represented_group(mock_profile_result):
    mock_profile_result["dimensions"][0]["under_represented"] = ["Female"]

    out = to_terminal(mock_profile_result)

    assert "Female" in out
    assert "<- under-represented" in out


def test_to_terminal_renders_flags_section(mock_profile_result):
    out = to_terminal(mock_profile_result)

    assert "FLAGS" in out
    assert "Gender under-representation detected" in out


def test_to_terminal_renders_proxy_hints(mock_profile_result):
    mock_profile_result["proxy_hints"] = [
        {"a": "sex", "b": "region", "p_value": 1.64e-22, "cramers_v": 0.98}
    ]

    out = to_terminal(mock_profile_result)

    assert "PROXY HINTS" in out
    assert "sex" in out and "region" in out


def test_to_terminal_no_dimensions_detected():
    out = to_terminal({
        "n_rows": 10, "n_cols": 2, "overall_score": 0, "grade": "F",
        "dimensions": [], "flags": [],
    })

    assert "No demographic columns detected." in out


def test_compare_to_terminal_smoke(mock_compare_result):
    """Smoke test for the default (no --json/--html) compare report."""
    out = compare_to_terminal(mock_compare_result)

    assert out.startswith("=" * 20)
    assert "FAIR CODE - REPRESENTATION DRIFT" in out


def test_compare_to_terminal_renders_key_figures(mock_compare_result):
    out = compare_to_terminal(mock_compare_result)

    assert "Dataset A" in out
    assert "Dataset B" in out
    assert "PSI 0.125" in out
    assert "significant drift" in out
    assert "TVD 0.082" in out


def test_compare_to_terminal_renders_added_removed_dimensions(mock_compare_result):
    out = compare_to_terminal(mock_compare_result)

    assert "Only in B: NewDim" in out
    assert "Only in A: OldDim" in out


def test_compare_to_terminal_renders_drift_flags(mock_compare_result):
    out = compare_to_terminal(mock_compare_result)

    assert "DRIFT FLAGS" in out
    assert "High drift in Gender" in out


def test_compare_to_terminal_no_shared_dimensions():
    out = compare_to_terminal({
        "score_delta": 0,
        "a": {"name": "A", "overall_score": 100, "n_rows": 10, "grade": "A"},
        "b": {"name": "B", "overall_score": 100, "n_rows": 10, "grade": "A"},
        "added_dimensions": [], "removed_dimensions": [], "flags": [], "dimensions": [],
    })

    assert "No shared demographic dimensions to compare." in out