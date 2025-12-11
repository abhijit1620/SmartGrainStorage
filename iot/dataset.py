import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# ------------ LOAD CSV -------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, "Dataset", "grain_storage.csv")

print("Loading CSV:", CSV_PATH)
df = pd.read_csv(CSV_PATH)

print("Columns:", df.columns.tolist())
print(df.head())

# ----------- CREATE LABEL -----------
def label_status(row):
    if row['hum'] > 70 or row['temp'] > 30 or row['co2'] > 500 or row['ammonia'] > 2:
        return "Spoilage"
    elif row['hum'] > 60 or row['temp'] > 28:
        return "Risk"
    else:
        return "Safe"

df["status"] = df.apply(label_status, axis=1)

# ------------ FEATURES & TARGET -------------
X = df[["temp", "hum", "co2", "ammonia"]]
y = df["status"]

# ------------ SPLIT & TRAIN --------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
print("\nModel Accuracy:", accuracy)

# ------------ SAVE MODEL -------------
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("Model saved at:", MODEL_PATH)