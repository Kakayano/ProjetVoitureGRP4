import board
import busio
import adafruit_tcs34725
from ProjetVoitureGRP4.sensor import Sensor
import threading

class RGBSensor(Sensor):
    def __init__(self, name: str, connexion_port: str):
        super().__init__(name, connexion_port)
        
        """
        Initialise le capteur RGB TCS34725 avec le nom et le port de connexion.
        :param name: Nom du capteur
        :param connexion_port: Port de connexion (non utilisé dans ce cas)
        :param i2c: Bus I2C pour la communication avec le capteur
        :param sensor: Instance du capteur TCS34725
        """
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = adafruit_tcs34725.TCS34725(self.__i2c)
        self.__thread = threading.Thread(target=self.is_green)
        self.__thread.daemon = True
        self.__thread.start()
        
    @property
    def sensor(self):
        """
        Retourne l'instance du capteur.
        :return: Instance du capteur TCS34725
        """
        return self.__sensor
    
    @sensor.setter
    def sensor(self, value):
        """
        Définit l'instance du capteur.
        :param value: Instance du capteur TCS34725
        """
        self.__sensor = value

    def read_data(self):
        """
        Lit les données RGB du capteur.
        :return: Dictionnaire des valeurs normalisées RGB
        """
        r, v, b, _ = self.__sensor.color_raw
        with self._lock:
            return {
                "rouge": r,
                "vert": v,
                "bleu": b
            }

    def is_green(self, threshold=1.5, min_green=150):
        """
        Vérifie si la couleur détectée est principalement verte.
        :param threshold: Seuil pour déterminer si la couleur est verte
        :param min_green: Valeur minimale pour considérer une couleur comme verte
        :return: True si la couleur est verte, False sinon
        """
        r, v, b, _ = self.__sensor.color_raw
        with self._lock:
            return v > r * threshold and v > b * threshold and v > min_green


    def stop(self):
        """
        Arrête le thread de mise à jour du capteur.
        Cette méthode doit être appelée pour libérer les ressources lorsque le capteur n'est plus utilisé.
        """
        self.__thread.join()
        self.__sensor.close()