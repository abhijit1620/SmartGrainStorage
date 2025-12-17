from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

BASE = Path(__file__).parent.parent
CSV_PATH = BASE / "Dataset" / "grain_storage_live.csv"

CSV_PATH.parent.mkdir(exist_ok=True)

# CSV create if not exists
if not CSV_PATH.exists():
    df = pd.DataFrame(columns=[
        "timestamp","temp","hum","co2","ammonia","status","confidence"
    ])
    df.to_csv(CSV_PATH, index=False)

def classify(temp, hum, co2, ammonia):
    # 🔥 Simple AI logic (can upgrade later)
    if hum > 70 or ammonia > 1:
        return "Spoilage", 0.95
    elif hum > 60:
        return "Risk", 0.75
    else:
        return "Safe", 0.40

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json

    temp = float(data["temp"])
    hum = float(data["hum"])
    co2 = float(data["co2"])
    ammonia = float(data["ammonia"])

    status, confidence = classify(temp, hum, co2, ammonia)

    row = {
        "timestamp": datetime.now().isoformat(timespec="milliseconds"),
        "temp": temp,
        "hum": hum,
        "co2": co2,
        "ammonia": ammonia,
        "status": status,
        "confidence": confidence
    }

    df = pd.read_csv(CSV_PATH)
    df.loc[len(df)] = row
    df.to_csv(CSV_PATH, index=False)

    return jsonify({"message": "Data received"}), 200

@app.route("/")
def home():
    return "Smart Grain Storage API Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)