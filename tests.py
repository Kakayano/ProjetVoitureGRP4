from capteurs.RGB_sensor import RGBSensor
from capteurs.ultrasonic_sensor import UltrasonicSensor
from capteurs.LineFollowSensor import LineFollowSensor
from moteurs.DCMotor import DCMotor
from moteurs.ServoMoteur import ServoMoteur
import time

"""
Test des capteurs à ultrasons
"""
front_ultrasonic = UltrasonicSensor("front_ultrasonic", "I2C", 6, 5)
left_ultrasonic = UltrasonicSensor("left_ultrasonic", "I2C", 11, 9)
right_ultrasonic = UltrasonicSensor("right_ultrasonic", "I2C", 26, 19)
front_ultrasonic.read_data()
left_ultrasonic.read_data()
right_ultrasonic.read_data()
print(front_ultrasonic.distance)
print(left_ultrasonic.distance)
print(right_ultrasonic.distance)

time.sleep(1)

"""
Test du capteur rgb
"""
rgb_sensor = RGBSensor("RGB", "I2C")
rgb_sensor.read_data()
print(rgb_sensor.colors)

time.sleep(1)

"""
Test du capteur suiveur de ligne
"""
line_follow_sensor = LineFollowSensor("LineFollow", "I2C", 20)
is_on_line = line_follow_sensor.read_data()
print("Le capteur détecte la ligne : ", is_on_line)