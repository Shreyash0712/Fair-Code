<div align="center">

# Fair Code - Public Roadmap

![Phase 1](https://img.shields.io/badge/Phase%201-Complete-brightgreen?style=flat-square)
![Phase 2](https://img.shields.io/badge/Phase%202-In%20Progress-yellow?style=flat-square)
![Phase 3](https://img.shields.io/badge/Phase%203-In%20Progress-yellow?style=flat-square)
![Phase 4](https://img.shields.io/badge/Phase%204-In%20Progress-yellow?style=flat-square)
![Phase 5](https://img.shields.io/badge/Phase%205-In%20Progress-yellow?style=flat-square)
![Phase 6](https://img.shields.io/badge/Phase%206-Paper%20In%20Review-orange?style=flat-square)

This is the public roadmap for Fair Code. It tracks what has been built, what is actively in progress, and what comes next.

*Last updated: August 2026*

[Where We Are](#where-we-are) · Phase 1 · Phase 2 · Phase 3 · Phase 4 · Phase 5 · Phase 6 · [Content Schedule](#content-schedule) · [How to Contribute](#how-to-contribute)

</div>

---

## Where We Are

Fair Code is an open-source responsible AI platform explaining algorithmic bias, fairness, and AI accountability through code audits, explainers, healthcare-bias case studies, and contributor-led GitHub documentation.

**Current traction (August 2026):**

| Stars | Contributors | Forks | Watching | Social Reach | Countries | Audits | Explainers | CI |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 42 | 14 | 19 | 8 | 26K+ | 16 | 7 | 36 | ✅ every push/PR |

> 🔒 **Paper freeze active.** The benchmark results are cited in a research paper under peer review and are frozen at tag `v1.0-paper` (commit `bbef2ba`). No results-affecting change ships until the paper is published. See [CLAUDE.md](CLAUDE.md) for the full policy.

**Version & release gate:**

- Current release: **v2.0.0**
- **v3.0.0 is blocked until the paper is published.** The next major version bundles re-run benchmarks and new audits - both frozen right now - so the version cannot move until Phase 6 completes.

---

## Phase 1 - Bias Glossary and Beginner Explainers ✅

**Status: Foundational library complete - 36 explainers published, expanding toward a 60+ library**

Build the foundational vocabulary and explain core fairness concepts clearly enough for a non-technical reader.

- [x] Proxy Variables
- [x] Equalized Odds
- [x] Sampling Bias
- [x] SHAP Values
- [x] Disparate Impact (The 80% Rule)
- [x] Disparate Treatment
- [x] Why Fairness Metrics Conflict
- [x] Calibration
- [x] Demographic Parity
- [x] Feedback Loop Bias
- [x] Label Bias
- [x] Individual Fairness
- [x] Counterfactual Fairness
- [x] What Happens Inside a Neural Network
- [x] Why AI Hallucinates
- [x] What Is Reinforcement Learning
- [x] Proxy Entanglement
- [x] What Is Machine Learning Bias
- [x] What Is Data Leakage
- [x] How AI Detects Patterns
- [x] What Is Distribution Shift
- [x] The Biggest Myth About AI Objectivity
- [x] What Is a Confounding Variable?
- [x] What Is Predictive Parity?
- [x] False Positives vs. False Negatives in Medical Risk Models
- [x] What Is Supervised Learning?
- [x] What Is Unsupervised Learning?
- [x] What Is Model Drift?
- [x] What Is Selection Bias?
- [x] What Is Automation Bias?
- [x] What Is a ROC Curve and AUC?
- [x] What Is a Protected Attribute?
- [x] What Is a Confusion Matrix?
- [x] What Is Class Imbalance?
- [x] What Is the Bias-Variance Trade-off?

---

## Phase 2 - Healthcare AI Bias Examples ✅ / 🔄 In Progress

**Status: Audits complete - the healthcare push has shifted to explainers during the paper freeze**

Publish healthcare-specific bias audits and explainers that show how AI discrimination shows up in clinical and insurance contexts. New audits are frozen until the paper publishes (see [CLAUDE.md](CLAUDE.md)), so this phase's active work is now **healthcare explainers** - fully freeze-safe, and where the deepest real-world harm lives anyway.

- [x] Insurance Denial bias audit
- [x] Benefits Denial bias audit
- [x] Healthcare Readmission bias audit
- [x] Jupyter notebooks for all three healthcare audits
- [x] Explainer: Why Accuracy Is Not Enough in Healthcare AI
- [x] Explainer: False Positives and False Negatives in Medical Risk Models
- [x] Case study write-up: Insurance Denial Bias 
- [x] Case study write-up: Benefits Denial Bias (standalone 
- [x] Case study write-up: Healthcare Readmission Bias 

**Planned healthcare explainers (freeze-safe focus while audits are on hold):**

- [ ] Explainer: Race Correction in Clinical Algorithms - why "race-adjusted" formulas (eGFR kidney function, spirometry, VBAC calculators) bake bias directly into the math
- [ ] Explainer: The Obermeyer Case - When Cost Becomes a Proxy for Health Need - a dedicated case study of the 2019 algorithm that under-referred sicker Black patients
- [ ] Explainer: Underdiagnosis Bias - When the Label Itself Is Sicker for One Group - why historical care gaps make the training target unequal before modeling starts
- [ ] Explainer: Miscalibration in Clinical Risk Scores Across Groups - when the same risk score means a different real-world risk depending on the patient's group
- [ ] Explainer: Missing Data as Bias in Electronic Health Records - how unequal access to care turns into unequal missingness, and how models misread it
- [ ] Explainer: Why Medical Imaging Models Fail on Underrepresented Groups - representation gaps in imaging datasets and the skin-tone / equipment confounders they hide

---

## Phase 3 - Code Audits 🔄 In Progress

**Status: 7 of 9 planned audits published - new audits on hold for the paper freeze**

Each audit follows the same pipeline: train a biased model → measure the fairness gap → remove proxies → retrain → measure again. The paper covers exactly these seven domains, so the two remaining audits are parked until publication (a timing hold, not a rejection - see [CLAUDE.md](CLAUDE.md)).

- [x] COMPAS - Criminal Justice Bias
- [x] AI Fair Recruitment - Hiring Bias
- [x] German Credit Lending - Lending Bias
- [x] Insurance Denial - Healthcare Bias
- [x] Benefits Denial - Welfare Eligibility Bias
- [x] Healthcare Readmission - Clinical Bias
- [x] Tenant Screening - Rental Application Bias
- [x] LLM bias audit
- [ ] HMDA Mortgage Lending Bias *(post-paper)*
- [ ] Facial Recognition Accuracy Gaps (MIT Gender Shades methodology) *(post-paper)*

---

## Phase 4 - Contributor Expansion 🔄 In Progress

**Status: Active - 13 external contributors, growing toward 15+**

Goal: grow to 15+ contributors with quality-controlled contributions.

- [x] CONTRIBUTING.md
- [x] Issue templates (bug report, new audit, new explainer)
- [x] PR template
- [x] CODE_OF_CONDUCT.md
- [x] CI pipeline (all audit scripts run on push/PR)
- [x] Good-first-issue and help-wanted labels
- [x] First-interaction workflow (greets new contributors)
- [x] 10–15 labelled issues open at all times
- [x] Contributor list in README
- [x] METRICS.md tracking contributor growth weekly

---

## Phase 5 - Fairness Metrics and Notebooks 🔄 In Progress

**Status: Cross-domain benchmark harness shipped - dashboards and notebooks continuing**

Go deeper on measurement - fairness dashboards, interactive notebooks, and statistical tools for auditors.

- [x] Fairness audit web dashboard - **Open Dataset Profiler** ([profiler.html](profiler.html))
- [x] Bias detection utility library (`faircode/` module) - diagnostic representation profiler + CLI
- [x] Profiler: two-dataset comparison for representation drift (`faircode compare`, PSI)
- [x] Profiler: manual column mapping, reference-population baseline, choosable intersection pair, tunable thresholds, and chi-squared proxy hints
- [x] Fairlearn integration: `ExponentiatedGradient` in-processing + `ThresholdOptimizer` post-processing, as two rungs of a five-strategy mitigation ladder (S0-S4) run uniformly across every audit
- [x] Cross-domain benchmark harness - declarative `audit.yaml` manifests (`faircode/MANIFEST_SPEC.md`) + `faircode benchmark`: 5 strategies x 3 model families x 6 fairness metrics (bootstrap CI + permutation p-value) + accuracy/AUC/F1, written to `results/`
- [x] Intersectional bias notebook (auditing across multiple protected attributes simultaneously)
- [x] Statistical significance testing for fairness gaps
- [ ] Fairness dashboard for the benchmark harness results (interactive `results/` explorer, mirroring the Open Dataset Profiler's web/CLI split)

---

## Phase 6 - Research Paper and Publication 🔄 In Progress

**Status: Results frozen - paper in peer review**

Publish a peer-reviewed paper on the cross-domain fairness benchmark. This phase gates the whole analysis side of the project: the results stay frozen and the version stays at v2.0.0 until it completes.

- [x] Freeze benchmark results at tag `v1.0-paper` (commit `bbef2ba`)
- [x] `CLAUDE.md` paper-freeze policy for the benchmark and audits
- [ ] Submit manuscript to peer review
- [ ] Address reviewer feedback (may require a re-run + re-freeze - flag, never silently patch)
- [ ] Paper accepted and published
- [ ] Add citation and DOI to [README.md](README.md) and [CITATION.cff](CITATION.cff)
- [ ] Lift the freeze: re-run the benchmark, merge parked audits, cut **v3.0.0** (`paper/results-frozen/` stays untouched as the permanent record)

---

## Content Schedule

**During school:**
- Monday: AI bias explainer
- Wednesday: Healthcare AI / fairness example
- Friday: Code audit or project update

**During holidays:**
- Monday–Friday posting acceptable if sustainable

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) to claim an open issue or propose a new audit or explainer.

New audits are welcome, but during the paper freeze they cannot be merged into `main` - they'll be parked on a branch or held with a `post-paper` label until publication (a timing hold, not a rejection). Explainers, docs, and website content are unaffected and merge as usual. See [CLAUDE.md](CLAUDE.md) before opening a PR.

---

*Fair Code is maintained by [Yash Kewlani](https://github.com/yakew7). Follow the project at [@thefaircodeproject](https://instagram.com/thefaircodeproject).*
