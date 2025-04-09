import unittest
from unittest.mock import patch, MagicMock
from RGB_sensor import RGBSensor

class TestRGBSensor(unittest.TestCase):
    """
    Classe de tests unitaires pour le capteur RGB TCS34725.
    Simule le matériel grâce à des mocks.
    """

    def setUp(self):
        """
        Méthode appelée avant chaque test.
        Initialise un objet RGBSensor avec mocks pour l'I2C et le capteur.
        """
        self.nom = "Capteur RGB"
        self.port = "/dev/i2c-1"

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_lecture_valeurs_rgb_valides(self, mock_i2c, mock_tcs):
        """
        Vérifie que le capteur lit correctement des valeurs RGB valides.
        """
        mock_instance = MagicMock()
        mock_instance.color_raw = (120, 200, 90, 0)
        mock_tcs.return_value = mock_instance

        capteur = RGBSensor(self.nom, self.port)
        couleurs = capteur.read_data()

        self.assertEqual(couleurs["rouge"], 120)
        self.assertEqual(couleurs["vert"], 200)
        self.assertEqual(couleurs["bleu"], 90)

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_detection_vert_vrai(self, mock_i2c, mock_tcs):
        """
        Vérifie que la détection du vert retourne True si le vert est dominant.
        """
        mock_instance = MagicMock()
        mock_instance.color_raw = (50, 150, 40, 0)
        mock_tcs.return_value = mock_instance

        capteur = RGBSensor(self.nom, self.port)
        capteur.read_data()
        self.assertTrue(capteur.is_green())

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_detection_vert_faux(self, mock_i2c, mock_tcs):
        """
        Vérifie que la détection du vert retourne False si le vert n'est pas dominant.
        """
        mock_instance = MagicMock()
        mock_instance.color_raw = (100, 110, 120, 0)
        mock_tcs.return_value = mock_instance

        capteur = RGBSensor(self.nom, self.port)
        capteur.read_data()
        self.assertFalse(capteur.is_green())

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_valeurs_nulles_ou_invalides(self, mock_i2c, mock_tcs):
        """
        Vérifie que le capteur gère correctement les valeurs nulles et lève une exception.
        """
        mock_instance = MagicMock()
        mock_instance.color_raw = (None, None, None, 0)
        mock_tcs.return_value = mock_instance

        capteur = RGBSensor(self.nom, self.port)
        with self.assertRaises(ValueError):
            capteur.read_data()

    @patch("RGB_sensor.adafruit_tcs34725.TCS34725")
    @patch("RGB_sensor.busio.I2C")
    def test_valeurs_rgb_zero(self, mock_i2c, mock_tcs):
        """
        Vérifie que le capteur signale une alerte si une ou plusieurs valeurs RGB sont à 0.
        """
        mock_instance = MagicMock()
        mock_instance.color_raw = (0, 100, 90, 0)
        mock_tcs.return_value = mock_instance

        capteur = RGBSensor(self.nom, self.port)
        with self.assertRaises(ValueError):
            capteur.read_data()

if __name__ == "__main__":
    unittest.main()
