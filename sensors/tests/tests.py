from CurrentSensor import CurrentSensor
from ultrasonic_sensor import UltrasonicSensor
from rgb_sensor import RGBSensor
from LineFollowSensor import LineFollowSensor
import threading
import time

trig = int(input("Enter the trigger pin: "))
echo = int(input("Enter the echo pin: "))
ultrasonic_sensor = UltrasonicSensor("Ultrasonic", "GPIO", trig, echo)
current_sensor = CurrentSensor("Current", "I2C")
rgb_sensor = RGBSensor("RGB", "I2C")
line_follow_sensor = LineFollowSensor("LineFollower", "GPIO", 20)

def stop_sensors():
    input("\nAppuyez sur Enter pour arrêter les capteurs...\n")
    ultrasonic_sensor.stop()
    current_sensor.stop()
    rgb_sensor.stop()
    line_follow_sensor.stop()
    time.sleep(1)
    print("\nLes capteurs ont été arrêtés.\n")

stop_threads = threading.Thread(target=stop_sensors)

if __name__ == "__main__":
    ultrasonic_sensor.start()
    current_sensor.start()
    rgb_sensor.start()
    line_follow_sensor.start()
    
    stop_threads.start()
    
    stop_threads.join()