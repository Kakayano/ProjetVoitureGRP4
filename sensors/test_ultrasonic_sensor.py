from ultrasonic_sensor import UltrasonicSensor

trig = int(input("Enter the trigger pin: "))
echo = int(input("Enter the echo pin: "))
sensor = UltrasonicSensor("Ultrasonic", "GPIO", trig, echo)
sensor.start()