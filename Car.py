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
        self.__ultrasonic_sensor_top = UltrasonicSensor("Ultrasonic", "GPIO", trigger=6, echo=5) # Capteur ultrasonique pour la détection d'obstacles
        

    
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
            distance = self.__ultrasonic_sensor_top.distance
            if distance is not None and distance < 0.5:
                print(f"Obstacle détecté à {distance:.2f} m. Arrêt des moteurs.")
                self.__motor.stop_motor()
                run = False
            else:
                print(f"Distance : {distance:.2f} m")
        


    

    def stop_car(self):
        '''
        Méthode pour arrêter la voiture
        '''
        self.__motor.stop_motor() # On arrête les moteurs
        self.__servo.disable()

if __name__ == "__main__":
    test_u = Car()
    while True:
        print("\nMenu:")
        print("1. Faire avancer la voiture")
        print("2. Faire un demi-tour")
        print("3.")
        print("4. Arrêter la voiture et quitter")
        
        choice = input("Choisissez une option (1-4): ")
        
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
            pass
        elif choice == "4":
            print("Arrêt de la voiture et sortie du programme.")
            GPIO.cleanup()
            break
        else:
            print("Option invalide. Veuillez réessayer.")
        
    

    
    