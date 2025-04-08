from rgb_sensor import RGBSensor


sensor = RGBSensor("RGB", "I2C")
print(sensor.read_data())