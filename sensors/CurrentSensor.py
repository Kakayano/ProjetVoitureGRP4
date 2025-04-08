import board
import busio
from adafruit_ina219 import INA219
from sensor import Sensor
import threading
import time

class CurrentSensor(Sensor):
    def __init__(self, name: str, connexion_port: str):
        """
        Initialise le capteur de courant avec un nom et un port de connexion.
        """
        super().__init__(name, connexion_port)
        
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = INA219(self.__i2c)

        self._voltage = 0.0
        self._current = 0.0
        self._power = 0.0

        self._running = True  

        self.__thread = threading.Thread(target=self.__update_loop)
        self.__thread.daemon = True
        self.__thread.start()

    def __update_loop(self):
        """
        Méthode interne qui lit les données en continu dans un thread.
        """
        while self._running:
            with self._lock:
                self._voltage = round(self.__sensor.bus_voltage, 2)
                self._current = round(self.__sensor.current / 1000, 3)
                self._power = round(self.__sensor.power / 1000, 2)
            time.sleep(1)

    def read_data(self):
        """ 
        Retourne les dernières données lues.
        """
        with self._lock:
            return {
                "voltage": self._voltage,
                "current": self._current,
                "power": self._power,
            }

    def stop_reading(self):
        """
        Arrête la boucle de lecture.
        """
        self._running = False
        if self.__thread.is_alive():
            self.__thread.join()

    def get_voltage(self):
        with self._lock:
            return self._voltage

    def get_current(self):
        with self._lock:
            return self._current

    def get_power(self):
        with self._lock:
            return self._power
