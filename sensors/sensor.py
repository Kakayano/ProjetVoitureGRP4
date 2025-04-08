from abc import ABC, abstractmethod
import threading
from log import Log

class Sensor(ABC):
    def __init__(self, name: str, connexion_port: str, log_file):
        self._name = name
        self._connexion_port = connexion_port
        self._lock = threading.RLock()
        self._log = Log(log_file)
        self._log.write(f"Sensor {self._name} initialized on {self._connexion_port}\n")

    @abstractmethod
    def read_data(self):
       with self._lock:
            pass

    @abstractmethod
    def stop(self):
        pass