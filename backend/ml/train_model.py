import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    ConfusionMatrixDisplay, precision_score, roc_auc_score, RocCurveDisplay
)
import joblib

# ---------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------
df = pd.read_csv('override_training_data.csv')
X = df[['severity', 'patient_age', 'allergy_count', 'active_med_count',
        'doctor_override_rate', 'time_of_day_busy']]
y = df['will_override']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------
# 2. Compare multiple models (for your report's justification section)
# ---------------------------------------------------------
candidates = {
    'Logistic Regression': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'Decision Tree': DecisionTreeClassifier(random_state=42, class_weight='balanced'),
    'SVM': SVC(probability=True, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
}

print("=" * 60)
print("MODEL COMPARISON (5-fold cross-validated precision)")
print("=" * 60)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
comparison_results = {}
for name, clf in candidates.items():
    scores = cross_val_score(clf, X, y, cv=cv, scoring='precision')
    comparison_results[name] = scores
    print(f"{name:20s}  mean precision = {scores.mean():.3f}  (+/- {scores.std()*2:.3f})")

# Save comparison chart for your report
plt.figure(figsize=(8, 5))
plt.boxplot(comparison_results.values(), labels=comparison_results.keys())
plt.ylabel('Cross-Validated Precision')
plt.title('Model Comparison: Precision Across 5 Folds')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150)
plt.close()
print("Saved model_comparison.png\n")

# ---------------------------------------------------------
# 3. Hyperparameter tuning for Random Forest (your chosen model)
# ---------------------------------------------------------
print("=" * 60)
print("HYPERPARAMETER TUNING (Random Forest)")
print("=" * 60)
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, class_weight='balanced'),
    param_grid,
    cv=cv,
    scoring='precision',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)
print(f"Best cross-validated precision: {grid_search.best_score_:.3f}\n")

model = grid_search.best_estimator_

# ---------------------------------------------------------
# 4. Final evaluation on held-out test set
# ---------------------------------------------------------
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("=" * 60)
print("FINAL MODEL EVALUATION (Tuned Random Forest, held-out test set)")
print("=" * 60)
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:\n", classification_report(y_test, predictions))
print("ROC-AUC Score:", roc_auc_score(y_test, probabilities))

# Confusion matrix
cm = confusion_matrix(y_test, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Override', 'Override'])
disp.plot(cmap='Blues')
plt.title('Tuned Random Forest - Confusion Matrix')
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved confusion_matrix.png")

# ROC curve
RocCurveDisplay.from_predictions(y_test, probabilities)
plt.title('ROC Curve - Random Forest')
plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved roc_curve.png")

# ---------------------------------------------------------
# 5. Feature importance
# ---------------------------------------------------------
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importance:\n", importances)

importances.plot(kind='bar', title='Feature Importance (Tuned Random Forest)', color='steelblue')
plt.ylabel('Importance')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved feature_importance.png")

# ---------------------------------------------------------
# 6. Save final model
# ---------------------------------------------------------
joblib.dump(model, 'override_predictor.pkl')
print("\nFinal tuned model saved as override_predictor.pkl")