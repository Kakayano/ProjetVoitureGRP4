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
        while self._running:
            # print("Vérification de la couleur...")
            self.read_data()
            time.sleep(1)
            
            if self.is_green():
                self._log.write("La couleur est verte.", "debug")
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
                with self._lock:
                    self.__rvb = {"rouge": 0, "vert": 0, "bleu": 0}
                    error = "Erreur : Données manquantes ou invalides pour RGB."
                    self._log.write(error, "error")
                raise ValueError(error)
                
            if not r or not v or not b:
                with self._lock:
                    self.__rvb = {"rouge": r if r else 0, "vert": v if v else 0, "bleu": b if b else 0}
                    error = f"Avertissement : Une ou plusieurs valeurs RGB sont à 0. Valeurs lues: Rouge={r}, Vert={v}, Bleu={b}."
                    self._log.write(error, "warning")
                raise ValueError(error)
            
            debug_message = f"Rouge: {r}, Vert: {v}, Bleu: {b}"
            # print(debug_message)
            self._log.write(debug_message, "debug")
            with self._lock:
                self.__rvb["rouge"] = r
                self.__rvb["vert"] = v
                self.__rvb["bleu"] = b
                return self.__rvb
                
        except Exception as e:
            error = f"Erreur lors de la lecture des données RGB: {e}"
            self._log.write(error, "error")
            print(error)
            with self._lock:
                self.__rvb["rouge"] = 0
                self.__rvb["vert"] = 0
                self.__rvb["bleu"] = 0
                raise ValueError(error)
        
        time.sleep(1)

    def is_green(self):
        """
        Vérifie si la couleur détectée est principalement verte.
        :param threshold: Seuil pour déterminer si la couleur est verte
        :return: True si la couleur est verte, False sinon
        """
        try:
            with self._lock:
                self.__green_found = self.__rvb["vert"] > self.__rvb["rouge"] and self.__rvb["vert"] > self.__rvb["bleu"]
        except Exception as e:
            error = f"Erreur lors de la vérification de la couleur: {e}"
            self._log.write(error, "error")
            # print(error)
            self.__green_found = False
        return self.__green_found

    def stop(self):
        """
        Arrête le capteur et libère les ressources.
        """
        super().stop()
        self.__sensor.close()
        self.__i2c.deinit()