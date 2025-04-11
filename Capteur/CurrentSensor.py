import board
import busio
from adafruit_ina219 import INA219
from sensor import Sensor
import time

class CurrentSensor(Sensor):
    def __init__(self, name: str, connexion_port: str):
        """
        Initialise le capteur de courant avec un nom et un port de connexion.
        """
        super().__init__(name, connexion_port)
        
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = INA219(self.__i2c)

        self.__voltage = 0.0
        self.__current = 0.0
        self.__power = 0.0
        
    def run(self):
        """
        Démarre la lecture des données du capteur dans un thread séparé.
        """
        while self._running:
            print("Démarrage de la lecture des données...")
            self.__update_loop()
            time.sleep(1)

    def __update_loop(self):
        """
        Méthode interne qui lit les données en continu dans un thread.
        """
        with self._lock:
            self.__voltage = round(self.__sensor.bus_voltage, 2)
            self.__current = round(self.__sensor.current / 1000, 3)
            self.__power = round(self.__sensor.power / 1000, 2)
            print(f"Current (brut): {self.__sensor.current}mA, Power (brut): {self.__sensor.power}mW")
            print(f"Voltage: {self.__voltage}V, Current: {self.__current}A, Power: {self.__power}W")
        time.sleep(1)

    def read_data(self):
        """ 
        Retourne les dernières données lues.
        """
        try:
            with self._lock:
                return {
                    "voltage": self.__voltage,
                    "current": self.__current,
                    "power": self.__power,
                }
        except Exception as e:
            error = f"Erreur de lecture du capteur : {e}"
            print(error)
            self._log.write(error, "error")
            return None

    @property
    def voltage(self):
        with self._lock:
            return self.__voltage

    @property
    def current(self):
        with self._lock:
            return self.__current

    @property
    def power(self):
        with self._lock:
            return self.__power