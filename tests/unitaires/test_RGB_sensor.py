import sys
import types
import unittest
from unittest.mock import MagicMock, patch


# MOCK des modules
# Mock du module 'board'
sys.modules['board'] = MagicMock()

# Mock de busio
mock_busio = types.ModuleType("busio")
mock_busio.I2C = MagicMock()
sys.modules['busio'] = mock_busio

# Mock d'adafruit_tcs34725 
mock_adafruit = types.ModuleType("adafruit_tcs34725")
mock_sensor_class = MagicMock()
mock_adafruit.TCS34725 = mock_sensor_class
sys.modules['adafruit_tcs34725'] = mock_adafruit

# Classe testée
from RGB_sensor import RGBSensor


class TestRGBSensor(unittest.TestCase):
    """
    Classe de tests unitaires pour le capteur RGB TCS34725.
    Simule le matériel grâce à des mocks.
    """

    def setUp(self):
        # Initialisation des variables 
        self.name = "RGB Sensor"
        self.port = "/dev/i2c-1"

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_read_valid_rgb_values(self, mock_i2c, mock_tcs):
        # Vérifie que le capteur lit correctement des valeurs RGB valides
        mock_instance = MagicMock()
        mock_instance.color_raw = (120, 200, 90, 0)
        mock_tcs.return_value = mock_instance

        sensor = RGBSensor(self.name, self.port)
        colors = sensor.read_data()

        self.assertEqual(colors["rouge"], 120)
        self.assertEqual(colors["vert"], 200)
        self.assertEqual(colors["bleu"], 90)

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_detect_green_true(self, mock_i2c, mock_tcs):
        # Vérifie que la détection du vert retourne True si le vert est dominant
        mock_instance = MagicMock()
        mock_instance.color_raw = (50, 150, 40, 0)
        mock_tcs.return_value = mock_instance

        sensor = RGBSensor(self.name, self.port)
        sensor.read_data()
        self.assertTrue(sensor.is_green())

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_detect_green_false(self, mock_i2c, mock_tcs):
        # Vérifie que la détection du vert retourne False si le vert n'est pas dominant
        mock_instance = MagicMock()
        mock_instance.color_raw = (100, 110, 120, 0)
        mock_tcs.return_value = mock_instance

        sensor = RGBSensor(self.name, self.port)
        sensor.read_data()
        self.assertFalse(sensor.is_green())

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_handle_null_rgb_values(self, mock_i2c, mock_tcs):
        # Vérifie que le capteur gère correctement les valeurs nulles et lève une exception
        mock_instance = MagicMock()
        mock_instance.color_raw = (None, None, None, 0)
        mock_tcs.return_value = mock_instance

        sensor = RGBSensor(self.name, self.port)
        with self.assertRaises(ValueError):
            sensor.read_data()

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_rgb_value_zero_alert(self, mock_i2c, mock_tcs):
        # Vérifie que le capteur signale une alerte si une ou plusieurs valeurs RGB sont à 0
        mock_instance = MagicMock()
        mock_instance.color_raw = (0, 100, 90, 0)
        mock_tcs.return_value = mock_instance

        sensor = RGBSensor(self.name, self.port)
        with self.assertRaises(ValueError):
            sensor.read_data()

if __name__ == "__main__":
    unittest.main()
