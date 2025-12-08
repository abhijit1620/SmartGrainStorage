import pandas as pd
import matplotlib.pyplot as plt

# Example: Simulated data CSV
df = pd.read_csv("grain_storage_data.csv")  # columns: timestamp,temp,hum,co2,ammonia

plt.figure(figsize=(12,6))
plt.plot(df['timestamp'], df['temp'], label="Temperature (°C)")
plt.plot(df['timestamp'], df['hum'], label="Humidity (%)")
plt.plot(df['timestamp'], df['co2'], label="CO2 (ppm)")
plt.plot(df['timestamp'], df['ammonia'], label="Ammonia (Spoilage Index)")

plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.title("Grain Storage Sensor Trends")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()