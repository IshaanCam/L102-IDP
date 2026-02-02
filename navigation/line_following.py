from machine import Pin, PWM
import utime
# from fakeStuff import FakeMotor as Motor, FakeLineSensor as LineTracker
from motorController import Motor
import config
from sensors.line_tracking import LineTracker

# WHITE IS HIGH

def centroid_position(vals, weights):

    val_weight_sum = 0.0
    val_sum = 0.0

    for vi, wi in zip(vals, weights):
        val_weight_sum += (1-vi) * wi
        val_sum += (1-vi)
    
    if val_sum == 0:
        return None, 0
    
    return val_weight_sum / val_sum, val_sum

def line_following(
        timer
    ):
    """
    Function reads inputs from the light sensors and uses a weighted approach to calculate deviation from the centroid. It then uses
    a PID controller to fix the said error
    
    Args
    - timer: Place holder object for the timer instance

    Returns
    None
    """
    base_speed = config.BASE_SPEED

    if config.LF:

        sensor_vals = [sensor.read_value() for sensor in config.LINE_SENSOR]

        pos, sum = centroid_position(sensor_vals, config.WEIGHTS)

        if pos is None:
            pos = config.prev_pos
            # print("T Junction detected")


        e = -pos
        
        config.prev_pos = pos  # storing in case of T junction detected
        correction = config.pid.update(e)
        

        cmd_left = base_speed - correction
        cmd_right = base_speed + correction

        cmd_left = max(0, min(100, cmd_left))
        cmd_right = max(0, min(100, cmd_right))

        config.LEFT_MOTOR.Forward(cmd_left)
        config.RIGHT_MOTOR.Forward(cmd_right)
        
    return 
