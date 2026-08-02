<div align="center">

# Fair Code - Metrics Tracker

![Stars](https://img.shields.io/badge/Stars-41-brightgreen?style=flat-square&logo=github)
![Contributors](https://img.shields.io/badge/Contributors-12-blue?style=flat-square)
![Forks](https://img.shields.io/badge/Forks-18-orange?style=flat-square)
![Watching](https://img.shields.io/badge/Watching-8-yellow?style=flat-square)
![Explainers](https://img.shields.io/badge/Explainers-36-blueviolet?style=flat-square)
![Updated](https://img.shields.io/badge/Updated-Weekly-lightgrey?style=flat-square)

Weekly snapshot of project health. Updated every Friday.

[How to Update](#how-to-update) · [Weekly Metrics](#weekly-metrics) · [Targets](#targets) · [Notes](#notes)

</div>

---

## How to Update

1. Check GitHub for stars, forks, watchers, and contributor count
2. Check Instagram and LinkedIn for combined impressions/followers
3. Count issues closed this week
4. Count code audits published this week
5. Add a new row to the table below

---

## Weekly Metrics

| Week | Stars | Forks | Watching | Contributors | Social Views | Issues Closed | Code Audits |
|------|------:|------:|---------:|-------------:|-------------:|--------------:|------------:|
| 2026-W26 (baseline) | 27 | 8 | - | 7 | ~10K total | - | 6 total |
| 2026-W27 | 27 | 8 | - | 7 | ~10K total | - | 6 total |
| 2026-W30 | 40 | 17 | 8 | 11 | ~21K total | 3 | 7 total |
| 2026-W31 | 41 | 18 | 8 | 12 | ~23K total | 22 | 7 total |

> **2026-W27 - v1.2.0 shipped:** Open Dataset Profiler (CLI + client-side web tool) released; 23 explainers total.
>
> **2026-W30 - v1.3.0-v1.3.2 shipped since last snapshot:** Tenant Screening audit (#07) and intersectional bias analysis (v1.3.0), Unsupervised Learning + Model Drift explainers (v1.3.1), Selection Bias explainer (v1.3.2), plus author attribution/schema, `llms.txt`, and a canonical-URL/sitemap fix for AI-crawler and Google Search Console indexing. Watching tracked for the first time this week. **Gap notice:** no snapshot was logged for three weeks (W28-W29) - issues-closed reflects the trailing 7 days, not the full gap.
>
> **2026-W31 - tooling + healthcare push under the freeze:** profiler confidence intervals (#83), shareable HTML/PDF report (#85), a `--fail-under` CI gate (#115) and `--min-group-size` small-subgroup warnings (#124), an automated em-dash CI lint (#112), and the "Why Accuracy Is Not Enough in Healthcare AI" explainer (#64). New contributors @tomatotomata and @ahmdkaml. **Note on issues-closed (22):** inflated by a one-time triage - 11 new-audit proposals were closed as `post-paper` (a timing hold aligning the tracker with the paper freeze, not rejected work), the rest are the tooling/explainer issues shipped above.

---

## Targets

| Metric | Current | Target | Timeline |
|--------|--------:|-------:|----------|
| Stars | 41 | 50+ | End of 2026 |
| Forks | 18 | 20+ | End of 2026 |
| Watching | 8 | 12+ | End of 2026 |
| Contributors | 12 | 15+ | End of 2026 |
| Social reach | ~23K | 40K+ | End of 2026 |
| Issues closed | 22 (past 7 days) | Track weekly | Ongoing |
| Code audits | 7 | 8+ | End of 2026 |
| Explainers | 36 | 60+ | End of 2026 |

---

## Notes

- Social views = combined Instagram + LinkedIn impressions
- Contributors = external contributors only (excluding Yash), via GitHub's contributors API
- Watching = GitHub repo watchers/subscribers, via GitHub's repo API
- Issues closed = issues merged or resolved that week, not total open
- Code audits = cumulative total published in repo
- Explainers = cumulative total in `explainers/`

---

*Resume-ready line (fill in at application time):*

> Created and scaled Fair Code, an open-source responsible AI platform explaining algorithmic bias through code audits, healthcare-bias case studies, beginner explainers, and contributor-led GitHub documentation; grew the project to **41 stars**, **12 contributors**, **18 forks**, and **~23K social views**.
