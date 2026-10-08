import pandas as pd
import numpy as np

np.random.seed(42)
n = 2000  # more rows = more stable training

df = pd.DataFrame({
    'severity': np.random.choice([1, 2, 3], n, p=[0.5, 0.3, 0.2]),        # 1=minor, 2=moderate, 3=major
    'patient_age': np.random.randint(18, 90, n),
    'allergy_count': np.random.poisson(1, n),
    'active_med_count': np.random.poisson(3, n),
    'doctor_override_rate': np.random.beta(2, 5, n),                       # most doctors override rarely
    'time_of_day_busy': np.random.choice([0, 1], n, p=[0.6, 0.4])          # 1 = busy period
})

# Build a sharper, more deterministic decision boundary using a logistic (sigmoid) function.
# Coefficients are scaled up so the probability pushes strongly toward 0 or 1,
# instead of hovering in a soft middle range.
linear_score = (
    -3.0
    - 0.9 * df['severity']                      # higher severity -> much less likely to override
    + 7.0 * (df['doctor_override_rate'] - 0.3)  # doctor's own history matters most
    + 1.8 * df['time_of_day_busy']               # busy time -> more likely to override
    + 0.35 * df['active_med_count']              # more meds -> slightly more likely
    - 0.03 * (df['patient_age'] - 50)            # older patients -> doctors more cautious
)

prob_override = 1 / (1 + np.exp(-linear_score))  # sigmoid sharpens the decision

# Deterministic label from the sharpened probability
deterministic_label = (prob_override > 0.5).astype(int)

# Add only a small amount of realistic noise (5% random flips),
# instead of using the raw probability as a coin-flip threshold
noise_mask = np.random.rand(n) < 0.05
df['will_override'] = np.where(noise_mask, 1 - deterministic_label, deterministic_label)

df.to_csv('override_training_data.csv', index=False)
print(f"Generated {n} rows. Override rate in data: {df['will_override'].mean():.2%}")