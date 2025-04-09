import unittest
from unittest.mock import patch, MagicMock
from LineFollowSensor import LineFollowSensor
import time

class TestLineFollowSensor(unittest.TestCase):
    """
    Classe de tests unitaires pour la classe LineFollowSensor.
    Ces tests vérifient l'initialisation GPIO, la lecture de la ligne, les messages retournés
    et l'arrêt du capteur avec nettoyage du port GPIO.
    """

    @patch("LineFollowSensor.GPIO")
    def test_initialization_sets_gpio_input_mode(self, mock_gpio):
        """
        Vérifie que le capteur configure correctement la broche GPIO en mode entrée.
        """
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setup.assert_called_once_with(17, mock_gpio.IN)

    @patch("LineFollowSensor.GPIO")
    def test_read_data_detects_line(self, mock_gpio):
        """
        Vérifie que le capteur détecte bien une ligne (niveau bas sur le GPIO).
        """
        mock_gpio.input.return_value = mock_gpio.LOW
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        result = sensor.read_data()
        self.assertTrue(result)

    @patch("LineFollowSensor.GPIO")
    def test_read_data_no_line_detected(self, mock_gpio):
        """
        Vérifie que le capteur détecte l'absence de ligne (niveau haut sur le GPIO).
        """
        mock_gpio.input.return_value = mock_gpio.HIGH
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        result = sensor.read_data()
        self.assertFalse(result)

    @patch("LineFollowSensor.GPIO")
    def test_detect_line_message(self, mock_gpio):
        """
        Vérifie que la méthode detect_line() retourne le bon message
        selon la présence ou non de la ligne.
        """
        mock_gpio.input.return_value = mock_gpio.LOW
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        self.assertEqual(sensor.detect_line(), "Line detected")

        mock_gpio.input.return_value = mock_gpio.HIGH
        self.assertEqual(sensor.detect_line(), "No line detected")

    @patch("LineFollowSensor.GPIO")
    def test_stop_cleans_up_gpio_pin(self, mock_gpio):
        """
        Vérifie que l'appel à stop() arrête correctement le thread
        et libère la broche GPIO utilisée.
        """
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        sensor.start()
        time.sleep(0.1)
        sensor.stop()
        mock_gpio.cleanup.assert_called_once_with(17)

if __name__ == "__main__":
    unittest.main()
