
---

### How to Run (2 Minutes Setup)

```bash
# 1. Clone or download this project
cd SmartGrainStorage

# 2. Install dependencies
pip install -r requirements.txt

# 3. Terminal 1 — Start the sensor + AI system
python -m iot.main

# 4. Terminal 2 — Launch the beautiful dashboard
streamlit run dashboard/visualize.py