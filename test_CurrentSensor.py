import unittest
from unittest.mock import patch, MagicMock
from CurrentSensor import CurrentSensor
import time

class TestCurrentSensor(unittest.TestCase):
    @patch('CurrentSensor.INA219')
    @patch('CurrentSensor.busio.I2C')
    def setUp(self, mock_i2c, mock_ina219):
        """
        Instancie un objet CurrentSensor avec des composants INA219 et I2C simulés.
        Initialise également des valeurs simulées pour voltage, courant et puissance.
        """
        self.mock_sensor = MagicMock()
        self.mock_sensor.bus_voltage = 12.34
        self.mock_sensor.current = 5678  # en mA
        self.mock_sensor.power = 12345  # en mW

        mock_ina219.return_value = self.mock_sensor
        self.current_sensor = CurrentSensor(name="TestSensor", connexion_port="I2C")

    def test_initialization(self):
        """
        Vérifie que les valeurs initiales du capteur sont correctement lues après démarrage.
        """
        time.sleep(1)  # Attend que le thread mette à jour les valeurs
        self.assertEqual(self.current_sensor.get_voltage(), 12.34)
        self.assertEqual(self.current_sensor.get_current(), 5.678)
        self.assertEqual(self.current_sensor.get_power(), 12.35)

    def test_read_data(self):
        """
        Vérifie que read_data() retourne les bonnes valeurs de voltage, courant et puissance.
        """
        time.sleep(1)
        data = self.current_sensor.read_data()
        self.assertEqual(data["voltage"], 12.34)
        self.assertEqual(data["current"], 5.678)
        self.assertEqual(data["power"], 12.35)

    def test_stop_reading(self):
        """
        Vérifie que le thread de mise à jour peut être arrêté correctement.
        """
        self.current_sensor.stop_reading()
        self.assertFalse(self.current_sensor._running)
        self.assertFalse(self.current_sensor._CurrentSensor__thread.is_alive())

if __name__ == '__main__':
    unittest.main()
