"""Renders the paper figures - Layer 2 of the benchmark harness.

Reads results_fairness.csv (written by faircode.benchmark) from disk and
renders one 300-dpi PNG per audit into <results_dir>/figures/: the chosen
fairness metric's point estimate (averaged across the three model families)
across the five mitigation strategies. This module never re-runs a model -
it only visualizes what benchmark.py already computed, so re-plotting with a
different metric doesn't require re-running the harness.

Requires matplotlib, the optional 'benchmark' extra
(`pip install faircode[benchmark]`).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .strategies import STRATEGIES

FIGURE_DPI = 300


def plot_strategy_comparison(fairness_df: pd.DataFrame, audit: str, out_path,
                             metric: str = "demographic_parity_diff"):
    """Bar chart of `metric`'s point estimate across the five mitigation
    strategies (averaged across model families) for one audit."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    subset = fairness_df[(fairness_df["audit"] == audit) & (fairness_df["metric"] == metric)]
    if subset.empty:
        raise ValueError(f"no rows for audit={audit!r} metric={metric!r}")

    grouped = subset.groupby("strategy")["value"].mean().reindex(STRATEGIES)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(grouped.index, grouped.to_numpy(), color="#4C72B0")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title(f"{audit}: {metric.replace('_', ' ')} across mitigation strategies")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(out_path, dpi=FIGURE_DPI)
    plt.close(fig)


def generate_figures(results_dir, figures_dir=None, metric: str = "demographic_parity_diff"):
    """Read results_fairness.csv from results_dir and write one
    <audit>_strategies.png per audit into figures_dir (default:
    <results_dir>/figures/)."""
    results_dir = Path(results_dir)
    figures_dir = Path(figures_dir) if figures_dir else results_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    fairness_df = pd.read_csv(results_dir / "results_fairness.csv")
    for audit in fairness_df["audit"].unique():
        plot_strategy_comparison(
            fairness_df, audit, figures_dir / f"{audit}_strategies.png", metric=metric)
    return figures_dir


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(
        prog="faircode-figures",
        description="Render paper figures from a benchmark results directory.")
    parser.add_argument("results_dir", nargs="?", default="results",
                       help="directory containing results_fairness.csv (default: results)")
    parser.add_argument("--metric", default="demographic_parity_diff",
                       help="fairness metric to plot (default: demographic_parity_diff)")
    args = parser.parse_args(argv)

    figures_dir = generate_figures(args.results_dir, metric=args.metric)
    print(f"Figures written to {figures_dir}/")


if __name__ == "__main__":
    main()
