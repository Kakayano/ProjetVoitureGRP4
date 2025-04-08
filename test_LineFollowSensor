import unittest
from unittest.mock import patch, MagicMock
from ProjetVoitureGRP4.line_follow_sensor import LineFollowSensor

class TestLineFollowSensor(unittest.TestCase):

    @patch("ProjetVoitureGRP4.line_follow_sensor.GPIO")
    def test_initialization_sets_gpio_input_mode(self, mock_gpio):
        """
        Teste que le capteur configure bien la broche GPIO en mode entrée.
        """
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setup.assert_called_once_with(17, mock_gpio.IN)

    @patch("ProjetVoitureGRP4.line_follow_sensor.GPIO")
    def test_read_data_detects_line(self, mock_gpio):
        """
        Teste read_data() quand une ligne est détectée (niveau bas).
        """
        mock_gpio.input.return_value = mock_gpio.LOW
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        result = sensor.read_data()
        self.assertTrue(result)
        mock_gpio.input.assert_called_once_with(17)

    @patch("ProjetVoitureGRP4.line_follow_sensor.GPIO")
    def test_read_data_no_line_detected(self, mock_gpio):
        """
        Teste read_data() quand aucune ligne n’est détectée (niveau haut).
        """
        mock_gpio.input.return_value = mock_gpio.HIGH
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        result = sensor.read_data()
        self.assertFalse(result)

    @patch("ProjetVoitureGRP4.line_follow_sensor.GPIO")
    def test_detect_line_message(self, mock_gpio):
        """
        Teste le message retourné par detect_line().
        """
        mock_gpio.input.return_value = mock_gpio.LOW
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        self.assertEqual(sensor.detect_line(), "Line detected")

        mock_gpio.input.return_value = mock_gpio.HIGH
        self.assertEqual(sensor.detect_line(), "No line detected")

    @patch("ProjetVoitureGRP4.line_follow_sensor.GPIO")
    def test_stop_cleans_up_gpio_pin(self, mock_gpio):
        """
        Teste que stop() appelle GPIO.cleanup avec la bonne broche.
        """
        sensor = LineFollowSensor("Suiveur", "PortX", 17)
        sensor.stop()
        mock_gpio.cleanup.assert_called_once_with(17)

if __name__ == "__main__":
    unittest.main()
