from junction_info import junction_info as path
from path import path as to_and_fro
# from utime import sleep
from time import sleep
from turn import turn
import config
from motorController import Motor
from machine import Timer
from line_following import line_following

# print(path)

def path_finder(right_motor: Motor, left_motor: Motor, JUNCTION_DETECTED, bays: list[str], states: list[str], lf: Timer) -> None:
    start_position = 'start'
    delivery_position = 'test'
    right_motor.Forward(config.BASE_SPEED)
    left_motor.Forward(config.BASE_SPEED)
    while not JUNCTION_DETECTED:
        sleep(0.5)
    right_motor.Stop()
    left_motor.Stop()
    for bay in bays:
        print(bay)
        position = (start_position, bay)
        for st in states:
            if st == 'pre-pickup_move':
                movement = to_and_fro[position]
                for junction in movement:
                    config.LINE_FOLLOWING = True
                    # lf.init(mode=Timer.PERIODIC, callback=line_following, freq=500)
                    right_motor.Forward(config.BASE_SPEED)
                    left_motor.Forward(config.BASE_SPEED)
                    while not JUNCTION_DETECTED:
                        sleep(0.5)
                    JUNCTION_DETECTED = False
                    if path[junction][position] != "forward":
                        config.LINE_FOLLOWING = False
                        turn(path[junction][position], right_motor, left_motor)
            elif st == 'pick_up_box':
                config.LINE_FOLLOWING = False
                delivery_position = "Test"
                # delivery_position = pick_up_box()
                pass
            elif st == 'pre-delivery_move':
                # lf.init(mode=Timer.PERIODIC, callback=line_following, freq=500)
                config.LINE_FOLLOWING = True
                movement = to_and_fro[(bay, delivery_position)]
                for junction in movement:
                    right_motor.Forward(config.BASE_SPEED)
                    left_motor.Forward(config.BASE_SPEED)
                    while not JUNCTION_DETECTED:
                        sleep(0.5)
                    JUNCTION_DETECTED = False
                    if path[junction][position] != "forward":
                        # lf.deinit()
                        config.LINE_FOLLOWING = False
                        turn(path[junction][position], right_motor, left_motor)
            else:
                # lf.deinit()
                config.LINE_FOLLOWING = False
                start_position = 'test'
    position = ('lower_b', 'start')
    movement = to_and_fro[position]
    for junction in movement:
        # lf.init(mode=Timer.PERIODIC, callback=line_following, freq=500)
        config.LINE_FOLLOWING = True
        right_motor.Forward(config.BASE_SPEED)
        left_motor.Forward(config.BASE_SPEED)
        while not JUNCTION_DETECTED:
            sleep(0.5)
        JUNCTION_DETECTED = False
        if path[junction][position] != "forward":
            # lf.deinit()
            config.LINE_FOLLOWING = False
            turn(path[junction][position], right_motor, left_motor)
