<div align="center">

# Contributors

*Fair Code exists because people outside the maintainer's laptop chose to spend their time on it.*

[![Contributors](https://contrib.rocks/image?repo=yakew7/Fair-Code&excludeBots=true)](https://github.com/yakew7/Fair-Code/graphs/contributors)

</div>

---

## Contents

- [How this file works](#how-this-file-works)
- [Maintainer](#maintainer)
- [Core contributors](#core-contributors)
- [Contributors](#contributors)
- [Contributions by area](#contributions-by-area)
- [Automation](#automation)
- [Git identity map](#git-identity-map)
- [How to get listed](#how-to-get-listed)
- [Recognition beyond this file](#recognition-beyond-this-file)
- [Code of Conduct](#code-of-conduct)

---

## How this file works

Everyone below has at least one merged pull request on
[`yakew7/Fair-Code`](https://github.com/yakew7/Fair-Code). Core contributors are listed separately
(sustained ownership, reflected in [`.github/CODEOWNERS`](.github/CODEOWNERS)); everyone else is
ordered by merged PR count, most first - ties broken by commit count, then by earliest first-merged
date. Within each entry, the PR numbers link the claim to the actual diff, so nothing here is an
unverifiable "thanks to".

**Snapshot:** 2026-08-17, covering everything merged through **PR #275**.
Anything merged after that date is real and welcome, but is not yet reflected here - the
[contributors graph](https://github.com/yakew7/Fair-Code/graphs/contributors) is always the live
source of truth, and the `contrib.rocks` grid above regenerates from it automatically.

The counts come from two different places and will not always agree:

| Number | Where it comes from | Why it differs |
|--------|--------------------|----------------|
| **Merged PRs** | `gh pr list --state merged` | The unit of contribution this file counts. One PR = one reviewed, merged change. |
| **Commits** | GitHub's contributors graph | Higher for anyone who pushed several commits per PR, and it only counts commits on `main`. |

Where a contributor's local git author name differs from their GitHub handle, both are recorded in
the [Git identity map](#git-identity-map) so `git shortlog -sne` can be reconciled against this file.

---

## Maintainer

| | Who | Role |
|:--|-----|------|
| <a href="https://github.com/yakew7"><img src="https://github.com/yakew7.png" width="48" height="48" alt="yakew7"></a> | **Yash Kewlani** - [@yakew7](https://github.com/yakew7) | Creator and maintainer. Author of the seven audits, the `faircode` library and benchmark harness, the Open Dataset Profiler, the website, and the bulk of the 39 explainers. Code owner for `faircode/`, `paper/`, every `audit.yaml`, `explainers/`, and project policy (`CLAUDE.md`, `CONTRIBUTING.md`). |

Contact: [yashkewlani2020@gmail.com](mailto:yashkewlani2020@gmail.com) · [@thefaircodeproject](https://instagram.com/thefaircodeproject)

---

## Core contributors

People carrying sustained ownership of an area, reflected in [`.github/CODEOWNERS`](.github/CODEOWNERS).

### Ahmed Mohamed Abdelhady Kamel - [@ahmdkaml](https://github.com/ahmdkaml)

**38 merged PRs · 54 commits · first merged 2026-07-31**

Co-code-owner of `.github/workflows/`, `.github/CODEOWNERS`, `scripts/`, `tests/`, `profiler.html`,
and the three `assets/profiler-*.js` engines. The single largest external contribution to the
project by volume, concentrated in two areas:

**Profiler & data loading**
- Parquet and JSON loaders for the CLI ([#127](https://github.com/yakew7/Fair-Code/pull/127)), client-side JSON support in the web profiler ([#144](https://github.com/yakew7/Fair-Code/pull/144)), documented JSON orientations ([#155](https://github.com/yakew7/Fair-Code/pull/155))
- Lazy-loaded SheetJS for XLSX profiling ([#192](https://github.com/yakew7/Fair-Code/pull/192)), CDN pin kept in sync ([#193](https://github.com/yakew7/Fair-Code/pull/193)), XLSX edge cases ([#194](https://github.com/yakew7/Fair-Code/pull/194)), ignored-sheet reporting in both the web UI ([#197](https://github.com/yakew7/Fair-Code/pull/197)) and the CLI ([#198](https://github.com/yakew7/Fair-Code/pull/198)), documented `--proxy-hints` on the web profiler landing copy ([#236](https://github.com/yakew7/Fair-Code/pull/236))
- Standalone HTML report for `faircode compare` ([#128](https://github.com/yakew7/Fair-Code/pull/128)), configurable `--min-group-size` warnings ([#124](https://github.com/yakew7/Fair-Code/pull/124)), `--reference` help-text fix ([#145](https://github.com/yakew7/Fair-Code/pull/145))
- JS/Python profiler parity tests ([#126](https://github.com/yakew7/Fair-Code/pull/126)), HTML report smoke tests ([#172](https://github.com/yakew7/Fair-Code/pull/172)), `--fail-under` equality test ([#123](https://github.com/yakew7/Fair-Code/pull/123)), XLSX tests in CI ([#200](https://github.com/yakew7/Fair-Code/pull/200)), favicon/OG image generator coverage ([#234](https://github.com/yakew7/Fair-Code/pull/234)), a locked-vs-declared dependency version test ([#233](https://github.com/yakew7/Fair-Code/pull/233), restored and its scikit-learn drift fixed in [#256](https://github.com/yakew7/Fair-Code/pull/256))

**CI, supply chain & freeze safety**
- CI enforcement of the frozen files ([#157](https://github.com/yakew7/Fair-Code/pull/157)) - the guardrail that makes the paper freeze in [CLAUDE.md](CLAUDE.md) mechanical rather than a matter of trust
- Benchmark resample/permutation counts warn when they drift from the paper defaults ([#226](https://github.com/yakew7/Fair-Code/pull/226)); results-workflow figure-filename drift check ([#195](https://github.com/yakew7/Fair-Code/pull/195)); audit-manifest dataset column validation ([#156](https://github.com/yakew7/Fair-Code/pull/156))
- CodeQL code scanning ([#153](https://github.com/yakew7/Fair-Code/pull/153), upgraded to v4 in [#229](https://github.com/yakew7/Fair-Code/pull/229)), Dependabot extended to GitHub Actions ([#146](https://github.com/yakew7/Fair-Code/pull/146))
- `CODEOWNERS` itself ([#142](https://github.com/yakew7/Fair-Code/pull/142)) and the CI-automation ownership entry ([#174](https://github.com/yakew7/Fair-Code/pull/174)), workflow YAML validation ([#225](https://github.com/yakew7/Fair-Code/pull/225)), `CITATION.cff` validation ([#223](https://github.com/yakew7/Fair-Code/pull/223)), optional extras in `make setup` ([#222](https://github.com/yakew7/Fair-Code/pull/222)), Actions maintenance docs ([#196](https://github.com/yakew7/Fair-Code/pull/196)), static favicon assets ([#154](https://github.com/yakew7/Fair-Code/pull/154)), documented the pre-push test suite's runtime ([#238](https://github.com/yakew7/Fair-Code/pull/238)), `frozen-files`/`Build Explainers` running on direct pushes to `main`, not just PRs ([#258](https://github.com/yakew7/Fair-Code/pull/258), [#259](https://github.com/yakew7/Fair-Code/pull/259)), `make coverage` plus a non-gating coverage-report step in the profiler CI job ([#263](https://github.com/yakew7/Fair-Code/pull/263), [#264](https://github.com/yakew7/Fair-Code/pull/264))

---

## Contributors

Ordered by merged PR count, most first (ties broken by commit count, then by earliest first-merged date).

### Evan Jain - [@evanjain-dot](https://github.com/evanjain-dot)

**6 merged PRs · 28 commits · first merged 2026-05-18**

Author of the second PR ever merged into the repo. Three explainers plus a CI check:
[Sampling Bias](explainers/sampling-bias.md) ([#2](https://github.com/yakew7/Fair-Code/pull/2)),
[Counterfactual Fairness](explainers/counterfactual-fairness.md) ([#31](https://github.com/yakew7/Fair-Code/pull/31)),
[Reinforcement Learning](explainers/reinforcement-learning.md) ([#48](https://github.com/yakew7/Fair-Code/pull/48)),
and `codeowners-access.yml` ([#224](https://github.com/yakew7/Fair-Code/pull/224)), which verifies that every user
listed in `CODEOWNERS` actually holds repo write access, closing issue #219. Later added `ruff check`
as the repo's first general-purpose Python linter ([#261](https://github.com/yakew7/Fair-Code/pull/261),
closing issue #248), scoped to Pyflakes-only rules to avoid false-positiving on an intentional
`pytest.importorskip` import pattern used throughout `tests/`. Most recently, the
[What Is a Precision-Recall Curve?](explainers/precision-recall-curve.md) explainer
([#275](https://github.com/yakew7/Fair-Code/pull/275), closing issue #92), anchored to Healthcare
Readmission's real 11.2% base rate rather than an invented one.

### [@propcgamer20-png](https://github.com/propcgamer20-png)

**4 merged PRs · 13 commits · first merged 2026-07-06**

The [Predictive Parity](explainers/predictive-parity.md) explainer ([#72](https://github.com/yakew7/Fair-Code/pull/72)) - the ProPublica vs. Northpointe dispute as two correct fairness checks that cannot both hold. Then the contributor tooling: [`Makefile`](Makefile), [`.pre-commit-config.yaml`](.pre-commit-config.yaml), and the local-setup section of [CONTRIBUTING.md](CONTRIBUTING.md) ([#125](https://github.com/yakew7/Fair-Code/pull/125), closing issue #114). Later refactored the first-interaction workflow to find a contributor's genuinely earliest issue/PR ([#227](https://github.com/yakew7/Fair-Code/pull/227)), and added proper `<th scope="col">`/`<caption>` markup to `faircode/report.py`'s HTML report tables ([#260](https://github.com/yakew7/Fair-Code/pull/260), closing issue #254).

### Shreyash Swami - [@Shreyash0712](https://github.com/Shreyash0712)

**4 merged PRs · 7 commits · first merged 2026-06-05**

Ten explainers and two rounds of workflow maintenance:
[Why AI Hallucinates](explainers/ai-hallucinations.md) ([#43](https://github.com/yakew7/Fair-Code/pull/43)); then
[Bias-Variance Trade-off](explainers/bias-variance-tradeoff.md),
[Class Imbalance](explainers/class-imbalance.md),
[Confusion Matrix](explainers/confusion-matrix.md), and
[Protected Attribute](explainers/protected-attribute.md) in a single PR ([#102](https://github.com/yakew7/Fair-Code/pull/102)).
Also fixed the first-interaction greeting trigger and upgraded the audits workflow's action versions ([#46](https://github.com/yakew7/Fair-Code/pull/46)).
Later, five more in one PR ([#262](https://github.com/yakew7/Fair-Code/pull/262)):
[What Is the Base Rate Fallacy?](explainers/base-rate-fallacy.md),
[The Obermeyer Case: When Cost Becomes a Proxy for Health Need](explainers/obermeyer-cost-proxy.md),
[Race Correction in Clinical Algorithms](explainers/race-correction-clinical-algorithms.md),
[What Is Reject Inference?](explainers/reject-inference.md), and
[Underdiagnosis Bias in Healthcare AI](explainers/underdiagnosis-bias.md).

### Yojeet - [@Circout-sudo](https://github.com/Circout-sudo)

**3 merged PRs · 3 commits · first merged 2026-08-16**

Added a `test` extra (`pytest`, `pytest-cov`) to `pyproject.toml` ([#265](https://github.com/yakew7/Fair-Code/pull/265), [#266](https://github.com/yakew7/Fair-Code/pull/266)), part of the same test-coverage-reporting effort as [@ahmdkaml](https://github.com/ahmdkaml)'s [#263](https://github.com/yakew7/Fair-Code/pull/263)/[#264](https://github.com/yakew7/Fair-Code/pull/264), both closing issue #249. Later refined the `coverage` Makefile target's comment and added the `-q` flag to match `test`'s style ([#267](https://github.com/yakew7/Fair-Code/pull/267)).

### Anjali Tiwari - [@cannotdoit13](https://github.com/cannotdoit13)

**2 merged PRs · 2 commits · first merged 2026-06-01**

Fixed the dataset path in the AI Fair Recruitment scripts ([#27](https://github.com/yakew7/Fair-Code/pull/27)), then standardised path resolution across *every* audit and added the workflow that runs all of them on each push and PR ([#29](https://github.com/yakew7/Fair-Code/pull/29)). That PR is the origin of [`audits.yml`](.github/workflows/audits.yml) and of the "each script resolves its dataset relative to its own location" guarantee in the README.

### Anay Dhawan - [@AnayDhawan](https://github.com/AnayDhawan)

**2 merged PRs · 2 commits · first merged 2026-07-14**

[Unsupervised Learning](explainers/unsupervised-learning.md) ([#74](https://github.com/yakew7/Fair-Code/pull/74)), on k-means over the Benefits Denial dataset recovering a sex split without sex ever being a feature, and [Model Drift](explainers/model-drift.md) ([#75](https://github.com/yakew7/Fair-Code/pull/75)), on why a fairness gap measured once at launch is not guaranteed to hold months later.

### Swastik Yadav - [@Swastik-Yadav](https://github.com/Swastik-Yadav)

**2 merged PRs · 2 commits · first merged 2026-08-07**

A build-time check for missing Open Graph images in `scripts/build_explainers.py` ([#191](https://github.com/yakew7/Fair-Code/pull/191)), and a wording standardisation sweep across the docs and audit-script comments ([#232](https://github.com/yakew7/Fair-Code/pull/232)) - prose only, leaving every reported number untouched, as the freeze requires.

### [@YashKewlani1](https://github.com/YashKewlani1)

**1 merged PR · 10 commits · first merged 2026-05-18**

PR [#1](https://github.com/yakew7/Fair-Code/pull/1) - the [German Credit Lending](German%20Credit%20Lending/) audit: dataset, `unfair.py`, `fair.py`, terminal screenshots, and the README section. The first merged pull request in the project's history, and the third audit to land.

### Rajveer Vadnal - [@Rajveerx11](https://github.com/Rajveerx11)

**1 merged PR · 3 commits · first merged 2026-05-19**

The [Disparate Impact](explainers/disparate-impact.md) explainer ([#14](https://github.com/yakew7/Fair-Code/pull/14)), covering the four-fifths rule and the legal threshold it sets under US employment law, landed alongside work on the AI Fair Recruitment audit files.

### [@shwetagupta1234](https://github.com/shwetagupta1234)

**1 merged PR · 2 commits · first merged 2026-05-18**

The [SHAP Values](explainers/shap-values.md) explainer ([#12](https://github.com/yakew7/Fair-Code/pull/12)) - how to see what actually drove a model's decision, and how to use that to catch bias.

### Tanish Goyal - [@TanishGoyal-Dev](https://github.com/TanishGoyal-Dev)

**1 merged PR · 2 commits · first merged 2026-05-19**

The [Equalized Odds](explainers/equalized-odds.md) explainer ([#13](https://github.com/yakew7/Fair-Code/pull/13)) - the metric that catches a model treating two groups differently even when overall accuracy looks fine.

### Aarav Saroliya - [@Aarav1611](https://github.com/Aarav1611)

**1 merged PR · 1 commit · first merged 2026-05-23**

The first draft of the [Calibration](explainers/calibration.md) explainer ([#26](https://github.com/yakew7/Fair-Code/pull/26)) - why a model can be equally accurate for everyone and still treat them unequally.

### Ahmad Alguydi - [@tomatotomata](https://github.com/tomatotomata)

**1 merged PR · 1 commit · first merged 2026-07-31**

The `faircode profile --fail-under N` CI gate ([#116](https://github.com/yakew7/Fair-Code/pull/116)) - exit code `1` with the failing score on stderr when a dataset's representation score falls below the threshold, with report output kept on stdout. This is what makes the Profiler usable as a pipeline check rather than only a human-read report.

### Anuj Kamdar - [@anujkamdar](https://github.com/anujkamdar)

**1 merged PR · 1 commit · first merged 2026-08-05**

Fixed the site's theme toggle to respect the OS `prefers-color-scheme` setting ([#143](https://github.com/yakew7/Fair-Code/pull/143)) - applied across every generated explainer page.

### Kumar Mangalam - [@ImMortaL0P](https://github.com/ImMortaL0P)

**1 merged PR · 1 commit · first merged 2026-08-06**

JSON edge-case coverage and clear parse-error messages on *both* engines ([#175](https://github.com/yakew7/Fair-Code/pull/175)) - `faircode/loaders_extra.py`, `assets/profiler-engine.js`, and a shared parity script, so the CLI and the browser fail the same way on the same bad file.
Added a `test` extra (`pytest`, `pytest-cov`) to `pyproject.toml` ([#265](https://github.com/yakew7/Fair-Code/pull/265), [#266](https://github.com/yakew7/Fair-Code/pull/266)), part of the same test-coverage-reporting effort as [@ahmdkaml](https://github.com/ahmdkaml)'s [#263](https://github.com/yakew7/Fair-Code/pull/263)/[#264](https://github.com/yakew7/Fair-Code/pull/264), both closing issue #249.

---

## Contributions by area

A cross-cut of the same work, for anyone looking for who to ask about what.

| Area | Contributors |
|------|--------------|
| **Audits** (`*/unfair.py`, `*/fair.py`, `audit.yaml`) | [@yakew7](https://github.com/yakew7), [@YashKewlani1](https://github.com/YashKewlani1), [@Rajveerx11](https://github.com/Rajveerx11), [@cannotdoit13](https://github.com/cannotdoit13) |
| **Explainers** (`explainers/`) | [@yakew7](https://github.com/yakew7), [@Shreyash0712](https://github.com/Shreyash0712), [@evanjain-dot](https://github.com/evanjain-dot), [@AnayDhawan](https://github.com/AnayDhawan), [@propcgamer20-png](https://github.com/propcgamer20-png), [@Rajveerx11](https://github.com/Rajveerx11), [@TanishGoyal-Dev](https://github.com/TanishGoyal-Dev), [@shwetagupta1234](https://github.com/shwetagupta1234), [@Aarav1611](https://github.com/Aarav1611) |
| **Profiler - CLI & loaders** (`faircode/`) | [@yakew7](https://github.com/yakew7), [@ahmdkaml](https://github.com/ahmdkaml), [@tomatotomata](https://github.com/tomatotomata), [@ImMortaL0P](https://github.com/ImMortaL0P), [@propcgamer20-png](https://github.com/propcgamer20-png) |
| **Profiler - web** (`profiler.html`, `assets/profiler-*.js`) | [@yakew7](https://github.com/yakew7), [@ahmdkaml](https://github.com/ahmdkaml), [@ImMortaL0P](https://github.com/ImMortaL0P) |
| **Benchmark harness & paper freeze** | [@yakew7](https://github.com/yakew7), [@ahmdkaml](https://github.com/ahmdkaml) |
| **CI & workflows** (`.github/`) | [@yakew7](https://github.com/yakew7), [@ahmdkaml](https://github.com/ahmdkaml), [@cannotdoit13](https://github.com/cannotdoit13), [@Shreyash0712](https://github.com/Shreyash0712), [@evanjain-dot](https://github.com/evanjain-dot), [@propcgamer20-png](https://github.com/propcgamer20-png), [@Swastik-Yadav](https://github.com/Swastik-Yadav) |
| **Website & explainer build** | [@yakew7](https://github.com/yakew7), [@anujkamdar](https://github.com/anujkamdar), [@Swastik-Yadav](https://github.com/Swastik-Yadav) |
| **Tests** (`tests/`) | [@yakew7](https://github.com/yakew7), [@ahmdkaml](https://github.com/ahmdkaml), [@tomatotomata](https://github.com/tomatotomata), [@ImMortaL0P](https://github.com/ImMortaL0P) |
| **Contributor tooling & docs** | [@yakew7](https://github.com/yakew7), [@propcgamer20-png](https://github.com/propcgamer20-png), [@ahmdkaml](https://github.com/ahmdkaml), [@Swastik-Yadav](https://github.com/Swastik-Yadav), [@Circout-sudo](https://github.com/Circout-sudo) |

---

## Automation

These accounts appear in the contributors graph but are not people. They are listed for completeness
and excluded from the avatar grid above.

| Bot | Merged PRs | What it does |
|-----|:---------:|--------------|
| [dependabot](https://github.com/apps/dependabot) | 24 | Dependency and GitHub Actions version bumps, configured in [`.github/dependabot.yml`](.github/dependabot.yml). **Note:** its `pip` scan also targets [`requirements-lock.txt`](requirements-lock.txt), which is frozen - those bumps get reverted, not merged. See [CLAUDE.md §1](CLAUDE.md). |
| [vercel](https://github.com/apps/vercel) | 2 | Web Analytics and Speed Insights wiring for the deployed site. |

---

## Git identity map

Some contributors commit under a local `user.name` that differs from their GitHub handle. This table
makes `git shortlog -sne` reconcilable with the list above.

| GitHub handle | Git author name(s) recorded in history |
|---------------|----------------------------------------|
| [@yakew7](https://github.com/yakew7) | `Yash Kewlani`, `yakew7_` |
| [@ahmdkaml](https://github.com/ahmdkaml) | `ahmdkaml`, `Ahmed Mohamed Abdelhady Kamel (احمد محمد عبدالهادي كامل)` |
| [@cannotdoit13](https://github.com/cannotdoit13) | `Anjali Tiwari` |
| [@AnayDhawan](https://github.com/AnayDhawan) | `unknown` |
| [@Rajveerx11](https://github.com/Rajveerx11) | `Rajveer Vadnal` |
| [@Shreyash0712](https://github.com/Shreyash0712) | `Shreyash0712`, `Shreyash Swami` |
| [@Swastik-Yadav](https://github.com/Swastik-Yadav) | `Swastik-Yadav`, `CHiGO` |
| [@ImMortaL0P](https://github.com/ImMortaL0P) | `Mangalam` |
| [@tomatotomata](https://github.com/tomatotomata) | `ahmadalguydi` |
| [@Aarav1611](https://github.com/Aarav1611) | `Aarav Saroliya` |
| [@anujkamdar](https://github.com/anujkamdar) | `Anuj Kamdar` |
| [@evanjain-dot](https://github.com/evanjain-dot) | `evanjain-dot` |
| [@YashKewlani1](https://github.com/YashKewlani1) | `Aarav Sharma` |
| [@TanishGoyal-Dev](https://github.com/TanishGoyal-Dev) | `TanishGoyal-Dev` |
| [@shwetagupta1234](https://github.com/shwetagupta1234) | `shwetagupta1234` |
| [@Circout-sudo](https://github.com/Circout-sudo) | `Yojeet` |

If your name is wrong, missing, or you would rather be listed under a different handle, or not
listed at all, open an issue or a one-line PR against this file. It gets merged, no questions asked.

---

## How to get listed

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. It covers the audit folder layout, the two required
   scripts, proxy-variable analysis, screenshots, dataset requirements, explainer structure, style
   rules, and what will *not* be merged.
2. Open an issue (or comment on an existing one) before starting anything substantial, so two people
   don't write the same explainer.
3. Open the PR. Add yourself to this file in the same PR - a new entry under
   [Contributors](#contributors) in first-merged order, with links to the files you touched.
4. When it merges, you're in.

**During the paper freeze, read [CLAUDE.md](CLAUDE.md) before you start.** The short version:

| Contribution | Status during the freeze |
|--------------|--------------------------|
| Explainers, docs, prose, website content, contributor tooling | ✅ Open - this is where the work is |
| Profiler features, tests, CI, loaders | ✅ Open, provided `results/` and the frozen files don't move |
| **New audits** | ⏸️ **Not merged to `main`** - the paper states exactly seven domains. Your PR gets parked on a branch or labeled `post-paper` and merged after publication. This is a timing hold, not a rejection, and you are credited either way. |
| Anything under `paper/results-frozen/`, `results/`, the core `faircode/` analysis modules, any `audit.yaml`, any dataset CSV, or `requirements-lock.txt` | ❌ Frozen. Found a genuine bug in the analysis code? [Open an issue](https://github.com/yakew7/Fair-Code/issues) - do not silently fix it. |

---

## Recognition beyond this file

- The **avatar grid** at the top of this file and in the [README](README.md#contributors) is generated
  from GitHub's contributors graph and can lag a merged PR by a few days.
- [`CITATION.cff`](CITATION.cff) is the citation record for the project. If your contribution is
  cited by the paper, that's where authorship is recorded.
- [`CHANGELOG.md`](CHANGELOG.md) records the change itself, release by release.
- [`METRICS.md`](METRICS.md) tracks contributor count among the project's weekly traction numbers.
- First-time contributors get an automated greeting via
  [`first.interaction.yml`](.github/workflows/first.interaction.yml).

---

## Code of Conduct

Everyone listed here, and everyone who wants to be, is held to
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Report concerns to
[yashkewlani2020@gmail.com](mailto:yashkewlani2020@gmail.com).

---

<div align="center">

*Fair Code is MIT-licensed. Every dataset used is publicly available.*
**[thefaircode.xyz](https://www.thefaircode.xyz)**

</div>
