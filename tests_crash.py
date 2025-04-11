import os
import subprocess
import socket
import time
import RPi.GPIO as GPIO
from moteurs.DCMotor import DCMotor
from moteurs.ServoMoteur import ServoMoteur
from capteurs.LineFollowSensor import LineFollowSensor
from capteurs.RGB_sensor import RGBSensor

class SystemChecker():
    """
    Classe permettant de vérifier l'état des différents composants matériels d'un Raspberry Pi :
    - Bus I2C et présence de l'INA219
    - Température et tension CPU
    - Broches GPIO
    - Capteurs ultrason
    - Moteurs DC
    - Servo moteur
    """

    def __init__(self):
        '''
        Consructeur de la classe SystemChecker
        Initialisation de l'I2C, GPIO, DC moteurs et servo moteur
        '''
        self.i2c_path = "/dev/i2c-1"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.motor = DCMotor()
        self.servo = ServoMoteur()
        self.rgb_sensor = RGBSensor("RGB", "I2C")
        self.line_follow_sensor = LineFollowSensor("LineFollow", "I2C", 20)

    def check_i2c(self):
        '''
        Vérifie présence de l'INA219 sur l' I2C
        '''
        try:
            if not os.path.exists(self.i2c_path):
                raise FileNotFoundError(f"{self.i2c_path} non détecté")
            output = subprocess.check_output(["i2cdetect", "-y", "1"]).decode()
            if "40" in output or "41" in output:
                print(" I2C OK - INA219 détecté")
            else:
                print(" I2C ERROR - INA219 non détecté")
        except Exception as e:
            print(f" I2C ERROR - {e}")

    def check_cpu_temp(self):
        '''
        Vérifie la température du CPU
        '''
        try:
            temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode().strip()
            print(f" Température CPU : {temp}")
        except Exception as e:
            print(f" Température CPU - erreur : {e}")

    def check_voltage(self):
        '''
        Vérifie tension du CPU
        '''
        
        try:
            voltage = subprocess.check_output(["vcgencmd", "measure_volts"]).decode().strip()
            print(f" Tension CPU : {voltage}")
        except Exception as e:
            print(f" Tension CPU - erreur : {e}")

    def check_gpio(self, pins):
        """
        Vérifie si broches GPIO choisies sont configurées correctement.
        :param pins: Liste des broches GPIO à vérifier.(Celle qu'on utilise pour le module)
        """
        try:
            for pin in pins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(pin, GPIO.LOW)
                print(f" GPIO {pin} testé avec succès.")
        except Exception as e:
            print(f" GPIO ERROR - {e}")

    def check_ultrasonic_sensor(self, trigger_pin, echo_pin):
        """
        Vérifie le fonctionnement du capteur ultrason
        :param trigger_pin: Pin déclenchement
        :param echo_pin: Pin écho
        """
        try:
            GPIO.setup(trigger_pin, GPIO.OUT)
            GPIO.setup(echo_pin, GPIO.IN)
            GPIO.output(trigger_pin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trigger_pin, GPIO.LOW)

            start_time = time.time()
            stop_time = start_time  # Initialisation de stop_time

            # Attendre que le signal d'écho commence
            timeout = time.time() + 1  # Timeout de 1 seconde
            while GPIO.input(echo_pin) == 0:
                start_time = time.time()
                if time.time() > timeout:
                    raise TimeoutError("Aucun signal d'écho reçu (timeout)")

            # Attendre que le signal d'écho se termine
            timeout = time.time() + 1  # Timeout de 1 seconde
            while GPIO.input(echo_pin) == 1:
                stop_time = time.time()
                if time.time() > timeout:
                    raise TimeoutError("Signal d'écho trop long (timeout)")

            elapsed_time = stop_time - start_time
            distance = (elapsed_time * 34300) / 2  # Distance en cm
            print(f" Capteur ultrason OK - Distance mesurée : {distance:.2f} cm")
        except TimeoutError as e:
            print(f" Capteur ultrason ERROR - {e}")
        except Exception as e:
            print(f" Capteur ultrason ERROR - {e}")

    def check_motors(self, motor):
        """
        Vérifie fonctionnement des moteurs
        :param motor: Instance classe DCMotor
        """
        try:
            print(" Test des moteurs en cours...")
            motor.motor_forward(50)
            time.sleep(1)
            motor.motor_backward(-50)
            time.sleep(1)
            motor.stop_motor()
            print(" Moteurs OK")
        except Exception as e:
            print(f" Moteurs ERROR - {e}")

    def check_servo(self, servo):
        """
        Vérifie fonctionnement du servo moteur
        :param servo: Instance classe ServoMoteur
        """
        try:
            print(" Test du servo moteur en cours...")
            servo.set_angle(0)
            time.sleep(1)
            servo.set_angle(30)
            time.sleep(1)
            servo.set_angle(-30)
            time.sleep(1)
            servo.reset()
            print(" Servo moteur OK")
        except Exception as e:
            print(f" Servo moteur ERROR - {e}")

    def cleanup(self):
        """
        Nettoie les GPIO après utilisation pour éviter les conflits
        """
        GPIO.cleanup()
        print(" GPIO nettoyés")

        
    def reboot_system(self):
            try:
                print("Redémarrage du système dans 5 secondes...")
                time.sleep(5)
                os.system("sudo reboot")
            except Exception as e:
                print(f"Erreur lors du redémarrage : {e}")

    def run_checks(self):
        '''
        Exécute toutes les vérifications système
        Exécute les GPIO, capteurs ultrason: devant, gauche, droit et moteur DC
        '''
        print("Début des vérifications système...\n")
        self.check_i2c()
        self.check_cpu_temp()
        self.check_voltage()


        # Ajouter les autres
        self.list_gpio = [4,5,6,9,11,17,18,19,20,26,27,22] # Liste broches GPIO utilisées qu'on vérifie
        self.check_gpio(self.list_gpio) # Liste broches GPIO utiliser qu'on vérifie

        # Vérification du capteur ultrason
        self.check_ultrasonic_sensor(6,5) # Test ultrason devant
        self.check_ultrasonic_sensor(11,9) # Test ultrason gauche
        self.check_ultrasonic_sensor(26,19) # Test ultrason droite

        # Vérification des moteurs
        self.check_motors(self.motor)

        # Vérification du servo moteur
        self.check_servo(self.servo)

        # Vérification du capteur RGB
        self.rgb_sensor.read_data()
        print(self.rgb_sensor.colors)
        self.rgb_sensor.stop()

        # Vérification du capteur suiveur de ligne
        is_on_line = self.line_follow_sensor.read_data()
        print("Le capteur détecte la ligne : ", is_on_line)
        self.line_follow_sensor.stop()

        print("\nVérifications terminées.")

        # Nettoyage des GPIO
        #self.cleanup()
        #print("Nettoyage des GPIO effectué")


if __name__ == "__main__":
    checker = SystemChecker()
    checker.run_checks()