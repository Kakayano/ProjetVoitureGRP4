import board
import busio
from adafruit_ina219 import INA219
from ProjetVoitureGRP4.sensor import Sensor
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

        self._running = False
        self._lock = threading.Lock()

    def read_data(self):
        """ 
        Lit les données du capteur de courant.
        :return: Dictionnaire contenant la tension, le courant et la puissance
        """
        with self._lock:
            self._voltage = round(self.__sensor.bus_voltage, 2)  
            self._current = round(self.__sensor.current / 1000, 3)  
            self._power = round(self.__sensor.power / 1000, 2)  

            return {
                "voltage": self._voltage,
                "current": self._current,
                "power": self._power,
            }

    def start_reading(self):
        """
        Démarre un thread pour lire les données périodiquement.
        """
        if self._running:
            print("Reading is already running.")
            return

        self._running = True

        def update_data():
            while self._running:
                data = self.read_data()
                print(f"Voltage: {data['voltage']}V, Current: {data['current']}A, Power: {data['power']}W")
                time.sleep(1)

        thread = threading.Thread(target=update_data)
        thread.daemon = True
        thread.start()

    def stop_reading(self):
        """
        Arrête la lecture des données.
        """
        self._running = False

    def get_voltage(self):
        """
        Retourne la dernière valeur de tension mesurée.
        """
        with self._lock:
            return self._voltage

    def get_current(self):
        """
        Retourne la dernière valeur de courant mesuré.
        """
        with self._lock:
            return self._current

    def get_power(self):
        """
        Retourne la dernière valeur de puissance mesurée.
        """
        with self._lock:
            return self._power