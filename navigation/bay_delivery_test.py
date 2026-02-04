from machine import Pin, PWM, Timer
import utime
import config
from path import path as to_and_fro
from line_following import line_following
from junction_detection import junction_detecter
from motorController import Motor

path = {
    "start": {
        ("start", "bay_3"): "forward",
        ("lower_b", "start"): "forward",
        ("lower_a", "start"): "forward",
        ("upper_b", "start"): "forward",
        ("upper_a", "start"): "forward",
        ("start", "start"): "forward",
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
        ("bay_3", "lower_b"): "left",
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
    "entrance_lower_b2": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b3": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b4": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b5": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b6": {
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
    "entrance_lower_a2": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a3": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a4": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a5": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a6": {
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
    left_motor.Forward()
    right_motor.Forward()
    utime.sleep(0.25)
    right_motor.Stop()
    left_motor.Stop()
    if direction == "left":
        left_motor.Forward(config.BASE_SPEED)
        utime.sleep(0.8)
        while not (config.CENTER_LEFT_SENSOR.read_value()):
            utime.sleep(0.003)
        right_motor.Forward(config.BASE_SPEED)
    else:
        right_motor.Forward(config.BASE_SPEED)
        utime.sleep(1.2)
        while not (config.CENTER_LEFT_SENSOR.read_value() and config.CENTER_RIGHT_SENSOR.read_value()):
            utime.sleep(0.003)
        left_motor.Forward(config.BASE_SPEED)
    

def main():
    start_position = "start"
    button_pin = 14
    button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
    while not button.value():
        utime.sleep(0.003)
    left_motor = config.LEFT_MOTOR
    right_motor = config.RIGHT_MOTOR
    base_speed = config.BASE_SPEED

    left_motor.Forward(base_speed)
    right_motor.Forward(base_speed)
    print("START")

    Timer(mode=1, freq=200, callback=line_following)
    Timer(mode=1, freq=200, callback=junction_detecter)

    while not config.JUNCTION_DETECTED:
        utime.sleep(0.003)
    config.JUNCTION_DETECTED = False
    for bay in config.bays:
        for st in config.states:
            if st == "pre-pickup_move":
                position = (start_position, bay)
                movement = to_and_fro[position]
                for junction in movement:
                    while not config.JUNCTION_DETECTED:
                        utime.sleep(0.003)
                    config.LF = False
                    if path[junction][position] != "forward":
                        turn(path[junction][position], right_motor, left_motor)
                    else:
                        left_motor.Forward()
                        right_motor.Forward()
                        utime.sleep(0.2)
                    config.LF = True
                    config.JUNCTION_DETECTED = False
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
                config.JUNCTION_DETECTED = False
                right_motor.Stop()
                left_motor.Stop()
            elif (st == "pick_up_box"):
                left_motor.Reverse(config.BASE_SPEED)
                right_motor.Reverse(config.BASE_SPEED)
            elif st == "pre-delivery_move":
                position = (bay, "lower_b")
                movement = to_and_fro[position]
                for junction in movement:
                    while not config.JUNCTION_DETECTED:
                        utime.sleep(0.003)
                    config.LF = False
                    if path[junction][position] != "forward":
                        turn(path[junction][position], right_motor, left_motor)
                    else:
                        left_motor.Forward()
                        right_motor.Forward()
                        utime.sleep(0.2)
                    config.LF = True
                    config.JUNCTION_DETECTED = False
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
                turn("left", right_motor, left_motor)
                left_motor.Stop()
                right_motor.Stop()
                start_position = "lower_b"
            elif st == "deliver_box":
                left_motor.Reverse(config.BASE_SPEED)
                right_motor.Reverse(config.BASE_SPEED)
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
                turn("left", right_motor, left_motor)

main()
