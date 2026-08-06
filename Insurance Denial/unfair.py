import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from faircode.significance import significance_report, intersectional_report

# ============================================================
# INSURANCE DENIAL BIAS AUDIT - BIASED MODEL
# Dataset: Insurance Claim Analysis: Demographic & Health
# https://www.kaggle.com/datasets/thedevastator/insurance-claim-analysis-demographic-and-health
#
# Protected attributes included: age, gender
# Proxy variables included:      bmi, smoker, diabetic
#
# BMI is a documented proxy for race - Black and Hispanic
# Americans are flagged as "obese" at higher rates due to
# population-level differences, not individual health risk.
# Smoker status correlates with income and education, which
# themselves correlate with race and class.
# Diabetic status correlates with race (Black and Hispanic
# Americans are diagnosed at 60–100% higher rates), encoding
# racial signal through an apparently clinical variable.
# ============================================================

df = pd.read_csv(Path(__file__).parent / 'insurance.csv')

# Binarize continuous claim charges at the median.
# Above median = high-cost claim (flagged for denial/review).
# At or below  = approved claim.
# Same threshold used in fair.py for a valid comparison.
median_charge = df['claim'].median()
y = (df['claim'] > median_charge).astype(int)

# Define age groups for fairness measurement
df['age_group'] = df['age'].apply(lambda x: 'Young (<35)' if x < 35 else 'Older (35+)')

# ── BIASED FEATURES ─────────────────────────────────────────
# age and gender are protected attributes.
# bmi      proxy: population BMI distributions differ by race;
#                 penalising high BMI penalises race.
# smoker   proxy: smoking rates correlate with poverty → race/class.
# diabetic proxy: Black and Hispanic Americans are diagnosed
#                 diabetic at 60–100% higher rates, encoding
#                 racial signal through a clinical label.
X = pd.get_dummies(df[[
    'age',          # protected attribute
    'gender',       # protected attribute
    'bmi',          # proxy: correlated with race via population BMI distributions
    'bloodpressure',
    'diabetic',     # proxy: diagnosis rates differ significantly by race
    'children',
    'smoker',       # proxy: correlated with income → race/class
    'region',
]])

# ── PROXY VARIABLE ANALYSIS ──────────────────────────────────
print("=" * 60)
print("PROXY VARIABLE ANALYSIS")
print("=" * 60)
print("\nBMI distribution by age group:")
print(df.groupby('age_group')['bmi'].mean().round(2))

smoker_age = pd.crosstab(df['smoker'], df['age_group'], normalize='columns').round(3)
print("\nSmoker rates by age group:")
print(smoker_age)

diabetic_age = pd.crosstab(df['diabetic'], df['age_group'], normalize='columns').round(3)
print("\nDiabetic rates by age group:")
print(diabetic_age)
print()

# ── TRAIN BIASED MODEL ───────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))

# ── MEASURE FAIRNESS GAP ─────────────────────────────────────
df_test = X_test.copy()
df_test['age_group'] = df.loc[X_test.index, 'age_group'].values
df_test['gender']    = df.loc[X_test.index, 'gender'].values
df_test['prediction'] = model.predict(X_test)

age_approval    = df_test.groupby('age_group')['prediction'].mean()
gender_approval = df_test.groupby('gender')['prediction'].mean()

print("=" * 60)
print("BIASED MODEL - RESULTS")
print("=" * 60)
print(f"\nModel Accuracy: {accuracy:.2%}\n")

print("── High-Cost Claim Flag Rate by Age Group ────────────")
for group, rate in age_approval.items():
    print(f"  {group:<20} {rate:.2%}")
age_sig = significance_report(
    df_test[df_test['age_group'] == 'Older (35+)']['prediction'],
    df_test[df_test['age_group'] == 'Young (<35)']['prediction'],
)
print(f"\n  Fairness Gap (Age):    {age_sig['gap']:.2%}")
print(f"  95% CI: [{age_sig['ci_low']:.2%}, {age_sig['ci_high']:.2%}] (bootstrap, n=10,000 resamples)")
print(f"  Permutation p-value:   {age_sig['p_value']:.4f} "
      f"({'significant' if age_sig['significant'] else 'not significant'} at α=0.05)")
if age_sig['small_sample_warning']:
    print(f"  Small-sample warning: n={age_sig['n_a']} vs {age_sig['n_b']} (<30)")

print("\n── High-Cost Claim Flag Rate by Gender ───────────────")
for group, rate in gender_approval.items():
    print(f"  {group:<20} {rate:.2%}")
gender_sig = significance_report(
    df_test[df_test['gender'] == 'male']['prediction'],
    df_test[df_test['gender'] == 'female']['prediction'],
)
print(f"\n  Fairness Gap (Gender): {gender_sig['gap']:.2%}")
print(f"  95% CI: [{gender_sig['ci_low']:.2%}, {gender_sig['ci_high']:.2%}] (bootstrap, n=10,000 resamples)")
print(f"  Permutation p-value:   {gender_sig['p_value']:.4f} "
      f"({'significant' if gender_sig['significant'] else 'not significant'} at α=0.05)")
if gender_sig['small_sample_warning']:
    print(f"  Small-sample warning: n={gender_sig['n_a']} vs {gender_sig['n_b']} (<30)")

# ── INTERSECTIONAL GAP: Young × Female ───────────────────────
# Age and gender each report a marginal gap above; crossing them
# checks the doubly-disadvantaged cell (young women) against the
# baseline (older men) to see if the harm compounds.
inter = intersectional_report(
    df_test['prediction'],
    df_test['age_group'] == 'Young (<35)',   # disadvantaged side of age
    df_test['gender'] == 'female',           # disadvantaged side of gender
)
isr = inter['intersectional']
marg_sum = abs(inter['gap_a_alone']) + abs(inter['gap_b_alone'])
print("\n── Intersectional: Young × Female ────────────────────")
print(f"  {'Both (young women)':<25}: {inter['cell_rates']['both']:.2%}  (n={inter['cell_sizes']['both']})")
print(f"  {'Neither (baseline)':<25}: {inter['cell_rates']['neither']:.2%}  (n={inter['cell_sizes']['neither']})")
print(f"  {'Marginal gap (age alone)':<25}: {inter['gap_a_alone']:.2%}")
print(f"  {'Marginal gap (sex alone)':<25}: {inter['gap_b_alone']:.2%}")
print(f"  {'Intersectional gap':<25}: {isr['gap']:.2%}  [CI: {isr['ci_low']:.2%}, {isr['ci_high']:.2%}]  "
      f"p={isr['p_value']:.4f} ({'significant' if isr['significant'] else 'not significant'})")
if inter['superadditive']:
    print(f"  Superadditive: yes - compounded gap exceeds the sum of marginal gaps ({marg_sum:.2%})")
else:
    print(f"  Superadditive: no - compounded gap is within the sum of marginal gaps ({marg_sum:.2%})")
if isr['small_sample_warning']:
    print(f"  Small-sample warning: doubly-disadvantaged cell n={isr['n_a']} vs baseline n={isr['n_b']} (<30)")

print("\n" + "=" * 60)
print("WHAT'S WRONG")
print("=" * 60)
print("""
This model includes age and gender as direct inputs - protected
attributes under the ACA and anti-discrimination law.

It also includes three proxy variables:

  BMI      → population-level BMI distributions differ by
              race/ethnicity. Flagging high BMI as a risk
              factor disproportionately penalises Black and
              Hispanic patients independent of actual health
              outcomes.

  Smoker   → smoking rates are inversely correlated with
              income and education. Income and education are
              themselves correlated with race and class.
              'Smoker' smuggles socioeconomic signal -
              and therefore racial signal - back into the
              model even if race is never named.

  Diabetic → Black and Hispanic Americans are diagnosed with
              diabetes at 60–100% higher rates than white
              Americans. A model that treats diabetic status
              as a risk factor is partially encoding race
              through a clinical label.

Run fair.py to see the fix.
""")