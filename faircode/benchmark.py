"""Cross-domain fairness benchmark harness - Layer 2 of the two-layer
architecture documented in faircode/MANIFEST_SPEC.md.

Reads every audit.yaml manifest and runs the SAME pipeline over each one -
the five-rung mitigation ladder (faircode.ladder) x three model families x
six fairness metrics (faircode.metrics, each with a bootstrap CI and a
permutation p-value), plus the intersectional gap for every pair of declared
protected attributes (faircode.significance.intersectional_report) - and
returns one tidy results table. One code path, same seed, same splits, same
metric definitions, for every domain: a cross-domain comparison is only as
trustworthy as that uniformity, and this module is what makes it literally
true rather than an assertion in a write-up.

Contributors add a dataset + audit.yaml (Layer 1). They never touch this
module.
"""

from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, train_test_split

from .ladder import RUNGS, encode_features, equalize_thresholds, reweigh, rung_features
from .manifest import discover_manifests, load_manifest
from .metrics import METRICS, compute_metrics
from .significance import intersectional_report

MODEL_FAMILIES = {
    "logistic_regression": lambda random_state: LogisticRegression(max_iter=1000, random_state=random_state),
    "random_forest": lambda random_state: RandomForestClassifier(n_estimators=100, random_state=random_state),
    "gradient_boosting": lambda random_state: GradientBoostingClassifier(random_state=random_state),
}


def _load_dataset(manifest):
    df = pd.read_csv(manifest.dataset_path, low_memory=False)
    for row_filter in manifest.row_filters:
        df = row_filter.apply(df)
    df = df.reset_index(drop=True)

    y = manifest.target.compute(df)

    protected_masks = {}
    known_mask = pd.Series(True, index=df.index)
    for pa in manifest.protected_attributes:
        disadv, known = pa.disadvantaged_mask(df)
        protected_masks[pa.name] = disadv
        known_mask &= known

    df = df[known_mask].reset_index(drop=True)
    y = y[known_mask].reset_index(drop=True)
    protected_masks = {
        name: mask[known_mask].reset_index(drop=True) for name, mask in protected_masks.items()
    }
    return df, y, protected_masks


def _run_rung(rung, model_name, manifest, X_all, y, protected_masks, idx_train, idx_test):
    protected_cols = [pa.column for pa in manifest.protected_attributes]
    feature_cols = rung_features(rung, manifest.core_features, manifest.proxy_features, protected_cols)
    X = X_all[feature_cols]
    X_train, X_test = X.iloc[idx_train], X.iloc[idx_test]
    y_train = y.iloc[idx_train].to_numpy()
    y_test = y.iloc[idx_test].to_numpy()

    primary = manifest.protected_attributes[0].name
    disadv_train = protected_masks[primary].iloc[idx_train].to_numpy()

    model = MODEL_FAMILIES[model_name](manifest.random_state)
    if rung == "reweigh":
        model.fit(X_train, y_train, sample_weight=reweigh(y_train, disadv_train))
    else:
        model.fit(X_train, y_train)

    if rung == "threshold_equalized":
        # Out-of-fold probabilities to fit thresholds on - an overfit model's
        # in-sample predict_proba on its own training rows is degenerately
        # confident (clustered near 0/1), which makes the threshold search
        # unstable. cross_val_predict trains a fold-held-out model per split,
        # so these probabilities behave like the test-set ones the fitted
        # thresholds will actually be applied to.
        cv = min(3, int(np.bincount(y_train.astype(int)).min())) if len(np.unique(y_train)) > 1 else 1
        if cv >= 2:
            train_proba = cross_val_predict(
                MODEL_FAMILIES[model_name](manifest.random_state), X_train, y_train,
                cv=cv, method="predict_proba")[:, 1]
        else:
            train_proba = model.predict_proba(X_train)[:, 1]
        test_proba = model.predict_proba(X_test)[:, 1]
        disadv_test = protected_masks[primary].iloc[idx_test].to_numpy()
        y_pred, _ = equalize_thresholds(train_proba, disadv_train, test_proba, disadv_test)
    else:
        y_pred = np.asarray(model.predict(X_test)).astype(int)

    return y_test, y_pred


def run_audit(manifest, n_resamples=2000, n_permutations=2000, random_state=None):
    """Run the full ladder x model x metric grid for one manifest.

    Returns a list of dict rows - one per (rung, model, protected attribute,
    metric), plus one per (rung, model, attribute pair) for the
    intersectional gap when two or more protected attributes are declared.
    """
    rs = manifest.random_state if random_state is None else random_state
    df, y, protected_masks = _load_dataset(manifest)

    protected_cols = [pa.column for pa in manifest.protected_attributes]
    all_cols = list(dict.fromkeys(manifest.core_features + manifest.proxy_features + protected_cols))
    X_all = encode_features(df, all_cols)

    idx_train, idx_test = train_test_split(
        np.arange(len(df)), test_size=manifest.test_size, random_state=rs,
        stratify=y if y.nunique() > 1 else None,
    )

    rows = []
    for rung in RUNGS:
        for model_name in MODEL_FAMILIES:
            y_test, y_pred = _run_rung(
                rung, model_name, manifest, X_all, y, protected_masks, idx_train, idx_test)

            for pa in manifest.protected_attributes:
                disadv_test = protected_masks[pa.name].iloc[idx_test].to_numpy()
                metrics = compute_metrics(
                    y_test, y_pred, disadv_test, n_resamples, n_permutations, random_state=rs)
                for metric_name in METRICS:
                    m = metrics[metric_name]
                    rows.append({
                        "audit": manifest.name, "rung": rung, "model": model_name,
                        "protected_attribute": pa.name, "metric": metric_name, **m,
                    })

            if len(manifest.protected_attributes) >= 2:
                for pa_a, pa_b in itertools.combinations(manifest.protected_attributes, 2):
                    mask_a = protected_masks[pa_a.name].iloc[idx_test].to_numpy()
                    mask_b = protected_masks[pa_b.name].iloc[idx_test].to_numpy()
                    inter = intersectional_report(
                        y_pred, mask_a, mask_b, n_resamples, n_permutations, random_state=rs)
                    isr = inter["intersectional"]
                    rows.append({
                        "audit": manifest.name, "rung": rung, "model": model_name,
                        "protected_attribute": f"{pa_a.name}_x_{pa_b.name}",
                        "metric": "intersectional_demographic_parity_diff",
                        "value": isr["gap"], "ci_low": isr["ci_low"], "ci_high": isr["ci_high"],
                        "p_value": isr["p_value"], "significant": isr["significant"],
                        "n_disadvantaged": isr["n_a"], "n_advantaged": isr["n_b"],
                        "small_sample_warning": isr["small_sample_warning"],
                        "note": "superadditive" if inter["superadditive"] else None,
                    })
    return rows


def run_benchmark(root=".", audits=None, n_resamples=2000, n_permutations=2000):
    """Discover every audit.yaml under root (or use explicit manifest paths)
    and run them all. Returns one tidy pandas.DataFrame across every audit."""
    paths = [Path(a) for a in audits] if audits else discover_manifests(root)
    all_rows = []
    for path in paths:
        manifest = load_manifest(path)
        all_rows.extend(run_audit(manifest, n_resamples, n_permutations))
    return pd.DataFrame(all_rows)


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    """One row per (audit, rung, protected_attribute, metric): the point
    estimate averaged across the three model families, plus how many of
    them found the gap statistically significant."""
    if results.empty:
        return results
    return (
        results.groupby(["audit", "rung", "protected_attribute", "metric"], as_index=False)
        .agg(mean_value=("value", "mean"),
             n_models_significant=("significant", "sum"),
             n_models=("model", "count"))
    )


def plot_ladder(results: pd.DataFrame, audit: str, out_path,
               metric: str = "demographic_parity_diff"):
    """Bar chart of `metric`'s point estimate across the five ladder rungs
    (averaged across model families) for one audit. Requires matplotlib,
    which is an optional extra (`pip install faircode[benchmark]`)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    subset = results[(results["audit"] == audit) & (results["metric"] == metric)]
    if subset.empty:
        raise ValueError(f"no rows for audit={audit!r} metric={metric!r}")

    grouped = subset.groupby("rung")["value"].mean().reindex(RUNGS)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(grouped.index, grouped.to_numpy(), color="#4C72B0")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title(f"{audit}: {metric.replace('_', ' ')} across the mitigation ladder")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def write_report(results: pd.DataFrame, out_dir, make_plots: bool = True,
                 plot_metric: str = "demographic_parity_diff"):
    """Write results.csv (full tidy table) and summary.csv (per-model-family
    average) to out_dir, plus one <audit>_ladder.png per audit if make_plots."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(out_dir / "results.csv", index=False)
    summarize(results).to_csv(out_dir / "summary.csv", index=False)
    if make_plots and not results.empty:
        for audit in results["audit"].unique():
            plot_ladder(results, audit, out_dir / f"{audit}_ladder.png", metric=plot_metric)
    return out_dir
