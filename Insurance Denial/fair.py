import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from faircode.significance import significance_report, intersectional_report

# ============================================================
# INSURANCE DENIAL BIAS AUDIT - FAIR MODEL
# Dataset: Insurance Claim Analysis: Demographic & Health
# https://www.kaggle.com/datasets/thedevastator/insurance-claim-analysis-demographic-and-health
#
# Protected attributes removed: age, gender
# Proxy variables removed:      bmi, smoker, diabetic
#
# Retained: only features that reflect documented policy
# context - not who the person is or proxies for their
# race, class, or protected status.
# ============================================================

df = pd.read_csv(Path(__file__).parent / 'insurance.csv')

# Same binarization threshold as unfair.py - valid comparison.
median_charge = df['claim'].median()
y = (df['claim'] > median_charge).astype(int)

df['age_group'] = df['age'].apply(lambda x: 'Young (<35)' if x < 35 else 'Older (35+)')

# ── THE FIX: Policy signals only ────────────────────────────
X = pd.get_dummies(df[[
    'bloodpressure', # objective clinical measurement
    'children',      # number of dependants - policy-level fact
    'region',        # geographic region - policy-level factor
    # age      removed ✓  (protected attribute)
    # gender   removed ✓  (protected attribute)
    # bmi      removed ✓  (proxy: encodes race via population BMI distributions)
    # smoker   removed ✓  (proxy: encodes income/class → race)
    # diabetic removed ✓  (proxy: diagnosis rates differ 60–100% by race)
]])

# ── TRAIN FAIR MODEL ─────────────────────────────────────────
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
print("FAIR MODEL - RESULTS")
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
# Same cross as unfair.py, so the mitigation can be judged on the
# compounded gap too - proxy removal may close the marginal gaps
# without closing the intersectional one.
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
print("WHAT CHANGED")
print("=" * 60)
print("""
THE FIX: Drop the protected attributes AND their proxies.

  age      → removed. Age is a protected characteristic.
              Young patients were flagged at higher rates
              not because of medical risk, but because
              age itself was a training signal.

  gender   → removed. Gender discrimination in insurance
              is illegal under the ACA. Removing it
              eliminates the channel through which the
              model learned to penalise women.

  bmi      → removed. BMI is not an independent health
              signal - it is partially a function of race,
              ethnicity, and socioeconomic status. A model
              that penalises high BMI is partially
              penalising race, regardless of whether
              "race" appears anywhere in the feature list.

  smoker   → removed. Smoking rates correlate with income
              and education. Including smoker status allows
              the model to encode class (and by extension
              racial) signal through an apparently neutral
              variable.

  diabetic → removed. Black and Hispanic Americans are
              diagnosed diabetic at 60–100% higher rates.
              Using diabetic status as a feature encodes
              racial disparities in healthcare access and
              diagnosis rates - not individual health risk.

Key Insight: Insurance AI models don't need to name race
to discriminate by race. BMI, smoking, and diabetic status
are the CustodyStatus of health insurance - clinical-
sounding features that carry protected-class signal because
of structural inequalities baked into American healthcare.
""")