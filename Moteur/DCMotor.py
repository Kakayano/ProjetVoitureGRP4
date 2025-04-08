import RPi.GPIO as GPIO
import time
import PCA9685 as PCA


class DCMotor:
    def __init__(self):
        self.__MotorL_A = 17 # Pin GPIO pour le moteur gauche A
        self.__MotorL_B = 18 # Pin GPIO pour le moteur gauche B
        self.__MotorR_A = 27 # Pin GPIO pour le moteur droit A
        self.__MotorR_B = 22 # Pin GPIO pour le moteur droit B
        self.__EN_MG = 4 # Enable Pin GPIO pour le moteur gauche (PWM)
        self.__EN_MD = 5 # Enable Pin GPIO pour le moteur droit (PWM)
        self.__pins = [self.__MotorL_A, self.__MotorL_B, self.__MotorR_A, self.__MotorR_B] # Liste des pins GPIO
        
        '''
        On instancie un objet PWM et on lui attribue une fréquence de 60Hz
        '''
        self.__pwm = PCA.PWM() 
        self.__pwm.frequency = 60 
        '''
        On initialise les GPIO
        '''
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM) 
        '''
        On déclare chaque pin comme une sortie
        '''
        for pin in self.__pins: 
            GPIO.setup(pin, GPIO.OUT)   


    def __set_motor_state(self, motor_a, motor_b, pwm_value): # Set l'etat des moteur / pin A / pin B / PWM value
        GPIO.output(motor_a, GPIO.HIGH if pwm_value > 0 else GPIO.LOW) # Set l'etat du moteur A si la valeur du PWM est superieur à 0 on met le moteur A à HIGH sinon on le met à LOW
        GPIO.output(motor_b, GPIO.LOW if pwm_value > 0 else GPIO.HIGH) # Set l'etat du moteur B si la valeur du PWM est superieur à 0 on met le moteur B à LOW sinon on le met à HIGH
        self.__pwm.write(self.__EN_MG if motor_a == self.__MotorL_A else self.__EN_MD, 0, int(abs(pwm_value))) # Set la vitesse du moteur si le moteur A est le moteur gauche on met la vitesse du moteur gauche sinon on met la vitesse du moteur droit

    def motor_forward(self,speed = 100): # Methode pour faire avancer les moteurs
        self.__set_motor_state(self.__MotorL_A, self.__MotorL_B, self.__convert_speed(speed))
        self.__set_motor_state(self.__MotorR_A, self.__MotorR_B, self.__convert_speed(speed))

    def motor_backward(self,speed = -100): # Methode pour faire reculer les moteurs
        if ((speed)<0):
            self.__set_motor_state(self.__MotorL_A, self.__MotorL_B, self.__convert_speed(speed))
            self.__set_motor_state(self.__MotorR_A, self.__MotorR_B, self.__convert_speed(speed))
        else:
            raise ValueError("La vitesse doit etre négative !")


    def stop_motor(self): # Methode pour arreter les moteurs
        self.__set_motor_state(self.__MotorL_A, self.__MotorL_B, 0)
        self.__set_motor_state(self.__MotorR_A, self.__MotorR_B, 0) 

    def __convert_speed(self, speed):  # Methode pour convertir la vitesse de -100 à 100 en valeur PWM de 0 à 4095
        speed = max(-100, min(100, speed))
        return speed * 4095 / 100
    
    def emergency_stop(self): # Methode pour arreter les moteurs en cas d'urgence
        print("Arrêt d'urgence des moteurs !")
        self.stop_motor()