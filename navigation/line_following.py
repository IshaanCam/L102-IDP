# from machine import Pin, PWM
import time as utime
from fakeStuff import FakeMotor as Motor, FakeLineSensor as LineTracker
# from motorController import Motor
import config
# from sensors.line_tracking import LineTracker
class PID:
    def __init__ (self, Kp, Ki, Kd, output_limits = (-100, 100)):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.min_out, self.max_out = output_limits
        self.I = 0.0
        self.e_prev = 0
        # self.t_prev = utime.ticks_ms()
        self.t_prev = int(utime.time() * 1000)
    
    def update(self, e):
        # t = utime.ticks_ms()
        t = int(utime.time() * 1000)
        # dt = utime.ticks_diff(t, self.t_prev) / 1000.0   # dividing by 1000 to convert to seconds
        dt = (t - self.t_prev) / 1000
        self.t_prev = t
        if dt <= 0:
            dt = 0.001  # protection from divide by 0 error
        
        self.I += e * dt
        D = (e - self.e_prev) / dt
        self.e_prev = e

        update = self.Kp * e + self.Ki * self.I + self.Kd * D

        if update < self.min_out: 
            return self.min_out
        if update > self.max_out:
            return self.max_out
        return update

# WHITE IS HIGH

def centroid_position(vals, weights):

    val_weight_sum = 0.0
    val_sum = 0.0

    for vi, wi in zip(vals, weights):
        val_weight_sum += vi * wi
        val_sum += vi
    
    if val_sum == 0:
        return None, 0
    
    return val_weight_sum / val_sum, val_sum

def line_following(
        timer
    ) -> None:
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