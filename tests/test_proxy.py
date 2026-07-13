"""Tests for the opt-in chi-squared proxy hints (needs the scipy extra).

Run from the repo root:  pytest tests/ -q
"""

import pandas as pd
import pytest

from faircode import profile
from faircode.proxy import proxy_hints

pytest.importorskip("scipy", reason="proxy hints need the optional scipy extra")


def test_perfect_proxy_is_flagged():
    # occupation is a perfect function of sex -> maximal association.
    df = pd.DataFrame({
        "sex": ["male", "female"] * 100,
        "occupation": ["engineer", "nurse"] * 100,
    })
    dims = profile(df)["dimensions"]
    hints = proxy_hints(df, dims)
    pair = next(h for h in hints
                if {h["a"], h["b"]} == {"sex", "occupation"})
    assert pair["p_value"] < 0.05
    assert pair["cramers_v"] > 0.9   # near-perfect association (Yates-corrected)


def test_independent_columns_not_flagged():
    # Deterministic independence: sex alternates every row, grp every 3 rows,
    # so the two are (near) independent and should not be flagged.
    df = pd.DataFrame({
        "sex": ["male", "female"] * 150,
        "grp": ["x", "y", "z"] * 100,
    })
    hints = proxy_hints(df, profile(df)["dimensions"])
    assert not any({h["a"], h["b"]} == {"sex", "grp"} for h in hints)
