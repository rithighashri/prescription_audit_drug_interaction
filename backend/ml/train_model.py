import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the data
df = pd.read_csv('override_training_data.csv')

X = df[['severity', 'patient_age', 'allergy_count', 'active_med_count',
        'doctor_override_rate', 'time_of_day_busy']]
y = df['will_override']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:\n", classification_report(y_test, predictions))

# Show which features matter most - useful for your report
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importance:\n", importances)

# Save the trained model
joblib.dump(model, 'override_predictor.pkl')
print("\nModel saved as override_predictor.pkl")