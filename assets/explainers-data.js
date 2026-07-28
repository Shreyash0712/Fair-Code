window.FAIR_CODE_EXPLAINERS = [
  {
    "slug": "proxy-variables",
    "title": "Proxy Variables",
    "subtitle": "Why removing race alone does not remove bias.",
    "summary": "Learn how correlated features like zip code, custody status, and employment history can smuggle protected attributes back into a model.",
    "tags": [
      "detection",
      "data",
      "explainability"
    ]
  },
  {
    "slug": "equalized-odds",
    "title": "Equalized Odds",
    "subtitle": "A fairness metric that checks error rates, not just accuracy.",
    "summary": "See how equalized odds compares true positive and false positive rates across groups and why that matters in high-stakes systems.",
    "tags": [
      "metrics"
    ]
  },
  {
    "slug": "sampling-bias",
    "title": "Sampling Bias",
    "subtitle": "When your dataset does not reflect the world it claims to describe.",
    "summary": "Understand how under-sampling, over-sampling, and skewed collection pipelines can distort what a model learns.",
    "tags": [
      "data"
    ]
  },
  {
    "slug": "shap-values",
    "title": "SHAP Values",
    "subtitle": "Explain model decisions feature by feature.",
    "summary": "Use SHAP to trace which inputs pushed a prediction up or down, and where explanation can still be misleading.",
    "tags": [
      "explainability"
    ]
  },
  {
    "slug": "disparate-impact",
    "title": "Disparate Impact",
    "subtitle": "When outcomes differ even without explicit intent.",
    "summary": "Measure whether a model or policy produces unequal results across groups, even when the protected attribute is hidden.",
    "tags": [
      "metrics"
    ]
  },
  {
    "slug": "disparate-treatment",
    "title": "Disparate Treatment",
    "subtitle": "Direct discrimination instead of proxy discrimination.",
    "summary": "Look at the difference between explicitly using protected attributes and indirectly encoding them through features.",
    "tags": [
      "metrics",
      "detection"
    ]
  },
  {
    "slug": "fairness-metric-conflicts",
    "title": "Fairness Metric Conflicts",
    "subtitle": "Why one fairness definition often breaks another.",
    "summary": "Understand the trade-offs between demographic parity, calibration, and equalized odds before choosing a metric.",
    "tags": [
      "metrics"
    ]
  },
  {
    "slug": "calibration",
    "title": "Calibration",
    "subtitle": "When a model score actually means what it says.",
    "summary": "Check whether predicted probabilities match real-world frequencies across groups and where calibration can still fail.",
    "tags": [
      "metrics"
    ]
  },
  {
    "slug": "demographic-parity",
    "title": "Demographic Parity",
    "subtitle": "Equal positive rates across groups.",
    "summary": "Learn when demographic parity is useful, where it breaks down, and why it can conflict with other fairness goals.",
    "tags": [
      "metrics"
    ]
  },
  {
    "slug": "feedback-loop-bias",
    "title": "Feedback Loop Bias",
    "subtitle": "Bias that gets stronger after deployment.",
    "summary": "See how model outputs feed back into future data and amplify unfairness over time.",
    "tags": [
      "data"
    ]
  },
  {
    "slug": "label-bias",
    "title": "Label Bias",
    "subtitle": "When the target itself is already skewed.",
    "summary": "Explore how historical decisions, biased raters, and unequal reporting can corrupt your labels before training even starts.",
    "tags": [
      "data"
    ]
  },
  {
    "slug": "individual-fairness",
    "title": "Individual Fairness",
    "subtitle": "Similar people should get similar outcomes.",
    "summary": "Understand the promise and difficulty of fairness definitions that focus on person-by-person consistency.",
    "tags": [
      "metrics"
    ]
  },
  {
    "slug": "counterfactual-fairness",
    "title": "Counterfactual Fairness",
    "subtitle": "Would the outcome change if identity changed?",
    "summary": "Use counterfactual reasoning to ask whether a model would behave differently under a hypothetical protected attribute.",
    "tags": [
      "explainability"
    ]
  },
  {
    "slug": "neural-networks",
    "title": "Neural Networks",
    "subtitle": "How complex models can hide simple bias.",
    "summary": "Break down how layered models learn patterns, why they are hard to inspect, and why fairness audits matter even more.",
    "tags": [
      "explainability"
    ]
  },
  {
    "slug": "ai-hallucinations",
    "title": "AI Hallucinations",
    "subtitle": "Confident outputs that are still wrong.",
    "summary": "See how hallucinations interact with bias, why they are dangerous, and how to spot them in practice.",
    "tags": [
      "explainability"
    ]
  },
  {
    "slug": "reinforcement-learning",
    "title": "Reinforcement Learning",
    "subtitle": "When reward signals shape real-world policy.",
    "summary": "Learn how RL-style systems can reinforce unfair incentives in recommendation, pricing, and risk scoring.",
    "tags": [
      "explainability",
      "data"
    ]
  },
  {
    "slug": "proxy-entanglement",
    "title": "Proxy Entanglement",
    "subtitle": "When proxies form clusters instead of single features.",
    "summary": "Explore how correlated proxy bundles can keep bias alive even after individual features are removed.",
    "tags": [
      "detection",
      "data",
      "explainability"
    ]
  },
  {
    "slug": "ml-bias",
    "title": "What Is Machine Learning Bias?",
    "subtitle": "Four entry points. One pipeline. Measurable everywhere.",
    "summary": "Understand how bias enters AI systems through training data, labels, proxy variables, and feedback loops - with detection code and real examples from every audit in this repo.",
    "tags": [
      "detection",
      "data",
      "explainability"
    ]
  },
  {
    "slug": "data-leakage",
    "title": "What Is Data Leakage?",
    "subtitle": "When the model has already seen the answer sheet.",
    "summary": "Data leakage contaminates a model's training signal with information unavailable at deployment, producing evaluation scores that overstate real-world performance. Learn to identify target leakage and train-test contamination - and detect both before they ship.",
    "tags": [
      "data",
      "detection"
    ]
  },
  {
    "slug": "how-ai-detects-patterns",
    "title": "How AI Detects Patterns",
    "subtitle": "A model can't tell a cause from a proxy",
    "summary": "Learn how a Random Forest finds patterns through splits, tree aggregation, and feature importance. See why a high importance score means reliance, not justification.",
    "tags": [
      "explainability"
    ]
  },
  {
    "slug": "distribution-shift",
    "title": "Distribution Shift",
    "subtitle": "A fairness audit is only valid for the data it was run on",
    "summary": "Learn why a model that passes a bias audit at launch can drift back into bias as the population it serves changes over time. Covers covariate shift, label shift, and concept drift, with detection code for monitoring both.",
    "tags": [
      "data",
      "detection"
    ]
  },
  {
    "slug": "ai-objectivity-myth",
    "title": "The Biggest Myth About AI Objectivity",
    "subtitle": "\"It's just math\" is not a defense",
    "summary": "Learn why statistical models trained on biased history reproduce that bias regardless of intent. See how COMPAS's \"neutral\" risk score hid an 86.77% fairness gap until the right proxies were found.",
    "tags": [
      "data",
      "explainability"
    ]
  },
  {
    "slug": "confounding-variable",
    "title": "Confounding Variable",
    "subtitle": "When a hidden cause makes two things look connected.",
    "summary": "Learn how a third variable that independently causes both a feature and an outcome creates spurious correlations that survive protected-attribute removal. See why COMPAS stayed biased after race was dropped - until the confounder was removed too.",
    "tags": [
      "detection",
      "data"
    ]
  },
  {
    "slug": "predictive-parity",
    "title": "Predictive Parity",
    "subtitle": "Equally trustworthy is not the same as equally fair",
    "summary": "Learn why Positive Predictive Value equal across groups is a real fairness property, and why the 2016 ProPublica vs Northpointe COMPAS dispute shows it can hold while one group absorbs a much higher false-positive rate.",
    "tags": [
      "metrics",
      "detection"
    ]
  },
  {
    "slug": "false-positives-vs-false-negatives",
    "title": "False Positives vs. False Negatives in Medical Risk Models",
    "subtitle": "When a missed high-risk flag costs more than a false alarm",
    "summary": "Learn why a single accuracy or AUC number can hide two very different kinds of mistakes, and why a missed diagnosis and a false alarm are almost never equally costly. See how one global decision threshold can produce equal overall accuracy while still leaving very different false negative rates across demographic groups.",
    "tags": [
      "metrics",
      "detection"
    ]
  },
  {
    "slug": "supervised-learning",
    "title": "What Is Supervised Learning?",
    "subtitle": "Teaching a model to reproduce exactly what it was shown",
    "summary": "See how a model turns labeled examples into a decision rule by walking through the AI Fair Recruitment audit's train/test split and fit step directly. Includes detection code that compares the gap in a dataset's labels against the gap in a trained model's own predictions.",
    "tags": [
      "explainability",
      "data"
    ]
  },
  {
    "slug": "unsupervised-learning",
    "title": "What Is Unsupervised Learning?",
    "subtitle": "It found the split on its own, because the split was already in the data",
    "summary": "See how k-means clustering on the Benefits Denial dataset recovers a strong sex split (89.3% male in one cluster) and a real race split without sex, race, or national origin ever being part of the feature set. Includes detection code that clusters on non-protected features, then checks the result for demographic skew.",
    "tags": [
      "detection",
      "explainability"
    ]
  },
  {
    "slug": "model-drift",
    "title": "What Is Model Drift?",
    "subtitle": "A fairness audit is a photograph of a moving room",
    "summary": "Learn why a fairness gap measured once at launch is not guaranteed to hold months later, and how rolling-window monitoring catches the drift a single audit snapshot misses. Re-measures the German Credit Lending age gap across five sequential windows (4.3%-15.1%) with PSI and a Page-Hinkley change-point test as detection code.",
    "tags": [
      "detection",
      "data"
    ]
  },
  {
    "slug": "selection-bias",
    "title": "What Is Selection Bias?",
    "subtitle": "A dataset does not remember the people who were turned away before it was collected.",
    "summary": "Learn why the process that decides whether someone enters a dataset at all can bias a model before any protected attribute or proxy is even considered. See why the German Credit Lending dataset's 700/300 good/bad split contains zero rejected applicants, and why that reject-inference gap survives Audit 03's proxy-variable fix untouched. Includes a Berkson's-paradox simulation as detection code.",
    "tags": [
      "data",
      "detection"
    ]
  },
  {
    "slug": "automation-bias",
    "title": "What Is Automation Bias?",
    "subtitle": "When humans defer to algorithms, bias gets automated too.",
    "summary": "Understand why judges, recruiters, and clinicians follow AI scores even when they know the scores are biased - and how automation bias amplifies disparities beyond what the model alone produces. Includes detection code measuring disparity amplification in human-in-the-loop decisions, mitigation strategies, and the COMPAS courtroom case study.",
    "tags": [
      "detection",
      "metrics",
      "explainability"
    ]
  },
  {
    "slug": "roc-curve-auc",
    "title": "What Is a ROC Curve and AUC?",
    "subtitle": "Why one threshold-free score can look great and still be unfair.",
    "summary": "Learn what a ROC curve and its area (AUC) actually measure - the model's ability to rank cases by risk - and why that single headline number hides the two things fairness depends on: where you set the decision threshold, and whether ranking quality is equal across groups. See how COMPAS's ordinary 0.68 baseline AUC (frozen from paper/results-frozen) sat on top of a large racial false-positive gap. Includes detection code for per-group AUC and overlaid ROC curves.",
    "tags": [
      "metrics",
      "detection"
    ]
  },
  {
    "slug": "class-imbalance",
    "title": "What Is Class Imbalance?",
    "subtitle": "When a 99% accuracy score just means the model ignored the 1% that mattered.",
    "summary": "Learn why skewed positive/negative ratios wreck naive accuracy and disproportionately hurt minority subgroups, and how common fixes (oversampling, undersampling, SMOTE, class weights) can either help or introduce new bias.",
    "tags": [
      "data",
      "metrics",
      "detection"
    ]
  },
  {
    "slug": "bias-variance-tradeoff",
    "title": "What Is the Bias-Variance Trade-off?",
    "subtitle": "Why an overfit model can memorize the majority and fail the minority.",
    "summary": "Learn the difference between statistical bias and societal bias, and see how the classic trade-off between underfitting and overfitting impacts fairness across demographic groups.",
    "tags": [
      "detection",
      "explainability",
      "data"
    ]
  },
  {
    "slug": "confusion-matrix",
    "title": "What Is a Confusion Matrix?",
    "subtitle": "The foundational building block behind most fairness metrics.",
    "summary": "Learn how a confusion matrix breaks down accuracy into true positives, true negatives, false positives, and false negatives, and why derived metrics like FPR and FNR are essential for detecting bias.",
    "tags": [
      "metrics",
      "explainability"
    ]
  },
  {
    "slug": "protected-attribute",
    "title": "What Is a Protected Attribute?",
    "subtitle": "Why removing race from a dataset does not remove the bias.",
    "summary": "Learn what a protected attribute is, how the law recognizes it, and why the \"fairness through unawareness\" approach fails by hiding the bias behind proxies.",
    "tags": [
      "data",
      "explainability",
      "detection"
    ]
  },
  {
    "slug": "accuracy-not-enough-healthcare-ai",
    "title": "Why Accuracy Is Not Enough in Healthcare AI",
    "subtitle": "A 95% accurate model can still miss the sickest patients in one group.",
    "summary": "Learn why a high accuracy number can hide a model that systematically fails the patients who matter most. Covers the accuracy paradox on rare clinical outcomes (a 'predict nothing' model scoring 97% while catching zero at-risk patients), why a single aggregate score masks per-group recall and false-negative gaps, and why in medicine a missed case and a false alarm are never equally costly. Anchored to the Healthcare Readmission audit and the Obermeyer et al. (2019) study, with per-group accuracy-vs-recall detection code.",
    "tags": [
      "metrics",
      "detection"
    ]
  }
];
