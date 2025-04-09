import unittest
from unittest.mock import patch, MagicMock
from CurrentSensor import CurrentSensor
import time

class TestCurrentSensor(unittest.TestCase):
    """
    Classe de tests unitaires pour la classe CurrentSensor.
    Simule le capteur INA219 et valide les lectures de données et le comportement du thread.
    """

    @patch('CurrentSensor.INA219')
    @patch('CurrentSensor.busio.I2C')
    def setUp(self, mock_i2c, mock_ina219):
        """
        Prépare un capteur simulé avec des valeurs prédéfinies pour chaque test.
        """
        self.mock_sensor = MagicMock()
        self.mock_sensor.bus_voltage = 12.34
        self.mock_sensor.current = 5678  
        self.mock_sensor.power = 12345  

        mock_ina219.return_value = self.mock_sensor
        self.current_sensor = CurrentSensor(name="TestSensor", connexion_port="I2C")

        self.current_sensor._CurrentSensor__update_loop()

    def test_initialization(self):
        """
        Vérifie que les valeurs internes du capteur sont initialisées correctement.
        """
        self.assertEqual(self.current_sensor.voltage, 12.34)
        self.assertEqual(self.current_sensor.current, 5.678)
        self.assertEqual(self.current_sensor.power, 12.35)

    def test_read_data(self):
        """
        Vérifie que read_data() retourne un dictionnaire avec les bonnes valeurs.
        """
        data = self.current_sensor.read_data()
        self.assertEqual(data["voltage"], 12.34)
        self.assertEqual(data["current"], 5.678)
        self.assertEqual(data["power"], 12.35)

    def test_stop(self):
        """
        Vérifie que le thread peut être démarré puis arrêté correctement.
        """
        self.current_sensor.start()  
        time.sleep(0.1)             
        self.current_sensor.stop()
        self.assertFalse(self.current_sensor._running)

if __name__ == '__main__':
    unittest.main()
