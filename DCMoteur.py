import RPi.GPIO as GPIO
import time
import PCA9685 as PCA


class DCMoteur:
    def __init__(self):
        self.__MotorG_A = 17 
        self.__MotorG_B = 18 
        self.__MotorD_A = 27 
        self.__MotorD_B = 22 
        self.__EN_MG = 4 
        self.__EN_MD = 5 
        self.__pins = [self.__MotorG_A, self.__MotorG_B, self.__MotorD_A, self.__MotorD_B] 
        
        self.__pwm = PCA.PWM() 
        self.__pwm.frequency = 60 
 
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM) 
        
        for pin in self.__pins: 
            GPIO.setup(pin, GPIO.OUT)   

    def __set_etat_moteur(self, motor_a, motor_b, pwm_value): 
        GPIO.output(motor_a, GPIO.HIGH if pwm_value > 0 else GPIO.LOW) 
        GPIO.output(motor_b, GPIO.LOW if pwm_value > 0 else GPIO.HIGH) 
        self.__pwm.write(self.__EN_MG if motor_a == self.__MotorG_A else self.__EN_MD, 0, int(abs(pwm_value))) 

    def moteur_avance(self,vitesse = 100): 
        self.__set_etat_moteur(self.__MotorG_A, self.__MotorG_B, self.__convertir_vitesse(vitesse))
        self.__set_etat_moteur(self.__MotorD_A, self.__MotorD_B, self.__convertir_vitesse(vitesse))

    def moteur_recule(self,vitesse = -100):
        if ((vitesse)<0):
            self.__set_etat_moteur(self.__MotorG_A, self.__MotorG_B, self.__convertir_vitesse(vitesse))
            self.__set_etat_moteur(self.__MotorD_A, self.__MotorD_B, self.__convertir_vitesse(vitesse))
        else:
            raise ValueError("La vitesse doit etre négative !")


    def stop_moteur(self):
        self.__set_etat_moteur(self.__MotorG_A, self.__MotorG_B, 0)
        self.__set_etat_moteur(self.__MotorD_A, self.__MotorD_B, 0) 

    def __convertir_vitesse(self, vitesse): 
        vitesse = max(-100, min(100, vitesse))
        return vitesse * 4095 / 100
    
    def stop_urgence(self):
        print("Arrêt d'urgence des moteurs !")
        self.stop_moteur()
        

