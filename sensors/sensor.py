from abc import ABC, abstractmethod
import threading

class Sensor(ABC, threading.Thread):
    def __init__(self, name: str, connexion_port: str):
        self._name = name
        self._connexion_port = connexion_port
        self._lock = threading.RLock()

    @abstractmethod
    def read_data(self):
       with self._lock:
            pass