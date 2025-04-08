from Moteur.DCMotor import DCMotor
from Moteur.ServoMoteur import ServoMoteur
from Capteur.rgb_sensor import RGBSensor
from Capteur.ultrasonic_sensor import UltrasonicSensor

import threading
import time

class Car:
    def __init__(self):
        self.__motor = DCMotor()
        self.__servo = ServoMoteur()
        self.__rgb = RGBSensor("RGB", "I2C")
        self.__ultrasonic_top = UltrasonicSensor("Ultrasonic", "GPIO", 6, 5)
        self.__ultrasonic_right = UltrasonicSensor("Ultrasonic", "GPIO", 26, 19)
        self.__ultrasonic_left = UltrasonicSensor("Ultrasonic", "GPIO", 11, 9)

    def forward(self, speed=100, period=2):
        def run():
            with self.__lock:
                print("Avancer")
                self.moteur.motor_forward(speed)
                time.sleep(period)
                self.moteur.stop_motor()
                print(" Arrêt après avance")
        thread = threading.Thread(target=run)
        thread.start()


    def turn_left(self, angle=30):
        print(" Tourner à gauche")
        self.direction.set_angle(-abs(angle))

    def turn_right(self, angle=30):
        print("Tourner à droite")
        self.direction.set_angle(abs(angle)) 

    def straitght(self):
        print("Direction tout droit")
        self.direction.set_angle(0)

    def stop(self):
        self.moteur.motor_stop()
        self.tout_droit()

    def backward(self, speed=-100, period=2):
        def run():
            with self.__lock:
                print("Reculer")
                self.moteur.motor_backward(speed)
                time.sleep(period)
                self.moteur.stop_motor()
                print(" Arrêt après recul")
        thread = threading.Thread(target=run)
        thread.start()
        
    def get_forward_distance(self):
        return self.__ultrasonic_top.update_distance()
    
    def get_left_distance(self):
        return self.__ultrasonic_left.update_distance()
    
    def get_right_distance(self):
        return self.__ultrasonic_right.update_distance()
    
    def start(self):
        if self.__rgb.is_green():
            print("La couleur est verte !")
            self.run()

    def u_turn(self,side='R' ,angle=45, speed=20 , duration=3):
        if side == 'R':
            self.turn_right(angle)
            self.forward(speed, duration)
        elif side == 'L':
            self.turn_left(angle)
            self.forward(speed, duration)
        else:
            self.stop()