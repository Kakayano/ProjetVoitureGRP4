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

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._out_pin, GPIO.IN)

    def read_data(self) -> bool:
        """
        Lit l'état du capteur : True si ligne détectée (niveau bas), False sinon.
        """
        with self._lock:
            return GPIO.input(self._out_pin) == GPIO.LOW
        time.sleep(0.1)

    def detect_line(self) -> str:
        """
        Retourne un message lisible selon la détection de ligne.
        """
        message = "Line detected" if self.read_data() else "No line detected"
        print(message)
        time.sleep(1)
        
        # return "Line detected" if self.read_data() else "No line detected"

    def stop(self):
        """
        Libère la broche GPIO utilisée par ce capteur uniquement.
        """
        GPIO.cleanup(self._out_pin)
