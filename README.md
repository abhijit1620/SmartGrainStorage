
```bash
# 1. Clone or download this project
cd SmartGrainStorage

# 2. Install dependencies
pip install -r requirements.txt

# 3. Terminal 1 — Start the sensor + AI system
python -m iot.main

# 4. Terminal 2 — Launch the beautiful dashboard
streamlit run dashboard/visualize.py




cd ~/Desktop/SmartGrainStorage/iot/esp32
pio run -t upload



cd ~/Desktop/SmartGrainStorage
python -m iot.main