from Capteur.sensor import Sensor
import RPi.GPIO as GPIO
import time

class LineFollowSensor(Sensor):
    def __init__(self, name: str, connexion_port: str, out_pin: int):
        """
        Initialise le capteur suiveur de ligne avec un nom, un port et une broche de sortie GPIO.
        """
        super().__init__(name, connexion_port)
        self._out_pin = out_pin
        self.__is_on_line = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._out_pin, GPIO.IN)
        
    @property
    def is_on_line(self):
        """
        Retourne True si la ligne est détectée (niveau bas), False sinon.
        """
        with self._lock:
            return self.__is_on_line
        
    def run(self):
        """
        Boucle principale du thread. Met à jour la détection de ligne toutes les secondes.
        """
        while self._running:
            print("Vérification de la ligne...")
            self.__is_on_line = self.read_data()
            print(f"Capteur sur la ligne : {self.__is_on_line}")
            time.sleep(1)

    def read_data(self) -> bool:
        """
        Lit l'état du GPIO : True si ligne détectée (niveau bas), False sinon.
        """
        try:
            with self._lock:
                return GPIO.input(self._out_pin) == GPIO.LOW
        except Exception as e:
            error = f"Erreur de lecture du capteur : {e}"
            print(error)
            self._log.write(error)
            return False

    def detect_line(self) -> str:
        """
        Retourne un message en fonction de la détection de la ligne.
        """
        return "Line detected" if self.read_data() else "No line detected"

    def stop(self):
        """
        Arrête proprement le thread s'il est lancé, et libère la broche GPIO.
        """
        if self.is_alive():
            self._running = False
            self.join()
        GPIO.cleanup(self._out_pin)