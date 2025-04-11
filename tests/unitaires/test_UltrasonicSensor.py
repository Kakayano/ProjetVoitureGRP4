import unittest
from unittest.mock import MagicMock
import sys
import types
"""
Modules :
    - gpiozero: Simulé via un mock pour le capteur ultrasonique.
    - time: Simulé pour éviter les pauses réelles lors des tests.

Testées :
    - Fonctionnement de la classe `UltrasonicSensor`.
    - Gestion des différentes valeurs de distance.
    - Retour de `None` lorsque les conditions ne sont pas remplies.
"""

# Mock du module gpiozero et de la classe DistanceSensor
mock_gpiozero = types.ModuleType("gpiozero")
mock_distance_sensor_class = MagicMock()
mock_gpiozero.DistanceSensor = mock_distance_sensor_class
sys.modules["gpiozero"] = mock_gpiozero

# Mock du module time
mock_time = types.ModuleType("time")
mock_time.sleep = MagicMock()
sys.modules["time"] = mock_time

from ultrasonic_sensor import UltrasonicSensor

class TestUltrasonicSensor(unittest.TestCase):
    """
    Attributs :
        - name : Nom du capteur
        - port : Port de connexion (non utilisé dans ce cas)
        - trigger_pin : Pin de déclenchement
        - echo_pin : Pin d'écho
        - mock_sensor_instance : Instance simulée du capteur ultrasonique
        - capteur : Instance de la classe UltrasonicSensor à tester
  Méthodes :
        - setUp() : Initialise les variables nécessaires et crée une instance de `UltrasonicSensor`.
        - test_distance_valide() : Vérifie que la distance est mesurée correctement lorsqu'elle est dans la plage acceptable.
        - test_distance_absente() : Vérifie que la distance est `None` lorsque aucun écho n'est reçu.
        - test_distance_trop_loin() : Vérifie que la distance est ignorée si elle dépasse la portée maximale.
        - test_distance_trop_proche() : Vérifie que la distance est ignorée si elle est en-dessous de la portée minimale.
    """

    def setUp(self):
        self.name = "CapteurTest"
        self.port = "/dev/test"
        self.trigger_pin = 23
        self.echo_pin = 24
        self.mock_sensor_instance = MagicMock()
        mock_distance_sensor_class.return_value = self.mock_sensor_instance
        self.capteur = UltrasonicSensor(self.name, self.port, self.trigger_pin, self.echo_pin)

    def test_valid_distance(self):
        self.mock_sensor_instance.distance = 1.234
        self.mock_sensor_instance.max_distance = 2.0
        self.capteur.read_data()
        self.assertEqual(self.capteur.distance, 123.4)

    def test_missing_distance(self):
        self.mock_sensor_instance.distance = None
        self.mock_sensor_instance.max_distance = 2.0
        self.capteur.read_data()
        self.assertIsNone(self.capteur.distance)

    def test_distance_out_of_range(self):
        self.mock_sensor_instance.distance = 3.0
        self.mock_sensor_instance.max_distance = 2.0
        self.capteur.read_data()
        self.assertIsNone(self.capteur.distance)

    def test_distance_too_close(self):
        self.mock_sensor_instance.distance = 0.01
        self.mock_sensor_instance.max_distance = 2.0
        self.capteur.read_data()
        self.assertIsNone(self.capteur.distance)

if __name__ == '__main__':
    unittest.main()
