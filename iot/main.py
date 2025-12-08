import time
import sys
from ..cloud.upload import upload_to_cloud
import os

# Add project root to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensors import read_temperature, read_humidity, read_co2, read_ammonia
from cloud.upload import upload_to_cloud  # now works correctly

def main():
    while True:
        temp = read_temperature()
        hum = read_humidity()
        co2 = read_co2()
        ammonia = read_ammonia()

        print(f"Temp: {temp}°C, Humidity: {hum}%, CO2: {co2} ppm, Ammonia: {ammonia}")

        # Send data to cloud
        upload_to_cloud(temp, hum, co2, ammonia)

        # Alert conditions
        if hum > 70:
            print("⚠️ Alert: Humidity too high!")
        if temp > 30:
            print("⚠️ Alert: Temperature too high!")
        if co2 > 600 or ammonia > 5:
            print("⚠️ Alert: Possible spoilage detected!")

        time.sleep(10)  # Every 10 seconds

if __name__ == "__main__":
    main()