import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time

st.set_page_config("Smart Grain Storage", "🌾", layout="wide")

BASE = Path(__file__).parent.parent
CSV_PATH = BASE / "Dataset" / "grain_storage_live.csv"
CONTROL_FILE = BASE / "control.txt"

st.markdown("<h1 style='text-align:center;color:#00ff41'>SMART GRAIN STORAGE</h1>", unsafe_allow_html=True)

# FAN CONTROL
c1, c2 = st.columns(2)
with c1:
    if st.button("FAN ON"):
        CONTROL_FILE.write_text("ON")
with c2:
    if st.button("FAN OFF"):
        CONTROL_FILE.write_text("OFF")

if CONTROL_FILE.exists():
    st.info(f"Fan Status: {CONTROL_FILE.read_text()}")

st.divider()

if not CSV_PATH.exists():
    st.error("No data yet")
    st.stop()

df = pd.read_csv(CSV_PATH)

# 🔥 FIXES
df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0)
df["status"] = df["status"].fillna("Unknown")

df = df.sort_values("timestamp")
latest = df.iloc[-1]

# ALERT
conf = latest["confidence"] * 100
if latest["status"] == "Spoilage":
    st.error(f"SPOILAGE | {conf:.0f}%")
elif latest["status"] == "Risk":
    st.warning(f"RISK | {conf:.0f}%")
else:
    st.success(f"SAFE | {conf:.0f}%")

# METRICS
m1, m2, m3, m4 = st.columns(4)
m1.metric("Temperature", f"{latest['temp']:.1f} °C")
m2.metric("Humidity", f"{latest['hum']:.1f} %")
m3.metric("CO₂", f"{latest['co2']:.0f} ppm")
m4.metric("Ammonia", f"{latest['ammonia']:.2f}")

# GRAPHS
tab1, tab2 = st.tabs(["Environment", "AI Confidence"])

with tab1:
    fig = go.Figure()
    fig.add_scatter(x=df["timestamp"], y=df["temp"], name="Temp")
    fig.add_scatter(x=df["timestamp"], y=df["hum"], name="Humidity", yaxis="y2")
    fig.update_layout(yaxis2=dict(overlaying="y", side="right"), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.area(
        df.tail(100),
        x="timestamp",
        y="confidence",
        color="status",
        template="plotly_dark",
        color_discrete_map={"Safe":"green","Risk":"orange","Spoilage":"red"}
    )
    fig2.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig2, use_container_width=True)

# LOG
st.subheader("Live Log")
for _, r in df.tail(15).iterrows():
    st.write(f"{r['timestamp'].strftime('%H:%M:%S')} | {r['temp']}°C {r['hum']}% → {r['status']}")

time.sleep(3)
st.rerun()