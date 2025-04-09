from CurrentSensor import CurrentSensor
import time

sensor = CurrentSensor("Current", "I2C")
sensor.run()