import unittest
from unittest.mock import patch, MagicMock
from Car import Car

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

    def test_u_turn(self):
        self.car.u_turn()
        self.assertEqual(self.mock_servo.set_angle.call_count, 3)
        self.assertEqual(self.mock_motor.motor_forward.call_count, 3)
        self.mock_motor.stop_motor.assert_called_once()
        self.mock_servo.disable.assert_called_once()


    def test_dodge_obstacle_detected(self):
        self.mock_sensor.distance = 0.3  # Distance trop proche
        with patch("builtins.print"):
            self.car.dodge_obstacle()
        self.mock_motor.motor_forward.assert_called_once_with(50)
        self.mock_motor.stop_motor.assert_called_once()

    def test_dodge_obstacle_clear(self):
        # Le capteur renvoie d'abord une distance sûre, puis une trop proche
        distances = [1.0, 0.8, 0.3]
        self.mock_sensor.distance = 1.0
        with patch("Car.time.sleep", side_effect=lambda x: None), \
             patch("builtins.print"), \
             patch.object(self.car._Car__ultrasonic_sensor_top, 'distance', new_callable=MagicMock, side_effect=distances):
            self.car.dodge_obstacle()
        self.mock_motor.stop_motor.assert_called_once()

    def test_stop_car(self):
        self.car.stop_car()
        self.mock_motor.stop_motor.assert_called_once()
        self.mock_servo.disable.assert_called_once()
        
if __name__ == "__main__":
    unittest.main()
