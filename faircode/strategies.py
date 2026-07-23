"""Five mitigation strategies - Layer 2 of the benchmark harness.

Given a manifest's core/proxy/protected feature partition, builds the
train/test feature set for five strategies of increasing mitigation:

  1. naive              - every feature; protected attributes included
  2. drop_protected      - protected attributes removed, proxies retained
  3. drop_proxies         - protected attributes AND proxies removed (the
                            classic fair.py fix every existing audit uses)
  4. reweigh              - same features as drop_proxies, plus per-row
                            sample weights that equalize the label x group
                            joint distribution on the training split
                            (Kamiran & Calders 2012 reweighing)
  5. threshold_equalized  - same features as drop_proxies, plus a per-group
                            decision threshold fit on the training split's
                            predicted probabilities so each group's
                            selection rate matches the overall base rate
                            (a simplified demographic-parity post-processor)

Strategies 4 and 5 key their group/label balancing off the manifest's FIRST
declared protected attribute; every strategy is still scored against every
declared protected attribute in faircode.benchmark, so a contributor can see
whether mitigating one attribute helps or harms another.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pandas.api.types as pdt
from sklearn.preprocessing import LabelEncoder

STRATEGIES = ("naive", "drop_protected", "drop_proxies", "reweigh", "threshold_equalized")

_THRESHOLD_GRID = np.linspace(0.0, 1.0, 101)


def encode_features(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Label-encode categorical columns, pass numeric columns through.

    Uniform ordinal encoding (rather than one-hot) keeps the harness code
    path identical across audits regardless of a categorical column's
    cardinality - several audits (e.g. Healthcare Readmission's ICD
    diagnosis codes) have hundreds of categories, where one-hot encoding
    would blow up the feature matrix differently per audit. Missing values
    are filled (median for numeric, a sentinel category for categorical) so
    every model family gets a fully-populated matrix.
    """
    out = pd.DataFrame(index=df.index)
    for col in columns:
        series = df[col]
        if pdt.is_numeric_dtype(series):
            numeric = pd.to_numeric(series, errors="coerce")
            median = numeric.median()
            out[col] = numeric.fillna(0.0 if pd.isna(median) else median)
        else:
            filled = series.astype(str).fillna("__missing__")
            out[col] = LabelEncoder().fit_transform(filled)
    return out


def strategy_features(strategy: str, core: list, proxies: list, protected: list) -> list:
    if strategy == "naive":
        return list(dict.fromkeys(core + proxies + protected))
    if strategy == "drop_protected":
        return list(dict.fromkeys(core + proxies))
    return list(core)  # drop_proxies, reweigh, threshold_equalized


def reweigh(y_train, disadvantaged_train) -> np.ndarray:
    """Kamiran & Calders (2012) reweighing: per-row weight that equalizes the
    (group, label) joint distribution to what independence would predict."""
    y = np.asarray(y_train)
    g = np.asarray(disadvantaged_train, dtype=bool)
    n = len(y)
    weights = np.ones(n, dtype=float)
    for g_val in (True, False):
        for y_val in (0, 1):
            cell = (g == g_val) & (y == y_val)
            n_cell = int(cell.sum())
            if n_cell == 0:
                continue
            p_group = float((g == g_val).mean())
            p_label = float((y == y_val).mean())
            p_joint = n_cell / n
            weights[cell] = (p_group * p_label) / p_joint
    return weights


def _best_threshold(proba: np.ndarray, target_rate: float) -> float:
    if len(proba) == 0:
        return 0.5
    rates = (proba[None, :] >= _THRESHOLD_GRID[:, None]).mean(axis=1)
    return float(_THRESHOLD_GRID[np.argmin(np.abs(rates - target_rate))])


def equalize_thresholds(train_proba, train_disadvantaged, test_proba, test_disadvantaged):
    """Fit per-group thresholds on train-set probabilities, apply at test time.

    A simplified demographic-parity post-processor: both groups' selection
    rate is pushed toward the overall base rate the model would produce at
    the default 0.5 threshold. Thresholds are fit on the training split and
    only applied (never re-fit) on the test split, so the test metrics stay
    out-of-sample.
    """
    train_proba = np.asarray(train_proba)
    test_proba = np.asarray(test_proba)
    train_disadvantaged = np.asarray(train_disadvantaged, dtype=bool)
    test_disadvantaged = np.asarray(test_disadvantaged, dtype=bool)

    target_rate = float((train_proba >= 0.5).mean())
    thr_disadv = _best_threshold(train_proba[train_disadvantaged], target_rate)
    thr_adv = _best_threshold(train_proba[~train_disadvantaged], target_rate)

    pred = np.zeros(len(test_proba), dtype=int)
    pred[test_disadvantaged] = (test_proba[test_disadvantaged] >= thr_disadv).astype(int)
    pred[~test_disadvantaged] = (test_proba[~test_disadvantaged] >= thr_adv).astype(int)
    info = {
        "threshold_disadvantaged": thr_disadv,
        "threshold_advantaged": thr_adv,
        "target_rate": target_rate,
    }
    return pred, info
