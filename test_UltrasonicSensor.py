import unittest
from unittest.mock import patch, MagicMock
from ProjetVoitureGRP4.ultrasonic_sensor import UltrasonicSensor
import threading

class TestUltrasonicSensor(unittest.TestCase):

    @patch('ProjetVoitureGRP4.ultrasonic_sensor.DistanceSensor')
    def test_initialization_should_create_sensor_and_start_thread(self, mock_distance_sensor):
        """
        Teste que le capteur est initialisé correctement et que le thread démarre.
        """
        mock_sensor_instance = MagicMock()
        mock_distance_sensor.return_value = mock_sensor_instance

        sensor = UltrasonicSensor("CapteurTest", "PortX", trigger_pin=23, echo_pin=24)

        self.assertIsNotNone(sensor)
        mock_distance_sensor.assert_called_once_with(echo=24, trigger=23, max_distance=2.0)
        self.assertTrue(sensor._UltrasonicSensor__thread.is_alive())

    @patch('ProjetVoitureGRP4.ultrasonic_sensor.DistanceSensor')
    def test_update_distance_should_store_rounded_distance_in_cm(self, mock_distance_sensor):
        """
        Teste que la méthode update_distance lit et stocke correctement la distance en cm.
        """
        mock_sensor_instance = MagicMock()
        mock_sensor_instance.distance = 1.2345  # mètres
        mock_distance_sensor.return_value = mock_sensor_instance

        sensor = UltrasonicSensor("CapteurTest", "PortX", trigger_pin=23, echo_pin=24)

        sensor.update_distance()

        expected_distance = round(1.2345 * 100, 2)
        actual_distance = sensor.read_data()

        self.assertEqual(actual_distance, expected_distance)

    @patch('ProjetVoitureGRP4.ultrasonic_sensor.DistanceSensor')
    def test_read_data_should_return_last_measured_distance(self, mock_distance_sensor):
        """
        Teste que read_data retourne la distance correctement mise à jour.
        """
        mock_sensor_instance = MagicMock()
        mock_sensor_instance.distance = 0.5  # mètres
        mock_distance_sensor.return_value = mock_sensor_instance

        sensor = UltrasonicSensor("CapteurTest", "PortX", trigger_pin=23, echo_pin=24)

        sensor.update_distance()
        result = sensor.read_data()