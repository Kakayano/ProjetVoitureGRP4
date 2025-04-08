from sensors.rgb_sensor import RGBSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.CurrentSensor import CurrentSensor
from sensors.LineFollowSensor import LineFollowerSensor
from motors.dc_motor import DCMotor
from motors.servo_motor import ServoMotor

class Car():
    def __init__(self):
        self.__rgb_sensor = RGBSensor("RGB", "I2C")
        self.__front_ultrasonic_sensor = UltrasonicSensor("Ultrasonic", "GPIO", 6, 5)
        self.__right_ultrasonic_sensor = UltrasonicSensor("Ultrasonic", "GPIO", 26, 19)
        self.__left_ultrasonic_sensor = UltrasonicSensor("Ultrasonic", "GPIO", 11, 9)
        self.__current_sensor = CurrentSensor("Current", "I2C")
        self.__line_sensor = LineFollowerSensor("LineFollower", "GPIO")
        self.__dc_motor = DCMotor()
        self.__servo_motor = ServoMotor()
        self.__limit = 10
        self.__is_moving = False
        self.__laps = 0
        
        
    def run(self):
        """
        Démarre la voiture et lit les données des capteurs.
        """
        while True:
            
            ina_data = self.__current_sensor.read_data()
            print(f"Voltage: {ina_data['voltage']}V, Current: {ina_data['current']}A, Power: {ina_data['power']}W")
            
            if self.__rgb_sensor.is_green() and not self.__is_moving:
                self.__is_moving = True
                self.__dc_motor.moteur_avance()
                
            angle = 0
            direction = 0
            front_distance = self.__front_ultrasonic_sensor.update_distance()
                        
            if self.__left_ultrasonic_sensor.update_distance() > self.__right_ultrasonic_sensor.update_distance():
                direction = -1
            else: 
                direction = 1
            
            if front_distance < 30:
                angle = 15
            elif front_distance < 20:
                angle = 30
            elif front_distance < self.__limit:
                angle = 45
                self.__dc_motor.stop_moteur()
            else: 
                angle = 0
                
            self.__servo_motor.set_angle(direction * angle)
            
            if self.__line_sensor.is_on_line():
                self.__laps += 1
                print(f"Number of laps: {self.__laps}")
                
                
                
                    
                    
            