<div align="center">

# Fair Code - Metrics Tracker

![Stars](https://img.shields.io/badge/Stars-43-brightgreen?style=flat-square&logo=github)
![Contributors](https://img.shields.io/badge/Contributors-17-blue?style=flat-square)
![Forks](https://img.shields.io/badge/Forks-22-orange?style=flat-square)
![Watching](https://img.shields.io/badge/Watching-8-yellow?style=flat-square)
![Explainers](https://img.shields.io/badge/Explainers-47-blueviolet?style=flat-square)
![Countries](https://img.shields.io/badge/Countries-18-informational?style=flat-square)
![Updated](https://img.shields.io/badge/Updated-Weekly-lightgrey?style=flat-square)

Weekly snapshot of project health. Updated every Friday.

[How to Update](#how-to-update) · [Weekly Metrics](#weekly-metrics) · [Targets](#targets) · [Notes](#notes)

</div>

---

## How to Update

1. Check GitHub for stars, forks, watchers, and contributor count
2. Check Instagram and LinkedIn for combined impressions/followers
3. Check site analytics for the count of unique countries visiting thefaircode.xyz
4. Count issues closed this week
5. Count code audits published this week
6. Add a new row to the table below

---

## Weekly Metrics

| Week | Stars | Forks | Watching | Contributors | Social Views | Countries | Issues Closed | Code Audits |
|------|------:|------:|---------:|-------------:|-------------:|----------:|--------------:|------------:|
| 2026-W26 (baseline) | 27 | 8 | - | 7 | ~10K total | - | - | 6 total |
| 2026-W27 | 27 | 8 | - | 7 | ~10K total | - | - | 6 total |
| 2026-W30 | 40 | 17 | 8 | 11 | ~21K total | - | 3 | 7 total |
| 2026-W31 | 41 | 18 | 8 | 12 | ~23K total | - | 22 | 7 total |
| 2026-W32 | 42 | 22 | 8 | 14 | 26K+ total | 17 | 11 | 7 total |
| 2026-W33 | 43 | 21 | 8 | 15 | 27K+ total | 17 | 55 | 7 total |
| 2026-W34 | 43 | 22 | 8 | 17 | 30K+ total | 18 | 35 | 7 total |

> **2026-W27 - v1.2.0 shipped:** Open Dataset Profiler (CLI + client-side web tool) released; 23 explainers total.
>
> **2026-W30 - v1.3.0-v1.3.2 shipped since last snapshot:** Tenant Screening audit (#07) and intersectional bias analysis (v1.3.0), Unsupervised Learning + Model Drift explainers (v1.3.1), Selection Bias explainer (v1.3.2), plus author attribution/schema, `llms.txt`, and a canonical-URL/sitemap fix for AI-crawler and Google Search Console indexing. Watching tracked for the first time this week. **Gap notice:** no snapshot was logged for three weeks (W28-W29) - issues-closed reflects the trailing 7 days, not the full gap.
>
> **2026-W31 - tooling + healthcare push under the freeze:** profiler confidence intervals (#83), shareable HTML/PDF report (#85), a `--fail-under` CI gate (#115) and `--min-group-size` small-subgroup warnings (#124), an automated em-dash CI lint (#112), and the "Why Accuracy Is Not Enough in Healthcare AI" explainer (#64). New contributors @tomatotomata and @ahmdkaml. **Note on issues-closed (22):** inflated by a one-time triage - 11 new-audit proposals were closed as `post-paper` (a timing hold aligning the tracker with the paper freeze, not rejected work), the rest are the tooling/explainer issues shipped above.
>
> **2026-W32 - GEO/SEO push, JSON/Parquet input, compare HTML reports, and a theme-toggle fix:** JSON-LD/FAQPage/Dataset schema, OpenGraph social-preview images, and an expanded `robots.txt` for AI crawlers across the site; `faircode profile`/`compare` gained `.json` and `.parquet` input (#127) and `faircode compare --html` plus a matching web-UI download button (#111, #128); `.github/CODEOWNERS` (#142, closes #138) and a theme toggle that now respects `prefers-color-scheme` (#143, closes #135). New contributor @anujkamdar. **Note on issues-closed (11):** the tooling issues shipped above, not a triage batch like W31's.
>
> **2026-W32 (later in week) - JS parity, client-side Excel, and a CI/security hardening batch:** JSON edge-case coverage and clearer parse errors (#175), client-side `.xlsx` support for the web profiler with a Subresource Integrity hash on its CDN script (#158), a `results/`-vs-`paper/results-frozen/` drift check (#173), a merge-base fix for the frozen-files check (#163), CodeQL extended to JavaScript (#162), a scripted favicon pipeline (#164), consolidated JS CLI-bridge scripts (#170), an audit-manifest `row_filters` validation test (#168), a GitHub Actions version-bump audit process (#167), removal of ~35K lines of dead vendored CI code, and CodeQL/Dependabot process docs (#161, #165). **Countries tracked for the first time this week** (16, unique countries visiting [thefaircode.xyz](https://www.thefaircode.xyz) per site analytics - distinct from the Instagram/LinkedIn-based social views figure).
>
> **2026-W32 (traction refresh) - forks and countries caught up to live data:** forks `19 → 22` (GitHub's API, was stale since the last snapshot), countries reached `16 → 17`. Contributors badge/targets/resume line also corrected to `14` - the weekly table row already had it, the rest of the doc hadn't caught up.
>
> **2026-W33 - three healthcare explainers close out the roadmap's "planned" list down to three:** Miscalibration in Clinical Risk Scores Across Groups (#106), Missing Data as Bias in Electronic Health Records (#107, with a real 10.7-point payer-code missingness gap by race computed straight from the Healthcare Readmission CSV), and Why Medical Imaging Models Fail on Underrepresented Groups (#108) - explainer count `36 → 39`. Stars, forks, watching, and contributors are unchanged from last week's live GitHub numbers. **Note on issues-closed (55):** not a triage batch like W31's - 36 PRs merged this week across CI hardening (CodeQL v4, CITATION.cff validation, workflow YAML validation, CODEOWNERS access checks), profiler tooling (XLSX/JSON edge cases, HTML report tests), and the three explainers above, several closing more than one linked issue.
>
> **2026-W33 (later in week) - a supply-chain/CI hardening + accessibility batch:** two real, previously-unnoticed drifts caught and fixed - `matplotlib`/`numpy` missing from `pyproject.toml` despite being imported unconditionally (#235, closes the same class of gap Pillow once had), and `scikit-learn` locked at `1.8.0` while `pyproject.toml` required `>=1.9.0` after the test that caught it was deleted rather than fixed (#255, restored by `@ahmdkaml`). `check-frozen-files`/`Build Explainers` now also run on direct pushes to `main`, not just PRs (#246, `@ahmdkaml`). `audits.yml`'s `profiler`/`benchmark-harness` jobs are now change-aware, skipping on docs-only pushes the same way the pre-push hook already did (#237); `run-audits` itself is left unconditional since it's the one required status check (#160). A new `scripts/check_broken_links.py` (#253) caught five real broken links in explainer markdown (a misspelled dataset-folder name, a missing `../`) plus a second bug in `build_explainers.py`'s own link resolver that had silently broken every such link in the generated `.html` too. The theme-toggle button now exposes its state via `aria-pressed` (#250), `faircode/report.py`'s HTML report tables get proper `<th scope="col">`/`<caption>` markup (#254, `@propcgamer20-png`), and `ruff check` lands as the repo's first general-purpose Python linter (#248, `@evanjain-dot`). Stars `42 → 43`; forks, watching, and contributors unchanged. Issues-closed for the week isn't re-tallied here since several of these closed same-day as this note.
>
> **2026-W33 (weekend update) - five more explainers, non-gating coverage reporting, and a new contributor:** five healthcare-adjacent explainers landed in one PR ([@Shreyash0712](https://github.com/Shreyash0712), #262) - What Is the Base Rate Fallacy?, The Obermeyer Case, Race Correction in Clinical Algorithms, What Is Reject Inference?, and Underdiagnosis Bias in Healthcare AI - closing out Phase 2's planned-healthcare-explainer backlog entirely; explainer count `39 → 44`. `make coverage` (pytest-cov, informational only, no CI gate) landed via three coordinated PRs (#263/#264 by `@ahmdkaml`, #265/#266 by new contributor **Circout-sudo**), but the profiler CI job's install step was never updated to include `pytest-cov`, so the new "Report test coverage" step failed on every run since - masked as an overall job success by `continue-on-error: true`. Fixed directly by adding `pytest-cov` to the install line; verified in a clean venv that it now reports real coverage numbers instead of erroring. Also fixed a stale `Build Explainers` CI failure from #262 skipping `make build-explainers` before opening the PR. **Contributors `14 → 15`** (Circout-sudo's first merged PR): GitHub's contributors API hadn't caught up at check time (same lag pattern as the W32 forks correction) - counted from `CONTRIBUTORS.md`'s manually-verified list instead, which is the more current source. Forks `22 → 21` (a real decrease, per GitHub's live API - not a data error). Stars `43` unchanged.
>
> **2026-W34 - traction refresh:** combined Instagram/LinkedIn impressions crossed `27K+ → 30K+`. Countries reached steady at 17. Stars, forks, watching, and contributors unchanged from last week's live numbers - this week's earlier merged work (#276-#279: a citation-links explainer pass, CLI error-handling test coverage plus a real `--html` traceback fix, favicon-parsing test coverage, and a docstring fix) was fixes and test coverage, not new explainers or audits.
>
> **2026-W34 (later in week) - two stale explainer issues closed, two real gaps filled:** cross-checking every open "Explainer:" issue against `explainers/` found four that were already done and never closed (#93, #94, #98, #99, plus #103 and #104 found in a second pass) - all closed with a pointer to the PR that already resolved them. Two were genuine gaps: [What Is Equal Opportunity?](explainers/equal-opportunity.md) (closes #80) and [What Is Intersectional Bias?](explainers/intersectional-bias.md) (closes #67) - both anchored to real frozen benchmark numbers (`equal_opportunity_diff`/`equalized_odds_diff` for COMPAS and Tenant Screening; a superadditive `intersectional_demographic_parity_diff` for Benefits Denial) rather than invented ones. Explainer count `45 → 47`.
>
> **2026-W34 (traction refresh) - forks, contributors, and countries caught up to live data:** forks `21 → 22` and countries `17 → 18` per live site analytics; contributors `15 → 17` - one from [@nivedmahendran](https://github.com/nivedmahendran)'s first merged PR (#287), the other from GitHub's contributors API finally catching up on [@TanishGoyal-Dev](https://github.com/TanishGoyal-Dev), whose own first PR it had been missing since the W32 lag note. Counted from `CONTRIBUTORS.md`'s manually-verified list rather than the raw API count (16), which still lags by that one contributor - the same reasoning as the W32/W33 corrections. Stars and watching unchanged at 43 and 8.

---

## Targets

| Metric | Current | Target | Timeline |
|--------|--------:|-------:|----------|
| Stars | 43 | 50+ | End of 2026 |
| Forks | 22 | 25+ | End of 2026 |
| Watching | 8 | 12+ | End of 2026 |
| Contributors | 17 | 20+ | End of 2026 |
| Social reach | 30K+ | 40K+ | End of 2026 |
| Countries reached | 18 | 20+ | End of 2026 |
| Issues closed | 35 (past 7 days) | Track weekly | Ongoing |
| Code audits | 7 | 8+ | End of 2026 |
| Explainers | 47 | 60+ | End of 2026 |

---

## Notes

- Social views = combined Instagram + LinkedIn impressions
- Countries = unique countries visiting the live website ([thefaircode.xyz](https://www.thefaircode.xyz)), via site analytics - not the social-views figure above
- Contributors = external contributors only (excluding Yash), via GitHub's contributors API
- Watching = GitHub repo watchers/subscribers, via GitHub's repo API
- Issues closed = issues merged or resolved that week, not total open
- Code audits = cumulative total published in repo
- Explainers = cumulative total in `explainers/`

---

*Resume-ready line (fill in at application time):*

> Created and scaled Fair Code, an open-source responsible AI platform explaining algorithmic bias through code audits, healthcare-bias case studies, beginner explainers, and contributor-led GitHub documentation; grew the project to **43 stars**, **17 contributors**, **22 forks**, **30K+ social views**, and website visitors from **18 countries**.
