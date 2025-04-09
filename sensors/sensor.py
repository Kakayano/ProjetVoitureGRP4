from abc import ABC, abstractmethod
import threading
from log import Log

class Sensor(ABC, threading.Thread):
    def __init__(self, name: str, connexion_port: str):
        threading.Thread.__init__(self)
        self._name = name
        self._connexion_port = connexion_port
        self._lock = threading.RLock()
        self._running = True
        self._log = Log()

    @abstractmethod
    def read_data(self):
        pass
        
    def stop(self):
        self._running = False
        self.join()