# iot/sensors.py
from __future__ import annotations
import random

# -------------------------------------------------
# CONFIG: Set this to False when real sensors are connected
USE_MOCK_SENSORS = True
# -------------------------------------------------

# Starting realistic values (slow drift ke liye)
_last = {"temp": 27.5, "hum": 66.0, "co2": 430.0, "nh3": 0.9}

def _drift(value: float, min_val: float, max_val: float, step: float = 1.0) -> float:
    """Helper for smooth drifting values"""
    global _last
    change = random.uniform(-step, step)
    new_val = _last[value] + change
    new_val = max(min_val, min(max_val, new_val))
    _last[value] = new_val
    return round(new_val, 2)

# ================== MOCK SENSORS (REALISTIC) ==================
def read_temperature() -> float:
    if USE_MOCK_SENSORS:
        return _drift("temp", 20, 35, step=0.7)
    # ← Jab real sensor lagaoge tab yeh line uncomment kar dena
    # from machine import Pin; import dht; d = dht.DHT22(Pin(4)); d.measure(); return d.temperature()

def read_humidity() -> float:
    if USE_MOCK_SENSORS:
        return _drift("hum", 50, 90, step=1.5)
    # return dht_sensor.humidity()

def read_co2() -> float:
    if USE_MOCK_SENSORS:
        return _drift("co2", 300, 900, step=15.0)
    # ← Real MH-Z19B / SCD30 code yahan aayega
    # return your_co2_sensor.read()

def read_ammonia() -> float:
    if USE_MOCK_SENSORS:
        # Ammonia badhta hai jab humidity aur temp zyada ho
        base = 0.3 + (read_humidity()-60)*0.08 + (read_temperature()-27)*0.05
        noise = random.uniform(-0.3, 0.8)
        nh3 = max(0.0, base + noise)
        return round(nh3, 2)
    # ← Real MQ-137 code yahan
    # return mq137.read_ppm()

# Optional simple hazard (agar kabhi chahiye ho)
def is_hazard(temp: float, hum: float, co2: float) -> bool:
    return hum > 75 or temp > 32 or co2 > 700