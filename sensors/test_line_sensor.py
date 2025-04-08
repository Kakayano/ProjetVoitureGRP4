from LineFollowSensor import LineFollowSensor

sensor = LineFollowSensor("LineFollower", "GPIO", 20)
while True:
    sensor.detect_line()