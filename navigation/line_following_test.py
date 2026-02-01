from machine import Pin, PWM, Timer
import utime
import config
from line_following import line_following
from junction_detection import junction_detecter
from motorController import Motor

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

def turn(direction: str, right_motor: Motor, left_motor: Motor) -> None:
    right_motor.Stop()
    left_motor.Stop()
    if direction == "left":
        right_motor.Forward(config.BASE_SPEED)
        while not config.CENTER_LEFT_SENSOR:
            utime.sleep(0.003)
        left_motor.Forward(config.BASE_SPEED)
    else:
        left_motor.Forward(config.BASE_SPEED)
        while not config.CENTER_RIGHT_SENSOR:
            utime.sleep(0.003)
        right_motor.Forward(config.BASE_SPEED)
    

def main():
    position = ('start', 'start')
    
    left_motor = config.LEFT_MOTOR
    right_motor = config.RIGHT_MOTOR
    base_speed = config.BASE_SPEED

    left_motor.Forward(base_speed)
    right_motor.Forward(base_speed)

    lf_timer = Timer(0, mode=Timer.PERIODIC, callback=line_following, freq=200)
    jd_timer = Timer(1, mode=Timer.PERIODIC, callback=junction_detecter, freq=200)

    while not config.JUNCTION_DETECTED:
        utime.sleep(0.003)
    config.JUNCTION_DETECTED = False
    movement = to_and_fro[position]
    for junction in movement:
        while not config.JUNCTION_DETECTED:
            utime.sleep(0.003)
        if path[junction][position] != "forward":
            turn(path[junction][position], right_motor, left_motor)
        config.LF = True
        config.JUNCTION_DETECTED = False
        if ((junction == 'entrance_lower_b') or (junction == 'exit_lower_a')):
            for _ in range(5):
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
                config.JUNCTION_DETECTED = False

main()
