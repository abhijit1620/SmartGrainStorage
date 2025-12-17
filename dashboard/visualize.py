import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time

# ================= PAGE =================
st.set_page_config(
    page_title="Smart Grain Storage",
    page_icon="🌾",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
body { background-color: #0e1117; }
.big-title {
    font-size: 55px;
    text-align: center;
    color: #00ff41;
    text-shadow: 0 0 20px #00ff41;
    font-weight: bold;
}
.card {
    background: linear-gradient(145deg, #1a1f2b, #11141c);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,65,0.25);
}
.log-box {
    background: #000;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #00ff41;
    font-family: monospace;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ================= PATHS =================
BASE = Path(__file__).parent.parent
CSV_PATH = BASE / "Dataset" / "grain_storage_live.csv"
CONTROL_FILE = BASE / "control.txt"

# ================= HEADER =================
st.markdown("<div class='big-title'>SMART GRAIN STORAGE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7CFC98'>AI Powered IoT Monitoring Dashboard</p>", unsafe_allow_html=True)

st.divider()

# ================= FAN CONTROL =================
c1, c2, c3 = st.columns([1,1,2])

with c1:
    if st.button("🌀 FAN ON"):
        CONTROL_FILE.write_text("ON")

with c2:
    if st.button("⛔ FAN OFF"):
        CONTROL_FILE.write_text("OFF")

with c3:
    if CONTROL_FILE.exists():
        st.info(f"Fan Status: **{CONTROL_FILE.read_text().strip()}**")

st.divider()

# ================= DATA =================
if not CSV_PATH.exists():
    st.error("No data received from ESP32 yet")
    st.stop()

df = pd.read_csv(CSV_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0)
df["status"] = df["status"].fillna("Unknown")

df = df.sort_values("timestamp")
latest = df.iloc[-1]
conf = latest["confidence"] * 100

# ================= ALERT =================
if latest["status"] == "Spoilage":
    st.error(f"🚨 SPOILAGE DETECTED | {conf:.0f}% confidence")
elif latest["status"] == "Risk":
    st.warning(f"⚠️ RISK CONDITION | {conf:.0f}% confidence")
else:
    st.success(f"✅ SAFE | {conf:.0f}% confidence")

# ================= METRICS =================
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"<div class='card'><h2>{latest['temp']:.1f} °C</h2><p>Temperature</p></div>", unsafe_allow_html=True)

with m2:
    st.markdown(f"<div class='card'><h2>{latest['hum']:.1f} %</h2><p>Humidity</p></div>", unsafe_allow_html=True)

with m3:
    st.markdown(f"<div class='card'><h2>{latest['co2']:.0f}</h2><p>CO₂ (ppm)</p></div>", unsafe_allow_html=True)

with m4:
    st.markdown(f"<div class='card'><h2>{latest['ammonia']:.2f}</h2><p>Ammonia</p></div>", unsafe_allow_html=True)

# ================= GRAPHS =================
tab1, tab2 = st.tabs(["🌡 Environment", "🧠 AI Confidence"])

with tab1:
    fig = go.Figure()
    fig.add_scatter(x=df["timestamp"], y=df["temp"], name="Temperature °C", line=dict(color="#ff5555"))
    fig.add_scatter(x=df["timestamp"], y=df["hum"], name="Humidity %", yaxis="y2", line=dict(color="#4fa3ff"))
    fig.update_layout(
        yaxis2=dict(overlaying="y", side="right"),
        template="plotly_dark",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.area(
        df.tail(100),
        x="timestamp",
        y="confidence",
        color="status",
        template="plotly_dark",
        color_discrete_map={
            "Safe":"green",
            "Risk":"orange",
            "Spoilage":"red",
            "Unknown":"gray"
        }
    )
    fig2.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig2, use_container_width=True)

# ================= LOG =================
st.subheader("📟 Live Sensor Log")

logs = ""
for _, r in df.tail(15).iterrows():
    color = "red" if r["status"] == "Spoilage" else "orange" if r["status"] == "Risk" else "#7CFC98"
    logs += f"<span style='color:{color}'>{r['timestamp'].strftime('%H:%M:%S')} | T:{r['temp']}°C H:{r['hum']}% → {r['status']}</span><br>"

st.markdown(f"<div class='log-box'>{logs}</div>", unsafe_allow_html=True)

# ================= AUTO REFRESH =================
time.sleep(3)
st.rerun()