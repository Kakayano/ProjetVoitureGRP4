import unittest
from unittest.mock import patch, MagicMock
from Car import Car

from Moteur.DCMotor import DCMotor
from Moteur.ServoMoteur import ServoMoteur
from Capteur.ultrasonic_sensor import UltrasonicSensor
import PCA9685 as PCA

import threading
import time
import RPi.GPIO as GPIO

class TestCar(unittest.TestCase):
    @patch("Car.DCMotor")
    @patch("Car.ServoMoteur")
    @patch("Car.UltrasonicSensor")
    def setUp(self, MockUltrasonicSensor, MockServoMoteur, MockDCMotor):
        # On mock les composants internes de la voiture
        self.mock_motor = MockDCMotor.return_value
        self.mock_servo = MockServoMoteur.return_value
        self.mock_sensor = MockUltrasonicSensor.return_value
        self.car = Car()

    def test_run_straight(self):
        self.car.run_straigth(speed=60, duration=2)
        self.mock_servo.disable.assert_called_once()
        self.assertEqual(self.mock_motor.motor_forward.call_count, 1)
        self.assertEqual(self.mock_motor.motor_backward.call_count, 1)
        self.mock_motor.stop_motor.assert_called_once()
        print("Test_run_straight réussi, roule droit")

    def test_u_turn(self):
        self.car.u_turn()
        self.assertEqual(self.mock_servo.set_angle.call_count, 3)
        self.assertEqual(self.mock_motor.motor_forward.call_count, 3)
        self.mock_motor.stop_motor.assert_called_once()
        self.mock_servo.disable.assert_called_once()
        print("Test_u_turn réussi, demitour effectué")


    def test_stop_car(self):
        self.car.stop_car()
        self.mock_motor.stop_motor.assert_called_once()
        self.mock_servo.disable.assert_called_once()
        print("Test_stop_car réussi, voiture arrêtée")

        
if __name__ == "__main__":
    unittest.main()
