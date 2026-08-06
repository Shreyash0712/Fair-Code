import pytest

# Adjust the import path to match your package structure (e.g., faircode.report)
from faircode.report import compare_to_html, to_html


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
        "score_delta": -5.0,
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
                "dimension_score_delta": -7.0,
                "groups": [
                    {
                        "label": "Female",
                        "status": "changed",
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