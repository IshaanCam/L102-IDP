import utime
import utility.config as config
from controllers.motorController import Motor

def turn(direction: str, right_motor: Motor, left_motor: Motor, time: float=1.1) -> None:
    """
    Turns the AGV in the appropriate direction

    Args:
    - direction (str): Whether to turn right or left
    - right_motor (Motor): The right hand side motor
    - left_motor (Motor): The left hand side motor
    - time (float): The time constant for the intial turn. 
    """
    right_motor.Forward() #Let the AGV overshoot the turn to make it possible to turn around
    left_motor.Forward()
    utime.sleep(0.05)
    right_motor.Stop()
    left_motor.Stop()
    if direction == "right": #depending on the direction turn only one motor, pivoting on the other
        left_motor.Forward(config.BASE_SPEED)
        utime.sleep(time) #turn halfway, set by a hardcoded limit
        while not (config.CENTER_LEFT_SENSOR.read_value()): #keep turning until the AGV in centered on the line
            utime.sleep(0.003)
        right_motor.Forward(config.BASE_SPEED) #set both motors going forward again
    else: #same but in the other direction
        right_motor.Forward(config.BASE_SPEED)
        utime.sleep(time)
        while not config.CENTER_RIGHT_SENSOR.read_value():
            utime.sleep(0.003)
        left_motor.Forward(config.BASE_SPEED)

def turn_180(direction: str, right_motor: Motor, left_motor: Motor) -> None:
    """
    Rotates the AGV 180 degrees

    Args:
    - direction (str): Which direction to swing in
    - right_motor (Motor): The right hand side motor
    - left_motor(Motor): The left hand side motor
    """
    right_motor.Stop()
    left_motor.Stop()
    if direction == "left":
        left_motor.Forward(config.BASE_SPEED) #Turn one wheel forward and the other back
        right_motor.Reverse(config.BASE_SPEED)
        utime.sleep(1.3) #Turn part of the way through for a hard coded limit
        while not (config.CENTER_RIGHT_SENSOR.read_value()): #keep turning until the AGV centered on the line
             utime.sleep(0.003)
        config.JUNCTION_DETECTED = False
        left_motor.Stop()
        right_motor.Stop()
        utime.sleep(0.2)
        left_motor.Forward(config.BASE_SPEED) #start moving forward again
        right_motor.Forward(config.BASE_SPEED)
    else: #same but in the other direction
        right_motor.Forward(config.BASE_SPEED)
        left_motor.Reverse(config.BASE_SPEED)
        utime.sleep(1.3)
        
        while not config.CENTER_LEFT_SENSOR.read_value():
             utime.sleep(0.003)
        config.JUNCTION_DETECTED = False
        left_motor.Stop()
        right_motor.Stop()
        utime.sleep(0.2)
        left_motor.Forward(config.BASE_SPEED)
        right_motor.Forward(config.BASE_SPEED)
