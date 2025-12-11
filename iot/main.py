# iot/main.py  ← FINAL PRODUCTION VERSION (copy-paste kar do pura)

import time
import csv
import pickle
from pathlib import Path
import pandas as pd  # ← YE LINE ADD KARO

# Relative import (package mode ke liye)
from .sensors import read_temperature, read_humidity, read_co2, read_ammonia

# Paths
BASE_DIR = Path(__file__).parent.parent
CSV_FILE = BASE_DIR / "Dataset" / "grain_storage_live.csv"
MODEL_PATH = BASE_DIR / "model.pkl"

# Load model
print("Loading AI model from:", MODEL_PATH)
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
print("Model loaded successfully!\n")

# CSV setup
def setup_csv():
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "temp", "hum", "co2", "ammonia", "status", "confidence"])

setup_csv()

# PREDICTION FUNCTION — WARNING-FREE VERSION
def predict_status(temp, hum, co2, ammonia):
    X = pd.DataFrame([[temp, hum, co2, ammonia]], 
                     columns=["temp", "hum", "co2", "ammonia"])
    pred = model.predict(X)[0]
    conf = model.predict_proba(X)[0].max()
    return pred, conf

# Main loop
print("Smart Grain Storage System STARTED")
print("="*50)

while True:
    try:
        temp = read_temperature()
        hum = read_humidity()
        co2 = read_co2()
        ammonia = read_ammonia()

        status, confidence = predict_status(temp, hum, co2, ammonia)

        print(f"Temp: {temp:5.1f}°C | Hum: {hum:5.1f}% | CO₂: {co2:5.1f} ppm | NH₃: {ammonia:5.2f}")
        print(f"Status: {status:9} | Confidence: {confidence:.1%}")

        if status in ["Spoilage", "DANGER"]:
            print("ALERT! SPOILAGE DETECTED → Fan ON | Buzzer ON | Ventilation Activated!\n")
        else:
            print("System SAFE\n")

        # Log to CSV
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                round(temp, 2),
                round(hum, 2),
                round(co2, 2),
                round(ammonia, 2),
                status,
                f"{confidence:.4f}"
            ])

        time.sleep(5)

    except KeyboardInterrupt:
        print("\nSystem stopped by user. Bye!")
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(5)