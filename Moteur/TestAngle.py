import time
import PCA9685 as PCA

class ServoMotorTest:
    def __init__(self, center_pulse=350, min_pulse=250, max_pulse=450):
        self.__pwm = PCA.PWM() 
        self.__pwm.frequency = 60 
        self.__center_pulse = center_pulse
        self.__min_pulse = min_pulse    
        self.__max_pulse = max_pulse   

    def set_angle(self, angle):
        if angle < -30 :
            angle = -30  # Contrainte de l'angle à -30 degrés
        if angle > 30:
            angle = 30
        # Contrainte de l'angle entre -30 et 30 degrés
        
        angle = max(-30, min(30, angle))  # Constrain l'angle entre -30 et 30
        if angle > 0:
            pulse_width = self.__center_pulse + ((angle / 30.0) * (self.__max_pulse - self.__center_pulse))
        elif angle < 0:
            pulse_width = self.__center_pulse + ((angle / 30.0) * (self.__center_pulse - self.__min_pulse))
        else:
            pulse_width = self.__center_pulse  # Angle is 0, set to center pulse width
        
        
        self.__pwm.write(0, 0, int(pulse_width))

    def reset(self):
        print("Réinitialisation du servo moteur...")
        self.set_angle(0)  # Réinitialise l'angle à 0 degré
        self.disable()

    def disable(self):
        self.__pwm.write(0, 0, 0)

    def test_motor(self):
        print("Test du moteur servo :")
        self.set_angle(0)
        for angle in range(-30, 31, 5):  # Test de -30 à 30 degrés avec un pas de 5
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
