import time
import PCA9685 as PCA

class ServoMotorTest:
    def __init__(self, center_pulse=320, min_pulse=200, max_pulse=500):
        self.__pwm = PCA.PWM() 
        self.__pwm.frequency = 60 
        self.__center_pulse = center_pulse
        self.__min_pulse = min_pulse    
        self.__max_pulse = max_pulse   

    def set_angle(self, angle):
        if angle < -45 or angle > 45:
            raise ValueError("L'angle doit être compris entre -45 et 45 degrés.")
        
        angle = max(-45, min(45, angle))  # Constrain l'angle entre -45 et 45
        if angle > 0:
            pulse_width = self.__center_pulse + ((angle / 45.0) * (self.__max_pulse - self.__center_pulse))
        else:
            pulse_width = self.__center_pulse + ((angle / 45.0) * (self.__center_pulse - self.__min_pulse))
        
        self.__pwm.write(0, 0, int(pulse_width))

    def reset(self):
        self.set_angle(0)  # Réinitialise l'angle à 0 degré

    def test_motor(self):
        print("Test du moteur servo :")
        for angle in range(-45, 46, 5):  # Test de -45 à 45 degrés avec un pas de 5
            try:
                print(f"Déplacement vers {angle} degrés...")
                self.set_angle(angle)
                time.sleep(1)  # Attendre que le moteur atteigne la position
            except ValueError as e:
                print(f"Erreur : {e}")

        self.reset()  # Réinitialiser le servo à 0 degré après le test
        print("Test terminé.")

# Exemple d'utilisation
if __name__ == "__main__":
    test_servo = ServoMotorTest()
    test_servo.test_motor()
