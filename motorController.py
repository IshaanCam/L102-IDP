from machine import Pin, PWM
from utime import sleep
import uasyncio as asyncio

class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def Stop(self):
        self.pwm.duty_u16(0)
        
    def Forward(self, speed=100):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def Reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))

def test_motor3():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5

    while True:
        print("Forward")
        motor3.Forward()
        sleep(1)
        print("Reverse")
        motor3.Reverse()
        sleep(1)

async def turn(left_motor: Motor, right_motor: Motor, turn_complete: bool, direction: str) -> None:
    """
    Control the motors to enable the vehicle to make a turn
    
    Args
    - left_motor (Motor): The left hand side motor
    - right_motor (Motor): The right hand side motor
    - turn_complete (bool): Global variable carrying the state of the turn
    - direction (str): The direction of the turn

    Returns
    - None
    """

    sleep(1)
    left_motor.Stop()
    right_motor.Stop()

    motor = right_motor

    if direction == 'right':
        motor = left_motor 

    motor.Forward(100)

    while not turn_complete:
        await asyncio.sleep(0.01)
    
    motor.Stop()

    return None

