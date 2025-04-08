from ultrasonic_sensor import UltrasonicSensor

sensor = UltrasonicSensor("Ultrasonic", "GPIO", 6, 5)
sensor.update_distance()