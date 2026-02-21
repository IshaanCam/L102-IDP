from machine import PWM, Pin
class Servo:
    def __init__(self, PWMPin):
        self.pwm = PWM(Pin(PWMPin))  # set servo pwm pin
        self.pwm.freq(100)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def Turn(self, angle=270):
        u16_level = 2621 + ((angle * (16383 - 2621))/270) # At 0°, u16 level ~ 2621 and at 270° u16 level ~ 16383. 
                                                          # Equation distributes whole range between the two ends                  
        self.pwm.duty_u16(int(u16_level))  # angle range 0° - 270°
