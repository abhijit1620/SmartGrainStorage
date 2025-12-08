import requests

THINGSPEAK_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your ThingSpeak API key

def upload_to_cloud(temp, hum, co2, ammonia):
    url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"
    payload = {
        "field1": temp,
        "field2": hum,
        "field3": co2,
        "field4": ammonia
    }
    try:
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            print("✅ Data uploaded to cloud successfully!")
        else:
            print("❌ Failed to upload data!")
    except Exception as e:
        print("Error:", e)