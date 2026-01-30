from machine import Pin, PWM
import utime
from motorController import Motor
import config
from sensors.line_tracking import LineTracker

class PID:
    def __init__ (self, Kp, Ki, Kd, output_limits = (-100, 100)):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.min_out, self.max_out = output_limits
        self.I = 0.0
        self.e_prev = 0
        self.t_prev = utime.ticks_ms()
    
    def update(self, e):
        t = utime.ticks_ms()
        dt = utime.ticks_diff(t, self.t_prev) / 1000.0   # dividing by 1000 to convert to seconds
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

left_motor = config.LEFT_MOTOR 
right_motor = config.RIGHT_MOTOR
left_sensor = config.CENTER_LEFT_SENSOR
right_sensor = config.CENTER_RIGHT_SENSOR
def line_following(timer):
    if config.LINE_FOLLOWING:
        if left_sensor.read_value() != 1:
            left_motor.Forward(config.BASE_SPEED + 5)
            right_motor.Forward(config.BASE_SPEED - 5)
        elif right_sensor.read_value() != 1:
            right_motor.Forward(config.BASE_SPEED + 5)
            left_motor.Forward(config.BASE_SPEED - 5)
        utime.sleep(0.001)
        left_motor.Forward(config.BASE_SPEED)
        right_motor.Forward(config.BASE_SPEED)