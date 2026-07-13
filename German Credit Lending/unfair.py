import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from faircode.significance import significance_report

# Load dataset
# Source: German Credit Risk dataset
# https://www.kaggle.com/datasets/ppb00x/credit-risk-customers
df = pd.read_csv(Path(__file__).parent / 'credit_customers.csv')

# Target: 1 = good credit, 0 = bad credit
df['target'] = (df['class'] == 'good').astype(int)

# Protected attribute: age
# Young applicants (<30) are flagged as bad credit at a significantly higher
# rate than older applicants despite equivalent financial profiles.
df['is_young'] = (df['age'] < 30).astype(int)

# Encode categorical columns
cat_cols = [
    'checking_status', 'credit_history', 'purpose', 'savings_status',
    'employment', 'personal_status', 'other_parties', 'property_magnitude',
    'other_payment_plans', 'housing', 'job', 'own_telephone', 'foreign_worker'
]
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Features - INCLUDES protected attribute (age) and proxy (employment)
# employment is a proxy for age: young applicants have <1yr employment at
# 27.2% vs only 11.3% for older applicants - the model learns age through tenure.
features = [
    'checking_status',
    'duration',
    'credit_history',
    'purpose',
    'credit_amount',
    'savings_status',
    'employment',           # proxy variable for age
    'installment_commitment',
    'personal_status',
    'other_parties',
    'residence_since',
    'property_magnitude',
    'age',                  # protected attribute
    'other_payment_plans',
    'housing',
    'existing_credits',
    'job',
    'num_dependents',
    'own_telephone',
    'foreign_worker',
]

X = df[features]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
results = X_test.copy()
results['pred'] = predictions
results['is_young'] = df.loc[X_test.index, 'is_young']

young_pred = results[results['is_young'] == 1]['pred']
older_pred = results[results['is_young'] == 0]['pred']
young_rate = young_pred.mean() * 100
older_rate = older_pred.mean() * 100

sig = significance_report(older_pred, young_pred)

print("--- BIASED MODEL RESULTS ---")
print()
print(f"Older Applicants (30+) Good Credit Rate: {older_rate:.2f}%")
print(f"Young Applicants (<30) Good Credit Rate: {young_rate:.2f}%")
print()
print(f"Fairness Gap: {sig['gap']:.2%}")
print(f"95% CI: [{sig['ci_low']:.2%}, {sig['ci_high']:.2%}] (bootstrap, n=10,000 resamples)")
print(f"Permutation test p-value: {sig['p_value']:.4f} "
      f"({'statistically significant' if sig['significant'] else 'not statistically significant'} at α=0.05)")
if sig['small_sample_warning']:
    print(f"Small-sample warning: n={sig['n_a']} vs {sig['n_b']} (<30) - interpret with caution")