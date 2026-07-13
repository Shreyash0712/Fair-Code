<div align="center">

# Fair Code Profiler - Analysis Spec

![Source of Truth](https://img.shields.io/badge/Source%20of%20Truth-Single%20Spec-blue?style=flat-square)
![Engines](https://img.shields.io/badge/Engines-Python%20%2B%20JS-orange?style=flat-square)
![Parity](https://img.shields.io/badge/Parity-Bit--for--Bit-brightgreen?style=flat-square)

This is the **single source of truth** for the Open Dataset Profiler. Both implementations -
the Python engine (`faircode/profiler.py`) and the browser engine (`assets/profiler-engine.js`) -
must implement *exactly* this spec so the same CSV yields the same numbers in the CLI and on the web.

The Profiler is **diagnostic**, not predictive. It audits a dataset's *demographic representation*
before any model is trained. It does not train models, drop columns, or measure prediction gaps -
that is what the `unfair.py` / `fair.py` audits do. The Profiler answers a different question:
**"who is, and is not, adequately represented in this data?"**

[1. Detection](#1-column-auto-detection) · [2. Age](#2-age-normalization) · [3. Metrics](#3-per-dimension-metrics) · [4. Intersections](#4-intersectional-gaps-informational-not-scored) · [5. Score](#5-headline-score--grade) · [6. Shape](#6-result-shape) · [7. Defaults](#7-defaults-single-place-to-tune) · [8. Comparison](#8-dataset-comparison-representation-drift)

</div>

---

## 1. Column auto-detection

**Tokenize** the column name: split on separators **and** camelCase boundaries, then lower-case.
`DateOfBirth → [date, of, birth]`, `Sex_Code_Text → [sex, code, text]`, `ageGroup → [age, group]`.
Token boundaries are what stop `age` from matching `Agency_Text` or `Language`.

A keyword matches a token by **exact match** when the keyword is <4 chars, or **prefix match** when
it is ≥4 chars (prefix, not substring - so `age` never matches `agency`, but `statecode` matches
`state`). Classify by the **first** keyword list that matches any token (order matters):

| Dimension   | Keywords                                                                 |
|-------------|--------------------------------------------------------------------------|
| `sex`       | `sex`, `gender`                                                          |
| `race`      | `race`, `ethnic`, `ethnicity`                                           |
| `age`       | `age`, `dob`, `yob`, `birth`                                            |
| `geography` | `region`, `state`, `zip`, `zipcode`, `postal`, `country`, `county`, `city`, `location`, `province` |

A column not matched above is treated as a **generic categorical** demographic *only if* its
distinct non-null value count is `2 ≤ n ≤ 20`.

Detection returns, for each kept column, its `name` and `kind` ∈ {`sex`, `race`, `age`,
`geography`, `categorical`}.

After per-dimension analysis, any dimension that exploded into more than `MAX_DIMENSION_GROUPS`
(default **50**) groups is **dropped** as a likely identifier/date column - *except* `geography`,
which legitimately has high cardinality (many cities/regions).

### Manual overrides

Both engines accept an optional `overrides` map (`{column: kind}`) that wins over auto-detection -
for datasets with unusual headers (`gndr`, `patient_region_code`) that the name heuristic misses or
mistypes. A value in {`sex`, `race`, `age`, `geography`, `categorical`} **forces** that column to
that kind regardless of its name; any other value (e.g. `ignore`) **excludes** the column. An
explicitly-forced column is also exempt from the `MAX_DIMENSION_GROUPS` drop above (the user's intent
overrides the heuristic). Surfaced as `faircode profile data.csv --map gndr=sex` in the CLI and as
editable per-column dropdowns in the web profiler.

---

## 2. Age normalization

Age columns come in three shapes - normalize to numeric bands:

- **Numeric** (e.g. `34`): use directly.
- **Interval string** (e.g. `[70-80)`): take the lower bound integer via the first run of digits.
- **Anything else**: treat as categorical (skip numeric handling).

Fixed bands (left-closed): `0–18`, `18–30`, `30–45`, `45–60`, `60–75`, `75+`.
The band shares are then analyzed exactly like a categorical column.

---

## 3. Per-dimension metrics

For a dimension with `k` groups and null-excluded normalized shares `p_1 … p_k` (each `p_i = count_i / N_nonnull`):

- **shares** - the `p_i`, descending, with raw counts.
- **min_share** = `min(p_i)`; **max_share** = `max(p_i)`.
- **imbalance_ratio** = `max_share / min_share` (the most-represented group is this many times the least).
- **entropy_ratio** = `H / ln(k)` where `H = −Σ p_i · ln(p_i)`.
  - Range `[0, 1]`; `1` = perfectly uniform, `0` = all mass in one group.
  - If `k ≤ 1`: `entropy_ratio = 0` (a single-group column has no diversity).
  - Use natural log in both languages (`Math.log` / `math.log`); the log base cancels in the ratio.
- **under_represented** - groups with `p_i < min_share_threshold` (default **0.05**).
- **missing_pct** = `null_count / N_total` for the column.

`dimension_score = round(entropy_ratio × 100)`.

### Numeric-age extra (informational, not scored)
- **skewness** - Fisher–Pearson sample skewness of the raw numeric ages:
  `g1 = (1/N · Σ (x−x̄)³) / (1/N · Σ (x−x̄)²)^1.5`. `null`/`0` if variance is 0 or `N < 3`.

---

## 4. Intersectional gaps (informational, not scored)

Take the **first two** detected demographic dimensions (in detection order). Build their crosstab of
counts. Report every cell whose count is `0` (an absent subgroup) or `< intersection_floor` of total
rows (default **0.01** → "near-empty"). Skip if fewer than two dimensions were detected.

---

## 5. Headline score & grade

```
overall_score = round( mean( dimension_score for every detected dimension ) )   # 0 if none
```

Grade bands:

| Grade | Score   | Meaning                                              |
|:-----:|---------|------------------------------------------------------|
| A     | 85–100  | Well balanced across detected demographics           |
| B     | 70–84   | Mostly balanced, minor under-representation          |
| C     | 55–69   | Noticeable imbalance in one or more dimensions       |
| D     | 40–54   | Strong imbalance / sparse subgroups                  |
| F     | 0–39    | Severe imbalance or single-group dimensions          |

The score intentionally reflects **balance only**. Missing-data %, imbalance ratios, and
intersectional gaps are surfaced as **flags** alongside the score, not folded into it - this keeps
the two engines trivially in sync and the score easy to explain.

---

## 6. Result shape

Both engines produce this structure (keys identical; Python uses a dataclass serialized to the same
dict, JS uses a plain object):

```jsonc
{
  "n_rows": 1340,
  "n_cols": 11,
  "overall_score": 72,
  "grade": "B",
  "dimensions": [
    {
      "name": "gender", "kind": "sex", "n_groups": 2,
      "dimension_score": 99, "entropy_ratio": 0.999,
      "imbalance_ratio": 1.05, "min_share": 0.49, "missing_pct": 0.0,
      "skewness": null,
      "groups": [ {"label": "male", "count": 676, "share": 0.504},
                  {"label": "female", "count": 664, "share": 0.496} ],
      "under_represented": []
    }
  ],
  "intersections": [
    { "dims": ["age_band", "gender"], "cells": [ {"a": "75+", "b": "female", "count": 0} ] }
  ],
  "flags": [ "region: 'southwest' is under-represented (3.1%)", "..." ]
}
```

`flags` is a human-readable list assembled from: every `under_represented` group, every dimension
with `imbalance_ratio ≥ 3`, every dimension with `missing_pct ≥ 0.05`, and every intersectional gap.

---

## 7. Defaults (single place to tune)

| Constant               | Default | Used by                          |
|------------------------|:-------:|----------------------------------|
| `MIN_SHARE_THRESHOLD`  | 0.05    | under-representation flagging    |
| `INTERSECTION_FLOOR`   | 0.01    | near-empty intersection cells    |
| `MAX_CATEGORICAL_CARD` | 20      | generic-categorical detection    |
| `IMBALANCE_FLAG`       | 3.0     | imbalance-ratio flag             |
| `MISSING_FLAG`         | 0.05    | missing-data flag                |
| `AGE_BANDS`            | 0,18,30,45,60,75 | age band edges          |
| `PSI_EPSILON`          | 0.0001  | share floor in PSI (§8)          |
| `PSI_MODERATE`         | 0.10    | PSI ≥ this → moderate drift (§8) |
| `PSI_SIGNIFICANT`      | 0.25    | PSI ≥ this → significant drift (§8) |
| `SCORE_DROP_FLAG`      | 5       | overall-score drop flagged (§8)  |

---

## 8. Dataset comparison (representation drift)

`compare(A, B)` takes two **profile results** - a baseline `A` (e.g. training data) and a
current `B` (e.g. production data) - and reports how each demographic dimension's representation
shifted. It is pure post-processing over two `profile()` outputs, so both engines agree bit-for-bit.
It reads the already-computed group **shares**; it never re-parses the raw rows.

Dimensions are matched by **name**. A dimension present in both is compared; one present only in `B`
is an `added_dimension`, only in `A` a `removed_dimension`.

For a shared dimension, take the **union** of group labels. Each label has `share_a` and `share_b`
(a share of `0` when the label is absent on that side). Per dimension:

- **PSI** (Population Stability Index) - the standard population-drift metric:
  `PSI = Σ (b_i − a_i) · ln(b_i / a_i)`, where `a_i = max(share_a_i, PSI_EPSILON)` and
  `b_i = max(share_b_i, PSI_EPSILON)`. The epsilon floor keeps appeared/disappeared groups finite.
  PSI ≥ 0; larger = more drift.
- **drift_level** from PSI: `none` (`< 0.10`), `moderate` (`0.10 ≤ PSI < 0.25`), `significant` (`≥ 0.25`).
- **TVD** (Total Variation Distance) - an easy-to-read companion: `0.5 · Σ |b_i − a_i|`, range `[0, 1]`.
- **dimension_score_delta** = `dimension_score_b − dimension_score_a`.
- Per group: `share_a`, `share_b`, `share_delta = share_b − share_a`, and a `status` of
  `appeared` (`a = 0, b > 0`), `disappeared` (`a > 0, b = 0`), or `shifted`. Groups are ordered by
  **descending `|share_delta|`**, then label ascending (deterministic tie-break, both engines agree).

Top level: `score_delta = overall_score_b − overall_score_a`. `flags` is assembled from: an
overall-score drop of `≥ SCORE_DROP_FLAG` points, every dimension whose `drift_level ≠ none`, every
`appeared`/`disappeared` group, and every added/removed dimension.

### Result shape

```jsonc
{
  "a": { "name": "train.csv", "n_rows": 5000, "overall_score": 78, "grade": "B" },
  "b": { "name": "prod.csv",  "n_rows": 4200, "overall_score": 61, "grade": "C" },
  "score_delta": -17,
  "dimensions": [
    {
      "name": "race", "kind": "race",
      "dimension_score_a": 82, "dimension_score_b": 55, "dimension_score_delta": -27,
      "psi": 0.3412, "tvd": 0.21, "drift_level": "significant",
      "groups": [
        { "label": "White", "share_a": 0.60, "share_b": 0.81, "share_delta": 0.21, "status": "shifted" },
        { "label": "Asian", "share_a": 0.10, "share_b": 0.0,  "share_delta": -0.10, "status": "disappeared" }
      ]
    }
  ],
  "added_dimensions": ["income_bracket"],
  "removed_dimensions": [],
  "flags": [ "race: significant representation drift (PSI 0.34)", "race: 'Asian' disappeared (10.0% → 0.0%)" ]
}
```

Rounding uses the same half-up helper as the rest of the spec (`Math.round` / `floor(x·f + 0.5)`):
`psi`, `tvd`, and the share fields to 4 dp; score deltas are integers.
