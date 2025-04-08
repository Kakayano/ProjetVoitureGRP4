import unittest
from unittest.mock import patch, MagicMock
from ProjetVoitureGRP4.rgb_sensor import RGBSensor

class TestRGBSensor(unittest.TestCase):

    @patch("ProjetVoitureGRP4.rgb_sensor.adafruit_tcs34725.TCS34725")
    @patch("ProjetVoitureGRP4.rgb_sensor.busio.I2C")
    def test_initialization_starts_thread(self, mock_i2c, mock_tcs):
        """
        Teste que le capteur est bien initialisé et que le thread démarre.
        """
        mock_sensor = MagicMock()
        mock_sensor.color_raw = (0, 0, 0, 0)
        mock_tcs.return_value = mock_sensor

        sensor = RGBSensor("CapteurRGB", "PortI2C")

        self.assertTrue(sensor._RGBSensor__thread.is_alive())
        self.assertEqual(sensor.sensor, mock_sensor)

    @patch("ProjetVoitureGRP4.rgb_sensor.adafruit_tcs34725.TCS34725")
    @patch("ProjetVoitureGRP4.rgb_sensor.busio.I2C")
    def test_read_data_returns_correct_rgb_values(self, mock_i2c, mock_tcs):
        """
        Teste que read_data retourne bien les valeurs RGB lues du capteur.
        """
        mock_sensor = MagicMock()
        mock_sensor.color_raw = (100, 200, 50, 0)  # R, G, B, Clear
        mock_tcs.return_value = mock_sensor

        sensor = RGBSensor("CapteurRGB", "PortI2C")

        result = sensor.read_data()
        expected = {"rouge": 100, "vert": 200, "bleu": 50}

        self.assertEqual(result, expected)

    @patch("ProjetVoitureGRP4.rgb_sensor.adafruit_tcs34725.TCS34725")
    @patch("ProjetVoitureGRP4.rgb_sensor.busio.I2C")
    def test_is_green_detects_green_correctly(self, mock_i2c, mock_tcs):
        """
        Teste si is_green détecte correctement une couleur verte.
        """
        mock_sensor = MagicMock()
        mock_sensor.color_raw = (50, 200, 30, 0)
        mock_tcs.return_value = mock_sensor

        sensor = RGBSensor("CapteurRGB", "PortI2C")

        self.assertTrue(sensor.is_green(threshold=1.5, min_green=100))

    @patch("ProjetVoitureGRP4.rgb_sensor.adafruit_tcs34725.TCS34725")
    @patch("ProjetVoitureGRP4.rgb_sensor.busio.I2C")
    def test_is_green_returns_false_for_non_green_color(self, mock_i2c, mock_tcs):
        """
        Teste si is_green retourne False quand la couleur n’est pas assez verte.
        """
        mock_sensor = MagicMock()
        mock_sensor.color_raw = (100, 120, 100, 0)  # Vert trop faible
        mock_tcs.return_value = mock_sensor

        sensor = RGBSensor("CapteurRGB", "PortI2C")

        self.assertFalse(sensor.is_green(threshold=1.5, min_green=150))

    @patch("ProjetVoitureGRP4.rgb_sensor.adafruit_tcs34725.TCS34725")
    @patch("ProjetVoitureGRP4.rgb_sensor.busio.I2C")
    def test_stop_joins_thread_and_closes_sensor(self, mock_i2c, mock_tcs):
        """
        Teste que stop ferme correctement le capteur et arrête le thread.
        """
        mock_sensor = MagicMock()
        mock_sensor.color_raw = (0, 0, 0, 0)
        mock_tcs.return_value = mock_sensor

        sensor = RGBSensor("CapteurRGB", "PortI2C")
        sensor._RGBSensor__thread = MagicMock()
        sensor._RGBSensor__thread.join = MagicMock()

        sensor.stop()

        sensor._RGBSensor__thread.join.assert_called_once()
        mock_sensor.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
