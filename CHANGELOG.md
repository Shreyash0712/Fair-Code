<div align="center">

# Changelog

![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-e05735?style=flat-square)
![SemVer](https://img.shields.io/badge/SemVer-2.0.0-blue?style=flat-square)
![Latest](https://img.shields.io/badge/Latest-v1.3.1-brightgreen?style=flat-square)

All notable changes to Fair Code are documented here, newest first.

</div>

---

## [1.3.1] - 14 Jul 2026
### Added
- Explainer: What Is Unsupervised Learning? - `unsupervised-learning.md` created (contributed by @AnayDhawan, #35/#74), added to `index.html`, `README.md`, and `CONTRIBUTING.md`
  - Full explainer on learning structure from unlabelled data: with no `y` to score against, a clustering algorithm has no concept of protected groups, yet can still sort people along demographic lines as a side effect of the features it is given
  - Real-world proof anchored to Audit 04 (Benefits Denial): running k-means (`k=2`) on the UCI Adult Census file with `sex`, `race`, and `native.country` excluded from the feature set still recovers a strong sex split (one cluster 89.3% male) and a real race split (Black applicants at more than 2x the rate between clusters). National origin is kept as an honest counterexample - it lands at essentially the same rate in both clusters (10.2% vs 10.7%) - rather than overclaiming
  - Detection code: `cluster_without_protected_attributes()` and `check_cluster_demographic_skew()` - k-means on a deliberately protected-attribute-free feature set, paired with a post-hoc crosstab of cluster assignment against each protected attribute
  - Four numbered limitations (no ground truth to evaluate against, `k` and distance metric as assumptions, disparate impact harder to audit without labels, dimensionality reduction erasing the very signal an audit needs), cross-links to proxy-variables, proxy-entanglement, ml-bias, and supervised-learning, and three further reading citations (ProPublica mortgage-algorithm investigation, Chierichetti et al. 2017 Fair Clustering, Barocas, Hardt & Narayanan)
  - Roadmap item added on the website
- Explainer: What Is Model Drift? - `model-drift.md` created (contributed by @AnayDhawan, #36/#75), added to `index.html`, `README.md`, and `CONTRIBUTING.md`
  - Full explainer on the operational, over-time side of distribution shift: a model that clears a bias audit at launch can drift back into an unfair state while sitting still, with no code change, no retraining, and no alert, unless someone monitors it. Distinguishes data drift (`P(X)` moves) from concept drift (`P(Y|X)` moves) because they need different fixes
  - Scoped explicitly against the existing `distribution-shift.md`: that explainer covers the one-shot reference-vs-current taxonomy (covariate/label/concept) with a single KS/chi-squared test; this one covers ongoing rolling-window monitoring of an already-deployed model
  - Real-world proof anchored to Audit 03 (German Credit Lending): re-measuring the age fairness gap across five sequential 200-row windows shows it swinging from 4.3% to 15.1%, versus the audit's single 6.39% snapshot - the instability a rolling view catches and a one-shot audit cannot. PSI on three features flags `credit_amount` (0.119) as the feature that moved most, ahead of `age` (0.096)
  - Detection code: `population_stability_index()`, `page_hinkley_test()` (change-point detection), and `rolling_fairness_gap()` - numpy/pandas, no new dependencies
  - Five numbered limitations (row order is not real time, data vs concept drift need different fixes, monitoring infrastructure is the real bottleneck, threshold choices are judgment calls, small windows inflate both PSI and the gap), cross-links to distribution-shift, feedback-loop-bias, and supervised-learning, and three further reading citations (Roberts et al. 2021, Gama et al. 2014, Page 1954)
  - Roadmap item added on the website
### Changed
- `README.md`: `unsupervised-learning.md` and `model-drift.md` added to the explainers table, repository structure tree, and What's Next checklist; Traction explainer count updated to 28
- `CONTRIBUTING.md`: both explainers added to the existing explainers table
- `assets/explainers-data.js`: both explainers added so the website's Explainers grid, search, and count pick them up
- `METRICS.md`: explainer count updated to 28
- `CITATION.cff`: version `1.3.0` → `1.3.1`; release date updated to 2026-07-14

---

## [1.3.0] - 13 Jul 2026
### Added
- Audit 07 - Tenant Screening / Rental Application Bias (#68) - a new domain (housing) auditing the criminal-history / recidivism-risk scores that real tenant-screening products (CoreLogic, TransUnion SmartMove, RealPage) sell to landlords as a risk flag on rental applicants
  - **Dataset: [`Tenant Screening/tenant-screening-data.csv`](Tenant%20Screening/)** - NIJ's Recidivism Challenge Full Dataset (Georgia Dept. of Community Supervision, 25,835 records, public domain via DOJ/NIJ). A reframed source: there is no clean public per-applicant screening dataset, so the audit treats `Recidivism_Within_3years` as the risk flag a background-check algorithm hands a landlord. Rows where the original challenge withheld the label are filtered out before training. Dataset choice and reframing rationale posted on issue #68 per CONTRIBUTING §1
  - **Protected attribute: Race** (Black vs White) - single-attribute audit, so no intersectional report per CONTRIBUTING
  - **`Tenant Screening/unfair.py` / `fair.py`** - Random Forest (`n_estimators=100`, `random_state=42`, 80/20 split), gap reported with `significance_report`. Twelve proxies dropped in `fair.py`: `Prior_Arrest_Episodes_{Felony,Violent,Property,Drug,GunCharges}`, the matching `Prior_Conviction_Episodes_*` fields, `Gang_Affiliated` (criminal record as a proxy for race), and `Residence_Changes` (housing instability standing in for eviction history). All twelve differ by race at chi-squared p far below 0.05
  - **Result: race gap 7.17% → 5.07% (29% reduction).** The residual gap stays statistically significant (p=0.0007) - the honest finding: the bias lives in the label itself (re-arrest is a policed quantity), so no feature removal fully closes it
  - **Notebook: [`07_tenant_screening_bias_audit.ipynb`](notebooks/07_tenant_screening_bias_audit.ipynb)** - the standard 8-section walkthrough, including a chi-squared proxy analysis with crosstab output. Docs site (`index.html`) gains a Project 07 card, nav + ticker entries, and a Housing filter; `ROADMAP.md` Phase 3 lists it as published
- Intersectional bias analysis - auditing two protected attributes at once, so the doubly-disadvantaged group at their intersection is measured directly instead of being averaged away into each single-axis gap (closes the roadmap's last open Phase 5 item)
  - **`intersectional_report()` in [`faircode/significance.py`](faircode/significance.py)** - takes an outcome and two boolean masks (each marking the disadvantaged side of one attribute), splits the population into the four `mask_a × mask_b` quadrants, and compares the doubly-disadvantaged cell against the baseline cell with the same bootstrap CI + permutation p-value the single-axis audits already use. Also returns each attribute's marginal gap (what it would report on its own), a `superadditive` flag (true when the compounded gap exceeds the sum of the two marginals), and per-quadrant rates/sizes so a thin intersection cell is visible before the small-sample warning fires. Pure numpy/pandas, no new dependencies
  - **Wired into the three audits that already track 2+ protected attributes**, as a new printed block after the existing single-attribute output in both `unfair.py` and `fair.py`: Insurance Denial (age × sex), Benefits Denial (sex × race), Healthcare Readmission (sex × race). COMPAS, AI Fair Recruitment, and German Credit Lending track one attribute each and are unchanged - there is nothing to cross
  - **Notebook: [`07_intersectional_bias_audit.ipynb`](notebooks/07_intersectional_bias_audit.ipynb)** - explains what intersectionality means (Crenshaw 1989) and why marginal fairness gaps can hide a worse compounded one, then runs `intersectional_report` on the biased vs. mitigated models for all three pairs. Finding: proxy removal closes the intersectional gap roughly in step with the marginals for Benefits and Healthcare, but for Insurance the marginal age/sex gaps shrink while the young-women gap does not, tipping the mitigated model into superadditive territory - the harm a marginal-only audit could not surface
  - Three new tests in `tests/test_significance.py` (additive → not superadditive, superadditive → flagged and significant, small doubly-disadvantaged cell → warning) - 50 significance tests passing
### Changed
- `README.md`: methodology note that audits tracking 2+ protected attributes also report an intersectional (combined) gap, linking notebook 07
- `ROADMAP.md`: Phase 5 "Intersectional bias notebook" item marked complete
- `CONTRIBUTING.md`: audit-script template now asks audits tracking 2+ attributes to report at least one intersectional pair with `intersectional_report`, following the three wired audits
- `CITATION.cff`: version `1.2.0` → `1.3.0`; release date updated to 2026-07-13; abstract extended to cover intersectional bias analysis

---

## [1.2.5] - 13 Jul 2026
### Added
- Open Dataset Profiler - a wave of six enhancements, all sharing one spec ([`faircode/SPEC.md`](faircode/SPEC.md)) so CLI and web stay bit-for-bit identical
  - **Two-dataset comparison for representation drift** (#60) - `faircode compare A.csv B.csv` and side-by-side A/B dropzones in the web profiler. Reports per-dimension drift with the Population Stability Index (PSI), Total Variation Distance, per-group share shifts, and appeared/disappeared groups; flags significant drift and overall-score drops. New `faircode/compare.py`, `assets/profiler-compare.js`, SPEC §8, `tests/test_compare.py`
  - **Manual column mapping** (#62) - override auto-detection when a column is oddly named (`gndr`, `patient_region_code`). `faircode profile --map COL=KIND` (repeatable) and editable per-column dropdowns in the web profiler that re-run the audit in place. Forced columns are exempt from the high-cardinality drop. SPEC §1
  - **Reference-population baseline** (#56) - score a dataset against an external population (e.g. Census age×sex), not just internal balance. `faircode profile --reference baseline.csv` and a web upload; surfaces per-group expected-vs-actual deltas, a deviation metric, and under-representation-vs-reference flags. SPEC §9
  - **Choosable intersection pair** (#58) - cross any two demographic columns, not just the first two detected. `faircode profile --cross colA,colB` and two dropdowns in the web profiler. SPEC §4
  - **Chi-squared proxy hints** (#61) - opt-in `faircode profile --proxy-hints` flags strongly-associated column pairs (a "this may be a proxy for that protected attribute" signal) with p-values and Cramér's V. Python/CLI-only via the optional `scipy` extra; never affects the score, so the two engines stay in sync. New `faircode/proxy.py`, `tests/test_proxy.py`
  - **Tunable thresholds** (#63) - `--min-share`, `--intersection-floor`, `--imbalance-flag`, `--missing-flag` on the CLI, threaded through `profile(df, opts=...)` and the JS engine. SPEC §7
### Changed
- `faircode/profiler.py`: `profile()` gains an `opts` argument (thresholds, `cross`, `reference`) plus a `parse_reference()` helper; `detect_columns()`/`profile()` gain manual overrides
- `assets/profiler-engine.js`: mirrors the new `opts`, `parseReference`, and `compare` surface (verified bit-for-bit against the Python CLI)
- `assets/profiler-ui.js`, `profiler.html`, `assets/profiler.css`: column-mapping panel, cross-dimension selectors, and reference-baseline controls
- `pyproject.toml`: new optional `proxy` extra (`scipy`)
- `README.md`, `ROADMAP.md`: Open Dataset Profiler capabilities and Phase 5 status updated

---

## [1.2.4] - 12 Jul 2026
### Changed
- Live site domain moved from `fair-code-five.vercel.app` to **[thefaircode.xyz](https://www.thefaircode.xyz)**
  - `README.md`: live-website link, repository-structure comment, Open Dataset Profiler section, and Website section updated to the new domain
  - `SECURITY.md`: website-vulnerability scope link updated
  - `CITATION.cff`: `url` field updated
  - `pyproject.toml`: `project.urls.Website` updated
  - `.github/workflows/first.interaction.yml`: first-issue greeting link updated

---

## [1.2.3] - 12 Jul 2026
### Added
- Explainer: What Is Supervised Learning? - `supervised-learning.md` created, added to `index.html`, `README.md`, and `CONTRIBUTING.md`
  - Full explainer covering the input-label-mapping mechanism behind every audit in this repo: features and a ground-truth label go in, a fitted model that generalises to unseen inputs comes out
  - Walks through `train_test_split` and `model.fit()` in the AI Fair Recruitment audit's `unfair.py` directly, showing the learning step has no way to distinguish a legitimate pattern from a discriminatory one
  - Real-world proof anchored to Audit 02 (AI Fair Recruitment): the published 4.51% gender hiring gap collapsing to 0.12% (97.3% reduction) once gender and age are dropped from the feature set, with German Credit Lending (Audit 03) referenced as a second supervised task with a different label type
  - Detection code: `train_supervised_classifier()` and `compare_label_vs_prediction_gap()` - pandas/scikit-learn training on labeled data plus a group-wise comparison of the label gap against the prediction gap on held-out rows
  - Four numbered limitations (label as proxy for the real target, matching labels not implying fairness, mapping expiry under population shift, generalisation assuming the future resembles the past), cross-links to label-bias, ml-bias, distribution-shift, and calibration, and three further reading citations (Hastie, Tibshirani & Friedman; Barocas, Hardt & Narayanan; Mehrabi et al. 2021)
  - Nav dropdown (desktop + mobile), ticker strips, and roadmap updated on website
### Changed
- `README.md`: `supervised-learning.md` added to explainers table, repository structure tree, and What's Next checklist
- `CONTRIBUTING.md`: `supervised-learning.md` added to existing explainers table

---

## [1.2.2] - 10 Jul 2026
### Added
- Explainer: False Positives vs. False Negatives in Medical Risk Models - `false-positives-vs-false-negatives.md` created, added to `index.html`, `README.md`, and `CONTRIBUTING.md`
  - Full explainer covering the false positive / false negative trade-off at a model's decision threshold, and why asymmetric clinical costs (a missed diagnosis vs. a false alarm) make this trade-off higher-stakes in medical risk models than elsewhere
  - Comparison table contrasting false positives and false negatives by immediate cost, downstream cost, and who absorbs each
  - Real-world proof anchored to Audit 06 (Healthcare Readmission): its published demographic parity gaps (race 0.08% to 0.06%, age 0.28% to 0.09%), paired with Obermeyer et al.'s 2019 finding that correcting a cost-as-proxy-for-illness algorithm would raise the share of Black patients identified for extra care from 17.7% to 46.5%
  - Detection code: `error_rate_gaps()` and `cost_weighted_threshold()` - pandas/scikit-learn group-wise FPR/FNR computation and a cost-weighted threshold sweep
  - Four numbered limitations (cost-ratio value judgments, per-group threshold vs. disparate treatment, small-subgroup FPR/FNR noise, equal error rates not guaranteeing equal outcomes), cross-links to equalized-odds, calibration, predictive-parity, and disparate-treatment, and three further reading citations (Obermeyer et al. 2019, Rajkomar et al. 2018, Chouldechova 2017)
  - Nav dropdown (desktop + mobile), ticker strips, and roadmap updated on website
### Changed
- `README.md`: `false-positives-vs-false-negatives.md` added to explainers table, repository structure tree, and What's Next checklist; corresponding item in the Healthcare AI Bias Focus "Upcoming" list replaced with a link to the published explainer; Traction explainer count updated to 24
- `CONTRIBUTING.md`: `false-positives-vs-false-negatives.md` added to existing explainers table

---

## [1.2.1] - 6 Jul 2026
### Added
- Explainer: Predictive Parity - `predictive-parity.md` created (contributed by @propcgamer20-png), added to `index.html`, `README.md`, and `CONTRIBUTING.md`
  - Full explainer covering predictive parity as a sufficiency metric: Positive Predictive Value equal across groups, and why that is a fundamentally different fairness check than error-rate parity
  - Comparison table across Demographic Parity, Equalized Odds, and Predictive Parity by what each conditions on
  - Real-world proof anchored to Audit 01 (COMPAS): the 2016 ProPublica vs Northpointe dispute, where ProPublica's error-rate reading found a roughly 2x false-positive gap for Black defendants while Northpointe's predictive-parity reading found PPV close across race, and Chouldechova's proof for why both readings can be correct at once
  - Detection code: `predictive_parity_gap()` and `base_rate_gap()` - pandas group-wise PPV and base-rate computation, paired to surface the Chouldechova trade-off signature
  - Four numbered limitations (impossibility with Equalized Odds under unequal base rates, uneven harm despite equal PPV, small-subgroup PPV noise, threshold-tuning blind spot), cross-links to equalized-odds, demographic-parity, disparate-impact, and fairness-metric-conflicts, and three further reading citations (Angwin et al. 2016, Chouldechova 2017, Kleinberg et al. 2017)
  - Nav dropdown (desktop + mobile), ticker strips, and roadmap updated on website
### Changed
- `README.md`: `predictive-parity.md` added to explainers table, repository structure tree, and What's Next checklist
- `CONTRIBUTING.md`: `predictive-parity.md` added to existing explainers table

---

<details>
<summary><strong>Older releases (v1.2.0 and earlier)</strong> - click to expand</summary>

## [1.2.0] - "Open Tools & Causal Foundations" - 30 Jun 2026

First release since **v1.1.0** (9 Jun 2026). The headline is the **Open Dataset Profiler** - Fair Code's first interactive, bring-your-own-data tool, turning the project from a showcase of six fixed audits into something visitors run on their own CSVs. This release also bundles the six explainers shipped between v1.1.0 and now, which deepen the causal and statistical foundations behind the audits.

### Added - Open Dataset Profiler (CLI + web)
- **`faircode/` Python package + CLI** - the diagnostic counterpart to the audits: instead of measuring a *model's* prediction gap, it audits a *dataset's* demographic representation **before any model is trained** (no model, no train/test split, no proxy removal). `pip install -e .` exposes a `faircode profile <csv>` command with terminal, `--json`, and `--html` output.
  - Detects demographic columns (sex, race, age, geography) by tokenized, prefix-aware name matching; computes per-dimension metrics - subgroup shares, an entropy-based balance score (0–100) with A–F grade, imbalance ratio, under-represented groups (<5%), missing-data %, numeric-age skewness, and intersectional gaps - all defined once in `faircode/SPEC.md`
  - Pure **pandas**; deliberately **does not depend on `ydata-profiling`** (a heavy, general-purpose profiler) - only a thin, fairness-specific slice is needed, so the metrics are computed directly
  - Domain-agnostic: validated on health (`insurance.csv`, `diabetic_data.csv`) and non-health (`adult.csv`, COMPAS) datasets; correctly handles numeric ages, `[70-80)`-style interval ages, and drops date-of-birth/identifier columns
- **`profiler.html` - client-side web tool** - drop in a CSV (or hit "Try a sample") and get an instant representation audit in the browser. **The file never leaves the visitor's machine** - no upload, no backend - which matters for health data. Built in the "Audit Ledger" design system: score ring, per-dimension bar charts (green = balanced, red = under-represented), flags list, and intersectional gaps; light/dark theme; a `?demo` deep-link auto-loads the sample dataset
- **`assets/profiler-engine.js`** - a JavaScript port of the Python engine, **verified bit-for-bit identical** to the CLI across every bundled dataset (same scores, dimensions, flags) by sharing the `faircode/SPEC.md` spec
- **Tests + CI** - `tests/test_profiler.py` (14 tests) and a dedicated `profiler` job in `.github/workflows/audits.yml` that runs the tests and smoke-tests the CLI on every push and PR
- Wired into the site: a **Profiler** nav link and a feature callout on `index.html`

### Added - Explainers (shipped since v1.1.0)
- **What Is Machine Learning Bias?** - `ml-bias.md`: the four entry points through which bias enters a model (training data, labels, proxies, feedback loops); detection via `demographic_parity_report()` and `check_proxy()`; anchored to COMPAS *(prev. 1.1.1)*
- **What Is Data Leakage?** - `data-leakage.md`: target leakage vs. train-test contamination; `detect_target_leakage()` and `check_preprocessing_leakage()`; anchored to COMPAS `CustodyStatus` *(prev. 1.1.2)*
- **How AI Detects Patterns** - `how-ai-detects-patterns.md`: Random Forest splitting, aggregation, and feature importance, and why the model can't tell a causal pattern from a discriminatory one; `get_pattern_reliance()` and `flag_correlated_patterns()` *(prev. 1.1.3)*
- **What Is Distribution Shift?** - `distribution-shift.md`: covariate / label / concept drift and why a one-time fairness audit expires; `detect_covariate_shift()` (KS + chi-squared) and `detect_label_shift()` *(prev. 1.1.4)*
- **The Biggest Myth About AI Objectivity** - `ai-objectivity-myth.md`: why "it's just math" fails once a model is trained on biased history; `audit_objectivity_claim()` and `find_features_explaining_gap()`; anchored to COMPAS *(prev. 1.1.5)*
- **What Is a Confounding Variable?** - `confounding-variable.md`: how a hidden third variable creates spurious associations that survive protected-attribute removal, and confounder vs. proxy vs. collider; `check_confounding()`; anchored to COMPAS *(prev. 1.1.6)*
- Each explainer ships with a full write-up, detection code, numbered limitations, cross-links, and further reading, and was added to `index.html` (nav dropdown, ticker strips, roadmap), `README.md`, and `CONTRIBUTING.md`

### Added - Tooling
- `pyproject.toml` - packages the `faircode` console script (single dependency: pandas)

### Changed
- `README.md`: six new explainers added to the explainers table, repository-structure tree, and What's Next checklist (total: 23 explainers); new **Open Dataset Profiler** section and Contents entry; "Fairness audit web dashboard" and `faircode/` module boxes checked
- `ROADMAP.md`: Phase 5 - "Fairness audit web dashboard" and "Bias detection utility library (`faircode/` module)" marked complete, pointing to the Profiler
- `CONTRIBUTING.md`: six new explainers added to the explainers table
- `CITATION.cff`: version `1.0.0` → `1.2.0`; release date updated to 2026-06-30; abstract extended to cover welfare-eligibility audits and the dataset profiler
- `METRICS.md`: explainer count corrected to 23; week 2026-W27 snapshot noting the Profiler release
- `.gitignore`: ignores Python build/cache artifacts (`__pycache__/`, `*.egg-info/`, `build/`, `dist/`, `.pytest_cache/`)

---

## [1.0.5] - 9 Jun 2026
### Added
- Explainer: Proxy Entanglement - `proxy-entanglement.md` created (PR #49, commits 475de938, 64a90772), added to `index.html`, `README.md`, and `CONTRIBUTING.md` (commits c018d8e8, 476a2771, 46d534fa)
  - Full explainer covering proxy entanglement as the failure mode where multiple correlated features encode the same protected signal through independent administrative channels, requiring cluster-level removal rather than one-variable-at-a-time removal
  - Real-world proof anchored to Audit 06 (Healthcare Readmission): `payer_code` (Medicaid rate encodes race: Hispanic 9.0%, AfricanAmerican 5.5%, Caucasian 2.7%), `discharge_disposition_id` (SNF access: Caucasian 17.3% vs AfricanAmerican 10.7%), `medical_specialty` (insurance access and geography), and `number_inpatient` (prior hospitalisation count: AfricanAmerican 0.70 vs Asian 0.48) identified as an entangled cluster sharing a common causal root in structural inequality
  - Results: removing the full cluster produces 25% reduction in race gap and 68% reduction in age gap; single-variable removal leaves most of the bias mechanism intact
  - `detect_proxy_entanglement()` detection code: two-pass chi-squared analysis - each candidate proxy tested against the protected attribute first, then confirmed proxies cross-tested against each other to surface the entangled cluster
  - Entangled cluster table (feature → what it encodes → causal root), limitations table (causal root ambiguity, accuracy trade-off, base-rate sensitivity in large datasets, distinction from multicollinearity), takeaway callout, and three further reading links (Obermeyer et al. *Science* 2019, Chiappa & Isaac 2019, Kilbertus et al. 2017)
  - Nav dropdown (desktop + mobile), ticker strips (original and dupe), roadmap, AI Hallucinates footer pills, and RL roadmap item (previously live but missing from roadmap) updated on website
### Changed
- `README.md`: `proxy-entanglement.md` added to explainers table, repository structure tree, and What's Next checklist (commit c018d8e8)
- `CONTRIBUTING.md`: `proxy-entanglement.md` added to existing explainers table (commit 476a2771)

---

## [1.0.4] - 8 Jun 2026
### Added
- Audit 06: Healthcare Readmission - Clinical Bias (Diabetes 130-US Hospitals 1999–2008, 101,766 records)
  - `fair.py` and `unfair.py` added to `Healthcare Readmission/` (commits ba226003, cec4a098)
  - Jupyter notebook: `06_healthcare_readmission_bias_audit.ipynb` (commit 9a8abd07)
  - Protected attributes audited: race, gender, age
  - Proxy variables identified and removed: `payer_code` (Medicaid rate encodes race: Hispanic 9.0%, AfricanAmerican 5.5%, Caucasian 2.7%), `discharge_disposition_id` (SNF access encodes insurance and geography: Caucasian 17.3% vs AfricanAmerican 10.7%), `medical_specialty` (encodes insurance type and geography), `number_inpatient` (prior hospitalisation count encodes preventive care access gap: AfricanAmerican 0.70 vs Asian 0.48)
  - Results: race gap 0.08% → 0.06% (25% reduction), age gap 0.28% → 0.09% (68% reduction), gender gap 0.02% → 0.04% (increased - proxy variables carried no meaningful gender signal; documented honestly)
  - Healthcare Readmission audit added to CI workflow (commit 60b4aa7f)
  - `index.html` updated: project card added with terminal outputs, bias bars, and key insight; desktop and mobile nav updated with `06 - Healthcare Readmission` link (commit d93fd1cf)
### Changed
- `README.md` and `CONTRIBUTING.md` updated: audit 06 added to results table, repository structure tree, projects section, and What's Next checklist (commits eced8281, 3d6f4ead)
- `.gitignore` updated to prevent `.DS_Store` from being committed (commit a175c40c)

---

## [1.0.3] - 7 Jun 2026
### Added
- Explainer: Reinforcement Learning - `reinforcement-learning.md` created by evanjain-dot (PR #48, commit a785ea95), added to `index.html`, `README.md`, and `CONTRIBUTING.md` (commit e3928af7)
  - Full explainer covering the three-part RL loop (state → action → reward → policy), reward function design as a political act, reward hacking, and the credit assignment problem
  - Real-world proof using COMPAS as an RL-adjacent system: biased policy produces 86.77% Black/White fairness gap; removing race + `CustodyStatus` proxy reduces gap to 15.69% (71% reduction)
  - Results table: biased policy vs. race-only removal vs. race + proxy removal
  - Second case: YouTube recommendation engine using watch time as reward signal - documents asymmetric demographic consequences and outrage optimisation
  - `fairness_gap()` detection code with chi-squared proxy check for state representation audit
  - Limitations table: reward misspecification, credit assignment failure, proxy exploitation, political nature of reward asymmetry
  - Further reading: Dressel & Farid (Science Advances, 2018), Sutton & Barto (MIT Press, 2018), Krakovna et al. DeepMind specification gaming catalogue (2020)
  - Nav dropdown (desktop + mobile), ticker, and AI Hallucinates footer pills updated on website
### Changed
- `README.md`: `reinforcement-learning.md` added to explainers table, repository structure tree, and What's Next checklist
- `CONTRIBUTING.md`: `reinforcement-learning.md` added to existing explainers table, folder structure tree, and blocked concepts list
- `.github/workflows/update-changelog.yml` deleted - Dependabot auto-changelog workflow removed (commit d4f1c0bb, PR #47)
- `README.md`: `update-changelog.yml` description removed (commit 63edce9a)
- PR template refined for improved contributor guidance (commit e611e442)

---

## [1.0.2] - 5–6 Jun 2026
### Added
- Explainer: Why AI Hallucinates - `ai-hallucinations.md` created by Shreyash0712 (PR #43), added to `index.html`, `README.md`, and `CONTRIBUTING.md` (commits 928ae7ae, 68c4de61, 46cd32e8)
  - Full explainer covering hallucination as out-of-distribution confidence failure, real-world proof using the Insurance Denial audit (sparse BMI/smoking/diabetic sub-populations), tabular density vs. confidence table, `audit_hallucination_risk()` detection code, four mitigation patterns (retrieval-first, source grounding, adversarial verification, confidence calibration), and limitations (confabulation vs. extrinsic vs. intrinsic hallucination taxonomy, RAG limitations, RLHF over-conservatism)
  - Legally documented real-world case: *Mata v. Avianca, Inc.* (678 F.Supp.3d 443) - ChatGPT-fabricated court citations resulting in federal sanctions
  - Nav dropdown (desktop + mobile), ticker, roadmap, and explainer footer pills updated on website
- Branch protection rules documented in `CONTRIBUTING.md`: PRs required, CI must pass, force pushes blocked, branch deletion restricted (commit 6574b20b)
- First interaction workflow added for issues and PRs (commit 60874af6)
- Dependabot configuration added for Python packages with daily changelog updates (commits fa519387, 82f6b262, 9301061c)
### Changed
- `README.md`: `ai-hallucinations.md` added to explainers table, repository structure tree, and What's Next checklist; dataset structure section refactored (commits 9a0eab2e, 6574b20b)
- `CONTRIBUTING.md`: `ai-hallucinations.md` added to existing explainers table, folder structure tree, and blocked concepts list; branch protection steps documented
- Dependencies bumped by Dependabot: `scikit-learn` ≥ 1.9.0 (PR #41, commit d8c6f9b4), `numpy` ≥ 2.4.6 (PR #39, commit 98efd433), `pandas` ≥ 3.0.3 (PR #38, commit 01e747f5), `matplotlib` ≥ 3.10.9 (PR #37, commit 3fd010cb)

---

## [1.0.1] - 4 Jun 2026
### Added
- Explainer: What Happens Inside a Neural Network - `neural-networks.md` created, added to `index.html`, `README.md`, and `CONTRIBUTING.md` (commits 4ff97866, c1023432, d372c002, f997fc52)
  - Full explainer covering forward pass, weights, loss function, backpropagation, and the three-part training loop
  - Real-world proof using the AI Fair Recruitment dataset: 20.9% → 0.1% gender gap after removing gender + age proxy
  - SHAP inspection code, what-each-component-does table, limitations table, and further reading
  - Nav dropdown (desktop + mobile), ticker, roadmap, and counterfactual fairness footer pills updated on website
### Changed
- `README.md`: neural-networks.md added to explainers table, repository structure tree, and What's Next checklist
- `CONTRIBUTING.md`: neural-networks.md added to existing explainers table, folder structure tree, and blocked concepts list

---

## [0.8.1] - 2 Jun 2026
### Added
- Explainer: Counterfactual Fairness - `counterfactual-fairness.md` created by evanjain-dot (PR #31), added to `index.html`, `README.md`, and `CONTRIBUTING.md`
  - Full explainer with SCM formal definition, COMPAS policing causal chain proof, detection code (biased model → counterfactual audit → fair model fix), IF vs CF comparison table, limitations, and further reading
  - Nav dropdown, mobile nav, and roadmap updated on website
### Changed
- `README.md` updated: counterfactual fairness added to explainers table, repository structure tree, and What's Next checklist
- `CONTRIBUTING.md` updated: counterfactual fairness added to existing explainers table and blocked concepts list
- `index.html`: CI badge added to README (commit 63c49cd8); CONTRIBUTING.md CI audit checks documented (commit 37f960c6); README formatting fixes (commit 646a3560)

---

## [0.8.0] - 2 Jun 2026
### Added
- CI pipeline: `.github/workflows/audits.yml` - runs all audit scripts (`unfair.py` and `fair.py`) automatically on every push and pull request (PR by Anjali Tiwari)
### Changed
- Dataset paths standardised across all audit scripts so every script resolves its dataset relative to its own file location, scripts now run correctly from the repo root, from within their own folder, and in CI (PR by Anjali Tiwari)

---

## [0.7.0] - 1 Jun 2026
### Added
- Explainer: Individual Fairness - added to index.html, README, and concepts covered
### Fixed
- HTML section closing tag bug in index.html (impact section broken)
- Mobile nav max-height increased for full scrollability on small screens
- Dataset path corrected in AI Fair Recruitment `fair.py` / `unfair.py` scripts (PR by Anjali Tiwari)
### Changed
- Code of Conduct revised for clarity and inclusivity
- scipy and shap package versions corrected in requirements.txt
- `CHANGELOG.md` added to project structure

---

## [0.6.0] - 31 May 2026
### Added
- Explainer: Label Bias - added to index.html, explainers directory, and CONTRIBUTING.md
### Changed
- README updated with new bias topics and explainers

---

## [0.5.1] - 30 May 2026
### Changed
- CONTRIBUTING.md revised for improved instructions
- README refactored for clarity and formatting

---

## [0.5.0] - 28–29 May 2026
### Added
- Explainer: Disparate Treatment - added to index.html, README, and CONTRIBUTING.md
- Explainer: Feedback Loop Bias - added to index.html, README, and CONTRIBUTING.md
- Welfare/Benefits Denial project button and project data on website
### Changed
- README updated with feedback loop bias and disparate treatment explainers

---

## [0.4.2] - 26–27 May 2026
### Added
- Explainer: Demographic Parity - added to index.html and CONTRIBUTING.md
- Star History section added to README
- Vercel deployment badge added to README
### Changed
- README formatting fixes

---

## [0.4.1] - 24 May 2026
### Added
- GitHub Issue Templates: bug report, new audit proposal, new explainer proposal (YAML)
- Pull request template
### Changed
- CONTRIBUTING.md updated with templates information
- README updated with PR and issue template references

---

## [0.4.0] - 21–23 May 2026
### Added
- Explainer: Calibration - `calibration.md`, added to index.html, README, CONTRIBUTING.md
- Explainer: Fairness Metric Conflicts - `fairness-metric-conflicts.md`
- Search placeholder and explainer card text updated on website
### Fixed
- Formatting fixes in CONTRIBUTING.md and README.md
### Changed
- Merged PR #26 (sofiya-iii): file additions

---

## [0.3.0] - 22 May 2026
### Added
- Audit 05: Benefits Denial (UCI Adult Census Income, 48,842 records)
  - `fair.py` and `unfair.py` for welfare eligibility bias
  - Dataset added
  - Jupyter notebook: `05_benefits_denial_bias_audit.ipynb`
  - README updated with Benefits Denial section and results
### Changed
- CONTRIBUTING.md updated for Benefits Denial audit

---

## [0.2.2] - 21 May 2026
### Added
- All five Jupyter notebooks added (`01` through `05`)
- `CITATION.cff` for project citation guidelines
- `SECURITY.md` for vulnerability reporting policy
- `requirements.txt` updated with full dependencies and instructions
### Fixed
- Various small website bugs
- Accessibility improvements and style refactors in index.html
- Cursor style set to pointer for navigation items

---

## [0.2.1] - 19–20 May 2026
### Added
- Explainer: Disparate Impact (80% Rule) - added to index.html, README, CONTRIBUTING.md
- Explainer: Equalized Odds - merged via PR #13 (TanishGoyal-Dev)
- Explainer: SHAP Values - merged via PR #12 (shwetagupta1234)
- Search bar with filtering for projects and explainers
- Copy and share buttons on website
- Back-to-top button for mobile
### Changed
- Website styles refactored: light mode, dark mode, navigation dropdowns
- Navigation improved with social media links and dropdown menus
- `requirements.txt` updated with pandas and scikit-learn

---

## [0.2.0] - 18–19 May 2026
### Added
- Audit 04: Insurance Denial (Kaggle, 1,340 records)
  - `fair.py`, `unfair.py`, dataset, and proof images
  - README and CONTRIBUTING.md updated
- Explainer: Sampling Bias - merged via PR #2 (evanjain-dot)
- `shap-values.md` added to explainers directory
- `CODE_OF_CONDUCT.md` added
### Changed
- CONTRIBUTING.md refined for explainer and audit submission guidelines
- README revised for project names, structure, and clarity

---

## [0.1.0] - 17–18 May 2026
### Added
- Audit 03: German Credit Lending Bias - merged via PR #1 (Aarav Sharma)
  - Random Forest model, dataset, `fair.py` / `unfair.py`
- Explainer section added to website with responsive styles
- Navigation dropdowns implemented in index.html
- Social media links added to navigation
### Changed
- README revised for project overview and results
- CONTRIBUTING.md created with audit guidelines

---

## [0.0.0] - 13–16 May 2026
### Added
- Audit 01: COMPAS Criminal Justice Bias (ProPublica, 70k+ records)
  - `fair.py`, `unfair.py`, dataset, proof images
- Audit 02: AI Fair Recruitment Bias (Kaggle)
  - `fair.py`, `unfair.py`, dataset, proof images
- Interactive website (`index.html`) deployed at fair-code-five.vercel.app
  - Light mode, mobile-responsive layout
- README with project overview, results table, and methodology

</details>
