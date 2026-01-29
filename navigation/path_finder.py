from junction_info import junction_info as path
from path import path as to_and_fro
from utime import sleep
from turn import turn
states = [
    'pre-pickup_move',
    'pick_up_box',
    'pre-delivery_move',
    'deliver_box'
]

bays = [
    'bay_3',
    'bay_4',
    'bay_1',
    'bay_2',
]

def path_finder(right_motor, left_motor, junction_detected):
    start_position = 'start'
    delivery_position = 'test'
    while not junction_detected:
        right_motor.Forward(50)
        left_motor.Forward(50)
        sleep(0.05)
    right_motor.Stop()
    left_motor.Stop()
    junction_detected = False
    for bay in bays:
        position = (start_position, bay)
        for st in states:
            if st == 'pre-pickup_move':
                movement = to_and_fro[position]
                for junction in movement:
                    right_motor.Forward(50)
                    left_motor.Forward(50)
                    while not junction_detected:
                        sleep(0.05)
                    if path[junction][position] != "forward":
                        turn(path[junction][position], right_motor, left_motor)
                    junction_detected = False
            elif st == 'pick_up_box':
                delivery_position = "Test"
                # delivery_position = pick_up_box()
                pass
            elif st == 'pre-delivery_move':
                movement = to_and_fro[(bay, delivery_position)]
                for junction in movement:
                    right_motor.Forward(50)
                    left_motor.Forward(50)
                    while not junction_detected:
                        sleep(0.05)
                    if path[junction][position] != "forward":
                        turn(path[junction][position], right_motor, left_motor)
                    junction_detected = False
            else:
                start_position = 'test'
    position = (start_position, 'start')
    movement = to_and_fro[position]
    for junction in movement:
        right_motor.Forward(50)
        left_motor.Forward(50)
        while not junction_detected:
            sleep(0.05)
        if path[junction][position] != "forward":
            turn(path[junction][position], right_motor, left_motor)
        junction_detected = False
