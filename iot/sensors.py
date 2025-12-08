import random

def read_temperature():
    return round(random.uniform(20, 35), 2)  # Celsius

def read_humidity():
    return round(random.uniform(50, 90), 2)  # Percent

def read_co2():
    return round(random.uniform(300, 800), 2)  # ppm

def read_ammonia():
    return round(random.uniform(0, 10), 2)  # Arbitrary spoilage index