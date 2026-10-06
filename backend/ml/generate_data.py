import pandas as pd
import numpy as np

np.random.seed(42)
n = 500  # number of synthetic past prescriptions

df = pd.DataFrame({
    'severity': np.random.choice([1, 2, 3], n, p=[0.5, 0.3, 0.2]),        # 1=minor, 2=moderate, 3=major
    'patient_age': np.random.randint(18, 90, n),
    'allergy_count': np.random.poisson(1, n),
    'active_med_count': np.random.poisson(3, n),
    'doctor_override_rate': np.random.beta(2, 5, n),                       # most doctors override rarely
    'time_of_day_busy': np.random.choice([0, 1], n, p=[0.6, 0.4])          # 1 = busy period
})

# Build a realistic probability of override based on the rules above
prob_override = (
    0.15
    - 0.05 * df['severity']                  # higher severity -> less likely to override
    + 0.5 * df['doctor_override_rate']       # doctor's own history matters most
    + 0.15 * df['time_of_day_busy']          # busy time -> more likely to override
    + 0.02 * df['active_med_count']          # more meds -> slightly more likely
)

df['will_override'] = (np.random.rand(n) < prob_override.clip(0, 1)).astype(int)

df.to_csv('override_training_data.csv', index=False)
print(f"Generated {n} rows. Override rate in data: {df['will_override'].mean():.2%}")