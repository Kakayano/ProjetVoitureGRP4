import unittest
from unittest.mock import patch, MagicMock
from test_CurrentSensor import CurrentSensor

class TestCurrentSensor(unittest.TestCase):
    @patch('test_CurrentSensor.busio.I2C')
    @patch('test_CurrentSensor.INA219')
    def setUp(self, mock_ina219, mock_i2c):
        """
        Prépare un objet CurrentSensor pour les tests.
        """
        self.mock_sensor = MagicMock()
        mock_ina219.return_value = self.mock_sensor
        self.current_sensor = CurrentSensor(name="TestSensor", connexion_port="I2C")

    def test_initialization(self):
        """
        Teste si le capteur est correctement initialisé.
        """
        self.assertEqual(self.current_sensor.get_voltage(), 0.0)
        self.assertEqual(self.current_sensor.get_current(), 0.0)
        self.assertEqual(self.current_sensor.get_power(), 0.0)

    @patch('test_CurrentSensor.time.sleep', return_value=None)
    def test_read_data(self, mock_sleep):
        """
        Teste la méthode read_data pour vérifier les valeurs lues.
        """
        self.mock_sensor.bus_voltage = 12.34
        self.mock_sensor.current = 5678  # en mA
        self.mock_sensor.power = 12345  # en mW

        time.sleep(1)  # Simule un délai pour que le thread mette à jour les valeurs
        data = self.current_sensor.read_data()

        self.assertEqual(data["voltage"], 12.34)
        self.assertEqual(data["current"], 5.678)
        self.assertEqual(data["power"], 12.35)

    def test_stop_reading(self):
        """
        Teste si la méthode stop_reading arrête correctement le thread.
        """
        self.current_sensor.stop_reading()
        self.assertFalse(self.current_sensor._running)
        self.assertFalse(self.current_sensor._CurrentSensor__thread.is_alive())

if __name__ == '__main__':
    unittest.main()