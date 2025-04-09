from sensor import Sensor
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
        Propriété pour vérifier si le capteur est sur la ligne.
        """
        with self._lock:
            return self.__is_on_line
        
    def run(self):
        while self._running:
            # print("Vérification de la ligne...")
            self.__is_on_line = self.read_data()
            # print(f"Capteur sur la ligne : {self.__is_on_line}")
            self._log.write(f"Capteur sur la ligne : {self.__is_on_line}", "debug")
            time.sleep(1)
                
            
    def read_data(self) -> bool:
        """
        Lit l'état du capteur : True si ligne détectée (niveau haut), False sinon.
        """
        try:
            with self._lock:
                return GPIO.input(self._out_pin) == GPIO.HIGH
        except Exception as e:
            error = f"Erreur de lecture du capteur : {e}"
            # print(error)
            self._log.write(error, "error")
            return False
