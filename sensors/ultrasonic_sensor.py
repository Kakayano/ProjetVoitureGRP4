from gpiozero import DistanceSensor
from sensor import Sensor
import threading
import time

class UltrasonicSensor(Sensor):
    def __init__(self, name: str, connexion_port: str, log_file, trigger_pin: int, echo_pin: int):
        super().__init__(name, connexion_port, log_file)

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
        
        self.__sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=2.0)
        self.__distance = None
        
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
        with self._lock:
            if self.__sensor.distance is None:
                self.__distance = None
                print("Aucun écho reçu, la distance est hors de portée.")
                    
            elif self.__sensor.distance > self.__sensor.max_distance:
                self.__distance = None
                print(f"Distance hors de portée, au-delà de {self.__sensor.max_distance} mètres.")
            else:
                self.__distance = round(self.__sensor.distance * 100, 2)
                
            self.read_data()
        time.sleep(0.25)

    def read_data(self):
        """
        Lit les données du capteur ultrasonique.
        :return: La distance mesurée (en cm)
        """
        with self._lock:
            if self.__distance is not None:
                print(f"Distance: {self.__distance} cm")
            else:
                print("La distance est hors de portée ou aucun écho reçu.")
            return self.__distance

    def stop(self):
        """
        Arrête le thread de mise à jour de la distance et ferme le capteur.
        Cette méthode doit être appelée pour libérer les ressources lorsque le capteur n'est plus utilisé.
        """
        self.__thread.join()
        self.__sensor.close()
