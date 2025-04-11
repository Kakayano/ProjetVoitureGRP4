from moteurs.DCMotor import DCMotor
from moteurs.ServoMoteur import ServoMoteur
from capteurs.ultrasonic_sensor import UltrasonicSensor
from capteurs.LineFollowSensor import LineFollowSensor
from capteurs.RGB_sensor import RGBSensor

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
            
    def run_until_line_then_stop(self, speed=50, post_detection_duration=0.5):
        '''
        Fait avancer la voiture et s'arrête peu après avoir détecté une ligne noire.
        La ligne est détectée une seule fois, puis la voiture continue brièvement avant de s'arrêter.

        :param speed: Vitesse du moteur pendant le déplacement (défaut = 50)
        :param post_detection_duration: Durée d'avance après détection (secondes)
        '''
        self.__servo.disable()
        self.__motor.motor_forward(speed)

        try:
            while True:
                line_detected = self.__line_follow_sensor.read_data()
                print(f"Détection actuelle : {line_detected}")

                if line_detected:
                    print("ligne détectée")
                    time.sleep(post_detection_duration)  # avance encore un petit peu
                    self.__motor.stop_motor()
                    break

                time.sleep(0.01)

        except Exception as e:
            print(f"Erreur pendant le suivi de ligne : {e}")
            self.__motor.stop_motor()

    def along_wall(self, side = "L"):
        '''
        Méthode pour suivre un mur
        '''
        green_detected = self.detect_color()
        i = True
        if green_detected:
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
            elif side == "LR":
                self.__motor.motor_forward(70)
                self.__servo.set_angle(0)
                while i:
                    self.__ultrasonic_sensor_right.read_data()
                    distance_right = self.__ultrasonic_sensor_right.distance
                    self.__ultrasonic_sensor_left.read_data()
                    distance_left = self.__ultrasonic_sensor_left.distance
                    self.__ultrasonic_sensor_top.read_data()
                    distance_top = self.__ultrasonic_sensor_top.distance
                    
                    if distance_left is not None and distance_right is not None and ( distance_right > 1.5 * distance_left or distance_left < 12 ):
                        if distance_top is None or distance_top < 9:
                            print("distance_top")
                            self.__motor.motor_backward(-50)
                            self.__servo.set_angle(-25)
                            #time.sleep(0.4)
                            self.__servo.set_angle(0)
                        #print(distance_right)
                        #print(distance_left)
                        self.__servo.set_angle(25)
                        self.__motor.motor_forward(30) 
                    elif distance_left is not None and distance_right is not None and (distance_left > 1.5 * distance_right or distance_right < 12):
                        if distance_top is None or distance_top < 9:
                            print("distance_top")
                            self.__motor.motor_backward(-50)
                            self.__servo.set_angle(25)
                            #time.sleep(0.4)
                            self.__servo.set_angle(0)
                        #print(distance_right)
                        #print(distance_left)
                        self.__servo.set_angle(-25)
                        self.__motor.motor_forward(30)
                    elif distance_left is not None and distance_right is not None and distance_left >60 and distance_right > 60:
                        if distance_top is None or distance_top < 9:
                            print("distance_top")
                            self.__motor.motor_backward(-50)
                            self.__servo.set_angle(0)
                            #time.sleep(0.4)
                            self.__servo.set_angle(0)
                        self.__servo.set_angle(0)
                        self.__motor.motor_forward(45)
                    else:
                        if distance_top is None or distance_top < 9:
                            print("distance_top")
                            self.__motor.motor_backward(-50)
                            self.__servo.set_angle(0)
                            #time.sleep(0.4)
                            self.__servo.set_angle(0)
                        self.__servo.set_angle(0)
                        self.__motor.motor_forward(45)
                        time.sleep(0.1)
                    print("devant" ,distance_top)
                    print("gauche" ,distance_left)
                    print("droite" ,distance_right)
                    
            else:
                raise ValueError("Le côté doit être 'L' ou 'R'.")
                

    def stop_after_finish_line(self, speed=30):
        '''
        Méthode pour faire avancer la voiture et s'arrêter après avoir franchi la ligne d'arrivée.
        La voiture avance à la vitesse spécifiée, détecte la ligne d'arrivée, 
        puis continue un peu avant de s'arrêter.
        '''
        print("La voiture recherche la ligne d'arrivée...")
        
        # Activer le capteur de ligne s'il n'est pas déjà actif
        self.__line_follow_sensor.start()
        
        # Préparation et démarrage
        self.__servo.set_angle(0)  # Voiture en ligne droite
        self.__motor.motor_forward(speed)
        
        line_found = False
        start_time = time.time()
        
        try:
            while not line_found:
                # Vérifier si la ligne est détectée
                if self.__line_follow_sensor.read_data():
                    print("Ligne d'arrivée détectée!")
                    line_found = True
                    
                    # Continue d'avancer pendant un court moment après la ligne
                    time.sleep(0.5)  # Continue sur environ 15 cm à vitesse 30%
                    
                    # Arrêt des moteurs
                    self.__motor.stop_motor()
                    print("Voiture arrêtée après la ligne d'arrivée")
                    break
                
                # Petit délai entre les vérifications
                time.sleep(0.05)
                
                # Mesure de sécurité: timeout après 60 secondes
                if time.time() - start_time > 60:
                    print("Timeout: Aucune ligne détectée après 60 secondes")
                    break

        except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            self.__motor.stop_motor()
            print("Moteurs arrêtés")    

    def detect_color(self):
        '''
        Méthode pour détecter la couleur
        '''
        self.__rgb_sensor.start()
        while True:
            if self.__rgb_sensor.is_green():
                return self.__rgb_sensor.is_green()
            
                
        
    def course(self):
        '''
        Méthode pour faire avancer la voiture
        '''
        side = "L"
        while True:
            self.along_wall(side)
            self.__motor.motor_forward(40)
            if side == "L":
                side = "R"
            else:
                side = "L"
            

    def stop_car(self):
        '''
        Méthode pour arrêter la voiture
        '''
        self._run_dodge = False
        if self._dodge_thread and self._dodge_thread.is_alive():
            self._dodge_thread.join()
        self.__motor.stop_motor()
        self.__servo.disable()
        GPIO.cleanup()

if __name__ == "__main__":
    test_u = Car()
    while True:
        print("\nMenu:")
        print("1. Faire avancer la voiture")
        print("2. Faire un demi-tour")
        print("3. Eviter les obstacles")
        print("4. Arrêter la voiture et quitter")
        print("5. S'arrêter après la ligne d'arrivée")
        print("6. Suivre le mur à gauche")
        print("7. Détecter la couleur")
        print("8. Suivre le mur à gauche et à droite")
        print("9. Avancer jusqu'à la ligne puis s'arrêter")

        choice = input("Choisissez une option (1-9): ")

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
                test_u.along_wall("LR")
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()

            except Exception as e:
                print(f"Erreur : {e}")
            finally:
                test_u.stop_car()
                
        elif choice == "9":
            try:
                test_u.run_until_line_then_stop(speed=50, post_detection_duration=0.8)
            except KeyboardInterrupt:
                print("Interruption clavier détectée. Arrêt des moteurs...")
                test_u.stop_car()
                GPIO.cleanup()
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