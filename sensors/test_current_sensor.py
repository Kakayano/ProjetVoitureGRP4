from CurrentSensor import CurrentSensor
import time

sensor = CurrentSensor("Current", "I2C")
while True:
    data = sensor.read_data()
    print(f"Voltage: {data['voltage']}V, Current: {data['current']}A, Power: {data['power']}W")
    time.sleep(1)