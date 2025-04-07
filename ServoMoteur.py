import PCA9685 as pca

class ServoMoteur:
    def __init__(self, channel=0, centre_pulse=320, min_pulse=200, max_pulse=500): 
        self.__pwm = pca.PWM()
        self.__pwm.frequency = 60
        self.__channel = channel
        self.__centre_pulse = centre_pulse
        self.__min_pulse = min_pulse    
        self.__max_pulse = max_pulse   

    def set_angle(self, angle):
        angle = max(-45, min(45, angle))  
        if angle >= 0:
            pulse_width = self.__centre_pulse + ((angle / 45.0) * (self.__max_pulse - self.__centre_pulse))
        else:
            pulse_width = self.__centre_pulse + ((angle / 45.0) * (self.__centre_pulse - self.__min_pulse))
        self.__pwm.write(self.__channel, 0, int(pulse_width))

    def reset(self):
        self.set_angle(0)

    def set_pwm(self, pulse_width):
        self.__pwm.write(self.__channel, 0, int(pulse_width))
        print(f'Pulse: {int(pulse_width)} µs on channel {self.__channel}')
