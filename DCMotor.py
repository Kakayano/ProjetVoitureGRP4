import RPi.GPIO as GPIO
import time
import PCA9685 as PCA


class DCMotor:
    def __init__(self):
        self.__MotorL_A = 17 
        self.__MotorL_B = 18 
        self.__MotorR_A = 27 
        self.__MotorR_B = 22 
        self.__EN_MG = 4 
        self.__EN_MD = 5 
        self.__pins = [self.__MotorL_A, self.__MotorL_B, self.__MotorR_A, self.__MotorR_B] 
        
        self.__pwm = PCA.PWM() 
        self.__pwm.frequency = 60 
 
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM) 
        
        for pin in self.__pins: 
            GPIO.setup(pin, GPIO.OUT)   

    def __set_motor_state(self, motor_a, motor_b, pwm_value): 
        GPIO.output(motor_a, GPIO.HIGH if pwm_value > 0 else GPIO.LOW) 
        GPIO.output(motor_b, GPIO.LOW if pwm_value > 0 else GPIO.HIGH) 
        self.__pwm.write(self.__EN_MG if motor_a == self.__MotorL_A else self.__EN_MD, 0, int(abs(pwm_value))) 

    def motor_forward(self,speed = 100): 
        self.__set_motor_state(self.__MotorL_A, self.__MotorL_B, self.__convert_speed(speed))
        self.__set_motor_state(self.__MotorR_A, self.__MotorR_B, self.__convert_speed(speed))

    def motor_backward(self,speed = -100):
        if ((speed)<0):
            self.__set_motor_state(self.__MotorL_A, self.__MotorL_B, self.__convert_speed(speed))
            self.__set_motor_state(self.__MotorR_A, self.__MotorR_B, self.__convert_speed(speed))
        else:
            raise ValueError("La vitesse doit etre négative !")


    def stop_motor(self):
        self.__set_motor_state(self.__MotorL_A, self.__MotorL_B, 0)
        self.__set_motor_state(self.__MotorR_A, self.__MotorR_B, 0) 

    def __convert_speed(self, speed): 
        speed = max(-100, min(100, speed))
        return speed * 4095 / 100
    
    def emergency_stop(self):
        print("Arrêt d'urgence des moteurs !")
        self.stop_motor()
        

