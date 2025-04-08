import RPi.GPIO as GPIO
import threading
import time
from sensor import Sensor

class UltrasonicSensor(Sensor):
    def __init__(self, name: str, connexion_port: str, trigger_pin: int, echo_pin: int):
        super().__init__(name, connexion_port)
        
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.__distance = None

        # Initialisation des pins GPIO
        GPIO.setmode(GPIO.BCM)  # Utilisation du mode BCM pour la numérotation des pins
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        self.__thread = threading.Thread(target=self.update_distance)
        self.__thread.daemon = True
        self.__thread.start()

    def update_distance(self):
        """
        Méthode pour mettre à jour la distance mesurée par le capteur.
        Cette méthode est exécutée dans un thread séparé pour éviter de bloquer le programme principal.
        Elle lit la distance du capteur toutes les 0.1 secondes et met à jour l'attribut _distance.
        La distance est convertie en centimètres (m * 100) et arrondie à deux décimales.
        """
        while True:
            # Envoi d'une impulsion de 10µs sur le trigger pour lancer la mesure
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)  # 10 microsecondes
            GPIO.output(self.trigger_pin, GPIO.LOW)

            # Mesure du temps pour lequel l'écho est à HIGH
            pulse_start = time.time()
            while GPIO.input(self.echo_pin) == GPIO.LOW:
                pulse_start = time.time()
            
            pulse_end = time.time()
            while GPIO.input(self.echo_pin) == GPIO.HIGH:
                pulse_end = time.time()

            # Calcul de la durée du pulse, et donc de la distance
            pulse_duration = pulse_end - pulse_start
            self.__distance = round(pulse_duration * 17150, 2)  # Distance en cm (vitesse du son = 34300 cm/s)

            self.read_data()
            time.sleep(0.1)  # Attente de 0.1 seconde avant la prochaine lecture

    def read_data(self):
        """
        Lit les données du capteur ultrasonique.
        :return: La distance mesurée (en cm)
        """
        print(f"Distance: {self.__distance} cm")
        return self.__distance

    def stop(self):
        """
        Arrête le thread de mise à jour de la distance et nettoie les broches GPIO.
        Cette méthode doit être appelée pour libérer les ressources lorsque le capteur n'est plus utilisé.
        """
        GPIO.cleanup()  # Nettoie les broches utilisées par GPIO
        self.__thread.join()