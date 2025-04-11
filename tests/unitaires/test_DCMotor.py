import unittest
from unittest.mock import patch, MagicMock
import sys

# Assurez-vous que les modules RPi.GPIO et smbus sont mockés avant toute importation
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['smbus'] = MagicMock()

import DCMotor

class TestDCMotor(unittest.TestCase):
    """
    Une suite de tests pour la classe DCMotor. Cette suite teste la fonctionnalité
    de la classe DCMotor en mockant les modules spécifiques au matériel tels que RPi.GPIO
    et smbus pour s'assurer que la logique de contrôle du moteur fonctionne comme prévu.
    """

    def setUp(self):
        """
        Configure l'environnement de test en remplaçant les modules RPi.GPIO et PCA9685
        par des objets mock. Cette méthode est appelée avant l'exécution de chaque méthode de test.
        """
        # Remplace le module RPi.GPIO
        self.gpio_patcher = patch('DCMotor.GPIO', new=MagicMock())
        self.mock_gpio = self.gpio_patcher.start()

        # Remplace le module PCA9685
        self.pca_patcher = patch('DCMotor.PCA', new=MagicMock())
        self.mock_pca = self.pca_patcher.start()

        # Mock l'objet PWM
        self.mock_pwm = MagicMock()
        self.mock_pca.PWM.return_value = self.mock_pwm

        # Configure éventuellement les objets mock
        self.mock_gpio.setwarnings = MagicMock()
        self.mock_gpio.setmode = MagicMock()
        self.mock_gpio.setup = MagicMock()
        self.mock_gpio.output = MagicMock()

        # Ajoute des méthodes de nettoyage pour arrêter les patchers
        self.addCleanup(self.gpio_patcher.stop)
        self.addCleanup(self.pca_patcher.stop)

        # Initialise l'instance DCMotor
        self.motor = DCMotor.DCMotor()

    def test_convert_speed(self):
        """
        Teste la méthode de conversion de vitesse pour s'assurer qu'elle convertit correctement
        les valeurs de vitesse en pourcentage en valeurs PWM.
        """
        self.assertEqual(self.motor._DCMotor__convert_speed(50), 2047.5)
        self.assertEqual(self.motor._DCMotor__convert_speed(-30), -1228.5)

    def test_emergency_stop(self):
        """
        Teste la méthode d'arrêt d'urgence pour s'assurer qu'elle arrête le moteur
        et affiche un message d'arrêt d'urgence.
        """
        self.motor.emergency_stop()
        self.mock_gpio.output.assert_called()
        self.mock_pwm.write.assert_called()

    def test_initialization(self):
        """
        Teste l'initialisation de la classe DCMotor pour s'assurer que les broches GPIO
        sont configurées correctement.
        """
        self.mock_gpio.setmode.assert_called_with(self.mock_gpio.BCM)
        self.mock_gpio.setup.assert_called()

    def test_motor_backward(self):
        """
        Teste le mouvement arrière du moteur pour s'assurer qu'il se déplace en arrière
        avec la vitesse correcte.
        """
        self.motor.motor_backward(-50)
        self.mock_gpio.output.assert_called()
        self.mock_pwm.write.assert_called()

    def test_motor_backward_positive_speed_raises_error(self):
        """
        Teste que la fourniture d'une valeur de vitesse positive à la méthode motor_backward
        lève une ValueError.
        """
        with self.assertRaises(ValueError):
            self.motor.motor_backward(50)

    def test_motor_forward(self):
        """
        Teste le mouvement avant du moteur pour s'assurer qu'il se déplace en avant
        avec la vitesse correcte.
        """
        self.motor.motor_forward(75)
        self.mock_gpio.output.assert_called()
        self.mock_pwm.write.assert_called()

    def test_motor_forward_custom_speed(self):
        """
        Teste le mouvement avant du moteur avec une vitesse personnalisée pour s'assurer
        qu'il se déplace en avant avec la vitesse spécifiée.
        """
        self.motor.motor_forward(30)
        self.mock_gpio.output.assert_called()
        self.mock_pwm.write.assert_called()

    def test_stop_motor(self):
        """
        Teste la méthode d'arrêt du moteur pour s'assurer qu'elle arrête correctement le moteur.
        """
        self.motor.stop_motor()
        self.mock_gpio.output.assert_called()
        self.mock_pwm.write.assert_called()

if __name__ == '__main__':
    unittest.main()
