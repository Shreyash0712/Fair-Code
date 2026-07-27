# CLAUDE.md — Standing Instructions

> Read this before making **any** change to this repo. It applies to AI agents and human contributors alike.

## 🔒 PAPER FREEZE — active

The benchmark results in this repo are cited in a research paper currently in **peer review**.
The paper quotes exact numbers frozen at:

- **Tag:** `v1.0-paper`
- **Commit:** `bbef2ba` (the commit the `v1.0-paper` tag points to; provenance/code state recorded in `paper/results-frozen/MANIFEST.md` is `2fa4a66`, whose code is identical and reproduces these numbers)

**Nothing that affects the benchmark results may change until the paper is published.**
Any drift makes the paper's tables disagree with the repo — a reviewer will catch it.
The **analysis side is frozen**; the **educational side stays fully active** (see §5).

---

## 1. DO NOT TOUCH

- **`paper/results-frozen/`** — the paper's evidence. **Never** modify, for any reason.
- **`results/`** — `results_fairness.csv`, `results_performance.csv`, `summary.csv`, `figures/`.
- **`faircode/`** core: `benchmark.py`, `metrics.py`, `strategies.py`, `models.py`, `manifest.py`, `loaders.py`, `significance.py`, `figures.py`.
- **Any `audit.yaml`** manifest in any audit folder.
- **Any dataset CSV** in any audit folder.
- **The `v1.0-paper` tag.**

## 2. Parameters that MUST NOT change

Changing any of these changes the published numbers:

- `random_state = 42` (models, split, bootstrap, permutations)
- `test_size = 0.2`, **stratified** split
- `EXPONENTIATED_GRADIENT_MAX_ITER = 50`
- The fairness constraint (**DemographicParity**)
- The **six** fairness metrics and their definitions
- Bootstrap resample count / permutation count
- Any `row_filters` or `target` spec in a manifest

## 3. NO NEW AUDITS on main (but contributors stay welcome)

The paper states it covers **exactly seven domains**, so new audits **must not be merged into main** during the freeze.

- Thank the contributor — this is a **timing hold, not a rejection**.
- Park the audit on a branch (e.g. `pending-audits/<name>`), **or** leave the PR open labeled `post-paper`.
- Merge after publication.

## 4. Do not change results claims in README

The README's results wording and numbers are aligned to the paper.
Prose may be **clarified**, but the **reported numbers** and the **interpretation of S1–S4** must not change.

## 5. STILL ALLOWED — active work

- New explainers in `explainers/` as `.md` files (conceptual AI/ML explanations)
- Website content and JSON entries
- Documentation, README prose, `CONTRIBUTING.md`, `CHANGELOG.md`
- Typo and clarity fixes in prose
- Social media caption files

**Caveat:** if an explainer quotes any Fair Code result, it must use the frozen numbers from
`paper/results-frozen` — never re-run its own.

## 6. Escape hatch — found a bug in the analysis code?

**Do NOT silently fix it.** Flag it instead.
A fix may require re-running the benchmark, re-freezing, and correcting the paper.
Quietly fixing it is **worse than the bug**.

## 7. When the freeze lifts (paper published)

- New audits may merge; the benchmark may be re-run.
- **`paper/results-frozen/` stays permanently untouched** as the historical record for the published paper.
- Add the paper citation and DOI to `README.md` and `CITATION.cff`.
