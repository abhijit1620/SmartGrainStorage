# dashboard/visualize.py  ← ULTIMATE FINAL CODE (FAN GREEN/RED + EVERYTHING)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time

st.set_page_config(page_title="Smart Grain Storage Pro", page_icon="wheat", layout="wide")

# CUSTOM CSS — SABSE KILLER LOOK
st.markdown("""
<style>
    .big-title {font-size: 60px; color: #00ff41; text-align: center; text-shadow: 0 0 25px #00ff41; font-weight: bold;}
    .metric-box {background: background: linear-gradient(145deg, #1e1e1e, #2d2d2d); padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px rgba(0,255,65,0.5);}
    
    /* FAN ON = GREEN BUTTON */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #00ff41 !important;
        color: black !important;
        font-weight: bold !important;
        border: 3px solid #00ff41 !important;
        height: 70px !important;
        font-size: 20px !important;
    }
    /* FAN OFF = RED BUTTON */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #ff0044 !important;
        color: white !important;
        font-weight: bold !important;
        border: 3px solid #ff0044 !important;
        height: 70px !important;
        font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-title'>SMART GRAIN STORAGE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#00ff41;'>AI-Powered Real-time Spoilage Detection + Manual Control</h3>", unsafe_allow_html=True)

# Paths
CSV_PATH = Path(__file__).parent.parent / "Dataset" / "grain_storage_live.csv"
CONTROL_FILE = Path(__file__).parent.parent / "control.txt"

# ================= FAN CONTROL =================
col1, col2, col3, col4 = st.columns([1,1,1,2])

with col1:
    if st.button("FAN ON", key="fan_on_btn"):
        CONTROL_FILE.write_text("ON")
        st.success("FAN ACTIVATED!")

with col2:
    if st.button("FAN OFF", key="fan_off_btn"):
        CONTROL_FILE.write_text("OFF")
        st.error("FAN DEACTIVATED!")

# Current Fan Status — BADA AUR COLORFUL
if CONTROL_FILE.exists():
    status = CONTROL_FILE.read_text().strip()
    if status == "ON":
        st.markdown("<h1 style='text-align:center; color:#00ff41; text-shadow:0 0 20px #00ff41;'>FAN IS RUNNING</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align:center; color:#ff0044; text-shadow:0 0 20px #ff0044;'>FAN IS OFF</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align:center; color:orange;'>FAN STATUS: UNKNOWN</h2>", unsafe_allow_html=True)

st.markdown("---")

# ================= LIVE DATA =================
if not CSV_PATH.exists():
    st.error("No data yet — Run: `python -m iot.main`")
    st.stop()

df = pd.read_csv(CSV_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
latest = df.iloc[-1]
conf = float(latest["confidence"]) * 100

# ALERT BANNER
if latest["status"] == "Spoilage":
    st.error(f"SPOILAGE DETECTED | Confidence: {conf:.1f}% | VENTILATION ACTIVE!")
elif latest["status"] == "Risk":
    st.warning(f"AT RISK | Confidence: {conf:.1f}%")
else:
    st.success(f"ALL SAFE | {conf:.1f}% Confidence")

# 4 BIG METRICS
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-box'><h2>{latest.temp:.1f}°C</h2><p>Temperature</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-box'><h2>{latest.hum:.1f}%</h2><p>Humidity</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-box'><h2>{latest.co2:.0f}</h2><p>CO₂ (ppm)</p></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-box'><h2>{latest.ammonia:.2f}</h2><p>Ammonia</p></div>", unsafe_allow_html=True)

# GRAPHS
tab1, tab2, tab3 = st.tabs(["Temp & Humidity", "CO₂ & Ammonia", "AI Confidence"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["temp"], name="Temperature °C", line=dict(color="#ff4444")))
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["hum"], name="Humidity %", yaxis="y2", line=dict(color="#4488ff")))
    fig.update_layout(title="Temperature & Humidity", yaxis2=dict(title="Humidity %", overlaying="y", side="right"), height=500, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["co2"], name="CO₂ ppm", line=dict(color="orange")))
    fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["ammonia"]*100, name="Ammonia ×100", line=dict(color="purple")))
    fig2.update_layout(title="CO₂ & Ammonia Levels", height=500, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.area(df.tail(100), x="timestamp", y="confidence", color="status",
                   color_discrete_map={"Safe":"green", "Risk":"orange", "Spoilage":"red"},
                   title="AI Spoilage Confidence Over Time")
    fig3.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig3, use_container_width=True)

# LIVE TERMINAL LOG
st.subheader("Live Terminal Log")
logs = ""
for _, r in df.tail(20).iterrows():
    color = "red" if r.status == "Spoilage" else "orange" if r.status == "Risk" else "lightgreen"
    alert = "  ALERT! SPOILAGE!" if r.status == "Spoilage" else ""
    t = r["timestamp"].strftime("%H:%M:%S")
    logs += f"<span style='color:{color}; font-family:monospace; font-size:17px;'>{t} | T:{r.temp:5.1f}°C H:{r.hum:5.1f}% → {r.status} ({float(r.confidence)*100:.0f}%) {alert}</span><br>"

st.markdown(f"""
<div style='background:#000; padding:20px; border-radius:15px; border:3px solid #00ff41; height:450px; overflow-y:auto; font-family:monospace; color:#00ff41; box-shadow:0 0 40px #00ff4130;'>
{logs}<span style='color:#00ff41; animation: blink 1s infinite;'>█</span>
</div>
""", unsafe_allow_html=True)

# Auto refresh
time.sleep(4)
st.rerun()