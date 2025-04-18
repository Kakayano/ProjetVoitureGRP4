import PCA9685 as pca

class ServoMoteur:
    def __init__(self, channel=0, centre_pulse=320, min_pulse=200, max_pulse=500): 
        self.__pwm = pca.PWM() # Instanciation de l'objet PWM
        self.__pwm.frequency = 60 # Fréquence de 60Hz pour le servo moteur
        self.__channel = channel # Canal du servo moteur
        self.__centre_pulse = centre_pulse # Largeur d'impulsion centrale
        self.__min_pulse = min_pulse # Largeur d'impulsion minimale
        self.__max_pulse = max_pulse # Largeur d'impulsion maximale

    def set_angle(self, angle): # Définit l'angle du servo moteur
        angle = max(-45, min(45, angle))  
        if angle >= 0:
            pulse_width = self.__centre_pulse + ((angle / 45.0) * (self.__max_pulse - self.__centre_pulse))
        else:
            pulse_width = self.__centre_pulse + ((angle / 45.0) * (self.__centre_pulse - self.__min_pulse))
        self.__pwm.write(self.__channel, 0, int(pulse_width))

    def reset(self): # Réinitialise le servo moteur à l'angle 0
        self.set_angle(0)

    def set_pwm(self, pulse_width): # Définit la largeur d'impulsion du servo moteur
        self.__pwm.write(self.__channel, 0, int(pulse_width))
        print(f'Pulse: {int(pulse_width)} µs on channel {self.__channel}')
