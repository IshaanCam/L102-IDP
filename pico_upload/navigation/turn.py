import utime
import utility.config as config
from controllers.motorController import Motor

def turn(direction: str, right_motor: Motor, left_motor: Motor) -> None:
    left_motor.Forward()
    right_motor.Forward()
    utime.sleep(0.25)
    right_motor.Stop()
    left_motor.Stop()
    if direction == "right":
        left_motor.Forward(config.BASE_SPEED)
        utime.sleep(0.8)
        while not (config.CENTER_RIGHT_SENSOR.read_value()):
            utime.sleep(0.003)
        right_motor.Forward(config.BASE_SPEED)
    else:
        right_motor.Forward(config.BASE_SPEED)
        utime.sleep(0.8)
        while not config.CENTER_RIGHT_SENSOR.read_value():
            utime.sleep(0.003)
        left_motor.Forward(config.BASE_SPEED)

def turn_180(direction: str, right_motor: Motor, left_motor: Motor) -> None:
    right_motor.Stop()
    left_motor.Stop()
    if direction == "left":
        left_motor.Forward(config.BASE_SPEED)
        right_motor.Reverse(config.BASE_SPEED)
        utime.sleep(1.2)
        right_motor.Forward(config.BASE_SPEED)
        
        # while not (config.CENTER_RIGHT_SENSOR.read_value()):
        #     utime.sleep(0.003)
    else:
        right_motor.Forward(config.BASE_SPEED)
        left_motor.Reverse(config.BASE_SPEED)
        utime.sleep(1.2)
        left_motor.Forward(config.BASE_SPEED)
        # while not config.CENTER_LEFT_SENSOR.read_value():
        #     utime.sleep(0.003)

