"""
Day 2 - Modeling & Tuning
Run with:  python src/train.py   (from the week8_project/ folder)

Produces:
  - a baseline score (DummyClassifier) printed to console
  - model_comparison.csv (Logistic Regression vs Random Forest, 5-fold CV)
  - models/final_model.pkl - the FULL fitted pipeline (preprocessing + model)
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline

from pipeline import build_preprocessor, NUMERIC, CATEGORICAL, TARGET

df = pd.read_csv('data/clean_dataset.csv')
X = df[NUMERIC + CATEGORICAL]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ---------------------------------------------------------------------
# Task 2.1 - Baseline first. If a real model can't beat this, stop and
# rethink before tuning anything.
# is_absent is ~90/10 imbalanced, so a "predict majority" baseline will
# already look deceptively high on accuracy - that's exactly why it's
# tracked here explicitly, not skipped.
# ---------------------------------------------------------------------
dummy = DummyClassifier(strategy='most_frequent')
dummy.fit(X_train, y_train)
print(f'Baseline accuracy (always predict majority): {dummy.score(X_test, y_test):.3f}')

# ---------------------------------------------------------------------
# Task 2.2 - Compare candidates with cross-validation. Preprocessing
# lives INSIDE the Pipeline so it's refit on every fold - no leakage.
# ---------------------------------------------------------------------
preprocessor = build_preprocessor()

candidates = {
    'Logistic Regression': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42,
                                             class_weight='balanced'),
}

results = []
for name, clf in candidates.items():
    pipe = Pipeline([('prep', preprocessor), ('model', clf)])
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='f1')
    results.append({'Model': name, 'CV F1 mean': scores.mean(), 'CV F1 std': scores.std()})
    print(f'{name}: F1 = {scores.mean():.3f} (+/- {scores.std():.3f})')

comparison_df = pd.DataFrame(results)
comparison_df.to_csv('model_comparison.csv', index=False)
print('\nSaved model_comparison.csv')

# ---------------------------------------------------------------------
# Task 2.3 - Tune the ACTUAL winner from the comparison above, not
# whichever model looks fancier. Here Logistic Regression clearly beat
# Random Forest on CV F1 (Random Forest scored 0.0 - with only ~35
# absences total and no-leakage features, it never learned to predict
# the minority class at all), so that's what gets tuned.
# ---------------------------------------------------------------------
param_grid = {
    'model__C': [0.01, 0.1, 1, 10],
}

best_pipe = Pipeline([
    ('prep', build_preprocessor()),
    ('model', LogisticRegression(max_iter=1000, class_weight='balanced')),
])

grid = GridSearchCV(best_pipe, param_grid, cv=5, scoring='f1', n_jobs=-1)
grid.fit(X_train, y_train)

print(f'\nBest params: {grid.best_params_}')
print(f'Best CV F1: {grid.best_score_:.3f}')

# FINAL evaluation on the held-out test set - touch this once
y_pred = grid.predict(X_test)
y_proba = grid.predict_proba(X_test)[:, 1]
print(classification_report(y_test, y_pred))
print(f'Test AUC: {roc_auc_score(y_test, y_proba):.3f}')

# Export the WHOLE pipeline - preprocessing travels with the model, so
# app.py can call .predict() straight on raw input.
import os
os.makedirs('models', exist_ok=True)
joblib.dump(grid.best_estimator_, 'models/final_model.pkl')
print('Saved models/final_model.pkl')
