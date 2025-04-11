import unittest
from unittest.mock import patch, MagicMock
import sys
import types

# Mock de PCA9685
mock_pca = types.ModuleType("PCA9685")
mock_pwm_class = MagicMock()
mock_pca.PWM = mock_pwm_class
sys.modules["PCA9685"] = mock_pca

from ServoMoteur import ServoMoteur

class TestServoMoteur(unittest.TestCase):

    """
    Tests unitaires pour la classe ServoMoteur.

    Ces tests vérifient que le servo moteur ne dépasse pas certains angles pour éviter que les roues ne tapent dans le module.
    On vérifie le comportement de la classe ServoMoteur, en vérifiant que
    les signaux PWM sont correctement calculés et envoyés en fonction des angles ou
    des valeurs d'impulsion en entrée. 
    La classe ServoMoteur contrôle un servo moteur grâce à un signal PWM.
    On utilise des mocks pour simuler le comportement de la classe PWM.

    Mocks :
        Utiliser pour mocker la classe PWM
        Utiliser pour mocker le module smbus
    """

    @patch("ServoMoteur.pca.PWM")
    def setUp(self, mock_pwm_class):
        # Créer une instance mockée de PWM
        self.mock_pwm = MagicMock()
        mock_pwm_class.return_value = self.mock_pwm

        # On crée le mock de la classe ServoMoteur
        self.servo = ServoMoteur(channel=1, centre_pulse=300, min_pulse=200, max_pulse=500)

    def test_set_angle_zero(self):
        '''
        Vérifie que définir l'angle à 0 entraîne l'utilisation de l'impulsion centrale.
        '''
        self.servo.set_angle(0)
        expected_pulse = 300 # Impulsion centrale
        self.mock_pwm.write.assert_called_with(1, 0, expected_pulse)

    def test_set_angle_positive(self):
        '''
        Vérifie qu'un angle positif (ici, 45) utilise l'impulsion maximale.
        '''
        self.servo.set_angle(45)
        expected_pulse = 500  # Impuslion maximale
        self.mock_pwm.write.assert_called_with(1, 0, expected_pulse)

    def test_set_angle_negative(self):
        '''
        Vérifie qu'un angle négatif (ici, -45) utilise de l'impulsion minimale.
        '''
        self.servo.set_angle(-45)
        expected_pulse = 200  # Impulsion minimum
        self.mock_pwm.write.assert_called_with(1, 0, expected_pulse)

    def test_angle_clamped_above_max(self):
        '''
        test_angle_clamped_above_max : Vérifie que les angles supérieurs au maximum (Ici, 90) sont limités à la valeur maximale (45).
        '''
        self.servo.set_angle(90)  # Devrait rester sur 45
        expected_pulse = 500
        self.mock_pwm.write.assert_called_with(1, 0, expected_pulse)

    def test_angle_clamped_below_min(self):
        '''
        Vérifie que les angles inférieurs au minimum (Ici, -90) sont limités à la valeur minimale(-45).
        '''
        self.servo.set_angle(-90)  # Devrait rester sur -45
        expected_pulse = 200
        self.mock_pwm.write.assert_called_with(1, 0, expected_pulse)

    def test_reset(self):
        '''
        Test la méthode reset() qui doit ramener le servo à 0 degré.
        '''
        self.servo.reset() # Réinitialise le servo à 0 degré
        self.mock_pwm.write.assert_called_with(1, 0, 300)

    def test_set_pwm(self):
        '''
        Vérifie qu'une valeur d'impulsion PWM spécifique peut être définie directement.
        '''
        self.servo.set_pwm(250) # Définit la largeur d'impulsion à 250
        self.mock_pwm.write.assert_called_with(1, 0, 250)

if __name__ == '__main__':
    unittest.main()
