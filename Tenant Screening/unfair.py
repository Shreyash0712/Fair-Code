import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from faircode.significance import significance_report

# 1. Load the dataset
# Real tenant-screening companies buy criminal-history / recidivism-risk scores
# like this one to flag rental applicants. We treat Recidivism_Within_3years as
# the "risk flag" a background-check algorithm would hand to a landlord.
df = pd.read_csv(Path(__file__).parent / 'tenant-screening-data.csv')

# The original NIJ challenge withholds the label on its test split, so drop the
# unlabelled rows before training.
df = df[df['Recidivism_Within_3years'].notna()].copy()

# 2. Focus on the clear Black vs White comparison
df = df[df['Race'].isin(['BLACK', 'WHITE'])]
df['race_binary'] = df['Race'].map({'BLACK': 1, 'WHITE': 0})

# 3. Target: 1 = flagged as high-risk (would-be-denied applicant)
df['is_flagged'] = df['Recidivism_Within_3years'].astype(int)

# 4. Prepare features (INCLUDE Race and the criminal-history / housing proxies)
proxy_features = [
    'Prior_Arrest_Episodes_Felony',
    'Prior_Arrest_Episodes_Violent',
    'Prior_Arrest_Episodes_Property',
    'Prior_Arrest_Episodes_Drug',
    'Prior_Arrest_Episodes_GunCharges',
    'Prior_Conviction_Episodes_Felony',
    'Prior_Conviction_Episodes_Viol',
    'Prior_Conviction_Episodes_Prop',
    'Prior_Conviction_Episodes_Drug',
    'Prior_Conviction_Episodes_GunCharges',
    'Gang_Affiliated',       # criminal record as a proxy for race
    'Residence_Changes',     # housing instability as a stand-in for eviction history
]
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

X = pd.get_dummies(df[['race_binary'] + proxy_features + legit_features])
y = df['is_flagged']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train and check the gap
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

test_results = X_test.copy()
test_results['prediction'] = model.predict(X_test)

black_pred = test_results[test_results['race_binary'] == 1]['prediction']
white_pred = test_results[test_results['race_binary'] == 0]['prediction']
black_rate = black_pred.mean()
white_rate = white_pred.mean()

sig = significance_report(black_pred, white_pred)

print(f"--- BIASED MODEL RESULTS ---")
print()
print(f"Black Applicant High-Risk Flag Rate: {black_rate:.2%}")
print(f"White Applicant High-Risk Flag Rate: {white_rate:.2%}")
print()
print(f"Fairness Gap: {sig['gap']:.2%}")
print(f"95% CI: [{sig['ci_low']:.2%}, {sig['ci_high']:.2%}] (bootstrap, n=10,000 resamples)")
print(f"Permutation test p-value: {sig['p_value']:.4f} "
      f"({'statistically significant' if sig['significant'] else 'not statistically significant'} at α=0.05)")
if sig['small_sample_warning']:
    print(f"Small-sample warning: n={sig['n_a']} vs {sig['n_b']} (<30) - interpret with caution")
