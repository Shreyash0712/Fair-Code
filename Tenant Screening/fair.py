import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from faircode.significance import significance_report

# 1. Load the dataset (same tenant-screening framing as unfair.py)
df = pd.read_csv(Path(__file__).parent / 'tenant-screening-data.csv')
df = df[df['Recidivism_Within_3years'].notna()].copy()
df = df[df['Race'].isin(['BLACK', 'WHITE'])]
df['race_binary'] = df['Race'].map({'BLACK': 1, 'WHITE': 0})
df['is_flagged'] = df['Recidivism_Within_3years'].astype(int)

# 2. THE FIX: drop Race AND every criminal-history / housing proxy.
#
#   Prior_Arrest_Episodes_*    removed - arrest counts track over-policing, not race-neutral risk
#   Prior_Conviction_Episodes_* removed - conviction history carries the same racial signal
#   Gang_Affiliated            removed - a criminal-record label that proxies for race
#   Residence_Changes          removed - housing instability standing in for eviction history
#   race_binary                removed - the protected attribute itself
#
# We keep only features a screener could defend as non-criminal-history signal.
legit_features = [
    'Gender',
    'Age_at_Release',
    'Education_Level',
    'Prison_Offense',
    'Prison_Years',
    'Percent_Days_Employed',
    'Dependents',
    'Supervision_Risk_Score_First',
]

X = pd.get_dummies(df[legit_features])
y = df['is_flagged']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train the fair model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Measure the final gap (re-attach race only for measurement, never for training)
test_results = X_test.copy()
test_results['race_binary'] = df.loc[X_test.index, 'race_binary']
test_results['prediction'] = model.predict(X_test)

black_pred = test_results[test_results['race_binary'] == 1]['prediction']
white_pred = test_results[test_results['race_binary'] == 0]['prediction']
black_rate = black_pred.mean()
white_rate = white_pred.mean()

sig = significance_report(black_pred, white_pred)

print(f"--- MITIGATED (UNBIASED) RESULTS ---")
print()
print(f"Black Applicant High-Risk Flag Rate: {black_rate:.2%}")
print(f"White Applicant High-Risk Flag Rate: {white_rate:.2%}")
print()
print(f"New Fairness Gap: {sig['gap']:.2%}")
print(f"95% CI: [{sig['ci_low']:.2%}, {sig['ci_high']:.2%}] (bootstrap, n=10,000 resamples)")
print(f"Permutation test p-value: {sig['p_value']:.4f} "
      f"({'statistically significant' if sig['significant'] else 'not statistically significant'} at α=0.05)")
if sig['small_sample_warning']:
    print(f"Small-sample warning: n={sig['n_a']} vs {sig['n_b']} (<30) - interpret with caution")
