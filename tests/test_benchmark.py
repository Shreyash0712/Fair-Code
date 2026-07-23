"""End-to-end test of the benchmark harness against ONE small audit.

This is the test that catches a contributed audit.yaml (or a change to
manifest.py/strategies.py/models.py/metrics.py) breaking the pipeline before
it reaches a PR - it runs the real thing, not a mock of it. German Credit
Lending is used because it's the smallest dataset (1,000 rows): the full
five-strategy x three-model grid, including fairlearn's ExponentiatedGradient
(which refits its base estimator multiple times), finishes in seconds here.
The full seven-domain sweep is deliberately NOT run in this suite - it's slow
(fairlearn's in-processing strategy alone takes minutes per audit on the
larger datasets) - see "Reproducibility & Paper Freeze" in README.md: run it
locally and commit results/ output instead of running it in CI.

Run from the repo root:  pytest tests/ -q
"""

from pathlib import Path

import pandas as pd
import pytest

pytest.importorskip("sklearn", reason="the benchmark harness needs the optional benchmark extra")
pytest.importorskip("fairlearn", reason="the benchmark harness needs the optional benchmark extra")
pytest.importorskip("yaml", reason="the benchmark harness needs the optional benchmark extra")

from faircode.benchmark import run_audit
from faircode.manifest import load_manifest
from faircode.metrics import METRICS, PERFORMANCE_METRICS
from faircode.strategies import STRATEGIES

REPO_ROOT = Path(__file__).resolve().parent.parent
SMALL_AUDIT = REPO_ROOT / "German Credit Lending" / "audit.yaml"

# Small enough to keep this test fast; not meant to be publication-quality.
N_RESAMPLES = 50
N_PERMUTATIONS = 50


@pytest.fixture(scope="module")
def result():
    manifest = load_manifest(SMALL_AUDIT)
    return run_audit(manifest, n_resamples=N_RESAMPLES, n_permutations=N_PERMUTATIONS)


def test_runs_without_raising(result):
    fairness_rows, performance_rows = result
    assert fairness_rows
    assert performance_rows


def test_fairness_table_covers_every_strategy_and_model(result):
    fairness_rows, _ = result
    df = pd.DataFrame(fairness_rows)
    assert set(df["strategy"]) == set(STRATEGIES)
    assert set(df["model"]) == {"logistic_regression", "random_forest", "gradient_boosting"}
    assert set(df["metric"]) == set(METRICS)
    # German Credit Lending declares one protected attribute (age) and no
    # pairs, so there's no intersectional row and every row is tagged "age".
    assert set(df["protected_attribute"]) == {"age"}


def test_performance_table_covers_every_strategy_and_model(result):
    _, performance_rows = result
    df = pd.DataFrame(performance_rows)
    assert set(df["strategy"]) == set(STRATEGIES)
    assert set(df["model"]) == {"logistic_regression", "random_forest", "gradient_boosting"}
    assert set(df["metric"]) == set(PERFORMANCE_METRICS)


def test_expected_row_counts(result):
    fairness_rows, performance_rows = result
    n_strategies, n_models = 5, 3
    n_protected_attrs = 1   # German Credit Lending has one protected attribute, no pairs
    assert len(fairness_rows) == n_strategies * n_models * n_protected_attrs * len(METRICS)
    assert len(performance_rows) == n_strategies * n_models * len(PERFORMANCE_METRICS)


def test_every_fairness_row_has_required_keys(result):
    fairness_rows, _ = result
    required = {"audit", "strategy", "model", "protected_attribute", "metric",
               "value", "ci_low", "ci_high", "p_value", "significant",
               "n_disadvantaged", "n_advantaged", "small_sample_warning", "note"}
    for row in fairness_rows:
        assert required <= set(row)


def test_post_processing_has_no_auc_by_design(result):
    # ThresholdOptimizer (S4) has no probability output - see faircode.strategies.
    _, performance_rows = result
    df = pd.DataFrame(performance_rows)
    post_auc = df[(df["strategy"] == "post_processing") & (df["metric"] == "auc")]
    assert post_auc["value"].isna().all()


def test_baseline_demographic_parity_gap_is_a_plausible_fraction(result):
    fairness_rows, _ = result
    df = pd.DataFrame(fairness_rows)
    baseline_dp = df[(df["strategy"] == "baseline") & (df["metric"] == "demographic_parity_diff")]
    assert len(baseline_dp) == 3   # one per model
    assert baseline_dp["value"].between(-1.0, 1.0).all()
