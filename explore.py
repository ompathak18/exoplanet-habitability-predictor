import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Load and prepare data
df = pd.read_csv("planets.csv", comment="#")
important_columns = ['pl_name', 'pl_radj', 'pl_bmassj', 'pl_orbsmax', 'st_teff']
df_small = df[important_columns].dropna().copy()

# Create habitability labels
def is_habitable(row):
    if (3700 <= row['st_teff'] <= 7200 and
        0.5 <= row['pl_orbsmax'] <= 2.0 and
        row['pl_radj'] <= 2.0):
        return 1
    else:
        return 0

df_small['habitable'] = df_small.apply(is_habitable, axis=1)

# Prepare features for ML model
X = df_small[['pl_radj', 'pl_bmassj', 'pl_orbsmax', 'st_teff']]
y = df_small['habitable']

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Check accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")