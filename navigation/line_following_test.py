from machine import Pin, PWM, Timer
import utime
import config

to_and_fro = {("start", "start"): ["start", "j1", "bay_3_entrance", "bay_4_entrance", "entrance_lower_b","exit_lower_b", "back_right_corner", "ramp", "back_left_corner", "exit_lower_a", "entrance_lower_a", "bay_1_entrance", "bay_2_entrance", "start"]}
path = {
    "start": {
        ("start", "bay_3"): "forward",
        ("lower_b", "start"): "forward",
        ("lower_a", "start"): "forward",
        ("upper_b", "start"): "forward",
        ("upper_a", "start"): "forward",
    },
    "j1": {
        ("bay_3", "lower_a"): "forward", 
        ("bay_4", "lower_a"): "forward", 
        ("lower_b", "bay_1"): "forward", 
        ("lower_b", "bay_2"): "forward",
        ("start", "bay_3"): "right", 
        ("lower_a", "bay_4"): "forward", 
        ("bay_2", "lower_b"): "forward",
        ("bay_1", "lower_b"): "forward",
        ("lower_a", "start"): "right",
        ("upper_a", "start"): "right",
        ("lower_b", "start"): "left",
        ("upper_b", "start"): "left",
        ("start", "start"): "right"
    },
    "bay_3_entrance": {
        ("bay_3", "lower_a"): "left", 
        ("bay_4", "lower_a"): "forward", 
        ("bay_3", "lower_b"): "right",
        ("bay_3", "upper_b"): "right",
        ("bay_3", "upper_a"): "right",
        ("lower_b", "bay_1"): "forward", 
        ("lower_b", "bay_2"): "forward",
        ("start", "bay_3"): "right", 
        ("lower_a", "bay_4"): "forward", 
        ("bay_2", "lower_b"): "forward",
        ("bay_1", "lower_b"): "forward",
        ("lower_b", "start"): "forward",
        ("upper_b", "start"): "forward",
        ("start", "start"): "forward"
    },
    "bay_4_entrance": {
        ("bay_4", "lower_a"): "left", 
        ("bay_3", "lower_b"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_3", "upper_a"): "left",
        ("lower_b", "bay_1"): "right", 
        ("lower_b", "bay_2"): "right",
        ("lower_b", "bay_4"): "forward",
        ("upper_b", "bay_4"): "forward",
        ("lower_a", "bay_4"): "right", 
        ("upper_a", "bay_4"): "forward",
        ("bay_2", "lower_b"): "left",
        ("bay_1", "lower_b"): "left",
        ("lower_b", "start"): "right",
        ("upper_b", "start"): "right",
        ("bay_4", "lower_b"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("start", "start"): "left"
    },
    "back_right_corner": {
        ("bay_3", "upper_a"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_a"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_a", "bay_4"): "right",
        ("upper_b", "bay_4"): "right",
        ("start", "start"): "left"
    },
    "ramp": {
        ("bay_3", "upper_a"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_a"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_a", "bay_4"): "right",
        ("upper_b", "bay_4"): "right",
        ("upper_a", "bay_1"): "left",
        ("upper_b", "bay_1"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_b", "bay_2"): "left",
        ("bay_1", "upper_a"): "right",
        ("bay_1", "upper_b"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_2", "upper_b"): "right",
        ("start", "start"): "forward"
    },
    "back_left_corner": {
        ("upper_a", "bay_1"): "left",
        ("upper_b", "bay_1"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_b", "bay_2"): "left",
        ("bay_1", "upper_a"): "right",
        ("bay_1", "upper_b"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_2", "upper_b"): "right",
        ("start", "start"): "left"
    },
    "entrance_lower_b": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "exit_lower_b": {
        ("upper_a", "bay_4"): "forward",
        ("upper_b", "bay_4"): "forward",
        ("start", "start"): "forward"
    },
    "top_of_ramp": {
        ("bay_1", "upper_a"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_3", "upper_a"): "right",
        ("bay_4", "upper_a"): "right",
        ("bay_1", "upper_b"): "left",
        ("bay_2", "upper_b"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_b", "bay_4"): "right",
        ("upper_b", "bay_2"): "right",
        ("upper_b", "bay_1"): "right",
        ("upper_a", "bay_4"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_a", "bay_1"): "left"
    },
    "corner_before_upper_b": {
        ("bay_1", "upper_b"): "left",
        ("bay_2", "upper_b"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_b", "bay_4"): "right",
        ("upper_b", "bay_2"): "right",
        ("upper_b", "bay_1"): "right"
    },
    "corner_before_upper_a": {
        ("bay_1", "upper_a"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_3", "upper_a"): "right",
        ("bay_4", "upper_a"): "right",
        ("upper_a", "bay_4"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_a", "bay_1"): "left"
    },
    "entrance_lower_a": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "exit_lower_a": {
        ("upper_a", "bay_1"): "forward",
        ("upper_b", "bay_1"): "forward",
        ("upper_a", "bay_2"): "forward",
        ("upper_b", "bay_2"): "forward",
        ("start", "start"): "forward"
    },
    "bay_1_entrance": {
        ("bay_1", "lower_a"): "forward",
        ("bay_2", "lower_a"): "right", 
        ("bay_3", "lower_a"): "right",
        ("bay_4", "lower_a"): "right", 
        ("bay_1", "upper_a"): "forward",
        ("bay_2", "upper_a"): "right",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_b"): "right",
        ("lower_a", "bay_4"): "left",
        ("lower_a", "bay_2"): "left",
        ("lower_a", "bay_1"): "forward",
        ("upper_a", "bay_2"): "left",
        ("upper_a", "bay_1"): "forward",
        ("upper_a", "start"): "left",
        ("lower_a", "start"): "left",
        ("upper_b", "bay_1"): "forward",
        ("upper_b", "bay_2"): "left",
        ("start", "start"): "left"
    },
    "bay_2_entrance": {
        ("bay_2", "lower_a"): "left",
        ("bay_2", "upper_a"): "left",
        ("bay_2", "upper_b"): "left",
        ("bay_2", "lower_b"): "right",
        ("bay_1", "lower_b"): "forward",
        ("bay_3", "lower_a"): "forward",
        ("bay_4", "lower_a"): "forward",
        ("lower_a", "start"): "forward",
        ("upper_a", "start"): "forward",
        ("lower_a", "bay_4"): "forward",
        ("lower_a", "bay_2"): "right",
        ("upper_a", "bay_2"): "right",
        ("upper_b", "bay_2"): "right",
        ("lower_b", "bay_2"): "left",
        ("lower_b", "bay_1"): "forward",
        ("start", "start"): "forward"
    }
}


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
        
left_motor = Motor(dirPin = 4, PWMPin = 5)    
right_motor = Motor(dirPin = 7, PWMPin = 6)

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
    
prev_pos = 0
pid = PID(Kp=60, Ki=-1, Kd=5, output_limits=(-50,50))

WEIGHTS = [-2, -1, 1, 2] #  These will be used for finding our centroid (negative for left, positive for right)

# ASSUMING WHITE IS HIGH

digital_pins = [10, 11, 12, 13]  #GPIO pin numbers
digital = [Pin(i, Pin.IN) for i in digital_pins]

def read_sensors(digital):
    vals = []
    for pin in digital:
        vals.append(float(pin.value()))
    return vals

def centroid_position(vals, weights):

    val_weight_sum = 0.0
    val_sum = 0.0

    for vi, wi in zip(vals, weights):
        val_weight_sum += (1-vi) * wi
        val_sum += (1-vi)
    
    if val_sum == 0:
        return None, 0
    
    return val_weight_sum / val_sum, val_sum

def turn(direction: str, right_motor, left_motor) -> None:
    right_motor.Stop()
    left_motor.Stop()
    print('Stop')
    motor = right_motor
    if direction == "left":
        motor = left_motor
    motor.Forward(90)
    utime.sleep(1.2)
    motor.Stop()
    

def line_following(timer):

    base_speed = 90   # This is a % of the max speed
    if config.lf:
        sensor_vals = read_sensors(digital)
        print(sensor_vals)

        pos, sum = centroid_position(sensor_vals, WEIGHTS)
                   
        if ((sensor_vals[0] == 1) or (sensor_vals[-1] == 1)):
            junction_detected = True

        if pos is None:
            pos = config.prev_pos
#            print("T Junction detected")


        e = -pos
        
        prev_pos = pos  # storing in case of T junction detected
        correction = pid.update(e)
#        print(correction)
        

        cmd_left = base_speed - correction
        cmd_right = base_speed + correction

        cmd_left = max(0, min(100, cmd_left))
        cmd_right = max(0, min(100, cmd_right))

        left_motor.Forward(cmd_left)
        right_motor.Forward(cmd_right)



def main():
    position = ('start', 'start')
    
    lf_timer = Timer(0, mode=Timer.PERIODIC, callback=line_following, freq=200)
    
    while not config.junction_detected:
        utime.sleep(0.005)
    config.junction_detected = False
    movement = to_and_fro[position]
    for junction in movement:
        while not config.junction_detected:
            utime.sleep(0.005)
        if path[junction][position] != "forward":
            config.lf = False
            turn(path[junction][position], right_motor, left_motor)
            config.lf = True
        config.junction_detected = False
        if ((junction == 'entrance_lower_b') or (junction == 'exit_lower_a')):
            for _ in range(5):
                while not config.junction_detected:
                    utime.sleep(0.005)
                config.junction_detected = False

main()
