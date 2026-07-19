<div align="center">

# Fair Code - Public Roadmap

![Phase 1](https://img.shields.io/badge/Phase%201-Complete-brightgreen?style=flat-square)
![Phase 2](https://img.shields.io/badge/Phase%202-In%20Progress-yellow?style=flat-square)
![Phase 3](https://img.shields.io/badge/Phase%203-In%20Progress-yellow?style=flat-square)
![Phase 4](https://img.shields.io/badge/Phase%204-In%20Progress-yellow?style=flat-square)
![Phase 5](https://img.shields.io/badge/Phase%205-Planned-lightgrey?style=flat-square)

This is the public roadmap for Fair Code. It tracks what has been built, what is actively in progress, and what comes next.

*Last updated: July 2026*

[Where We Are](#where-we-are) · Phase 1 · Phase 2 · Phase 3 · Phase 4 · Phase 5 · [Content Schedule](#content-schedule) · [How to Contribute](#how-to-contribute)

</div>

---

## Where We Are

Fair Code is an open-source responsible AI platform explaining algorithmic bias, fairness, and AI accountability through code audits, explainers, healthcare-bias case studies, and contributor-led GitHub documentation.

**Current traction (July 2026):**

| Stars | Contributors | Forks | Social Reach | Audits | Explainers | CI |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 37+ | 8+ | 13+ | 16K+ | 7 | 29 | ✅ every push/PR |

---

## Phase 1 - Bias Glossary and Beginner Explainers ✅

**Status: Complete**

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

---

## Phase 2 - Healthcare AI Bias Examples ✅ / 🔄 In Progress

**Status: Audits complete - explainers expanding**

Publish healthcare-specific bias audits and explainers that show how AI discrimination shows up in clinical and insurance contexts.

- [x] Insurance Denial bias audit
- [x] Benefits Denial bias audit
- [x] Healthcare Readmission bias audit
- [x] Jupyter notebooks for all three healthcare audits
- [ ] Explainer: Why Accuracy Is Not Enough in Healthcare AI
- [x] Explainer: False Positives and False Negatives in Medical Risk Models
- [x] Case study write-up: Insurance Denial Bias 
- [x] Case study write-up: Benefits Denial Bias (standalone 
- [x] Case study write-up: Healthcare Readmission Bias 

---

## Phase 3 - Code Audits 🔄 In Progress

**Status: 7 of 9 planned audits published**

Each audit follows the same pipeline: train a biased model → measure the fairness gap → remove proxies → retrain → measure again.

- [x] COMPAS - Criminal Justice Bias
- [x] AI Fair Recruitment - Hiring Bias
- [x] German Credit Lending - Lending Bias
- [x] Insurance Denial - Healthcare Bias
- [x] Benefits Denial - Welfare Eligibility Bias
- [x] Healthcare Readmission - Clinical Bias
- [x] Tenant Screening - Rental Application Bias
- [ ] HMDA Mortgage Lending Bias
- [ ] Facial Recognition Accuracy Gaps (MIT Gender Shades methodology)
- [x] LLM bias audit

---

## Phase 4 - Contributor Expansion 🔄 In Progress

**Status: Active - 7 external contributors**

Goal: grow to 10+ contributors with quality-controlled contributions.

- [x] CONTRIBUTING.md
- [x] Issue templates (bug report, new audit, new explainer)
- [x] PR template
- [x] CODE_OF_CONDUCT.md
- [x] CI pipeline (all audit scripts run on push/PR)
- [x] Good-first-issue and help-wanted labels
- [x] First-interaction workflow (greets new contributors)
- [x] 10–15 labelled issues open at all times
- [x] Contributor list in README
- [ ] METRICS.md tracking contributor growth weekly

---

## Phase 5 - Fairness Metrics and Notebooks ⏳ Planned

**Status: Planned**

Go deeper on measurement - fairness dashboards, interactive notebooks, and statistical tools for auditors.

- [x] Fairness audit web dashboard - **Open Dataset Profiler** ([profiler.html](profiler.html))
- [x] Bias detection utility library (`faircode/` module) - diagnostic representation profiler + CLI
- [x] Profiler: two-dataset comparison for representation drift (`faircode compare`, PSI)
- [x] Profiler: manual column mapping, reference-population baseline, choosable intersection pair, tunable thresholds, and chi-squared proxy hints
- [x] AIF360 / Fairlearn integration examples
- [x] Intersectional bias notebook (auditing across multiple protected attributes simultaneously)
- [x] Statistical significance testing for fairness gaps

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

If you want to take on a Phase 3 audit (HMDA, facial recognition, or LLM bias), open an issue first with a brief description of your approach and the dataset you plan to use.

---

*Fair Code is maintained by [Yash Kewlani](https://github.com/yakew7). Follow the project at [@thefaircodeproject](https://instagram.com/thefaircodeproject).*
