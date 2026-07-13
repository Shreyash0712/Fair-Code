"""Tests for the fairness-gap significance module.

Run from the repo root:  pytest tests/ -q
"""

import pytest

from faircode.significance import (
    bootstrap_ci,
    permutation_test,
    significance_report,
)


# ── Zero-gap case ────────────────────────────────────────────────────────────
def test_identical_groups_have_zero_gap_and_high_p():
    a = [1, 0] * 50
    b = [1, 0] * 50
    rep = significance_report(a, b)
    assert rep["gap"] == 0.0
    assert rep["p_value"] > 0.9          # label shuffling can't beat a zero gap
    assert not rep["significant"]
    assert rep["ci_low"] <= 0.0 <= rep["ci_high"]


# ── Large-gap case ───────────────────────────────────────────────────────────
def test_separated_groups_are_significant_and_ci_excludes_zero():
    a = [1] * 90 + [0] * 10   # 0.9 positive rate
    b = [0] * 90 + [1] * 10   # 0.1 positive rate
    rep = significance_report(a, b)
    assert rep["gap"] == pytest.approx(0.8, abs=1e-9)
    assert rep["p_value"] < 0.05
    assert rep["significant"]
    assert rep["ci_low"] > 0.0           # interval sits entirely above zero
    assert rep["ci_low"] <= rep["gap"] <= rep["ci_high"]


# ── Determinism ──────────────────────────────────────────────────────────────
def test_random_state_makes_results_deterministic():
    a = [1] * 40 + [0] * 60
    b = [1] * 25 + [0] * 75
    assert significance_report(a, b) == significance_report(a, b)
    # An explicit seed pins bootstrap and permutation to the same numbers.
    assert bootstrap_ci(a, b, random_state=7) == bootstrap_ci(a, b, random_state=7)
    assert (permutation_test(a, b, random_state=7)
            == permutation_test(a, b, random_state=7))


# ── Small-sample warning ─────────────────────────────────────────────────────
def test_small_sample_warning_trigger():
    small = [1, 0] * 7           # n = 14 < 30
    large = [1, 0] * 100         # n = 200
    assert significance_report(small, large)["small_sample_warning"]
    assert significance_report(large, small)["small_sample_warning"]
    assert not significance_report(large, large)["small_sample_warning"]
