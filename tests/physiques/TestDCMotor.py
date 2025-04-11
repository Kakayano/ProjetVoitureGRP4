"""
Module de tests unitaires pour la classe DCMotor.

Ce module teste le fonctionnement du contrôleur de moteurs DC
en simulant les dépendances matérielles (GPIO et PCA9685).
"""

import unittest
from unittest.mock import patch, MagicMock, call
import DCMotor

class TestDCMotor(unittest.TestCase):
    
    def setUp(self):
        """
        Préparation des tests.
        
        Crée des simulations pour:
        - GPIO (self.mock_gpio)
        - PCA9685 (self.mock_pca)
        - PWM (self.mock_pwm)
        
        Configure les simulations et initialise une instance de DCMotor.
        """
        # Création des simulations
        self.mock_gpio = MagicMock()
        self.mock_pca = MagicMock()
        self.mock_pwm = MagicMock()
        
        # Configuration de la simulation PCA
        self.mock_pca.PWM.return_value = self.mock_pwm
        
        # Remplacement des imports par nos simulations
        self.gpio_patcher = patch('DCMotor.GPIO', self.mock_gpio)
        self.pca_patcher = patch('DCMotor.PCA', self.mock_pca)
        
        # Activation des simulations
        self.gpio_patcher.start()
        self.pca_patcher.start()
        
        # Création d'une instance de DCMotor avec dépendances simulées
        self.motor = DCMotor.DCMotor()
        
    def tearDown(self):
        """
        Nettoyage après chaque test.
        
        Désactive les simulations pour isoler les tests.
        """
        self.gpio_patcher.stop()
        self.pca_patcher.stop()
        
    def test_initialization(self):
        """Vérifie l'initialisation correcte du contrôleur."""
        # Vérification du mode GPIO
        self.mock_gpio.setmode.assert_called_with(self.mock_gpio.BCM)
        
        # Vérification de la désactivation des avertissements
        self.mock_gpio.setwarnings.assert_called_with(False)
        
        # Vérification de la configuration des broches
        pins_attendus = [17, 18, 27, 22]
        appels_attendus = [call(pin, self.mock_gpio.OUT) for pin in pins_attendus]
        self.mock_gpio.setup.assert_has_calls(appels_attendus, any_order=True)
        
        # Vérification de l'initialisation PWM
        self.mock_pca.PWM.assert_called_once()
        self.assertEqual(self.mock_pwm.frequency, 60)
        
    def test_convert_speed(self):
        """Teste la conversion vitesse % vers valeur PWM."""
        # Accès à la méthode privée
        convert_speed = self.motor._DCMotor__convert_speed
        
        # Test des valeurs normales
        self.assertEqual(convert_speed(100), 4095)
        self.assertEqual(convert_speed(50), 2047.5)
        self.assertEqual(convert_speed(0), 0)
        self.assertEqual(convert_speed(-50), -2047.5)
        
        # Test du limiteur de vitesse
        self.assertEqual(convert_speed(150), 4095)
        self.assertEqual(convert_speed(-150), -4095)
        
    def test_motor_forward(self):
        """Teste le mouvement avant à vitesse par défaut."""
        self.motor.motor_forward()
        
        # Vérification des états des moteurs
        self.mock_gpio.output.assert_any_call(17, self.mock_gpio.HIGH)  # MotorL_A HIGH
        self.mock_gpio.output.assert_any_call(18, self.mock_gpio.LOW)   # MotorL_B LOW
        self.mock_gpio.output.assert_any_call(27, self.mock_gpio.HIGH)  # MotorR_A HIGH
        self.mock_gpio.output.assert_any_call(22, self.mock_gpio.LOW)   # MotorR_B LOW
        
        # Vérification de la PWM à pleine vitesse
        self.mock_pwm.write.assert_any_call(4, 0, 4095)  # EN_MG
        self.mock_pwm.write.assert_any_call(5, 0, 4095)  # EN_MD
        
    def test_motor_forward_custom_speed(self):
        """Teste le mouvement avant avec vitesse personnalisée."""
        self.motor.motor_forward(75)
        
        # Vérification de la PWM à 75%
        pwm_attendu = int(4095 * 0.75)
        self.mock_pwm.write.assert_any_call(4, 0, pwm_attendu)
        self.mock_pwm.write.assert_any_call(5, 0, pwm_attendu)
        
    def test_motor_backward(self):
        """Teste le mouvement arrière."""
        self.motor.motor_backward(-50)
        
        # Vérification des états inversés
        self.mock_gpio.output.assert_any_call(17, self.mock_gpio.LOW)   # MotorL_A LOW
        self.mock_gpio.output.assert_any_call(18, self.mock_gpio.HIGH)  # MotorL_B HIGH
        self.mock_gpio.output.assert_any_call(27, self.mock_gpio.LOW)   # MotorR_A LOW
        self.mock_gpio.output.assert_any_call(22, self.mock_gpio.HIGH)  # MotorR_B HIGH
        
        # Vérification de la PWM à 50%
        pwm_attendu = int(4095 * 0.5)
        self.mock_pwm.write.assert_any_call(4, 0, pwm_attendu)
        self.mock_pwm.write.assert_any_call(5, 0, pwm_attendu)
        
    def test_motor_backward_positive_speed_raises_error(self):
        """Vérifie qu'une vitesse positive lève une exception."""
        with self.assertRaises(ValueError):
            self.motor.motor_backward(50)
            
    def test_stop_motor(self):
        """Teste l'arrêt des moteurs."""
        self.motor.stop_motor()
        
        # Vérification de la PWM à 0
        self.mock_pwm.write.assert_any_call(4, 0, 0)
        self.mock_pwm.write.assert_any_call(5, 0, 0)
        
    def test_emergency_stop(self):
        """Teste la fonction d'arrêt d'urgence."""
        with patch('builtins.print') as mock_print:
            self.motor.emergency_stop()
            
            # Vérification de l'arrêt
            self.mock_pwm.write.assert_any_call(4, 0, 0)
            self.mock_pwm.write.assert_any_call(5, 0, 0)
            
            # Vérification du message
            mock_print.assert_called_with("Arrêt d'urgence des moteurs !")

if __name__ == '__main__':
    unittest.main()