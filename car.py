from Moteur.DCMotor import DCMotor
from Moteur.ServoMoteur import ServoMoteur
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.LineFollowSensor import LineFollowSensor
from sensors.CurrentSensor import CurrentSensor
from sensors.rgb_sensor import RGBSensor

import time
import RPi.GPIO as GPIO

class Car:
    def __init__(self):
        '''
        On initialise la voiture avec les moteurs, le servo moteur et les capteurs
        '''
        self.__motor = DCMotor()
        self.__servo = ServoMoteur()
        self.__ultrasonic_sensor_top = UltrasonicSensor("Ultrasonic", "GPIO", 6, 5) # Capteur ultrasonique pour la détection d'obstacles
        self.__left_ultrasonic_sensor = UltrasonicSensor("Left Ultrasonic", "GPIO", 11, 9)
        self.__right_ultrasonic_sensor = UltrasonicSensor("Left Ultrasonic", "GPIO", 26, 19)
        self.__rgb_sensor = RGBSensor("RGB", "GPIO")
        self.__current_sensor = CurrentSensor("Current", "GPIO")
        self.__line_follow_sensor = LineFollowSensor("LineFollower", "GPIO", 20)
        

    
    def run_straigth(self, speed=50, duration=5): # Méthode pour faire avancer la voiture
        '''
        Méthode pour faire avancer la voiture
        elle prend en paramètre la vitesse et la durée
        '''
        
        self.__servo.disable() # On désactive le servo moteur
        self.__motor.motor_forward(speed)
        time.sleep(duration/2) # On fait avancer la voiture pendant la durée spécifiée
        self.__motor.motor_backward(-speed)
        time.sleep(duration/2) # On fait reculer la voiture pendant la durée spécifiée
        self.__motor.stop_motor() # On arrête la voiture après la durée spécifiée
    
    def u_turn(self): # Méthode pour faire un demi-tour
        '''
        Méthode pour faire un demi-tour à gauche ou à droite
        elle prend en paramètre le côté (gauche ou droite), l'angle, la vitesse et la durée
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

    def dodge_obstacle(self): # Méthode pour éviter les obstacles
        '''
        Méthode pour éviter les obstacles détectés par le capteur ultrasonique
        '''
        run = True
        self.__motor.motor_forward(50)
        while run:
            self.__ultrasonic_sensor_top.read_data() # On lit les données du capteur ultrasonique
            distance = self.__ultrasonic_sensor_top.distance # On récupère la distance mesurée par le capteur
            if distance is not None and distance < 20: # Si un obstacle est détecté à moins de 20 cm
                print(f"Obstacle détecté à {distance} cm. Arrêt des moteurs.")
                self.__motor.stop_motor()
                time.sleep(0.5)
                self.__servo.set_angle(30) # On tourne le servo moteur à gauche
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()
                time.sleep(0.5)
                self.__servo.set_angle(-30) # On tourne le servo moteur à droite
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()
                time.sleep(0.5)
                self.__servo.set_angle(0) # On remet le servo moteur à 0
                self.__motor.motor_forward(30)
                time.sleep(5)
                self.__motor.stop_motor()
                time.sleep(0.5)
                self.__servo.set_angle(-30)
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()
                time.sleep(0.5)
                self.__servo.set_angle(30)
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()
                time.sleep(0.5)
                self.__servo.set_angle(0) # On remet le servo moteur à 0
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()
                self.__servo.disable()
                print("Obstacle évité.")
                run = False
            elif distance is not None:
                print(f"Distance : {distance} m")
            else:
                print("Distance non mesurée (None).")
        
    def detect_green(self): 
        self.__rgb_sensor.start()
        isgreen = self.__rgb_sensor.green_found
        if isgreen:
            print("La voiture peut démarrer.")
        else:
            print("La voiture ne peut pas démarrer.")

    

    def stop_car(self):
        '''
        Méthode pour arrêter la voiture
        '''
        self.__motor.stop_motor() # On arrête les moteurs
        self.__servo.disable()
        self.__current_sensor.stop()
        self.__line_follow_sensor.stop()
        self.__rgb_sensor.stop()
        self.__ultrasonic_sensor_top.stop()
        self.__left_ultrasonic_sensor.stop()
        self.__right_ultrasonic_sensor.stop()

if __name__ == "__main__":
    test_u = Car()
    while True:
        print("\nMenu:")
        print("1. Faire avancer la voiture")
        print("2. Faire un demi-tour")
        print("3. Eviter les obstacles")
        print("4. Arrêter la voiture et quitter")
        print("5. Détecter la couleur verte")
        
        choice = input("Choisissez une option (1-5): ")
        
        if choice == "1":
            try:
                test_u.run_straigth(50, 8) # Test de la méthode run_straigth

            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()
                
        elif choice == "2":
            try:
                test_u.u_turn() # Test de la méthode u_turn
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()
                
        elif choice == "3":
            try:
                test_u.dodge_obstacle() # Test de la méthode dodge_obstacle
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()

        elif choice == "4":
            print("Arrêt de la voiture et sortie du programme.")
            GPIO.cleanup()
            break

        elif choice == "5":
            try:
                test_u.detect_green() 
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()

        else:
            print("Option invalide. Veuillez réessayer.")
        
    

    
    