from rgb_sensor import RGBSensor

sensor = RGBSensor("RGB", "I2C")
while True:
    sensor.read_data()