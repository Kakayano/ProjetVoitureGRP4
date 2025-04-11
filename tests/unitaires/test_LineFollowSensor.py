import unittest
from unittest.mock import MagicMock, patch
import sys
import types

# Création du faux module RPi.GPIO
mock_gpio_module = types.ModuleType("RPi.GPIO")
mock_gpio_module.BCM = "BCM"
mock_gpio_module.IN = "IN"
mock_gpio_module.LOW = 0
mock_gpio_module.HIGH = 1
mock_gpio_module.setmode = MagicMock()
mock_gpio_module.setup = MagicMock()
mock_gpio_module.input = MagicMock()
mock_gpio_module.cleanup = MagicMock()

# Injection dans sys.modules
sys.modules["RPi"] = types.ModuleType("RPi")
sys.modules["RPi.GPIO"] = mock_gpio_module

# Patchs des autres dépendances
with patch("LineFollowSensor.Sensor") as mock_sensor, \
     patch("LineFollowSensor.time"):

    from LineFollowSensor import LineFollowSensor

    class TestLineFollowSensor(unittest.TestCase):
        """
        Tests unitaires pour la classe LineFollowSensor avec mocks complets.
        Tous les composants externes (GPIO, Sensor, time) sont simulés.
        """

        def setUp(self):
            """
            Prépare un environnement de test propre avant chaque test :
            - Mock de la classe parente Sensor
            - Réinitialisation des appels aux fonctions GPIO simulées
            """
            self.mock_sensor_instance = MagicMock()
            mock_sensor.return_value = self.mock_sensor_instance
            self.mock_sensor_instance._lock = MagicMock()
            self.mock_sensor_instance._log = MagicMock()
            self.mock_sensor_instance._running = True

            mock_gpio_module.setmode.reset_mock()
            mock_gpio_module.setup.reset_mock()
            mock_gpio_module.input.reset_mock()
            mock_gpio_module.cleanup.reset_mock()

        def test_initialisation_gpio(self):
            """
            Vérifie que la méthode __init__ configure bien le mode GPIO et le pin en entrée.
            """
            LineFollowSensor("Capteur", "PortX", 17)
            mock_gpio_module.setmode.assert_called_once_with("BCM")
            mock_gpio_module.setup.assert_called_once_with(17, "IN")

        def test_read_data_detected(self):
            """
            Vérifie que read_data retourne True si le capteur détecte la ligne (niveau bas).
            """
            mock_gpio_module.input.return_value = 0  # GPIO.LOW
            sensor = LineFollowSensor("Capteur", "PortX", 17)
            self.assertTrue(sensor.read_data())

        def test_read_data_not_detected(self):
            """
            Vérifie que read_data retourne False si aucune ligne n'est détectée (niveau haut).
            """
            mock_gpio_module.input.return_value = 1  # GPIO.HIGH
            sensor = LineFollowSensor("Capteur", "PortX", 17)
            self.assertFalse(sensor.read_data())

        def test_detect_line_messages(self):
            """
            Vérifie que detect_line retourne un message textuel cohérent selon l'état du capteur.
            """
            mock_gpio_module.input.return_value = 0
            sensor = LineFollowSensor("Capteur", "PortX", 17)
            self.assertEqual(sensor.detect_line(), "Line detected")

            mock_gpio_module.input.return_value = 1
            self.assertEqual(sensor.detect_line(), "No line detected")

        def test_stop_cleanup(self):
            """
            Vérifie que la méthode stop termine le thread proprement et nettoie le pin GPIO.
            """
            sensor = LineFollowSensor("Capteur", "PortX", 17)
            sensor.is_alive = MagicMock(return_value=True)
            sensor.join = MagicMock()

            sensor.stop()

            sensor.join.assert_called_once()
            mock_gpio_module.cleanup.assert_called_once_with(17)

    if __name__ == "__main__":
        unittest.main()
