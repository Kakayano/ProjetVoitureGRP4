from Moteur.DCMotor import DCMotor
from Moteur.ServoMoteur import ServoMoteur
from Capteur.ultrasonic_sensor import UltrasonicSensor

import threading
import time
import RPi.GPIO as GPIO

class Car:
    def __init__(self):
        '''
        On initialise la voiture avec les moteurs, le servo moteur et les capteurs
        '''
        self.__motor = DCMotor()
        self.__servo = ServoMoteur()
        self.__ultrasonic_sensor_top = UltrasonicSensor("Ultrasonic", "GPIO", 6, 5)
        self.__ultrasonic_sensor_left = UltrasonicSensor("Ultrasonic", "GPIO", 11, 9)
        self.__ultrasonic_sensor_right = UltrasonicSensor("Ultrasonic", "GPIO", 26, 19)

        self._run_dodge = False
        self._dodge_thread = None

    def run_straigth(self, speed=50, duration=5):
        '''
        Méthode pour faire avancer la voiture
        '''
        self.__servo.disable()
        self.__motor.motor_forward(speed)
        time.sleep(duration / 2)
        self.__motor.motor_backward(-speed)
        time.sleep(duration / 2)
        self.__motor.stop_motor()

    def u_turn(self):
        '''
        Méthode pour faire un demi-tour
        '''
        self.__servo.set_angle(-30)
        self.__motor.motor_forward(30)
        time.sleep(8)
        self.__servo.set_angle(30)
        self.__motor.motor_forward(30)
        time.sleep(8)
        self.__servo.set_angle(0)
        self.__motor.motor_forward(30)
        time.sleep(1)
        self.__motor.stop_motor()
        self.__servo.disable()
        print("Demi-tour effectué.")

    def _detect_obstacle_loop(self):
        self.__motor.motor_forward(30)
        self._run_dodge = True
        while self._run_dodge:
            self.__ultrasonic_sensor_top.read_data()
            distance = self.__ultrasonic_sensor_top.distance

            if distance is not None and distance < 40:
                print(f" Obstacle détecté à {distance} cm.")
                self._run_dodge = False

                self.__motor.stop_motor()
                time.sleep(0.5)

                self.__servo.set_angle(20)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()

                self.__servo.set_angle(-20)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()

                self.__servo.set_angle(0)
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()

                self.__servo.set_angle(-20)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()

                self.__servo.set_angle(20)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()

                self.__servo.set_angle(0)
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()

                self.__servo.disable()
                print(" Obstacle évité.")
                self._run_dodge = False
                break

            elif distance is not None:
                print(f" Distance libre : {distance} cm")
            else:
                print("Distance non mesurée.")

            time.sleep(0.2)
        pass

    def dodge_obstacle(self):
        '''
        Méthode pour éviter les obstacles avec threads
        '''
        if self._dodge_thread is None or not self._dodge_thread.is_alive():
            
            self._dodge_thread = threading.Thread(target=self._detect_obstacle_loop)
            self._run_dodge = True
            self._dodge_thread.start()
        else:
            print(" Détection déjà en cours...")

    def along_wall(self, side = "L"):
        '''
        Méthode pour suivre un mur
        '''
        if side == "L":
            while True:
                self.__motor.motor_forward(30)
                self.__ultrasonic_sensor_left.read_data()
                distance = self.__ultrasonic_sensor_left.distance
                if distance is not None and distance < 10:
                    print(distance)
                    self.__servo.set_angle(-20)
                elif distance is not None and distance > 20:
                    print(distance)
                    self.__servo.set_angle(20)
                else:
                    self.__servo.set_angle(0)  
                    
        elif side == "R":
            while True:
                self.__motor.motor_forward(30)
                self.__ultrasonic_sensor_right.read_data()
                distance = self.__ultrasonic_sensor_right.distance
                if distance is not None and distance < 10:
                    print(distance )
                    self.__servo.set_angle(20)
                elif distance is not None and distance > 20:
                    print(distance)
                    self.__servo.set_angle(-20)
                else:
                    self.__servo.set_angle(0)
                
        else:
            raise ValueError("Le côté doit être 'L' ou 'R'.")
                

        

    def stop_car(self):
        '''
        Méthode pour arrêter la voiture
        '''
        self._run_dodge = False
        if self._dodge_thread and self._dodge_thread.is_alive():
            self._dodge_thread.join()
        self.__motor.stop_motor()
        self.__servo.disable()

if __name__ == "__main__":
    test_u = Car()
    while True:
        print("\nMenu:")
        print("1. Faire avancer la voiture")
        print("2. Faire un demi-tour")
        print("3. Eviter les obstacles")
        print("4. Arrêter la voiture et quitter")

        choice = input("Choisissez une option (1-4): ")

        if choice == "1":
            try:
                test_u.run_straigth(50, 8)
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()

        elif choice == "2":
            try:
                test_u.u_turn()
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()

        elif choice == "3":
            try:
                test_u.dodge_obstacle()
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()
        
        elif choice == "6":
            try:
                test_u.along_wall("L")
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()

        elif choice == "4":
            print("Arrêt de la voiture et sortie du programme.")
            test_u.stop_car()
            GPIO.cleanup()
            break
        else:
            print("Option invalide. Veuillez réessayer.")