import PCA9685 as pca
from log import Log

class ServoMoteur:
    def __init__(self, channel=0, center_pulse=350, min_pulse=250, max_pulse=450): 
        '''
        Initialise le servo moteur avec le canal, la largeur d'impulsion centrale, minimale et maximale.
        :param channel: Canal du servo moteur (0 par défaut)
        '''
        self.__pwm = pca.PWM() # Instanciation de l'objet PWM
        self.__pwm.frequency = 60 # Fréquence de 60Hz pour le servo moteur
        self.__channel = channel # Canal du servo moteur
        self.__center_pulse = center_pulse # Largeur d'impulsion centrale
        self.__min_pulse = min_pulse # Largeur d'impulsion minimale
        self.__max_pulse = max_pulse # Largeur d'impulsion maximale
        self.__log = Log()

    def set_angle(self, angle): # Définit l'angle du servo moteur
        '''
        Définit l'angle du servo moteur en fonction de la largeur d'impulsion.
        elle prend en paramètre l'angle
        '''
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

    def reset(self): # Réinitialise le servo moteur à l'angle 0
        '''
        Réinitialise le servo moteur à la position 0 degré.
        '''
        print("Réinitialisation du servo moteur...")
        self.__log.write("Réinitialisation du servo moteur...", "debug")
        self.set_angle(0)  # Réinitialise l'angle à 0 degré
        self.disable()

    def disable(self):
        self.__pwm.write(0, 0, 0)
        self.__log.write("Servo moteur désactivé.", "debug")

    def set_pwm(self, pulse_width): # Définit la largeur d'impulsion du servo moteur
        '''
        Définit la largeur d'impulsion du servo moteur.
        elle prend en paramètre la largeur d'impulsion
        '''
        self.__pwm.write(self.__channel, 0, int(pulse_width))
        print(f'Pulse: {int(pulse_width)} µs on channel {self.__channel}')
        self.__log.write(f'Pulse: {int(pulse_width)} µs on channel {self.__channel}', "debug")
