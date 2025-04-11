from Moteur.DCMotor import DCMotor
from Moteur.ServoMoteur import ServoMoteur
from Capteur.ultrasonic_sensor import UltrasonicSensor
from Capteur.LineFollowSensor import LineFollowSensor
from Capteur.rgb_sensor import RGBSensor
from RestartCrash import SystemChecker
import os

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
        self.__line_follow_sensor = LineFollowSensor("LineFollow", "GPIO", 20)
        self.__rgb_sensor = RGBSensor("RGB", "I2C")
        self.__is_green = False
        self.__system_checker = SystemChecker()

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

            if distance is not None and distance < 25:
                print(f" Obstacle détecté à {distance} cm.")
                self._run_dodge = False

                self.__motor.stop_motor()
                time.sleep(0.5)

                self.__servo.set_angle(-25)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()

                self.__servo.set_angle(25)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__motor.stop_motor()

                self.__servo.set_angle(0)
                self.__motor.motor_forward(30)
                time.sleep(3)
                self.__motor.stop_motor()

                self.__servo.set_angle(-25)
                self.__motor.motor_forward(30)
                time.sleep(2)
                self.__servo.set_angle(0)
                self.__motor.motor_forward(30)
                time.sleep(0.5)
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
        i = True
        if side == "L":
            while i:
                self.__motor.motor_forward(70)
                self.__ultrasonic_sensor_left.read_data()
                distance = self.__ultrasonic_sensor_left.distance
                self.__ultrasonic_sensor_top.read_data()
                distance_top = self.__ultrasonic_sensor_top.distance
                if distance is not None and distance < 5 :
                    print(distance)
                    print("mur à gauche -5")
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(25)
                elif distance is not None and distance < 10:
                    print(distance)
                    print("mur à gauche -10")
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(10)
                elif distance is not None and distance > 30 :
                    print(distance)
                    print("mur plus à gauche +30")
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(-25)
                elif distance is not None and distance > 20:
                    print(distance)
                    print("mur plus à gauche +15")
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(-10)
                elif distance is not None and distance_top < 5:
                    print(distance_top)
                    print("mur au devant")
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(-25)
                else:
                    self.__servo.set_angle(0)  
                    print(distance)
                '''
                if self.__ultrasonic_sensor_top.distance <= 5:
                    self.__motor.stop_motor()
                    i = False
                    break'''
                    
        elif side == "R":
            while i:
                self.__motor.motor_forward(70)
                self.__ultrasonic_sensor_right.read_data()
                distance = self.__ultrasonic_sensor_right.distance
                self.__ultrasonic_sensor_top.read_data()
                if distance is not None and distance < 5:
                    print(distance)
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(-25)
                elif distance is not None and distance < 10:
                    print(distance)
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(-10)
                elif distance is not None and distance > 30:
                    print(distance)
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(25)
                elif distance is not None and distance > 15:
                    print(distance)
                    self.__motor.motor_forward(30)
                    self.__servo.set_angle(10)
                else:
                    self.__servo.set_angle(0)  

                if self.__ultrasonic_sensor_top.distance <= 5:
                    self.__motor.stop_motor()
                    i = False
                    break     
        else:
            raise ValueError("Le côté doit être 'L' ou 'R'.")

    def check(self):
        '''
        Méthode pour vérifier le système
        '''
        self.__system_checker.run_checks()
        

    def run_for_laps(self, laps=1, speed=50):
        '''
        Fait avancer la voiture et utilise le capteur de ligne pour compter le nombre de tours effectués.
        La voiture s'arrête immédiatement après avoir détecté le nombre de lignes correspondant aux tours demandés.

        :param laps: Nombre de passages sur la ligne (tours) avant arrêt
        :param speed: Vitesse à laquelle la voiture avance
        '''
        if laps <= 0:
            print("Le nombre de tours doit être supérieur à 0.")
            return

        self.__servo.disable()
        self.__motor.motor_forward(speed)

        current_lap = -1 # Doit passer la première ligne pour être à 0
        on_line = False

        try:
            while True:
                line_detected = self.__line_follow_sensor.read_data()

                # Détection du front montant : passage de False à True
                if line_detected and not on_line:
                    current_lap += 1
                    print(f"Ligne détectée - Tour {current_lap}")
                    on_line = True

                    if current_lap >= laps:
                        print("Nombre de tours atteint, arrêt de la voiture.")
                        self.__motor.stop_motor()
                        break

                elif not line_detected:
                    on_line = False

                time.sleep(0.05)

        except Exception as e:
            print(f"Erreur pendant le comptage des tours : {e}")
            self.__motor.stop_motor()

    def detect_color(self):
        '''
        Méthode pour détecter la couleur
        '''
        self.__rgb_sensor.start()
        while True:
            self.__is_green = self.__rgb_sensor.is_green()
            if self.__is_green:
                self.__motor.motor_forward(30)
                time.sleep(0.1)
                break
        
    def track_less_green(self):
        '''
        Méthode pour faire avancer la voiture
        '''
        i = True
        self.__motor.motor_forward(70)
        self.__servo.set_angle(0)
        while i:
            line_detected = self.__line_follow_sensor.read_data()

            self.__ultrasonic_sensor_right.read_data()
            distance_right = self.__ultrasonic_sensor_right.distance
            self.__ultrasonic_sensor_left.read_data()
            distance_left = self.__ultrasonic_sensor_left.distance
            self.__ultrasonic_sensor_top.read_data()
            distance_top = self.__ultrasonic_sensor_top.distance
            T = 'D'
                
            if distance_top is None or distance_top < 9  or distance_top >= 400:
                print("distance_top")
                self.__motor.motor_backward(-45)
                if T == 'R':
                    self.__servo.set_angle(30)
                elif T == 'L':
                    self.__servo.set_angle(-30)
                else:
                    self.__servo.set_angle(20)
                time.sleep(0.4)
                self.__servo.set_angle(0)

            if distance_left is not None and distance_right is not None and ( distance_right > 1.5 * distance_left or distance_left < 12 ):
                T = 'R'
                #print(distance_right)
                #print(distance_left)
                self.__servo.set_angle(25)
                self.__motor.motor_forward(25) 
            elif distance_left is not None and distance_right is not None and (distance_left > 1.5 * distance_right or distance_right < 12):
                T = 'L'
                #print(distance_right)
                #print(distance_left)
                self.__servo.set_angle(-25)
                self.__motor.motor_forward(25)
            elif distance_left is not None and distance_right is not None and distance_left >60 and distance_right > 60:
                T = 'D'
                self.__servo.set_angle(0)
                self.__motor.motor_forward(40)
            else:
                T = 'D'
                self.__servo.set_angle(0)
                self.__motor.motor_forward(40)
                time.sleep(0.1)
            print("devant" ,distance_top)
            print("gauche" ,distance_left)
            print("droite" ,distance_right)

            

    def track_finish(self, laps=1):
        '''
        Méthode pour la course
        '''
        self.detect_color()
        self.track_less_green_for_laps(laps=laps)

    def reboot_system(self):
        self.__system_checker.reboot_system()
     
    def track_less_green_for_laps(self, laps=1):
        '''
        Suivre un circuit tout en comptant un nombre de tours à partir de la ligne noire.
        '''
        if laps <= 0:
            print("Le nombre de tours doit être supérieur à 0.")
            return

        print(f"Début de la course pour {laps} tour(s).")
        current_lap = -1  # Attente du premier passage
        on_line = False

        self.__motor.motor_forward(70)
        self.__servo.set_angle(0)

        try:
            while True:
                # Détection ligne noire
                line_detected = self.__line_follow_sensor.read_data()
                if line_detected and not on_line:
                    current_lap += 1
                    print(f"Ligne détectée - Tour {current_lap}")
                    on_line = True

                    if current_lap >= laps:
                        print("Nombre de tours atteint. Arrêt.")
                        self.__motor.stop_motor()
                        break
                elif not line_detected:
                    on_line = False

                # Lecture des distances
                self.__ultrasonic_sensor_right.read_data()
                distance_right = self.__ultrasonic_sensor_right.distance
                self.__ultrasonic_sensor_left.read_data()
                distance_left = self.__ultrasonic_sensor_left.distance
                self.__ultrasonic_sensor_top.read_data()
                distance_top = self.__ultrasonic_sensor_top.distance

                # Évitement obstacle
                if distance_top is None or distance_top < 9 or distance_top >= 400:
                    print("Obstacle devant")
                    self.__motor.motor_backward(-45)
                    self.__servo.set_angle(20)
                    time.sleep(0.4)
                    self.__servo.set_angle(0)

                # Évitement latéral
                if distance_left and distance_right:
                    if distance_right > 1.5 * distance_left or distance_left < 12:
                        self.__servo.set_angle(25)
                        self.__motor.motor_forward(25)
                    elif distance_left > 1.5 * distance_right or distance_right < 12:
                        self.__servo.set_angle(-25)
                        self.__motor.motor_forward(25)
                    elif distance_left > 60 and distance_right > 60:
                        self.__servo.set_angle(0)
                        self.__motor.motor_forward(40)
                    else:
                        self.__servo.set_angle(0)
                        self.__motor.motor_forward(40)

                time.sleep(0.05)

        except Exception as e:
            print(f"Erreur pendant le suivi : {e}")
            self.__motor.stop_motor()


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
    def menu():
        test_u = Car()
        while True:
            print("\nMenu:")
            print("1. Faire avancer la voiture")
            print("2. Faire un demi-tour")
            print("3. Eviter les obstacles")
            print("4. Arrêter la voiture et quitter")
            print("5. Arrêter la voiture après la ligne d'arrivée")
            print("6. Suivre un mur")
            print("7. Détecter la couleur")
            print("8. Suivre le parcours")
            print("9. Vérifier le système")
            print("10. Commencer la course avec le feu vert")
            print("11. Effectuer un nombre de tours")
            print("12. Suivre le parcours avec le feu vert")
            print("13. Reboot le système")


            choice = input("Choisissez une option (1-13): ")

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
            
            elif choice == "5":
                try:
                    test_u.stop_after_finish_line()
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

            elif choice == "7":
                try:
                    test_u.detect_color()
                except KeyboardInterrupt:
                    print("Interruption clavier détectée. Arrêt des moteurs...")
                    test_u.stop_car()
                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    test_u.stop_car()

            elif choice == "8":
                try:
                    test_u.track_less_green()
                except KeyboardInterrupt:
                    print("Interruption clavier détectée. Arrêt des moteurs...")
                    test_u.stop_car()

                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    test_u.stop_car()

            elif choice == "9":
                try:
                    test_u.check()
                except KeyboardInterrupt:
                    print("Interruption clavier détectée. Arrêt des moteurs...")
                    test_u.stop_car()

                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    test_u.stop_car()

            elif choice == "10":
                try:
                    laps = int(input("Entrez le nombre de tours à effectuer : "))
                    test_u.track_finish(laps=laps)
                except KeyboardInterrupt:
                    print("Interruption clavier détectée. Arrêt des moteurs...")
                    test_u.stop_car()
                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    test_u.stop_car()

            elif choice == "11":
                try:
                    laps = int(input("Entrez le nombre de tours à effectuer : "))
                    test_u.run_for_laps(laps=laps, speed=50)
                except KeyboardInterrupt:
                    print("Interruption clavier détectée. Arrêt des moteurs...")
                    test_u.stop_car()
                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    test_u.stop_car()

            elif choice == "12":
                try:
                    laps = int(input("Nombre de tours à effectuer avec suivi du parcours : "))
                    test_u.track_less_green_for_laps(laps)
                except KeyboardInterrupt:
                    print("Interruption clavier détectée. Arrêt des moteurs...")
                    test_u.stop_car()
                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    test_u.stop_car()

            elif choice == "13":
                try:
                    test_u.reboot_system()
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
    menu()