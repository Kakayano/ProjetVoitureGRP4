import board
import busio
import adafruit_tcs34725
from sensor import Sensor
import time

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
        self.__sensor.integration_time = 25
        self.__rvb = {"rouge": 0, "vert": 0, "bleu": 0}
        self.__green_found = False
        
    @property
    def green_found(self):
        """
        Propriété pour vérifier si la couleur verte a été trouvée.
        :return: True si la couleur verte a été trouvée, False sinon
        """
        with self._lock:
            return self.__green_found

    @property
    def colors(self):
        with self._lock:
            return self.__rvb
    
    def run(self):
        while True:
            print("Vérification de la couleur...")
            self.read_data()
            time.sleep(1)
            
            if self.is_green():
                print("La couleur est verte.")
                self.__green_found = True
                return
    

    def read_data(self):
        """
        Lit les données RGB du capteur.
        :return: Dictionnaire des valeurs normalisées RGB
        """
        try :
            r, v, b, _ = self.__sensor.color_raw
            if r is None or v is None or b is None:
                print("Erreur : Données manquantes ou invalides pour RGB.")
                return {"rouge": 0, "vert": 0, "bleu": 0}
            if not r or not v or not b:
                print(f"Avertissement : Une ou plusieurs valeurs RGB sont à 0. Valeurs lues: Rouge={r}, Vert={v}, Bleu={b}.")
                return {"rouge": r if r else 0, "vert": v if v else 0, "bleu": b if b else 0}
            
            print(f"Rouge: {r}, Vert: {v}, Bleu: {b}")
            with self._lock:
                self.__rvb["rouge"] = r
                self.__rvb["vert"] = v
                self.__rvb["bleu"] = b
                
        except Exception as e:
            print(f"Erreur lors de la lecture des données: {e}")
            with self._lock:
                self.__rvb["rouge"] = 0
                self.__rvb["vert"] = 0
                self.__rvb["bleu"] = 0
        time.sleep(0.5)

    def is_green(self, threshold=1.2, min_green=150):
        """
        Vérifie si la couleur détectée est principalement verte.
        :param threshold: Seuil pour déterminer si la couleur est verte
        :param min_green: Valeur minimale pour considérer une couleur comme verte
        :return: True si la couleur est verte, False sinon
        """
        try:
            r, v, b, _ = self.__sensor.color_raw
            with self._lock:
                self.__green_found = v > r * threshold and v > b * threshold and v > min_green
        except Exception as e:
            print(f"Erreur lors de la vérification de la couleur: {e}")
            self.__green_found = False
