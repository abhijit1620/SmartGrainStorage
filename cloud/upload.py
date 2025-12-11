import requests

API_URL = "https://example.api/upload"

def upload_to_cloud(payload):
    try:
        r = requests.post(API_URL, json=payload)
        print("Cloud Upload:", r.status_code)
    except:
        print("Cloud Upload Failed")