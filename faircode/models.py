"""The three model families - Layer 2 of the benchmark harness.

Fixed hyperparameters and a shared random_state, so a fairness-metric
difference between two runs reflects the mitigation strategy, not an
uncontrolled modelling choice. Every factory returns a scikit-learn
estimator, so callers get scikit-learn's own uniform fit/predict/
predict_proba interface for free - no wrapper class needed.

Ordinal (label-encoded) categoricals suit the two tree ensembles natively.
Logistic regression treats them as numeric/ordinal too, which is an
imperfect fit for unordered categories - a known, documented trade-off in
favour of one feature-encoding path shared by every model family and audit
(see faircode.strategies.encode_features).
"""

from __future__ import annotations

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

MODEL_FAMILIES = {
    "logistic_regression": lambda random_state: LogisticRegression(
        max_iter=1000, random_state=random_state),
    "random_forest": lambda random_state: RandomForestClassifier(
        n_estimators=100, random_state=random_state),
    "gradient_boosting": lambda random_state: GradientBoostingClassifier(
        random_state=random_state),
}


def build_model(model_name: str, random_state: int):
    """Construct a fresh, unfit estimator for `model_name` (a key of MODEL_FAMILIES)."""
    return MODEL_FAMILIES[model_name](random_state)
