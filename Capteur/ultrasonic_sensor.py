from gpiozero import DistanceSensor
from Capteur.sensor import Sensor
import time

class UltrasonicSensor(Sensor):
    def __init__(self, name: str, connexion_port: str, trigger_pin: int, echo_pin: int):
        super().__init__(name, connexion_port)

        """
        Initialise le capteur ultrasonique avec le nom, le port de connexion, le pin de déclenchement et le pin d'écho.
        :param name: Nom du capteur
        :param connexion_port: Port de connexion (non utilisé dans ce cas)
        :param trigger_pin: Pin de déclenchement
        :param echo_pin: Pin d'écho
        :param sensor: Capteur ultrason (DistanceSensor de gpiozero)
        :param distance: Distance mesurée (en cm)
        :param stop_thread: Indicateur pour arrêter le thread de mise à jour
        :param lock: Verrou pour gérer les accès concurrents à la distance
        :param thread: Thread pour mettre à jour la distance
        """
        
        self.__sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=4.0)
        self.__distance = None
        self.__min_distance = 0.03
        
    @property
    def distance(self):
        """
        Propriété pour obtenir la distance mesurée par le capteur.
        :return: Distance mesurée (en cm)
        """
        with self._lock:
            return self.__distance

    def run(self):
        """
        Méthode exécutée dans le thread pour mettre à jour la distance mesurée par le capteur.
        Elle est appelée automatiquement lors du démarrage du thread.
        """
        while self._running:
            self.read_data()

    def read_data(self):
        """
        Méthode pour mettre à jour la distance mesurée par le capteur.
        Cette méthode est exécutée dans un thread séparé pour éviter de bloquer le programme principal.
        Elle lit la distance du capteur toutes les 0.1 secondes et met à jour l'attribut _distance.
        La distance est convertie en centimètres (m * 100) et arrondie à deux décimales.
        """
        with self._lock:
            if self.__sensor.distance is None:
                self.__distance = None
                message = "Aucun écho reçu, la distance est hors de portée."
                print(message)
                self._log.write(message)
            elif self.__sensor.distance > self.__sensor.max_distance:
                self.__distance = None
                message = f"Distance hors de portée, au-delà de {self.__sensor.max_distance} mètres."
                print(message)
                self._log.write(message)
            elif self.__sensor.distance < self.__min_distance:
                self.__distance = None
                message = "Distance trop proche, capteur hors de portée."
                print(message)
            else:
                self.__distance = round(self.__sensor.distance * 100, 2)
                message = f"Distance mesurée: {self.__distance} cm"
                print(message)
                
            self._log.write(message)

        time.sleep(1)