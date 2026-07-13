"""Chi-squared proxy hints (informational; CLI/Python only).

Flags pairs of detected demographic columns that are strongly associated - a
"this column may be a proxy for that protected attribute" signal, the same
chi-squared pattern the bias audits use. Requires the optional scipy extra
(`pip install faircode[proxy]`).

This is intentionally NOT part of profile() or the JS engine: it is an opt-in
add-on that never affects the representation score, so the two engines stay
bit-for-bit identical. The result is attached to the profile under
`proxy_hints` by the CLI when `--proxy-hints` is passed.
"""

from __future__ import annotations

import math

import pandas as pd

from .profiler import _age_band, _age_to_numeric, _looks_like_dates

PROXY_ALPHA = 0.05


def _labelize(df, name, kind):
    """Same value normalization the intersection crosstab uses (age → bands)."""
    if kind == "age" and not _looks_like_dates(df[name]):
        nums = [_age_to_numeric(v) for v in df[name]]
        if any(n is not None for n in nums):
            return pd.Series([_age_band(n) for n in nums], index=df.index)
    return df[name].astype("object")


def proxy_hints(df: pd.DataFrame, dimensions: list, alpha=PROXY_ALPHA) -> list:
    """Chi-squared test of independence over every pair of detected dimensions.

    Returns pairs with p < alpha, most-significant first, each with its p-value
    and Cramér's V effect size. Raises RuntimeError if scipy is unavailable.
    """
    try:
        from scipy.stats import chi2_contingency
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise RuntimeError(
            "proxy hints need scipy (install with: pip install faircode[proxy])"
        ) from exc

    cols = [(d["name"], d["kind"]) for d in dimensions]
    hints = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            name_a, kind_a = cols[i]
            name_b, kind_b = cols[j]
            ct = pd.crosstab(_labelize(df, name_a, kind_a),
                             _labelize(df, name_b, kind_b))
            if ct.shape[0] < 2 or ct.shape[1] < 2:
                continue
            chi2, p_value, _dof, _exp = chi2_contingency(ct)
            n = int(ct.to_numpy().sum())
            k = min(ct.shape) - 1
            cramers_v = math.sqrt(chi2 / (n * k)) if n and k else 0.0
            if p_value < alpha:
                hints.append({
                    "a": name_a, "b": name_b,
                    "p_value": p_value,
                    "cramers_v": round(cramers_v, 4),
                    "chi2": round(float(chi2), 2),
                })
    hints.sort(key=lambda h: h["p_value"])
    return hints
