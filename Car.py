from Moteur.DCMotor import DCMotor
from Moteur.ServoMoteur import ServoMoteur
from Capteur.rgb_sensor import RGBSensor
from Capteur.ultrasonic_sensor import UltrasonicSensor
from Capteur.LineFollowSensor import LineFollowSensor
from Capteur.CurrentSensor import CurrentSensor
from Capteur.sensor import Sensor

import threading
import time

class Car:
    def __init__(self):
        '''
        On initialise la voiture avec les moteurs, le servo moteur et les capteurs
        '''
        self.__motor = DCMotor()
        self.__servo = ServoMoteur()
        self.__rgb = RGBSensor("RGB", "I2C")
        self.__ultrasonic_top = UltrasonicSensor("Ultrasonic", "GPIO", 6, 5)
        self.__ultrasonic_right = UltrasonicSensor("Ultrasonic", "GPIO", 26, 19)
        self.__ultrasonic_left = UltrasonicSensor("Ultrasonic", "GPIO", 11, 9)
        self.__line_follow_sensor = LineFollowSensor("LineFollow", "GPIO", 20)
        self.__current_sensor = CurrentSensor("Current", "I2C")

    def forward(self, speed=100, period=2): # Avancer la voiture
        '''
        Avancer la voiture en utilisant le moteur DC
        elle prend en paramètre la vitesse et la durée
        on utilise un thread pour éviter de bloquer le programme principal
        '''
        def run():
            with self.__lock: ## Utilisation d'un verrou pour éviter les accès concurrents
                print("Avancer")
                self.__motor.motor_forward(speed)
                time.sleep(period)
                self.__motor.stop_motor()
                print(" Arrêt après avance")
        thread = threading.Thread(target=run)
        thread.start()


    def turn_left(self, angle=30): # Tourner à gauche
        '''
        Tourner à gauche en utilisant le servo moteur
        elle prend en paramètre l'angle
        '''
        print(" Tourner à gauche")
        self.__servo.set_angle(-abs(angle))

    def turn_right(self, angle=30): # Tourner à droite
        '''
        Tourner à droite en utilisant le servo moteur
        elle prend en paramètre l'angle
        '''
        print("Tourner à droite")
        self.__servo.set_angle(abs(angle)) 

    def straitght(self): # Avancer tout droit
        '''
        Avancer tout droit en utilisant le servo moteur
        '''
        print("Direction tout droit")
        self.__servo.set_angle(0)

    def stop(self): # Arrêter les moteursdc et remettre la direction à 0
        '''
        Arrêter les moteurs DC et remettre la direction à 0
        '''
        self.__motor.motor_stop()
        self.tout_droit()

    def backward(self, speed=-100, period=2): # Reculer la voiture
        '''
        Reculer la voiture en utilisant le moteur DC
        elle prend en paramètre la vitesse et la durée
        on utilise un thread pour éviter de bloquer le programme principal
        '''
        def run():
            with self.__lock: ## Utilisation d'un verrou pour éviter les accès concurrents
                print("Reculer")
                self.__motor.motor_backward(speed)
                time.sleep(period)
                self.__motor.stop_motor()
                print(" Arrêt après recul")
        thread = threading.Thread(target=run)
        thread.start()
        
    def get_forward_distance(self):
        return self.__ultrasonic_top.update_distance()
    
    def get_left_distance(self):
        return self.__ultrasonic_left.update_distance()
    
    def get_right_distance(self):
        return self.__ultrasonic_right.update_distance()
    
    def start(self): # Démarrer la voiture après que le capteur RGB ait détecté une couleur verte
        '''
        Démarrer la voiture après que le capteur RGB ait détecté une couleur verte
        '''
        if self.__rgb.is_green():
            print("La couleur est verte !")
            self.run()

    def u_turn(self,side='R' ,angle=45, speed=20 , duration=3): # Méthode pour faire un demi-tour
        '''
        Méthode pour faire un demi-tour à gauche ou à droite
        elle prend en paramètre le côté (gauche ou droite), l'angle, la vitesse et la durée
        '''
        if side == 'R': # demi-tour à droite
            self.turn_right(angle)
            self.forward(speed, duration)
        elif side == 'L': # demi-tour à gauche
            self.turn_left(angle)
            self.forward(speed, duration)
        else:
            self.stop()

    def run_straigth(self, speed=50, duration=5): # Méthode pour faire avancer la voiture
        '''
        Méthode pour faire avancer la voiture
        elle prend en paramètre la vitesse et la durée
        '''
        self.straitght()
        self.forward(speed, duration)
        self.stop()

    def count_turn(self, nbr_turn=1):
        '''
        Compte le nombre de tours effectués par la voiture et arrête la voiture après un nombre spécifié de tours.

        Arguments :
            nbr_turn (int) : Le nombre de tours à compter avant d'arrêter la voiture. Par défaut, 1.

        Comportement :
            - La méthode vérifie en continu le capteur de suivi de ligne pour détecter quand la voiture traverse une ligne.
            - Un tour est compté lorsque la ligne est détectée et qu'un intervalle de temps minimum s'est écoulé depuis la dernière détection.
            - La voiture s'arrête automatiquement une fois que le nombre spécifié de tours (`nbr_turn`) est atteint.

        Remarques :
            - La méthode utilise un petit délai (`time.sleep(0.1)`) pour éviter une attente active lors de la réinitialisation du temps de départ.
            - La méthode `self.stop()` est appelée pour arrêter la voiture après que le nombre de tours a été atteint.
        '''
        print(f"Début du comptage pour {nbr_turn} tour(s).")
        count = 0
        start_time = None
        run = True
        while run:
            if self.__line_follow_sensor.detect_line() == "Line detected":
                if start_time is None:
                    start_time = time.time()
                elif time.time() - start_time > 1:
                    count += 1
                    print(f"Tour n°: {count}")
                    start_time = None  
                else:
                    start_time = None 
                    time.sleep(0.1)  
            if count >= nbr_turn:
                run = False
        self.stop()
        print(f"Final count: {count}")
